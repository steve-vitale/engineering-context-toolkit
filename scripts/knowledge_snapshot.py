"""Read one operator-selected onboarding packet; source and workflow text remain data.

Standard library only. Three bounded reads, no source fetching, writes, workflow execution,
identity service or permission decisions. Derived states describe supplied source pins only.
"""
import argparse
import copy
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

MAX_INPUT_BYTES = 32 * 1024 * 1024
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
READ_CHUNK_BYTES = 65536
SDK_RESULT_ALLOWANCE = 4096
KINDS = ('source', 'landing', 'term', 'system_reference', 'role_reference', 'claim', 'workflow', 'practice')
REASON_ORDER = ('selected_basis_changed', 'original_fingerprint_unavailable', 'capture_not_supplied', 'no_evidence_declared')
NEXT_REVIEW = 'Review the supplied source basis and record any decision in the existing company process.'
_MESSAGES = {'invalid_packet': 'Invalid onboarding packet.', 'invalid_selection': 'Invalid component selection.',
             'invalid_argument': 'Invalid onboarding request.', 'unknown_record': 'Unknown onboarding record.',
             'result_too_large': 'Onboarding result exceeds 2 MiB.'}
_MISSING = object()


class OnboardingError(ValueError):
    """A bounded public diagnostic; neither message nor repr contains supplied values."""
    def __init__(self, code, reason, path=None):
        self.code, self.reason, self.path = code, reason, path
        super().__init__(_MESSAGES[code])

    def as_dict(self):
        return dict(code=self.code, reason=self.reason, path=self.path, message=str(self))


def _fail(reason, path=None, code='invalid_packet'):
    raise OnboardingError(code, reason, path) from None


def _pointer(value):
    return value.replace('~', '~0').replace('/', '~1')


def _text(value, path, *, identity=False, blank=False):
    if type(value) is not str:
        _fail('invalid_type', path)
    try:
        value.encode('utf-8', 'strict')
    except UnicodeError:
        _fail('invalid_utf8')
    if not blank and not value.strip():
        _fail('invalid_schema', path)
    if identity and (not value or value != value.strip()):
        _fail('invalid_schema', path)


def _object(value, path, required, optional=()):
    if type(value) is not dict:
        _fail('invalid_type', path)
    if any(type(k) is not str for k in value) or set(value) - set(required) - set(optional) or set(required) - set(value):
        _fail('invalid_schema', path)


def _array(value, path, *, minimum=0):
    if type(value) is not list:
        _fail('invalid_type', path)
    if len(value) < minimum:
        _fail('invalid_schema', path)


def _texts(value, path, *, identities=False, minimum=0, unique=False):
    _array(value, path, minimum=minimum)
    for i, item in enumerate(value):
        _text(item, path + '/' + str(i), identity=identities)
    if unique and len(set(value)) != len(value):
        _fail('invalid_schema', path)


def _enum(value, choices, path):
    _text(value, path)
    if value not in choices:
        _fail('invalid_schema', path)


def _hash(value, path, *, nullable=False):
    if nullable and value is None:
        return
    _text(value, path)
    if re.fullmatch('[0-9a-f]{64}', value) is None:
        _fail('invalid_schema', path)


def _size(value, path, maximum=9223372036854775807):
    if type(value) is not int:
        _fail('invalid_type', path)
    if not 0 <= value <= maximum:
        _fail('invalid_schema', path)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail('invalid_json')
        result[key] = value
    return result


def _constant(_value):
    _fail('invalid_json')


def read_bounded(stream):
    """Return complete exact bytes up to cap+1; short reads are not EOF."""
    parts, size = [], 0
    while size < MAX_INPUT_BYTES + 1:
        block = stream.read(min(READ_CHUNK_BYTES, MAX_INPUT_BYTES + 1 - size))
        if not block:
            break
        parts.append(block)
        size += len(block)
    if size > MAX_INPUT_BYTES:
        _fail('input_too_large')
    return b''.join(parts)


