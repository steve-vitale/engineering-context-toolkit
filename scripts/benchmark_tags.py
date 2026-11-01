"""Explicit tag task adapter. Legacy matching/normalization remains in the unchanged scorers."""
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import statistics
import struct
import xml.etree.ElementTree as ET

import score_pid2graph as geometry
import score_tags as tags

TASK = 'tag-reading'
CONTRACT = 'tag-text-v1'
MODES = ('geometry', 'taglist')
PROVENANCE_SCHEMA = 'tag-source-provenance-1'


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def raw_identity(path):
    h, size = hashlib.sha256(), 0
    with path.open('rb') as stream:
        while True:
            block = stream.read(65536)
            if not block:
                break
            h.update(block)
            size += len(block)
    return {'raw_sha256': h.hexdigest(), 'size_bytes': size}


def validate_source_provenance(case, root, api):
    """Validate generic declared local raw artifacts and LICENSE before interpreting any answer."""
    manifest_path = api.reference(root, case.get('source_provenance'))
    manifest = api.read_json(manifest_path)
    api.require(isinstance(manifest, dict) and manifest.get('schema') == PROVENANCE_SCHEMA,
                'Tag source provenance needs ' + PROVENANCE_SCHEMA)
    api.text_fields(manifest.get('source'), ('repository', 'revision', 'license', 'attribution'), 'source')
    originals = manifest['source'].get('originals')
    api.require(isinstance(originals, list) and originals, 'Source needs original-file declarations')
    names = set()
    for original in originals:
        api.text_fields(original, ('path', 'url', 'raw_sha256'), 'original')
        api.require(original['path'] not in names, 'Duplicate original source declaration')
        names.add(original['path'])
        api.require(len(original['raw_sha256']) == 64 and all(c in '0123456789abcdef' for c in original['raw_sha256']),
                    'Invalid original source SHA256')
        api.require(type(original.get('size_bytes')) is int and original['size_bytes'] >= 0,
                    'Original source byte count must be nonnegative integer')
    derivation = manifest.get('derivation')
    api.text_fields(derivation, ('historical_producing_converter', 'original_historical_key_bytes', 'limits'), 'derivation')
    api.require(isinstance(derivation.get('current_associated_files'), list) and derivation['current_associated_files'],
                'Derivation needs current associated file references')
    for ref in derivation['current_associated_files']:
        api.reference(root, ref)
    api.require(isinstance(derivation.get('render_parameters'), dict), 'Derivation needs declared render parameters')
    artifacts = manifest.get('artifacts')
    api.require(isinstance(artifacts, list) and artifacts, 'Source provenance needs raw artifacts')
    by_path, received = {}, []
    for row in [*artifacts, manifest.get('license')]:
        api.text_fields(row, ('path', 'raw_sha256'), 'raw source artifact')
        api.require(type(row.get('size_bytes')) is int and row['size_bytes'] >= 0,
                    'Raw source artifact byte count must be nonnegative integer')
        api.require(len(row['raw_sha256']) == 64 and all(c in '0123456789abcdef' for c in row['raw_sha256']),
                    'Invalid raw source artifact SHA256')
        path = api.local(root, row['path'])
        api.require(path.is_file(), 'Raw source artifact unavailable: ' + row['path'])
        actual = raw_identity(path)
        api.require(actual == {k: row[k] for k in ('raw_sha256', 'size_bytes')},
                    'Raw source artifact fingerprint/size differs: ' + row['path'])
        if row is not manifest['license']:
            api.text_fields(row, ('role',), 'artifact')
            api.require(row['role'] in ('input', 'key', 'tags'), 'Unknown source artifact role')
            api.require(path not in by_path, 'Duplicate resolved source artifact path')
            associations = row.get('source_paths')
            api.require(isinstance(associations, list) and associations and all(p in names for p in associations),
                        'Artifact needs declared original source associations')
            by_path[path] = row
        received.append({'path': row['path'], **actual})
    for role, ref in case['files'].items():
        path = api.local(root, ref['path'])
        api.require(path in by_path and by_path[path]['role'] == role, 'Case/source provenance artifact role mismatch')
    return {'reference': case['source_provenance'], 'raw_artifacts_and_license': received,
            'historical_producing_converter': derivation['historical_producing_converter'],
            'original_historical_key_bytes': derivation['original_historical_key_bytes']}


