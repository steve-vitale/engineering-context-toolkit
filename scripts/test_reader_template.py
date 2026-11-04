"""The template reader adapter (scripts/reader_template.py) and its worked example (examples/plug-in-a-reader).

  - the committed sample is exactly the committed sheet-0 reading re-expressed in the template's reader format
    (pixel boxes, reader type names, string ids), so it is a format exercise, not a new reader
  - converting it reproduces the committed prediction byte for byte, and scores the same as the original reading
    with the frozen scorer (the numbers docs/PLUG_IN_A_READER.md quotes)
  - the converted file imports through scripts/import_site_drawing.py into a review bundle
  - unknown types, collapsed boxes, unsafe ids/tags and bad links are dropped and reported, never silently kept
Stdlib only, offline, no model.
"""
import csv
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import evaluate_vendor as ev  # noqa: E402
import reader_template as rt  # noqa: E402

EXAMPLE = ROOT / "examples" / "plug-in-a-reader"
SOURCE = ROOT / "examples" / "own-drawing" / "extraction_sheet0.json"
KEYS = ROOT / "data" / "external" / "pid2graph" / "PID2Graph" / "Complete" / "PID2Graph OPEN100"
GUIDE = ROOT / "docs" / "PLUG_IN_A_READER.md"
# How the sample names the six classes: a reader's own vocabulary, mapped back by reader_template.CLASS_MAP.
SAMPLE_TYPES = {"tank": "vessel", "pump": "centrifugal pump", "valve": "gate valve", "instrumentation": "instrument bubble",
                "inlet/outlet": "off-page connector", "general": "fitting"}


def sample_from_reading(record, width, height):
    """The committed sample's derivation: the sheet-0 reading in the template's reader format."""
    pred = record["prediction"]
    ids = {s["id"]: f"sym-{n:03d}" for n, s in enumerate(pred["symbols"], 1)}
    symbols = []
    for s in pred["symbols"]:
        b = s["bbox"]
        symbols.append({"id": ids[s["id"]], "type": SAMPLE_TYPES[s["class"]], "tag": s.get("tag"),
                        "box_px": [round(b["x_min"] * width / 1000, 2), round(b["y_min"] * height / 1000, 2),
                                   round(b["x_max"] * width / 1000, 2), round(b["y_max"] * height / 1000, 2)],
                        "score": s.get("confidence")})
    return {"schema": rt.SCHEMA, "image_px": [width, height],
            "about": "The committed GPT reading of PID2Graph OPEN100 sheet 0 (examples/own-drawing/extraction_sheet0.json) "
                     "re-expressed in the template reader format to exercise scripts/reader_template.py. Not a new reader.",
            "symbols": symbols, "lines": [{"from": ids[c["from"]], "to": ids[c["to"]]} for c in pred["connections"]]}


def dumps(obj):
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


class WorkedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.sample_text = (EXAMPLE / "reader_output_sheet0.json").read_text(encoding="utf-8")
        cls.prediction_text = (EXAMPLE / "prediction_sheet0.json").read_text(encoding="utf-8")
        cls.guide = " ".join(GUIDE.read_text(encoding="utf-8").split())

    def test_sample_is_the_committed_reading_reexpressed(self):
        self.assertEqual(self.sample_text, dumps(sample_from_reading(self.record, 2604, 1744)))

    def test_cli_round_trip_reproduces_the_committed_prediction(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "0.json"
            r = subprocess.run([sys.executable, "-S", str(ROOT / "scripts" / "reader_template.py"),
                                str(EXAMPLE / "reader_output_sheet0.json"), "--out", str(out),
                                "--image", str(KEYS / "0.png")], capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), self.prediction_text)
            report = json.loads(r.stdout)
            self.assertEqual((report["symbols_out"], report["connections_out"]),
                             (len(self.record["prediction"]["symbols"]), len(self.record["prediction"]["connections"])))
            self.assertEqual(report["unmapped_types"], {})

    def test_converted_reading_scores_like_the_original(self):
        converted = json.loads(self.prediction_text)
        original, _ = ev.score_sheet(KEYS, "0", self.record["prediction"])
        after, _ = ev.score_sheet(KEYS, "0", converted)
        m0, m1 = ev.metrics(ev.total([original])), ev.metrics(ev.total([after]))
        for k in m0:
            self.assertAlmostEqual(m0[k], m1[k], places=9, msg=k)
        quoted = (f"review load {m1['review_load_per_100']:.1f}", f"symbol F1 {m1['symbol_f1_rough_classified']:.3f}",
                  f"connection F1 {m1['connection_f1']:.3f}")
        for words in quoted:
            self.assertIn(words, self.guide, f"the guide should quote {words}")

    def test_imports_into_a_review_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "bundle"
            r = subprocess.run([sys.executable, "-S", str(ROOT / "scripts" / "import_site_drawing.py"),
                                "--manifest", str(EXAMPLE / "manifest.json"), "--out", str(out)],
                               capture_output=True, text=True, timeout=300)
            self.assertEqual(r.returncode, 0, r.stderr)
            for rel in ("review_queue.csv", "plant_model.json", "ignition/tags.json", "READ_ME.txt"):
                self.assertTrue((out / rel).is_file(), rel)
            with open(out / "review_queue.csv", encoding="utf-8-sig", newline="") as f:
                rows = len(list(csv.DictReader(f)))
            self.assertRegex(self.guide, rf"\b{rows} rows\b")


