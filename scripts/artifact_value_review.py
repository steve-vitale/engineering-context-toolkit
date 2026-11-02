"""Admit explicitly reviewed frozen Native value inventories, then reuse source_support-v1.

No claim discovery, source authentication, engineering truth or rationale-quality inference.
All file reads happen during admit(); scoring/controls use that captured per-case snapshot.
"""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re

PROTOCOL = 'provided-model-values-v1'
INPUT_SCHEMA = 'source-support-artifact-values-1'
KEY_SCHEMA = 'artifact-value-review-key-1'
MAXIMUM = 16 * 1024 * 1024
TEXT = {'.json', '.graphml', '.xml', '.md', '.txt', '.csv', '.py'}
HEADER = ['model_pointer', 'record_identity_json', 'value_json', 'source_locator',
          'source_quote_json', 'verdict', 'independent_evidence', 'review_note']
VALUE_MARKER = ' Exact bound values: '


def require(ok, message):
    if not ok:
        raise ValueError('Artifact value review: ' + message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def same(a, b):
    return canonical(a) == canonical(b)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def parse(raw):
    def invalid(value):
        raise ValueError('Artifact value review: non-finite JSON number')
    try:
        value = json.loads(raw.decode('utf-8-sig') if isinstance(raw, bytes) else raw,
                           object_pairs_hook=pairs, parse_constant=invalid)
        canonical(value).encode('utf-8')
        return value
    except (UnicodeError, RecursionError, OverflowError) as exc:
        raise ValueError('Artifact value review: invalid JSON encoding or depth') from None


def ids(values, label, nonempty=True):
    require(isinstance(values, list) and (bool(values) or not nonempty), label + ' must be a list')
    require(all(isinstance(v, str) and v and v == v.strip() for v in values), label + ' needs exact nonempty identities')
    require(len(values) == len(set(values)), label + ' repeats an identity')
    return values


def leaves(value, pointer=''):
    if isinstance(value, dict) and value:
        for key, child in value.items():
            yield from leaves(child, pointer + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(value, list) and value:
        for index, child in enumerate(value):
            yield from leaves(child, pointer + '/' + str(index))
    else:
        yield pointer, value


def kind(value):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, int):
        return 'integer'
    if isinstance(value, float):
        return 'number'
    if isinstance(value, str):
        return 'string'
    return 'empty-object' if isinstance(value, dict) else 'empty-array'


def raw_pin(raw):
    return {'sha256_raw': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def check_pin(ref, raw, label):
    require(isinstance(ref, dict), label + ' needs a raw fingerprint')
    require(isinstance(ref.get('sha256_raw'), str) and re.fullmatch('[0-9a-f]{64}', ref['sha256_raw']), label + ' has an invalid raw fingerprint')
    require(type(ref.get('bytes')) is int and ref['bytes'] >= 0, label + ' needs a byte count')
    require(ref['sha256_raw'] == raw_pin(raw)['sha256_raw'] and ref['bytes'] == len(raw), label + ' raw identity differs')


class Capture:
    """One bounded read/parse per resolved path during a single case admission."""
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.raw = {}
        self.parsed = {}
        self.read_counts = {}

    def path(self, value):
        require(isinstance(value, str) and value and not Path(value).is_absolute(), 'use a root-relative file path')
        path = (self.root / value).resolve()
        require(path.is_relative_to(self.root), 'file reference escapes selected root')
        return path

    def read(self, ref, maximum=MAXIMUM, outer=False):
        require(isinstance(ref, dict) and 'path' in ref, 'file reference needs a path')
        path = self.path(ref['path'])
        if path not in self.raw:
            require(path.is_file(), 'referenced file is unavailable')
            with path.open('rb') as stream:
                value = stream.read(maximum + 1)
            require(len(value) <= maximum, 'selected file exceeds its byte limit')
            self.raw[path] = value
            self.read_counts[path] = 1
        value = self.raw[path]
        require(len(value) <= maximum, 'selected file exceeds its byte limit')
        if outer:
            require(set(ref) <= {'path', 'sha256', 'role'} and 'sha256' in ref, 'outer reference needs the existing benchmark fingerprint')
            require('role' not in ref or isinstance(ref['role'], str) and bool(ref['role']), 'outer reference role must be nonempty text')
            hashed = value.replace(b'\r\n', b'\n') if path.suffix.lower() in TEXT else value
            require(isinstance(ref['sha256'], str) and ref['sha256'] == hashlib.sha256(hashed).hexdigest(), 'outer file fingerprint differs')
        else:
            check_pin(ref, value, 'selected file')
        return path, value

    def json(self, ref, outer=False):
        path, raw = self.read(ref, outer=outer)
        if path not in self.parsed:
            self.parsed[path] = parse(raw)
        return self.parsed[path], raw

    def report(self):
        return {path.relative_to(self.root).as_posix(): {**raw_pin(value), 'capture_reads': self.read_counts[path]}
                for path, value in self.raw.items()}


def csv_rows(raw):
    try:
        stream = io.StringIO(raw.decode('utf-8-sig'), newline='')
        reader = csv.DictReader(stream)
        require(reader.fieldnames == HEADER, 'provided CSV needs the exact eight-column schema/order')
        rows = list(reader)
        require(all(set(row) == set(HEADER) and all(isinstance(v, str) for v in row.values()) for row in rows), 'malformed CSV row')
        ids([r['model_pointer'] for r in rows], 'provided CSV pointers', nonempty=False)
        return rows
    except (UnicodeError, csv.Error):
        raise ValueError('Artifact value review: invalid provided CSV') from None


def cell(value, empty=False):
    if empty and value == '':
        return None
    return parse(value)


class Admitted:
    def __init__(self, packet, key, report):
        self._packet = copy.deepcopy(packet)
        self._key = copy.deepcopy(key)
        self._report = copy.deepcopy(report)

    def score(self, prediction):
        import source_support
        return source_support.score(self._packet, self._key, prediction)

    def controls(self):
        import source_support
        return source_support.controls(self._packet, self._key)

    def normalized(self):
        return copy.deepcopy(self._packet), copy.deepcopy(self._key)

    def report(self):
        return copy.deepcopy(self._report)


def admit(root, input_ref, key_ref):
    """Capture/admit one opt-in case once; returned scores do not reopen selected files."""
    import description_workflow as workflow
    import source_support
    capture = Capture(root)
    packet, _ = capture.json(input_ref, outer=True)
    key, _ = capture.json(key_ref, outer=True)
    require(isinstance(packet, dict) and packet.get('schema') == INPUT_SCHEMA, 'unsupported artifact input schema')
    require(isinstance(key, dict) and key.get('schema') == KEY_SCHEMA, 'unsupported artifact key schema')
    require(packet.get('model_root_pointer') == '', 'this version requires a bare Native model root')
    model, model_raw = capture.json(packet.get('artifact'))
    inventory, inventory_raw = capture.json(packet.get('inventory'))
    projection, projection_raw = capture.json(packet.get('v1_projection'))
    _, source_raw = capture.read(packet.get('source'), maximum=workflow.MAX_SOURCE)
    _, provided_raw = capture.read(packet.get('provided_values'))
    require(isinstance(model, dict) and isinstance(model.get('meta'), dict), 'model needs Native meta')
    require(all(isinstance(model['meta'].get(f), list) for f in ('unknowns', 'assumptions')), 'model needs explicit unknowns/assumptions lists')
    require(isinstance(model['meta'].get('source_document'), str) and bool(model['meta']['source_document']), 'model needs its literal source display label')
    require(model['meta'].get('source_sha256') == raw_pin(source_raw)['sha256_raw'], 'model source identity differs from captured source')
    require(isinstance(inventory, dict) and inventory.get('schema') == 'provided-model-value-inventory-1', 'unsupported inventory schema')
    for field, raw in [('artifact', model_raw), ('source', source_raw), ('inventory', inventory_raw), ('provided_values', provided_raw), ('v1_projection', projection_raw)]:
        check_pin(key.get(field), raw, 'key ' + field)
    for field, raw in [('artifact_raw', model_raw), ('source_raw', source_raw), ('provided_values_raw', provided_raw)]:
        check_pin(inventory.get(field), raw, 'inventory ' + field)
    actual = list(leaves(model))
    actual_paths = [p for p, _ in actual]
    require(ids(key.get('required_all_model_pointers'), 'key model pointers') == actual_paths, 'model pointer scope/order differs from key')
    entries = inventory.get('entries')
    require(isinstance(entries, list) and all(isinstance(e, dict) for e in entries), 'inventory needs entries')
    require(ids([e.get('pointer') for e in entries], 'inventory pointers') == actual_paths, 'inventory does not cover every actual model value in order')
    roles = key.get('roles')
    require(isinstance(roles, dict) and set(roles) == set(actual_paths), 'key roles do not partition all model values')
    groups = ids(key.get('required_group_ids'), 'key groups')
    require(ids(packet.get('claim_group_ids'), 'input groups') == groups, 'input/key group scope differs')
    membership = key.get('group_membership')
    require(isinstance(membership, dict) and set(membership) == set(groups), 'key group membership is incomplete')
    for group in groups:
        ids(membership[group], 'group component pointers')
        require(set(membership[group]) <= set(actual_paths), 'group has an unknown component pointer')
    require(isinstance(key.get('judgments'), dict) and set(key['judgments']) == set(groups), 'key labels do not cover every declared group')
    require(isinstance(projection, dict) and isinstance(projection.get('items'), list), 'projection needs items')
    require(ids([item.get('id') for item in projection['items'] if isinstance(item, dict)], 'projection groups') == groups and len(projection['items']) == len(groups), 'projection group membership/order differs')
    values = dict(actual)
    for item in projection['items']:
        text = item.get('candidate_claim')
        expected = canonical({p: values[p] for p in membership[item['id']]})
        require(isinstance(text, str) and VALUE_MARKER in text and text.rpartition(VALUE_MARKER)[2] == expected,
                'projection does not retain the exact typed group values')
    try:
        lines = source_raw.decode('utf-8-sig').splitlines()
    except UnicodeError:
        raise ValueError('Artifact value review: invalid source UTF-8') from None
    # Reuse the existing record/source inheritance and supplied-value enumeration, not a second review workflow.
    try:
        generated = workflow.interpretation_review(model, source_raw)
    except (ValueError, TypeError, KeyError, AttributeError, IndexError, RecursionError, OverflowError):
        raise ValueError('Artifact value review: model cannot produce the declared review format') from None
    expected_rows = csv_rows(generated['interpretation_review.csv'])
    provided_rows = csv_rows(provided_raw)
    require(len(provided_rows) == len(expected_rows), 'provided CSV row coverage differs')
    for actual_row, expected_row in zip(provided_rows, expected_rows):
        require(actual_row['model_pointer'] == expected_row['model_pointer'], 'provided CSV row order/pointer differs')
        require(actual_row['source_locator'] == expected_row['source_locator'], 'provided CSV source locator differs')
        for field in ('value_json', 'record_identity_json', 'source_quote_json'):
            require((actual_row[field] == '' if expected_row[field] == '' else actual_row[field] != '' and same(cell(actual_row[field]), cell(expected_row[field]))),
                    'provided CSV typed value/identity/quote differs')
    provided = {row['model_pointer']: (index + 1, row) for index, row in enumerate(provided_rows)}
    require(set(ids(key.get('required_provided_pointers'), 'key provided pointers', nonempty=False)) == set(provided), 'key does not cover the full provided-value scope')
    required_entry_fields = {'pointer', 'value', 'json_kind', 'canonical_typed_value', 'role', 'claim_ids',
                             'provided_row', 'record_pointer', 'record_identity', 'source_locator', 'source_quote'}
    for entry, (pointer, value) in zip(entries, actual):
        require(set(entry) == required_entry_fields, 'inventory entry fields differ from versioned format')
        require(same(entry['value'], value) and entry['canonical_typed_value'] == canonical(value) and entry['json_kind'] == kind(value), 'inventory typed value/kind differs from artifact')
        require(isinstance(entry['role'], str) and entry['role'] and entry['role'] == roles[pointer], 'inventory role differs from reviewed key')
        expected_groups = [g for g in groups if pointer in membership[g]]
        require(ids(entry['claim_ids'], 'entry claim ids', nonempty=False) == expected_groups, 'entry claim/group membership differs')
        require((entry['role'] == 'semantic-claim-component') == bool(expected_groups), 'semantic component is hidden or role-only value is promoted')
        row_pair = provided.get(pointer)
        row_index, row = row_pair if row_pair else (None, None)
        require(type(entry['provided_row']) is int if row is not None else entry['provided_row'] is None, 'invalid provided row ordinal')
        require(entry['provided_row'] == row_index, 'inventory provided row ordinal differs')
        parts = pointer.split('/')
        is_record = len(parts) > 2 and parts[1] in workflow.RECORDS
        record_pointer = '/'.join(parts[:3]) if is_record else None
        identity, locator, quotation = None, None, None
        if is_record:
            try:
                record = model[parts[1]][int(parts[2])]
                identity = record[workflow.RECORDS[parts[1]]]
            except (KeyError, IndexError, TypeError, ValueError):
                raise ValueError('Artifact value review: invalid record identity context') from None
        if row:
            locator = row['source_locator'] or None
            quotation = cell(row['source_quote_json'], empty=True)
        elif is_record and parts[-1] == 'source':
            match = workflow.CITATION.fullmatch(value) if isinstance(value, str) else None
            require(match is not None, 'source field has an invalid locator')
            start, end = map(int, match.groups())
            require(start <= end <= len(lines), 'source field locator is out of bounds')
            locator, quotation = value, '\n'.join(lines[start-1:end])
        require(entry['record_pointer'] == record_pointer and same(entry['record_identity'], identity), 'inventory record context differs')
        require(entry['source_locator'] == locator and same(entry['source_quote'], quotation), 'inventory source context differs')
    normalized_key = {'judgments': copy.deepcopy(key['judgments'])}
    source_support.validate(projection, normalized_key)
    contradictions = [{'id':group, 'pointers':membership[group], 'values':{p:values[p] for p in membership[group]}}
                      for group in groups if key['judgments'][group] == 'contradicted']
    report = {'schema':'artifact-value-review-admission-1', 'protocol':PROTOCOL,
              'coverage':{'model_entries':len(actual), 'provided_values':len(provided), 'semantic_groups':len(groups),
                          'semantic_component_values':sum(bool(e['claim_ids']) for e in entries),
                          'role_only_values':sum(not e['claim_ids'] for e in entries)},
              'keyed_artifact_contradictions':contradictions, 'captured_files':capture.report(),
              'limits':'Exact declared frozen value/group coverage and fixed-key reviewer labels only. Role exclusions/source judgments need independent review. No automatic claim discovery, rationale-quality, source authority, generator correctness, current installation or plant acceptance.'}
    return Admitted(projection, normalized_key, report)
