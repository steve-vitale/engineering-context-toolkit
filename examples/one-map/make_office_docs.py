"""Write the two fictional Office documents of the one-map Office variant (inputs/documents-office.json): a Word
start-up procedure and an Excel PM plan for Unit 200 that write tags in other styles (P 101, TT2205, FP01, ft-2203,
e-205, FV 2203, LV2204). Generated rather than committed, so the repository holds no binary documents; the bytes are
identical on every run and every OS (the same stored-zip writer as examples/document-text/make_samples.py, which
makes them complete packages Office programs open).
Stdlib only.

    python examples/one-map/make_office_docs.py examples/one-map/inputs/docs/office
"""
import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "document_text_samples", Path(__file__).resolve().parent.parent / "document-text" / "make_samples.py")
samples = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(samples)


def startup_procedure(path):
    body = (samples.para("Purpose: start feed pump P 101 after a seal change.")
            + samples.para("1. Confirm cooler outlet temperature on TT2205 is below 40 C.")
            + samples.para("2. Older check sheets call the pump FP01; it is the same pump.")
            + "<w:tbl>" + samples.row("Tag", "Check before start")
            + samples.row("ft-2203", "flow reading at zero")
            + samples.row("PSV-204", "inlet valve car-sealed open") + "</w:tbl>")
    samples.zip_parts(path, {
        "word/document.xml": f'<?xml version="1.0"?><w:document {samples.W} {samples.RR}><w:body>{body}'
                             '<w:sectPr><w:headerReference w:type="default" r:id="rIdH1"/></w:sectPr>'
                             "</w:body></w:document>",
        "word/_rels/document.xml.rels": samples.rels(("rIdH1", "header", "header1.xml")),
        "word/header1.xml": f'<?xml version="1.0"?><w:hdr {samples.W}>'
                            + samples.para("SU-200-03 rev A, Unit 200 feed pump start-up (fictional)") + "</w:hdr>",
    })


def pm_plan(path):
    strings = ["Equipment", "Task", "Interval (weeks)", "e-205", "Clean cooler tubes", "FV 2203",
               "Stroke test", "LV2204", "Stroke test and check positioner"]
    sst = f"<sst {samples.SS}>" + "".join(f"<si><t>{s}</t></si>" for s in strings) + "</sst>"
    rows = {1: [("A", 0), ("B", 1), ("C", 2)], 2: [("A", 3), ("B", 4)], 3: [("A", 5), ("B", 6)],
            4: [("A", 7), ("B", 8)]}
    weeks = {2: 52, 3: 26, 4: 26}
    data = "".join(f'<row r="{r}">' + "".join(f'<c r="{c}{r}" t="s"><v>{s}</v></c>' for c, s in cells)
                   + (f'<c r="C{r}"><v>{weeks[r]}</v></c>' if r in weeks else "") + "</row>"
                   for r, cells in sorted(rows.items()))
    samples.zip_parts(path, {
        "xl/workbook.xml": f'<workbook {samples.SS} {samples.RR}><sheets><sheet name="PM plan" sheetId="1" '
                           'r:id="rId1"/></sheets></workbook>',
        "xl/_rels/workbook.xml.rels": samples.rels(("rId1", "worksheet", "worksheets/sheet1.xml"),
                                                   ("rIdS", "sharedStrings", "sharedStrings.xml")),
        "xl/sharedStrings.xml": sst,
        "xl/worksheets/sheet1.xml": f"<worksheet {samples.SS}><sheetData>{data}</sheetData></worksheet>",
    })


def build(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    startup_procedure(folder / "su-200-03-revA.docx")
    pm_plan(folder / "pm-200-plan.xlsx")
    return folder


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(f"wrote {build(sys.argv[1]).as_posix()}")