def read_packet(path):
    try:
        with Path(path).open('rb') as stream:
            raw = read_bounded(stream)
    except OSError:
        _fail('input_unavailable')
    return decode_packet(raw), hashlib.sha256(raw).hexdigest()


def decode_packet(raw):
    if type(raw) is not bytes:
        _fail('invalid_type')
    if len(raw) > MAX_INPUT_BYTES:
        _fail('input_too_large')
    try:
        text = raw.decode('utf-8', 'strict')
    except UnicodeError:
        _fail('invalid_utf8')
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
        # Reject decoded surrogates and number overflow before building indexes.
        json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf-8', 'strict')
    except UnicodeError:
        _fail('invalid_utf8')
    except (ValueError, RecursionError, OverflowError):
        _fail('invalid_json')
    return value


def _review(value, path):
    _object(value, path, ('state', 'reviewer_role', 'reviewed_on'))
    _enum(value['state'], ('unreviewed', 'proposed', 'source_matched', 'rejected', 'disputed'), path + '/state')
    role, day = value['reviewer_role'], value['reviewed_on']
    if role is not None:
        _text(role, path + '/reviewer_role', identity=True)
    if day is not None:
        if type(day) is not str:
            _fail('invalid_type', path + '/reviewed_on')
        try:
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', day) is None:
                raise ValueError
            date.fromisoformat(day)
        except ValueError:
            _fail('invalid_date', path + '/reviewed_on')
    if (role is None) != (day is None) or (value['state'] in ('source_matched', 'rejected', 'disputed') and role is None):
        _fail('invalid_schema', path)


def _source(d, path):
    fields = ('document_id', 'source_revision', 'original_reference', 'original_raw_sha256', 'original_size_bytes',
              'capture_kind', 'capture_sha256', 'captured_text', 'capture_complete', 'acquisition_time',
              'original_reverified_at_runtime', 'source_authority')
    _object(d, path, fields, ('original_status', 'capture_size_bytes'))
    def profile(check, value, field, **kwargs):
        try:
            check(value, path + '/' + field, **kwargs)
        except OnboardingError as exc:
            if exc.reason == 'invalid_utf8':
                raise
            _fail('source_profile_mismatch', path + '/' + field)
    _text(d['document_id'], path + '/document_id', identity=True)
    for key in ('source_revision', 'source_authority'):
        _text(d[key], path + '/' + key)
    if d['original_reference'] is not None:
        profile(_text, d['original_reference'], 'original_reference')
    kind = d['capture_kind']
    if type(kind) is not str or kind not in ('complete-utf8-text', 'excerpt-utf8-text', 'reference-only'):
        _fail('source_profile_mismatch', path + '/capture_kind')
    if d['original_reverified_at_runtime'] is not False:
        _fail('source_profile_mismatch', path + '/original_reverified_at_runtime')
    stamp = d['acquisition_time']
    if stamp is not None:
        if type(stamp) is not str:
            _fail('invalid_type', path + '/acquisition_time')
        try:
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', stamp) is None:
                raise ValueError
            datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        except ValueError:
            _fail('invalid_date', path + '/acquisition_time')
    status = d.get('original_status', 'fingerprint_supplied')
    allowed = ('fingerprint_supplied',) if kind == 'complete-utf8-text' else ('unavailable', 'declared_not_reverified')
    if type(status) is not str or status not in allowed:
        _fail('source_profile_mismatch', path + '/original_status')
    if kind != 'complete-utf8-text' and not {'original_status', 'capture_size_bytes'} <= set(d):
        _fail('invalid_schema', path)
    for key in ('original_raw_sha256', 'original_size_bytes'):
        value = d[key]
        if (value is None) != (status == 'unavailable'):
            _fail('source_profile_mismatch', path + '/' + key)
    if status != 'unavailable':
        profile(_hash, d['original_raw_sha256'], 'original_raw_sha256')
        profile(_size, d['original_size_bytes'], 'original_size_bytes')
    complete = kind == 'complete-utf8-text'
    if d['capture_complete'] is not complete:
        _fail('source_profile_mismatch', path + '/capture_complete')
    if kind == 'reference-only':
        for key in ('capture_sha256', 'captured_text', 'capture_size_bytes'):
            if d[key] is not None:
                _fail('source_profile_mismatch', path + '/' + key)
        return
    profile(_text, d['captured_text'], 'captured_text', blank=True)
    if kind == 'excerpt-utf8-text' and not d['captured_text']:
        _fail('source_profile_mismatch', path + '/captured_text')
    profile(_hash, d['capture_sha256'], 'capture_sha256')
    raw = d['captured_text'].encode('utf-8')
    if hashlib.sha256(raw).hexdigest() != d['capture_sha256']:
        _fail('capture_mismatch', path + '/capture_sha256')
    if complete and d['capture_sha256'] != d['original_raw_sha256']:
        _fail('capture_mismatch', path + '/capture_sha256')
    if 'capture_size_bytes' in d:
        profile(_size, d['capture_size_bytes'], 'capture_size_bytes', maximum=MAX_INPUT_BYTES)
        if len(raw) != d['capture_size_bytes']:
            _fail('capture_mismatch', path + '/capture_size_bytes')
    if complete and len(raw) != d['original_size_bytes']:
        _fail('capture_mismatch', path + '/original_size_bytes')


