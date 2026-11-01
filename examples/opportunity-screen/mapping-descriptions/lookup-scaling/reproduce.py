"""Generate fictional I/O inputs and count capture/lookup record visits for one selected local method.

Standard library only. This diagnostic imports the supplied local toolkit code; it does not fetch methods,
change versions, call models or contact a plant. Outputs go to a new folder. See README.md for metric limits.
"""
import argparse
import ast
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def csv_line(values):
    stream = io.StringIO(newline='')
    csv.writer(stream, lineterminator='\r\n').writerow(values)
    return stream.getvalue().encode('utf-8')


def generate(inputs):
    """Same case/model/CSV/catalog bytes as the frozen original study; no product calls here."""
    question = {'id': 'IO1', 'family': 'metering', 'question': 'Fictional lookup control; no engineering finding.',
        'applies_when': {'anchor': {'kind': ['instrument'], 'variable': ['flow']}, 'group_by': 'item'},
        'evidence_fields': ['tag'], 'data_requests': [{'item': 'Supplied flow record',
        'how': 'Inspect the selected source context.', 'where': [{'place': 'historian', 'quantity': 'flow'}]}],
        'decision_rule': 'Review the supplied record; no operating action.',
        'typical_benefit': {'wording': 'No engineering benefit claimed for fictional controls.', 'source': [], 'arc': None},
        'limits': 'Synthetic exposed development; no plant capacity or model accuracy result.'}
    put(inputs / 'catalog.json', {'families': {'metering': 'Metering'}, 'sources': {}, 'questions': [question]})
    cases = []
    for count, mixed in ((32, False), (128, False), (512, False), (128, True)):
        name = f'n{count:04d}' + ('-mixed-two-sources' if mixed else '-modern')
        folder = inputs / name
        (folder / 'a').mkdir(parents=True)
        (folder / 'b').mkdir()
        raw = bytearray(b'\xef\xbb\xbf' + csv_line(['tag', 'server', 'base_path', 'point', 'asset_id', 'description']))
        physical, logical, instruments, expected = 1, 1, [], []
        for number in range(count):
            if number and number % 17 == 0:
                raw.extend(b'\r\n')
                physical += 1
                logical += 1
            description = f'SYNTHETIC source record {number:04d}' + ('\r\nsecond physical line' if number % 7 == 0 else '')
            record = csv_line([f'ft_{number:04d}', 'Fixture-Only', 'ns=2;s=FICT', f'P{number:04d}',
                               f'I-{number:04d}' if number % 2 == 0 else '', description])
            first = physical + 1
            physical += record.count(b'\n')
            logical += 1
            raw.extend(record)
            point = {'server': 'Fixture-Only', 'base_path': 'ns=2;s=FICT', 'point': f'P{number:04d}',
                     'source': f'io.csv line {first}' if first == physical else f'io.csv lines {first}-{physical}',
                     'source_lines': [first, physical]}
            legacy = mixed and number % 2 == 0
            if legacy:
                point = {key: point[key] for key in ('server', 'base_path', 'point')}
                point['source'] = f'io.csv row {logical}'
            instruments.append({'id': f'I-{number:04d}', 'tag': f'FT-{number:04d}', 'isa_letters': 'FT',
                                'variable': 'flow', 'provenance': [{'sheet': '0'}], 'data_point': point})
            expected.append({'asset_id': f'I-{number:04d}', 'status': 'unavailable' if legacy else 'matched',
                             'description': None if legacy else description})
        first_source = folder / 'a/io.csv'
        first_source.write_bytes(raw)
        raw_hash = digest(first_source)
        for item in instruments:
            if 'source_lines' in item['data_point']:
                item['data_point']['source_sha256'] = raw_hash
        sources = [first_source]
        if mixed:
            second_source = folder / 'b/io.csv'
            second_source.write_bytes(bytes(raw).replace(b'SYNTHETIC source record', b'SYNTHETIC SECOND record'))
            sources.append(second_source)
        put(folder / 'model.json', {'meta': {'model_kind': 'extracted_twin',
            'title': 'Fictional source lookup scaling control'}, 'units': [], 'instruments': instruments})
        put(folder / 'expected.json', expected)
        cases.append({'id': name, 'records_per_source': count, 'queries': count,
                      'sources': [p.relative_to(inputs).as_posix() for p in sources],
                      'model': f'{name}/model.json', 'expected': f'{name}/expected.json'})
    return cases


