"""Reproduce fictional typed-context controls with a selected local method; stdlib, no SDK/network."""
import argparse
import copy
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def read(path):
    return json.loads(path.read_bytes())


def save(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode('utf-8'))


def pin(path):
    raw = path.read_bytes()
    return {'sha256_raw': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def history(register):
    return canonical({key: register[key] for key in ('decisions', 'ownership_history')})


def summary(register):
    return {qid: {'state': row['state'], 'owner': row['owner'], 'answers': row['answers']}
            for qid, row in register['current'].items()}


def mutate(document, pointer, value):
    parts = pointer.strip('/').split('/')
    current = document
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    key = int(parts[-1]) if isinstance(current, list) else parts[-1]
    current[key] = copy.deepcopy(value)


def reordered(value):
    if isinstance(value, dict):
        return {key: reordered(value[key]) for key in reversed(value)}
    if isinstance(value, list):
        return [reordered(item) for item in value]
    return value


def validate_packet(parser):
    """Check only this committed example's declared files; no output or product calls."""
    try:
        manifest = HERE/'PROVENANCE.json'
        declared = read(manifest)['files']
        if type(declared) is not dict or not declared:
            raise ValueError('PROVENANCE.files must be a nonempty object')
        paths = [manifest]
        for name, expected in declared.items():
            if type(name) is not str or not name or Path(name).is_absolute():
                raise ValueError('declared file names must be relative paths')
            path = HERE/name
            if not path.resolve().is_relative_to(HERE.resolve()) or not path.is_file():
                raise ValueError('declared path must be a file within the example: '+name)
            if (type(expected) is not dict or set(expected) != {'sha256_raw', 'bytes'}
                    or type(expected['bytes']) is not int or expected['bytes'] < 0
                    or type(expected['sha256_raw']) is not str):
                raise ValueError('invalid declared pin for '+name)
            if pin(path) != expected:
                raise ValueError('checksum/size mismatch for '+name)
            paths.append(path)
        return paths
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        parser.error('typed-evidence packet provenance check failed: '+str(exc))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='toolkit checkout supplying shared modules')
    parser.add_argument('--method', type=Path, help='selected local context_register.py; no checkout or download')
    parser.add_argument('--out', type=Path, required=True, help='new private output directory outside the checkout')
    parser.add_argument('--expect', choices=('original', 'repaired'), default='repaired')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    method = (args.method or root/'scripts/context_register.py').resolve()
    destination = args.out.resolve()
    if not method.is_file() or destination.exists() or os.path.lexists(destination):
        parser.error('method must be a regular local file and --out must not exist')
    if not destination.parent.is_dir() or destination.is_relative_to(root):
        parser.error('--out needs an existing private parent outside the checkout')
    packet_paths = validate_packet(parser)
    shared_paths = [root/'scripts'/name for name in
                    ('graph_export.py', 'graph_review_records.py', 'serve_snapshot.py', 'output_paths.py')]
    captured_paths = [method, *shared_paths, *packet_paths]
    before_pins = {str(path): pin(path) for path in captured_paths}
    cases = read(HERE/'cases.json')
    expected = read(HERE/'expected.json')[args.expect]
    destination.mkdir()
    work = destination/'work'
    work.mkdir()
    env = dict(os.environ, PYTHONPATH=str(root/'scripts'), PYTHONDONTWRITEBYTECODE='1')
    jobs, observations = [], []
    result = {'pass': False, 'expectation': args.expect, 'method': pin(method), 'jobs': jobs,
              'cases': observations, 'scope': 'Fictional local software binding; no SDK, source fetch or plant acceptance.',
              'precall_source_pins': before_pins}
    save(destination/'precall.json', {'selected_method': str(method), 'expectation': args.expect,
                                    'source_pins': before_pins, 'planned_CLI_calls': 14,
                                    'valid_pair_controls': 7, 'bad_pair_controls': 2, 'SDK_calls': 0})

    def cli(label, inputs, action, output, register=None, answers=None, wanted=0):
        command = [sys.executable, '-B', '-S', str(method), action, '--model', str(inputs/'model.json'),
                   '--questions', str(inputs/'questions.json'), '--sources', str(inputs/'sources.json'), '--out', str(output)]
        if register is not None:
            command += ['--register', str(register)]
        if answers is not None:
            command += ['--answers', str(answers)]
        log = destination/(label+'.log')
        start = datetime.now(timezone.utc).isoformat()
        input_pins = {name: pin(inputs/name) for name in ('model.json', 'questions.json', 'sources.json',
                                                        'manual.txt', 'schedule.txt')}
        with log.open('xb') as stream:
            process = subprocess.Popen(command, cwd=work, env=env, stdout=stream, stderr=subprocess.STDOUT)
            process_info = {'label': label, 'argv': command, 'cwd': str(work), 'pid': process.pid,
                            'start_utc': start, 'input_pins': input_pins}
            save(destination/(label+'-process.json'), process_info)
            code = process.wait()
        jobs.append(dict(process_info, end_utc=datetime.now(timezone.utc).isoformat(), exit_code=code,
                         log=log.name, log_pin=pin(log)))
        save(destination/(label+'-result.json'), jobs[-1])
        if code != wanted:
            raise AssertionError(f'{label}: exit {code}, expected {wanted}; inspect {log.name}')
        if wanted == 2:
            assert 'stale or missing evidence_fingerprint' in log.read_text(encoding='utf-8'), label

    seed = work/'seed'
    input_pins = {}
    try:
        shutil.copytree(HERE/'inputs', seed)
        input_pins = {path.name: pin(path) for path in seed.iterdir()}
        result['inputs'] = input_pins
        cli('seed-prepare', seed, 'prepare', seed/'prepared')
        with (seed/'prepared/evidence_choices.csv').open(encoding='utf-8', newline='') as stream:
            choices = {(r['question_id'], r['source_id'], r['locator_id']): r['evidence_fingerprint']
                       for r in csv.DictReader(stream)}
        with (seed/'filled.csv').open(encoding='utf-8', newline='') as stream:
            for row in csv.DictReader(stream):
                assert row['evidence_fingerprint'] == choices[(row['question_id'], row['source_id'], row['locator_id'])]
        cli('seed-accepted', seed, 'apply', seed/'accepted', seed/'prepared/context.json', seed/'filled.csv')
        # Read-only application APIs only: no SDK transport/server starts here.
        sys.path.insert(0, str(root/'scripts'))
        spec = importlib.util.spec_from_file_location('context_register', method)
        selected = importlib.util.module_from_spec(spec)
        sys.modules['context_register'] = selected
        spec.loader.exec_module(selected)
        import serve_snapshot

        def valid_pair(label, output, register):
            graph = read(output/'enriched_graph.json')
            selected.validate_export(graph, register)
            packet = serve_snapshot.Snapshot(output/'enriched_graph.json', output/'context.json')
            readback = {'current': {}, 'ownership_history': {}, 'decisions': None}
            for qid, current in register['current'].items():
                response = packet.context_question(qid)
                assert canonical(response['result']['current']) == canonical(current), (label, qid)
                ownership = [row for row in register['ownership_history'] if row['question_id'] == qid]
                assert canonical(response['result']['ownership_history']) == canonical(ownership), (label, qid)
                readback['current'][qid] = response
                readback['ownership_history'][qid] = ownership
            response = packet.decisions(limit=50)
            assert response['result']['next_offset'] is None, label
            assert canonical(response['result']['decisions']) == canonical(register['decisions']), label
            readback['decisions'] = response
            path = destination/(label+'-valid-readback.json')
            save(path, readback)
            return {'path': path.name, 'pin': pin(path), 'current_and_full_history_typed_exact': True}
        accepted = read(seed/'accepted/context.json')
        assert all(r['state'] == 'answered' for r in accepted['current'].values())
        result['seed_valid_readback'] = valid_pair('seed', seed/'accepted', accepted)
        for case in cases['cases']:
            folder = work/case['id']
            shutil.copytree(HERE/'inputs', folder)
            model, questions = read(folder/'model.json'), read(folder/'questions.json')
            documents = {'model.json': model, 'questions.json': questions}
            for change in case['mutations']:
                mutate(documents[change['document']], change['pointer'], change['value'])
            if case.get('reverse_object_keys'):
                documents = {key: reordered(value) for key, value in documents.items()}
            for name, value in documents.items():
                save(folder/name, value)
            output = folder/'refreshed'
            cli(case['id'], folder, 'apply', output, seed/'accepted/context.json')
            register = read(output/'context.json')
            assert history(register) == history(accepted), case['id']+' changed retained history'
            observed = {'case': case['id'], 'current': summary(register), 'history_typed_exact': True,
                        'outputs': {p.name: pin(p) for p in output.iterdir() if p.is_file()}}
            observed['valid_readback'] = valid_pair(case['id'], output, register)
            observations.append(observed)
            wanted = expected[case['id']]
            for qid, state in wanted.items():
                assert register['current'][qid]['state'] == state['state'], (case['id'], qid)
                assert [a['freshness'] for a in register['current'][qid]['answers']] == state['freshness'], (case['id'], qid)
            if case.get('old_csv_refuses'):
                sentinel = folder/'old-csv'
                sentinel.mkdir()
                (sentinel/'keep.txt').write_bytes(b'retain existing output\n')
                before = {p.name: pin(p) for p in sentinel.iterdir()}
                cli(case['id']+'-old-csv', folder, 'apply', sentinel,
                    seed/'accepted/context.json', seed/'filled.csv', wanted=2)
                assert {p.name: pin(p) for p in sentinel.iterdir()} == before
            if case.get('exact_reversion'):
                cli('TF06-reversion', seed, 'apply', folder/'reverted', output/'context.json')
                reverted = read(folder/'reverted/context.json')
                assert all(r['state'] == 'answered' for r in reverted['current'].values())
                assert history(reverted) == history(accepted)
                observed['exact_reversion_current'] = True
        # Conflicting pair controls complement the seven valid pair readbacks above.
        result['validators'] = {}
        for label in ('V01', 'V02'):
            graph, register = read(seed/'accepted/enriched_graph.json'), copy.deepcopy(accepted)
            if label == 'V01':
                register['current']['Q1@P-1']['question']['data_requests'][0]['candidate_facts'][0]['value'] = 1
                graph['context_register']['content_sha256'] = hashlib.sha256(canonical(register).encode('utf-8')).hexdigest()
            else:
                graph['questions'][0]['context']['question']['data_requests'][0]['candidate_facts'][0]['value'] = 1
            folder = work/label
            folder.mkdir()
            save(folder/'graph.json', graph)
            save(folder/'context.json', register)
            admitted, refusals = [], []
            intended = 'current state' if label == 'V01' else 'question context'
            calls = ((lambda: selected.validate_export(graph, register), selected.InputError),
                     (lambda: serve_snapshot.Snapshot(folder/'graph.json', folder/'context.json'), serve_snapshot.InputError))
            for call, expected_error in calls:
                try:
                    call()
                except expected_error as exc:
                    assert intended in str(exc), (label, 'unrelated refusal', str(exc))
                    admitted.append(False)
                    refusals.append({'type': type(exc).__name__, 'message': str(exc)})
                else:
                    admitted.append(True)
            result['validators'][label] = {'admitted': admitted, 'refusals': refusals}
            assert admitted == ([True, True] if args.expect == 'original' else [False, False]), label
        result['pass'] = True
    finally:
        after_pins = {str(path): pin(path) for path in captured_paths}
        result['source_pins_after'] = after_pins
        result['captured_sources_unchanged'] = after_pins == before_pins
        result['copied_seed_inputs_unchanged'] = all(pin(seed/name) == value for name, value in input_pins.items())
        if not result['captured_sources_unchanged'] or not result['copied_seed_inputs_unchanged']:
            result['pass'] = False
        save(destination/'observed.json', result)
        assert result['captured_sources_unchanged'] and result['copied_seed_inputs_unchanged'], 'captured input/method bytes changed'
    print('PASS fictional typed-evidence controls; complete local outputs retained; no engineering/client acceptance claimed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
