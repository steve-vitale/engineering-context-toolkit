"""The question engine: the catalog is well-formed and every question cites a known source or says it has none,
the committed opportunity-screen examples regenerate exactly, known findings appear and known false triggers stay
quiet, the three evidence states come out right, and no output carries a currency symbol or a computed figure.
Stdlib only."""
import io
import copy
import contextlib
import json
import os
import re
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import question_engine as qe  # noqa: E402
import graph_export as gx  # noqa: E402

EX = ROOT / "examples" / "opportunity-screen"
CAT = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
RUNS = {
    "te": ["--model", "data/te_process_model.json", "--loops", "examples/loop-audit/te_loops.csv"],
    "bayer": ["--model", "data/bayer_rt/process_model.json"],
    "open100": ["--model", "out/twin/r2-tiles-trace/codex/plant_model.json", "--schedule",
                "data/open100_equipment_schedule.json", "--schedule",
                "examples/opportunity-screen/open100_schedule_fields.json", "--io-list",
                "data/io_lists/open100_sheet0_demo.csv"],
    "food": ["--model", "examples/opportunity-screen/food_plant_model.json"],
    "millard/screen": ["--model", "examples/opportunity-screen/millard/model.json", "--question", "E30"],
}
ROLLUP = ["examples/opportunity-screen/food", "examples/opportunity-screen/bayer"]
# Refrigeration, oven, dryer and fryer questions (added 2026-10-29 from a food manufacturer's walkthrough)
NEW = {"E27", "E28", "E29", "E30", "E31", "E32", "H5", "H6", "C11", "C12"}
SELECTOR_KEYS = {"kind", "type", "type_text", "not_type_text", "isa", "variable", "text", "text_all", "not_text", "tagged",
                 "control_valve", "fact_C_min", "fact_C_max", "schedule_field"}
CLAUSE_KEYS = {"select", "relation", "max_hops", "as", "twin_only", "hand_only", "anchor_kind"}
RELATIONS = {"same_unit", "same_stream", "same_unit_same_medium", "other_unit", "discharge_side", "near", "drives",
             "reads", "anywhere", "linked"}
PLACES = {"historian", "dcs", "nameplate", "vendor", "maintenance", "records", "bills", "walkdown", "text"}
CURRENCY = re.compile(r"[$€£¥]|\bUSD\b|\d[\d,.]*\s*(dollars?|cents?)\b", re.I)


def load(name):
    return json.loads((EX / name / "questions.json").read_text(encoding="utf-8"))


def finding(doc, fid):
    return next((f for f in doc["questions"] if f["id"] == fid), None)


def ids(doc):
    return {f["id"] for f in doc["questions"]}


def run(args, out):
    old = sys.stdout
    try:
        sys.stdout = open(Path(out) / "log.txt", "w", encoding="utf-8")
        rc = qe.main([*args, "--out", str(out)])
    finally:
        sys.stdout.close()
        sys.stdout = old
    return rc, json.loads((Path(out) / "questions.json").read_text(encoding="utf-8"))


class Catalog(unittest.TestCase):
    def test_questions_are_well_formed(self):
        seen = set()
        for q in CAT["questions"]:
            with self.subTest(q=q["id"]):
                self.assertNotIn(q["id"], seen)
                seen.add(q["id"])
                self.assertIn(q["family"], CAT["families"])
                for key in ("question", "applies_when", "evidence_fields", "data_requests", "decision_rule",
                            "typical_benefit"):
                    self.assertTrue(q.get(key), key)
                aw = q["applies_when"]
                anchors = aw["anchor"] if isinstance(aw["anchor"], list) else [aw["anchor"]]
                for sel in anchors:
                    self.assertLessEqual(set(sel), SELECTOR_KEYS)
                for part in ("with", "without", "also_show"):
                    for cl in aw.get(part, []):
                        self.assertLessEqual(set(cl), CLAUSE_KEYS)
                        self.assertLessEqual(set(cl["select"]), SELECTOR_KEYS)
                        self.assertIn(cl.get("relation", "same_unit"), RELATIONS)
                self.assertIn(aw.get("group_by", "unit"), ("unit", "item", "model"))
                for r in q["data_requests"]:
                    self.assertTrue(r["item"] and r["how"] and r["where"])
                    for pl in r["where"]:
                        self.assertIn(pl["place"], PLACES)

    def test_every_question_cites_a_known_source_or_says_none(self):
        for q in CAT["questions"]:
            tb = q["typical_benefit"]
            with self.subTest(q=q["id"]):
                for s in tb["source"]:
                    self.assertIn(s, CAT["sources"])
                if not tb["source"]:
                    self.assertRegex(tb["wording"].lower(), r"\bno\b.*\bsource\b")
        for key, s in CAT["sources"].items():
            self.assertTrue(s["title"] and s["url"].startswith("https://") and s["license"], key)

    def test_catalog_carries_no_currency(self):
        prose = [CAT["about"], CAT["source_notes"]]  # trigger regexes use $ as an anchor, so check the prose only
        for q in CAT["questions"]:
            prose += [q["question"], q["decision_rule"], q.get("limits") or "", q["typical_benefit"]["wording"],
                      q["typical_benefit"].get("arc") or ""]
            prose += [r["item"] + r["how"] + json.dumps(r["where"]) for r in q["data_requests"]]
        self.assertIsNone(CURRENCY.search("\n".join(prose)))

    def test_counts_by_family(self):
        fam = {}
        for q in CAT["questions"]:
            fam[q["family"]] = fam.get(q["family"], 0) + 1
        self.assertEqual(fam, {"energy": 30, "heat_grade": 6, "metering": 2, "controls": 8, "safety_question": 2,
                               "emissions": 2})

    def test_new_questions_quote_a_page_of_a_checked_source(self):
        """Each refrigeration / oven / dryer / fryer question quotes its source with a page, and the source records
        which file its quotes were checked against."""
        qs = {q["id"]: q for q in CAT["questions"]}
        self.assertEqual(NEW - set(qs), set())
        for qid in NEW:
            tb = qs[qid]["typical_benefit"]
            with self.subTest(q=qid):
                self.assertTrue(tb["source"])
                self.assertRegex(tb["wording"], r"p\. \d+")
                self.assertIn('"', tb["wording"])
                for s in tb["source"]:
                    self.assertIn("checked", CAT["sources"][s], s)


class Examples(unittest.TestCase):
    def test_committed_examples_regenerate_exactly(self):
        for name, args in RUNS.items():
            with self.subTest(model=name), tempfile.TemporaryDirectory() as tmp:
                run(args, tmp)
                for f in ("questions.json", "screen.md"):
                    self.assertEqual((Path(tmp) / f).read_text(encoding="utf-8"),
                                     (EX / name / f).read_text(encoding="utf-8"), f"{name}/{f}")

    def test_no_currency_no_local_path_and_benefits_quoted_verbatim(self):
        wording = {q["id"]: q["typical_benefit"]["wording"] for q in CAT["questions"]}
        for name in RUNS:
            doc = load(name)
            for f in ("questions.json", "screen.md"):
                text = (EX / name / f).read_text(encoding="utf-8")
                self.assertIsNone(CURRENCY.search(text), f"{name}/{f}")
                self.assertNotIn("Users/", text)
                self.assertNotIn("Users\\", text)
            for fd in doc["questions"]:
                self.assertEqual(fd["typical_benefit"]["wording"], wording[fd["question_id"]])
                self.assertEqual(fd["status"], "asked")

    @staticmethod
    def _first_unattributed_figure(markdown, doc, model, catalog):
        """Exempt only an exact sourced controller setpoint token on its own evidence line."""
        import math
        controllers = {}
        for controller in model.get("controllers", []):
            controllers.setdefault(controller.get("tag"), []).append(controller)
        allowed_lines = {}
        for question in doc["questions"]:
            for evidence in question["evidence"]:
                identifier = evidence.get("id")
                records = controllers.get(identifier, [])
                if len(records) != 1 or evidence.get("field") != f"controllers[{identifier}]":
                    continue
                if evidence.get("tag") != identifier:
                    continue
                controller = records[0]
                setpoint = controller.get("setpoint") or {}
                value, unit = setpoint.get("value"), setpoint.get("uom")
                source = setpoint.get("source") or controller.get("source")
                if (type(value) not in (int, float) or not math.isfinite(value)
                        or not isinstance(unit, str) or not isinstance(source, str) or not source.strip()):
                    continue
                token = f"(setpoint {value} {unit})"
                if evidence["text"].count(token) != 1:
                    continue
                prefix = "" if evidence["role"] == "trigger" else evidence["role"].capitalize() + ": "
                line = f"- {prefix}{evidence['text']} (`{evidence['field']}`)"
                allowed_lines.setdefault(line, set()).add(token)
        lines = []
        for line in markdown.splitlines(keepends=True):
            bare = line.rstrip("\r\n")
            tokens = allowed_lines.get(bare, set())
            if len(tokens) == 1:
                line = line.replace(next(iter(tokens)), "(declared controller setpoint)", 1)
            lines.append(line)
        text = "".join(lines)
        strings = []
        for question in catalog["questions"]:
            strings += [question["typical_benefit"]["wording"], question["decision_rule"],
                        question.get("limits") or "", question["typical_benefit"].get("arc") or ""]
        for supplied in sorted(strings, key=len, reverse=True):
            if supplied:
                text = text.replace(supplied, "")
        figure = re.compile(r"\d[\d,.]*\s*(%|kWh|MWh|MMBtu|Btu|kW\b|hp\b|lb/hr|per year|/yr|years?\b|yr\b)", re.I)
        return figure.search(text)

    def test_engine_adds_no_figures_of_its_own(self):
        """Catalog wording and exact attributable setpoint tokens are exempt; remaining figures still fail."""
        for name, arguments in RUNS.items():
            with self.subTest(model=name):
                raw_model = (ROOT / arguments[arguments.index("--model") + 1]).read_bytes()
                model = json.loads(raw_model)
                doc = load(name)
                markdown = (EX / name / "screen.md").read_text(encoding="utf-8")
                match = self._first_unattributed_figure(markdown, doc, model, CAT)
                self.assertIsNone(match, (name, match and match.group(0)))
        # Negative controls change saved output only; the declared original model stays unchanged.
        model = json.loads((ROOT / "data/bayer_rt/process_model.json").read_bytes())
        original = copy.deepcopy(model)
        doc, markdown = load("bayer"), (EX / "bayer/screen.md").read_text(encoding="utf-8")
        controller = next(row for row in model["controllers"] if row["tag"] == "LIC-102")
        point = controller["setpoint"]
        token = f"(setpoint {point['value']} {point['uom']})"
        for mode in ("changed-value", "wrong-id", "wrong-field", "wrong-tag", "missing-tag", "appended-saving", "same-value-elsewhere"):
            with self.subTest(control=mode):
                changed, text = copy.deepcopy(doc), markdown
                row = next(e for q in changed["questions"] for e in q["evidence"]
                           if e.get("id") == "LIC-102" and e.get("field") == "controllers[LIC-102]")
                if mode == "changed-value":
                    old_text = row["text"]
                    row["text"] = old_text.replace(token, f"(setpoint {point['value'] + 1} {point['uom']})", 1)
                    self.assertNotEqual(row["text"], old_text)
                    text = text.replace(old_text, row["text"], 1)
                elif mode == "wrong-id":
                    row["id"] = "unrelated-controller"
                elif mode == "wrong-field":
                    old_field = row["field"]
                    row["field"] = "controllers[unrelated-controller]"
                    text = text.replace(f"(`{old_field}`)", f"(`{row['field']}`)", 1)
                elif mode == "wrong-tag":
                    row["tag"] = "unrelated-controller"
                elif mode == "missing-tag":
                    row.pop("tag")
                elif mode == "appended-saving":
                    text += "\nInvented local saving: 7.25 % per year.\n"
                else:
                    text += f"\nUnattributed percentage: {point['value']} {point['uom']}\n"
                self.assertIsNotNone(self._first_unattributed_figure(text, changed, model, CAT), mode)
        self.assertEqual(model, original)


    def test_graph_export_accepts_each_questions_file(self):
        models = {"te": "data/te_process_model.json", "bayer": "data/bayer_rt/process_model.json",
                  "open100": "out/twin/r2-tiles-trace/codex/plant_model.json",
                  "food": "examples/opportunity-screen/food_plant_model.json"}
        for name, model in models.items():
            g = gx.build(ROOT / model, questions=EX / name / "questions.json")
            self.assertEqual(gx.problems(g), [], name)
            self.assertEqual(g["counts"]["questions"], len(load(name)["questions"]))


class ExpectedFindings(unittest.TestCase):
    def test_tennessee_eastman(self):
        doc = load("te")
        e6 = finding(doc, "E6@K-101")
        self.assertIn("FV-105", {a["id"] for a in e6["assets"]})
        e18 = finding(doc, "E18@model")
        self.assertTrue({"TV-121", "FV-117", "FV-119"} <= {a["id"] for a in e18["assets"]})
        self.assertIn("TT-122", {a["id"] for a in finding(doc, "H4@E-101")["assets"]})
        self.assertIn("FT-119", {a["id"] for a in finding(doc, "E18@model")["assets"]})
        self.assertIsNotNone(finding(doc, "H2@C-101"))
        # stripper steam is metered (FT-119); condenser and reactor cooling water are not
        self.assertNotIn("C1@C-101", ids(doc))
        self.assertEqual({"C1@R-101", "C1@E-101"}, {i for i in ids(doc) if i.startswith("C1@")})
        # no pumps in this model: no pump questions; a process recycle compressor is not an air compressor
        for q in ("E1", "E2", "E3", "E4", "E19", "E20", "E21", "E22", "E23", "C7"):
            self.assertIn(q, doc["did_not_fire"])
        # loop list read: the uncontrolled measurements are exactly the eight without a loop
        c2 = finding(doc, "C2@model")
        self.assertEqual({a["id"] for a in c2["assets"]},
                         {"FT-106", "PT-107", "TT-111", "PT-113", "FT-114", "PT-116", "JT-120", "TT-122"})
        # historian names come from the model's recorded-signal index
        e6_text = json.dumps(e6)
        self.assertIn("XMV(5)", e6_text)

    def test_bayer(self):
        doc = load("bayer")
        e18 = {a["id"] for a in finding(doc, "E18@model")["assets"]}
        self.assertTrue({"stream:U1", "stream:U2"} <= e18)
        h4 = finding(doc, "H4@E-3")
        self.assertTrue(any(e["role"] == "on drawing" and "cooling_water_C = 80" in e["text"] for e in h4["evidence"]))
        self.assertIn("TIC-104", {a["id"] for a in finding(doc, "C6@TV-104C")["assets"]})
        self.assertIsNotNone(finding(doc, "E1@P-1"))
        # named false triggers: the recirculation loop is the process loop, not a pump bypass or minimum-flow
        # line; "alternate fuel tank" is not a fuel supply
        self.assertNotIn("E2@P-1", ids(doc))
        self.assertNotIn("E3@P-1", ids(doc))
        self.assertNotIn("C1@RT-1", ids(doc))
        # the steam heater is metered (FT-106); the 80 C water cooler is not
        self.assertEqual({i for i in ids(doc) if i.startswith("C1@")}, {"C1@E-3"})

    def test_open100(self):
        doc = load("open100")
        h1 = finding(doc, "H1@S4-TK001")
        tags = {a["tag"] for a in h1["assets"]}
        self.assertTrue({"ESS-HTR-180", "PCV-14011", "TCV-16013"} <= tags)
        self.assertIn("MSBV-1407", {a["tag"] for a in finding(doc, "H1@S0-OP005")["assets"]})
        self.assertIsNotNone(finding(doc, "H2@S4-OP005"))
        # blank schedule fields become data requests naming the field and sheet
        e4 = finding(doc, "E4@S2-PU001")
        req = e4["data_requests"][0]
        self.assertEqual(req["state"], "blank_on_drawing")
        self.assertIn("the blank HP field on the sheet 2 equipment schedule, entry CND-PU-162", req["where"])
        # named false triggers: a superheater is not a desuperheater; the ACC pumps reach LCV-1501 only through
        # the air-cooled condenser (they are vacuum pumps on the drawing); a drains blowdown tank vent is not boiler
        # blowdown; the pressurizer electric heater has no stated low temperature and is excluded anyway
        self.assertNotIn("H1@S0-TK001", ids(doc))
        for pump in ("S1-PU013", "S1-PU014", "S1-PU015"):
            self.assertNotIn(f"E1@{pump}", ids(doc))
        self.assertIn("E13", doc["did_not_fire"])
        self.assertIn("H3", doc["did_not_fire"])
        self.assertIn("RCS-EX-105", sum(doc["left_out"].values(), []))
        # no controller list in an extracted drawing: controller questions are reported as not checked
        self.assertEqual({n["question_id"] for n in doc["not_checked"]}, {"C2", "C6"})

    def test_new_questions_stay_quiet_on_the_chemical_and_power_examples(self):
        """No refrigerant, oven, dryer or fryer is drawn in TE, Bayer or OPEN100: TE's recycle compressor K-101, its
        condenser E-101, Bayer's vent condenser E-1 and OPEN100's air-cooled condenser must not read as
        refrigeration plant."""
        for name in ("te", "bayer", "open100"):
            doc = load(name)
            with self.subTest(model=name):
                self.assertEqual(NEW - set(doc["did_not_fire"]), set())
                self.assertFalse({f["question_id"] for f in doc["questions"]} & NEW)

    def test_food_plant(self):
        doc = load("food")
        found = ids(doc)
        for fid in ("E27@C-201", "E28@model", "E29@K-201", "E29@K-202", "E30@EV-201", "H5@model", "C12@model",
                    "E31@D-301", "E31@O-302", "E32@D-301", "E32@F-303", "C11@D-301", "C11@O-302", "H6@D-301",
                    "H6@O-302"):
            self.assertIn(fid, found)
        # Source-informed collection keeps drive and DP labels as candidates, not proof of actual function.
        for fid in ("E29@K-203", "E30@EV-202"):
            self.assertIn(fid, found)
        # Existing oxygen/recovery labels do not settle the scoped burner or residual-heat record review.
        # These source-informed collection jobs are positive leads, not installed deficiencies/projects.
        # K-201's stated power reading remains a candidate; actual real-input suitability stays open.
        for fid in ("E32@O-302", "E31@F-303", "H6@F-303"):
            self.assertIn(fid, found)
        c12 = {a["id"] for a in finding(doc, "C12@model")["assets"]}
        self.assertEqual(c12 & {"K-201", "K-202", "K-203"}, {"K-201", "K-202", "K-203"})
        self.assertIn("JT-201", c12)
        # the instrument air compressor and its refrigerated air dryer are not refrigeration plant or a process dryer
        for f in doc["questions"]:
            if f["question_id"] in NEW:
                self.assertFalse({a["id"] for a in f["assets"]} & {"AC-501", "AD-502"}, f["id"])
        self.assertIn("E19@AC-501", found)  # ...while the compressed air questions do ask about the air compressor
        self.assertFalse({i for i in found if i.split("@")[0] in ("E19", "E20", "E21", "E22", "E23") and
                          i.split("@")[1].startswith("K-")})
        # data requests name the quantities and where they live
        e27 = {r["item"]: r for r in finding(doc, "E27@C-201")["data_requests"]}
        head = next(r for k, r in e27.items() if k.startswith("Head (discharge) pressure"))
        self.assertIn("PT-203", " ".join(head["where"]))
        self.assertTrue(any("head pressure setpoint" in w for w in head["where"]))
        e30 = " ".join(json.dumps(r) for r in finding(doc, "E30@EV-201")["data_requests"])
        self.assertIn("defrost", e30.lower())
        e31 = {r["item"]: r for r in finding(doc, "E31@D-301")["data_requests"]}
        self.assertIn("TT-304", " ".join(e31["Existing exhaust-condition, product and maintenance basis"]["where"]))

    def test_new_triggers_ignore_look_alikes(self):
        """A process condenser on cooling water, a recycle gas compressor, an instrument air compressor, a
        refrigerated compressed air dryer, a desiccant air dryer and a nuclear steam dryer are not refrigeration
        plant, ovens or dryers."""
        with tempfile.TemporaryDirectory() as tmp:
            m = {"meta": {"title": "look-alikes"}, "instruments": [], "final_elements": [],
                 "units": [{"id": "E-1", "name": "Overhead condenser (cooling water)", "type": "condenser"},
                           {"id": "K-1", "name": "Recycle gas compressor", "type": "compressor"},
                           {"id": "K-2", "name": "Instrument air compressor", "type": "compressor"},
                           {"id": "D-1", "name": "Refrigerated compressed air dryer", "type": "dryer"},
                           {"id": "D-2", "name": "Desiccant air dryer", "type": "dryer"},
                           {"id": "D-3", "name": "Steam dryer", "type": "dryer"},
                           {"id": "W-1", "name": "Hot water heater for CIP", "type": "heater"}],
                 "streams": [{"id": "U1", "name": "Natural gas", "from": "BL", "to": "W-1", "utility": True}]}
            (Path(tmp) / "m.json").write_text(json.dumps(m), encoding="utf-8")
            _, doc = run(["--model", str(Path(tmp) / "m.json")], tmp)
        self.assertFalse({f["question_id"] for f in doc["questions"]} & NEW, ids(doc))
        # tightened with them: an air dryer is not an air compressor (E19-E23 fired on it as "compressed air")
        self.assertEqual({i for i in ids(doc) if i.startswith(("E19@", "E22@", "E23@"))},
                         {"E19@K-2", "E22@K-2", "E23@K-2"} & ids(doc))
        self.assertIn("E23@K-2", ids(doc))

    def test_linked_heat_recovery_keeps_both_investigations_and_scopes_the_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = {"meta": {"title": "two dryers"}, "instruments": [], "final_elements": [],
                 "units": [{"id": "D-1", "name": "Product dryer", "type": "dryer"},
                           {"id": "D-2", "name": "Product dryer", "type": "dryer"},
                           {"id": "HX-1", "name": "Exhaust air heat recovery exchanger", "type": "heat_exchanger"}],
                 "streams": [{"id": "S1", "name": "Dryer exhaust", "from": "D-1", "to": "HX-1"},
                             {"id": "S2", "name": "Dryer exhaust to atmosphere", "from": "D-2", "to": "ATM"}]}
            (Path(tmp) / "m.json").write_text(json.dumps(m), encoding="utf-8")
            _, doc = run(["--model", str(Path(tmp) / "m.json"), "--question", "E31"], tmp)
        self.assertEqual(ids(doc), {"E31@D-1", "E31@D-2"})
        first = finding(doc, "E31@D-1")
        second = finding(doc, "E31@D-2")
        self.assertIn("HX-1", {a["id"] for a in first["assets"]})
        self.assertNotIn("HX-1", {a["id"] for a in second["assets"]})
        self.assertIn(("HX-1", "represented recovery candidate"),
                      {(e["id"], e["role"]) for e in first["evidence"]})
        self.assertNotIn("HX-1", {e["id"] for e in second["evidence"]})


class Rollup(unittest.TestCase):
    def roll(self, dirs, out):
        old = sys.stdout
        try:
            sys.stdout = open(Path(out) / "log.txt", "w", encoding="utf-8")
            rc = qe.main([*sum((["--rollup", d] for d in dirs), []), "--out", str(out)])
        finally:
            sys.stdout.close()
            sys.stdout = old
        return rc

    def test_committed_rollup_regenerates_exactly(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.roll(ROLLUP, tmp), 0)
            for f in ("rollup.json", "rollup.md"):
                self.assertEqual((Path(tmp) / f).read_text(encoding="utf-8"),
                                 (EX / "rollup-food-bayer" / f).read_text(encoding="utf-8"), f)

    def test_rollup_content(self):
        doc = json.loads((EX / "rollup-food-bayer" / "rollup.json").read_text(encoding="utf-8"))
        self.assertEqual([s["site"] for s in doc["sites"]], ["food", "bayer"])
        by = {q["question_id"]: q for q in doc["questions"]}
        # every finding of every site is accounted for, once
        for site in ("food", "bayer"):
            src = load(site)
            got = sorted(f["finding_id"] for q in doc["questions"] for s in q["sites"] if s["site"] == site
                         for f in s["findings"])
            self.assertEqual(got, sorted(f["id"] for f in src["questions"]), site)
        # a question asked at both sites lists both, with the assets, and comes before single-site questions
        c9 = by["C9"]
        self.assertEqual([s["site"] for s in c9["sites"]], ["food", "bayer"])
        self.assertIn("P-1", {a["tag"] for s in c9["sites"] for f in s["findings"] for a in f["assets"]})
        order = [len(q["sites"]) for q in doc["questions"]]
        self.assertEqual(order, sorted(order, reverse=True))
        # data requests are combined by item: one entry per item, each site's places kept and deduplicated
        for q in doc["questions"]:
            items = [r["item"] for r in q["data_requests"]]
            self.assertEqual(len(items), len(set(items)), q["question_id"])
            for r in q["data_requests"]:
                for s in r["sites"]:
                    places = s["where"] + [w for b in s["where_by_finding"] for w in b["where"]]
                    self.assertTrue(places)
                    self.assertEqual(len(s["where"]), len(set(s["where"])))
                    for b in s["where_by_finding"]:
                        self.assertFalse(set(b["where"]) & set(s["where"]))
        # places shared by a site's findings are listed once; each meter-less valve stays with its own finding
        c1 = {r["item"]: r for r in by["C1"]["data_requests"]}["Utility flow to this user"]
        food = next(s for s in c1["sites"] if s["site"] == "food")
        self.assertTrue(any(w.startswith("a walkdown: clamp-on") for w in food["where"]))
        self.assertEqual({b["finding_id"] for b in food["where_by_finding"]}, {"C1@O-302", "C1@F-303", "C1@WH-401"})
        self.assertEqual([s["site"] for s in by["E27"]["sites"]], ["food"])
        self.assertIn("bayer", by["E27"]["quiet_at"])
        text = (EX / "rollup-food-bayer" / "rollup.md").read_text(encoding="utf-8")
        self.assertIsNone(CURRENCY.search(text))
        self.assertIsNone(CURRENCY.search(json.dumps(doc)))
        self.assertNotIn("Users/", text)

    def test_rollup_refuses_bad_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            err, old = io.StringIO(), sys.stderr
            sys.stderr = err
            try:
                rc = qe.main(["--rollup", str(Path(tmp) / "nope"), "--rollup", ROLLUP[0], "--out", tmp])
                self.assertEqual(rc, 2)
                self.assertIn("no questions.json", err.getvalue())
                (Path(tmp) / "x").mkdir()
                (Path(tmp) / "x" / "questions.json").write_text('{"schema": "other"}', encoding="utf-8")
                rc = qe.main(["--rollup", str(Path(tmp) / "x"), "--rollup", ROLLUP[0], "--out", tmp])
                self.assertEqual(rc, 2)
                self.assertIn("not an opportunity screen", err.getvalue())
                rc = qe.main(["--rollup", ROLLUP[0], "--rollup", ROLLUP[0], "--out", tmp])
                self.assertEqual(rc, 2)
                self.assertIn("named twice", err.getvalue())
            finally:
                sys.stderr = old