def run(root, method, out):
    if out.exists() or out.is_symlink():
        raise ValueError('--out must be a new folder')
    if not out.parent.is_dir():
        raise ValueError('--out parent must already exist')
    support = [root / 'scripts/graph_export.py', root / 'scripts/context_register.py']
    for path in [method, *support]:
        if not path.is_file():
            raise ValueError(f'local method/support file missing: {path.name}')
    # Fail before imports if the two declared instrumentation sites are not identifiable.
    tree = ast.parse(method.read_text(encoding='utf-8'))
    parser = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'load_io_sources')
    resolver = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'point_description')
    appends = [n for n in ast.walk(parser) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
               and isinstance(n.value.func, ast.Attribute) and isinstance(n.value.func.value, ast.Name)
               and n.value.func.value.id == 'records' and n.value.func.attr == 'append']
    visit_lines = {n.body[0].lineno for n in ast.walk(resolver)
                   if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == 'record'}
    if len(appends) != 1 or len(visit_lines) != 1:
        raise ValueError('method does not expose the declared capture/record-loop metric; revise protocol first')
    out.mkdir()
    inputs = out / 'inputs'
    inputs.mkdir()
    cases = generate(inputs)
    pins = {p.relative_to(inputs).as_posix(): digest(p) for p in inputs.rglob('*') if p.is_file()}
    put(out / 'PRECALL.json', {'method_sha256_raw': digest(method),
        'support': [{'file': p.name, 'sha256_raw': digest(p)} for p in support],
        'harness_sha256_raw': digest(Path(__file__)), 'input_pins': pins, 'cases': cases,
        'metric': 'CPython C-profile records.append calls during capture plus record-loop body entries during lookup; selected raw source reads counted separately.'})
    sys.path.insert(0, str(root / 'scripts'))
    spec = importlib.util.spec_from_file_location('measured_question_engine', method)
    qe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qe)
    import graph_export as gx
    import context_register as cr
    qe.ROOT = inputs
    gx.ROOT = inputs
    catalog = json.loads((inputs / 'catalog.json').read_bytes())
    results = []
    for case in cases:
        target = out / case['id']
        target.mkdir()
        counts = {'capture_record_visits': 0, 'lookup_record_visits': 0, 'selected_source_reads': 0}
        paths = {str((inputs / p).resolve()) for p in case['sources']}
        read_bytes = Path.read_bytes
        previous_trace, previous_profile = sys.gettrace(), sys.getprofile()

        def read(path):
            if str(path.resolve()) in paths:
                counts['selected_source_reads'] += 1
            return read_bytes(path)

        def trace(frame, event, _arg):
            if (event == 'line' and frame.f_code.co_filename == str(method)
                    and frame.f_code.co_name == 'point_description' and frame.f_lineno in visit_lines):
                counts['lookup_record_visits'] += 1
            return trace

        def profile(frame, event, arg):
            if (event == 'c_call' and frame.f_code.co_filename == str(method)
                    and frame.f_code.co_name == 'load_io_sources' and getattr(arg, '__name__', None) == 'append'
                    and getattr(arg, '__self__', None) is frame.f_locals.get('records')):
                counts['capture_record_visits'] += 1

        Path.read_bytes = read
        sys.setprofile(profile)
        sys.settrace(trace)
        try:
            model = qe.Model(inputs / case['model'], io_paths=[inputs / p for p in case['sources']])
        finally:
            sys.settrace(previous_trace)
            sys.setprofile(previous_profile)
            Path.read_bytes = read_bytes
        found, not_checked, quiet, excluded = qe.screen(model, catalog)
        doc = qe.write_outputs(model, catalog, found, not_checked, quiet, excluded, target / 'screen',
                               catalog_path=inputs / 'catalog.json')
        graph = gx.build(inputs / case['model'], questions=target / 'screen/questions.json')
        put(target / 'graph-full.json', graph)
        put(target / 'graph-core.json', gx.apply_profile(graph, 'core'))
        _, _, keyed = cr.bind_inputs(graph, doc)
        put(target / 'context-basis.json', keyed)
        put(target / 'descriptions.json', model.mapping_descriptions)
        put(target / 'signals.json', {item['id']: item.get('signal') for item in model.items})
        expected = json.loads((inputs / case['expected']).read_bytes())
        checks = {'all_queries': len(doc['questions']) == case['queries'],
            'source_reads_once': counts['selected_source_reads'] == len(case['sources']),
            'captured_rows': counts['capture_record_visits'] == case['records_per_source'] * len(case['sources']),
            'expected_statuses_and_text': len(model.mapping_descriptions) == len(expected) and all(
                actual['asset_id'] == wanted['asset_id'] and actual['status'] == wanted['status']
                and actual.get('description') == wanted['description']
                for actual, wanted in zip(model.mapping_descriptions, expected))}
        counts['total_record_visits'] = counts['capture_record_visits'] + counts['lookup_record_visits']
        files = {p.relative_to(target).as_posix(): digest(p) for p in target.rglob('*') if p.is_file()}
        result = {'case': case['id'], 'pass': all(checks.values()), 'counts': counts, 'checks': checks, 'files': files}
        put(target / 'RESULT.json', result)
        results.append(result)
    result = {'pass': all(r['pass'] for r in results), 'method_sha256_raw': digest(method),
        'inputs_unchanged': all(digest(inputs / p) == h for p, h in pins.items()), 'results': results}
    result['pass'] = result['pass'] and result['inputs_unchanged']
    put(out / 'RESULT.json', result)
    print(json.dumps({'pass': result['pass'], 'cases': [{k: r[k] for k in ('case', 'counts')} for r in results]}))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', type=Path, required=True, help='local toolkit root for stdlib support modules')
    parser.add_argument('--method', type=Path, required=True, help='selected question_engine.py; relative to --root')
    parser.add_argument('--out', type=Path, required=True, help='new output folder; relative to current directory')
    args = parser.parse_args()
    root = args.root.resolve()
    method = args.method.resolve() if args.method.is_absolute() else (root / args.method).resolve()
    try:
        raise SystemExit(run(root, method, args.out.resolve()))
    except (OSError, ValueError, StopIteration) as error:
        parser.exit(2, f'lookup study refused/stopped: {error}\n')