def png_dimensions(path, api):
    with path.open('rb') as stream:
        header = stream.read(24)
    api.require(len(header) == 24 and header[:8] == b'\x89PNG\r\n\x1a\n' and
                header[8:16] == b'\x00\x00\x00\rIHDR', 'Tag input needs a PNG IHDR header')
    width, height = struct.unpack('>II', header[16:24])
    api.require(width > 0 and height > 0, 'Tag PNG dimensions must be positive')
    return width, height


def validate_key(mode, files, case, api):
    width, height = png_dimensions(files['input'], api)
    if mode == 'taglist':
        key = api.read_json(files['key'])
        api.require(isinstance(key, dict) and isinstance(key.get('items'), list) and key['items'],
                    'Tag-list key needs nonempty items')
        seen, identifiers = set(), defaultdict(list)
        for row in key['items']:
            api.text_fields(row, ('identifier', 'list', 'class'), 'tag-list item')
            normalized = tags.norm_lenient(row['identifier'])
            api.require(bool(normalized), 'Tag-list identifier normalizes empty')
            complete = (row['identifier'], row['list'], row['class'])
            api.require(complete not in seen, 'Duplicate complete tag-list row')
            seen.add(complete)
            identifiers[normalized].append(dict(row))
        overlaps = {key: value for key, value in identifiers.items() if len(value) > 1}
        if overlaps:
            api.text_fields(case, ('taglist_overlap_note',), 'case with repeated list identifiers')
        return {'tag_key_kind': mode, 'listed': len(key['items']), 'identifier_overlaps': overlaps,
                'overlap_note': case.get('taglist_overlap_note'), 'image_dimensions': [width, height]}
    try:
        document = ET.parse(files['key']).getroot()
    except ET.ParseError as exc:
        raise ValueError('Malformed tag geometry GraphML') from exc
    ns = geometry.NS
    api.require(document.tag == '{' + ns['g'] + '}graphml', 'Tag geometry needs GraphML namespace')
    definitions = {}
    for key in document.findall('g:key', ns):
        name = key.get('id')
        api.require(isinstance(name, str) and name.strip() and name not in definitions, 'Duplicate/empty GraphML field ID')
        definitions[name] = key.get('attr.name')
    graphs = document.findall('g:graph', ns)
    api.require(len(graphs) == 1, 'Tag geometry needs exactly one graph')
    identities, non_scored = set(), []
    for node in graphs[0].findall('g:node', ns):
        ident = node.get('id')
        api.require(isinstance(ident, str) and ident.strip() and ident not in identities, 'Duplicate/empty GraphML node ID')
        identities.add(ident)
        fields = {}
        for entry in node.findall('g:data', ns):
            api.require(entry.get('key') in definitions, 'Unknown GraphML field reference')
            field = definitions[entry.get('key')]
            api.require(field not in fields, 'Ambiguous repeated GraphML node field')
            fields[field] = entry.text
        api.text_fields(fields, ('label', 'xmin', 'xmax', 'ymin', 'ymax'), 'GraphML node')
        try:
            box = [float(fields[k]) for k in ('xmin', 'ymin', 'xmax', 'ymax')]
        except (ValueError, OverflowError) as exc:
            raise ValueError('Invalid GraphML coordinates') from exc
        api.require(all(math.isfinite(v) for v in box), 'GraphML coordinates must be finite')
        if fields['label'] in geometry.SCORED:
            api.require(box[2] > box[0] and box[3] > box[1], 'Scored GraphML node needs positive area')
        else:
            non_scored.append({'id': ident, 'class': fields['label'], 'box': box})
    api.require(bool(identities), 'Tag GraphML has no nodes')
    truth = api.read_json(files['tags'])
    api.require(isinstance(truth, dict) and isinstance(truth.get('tags'), dict), 'Geometry tag key needs tags object')
    nodes, _ = geometry.load_key(files['key'], width, height)
    excluded, eligible = [], 0
    for ident, text in truth['tags'].items():
        api.require(text is None or isinstance(text, str), 'Tag truth must be text or null')
        api.require(not isinstance(text, str) or text == '' or bool(text.strip()), 'Whitespace-only tag truth is invalid')
        reasons = []
        if ident not in nodes:
            reasons.append('missing-geometry-key')
        elif nodes[ident]['class'] not in geometry.SCORED:
            reasons.append('non-scored-key-class')
        if text is None or text == '':
            reasons.append('non-bearing-text')
        if reasons:
            excluded.append({'key': ident, 'truth': text, 'reasons': reasons})
        else:
            eligible += 1
    api.require(eligible > 0, 'Geometry tag key has no eligible labelled truth')
    return {'tag_key_kind': mode, 'eligible_truth': eligible, 'excluded_truth': excluded,
            'non_scored_geometry': non_scored, 'image_dimensions': [width, height]}