class EvidenceStates(unittest.TestCase):
    def tiny_twin(self, tmp, fields):
        def prov(sheet):
            return [{"sheet": sheet}]
        model = {"meta": {"model_kind": "extracted_twin", "title": "tiny"},
                 "systems": [{"id": "SYS-1", "system_code": "CWS"}],
                 "units": [{"id": "S1-PU001", "tag": "P�9", "class": "pump", "sheets": ["1"], "system": "SYS-1"}],
                 "instruments": [{"id": "S1-IN001", "tag": "FCV 9", "isa_letters": "FCV", "parent": "S1-VL001",
                                  "instrument_kind": "final element (valve)", "provenance": prov("1"),
                                  "system": "SYS-1"}],
                 "line_items": [{"id": "S1-VL001", "class": "valve", "provenance": prov("1"), "system": "SYS-1"}],
                 "offpage_connectors": [],
                 "streams": [{"id": "L1", "from": "S1-PU001", "to": "S1-VL001", "direction": "unknown"}]}
        sched = {"sheets": {"1": [{"tag": "P-9", "service": "WATER PUMP", "fields": fields}]}}
        (Path(tmp) / "m.json").write_text(json.dumps(model), encoding="utf-8")
        (Path(tmp) / "s.json").write_text(json.dumps(sched), encoding="utf-8")
        return ["--model", str(Path(tmp) / "m.json"), "--schedule", str(Path(tmp) / "s.json")]

    def test_three_states(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.tiny_twin(tmp, {"CAPACITY": None, "DISCHARGE": "XXX", "RPM": "1780", "HP": "40"})
            _, doc = run(args, tmp)
            e1 = finding(doc, "E1@S1-PU001")
            reqs = {r["item"]: r for r in e1["data_requests"]}
            rated = reqs["Pump rated flow and head"]
            self.assertEqual(rated["state"], "blank_on_drawing")
            self.assertIn("the blank CAPACITY field on the sheet 1 equipment schedule, entry P-9", rated["where"])
            self.assertTrue(any("DISCHARGE field (printed as 'XXX')" in w for w in rated["where"]))
            # both motor fields are filled in: quoted as evidence, no request
            self.assertNotIn("Motor rating and speed", reqs)
            on = [e["text"] for e in e1["evidence"] if e["role"] == "on drawing"]
            self.assertTrue(any("HP = 40" in t for t in on) and any("RPM = 1780" in t for t in on))
            # not on the drawing at all: the request names where it lives instead
            self.assertEqual(reqs["Static head versus friction head"]["state"], "not_on_drawing")
            self.assertTrue(reqs["Static head versus friction head"]["where"][0].startswith("a walkdown"))

    def test_speed_control_suppresses_the_drive_question(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.tiny_twin(tmp, {"HP": None})
            m = json.loads((Path(tmp) / "m.json").read_text(encoding="utf-8"))
            m["instruments"].append({"id": "S1-IN002", "tag": "SC 9", "isa_letters": "SC", "parent": "S1-PU001",
                                     "instrument_kind": "measurement / control", "provenance": [{"sheet": "1"}]})
            (Path(tmp) / "m.json").write_text(json.dumps(m), encoding="utf-8")
            _, doc = run(args, tmp)
            self.assertNotIn("E1@S1-PU001", ids(doc))
            self.assertIn("E4@S1-PU001", ids(doc))

    def test_model_with_no_pumps_gets_no_pump_questions(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = {"meta": {"title": "no pumps"}, "units": [{"id": "T-1", "name": "Tank", "type": "tank"}],
                 "streams": [], "instruments": [{"tag": "LT-1", "unit": "T-1", "variable": "level"}],
                 "final_elements": [{"tag": "LV-1", "unit": "T-1"}], "controllers": []}
            (Path(tmp) / "m.json").write_text(json.dumps(m), encoding="utf-8")
            _, doc = run(["--model", str(Path(tmp) / "m.json")], tmp)
            pump_qs = {"E1", "E2", "E3", "E4"}
            self.assertFalse({f["question_id"] for f in doc["questions"]} & pump_qs)

    def test_electric_heat_needs_a_stated_low_temperature(self):
        with tempfile.TemporaryDirectory() as tmp:
            def screen(facts):
                m = {"meta": {"title": "heater"}, "streams": [], "instruments": [], "final_elements": [],
                     "units": [{"id": "EH-1", "name": "Electric heater, tank warming", "type": "heater",
                                "facts": facts}]}
                (Path(tmp) / "m.json").write_text(json.dumps(m), encoding="utf-8")
                return run(["--model", str(Path(tmp) / "m.json"), "--question", "H3"], tmp)[1]
            self.assertEqual(ids(screen({"load_temperature_C": 60})), {"H3@EH-1"})
            self.assertEqual(ids(screen({})), set())
            self.assertEqual(ids(screen({"load_temperature_C": 340})), set())

    def test_a_request_stays_open_for_the_fields_not_on_the_drawing(self):
        """Review fix 2: a value found for one part of a multi-part request must not close the whole request."""
        with tempfile.TemporaryDirectory() as tmp:
            args = self.tiny_twin(tmp, {"HP": "40"})  # the schedule prints HP only; RPM is nowhere on the drawing
            _, doc = run(args, tmp)
            reqs = {r["item"]: r for r in finding(doc, "E1@S1-PU001")["data_requests"]}
            motor = reqs["Motor rating and speed"]
            self.assertEqual(motor["already_on_drawing"], ["HP"])
            self.assertEqual(motor["still_needed"], ["RPM"])
            self.assertEqual(motor["state"], "not_on_drawing")


class FieldSubjects(unittest.TestCase):
    """Independent supplies must not answer each other's missing fields."""

    def model(self, supplies):
        return {"meta": {"name": "Fictional independent supplies"},
                "units": [{"id": "H-1", "type": "heater", "name": "Process water heater"}],
                "streams": [], "instruments": [], "controllers": [],
                "final_elements": [{"tag": f"TV-{101 + i}", "unit": "H-1",
                                    "description": f"Steam supply from independent header {i + 1}", "facts": facts}
                                   for i, facts in enumerate(supplies)]}

    def screen(self, model, tmp, catalog=None):
        path = Path(tmp) / "model.json"
        path.write_text(json.dumps(model), encoding="utf-8")
        args = ["--model", str(path), "--question", "H2"]
        if catalog:
            cp = Path(tmp) / "catalog.json"
            cp.write_text(json.dumps(catalog), encoding="utf-8")
            args += ["--catalog", str(cp)]
        doc = run(args, tmp)[1]
        f = finding(doc, "H2@H-1")
        request = next((r for r in f["data_requests"] if r["item"] == "Steam supply pressure and temperature"), None)
        return doc, request

    def test_split_values_and_unknown_siblings_stay_open_with_each_obligation(self):
        p, t = "steam_pressure", "steam_temperature_C"
        cases = [([{p: "8 bar"}, {t: 140}], [[t], [p]]),
                 ([{p: "8 bar", t: 140}, {}], [[], [p, t]]),
                 ([{p: None}, {p: "8 bar", t: 140}], [[p, t], []]),
                 ([{}, {}], [[p, t], [p, t]])]
        for supplies, needed in cases:
            for reverse in (False, True):
                with self.subTest(supplies=supplies, reverse=reverse), tempfile.TemporaryDirectory() as tmp:
                    model = self.model(supplies)
                    if reverse:
                        model["final_elements"].reverse()
                    _, req = self.screen(model, tmp)
                    self.assertIsNotNone(req)
                    self.assertEqual(req["field_scope"], "anchors")
                    by_id = {s["id"]: s for s in req["field_coverage"]}
                    for i, missing in enumerate(needed):
                        self.assertEqual(by_id[f"TV-{101 + i}"]["still_needed"], missing)
                    self.assertEqual(set(req["still_needed"]), set(f for fs in needed for f in fs))
                    md = (Path(tmp) / "screen.md").read_text(encoding="utf-8")
                    for i in range(2):
                        self.assertIn(f"TV-{101 + i} (TV-{101 + i}): supplied", md)

    def test_context_cannot_complete_a_supply_but_is_not_an_extra_subject(self):
        p, t = "steam_pressure", "steam_temperature_C"
        with tempfile.TemporaryDirectory() as tmp:
            model = self.model([{p: "8 bar"}])
            model["units"][0]["facts"] = {t: 140}
            model["instruments"] = [{"tag": "TT-1", "unit": "H-1", "variable": "temperature",
                                      "description": "Process outlet temperature", "facts": {t: 140}}]
            _, req = self.screen(model, tmp)
            self.assertEqual(req["still_needed"], [t])
            self.assertEqual([s["id"] for s in req["field_coverage"]], ["TV-101"])
            model["final_elements"][0]["facts"][t] = 140
            self.assertIsNone(self.screen(model, tmp)[1])

    def test_complete_subjects_zero_false_and_case_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            complete = {"STEAM_PRESSURE": 0, "Steam_Temperature_C": False}
            doc, req = self.screen(self.model([complete, complete]), tmp)
            self.assertIsNone(req)
            evidence = finding(doc, "H2@H-1")["evidence"]
            fields = {e["field"] for e in evidence if e["role"] == "on drawing"}
            self.assertEqual(len(fields), 4)
            self.assertTrue(any(" = False" in e["text"] for e in evidence))

    def test_schedule_empty_strings_are_blank_without_losing_zero_false(self):
        for value in (None, "", "  ", "XXX", 0, False):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as tmp:
                args = EvidenceStates().tiny_twin(tmp, {"hp": value, "rpm": 1780})
                _, doc = run(args, tmp)
                f = finding(doc, "E1@S1-PU001")
                req = next((r for r in f["data_requests"] if r["item"] == "Motor rating and speed"), None)
                if value is False or value == 0:
                    self.assertIsNone(req)
                else:
                    self.assertEqual(req["state"], "blank_on_drawing")
                    self.assertEqual(req["still_needed"], ["HP"])

    def test_unit_scope_requires_actual_group_owner_and_also_needs_remains_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalog = copy.deepcopy(CAT)
            q = next(q for q in catalog["questions"] if q["id"] == "H2")
            r = q["data_requests"][0]
            r["field_scope"] = "unit"
            model = self.model([{}, {}])
            model["units"][0]["facts"] = {"steam_pressure": "8 bar", "steam_temperature_C": 140}
            self.assertIsNone(self.screen(model, tmp, catalog)[1])
            r["also_needs"] = ["Operating hours"]
            _, req = self.screen(model, tmp, catalog)
            self.assertEqual(req["still_needed"], ["Operating hours"])
            # Item grouping has no selected owning unit: proximity is not an ownership contract.
            q["applies_when"]["group_by"] = "item"
            path = Path(tmp) / "catalog.json"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            _, doc = run(["--model", str(Path(tmp) / "model.json"), "--question", "H2", "--catalog", str(path)], tmp)
            for f in doc["questions"]:
                req = f["data_requests"][0]
                self.assertEqual(req["field_coverage"], [])
                self.assertEqual(req["still_needed"], r["fields"] + ["Operating hours"])
                self.assertIn("No owning equipment unit", req["scope_note"])

    def test_rollup_keeps_scope_and_missing_fields_per_site_and_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            site = base / "site"
            site.mkdir()
            _, req = self.screen(self.model([{"steam_pressure": "8 bar"}, {"steam_temperature_C": 140}]), site)
            doc = qe.rollup([f"A={site}", f"B={site}"], CAT)
            r = doc["questions"][0]["data_requests"][0]
            for s in r["sites"]:
                detail = s["coverage_by_finding"][0]
                self.assertEqual(detail["field_coverage"], req["field_coverage"])
                self.assertEqual(detail["field_scope"], "anchors")
            md = qe.render_rollup_md(doc, CAT)
            self.assertEqual(md.count("TV-101 (TV-101): supplied steam_pressure; still needed steam_temperature_C (absent)"), 2)
            graph = gx.build(site / "model.json", questions=site / "questions.json")
            self.assertIn("field_coverage", json.dumps(graph))

    def test_scope_and_coverage_conflicts_refuse_before_replacing_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            site = base / "site"
            site.mkdir()
            self.screen(self.model([{}, {}]), site)
            catalog = copy.deepcopy(CAT)
            request = next(q for q in catalog["questions"] if q["id"] == "H2")["data_requests"][0]
            catalog_path = base / "catalog.json"
            out = base / "reports"
            out.mkdir()
            (out / "rollup.json").write_text("prior JSON", encoding="utf-8")
            (out / "rollup.md").write_text("prior Markdown", encoding="utf-8")
            before = {p.name: p.read_bytes() for p in out.iterdir()}
            for scope, message in (("unit", "field_scope"), ("pool", "field_scope must be")):
                request["field_scope"] = scope
                catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
                with contextlib.redirect_stderr(io.StringIO()) as err:
                    self.assertEqual(qe.main(["--rollup", str(site), "--catalog", str(catalog_path), "--out", str(out)]), 2)
                self.assertIn(message, err.getvalue())
                self.assertEqual({p.name: p.read_bytes() for p in out.iterdir()}, before)
            doc = json.loads((site / "questions.json").read_text(encoding="utf-8"))
            doc["questions"][0]["data_requests"][0]["field_coverage"][0]["still_needed"] = []
            (site / "questions.json").write_text(json.dumps(doc), encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(qe.main(["--rollup", str(site), "--out", str(out)]), 2)
            self.assertIn("field_coverage", err.getvalue())
            self.assertEqual({p.name: p.read_bytes() for p in out.iterdir()}, before)

    def test_committed_split_supply_example_reproduces(self):
        with tempfile.TemporaryDirectory() as tmp:
            run(["--model", str(EX / "field-coverage/model.json"), "--question", "H2"], tmp)
            for name in ("questions.json", "screen.md"):
                self.assertEqual((Path(tmp) / name).read_text(encoding="utf-8"),
                                 (EX / "field-coverage" / name).read_text(encoding="utf-8"))

    def test_rollup_rejects_incomplete_or_invented_subject_coverage(self):
        def missing_coverage(r):
            del r["field_coverage"]

        def unknown_subject(r):
            r["field_coverage"][0]["id"] = "NOT-AN-ASSET"

        def missing_value(r):
            del r["field_coverage"][0]["fields"][0]["value"]

        def missing_locator(r):
            del r["field_coverage"][0]["fields"][0]["where"]

        changes = [missing_coverage, unknown_subject, missing_value, missing_locator,
                   lambda r: r.update(field_coverage=[]), lambda r: r.update(already_on_drawing=17),
                   lambda r: r["field_coverage"][0]["fields"][0].update(value=None)]
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            original, _ = self.screen(self.model([{"steam_pressure": "8 bar"}, {"steam_temperature_C": 140}]), tmp)
            for change in changes:
                with self.subTest(change=change.__name__):
                    doc = copy.deepcopy(original)
                    change(doc["questions"][0]["data_requests"][0])
                    (site / "questions.json").write_text(json.dumps(doc), encoding="utf-8")
                    with self.assertRaisesRegex(qe.InputError, "field_coverage"):
                        qe.rollup([str(site)], CAT)

    def test_rollup_cannot_erase_a_known_unit_or_dereference_a_scalar_subject(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            original = copy.deepcopy(load("bayer"))
            for coverage in ([], [None], [17], ["subject"], [[]]):
                with self.subTest(coverage=coverage):
                    doc = copy.deepcopy(original)
                    request = next(r for r in finding(doc, "H4@E-3")["data_requests"] if r["item"] == "Cooler duty")
                    request["field_coverage"] = coverage
                    request["scope_note"] = "No owning equipment unit is identified."
                    (site / "questions.json").write_text(json.dumps(doc), encoding="utf-8")
                    with self.assertRaisesRegex(qe.InputError, "field_coverage"):
                        qe.rollup([str(site)], CAT)


class CollectionContractRepairs(unittest.TestCase):
    """Actual CLI regressions for ratings, source-scoped questions and ambiguous field intake."""

    example = EX / "pump-motor-basis"
    source_example = EX / "source-investigation"

    def cli(self, args, expected=0):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/question_engine.py"), *map(str, args)],
                                cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def test_pump_motor_and_duty_example_reproduces(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.cli(["--model", self.example / "model.json", "--question", "E1", "--question", "E2",
                      "--question", "E4", "--question", "H4", "--out", tmp])
            for name in ("questions.json", "screen.md"):
                self.assertEqual((Path(tmp) / name).read_text(encoding="utf-8"),
                                 (self.example / name).read_text(encoding="utf-8"))

    def test_scalar_and_document_candidates_cannot_close_larger_tasks(self):
        cases = [{}, {"pump_curve": True}, {"pump_curve_uri": "other.pdf", "pump_curve_asset": "P-901",
                                          "pump_curve_readable": False},
                 {"BEP_flow": 100, "BEP_head": 90, "motor_efficiency": 0.9, "full_load_efficiency": 0.9,
                  "input_power_kW": 0, "operating_hours": 8000, "heat_duty_kW": 100}]
        tasks = {"E1@P-900": {"Matched pump curve, rated duty and system operating points",
                              "Motor nameplate, efficiency and drive basis"},
                 "E2@P-900": {"Matched pump curve and best-efficiency-point (BEP) duty"},
                 "E4@P-900": {"Motor nameplate, rated output and full-load efficiency",
                              "Measured input power or current at normal load"},
                 "H4@E-900": {"Cooler duty"}}
        for values in cases:
            with self.subTest(values=values), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model = json.loads((self.example / "model.json").read_text(encoding="utf-8"))
                for unit in model["units"]:
                    unit["facts"].update(values)
                path = base / "model.json"
                path.write_text(json.dumps(model), encoding="utf-8")
                self.cli(["--model", path, "--out", base])
                doc = json.loads((base / "questions.json").read_text(encoding="utf-8"))
                for fid, required in tasks.items():
                    actual = {r["item"]: r for r in finding(doc, fid)["data_requests"]}
                    self.assertLessEqual(required, actual.keys())
                    for name in required:
                        self.assertIn("candidate_facts", actual[name])
                        self.assertNotIn("already_on_drawing", actual[name])
                cooler = next(r for r in finding(doc, "H4@E-900")["data_requests"] if r["item"] == "Cooler duty")
                self.assertEqual(cooler["candidate_scope"], "unit")
                self.assertTrue(any(f["name"] == "CAPACITY" and f["value"] == "100 gpm"
                                    for f in cooler["candidate_facts"]))
                self.assertEqual(gx.build(path, questions=base / "questions.json")["questions"], doc["questions"])
                qe.rollup([str(base)], CAT)

    def test_source_scoped_catalog_reproduces_and_retains_historical_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            self.cli(["--model", ROOT / "examples/from-description/mgpi/model-expanded-source.json",
                      "--catalog", self.source_example / "catalog.json", "--out", base])
            for name in ("questions.json", "screen.md"):
                self.assertEqual((base / name).read_text(encoding="utf-8"),
                                 (self.source_example / name).read_text(encoding="utf-8"))
            doc = json.loads((base / "questions.json").read_text(encoding="utf-8"))
            self.assertEqual(len(doc["questions"]), 2)
            self.assertTrue(all(q["data_requests"] for q in doc["questions"]))
            notify = finding(doc, "MGPI-NOTIFY@HYPO_BULK")
            endpoint = finding(doc, "MGPI-ENDPOINT@HYPO_BULK")
            self.assertIn("not configured to shut the transfer automatically", notify["limits"])
            self.assertIn("likely", notify["limits"])
            self.assertIn("not unloading-to-bulk flow", endpoint["limits"])
            self.assertIn("historical question", notify["decision_rule"])
            catalog = json.loads((self.source_example / "catalog.json").read_text(encoding="utf-8"))
            rolled = qe.rollup([str(base)], catalog)
            self.assertIn("MGPI", qe.render_rollup_md(rolled, catalog))

    def test_source_recipe_does_not_become_a_generic_level_checklist(self):
        models = [ROOT / "data/te_process_model.json", ROOT / "data/bayer_rt/process_model.json",
                  EX / "food_plant_model.json"]
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for n, path in enumerate(models):
                self.cli(["--model", path, "--catalog", self.source_example / "catalog.json", "--out", base / str(n)])
                doc = json.loads((base / str(n) / "questions.json").read_text(encoding="utf-8"))
                self.assertEqual(doc["questions"], [])
            # Default remains an honest zero; this authored recipe is not a generalization improvement.
            self.cli(["--model", ROOT / "examples/from-description/mgpi/model-expanded-source.json",
                      "--out", base / "default"])
            self.assertEqual(json.loads((base / "default/questions.json").read_text(encoding="utf-8"))["questions"], [])

    def intake(self, base, facts=None):
        model = {"meta": {"model_kind": "extracted_twin", "title": "fictional field intake"},
                 "units": [{"id": "P1", "tag": "P-1", "class": "pump", "sheets": ["1"],
                            "facts": facts or {}}], "instruments": [], "streams": []}
        path = base / "model.json"
        path.write_text(json.dumps(model), encoding="utf-8")
        return path

    def schedule(self, base, name, fields):
        path = base / name
        path.write_text(json.dumps({"sheets": {"1": [{"tag": "P-1", "service": "Water pump", "fields": fields}]}}),
                        encoding="utf-8")
        return path

    def test_disjoint_schedule_fields_merge_with_per_field_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model = self.intake(base)
            first = self.schedule(base, "first.json", {"HP": 10, "RPM": 1750})
            second = self.schedule(base, "second.json", {"CAPACITY": "100 gpm"})
            third = self.schedule(base, "third.json", {"DISCHARGE": "90 ft"})
            self.cli(["--model", model, "--schedule", first, "--schedule", second, "--schedule", third,
                      "--out", base / "reports"])
            doc = json.loads((base / "reports/questions.json").read_text(encoding="utf-8"))
            self.assertEqual(doc["schedules"], ["first.json", "second.json", "third.json"])
            motor = finding(doc, "E4@P1")
            evidence = next(e for e in motor["evidence"] if "HP = 10" in e["text"])
            self.assertIn("first.json", evidence["field"])
            loaded = qe.Model(model, schedule_paths=[third, second, first])
            self.assertEqual(qe.field_state(loaded.by_id["P1"], "HP")[1], 10)

    def test_ambiguous_inputs_refuse_before_overwriting_reports(self):
        cases = [("facts", {"HP": 10, "hp": 20}, None, None, "case-variant"),
                 ("fields", None, {"HP": 10, "hp": 20}, None, "case-variant"),
                 ("scheduleconflict", None, {"HP": 10}, {"hp": 20}, "conflicting schedule"),
                 ("typedconflict", None, {"HP": False}, {"hp": 0}, "conflicting schedule"),
                 ("factconflict", {"HP": 10}, {"hp": 20}, None, "conflicting model fact"),
                 ("whitespace", {" HP ": 10}, None, None, "surrounding whitespace")]
        for name, facts, fields, later, diagnostic in cases:
            with self.subTest(case=name), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model = self.intake(base, facts)
                out = base / "reports"
                out.mkdir()
                (out / "questions.json").write_text("prior JSON", encoding="utf-8")
                (out / "screen.md").write_text("prior report", encoding="utf-8")
                before = {p.name: p.read_bytes() for p in out.iterdir()}
                args = ["--model", model, "--out", out]
                if fields is not None:
                    args += ["--schedule", self.schedule(base, "first.json", fields)]
                if later is not None:
                    args += ["--schedule", self.schedule(base, "second.json", later)]
                result = self.cli(args, 2)
                self.assertIn(diagnostic, result.stderr)
                self.assertEqual({p.name: p.read_bytes() for p in out.iterdir()}, before)

    def test_duplicate_and_nonfinite_json_refuse(self):
        for raw in ['{"units":[],"units":[]}', '{"units":[],"value":NaN}', '{"units":[],"value":1e999}']:
            with self.subTest(raw=raw), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                path = base / "model.json"
                path.write_text(raw, encoding="utf-8")
                result = self.cli(["--model", path, "--out", base / "reports"], 2)
                self.assertIn("not valid JSON", result.stderr)
                self.assertFalse((base / "reports").exists())

    def test_identical_fields_and_opaque_qualifiers_survive(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model = self.intake(base, {"HP": {"value": 10, "basis": "unknown", "source": {"revision": "A"}}})
            first = self.schedule(base, "first.json", {"hp": {"value": 10, "basis": "unknown", "source": {"revision": "A"}}})
            self.cli(["--model", model, "--schedule", first, "--out", base / "reports"])
            loaded = qe.Model(model, schedule_paths=[first])
            self.assertEqual(qe.field_state(loaded.by_id["P1"], "HP")[1],
                             {"value": 10, "basis": "unknown", "source": {"revision": "A"}})

    def test_native_schedule_is_refused_instead_of_silently_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = self.schedule(base, "schedule.json", {"HP": 10})
            result = self.cli(["--model", self.example / "model.json", "--schedule", path,
                               "--out", base / "reports"], 2)
            self.assertIn("only to extracted twins", result.stderr)
            self.assertFalse((base / "reports").exists())


class SteamCollectionContracts(unittest.TestCase):
    """Public-model copies expose wrong units/basis without treating field presence as suitability."""

    cli = CollectionContractRepairs.cli
    ids_by_question = {"E11": "E11@stream:U1", "H1": "H1@S4-TK001", "H2": "H2@E-2"}
    tasks = {"E11": "Applicable surface-temperature and insulation evidence",
             "H1": "Matched station steam-throughput rating and conditions",
             "H2": "Applicable steam-supply conditions and operating basis"}

    def copied_model(self, qid, facts):
        relative = ("out/twin/r2-tiles-trace/codex/plant_model.json" if qid == "H1"
                    else "data/bayer_rt/process_model.json")
        model = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        target = (next(u for u in model["units"] if u["id"] == "S4-TK001") if qid == "H1"
                  else next(s for s in model["streams"] if s["id"] == "U1"))
        target["facts"] = copy.deepcopy(facts)
        if qid == "H2":
            next(v for v in model["final_elements"] if v["tag"] == "TV-104C")["facts"] = copy.deepcopy(facts)
        model.setdefault("meta", {})["audit_fixture"] = "Fictional software mutation of a public development model"
        return model

    def generate(self, base, qid, facts):
        path = base / "model.json"
        path.write_text(json.dumps(self.copied_model(qid, facts)), encoding="utf-8")
        before = path.read_bytes()
        args = ["--model", path, "--question", qid, "--out", base]
        if qid == "H1":
            args += ["--schedule", ROOT / "data/open100_equipment_schedule.json"]
        self.cli(args)
        self.assertEqual(path.read_bytes(), before)
        return json.loads((base / "questions.json").read_text(encoding="utf-8"))

    def test_wrong_basis_units_flags_and_rich_candidates_keep_review_tasks_open(self):
        cases = {
            "E11": [{}, {"normal_temperature_C": False}, {"normal_temperature_C": 0},
                    {"normal_temperature_C": None},
                    {"normal_temperature_C": {"value": 150, "basis": "design fluid; surface unknown", "status": "draft"}},
                    {"normal_temperature_C": 150, "insulation_survey": "wrong-asset.pdf",
                     "insulation_survey_asset": "OTHER", "insulation_survey_readable": False},
                    {"normal_temperature_C": 150, "surface_temperature_C": 75,
                     "surface_temperature_basis": {"source": "survey", "period": "example", "status": "unreviewed"},
                     "insulation_condition": "bare? draft observation"}],
            "H1": [{}, {"CAPACITY": False}, {"CAPACITY": 0}, {"CAPACITY": None},
                   {"CAPACITY": "500 gal internal volume"},
                   {"CAPACITY": "500 gal", "rating_document": "wrong-asset.pdf", "rating_asset": "OTHER",
                    "rating_document_readable": False},
                   {"CAPACITY": "3000 lb/hr", "rated_steam_flow": 3000, "rated_steam_flow_uom": "lb/hr",
                    "rating_conditions": {"basis": "vendor rating; actual duration unknown", "status": "unreviewed"}}],
            "H2": [{}, {"steam_pressure": False, "steam_temperature_C": False},
                   {"steam_pressure": 0, "steam_temperature_C": 0},
                   {"steam_pressure": None, "steam_temperature_C": "  "},
                   {"steam_pressure": {"value": 10, "units": "bar", "reference": "unknown", "basis": "design"},
                    "steam_temperature_C": {"value": 300, "basis": "different time/location", "status": "draft"}},
                   {"steam_pressure": "10 bar", "steam_temperature_C": 300, "steam_supply_asset": "OTHER",
                    "steam_conditions_source": "unreadable.pdf", "steam_conditions_readable": False},
                   {"steam_pressure": "10 bar", "steam_temperature_C": 300, "steam_state": "superheated candidate",
                    "steam_pressure_reference": "absolute", "steam_conditions_period": {"period": "example", "status": "unreviewed"}}]}
        for qid, variants in cases.items():
            for facts in variants:
                with self.subTest(question=qid, facts=facts), tempfile.TemporaryDirectory() as tmp:
                    base = Path(tmp)
                    doc = self.generate(base, qid, facts)
                    selected = finding(doc, self.ids_by_question[qid])
                    task = next(r for r in selected["data_requests"] if r["item"] == self.tasks[qid])
                    self.assertIn("candidate_facts", task)
                    self.assertNotIn("already_on_drawing", task)
                    self.assertNotIn("still_needed", task)
                    for fact in task["candidate_facts"]:
                        self.assertEqual(fact["value"], facts[fact["name"]])
                        self.assertIn(".facts.", fact["where"])
                    graph = gx.build(base / "model.json", questions=base / "questions.json")
                    self.assertEqual(graph["questions"], doc["questions"])
                    qe.rollup([str(base)], CAT)
                    self.assertIn("collection/review request remains open", (base / "screen.md").read_text(encoding="utf-8"))

    def test_missing_new_review_tasks_refuse_rollup_without_changing_reports(self):
        for qid in self.tasks:
            with self.subTest(question=qid), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                doc = self.generate(base, qid, {})
                selected = finding(doc, self.ids_by_question[qid])
                selected["data_requests"] = [r for r in selected["data_requests"] if r["item"] != self.tasks[qid]]
                (base / "questions.json").write_text(json.dumps(doc), encoding="utf-8")
                out = base / "rollup"
                out.mkdir()
                (out / "rollup.json").write_text("prior JSON", encoding="utf-8")
                (out / "rollup.md").write_text("prior Markdown", encoding="utf-8")
                before = {p.name: p.read_bytes() for p in out.iterdir()}
                result = self.cli(["--rollup", base, "--out", out], 2)
                self.assertIn("missing_required", result.stderr)
                self.assertEqual({p.name: p.read_bytes() for p in out.iterdir()}, before)

    def test_stated_field_accounting_does_not_claim_semantic_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            doc = self.generate(base, "H1", {"CAPACITY": "500 gal internal volume"})
            selected = finding(doc, self.ids_by_question["H1"])
            self.assertNotIn("Stated station capacity", {r["item"] for r in selected["data_requests"]})
            self.assertIn(self.tasks["H1"], {r["item"] for r in selected["data_requests"]})
            self.assertTrue(any("500 gal internal volume" in e["text"] for e in selected["evidence"]))
            self.assertIn("not actual flow-duration", next(r for r in selected["data_requests"]
                                                         if r["item"] == self.tasks["H1"])["how"])


class RefrigerationCollectionContracts(unittest.TestCase):
    """Source-informed development controls: quantity labels and unrelated trains cannot settle collection."""

    cli = CollectionContractRepairs.cli
    tasks = {"C12": "Applicable real-input-power and coincident operating basis",
             "E28": "Suction-level membership and reset coverage",
             "H5": "Recovery coverage by refrigeration train and heating duty"}

    def model(self):
        model = json.loads((EX / "food_plant_model.json").read_text(encoding="utf-8"))
        model["meta"]["audit_fixture"] = "Fictional mutation of the illustrative food model; no new observation"
        return model

    def screen(self, base, model, qid):
        source = base / "model.json"
        source.write_text(json.dumps(model), encoding="utf-8")
        before = source.read_bytes()
        self.cli(["--model", source, "--question", qid, "--out", base / "screen"])
        self.assertEqual(source.read_bytes(), before)
        doc = json.loads((base / "screen/questions.json").read_text(encoding="utf-8"))
        return doc, finding(doc, qid + "@model")

    def assert_open(self, selected, qid):
        task = next(r for r in selected["data_requests"] if r["item"] == self.tasks[qid])
        self.assertNotIn("already_on_drawing", task)
        self.assertNotIn("still_needed", task)
        self.assertIn("K-201", {a["id"] for a in selected["assets"]})
        return task

    def test_electrical_quantities_and_claims_retain_actual_real_input_basis(self):
        # DOE motor-input basis requires more than amperes, volts, or a supplied power label.
        # Even an explicitly real-kW-labelled candidate is not authenticated, representative operating data.
        cases = [("IT-201", "current", "A", "current only"),
                 ("ET-201", "voltage", "V", "voltage only"),
                 ("EQ-201", "energy", "kWh", "cumulative energy without interval"),
                 ("JT-201", "power", "kVA", "apparent power"),
                 ("JT-201", "power", "kvar", "reactive power"),
                 ("JT-201", "power", "unknown", "unverified quantity"),
                 ("OTHER-201", "power", "kW", "supplied real input power"),
                 ("JT-201", "unknown", "kW", "typed claim with unknown quantity"),
                 ("JT-201", "power", "kW", "average real power from supplied matching energy delta and interval")]
        for tag, variable, uom, meaning in cases:
            with self.subTest(quantity=meaning), tempfile.TemporaryDirectory() as tmp:
                base, model = Path(tmp), self.model()
                reading = next(i for i in model["instruments"] if i["tag"] == "JT-201")
                reading.update(tag=tag, variable=variable, uom=uom,
                               description=meaning + " (" + uom + ")",
                               facts={"reading_basis": {"value": 0, "uom": uom, "status": "draft",
                                                        "readable": False, "period": None}})
                doc, selected = self.screen(base, model, "C12")
                self.assert_open(selected, "C12")
                self.assertIn(tag, {a["id"] for a in selected["assets"]})
                self.assertTrue(any(meaning in e["text"] for e in selected["evidence"]))
                self.assertNotIn("no power measurement", json.dumps(selected))
                graph = gx.build(base / "model.json", questions=base / "screen/questions.json")
                self.assertEqual(graph["questions"], doc["questions"])
                self.assertIn("reading_basis", json.dumps(graph))
                self.assertIn(uom, json.dumps(graph))

    def test_reset_and_recovery_candidates_cannot_hide_other_trains(self):
        for case in ("unrelated_reset", "own_reset", "owned_reset", "unrelated_recovery", "local_recovery"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                base, model = Path(tmp), self.model()
                qid = "E28" if "reset" in case else "H5"
                if case == "unrelated_reset":
                    model["units"].append({"id": "K-999", "type": "compressor",
                                           "name": "Ammonia compressor, floating suction on disconnected train"})
                elif case == "own_reset":
                    model["units"][0]["name"] += "; floating suction on K-201 only"
                elif case == "owned_reset":
                    model["controllers"].append({"tag": "PIC-999", "unit": "K-201", "measurement": "PT-201",
                                                  "description": "Floating suction for K-201 only"})
                else:
                    model["units"].append({"id": "HX-999", "type": "heat_exchanger",
                                           "name": "Ammonia heat recovery, supplied coverage unverified"})
                    if case == "local_recovery":
                        model["streams"].append({"id": "R999", "from": "K-201", "to": "HX-999",
                                                 "name": "Supplied discharge connection, coverage unverified"})
                # Unequal approaches mean even a generic 'coldest room governs' shortcut is insufficient.
                for uid, required, approach in [("EV-201", -20, 1), ("EV-202", 4, 30)]:
                    next(u for u in model["units"] if u["id"] == uid)["facts"] = {
                        "required_temperature_C": required, "approach_K": approach,
                        "served_suction_level": "unverified", "status": "draft"}
                _, selected = self.screen(base, model, qid)
                self.assert_open(selected, qid)
                self.assertLessEqual({"K-201", "K-202", "K-203"}, {a["id"] for a in selected["assets"]})
                if qid == "E28":
                    self.assertNotIn("warmest load on a suction level", json.dumps(selected))
                    self.assertIn("every coincident load", json.dumps(selected).lower())
                    self.assertIn("approach", json.dumps(selected).lower())
                else:
                    self.assertIn("HX-999", {a["id"] for a in selected["assets"]})
                    self.assertNotIn("no desuperheater or refrigeration heat recovery exchanger anywhere",
                                     json.dumps(selected))

    def test_new_basis_tasks_survive_context_and_omission_is_refused(self):
        for qid in self.tasks:
            with self.subTest(question=qid), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                doc, selected = self.screen(base, self.model(), qid)
                self.assert_open(selected, qid)
                sources = base / "sources.json"
                sources.write_text(json.dumps({"schema": "context-sources-1", "documents": []}), encoding="utf-8")
                result = subprocess.run([sys.executable, str(ROOT / "scripts/context_register.py"), "prepare",
                                         "--model", str(base / "model.json"), "--questions",
                                         str(base / "screen/questions.json"), "--sources", str(sources),
                                         "--out", str(base / "context")], cwd=ROOT, capture_output=True,
                                        text=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stderr)
                enriched = json.loads((base / "context/enriched_questions.json").read_text(encoding="utf-8"))
                self.assertEqual([{k: v for k, v in f.items() if k != "context"}
                                  for f in enriched["questions"]], doc["questions"])
                selected["data_requests"] = [r for r in selected["data_requests"] if r["item"] != self.tasks[qid]]
                (base / "screen/questions.json").write_text(json.dumps(doc), encoding="utf-8")
                refused = self.cli(["--rollup", base / "screen", "--out", base / "rollup"], 2)
                self.assertIn("missing_required", refused.stderr)
                self.assertFalse((base / "rollup").exists())


class CondenserTrainCollectionContracts(unittest.TestCase):
    """Two fictional disconnected condensers: supplied reset text cannot settle either operating basis."""

    cli = CollectionContractRepairs.cli
    task = "Condenser-train coverage and applicable head-pressure operating basis"

    def model(self):
        return {"meta": {"model_id": "fictional-condenser-trains",
                         "title": "Synthetic collection-contract regression; no plant observations"},
                "units": [{"id": "CA", "type": "condenser", "name": "Ammonia condenser A"},
                          {"id": "CB", "type": "condenser", "name": "Ammonia condenser B"},
                          {"id": "CC", "type": "vessel", "name": "Unrelated vessel C"}],
                "streams": [], "instruments": [], "controllers": [], "final_elements": []}

    def screen(self, base, model):
        source = base / "model.json"
        source.write_text(json.dumps(model), encoding="utf-8")
        before = source.read_bytes()
        self.cli(["--model", source, "--question", "E27", "--out", base / "screen"])
        self.assertEqual(source.read_bytes(), before)
        return json.loads((base / "screen/questions.json").read_text(encoding="utf-8"))

    def assert_both_open(self, doc):
        self.assertEqual(ids(doc), {"E27@CA", "E27@CB"})
        for uid in ("CA", "CB"):
            selected = finding(doc, "E27@" + uid)
            self.assertIn(uid, {a["id"] for a in selected["assets"]})
            task = next(r for r in selected["data_requests"] if r["item"] == self.task)
            self.assertNotIn("already_on_drawing", task)
            self.assertNotIn("still_needed", task)
        return doc

    def test_reset_scope_and_qualified_labels_keep_both_train_reviews_open(self):
        cases = [("none", None, None),
                 ("local", "CA", "Floating head pressure for A only"),
                 ("wet_bulb", "CA", "Wet-bulb reset for A only"),
                 ("unrelated", "CC", "Floating head pressure for unrelated C"),
                 ("unknown", None, "Head pressure reset, target unknown"),
                 ("contradictory", "CA", "Floating head pressure for B; disabled; draft"),
                 ("negated", "CA", "No floating head pressure; reset disabled"),
                 ("shared", "CA", "Floating head pressure explicitly shared by A and B"),
                 ("own_label", None, None),
                 ("rejected", "CA", "Floating head pressure, rejected record")]
        for case, unit, description in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                base, model = Path(tmp), self.model()
                if description is not None:
                    controller = {"tag": "PIC-1", "description": description,
                                  "source": "Synthetic source revision R1",
                                  "facts": {"enabled": {"value": False},
                                            "target": {"value": "unknown", "status": "draft"}}}
                    if unit is not None:
                        controller["unit"] = unit
                    if case == "rejected":
                        controller["ops_review"] = {"status": "rejected"}
                    model["controllers"].append(controller)
                if case == "own_label":
                    model["units"][0]["name"] += "; floating head pressure on A only"
                doc = self.assert_both_open(self.screen(base, model))
                graph = gx.build(base / "model.json", questions=base / "screen/questions.json")
                self.assertEqual(graph["questions"], doc["questions"])
                if description is not None and case != "rejected":
                    self.assertTrue(any(description in e["text"]
                                        for q in doc["questions"] for e in q["evidence"]))
                if case == "rejected":
                    self.assertFalse(any(description in e["text"]
                                         for q in doc["questions"] for e in q["evidence"]))

    def test_nonrefrigeration_and_rejected_condensers_do_not_trigger(self):
        for case in ("nonrefrigeration", "rejected"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                model = self.model()
                for unit in model["units"][:2]:
                    if case == "rejected":
                        unit["ops_review"] = {"status": "rejected"}
                    else:
                        unit["name"] = "Process water condenser"
                self.assertEqual(ids(self.screen(Path(tmp), model)), set())

    def test_named_rollup_retains_basis_and_refuses_missing_task_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            doc = self.assert_both_open(self.screen(base, self.model()))
            self.cli(["--rollup", "synthetic=" + str(base / "screen"), "--out", base / "rollup"])
            rolled = json.loads((base / "rollup/rollup.json").read_text(encoding="utf-8"))
            text = json.dumps(rolled)
            self.assertIn(self.task, text)
            self.assertIn("synthetic", text)
            selected = finding(doc, "E27@CB")
            selected["data_requests"] = [r for r in selected["data_requests"] if r["item"] != self.task]
            (base / "screen/questions.json").write_text(json.dumps(doc), encoding="utf-8")
            refused = self.cli(["--rollup", base / "screen", "--out", base / "refused"], 2)
            self.assertIn("missing_required", refused.stderr)
            self.assertFalse((base / "refused").exists())



class MachineFunctionCollectionContracts(unittest.TestCase):
    """C9 is record collection: a supplied trip label cannot settle another machine or actual protection."""

    cli = CollectionContractRepairs.cli
    task = "Machine/function association and current evidence"

    def model(self, case):
        model = {"meta": {"title": "Fictional mixed-machine association control", "illustrative": True},
                 "units": [{"id": "K-901", "name": "Fictional compressor A", "type": "compressor"},
                           {"id": "B-902", "name": "Fictional boiler B", "type": "boiler"}],
                 "streams": [],
                 "instruments": [{"tag": "PT-901", "unit": "K-901", "variable": "pressure",
                                  "description": "Fictional A pressure"}],
                 "final_elements": [{"tag": "MTR-901", "unit": "K-901", "description": "Fictional motor contactor"},
                                    {"tag": "MV-902", "unit": "B-902", "description": "Fictional burner final element"}],
                 "interlocks": []}
        trip = {"id": "IL-901", "class": "safety", "cause": "Supplied condition at PT-901",
                "effect": "STOP K-901 only", "measurement": "PT-901", "final_element": "MTR-901",
                "source": "Fictional unverified function record; not installed or tested",
                "facts": {"record_status": "draft", "proof_tested": False, "revision": 0, "unknown": None}}
        if case != "none":
            model["interlocks"] = [trip]
        if case == "unrelated":
            model["units"].append({"id": "P-903", "name": "Fictional unrelated pump C", "type": "pump"})
            model["final_elements"].append({"tag": "MTR-903", "unit": "P-903", "description": "C contactor"})
            trip.update(effect="TRIP unrelated P-903 only", final_element="MTR-903")
        elif case == "unknown":
            trip.pop("measurement"); trip.pop("final_element")
            trip.update(cause="Unknown initiating condition", effect="SHUTDOWN target unknown")
        elif case == "contradictory":
            trip["final_element"] = "MV-902"  # Preserve conflict with supplied A-only text, never normalize it.
        elif case == "shared":
            trip["shared_record"] = "Supplied two-target function; coverage/effectiveness unverified"
            other = copy.deepcopy(trip); other.update(id="IL-902", effect="STOP B-902 only", final_element="MV-902")
            model["interlocks"].append(other)
        elif case == "rejected":
            trip["ops_review"] = {"status": "rejected", "by": "Fictional test", "on": "2026-10-30"}
        elif case == "switch":
            model["interlocks"] = []
            model["instruments"].append({"tag": "BMS-902", "unit": "B-902", "variable": "unknown",
                                         "description": "Supplied burner-management indication, scope unverified"})
        return model

    def generate(self, base, case):
        model = self.model(case); path = base / "model.json"
        path.write_text(json.dumps(model), encoding="utf-8"); before = path.read_bytes()
        self.cli(["--model", path, "--question", "C9", "--out", base / "screen"])
        self.assertEqual(path.read_bytes(), before)
        doc = json.loads((base / "screen/questions.json").read_text(encoding="utf-8"))
        selected = finding(doc, "C9@model")
        self.assertIsNotNone(selected)
        self.assertEqual({e["id"] for e in selected["evidence"] if e["role"] == "trigger"},
                         {u["id"] for u in model["units"]})
        self.assertIn(self.task, {r["item"] for r in selected["data_requests"]})
        self.assertFalse(any(e["role"] == "checked, none found" for e in selected["evidence"]))
        return model, doc, selected

    def test_local_unrelated_shared_unknown_and_rejected_candidates_keep_machine_review(self):
        for case in ("none", "local", "unrelated", "unknown", "contradictory", "shared", "rejected", "switch"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                _, _, selected = self.generate(Path(tmp), case)
                evidence = {e.get("id") for e in selected["evidence"]}
                if case not in ("none", "rejected", "switch"):
                    self.assertIn("IL-901", evidence)
                if case == "shared":
                    self.assertIn("IL-902", evidence)
                if case == "rejected":
                    self.assertNotIn("IL-901", evidence)
                if case == "switch":
                    self.assertIn("BMS-902", evidence)
                self.assertIn("Missing or unknown model evidence does not establish missing installed protection",
                              selected["limits"])
                self.assertIn("no primary safety-design source", selected["limits"])

    def test_raw_targets_and_qualifiers_survive_context_and_snapshot_without_approval(self):
        import serve_snapshot
        for case in ("unknown", "shared", "contradictory"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp); model, doc, _ = self.generate(base, case)
                sources = base / "sources.json"
                sources.write_text(json.dumps({"schema": "context-sources-1", "documents": []}), encoding="utf-8")
                result = subprocess.run([sys.executable, str(ROOT / "scripts/context_register.py"), "prepare",
                                         "--model", str(base / "model.json"), "--questions",
                                         str(base / "screen/questions.json"), "--sources", str(sources),
                                         "--out", str(base / "context")], cwd=ROOT, capture_output=True,
                                        text=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stderr)
                enriched = json.loads((base / "context/enriched_questions.json").read_text(encoding="utf-8"))
                self.assertEqual([{k: v for k, v in q.items() if k != "context"}
                                  for q in enriched["questions"]], doc["questions"])
                snapshot = serve_snapshot.Snapshot(base / "context/enriched_graph.json", base / "context/context.json")
                self.assertEqual(snapshot.question("C9@model")["result"], enriched["questions"][0])
                for original in model["interlocks"]:
                    asset = snapshot.asset(original["id"])["result"]
                    self.assertEqual(asset["status"], "unverified")
                    claims = {a["name"]: a["value"] for a in asset["attributes"]}
                    self.assertEqual(claims["cause"], original["cause"])
                    self.assertEqual(claims["effect"], original["effect"])
                    for key, value in original["facts"].items():
                        self.assertEqual(claims[key], value)
                    edges = snapshot.relations(original["id"], 100)["result"]["relations"]
                    if "final_element" in original:
                        self.assertTrue(any(e["type"] == "acts_on" and e["to"] == original["final_element"]
                                            and e["status"] == "unverified" for e in edges))
                    else:
                        self.assertFalse(any(e["type"] == "acts_on" for e in edges))
                self.assertEqual(json.loads((base / "context/context.json").read_text(encoding="utf-8"))["decisions"], [])

    def test_rollup_refuses_omitted_machine_basis_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); _, doc, selected = self.generate(base, "local")
            selected["data_requests"] = [r for r in selected["data_requests"] if r["item"] != self.task]
            (base / "screen/questions.json").write_text(json.dumps(doc), encoding="utf-8")
            result = self.cli(["--rollup", base / "screen", "--out", base / "rollup"], 2)
            self.assertIn("missing_required", result.stderr)
            self.assertFalse((base / "rollup").exists())


class ServiceReconciliation(unittest.TestCase):
    """Exact imported service choices replace input-order selection, without claiming approval."""

    cli = CollectionContractRepairs.cli
    intake = CollectionContractRepairs.intake
    schedule = CollectionContractRepairs.schedule

    def sources(self, base):
        model = self.intake(base)
        first = self.schedule(base, "water.json", {"HP": 10})
        second = self.schedule(base, "refrigeration.json", {"HP": 10})
        value = json.loads(second.read_text(encoding="utf-8"))
        value["sheets"]["1"][0]["service"] = "Ammonia refrigeration compressor"
        second.write_text(json.dumps(value), encoding="utf-8")
        return model, first, second

    def declaration(self, first="water.json", second="refrigeration.json", selected=0):
        candidates = [{"file": first, "row": 1, "service": "Water pump"},
                      {"file": second, "row": 1, "service": "Ammonia refrigeration compressor"}]
        return {"candidates": candidates, "selected": candidates[selected],
                "basis": "Fictional imported service choice; needs source review", "status": "draft"}

    def attach(self, path, resolution):
        value = json.loads(path.read_text(encoding="utf-8"))
        value["sheets"]["1"][0]["service_resolution"] = resolution
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_conflicting_services_refuse_in_both_orders_before_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model, first, second = self.sources(base)
            out = base / "reports"
            out.mkdir()
            (out / "questions.json").write_text("previous JSON", encoding="utf-8")
            (out / "screen.md").write_text("previous Markdown", encoding="utf-8")
            prior = {p.name: p.read_bytes() for p in out.iterdir()}
            for a, b in ((first, second), (second, first)):
                result = self.cli(["--model", model, "--schedule", a, "--schedule", b, "--out", out], 2)
                self.assertIn("conflicting schedule service", result.stderr)
                self.assertEqual({p.name: p.read_bytes() for p in out.iterdir()}, prior)

    def test_exact_draft_choice_is_order_independent_and_retained_in_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model, first, second = self.sources(base)
            self.attach(second, self.declaration())
            packets = []
            for n, (a, b) in enumerate(((first, second), (second, first))):
                out = base / str(n)
                self.cli(["--model", model, "--schedule", a, "--schedule", b, "--out", out])
                doc = json.loads((out / "questions.json").read_text(encoding="utf-8"))
                self.assertEqual(ids(doc), {"E4@P1", "C9@model"})
                resolution = doc["service_reconciliations"][0]
                self.assertEqual({r["service"] for r in resolution["candidates"]},
                                 {"Water pump", "Ammonia refrigeration compressor"})
                self.assertIn("unverified", resolution["authority"])
                self.assertEqual(resolution["declarations"][0]["status"], "draft")
                self.assertTrue(any(e.get("service_reconciliation") == resolution
                                    for q in doc["questions"] for e in q["evidence"]))
                self.assertEqual(gx.build(model, questions=out / "questions.json")["questions"], doc["questions"])
                self.assertIn("Supplied service choice, unverified", (out / "screen.md").read_text(encoding="utf-8"))
                packets.append({p.name: p.read_bytes() for p in out.iterdir()})
            self.assertEqual(packets[0], packets[1])

    def test_stale_unknown_and_malformed_declarations_refuse(self):
        good = self.declaration()
        def duplicate(value):
            value["candidates"].append(copy.deepcopy(value["candidates"][0]))
        mutations = [lambda value: value.update(basis="  "), lambda value: value.update(status="accepted"),
                     lambda value: value.update(status=[]), lambda value: value.update(selected={}),
                     lambda value: value["selected"].update(file="missing.json"), duplicate,
                     lambda value: value["candidates"][0].update(row=2),
                     lambda value: value["candidates"][0].update(service="different source text"),
                     lambda value: value.pop("basis"), lambda value: value.update(extra="ignored?")]
        for mutate in mutations:
            with self.subTest(mutation=mutate), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model, first, second = self.sources(base)
                resolution = copy.deepcopy(good)
                mutate(resolution)
                self.attach(second, resolution)
                result = self.cli(["--model", model, "--schedule", first, "--schedule", second,
                                   "--out", base / "reports"], 2)
                self.assertIn("service_resolution", result.stderr)
                self.assertFalse((base / "reports").exists())

    def test_multiple_declarations_are_retained_but_conflicting_choices_refuse(self):
        for selected in (0, 1):
            with self.subTest(selected=selected), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model, first, second = self.sources(base)
                self.attach(first, self.declaration())
                other = self.declaration(selected=selected)
                other.update(status="reviewed", basis="Another supplied declaration; no authenticated approval")
                self.attach(second, other)
                result = self.cli(["--model", model, "--schedule", first, "--schedule", second,
                                   "--out", base / "reports"], 2 if selected else 0)
                if selected:
                    self.assertIn("conflicting service_resolution", result.stderr)
                else:
                    doc = json.loads((base / "reports/questions.json").read_text(encoding="utf-8"))
                    resolution = doc["service_reconciliations"][0]
                    self.assertEqual(len(resolution["declarations"]), 2)
                    self.assertEqual({r["status"] for r in resolution["declarations"]}, {"draft", "reviewed"})
                    self.assertIn("organizational approval unverified", resolution["authority"])

    def test_identical_and_blank_services_do_not_create_conflicts(self):
        for value in (None, "", "  ", "Water pump"):
            with self.subTest(service=value), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model, first, second = self.sources(base)
                data = json.loads(second.read_text(encoding="utf-8"))
                data["sheets"]["1"][0]["service"] = value
                second.write_text(json.dumps(data), encoding="utf-8")
                for n, (a, b) in enumerate(((first, second), (second, first))):
                    out = base / str(n)
                    self.cli(["--model", model, "--schedule", a, "--schedule", b, "--out", out])
                    doc = json.loads((out / "questions.json").read_text(encoding="utf-8"))
                    self.assertEqual(ids(doc), {"E4@P1", "C9@model"})
                    self.assertNotIn("service_reconciliations", doc)

    def test_changed_source_set_or_asset_identity_cannot_reuse_a_declaration(self):
        for changed in ("missing_source", "identity", "text", "row"):
            with self.subTest(changed=changed), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model, first, second = self.sources(base)
                self.attach(second, self.declaration())
                data = json.loads(first.read_text(encoding="utf-8"))
                if changed == "identity":
                    data["sheets"]["1"][0]["tag"] = "P-OTHER"
                elif changed == "text":
                    data["sheets"]["1"][0]["service"] = "Changed description"
                elif changed == "row":
                    data["sheets"]["1"].insert(0, {"tag": "P-OTHER", "service": "Other pump"})
                first.write_text(json.dumps(data), encoding="utf-8")
                args = ["--model", model, "--schedule", second, "--out", base / "reports"]
                if changed != "missing_source":
                    args += ["--schedule", first]
                result = self.cli(args, 2)
                self.assertIn("stale or mismatched service_resolution", result.stderr)
                self.assertFalse((base / "reports").exists())

    def test_unmatched_asset_declarations_and_nontext_services_do_not_escape_validation(self):
        for service in (False, 23, [], {}, "Water pump"):
            with self.subTest(service=service), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model = self.intake(base)
                schedule = self.schedule(base, "other.json", {})
                value = json.loads(schedule.read_text(encoding="utf-8"))
                value["sheets"]["1"][0].update(tag="unmatched", service=service)
                if service == "Water pump":
                    value["sheets"]["1"][0]["service_resolution"] = {}
                schedule.write_text(json.dumps(value), encoding="utf-8")
                result = self.cli(["--model", model, "--schedule", schedule, "--out", base / "reports"], 2)
                self.assertIn("service", result.stderr)

    def test_open100_resolutions_are_explicit_and_original_transcriptions_remain(self):
        paths = ["data/open100_equipment_schedule.json", "examples/opportunity-screen/open100_schedule_fields.json"]
        original = json.loads((ROOT / paths[0]).read_text(encoding="utf-8"))
        supplements = json.loads((ROOT / paths[1]).read_text(encoding="utf-8"))
        self.assertEqual(sum("service_resolution" in r for rows in supplements["sheets"].values() for r in rows), 3)
        entries = qe.load_schedule([ROOT / p for p in paths])
        reversed_entries = qe.load_schedule([ROOT / p for p in reversed(paths)])
        for sheet in ("2", "3", "4"):
            row = next(r for r in original["sheets"][sheet] if r["tag"] == "CND-TK-165")
            self.assertIn(row["service"], {"DEAREATOR STORAGE TANK", "DEAREATER STORAGE TANK"})
            resolution = entries[(sheet, "CND-TK-165")]["service_reconciliation"]
            self.assertEqual(resolution, reversed_entries[(sheet, "CND-TK-165")]["service_reconciliation"])
            self.assertEqual(resolution["selected"]["service"], "DEAERATOR STORAGE TANK")
            self.assertEqual(resolution["declarations"][0]["status"], "draft")

    def test_resolution_inputs_are_protected_from_output_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model, first, second = self.sources(base)
            target = base / "screen.md"
            first.rename(target)
            self.attach(second, self.declaration(first="screen.md"))
            (base / "questions.json").write_text("previous JSON", encoding="utf-8")
            prior = {p.name: p.read_bytes() for p in base.iterdir() if p.is_file()}
            result = self.cli(["--model", model, "--schedule", target, "--schedule", second, "--out", base], 2)
            self.assertIn("overlaps input", result.stderr)
            self.assertEqual({p.name: p.read_bytes() for p in base.iterdir() if p.is_file()}, prior)


class CollectionBasis(unittest.TestCase):
    """Scalar candidates cannot stand in for performance documents or representative operating records."""

    example = EX / "collection-basis"

    def screen(self, facts=None):
        model = json.loads((self.example / "model.json").read_text(encoding="utf-8"))
        if facts:
            for unit in model["units"]:
                unit["facts"].update(facts)
        return model

    def generate(self, tmp, facts=None, catalog=None):
        model = self.screen(facts)
        path = Path(tmp) / "model.json"
        path.write_text(json.dumps(model), encoding="utf-8")
        args = ["--model", str(path), "--question", "E5", "--question", "H3"]
        if catalog:
            cp = Path(tmp) / "catalog.json"
            cp.write_text(json.dumps(catalog), encoding="utf-8")
            args += ["--catalog", str(cp)]
        return run(args, tmp)[1]

    def test_nameplate_and_rich_raw_candidates_keep_collection_review_open(self):
        cases = [None, {"input_power_kW": 10}, {"operating_hours": 8000},
                 {"fan_curve_uri": "F-2-curve.pdf", "fan_curve_asset": "F-2", "fan_curve_readable": False},
                 {"fan_curve": True, "fan_curve_uri": "F-1-curve.pdf", "input_power_kW": 10,
                  "operating_hours": 8000, "energy_kWh": 80000, "control_mode": "mixed manual/bypass"}]
        for values in cases:
            with self.subTest(values=values), tempfile.TemporaryDirectory() as tmp:
                doc = self.generate(tmp, values)
                fan, heater = finding(doc, "E5@F-1"), finding(doc, "H3@EH-1")
                self.assertEqual(len(fan["data_requests"]), 4)
                self.assertEqual(len(heater["data_requests"]), 3)
                self.assertTrue(all(r["state"] == "not_on_drawing" for f in (fan, heater) for r in f["data_requests"]))
                self.assertFalse(any("still_needed" in r or "already_on_drawing" in r
                                     for f in (fan, heater) for r in f["data_requests"]))
                facts = [v for f in (fan, heater) for r in f["data_requests"] for v in r.get("candidate_facts", [])]
                self.assertTrue(any(v["name"] == "HP" and v["id"] == "F-1" and v["value"] == 15 for v in facts))
                if values and "fan_curve_readable" in values:
                    self.assertTrue(any(v["name"] == "fan_curve_readable" and v["value"] is False for v in facts))
                md = (Path(tmp) / "screen.md").read_text(encoding="utf-8")
                self.assertIn("collection/review request remains open", md)
                self.assertIn("representative period", md)
                self.assertIn("a URI or present/readable flag", md)
                self.assertIn("original units", md)

    def test_candidate_values_case_and_locator_survive_rollup_and_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = self.generate(tmp, {"INPUT_POWER_KW": 0, "fan_curve_readable": False})
            r = next(r for r in finding(doc, "E5@F-1")["data_requests"] if r["item"] == "Fan electrical-input and load history")
            fact = next(f for f in r["candidate_facts"] if f["name"] == "input_power_kW")
            self.assertEqual(fact["value"], 0)
            self.assertEqual(fact["where"], "units[F-1].facts.INPUT_POWER_KW")
            graph = gx.build(Path(tmp) / "model.json", questions=Path(tmp) / "questions.json")
            self.assertEqual(graph["questions"], doc["questions"])
            rolled = qe.rollup(["A=" + tmp, "B=" + tmp], CAT)
            rr = next(q for q in rolled["questions"] if q["question_id"] == "E5")
            request = next(x for x in rr["data_requests"] if x["item"] == r["item"])
            for site in request["sites"]:
                self.assertEqual(site["coverage_by_finding"][0]["candidate_facts"], r["candidate_facts"])
            self.assertEqual(qe.render_rollup_md(rolled, CAT).count("units[F-1].facts.INPUT_POWER_KW"), 2)

    def test_supplied_facts_never_count_toward_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalog = copy.deepcopy(CAT)
            r = next(q for q in catalog["questions"] if q["id"] == "E5")["data_requests"][0]
            r["fields"] = ["reviewed_period"]
            doc = self.generate(tmp, {"damper_position": 40}, catalog)
            request = finding(doc, "E5@F-1")["data_requests"][0]
            self.assertEqual(request["still_needed"], ["reviewed_period"])
            self.assertNotIn("already_on_drawing", request)
            self.assertEqual(request["candidate_facts"][0]["value"], 40)

    def test_committed_collection_reports_reproduce(self):
        with tempfile.TemporaryDirectory() as tmp:
            run(["--model", str(self.example / "model.json"), "--question", "E5", "--question", "H3"], tmp)
            for name in ("questions.json", "screen.md"):
                self.assertEqual((Path(tmp) / name).read_text(encoding="utf-8"),
                                 (self.example / name).read_text(encoding="utf-8"))

    def test_rollup_cannot_erase_always_open_collection_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = self.generate(tmp)
            for requests in ([], original["questions"][0]["data_requests"][1:]):
                with self.subTest(count=len(requests)):
                    doc = copy.deepcopy(original)
                    doc["questions"][0]["data_requests"] = requests
                    (Path(tmp) / "questions.json").write_text(json.dumps(doc), encoding="utf-8")
                    with self.assertRaisesRegex(qe.InputError, "missing_required"):
                        qe.rollup([tmp], CAT)

    def test_evidence_only_unit_request_explains_missing_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalog = copy.deepcopy(CAT)
            next(q for q in catalog["questions"] if q["id"] == "H3")["data_requests"][0]["field_scope"] = "unit"
            doc = self.generate(tmp, catalog=catalog)
            request = finding(doc, "H3@EH-1")["data_requests"][0]
            self.assertEqual(request["candidate_scope"], "unit")
            self.assertEqual(request["candidate_facts"], [])
            self.assertIn("No owning equipment unit", request["scope_note"])
            self.assertIn("No owning equipment unit", (Path(tmp) / "screen.md").read_text(encoding="utf-8"))
            rolled = qe.rollup([tmp], catalog)
            self.assertIn("No owning equipment unit", qe.render_rollup_md(rolled, catalog))

    def test_invalid_show_fields_refuse_without_replacing_existing_reports(self):
        for show in (None, "HP", [], ["HP", "hp"], [""], [False]):
            with self.subTest(show=show), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                self.generate(tmp)
                before = {name: (base / name).read_bytes() for name in ("questions.json", "screen.md")}
                catalog = copy.deepcopy(CAT)
                next(q for q in catalog["questions"] if q["id"] == "E5")["data_requests"][0]["show_fields"] = show
                cp = base / "catalog.json"
                cp.write_text(json.dumps(catalog), encoding="utf-8")
                with contextlib.redirect_stderr(io.StringIO()) as err:
                    code = qe.main(["--model", str(base / "model.json"), "--catalog", str(cp), "--out", str(base)])
                self.assertEqual(code, 2)
                self.assertIn("show_fields", err.getvalue())
                self.assertEqual({name: (base / name).read_bytes() for name in before}, before)

    def test_malformed_candidate_metadata_refuses_before_rollup_publication(self):
        def duplicate(r):
            r["candidate_facts"].append(copy.deepcopy(r["candidate_facts"][0]))

        changes = [duplicate, lambda r: r.update(candidate_facts=17),
                   lambda r: r.pop("candidate_facts"), lambda r: r.update(candidate_scope="unit"),
                   lambda r: r["candidate_facts"][0].update(id="OUTSIDE"),
                   lambda r: r["candidate_facts"][0].update(label=""),
                   lambda r: r["candidate_facts"][0].update(name="UNLISTED"),
                   lambda r: r["candidate_facts"][0].update(value=None),
                   lambda r: r["candidate_facts"][0].update(where="")]
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            original = self.generate(tmp)
            out = base / "rollup"
            out.mkdir()
            for name in ("rollup.json", "rollup.md"):
                (out / name).write_text("previous report", encoding="utf-8")
            before = {p.name: p.read_bytes() for p in out.iterdir()}
            for change in changes:
                with self.subTest(change=change.__name__):
                    doc = copy.deepcopy(original)
                    change(finding(doc, "E5@F-1")["data_requests"][2])
                    (base / "questions.json").write_text(json.dumps(doc), encoding="utf-8")
                    with contextlib.redirect_stderr(io.StringIO()) as err:
                        code = qe.main(["--rollup", str(base), "--out", str(out)])
                    self.assertEqual(code, 2)
                    self.assertIn("candidate_facts", err.getvalue())
                    self.assertEqual({p.name: p.read_bytes() for p in out.iterdir()}, before)


class ReviewFixes(unittest.TestCase):
    """One regression test per finding of the two independent reviews (2026-10-29)."""

    def test_h4_never_fires_on_a_cooler_of_the_cooling_water_itself(self):
        self.assertNotIn("H4@S7-TK002", ids(load("open100")))  # ACW-AXC-210, AUX COOLING WATER COOLER (to air)
        with tempfile.TemporaryDirectory() as tmp:
            m = {"meta": {"title": "cw loop"}, "streams": [], "instruments": [], "final_elements": [],
                 "units": [{"id": "X-1", "name": "Cooling water cooler (air cooled)", "type": "heat_exchanger"},
                           {"id": "X-2", "name": "Cooling tower water exchanger", "type": "heat_exchanger"},
                           {"id": "X-3", "name": "Product cooler (cooling water)", "type": "heat_exchanger"}]}
            (Path(tmp) / "m.json").write_text(json.dumps(m), encoding="utf-8")
            _, doc = run(["--model", str(Path(tmp) / "m.json"), "--question", "H4"], tmp)
            self.assertEqual(ids(doc), {"H4@X-3"})
        # The unit decides, whichever item triggered it: a cooling-water line or valve on the air cooler is not
        # heat rejected to cooling water (second review round found this on a renamed Bayer E-3)
        with tempfile.TemporaryDirectory() as tmp:
            m = {"meta": {"title": "cw loop"}, "instruments": [],
                 "units": [{"id": "X-1", "name": "Aux cooling water air-cooled exchanger", "type": "heat_exchanger"}],
                 "streams": [{"id": "U1", "name": "Cooling water supply to the cooler", "from": "BL", "to": "X-1"}],
                 "final_elements": [{"tag": "HV-1", "unit": "X-1", "description": "cooling water hand valve"}]}
            (Path(tmp) / "m.json").write_text(json.dumps(m), encoding="utf-8")
            _, doc = run(["--model", str(Path(tmp) / "m.json"), "--question", "H4"], tmp)
            self.assertEqual(ids(doc), set())

    def test_a_null_fact_is_not_a_known_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = {"meta": {"title": "x"}, "streams": [], "instruments": [], "final_elements": [],
                 "units": [{"id": "E-3", "type": "heat_exchanger", "name": "Product cooler (cooling water)",
                            "facts": {"cooling_water_C": None}}]}
            (Path(tmp) / "m.json").write_text(json.dumps(m), encoding="utf-8")
            _, doc = run(["--model", str(Path(tmp) / "m.json"), "--question", "H4"], tmp)
        reqs = {r["item"] for r in finding(doc, "H4@E-3")["data_requests"]}
        self.assertIn("Cooling water supply temperature", reqs)

    def test_h4_process_temperature_is_never_the_cooling_water_side(self):
        h4 = finding(load("te"), "H4@E-101")
        req = next(r for r in h4["data_requests"] if r["item"].startswith("Temperature of the stream being cooled"))
        self.assertNotIn("XMEAS(22)", " ".join(req["where"]))  # TT-122 is the separator cooling water outlet

    def test_bayer_h4_requests_the_return_temperature(self):
        h4 = finding(load("bayer"), "H4@E-3")
        reqs = {r["item"]: r for r in h4["data_requests"]}
        self.assertNotIn("Cooling water supply temperature", reqs)  # the model holds it: 80 C on the supply
        self.assertEqual(reqs["Cooling water return temperature"]["state"], "not_on_drawing")
        self.assertTrue(any("cooling_water_C = 80" in e["text"] for e in h4["evidence"]))

    def test_flow_requests_never_cite_a_valve_position(self):
        pos = re.compile(r"_POS\b|XMV\(")
        for name in RUNS:
            for f in load(name)["questions"]:
                for r in f["data_requests"]:
                    if "flow" not in r["item"].lower() or "position" in r["item"].lower():
                        continue
                    for w in r["where"]:
                        offered = w.split("only the valve position is recorded")[0]
                        self.assertIsNone(pos.search(offered), (name, f["id"], r["item"], w))
        c1 = {r["item"]: r for r in finding(load("te"), "C1@R-101")["data_requests"]}["Utility flow to this user"]
        self.assertTrue(c1["where"][0].startswith("only the valve position is recorded (TV-121: recorded signal "
                                                  "XMV(10)"))
        self.assertIn("flow needs a meter or a calibrated valve curve", c1["where"][0])
        h1 = {r["item"]: r for r in finding(load("open100"), "H1@S0-OP005")["data_requests"]}
        self.assertTrue(h1["Steam flow through the station, with hours"]["where"][0].startswith(
            "only the valve position is recorded"))
        # a cooling water outlet temperature is not offered for the supply temperature
        h4 = {r["item"]: r for r in finding(load("te"), "H4@R-101")["data_requests"]}
        self.assertNotIn("TT-121", " ".join(h4["Cooling water supply temperature"]["where"]))
        self.assertIn("TT-121", " ".join(h4["Cooling water return temperature"]["where"]))

    def test_a_drawn_flow_meter_is_not_contradicted_by_the_valve_beside_it(self):
        """2026-10-29: a flow request said 'only a valve is drawn on this line, with no flow measurement' next to the
        flow meter on the same line (TE FT-119 with FV-119, the food dryer's FT-301 with TV-301)."""
        e18 = {r["item"]: r for r in finding(load("te"), "E18@model")["data_requests"]}
        where = " ".join(e18["Temperatures and duties of the cooled and the heated streams"]["where"])
        self.assertIn("FT-119", where)
        self.assertNotIn("XMV(9)", where)
        self.assertIn("XMV(10)", where)  # the unmetered cooling water side keeps its caveat
        e31 = {r["item"]: r for r in finding(load("food"), "E31@D-301")["data_requests"]}
        fuel = " ".join(e31["Existing heat-input, operating-period and comparison basis"]["where"])
        self.assertIn("FT-301", fuel)
        self.assertNotIn("only a valve", fuel)

    def test_every_source_named_in_a_wording_is_in_its_source_list(self):
        for q in CAT["questions"]:
            named = set(re.findall(r"\bS\d+\b", q["typical_benefit"]["wording"]))
            self.assertLessEqual(named, set(q["typical_benefit"]["source"]), q["id"])
        self.assertIn("S11", finding(load("te"), "H4@R-101")["typical_benefit"]["source"])

    def test_controller_evidence_quotes_as_found_and_formats_the_setpoint(self):
        c6 = finding(load("bayer"), "C6@TV-104C")
        tic = next(e for e in c6["evidence"] if e.get("id") == "TIC-104")["text"]
        self.assertIn("to the cooler (setpoint 135 C)", tic)
        self.assertIn("As found: incorrectly programmed", tic)
        self.assertIn("footnote 29", tic)

    def test_bad_inputs_are_refused_clearly(self):
        def refuse(files, extra=()):
            with tempfile.TemporaryDirectory() as tmp:
                for name, text in files.items():
                    (Path(tmp) / name).write_text(text, encoding="utf-8")
                err, old = io.StringIO(), sys.stderr
                sys.stderr = err
                try:
                    rc = qe.main(["--model", str(Path(tmp) / "m.json"), *[a.replace("TMP", tmp) for a in extra]])
                finally:
                    sys.stderr = old
                return rc, err.getvalue()
        good = json.dumps({"meta": {}, "units": [{"id": "T-1", "type": "tank"}]})
        for files, expect in (({"m.json": "{}"}, "has no units or instruments"),
                              ({"m.json": json.dumps({"units": []})}, "is this the right file?"),
                              ({"m.json": "not json at all"}, "is not valid JSON"),
                              ({"m.json": ""}, "is not valid JSON"),
                              ({"m.json": "[1, 2]"}, "not a JSON object"),
                              ({}, "cannot read the model")):
            rc, msg = refuse(files)
            self.assertEqual(rc, 2, msg)
            self.assertIn(expect, msg)
        rc, msg = refuse({"m.json": good, "l.csv": "loop,pv,mv\nFIC-1,FT-1,FV-1\n"}, ["--loops", "TMP/l.csv"])
        self.assertEqual(rc, 2)
        self.assertIn("has no column(s) controller, measurement, output", msg)
        rc, msg = refuse({"m.json": good, "l.csv": "controller,measurement,output\nXIC-1,XT-1,XV-1\n"},
                         ["--loops", "TMP/l.csv"])
        self.assertEqual((rc, "names a tag in the model" in msg), (2, True))  # a typo'd list isn't silently used
        bayer = json.loads((ROOT / "data" / "bayer_rt" / "process_model.json").read_text(encoding="utf-8"))
        for mutate, expect in (  # round-3 review: each of these was a traceback
                (lambda m: m["units"][0].update(id={}), "units[0].id must be text"),
                (lambda m: m["instruments"][0].update(unit=["x"]), "instruments[0].unit must be text"),
                (lambda m: m["units"][0].update(type=5), "units[0].type must be text"),
                (lambda m: m["units"][0].update(facts="x"), "units[0].facts must be an object"),
                (lambda m: m.update(controllers={}), "'controllers' must be a list"),
                (lambda m: m["units"].append(dict(m["units"][0])), "appears more than once"),
                # round 4 (Codex): a split range written as one tag string was split into characters
                (lambda m: m["controllers"][1]["output"].update(split_range="TV-104C"),
                 "output.split_range must be a list of tags")):
            bad = json.loads(json.dumps(bayer))
            mutate(bad)
            rc, msg = refuse({"m.json": json.dumps(bad)})
            self.assertEqual((rc, expect in msg), (2, True), msg)
        nullmeta = json.loads(json.dumps(bayer))
        nullmeta["meta"] = None  # round 4 (Codex): crashed while rendering; an empty meta is no meta
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "m.json").write_text(json.dumps(nullmeta), encoding="utf-8")
            rc, _ = run(["--model", str(Path(tmp) / "m.json")], tmp)
        self.assertEqual(rc, 0)
        rc, msg = refuse({"m.json": json.dumps({"units": [{}]})})
        self.assertEqual((rc, "has no 'id' field" in msg), (2, True))  # a nested record, not just the top level
        rc, msg = refuse({"m.json": good, "s.json": json.dumps({"sheets": {"2": [{}]}})}, ["--schedule", "TMP/s.json"])
        self.assertEqual(rc, 2, msg)
        rc, msg = refuse({"m.json": good}, ["--loops", "TMP/missing.csv"])
        self.assertEqual((rc, "cannot read the loop list" in msg), (2, True))
        rc, msg = refuse({"m.json": good, "s.json": "{}"}, ["--schedule", "TMP/s.json"])
        self.assertEqual((rc, "has no 'sheets' object" in msg), (2, True))

    def test_placeholder_tags_are_marked(self):
        c3 = finding(load("open100"), "C3@model")
        xxx = [e for e in c3["evidence"] if (e.get("tag") or "").endswith("-XXX")]
        self.assertEqual(len(xxx), 6)
        self.assertTrue(all("[placeholder tag on the drawing]" in e["text"] for e in xxx))
        self.assertFalse(any("placeholder" in e["text"] for e in c3["evidence"] if e.get("tag") == "LCV-1501"))

    def test_synthetic_demo_points_are_labelled(self):
        text = (EX / "open100" / "screen.md").read_text(encoding="utf-8")
        self.assertGreater(text.count("mapped data point"), 0)
        self.assertEqual(text.count("mapped data point"), text.count("SYNTHETIC mapped data point"))
        self.assertIn("synthetic demo point", text)


class ReviewRefresh(unittest.TestCase):
    """Fictional review controls, not a review of any plant's engineering facts."""

    def load_model(self, source, loops=None):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "model.json"
        path.write_text(json.dumps(source), encoding="utf-8")
        loop_path = None
        if loops:
            loop_path = path.with_suffix(".csv")
            loop_path.write_text(loops, encoding="utf-8")
        before = path.read_bytes()
        model = qe.Model(path, loop_path)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(model.m, source)
        return model

    def food(self):
        return json.loads((EX / "food_plant_model.json").read_text(encoding="utf-8"))

    def test_actual_cli_review_refresh_and_reconfirmation_packet(self):
        p = subprocess.run([sys.executable, "-S", str(EX / "review-refresh" / "demonstrate.py")], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_each_supported_hand_collection_excludes_rejected_record(self):
        records = {"units": {"id": "P-1", "type": "pump"},
                   "streams": {"id": "S1", "from": "P-1", "to": "BL", "name": "Cooling water", "utility": True},
                   "instruments": {"tag": "FT-1", "unit": "P-1"},
                   "final_elements": {"tag": "FV-1", "unit": "P-1"},
                   "manual_valves": {"tag": "HV-1", "unit": "P-1"},
                   "relief_devices": {"tag": "PSV-1", "unit": "P-1"},
                   "controllers": {"tag": "FIC-1", "measurement": "FT-1", "output": {"final_element": "FV-1"}},
                   "interlocks": {"id": "I-1", "measurement": "FT-1", "final_element": "FV-1"}}
        for section, record in records.items():
            with self.subTest(section=section):
                source = {sec: [copy.deepcopy(r)] for sec, r in records.items()}
                source[section][0]["ops_review"] = {"status": "rejected", "notes": "Fictional control"}
                model = self.load_model(source)
                key = record.get("id") or record.get("tag")
                normalized_key = "stream:" + key if section == "streams" else key
                self.assertNotIn(normalized_key, model.by_id)
                self.assertEqual([r["id"] for r in model.review_exclusions], [key])

    def test_missing_and_nonrejected_reviews_remain_eligible(self):
        base = self.food()
        expected = qe.screen(self.load_model(base), CAT)[0]
        for status in (None, "unverified", "confirmed", "corrected"):
            with self.subTest(status=status):
                source = copy.deepcopy(base)
                source["instruments"][1]["ops_review"] = None if status is None else {"status": status}
                model = self.load_model(source)
                self.assertIn("JT-201", model.by_id)
                self.assertEqual(qe.screen(model, CAT)[0], expected)

    def test_rejected_anchor_cannot_supply_evidence_or_data_locations(self):
        source = self.food()
        source["instruments"][0]["ops_review"] = {"status": "rejected"}
        found = qe.screen(self.load_model(source), CAT)[0]
        content = json.dumps(found)
        self.assertNotIn("PT-201", content)
        self.assertTrue(any(f["question_id"] == "C2" for f in found))

    def test_rejected_unit_does_not_reject_or_group_its_children(self):
        source = self.food()
        source["units"][0]["ops_review"] = {"status": "rejected"}
        model = self.load_model(source)
        self.assertNotIn("K-201", model.by_id)
        self.assertIn("PT-201", model.by_id)
        self.assertIsNone(model.by_id["PT-201"].get("unit"))
        self.assertIsNone(model.by_id["stream:R1"].get("dst"))
        self.assertNotIn('"id": "K-201"', json.dumps(qe.screen(model, CAT)[0]))

    def test_rejected_stream_no_longer_links_heat_recovery(self):
        source = self.food()
        next(s for s in source["streams"] if s["id"] == "S3")["ops_review"] = {"status": "rejected"}
        model = self.load_model(source)
        found = {f["id"] for f in qe.screen(model, CAT)[0]}
        self.assertTrue({"E31@F-303", "H6@F-303"} <= found)
        self.assertIn("HX-303", model.by_id)

    def twin(self):
        return {"meta": {"model_kind": "extracted_twin"},
                "units": [{"id": "P", "tag": "P-1", "name": "Pump", "class": "pump", "sheets": [0]}],
                "line_items": [{"id": "L", "class": "line", "unit": "P"}],
                "instruments": [{"id": "FT", "tag": "FT-1", "parent": "L", "unit": "P"}],
                "streams": [{"id": "s", "from": "P", "to": "L"}]}

    def test_twin_rejected_parent_is_not_a_path_but_child_survives(self):
        source = self.twin()
        source["line_items"][0]["ops_review"] = {"status": "rejected"}
        model = self.load_model(source)
        self.assertIn("FT", model.by_id)
        self.assertIsNone(model.by_id["FT"].get("parent"))
        self.assertNotIn("L", model.near("P", 5, "0"))
        self.assertNotIn("FT", model.near("P", 5, "0"))

    def test_twin_rejected_edge_is_not_a_path(self):
        source = self.twin()
        source["streams"][0]["ops_review"] = {"status": "rejected"}
        model = self.load_model(source)
        self.assertNotIn("L", model.near("P", 5, "0"))
        self.assertIn("FT", model.near("L", 5, "0"))

    def test_twin_rejected_instrument_and_connector_are_excluded(self):
        source = self.twin()
        source["instruments"][0]["ops_review"] = {"status": "rejected"}
        source["offpage_connectors"] = [{"id": "O", "text": "Steam", "ops_review": {"status": "rejected"}}]
        model = self.load_model(source)
        self.assertNotIn("FT", model.by_id)
        self.assertNotIn("O", model.by_id)

    def test_rejected_controller_does_not_satisfy_needs_model(self):
        source = self.food()
        for c in source["controllers"]:
            c["ops_review"] = {"status": "rejected"}
        model = self.load_model(source)
        found, nc, *_ = qe.screen(model, CAT, ["C2"])
        self.assertFalse(found)
        self.assertEqual([n["question_id"] for n in nc], ["C2"])

    def test_loop_list_cannot_reinstate_rejected_hand_controller(self):
        source = self.food()
        source["controllers"][0]["ops_review"] = {"status": "rejected"}
        model = self.load_model(source, "controller,measurement,output\nPIC-202,PT-202,SC-203\n")
        self.assertNotIn("PIC-202", model.by_id)
        self.assertEqual(model.loop_rejected, ["PIC-202"])
        c2 = next(f for f in qe.screen(model, CAT)[0] if f["id"] == "C2@model")
        self.assertIn("PT-202", {a["id"] for a in c2["assets"]})

    def test_loop_list_cannot_reinstate_rejected_twin_bubble(self):
        source = self.twin()
        source["instruments"].append({"id": "FIC", "tag": "FIC-1", "ops_review": {"status": "rejected"}})
        model = self.load_model(source, "controller,measurement,output\nFIC-1,FT-1,FV-1\n")
        self.assertNotIn("FIC-1", model.by_id)
        self.assertEqual(model.loop_rejected, ["FIC-1"])

    def test_loop_list_cannot_reclassify_other_rejected_assets_as_controllers(self):
        source = self.food()
        source["final_elements"][0]["ops_review"] = {"status": "rejected"}
        model = self.load_model(source, "controller,measurement,output\nsc_203,JT-201,TV-303\n")
        self.assertNotIn("sc_203", model.by_id)
        self.assertNotIn("SC-203", model.by_id)
        self.assertEqual(model.loop_rejected, ["sc_203"])
        c2 = next(f for f in qe.screen(model, CAT)[0] if f["id"] == "C2@model")
        self.assertIn("JT-201", {a["id"] for a in c2["assets"]})

    def test_live_duplicate_tag_is_not_blanket_rejected(self):
        source = self.twin()
        source["instruments"].extend([{"id": "bad", "tag": "FIC-1", "ops_review": {"status": "rejected"}},
                                       {"id": "live", "tag": "FIC-1"}])
        model = self.load_model(source, "controller,measurement,output\nFIC-1,FT-1,FV-1\n")
        self.assertIn("live", model.by_id)
        self.assertIn("FIC-1", model.by_id)
        self.assertEqual(model.loop_rejected, [])

    def test_ordinary_unresolved_references_are_retained(self):
        source = self.twin()
        source["instruments"][0].update(unit="unresolved-unit", parent="unresolved-parent")
        model = self.load_model(source)
        self.assertEqual(model.by_id["FT"]["unit"], "unresolved-unit")
        self.assertEqual(model.by_id["FT"]["parent"], "unresolved-parent")

    def test_malformed_reviews_refuse_before_output_changes(self):
        for review in ([], "rejected", {"status": "reject"}, {"status": []}, {"by": 2}, {"on": []}, {"notes": {}}):
            with self.subTest(review=review), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                path = base / "model.json"
                source = self.food()
                source["instruments"][0]["ops_review"] = review
                path.write_text(json.dumps(source), encoding="utf-8")
                (base / "questions.json").write_text("existing packet", encoding="utf-8")
                (base / "screen.md").write_text("existing report", encoding="utf-8")
                prior = {p.name: p.read_bytes() for p in base.iterdir()}
                err, old = io.StringIO(), sys.stderr
                sys.stderr = err
                try:
                    self.assertEqual(qe.main(["--model", str(path), "--out", str(base)]), 2)
                finally:
                    sys.stderr = old
                self.assertIn("ops_review", err.getvalue())
                self.assertEqual({p.name: p.read_bytes() for p in base.iterdir()}, prior)


class OutputPublication(unittest.TestCase):
    """Reports may refresh, but must never replace any of their inputs."""

    def call(self, args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as err:
            rc = qe.main([str(a) for a in args])
        return rc, err.getvalue()

    def snapshot(self, folder):
        return {p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob("*") if p.is_file()}

    def model(self, folder, name="model.json"):
        path = folder / name
        path.write_bytes((ROOT / "data/bayer_rt/process_model.json").read_bytes())
        return path

    def refuse_unchanged(self, folder, args):
        before = self.snapshot(folder)
        rc, err = self.call(args)
        self.assertEqual(rc, 2, err)
        self.assertTrue(err.startswith("error:"), err)
        self.assertEqual(self.snapshot(folder), before)

    def test_model_overlap_preserves_both_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model = self.model(base, "questions.json")
            (base / "screen.md").write_text("prior report", encoding="utf-8")
            self.refuse_unchanged(base, ["--model", model, "--out", base])

    def test_catalog_and_loop_inputs_are_protected(self):
        for role in ("catalog", "loops"):
            with self.subTest(role=role), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model = self.model(base)
                target = base / "screen.md"
                target.write_text(json.dumps(CAT) if role == "catalog" else "controller,measurement,output\n",
                                  encoding="utf-8")
                (base / "questions.json").write_text("prior JSON", encoding="utf-8")
                self.refuse_unchanged(base, ["--model", model, "--" + role, target, "--out", base])

    def test_every_schedule_is_protected_even_when_later_entries_replace_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model = base / "model.json"
            model.write_text(json.dumps({"meta": {"model_kind": "extracted_twin"},
                                         "units": [{"id": "P1", "tag": "P-1", "class": "pump", "sheets": ["0"]}],
                                         "instruments": [], "streams": []}), encoding="utf-8")
            first, second = base / "screen.md", base / "later.json"
            first.write_text(json.dumps({"sheets": {"0": [{"tag": "P-1", "service": "Water pump"}]}}),
                             encoding="utf-8")
            second.write_text(json.dumps({"sheets": {"0": [{"tag": "P-1", "service": "Water pump"}]}}),
                              encoding="utf-8")
            (base / "questions.json").write_text("prior JSON", encoding="utf-8")
            self.refuse_unchanged(base, ["--model", model, "--schedule", first, "--schedule", second,
                                         "--out", base])
            rc, err = self.call(["--model", model, "--schedule", first, "--schedule", second, "--out", base])
            self.assertEqual(rc, 2)
            self.assertIn("overlaps input", err)

    def test_rollup_direct_file_and_catalog_inputs_are_protected(self):
        for role in ("screen", "catalog"):
            with self.subTest(role=role), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                screen = base / ("rollup.json" if role == "screen" else "questions.json")
                screen.write_bytes((EX / "bayer/questions.json").read_bytes())
                args = ["--rollup", "site=" + str(screen if role == "screen" else base)]
                if role == "catalog":
                    catalog = base / "rollup.md"
                    catalog.write_text(json.dumps(CAT), encoding="utf-8")
                    (base / "rollup.json").write_text("prior JSON", encoding="utf-8")
                    args += ["--catalog", catalog]
                else:
                    (base / "rollup.md").write_text("prior report", encoding="utf-8")
                self.refuse_unchanged(base, [*args, "--out", base])

    def test_hardlink_alias_to_source_or_other_output_is_refused(self):
        for alias in ("source", "output"):
            with self.subTest(alias=alias), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model = self.model(base)
                first, second = base / "questions.json", base / "screen.md"
                if alias == "source":
                    os.link(model, first)
                    second.write_text("prior report", encoding="utf-8")
                else:
                    first.write_text("prior JSON", encoding="utf-8")
                    os.link(first, second)
                self.refuse_unchanged(base, ["--model", model, "--out", base])

    def test_symlink_source_alias_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model = self.model(base)
            try:
                (base / "questions.json").symlink_to(model)
            except OSError as exc:
                self.skipTest(f"file symlinks unavailable: {exc}")
            self.refuse_unchanged(base, ["--model", model, "--out", base])

    def test_invalid_second_target_or_parent_preserves_existing_report(self):
        for kind in ("second target directory", "parent file"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                model = self.model(base)
                (base / "questions.json").write_text("prior JSON", encoding="utf-8")
                if kind == "second target directory":
                    (base / "screen.md").mkdir()
                    out = base
                else:
                    out = base / "questions.json" / "reports"
                self.refuse_unchanged(base, ["--model", model, "--out", out])

    def test_explicit_io_list_is_protected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "io.csv"
            source.write_text("tag,server,base_path,point,description\nPT-1,SYNTHETIC-OPC,path,PT-1,synthetic fixture\n", encoding="utf-8")
            model = base / "model.json"
            model.write_text(json.dumps({"meta": {"model_kind": "extracted_twin"}, "units": [],
                "instruments": [{"id": "PT-1", "tag": "PT-1", "data_point":
                                 {"server": "SYNTHETIC-OPC", "base_path": "path", "point": "PT-1",
                                  "source": "io.csv row 2"}}]}), encoding="utf-8")
            os.link(source, base / "questions.json")
            self.refuse_unchanged(base, ["--model", model, "--io-list", source, "--out", base])

    def test_same_directory_generation_and_repeated_refresh_remain_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model = self.model(base)
            original = model.read_bytes()
            for args in (["--model", model], ["--rollup", "site=" + str(base)]):
                self.assertEqual(self.call([*args, "--out", base])[0], 0)
                before = self.snapshot(base)
                self.assertEqual(self.call([*args, "--out", base])[0], 0)
                self.assertEqual(self.snapshot(base), before)
            self.assertEqual(model.read_bytes(), original)

    def test_render_failure_leaves_existing_pairs_untouched(self):
        for renderer, args, names in (
                ("render_md", ["--model", ROOT / "data/bayer_rt/process_model.json"],
                 ("questions.json", "screen.md")),
                ("render_rollup_md", ["--rollup", EX / "bayer"], ("rollup.json", "rollup.md"))):
            with self.subTest(renderer=renderer), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                for name in names:
                    (base / name).write_text("prior report", encoding="utf-8")
                before = self.snapshot(base)
                with patch.object(qe, renderer, side_effect=ValueError("render control")):
                    with self.assertRaisesRegex(ValueError, "render control"):
                        self.call([*args, "--out", base])
                self.assertEqual(self.snapshot(base), before)


class CatalogHandoff(unittest.TestCase):
    """A source label must name the selected catalog; a shared ID must not hide a visible definition conflict."""

    def cli(self, args):
        result = subprocess.run([sys.executable, "-S", str(ROOT / "scripts/question_engine.py"),
                                 *map(str, args)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def refuse(self, base, doc, catalog=None, message="conflicts with catalog question E18"):
        source = base / "questions.json"
        source.write_text(json.dumps(doc), encoding="utf-8")
        out = base / "reports"
        out.mkdir()
        for name in ("rollup.json", "rollup.md"):
            (out / name).write_text("prior report", encoding="utf-8")
        before = OutputPublication.snapshot(self, base)
        args = ["--rollup", "fixture=" + str(base), "--out", str(out)]
        if catalog:
            args += ["--catalog", str(catalog)]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(qe.main(args), 2)
        self.assertIn(message, err.getvalue())
        self.assertEqual(OutputPublication.snapshot(self, base), before)

    def test_custom_catalog_is_identified_in_both_file_and_stdout_modes(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            catalog = copy.deepcopy(CAT)
            q = next(q for q in catalog["questions"] if q["id"] == "E18")
            q["question"] = "Fictional custom question: " + q["question"]
            path = base / "company-questions.json"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            site = base / "site"
            args = ["--model", ROOT / "data/bayer_rt/process_model.json", "--question", "E18",
                    "--catalog", path]
            self.cli([*args, "--out", site])
            doc = json.loads((site / "questions.json").read_text(encoding="utf-8"))
            self.assertEqual(doc["catalog"], path.name)
            self.assertEqual(doc["questions"][0]["question"], q["question"])
            for text in ((site / "screen.md").read_text(encoding="utf-8"), self.cli(args)):
                self.assertIn(f"Questions: `{path.name}`", text)
                self.assertIn(q["question"], text)
                self.assertNotIn(str(base), text)
            roll_args = ["--rollup", "fixture=" + str(site), "--catalog", path]
            self.cli([*roll_args, "--out", base / "combined"])
            rolled = json.loads((base / "combined/rollup.json").read_text(encoding="utf-8"))
            self.assertEqual(rolled["catalog"], path.name)
            self.assertEqual(rolled["questions"][0]["question"], q["question"])
            for text in ((base / "combined/rollup.md").read_text(encoding="utf-8"), self.cli(roll_args)):
                self.assertIn(f"Questions: `{path.name}`", text)
                self.assertNotIn(str(base), text)

    def test_rollup_refuses_visible_definition_conflicts_without_replacing_reports(self):
        changes = [("question", "Fictional other question"), ("family", "controls"),
                   ("decision_rule", "Fictional other rule"), ("limits", "Fictional other limit"),
                   ("typical_benefit.wording", "Fictional other wording"),
                   ("typical_benefit.source_titles", ["Fictional other title"]),
                   ("data_requests.how", "Fictional other collection instruction"),
                   ("data_requests.item", "Fictional other collection item")]
        for field, value in changes:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                doc = copy.deepcopy(load("bayer"))
                f = finding(doc, "E18@model")
                parts = field.split(".")
                if parts[0] == "data_requests":
                    f["data_requests"][0][parts[1]] = value
                elif len(parts) == 2:
                    f[parts[0]][parts[1]] = value
                else:
                    f[field] = value
                self.refuse(Path(tmp), doc)

    def test_malformed_findings_and_request_shapes_refuse_clearly(self):
        for bad in (None, {}, "requests", ["request"], [{"item": [], "how": "collect"}]):
            with self.subTest(requests=bad), tempfile.TemporaryDirectory() as tmp:
                doc = copy.deepcopy(load("bayer"))
                finding(doc, "E18@model")["data_requests"] = bad
                self.refuse(Path(tmp), doc)
        for bad in (None, "finding", {"question_id": []}):
            with self.subTest(finding=bad), tempfile.TemporaryDirectory() as tmp:
                doc = copy.deepcopy(load("bayer"))
                doc["questions"] = [bad]
                self.refuse(Path(tmp), doc, message="without a string question_id")

    def test_compatible_catalog_copy_does_not_require_the_same_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / "reviewed-copy.json"
            path.write_text(json.dumps(CAT), encoding="utf-8")
            self.cli(["--rollup", "fixture=" + str(EX / "bayer"), "--catalog", path, "--out", base / "reports"])
            doc = json.loads((base / "reports/rollup.json").read_text(encoding="utf-8"))
            self.assertEqual(doc["catalog"], path.name)
            self.assertEqual(doc["counts"]["findings"], len(load("bayer")["questions"]))

    def test_ambiguous_catalog_request_instructions_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            catalog = copy.deepcopy(CAT)
            q = next(q for q in catalog["questions"] if q["id"] == "E18")
            q["data_requests"].append(dict(q["data_requests"][0], how="Fictional conflicting instruction"))
            path = base / "catalog.json"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            self.refuse(base, load("bayer"), catalog=path, message="conflicting instructions for the same request item")


class ReadableFindingReferences(unittest.TestCase):
    """Readable references are copyable exact identities, not new findings or company asset aliases."""

    @staticmethod
    def render_saved(relative):
        doc = json.loads((ROOT / relative / "questions.json").read_text(encoding="utf-8"))
        model = qe.Model(ROOT / doc["source_model"])
        before = json.dumps(doc, ensure_ascii=False)
        text = qe.render_md(model, CAT, doc)
        if json.dumps(doc, ensure_ascii=False) != before:
            raise AssertionError("render changed finding, evidence, request, or key/list order")
        return text, doc

    def test_bayer_model_reference_and_exact_stream_assets(self):
        text, doc = self.render_saved("examples/context-register/bayer/screen")
        self.assertIn('**Finding reference (JSON string):** `"E18@model"`', text)
        self.assertIn('**Asset IDs (JSON array):** `["stream:U2", "HV-112", "stream:U1", "FT-106", "TV-104C", "HV-108"]`', text)
        self.assertEqual(doc["questions"][0]["id"], "E18@model")

    def test_te_repeated_rules_have_distinct_literal_references(self):
        text, _ = self.render_saved("examples/opportunity-screen/te")
        expected = (
            ('"H4@R-101"', '["R-101", "TT-121", "TV-121", "TT-109"]'),
            ('"H4@E-101"', '["E-101", "TT-122", "FV-117"]'),
            ('"C1@R-101"', '["R-101", "TV-121", "TT-121"]'),
            ('"C1@E-101"', '["E-101", "FV-117", "TT-122"]'),
        )
        for reference, assets in expected:
            with self.subTest(reference=reference):
                block = '**Finding reference (JSON string):** `' + reference + '`\n**Asset IDs (JSON array):** `' + assets + '`'
                self.assertEqual(text.count(block), 1)

    def test_ascii_json_and_backtick_safe_literal_display(self):
        # Independent literal expectations: JSON escapes encode exact data; backtick runs cannot close the span.
        vectors = (
            ("plain", '`"plain"`'),
            ("  A  ", '`"  A  "`'),
            ("a\nb\tc\r", r'`"a\nb\tc\r"`'),
            ("雪\u00a0Ω", r'`"\u96ea\u00a0\u03a9"`'),
            ("`", '``"`"``'),
            ("a``b", '```"a``b"```'),
            ('P|[a]<b>&"\\', r'`"P|[a]<b>&\"\\"`'),
            ([], '`[]`'),
            (["stream:S1", "雪", "`"], '``["stream:S1", "\\u96ea", "`"]``'),
        )
        for value, expected in vectors:
            with self.subTest(value=value):
                actual = qe._markdown_json(value)
                self.assertEqual(actual, expected)
                self.assertTrue(actual.isascii())
                fence = re.match(r"`+", actual).group()
                self.assertTrue(actual.endswith(fence))
                self.assertEqual(json.loads(actual[len(fence):-len(fence)]), value)

    def test_render_keeps_exact_encoded_identity_and_empty_assets(self):
        doc = load("te")
        doc["questions"] = [copy.deepcopy(doc["questions"][0])]
        q = doc["questions"][0]
        q["id"] = "  雪`\n  "
        q["assets"] = []
        before = copy.deepcopy(doc)
        model = qe.Model(ROOT / "data/te_process_model.json")
        text = qe.render_md(model, CAT, doc)
        self.assertIn('**Finding reference (JSON string):** ``"  \\u96ea`\\n  "``', text)
        self.assertIn('**Asset IDs (JSON array):** `[]`', text)
        self.assertEqual(doc, before)
        q["assets"] = [{"id": "  stream:S1  "}, {"id": "Ω|[x]"}, {"id": "a``b"}]
        text = qe.render_md(model, CAT, doc)
        self.assertIn('**Asset IDs (JSON array):** ```["  stream:S1  ", "\\u03a9|[x]", "a``b"]```', text)

    def test_complete_published_markdown_matches_rendered_references(self):
        # Parse actual references independently, then require the entire currently published screen.
        def decode(line, label):
            self.assertTrue(line.startswith(label))
            code = line[len(label):].removesuffix("\n")
            match = re.match(r"`+", code)
            self.assertIsNotNone(match)
            fence = match.group()
            self.assertTrue(code.endswith(fence))
            payload = code[len(fence):-len(fence)]
            self.assertNotIn(fence, payload)
            return json.loads(payload)

        for relative in ("examples/context-register/bayer/screen", "examples/opportunity-screen/te",
                         "examples/opportunity-screen/millard/screen"):
            with self.subTest(relative=relative):
                text, doc = self.render_saved(relative)
                lines = text.splitlines(keepends=True)
                i, count = 0, 0
                while i < len(lines):
                    if lines[i].startswith("**Finding reference (JSON string):** "):
                        self.assertLess(count, len(doc["questions"]))
                        q = doc["questions"][count]
                        self.assertEqual(decode(lines[i], "**Finding reference (JSON string):** "), q["id"])
                        self.assertEqual(decode(lines[i + 1], "**Asset IDs (JSON array):** "),
                                         [a["id"] for a in q["assets"]])
                        self.assertEqual(lines[i + 2], "\n")
                        count += 1
                        i += 3
                    else:
                        i += 1
                self.assertEqual(count, len(doc["questions"]))
                self.assertEqual(text, (ROOT / relative / "screen.md").read_text(encoding="utf-8"))

    def test_zero_finding_screen_remains_exact(self):
        class EmptyModel:
            twin = False
            m = {"meta": {"title": "Empty screen"}}
        doc = {"source_model": "empty.json", "catalog": "questions.json", "loops": None, "schedules": [],
               "counts": {"by_family": {}}, "questions": [], "not_checked": [], "did_not_fire": [], "left_out": {}}
        expected = "\n".join(["# Opportunity screen: Empty screen", "",
                              "Model: `empty.json`. Questions: `questions.json`.", "", qe.HOW_TO_READ, "",
                              "| Family | Findings |", "|---|---|", "| Energy | 0 |", ""])
        self.assertEqual(qe.render_md(EmptyModel(), {"families": {"energy": "Energy"}, "sources": {}}, doc), expected)

    def test_actual_cli_json_bytes_remain_exact(self):
        """Complete JSON text/order stays exact under the existing CRLF-to-LF text policy, not raw-byte identity."""
        cases = (
            (["--model", "data/bayer_rt/process_model.json", "--question", "E18"], "examples/context-register/bayer/screen"),
            (RUNS["te"], "examples/opportunity-screen/te"),
        )
        for args, relative in cases:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
                result = subprocess.run([sys.executable, "-B", "-S", str(ROOT / "scripts/question_engine.py"),
                                         *args, "--out", tmp], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((Path(tmp) / "questions.json").read_text(encoding="utf-8"),
                                 (ROOT / relative / "questions.json").read_text(encoding="utf-8"))
                self.assertIn("**Finding reference (JSON string):**", (Path(tmp) / "screen.md").read_text(encoding="utf-8"))


class FunctionBasisCollection(unittest.TestCase):
    """Synthetic source-development cases and candidate-only field behavior; no plant/usefulness claim."""
    BASE = EX / "function-basis"
    ROLE = "supplied candidate field"
    TEST_ID = "TEST-FUNCTION-BASIS"

    @staticmethod
    def _question(kinds, fields=None):
        question = {
            "id": FunctionBasisCollection.TEST_ID, "family": "energy",
            "question": "Which supplied qualifiers belong to this record?",
            "applies_when": {"anchor": {"kind": list(kinds)}, "group_by": "item"},
            "evidence_fields": ["supplied record only"],
            "data_requests": [{"item": "Review source and current function",
                               "where": [{"place": "records", "what": "approved existing configuration"}],
                               "how": "Supplied candidates do not settle the review."}],
            "decision_rule": "Return a qualified source investigation for review.",
            "typical_benefit": {"wording": "No source or quantified benefit for this fictional software control.",
                                "source": [], "arc": None},
            "limits": "Representation test only, not an engineering recommendation.",
        }
        if fields is not None:
            question["evidence_show_fields"] = fields
        return question

    @staticmethod
    def _model():
        return {"meta": {"model_id": "illustrative-function-basis-test", "illustrative": True},
                "units": [{"id": "K-A", "name": "Ammonia screw compressor A", "type": "compressor"}],
                "streams": [], "instruments": [], "controllers": [], "interlocks": [],
                "final_elements": [], "manual_valves": []}

    def _invoke(self, model, question=None, *, question_id=None, sentinel=False):
        catalog = copy.deepcopy(CAT)
        if question is not None:
            self.assertNotIn(question["id"], {q["id"] for q in catalog["questions"]})
            catalog["questions"].append(question)
            question_id = question["id"]
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source, catalog_path, out = base / "model.json", base / "catalog.json", base / "outputs"
            source.write_text(json.dumps(model, ensure_ascii=True), encoding="utf-8")
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=True), encoding="utf-8")
            sources_before = (source.read_bytes(), catalog_path.read_bytes())
            if sentinel:
                out.mkdir()
                (out / "questions.json").write_bytes(b"QUESTIONS SENTINEL\x00\xff")
                (out / "screen.md").write_bytes(b"SCREEN SENTINEL\x00\xff")
            before = (out.exists(), {p.name: p.read_bytes() for p in out.iterdir()} if out.exists() else {})
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = qe.main(["--model", str(source), "--catalog", str(catalog_path),
                                "--question", question_id, "--out", str(out)])
            after = (out.exists(), {p.name: p.read_bytes() for p in out.iterdir()} if out.exists() else {})
            self.assertEqual((source.read_bytes(), catalog_path.read_bytes()), sources_before)
            doc = json.loads(after[1]["questions.json"].decode("utf-8")) if code == 0 else None
            markdown = after[1]["screen.md"].decode("utf-8") if code == 0 else None
            return code, stdout.getvalue(), stderr.getvalue(), before, after, doc, markdown

    def _assert_field(self, questions, expected):
        rows = [e for q in questions for e in q["evidence"]
                if e["role"] == self.ROLE and e.get("id") == expected["id"] and e["field"] == expected["field"]]
        self.assertEqual(len(rows), 1, expected)
        row = rows[0]
        prefix = f"{expected.get('label', expected['id'])} {expected['name']} = "
        suffix = f"; {expected['state']}; meaning and suitability unverified"
        self.assertTrue(row["text"].startswith(prefix), row)
        self.assertTrue(row["text"].endswith(suffix), row)
        value = json.loads(row["text"][len(prefix):-len(suffix)])
        # JSON comparison preserves false/zero and nested types as well as array/key order.
        self.assertEqual(json.dumps(value, ensure_ascii=True),
                         json.dumps(expected["value"], ensure_ascii=True))

    def _decode_span(self, text):
        count = len(text) - len(text.lstrip("`"))
        self.assertGreater(count, 0)
        end = text.find("`" * count, count)
        self.assertGreaterEqual(end, count)
        payload = text[count:end]
        self.assertTrue(payload.isascii())
        return json.loads(payload), text[end + count:]

    def _assert_literal_markdown(self, doc, markdown):
        rows = [e for q in doc["questions"] for e in q["evidence"] if e["role"] == self.ROLE]
        prefix = "- Supplied candidate field: "
        lines = [line[len(prefix):] for line in markdown.splitlines() if line.startswith(prefix)]
        self.assertEqual(len(lines), len(rows))
        for row, line in zip(rows, lines):
            text, rest = self._decode_span(line)
            self.assertTrue(rest.startswith(" ("))
            field, rest = self._decode_span(rest[2:])
            self.assertEqual(rest, ")")
            self.assertEqual((text, field), (row["text"], row["field"]))

    def test_source_development_corpus_preserves_subjects_candidates_and_open_requests(self):
        oracle_path = self.BASE / "expected" / "cases.json"
        self.assertTrue(oracle_path.is_file(), "install the committed function-basis corpus with this method")
        oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
        self.assertEqual(oracle["schema"], "function-basis-cases-1")
        self.assertEqual(oracle["evidence_class"], "synthetic-development")
        self.assertGreaterEqual(len(oracle["cases"]), 25)  # Later preregistered cases may be appended.
        self.assertEqual(len({c["id"] for c in oracle["cases"]}), len(oracle["cases"]))
        for case in oracle["cases"]:
            with self.subTest(case=case["id"]):
                path = (self.BASE / case["model"]).resolve()
                self.assertTrue(path.is_relative_to(self.BASE.resolve()))
                self.assertTrue(path.is_file())
                questions, _, _, _ = qe.screen(qe.Model(path), CAT, [case["question_id"]])
                self.assertEqual([q["about"] for q in questions], case["expected_subjects"])
                self.assertTrue(all(q["question_id"] == case["question_id"] for q in questions))
                assets = {a["id"] for q in questions for a in q["assets"]}
                self.assertLessEqual(set(case["required_candidate_ids"]), assets)
                self.assertFalse(set(case["forbidden_candidate_ids"]) & assets)
                for question in questions:
                    self.assertEqual(len(question["data_requests"]), case.get("expected_request_count", 3))
                    self.assertTrue(all(r["state"] == "not_on_drawing" and r["where"]
                                        for r in question["data_requests"]))
                for field in case["candidate_fields"]:
                    self._assert_field(questions, field)

    def test_heating_development_corpus_preserves_scope_literals_and_records_first_requests(self):
        oracle = json.loads((self.BASE / "expected/heating-cases.json").read_text(encoding="utf-8"))
        supplement = json.loads((self.BASE / "expected/heating-literal-supplement.json").read_text(encoding="utf-8"))
        self.assertEqual(oracle["schema"], "function-basis-heating-cases-1")
        self.assertEqual(supplement["schema"], "function-basis-heating-literal-supplement-1")
        self.assertEqual(oracle["evidence_class"], "synthetic-development")
        self.assertEqual(supplement["evidence_class"], "synthetic-development")
        self.assertEqual(len(oracle["cases"]), oracle["case_count"])
        self.assertEqual(len({c["id"] for c in oracle["cases"]}), len(oracle["cases"]))
        self.assertEqual(sum(len(c.get("candidate_fields", [])) for c in oracle["cases"])
                         + len(supplement["literals"]), supplement["count_profile"]["combined_inputs"])
        case_ids = {c["id"] for c in oracle["cases"]}
        self.assertTrue(all(v["case"] in case_ids for v in supplement["literals"]))
        checked_supplement = set()
        # These four quiet controls preserve the accepted bounded trigger scope. The source does not
        # mandate silence whenever a record is absent, and optional working coverage can be shown or quiet.
        quiet_controls = {"H6-05-no-external-duty-lead", "E31-06-no-process-anchor",
                          "H6-06-no-process-anchor", "E32-06-nonfuel-and-unrelated-burner"}
        for case in oracle["cases"]:
            with self.subTest(case=case["id"]):
                path = (self.BASE / case["model"]).resolve()
                self.assertTrue(path.is_relative_to(self.BASE.resolve()))
                model = json.loads(path.read_text(encoding="utf-8"))
                result = self._invoke(model, question_id=case["question_id"])
                self.assertEqual(result[0], 0, result[2])
                doc, markdown = result[5], result[6]
                questions = doc["questions"]
                self._assert_literal_markdown(doc, markdown)
                self.assertTrue(all(q["question_id"] == case["question_id"] for q in questions))
                subjects = {q["about"] for q in questions}
                self.assertEqual(len(subjects), len(questions))
                if case["subject_policy"] == "exact":
                    self.assertEqual([q["about"] for q in questions], case["expected_subjects"])
                    self.assertEqual([q["id"] for q in questions], case["expected_finding_ids"])
                else:
                    self.assertEqual(case["subject_policy"], "minimum_plus_quiet_permitted")
                    required = set(case["required_subjects"])
                    self.assertLessEqual(required, subjects)
                    self.assertLessEqual(subjects, required | set(case["quiet_permitted_subjects"]))
                    self.assertFalse(subjects & set(case["forbidden_subjects"]))
                if case["id"] in quiet_controls:
                    self.assertEqual(questions, [])
                extra_literals = [(n, v) for n, v in enumerate(supplement["literals"]) if v["case"] == case["id"]]
                for question in questions:
                    subject = question["about"]
                    assets = {a["id"] for a in question["assets"]}
                    required_candidates = case.get("candidate_ids_by_subject_if_shown",
                                                   case.get("required_candidate_ids_by_subject", {}))
                    self.assertLessEqual(set(required_candidates.get(subject, [])), assets)
                    self.assertFalse(assets & set(case.get("forbidden_candidate_ids_by_subject", {}).get(subject, [])))
                    self.assertFalse(assets & set(case.get("forbidden_offsubject_candidate_ids", [])))
                    for entry in question["evidence"]:
                        if entry.get("id") in case.get("forbidden_combustion_basis_candidate_ids", []):
                            self.assertTrue(entry["role"].startswith("unclassified"), entry)
                    if case["id"] == "E32-02-product-and-foreign-oxygen":
                        # O2-P may be unclassified negative context; foreign O2-X cannot qualify this source.
                        self.assertNotIn("O2-X", assets)
                        self.assertFalse(any(e.get("id") == "O2-X" for e in question["evidence"]))
                    for field in case.get("candidate_fields", []):
                        if field["id"] in assets:
                            self._assert_field([question], field)
                    for index, field in extra_literals:
                        if subject in field["predicted_shown_subjects"]:
                            self.assertIn(field["id"], assets)
                            self._assert_field([question], field)
                            checked_supplement.add(index)
                    self.assertTrue(question["data_requests"])
                    for request in question["data_requests"]:
                        self.assertEqual(request["state"], "not_on_drawing")
                        self.assertTrue(request["how"].strip())
                        self.assertTrue(request["where"])
                        self.assertTrue(request["where"][0].startswith("site records:"), request)
                    plan = " ".join(r["how"] + " " + " ".join(r["where"]) for r in question["data_requests"])
                    self.assertIn("existing", plan.lower())
                    if subject in case.get("quiet_permitted_subjects", []):
                        # Retain supplied working coverage without calling it a required new project.
                        self.assertIn("recovery", plan.lower())
                        self.assertNotRegex(plan.lower(), r"\b(?:must install|retrofit is required|new recovery is required)\b")
        self.assertEqual(checked_supplement, set(range(len(supplement["literals"]))))


    def test_native_controller_and_interlock_qualifiers_do_not_become_screening_truth(self):
        for kind in ("controller", "interlock"):
            with self.subTest(kind=kind):
                model = self._model()
                model["units"][0]["name"] = "Utility skid"
                facts = {"normal_temperature_C": 100, "enabled": False, "observed_hours": 0, "mode": "unknown"}
                if kind == "controller":
                    identity, section = "TIC-X", "controllers"
                    model[section] = [{"tag": identity, "unit": "K-A", "description": "Electric heater temperature control",
                                       "measurement": None, "output": {}, "facts": facts}]
                else:
                    identity, section = "IL-X", "interlocks"
                    model[section] = [{"id": identity, "unit": "K-A", "cause": "Electric heater temperature high",
                                       "effect": "Trip request", "facts": facts}]
                result = self._invoke(model, question_id="H3")
                self.assertEqual(result[0], 0, result[2])
                self.assertEqual(result[5]["questions"], [])
                result = self._invoke(model, self._question([kind], ["enabled", "observed_hours", "mode"]))
                self.assertEqual(result[0], 0, result[2])
                for name, state, value in (("enabled", "present", False), ("observed_hours", "present", 0),
                                           ("mode", "blank", "unknown")):
                    self._assert_field(result[5]["questions"], {"id": identity, "name": name, "state": state,
                        "value": value, "field": f"{section}[{identity}].facts.{name}"})

    def test_candidate_literal_values_and_markdown_are_exact_and_inert(self):
        model = self._model()
        values = {"Enabled": False, "observed_hours": 0, "null_value": None, "empty_value": "",
                  "whitespace_value": " \t", "unknown_value": "unknown", "array_value": [], "object_value": {},
                  "nested_value": {"flag": False, "count": 0, "note": None},
                  "as_operated": 'manual `A` **B** [link](https://example.invalid) <b>x</b>\nline2 μ',
                  "event_history": '["this remains a string"]'}
        model["final_elements"] = [{"tag": "SC-A", "unit": "K-A", "description": "Drive candidate", "facts": values}]
        names = ["enabled" if n == "Enabled" else n for n in values]
        result = self._invoke(model, self._question(["final_element"], names))
        self.assertEqual(result[0], 0, result[2])
        for name, value in values.items():
            state = "blank" if name in {"null_value", "empty_value", "whitespace_value", "unknown_value"} else "present"
            self._assert_field(result[5]["questions"], {"id": "SC-A", "name": "enabled" if name == "Enabled" else name,
                "state": state, "value": value, "field": "final_elements[SC-A].facts." + name})
        self._assert_literal_markdown(result[5], result[6])
        self.assertTrue(all(q["data_requests"] for q in result[5]["questions"]))

    def test_unrelated_rejected_and_unshown_records_cannot_lend_qualifiers(self):
        model = self._model()
        model["units"][0]["facts"] = {"enabled": True, "observed_hours": 999}
        model["units"].append({"id": "P-X", "name": "Wash pump X", "type": "pump"})
        model["final_elements"] = [
            {"tag": "SC-A", "unit": "K-A", "description": "VFD candidate A", "facts": {"Enabled": False, "observed_hours": 0}},
            {"tag": "SC-X", "unit": "P-X", "description": "VFD unrelated X", "facts": {"enabled": True, "observed_hours": 888}},
            {"tag": "SC-R", "unit": "K-A", "description": "VFD rejected R", "facts": {"enabled": True, "observed_hours": 777},
             "ops_review": {"status": "rejected"}},
        ]
        model["instruments"] = [{"tag": "TT-N", "unit": "K-A", "variable": "temperature", "description": "Ordinary temperature",
                                 "facts": {"enabled": True, "observed_hours": 666}}]
        result = self._invoke(model, question_id="E29")
        self.assertEqual(result[0], 0, result[2])
        question = result[5]["questions"][0]
        self.assertEqual({a["id"] for a in question["assets"]}, {"K-A", "SC-A"})
        for identity, name, value, original in (("K-A", "observed_hours", 999, "observed_hours"),
                                               ("SC-A", "observed_hours", 0, "observed_hours"),
                                               ("SC-A", "enabled", False, "Enabled")):
            section = "units" if identity == "K-A" else "final_elements"
            self._assert_field([question], {"id": identity, "name": name, "state": "present", "value": value,
                                           "field": f"{section}[{identity}].facts.{original}"})

    def test_invalid_allowlists_refuse_before_outputs_or_sentinel_replacement(self):
        invalid = (None, [], "enabled", [None], [1], [""], [" "], [" enabled"], ["enabled "],
                   ["enabled", "Enabled"], ["ß", "SS"])
        for names in invalid:
            for sentinel in (False, True):
                with self.subTest(names=names, sentinel=sentinel):
                    question = self._question(["equipment"])
                    question["evidence_show_fields"] = names
                    result = self._invoke(self._model(), question, sentinel=sentinel)
                    self.assertEqual(result[0], 2)
                    self.assertEqual(result[1], "")
                    self.assertIn("evidence_show_fields", result[2])
                    self.assertEqual(result[3], result[4])

    def test_role_marker_is_reserved_only_for_questions_that_opt_in(self):
        model = self._model()
        model["controllers"] = [{"tag": "SC-A", "unit": "K-A", "description": "Speed controller candidate",
                                  "measurement": None, "output": {}, "facts": {"enabled": False}}]
        for location in ("anchor_role", "with", "also_show"):
            with self.subTest(location=location):
                question = self._question(["controller"])
                if location == "anchor_role":
                    question["applies_when"][location] = self.ROLE
                else:
                    question["applies_when"][location] = [{"select": {"kind": ["equipment"]},
                        "relation": "same_unit", "as": self.ROLE}]
                result = self._invoke(model, question)
                self.assertEqual(result[0], 0, result[2])
                self.assertIn("- Supplied candidate field: ", result[6])
                self.assertNotIn("- Supplied candidate field: `", result[6])
                question["evidence_show_fields"] = ["enabled"]
                result = self._invoke(model, question, sentinel=True)
                self.assertEqual(result[0], 2)
                self.assertEqual(result[1], "")
                self.assertIn("reserves the 'supplied candidate field' role", result[2])
                self.assertEqual(result[3], result[4])

    def test_escaped_surrogate_values_complete_utf8_and_preserve_literal_meaning(self):
        values = ("\ud800", "\udfff", "μ-\ud800-🚀", {"μ": "\ud800", "valid": [False, 0, None, "🚀"]})
        for value in values:
            for sentinel in (False, True):
                with self.subTest(value=repr(value), sentinel=sentinel):
                    model = self._model()
                    model["units"][0]["facts"] = {"source_revision": value}
                    result = self._invoke(model, self._question(["equipment"], ["source_revision"]), sentinel=sentinel)
                    self.assertEqual(result[0], 0, result[2])
                    self.assertEqual(set(result[4][1]), {"questions.json", "screen.md"})
                    self._assert_field(result[5]["questions"], {"id": "K-A", "name": "source_revision", "state": "present",
                                                             "value": value, "field": "units[K-A].facts.source_revision"})
                    self._assert_literal_markdown(result[5], result[6])

    def test_non_utf8_allowlist_names_refuse_without_touching_targets(self):
        for name in ("field_\ud800", "field_\udfff"):
            for sentinel in (False, True):
                with self.subTest(name=repr(name), sentinel=sentinel):
                    model = self._model()
                    model["units"][0]["facts"] = {name: False}
                    result = self._invoke(model, self._question(["equipment"], [name]), sentinel=sentinel)
                    self.assertEqual(result[0], 2)
                    self.assertEqual(result[1], "")
                    self.assertEqual(result[2], "error: catalog evidence_show_fields names must be valid UTF-8 text\n")
                    self.assertEqual(result[3], result[4])

    def test_candidate_only_controller_field_does_not_complete_required_field_scope(self):
        model = self._model()
        model["controllers"] = [{"tag": "SC-A", "unit": "K-A", "description": "Speed controller candidate",
                                  "measurement": None, "output": {}, "facts": {"enabled": False}}]
        question = self._question(["controller"], ["enabled"])
        question["data_requests"][0]["fields"] = ["enabled"]
        result = self._invoke(model, question)
        self.assertEqual(result[0], 0, result[2])
        self._assert_field(result[5]["questions"], {"id": "SC-A", "name": "enabled", "state": "present", "value": False,
                                                  "field": "controllers[SC-A].facts.enabled"})
        request = result[5]["questions"][0]["data_requests"][0]
        self.assertEqual(request["still_needed"], ["enabled"])
        self.assertEqual(request["field_coverage"][0]["fields"][0]["state"], "absent")


class ExplicitHeatingRoles(unittest.TestCase):
    """Post-food-failure controls, separate from the43 core source-collection models."""
    def _controls(self):
        folder = EX / "function-basis" / "role-controls"
        return folder, json.loads((folder / "cases.json").read_text(encoding="utf-8"))

    def test_portable_role_controls_have_explicit_development_scope(self):
        folder, controls = self._controls()
        self.assertEqual(controls["schema"], "heating-role-controls-1")
        self.assertEqual(controls["exposure"], "post-food-failure development; not blind, heldout, plant or source-family evidence")
        self.assertEqual(len({v["id"] for v in controls["matcher_vectors"]}), len(controls["matcher_vectors"]))
        self.assertTrue(controls["regex"].endswith(r"\Z"))
        for case in controls["fixture_expectations"]:
            self.assertTrue((folder / case["model"]).is_file())
        for question in CAT["questions"]:
            if question["id"] in ("E31", "E32", "H6"):
                self.assertEqual(question["applies_when"]["anchor"]["not_type_text"], controls["regex"])
        self.assertIn("not_type_text", CAT["fields_help"]["selector"])

    def test_explicit_type_filter_vectors_keep_legacy_and_name_fallback(self):
        _, controls = self._controls()
        anchor = copy.deepcopy(next(q for q in CAT["questions"] if q["id"] == "E31")["applies_when"]["anchor"])
        legacy = dict(anchor)
        legacy.pop("not_type_text")
        for case in controls["matcher_vectors"]:
            with self.subTest(case=case["id"]):
                item = {"id": "test-role", "kind": "equipment", "text": case["text"], "facts": {}}
                if not case.get("type_key_absent"):
                    item["type"] = case["explicit_type"]
                self.assertIs(qe.matches(item, legacy), case["without_new_key"])
                self.assertIs(qe.matches(item, anchor), case["with_new_key"])
                empty_optin = dict(legacy, not_type_text="")
                self.assertIs(qe.matches(item, empty_optin), case["without_new_key"])

    def test_native_role_controls_keep_process_and_scoped_recovery_context(self):
        folder, controls = self._controls()
        for case in controls["fixture_expectations"]:
            with self.subTest(model=case["model"]):
                found, not_checked, _, _ = qe.screen(qe.Model(folder / case["model"]), CAT, ["E31", "E32", "H6"])
                self.assertEqual(not_checked, [])
                self.assertEqual({f["id"] for f in found}, set(case["required_ids"]))
                for f in found:
                    self.assertNotIn(f["id"].split("@", 1)[1], case.get("forbidden_subjects", []))
                    candidates = {a["id"] for a in f["assets"]}
                    self.assertNotIn(case.get("forbidden_D_A_candidate"), candidates)
                    if case.get("represented_recovery_candidate_for_D_A") and f["question_id"] in ("E31", "H6"):
                        self.assertIn(case["represented_recovery_candidate_for_D_A"], candidates)

    def test_food_typed_recoverer_is_context_not_another_process_subject(self):
        _, controls = self._controls()
        found, not_checked, _, _ = qe.screen(qe.Model(EX / "food_plant_model.json"), CAT)
        self.assertEqual(not_checked, [])
        expected = controls["actual_food_expected"]
        self.assertEqual(len(found), expected["findings"])
        self.assertFalse({f["id"] for f in found} & set(expected["forbidden_ids"]))
        for fid in ("E31@F-303", "H6@F-303"):
            self.assertIn("HX-303", {a["id"] for f in found if f["id"] == fid for a in f["assets"]})




class CombustionControlBasis(unittest.TestCase):
    """Exposed fictional source-policy controls; emission is not engineering acceptance."""
    BASE = EX / "combustion-control-basis"

    def _cases(self):
        data = json.loads((self.BASE / "expected/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], "combustion-control-basis-cases-1")
        self.assertGreaterEqual(len(data["cases"]), 10)
        self.assertEqual(len({c["id"] for c in data["cases"]}), len(data["cases"]))
        return data["cases"]

    def _assert_typed_literal(self, question, vector):
        rows = [e for e in question["evidence"] if e.get("role") == "supplied candidate field"
                and e.get("id") == vector["item_id"] and e.get("field") == vector["where"]]
        self.assertEqual(len(rows), 1, vector)
        _, marker, tail = rows[0]["text"].partition(" = ")
        self.assertTrue(marker, rows[0])
        value, end = json.JSONDecoder().raw_decode(tail)
        self.assertIs(type(value), type(vector["value"]), vector)
        self.assertEqual(value, vector["value"], vector)
        self.assertTrue(tail[end:].startswith("; " + vector["state"] + ";"), rows[0])
        self.assertIn("unverified", tail[end:])

    def _assert_markdown_readback(self, doc, markdown):
        # Decode actual code spans; do not call the product's Markdown formatter as an oracle.
        rows = [e for q in doc["questions"] for e in q["evidence"]
                if e.get("role") == "supplied candidate field"]
        prefix = "- Supplied candidate field: "
        lines = [line[len(prefix):] for line in markdown.splitlines() if line.startswith(prefix)]
        self.assertEqual(len(lines), len(rows))
        def decode_span(text):
            count = len(text) - len(text.lstrip("`"))
            self.assertGreater(count, 0)
            end = text.find("`" * count, count)
            self.assertGreaterEqual(end, count)
            return json.loads(text[count:end]), text[end + count:]
        for row, line in zip(rows, lines):
            text, rest = decode_span(line)
            self.assertTrue(rest.startswith(" ("))
            field, suffix = decode_span(rest[2:])
            self.assertEqual(suffix, ")")
            self.assertEqual((text, field), (row["text"], row["field"]))

    def test_source_cases_keep_minimum_scope_candidates_and_conditional_literals(self):
        import hashlib
        literals = json.loads((self.BASE / "expected/literals.json").read_text(encoding="utf-8"))
        self.assertEqual(literals["schema"], "combustion-control-candidate-literals-1")
        self.assertGreaterEqual(len(literals["rows"]), 197)
        assessed = 0
        for case in self._cases():
            model = (self.BASE / case["model"]).resolve()
            self.assertTrue(model.is_relative_to(self.BASE.resolve()))
            self.assertEqual(hashlib.sha256(model.read_bytes()).hexdigest(), case["model_sha256_raw"])
            for qid, policy in case["rules"].items():
                with self.subTest(case=case["id"], question=qid), tempfile.TemporaryDirectory() as tmp:
                    rc, doc = run(["--model", str(model), "--question", qid], tmp)
                    self.assertEqual(rc, 0)
                    self.assertTrue(all(q["question_id"] == qid for q in doc["questions"]))
                    by_subject = {q["about"]: q for q in doc["questions"]}
                    self.assertEqual(len(by_subject), len(doc["questions"]))
                    self.assertLessEqual(set(policy["minimum_subjects"]), set(by_subject))
                    self.assertLessEqual(set(by_subject), set(policy["allowed_subjects"]))
                    for subject in policy.get("review_or_named_not_checked_subjects", []):
                        explicit_reason = any(n.get("question_id") == qid and subject in n.get("reason", "")
                                              for n in doc.get("not_checked", []) if isinstance(n, dict))
                        self.assertTrue(subject in by_subject or explicit_reason, (case["id"], subject))
                    for subject, question in by_subject.items():
                        assets = {a["id"] for a in question["assets"]}
                        self.assertIn(subject, assets, "every finding must retain its primary subject")
                        self.assertFalse(assets & set(policy["forbidden_candidate_ids"]))
                        self.assertLessEqual(set(policy["required_candidates_if_subject_shown"].get(subject, [])), assets)
                        requests = question["data_requests"]
                        self.assertEqual(len(requests), 2)
                        self.assertTrue(all(r["state"] == "not_on_drawing" and r["where"] for r in requests))
                        self.assertTrue(requests[0]["where"][0].startswith("site records: "))
                        definition = next(q for q in CAT["questions"] if q["id"] == qid)
                        self.assertEqual(len(requests), len(definition["data_requests"]))
                        for request_definition, request in zip(definition["data_requests"], requests):
                            if request_definition.get("show_fields"):
                                self.assertIn("candidate_scope", request)
                                self.assertEqual(request["candidate_scope"], "unit")
                                self.assertIn("candidate_facts", request)
                                self.assertIsInstance(request["candidate_facts"], list)
                                self.assertTrue(all(f["id"] == subject for f in request["candidate_facts"]))
                            self.assertNotIn("already_on_drawing", request)
                        for candidate in policy.get("unclassified_if_shown", []):
                            if candidate in assets:
                                evidence = [e for e in question["evidence"] if e.get("id") == candidate
                                            and e.get("role") != "supplied candidate field"]
                                self.assertTrue(evidence)
                                self.assertTrue(all(re.search(r"unclassified|candidate|context", e["role"], re.I)
                                                    for e in evidence))
                        for vector in literals["rows"]:
                            if (vector["case"], vector["question_id"], vector["subject_id"]) != (case["id"], qid, subject):
                                continue
                            if vector["item_id"] in assets:
                                self._assert_typed_literal(question, vector)
                                assessed += 1
                    # An optional quiet owner contributes no literal-display credit or completion assertion.
                    self._assert_markdown_readback(doc, (Path(tmp) / "screen.md").read_text(encoding="utf-8"))
        self.assertGreater(assessed, 0)

    def test_catalog_keeps_function_sources_and_records_requests_separate_from_project_benefit(self):
        questions = {q["id"]: q for q in CAT["questions"]}
        for qid, required_source in (("E16", "S27"), ("C5", "S8")):
            with self.subTest(question=qid):
                q = questions[qid]
                self.assertIn(required_source, q["typical_benefit"]["source"])
                self.assertIn(required_source, CAT["sources"])
                # This structural guard is not a semantic/source review of arbitrary replacement prose.
                self.assertRegex(q["typical_benefit"]["wording"].lower(), r"\b(no|not|neither)\b")
                self.assertEqual(len(q["data_requests"]), 2)
                self.assertEqual(q["data_requests"][0]["where"][0]["place"], "records")
                self.assertTrue(q["evidence_show_fields"])
                for request in q["data_requests"]:
                    self.assertFalse(request.get("fields"), "candidate fields must not discharge this records review")
                    if request.get("show_fields"):
                        self.assertEqual(request["field_scope"], "unit")

    def test_present_unit_candidates_do_not_complete_the_records_review(self):
        case = next(c for c in self._cases() if c["id"] == "COMB-04-supplied-qualified-flue-record")
        original = json.loads((self.BASE / case["model"]).read_text(encoding="utf-8"))
        definitions = {q["id"]: q for q in CAT["questions"]}
        for qid in ("E16", "C5"):
            with self.subTest(question=qid), tempfile.TemporaryDirectory() as tmp:
                model = copy.deepcopy(original)
                names = {n for r in definitions[qid]["data_requests"] for n in r.get("show_fields", [])}
                self.assertTrue(names)
                for unit in model["units"]:
                    unit.setdefault("facts", {}).update({n: "fictional supplied candidate" for n in names})
                path = Path(tmp) / "candidate-only.json"
                path.write_text(json.dumps(model, ensure_ascii=True), encoding="utf-8")
                out = Path(tmp) / "screen"
                out.mkdir()
                rc, doc = run(["--model", str(path), "--question", qid], out)
                self.assertEqual(rc, 0)
                self.assertTrue(doc["questions"])
                for question in doc["questions"]:
                    self.assertEqual(len(question["data_requests"]), 2)
                    self.assertTrue(all(r["state"] == "not_on_drawing" for r in question["data_requests"]))
                    self.assertTrue(any(r.get("candidate_facts") for r in question["data_requests"]))


    def test_post_static_boiler_selector_controls_keep_declared_roles_separate(self):
        import hashlib
        folder = self.BASE / "selector-controls"
        data = json.loads((folder / "cases.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], "combustion-control-selector-cases-1")
        self.assertEqual(len(data["controls"]), 8)
        for case in data["controls"]:
            with self.subTest(selector=case["id"]):
                path = (folder / case["model"]).resolve()
                self.assertTrue(path.is_relative_to(folder.resolve()))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), case["sha256_raw"])
                questions, not_checked, _, _ = qe.screen(qe.Model(path), CAT, ["C5"])
                self.assertEqual(not_checked, [])
                self.assertEqual([q["id"] for q in questions], case["expected_C5_findings"])
                for question in questions:
                    for vector in case["conditional_literals"]:
                        self._assert_typed_literal(question, vector)
                    self.assertEqual(len(question["data_requests"]), 2)
                    self.assertTrue(all(r["state"] == "not_on_drawing" for r in question["data_requests"]))


class MappingDescriptionSources(unittest.TestCase):
    """Fictional source identity controls; no OPC connection or signal acceptance."""

    CORPUS = EX / "mapping-descriptions"

    def inputs(self, folder):
        model = folder / "model.json"
        model.write_bytes((self.CORPUS / "legacy-model.json").read_bytes())
        sources = []
        for revision in ("revision-a", "revision-b"):
            path = folder / revision / "io.csv"
            path.parent.mkdir()
            path.write_bytes((self.CORPUS / revision / "io.csv").read_bytes())
            sources.append(path)
        return model, sources

    def catalog(self):
        catalog = copy.deepcopy(CAT)
        question = copy.deepcopy(CAT["questions"][0])
        question.update(id="IO1", question="Fictional source-context control, not an engineering finding.",
                        applies_when={"anchor": {"kind": ["instrument"], "isa": "^FT$"},
                                      "group_by": "item"},
                        data_requests=[{"item": "Supplied flow record", "how": "Review the selected source.",
                                        "where": [{"place": "historian", "quantity": "flow"}]}])
        catalog["questions"] = [question]
        return catalog

    def screen(self, model_path, io_paths, output):
        model = qe.Model(model_path, io_paths=io_paths)
        catalog = self.catalog()
        found, nc, quiet, excluded = qe.screen(model, catalog)
        self.assertEqual([q["id"] for q in found], ["IO1@I-FLOW"])
        doc = qe.write_outputs(model, catalog, found, nc, quiet, excluded, output)
        self.assertEqual(doc, json.loads((output / "questions.json").read_bytes()))
        record = next(x for x in doc["mapping_descriptions"] if x["asset_id"] == "I-FLOW")
        signal = next(x["signal"] for x in model.items if x["id"] == "I-FLOW")
        self.assertIn("signal identity unverified", signal.lower())
        return doc, record, signal

    def modern(self, model_path, source):
        import map_points
        fields, rows, spans, evidence = map_points.read_io_list(source)
        self.assertIn("description", fields)
        original = json.loads(model_path.read_bytes())
        updated, report = map_points.plan_mapping(original, rows, source.name,
                                                  source_rows=spans, source_sha256=evidence["sha256"])
        self.assertTrue(report["valid"], report["errors"])
        model_path.write_bytes((json.dumps(updated, indent=2) + "\n").encode("utf-8"))
        return evidence, spans

    def test_actual_mapper_multiline_snapshot_and_renamed_source_are_retained(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            model, (source, _) = self.inputs(folder)
            raw = source.read_bytes()
            evidence, spans = self.modern(model, source)
            self.assertEqual(spans, [(2, 3)])
            moved = folder / "retained-renamed.csv"
            source.rename(moved)
            doc, record, signal = self.screen(model, [moved], folder / "screen")
            expected = json.loads((self.CORPUS / "cases.json").read_bytes())
            self.assertEqual(record["status"], "matched")
            self.assertEqual(record["description"], expected["description_a"])
            self.assertEqual(record["mapping_source"]["source_sha256"], evidence["sha256"])
            self.assertEqual(record["mapping_source"]["source_lines"], [2, 3])
            self.assertEqual(record["selected_source"]["source_lines"], [2, 3])
            self.assertEqual(record["selected_source"]["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(record["selected_source"]["file"], moved.name)
            self.assertEqual(doc["io_lists"], [{"file": moved.name, "sha256": evidence["sha256"], "bytes": len(raw)}])
            self.assertNotIn(str(folder), json.dumps(doc))
            self.assertIn("SYNTHETIC", signal)
            self.assertEqual(moved.read_bytes(), raw)

    def test_bound_wrong_revision_and_unselected_source_remain_unavailable(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            model, (source, foreign) = self.inputs(folder)
            self.modern(model, source)
            original = model.read_bytes()
            good, _, _ = self.screen(model, [source], folder / "matching")
            for label, selected in (("wrong-revision", [foreign]), ("unselected", [])):
                with self.subTest(label=label):
                    doc, record, signal = self.screen(model, selected, folder / label)
                    self.assertEqual(record["status"], "unavailable")
                    self.assertTrue(record["reason"])
                    self.assertNotIn("description", record)
                    self.assertNotIn("UNRELATED REVISION B", signal)
                    self.assertEqual(ids(doc), ids(good))
                    self.assertEqual([q["assets"] for q in doc["questions"]],
                                     [q["assets"] for q in good["questions"]])
            self.assertEqual(model.read_bytes(), original)

    def test_legacy_selection_is_explicit_unverified_and_ambiguous_sources_do_not_attach(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            model, (source, foreign) = self.inputs(folder)
            ambient = folder / "data" / "io_lists"
            ambient.mkdir(parents=True)
            (ambient / "io.csv").write_bytes(foreign.read_bytes())
            with patch.object(qe, "ROOT", folder):
                _, absent, signal = self.screen(model, [], folder / "none")
                self.assertEqual(absent["status"], "unavailable")
                self.assertNotIn("UNRELATED REVISION B", signal)
            _, supplied, signal = self.screen(model, [source], folder / "supplied")
            self.assertEqual(supplied["status"], "unverified_legacy")
            self.assertEqual(supplied["selected_source"]["logical_row"], 2)
            self.assertEqual(supplied["selected_source"]["source_lines"], [2, 3])
            self.assertNotIn("source_sha256", supplied["mapping_source"])
            self.assertIn("unverified", signal.lower())
            _, ambiguous, _ = self.screen(model, [source, foreign], folder / "ambiguous")
            self.assertEqual(ambiguous["status"], "unavailable")
            self.assertNotIn("description", ambiguous)

    def test_same_path_revised_source_is_recaptured_without_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            model, (source, foreign) = self.inputs(folder)
            _, first, _ = self.screen(model, [source], folder / "first")
            source.write_bytes(foreign.read_bytes())
            _, second, signal = self.screen(model, [source], folder / "second")
            self.assertEqual(first["status"], "unverified_legacy")
            self.assertEqual(second["status"], "unverified_legacy")
            self.assertNotEqual(first["selected_source"]["sha256"], second["selected_source"]["sha256"])
            self.assertNotEqual(first["description"], second["description"])
            self.assertIn("UNRELATED REVISION B", signal)
            # Same-address legacy prose is explicitly supplied, not authenticated historical identity.

    def test_physical_span_address_and_explicit_asset_id_are_independent_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            model, (source, _) = self.inputs(folder)
            self.modern(model, source)
            original = json.loads(model.read_bytes())
            changes = [("span", lambda x: x["instruments"][0]["data_point"].update(source_lines=[2, 2])),
                       ("address", lambda x: x["instruments"][0]["data_point"].update(point="OTHER")),
                       ("asset", lambda x: x["instruments"][0].update(id="OTHER-ASSET"))]
            for name, change in changes:
                with self.subTest(name=name):
                    current = copy.deepcopy(original)
                    change(current)
                    model.write_text(json.dumps(current), encoding="utf-8")
                    _, record, _ = self.screen_for_any_id(model, [source], folder / name)
                    self.assertEqual(record["status"], "unavailable")
                    self.assertNotIn("description", record)

    def screen_for_any_id(self, path, sources, output):
        model = qe.Model(path, io_paths=sources)
        catalog = self.catalog()
        found, nc, quiet, excluded = qe.screen(model, catalog)
        self.assertEqual(len(found), 1)
        doc = qe.write_outputs(model, catalog, found, nc, quiet, excluded, output)
        return doc, doc["mapping_descriptions"][0], model.items[0]

    def test_explicit_unreadable_or_malformed_csv_preserves_existing_reports(self):
        for label, raw in (("missing", None), ("duplicate", b"tag,tag,server,base_path,point\n"),
                           ("extra", b"tag,server,base_path,point\nFT-1,S,B,P,extra\n"),
                           ("utf8", b"tag,server,base_path,point\n\xff,S,B,P\n"),
                           ("quote", b'tag,server,base_path,point,description\nFT-1,S,B,P,"unclosed')):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                folder = Path(temp)
                model, _ = self.inputs(folder)
                source = folder / "selected.csv"
                if raw is not None:
                    source.write_bytes(raw)
                output = folder / "out"
                output.mkdir()
                (output / "questions.json").write_bytes(b"prior JSON")
                (output / "screen.md").write_bytes(b"prior Markdown")
                before = OutputPublication.snapshot(self, folder)
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as error:
                    rc = qe.main(["--model", str(model), "--io-list", str(source), "--out", str(output)])
                self.assertEqual(rc, 2, error.getvalue())
                self.assertTrue(error.getvalue())
                self.assertEqual(OutputPublication.snapshot(self, folder), before)


    def test_question_source_metadata_survives_full_core_and_context_semantics(self):
        import context_register as cr
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            model, (source, foreign) = self.inputs(folder)
            original = json.loads(model.read_bytes())
            unrelated = copy.deepcopy(original["instruments"][0])
            unrelated.update(id="I-PRESSURE", tag="PT-2", isa_letters="PT", variable="pressure")
            original["instruments"].append(unrelated)
            model.write_text(json.dumps(original), encoding="utf-8")
            doc, record, _ = self.screen(model, [source], folder / "screen")
            self.assertEqual(len(doc["mapping_descriptions"]), 2)
            expected = doc["questions"][0]["mapping_descriptions"]
            self.assertEqual(expected, [record])
            self.assertEqual([x["asset_id"] for x in expected], ["I-FLOW"])
            question_path = folder / "screen" / "questions.json"
            graph = gx.build(model, questions=question_path)
            for profile in ("full", "core"):
                with self.subTest(profile=profile):
                    selected = gx.apply_profile(graph, profile)
                    self.assertEqual(selected["questions"], doc["questions"])
                    graph_path = folder / (profile + ".json")
                    graph_path.write_text(json.dumps(selected), encoding="utf-8")
                    _, _, keyed = cr.load_inputs(graph_path, question_path)
                    self.assertEqual(keyed["IO1@I-FLOW"]["question"]["mapping_descriptions"], expected)
            question = doc["questions"][0]
            self.assertEqual(cr.semantic(question)["mapping_descriptions"], expected)
            changed_status = copy.deepcopy(question)
            changed_status["mapping_descriptions"][0]["status"] = "unavailable"
            self.assertNotEqual(cr.semantic(question), cr.semantic(changed_status))
            revised, _, _ = self.screen(model, [foreign], folder / "revision-b")
            self.assertEqual(ids(revised), ids(doc))
            self.assertNotEqual(cr.semantic(question), cr.semantic(revised["questions"][0]))

    def test_source_identity_types_address_components_and_tag_fallback(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            model, (source, _) = self.inputs(folder)
            self.modern(model, source)
            item = json.loads(model.read_bytes())["instruments"][0]
            sources = qe.load_io_sources([source])
            for field, value in (("source_lines", [True, 3]), ("source_lines", [2.0, 3]),
                                 ("source_lines", [2, False]), ("source_sha256", True),
                                 ("source_sha256", "not-a-raw-hash"),
                                 ("server", "OTHER"), ("base_path", "OTHER"), ("point", "OTHER")):
                with self.subTest(field=field, value=value):
                    dp = copy.deepcopy(item["data_point"])
                    dp[field] = value
                    record = qe.point_description(dp, item, sources)
                    self.assertEqual(record["status"], "unavailable")
                    self.assertNotIn("description", record)
                    self.assertTrue(record["reason"])
            no_hash = copy.deepcopy(item["data_point"])
            no_hash.pop("source_sha256")
            self.assertEqual(qe.point_description(no_hash, item, sources)["status"], "unavailable")
            original_pin = qe.point_description(item["data_point"], dict(item, tag="DIFFERENT-TAG"), sources)
            self.assertEqual(original_pin["status"], "matched")
            # An explicit asset_id takes precedence over the CSV/model tag spelling.
            normalized = folder / "normalized.csv"
            raw = source.read_bytes().replace(b"I-FLOW,FT-1,", b",ft_1,")
            normalized.write_bytes(raw)
            dp = copy.deepcopy(item["data_point"])
            dp["source_sha256"] = hashlib.sha256(raw).hexdigest()
            normalized_sources = qe.load_io_sources([normalized])
            self.assertEqual(qe.point_description(dp, item, normalized_sources)["status"], "matched")
            self.assertEqual(qe.point_description(dp, dict(item, tag="PT-2"), normalized_sources)["status"],
                             "unavailable")
            expected = json.loads((self.CORPUS / "cases.json").read_bytes())
            for source_case in expected["raw_sources"]:
                original_raw = (self.CORPUS / source_case["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(original_raw).hexdigest(), source_case["sha256_raw"])
                self.assertEqual(len(original_raw), source_case["bytes"])


class MappingDescriptionLookupWork(unittest.TestCase):
    """Generated fictional records; bounded traversal work, no clock or plant-scale claim."""

    class VisitRecords(list):
        def __init__(self, records):
            super().__init__(records)
            self.__dict__.update(getattr(records, "__dict__", {}))
            self.visits = 0

        def __iter__(self):
            for record in super().__iter__():
                self.visits += 1
                yield record

    def source(self, folder, count, name="io.csv", suffix=""):
        raw = ("tag,server,base_path,point,description\n" + "".join(
            f"FT-{n},SYNTHETIC-OPC,basis,P{n},supplied {n}{suffix}\n" for n in range(1, count + 1))).encode()
        path = folder / name
        path.write_bytes(raw)
        return path, qe.load_io_sources([path])[0]

    def mapping(self, source, row, *, legacy=False):
        dp = {"server": "SYNTHETIC-OPC", "base_path": "basis", "point": f"P{row}",
              "source": f"io.csv {'row' if legacy else 'line'} {row + 1}"}
        if not legacy:
            dp.update(source_sha256=source["sha256"], source_lines=[row + 1, row + 1])
        return dp, {"id": f"I-{row}", "tag": f"FT-{row}"}

    def test_captured_lookup_work_does_not_scan_all_rows_for_each_asset(self):
        observed = []
        for count in (64, 256):
            with self.subTest(records=count), tempfile.TemporaryDirectory() as temp:
                _, source = self.source(Path(temp), count)
                records = self.VisitRecords(source["records"])
                source["records"] = records
                lookup_rows = (1, count // 2, count, count + 1) * 2
                for row in lookup_rows:
                    dp, asset = self.mapping(source, row)
                    result = qe.point_description(dp, asset, [source])
                    if row <= count:
                        self.assertEqual(result["status"], "matched")
                        self.assertEqual(result["description"], f"supplied {row}")
                        self.assertEqual(result["selected_source"]["source_lines"], [row + 1, row + 1])
                        self.assertEqual(result["selected_source"]["logical_row"], row + 1)
                    else:
                        self.assertEqual(result["status"], "unavailable")
                        self.assertNotIn("description", result)
                # Bound exposed-record traversal per lookup, rather than elapsed time or an index layout.
                observed.append(records.visits)
                self.assertLessEqual(records.visits, 2 * len(lookup_rows))
        self.assertLessEqual(observed[1], max(observed[0], 16))

    def test_lookup_indexes_preserve_duplicate_order_ambiguity_and_plain_context(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            first_path, first = self.source(folder, 4)
            renamed_path = folder / "renamed.csv"
            renamed_path.write_bytes(first_path.read_bytes())
            renamed = qe.load_io_sources([renamed_path])[0]
            dp, asset = self.mapping(first, 4)
            expected = qe.point_description(dp, asset, [first])
            self.assertEqual(expected["status"], "matched")
            self.assertEqual(qe.point_description(dp, asset, [first, renamed]), expected)
            reversed_result = qe.point_description(dp, asset, [renamed, first])
            renamed_expected = copy.deepcopy(expected)
            renamed_expected["selected_source"]["file"] = "renamed.csv"
            self.assertEqual(reversed_result, renamed_expected)
            plain = {key: copy.deepcopy(first[key]) for key in ("file", "sha256", "bytes", "records")}
            plain["records"] = list(plain["records"])
            self.assertEqual(qe.point_description(dp, asset, [plain]), expected)
            # Source contexts remain ordinary JSON content; index internals must not leak into its keys.
            self.assertEqual(json.loads(json.dumps(first)), plain)
            other = folder / "other"
            other.mkdir()
            _, revised = self.source(other, 4, suffix=" revised")
            legacy_dp, legacy_asset = self.mapping(first, 4, legacy=True)
            self.assertEqual(qe.point_description(legacy_dp, legacy_asset, [first])["status"],
                             "unverified_legacy")
            ambiguous = qe.point_description(legacy_dp, legacy_asset, [first, revised])
            self.assertEqual(ambiguous["status"], "unavailable")
            self.assertNotIn("description", ambiguous)


class PortableScheduleLabels(unittest.TestCase):
    """Working-copy logical identities; labels do not authenticate schedules or select revisions."""

    cli = ServiceReconciliation.cli
    intake = ServiceReconciliation.intake
    schedule = ServiceReconciliation.schedule
    sources = ServiceReconciliation.sources
    declaration = ServiceReconciliation.declaration
    attach = ServiceReconciliation.attach

    def copied_sources(self, base):
        model, first, second = self.sources(base)
        labels = ("../not-opened/水 [draft] `A`.json", "site records/refrigeration B.json")
        self.attach(second, self.declaration(first=labels[0], second=labels[1]))
        originals = {first: first.read_bytes(), second: second.read_bytes()}
        copies = []
        for number, (source, label) in enumerate(zip((first, second), labels)):
            folder = base / f"relocated-{number}"
            folder.mkdir()
            target = folder / "schedule.json"
            data = json.loads(source.read_bytes())
            data["source_label"] = label
            target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            self.assertEqual({key: value for key, value in data.items() if key != "source_label"},
                             json.loads(originals[source]))
            copies.append(target)
        return model, copies, labels, originals

    def test_distinct_labels_relocate_same_basename_and_preserve_complete_choice(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            model, (first, second), labels, originals = self.copied_sources(base)
            expected = self.declaration(first=labels[0], second=labels[1])
            resolutions = []
            for paths in ((first, second), (second, first)):
                merged = qe.load_schedule(paths)
                entry = merged[("1", "P-1")]
                resolution = entry["service_reconciliation"]
                self.assertEqual(resolution["candidates"], sorted(expected["candidates"], key=lambda x: (x["file"], x["row"], x["service"])))
                self.assertEqual(resolution["selected"], expected["selected"])
                self.assertEqual(resolution["declarations"], [{"file": labels[1], "row": 1,
                    "status": "draft", "basis": expected["basis"], "selected": expected["selected"]}])
                self.assertIn("organizational approval unverified", resolution["authority"])
                self.assertEqual(entry["fields"], {"HP": 10})
                self.assertEqual(entry["field_sources"], {"HP": sorted(labels)})
                resolutions.append(copy.deepcopy(resolution))
                loaded = qe.Model(model, schedule_paths=paths)
                self.assertEqual(loaded.schedule_sources, sorted(labels))
                self.assertTrue(set(map(Path, paths)) <= loaded.source_paths)
            self.assertEqual(resolutions[0], resolutions[1])
            self.assertTrue(all(path.read_bytes() == raw for path, raw in originals.items()))
            # The path-shaped logical label above does not exist and must never be opened as input.

    def test_invalid_duplicate_labels_and_changed_candidates_refuse(self):
        invalid = (None, False, 7, [], {}, "", " ", " label", "label ", "a\x00b", "a\x1fb",
                   "a\x7fb", "a\x85b", "a\u2028b", "a\u2029b", "a\ud800b", "a\udfffb")
        for label in invalid:
            with self.subTest(label=repr(label)), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "empty.json"
                path.write_text(json.dumps({"source_label": label, "sheets": {}}), encoding="utf-8")
                before = path.read_bytes()
                with self.assertRaises(qe.InputError):
                    qe.load_schedule([path])
                self.assertEqual(path.read_bytes(), before)
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            first, second = base / "a.json", base / "b.json"
            for path in (first, second):
                path.write_text(json.dumps({"source_label": "same opaque ID", "sheets": {}}), encoding="utf-8")
            with self.assertRaises(qe.InputError):
                qe.load_schedule([first, second])
        for change in ("service", "row"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temp:
                base = Path(temp)
                _, (first, second), _, originals = self.copied_sources(base)
                value = json.loads(first.read_bytes())
                if change == "service":
                    value["sheets"]["1"][0]["service"] = "Changed source service"
                else:
                    value["sheets"]["1"].insert(0, {"tag": "OTHER", "service": "Other service"})
                first.write_text(json.dumps(value), encoding="utf-8")
                with self.assertRaisesRegex(qe.InputError, "stale or mismatched service_resolution"):
                    qe.load_schedule([first, second])
                self.assertTrue(all(path.read_bytes() == raw for path, raw in originals.items()))

    def test_logical_labels_do_not_replace_actual_path_output_protection(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            model, (first, second), _, _ = self.copied_sources(base)
            output = base / "reports"
            output.mkdir()
            os.link(first, output / "screen.md")
            (output / "questions.json").write_bytes(b"prior report")
            before = {path.relative_to(base).as_posix(): path.read_bytes() for path in base.rglob('*') if path.is_file()}
            result = self.cli(["--model", model, "--schedule", first, "--schedule", second, "--out", output], 2)
            self.assertIn("overlaps input", result.stderr)
            self.assertEqual({path.relative_to(base).as_posix(): path.read_bytes() for path in base.rglob('*') if path.is_file()}, before)


    def test_explicit_label_field_locations_survive_screen_and_saved_rollup(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            model, first, second = self.sources(base)
            labels = ("Ω source `A`, field invented.json", "records/B [draft], field `x`.json")
            for path, label in zip((first, second), labels):
                value = json.loads(path.read_bytes())
                value.update(source_label=label)
                value["sheets"]["1"][0]["fields"] = {"HP": 10, "RPM": None}
                path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
            self.attach(second, self.declaration(first=labels[0], second=labels[1]))
            loaded = qe.Model(model, schedule_paths=[first, second])
            self.assertEqual(loaded.schedule[("1", "P-1")]["field_sources"],
                             {"HP": sorted(labels), "RPM": sorted(labels)})
            catalog = {"families": {"metering": "Metering"}, "sources": {}, "questions": [{
                "id": "SL01", "family": "metering", "question": "Fictional schedule-location control.",
                "applies_when": {"anchor": {"kind": ["equipment"]}, "group_by": "item"},
                "evidence_fields": ["tag"], "data_requests": [{"item": "Supplied rating fields",
                    "fields": ["HP", "RPM"], "where": [{"place": "records", "what": "selected schedule"}],
                    "how": "Review the supplied field locations; no engineering conclusion."}],
                "decision_rule": "Review source context only.", "limits": "Fictional software control.",
                "typical_benefit": {"wording": "No benefit claimed.", "source": [], "arc": None}}]}
            catalog_path = base / "catalog.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            found, nc, quiet, excluded = qe.screen(loaded, catalog)
            self.assertEqual([q["id"] for q in found], ["SL01@P1"])
            self.assertEqual(found[0]["assets"], [{"id": "P1", "tag": "P-1"}])
            present = next(e for e in found[0]["evidence"] if e["role"] == "on drawing")
            request = found[0]["data_requests"][0]
            blank_location = next(where for where in request["where"] if "blank RPM" in where)
            self.assertIn(", field HP (source: ", present["field"])
            self.assertIn(", field RPM (source: ", blank_location)
            quoted_labels = ["``" + json.dumps(label, ensure_ascii=True) + "``" for label in labels]
            for literal in quoted_labels:
                self.assertIn(literal, present["field"])
                self.assertIn(literal, blank_location)
            output = base / "screen"
            doc = qe.write_outputs(loaded, catalog, found, nc, quiet, excluded, output,
                                   catalog_path=catalog_path)
            saved = json.loads((output / "questions.json").read_bytes())
            self.assertEqual(saved, doc)
            self.assertEqual(saved["schedules"], sorted(labels))
            self.assertEqual(saved["service_reconciliations"][0]["selected"]["file"], labels[0])
            readable = (output / "screen.md").read_text(encoding="utf-8")
            whole_literal = "```" + json.dumps(present["field"], ensure_ascii=True) + "```"
            self.assertIn("(" + whole_literal + ")", readable)
            self.assertNotIn("(`" + present["field"] + "`)", readable)
            self.assertIn(blank_location, readable)
            rolled = qe.rollup(["fixture=" + str(output)], catalog, catalog_path=catalog_path)
            rollup_text = qe.render_rollup_md(rolled, catalog)
            self.assertIn(blank_location, rollup_text)
            for literal in quoted_labels:
                self.assertIn(literal, rollup_text)
            self.assertEqual(json.loads((output / "questions.json").read_bytes()), saved)


class ValveFeedbackBasis(unittest.TestCase):
    """Frozen source-policy/software controls; not installed-state or human-usefulness acceptance."""
    BASE = EX / "valve-feedback-basis"

    def inputs(self):
        expected = json.loads((self.BASE / "expected/source-cases.json").read_bytes())
        inventory = json.loads((self.BASE / "expected/model-inventory.json").read_bytes())
        vectors = json.loads((self.BASE / "expected/input-vectors.json").read_bytes())
        self.assertEqual(expected["schema"], "c3-source-cases-1")
        self.assertGreaterEqual(len(expected["cases"]), 6)
        self.assertGreaterEqual(len(inventory), 8)
        self.assertGreaterEqual(len(vectors), 189)
        return {case["id"]: case for case in expected["cases"]}, inventory, vectors

    def model_path(self, case):
        import hashlib
        path = (ROOT / case["model"]).resolve()
        self.assertTrue(path.is_relative_to(self.BASE.resolve()))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), case["sha256_raw"])
        return path

    def questions(self, case):
        path = self.model_path(case)
        model = qe.Model(path)
        questions, not_checked, quiet, _ = qe.screen(model, CAT, ["C3"])
        return path, model, questions, not_checked, quiet

    def subjects(self, questions):
        return {e["id"] for q in questions for e in q["evidence"]
                if e.get("role") == "trigger" and e.get("id") in {"FCV-A", "FCV-B"}}

    def assert_literal(self, questions, vector):
        where = f"{vector['section']}[{vector['id']}].facts.{vector['name']}"
        matches = [e for q in questions for e in q["evidence"]
                   if e.get("role") == "supplied candidate field"
                   and e.get("id") == vector["id"] and e.get("field") == where]
        self.assertEqual(len(matches), 1, vector)
        _, separator, tail = matches[0]["text"].partition(" = ")
        self.assertTrue(separator, matches[0])
        value, end = json.JSONDecoder().raw_decode(tail)
        self.assertIs(type(value), type(vector["value"]), vector)
        self.assertEqual(type(value).__name__, vector["type"], vector)
        self.assertEqual(json.dumps(value, ensure_ascii=True, sort_keys=True),
                         json.dumps(vector["value"], ensure_ascii=True, sort_keys=True), vector)
        # These frozen inputs use only null/'unknown' placeholders; preserve their exact JSON values.
        state = "blank" if vector["value"] is None or vector["value"] == "unknown" else "present"
        self.assertTrue(tail[end:].startswith("; " + state + ";"), matches[0])
        self.assertIn("unverified", tail[end:])

    def test_source_pairs_selectors_and_all_active_typed_input_facts(self):
        policies, inventory, vectors = self.inputs()
        assessed, unshown = 0, 0
        for case in inventory:
            with self.subTest(case=case["id"]):
                path, _, questions, not_checked, quiet = self.questions(case)
                shown = self.subjects(questions)
                minimum, allowed = set(case["minimum_subjects"]), set(case["allowed_subjects"])
                self.assertLessEqual(shown, allowed)
                for subject in minimum - shown:
                    self.assertTrue(any(row.get("question_id") == "C3" and subject in row.get("reason", "")
                                        for row in not_checked), (case["id"], subject))
                if not allowed:
                    self.assertEqual(questions, [])
                    self.assertTrue("C3" in quiet or any(r.get("question_id") == "C3" for r in not_checked))
                    continue
                policy = policies[case["id"]]
                self.assertEqual(minimum, set(policy["minimum_subjects"]))
                self.assertEqual(allowed, set(policy["allowed_subjects"]))
                self.assertTrue(all(q["id"] == policy["expected_finding_id_if_shown"] for q in questions))
                assets = {a["id"] for q in questions for a in q["assets"]}
                for record in policy["records"]:
                    target = record.get("measures_valve")
                    relevant = target in shown or target not in allowed and bool(shown)
                    if relevant and record["id"] in policy["required_record_ids_if_relevant_subject_shown"]:
                        self.assertIn(record["id"], assets)
                for vector in (v for v in vectors if v["case"] == case["id"]):
                    if vector["id"] in assets:
                        self.assert_literal(questions, vector)
                        assessed += 1
                    else:
                        unshown += 1  # Optional quiet is not assessed as a literal-display pass.
                # Controller qualifier facts are separate source carriers, never anchor completion fields.
                source = json.loads(path.read_bytes())
                selected = next(q for q in CAT["questions"] if q["id"] == "C3")["evidence_show_fields"]
                for controller in source.get("controllers", []):
                    if controller["tag"] not in assets:
                        continue
                    for name, value in (controller.get("facts") or {}).items():
                        if name in selected:
                            self.assert_literal(questions, {"section": "controllers", "id": controller["tag"],
                                "name": name, "value": value, "type": type(value).__name__})
        self.assertEqual(assessed + unshown, len(vectors))
        self.assertGreater(assessed, 0)

    def test_both_records_reviews_stay_open_and_candidates_do_not_complete_other_anchors(self):
        policies, inventory, _ = self.inputs()
        definition = next(q for q in CAT["questions"] if q["id"] == "C3")
        self.assertEqual(len(definition["data_requests"]), 2)
        for request in definition["data_requests"]:
            self.assertEqual(request.get("field_scope", "anchors"), "anchors")
            self.assertFalse(request.get("fields"))
            self.assertTrue(request.get("show_fields"))
            self.assertTrue(all(place["place"] in {"dcs", "maintenance", "records", "historian"}
                                for place in request["where"]))
        candidates = 0
        for case in (c for c in inventory if c["id"] in policies):
            with self.subTest(case=case["id"]):
                _, _, questions, _, _ = self.questions(case)
                for question in questions:
                    anchors = self.subjects([question])
                    nonanchors = {a["id"] for a in question["assets"]} - anchors
                    self.assertEqual(len(question["data_requests"]), 2)
                    for request in question["data_requests"]:
                        self.assertEqual(request["state"], "not_on_drawing")
                        self.assertEqual(request["candidate_scope"], "anchors")
                        self.assertIsInstance(request["candidate_facts"], list)
                        self.assertTrue(request["where"])
                        self.assertFalse(any(location.startswith("a walkdown:") for location in request["where"]))
                        self.assertNotIn("already_on_drawing", request)
                        for fact in request["candidate_facts"]:
                            self.assertIn(fact["id"], anchors)
                            self.assertNotIn(fact["id"], nonanchors)
                            self.assertTrue(fact["where"].startswith(f"final_elements[{fact['id']}].facts."))
                            candidates += 1
        self.assertGreater(candidates, 0)

    def test_complete_generated_c3_question_survives_full_and_core_graph(self):
        _, inventory, _ = self.inputs()
        case = next(c for c in inventory if c["id"] == "C3-01-omission-local")
        path, _, questions, not_checked, _ = self.questions(case)
        self.assertEqual(not_checked, [])
        self.assertEqual([q["id"] for q in questions], ["C3@model"])
        expected = json.dumps(questions, ensure_ascii=True, sort_keys=True)
        with tempfile.TemporaryDirectory() as temp:
            question_path = Path(temp) / "questions.json"
            question_path.write_text(json.dumps({"questions": questions}, ensure_ascii=False), encoding="utf-8")
            before = question_path.read_bytes()
            graph = gx.build(path, questions=question_path)
            for profile in ("full", "core"):
                with self.subTest(profile=profile):
                    result = gx.apply_profile(graph, profile)
                    self.assertEqual(json.dumps(result["questions"], ensure_ascii=True, sort_keys=True), expected)
                    self.assertEqual(result["counts"]["questions"], 1)
                    self.assertEqual(gx.problems(result), [])
            self.assertEqual(question_path.read_bytes(), before)

class NativeUnplacedQuestionHandoff(unittest.TestCase):
    """Seen reader interpretations and fictional controls; no operating or human-usefulness acceptance."""

    def fixture(self, name):
        base = Path(globals().get("N114_DATA", ROOT / "examples/graph-export/unplaced-dexpi/question-handoff/expected"))
        return base / name

    def data(self, name):
        return json.loads(self.fixture(name).read_bytes())

    def equal_json(self, actual, expected):
        # Python nested equality alone would equate false/0 and integer/float values.
        self.assertEqual(json.dumps(actual, ensure_ascii=True, sort_keys=True, allow_nan=False),
                         json.dumps(expected, ensure_ascii=True, sort_keys=True, allow_nan=False))

    def patched(self, value, operations):
        result = copy.deepcopy(value)
        def location(pointer):
            parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
            parent = result
            for part in parts[:-1]:
                parent = parent[int(part)] if isinstance(parent, list) else parent[part]
            return parent, parts[-1]
        for operation in operations:
            parent, key = location(operation["path"])
            if operation["op"] == "copy":
                source, source_key = location(operation["from"])
                incoming = copy.deepcopy(source[int(source_key)] if isinstance(source, list) else source[source_key])
            else:
                incoming = copy.deepcopy(operation.get("value"))
            if operation["op"] == "test":
                self.equal_json(parent[int(key)] if isinstance(parent, list) else parent[key], incoming)
            elif operation["op"] == "remove":
                if isinstance(parent, list):
                    del parent[int(key)]
                else:
                    del parent[key]
            elif isinstance(parent, list):
                if key == "-":
                    parent.append(incoming)
                elif operation["op"] in ("add", "copy"):
                    parent.insert(int(key), incoming)
                else:
                    parent[int(key)] = incoming
            else:
                parent[key] = incoming
        return result

    def case(self, case_id):
        import hashlib
        documents = (self.data("core-controls.json"), self.data("supplement-controls.json"), self.data("L4-controls.json"))
        for document in documents:
            for case in document["cases"]:
                if case["id"] != case_id:
                    continue
                if "raw_model_utf8" in case:
                    return case["raw_model_utf8"].encode("utf-8")
                base_id = case.get("base", "i04")
                base = documents[0]["base_models"][base_id]
                raw = (ROOT / base["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), base["sha256_raw"])
                model = self.patched(json.loads(raw), case.get("patch", []))
                if document is documents[0] and case.get("authored"):
                    model["meta"]["authored_control"] = {"case_id": case_id,
                        "basis": "FICTIONAL N114 SOFTWARE CONTROL; original XML does not assert these changes"}
                return model
        self.fail("Unknown frozen control " + case_id)

    def screen_case(self, folder, model, loops=None, expected=0):
        folder.mkdir(parents=True, exist_ok=True)
        path, out = folder / "model.json", folder / "screen"
        if isinstance(model, bytes):
            path.write_bytes(model)
        else:
            path.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        argv = ["--model", str(path), "--catalog", str(globals().get("N114_CATALOG", ROOT / "data/questions.json")),
                "--question", "C3", "--out", str(out)]
        if loops is not None:
            loop_path = folder / "loops.csv"
            loop_path.write_text(loops, encoding="utf-8", newline="\n")
            argv += ["--loops", str(loop_path)]
        if expected:
            out.mkdir(exist_ok=True)
            for name in ("questions.json", "screen.md"):
                (out / name).write_bytes(b"retained sentinel\n")
            before = {p.name: p.read_bytes() for p in out.iterdir()}
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = qe.main(argv)
        self.assertEqual(result, expected, stderr.getvalue())
        if expected:
            self.assertEqual({p.name: p.read_bytes() for p in out.iterdir()}, before)
            return stderr.getvalue()
        self.assertEqual(stderr.getvalue(), "")
        return path, out, json.loads((out / "questions.json").read_bytes()), (out / "screen.md").read_text(encoding="utf-8")

    def anchors(self, document):
        return {record["id"] for question in document["questions"] for record in question["evidence"]
                if record.get("role") == "trigger"}

    def context_rows(self, document, identity):
        return [record["provenance"] for question in document["questions"] for record in question["evidence"]
                if record.get("id") == identity and isinstance(record.get("provenance"), dict)]

    def readable_rows(self, document, markdown):
        decoded = []
        for match in re.finditer(r'`+(?=")', markdown):
            try:
                value, _ = json.JSONDecoder().raw_decode(markdown[match.end():])
            except ValueError:
                continue
            if isinstance(value, str):
                decoded.append(value)
        for question in document["questions"]:
            for record in question["evidence"]:
                if record.get("provenance"):
                    self.assertIn(record["text"], decoded)

    def test_partial_roles_unknown_placement_and_original_source_qualifiers(self):
        expectations = {case["id"]: case for case in self.data("core-expected.json")["cases"]}
        expectations["L4-class-qualified-local-identifier"] = self.data("L4-expected.json")
        selected = ["U00-i04-original", "U01-i01-original", "U02-controller-only", "U03-unplaced-only",
                    "U04-unknown-role", "U05-rejected-valve", "U11-utility-does-not-own", "L4-class-qualified-local-identifier"]
        with tempfile.TemporaryDirectory() as tmp:
            for number, case_id in enumerate(selected):
                with self.subTest(case=case_id):
                    source = self.case(case_id)
                    path, out, document, markdown = self.screen_case(Path(tmp) / str(number), source)
                    expected = expectations[case_id]
                    required = expected.get("required_valve_anchors", expected.get("required_C3_anchors", []))
                    self.assertEqual(self.anchors(document), set(required))
                    self.assertEqual([q["id"] for q in document["questions"]], ["C3@model"] if required else [])
                    self.readable_rows(document, markdown)
                    for identity in required:
                        contexts = self.context_rows(document, identity)
                        self.assertTrue(contexts)
                        original = next(row for row in source["unplaced"] if row["tag"] == identity)
                        for context in contexts:
                            for field in ("tag", "kind", "unit", "source", "dexpi_id", "dexpi_class", "tag_basis",
                                          "assigned_tag", "unit_basis", "unplaced_reason", "variable"):
                                if field in original:
                                    self.assertIn(field, context["record_fields"])
                                    self.equal_json(context["record_fields"][field], original[field])
                            self.assertIn("unknown", context["placement"])
                            self.assertIsNone(context["record_fields"].get("unit"))
                        self.assertNotIn("at T100", markdown)
                    if case_id == "U00-i04-original":
                        controller = self.context_rows(document, "FIC-04")
                        self.assertTrue(controller)
                        endpoint = next(row for row in controller[0]["endpoint_context"] if row["id"] == "FT-04")
                        self.assertIs(endpoint["record_fields"]["assigned_tag"], True)
                        self.assertEqual(endpoint["record_fields"]["variable"], "flow")
                        self.assertIn("ASSIGNED here", endpoint["record_fields"]["tag_basis"])
                        self.assertIn("not measured valve travel", markdown)
                    if case_id.startswith("L4"):
                        valve_row = next(e for q in document["questions"] for e in q["evidence"]
                                         if e["id"] == "local-item-alpha" and e.get("role") == "trigger")
                        self.assertNotIn("reader-assigned", valve_row["text"])
                        self.assertNotIn("assigned by the reader", valve_row["text"])
                    if case_id == "U05-rejected-valve":
                        self.assertIn("FV-04", json.dumps(document["review_exclusions"]))

    def test_exact_reference_scope_lists_graphs_and_separate_loop_controls(self):
        core = {case["id"]: case for case in self.data("core-expected.json")["cases"]}
        supplementary = self.data("supplement-expected.json")["cases"]
        selected = ["U09-foreign-valid-endpoint", "U12-exact-ids-not-aliases", *supplementary]
        with tempfile.TemporaryDirectory() as tmp:
            for number, case_id in enumerate(selected):
                with self.subTest(case=case_id):
                    source = self.case(case_id)
                    path, out, document, markdown = self.screen_case(Path(tmp) / str(number), source)
                    expected = core.get(case_id, supplementary.get(case_id))
                    required = expected.get("required_valve_anchors", expected.get("required_C3_anchors", []))
                    self.assertEqual(self.anchors(document), set(required))
                    contexts = self.context_rows(document, "FIC-04")
                    self.assertTrue(contexts)
                    raw = source["controllers"][0]
                    reference_fields = {key: raw[key] for key in ("measurement", "measurement_unplaced", "output_unplaced", "output") if key in raw}
                    for context in contexts:
                        self.equal_json(context["reference_fields"], reference_fields)
                        commands = expected.get("controller_exact_command_endpoints", {}).get("FIC-04")
                        if commands is None:
                            commands = list(expected.get("command_targets_ordered", []))
                            if "command_targets_by_field" in expected:
                                commands = [target for targets in expected["command_targets_by_field"].values() for target in targets]
                        self.equal_json(context["active_exact_endpoints"]["outputs"], commands)
                    graph = gx.build(path, questions=out / "questions.json")
                    for profile in ("full", "core"):
                        result = gx.apply_profile(graph, profile)
                        self.assertEqual(gx.problems(result), [])
                        self.equal_json(result["questions"], document["questions"])
                        graph_ids = {node["id"] for node in result["nodes"]}
                        for question in result["questions"]:
                            self.assertLessEqual({a["id"] for a in question["assets"]}, graph_ids)
                            self.assertLessEqual({e["id"] for e in question["evidence"]}, graph_ids)
                    if "controls_edges" in expected:
                        actual = {(edge["from"], edge["to"]) for edge in graph["edges"] if edge["type"] == "controls"}
                        self.assertEqual(actual, {tuple(edge) for edge in expected["controls_edges"]})
                    self.readable_rows(document, markdown)
            # These are nine exposed loop-supplement controls, not extra source models/plants.
            loop_cases = {case["id"]: case for case in self.data("loops-controls.json")["cases"]}
            for case_id in ("NL01-new-exact-controller", "NL02-known-rejected-controller", "NL03-known-rejected-output",
                            "NL08-active-CSV-controller-cascade", "NL09-empty-endpoints-unknown"):
                with self.subTest(loop_control=case_id):
                    case = loop_cases[case_id]
                    model = self.patched(self.case("U00-i04-original"), case.get("patch", []))
                    folder = Path(tmp) / case_id
                    path, out, document, markdown = self.screen_case(folder, model, case["csv"])
                    if case_id.startswith("NL03"):
                        self.assertEqual(document["questions"], [])
                    elif case_id.startswith("NL02"):
                        self.assertEqual(self.anchors(document), {"FV-04"})
                        self.assertFalse(self.context_rows(document, "FIC-04"))
                    else:
                        parsed = qe.Model(path, loops=folder / "loops.csv")
                        identities = ["FIC-904"] if case_id.startswith("NL01") else ["FIC-904", "FIC-905"]
                        for identity in identities:
                            self.assertIn(identity, parsed.by_id)
                        if case_id.startswith("NL08"):
                            self.equal_json(parsed.by_id["FIC-904"]["sets"], ["FIC-905"])
                            self.assertFalse(qe.related(parsed, parsed.by_id["FV-04"], parsed.by_id["FIC-904"], {"relation": "drives"}))
                        if case_id.startswith("NL09"):
                            self.assertFalse(qe.related(parsed, parsed.by_id["FV-04"], parsed.by_id["FIC-904"], {"relation": "drives"}))
                        candidate = "FIC-904" if case_id.startswith("NL01") else "FIC-905"
                        contexts = self.context_rows(document, candidate)
                        self.assertTrue(contexts)
                        self.assertIn("not a node", contexts[0]["graph_representation"])
                        self.assertEqual(contexts[0]["loop_record"]["controller"], candidate)

    def test_source_specific_refusals_preserve_both_reports(self):
        controls = {"U06-duplicate-identity": ("ambiguous", "duplicate"),
                    "U07-incompatible-endpoint": ("incompatible", "role"),
                    "U08-missing-endpoint": ("missing",), "U10-malformed-json": ("json",)}
        with tempfile.TemporaryDirectory() as tmp:
            for case_id, words in controls.items():
                with self.subTest(case=case_id):
                    error = self.screen_case(Path(tmp) / case_id, self.case(case_id), expected=2)
                    for word in words:
                        self.assertIn(word, error.casefold())
            cases = self.data("loops-controls.json")["cases"]
            for case in cases:
                case_id = case["id"]
                if not case_id.startswith(("NL04", "NL05", "NL06", "NL07")):
                    continue
                with self.subTest(loop_control=case_id):
                    base = "U09-foreign-valid-endpoint" if case_id.startswith("NL05") else "U00-i04-original"
                    source = self.patched(self.case(base), case.get("patch", []))
                    error = self.screen_case(Path(tmp) / case_id, source, case["csv"], expected=2)
                    words = (("none", "names a tag") if case_id.startswith("NL04") else
                             ("conflict", "endpoint") if case_id.startswith("NL05") else
                             ("FIC-904", "output", "FT-04", "incompatible") if case_id.startswith("NL06") else
                             ("FIC-904", "output", "FV_04", "missing"))
                    for word in words:
                        self.assertIn(word, error)

    def test_partial_answer_source_revision_and_review_qualifier_freshness(self):
        import csv
        import context_register as cr
        from serve_snapshot import Snapshot, InputError as SnapshotInputError
        def save(path, value):
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        def context(command, graph, questions, sources, out, register=None, answers=None, expected=0):
            argv = [command, "--model", str(graph), "--questions", str(questions), "--sources", str(sources), "--out", str(out)]
            if register: argv += ["--register", str(register)]
            if answers: argv += ["--answers", str(answers)]
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = cr.main(argv)
            self.assertEqual(result, expected, stderr.getvalue())
            return stderr.getvalue() if expected else json.loads((out / "context.json").read_bytes())
        def accept(folder, model):
            path, screen, document, markdown = self.screen_case(folder, model)
            self.assertEqual([q["id"] for q in document["questions"]], ["C3@model"])
            graph = folder / "full.graph.json"
            save(graph, gx.build(path, questions=screen / "questions.json"))
            prepared, accepted = folder / "prepared", folder / "accepted"
            sources = self.fixture("r1/sources.json")
            context("prepare", graph, screen / "questions.json", sources, prepared)
            with (prepared / "evidence_choices.csv").open(encoding="utf-8", newline="") as stream:
                choices = list(csv.DictReader(stream))
            choice = next(row for row in choices if (row["question_id"], row["source_id"], row["locator_id"]) ==
                          ("C3@model", "N114-FICTIONAL-NOTE", "command-limits"))
            fields = self.data("answer-fields.json")["fields"]
            row = {name: "" for name in cr.COLUMNS}
            row.update(fields, evidence_fingerprint=choice["evidence_fingerprint"])
            answers = folder / "filled.csv"
            answers.write_text(cr.csv_text(cr.COLUMNS, [row]), encoding="utf-8", newline="")
            register = context("apply", graph, screen / "questions.json", sources, accepted,
                               prepared / "context.json", answers)
            self.assertEqual(register["current"]["C3@model"]["state"], "partial")
            self.assertEqual(len(register["decisions"]), 1)
            self.assertEqual(len(register["ownership_history"]), 1)
            self.assertEqual(register["decisions"][0]["plant_truth"], "unknown")
            return path, screen, graph, accepted, answers, register
        def assert_readback(folder, expected):
            snapshot = Snapshot(folder / "enriched_graph.json", folder / "context.json")
            question = json.loads((folder / "enriched_graph.json").read_bytes())["questions"][0]
            self.equal_json(snapshot.question("C3@model")["result"], question)
            self.equal_json(snapshot.context_question("C3@model")["result"]["current"], expected["current"]["C3@model"])
            history, offset = [], 0
            while True:
                page = snapshot.decisions("C3@model", limit=1, offset=offset)["result"]
                history += page["decisions"]
                if page["next_offset"] is None: break
                offset = page["next_offset"]
            self.equal_json(history, expected["decisions"])
        def assert_history(current, original):
            self.equal_json(current["decisions"], original["decisions"])
            self.equal_json(current["ownership_history"], original["ownership_history"])
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model = self.case("U00-i04-original")
            path, screen, graph, accepted, answers, original = accept(base / "main", model)
            assert_readback(accepted, original)
            sources = self.fixture("r1/sources.json")
            source_out = base / "source-refresh"
            source_result = context("apply", graph, screen / "questions.json", self.fixture("r2/sources.json"),
                                    source_out, accepted / "context.json")
            self.assertEqual(source_result["current"]["C3@model"]["state"], "unanswered")
            self.assertEqual(source_result["current"]["C3@model"]["answers"][0]["freshness"], "stale")
            assert_history(source_result, original)
            assert_readback(source_out, source_result)
            refused = base / "refused"
            refused.mkdir()
            sentinel = refused / "context.json"
            sentinel.write_bytes(b"do not replace\n")
            error = context("apply", graph, screen / "questions.json", self.fixture("r2/sources.json"), refused,
                            accepted / "context.json", answers, expected=2)
            self.assertIn("evidence_fingerprint", error)
            self.assertEqual(sentinel.read_bytes(), b"do not replace\n")
            with self.assertRaisesRegex(SnapshotInputError, "Invalid selected context"):
                Snapshot(source_out / "enriched_graph.json", accepted / "context.json")
            changed = self.patched(model, self.data("model-qualifier-revision.json")["patch"])
            _, _, revised, _ = self.screen_case(base / "main", changed)
            changed_graph = base / "changed.graph.json"
            save(changed_graph, gx.build(path, questions=screen / "questions.json"))
            changed_out = base / "model-refresh"
            changed_result = context("apply", changed_graph, screen / "questions.json", sources, changed_out, accepted / "context.json")
            self.assertEqual(changed_result["current"]["C3@model"]["state"], "unanswered")
            assert_history(changed_result, original)
            assert_readback(changed_out, changed_result)
            # Status-only requires an already-present review envelope; dictionary addition is not this control.
            for identity in ("FV-04", "FT-04"):
                for envelope in ("ops_review", "verification", "topology_verification"):
                    with self.subTest(identity=identity, envelope=envelope):
                        seed = copy.deepcopy(model)
                        record = next(row for row in seed["unplaced"] if row["tag"] == identity)
                        record[envelope] = self.data("review-envelope.json")
                        folder = base / (identity + "-" + envelope)
                        p, s, g, a, _, old = accept(folder, seed)
                        record[envelope]["status"] = "confirmed"
                        self.screen_case(folder, seed)
                        save(g, gx.build(p, questions=s / "questions.json"))
                        refreshed = folder / "status-refreshed"
                        result = context("apply", g, s / "questions.json", sources, refreshed, a / "context.json")
                        self.assertEqual(result["current"]["C3@model"]["state"], "partial")
                        self.assertEqual(result["current"]["C3@model"]["answers"][0]["freshness"], "current")
                        assert_history(result, old)
                        assert_readback(refreshed, result)
            # Notes remain evidence. This is deliberately not a global stripping of review records.
            seed = copy.deepcopy(model)
            seed["unplaced"][0]["ops_review"] = self.data("review-envelope.json")
            folder = base / "changed-note"
            p, s, g, a, _, old = accept(folder, seed)
            seed["unplaced"][0]["ops_review"]["notes"] += " AUTHORED source caveat changed."
            self.screen_case(folder, seed)
            save(g, gx.build(p, questions=s / "questions.json"))
            result = context("apply", g, s / "questions.json", sources, folder / "refreshed", a / "context.json")
            self.assertEqual(result["current"]["C3@model"]["state"], "unanswered")
            assert_history(result, old)
            # Native top-level status is a literal claim.value, not merely an exported status envelope.
            seed = copy.deepcopy(model)
            seed["unplaced"][0]["status"] = "unverified"
            folder = base / "literal-record-status"
            p, s, g, a, _, old = accept(folder, seed)
            seed["unplaced"][0]["status"] = "confirmed"
            self.screen_case(folder, seed)
            save(g, gx.build(p, questions=s / "questions.json"))
            result = context("apply", g, s / "questions.json", sources, folder / "refreshed", a / "context.json")
            self.assertEqual(result["current"]["C3@model"]["state"], "unanswered")
            assert_history(result, old)


class AlarmBasisRecordReview(unittest.TestCase):
    """Exposed source-policy controls; not plant performance or alarm authority."""
    packet = EX / "alarm-basis"

    def _run_model(self, model, folder):
        out = folder / "screen"
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = qe.main(["--model", str(model), "--out", str(out)])
        self.assertEqual(rc, 0, stdout.getvalue() + stderr.getvalue())
        return (json.loads((out / "questions.json").read_bytes().decode("utf-8")),
                (out / "screen.md").read_bytes().decode("utf-8"), out)

    @staticmethod
    def _span(text):
        fence = re.match(r"`+", text).group()
        end = text.index(fence, len(fence))
        return json.loads(text[len(fence):end]), text[end + len(fence):]

    def _readable_pairs(self, markdown):
        result = []
        prefix = "- Supplied candidate field: "
        for line in markdown.splitlines():
            if not line.startswith(prefix):
                continue
            value, rest = self._span(line[len(prefix):])
            self.assertTrue(rest.startswith(" ("))
            field, rest = self._span(rest[2:])
            self.assertEqual(rest, ")")
            result.append((value, field))
        return result

    def _rows(self, question):
        result = {}
        for evidence in question["evidence"]:
            if evidence.get("role") != "supplied candidate field":
                continue
            name = evidence["field"].rsplit(".facts.", 1)[1]
            tail = evidence["text"].split(" " + name + " = ", 1)[1]
            value, end = json.JSONDecoder().raw_decode(tail)
            state = re.match(r"; (present|blank);", tail[end:]).group(1)
            key = (evidence["id"], name)
            self.assertNotIn(key, result)
            result[key] = (value, state, evidence)
        return result

    def test_committed_cases_reproduce_and_keep_typed_readable_records(self):
        cases = json.loads((self.packet / "expected/cases.json").read_bytes())["cases"]
        vectors = {c["case"]: c["vectors"] for c in json.loads(
            (self.packet / "expected/input-vectors.json").read_bytes())["cases"]}
        checked = 0
        for case in cases:
            with self.subTest(case=case["case"]), tempfile.TemporaryDirectory() as tmp:
                doc, markdown, out = self._run_model(self.packet / case["model"], Path(tmp))
                for name in ("questions.json", "screen.md"):
                    self.assertEqual((out / name).read_bytes(),
                                     (self.packet / case["expected_output_folder"] / name).read_bytes())
                questions = [q for q in doc["questions"] if q["question_id"] == "C8"]
                self.assertEqual([q["id"] for q in questions], case["expected_C8_ids"])
                self.assertEqual([a["id"] for q in questions for a in q["assets"]],
                                 case["expected_C8_assets"])
                for question in questions:
                    self.assertEqual(question["status"], "asked")
                    open_requests = [r for r in question["data_requests"]
                                     if r["state"] in {"not_on_drawing", "blank_on_drawing"}]
                    self.assertGreaterEqual(len(open_requests), case["minimum_open_review_requests"])
                if not questions:
                    self.assertEqual(case["minimum_open_review_requests"], 0)
                    self.assertEqual(vectors[case["case"]], [])
                    continue  # Quiet coverage is not a shown-evidence pass.
                rows = self._rows(questions[0])
                readable = self._readable_pairs(markdown)
                for vector in vectors[case["case"]]:
                    key = (vector["asset_id"], vector["name"])
                    self.assertIn(key, rows, "missing supplied alarm record: " + repr(key))
                    value, state, evidence = rows[key]
                    self.assertIs(type(value), type(vector["value"]))
                    self.assertEqual(json.dumps(value, ensure_ascii=True, sort_keys=True),
                                     json.dumps(vector["value"], ensure_ascii=True, sort_keys=True))
                    self.assertEqual(state, vector["state"])
                    self.assertEqual(evidence["field"], vector["field"])
                    self.assertIn((evidence["text"], evidence["field"]), readable)
                    checked += 1
        self.assertEqual(checked, sum(c["active_literal_rows"] for c in cases))

    def test_shared_and_foreign_scopes_remain_qualified_review_requests(self):
        def current(case):
            doc = json.loads((self.packet / "expected/after" / case / "questions.json").read_bytes())
            return next(q for q in doc["questions"] if q["question_id"] == "C8")

        shared = current("C8-S01-shared-operator-record")
        foreign = current("C8-S02-repeated-label-foreign-scopes")
        for question in (shared, foreign):
            self.assertEqual(question["status"], "asked")
            self.assertTrue(question["data_requests"])
            items = [r["item"] for r in question["data_requests"]]
            self.assertEqual(items, list(dict.fromkeys(items)))
        rows = self._rows(shared)
        ids = [a["id"] for a in shared["assets"]]
        for aid in ids:
            for name in ("record_reference", "record_subjects", "record_units", "plant_truth"):
                self.assertIn((aid, name), rows, "missing shared-scope record: " + repr((aid, name)))
        self.assertEqual(len({rows[(aid, "record_reference")][0] for aid in ids}), 1)
        for aid in ids:
            self.assertEqual(rows[(aid, "record_subjects")][0], ids)
            self.assertEqual(rows[(aid, "record_units")][0], ["U-A", "U-B"])
            self.assertEqual(rows[(aid, "plant_truth")][:2], ("unknown", "blank"))
        rows = self._rows(foreign)
        ids = [a["id"] for a in foreign["assets"]]
        for aid in ids:
            for name in ("console_id", "operator_role", "site_namespace", "record_site_namespace",
                         "source_namespace", "record_source_namespace"):
                self.assertIn((aid, name), rows, "missing foreign-scope record: " + repr((aid, name)))
        self.assertEqual(len({rows[(aid, "console_id")][0] for aid in ids}), 1)
        self.assertEqual(len({rows[(aid, "operator_role")][0] for aid in ids}), 1)
        self.assertEqual(len({rows[(aid, "site_namespace")][0] for aid in ids}), 2)
        for aid in ids:
            self.assertNotEqual(rows[(aid, "site_namespace")][0],
                                rows[(aid, "record_site_namespace")][0])
            self.assertNotEqual(rows[(aid, "source_namespace")][0],
                                rows[(aid, "record_source_namespace")][0])

    def test_approval_and_zero_claims_do_not_complete_the_review(self):
        model = json.loads((self.packet / "models/C8-S01-shared-operator-record.json").read_bytes())
        for instrument in model["instruments"]:
            instrument["facts"].update(underlying_claim_verified=True,
                                       record_review_status="approved",
                                       normal_presentations_per_10min=0)
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / "claims.json"
            source.write_text(json.dumps(model), encoding="utf-8", newline="\n")
            doc, _, _ = self._run_model(source, folder)
            question = next(q for q in doc["questions"] if q["question_id"] == "C8")
            self.assertEqual(question["status"], "asked")
            self.assertTrue(question["data_requests"])
            rows = self._rows(question)
            for aid in ("PAH-101", "LAHH-201"):
                for name in ("underlying_claim_verified", "normal_presentations_per_10min", "plant_truth"):
                    self.assertIn((aid, name), rows, "missing supplied claim: " + repr((aid, name)))
                self.assertIs(rows[(aid, "underlying_claim_verified")][0], True)
                self.assertIs(type(rows[(aid, "normal_presentations_per_10min")][0]), int)
                self.assertEqual(rows[(aid, "normal_presentations_per_10min")][0], 0)
                self.assertEqual(rows[(aid, "plant_truth")][:2], ("unknown", "blank"))


class CompressorRecycleBasisRecordReview(unittest.TestCase):
    """Finite collection controls, not machine/protection acceptance."""
    packet = EX / "compressor-recycle-basis"
    _run_model = AlarmBasisRecordReview._run_model
    _span = staticmethod(AlarmBasisRecordReview._span)
    _readable_pairs = AlarmBasisRecordReview._readable_pairs
    _rows = AlarmBasisRecordReview._rows

    def test_cases_reproduce_and_preserve_records_without_settling_review(self):
        cases = json.loads((self.packet / "expected/cases.json").read_bytes())["cases"]
        vectors = json.loads((self.packet / "expected/input-vectors.json").read_bytes())["vectors"]
        current, checked, findings = {}, 0, 0
        for case in cases:
            with self.subTest(case=case["case"]), tempfile.TemporaryDirectory() as tmp:
                doc, markdown, out = self._run_model(self.packet / case["model"], Path(tmp))
                for name in ("questions.json", "screen.md"):
                    self.assertEqual((out / name).read_bytes(),
                        (self.packet / case["expected_output_folder"] / name).read_bytes())
                questions = [q for q in doc["questions"] if q["question_id"] == "E6"]
                self.assertEqual([q["id"] for q in questions], case["expected_E6_ids"])
                self.assertEqual([a["id"] for q in questions for a in q["assets"]], case["expected_E6_assets"])
                before = json.loads((self.packet / case["original_output_folder"] / "questions.json").read_bytes())
                self.assertEqual(
                    json.dumps([q for q in doc["questions"] if q["question_id"] != "E6"],
                               sort_keys=True, ensure_ascii=True),
                    json.dumps([q for q in before["questions"] if q["question_id"] != "E6"],
                               sort_keys=True, ensure_ascii=True))
                readable, rows = self._readable_pairs(markdown), {}
                for question in questions:
                    self.assertEqual(question["status"], "asked")
                    self.assertGreaterEqual(sum(r["state"] in {"not_on_drawing", "blank_on_drawing"}
                        for r in question["data_requests"]), case["minimum_open_review_requests"])
                    findings += 1
                    for key, value in self._rows(question).items():
                        self.assertNotIn(key, rows)
                        rows[key] = value
                for vector in [v for v in vectors if v["case_id"] == case["case"]]:
                    key = (vector["subject_id"], vector["field"])
                    if not vector["present"] or not vector["expected_E6_field_carrier"]:
                        self.assertNotIn(key, rows)
                        continue
                    self.assertIn(key, rows, "missing whole supplied record: " + repr(key))
                    value, state, evidence = rows[key]
                    self.assertIs(type(value), type(vector["value"]))
                    self.assertEqual(json.dumps(value, ensure_ascii=True, sort_keys=True),
                                     json.dumps(vector["value"], ensure_ascii=True, sort_keys=True))
                    self.assertEqual(state, vector["field_state"])
                    self.assertEqual(evidence["field"], vector["input_location"])
                    self.assertIn((evidence["text"], evidence["field"]), readable)
                    checked += 1
                if not questions:
                    self.assertEqual(case["minimum_open_review_requests"], 0)
                current[case["case"]] = rows
        self.assertEqual((checked, findings), (24, 18))
        for suffix, covers in (("A", ["K-A", "K-B"]), ("B", ["K-A"])):
            key = "E6-06-power-and-sibling-coverage-" + suffix
            self.assertIn(key, current, "missing completed shared-scope case: " + key)
            rows = current[key]
            for aid in ("K-A", "K-B"):
                self.assertIn((aid, "control_records"), rows)
            left, right = (rows[(aid, "control_records")][0] for aid in ("K-A", "K-B"))
            self.assertEqual(left, right)  # References to one supplied claim, not two reports.
            self.assertEqual(left[0]["covers"], covers)
            self.assertIs(left[0]["approval"], False)
            self.assertIs(type(left[0]["value"]), int)
            self.assertEqual(left[0]["value"], 0)


if __name__ == "__main__":
    unittest.main()
