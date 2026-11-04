"""The reader leaderboard (scripts/reader_leaderboard.py -> benchmarks/LEADERBOARD.md).

  - rendering is deterministic and the committed page matches it (--check passes); a stale or missing page fails
  - development results are never ranked; validation/held-out rows are ranked only inside one table
  - every table shows its controls, and review load agrees with the vendor-evaluation kit's committed report
  - rescoring that disagrees with a registered report, a changed prediction or an unknown split stops the script
Stdlib only, offline, reads only committed files.
"""
import copy
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import reader_leaderboard as lb  # noqa: E402


def section(text, title):
    start = text.index(f"\n## {title}\n")
    end = text.find("\n## ", start + 1)
    return text[start:end if end >= 0 else None]


class Leaderboard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = lb.build()
        cls.committed = lb.OUT.read_text(encoding="utf-8").replace("\r\n", "\n")

    def test_deterministic_and_committed(self):
        self.assertEqual(lb.build(), self.text)
        self.assertEqual(self.committed, self.text, "run python scripts/reader_leaderboard.py")

    def test_check_passes_from_the_command_line(self):
        r = subprocess.run([sys.executable, "-S", str(ROOT / "scripts" / "reader_leaderboard.py"), "--check"],
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_check_catches_drift_and_absence(self):
        with tempfile.TemporaryDirectory() as tmp:
            stale = Path(tmp) / "LEADERBOARD.md"
            stale.write_text(self.text.replace("20.1", "19.1", 1), encoding="utf-8")
            with patch.object(lb, "OUT", stale), patch.object(lb, "build", return_value=self.text), \
                    redirect_stderr(io.StringIO()) as err, redirect_stdout(io.StringIO()):
                self.assertEqual(lb.main(["--check"]), 1)
                self.assertIn("stale", err.getvalue())
            with patch.object(lb, "OUT", Path(tmp) / "absent.md"), patch.object(lb, "build", return_value=self.text), \
                    redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
                self.assertEqual(lb.main(["--check"]), 1)

    def test_development_never_ranked(self):
        dev = section(self.text, "Development")
        rows = [line for line in dev.splitlines() if line.startswith("| ") and not line.startswith("| Rank")
                and not line.startswith("| control")]
        self.assertTrue(rows, "the registry has development reader results")
        for line in rows:
            self.assertTrue(line.startswith("| not ranked |"), line)
        self.assertIn("Development: not ranked.", dev)
        self.assertIn("not a claim about unseen drawings", dev)

    def test_validation_ranked_by_review_load_inside_one_table(self):
        val = section(self.text, "Validation")
        for table in re.split(r"\n### ", val)[1:]:
            ranks = [(int(m.group(1)), float(m.group(2)))
                     for m in re.finditer(r"^\| (\d+) \|[^|]+\|[^|]+\| ([\d.]+)", table, re.M)]
            self.assertEqual([r for r, _ in ranks], list(range(1, len(ranks) + 1)))
            self.assertEqual([v for _, v in ranks], sorted(v for _, v in ranks))
            self.assertIn("optimistic", val)

    def test_every_table_shows_controls(self):
        for table in re.split(r"\n### ", self.text)[1:]:
            self.assertIn("| control | Control: empty answer", table)
            self.assertRegex(table, r"\| control \| Control: (perfect|reference) answer")

    def test_held_out_gap_is_stated_not_hidden(self):
        held = section(self.text, "Held-out")
        if "\n### " not in held:
            self.assertIn("No reader result is registered on a held-out split yet", held)

    def test_review_load_matches_the_vendor_evaluation_report(self):
        report = json.loads((ROOT / "examples" / "vendor-evaluation" / "report.json").read_text(encoding="utf-8"))
        registry = lb.read(lb.REGISTRY)
        entry = next(e for e in registry["reports"] if e["suite"] == "benchmarks/open100-validation.json")
        tables = lb.drawing_tables(entry, lb.read(ROOT / f"{entry['report']}.json"), lb.read(ROOT / entry["suite"]))
        rows = [r for t in tables.values() for r in t["rows"] if r["reader"].startswith("gpt-6.1-sol")]
        self.assertEqual(len(rows), 1)
        ours = sorted(rows[0]["review"]["values"])
        theirs = sorted(report["replicates"]["review_load_per_100"]["values"])
        for a, b in zip(ours, theirs, strict=True):
            self.assertAlmostEqual(a, b, places=9)
        control = next(iter(tables.values()))["controls"]["shifted"]["review_load_per_100"]
        self.assertAlmostEqual(control, report["controls"]["shifted"]["review_load_per_100"], places=9)


class Guards(unittest.TestCase):
    def setUp(self):
        registry = lb.read(lb.REGISTRY)
        self.entry = next(e for e in registry["reports"] if e["suite"] == "benchmarks/open100-validation.json")
        self.report = lb.read(ROOT / f"{self.entry['report']}.json")
        self.suite = lb.read(ROOT / self.entry["suite"])
        self.cases = {c["id"]: c for c in self.suite["cases"]}

    def test_rescoring_must_reproduce_the_registered_counts(self):
        run = copy.deepcopy(self.report["results"][0])
        run["metrics"]["networks"]["f1"] += 0.01
        with self.assertRaisesRegex(lb.LeaderboardError, "differs from the registered"):
            lb.drawing_run(run, self.cases)

    def test_changed_prediction_refused(self):
        row = self.report["results"][0]["rows"][0]
        with patch.object(lb, "file_sha", return_value="0" * 64):
            with self.assertRaisesRegex(lb.LeaderboardError, "changed since its report was registered"):
                lb.load_answer(row)

    def test_failed_answer_scores_empty_not_skipped(self):
        self.assertIsNone(lb.load_answer(dict(self.report["results"][0]["rows"][0], status="failed")))

    def test_split_levels(self):
        self.assertEqual(lb.level_of("development"), "development")
        self.assertEqual(lb.level_of("validation"), "validation")
        self.assertEqual(lb.level_of("held-out"), "held-out")
        with self.assertRaises(lb.LeaderboardError):
            lb.level_of("training-ish")

    def test_ranking_rules(self):
        rows = [{"reader": "b", "x": 2}, {"reader": "a", "x": 1}]
        self.assertEqual([(r, row["reader"]) for r, row in lb.ranked(rows, "validation", lambda r: r["x"])],
                         [("1", "a"), ("2", "b")])
        self.assertEqual([r for r, _ in lb.ranked(rows, "development", lambda r: -r["x"])],
                         ["not ranked", "not ranked"])

    def test_uncertainty_formatting(self):
        self.assertEqual(lb.fmt(lb.stats([0.5]), 3), "0.500 (single run)")
        self.assertEqual(lb.fmt(lb.stats([0.5, 0.5]), 3), "0.500 (same in all 2)")
        self.assertRegex(lb.fmt(lb.stats([0.4, 0.6]), 3), r"^0\.500 ± 0\.141 \(0\.400–0\.600\)$")
        self.assertEqual(lb.fmt(None, 3), "n/a")


if __name__ == "__main__":
    unittest.main()
