"""Reconstruct the fictional investigation through real tools and retained source revisions."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
from unittest import mock
import uuid

import join_batch_records

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/batch-analysis/investigation'
JOIN = ROOT / 'examples/batch-analysis/record-joins'


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class InvestigationExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='investigation-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.out = Path(cls.temp.name) / 'exercise'
        cls.command = [sys.executable, '-B', '-S', str(CASE / 'reproduce.py'), '--out', str(cls.out)]
        cls.process = subprocess.run(cls.command, cwd=ROOT, capture_output=True, timeout=90)
        if cls.process.returncode:
            raise AssertionError((cls.process.stdout + cls.process.stderr).decode('utf-8', 'replace'))

    def test_actual_composition_and_record_check_boundaries(self):
        result = read(self.out / 'RESULT.json')
        self.assertTrue(result['passed'])
        self.assertEqual(len(result['checks']), 24)
        self.assertTrue(all(result['checks'].values()))
        jobs = read(self.out / 'ACTUAL-JOBS.json')
        self.assertEqual(len(jobs), 30)
        self.assertEqual(sum(j['exit'] == 1 for j in jobs), 2)
        for job in jobs:
            self.assertEqual(job['exit'], job['expected'])
            self.assertGreater(job['pid'], 0)
            self.assertLessEqual(job['start_utc'], job['end_utc'])
        check = read(self.out / 'checks/recipe-record-result.json')
        self.assertEqual(check['state'], 'recorded')
        self.assertEqual(check['report_sha256'], sha(self.out / '02-join-initial/batch_join.json'))
        self.assertEqual(check['join_check_sha256'], sha(self.out / 'checks/03-check-initial.json'))
        self.assertEqual([r['reported_execution']['recipe_revision'] for r in check['records']], ['3', '3'])
        self.assertIn('Not evidence of identical physical execution', check['limitation'])

    def test_all_capture_history_and_raw_sources_are_preserved(self):
        stages = ['01-plan', '04-record-check', '06-missing-evidence', '09-select-changed-feed',
                  '13-regenerated-follow-up', '16-lab-follow-up', 'control-unsupported-cause']
        before = (CASE / 'seed.knowledge.json').read_bytes()
        original_hypothesis = next(r for r in json.loads(before)['records'] if r['id'] == 'hypothesis:recipe-revision')
        for stage in stages:
            folder = self.out / stage
            self.assertEqual((folder / 'before.json').read_bytes(), before)
            packet = read(folder / 'knowledge.json')
            previous = json.loads(before)
            self.assertEqual(packet['records'][:len(previous['records'])], previous['records'])
            self.assertEqual(next(r for r in packet['records'] if r['id'] == original_hypothesis['id']), original_hypothesis)
            for record in packet['records']:
                self.assertEqual(record['review']['state'], 'unreviewed')
                if record['kind'] == 'source':
                    data = record['data']; raw = data['captured_text'].encode('utf-8')
                    self.assertEqual(hashlib.sha256(raw).hexdigest(), data['original_raw_sha256'])
                    self.assertEqual(len(raw), data['original_size_bytes'])
                    self.assertFalse(data['original_reverified_at_runtime'])
            for name, pin in read(folder / 'receipt.json')['files'].items():
                self.assertEqual(sha(folder / name), pin['raw_sha256'])
                self.assertEqual((folder / name).stat().st_size, pin['size_bytes'])
            before = (folder / 'knowledge.json').read_bytes()

    def test_changed_basis_is_distinct_from_a_perpetually_unknown_hypothesis(self):
        def response(label):
            return read(self.out / 'readback' / (label + '.json'))['result']
        initial = response('read-initial-observation')
        reopened = response('read-feed-reopened')
        self.assertEqual(initial['record'], reopened['record'])
        self.assertEqual(initial['diagnostics']['basis_state'], 'matches')
        self.assertEqual(reopened['diagnostics']['basis_state'], 'stale')
        self.assertTrue(any(r['source_record_id'] == 'source:feed-r1' and r['selected_source_record_id'] == 'source:feed-r2'
                            for r in reopened['diagnostics']['basis_reasons']))
        final = read(self.out / '16-lab-follow-up/knowledge.json')
        self.assertEqual(final['selected_sources']['FEED'], 'source:feed-r1')
        self.assertEqual(final['selected_sources']['ANALYSIS'], 'source:analysis-r1')
        self.assertEqual(final['selected_sources']['LABS'], 'source:labs-r2')
        self.assertEqual(final['selected_sources']['JOIN-CHECK'], 'source:join-check-lab-r2')
        check = read(self.out / 'checks/15-current-lab-check.json')
        self.assertEqual(check['status'], 'matched_and_reproduced')
        self.assertEqual(check['saved_report_sha256'], sha(self.out / '15-revised-lab-comparison/batch_join.json'))
        dependencies = response('read-final-handoff')['diagnostics']['dependency_reasons']
        self.assertTrue(any(r['path'][-1] == 'observation:initial-records' and r['basis_state'] == 'stale'
                            and 'selected_basis_changed' in r['reason_codes'] for r in dependencies))

    def test_retained_failure_reproduces_without_claiming_missing_is_different(self):
        history = JOIN / 'history/before-comparison-basis'
        spec = importlib.util.spec_from_file_location('historical_join_basis_case', history / 'join_batch_records.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        manifest = history / 'failing-cutoff/manifest.json'
        original, original_audit, original_inputs = module.build(manifest)
        self.assertEqual(original, read(history / 'failing-cutoff/batch_join.json'))
        current, current_audit, current_inputs = join_batch_records.build(manifest)
        self.assertEqual(original_audit, current_audit)
        self.assertEqual(original_inputs, current_inputs)
        self.assertIn('recipe_scale_method_or_outcome_basis_differs', original['comparison']['gaps'])
        self.assertNotIn('recipe_scale_method_or_outcome_basis_differs', current['comparison']['gaps'])
        self.assertIn('comparison_basis_unavailable', current['comparison']['gaps'])
        expected = copy.deepcopy(original)
        expected['method']['join_code_lf'] = current['method']['join_code_lf']
        expected['comparison']['gaps'] = current['comparison']['gaps']
        self.assertEqual(expected, current)
        self.assertIsNone(current['rows'][1]['lab_value'])
        self.assertIsNone(current['comparison']['differences'])

    def test_published_outputs_and_method_pins_are_honest(self):
        provenance = read(CASE / 'PROVENANCE.json')
        for name, pin in provenance['selected_actual_files'].items():
            path = CASE / name
            self.assertEqual(dict(raw_sha256=sha(path), size_bytes=path.stat().st_size), pin)
        for name, pin in provenance['method_files'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes().replace(b'\r\n', b'\n')).hexdigest(), pin['sha256_text_lf'])
        final = read(CASE / 'worked/final/knowledge.json')
        self.assertFalse(final.get('companion_bindings'))
        self.assertTrue(all(r['record_state'] == 'proposed' and r['review']['state'] == 'unreviewed' for r in final['records']))
        control = read(self.out / 'readback/read-unsupported-control.json')['result']['record']
        self.assertIn('Deliberately unsupported control', control['data']['statement'])
        self.assertEqual(control['review']['state'], 'unreviewed')

    def test_input_tree_destination_refuses_before_creation_or_process(self):
        spec = importlib.util.spec_from_file_location('investigation_destination_control', CASE / 'reproduce.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        target = JOIN / ('refused-investigation-' + uuid.uuid4().hex)
        self.assertFalse(target.exists())
        try:
            with mock.patch.object(module.subprocess, 'Popen') as launched:
                with self.assertRaises(ValueError):
                    module.reproduce(target)
                launched.assert_not_called()
            self.assertFalse(target.exists())
        finally:
            if target.exists():
                self.assertTrue(target.resolve().is_relative_to(JOIN.resolve()))
                self.assertTrue(target.name.startswith('refused-investigation-'))
                shutil.rmtree(target)

    def test_timeout_reaps_owned_child_and_retains_failed_process_receipt(self):
        """A labelled mocked timeout control, not a completed capture or source experiment."""
        spec = importlib.util.spec_from_file_location('investigation_timeout_control', CASE / 'reproduce.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        child = mock.Mock(pid=12345)
        child.wait.side_effect = [subprocess.TimeoutExpired(['labelled-test-child'], 90), -9]
        folder = Path(self.temp.name) / 'timeout-control'
        with mock.patch.object(module.subprocess, 'Popen', return_value=child):
            with self.assertRaises(TimeoutError):
                module.reproduce(folder)
        child.kill.assert_called_once_with()
        self.assertEqual(child.wait.call_count, 2)
        job = read(folder / 'ACTUAL-JOBS.json')[0]
        self.assertTrue(job['timed_out'])
        self.assertEqual(job['exit'], -9)
        self.assertTrue((folder / 'logs/01-plan.stdout').is_file())
        self.assertTrue((folder / 'logs/01-plan.stderr').is_file())
        result = read(folder / 'RESULT.json')
        self.assertFalse(result['passed'])
        self.assertTrue(result['selected_source_code_unchanged'])
        self.assertEqual(result['failure']['type'], 'TimeoutError')


if __name__ == '__main__':
    unittest.main()
