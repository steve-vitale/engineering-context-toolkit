"""Teach one fictional investigation using the existing join, capture and reader CLIs.

This fixed-example runner is not an investigation engine or an arbitrary-input importer.
Investigation roles and reasoning are authored; the generic capture validates neither.
"""
import argparse
import copy
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CASE = Path(__file__).resolve().parent
BASIS = CASE.parent / 'record-joins'
CODE = ('join_batch_records.py', 'check_analysis_basis.py', 'batch_analysis.py',
        'knowledge_capture.py', 'knowledge_snapshot.py')


def read(path):
    return json.loads(Path(path).read_bytes())


def write(path, value):
    Path(path).write_bytes((json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + '\n').encode())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory(folder):
    return {p.relative_to(folder).as_posix(): sha(p) for p in sorted(folder.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and 'worked' not in p.relative_to(folder).parts}


def now():
    return datetime.now(timezone.utc).isoformat()


def reproduce(destination):
    out = Path(destination).resolve()
    if any(out == source or source in out.parents for source in (CASE, BASIS)) or not out.parent.is_dir():
        raise ValueError('Use a new output directory outside this tutorial, under an existing parent.')
    out.mkdir(exist_ok=False)
    for name in ('logs', 'requests', 'sources', 'checks', 'readback'):
        (out / name).mkdir()
    guard = dict(case=inventory(CASE), basis=inventory(BASIS),
                 code={name: sha(ROOT / 'scripts' / name) for name in CODE})
    write(out / 'START.json', dict(started_utc=now(), selected_inputs=guard,
        scope='Exposed fictional records; bounded source/code guard, not an environment lock or company trial.'))
    jobs, checks = [], {}

    def check(name, condition):
        checks[name] = bool(condition)
        write(out / 'CHECKS.json', checks)
        if not condition:
            raise AssertionError(name)

    def run(label, args, expected=0):
        if any(j['label'] == label for j in jobs):
            raise ValueError('Duplicate job label')
        argv = [sys.executable, '-B', '-S', *map(str, args)]
        start = now()
        with (out / 'logs' / (label + '.stdout')).open('xb') as stdout, \
             (out / 'logs' / (label + '.stderr')).open('xb') as stderr:
            child = subprocess.Popen(argv, cwd=ROOT, stdout=stdout, stderr=stderr,
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1'})
            pid = child.pid
            timed_out = False
            try:
                status = child.wait(timeout=90)
            except subprocess.TimeoutExpired:
                # Own only this child; reap it before finalizing source guards or a stop receipt.
                child.kill()
                status = child.wait()
                timed_out = True
        jobs.append(dict(label=label, argv=argv, pid=pid, start_utc=start, end_utc=now(),
                         exit=status, expected=expected, timed_out=timed_out))
        write(out / 'ACTUAL-JOBS.json', jobs)
        if timed_out:
            raise TimeoutError(label + ': owned child timed out and was killed/reaped; logs retained')
        if status != expected:
            raise RuntimeError(label + ': unexpected exit ' + str(status) + '; complete logs retained')
        return (out / 'logs' / (label + '.stdout')).read_bytes()

    def clone(label):
        target = out / 'sources' / label
        target.mkdir()
        for folder in ('sources', 'analysis'):
            shutil.copytree(BASIS / folder, target / folder)
        shutil.copyfile(BASIS / 'manifest-qualified.json', target / 'manifest.json')
        return target

    def join(label, source):
        run(label, ['scripts/join_batch_records.py', '--manifest', source / 'manifest.json', '--out', out / label])
        return out / label / 'batch_join.json'

    def join_check(label, source, report, expected=0):
        raw = run(label, ['scripts/join_batch_records.py', '--manifest', source / 'manifest.json', '--check', report], expected)
        path = out / 'checks' / (label + '.json')
        path.write_bytes(raw)
        value = read(path)
        check(label + '-report-bound', value['saved_report_sha256'] == sha(report))
        return path

    def edit_csv(source, name, edit):
        path = source / 'sources' / (name + '.csv')
        reader = csv.DictReader(io.StringIO(path.read_text(encoding='utf-8'), newline=''))
        header, rows = reader.fieldnames, list(reader)
        edit(rows)
        text = io.StringIO(newline='')
        writer = csv.DictWriter(text, fieldnames=header, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
        path.write_bytes(text.getvalue().encode())

    def source(rid, doc, revision, path, title):
        path = Path(path)
        reference = ('exercise/' + path.relative_to(out).as_posix() if path.is_relative_to(out)
                     else path.relative_to(ROOT).as_posix())
        return dict(id=rid, document_id=doc, source_revision=revision, title=title,
                    source_authority='Fictional local teaching record; no authenticated company authority.',
                    original_reference=reference), path

    def evidence(rid, locator, currency='selected_basis'):
        return dict(source_record_id=rid, locator=locator, currency_requirement=currency)

    def claim(rid, title, statement, citations, dependencies=(), basis='cited_record'):
        return dict(id=rid, title=title, summary='Authored investigation record; role is prose, not a validated type.',
            basis=basis, statement=statement, evidence=citations, depends_on=list(dependencies), owner_roles=[],
            known_unknowns=['Actual process identity, execution, causation and company acceptance remain unverified.'],
            interpretation_limit='Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.')

    stages = []

    def capture(label, base, sources=(), claims=(), select=None):
        request = dict(schema='knowledge-capture-1', base_sha256=sha(base), revision=label,
            contributor='Fictional example author; no authenticated identity.',
            reason='Retain this explicit investigation contribution and its exact prior state.',
            new_sources=[item for item, path in sources], claims=list(claims),
            select_sources={**{item['document_id']: item['id'] for item, path in sources}, **(select or {})})
        path = out / 'requests' / (label + '.json')
        write(path, request)
        args = ['scripts/knowledge_capture.py', '--knowledge', base, '--change', path, '--out', out / label]
        for item, source_path in sources:
            args.extend(['--source', item['id'], source_path])
        run(label, args)
        packet = out / label / 'knowledge.json'
        stages.append(label)
        return packet

    def get(label, packet, rid):
        raw = run(label, ['scripts/knowledge_snapshot.py', '--knowledge', packet, 'get', '--record-id', rid])
        (out / 'readback' / (label + '.json')).write_bytes(raw)
        return json.loads(raw)['result']

    failure = None
    try:
        seed = CASE / 'seed.knowledge.json'
        planned = capture('01-plan', seed, [source('source:notes-r1', 'NOTES', '1',
            CASE / 'INVESTIGATION-NOTES.md', 'Prospective authored hypothesis and check plan')])
        baseline = clone('initial')
        initial = join('02-join-initial', baseline)
        fresh = join_check('03-check-initial', baseline, initial)
        doc = read(initial)
        expected = read(CASE / 'EXPECTATIONS.json')['initial_descriptive_values']
        check('initial-values', [(r['feed_integral'], r['lab_value'], r['outcome_value']) for r in doc['rows']]
              == [(expected[k]['feed_kg'], expected[k]['reported_assay_g_per_L'], expected[k]['reported_harvest_L']) for k in ('A', 'B')])
        # This is a fixed-example record check, not a new general scientific checking tool.
        recipe_rows = [dict(selection=r['selection'], batch=r['eligible_records']['batch'],
                            reported_execution=r['eligible_records']['recipes']) for r in doc['rows']]
        recipe_facts = [(x['batch']['recipe_id'], x['batch']['recipe_revision'],
                         x['reported_execution']['recipe_id'], x['reported_execution']['recipe_revision'],
                         x['reported_execution']['execution_basis']) for x in recipe_rows]
        check('same-declared-recipe', recipe_facts == [('RCP-1', '3', 'RCP-1', '3', 'reported_executed')] * 2)
        result_path = out / 'checks' / 'recipe-record-result.json'
        write(result_path, dict(schema='fictional-recipe-record-check-1', state='recorded',
            report_sha256=sha(initial), join_check_sha256=sha(fresh), as_of=doc['as_of'], records=recipe_rows,
            result='Different declared recipe revisions are not supported by these selected records.',
            limitation='Not evidence of identical physical execution, another cause, or an attempted equipment/process change.'))
        common = [evidence('source:join-r1', '/rows/0 and /rows/1; /comparison/differences/0'),
                  evidence('source:feed-r1', 'CSV records 2-7: batch_id, time_s, FT-101, feed_quality; complete selected calculation input'),
                  evidence('source:labs-r1', 'CSV records 2 and 3, A-lab/B-lab value, unit, availability and source_revision'),
                  evidence('source:outcomes-r1', 'CSV records 2 and 3, A-outcome/B-outcome value and unit'),
                  evidence('source:manifest-r1', '/as_of; /quantities; /analyses/0/availability; /time_alignment_basis'),
                  evidence('source:plan-r1', '/windows; full declared method/quality/unit basis'),
                  evidence('source:analysis-r1', '/windows; complete saved calculation and source/code pins'),
                  evidence('source:events-r1', 'CSV records 2 and 3: A-phase/B-phase source windows')]
        sources = [source('source:join-r1', 'JOIN', '1', initial, 'Initial selected record comparison'),
                   source('source:join-check-r1', 'JOIN-CHECK', '1', fresh, 'Dated successful join reproduction'),
                   source('source:recipe-check-r1', 'RECIPE-CHECK', '1', result_path, 'Recorded declared-recipe check'),
                   source('source:manifest-r1', 'MANIFEST', '1', baseline / 'manifest.json', 'Explicit original source selections and assumptions'),
                   source('source:plan-r1', 'PLAN', '1', baseline / 'sources/analysis.plan.json', 'Declared calculation plan'),
                   source('source:analysis-r1', 'ANALYSIS', '1', baseline / 'analysis/batch_analysis.json', 'Original saved feed calculation'),
                   source('source:events-r1', 'EVENTS', '1', baseline / 'sources/events.csv', 'Declared source event windows')]
        for role, filename, title in [('feed', 'observations', 'Recorded feed input'), ('labs', 'labs', 'Reported assay records'),
                                     ('outcomes', 'outcomes', 'Reported harvest records'), ('recipes', 'recipes', 'Reported executed recipes'),
                                     ('batches', 'batches', 'Batch identities and declared revisions')]:
            sources.append(source('source:' + role + '-r1', role.upper(), '1', baseline / 'sources' / (filename + '.csv'), title))
        one = capture('04-record-check', planned, sources, [
            claim('observation:initial-records', 'Observation: initial recorded comparison',
                'At the declared 2026-01-03 cutoff, A/B recorded feed is 2/4 kg, reported assay 10/12 g/L and harvest 900/920 L. Differences are 2 kg, 2 g/L and 20 L. These do not establish physical comparability, yield or cause.', common),
            claim('check:recipe-revision-result', 'Recorded check: declared recipe revisions',
                'The recorded P1 check finds both selected batch and reported-executed recipe records declare RCP-1 revision 3. H1 is not supported as a different-declared-revision explanation. No operating trial or failed equipment change occurred in these sources.',
                [evidence('source:recipe-check-r1', '/records/0 and /records/1; /result'),
                 evidence('source:recipes-r1', 'CSV records 2 and 3: A-recipe/B-recipe, recipe_id, recipe_revision, execution_basis'),
                 evidence('source:batches-r1', 'CSV records 2 and 3: A-batch/B-batch, recipe_id, recipe_revision')], ['plan:recipe-record-check']),
            claim('disposition:recipe-explanation', 'Proposed disposition: retain the failed explanation',
                'Retain H1 and its contrary record evidence. Equal declared revisions do not prove identical execution or identify the cause of the reported assay contrast. No recipe adoption or process change is authorized; source owner and reviewer are unassigned.',
                [evidence('source:join-r1', '/comparison and /rows'), evidence('source:recipe-check-r1', '/result and /limitation')],
                ['hypothesis:recipe-revision', 'observation:initial-records', 'check:recipe-revision-result'], 'interpretation')])
        initial_observation = get('read-initial-observation', one, 'observation:initial-records')
        get('read-hypothesis', one, 'hypothesis:recipe-revision')
        get('read-plan', one, 'plan:recipe-record-check')
        get('read-recorded-check', one, 'check:recipe-revision-result')
        initial_disposition = get('read-initial-disposition', one, 'disposition:recipe-explanation')
        check('initial-observation-source-matches', initial_observation['diagnostics']['basis_state'] == 'matches')

        early = clone('earlier-cutoff')
        value = read(early / 'manifest.json'); value['as_of'] = '2026-01-02T02:00:00Z'; write(early / 'manifest.json', value)
        early_report = join('05-earlier-cutoff', early)
        early_doc = read(early_report)
        check('missing-is-not-negative', early_doc['rows'][1]['lab_value'] is None and
              'labs_not_available_as_of' in early_doc['rows'][1]['gaps'] and early_doc['comparison']['differences'] is None
              and 'comparison_basis_unavailable' in early_doc['comparison']['gaps']
              and 'recipe_scale_method_or_outcome_basis_differs' not in early_doc['comparison']['gaps'])
        two = capture('06-missing-evidence', one, [source('source:early-join', 'EARLIER-CUTOFF', '1', early_report, 'Earlier cutoff scenario')], [
            claim('observation:missing-as-of', 'Unresolved: assay not available at the earlier cutoff',
                'The earlier-cutoff decision view has no eligible B assay and no complete comparison. Missing is neither zero nor a negative assay. The audit retains later values; this packet is not a blinded or access-controlled as-of dataset.',
                [evidence('source:early-join', '/as_of; /rows/1/lab_value; /rows/1/gaps; /comparison/differences', 'snapshot_evidence')])])

        changed = clone('changed-feed')
        feed = changed / 'sources/observations.csv'
        original_feed = feed.read_bytes(); check('feed-edit-target-exists', original_feed.count(b'B,0,4,GOOD') == 1)
        feed.write_bytes(original_feed.replace(b'B,0,4,GOOD', b'B,0,8,GOOD'))
        failed = join_check('07-old-join-feed-check', changed, initial, 1)
        snapshot = get('read-snapshot-before-selection', two, 'observation:initial-records')
        check('snapshot-is-not-external-freshness', snapshot == initial_observation and read(failed)['status'] == 'changed')
        stale = join('08-stale-calculation', changed)
        check('stale-calculation-withholds-feed', all(r['feed_integral'] is None and 'analysis_basis_changed' in r['gaps'] for r in read(stale)['rows']))
        three = capture('09-select-changed-feed', two, [
            source('source:feed-r2', 'FEED', '2', feed, 'Changed feed source scenario'),
            source('source:join-check-failed', 'EXTERNAL-REUSE-CHECK', '1', failed, 'Dated changed-input check')], [
            claim('observation:reuse-needs-review', 'Recorded check: saved join cannot be reused',
                'The operator-selected current feed CSV differs from the saved calculation/join. The actual join check reports changed; generation with the old calculation withholds both feed totals. Knowledge snapshot matching alone had not rechecked these external files.',
                [evidence('source:join-check-failed', '/status; /changes; /saved_report_sha256'), evidence('source:feed-r2', 'CSV record 5: batch_id B, time_s 0, FT-101 and feed_quality')])])
        reopened = get('read-feed-reopened', three, 'observation:initial-records')
        check('selected-feed-reopens-review', reopened['diagnostics']['basis_state'] == 'stale')
        dependent = get('read-dependent-disposition', three, 'disposition:recipe-explanation')
        def has_changed_observation_path(value):
            return any(reason['path'][-1] == 'observation:initial-records'
                       and reason['basis_state'] == 'stale'
                       and 'selected_basis_changed' in reason['reason_codes']
                       for reason in value['diagnostics']['dependency_reasons'])
        check('feed-change-propagates-distinct-reason', not has_changed_observation_path(initial_disposition)
              and has_changed_observation_path(dependent)
              and any(reason['source_record_id'] == 'source:feed-r1' and reason['selected_source_record_id'] == 'source:feed-r2'
                      for reason in reopened['diagnostics']['basis_reasons']))

        run('10-regenerate-calculation', ['scripts/batch_analysis.py', '--csv', feed, '--plan', changed / 'sources/analysis.plan.json', '--out', changed / 'regenerated-analysis'])
        value = read(changed / 'manifest.json'); value['analyses'][0]['report'] = 'regenerated-analysis/batch_analysis.json'; write(changed / 'manifest.json', value)
        rebuilt = join('11-regenerated-comparison', changed)
        rebuilt_check = join_check('12-regenerated-check', changed, rebuilt)
        check('regenerated-source-values', [r['feed_integral'] for r in read(rebuilt)['rows']] == [2.0, 6.0])
        four = capture('13-regenerated-follow-up', three, [source('source:join-feed-r2', 'JOIN', '2-feed', rebuilt, 'Regenerated comparison'),
            source('source:join-check-r2', 'JOIN-CHECK', '2', rebuilt_check, 'Dated regenerated join check'),
            source('source:analysis-r2', 'ANALYSIS', '2-feed', changed / 'regenerated-analysis/batch_analysis.json', 'Regenerated feed calculation'),
            source('source:manifest-feed-r2', 'MANIFEST', '2-feed', changed / 'manifest.json', 'Explicit regenerated-feed source selection')], [
            claim('observation:feed-source-revision', 'Observation: regenerated feed-source scenario',
                'Explicit calculation regeneration reports A/B recorded feed 2/6 kg, difference 4 kg. The old 4 kg B result remains historical. A changed source/calculation scenario is not evidence of an actual feed adjustment or intervention.',
                [evidence('source:join-feed-r2', '/rows/0/feed_integral; /rows/1/feed_integral; /comparison/differences/0'), evidence('source:feed-r2', 'CSV records 5-7: B, time_s and FT-101'),
                 evidence('source:analysis-r2', '/windows; complete regenerated calculation'),
                 evidence('source:manifest-feed-r2', '/analyses; /quantities; /as_of')])])

        revised = clone('revised-lab')
        edit_csv(revised, 'labs', lambda rows: rows[1].update(value='13', source_revision='2'))
        lab_old_check = join_check('14-old-join-lab-check', revised, initial, 1)
        lab_report = join('15-revised-lab-comparison', revised)
        lab_current_check = join_check('15-current-lab-check', revised, lab_report)
        check('revised-lab-values', [r['lab_value'] for r in read(lab_report)['rows']] == [10.0, 13.0]
              and read(lab_report)['comparison']['differences'][0]['difference']['lab_value'] == 3.0)
        # This is a separate source scenario: the manifest selects baseline feed, not the changed-feed branch.
        five = capture('16-lab-follow-up', four, [
            source('source:join-lab-r2', 'JOIN', '2-lab', lab_report, 'Lab revision scenario with baseline feed'),
            source('source:labs-r2', 'LABS', '2', revised / 'sources/labs.csv', 'Explicit revised lab source'),
            source('source:lab-reuse-check', 'LAB-REUSE-CHECK', '1', lab_old_check, 'Dated lab-source change check'),
            source('source:manifest-lab-r2', 'MANIFEST', '2-lab', revised / 'manifest.json', 'Explicit lab-source scenario selection'),
            source('source:join-check-lab-r2', 'JOIN-CHECK', '2-lab', lab_current_check, 'Dated successful final lab-report reproduction')], [
            claim('observation:lab-source-revision', 'Observation: revised reported assay',
                'In the separate lab-revision scenario, B-lab revision 2 reports 13 g/L, so the A/B reported concentration contrast is 3 g/L. Revision 1 at 12 g/L remains historical. This report uses baseline feed 2/4 kg; it is not the 2/6 kg feed branch and proves no intervention or cause.',
                [evidence('source:join-lab-r2', '/rows/1/lab_value; /comparison/differences/0'), evidence('source:labs-r2', 'CSV record 3: B-lab value and source_revision'),
                 evidence('source:feed-r1', 'CSV records 5-7: historical B baseline-feed branch', 'snapshot_evidence'),
                 evidence('source:join-check-lab-r2', '/status; /saved_report_sha256; /changes')]),
            claim('disposition:reopened-source-basis', 'Proposed handoff: keep conflicting revisions and unresolved causes',
                'Retain H1, the recorded recipe check and its contrary evidence, the earlier 12 g/L report, the revised 13 g/L report and the separate feed-source scenario. The final lab-report join check matched the explicitly selected inputs during this run. Before future reuse, select a coherent manifest and rerun join --check. Request qualified execution, mapping, clock, sampling and assay evidence from the responsible engineer/lab owner. No causal conclusion, recipe adoption or operating change is approved; receiving owner remains unassigned.',
                [evidence('source:join-lab-r2', '/rows; /comparison; /limits'), evidence('source:labs-r2', 'CSV record 3: B-lab'),
                 evidence('source:join-check-lab-r2', '/status; /saved_report_sha256; /changes')],
                ['hypothesis:recipe-revision', 'check:recipe-revision-result', 'observation:initial-records', 'observation:lab-source-revision', 'observation:feed-source-revision'], 'interpretation')],
            select={'FEED': 'source:feed-r1', 'ANALYSIS': 'source:analysis-r1'})
        final_old = get('read-retained-initial', five, 'observation:initial-records')
        final_new = get('read-new-lab', five, 'observation:lab-source-revision')
        final_disposition = get('read-final-handoff', five, 'disposition:reopened-source-basis')
        check('old-lab-source-reopens-review', final_old['diagnostics']['basis_state'] == 'stale'
              and any(reason['source_record_id'] == 'source:labs-r1' and reason['selected_source_record_id'] == 'source:labs-r2'
                      for reason in final_old['diagnostics']['basis_reasons']))
        check('final-handoff-retains-source-change-path', has_changed_observation_path(final_disposition))
        check('new-lab-does-not-hide-cross-scenario-feed', final_new['diagnostics']['basis_state'] == 'matches'
              and final_disposition['diagnostics']['dependency_state'] == 'needs_review')

        # Deliberately false authored prose is structurally admissible, but never accepted as science.
        bad = capture('control-unsupported-cause', five, claims=[claim('control:unsupported-cause', 'CONTROL: unsupported causal sentence',
            'Deliberately unsupported control: these records prove that a recipe change caused the assay increase.',
            [evidence('source:join-lab-r2', '/comparison')], basis='interpretation')])
        wrong = get('read-unsupported-control', bad, 'control:unsupported-cause')['record']
        check('capture-is-not-scientific-approval', wrong['review']['state'] == 'unreviewed' and wrong['record_state'] == 'proposed')
        packets = [read(out / stage / 'knowledge.json') for stage in stages]
        check('all-prior-records-exact', all(new['records'][:len(old['records'])] == old['records'] for old, new in zip([read(seed), *packets[:-1]], packets)))
        check('original-hypothesis-retained', next(r for r in read(seed)['records'] if r['id'] == 'hypothesis:recipe-revision')
              == next(r for r in read(five)['records'] if r['id'] == 'hypothesis:recipe-revision'))
        check('all-claims-unreviewed', all(r['review']['state'] == 'unreviewed' and r['record_state'] == 'proposed'
              for packet in packets for r in packet['records'] if r['kind'] == 'claim'))
        check('capture-receipts-complete', all(all(sha(out / stage / name) == pin['raw_sha256'] and
            (out / stage / name).stat().st_size == pin['size_bytes'] for name, pin in read(out / stage / 'receipt.json')['files'].items()) for stage in stages))
    except BaseException as exc:
        failure = dict(type=type(exc).__name__, message=str(exc))
        write(out / 'STOP.json', failure)
        raise
    finally:
        intact = guard == dict(case=inventory(CASE), basis=inventory(BASIS), code={name: sha(ROOT / 'scripts' / name) for name in CODE})
        commands = [dict(label=j['label'], exit=j['exit'], expected=j['expected'], pid=j['pid'],
                        start_utc=j['start_utc'], end_utc=j['end_utc'],
                        display_template=[str(a).replace(str(out), '<exercise-output>').replace(str(ROOT), '<toolkit>') for a in j['argv'][1:]]) for j in jobs]
        write(out / 'RESULT.json', dict(schema='fictional-investigation-composition-1', passed=failure is None and intact and all(checks.values()),
            failure=failure, checks=checks, commands=commands, selected_source_code_unchanged=intact,
            scope='Authored exposed fictional retention exercise. Display templates are not raw argv; ACTUAL-JOBS.json and logs retain actual invocations.',
            guarantees=['Exact source/prior-packet retention and declared-dependency diagnostics', 'Explicit current join reproduction when called'],
            not_established=['Scientific truth or typed investigation-role validation', 'Causation, kinetics, process execution or approval',
                             'Automatic external-file monitoring or accepted-resolution selection', 'Human usefulness or company acceptance']))
    return read(out / 'RESULT.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = reproduce(args.out)
    print(json.dumps(dict(passed=result['passed'], calls=len(result['commands']), checks=len(result['checks']))))