def _body(kind, d, path):
    required = {
        'landing': ('start_here', 'leader_preparation', 'new_engineer_outcome'),
        'term': ('definition',),
        'system_reference': ('reference', 'availability', 'purpose', 'source_access'),
        'role_reference': ('responsibility', 'authenticated_identity', 'assignment_authority'),
        'claim': ('basis', 'statement'),
        'workflow': ('purpose', 'prerequisites', 'steps', 'stop_or_review_conditions', 'review_handoff', 'execution'),
        'practice': ('purpose', 'exercise_scope', 'inputs', 'expected_draft_fields', 'reviewer_role', 'excluded_real_work', 'completion_tracking')}
    if kind == 'source':
        _source(d, path)
        return
    _object(d, path, required[kind], ('interpretation_limit', 'attribution', 'underlying_claim_verified') if kind == 'claim' else ())
    if kind == 'landing':
        _array(d['start_here'], path + '/start_here', minimum=1)
        for i, item in enumerate(d['start_here']):
            p = path + '/start_here/' + str(i)
            _object(item, p, ('record_id', 'reason'))
            _text(item['record_id'], p + '/record_id', identity=True)
            _text(item['reason'], p + '/reason')
        _texts(d['leader_preparation'], path + '/leader_preparation')
        _text(d['new_engineer_outcome'], path + '/new_engineer_outcome')
    elif kind == 'term':
        _text(d['definition'], path + '/definition')
    elif kind == 'system_reference':
        for key in ('reference', 'purpose', 'source_access'):
            _text(d[key], path + '/' + key)
        _enum(d['availability'], ('not_connected', 'reference_only', 'unknown'), path + '/availability')
    elif kind == 'role_reference':
        for key in ('responsibility', 'assignment_authority'):
            _text(d[key], path + '/' + key)
        if d['authenticated_identity'] is not None:
            _fail('invalid_schema', path + '/authenticated_identity')
    elif kind == 'claim':
        _enum(d['basis'], ('cited_record', 'interpretation', 'attributed_memory', 'unknown'), path + '/basis')
        _text(d['statement'], path + '/statement')
        if 'interpretation_limit' in d:
            _text(d['interpretation_limit'], path + '/interpretation_limit')
        if d['basis'] == 'attributed_memory':
            if 'attribution' not in d or 'underlying_claim_verified' not in d:
                _fail('invalid_schema', path)
            _text(d['attribution'], path + '/attribution')
            if d['underlying_claim_verified'] is not False:
                _fail('memory_contradiction', path + '/underlying_claim_verified')
        elif 'attribution' in d or 'underlying_claim_verified' in d:
            _fail('invalid_schema', path)
    elif kind == 'workflow':
        _text(d['purpose'], path + '/purpose')
        _texts(d['prerequisites'], path + '/prerequisites', identities=True, unique=True)
        _array(d['steps'], path + '/steps', minimum=1)
        for i, step in enumerate(d['steps']):
            p = path + '/steps/' + str(i)
            _object(step, p, ('id', 'description', 'inputs', 'draft_output'))
            _text(step['id'], p + '/id', identity=True)
            for key in ('description', 'draft_output'):
                _text(step[key], p + '/' + key)
            _texts(step['inputs'], p + '/inputs', identities=True, unique=True)
        _texts(d['stop_or_review_conditions'], path + '/stop_or_review_conditions')
        h = d['review_handoff'];p = path + '/review_handoff'
        _object(h, p, ('reviewer_role', 'system_reference', 'deliverables', 'acceptance'))
        for key in ('reviewer_role', 'system_reference'):
            _text(h[key], p + '/' + key, identity=True)
        _texts(h['deliverables'], p + '/deliverables', minimum=1)
        _text(h['acceptance'], p + '/acceptance')
        _enum(d['execution'], ('template_data_only',), path + '/execution')
    elif kind == 'practice':
        for key in ('purpose', 'exercise_scope', 'completion_tracking'):
            _text(d[key], path + '/' + key)
        _texts(d['inputs'], path + '/inputs', identities=True, unique=True)
        _texts(d['expected_draft_fields'], path + '/expected_draft_fields', minimum=1)
        _text(d['reviewer_role'], path + '/reviewer_role', identity=True)
        _texts(d['excluded_real_work'], path + '/excluded_real_work')


