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
        # connectivity on the development sheet: runs through untagged items; placement and pairing left for review
        self.assertEqual((c["lines"], c["instruments_placed"], len(c["placement_unclear"])), (38, 0, 20))
        self.assertEqual([len(n["run_ends"]) for n in c["branched_networks"]], [5, 8])
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
        psv = [r for r in rows if r["item"].rsplit("/", 1)[1].startswith("PSV-")
               and r["kind"] == "on the P&ID, not in the maintenance equipment export"]
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
        self.assertEqual(lines, {("P-101", "V-101"): "v1", ("o2", "XV-???"): "",  # g1 is a tee: one run per pair
                                 ("o1", "o2"): "g1", ("o1", "P-101"): "g1", ("o2", "P-101"): "g1"})
        self.assertEqual(read["conversion"]["branched_networks"],
                         [{"run_ends": ["o1", "o2", "P-101"], "untagged_in_line_symbols": 1, "runs_written": True}])
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


def sym(i, cls, tag=None, x=100):
    return {"id": i, "class": cls, "tag": tag, "confidence": 0.9,
            "bbox": {"x_min": x, "y_min": 100, "x_max": x + 10, "y_max": 110}}


def read_of(symbols, links, sheet="1"):
    """Convert a small prediction (symbols, [(a, b), ...]) into a sheet read."""
    pred = {"symbols": symbols, "connections": [{"from": a, "to": b} for a, b in links]}
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "p.json"
        p.write_text(json.dumps(pred), encoding="utf-8")
        return om.sheet_from_prediction(p, sheet=sheet, revision="0", plant="P1", unit="U1")


