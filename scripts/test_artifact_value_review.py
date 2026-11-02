"""Offline regression controls for reviewed frozen artifact admission and unchanged label scoring."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import artifact_value_review as av
import benchmark as b

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'benchmarks/source-support/artifact-values'
EXPECTED_ADMISSION_IDS = (
    'A01-reference-valid',
    'A02-false-valid',
    'A03-stale-reference-inventory',
    'A04-omitted-critical-entry',
    'A05-duplicate-inventory-pointer',
    'A06-extra-inventory-pointer',
    'A07-boolean-numeric-typed-mismatch',
    'A08-integer-float-typed-mismatch',
    'A09-stale-source-bytes',
    'A10-wrong-source-quote',
    'A11-wrong-locator-same-source',
    'A12-critical-role-downgrade',
    'A13-omit-critical-group-and-key',
    'A14-wrong-group-record-membership',
    'A15-CSV-missing-critical-row',
    'A16-CSV-duplicate-row',
    'A17-CSV-foreign-record-identity',
    'A18-missing-key-label',
    'A19-omitted-complementary-meta',
    'A20-new-model-field-uninventoried',
    'A21-model-duplicate-JSON-key',
    'A22-CSV-boolean-numeric-value',
    'A23-changed-claim-prefix',
    'A24-changed-claim-time',
    'A25-changed-evidence-paraphrase',
    'A26-changed-evidence-source-context',
    'A27-mismatched-value-with-coherent-key-pin',
)


def load(path):
    return json.loads(path.read_bytes())


def typed(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


class ArtifactValueReview(unittest.TestCase):
    def test_frozen_admission_controls_refuse_scope_type_source_and_context_drift(self):
        controls = load(PACKET / 'admission-controls.json')['cases']
        expected = load(PACKET / 'label-controls.json')
        self.assertEqual(tuple(case['id'] for case in controls), EXPECTED_ADMISSION_IDS)
        self.assertEqual(tuple(case['id'] for case in controls if case['expected'] == 'admit'),
                         ('A01-reference-valid', 'A02-false-valid'))
        self.assertEqual(sum(case['expected'] == 'refuse' for case in controls), 25)
        for case in controls:
            with self.subTest(control=case['id']):
                if case['expected'] == 'refuse':
                    with self.assertRaises(ValueError) as caught:
                        av.admit(ROOT, case['input_ref'], case['key_ref'])
                    self.assertEqual(str(caught.exception), case['expected_message'])
                else:
                    admitted = av.admit(ROOT, case['input_ref'], case['key_ref'])
                    report = admitted.report()
                    self.assertEqual(typed(report['coverage']), typed(expected['coverage_each']))
                    reference = expected['runs']['artifact-control-' + case['case'] + '-keyed-review']
                    self.assertEqual(typed(report['keyed_artifact_contradictions']), typed(reference['keyed_artifact_contradictions']))

    def test_one_admitted_snapshot_keeps_scores_after_selected_files_are_removed(self):
        case = load(PACKET / 'admission-controls.json')['cases'][1]
        prediction = load(PACKET / 'predictions/false-shutdown-keyed-review.json')
        with tempfile.TemporaryDirectory(prefix='artifact-review-captured-') as folder:
            root = Path(folder)
            shutil.copytree(PACKET, root / PACKET.relative_to(ROOT))
            admitted = av.admit(root, case['input_ref'], case['key_ref'])
            report = admitted.report()
            self.assertTrue(report['captured_files'])
            self.assertTrue(all(item['capture_reads'] == 1 for item in report['captured_files'].values()))
            expected_score = admitted.score(prediction)
            expected_controls = admitted.controls()
            for relative in report['captured_files']:
                (root / relative).unlink()
            self.assertEqual(typed(admitted.score(prediction)), typed(expected_score))
            self.assertEqual(typed(admitted.controls()), typed(expected_controls))
            self.assertEqual(typed(admitted.report()), typed(report))
            # Returned normalized data is a copy, not an override API on the admitted snapshot.
            packet, key = admitted.normalized()
            packet.clear(); key.clear()
            self.assertEqual(typed(admitted.score(prediction)), typed(expected_score))

    def test_missing_judgments_and_bad_reasons_do_not_hide_artifact_contradiction(self):
        case = load(PACKET / 'admission-controls.json')['cases'][1]
        admitted = av.admit(ROOT, case['input_ref'], case['key_ref'])
        correct = load(PACKET / 'predictions/false-shutdown-keyed-review.json')
        poor_reason = load(PACKET / 'predictions/false-shutdown-correct-label-poor-reason.json')
        counts, diagnostics = admitted.score(correct)
        self.assertEqual(typed(admitted.score(poor_reason)), typed((counts, diagnostics)))
        self.assertFalse(diagnostics['reason_quality_scored'])
        self.assertEqual(counts['judgments']['tp'], counts['judgments']['truth'])
        self.assertTrue(admitted.report()['keyed_artifact_contradictions'])
        partial = copy.deepcopy(correct); removed = partial['decisions'].pop()
        missing_counts, missing = admitted.score(partial)
        self.assertEqual(missing_counts['judgments']['truth'], counts['judgments']['truth'])
        self.assertEqual(missing_counts['judgments']['tp'], counts['judgments']['tp'] - 1)
        self.assertEqual(missing['missing_judgments'], [removed['id']])
        unreviewed = load(PACKET / 'predictions/false-shutdown-literal-unreviewed.json')
        with self.assertRaisesRegex(ValueError, 'Unknown judgment label'):
            admitted.score(unreviewed)

    def test_normal_evaluator_preserves_all_saved_controls_and_exact_readable_coverage(self):
        expected = load(PACKET / 'label-controls.json')['runs']
        suite = load(PACKET / 'suite.json')
        order = [load(ROOT / path)['id'] for path in suite['runs']]
        report = b.evaluate(PACKET / 'suite.json', ROOT)
        self.assertEqual([result['run'] for result in report['results']], order)
        self.assertEqual(set(order), set(expected))
        rows = []
        for result in report['results']:
            wanted = expected[result['run']]
            self.assertEqual(len(result['rows']), 1)
            row = result['rows'][0]
            for field in ['case', 'status', 'note', 'counts', 'diagnostics']:
                self.assertEqual(typed(row[field]), typed(wanted[field]), (result['run'], field))
            self.assertEqual(result['not_attempted'], wanted['not_attempted'])
            admission = row['artifact_value_review']
            self.assertEqual(typed(admission['coverage']), typed(wanted['coverage']))
            self.assertEqual(typed(admission['keyed_artifact_contradictions']), typed(wanted['keyed_artifact_contradictions']))
            c = wanted['coverage']
            contradictions = '; '.join(x['id'] + ': ' + ', '.join(x['pointers']) for x in wanted['keyed_artifact_contradictions']) or 'none in declared key'
            fields = [result['run'], wanted['case'], c['model_entries'], c['provided_values'], c['semantic_groups'], contradictions, ', '.join(wanted['diagnostics']['missing_judgments']) or 'none']
            safe = lambda value: str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
            rows.append('| ' + ' | '.join(safe(value) for value in fields) + ' |')
        header = '| Run | Case | Model entries | Provided values | Declared groups | Keyed artifact contradictions (ID and pointer) | Missing reviewer judgments |'
        separator = '|---|---|---|---|---|---|---|'
        section = b.markdown(report).split('## Declared artifact value coverage\n', 1)[1]
        start = section.index(header + '\n'); end = section.index('\n\n', start)
        self.assertEqual(section[start:end].split('\n'), [header, separator] + rows)


if __name__ == '__main__':
    unittest.main()
