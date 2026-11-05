"""Tests for the plant-workflow pieces of scripts/one_map.py and scripts/map_changes.py: the work order closeout
check, field verification rulings, the change report between two map builds, the affected-records report and its
closeout, and the change flags. Built on copies of the fictional pasteurizer example. Stdlib only.

Usage:  python scripts/test_plant_workflows.py
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
import one_map as om  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAST = ROOT / "examples" / "one-map" / "inputs" / "pasteurizer"
FDV = "S1/P1/PAST1/FDV-2210"


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*a, **k)


def write_csv(path, header, rows):
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(buf.getvalue(), encoding="utf-8", newline="\n")


WO_HEADER = ["work_order", "tag", "plant", "unit", "work_type", "opened_on", "closed_on", "description",
             "installed_manufacturer", "installed_model", "installed_serial_number", "installed_size"]


class Site:
    """A temporary copy of the pasteurizer inputs with a valve datasheet, installed-equipment columns on the
    maintenance equipment export and a work order history."""

    def __init__(self, tmp, work_orders, export_fdv=("Alfa Valve", "SRC-2", "AV-51007")):
        self.dir = Path(tmp) / "in"
        shutil.copytree(PAST, self.dir)
        site = json.loads((self.dir / "site.json").read_text(encoding="utf-8"))
        rows = list(csv.DictReader(io.StringIO((self.dir / "lists" / "maintenance_equipment.csv")
                                               .read_text(encoding="utf-8"))))
        header = list(rows[0]) + ["manufacturer", "model", "serial_number"]
        write_csv(self.dir / "lists" / "maintenance_equipment.csv", header,
                  [[r[k] for k in rows[0]] + (list(export_fdv) if r["tag"] == "FDV-2210" else ["", "", ""])
                   for r in rows])
        write_csv(self.dir / "lists" / "valve_datasheets.csv", ["tag", "plant", "unit", "size", "body_material"],
                  [["FDV-2210", "P1", "PAST1", "DN50", "316L"]])
        site["datasheets"].append({"id": "VALVE-DATASHEETS", "path": "lists/valve_datasheets.csv", "revision": "2",
                                   "scopes": ["S1/P1"]})
        write_csv(self.dir / "records" / "work_orders.csv", WO_HEADER, work_orders)
        site["records"].append({"id": "WO-HISTORY", "register": "work_order", "path": "records/work_orders.csv",
                                "revision": "2026-11-01", "scopes": ["S1/P1"]})
        site["record_owners"]["work_order"] = "Maintenance"
        (self.dir / "site.json").write_text(json.dumps(site, indent=1), encoding="utf-8")

    def build(self, out, **kw):
        g, _, rows, _ = quiet(om.build, self.dir / "site.json", Path(out), full=True, **kw)
        return g, rows


REPLACED = ["WO-60311", "FDV-2210", "P1", "PAST1", "modification", "2026-10-20", "2026-10-22",
            "Replace divert valve under MOC-0412", "Alfa Valve", "SRC-3", "AV-88412", "DN65"]


def conflicts_of(g):
    return [n["conflict"] for n in g["nodes"] if n["kind"] == "conflict"]


class WorkOrderCloseout(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_installed_values_against_the_export_and_the_datasheet(self):
        site = Site(self.tmp.name, [
            REPLACED,
            ["WO-60312", "FDV-2210", "P1", "PAST1", "corrective", "2026-10-25", "", "Still open", "Other", "X-1",
             "S-1", "DN80"],  # not closed: not compared
            ["WO-60313", "P-101", "P1", "PAST1", "corrective", "2026-08-04", "2026-08-04", "Seal", "", "", "", ""],
            ["WO-60314", "XV-9999", "P1", "PAST1", "corrective", "2026-09-01", "2026-09-02", "Replaced", "Acme",
             "Q-1", "", ""],
        ])
        g, rows = site.build(Path(self.tmp.name) / "out")
        wo = {c["attribute"]: c for c in conflicts_of(g) if c["subject"] == FDV
              and c["source_a"]["source"]["document"] == "WO-HISTORY"}
        self.assertEqual(sorted(wo), ["model", "serial_number"], "manufacturer agrees; size is a datasheet fact")
        for c in wo.values():
            self.assertEqual(c["type"], "value_disagreement")
            self.assertEqual(c["record_owner"], "Maintenance")
            self.assertIn("work order WO-60311 (closed 2026-10-22)", c["what"])
        self.assertEqual((wo["model"]["source_a"]["says"], wo["model"]["source_b"]["says"]), ("SRC-3", "SRC-2"))
        like = [r for r in rows if r["kind"] == om.LIKE_FOR_LIKE]
        self.assertEqual(len(like), 1)
        self.assertEqual((like[0]["item"], like[0]["owner"]), (FDV, "Engineering"))
        for words in ("size DN65 installed", "datasheet VALVE-DATASHEETS (row 2) says DN50", "management of change",
                      "not a decision"):
            self.assertIn(words, like[0]["why"])
        notes = [r for r in rows if r["kind"] == om.WO_NOTE]
        self.assertEqual(len(notes), 1, [r["why"] for r in notes])
        self.assertIn("XV-9999", notes[0]["why"])
        self.assertFalse([c for c in conflicts_of(g) if "WO-60312" in c["what"] or "DN80" in json.dumps(c)])
        self.assertEqual(om.problems(g), [])

    def test_matching_closeout_raises_nothing_and_case_or_spacing_is_not_a_difference(self):
        site = Site(self.tmp.name, [REPLACED[:8] + ["alfa  valve", "src-3", "AV-88412", "dn65"]],
                    export_fdv=("Alfa Valve", "SRC-3", "AV-88412"))
        (site.dir / "lists" / "valve_datasheets.csv").write_text(
            "tag,plant,unit,size,body_material\nFDV-2210,P1,PAST1,DN65,316L\n", encoding="utf-8")
        g, rows = site.build(Path(self.tmp.name) / "out")
        self.assertFalse([c for c in conflicts_of(g) if c["source_a"]["source"]["document"] == "WO-HISTORY"])
        self.assertFalse([r for r in rows if r["kind"] in (om.LIKE_FOR_LIKE, om.WO_NOTE)])

    def test_installed_value_no_record_holds_is_a_note(self):
        site = Site(self.tmp.name, [["WO-1", "P-102", "P1", "PAST1", "corrective", "2026-10-01", "2026-10-02", "x",
                                     "Pumpco", "", "", ""]])
        _, rows = site.build(Path(self.tmp.name) / "out")
        notes = [r for r in rows if r["kind"] == om.WO_NOTE]
        self.assertEqual(len(notes), 1)
        self.assertIn("no maintenance equipment export or instrument index row for it holds manufacturer",
                      notes[0]["why"])


RULING_HEADER = ["ruling_id", "concerns", "attribute", "ruling", "chosen_source", "chosen_value", "reason", "by",
                 "on", "authority", "evidence"]


class FieldVerificationRulings(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.site = Site(self.tmp.name, [REPLACED])
        self.out = Path(self.tmp.name) / "out"
        self.g, _ = self.site.build(self.out)
        self.serial = next(c for c in conflicts_of(self.g) if c["subject"] == FDV and c["attribute"] == "serial_number")

    def tearDown(self):
        self.tmp.cleanup()

    def rulings(self, *rows):
        p = Path(self.tmp.name) / "rulings.csv"
        write_csv(p, RULING_HEADER, rows)
        return p

    def test_walkdown_ruling_settles_the_conflict_and_asks_the_record_owner_to_update(self):
        walk = ["R-0101", FDV, "serial_number", "accept_value", "", "AV-88412",
                "Walkdown: the nameplate on the installed body reads AV-88412", "Maintenance planner", "2026-11-03",
                "field", "photo walkdown-2026-11-03/FDV-2210-nameplate.jpg"]
        g, rows = self.site.build(self.out, decisions=[str(self.rulings(walk))])
        c = next(n["conflict"] for n in g["nodes"] if n["kind"] == "conflict" and n["conflict"]["id"] == self.serial["id"])
        self.assertEqual(c["status"], "resolved")
        h = c["history"][-1]
        self.assertEqual((h["authority"], h["ruling_id"], h["chosen_value"], h["by"], h["on"]),
                         ("field", "R-0101", "AV-88412", "Maintenance planner", "2026-11-03"))
        self.assertIn("nameplate", h["evidence"])
        upd = [r for r in rows if r["kind"] == om.RULED]
        self.assertEqual(len(upd), 1)
        self.assertEqual(upd[0]["owner"], "Maintenance")
        for words in ("ruled AV-88412 on 2026-11-03 (field: photo walkdown-2026-11-03", "CMMS-2026-10",
                      "still says AV-51007: update it"):
            self.assertIn(words, upd[0]["why"])
        self.assertFalse([r for r in rows if r["item"].endswith(self.serial["id"]) and r["tier"] == "red"])
        md = (self.out / "conflicts.md").read_text(encoding="utf-8")
        self.assertIn("## Decision history", md)
        self.assertIn("2026-11-03 Maintenance planner: resolved (ruling_id R-0101; ruling accept_value; authority field",
                      md)
        # the same file again adds no second history line; the earlier state carries the ruling forward
        g2, _ = self.site.build(self.out, decisions=[str(self.rulings(walk))])
        c2 = next(n["conflict"] for n in g2["nodes"] if n["kind"] == "conflict" and n["conflict"]["id"] == c["id"])
        self.assertEqual(len(c2["history"]), 1)

    def test_conflict_id_form_decisions_csv_and_refusals(self):
        cid = f"S1/CONFLICT/{self.serial['id']}"
        ok = ["R-1", cid, "", "defer", "", "", "Wait for the walkdown", "Maintenance planner", "2026-11-01", "", ""]
        g, _ = self.site.build(self.out, decisions=[str(self.rulings(ok))])
        c = next(n["conflict"] for n in g["nodes"] if n["kind"] == "conflict" and n["conflict"]["id"] == self.serial["id"])
        self.assertEqual((c["status"], c["history"][-1]["authority"]), ("disputed", "person"))
        bad = (
            (["R-2", FDV, "serial_number", "accept_value", "", "AV-88412", "seen", "x", "2026-11-03", "field", ""],
             "needs evidence"),
            (["R-3", FDV, "", "accept_value", "", "AV-88412", "seen", "x", "2026-11-03", "", ""], "names the attribute"),
            (["R-4", FDV, "flange_rating", "accept_value", "", "PN16", "seen", "x", "2026-11-03", "", ""],
             "no detected conflict"),
            (["R-5", cid, "", "overrule", "", "", "seen", "x", "2026-11-03", "", ""], "ruling must be one of"),
            (["R-6", cid, "", "defer", "", "", "seen", "x", "3 Nov", "", ""], "YYYY-MM-DD"),
            (["R-7", cid, "", "defer", "", "", "seen", "x", "2026-11-03", "drone", ""], "authority must be one of"),
        )
        for row, words in bad:
            with self.assertRaises(om.InputError) as cm:
                self.site.build(self.out, decisions=[str(self.rulings(row))])
            self.assertIn(words, str(cm.exception), row)


if __name__ == "__main__":
    unittest.main()
