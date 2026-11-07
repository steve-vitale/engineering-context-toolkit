"""Author a small fictional DXF attribute fixture; not a complete or accepted P&ID."""
import json
import sys
from pathlib import Path

import ezdxf

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import cad_handoff as cad


def main():
    folder = Path(__file__).resolve().parent / "source"
    folder.mkdir(exist_ok=True)
    path = folder / "valve.dxf"
    if path.exists():
        raise SystemExit("Fixture already exists; retain it rather than replacing its source identity")
    # Fixed writer metadata makes this authored fixture reproducible, not the production editor.
    ezdxf.options.write_fixed_meta_data_for_testing = True
    doc = ezdxf.new("R2000")
    doc.layers.new("PROCESS", dxfattribs={"color": 3})
    block = doc.blocks.new("DRAFT_VALVE")
    block.add_lwpolyline([(-4, -3), (4, 3), (4, -3), (-4, 3), (-4, -3)])
    values = {"ICT_ID": "S1/P1/PAST1/FDV-2210", "TAG": "FDV-2210", "MODEL": "SRC-2",
              "SERIAL": "UNKNOWN", "SIZE": "DN50", "VENDOR_NOTE": "retain this unfamiliar attribute"}
    for i, key in enumerate(values):
        block.add_attdef(key, (-4, -6 - 3 * i), height=1.2)
    ref = doc.modelspace().add_blockref("DRAFT_VALVE", (30, 40), dxfattribs={"layer": "PROCESS"})
    ref.add_auto_attribs(values)
    doc.modelspace().add_line((5, 40), (26, 40), dxfattribs={"layer": "PROCESS"})
    doc.modelspace().add_line((34, 40), (60, 40), dxfattribs={"layer": "PROCESS"})
    doc.modelspace().add_text("FICTIONAL ATTRIBUTE EXERCISE - NOT AN ACCEPTED P&ID",
                             dxfattribs={"insert": (5, 60), "height": 1.5})
    doc.saveas(path)
    plan = {"schema": "cad-edit-plan-1", "source_sha256": cad.digest(path), "changes": [
        {"id": values["ICT_ID"], "attribute": key, "before": values[key], "after": after,
         "reason": "Fictional WO-60311 observation in examples/one-map; proposed CAD edit, "
                   "not an accepted engineering change"}
        for key, after in (("MODEL", "SRC-3"), ("SERIAL", "AV-88412"), ("SIZE", "DN65"))]}
    cad.write_json(folder / "edit-plan.json", plan)
    cad.write_json(folder / "PROVENANCE.json", {
        "kind": "authored fictional fixture", "license": "repository license", "source_sha256": cad.digest(path),
        "stable_id": values["ICT_ID"], "basis": "existing fictional pasteurizer replacement scenario",
        "note": "Geometry, baseline CAD model and UNKNOWN serial were authored for this exchange exercise; "
                "not extracted from a CAD project, photograph or plant. No connectivity is inferred.",
        "writer": "ezdxf " + ezdxf.__version__, "script": "examples/cad-handoff/make_fixture.py"})
    print(path)


if __name__ == "__main__":
    main()