def admitted_prediction(mode, prediction, api):
    if prediction is None:
        return None
    api.require(isinstance(prediction, dict) and isinstance(prediction.get('symbols'), list), 'Tag answer needs symbols list')
    api.require(all(isinstance(row, dict) for row in prediction['symbols']), 'Tag symbols must be objects')
    if mode == 'geometry':
        seen = set()
        for row in prediction['symbols']:
            ident = row.get('id')
            api.require(type(ident) is str and bool(ident.strip()), 'Geometry prediction IDs must be nonempty plain strings')
            api.require(ident not in seen, 'Duplicate geometry prediction ID across symbol rows')
            seen.add(ident)
    return prediction


def score_case(mode, files, prediction, api, key_diagnostics):
    prediction = admitted_prediction(mode, prediction, api)
    if mode == 'geometry':
        scored = tags.score_geometry(files['key'], files['tags'], prediction, files['input'])
        counts = {profile: {name: scored[profile][name] for name in ('correct', 'wrong', 'no_tag', 'missed', 'found')}
                  | {'with_truth': scored['with_truth']} for profile in ('strict', 'lenient')}
        diagnostics = {'key_admission': key_diagnostics, 'items': scored['items'],
                       'ignored_or_malformed_symbols': 0 if prediction is None else len(prediction['symbols']) - len(geometry.valid_symbols(prediction)),
                       'legacy_three_decimal_rates': {profile: {name: scored[profile][name] for name in ('accuracy_on_found', 'end_to_end_recall')}
                                                     for profile in ('strict', 'lenient')}}
    else:
        scored = tags.score_taglist(files['key'], prediction)
        fields = ('listed', 'found', 'found_with_list_class')
        counts = {'all': {name: scored['all'][name] for name in fields},
                  'by_list': {label: {name: row[name] for name in fields} for label, row in scored['by_list'].items()},
                  'predicted_tags': scored['predicted_tags']}
        diagnostics = {'key_admission': key_diagnostics, 'items': scored['items']}
    return counts, diagnostics


def pooled(mode, rows):
    if mode == 'geometry':
        return {profile: {field: sum(row[profile][field] for row in rows) for field in rows[0][profile]}
                for profile in ('strict', 'lenient')}
    labels = sorted({label for row in rows for label in row['by_list']})
    fields = ('listed', 'found', 'found_with_list_class')
    return {'all': {field: sum(row['all'][field] for row in rows) for field in fields},
            'by_list': {label: {field: sum(row['by_list'].get(label, {}).get(field, 0) for row in rows) for field in fields}
                        for label in labels}, 'predicted_tags': sum(row['predicted_tags'] for row in rows)}


def rates(mode, counts):
    if mode == 'geometry':
        result = {}
        for profile in ('strict', 'lenient'):
            row = counts[profile]
            result[profile + '_end_to_end_recall'] = ratio(row['correct'], row['with_truth'])
            result[profile + '_accuracy_on_found'] = ratio(row['correct'], row['found'])
        return result, {}
    def one(row):
        return {'identifier_recall': ratio(row['found'], row['listed']),
                'found_identifier_class_agreement': ratio(row['found_with_list_class'], row['found'])}
    return one(counts['all']), {label: one(row) for label, row in counts['by_list'].items()}


