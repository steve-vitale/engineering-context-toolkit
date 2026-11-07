"""DXF edit/readback, foreign attributes/geometry, stale plans and destructive-return controls."""
import copy
import json
import importlib.util
import tempfile
import unittest
from pathlib import Path

import ezdxf
import cad_handoff as ch


def drawing(path):
    doc = ezdxf.new("R2000")
    doc.layers.new("PROCESS", dxfattribs={"color": 3})
    block = doc.blocks.new("VALVE")
    block.add_circle((0, 0), 2)
    for i, key in enumerate(("ICT_ID", "TAG", "MODEL", "SERIAL", "SIZE", "VENDOR_PRIVATE")):
        block.add_attdef(key, (3, -i), height=0.7)
    ref = doc.modelspace().add_blockref("VALVE", (10, 20), dxfattribs={"layer": "PROCESS"})
    ref.add_auto_attribs(dict(ICT_ID="fixture/valve-01", TAG="FV-101", MODEL="A", SERIAL="123", SIZE="DN50",
                             VENDOR_PRIVATE="retain me"))
    line = doc.modelspace().add_line((0, 20), (8, 20), dxfattribs={"layer": "PROCESS"})
    doc.appids.new("VENDOR_TEST")
    line.set_xdata("VENDOR_TEST", [(1000, "do not flatten"), (1040, 1.25)])
    doc.saveas(path)


class Handoff(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "original.dxf"
        drawing(self.source)
        self.before = ch.snapshot(self.source)
        self.plan = {"schema": "cad-edit-plan-1", "source_sha256": ch.digest(self.source), "changes": [
            {"id": "fixture/valve-01", "attribute": "SIZE", "before": "DN50", "after": "DN65",
             "reason": "Fictional reviewed replacement note; not installed-state evidence"}]}

    def test_edit_round_trip_retains_source_foreign_data_and_context_identity(self):
        source_bytes = self.source.read_bytes()
        out = self.root / "proposal"
        report = ch.apply(self.source, self.plan, out)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(self.source.read_bytes(), source_bytes)
        self.assertEqual((out / "source.dxf").read_bytes(), source_bytes)
        after = ch.snapshot(out / "candidate.dxf")
        self.assertEqual(after["assets"][0]["id"], "fixture/valve-01")
        self.assertEqual(after["assets"][0]["attributes"]["VENDOR_PRIVATE"], "retain me")
        self.assertEqual(after["assets"][0]["attributes"]["SIZE"], "DN65")
        self.assertEqual(ch.compare(self.before, after, self.plan)["unexpected"], [])
        self.assertTrue(ch.compare(self.before, after)["unexpected"])
        proposed = json.loads((out / "candidate-context/cad_context.json").read_text())
        self.assertEqual(proposed["nodes"][0]["attributes"]["SIZE"], "DN65")
        self.assertEqual(proposed["relationships"], [])

    def test_stale_source_before_value_duplicate_and_identity_edits_refused(self):
        for mutate in (lambda p: p.update(source_sha256="0" * 64),
                       lambda p: p["changes"][0].update(before="DN40"),
                       lambda p: p["changes"].append(p["changes"][0]),
                       lambda p: p["changes"][0].update(attribute="ICT_ID")):
            with self.subTest(mutate=mutate):
                plan = copy.deepcopy(self.plan)
                mutate(plan)
                with self.assertRaises(ch.InputError):
                    ch.apply(self.source, plan, self.root / "refused")
                self.assertFalse((self.root / "refused").exists())

    def test_geometry_layer_foreign_field_and_xdata_loss_are_detected(self):
        mutations = [lambda d: setattr(d.modelspace().query("LINE")[0].dxf, "end", (9, 20, 0)),
                     lambda d: setattr(d.layers.get("PROCESS").dxf, "color", 1),
                     lambda d: setattr(d.modelspace().query("INSERT")[0].get_attrib("VENDOR_PRIVATE").dxf, "text", "lost"),
                     lambda d: d.modelspace().query("LINE")[0].discard_xdata("VENDOR_TEST")]
        for i, mutate in enumerate(mutations):
            doc = ch.load(self.source)
            mutate(doc)
            returned = self.root / f"wrong-{i}.dxf"
            doc.saveas(returned)
            with self.subTest(i=i):
                self.assertTrue(ch.compare(self.before, ch.snapshot(returned))["unexpected"])

    def test_empty_flattened_and_duplicate_ids_are_not_accepted_as_assets(self):
        for i in range(3):
            doc = ch.load(self.source)
            ref = doc.modelspace().query("INSERT")[0]
            if i == 0:
                ref.delete_attrib("ICT_ID")
            elif i == 1:
                doc.modelspace().delete_entity(ref)
            else:
                doc.modelspace().add_entity(ref.copy())
            path = self.root / f"invalid-{i}.dxf"
            doc.saveas(path)
            with self.subTest(i=i), self.assertRaises(ch.InputError):
                ch.snapshot(path)

    def test_existing_output_is_not_overwritten(self):
        ch.apply(self.source, self.plan, self.root / "proposal")
        with self.assertRaises(ch.InputError):
            ch.apply(self.source, self.plan, self.root / "proposal")

    def test_explicit_map_projection_retains_identity_and_rejects_a_guessed_match(self):
        spec = importlib.util.spec_from_file_location("cad_projection", Path(__file__).resolve().parents[1] /
                                                    "examples/cad-handoff/project_to_map.py")
        projection = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(projection)
        packet = self.root / "packet"
        ch.apply(self.source, self.plan, packet)
        mapping = {"site": "S", "plant": "P", "unit": "U", "assets": [
            {"id": "fixture/valve-01", "tag": "FV-101", "section": "instruments"}]}
        projection.project(packet / "candidate-context", mapping, self.root / "projection")
        sheet = json.loads((self.root / "projection/sheet.json").read_text())
        self.assertEqual(sheet["instruments"][0]["attributes"]["cad_size"], "DN65")
        self.assertEqual(sheet["lines"], [])
        mapping["assets"][0]["tag"] = "FV-102"
        with self.assertRaises(ValueError):
            projection.project(packet / "candidate-context", mapping, self.root / "wrong-match")
        self.assertFalse((self.root / "wrong-match").exists())


if __name__ == "__main__":
    unittest.main()
