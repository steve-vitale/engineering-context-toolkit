"""Capture portable review source records and validate supplied associations; no authority inference."""
import base64
import binascii
import copy
import hashlib
import json
import math
import re
import unicodedata
from pathlib import Path

CONTEXT_SCHEMA = 'graph-review-context-1'
ASSOCIATION_SCHEMA = 'graph-review-associations-1'
MAX_RECORDS = 128
MAX_RECORD_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024
READ_CHUNK = 64 * 1024
HASH = re.compile(r'[0-9a-f]{64}\Z')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_stream(stream, limit):
    """Read through positive short reads; acquire at most limit+1 bytes."""
    chunks, size = [], 0
    while True:
        part = stream.read(min(READ_CHUNK, limit + 1 - size))
        if not part:
            return b''.join(chunks)
        chunks.append(part)
        size += len(part)
        if size > limit:
            raise ValueError('Selected review input exceeds its raw byte budget')


def _finite_values(value):
    if type(value) is dict:
        for key, child in value.items():
            if type(key) is not str:
                raise ValueError('Review JSON object keys must be strings')
            key.encode('utf-8')
            _finite_values(child)
    elif type(value) is list:
        for child in value:
            _finite_values(child)
    elif type(value) is str:
        value.encode('utf-8')
    elif type(value) is float:
        if not math.isfinite(value):
            raise ValueError('Review JSON numbers must be finite')
    elif value is not None and type(value) not in (int, bool):
        raise ValueError('Review JSON must contain ordinary JSON values')


def typed(value):
    """JSON spelling distinguishes bool/int/float and floating signed zero."""
    _finite_values(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      allow_nan=False, separators=(',', ':'))


def parse_object(raw):
    def pairs(entries):
        result = {}
        for key, value in entries:
            if key in result:
                raise ValueError('Duplicate review JSON property')
            result[key] = value
        return result

    def constant(value):
        raise ValueError('Nonfinite review JSON number')

    try:
        if raw.startswith(b'\xef\xbb\xbf'):
            raise ValueError('Review JSON must be UTF-8 without a BOM')
        result = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                            parse_constant=constant)
        if type(result) is not dict:
            raise ValueError('Selected review JSON must be an object')
        typed(result)
        return result
    except (ValueError, UnicodeError, RecursionError, OverflowError, TypeError):
        raise ValueError('Selected review input must be finite UTF-8 JSON without BOM or duplicate properties') from None


def _keys(value, keys, what):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError(what + ' has unexpected or missing fields')


def _hash(value):
    if type(value) is not str or not HASH.fullmatch(value):
        raise ValueError('Review identity must be 64 lowercase hexadecimal digits')


def _name(value):
    if (type(value) is not str or not value or value in ('.', '..')
            or '/' in value or '\\' in value
            or any(unicodedata.category(c) == 'Cc' for c in value)):
        raise ValueError('Review record name must be a safe basename')
    try:
        if len(value.encode('utf-8')) > 255:
            raise ValueError('Review record name exceeds 255 UTF-8 bytes')
    except UnicodeError:
        raise ValueError('Review record name must be valid UTF-8') from None
    if Path(value).suffix.casefold() != '.json':
        raise ValueError('Selected review record name must end in .json (case insensitive)')


def _names(names):
    folded = set()
    for name in names:
        _name(name)
        if name.casefold() in folded:
            raise ValueError('Selected review record names collide under case folding')
        folded.add(name.casefold())


def envelope(raw):
    return {'sha256_raw': digest(raw), 'raw_base64': base64.b64encode(raw).decode('ascii'),
            'payload': parse_object(raw)}


def admitted(payload):
    if not any(key in payload for key in ('applied', 'needs_moc')):
        return False
    for key, required in (('applied', ('item', 'decision')), ('needs_moc', ('item', 'request'))):
        actions = payload.get(key, [])
        if type(actions) is not list:
            return False
        if any(type(action) is not dict or any(type(action.get(k)) is not str
               or not action[k] for k in required) for action in actions):
            return False
    return True


def associations(payload, model_hash, records):
    _keys(payload, ('schema', 'model_sha256_raw', 'records'), 'Review association manifest')
    if payload['schema'] != ASSOCIATION_SCHEMA:
        raise ValueError('Unknown review association schema')
    _hash(payload['model_sha256_raw'])
    if payload['model_sha256_raw'] != model_hash:
        raise ValueError('Review association model raw hash does not match the selected model')
    entries = payload['records']
    if type(entries) is not list or len(entries) > MAX_RECORDS:
        raise ValueError('Review association records must be a bounded list')
    result, names = {}, []
    available = {record['name']: record for record in records}
    for entry in entries:
        _keys(entry, ('name', 'sha256_raw', 'relationship', 'basis'), 'Review association entry')
        _name(entry['name'])
        names.append(entry['name'])
        _names(names)
        _hash(entry['sha256_raw'])
        if entry['relationship'] not in ('current', 'historical') or type(entry['relationship']) is not str:
            raise ValueError('Review association relationship must be current or historical')
        basis = entry['basis']
        if type(basis) is not str or not basis.strip() or len(basis) > 2048:
            raise ValueError('Review association basis must be nonblank text of at most 2048 characters')
        record = available.get(entry['name'])
        if record is None:
            raise ValueError('A listed review record is missing from the selected packet')
        if entry['sha256_raw'] != record['sha256_raw']:
            raise ValueError('A listed review record raw hash does not match')
        if not admitted(record['payload']):
            raise ValueError('A listed record does not contain admitted review event arrays')
        result[entry['name']] = {'status': 'supplied', 'relationship': entry['relationship'], 'basis': basis}
    return result