def controls(mode, files, api, diagnostics):
    if mode == 'geometry':
        width, height = diagnostics['image_dimensions']
        nodes, _ = geometry.load_key(files['key'], width, height)
        truth = api.read_json(files['tags'])['tags']
        prediction = {'symbols': [{'id': ident, 'class': node['class'], 'box': node['box'], 'tag': truth.get(ident)}
                                  for ident, node in nodes.items() if node['class'] in geometry.SCORED]}
    else:
        prediction = {'symbols': [{'id': 'reference-' + str(i), 'class': row['class'], 'tag': row['identifier']}
                                  for i, row in enumerate(api.read_json(files['key'])['items'])]}
    positive = score_case(mode, files, prediction, api, diagnostics)[0]
    empty = score_case(mode, files, None, api, diagnostics)[0]
    if mode == 'geometry':
        api.require(positive['strict']['correct'] == positive['strict']['with_truth'] > 0,
                    'Geometry tag reference control does not recover every declared eligible label')
    else:
        api.require(positive['all']['found'] == positive['all']['listed'] > 0,
                    'Tag-list reference control does not recover every listed identifier')
    return {'reference': positive, 'empty': empty, 'key_admission': diagnostics}


def evaluate(suite_path, root, api, suite):
    api.require(isinstance(suite.get('cases'), list) and suite['cases'], 'Suite needs cases')
    api.require(isinstance(suite.get('runs'), list) and suite['runs'], 'Suite needs run manifest paths')
    sources = ('benchmark.py', 'benchmark_tags.py', 'score_tags.py', 'score_pid2graph.py')
    code_hashes = {name: api.file_hash(Path(api.__file__).parent / name) for name in sources}
    cases, loaded, known_controls, provenance = {}, {}, {}, {}
    for case in suite['cases']:
        api.text_fields(case, ('id', 'family', 'split', 'evidence', 'source_url', 'license', 'key_author', 'tag_key_kind'), 'case')
        api.require(case['id'] not in cases, 'Duplicate case ID')
        api.require(case['split'] in ('development', 'validation', 'held-out', 'synthetic-control'), 'Unknown case split')
        mode = case['tag_key_kind']
        api.require(mode in MODES, 'tag_key_kind must be geometry or taglist')
        required = {'input', 'key', 'tags'} if mode == 'geometry' else {'input', 'key'}
        api.require(set(case.get('files', {})) == required, 'Tag case files disagree with explicit key kind')
        provenance[case['id']] = validate_source_provenance(case, root, api)
        files = {role: api.reference(root, ref) for role, ref in case['files'].items()}
        diagnostics = validate_key(mode, files, case, api)
        known_controls[case['id']] = controls(mode, files, api, diagnostics)
        cases[case['id']], loaded[case['id']] = case, files
    results, submissions, run_ids, used_artifacts = [], [], set(), set()
    for path in suite['runs']:
        run_path = api.local(root, path)
        run = api.read_json(run_path)
        api.text_fields(run, ('id', 'ran_at', 'interface', 'method', 'provenance'), 'run')
        api.text_fields(run.get('model'), ('provider', 'id', 'version'), 'model')
        api.require(run['id'] not in run_ids, 'Duplicate run ID')
        run_ids.add(run['id'])
        attempted = run.get('cases')
        api.require(isinstance(attempted, list) and attempted and all(isinstance(cid, str) and cid in cases for cid in attempted),
                    'Run needs declared attempted case IDs')
        api.require(len(attempted) == len(set(attempted)), 'Duplicate attempted case')
        predictions = run.get('predictions')
        api.require(isinstance(predictions, dict) and not set(predictions) - set(attempted), 'Prediction is outside the attempted set')
        api.require(isinstance(run.get('configuration'), dict), 'Run needs a configuration object (unknown values stay explicit)')
        api.require(isinstance(run.get('recipe'), list) and run['recipe'], 'Run needs pinned prompt/recipe files')
        for ref in run['recipe']:
            api.reference(root, ref)
        submissions.append({'id': run['id'], 'path': path, 'sha256': api.file_hash(run_path)})
        buckets = defaultdict(list)
        for cid in sorted(attempted):
            case = cases[cid]
            buckets[(case['tag_key_kind'], case['family'], case['split'], case['evidence'])].append(cid)
        for (mode, family, split, evidence), ids in sorted(buckets.items()):
            cohort = {'task': TASK, 'scoring_contract': CONTRACT, 'tag_key_kind': mode, 'protocol': suite['protocol'],
                      'scorer_code_sha256': code_hashes, 'cases': [cases[cid] for cid in ids]}
            rows = []
            for cid in ids:
                case, ref = cases[cid], predictions.get(cid)
                prediction, status, note, recorded_run_at = None, 'missing', None, None
                reported = {'seconds': None, 'cost_usd': None, 'cost_usd_notional': None}
                if ref is not None:
                    artifact = api.reference(root, ref, missing=True)
                    if artifact:
                        stat = artifact.stat()
                        file_identity = (stat.st_dev, stat.st_ino) if stat.st_ino else str(artifact)
                        artifact_identity = (json.dumps(run['model'], sort_keys=True), run['interface'], run['method'],
                                             api.digest(api.encoded(run['configuration'])), cid, file_identity)
                        api.require(artifact_identity not in used_artifacts, 'Same answer file reused as a model/method replicate')
                        used_artifacts.add(artifact_identity)
                        try:
                            record = api.read_json(artifact)
                            api.require(isinstance(record, dict), 'Answer must be a JSON object')
                            # Always check supplied metadata, including flattened answers and unknown schema labels.
                            api.check_saved_metadata(record, run, case)
                            reported = {key: record.get(key) for key in reported}
                            recorded_run_at = record.get('ran_at')
                            prediction = record.get('prediction', record)
                            status = 'failed' if prediction is None or record.get('error') or record.get('parse_error') else 'ok'
                            if status != 'ok':
                                prediction = None
                        except api.ProvenanceError:
                            raise
                        except (ValueError, UnicodeError, RecursionError) as exc:
                            prediction, status, note = None, 'invalid-answer', str(exc)
                try:
                    scored, diagnostics = score_case(mode, loaded[cid], prediction, api, known_controls[cid]['key_admission'])
                except (ValueError, TypeError, KeyError, AttributeError, IndexError, OverflowError) as exc:
                    scored, diagnostics = score_case(mode, loaded[cid], None, api, known_controls[cid]['key_admission'])
                    status, note = 'invalid-answer', str(exc)
                row_rates, row_list_rates = rates(mode, scored)
                rows.append({'case': cid, 'status': status, 'note': note, 'counts': scored, 'metrics': row_rates,
                             'by_list_metrics': row_list_rates, 'diagnostics': diagnostics, 'source_provenance': provenance[cid],
                             'reported_resources': reported, 'recorded_run_at': recorded_run_at, 'prediction_ref': ref})
            total = pooled(mode, [row['counts'] for row in rows])
            primary_rates, list_rates = rates(mode, total)
            results.append({'run': run['id'], 'model': run['model'], 'interface': run['interface'], 'method': run['method'],
                            'configuration': run['configuration'], 'recipe': run['recipe'], 'ran_at': run['ran_at'],
                            'provenance': run['provenance'], 'cohort': api.digest(api.encoded(cohort)), 'tag_key_kind': mode,
                            'family': family, 'split': split, 'evidence': evidence, 'case_count': len(ids),
                            'not_attempted': sorted(set(cases) - set(attempted)), 'rows': rows, 'counts': total,
                            'metrics': primary_rates, 'by_list_metrics': list_rates})
    groups = defaultdict(list)
    for result in results:
        grouping = {key: result[key] for key in ('cohort', 'model', 'interface', 'method', 'configuration', 'recipe')}
        groups[api.digest(api.encoded(grouping))].append(result)
    def repeat_summary(values):
        finite = [value for value in values if value is not None]
        return {'mean': statistics.mean(finite) if finite else None, 'min': min(finite) if finite else None,
                'max': max(finite) if finite else None, 'stdev': statistics.stdev(finite) if len(finite) > 1 else None,
                'defined_replicates': len(finite), 'total_replicates': len(values)}
    summary = []
    for group_id, repeats in sorted(groups.items()):
        first = repeats[0]
        row = {key: first[key] for key in ('model', 'interface', 'method', 'configuration', 'cohort', 'tag_key_kind',
                                          'family', 'split', 'evidence', 'case_count')}
        row.update(group=group_id, runs=[r['run'] for r in repeats], replicates=len(repeats),
                   metrics={name: repeat_summary([r['metrics'][name] for r in repeats]) for name in first['metrics']},
                   by_list_metrics={label: {name: repeat_summary([r['by_list_metrics'][label][name] for r in repeats])
                                            for name in first['by_list_metrics'][label]} for label in first['by_list_metrics']})
        summary.append(row)
    return {'schema': 'task-benchmark-1', 'suite': suite['id'], 'suite_version': suite['version'], 'task': TASK,
            'registration': suite['registration'], 'scoring_contract': CONTRACT, 'suite_sha256': api.file_hash(suite_path),
            'code_sha256': code_hashes, 'hash_method': 'SHA256; declared text refs CRLF-to-LF; additional provenance raw SHA256 and byte counts',
            'case_total': len(cases), 'controls': known_controls, 'submissions': submissions, 'results': results, 'summary': summary,
            'limits': ['Geometry and partial-list modes have distinct denominators/cohorts and are never pooled.',
                       'Geometry reports strict/lenient tag recall and conditional found accuracy, not tag precision or F1.',
                       'Tag-list substring recall is partial coverage, not item assignment; class agreement is a derived found-identifier share.',
                       'Only comparable cohorts may be compared. Source/key/model metadata is declared, not authenticated engineering truth.',
                       'Missing/failed/invalid attempted answers retain full admitted truth denominators; unattempted cases remain visible.',
                       'Replicates summarize defined pooled rates with explicit defined/total counts; no significance test or winner.',
                       'Exposed historical/development registration and generated controls do not establish blindness or new source families.']}