class Conversion(unittest.TestCase):
    def base(self, **extra):
        data = {"schema": rt.SCHEMA, "image_px": [2000, 1000],
                "symbols": [{"id": "a", "type": "Gate Valve", "tag": " HV-1 ", "box_px": [100, 100, 140, 160], "score": 0.8},
                            {"id": "b", "type": "pump", "tag": None, "box_px": [400, 300, 300, 200], "score": 2},
                            {"id": "c", "type": "nozzle", "tag": None, "box_px": [10, 10, 20, 20], "score": 0.5}],
                "lines": [{"from": "a", "to": "b"}, {"from": "b", "to": "a"}, {"from": "a", "to": "a"},
                          {"from": "a", "to": "c"}]}
        data.update(extra)
        return data

    def test_maps_scales_and_reports(self):
        pred, report = rt.convert(self.base())
        a, b = pred["symbols"]
        self.assertEqual((a["class"], a["tag"], a["confidence"]), ("valve", "HV-1", 0.8))
        self.assertEqual(a["bbox"], {"x_min": 50.0, "y_min": 100.0, "x_max": 70.0, "y_max": 160.0})
        self.assertEqual(b["bbox"], {"x_min": 150.0, "y_min": 200.0, "x_max": 200.0, "y_max": 300.0})  # reversed box
        self.assertIsNone(b["confidence"])  # out of [0, 1] is not invented into range
        self.assertEqual(pred["connections"], [{"from": "a", "to": "b"}])
        self.assertEqual(report["unmapped_types"], {"nozzle": 1})
        self.assertEqual(report["links_dropped"], {"self": 1, "duplicate": 1, "unknown_end": 1})

    def test_unsafe_ids_renamed_and_formula_tags_withheld(self):
        data = self.base()
        data["symbols"][0].update(id="bad id/1", tag="=HYPERLINK(1)")
        data["lines"] = [{"from": "bad id/1", "to": "b"}]
        pred, report = rt.convert(data)
        self.assertEqual(pred["symbols"][0]["id"], "r1")
        self.assertIsNone(pred["symbols"][0]["tag"])
        self.assertEqual(report["tags_withheld"], ["r1"])
        self.assertEqual(pred["connections"], [{"from": "r1", "to": "b"}])

    def test_collapsed_box_dropped(self):
        data = self.base()
        data["symbols"][0]["box_px"] = [100, 100, 100.01, 160]
        pred, report = rt.convert(data)
        self.assertEqual(report["bad_boxes"], ["a"])
        self.assertEqual([s["id"] for s in pred["symbols"]], ["b"])

    def test_refuses_what_it_cannot_convert(self):
        with self.assertRaises(ValueError):
            rt.convert({"schema": "other"})
        with self.assertRaises(ValueError):
            rt.convert(self.base(image_px=None))
        with self.assertRaises(ValueError):
            rt.convert(self.base(), image_px=[10, 10])
        data = self.base()
        for s in data["symbols"]:
            s["type"] = "nozzle"
        with self.assertRaises(ValueError):
            rt.convert(data)

    def test_cli_writes_nothing_on_bad_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "in.json", Path(tmp) / "out.json"
            src.write_text(json.dumps({"schema": "other"}), encoding="utf-8")
            r = subprocess.run([sys.executable, "-S", str(ROOT / "scripts" / "reader_template.py"), str(src),
                                "--out", str(out)], capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 1)
            self.assertFalse(out.exists())
            self.assertTrue(re.search("schema", r.stderr))


if __name__ == "__main__":
    unittest.main()
