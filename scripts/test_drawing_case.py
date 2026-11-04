"""Tests for scripts/drawing_case.py: a contributed drawing case is admitted only with complete provenance, an
independent sampled review bound to the exact key, passing known-answer controls and a validation split.

Uses the committed OPEN100 sheets and the committed worked example; no network, no model calls.
Run: python scripts/test_drawing_case.py
"""
import contextlib
import csv
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import benchmark as bm  # noqa: E402
import drawing_case as dc  # noqa: E402
import evaluate_vendor as ev  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SHEETS = ROOT / "data/external/pid2graph/PID2Graph/Complete/PID2Graph OPEN100"
EXAMPLE = ROOT / "examples/contribute-a-pid"
DEMO = EXAMPLE / "open100-0-demo"
AUTHOR, REVIEWER = "Pat Author", "Robin Reviewer"


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = dc.main([str(a) for a in argv])
    return code, out.getvalue() + err.getvalue()


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args)


def fill(sheet, verdict="confirm", first=None):
    with sheet.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for i, r in enumerate(rows):
        r["REVIEW_confirm_or_correct"] = first if (first and i == 0) else verdict
    with sheet.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=dc.SHEET_COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


class Flow(unittest.TestCase):
    """A private root holding a copy of sheet 8 (smallest key) and the task prompt."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "extraction").mkdir()
        shutil.copyfile(ROOT / "extraction/prompt.md", self.root / "extraction/prompt.md")
        self.image = self.root / "drawings" / "sheet8.png"
        self.image.parent.mkdir()
        shutil.copyfile(SHEETS / "8.png", self.image)
        self.pred = self.root / "pred8.json"
        self.pred.write_text(json.dumps(ev.perfect_prediction(SHEETS / "8.graphml", SHEETS / "8.png")), encoding="utf-8")
        self.cases = self.root / "cases"

    def tearDown(self):
        self.tmp.cleanup()

    def init(self, case_id="sheet8", **over):
        args = {"--source-url": "https://example.org/sheet8.png", "--license": "CC-BY-SA-4.0",
                "--attribution": "Test attribution", "--redistributable": "yes", "--family": "test-family",
                "--key-author": AUTHOR, "--assistance": "model draft", "--exposure": "public test sheet"}
        args.update(over)
        argv = ["init", self.image, "--case-id", case_id, "--dir", self.cases]
        for k, v in args.items():
            if v is not None:
                argv += [k, v]
        code, text = run(*argv)
        self.assertEqual(code, 0, text)
        return self.cases / case_id

    def drafted(self, **over):
        case = self.init(**over)
        code, text = run("draft-key", "--case", case, "--from", self.pred)
        self.assertEqual(code, 0, text)
        return case

    def verified(self, **over):
        case = self.drafted(**over)
        self.assertEqual(run("verify", "--case", case, "--reviewer", REVIEWER, "--prepare")[0], 0)
        fill(dc.sheet_path(case, dc.file_hash(case / dc.KEY)))
        code, text = run("verify", "--case", case, "--reviewer", REVIEWER, "--date", "2026-11-04")
        self.assertEqual(code, 0, text)
        return case

    def admit(self, case, suite=None, *extra):
        suite = suite or self.root / "suite" / "contributed.json"
        suite.parent.mkdir(exist_ok=True)
        return run("admit", "--case", case, "--suite", suite, "--root", self.root, *extra)

    # --- the requested guarantees

    def test_reviewer_who_is_the_key_author_is_refused(self):
        case = self.drafted()
        for name in (AUTHOR, "  pat   AUTHOR ", "Pat Author."):
            code, text = run("verify", "--case", case, "--reviewer", name, "--prepare")
            self.assertEqual(code, 2)
            self.assertIn("reviewer is the key author", text)
        self.assertFalse((case / "review").exists())
        self.assertEqual(dc.load(case)["key_status"], "draft")

    def test_missing_or_closed_license_is_refused(self):
        case = self.verified(**{"--license": None})
        report, problems = dc.check(case)
        self.assertTrue(any("source.license_id" in p for p in problems), problems)
        code, text = self.admit(case)
        self.assertEqual(code, 2)
        self.assertIn("admission refused", text)
        self.assertFalse((self.root / "suite" / "contributed.json").exists())
        closed = self.verified(case_id="closed", **{"--license": "LicenseRef-all-rights-reserved"})
        self.assertTrue(any("not a recognised redistributable license" in p for p in dc.check(closed)[1]))

    def test_non_redistributable_stores_no_image(self):
        case = self.init(case_id="private", **{"--redistributable": "no"})
        meta = dc.load(case)
        self.assertIsNone(meta["image"]["path"])
        self.assertEqual(meta["image"]["sha256"], dc.file_hash(self.image))
        self.assertEqual(sorted(p.name for p in case.iterdir()), ["case.json", "packet.json"])
        # Without a local copy nothing can be scored, and a copy dropped into the case folder is refused.
        self.assertEqual(run("draft-key", "--case", case, "--from", self.pred)[0], 2)
        self.assertEqual(run("draft-key", "--case", case, "--from", self.pred, "--image", self.image)[0], 0)
        shutil.copyfile(self.image, case / "input.png")
        _, problems = dc.check(case, image=self.image)
        self.assertTrue(any("must not be stored" in p for p in problems), problems)

    def test_non_redistributable_case_never_enters_the_public_repository_suite(self):
        case = self.init(case_id="private2", **{"--redistributable": "no"})
        run("draft-key", "--case", case, "--from", self.pred, "--image", self.image)
        run("verify", "--case", case, "--reviewer", REVIEWER, "--prepare", "--image", self.image)
        fill(dc.sheet_path(case, dc.file_hash(case / dc.KEY)))
        self.assertEqual(run("verify", "--case", case, "--reviewer", REVIEWER, "--image", self.image)[0], 0)
        code, text = run("admit", "--case", case, "--image", self.image,
                         "--suite", ROOT / "benchmarks" / "never-written.json")
        self.assertEqual(code, 2)
        self.assertIn("cannot be scored in the public repository", text)
        self.assertFalse((ROOT / "benchmarks" / "never-written.json").exists())

    def test_check_runs_the_four_known_answer_controls(self):
        case = self.drafted()
        report, problems = dc.check(case)
        self.assertEqual(problems, [])
        c = report["controls"]
        self.assertEqual(list(c), list(ev.CONTROL_ORDER))
        self.assertEqual((c["perfect"]["review_load_per_100"], c["perfect"]["symbol_f1_strict_classified"]), (0, 1))
        self.assertEqual(c["empty"]["review_load_per_100"], 100)
        for name in ("wrong_class", "shifted"):
            self.assertLessEqual(c[name]["symbol_f1_rough_classified"], ev.WRONG_MAX_F1)
        # A key with no scored symbol cannot be controlled and fails check (exit 1).
        dc.write_graphml(case / dc.KEY, [("c1", "connector", (1, 1, 2, 2))], [])
        code, text = run("check", "--case", case)
        self.assertEqual(code, 1)
        self.assertIn("no scored symbol", text)

    def test_admit_only_as_validation(self):
        case = self.verified(**{"--split": "held-out"})
        code, text = self.admit(case)
        self.assertEqual(code, 2)
        self.assertIn("'validation' only", text)
        meta = dc.load(case)
        meta["split"] = "development"
        dc.save(case, meta)
        self.assertTrue(any(p.startswith("split:") for p in dc.check(case)[1]))
        self.assertEqual(self.admit(case)[0], 2)

    def test_editing_the_key_after_verification_voids_it(self):
        case = self.verified()
        self.assertEqual(dc.check(case, require_verified=True)[1], [])
        old_sheet = dc.sheet_path(case, dc.file_hash(case / dc.KEY))
        text = (case / dc.KEY).read_text(encoding="utf-8").replace("<data key=\"d0\">valve", "<data key=\"d0\">pump", 1)
        (case / dc.KEY).write_text(text, encoding="utf-8")
        report, problems = dc.check(case)
        self.assertEqual(report["key_status"], "verification void (key edited after review)")
        self.assertTrue(any("key changed after verification" in p for p in problems), problems)
        code, text = self.admit(case)
        self.assertEqual(code, 2)
        # The old sheet cannot be replayed onto the edited key.
        code, text = run("verify", "--case", case, "--reviewer", REVIEWER, "--sheet", old_sheet)
        self.assertEqual(code, 2)
        self.assertIn("not this key's sample", text)

    # --- supporting guarantees

    def test_disputed_review_is_not_verification_and_hand_edited_status_fails(self):
        case = self.drafted()
        run("verify", "--case", case, "--reviewer", REVIEWER, "--prepare")
        fill(dc.sheet_path(case, dc.file_hash(case / dc.KEY)), first="correct")
        self.assertEqual(run("verify", "--case", case, "--reviewer", REVIEWER)[0], 1)
        meta = dc.load(case)
        self.assertEqual((meta["key_status"], meta["verification"][-1]["disagreements"]), ("draft", 1))
        meta["key_status"] = dc.VERIFIED
        dc.save(case, meta)
        self.assertTrue(dc.check(case)[1])

    def test_receipt_copied_onto_another_key_is_refused(self):
        case = self.verified()
        text = (case / dc.KEY).read_text(encoding="utf-8").replace('<data key="d0">valve', '<data key="d0">pump', 1)
        (case / dc.KEY).write_text(text, encoding="utf-8")
        meta = dc.load(case)
        meta["verification"][-1]["key_sha256"] = dc.file_hash(case / dc.KEY)
        dc.save(case, meta)
        self.assertTrue(any("not this key's sample" in p for p in dc.check(case)[1]))

    def test_sample_is_drawn_from_items_the_author_left_unchanged(self):
        case = self.drafted()
        text = (case / dc.KEY).read_text(encoding="utf-8")
        first = text.index("<node id=")
        line = text[first:text.index("</node>", first) + len("</node>")]
        node_id = line.split('"')[1]
        label = line.split('<data key="d0">')[1].split("<")[0]
        relabelled = line.replace(f'<data key="d0">{label}<', '<data key="d0">' + ("pump" if label != "pump" else "tank") + "<")
        (case / dc.KEY).write_text(text.replace(line, relabelled), encoding="utf-8")
        key_sha, items, eligible, basis, sample = dc.sample_for(case, dc.load(case), 400)
        self.assertNotIn(f"symbol:{node_id}", eligible)
        self.assertIn("left as the model drafted", basis)
        self.assertEqual(sample, dc.sample_for(case, dc.load(case), 400)[4])

    def test_draft_from_a_prediction_of_another_drawing_is_refused(self):
        case = self.init()
        record = {"image_sha256": "0" * 64, "prediction": json.loads(self.pred.read_text(encoding="utf-8"))}
        other = self.root / "other.json"
        other.write_text(json.dumps(record), encoding="utf-8")
        code, text = run("draft-key", "--case", case, "--from", other)
        self.assertEqual(code, 2)
        self.assertIn("different image", text)

    def test_key_in_the_inference_packet_is_refused(self):
        case = self.drafted()
        packet = json.loads((case / dc.PACKET).read_text(encoding="utf-8"))
        packet["files"][1]["path"] = dc.KEY
        (case / dc.PACKET).write_text(json.dumps(packet), encoding="utf-8")
        self.assertTrue(any("never get it" in p for p in dc.check(case)[1]))

    def test_admit_writes_hashed_validation_case_new_report_and_registry(self):
        case = self.verified()
        registry = self.root / "registry.json"
        registry.write_text(json.dumps({"schema": "benchmark-registry-1", "reports": []}), encoding="utf-8")
        code, text = self.admit(case, None, "--registry", registry)
        self.assertEqual(code, 0, text)
        suite = json.loads((self.root / "suite/contributed.json").read_text(encoding="utf-8"))
        entry = suite["cases"][0]
        self.assertEqual(entry["split"], "validation")
        self.assertEqual(entry["files"]["key"]["sha256"], dc.file_hash(case / dc.KEY))
        self.assertEqual(entry["files"]["input"]["sha256"], dc.file_hash(self.image))
        self.assertEqual(quiet(bm.main, ["--registry", str(registry), "--root", str(self.root)]), 0)
        # Second admission of the same drawing is refused; a second case gets a new report, the first is retained.
        self.assertEqual(self.admit(case)[0], 2)
        reports = sorted(p.name for p in (self.root / "suite/results").glob("*.md"))
        self.assertEqual(reports, ["contributed-1-cases.md"])

    def test_blank_start_samples_every_item(self):
        case = self.init()
        self.assertEqual(run("draft-key", "--case", case, "--blank")[0], 0)
        self.assertEqual(dc.load(case)["key"]["origin"], "blank")
        shutil.copyfile(SHEETS / "8.graphml", case / dc.KEY)
        _, items, eligible, basis, sample = dc.sample_for(case, dc.load(case), 20)
        self.assertEqual(sorted(items), eligible)
        self.assertIn("every key item", basis)


class WorkedExample(unittest.TestCase):
    """The committed demonstration in examples/contribute-a-pid stays consistent and reproducible."""

    def test_committed_example_checks_and_its_report_is_current(self):
        report, problems = dc.check(DEMO, require_verified=True)
        self.assertEqual(problems, [])
        self.assertEqual(report["key_status"], dc.DEMO_VERIFIED)
        self.assertTrue(report["demonstration"])
        self.assertEqual(quiet(bm.main, ["--suite", str(EXAMPLE / "demo-suite.json"),
                                         "--out", str(EXAMPLE / "results/demo-suite-1-cases"), "--check"]), 0)
        receipts = dc.load(DEMO)["verification"]
        self.assertEqual([r["accepted"] for r in receipts], [False, True])

    def test_demonstration_is_never_admitted_to_benchmarks(self):
        code, text = run("admit", "--case", DEMO, "--suite", ROOT / "benchmarks" / "never-written.json")
        self.assertEqual(code, 2)
        self.assertIn("demonstration case", text)
        self.assertFalse((ROOT / "benchmarks" / "never-written.json").exists())

    def test_reproduce_regenerates_the_same_key_and_review_sheets(self):
        sys.path.insert(0, str(EXAMPLE))
        import reproduce
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "extraction").mkdir()
            shutil.copyfile(ROOT / "extraction/prompt.md", root / "extraction/prompt.md")
            shutil.copyfile(SHEETS / "0.png", root / "0.png")
            out = root / "example"
            out.mkdir()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                reproduce.main(["--out", str(out), "--root", str(root), "--image", str(root / "0.png")])
            for name in (dc.KEY, dc.DRAFT, *(f"review/{p.name}" for p in (DEMO / "review").iterdir())):
                self.assertEqual(dc.file_hash(out / reproduce.CASE_ID / name), dc.file_hash(DEMO / name), name)
            fresh, committed = dc.load(out / reproduce.CASE_ID), dc.load(DEMO)
            for meta in (fresh, committed):
                meta["image"].pop("path")
            self.assertEqual(fresh, committed)


if __name__ == "__main__":
    unittest.main()
