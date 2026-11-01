"""Worked I04 partial-answer handoff. Stdlib, local files, no SDK or source fetching."""
import argparse
import copy
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]

def read(path):
    return json.loads(path.read_bytes())

def pin(path):
    raw = path.read_bytes()
    return {'sha256_raw': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def save(path, value):
    with path.open('xb') as stream:
        stream.write((json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode('utf-8'))

def typed(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(',', ':'))

def utc():
    return datetime.now(timezone.utc).isoformat()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True, help='new private output folder; never overwrite a prior run')
    args = parser.parse_args()
    out = args.out.resolve()
    if out.exists():
        parser.error('--out must be a new folder; retain earlier runs separately')
    provenance = read(HERE/'PROVENANCE.json')
    protected = [HERE/'PROVENANCE.json']
    for name, expected in provenance['files'].items():
        path = HERE/name
        if Path(name).is_absolute() or not path.resolve().is_relative_to(HERE) or pin(path) != expected:
            parser.error('example file checksum/path mismatch: '+name)
        protected.append(path)
    for name, expected in provenance['source_models'].items():
        path = ROOT/name
        if pin(path) != expected:
            parser.error('worked source model changed; review the example basis first: '+name)
        protected.append(path)
    scripts = ('question_engine.py', 'graph_export.py', 'graph_review_records.py',
               'context_register.py', 'serve_snapshot.py', 'output_paths.py')
    protected += [ROOT/'scripts'/name for name in scripts] + [ROOT/'data/questions.json']
    before = {str(path): pin(path) for path in protected}
    out.mkdir(parents=True)
    logs = out/'logs'
    logs.mkdir()
    save(out/'INPUTS-BEFORE.json', before)
    calls = []

    def cli(script, *arguments):
        number = len(calls)+1
        job = logs/f'{number:02d}-{script.removesuffix(".py")}'
        job.mkdir()
        argv = [sys.executable, '-B', '-S', str(ROOT/'scripts'/script), *map(str, arguments)]
        started = utc()
        save(job/'START.json', {'argv': argv, 'cwd': str(ROOT), 'start_utc': started})
        process = subprocess.Popen(argv, cwd=ROOT, env=dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1'),
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        save(job/'PROCESS.json', {'pid': process.pid})
        stdout, stderr = process.communicate()
        (job/'stdout.bin').write_bytes(stdout)
        (job/'stderr.bin').write_bytes(stderr)
        result = {'argv': argv, 'pid': process.pid, 'start_utc': started, 'end_utc': utc(),
                  'exit_code': process.returncode, 'stdout': pin(job/'stdout.bin'), 'stderr': pin(job/'stderr.bin')}
        calls.append(result)
        save(job/'RESULT.json', result)
        if process.returncode != 0:
            raise RuntimeError(f'{script} exited {process.returncode}; retain logs and diagnose before another run')

    sys.path.insert(0, str(ROOT/'scripts'))
    try:
        import graph_export as gx
        import context_register as cr
        from serve_snapshot import Snapshot
        gx.ROOT = ROOT
        catalog = ROOT/'data/questions.json'

        def screen(folder, model_raw):
            folder.mkdir()
            model = folder/'model.json'
            model.write_bytes(model_raw)
            cli('question_engine.py', '--model', model, '--question', 'C3', '--catalog', catalog, '--out', folder/'screen')
            questions = folder/'screen/questions.json'
            document = read(questions)
            assert [q['id'] for q in document['questions']] == ['C3@model']
            full = gx.build(model, questions=questions)
            assert gx.problems(full) == []
            core = gx.apply_profile(copy.deepcopy(full), 'core')
            assert gx.problems(core) == []
            assert typed(full['questions']) == typed(core['questions']) == typed(document['questions'])
            save(folder/'full.graph.json', full)
            save(folder/'core.graph.json', core)
            return model, questions, folder/'full.graph.json'

        def readback(folder, expected_state, expected_freshness):
            graph, register = read(folder/'enriched_graph.json'), read(folder/'context.json')
            cr.validate_export(graph, register)
            snapshot = Snapshot(folder/'enriched_graph.json', folder/'context.json')
            question = snapshot.question('C3@model')['result']
            current = snapshot.context_question('C3@model')['result']['current']
            assert typed(question) == typed(graph['questions'][0])
            assert typed(current) == typed(register['current']['C3@model'])
            assert current['state'] == expected_state
            assert current['answers'][0]['freshness'] == expected_freshness
            decisions, offset = [], 0
            while True:
                page = snapshot.decisions('C3@model', limit=1, offset=offset)['result']
                decisions += page['decisions']
                if page['next_offset'] is None:
                    break
                offset = page['next_offset']
            assert typed(decisions) == typed(register['decisions'])
            save(folder/'readback.json', {'question': question, 'current': current, 'decisions': decisions,
                                         'ownership_history': register['ownership_history']})
            return register

        raw = (ROOT/'examples/graph-export/unplaced-dexpi/i04.model.json').read_bytes()
        _, questions, graph = screen(out/'A', raw)
        source_a, source_b = HERE/'expected/r1/sources.json', HERE/'expected/r2/sources.json'
        prepared, current_a = out/'prepare-A', out/'current-A'
        cli('context_register.py', 'prepare', '--model', graph, '--questions', questions,
            '--sources', source_a, '--out', prepared)
        with (prepared/'evidence_choices.csv').open(encoding='utf-8', newline='') as stream:
            choices = list(csv.DictReader(stream))
        choice = next(row for row in choices if (row['question_id'], row['source_id'], row['locator_id']) ==
                      ('C3@model', 'N114-FICTIONAL-NOTE', 'command-limits'))
        row = {name: '' for name in cr.COLUMNS}
        row.update(read(HERE/'expected/answer-fields.json')['fields'], evidence_fingerprint=choice['evidence_fingerprint'])
        answers = out/'filled-fictional-answer.csv'
        with answers.open('x', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=cr.COLUMNS)
            writer.writeheader()
            writer.writerow(row)
        cli('context_register.py', 'apply', '--model', graph, '--questions', questions, '--sources', source_a,
            '--register', prepared/'context.json', '--answers', answers, '--out', current_a)
        original = readback(current_a, 'partial', 'current')
        assert original['decisions'][0]['plant_truth'] == 'unknown'
        source_out = out/'current-B-source'
        cli('context_register.py', 'apply', '--model', graph, '--questions', questions, '--sources', source_b,
            '--register', current_a/'context.json', '--out', source_out)
        source_changed = readback(source_out, 'unanswered', 'stale')
        changed_model = json.loads(raw)
        for operation in read(HERE/'expected/model-qualifier-revision.json')['patch']:
            parts = operation['path'].strip('/').split('/')
            target = changed_model
            for part in parts[:-1]:
                target = target[int(part)] if isinstance(target, list) else target[part]
            key = parts[-1]
            if operation['op'] == 'test':
                assert typed(target[key]) == typed(operation['value'])
            else:
                assert operation['op'] == 'replace'
                target[key] = copy.deepcopy(operation['value'])
        _, changed_questions, changed_graph = screen(out/'B-model', (json.dumps(changed_model, indent=2, ensure_ascii=False)+'\n').encode('utf-8'))
        model_out = out/'current-B-model'
        cli('context_register.py', 'apply', '--model', changed_graph, '--questions', changed_questions, '--sources', source_a,
            '--register', current_a/'context.json', '--out', model_out)
        model_changed = readback(model_out, 'unanswered', 'stale')
        for register in (source_changed, model_changed):
            for name in ('decisions', 'ownership_history'):
                assert typed(register[name]) == typed(original[name]), 'history changed: '+name
        after = {str(path): pin(path) for path in protected}
        assert after == before, 'selected source/example/method inputs changed during execution'
        save(out/'INPUTS-AFTER.json', after)
        generated = {p.relative_to(out).as_posix(): pin(p) for p in sorted(out.rglob('*')) if p.is_file()}
        save(out/'observed.json', {'pass': True, 'scope': 'I04 + fictional answer/source revisions; pure Snapshot API, no SDK/listener',
            'CLI_calls': calls, 'direct_readback_pairs': 3, 'states': {'A': 'partial/current',
            'B-source': 'unanswered/stale', 'B-tag-basis': 'unanswered/stale'},
            'history_unchanged': True, 'protected_inputs_unchanged': True, 'generated_files': generated})
        print('PASS: one fictional partial answer; two evidence changes reopen it; complete history retained.')
        return 0
    except Exception:
        save(out/'STOP.json', {'pass': False, 'calls': calls, 'error': traceback.format_exc(),
                              'protected_inputs_unchanged': all(pin(Path(path)) == value for path, value in before.items())})
        raise

if __name__ == '__main__':
    raise SystemExit(main())