def validate_packet(packet):
    """Validate all closed fields and exact typed links before building a readable view."""
    _object(packet, '', ('schema', 'packet_id', 'revision', 'scope', 'title', 'landing_record_id', 'selected_sources', 'records'), ('companion_bindings',))
    _enum(packet['schema'], ('engineering-onboarding-1',), '/schema')
    for key in ('packet_id', 'landing_record_id'):
        _text(packet[key], '/' + key, identity=True)
    for key in ('revision', 'scope', 'title'):
        _text(packet[key], '/' + key)
    _object(packet['selected_sources'], '/selected_sources', (), tuple(packet['selected_sources']) if type(packet['selected_sources']) is dict else ())
    for key, value in packet['selected_sources'].items():
        _text(key, '/selected_sources', identity=True)
        _text(value, '/selected_sources/' + _pointer(key), identity=True)
    _array(packet['records'], '/records', minimum=1)
    for i, r in enumerate(packet['records']):
        p = '/records/' + str(i)
        _object(r, p, ('id', 'kind', 'title', 'summary', 'aliases', 'revision', 'record_state', 'audience_hints', 'owner_roles', 'review', 'evidence', 'depends_on', 'known_unknowns', 'data'))
        _text(r['id'], p + '/id', identity=True)
        _enum(r['kind'], KINDS, p + '/kind')
        for key in ('title', 'summary', 'revision'):
            _text(r[key], p + '/' + key)
        for key in ('aliases', 'audience_hints', 'known_unknowns'):
            _texts(r[key], p + '/' + key)
        for key in ('owner_roles', 'depends_on'):
            _texts(r[key], p + '/' + key, identities=True, unique=True)
        _enum(r['record_state'], ('example', 'draft', 'proposed', 'superseded', 'withdrawn'), p + '/record_state')
        _review(r['review'], p + '/review')
        _array(r['evidence'], p + '/evidence')
        for j, e in enumerate(r['evidence']):
            ep = p + '/evidence/' + str(j)
            _object(e, ep, ('source_record_id', 'document_id', 'revision', 'raw_sha256', 'locator', 'currency_requirement'), ('capture_sha256',))
            for key in ('source_record_id', 'document_id'):
                _text(e[key], ep + '/' + key, identity=True)
            for key in ('revision', 'locator'):
                _text(e[key], ep + '/' + key)
            _hash(e['raw_sha256'], ep + '/raw_sha256', nullable=True)
            if 'capture_sha256' in e:
                _hash(e['capture_sha256'], ep + '/capture_sha256', nullable=True)
            _enum(e['currency_requirement'], ('snapshot_evidence', 'selected_basis'), ep + '/currency_requirement')
        _body(r['kind'], r['data'], p + '/data')
        if r['kind'] == 'claim' and r['data']['basis'] != 'unknown' and not r['evidence']:
            _fail('invalid_schema', p + '/evidence')
    # All local constraints precede the shared record/step identity stage.
    bindings = packet.get('companion_bindings', {})
    _object(bindings, '/companion_bindings', (), ('graph', 'context'))
    for role, binding in bindings.items():
        p = '/companion_bindings/' + role;_object(binding, p, ('schema', 'raw_sha256'))
        _text(binding['schema'], p + '/schema');_hash(binding['raw_sha256'], p + '/raw_sha256')
    index = {}
    for i, r in enumerate(packet['records']):
        p = '/records/' + str(i)
        if r['id'] in index:
            _fail('duplicate_record_id', p + '/id')
        index[r['id']] = r
        if r['kind'] == 'workflow':
            seen = set()
            for j, step in enumerate(r['data']['steps']):
                if step['id'] in seen:
                    _fail('duplicate_step_id', p + '/data/steps/' + str(j) + '/id')
                seen.add(step['id'])
    def fk(value, kinds, path):
        if value not in index:
            _fail('unknown_reference', path)
        if index[value]['kind'] not in kinds:
            _fail('wrong_reference_kind', path)
    fk(packet['landing_record_id'], ('landing',), '/landing_record_id')
    for i, r in enumerate(packet['records']):
        p = '/records/' + str(i);d = r['data']
        for j, value in enumerate(r['owner_roles']):fk(value, ('role_reference',), p + '/owner_roles/' + str(j))
        if r['review']['reviewer_role'] is not None:fk(r['review']['reviewer_role'], ('role_reference',), p + '/review/reviewer_role')
        for j, value in enumerate(r['depends_on']):fk(value, KINDS, p + '/depends_on/' + str(j))
        for j, e in enumerate(r['evidence']):fk(e['source_record_id'], ('source',), p + '/evidence/' + str(j) + '/source_record_id')
        if r['kind'] == 'landing':
            for j, item in enumerate(d['start_here']):fk(item['record_id'], KINDS, p + '/data/start_here/' + str(j) + '/record_id')
        if r['kind'] == 'workflow':
            for j, value in enumerate(d['prerequisites']):fk(value, KINDS, p + '/data/prerequisites/' + str(j))
            for j, step in enumerate(d['steps']):
                for k, value in enumerate(step['inputs']):fk(value, KINDS, p + '/data/steps/' + str(j) + '/inputs/' + str(k))
            fk(d['review_handoff']['reviewer_role'], ('role_reference',), p + '/data/review_handoff/reviewer_role')
            fk(d['review_handoff']['system_reference'], ('system_reference',), p + '/data/review_handoff/system_reference')
        if r['kind'] == 'practice':
            for j, value in enumerate(d['inputs']):fk(value, KINDS, p + '/data/inputs/' + str(j))
            fk(d['reviewer_role'], ('role_reference',), p + '/data/reviewer_role')
    for i, r in enumerate(packet['records']):
        for j, e in enumerate(r['evidence']):
            sd = index[e['source_record_id']]['data'];p = '/records/' + str(i) + '/evidence/' + str(j)
            for key, skey in (('document_id','document_id'), ('revision','source_revision'), ('raw_sha256','original_raw_sha256')):
                if e[key] != sd[skey]:_fail('citation_mismatch', p + '/' + key)
            if 'capture_sha256' in e and e['capture_sha256'] != sd['capture_sha256']:
                _fail('citation_mismatch', p + '/capture_sha256')
            if sd['capture_kind'] != 'complete-utf8-text' and 'capture_sha256' not in e:
                _fail('invalid_schema', p)
    for doc, value in packet['selected_sources'].items():
        p = '/selected_sources/' + _pointer(doc);fk(value, ('source',), p)
        if index[value]['data']['document_id'] != doc:_fail('selected_document_mismatch', p)
    for i, r in enumerate(packet['records']):
        for j, e in enumerate(r['evidence']):
            if e['currency_requirement'] == 'selected_basis' and e['document_id'] not in packet['selected_sources']:
                _fail('missing_selected_basis', '/records/' + str(i) + '/evidence/' + str(j) + '/document_id')
    # Iterative DFS keeps deep valid dependency chains out of the Python call stack.
    colors = {}
    positions = {r['id']:i for i,r in enumerate(packet['records'])}
    for first in index:
        if colors.get(first):continue
        colors[first] = 1;stack = [(first, iter(enumerate(index[first]['depends_on'])))]
        while stack:
            current, edges = stack[-1]
            try:j, target = next(edges)
            except StopIteration:colors[current] = 2;stack.pop();continue
            if colors.get(target) == 1:
                _fail('dependency_cycle', '/records/' + str(positions[current]) + '/depends_on/' + str(j))
            if not colors.get(target):
                colors[target] = 1;stack.append((target, iter(enumerate(index[target]['depends_on']))))
    return index