def markdown(report):
    def safe(value):
        return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
    def fmt(value):
        return 'undefined' if value is None else f'{value:.4f}'
    lines = ['# Tag reading results: ' + safe(report['suite']), '', safe(report['registration']), '',
             'Task: `tag-reading` / `tag-text-v1`. Geometry and tag-list modes have separate denominators and cohorts.', '']
    for mode in MODES:
        lines += ['## ' + ('Geometry-keyed tag rates' if mode == 'geometry' else 'Partial-list identifier rates'), '',
                  ('Strict recall includes unfound labelled symbols; found accuracy is conditional on a matched symbol. '
                   'Lenient rates use the companion text normalization.' if mode == 'geometry' else
                   'Substring recall measures coverage of partial lists, without assigning identifiers to the correct item. '
                   'Class agreement is a share of found identifiers, not precision.'), '']
        for row in report['summary']:
            if row['tag_key_kind'] != mode:
                continue
            lines += ['### ' + safe(row['model']['id']), '',
                      '- **Provider / version:** ' + safe(row['model']['provider']) + ' / ' + safe(row['model']['version']),
                      '- **Method / client:** ' + safe(row['method']) + ' / ' + safe(row['interface']),
                      '- **Family / split / evidence:** ' + safe(row['family']) + ' / ' + safe(row['split']) + ' / ' + safe(row['evidence']),
                      '- **Cohort:** ' + safe(row['cohort']) + '; **group:** ' + safe(row['group']),
                      '- **Selected cases / repeats:** ' + str(row['case_count']) + ' / ' + str(row['replicates']),
                      '- **Configuration:** ' + safe(json.dumps(row['configuration'], ensure_ascii=True, sort_keys=True)), '',
                      '| Rate | Mean | Range | SD | Defined / total |',
                      '|---|---|---|---|---|']
            entries = list(row['metrics'].items()) + [(name + ' / list ' + label, values)
                for label, metrics in row['by_list_metrics'].items() for name, values in metrics.items()]
            for name, values in entries:
                fields = [name, fmt(values['mean']), fmt(values['min']) + '–' + fmt(values['max']),
                          fmt(values['stdev']), str(values['defined_replicates']) + ' / ' + str(values['total_replicates'])]
                lines.append('| ' + ' | '.join(safe(value) for value in fields) + ' |')
            lines.append('')
    lines += ['<details>', '<summary>Per-run counts and coverage (' + str(len(report['results'])) + ' run/cohort records)</summary>', '',
              '## Per-run primitive counts and coverage', '']
    for row in report['results']:
        lines.append('- ' + safe(row['run']) + ' / ' + row['tag_key_kind'] + ' / ' + safe(row['family']) + ': ' +
                     str(row['case_count']) + ' selected cases; counts ' + safe(json.dumps(row['counts'], ensure_ascii=True)) +
                     '; suite-wide unattempted: ' + safe(', '.join(row['not_attempted']) or 'none') + '.')
        for item in row['rows']:
            lines.append('  - ' + safe(item['case']) + ': ' + safe(item['status']) +
                         ('; ' + safe(item['note']) if item['note'] else '') + '.')
    lines += ['', '</details>', '', '## Limits', ''] + ['- ' + limit for limit in report['limits']] + ['']
    return '\n'.join(lines)