def project(records):
    events = []
    for record in records:
        association = record['association']
        if association['status'] != 'supplied':
            continue
        payload = record['payload']
        for action in payload.get('applied', []):
            events.append({'type': 'review_decision', 'item': action['item'],
                           'decision': action['decision'], 'changes': action.get('changes'),
                           'notes': action.get('notes'), 'by': payload.get('reviewer'),
                           'on': payload.get('date'), 'record': record['name'],
                           'record_sha256_raw': record['sha256_raw'], 'association': dict(association)})
        for action in payload.get('needs_moc', []):
            events.append({'type': 'change_review_needed', 'item': action['item'],
                           'request': action['request'], 'why': action.get('why'),
                           'by': payload.get('reviewer'), 'on': payload.get('date'),
                           'record': record['name'], 'record_sha256_raw': record['sha256_raw'],
                           'association': dict(association)})
    return copy.deepcopy(events)


def capture(model_path, model_raw, reviews, manifest=None):
    """Return context, derived events and the exact consumed path inventory."""
    folder = Path(reviews)
    if not folder.is_dir():
        raise ValueError(f'--reviews {reviews}: not a folder (give the folder containing selected review records)')
    selected = sorted((p for p in folder.iterdir() if p.suffix.casefold() == '.json'), key=lambda p: p.name)
    if len(selected) > MAX_RECORDS:
        raise ValueError('Too many selected review records')
    _names([p.name for p in selected])
    cache = {Path(model_path).resolve(): model_raw}

    def acquire(path, limit):
        key = Path(path).resolve()
        if key not in cache:
            try:
                if not Path(path).is_file():
                    raise ValueError('Selected review input is not a regular file')
                with Path(path).open('rb') as stream:
                    cache[key] = read_stream(stream, limit)
            except OSError:
                raise ValueError('Cannot read a selected review input') from None
        raw = cache[key]
        if len(raw) > limit:
            raise ValueError('Selected review input exceeds its raw byte budget')
        return raw

    records, total = [], 0
    for path in selected:
        raw = acquire(path, min(MAX_RECORD_BYTES, MAX_TOTAL_BYTES - total))
        total += len(raw)
        records.append({'name': path.name, **envelope(raw), 'association': {'status': 'unbound'}})
    manifest_envelope = None
    consumed = list(selected)
    if manifest is not None:
        manifest_envelope = envelope(acquire(manifest, MAX_MANIFEST_BYTES))
        supplied = associations(manifest_envelope['payload'], digest(model_raw), records)
        for record in records:
            if record['name'] in supplied:
                record['association'] = supplied[record['name']]
        consumed.append(Path(manifest))
    context = {'schema': CONTEXT_SCHEMA, 'model_sha256_raw': digest(model_raw),
               'records': records, 'association_manifest': manifest_envelope}
    return context, project(records), tuple(consumed)


def _decode(value, limit):
    _keys(value, ('sha256_raw', 'raw_base64', 'payload'), 'Retained review envelope')
    _hash(value['sha256_raw'])
    encoded = value['raw_base64']
    if type(encoded) is not str or len(encoded) > 4 * ((limit + 2) // 3):
        raise ValueError('Retained review base64 exceeds its byte budget')
    try:
        raw = base64.b64decode(encoded.encode('ascii'), validate=True)
    except (UnicodeError, ValueError, binascii.Error):
        raise ValueError('Retained review bytes are not canonical base64') from None
    if (len(raw) > limit or base64.b64encode(raw).decode('ascii') != encoded
            or digest(raw) != value['sha256_raw']):
        raise ValueError('Retained review bytes do not match their raw identity or budget')
    if typed(parse_object(raw)) != typed(value['payload']):
        raise ValueError('Retained review payload differs from its exact typed raw JSON')
    return raw


def validate_graph(graph):
    """Check internal packet consistency only; no original model/authority is authenticated."""
    context = graph['review_context']
    _keys(context, ('schema', 'model_sha256_raw', 'records', 'association_manifest'), 'Review context')
    if context['schema'] != CONTEXT_SCHEMA:
        raise ValueError('Unknown review context schema')
    _hash(context['model_sha256_raw'])
    records = context['records']
    if type(records) is not list or len(records) > MAX_RECORDS:
        raise ValueError('Retained review records must be a bounded list')
    names, total = [], 0
    for record in records:
        _keys(record, ('name', 'sha256_raw', 'raw_base64', 'payload', 'association'), 'Retained review record')
        names.append(record['name'])
        _names(names)
        raw = _decode({k: record[k] for k in ('sha256_raw', 'raw_base64', 'payload')},
                      min(MAX_RECORD_BYTES, MAX_TOTAL_BYTES - total))
        total += len(raw)
    if names != sorted(names):
        raise ValueError('Retained review records are not in filename order')
    manifest = context['association_manifest']
    supplied = {}
    if manifest is not None:
        _decode(manifest, MAX_MANIFEST_BYTES)
        supplied = associations(manifest['payload'], context['model_sha256_raw'], records)
    for record in records:
        expected = supplied.get(record['name'], {'status': 'unbound'})
        if typed(record['association']) != typed(expected):
            raise ValueError('Record association differs from the supplied manifest')
    expected_events = project(records)
    if typed(graph.get('events')) != typed(expected_events):
        raise ValueError('Graph events differ from the complete ordered supplied review projection')
    counts = graph.get('counts')
    if type(counts) is not dict:
        raise ValueError('Graph counts must be an object for review context')
    count = counts.get('events')
    if type(count) is not int or count != len(expected_events):
        raise ValueError('Graph event count must be an exact integer matching the supplied projection')
