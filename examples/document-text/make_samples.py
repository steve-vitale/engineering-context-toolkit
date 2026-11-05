"""Build the fictional sample documents read in docs/DOCUMENT_TEXT.md: a Word procedure, an Excel PM plan, a
PowerPoint PHA review, an HTML CAPA, a work-order export (CSV) and a legacy .doc placeholder. Generated rather than
committed, so the repository holds no binary documents; the files are byte-identical on every run (stored zip
entries with a fixed timestamp). Stdlib only.

    python examples/document-text/make_samples.py samples      # writes samples/ (relative to the current folder)
"""
import sys
import zipfile
from pathlib import Path

STAMP = (2026, 11, 4, 0, 0, 0)
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
SS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
RR = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
PP = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
AA = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"


def zip_parts(path, parts):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as z:
        for name, text in parts.items():
            info = zipfile.ZipInfo(name, STAMP)
            info.create_system = 0  # the default depends on the OS; pin it so the bytes match everywhere
            z.writestr(info, text.encode("utf-8"))


def rels(*items):
    body = "".join(f'<Relationship Id="{i}" Type="{REL}{t}" Target="{target}"/>' for i, t, target in items)
    return ('<?xml version="1.0" encoding="UTF-8"?><Relationships '
            f'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{body}</Relationships>')


def para(text):
    return f'<w:p><w:r><w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def row(*cells):
    return "<w:tr>" + "".join(f"<w:tc>{para(c)}</w:tc>" for c in cells) + "</w:tr>"


def procedure(path):
    body = (para("Purpose: isolate feed pump P-101 for seal replacement.")
            + para("1. Confirm the work order and the permit are signed.")
            + para("2. Stop P-101 from the control room and close suction valve HV-101A.")
            + "<w:tbl>" + row("Tag", "Check before work", "Expected")
            + row("TT-2207", "Feed temperature", "below 40 C")
            + row("FDV-2210", "Flame detector vent closed", "closed") + "</w:tbl>"
            + para("3. Apply locks at MCC bucket 4B and record them on the permit."))
    zip_parts(path, {
        "[Content_Types].xml": "<Types/>",
        "word/document.xml": f'<?xml version="1.0"?><w:document {W}><w:body>{body}</w:body></w:document>',
        "word/header1.xml": f'<?xml version="1.0"?><w:hdr {W}>'
                            + para("SOP-104 rev C | Area 2 feed system (P-101, TT-2207)") + "</w:hdr>",
    })


def pm_plan(path):
    strings = ["Equipment", "Task", "Interval", "P-101", "Replace mechanical seal", "TT-2207",
               "Calibrate transmitter", "FDV-2210", "Function test"]
    sst = f"<sst {SS}>" + "".join(f"<si><t>{s}</t></si>" for s in strings) + "</sst>"
    cells = [(1, "A", 0), (1, "B", 1), (1, "C", 2), (5, "A", 3), (5, "B", 4), (7, "B", 5), (7, "C", 6),
             (9, "B", 7), (9, "C", 8)]
    rows = {}
    for r, c, s in cells:
        rows.setdefault(r, []).append(f'<c r="{c}{r}" t="s"><v>{s}</v></c>')
    rows[5].append('<c r="D5"><v>12</v></c>')
    data = "".join(f'<row r="{r}">{"".join(v)}</row>' for r, v in sorted(rows.items()))
    zip_parts(path, {
        "xl/workbook.xml": f'<workbook {SS} {RR}><sheets><sheet name="PM plan" sheetId="1" r:id="rId1"/>'
                           "</sheets></workbook>",
        "xl/_rels/workbook.xml.rels": rels(("rId1", "worksheet", "worksheets/sheet1.xml")),
        "xl/sharedStrings.xml": sst,
        "xl/worksheets/sheet1.xml": f"<worksheet {SS}><sheetData>{data}</sheetData></worksheet>",
    })


def pha_review(path):
    def slide(*paras):
        body = "".join(f"<a:p><a:r><a:t>{p}</a:t></a:r></a:p>" for p in paras)
        return (f"<p:sld {PP} {AA}><p:cSld><p:spTree><p:sp><p:txBody>{body}</p:txBody></p:sp></p:spTree>"
                "</p:cSld></p:sld>")
    zip_parts(path, {
        "ppt/presentation.xml": f'<p:presentation {PP} {RR}><p:sldIdLst><p:sldId id="256" r:id="rId1"/>'
                                '<p:sldId id="257" r:id="rId2"/></p:sldIdLst></p:presentation>',
        "ppt/_rels/presentation.xml.rels": rels(("rId1", "slide", "slides/slide1.xml"),
                                                ("rId2", "slide", "slides/slide2.xml")),
        "ppt/slides/slide1.xml": slide("PHA revalidation, Area 2 feed system", "Fictional example"),
        "ppt/slides/slide2.xml": slide("Node 3: feed pump P-101 discharge",
                                       "Deviation: high temperature (TT-2207)",
                                       "Safeguard: FDV-2210 trip"),
        "ppt/slides/_rels/slide2.xml.rels": rels(("rId1", "notesSlide", "../notesSlides/notesSlide2.xml")),
        "ppt/notesSlides/notesSlide2.xml": f"<p:notes {PP} {AA}><p:cSld><p:spTree><p:sp><p:txBody>"
                                           "<a:p><a:r><a:t>Action: confirm PSV-3301 set pressure</a:t></a:r></a:p>"
                                           "</p:txBody></p:sp></p:spTree></p:cSld></p:notes>",
    })


def build(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    procedure(folder / "SOP-104-feed-pump-isolation.docx")
    pm_plan(folder / "PM-plan-area-2.xlsx")
    pha_review(folder / "PHA-node-review.pptx")
    (folder / "CAPA-0042.html").write_text(
        "<html><head><title>CAPA-0042</title></head><body>\n<h1>CAPA-0042: seal leak on P-101</h1>\n"
        "<p>Root cause: seal flush blocked; TT-2207 read high for two shifts.</p>\n"
        "<table><tr><th>Action</th><th>Tag</th></tr>\n<tr><td>Add flush flow check</td><td>FI-2215</td></tr>"
        "</table>\n</body></html>\n", encoding="utf-8", newline="\n")
    (folder / "work-order-export.csv").write_text(
        "order,tag,description\nWO-5512,P-101,Replace seal\nWO-5513,FDV-2210,Function test\n",
        encoding="utf-8", newline="\n")
    (folder / "HACCP-plan-2019.doc").write_bytes(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 56)
    return folder


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(f"wrote {build(sys.argv[1]).as_posix()}")