def selection_digest(components):
    preimage = dict(domain='engineering-onboarding-selection', version=1, components=components)
    raw = json.dumps(preimage, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
    return preimage, hashlib.sha256(raw).hexdigest()


def _basis_diagnostics(packet, index):
    selected = packet['selected_sources'];all_d = {}
    for i, r in enumerate(packet['records']):
        d = dict(basis_state='matches', basis_reasons=[], evidence=[], dependency_state='not_declared',
                 dependency_reasons=[], basis_review_notice='none', next_review_step=None, source_capture=None)
        states = []
        def reason(code, path, source_id, selected_id):
            d['basis_reasons'].append(dict(code=code,path=path,source_record_id=source_id,selected_source_record_id=selected_id))
        if r['kind'] == 'source':
            sd=r['data'];sid=selected.get(sd['document_id']);state='unknown' if sd['original_raw_sha256'] is None else 'matches';states.append(state)
            d['source_capture']=dict(capture_kind=sd['capture_kind'],capture_integrity='not_supplied' if sd['capture_kind']=='reference-only' else 'matches',capture_complete=sd['capture_complete'],original_status=sd.get('original_status','fingerprint_supplied'),original_verified=False)
            if sd['original_raw_sha256'] is None:reason('original_fingerprint_unavailable',f'/records/{i}/data/original_raw_sha256',r['id'],sid)
            if sd['capture_kind']=='reference-only':reason('capture_not_supplied',f'/records/{i}/data/capture_sha256',r['id'],sid)
        for j,e in enumerate(r['evidence']):
            p=f'/records/{i}/evidence/{j}';sd=index[e['source_record_id']]['data'];sid=selected.get(e['document_id']);codes=[]
            if e['currency_requirement']=='selected_basis' and e['source_record_id']!=sid:
                codes.append('selected_basis_changed');reason(codes[-1],p+'/source_record_id',e['source_record_id'],sid)
            if e['raw_sha256'] is None:
                codes.append('original_fingerprint_unavailable');reason(codes[-1],p+'/raw_sha256',e['source_record_id'],sid)
            if sd['capture_kind']=='reference-only':
                codes.append('capture_not_supplied');reason(codes[-1],p+'/capture_sha256',e['source_record_id'],sid)
            state='stale' if 'selected_basis_changed' in codes else 'unknown' if codes else 'matches';states.append(state)
            d['evidence'].append(dict(evidence_path=p,source_record_id=e['source_record_id'],document_id=e['document_id'],pinned_revision=e['revision'],pinned_raw_sha256=e['raw_sha256'],selected_source_record_id=sid,state=state,reason_codes=codes))
        if not states:
            states=['unknown'];reason('no_evidence_declared',f'/records/{i}/evidence',None,None)
        d['basis_state']=next(s for s in ('stale','unknown','matches') if s in states);all_d[r['id']]=d
    return all_d


def _record_diagnostics(rid, index, basis):
    """Expand one complete record's paths without retaining every root's expanded paths."""
    r=index[rid];d=copy.deepcopy(basis[rid])
    if r['depends_on']:
        # Breadth-first, sorted neighbors => first path is shortest with lexical tie-break.
        paths={};frontier=[(rid,)];seen={rid}
        while frontier:
            following=[]
            for path in sorted(frontier):
                for target in sorted(index[path[-1]]['depends_on']):
                    if target in seen:continue
                    seen.add(target);new=path+(target,);paths[target]=new;following.append(new)
            frontier=following
        for target,path in sorted(paths.items(),key=lambda item:item[1]):
            td=basis[target]
            if td['basis_state']!='matches':
                codes=[code for code in REASON_ORDER if any(x['code']==code for x in td['basis_reasons'])]
                d['dependency_reasons'].append(dict(path=list(path),basis_state=td['basis_state'],reason_codes=codes))
        d['dependency_state']='needs_review' if d['dependency_reasons'] else 'matches'
    if d['basis_state']!='matches' or d['dependency_state']=='needs_review':
        d['basis_review_notice']='review_supplied_basis';d['next_review_step']=NEXT_REVIEW
    return d


class KnowledgeSnapshot:
    """One validated startup selection. All responses deep-copy its selected data."""
    def __init__(self, path, *, components=None, loaded_at=None):
        packet,digest=read_packet(path)
        self._index=validate_packet(packet)
        self._packet=packet;self.digest=digest
        chosen={'knowledge':dict(schema=packet['schema'],raw_sha256=digest)}
        if components is not None:
            if type(components) is not dict or any(type(k) is not str or k not in ('knowledge','graph','context') for k in components):
                _fail('invalid_schema',code='invalid_selection')
            for role,value in components.items():
                if type(value) is not dict or any(type(k) is not str for k in value) or set(value)!= {'schema','raw_sha256'} or any(type(v) is not str for v in value.values()):
                    _fail('invalid_schema',code='invalid_selection')
                expected={'knowledge':'engineering-onboarding-1','graph':'twin-graph-1','context':'context-register-1'}[role]
                if value['schema']!=expected or re.fullmatch('[0-9a-f]{64}',value['raw_sha256']) is None:
                    _fail('invalid_schema',code='invalid_selection')
                if role=='knowledge' and value!=chosen['knowledge']:_fail('companion_mismatch',code='invalid_selection')
                chosen[role]=copy.deepcopy(value)
        if 'context' in chosen and 'graph' not in chosen:_fail('missing_required_companion',code='invalid_selection')
        for role,binding in packet.get('companion_bindings',{}).items():
            if role not in chosen:_fail('missing_required_companion',code='invalid_selection')
            if chosen[role]!=binding:_fail('companion_mismatch',code='invalid_selection')
        self._selection,self.selection_sha256=selection_digest(chosen)
        if loaded_at is not None:
            _text(loaded_at, None)
            try:
                if re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+00:00', loaded_at) is None:
                    raise ValueError
                datetime.fromisoformat(loaded_at)
            except ValueError:
                _fail('invalid_date')
        self.loaded_at=loaded_at if loaded_at is not None else datetime.now(timezone.utc).isoformat(timespec='microseconds')
        self._basis_diagnostics=_basis_diagnostics(packet,self._index)
        self._summaries=[]
        for r in sorted(packet['records'],key=lambda r:r['id']):
            d=_record_diagnostics(r['id'],self._index,self._basis_diagnostics)
            # Admit every complete record response before publishing any catalogue. Expanded paths live
            # for this record only; per-request reads reconstruct the same complete diagnostics.
            self._response(dict(record=r,diagnostics=d))
            row={k:copy.deepcopy(r[k]) for k in ('id','kind','title','summary','aliases','revision','record_state','audience_hints','owner_roles')}
            row.update(review_state=r['review']['state'],basis_state=d['basis_state'],dependency_state=d['dependency_state'],basis_review_notice=d['basis_review_notice']);self._summaries.append(row)
            del d
        # No partial catalogue is published if any complete record cannot be read.
        self.onboarding_overview()
        self.list_onboarding_records(limit=1)

    def _response(self,result):
        payload=dict(knowledge_sha256=self.digest,selection_sha256=self.selection_sha256,loaded_at=self.loaded_at,
                     live=False,source_currency='selected_snapshot_only',reference_data_only=True,result=result)
        encoded=json.dumps(payload,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode('utf-8')
        if len(encoded)>MAX_RESPONSE_BYTES:_fail('result_too_large',code='result_too_large')
        return copy.deepcopy(payload)

    def onboarding_overview(self,**extra):
        if extra:_fail('invalid_schema','',code='invalid_argument')
        p=self._packet
        return self._response(dict(schema='engineering-onboarding-overview-1',packet={k:p[k] for k in ('schema','packet_id','revision','scope','title')},
            landing_record=self._index[p['landing_record_id']],landing_diagnostics=_record_diagnostics(p['landing_record_id'],self._index,self._basis_diagnostics),record_count=len(self._index),
            counts_by_kind={k:sum(r['kind']==k for r in p['records']) for k in KINDS},selected_sources=p['selected_sources'],selection=self._selection,
            capabilities=dict(read_only=True,workflow_execution=False,decision_acceptance=False,authorization='external')))

    def list_onboarding_records(self,kind='',query='',limit=20,offset=0,**extra):
        if extra:_fail('invalid_schema','',code='invalid_argument')
        if type(kind) is not str or kind not in ('',)+KINDS:_fail('invalid_kind','/kind',code='invalid_argument')
        if type(query) is not str:_fail('invalid_query','/query',code='invalid_argument')
        try:query.encode('utf-8')
        except UnicodeError:_fail('invalid_query','/query',code='invalid_argument')
        if len(query.strip())>200:_fail('invalid_query','/query',code='invalid_argument')
        if type(limit) is not int or not 1<=limit<=50:_fail('invalid_limit','/limit',code='invalid_argument')
        if type(offset) is not int or not 0<=offset<=9223372036854775807:_fail('invalid_offset','/offset',code='invalid_argument')
        q=query.strip().casefold()
        found=[r for r in self._summaries if (not kind or r['kind']==kind) and any(q in v.casefold() for v in [r['id'],r['title'],r['summary']]+r['aliases']+r['audience_hints'])]
        total=len(found)
        if offset>total or offset==total and total>0:_fail('invalid_offset','/offset',code='invalid_argument')
        end=min(offset+limit,total)
        return self._response(dict(total=total,offset=offset,limit=limit,next_offset=end if end<total else None,truncated=offset>0 or end<total,records=found[offset:end]))

    def get_onboarding_record(self,record_id=_MISSING,**extra):
        if extra or record_id is _MISSING:_fail('invalid_schema','',code='invalid_argument')
        if type(record_id) is not str or not record_id:_fail('invalid_type','/record_id',code='invalid_argument')
        try:record_id.encode('utf-8')
        except UnicodeError:_fail('invalid_type','/record_id',code='invalid_argument')
        if record_id not in self._index:_fail('unknown_record','/record_id',code='unknown_record')
        return self._response(dict(record=self._index[record_id],diagnostics=_record_diagnostics(record_id,self._index,self._basis_diagnostics)))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--knowledge',type=Path,required=True)
    parser.add_argument('action',choices=('overview','list','get'))
    parser.add_argument('--record-id');parser.add_argument('--kind',default='');parser.add_argument('--query',default='')
    parser.add_argument('--limit',type=int,default=20);parser.add_argument('--offset',type=int,default=0)
    args=parser.parse_args(argv)
    try:
        packet=KnowledgeSnapshot(args.knowledge)
        if args.action=='overview':result=packet.onboarding_overview()
        elif args.action=='list':result=packet.list_onboarding_records(args.kind,args.query,args.limit,args.offset)
        else:result=packet.get_onboarding_record(args.record_id)
    except OnboardingError as exc:
        print(json.dumps(exc.as_dict(),ensure_ascii=False),file=sys.stderr);return 2
    sys.stdout.write(json.dumps(result,ensure_ascii=False,allow_nan=False,separators=(',',':')));return 0


if __name__=='__main__':
    raise SystemExit(main())