def build_site(reads):
    """Build a one-unit site from {sheet: sheet read}; returns (graph, review rows)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "sheets").mkdir()
        reg = ["sheet,rev,plant,unit,owner,path"]
        for sheet, read in reads.items():
            (tmp / "sheets" / f"{sheet}.json").write_text(json.dumps(read), encoding="utf-8")
            reg.append(f"{sheet},0,P1,U1,Doc control,sheets/{sheet}.json")
        (tmp / "register.csv").write_text("\n".join(reg) + "\n", encoding="utf-8")
        (tmp / "site.json").write_text(json.dumps({
            "schema": "one-map-site-1", "site": {"id": "S", "name": "small"},
            "plants": [{"id": "P1", "units": [{"id": "U1"}]}], "record_owners": {"pid": "Doc control"},
            "drawing_register": "register.csv"}), encoding="utf-8")
        g, _, rows, _ = quiet(om.build, tmp / "site.json", tmp / "out")
    return g, rows


class Connectivity(unittest.TestCase):
    """Runs collapsed through untagged in-line symbols, instrument placement and off-page pairing."""

    def test_a_run_collapses_through_valves_and_fittings_with_provenance(self):
        links = [("t1", "v1"), ("v1", "f1"), ("f1", "v2"), ("v2", "p1")]
        read = read_of([sym("t1", "tank", "V-101"), sym("v1", "valve"), sym("f1", "general"), sym("v2", "valve"),
                        sym("p1", "pump", "P-101")], links)
        [run] = read["lines"]
        self.assertEqual((run["from"], run["to"]), ("P-101", "V-101"))
        a = run["attributes"]
        self.assertEqual(a["via_symbols"], "v2 f1 v1")  # in path order from the run's first end
        self.assertEqual(a["through"], "2 valves and 1 other in-line symbol")
        # provenance: each id is the index of the reader's connection in the prediction, along the path
        hops = [frozenset(links[int(c[1:])]) for c in a["prediction_connections"].split()]
        self.assertEqual(hops, [frozenset(x) for x in (("p1", "v2"), ("v2", "f1"), ("f1", "v1"), ("v1", "t1"))])
        self.assertNotIn("branched_network", a)
        self.assertTrue(all(u["on_a_line"] for u in read["untagged"]))
        g, _ = build_site({"1": read})
        edge = next(e for e in g["edges"] if e["type"] == "connects")
        claims = {c["name"]: c["value"] for c in edge["attributes"]}
        self.assertEqual(claims["prediction_connections"], a["prediction_connections"])
        self.assertEqual((edge["from"], edge["to"]), ("S/P1/U1/P-101", "S/P1/U1/V-101"))
        self.assertEqual(edge["direction"], "unknown")  # ends ordered by symbol id, not by flow
        self.assertEqual(om.problems(g), [])

    def test_a_tee_gives_a_run_per_pair_and_a_bigger_network_is_capped(self):
        read = read_of([sym("a", "tank", "V-11"), sym("b", "tank", "V-12"), sym("c", "inlet/outlet", "TO PID 9-1"),
                        sym("tee", "general"), sym("v", "valve")],
                       [("a", "tee"), ("tee", "b"), ("tee", "v"), ("v", "c")])
        self.assertEqual(sorted((r["from"], r["to"], r["attributes"]["through"]) for r in read["lines"]),
                         [("V-11", "V-12", "1 other in-line symbol"), ("V-11", "c", "1 valve and 1 other in-line symbol"),
                          ("V-12", "c", "1 valve and 1 other in-line symbol")])
        self.assertTrue(all("3 run ends" in r["attributes"]["branched_network"] for r in read["lines"]))
        n = om.MAX_RUN_ENDS + 1  # one header touching more ends than the cap: no runs, listed instead
        tanks = [sym(f"t{i}", "tank", f"V-{100 + i}") for i in range(n)]
        big = read_of(tanks + [sym("h", "general")], [(t["id"], "h") for t in tanks])
        self.assertEqual(big["lines"], [])
        self.assertEqual([x["runs_written"] for x in big["conversion"]["branched_networks"]], [False])
        self.assertTrue(any(f"more than {om.MAX_RUN_ENDS} run ends" in x for x in big["conversion"]["not_converted"]))
        at_cap = read_of(tanks[:-1] + [sym("h", "general")], [(t["id"], "h") for t in tanks[:-1]])
        self.assertEqual(len(at_cap["lines"]), om.MAX_RUN_ENDS * (om.MAX_RUN_ENDS - 1) // 2)

    def test_placement_unique_ambiguous_and_hop_limit(self):
        read = read_of([sym("a", "tank", "V-11"), sym("b", "tank", "V-12"), sym("c", "tank", "V-13"),
                        sym("v", "valve"), sym("tee", "general"), sym("noz", "general"), sym("d", "tank", "V-14"),
                        sym("s1", "valve"), sym("s2", "valve"), sym("s3", "valve"),
                        sym("i1", "instrumentation", "PT 101"), sym("i2", "instrumentation", "TT 102"),
                        sym("i3", "instrumentation", "LT 103"), sym("i4", "instrumentation", "FT 104")],
                       [("a", "v"), ("v", "tee"), ("tee", "b"), ("tee", "c"),  # a -- v -- tee < b, c
                        ("d", "noz"),                                           # a nozzle on V-4, no run
                        ("s1", "s2"), ("s2", "s3"),                             # a stub of valves, no tagged end
                        ("i1", "v"), ("i2", "tee"), ("i3", "noz"), ("i4", "s1")])
        inst = {t["tag"]: t for t in read["instruments"]}
        runs = {r["id"]: (r["from"], r["to"]) for r in read["lines"]}
        # v lies on the runs V-11 to V-2 and V-11 to V-3 (both pass through it): two candidates, not guessed
        self.assertEqual(sorted(runs[x] for x in inst["PT-101"]["placement_candidates"]),
                         [("V-11", "V-12"), ("V-11", "V-13")])
        self.assertEqual(len(inst["TT-102"]["placement_candidates"]), 3)  # on the tee itself
        self.assertEqual(inst["LT-103"].get("on"), "V-14")                  # bubble -> nozzle -> vessel: 2 hops
        self.assertFalse({"on", "on_line", "placement_candidates"} & set(inst["FT-104"]))  # reaches nothing
        self.assertEqual(read["conversion"]["placement_unclear"], ["PT-101", "TT-102"])
        # a bubble on a valve between exactly two ends is placed on that run
        two = read_of([sym("a", "tank", "V-11"), sym("v", "valve"), sym("b", "tank", "V-12"),
                       sym("i", "instrumentation", "PT 77")], [("a", "v"), ("v", "b"), ("i", "v")])
        pt = two["instruments"][0]
        self.assertEqual(pt["on_line"], two["lines"][0]["id"])
        self.assertEqual(two["conversion"]["instruments_placed_on_runs"], 1)
        g, _ = build_site({"1": two})
        app = next(n for n in g["nodes"] if n["id"] == "S/P1/U1/PT-77")["appearances"][0]
        self.assertEqual(app["on_line"], "S/P1/U1/@1/" + pt["on_line"])
        edge = next(e for e in g["edges"] if e["type"] == "connects")
        self.assertIn(("instruments_on", "PT-77"), [(c["name"], c["value"]) for c in edge["attributes"]])
        self.assertEqual(om.problems(g), [])
        _, rows = build_site({"1": read})
        unclear = {r["item"]: r["why"] for r in rows if r["kind"] == "placement unclear"}
        self.assertEqual(sorted(unclear), ["S/P1/U1/PT-101", "S/P1/U1/TT-102"])
        self.assertIn("every candidate run ends at V-11", unclear["S/P1/U1/PT-101"])

    def test_offpage_connectors_pair_by_printed_reference(self):
        s140 = read_of([sym("e", "tank", "V-11"), sym("oa", "inlet/outlet", "EXTRACTION STEAM\nES PID 180-1"),
                        sym("od", "inlet/outlet", "DRAIN PID 180-1"), sym("ob", "inlet/outlet", "HPD PID 190-1"),
                        sym("ov", "inlet/outlet", "VENT")],
                       [("e", "oa"), ("e", "ob")], sheet="140")
        s180 = read_of([sym("f", "tank", "V-12"), sym("oc", "inlet/outlet", "EXTRACTION STEAM\nMSS PID 140-1")],
                       [("f", "oc")], sheet="180-1")
        g, rows = build_site({"140": s140, "180-1": s180})
        pairs = [(e["from"], e["to"]) for e in g["edges"] if e.get("layer") == "offpage_pair"]
        self.assertEqual(pairs, [("S/P1/U1/@140/oa", "S/P1/U1/@180-1/oc")])  # the printed names narrow two to one
        kinds = {r["item"].rsplit("/", 1)[1]: (r["kind"], r["why"]) for r in rows if "off-page" in r["kind"]}
        self.assertEqual(sorted(kinds), ["ob", "od", "ov"])
        self.assertEqual(kinds["ob"][0], "off-page connector unpaired")
        self.assertIn("not in the sheet index", kinds["ob"][1])
        self.assertIn("no sheet reference", kinds["ov"][1])
        self.assertEqual(kinds["od"][0], "off-page pairing unclear")  # oc already pairs with oa
        self.assertEqual(om.problems(g), [])
        # two identical connectors on each side: never guessed
        twin = read_of([sym("x", "inlet/outlet", "DRAIN PID 180-1"), sym("y", "inlet/outlet", "DRAIN PID 180-1")],
                       [], sheet="140")
        back = read_of([sym("p", "inlet/outlet", "DRAIN PID 140-1"), sym("q", "inlet/outlet", "DRAIN PID 140-1")],
                       [], sheet="180")
        g, rows = build_site({"140": twin, "180": back})
        self.assertFalse([e for e in g["edges"] if e.get("layer") == "offpage_pair"])
        self.assertEqual(sorted(r["kind"] for r in rows if "off-page" in r["kind"]), ["off-page pairing unclear"] * 4)


if __name__ == "__main__":
    unittest.main()
