"""Capture permitted UTF-8 records and authored contributions into a new local knowledge revision.

Standard library only. Never overwrites inputs, fetches documents, interprets source prose,
accepts decisions or writes through MCP. The existing snapshot reader remains read-only.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

import knowledge_snapshot as knowledge


class CaptureError(ValueError):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + '\n').encode('utf-8')


def fields(value, required, optional=()):
    if type(value) is not dict or set(value) - set(required) - set(optional) or set(required) - set(value):
        raise CaptureError('Unexpected or missing change fields.')


def text(value):
    if type(value) is not str or not value.strip():
        raise CaptureError('Expected a nonempty text value.')


def read_raw(path):
    with Path(path).open('rb') as stream:
        return knowledge.read_bounded(stream)


def record(rid, kind, title, summary, revision, data, *, evidence=None, depends_on=None,
           known_unknowns=None, owner_roles=None):
    return dict(id=rid, kind=kind, title=title, summary=summary, aliases=[], revision=revision,
                record_state='proposed', audience_hints=[], owner_roles=owner_roles or [],
                review=dict(state='unreviewed', reviewer_role=None, reviewed_on=None),
                evidence=evidence or [], depends_on=depends_on or [],
                known_unknowns=known_unknowns or [], data=data)


def prepare(before_raw, change_raw, source_files, *, captured_at=None):
    """Build all output bytes before creating a destination; supplied records stay immutable."""
    before = knowledge.decode_packet(before_raw)
    old_index = knowledge.validate_packet(before)
    if before.get('companion_bindings'):
        raise CaptureError('Use an unbound knowledge-only packet; companion reconciliation is separate.')
    change = knowledge.decode_packet(change_raw)
    fields(change, ('schema', 'base_sha256', 'revision', 'contributor', 'reason', 'new_sources',
                    'claims', 'select_sources'))
    if change['schema'] != 'knowledge-capture-1' or change['base_sha256'] != digest(before_raw):
        raise CaptureError('Change schema or exact base fingerprint does not match.')
    for key in ('revision', 'contributor', 'reason'):
        text(change[key])
    if change['revision'] == before['revision']:
        raise CaptureError('Choose a new packet revision.')
    if type(change['new_sources']) is not list or type(change['claims']) is not list or type(change['select_sources']) is not dict:
        raise CaptureError('Invalid change collection.')
    source_ids = []
    for source in change['new_sources']:
        fields(source, ('id', 'document_id', 'source_revision', 'title', 'source_authority', 'original_reference'))
        for value in source.values():
            text(value)
        source_ids.append(source['id'])
    if len(set(source_ids)) != len(source_ids) or set(source_files) != set(source_ids):
        raise CaptureError('Supply exactly one explicit --source ID FILE for each new source.')
    stamp = captured_at or datetime.now(timezone.utc).isoformat(timespec='microseconds')
    after = copy.deepcopy(before)
    after['revision'] = change['revision']
    captured = []
    for source in change['new_sources']:
        raw = read_raw(source_files[source['id']])
        try:
            content = raw.decode('utf-8', 'strict')
        except UnicodeError:
            raise CaptureError('A supplied source is not UTF-8 text.') from None
        sha = digest(raw)
        data = dict(document_id=source['document_id'], source_revision=source['source_revision'],
                    original_reference=source['original_reference'], original_raw_sha256=sha,
                    original_size_bytes=len(raw), capture_kind='complete-utf8-text', capture_sha256=sha,
                    captured_text=content, capture_complete=True, acquisition_time=stamp,
                    original_reverified_at_runtime=False, source_authority=source['source_authority'])
        after['records'].append(record(source['id'], 'source', source['title'],
                                       'Operator-supplied complete UTF-8 source; authority is a declaration.', '1', data))
        captured.append(dict(record_id=source['id'], raw_sha256=sha, size_bytes=len(raw)))
    after['selected_sources'].update(change['select_sources'])
    index = {r['id']: r for r in after['records']}
    for claim in change['claims']:
        fields(claim, ('id', 'title', 'summary', 'basis', 'statement', 'evidence', 'depends_on',
                       'known_unknowns', 'owner_roles'), ('interpretation_limit', 'attribution'))
        if any(type(claim[key]) is not list for key in ('evidence', 'depends_on', 'known_unknowns', 'owner_roles')):
            raise CaptureError('Invalid claim evidence, dependencies, unknowns or owners.')
        evidence = []
        for e in claim['evidence']:
            fields(e, ('source_record_id', 'locator', 'currency_requirement'))
            sid = e['source_record_id']
            if type(sid) is not str or sid not in index or index[sid]['kind'] != 'source':
                raise CaptureError('Claim cites an unknown source record.')
            d = index[sid]['data']
            evidence.append(dict(source_record_id=sid, document_id=d['document_id'],
                                 revision=d['source_revision'], raw_sha256=d['original_raw_sha256'],
                                 capture_sha256=d['capture_sha256'], locator=e['locator'],
                                 currency_requirement=e['currency_requirement']))
        data = dict(basis=claim['basis'], statement=claim['statement'])
        if 'interpretation_limit' in claim:
            data['interpretation_limit'] = claim['interpretation_limit']
        if 'attribution' in claim:
            data.update(attribution=claim['attribution'], underlying_claim_verified=False)
        # Every declared source citation is also a dependency. Other semantic links must be authored.
        dependencies = list(claim['depends_on'])
        for e in evidence:
            if e['source_record_id'] not in dependencies:
                dependencies.append(e['source_record_id'])
        after['records'].append(record(claim['id'], 'claim', claim['title'], claim['summary'], '1', data,
                                       evidence=evidence, depends_on=dependencies,
                                       known_unknowns=claim['known_unknowns'], owner_roles=claim['owner_roles']))
    new_index = knowledge.validate_packet(after)
    if not change['new_sources'] and not change['claims'] and before['selected_sources'] == after['selected_sources']:
        raise CaptureError('No records or source selections changed.')
    after_raw = encoded(after)
    if len(after_raw) > knowledge.MAX_INPUT_BYTES:
        raise CaptureError('Result exceeds the 32 MiB packet limit.')
    # Apply the actual reader's full-record/response admission, not only its schema check.
    with tempfile.TemporaryDirectory(prefix='knowledge-capture-') as folder:
        candidate = Path(folder) / 'knowledge.json'
        candidate.write_bytes(after_raw)
        knowledge.KnowledgeSnapshot(candidate)
    old_basis = knowledge._basis_diagnostics(before, old_index)
    new_basis = knowledge._basis_diagnostics(after, new_index)
    diagnostics = {rid: knowledge._record_diagnostics(rid, new_index, new_basis) for rid in new_index}
    changed = []
    for rid in old_index:
        prior = knowledge._record_diagnostics(rid, old_index, old_basis)
        if prior != diagnostics[rid]:
            changed.append(dict(record_id=rid, before=prior, after=diagnostics[rid]))
    files = {'before.json': before_raw, 'change.json': change_raw, 'knowledge.json': after_raw,
             'handoff.md': render(after, diagnostics, change).encode('utf-8')}
    receipt = dict(schema='knowledge-capture-receipt-1', captured_at=stamp,
                   packet_id=after['packet_id'], base_sha256=digest(before_raw), knowledge_sha256=digest(after_raw),
                   contributor_declaration=change['contributor'], reason=change['reason'],
                   company_acceptance='not_established', source_currency='selected_snapshot_only',
                   added_record_ids=[r['id'] for r in after['records'][len(before['records']):]],
                   supplied_sources=captured,
                   selected_source_changes=[dict(document_id=doc, before=before['selected_sources'].get(doc), after=sid)
                                            for doc, sid in sorted(after['selected_sources'].items())
                                            if sid != before['selected_sources'].get(doc)],
                   changed_existing_diagnostics=changed,
                   files={name: dict(raw_sha256=digest(raw), size_bytes=len(raw)) for name, raw in files.items()})
    files['receipt.json'] = encoded(receipt)
    return files, receipt


def render(packet, diagnostics, change):
    lines = ['# Engineering contribution handoff', '',
             'Draft for company review. Source text and contributor names are supplied data; no approval is established.', '',
             'The complete source captures, exact identities and dependency paths are in `knowledge.json`.',
             'The unmodified prior packet and requested change are beside it; `receipt.json` pins their bytes.', '']
    def escaped(value):
        return re.sub(r'([\\`*_{}\[\]<>#+!|])', r'\\\1', value)
    def show(label, value):
        # Quote and escape supplied Markdown; retain exact values in the complete JSON companion.
        lines.extend(['**' + label + '**', ''])
        lines.extend('> ' + escaped(line) for line in value.splitlines())
        lines.append('')
    show('Question/scope', packet['scope'])
    show('Contribution reason', change['reason'])
    index = {r['id']: r for r in packet['records']}
    added_claims = {c['id'] for c in change['claims']}
    ordered = [r for r in packet['records'] if r['id'] in added_claims]
    ordered += [r for r in packet['records'] if r['id'] not in added_claims]
    for r in ordered:
        if r['kind'] != 'claim':
            continue
        d = diagnostics[r['id']]
        lines.extend(['## ' + escaped(r['title']), ''])
        lines.extend(['Authored this revision.' if r['id'] in added_claims else 'Retained earlier finding; inspect its source status.', ''])
        show('Record and review', r['id'] + ' | ' + r['record_state'] + ' | ' + r['review']['state'])
        show('Authored finding (' + r['data']['basis'] + ')', r['data']['statement'])
        if 'interpretation_limit' in r['data']:
            show('Limits', r['data']['interpretation_limit'])
        if 'attribution' in r['data']:
            show('Unverified recollection', r['data']['attribution'] + '; underlying claim verified: false')
        show('Source and dependency status', 'source basis: ' + d['basis_state'] + '; declared dependencies: ' + d['dependency_state'])
        for e in r['evidence']:
            show('Evidence', e['source_record_id'] + ' | document ' + e['document_id'] + ', revision ' + e['revision']
                 + ' | ' + e['locator'] + ' | ' + e['currency_requirement'])
        for reason in d['basis_reasons']:
            if reason['code'] == 'selected_basis_changed':
                show('Review changed basis', reason['source_record_id'] + ' -> ' + reason['selected_source_record_id'])
        for reason in d['dependency_reasons']:
            show('Review dependency path', ' -> '.join(reason['path']) + ' (' + ', '.join(reason['reason_codes']) + ')')
        for unknown in r['known_unknowns']:
            show('Missing evidence / open question', unknown)
        if not r['owner_roles']:
            show('Receiving owner', 'Unassigned; needs owner.')
        for rid in r['owner_roles']:
            role=index[rid]
            show('Requested receiving role', rid + ' | ' + role['title'] + ' | ' + role['data']['responsibility'])
    lines.extend(['## Next reviewer', '',
                  'Use the supplied role references and the company handoff process. Unassigned roles still need an owner.',
                  'A matching pin checks identity, not source support or installed truth. Review every cited passage.',
                  'Historical claims remain visible; compare them with follow-up claims before using either.', ''])
    return '\n'.join(lines)


def capture(knowledge_path, change_path, source_files, output):
    files, receipt = prepare(read_raw(knowledge_path), read_raw(change_path), source_files)
    output = Path(output)
    # Exclusive directory creation refuses even an empty existing directory. Receipt is written last.
    # An interrupted output is incomplete; retry into a new directory, never overwrite it.
    output.mkdir(parents=False, exist_ok=False)
    for name, raw in files.items():
        with (output / name).open('xb') as stream:
            stream.write(raw)
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--knowledge', required=True, type=Path)
    parser.add_argument('--change', required=True, type=Path)
    parser.add_argument('--source', action='append', nargs=2, metavar=('ID', 'FILE'), default=[])
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args(argv)
    if len(dict(args.source)) != len(args.source):
        parser.error('Duplicate --source ID.')
    try:
        receipt = capture(args.knowledge, args.change, dict(args.source), args.out)
    except (CaptureError, knowledge.OnboardingError, OSError, UnicodeError, TypeError, RecursionError, OverflowError) as exc:
        # Do not leak source text, paths or malformed supplied values through tracebacks.
        print(json.dumps(dict(error='capture_refused', category=type(exc).__name__)), file=sys.stderr)
        return 2
    print(json.dumps(dict(knowledge_sha256=receipt['knowledge_sha256'],
                          added_records=len(receipt['added_record_ids']),
                          changed_existing_records=len(receipt['changed_existing_diagnostics']),
                          company_acceptance='not_established')))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
