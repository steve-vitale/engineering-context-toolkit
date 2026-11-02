"""Fixed fictional engineering-change tutorial; existing tools, no server or plant connection."""
from pathlib import Path
import argparse
import copy
import csv
import hashlib
import io
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = value if isinstance(value, bytes) else (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(raw)


def require(value, message):
    if not value:
        raise ValueError(message)


def inventory(folder):
    return {p.relative_to(folder).as_posix(): sha(p) for p in sorted(folder.rglob('*')) if p.is_file()}


def utc():
    return datetime.now(timezone.utc).isoformat()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=HERE.parents[1])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    require((root / 'scripts/description_workflow.py').is_file(), 'Select the toolkit with --root')
    require(not out.exists() and out.parent.is_dir() and not out.is_relative_to(root)
            and not out.is_relative_to(HERE), 'Choose a new output folder outside the toolkit and this example')
    frozen = inventory(HERE / 'inputs')
    custody = {'runner': sha(Path(__file__).resolve()), 'acceptance_key': sha(HERE / 'ACCEPTANCE.json'),
               'default_catalog': sha(root / 'data/questions.json')}
    code_names = ['description_workflow.py', 'draw_pid_from_model.py', 'generate.py', 'question_engine.py',
                  'graph_export.py', 'context_register.py', 'serve_snapshot.py', 'graph_review_records.py', 'output_paths.py']
    code = {name: sha(root / 'scripts' / name) for name in code_names}
    key = read(HERE / 'ACCEPTANCE.json')
    jobs, checks = [], []
    out.mkdir()
    (out / 'tmp').mkdir()
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', TEMP=str(out / 'tmp'), TMP=str(out / 'tmp'))
    save(out / 'START.json', {'utc': utc(), 'argv': sys.argv, 'pid': os.getpid(), 'code_sha256_raw': code,
                             'source_sha256_raw': frozen, 'custody_sha256_raw': custody})

    def check(label, value):
        require(value, label)
        checks.append(label)

    def run(label, script, tail, expected=0):
        folder = out / 'jobs' / label
        folder.mkdir(parents=True)
        command = [sys.executable, '-B', str(root / 'scripts' / script)] + [str(v) for v in tail]
        save(folder / 'START.json', {'utc': utc(), 'argv': command, 'expected_exit': expected})
        with (folder / 'stdout.bin').open('xb') as stdout, (folder / 'stderr.bin').open('xb') as stderr:
            child = subprocess.Popen(command, cwd=root, env=env, stdout=stdout, stderr=stderr)
            save(folder / 'CHILD.json', {'pid': child.pid, 'parent_pid': os.getpid()})
            try:
                status = child.wait(timeout=120)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
                save(folder / 'TIMEOUT.json', {'pid': child.pid, 'limit_seconds': 120, 'exit': child.returncode})
                raise ValueError(label + ' exceeded the fixed-example 120-second command limit')
        item = {'job': label, 'exit': status, 'expected_exit': expected, 'pid': child.pid, 'end_utc': utc()}
        jobs.append(item)
        save(folder / 'RESULT.json', item)
        require(status == expected, label + ' unexpected exit; inspect retained stdout/stderr')
        return folder

    failure = None
    try:
        for rev in ['A', 'B']:
            folder = out / rev
            folder.mkdir()
            inputs = HERE / 'inputs' / rev
            run(rev + '-prepare', 'description_workflow.py', ['prepare', '--source', inputs / 'source.txt', '--out', folder / 'packet'])
            run(rev + '-check', 'description_workflow.py', ['check', '--packet', folder / 'packet', '--answer', inputs / 'answer.json'])
            run(rev + '-build', 'description_workflow.py', ['build', '--packet', folder / 'packet', '--answer', inputs / 'answer.json', '--out', folder / 'build'])
            check(rev + ' retained exact selected catalog', sha(folder / 'build/question_catalog.json') == custody['default_catalog'])
            model = read(folder / 'build/model.json')
            expected = key['expected'][rev]
            check(rev + ' exact equipment identities', [u['id'] for u in model['units']] == expected['equipment_ids'])
            check(rev + ' exact directed stream endpoints', [[s['id'], s['from'], s['to']] for s in model['streams']] == expected['stream_endpoints'])
            check(rev + ' no invented instruments, final elements or controllers', all(model[k] == [] for k in ['instruments', 'final_elements', 'controllers']))
            tags = read(folder / 'build/exports/ignition/tags.json')
            instances = next(t for t in tags['tags'] if t['name'] == model['meta']['model_id'])['tags']
            check(rev + ' exact Ignition staging equipment identities', [t['name'] for t in instances] == expected['equipment_ids'])
            check(rev + ' empty signal templates are not live mappings', all(t['tags'] == [] for t in next(t for t in tags['tags'] if t['name'] == '_types_')['tags']))
            with (folder / 'build/exports/pi/pi_builder_af.csv').open(encoding='utf-8-sig', newline='') as stream:
                af = list(csv.DictReader(stream))
            check(rev + ' exact PI staging equipment identities', [r['Name'] for r in af if r['ObjectType'] == 'Element' and r['Parent'] == model['meta']['model_id']] == expected['equipment_ids'])
            generated = read(folder / 'build/questions/questions.json')
            actual_ids = [q['id'] for q in generated['questions']]
            check(rev + ' exact generated question identities', actual_ids == expected['generated_question_ids'])
            machine_review = next(q for q in generated['questions'] if q['id'] == 'C9@model')
            check(rev + ' exact machines in grouped record review', [a['id'] for a in machine_review['assets']] == expected['generated_machine_review_assets'])
            manual = read(HERE / 'inputs/questions.json')
            composed = copy.deepcopy(generated)
            composed['questions'] += copy.deepcopy(manual['questions'])
            composed['demo_composition'] = {'generated_ids': [q['id'] for q in generated['questions']],
                                          'authored_ids': [q['id'] for q in manual['questions']],
                                          'scope': 'Authored follow-ups are not catalog findings.'}
            save(folder / 'questions.json', composed)
            run(rev + '-context-prepare', 'context_register.py', ['prepare', '--model', folder / 'build/graph.json', '--questions', folder / 'questions.json',
                '--sources', inputs / 'sources.json', '--source-root', inputs, '--out', folder / 'prepared'])

        # These negative inputs are disposable copies; keep both original revisions intact.
        old_model_log = run('refuse-old-model-on-B', 'description_workflow.py', ['check', '--packet', out / 'B/packet', '--answer', HERE / 'inputs/A/answer.json'], 2)
        check('old model refusal names source identity mismatch', 'exact prepared source_sha256' in (old_model_log / 'stdout.bin').read_text(encoding='utf-8'))
        wrong = copy.deepcopy(read(HERE / 'inputs/B/answer.json'))
        next(s for s in wrong['model']['streams'] if s['id'] == 'S5')['to'] = 'P-1'
        save(out / 'wrong-endpoint.json', wrong)
        wrong_log = run('refuse-wrong-topology', 'description_workflow.py', ['check', '--packet', out / 'B/packet', '--answer', out / 'wrong-endpoint.json'], 2)
        check('wrong topology refusal names directed endpoint mismatch', 'resolves to BL' in (wrong_log / 'stdout.bin').read_text(encoding='utf-8'))
        wrong_destination = out / 'refused-wrong-build'
        run('refuse-wrong-build', 'description_workflow.py', ['build', '--packet', out / 'B/packet', '--answer', out / 'wrong-endpoint.json', '--out', wrong_destination], 2)
        check('wrong topology build refuses before output writes', not wrong_destination.exists())

        with (out / 'A/prepared/evidence_choices.csv').open(encoding='utf-8', newline='') as stream:
            choices = list(csv.DictReader(stream))
        recipe = read(HERE / 'inputs/answer.recipe.json')
        matches = [c for c in choices if all(c[k] == recipe[k] for k in ['question_id', 'source_id', 'locator_id'])]
        check('exact one source choice for fictional partial proposal', len(matches) == 1)
        with (out / 'A/prepared/answers.csv').open(encoding='utf-8', newline='') as stream:
            header = csv.DictReader(stream).fieldnames
        answer = {k: recipe.get(k, '') for k in header}
        answer['evidence_fingerprint'] = matches[0]['evidence_fingerprint']
        text = io.StringIO(newline='')
        writer = csv.DictWriter(text, fieldnames=header, lineterminator='\n')
        writer.writeheader()
        writer.writerow(answer)
        save(out / 'fictional-partial.csv', text.getvalue().encode())
        old_answer_sha = sha(out / 'fictional-partial.csv')

        def context_args(rev):
            return ['--model', out / rev / 'build/graph.json', '--questions', out / rev / 'questions.json',
                    '--sources', HERE / 'inputs' / rev / 'sources.json', '--source-root', HERE / 'inputs' / rev]

        run('A-retain-partial', 'context_register.py', ['apply'] + context_args('A') + ['--register', out / 'A/prepared/context.json',
            '--answers', out / 'fictional-partial.csv', '--out', out / 'A/context'])
        run('B-explicit-refresh', 'context_register.py', ['apply'] + context_args('B') + ['--register', out / 'A/context/context.json', '--out', out / 'B/context'])
        a, b = read(out / 'A/context/context.json'), read(out / 'B/context/context.json')
        qid = key['retained_answer']['id']
        check('A source summary is partial, proposed and plant truth unknown', a['current'][qid]['state'] == 'partial'
              and len(a['decisions']) == 1 and a['decisions'][0]['decision'] == 'proposed' and a['decisions'][0]['plant_truth'] == 'unknown')
        check('B source revision reopens prior arrangement answer', b['current'][qid]['state'] == 'unanswered'
              and b['current'][qid]['answers'][0]['freshness'] == 'stale'
              and 'source revision/bytes/locator' in b['current'][qid]['answers'][0]['changed'])
        check('complete decision and owner history retained', a['decisions'] == b['decisions']
              and len(a['ownership_history']) == 1 and a['ownership_history'] == b['ownership_history'])
        check('B grouped machine-record review and authored operability review remain unanswered', b['current']['C9@model']['state'] == 'unanswered'
              and b['current']['OPERABILITY@P-1']['state'] == 'unanswered')
        refused = out / 'refused-old-answer'
        old_log = run('refuse-old-context-answer', 'context_register.py', ['apply'] + context_args('B') + [
            '--register', out / 'A/context/context.json', '--answers', out / 'fictional-partial.csv', '--out', refused], 2)
        check('old answer refuses before output writes', not refused.exists()
              and 'stale or missing evidence_fingerprint' in (old_log / 'stderr.bin').read_text(encoding='utf-8'))
        check('old answer fingerprint never restamped', sha(out / 'fictional-partial.csv') == old_answer_sha)

        # Pure in-process reader only: no SDK, server creation, transport, or listener.
        sys.path.insert(0, str(root / 'scripts'))
        import serve_snapshot
        check('selected Snapshot implementation', Path(serve_snapshot.__file__).resolve() == root / 'scripts/serve_snapshot.py')
        for rev, register in [('A', a), ('B', b)]:
            graph_path, context_path = out / rev / 'context/enriched_graph.json', out / rev / 'context/context.json'
            graph = read(graph_path)
            snapshot = serve_snapshot.Snapshot(graph_path, context_path)
            check(rev + ' complete selected graph and context loaded', snapshot.graph == graph and snapshot.context == register)
            payload = {'summary': snapshot.summary(), 'assets': {uid: snapshot.asset(uid) for uid in key['expected'][rev]['equipment_ids']},
                       'questions': {q['id']: snapshot.question(q['id']) for q in graph['questions']},
                       'context': {qid: snapshot.context_question(qid) for qid in register['current']}, 'decisions': snapshot.decisions('', 50, 0)}
            for uid, envelope in payload['assets'].items():
                check(rev + '/' + uid + ' complete asset readback', envelope['result'] == next(n for n in graph['nodes'] if n['id'] == uid))
            for question_id, envelope in payload['questions'].items():
                check(rev + '/' + question_id + ' complete question readback', envelope['result'] == next(q for q in graph['questions'] if q['id'] == question_id))
                wanted = {'question_id': question_id, 'current': register['current'][question_id],
                          'ownership_history': [r for r in register['ownership_history'] if r['question_id'] == question_id],
                          'sources': [dict(src, locators=[loc for loc in src['locators'] if question_id in loc['questions']])
                                      for src in register['sources'] if any(question_id in loc['questions'] for loc in src['locators'])]}
                check(rev + '/' + question_id + ' complete context and source readback', payload['context'][question_id]['result'] == wanted)
            check(rev + ' complete decision readback', payload['decisions']['result']['decisions'] == register['decisions'])
            envelopes = [payload['summary'], payload['decisions']] + list(payload['assets'].values()) + list(payload['questions'].values()) + list(payload['context'].values())
            check(rev + ' selected snapshot fingerprints and offline qualifiers', all(e['live'] is False and e['source_acquisition_time'] is None
                  and e['snapshot_sha256'] == sha(graph_path) and e['context_sha256'] == sha(context_path) for e in envelopes))
            save(out / rev / 'snapshot-readback.json', payload)

        for graph_rev, context_rev in [('A', 'B'), ('B', 'A')]:
            try:
                serve_snapshot.Snapshot(out / graph_rev / 'context/enriched_graph.json', out / context_rev / 'context/context.json')
            except Exception as exc:
                save(out / ('mixed-' + graph_rev + '-graph-' + context_rev + '-context.json'),
                     {'class': type(exc).__name__, 'message': str(exc), 'admitted': False})
                check('refuse mixed ' + graph_rev + ' graph/' + context_rev + ' context',
                      str(exc) == 'Invalid selected context: selected context content hash does not match the graph')
            else:
                raise ValueError('Mixed graph/context pair unexpectedly admitted')

        check('changed P&ID image bytes', sha(out / 'A/build/pid/D1.png') != sha(out / 'B/build/pid/D1.png'))
        check('changed model and graph bytes', sha(out / 'A/build/model.json') != sha(out / 'B/build/model.json')
              and sha(out / 'A/build/graph.json') != sha(out / 'B/build/graph.json'))
        summary = {'schema': 'engineering-change-demo-1', 'scope': 'Fictional structural change and explicit retained-source refresh; no installed or operating acceptance.',
                   'revisions': {}, 'answer_change': {'id': qid, 'A_state': a['current'][qid]['state'], 'B_state': b['current'][qid]['state'],
                       'changed': b['current'][qid]['answers'][0]['changed'], 'decisions_retained': len(b['decisions']), 'owner_records_retained': len(b['ownership_history'])},
                   'automatic': ['Validate supplied source quotations and supported model/layout consistency', 'Generate supported draft outputs and catalog questions',
                                 'Reconcile retained answers when explicitly refreshed', 'Read selected graph/context records'],
                   'authored': ['Fictional source revisions, interpretations and geometry', 'Selected source dependencies and manual follow-up questions',
                               'Fictional proposed partial answer and role assignment'],
                   'unresolved': key['limits'] + ['No company approval, physical acceptance, automatic source monitoring, complete impact analysis or timing benefit demonstrated.']}
        selected = ['model.json', 'graph.json', 'pid/D1.png', 'pid/D1.svg', 'exports/ignition/tags.json', 'exports/pi/pi_builder_af.csv']
        for rev in ['A', 'B']:
            build = out / rev / 'build'
            summary['revisions'][rev] = {'equipment_ids': key['expected'][rev]['equipment_ids'], 'stream_endpoints': key['expected'][rev]['stream_endpoints'],
                'generated_question_ids': [q['id'] for q in read(build / 'questions/questions.json')['questions']],
                'source_sha256': sha(HERE / 'inputs' / rev / 'source.txt'), 'selected_outputs_sha256': {name: sha(build / name) for name in selected},
                'context_sha256': sha(out / rev / 'context/context.json')}
        save(out / 'CHANGE-REVIEW.json', summary)
    except BaseException as exc:
        failure = {'type': type(exc).__name__, 'message': str(exc)}
        save(out / 'STOP.json', failure)
    finally:
        guards = (inventory(HERE / 'inputs') == frozen and all(sha(root / 'scripts' / name) == value for name, value in code.items())
                  and sha(Path(__file__).resolve()) == custody['runner'] and sha(HERE / 'ACCEPTANCE.json') == custody['acceptance_key']
                  and sha(root / 'data/questions.json') == custody['default_catalog'])
        passed = failure is None and guards
        save(out / 'RESULT.json', {'pass': passed, 'failure': failure, 'jobs': jobs, 'checks': checks,
                                   'source_code_unchanged': guards, 'no_server_transport_or_plant_connection': True})
        save(out / 'EVIDENCE-MANIFEST.json', inventory(out))
        print(json.dumps({'pass': passed, 'jobs': len(jobs), 'checks': len(checks), 'failure': failure}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
