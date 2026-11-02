"""Replay the fictional structural-change tutorial through real local tools; no SDK/network."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/engineering-change'
RUNNER = EXAMPLE / 'reproduce.py'


class EngineeringChangeTests(unittest.TestCase):
    def test_actual_replay_matches_selected_evidence_and_refusal_controls(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'changed'
            result = subprocess.run([sys.executable, '-B', str(RUNNER), '--out', str(out)],
                                    cwd=temp, capture_output=True, text=True, timeout=180)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            receipt = json.loads((out / 'RESULT.json').read_bytes())
            self.assertTrue(receipt['pass'])
            self.assertEqual(len(receipt['jobs']), 14)
            self.assertEqual([j['exit'] for j in receipt['jobs']].count(2), 4)
            self.assertTrue(receipt['source_code_unchanged'])
            self.assertEqual(len(receipt['checks']), 56)
            pairs = [('build/model.json', 'model.json'), ('build/graph.json', 'graph.json'),
                     ('build/pid/D1.svg', 'D1.svg'), ('build/exports/ignition/tags.json', 'ignition-tags.json'),
                     ('build/exports/pi/pi_builder_af.csv', 'pi-af.csv'), ('context/context.json', 'context.json'),
                     ('context/enriched_graph.json', 'enriched_graph.json'), ('questions.json', 'questions.json')]
            for rev in ['A', 'B']:
                for actual, saved in pairs:
                    with self.subTest(revision=rev, artifact=saved):
                        self.assertEqual((out / rev / actual).read_bytes(), (EXAMPLE / 'expected' / rev / saved).read_bytes())
                # Compare the rendered pixels, not platform-dependent PNG compression metadata.
                with Image.open(out / rev / 'build/pid/D1.png') as actual, Image.open(EXAMPLE / 'expected' / rev / 'D1.png') as saved:
                    self.assertEqual(actual.size, saved.size)
                    self.assertEqual(actual.convert('L').tobytes(), saved.convert('L').tobytes())
                self.assertEqual((out / rev / 'build/question_catalog.json').read_bytes(),
                                 (EXAMPLE / 'expected/question_catalog.json').read_bytes())

    def test_existing_output_refuses_before_mutating_any_file(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            marker = folder / 'keep.txt'
            marker.write_bytes(b'Keep the earlier run intact.\n')
            result = subprocess.run([sys.executable, '-B', str(RUNNER), '--out', temp],
                                    cwd=temp, capture_output=True, text=True, timeout=15)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Choose a new output folder outside', result.stderr)
            self.assertEqual(list(folder.iterdir()), [marker])
            self.assertEqual(marker.read_bytes(), b'Keep the earlier run intact.\n')

    def test_saved_public_selection_has_exact_raw_custody(self):
        provenance = json.loads((EXAMPLE / 'PROVENANCE.json').read_bytes())
        selection = provenance['public_selection']
        self.assertEqual(set(selection), {p.relative_to(EXAMPLE).as_posix() for p in (EXAMPLE / 'expected').rglob('*') if p.is_file()})
        for relative, pin in selection.items():
            raw = (EXAMPLE / relative).read_bytes()
            self.assertEqual({'sha256_raw': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}, pin, relative)


if __name__ == '__main__':
    unittest.main()
