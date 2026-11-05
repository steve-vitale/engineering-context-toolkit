"""Tests for one_map.py sheet-from-prediction (a drawing reader's prediction -> a one-map-sheet-1 sheet read) and
scripts/sheet_zone.py (the one zone convention). The worked example is examples/drawing-to-map: the committed
OPEN100 sheet 0 reading, converted, then built into a one-sheet site. Stdlib only.

Usage:  python -m unittest scripts/test_sheet_from_prediction.py
"""
import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import draw_pid_from_model as drawgen  # noqa: E402
import one_map as om  # noqa: E402
import sheet_zone as sz  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EX = ROOT / "examples" / "drawing-to-map"
PRED = "predictions/r2-tiles-trace/codex/0.json"
BARE = ROOT / "examples" / "plug-in-a-reader" / "prediction_sheet0.json"  # the same reading with other symbol ids
# The printed border of OPEN100 sheet 0 (measured on 0.png: frame lines at x 24.5..2232 of 2604, y 34..1711 of 1744)
FRAME = (9.4, 19.5, 857.1, 981.1)
ARGS = ["--sheet", "140", "--rev", "A", "--plant", "NPP", "--unit", "MSS", "--zone-frame", "9.4,19.5,857.1,981.1"]


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*a, **k)


def convert(path=ROOT / PRED, **kw):
    args = dict(sheet="140", revision="A", plant="NPP", unit="MSS", frame=FRAME)
    args.update(kw)
    return om.sheet_from_prediction(path, **args)


class Zones(unittest.TestCase):
    def test_same_rule_as_the_existing_generator(self):
        # scripts/draw_pid_from_model.py letters the generated sheets; the shared function reproduces it exactly
        bad = [(x, y) for x in range(0, 3200, 13) for y in range(0, 2140, 13)
               if drawgen.zone(x, y) != sz.zone_at(x, y, frame=drawgen.FRAME)]
        self.assertEqual(bad, [])

    def test_convention_and_options(self):
        whole = dict(frame=(0, 0, 1000, 1000))
        self.assertEqual(sz.zone_at(1, 1, **whole), "H-12")      # top left: top row H, left column 12
        self.assertEqual(sz.zone_at(999, 999, **whole), "A-1")   # bottom right is A-1 (ASME style, default)
        self.assertEqual(sz.zone_at(1, 1, origin="top-left", **whole), "A-1")      # ISO style
        self.assertEqual(sz.zone_at(999, 999, origin="top-left", **whole), "H-12")
        self.assertEqual(sz.zone_at(500, 500, 4, 6, **whole), "B-3")
        self.assertEqual(sz.zone_at(-50, 2000, **whole), "A-12")  # outside the frame clamps to the edge zone
        self.assertEqual(sz.zone_of_box([10, 10, 30, 30], **whole), "H-12")
        self.assertIsNone(sz.zone_of_box(None))
        self.assertEqual(sz.parse_grid("8x12"), (8, 12))
        for bad in ("8", "0x12", "8x0", "axb"):
            with self.assertRaises(ValueError):
                sz.parse_grid(bad)
        with self.assertRaises(ValueError):
            sz.parse_frame("1,2,3")
        with self.assertRaises(ValueError):
            sz.parse_frame("10,10,5,5")
        with self.assertRaises(ValueError):
            sz.zone_at(1, 1, origin="middle")

    def test_open100_sheet0_zones_match_its_printed_border(self):
        # checked by eye against the printed border of 0.png: column numbers 12..1 left to right, rows H..A top down
        read = convert()
        zone = {t["tag"]: t["zone"] for t in read["equipment"] + read["instruments"]}
        self.assertEqual(zone["PSV-1404"], "G-6")
        self.assertEqual(zone["RCS-SG-100"], "C-11")
        self.assertEqual(zone["MSS-XSS-140"], "D-9")
        self.assertEqual(zone["TCV-1401"], "E-10")
        self.assertEqual(zone["TCV-1409"], "D-4")
        self.assertEqual(read["zone_grid"]["frame_0_1000"], list(FRAME))


class Conversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.read = convert()
        cls.items = {t["tag"]: t for t in cls.read["equipment"] + cls.read["instruments"]}

    def test_committed_example_round_trips_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "open100-0.json"
            cwd = Path.cwd()
            try:
                import os
                os.chdir(ROOT)  # the source path is recorded as given, relative to the repository root
                self.assertEqual(quiet(om.main, ["sheet-from-prediction", PRED, *ARGS, "--out", str(out)]), 0)
            finally:
                os.chdir(cwd)
            self.assertEqual(out.read_bytes(), (EX / "inputs" / "sheets" / "open100-0.json").read_bytes()
                             .replace(b"\r\n", b"\n"))
            quiet(om.build, EX / "inputs" / "site.json", Path(tmp) / "map")
            quiet(om.draft_lists, EX / "inputs" / "site.json", Path(tmp) / "drafts")
            for exp in sorted(p for p in (EX / "expected").rglob("*") if p.is_file()):
                got = Path(tmp) / exp.relative_to(EX / "expected")
                self.assertTrue(got.exists(), exp)
                self.assertEqual(got.read_bytes().replace(b"\r\n", b"\n"), exp.read_bytes().replace(b"\r\n", b"\n"),
                                 exp)

    def test_nothing_is_dropped_and_counts_add_up(self):
        c = self.read["conversion"]
        self.assertEqual((c["symbols_in"], c["connections_in"]), (100, 345))
        self.assertEqual(c["equipment"] + c["instruments"] + c["offpage"] + c["untagged"], 100)
        self.assertEqual((c["equipment"], c["instruments"], c["offpage"], c["untagged"]), (2, 37, 9, 52))
        self.assertEqual(self.read["signal_lines"], [])
        self.assertTrue(any("no line type" in x for x in c["not_converted"]))
        self.assertEqual(self.read["source"]["sha256"], om.sha_bytes((ROOT / PRED).read_bytes()))
        self.assertEqual((self.read["source"]["tool"], self.read["source"]["model"]), ("codex", "gpt-6.1-sol"))

    def test_bare_and_stored_forms_convert_alike(self):
        bare = convert(BARE)
        strip = lambda r: sorted((t["tag"], t["zone"], t["tag_status"]) for t in r["equipment"] + r["instruments"])  # noqa: E731
        self.assertEqual(strip(bare), strip(self.read))
        self.assertFalse(bare["source"]["stored_form"])
        self.assertEqual({k: v for k, v in bare["conversion"].items() if isinstance(v, int)},
                         {k: v for k, v in self.read["conversion"].items() if isinstance(v, int)})

    def test_tags_are_joined_and_printed_text_kept(self):
        t = self.items["TCV-1401"]
        self.assertEqual((t["printed_tag"], t["tag_status"], t["reader_class"]), ("TCV 1401", "as_extracted",
                                                                                   "instrumentation"))
        printed = {u["printed_text"] for u in self.read["untagged"]}
        self.assertTrue({"N1", "H", "M"} <= printed)  # nozzle and operator letters are not tags

    def test_placeholders_and_duplicates_are_carried_and_flagged_downstream(self):
        self.assertEqual(self.read["conversion"]["placeholder_tags"], ["AORV-XXX", "MSCV-XXX"])
        self.assertEqual(self.read["conversion"]["duplicate_tags"], ["FT-1401"])
        self.assertEqual(sum(1 for t in self.read["instruments"] if t["tag"] == "FT-1401"), 2)
        rows = list(csv.DictReader(io.StringIO((EX / "expected" / "map" / "queues" / "review_queue.csv")
                                               .read_text(encoding="utf-8"))))
        kinds = {(r["item"].rsplit("/", 1)[1], r["kind"]) for r in rows}
        self.assertIn(("AORV-XXX", "placeholder tag"), kinds)
        self.assertIn(("MSCV-XXX", "placeholder tag"), kinds)
        self.assertIn(("FT-1401", "duplicate tag"), kinds)
        drafts = (EX / "expected" / "drafts" / "npp-mss" / "instrument_index.csv").read_text(encoding="utf-8")
        draft = {r["tag"]: r for r in csv.DictReader(io.StringIO("".join(
            ln for ln in drafts.splitlines(True) if not ln.startswith("#"))))}
        self.assertEqual(draft["AORV-XXX"]["review_tier"], "amber")
        self.assertEqual(draft["FT-1401"]["review_tier"], "amber")
        graph = json.loads((EX / "expected" / "map" / "graph.json").read_text(encoding="utf-8"))
        node = next(n for n in graph["nodes"] if n["id"] == "O100/NPP/MSS/MSCV-XXX")
        self.assertEqual(node["tag_status"], "placeholder")
        self.assertEqual(node["appearances"][0]["printed_tag"], "MSCV-XXX")

    def test_relief_valves_land_in_the_review_floor(self):
        rows = list(csv.DictReader(io.StringIO((EX / "expected" / "map" / "queues" / "review_queue.csv")
                                               .read_text(encoding="utf-8"))))
        psv = [r for r in rows if r["item"].rsplit("/", 1)[1].startswith("PSV-")]
        self.assertEqual(sorted(r["item"].rsplit("/", 1)[1] for r in psv),
                         ["PSV-1404", "PSV-1405", "PSV-1406", "PSV-1407"])
        self.assertTrue(all(r["tier"] == "amber" and r["safety"] == "relief device" for r in psv))
        self.assertEqual(om.floor_problems(rows), [])
        first = [r["safety"] for r in rows[:len([r for r in rows if r["safety"]])]]
        self.assertTrue(all(first))  # safety rows come first

    def test_small_cases_lines_branches_placement_and_untagged(self):
        sym = lambda i, cls, tag, x: {"id": i, "class": cls, "tag": tag, "confidence": 0.9,  # noqa: E731
                                      "bbox": {"x_min": x, "y_min": 100, "x_max": x + 10, "y_max": 110}}
        pred = {"symbols": [sym("t1", "tank", "V-101", 100), sym("v1", "valve", None, 200),
                            sym("p1", "pump", "P-101", 300), sym("g1", "general", None, 400),
                            sym("o1", "inlet/outlet", "HPD PID 12-3", 500), sym("o2", "inlet/outlet", "VENT", 600),
                            sym("i1", "instrumentation", "LT 101", 120), sym("t2", "tank", None, 700),
                            sym("i2", "instrumentation", None, 800), sym("x1", "valve", "XV-???", 900)],
                "connections": [{"from": "t1", "to": "v1"}, {"from": "v1", "to": "p1"},   # a run: V-101 - P-101
                                {"from": "p1", "to": "g1"}, {"from": "g1", "to": "o1"},   # g1 branches three ways
                                {"from": "g1", "to": "o2"}, {"from": "i1", "to": "t1"},   # LT-101 sits on V-101
                                {"from": "x1", "to": "o2"}]}
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "p.json"
            p.write_text(json.dumps(pred), encoding="utf-8")
            read = om.sheet_from_prediction(p, sheet="1", revision="0", plant="P1", unit="U1")
        lines = {(ln["from"], ln["to"]): ln["attributes"]["via_symbols"] for ln in read["lines"]}
        self.assertEqual(lines, {("P-101", "V-101"): "v1", ("o2", "XV-???"): ""})
        self.assertEqual(read["conversion"]["branch_points"], ["g1"])
        self.assertEqual(read["conversion"]["networks_not_written_as_lines"], [["P-101", "o1", "o2"]])
        lt = next(t for t in read["instruments"] if t["tag"] == "LT-101")
        self.assertEqual(lt["on"], "V-101")
        self.assertEqual({u["symbol"]: u["class"] for u in read["untagged"]},
                         {"v1": "valve", "g1": "general", "t2": "tank", "i2": "instrumentation"})
        self.assertEqual([t["tag"] for t in read["instruments"] if t["tag_status"] == "placeholder"], ["XV-???"])
        ops = {o["id"]: o for o in read["offpage"]}
        self.assertEqual(ops["o1"]["attributes"], {"drawing_reference": "HPD PID 12-3"})
        self.assertEqual(ops["o2"].get("attributes"), None)
        self.assertEqual(read["source"]["kind"], "reader_prediction")
        # an untagged vessel or instrument becomes its own review row downstream
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "sheets").mkdir()
            (tmp / "sheets" / "1.json").write_text(json.dumps(read), encoding="utf-8")
            (tmp / "register.csv").write_text("sheet,rev,plant,unit,owner,path\n1,0,P1,U1,Doc control,sheets/1.json\n",
                                              encoding="utf-8")
            (tmp / "site.json").write_text(json.dumps({
                "schema": "one-map-site-1", "site": {"id": "S", "name": "small"},
                "plants": [{"id": "P1", "units": [{"id": "U1"}]}], "record_owners": {"pid": "Doc control"},
                "drawing_register": "register.csv"}), encoding="utf-8")
            _, _, rows, _ = quiet(om.build, tmp / "site.json", tmp / "out")
        kinds = sorted((r["item"], r["kind"]) for r in rows if "untagged" in r["kind"])
        self.assertEqual(kinds, [("S/P1/U1/@1/untagged-i2", "untagged symbol"),
                                 ("S/P1/U1/@1/untagged-inline", "untagged in-line symbols"),
                                 ("S/P1/U1/@1/untagged-t2", "untagged symbol")])

    def test_refusals(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            bad = tmp / "bad.json"
            bad.write_text(json.dumps({"symbols": [{"id": "s1", "class": "robot", "tag": None, "confidence": None,
                                                    "bbox": {"x_min": 1, "y_min": 1, "x_max": 2, "y_max": 2}}],
                                       "connections": []}), encoding="utf-8")
            with self.assertRaisesRegex(om.InputError, "documented prediction format"):
                convert(bad)
            failed = tmp / "failed.json"
            failed.write_text(json.dumps({"schema": "pid-prediction/1", "prediction": None}), encoding="utf-8")
            with self.assertRaisesRegex(om.InputError, "prediction null"):
                convert(failed)
            with self.assertRaisesRegex(om.InputError, "sheet"):
                convert(sheet="a/b")
            with self.assertRaisesRegex(om.InputError, "zone grid"):
                convert(rows=0)
            self.assertEqual(quiet(om.main, ["sheet-from-prediction", str(bad), *ARGS, "--out",
                                             str(tmp / "x.json")]), 2)
            self.assertEqual(quiet(om.main, ["sheet-from-prediction", PRED, *ARGS[:-2], "--zone-frame", "1,2",
                                             "--out", str(tmp / "x.json")]), 2)


if __name__ == "__main__":
    unittest.main()
