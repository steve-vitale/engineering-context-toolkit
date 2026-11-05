"""Tests for scripts/extract_text.py: locators per format, tags inside table cells and page headers, PDF text layer
and needs-OCR pages, missing optional dependency, legacy and disguised files, hostile archives, limits, the CLI and
its deterministic manifest. Office fixtures are built here with zipfile and the PDF by hand, so no binary blobs are
committed. PDF tests skip cleanly when pypdf (or pdftotext) is absent. Stdlib only.

Usage:  python -m unittest scripts/test_extract_text.py      (or python scripts/test_extract_text.py)
"""
import contextlib
import os
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_text as et  # noqa: E402

TAG = re.compile(r"\b[A-Z]{1,4}-\d{3,4}[A-Z]?\b")
WNS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
MCNS = 'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"'
SNS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
RNS = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
PNS = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
ANS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"


def tags_at(result):
    """tag -> sorted locators where it appears."""
    found = {}
    for locator, text in result:
        for m in TAG.finditer(text):
            found.setdefault(m.group(0), set()).add(locator)
    return {k: sorted(v) for k, v in found.items()}


def write_zip(path, parts):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    return path


def rels(*items):
    body = "".join(f'<Relationship Id="{i}" Type="{REL}{t}" Target="{target}"/>' for i, t, target in items)
    return ('<?xml version="1.0" encoding="UTF-8"?><Relationships '
            f'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{body}</Relationships>')


def w_p(text):
    return f'<w:p><w:r><w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def w_row(*cells):
    return "<w:tr>" + "".join(f"<w:tc>{w_p(c)}</w:tc>" for c in cells) + "</w:tr>"


def make_docx(path, body=None, extra=None):
    body = body if body is not None else (
        w_p("Procedure SOP-7: isolate the feed pump before work.")
        + "<w:p/>"  # empty paragraphs are not counted
        + w_p("Stop pump P-101 and close its suction valve.")
        + '<w:p><w:r><w:t>Before </w:t></w:r><w:del><w:r><w:delText>XV-9999 </w:delText></w:r></w:del>'
          '<w:r><w:t>check the vent.</w:t></w:r></w:p>'
        + "<w:tbl>" + w_row("Tag", "Service") + w_row("TT-2207", "Feed temperature")
        + w_row("FDV-2210", "Flame detector vent") + "</w:tbl>"
        + '<w:p><w:r><mc:AlternateContent><mc:Choice Requires="wps"><w:drawing><w:txbxContent>'
          + w_p("Text box: PSV-3301") + '</w:txbxContent></w:drawing></mc:Choice><mc:Fallback><w:pict>'
          '<w:txbxContent>' + w_p("Text box: PSV-3301") + '</w:txbxContent></w:pict></mc:Fallback>'
          '</mc:AlternateContent></w:r></w:p>')
    parts = {
        "[Content_Types].xml": "<Types/>",
        "word/document.xml": f'<?xml version="1.0"?><w:document {WNS} {MCNS}><w:body>{body}</w:body></w:document>',
        "word/header1.xml": f'<?xml version="1.0"?><w:hdr {WNS}>{w_p("HACCP plan for line TT-2207 area")}</w:hdr>',
        "word/footer2.xml": f'<?xml version="1.0"?><w:ftr {WNS}>{w_p("Rev 3 LT-400")}</w:ftr>',
        "word/footnotes.xml": f'<?xml version="1.0"?><w:footnotes {WNS}>'
                              '<w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:t>-</w:t></w:r></w:p></w:footnote>'
                              f'<w:footnote w:id="1">{w_p("See CAPA-0042 for HV-118.")}</w:footnote></w:footnotes>',
    }
    parts.update(extra or {})
    return write_zip(path, parts)


def make_xlsx(path, extra=None, hidden=False):
    shared = ["Tag", "Task", "TT-2207", "Calibrate", "Rich ", "FDV-2210"]
    sst = (f'<sst {SNS}>' + "".join(f"<si><t>{s}</t></si>" for s in shared[:4])
           + '<si><r><t xml:space="preserve">Rich </t></r><r><t>FDV-2210</t></r>'
             '<rPh><t>PHONETIC-999</t></rPh></si></sst>')
    sheet1 = (f'<worksheet {SNS}><sheetData>'
              '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c></row>'
              '<row r="7"><c r="A7" t="s"><v>3</v></c><c r="B7" t="s"><v>2</v></c><c r="C7"><v>42.5</v></c></row>'
              '<row r="8"><c r="A8" t="inlineStr"><is><t>Work order WO-5512 for P-101</t></is></c>'
              '<c t="s"><v>4</v></c><c r="D8" t="b"><v>1</v></c>'
              '<c r="E8" t="str"><f>A8&amp;"!"</f><v>LIC-300!</v></c></row>'
              '</sheetData></worksheet>')
    sheet2 = (f'<worksheet {SNS}><sheetData><row r="2"><c r="AA2" t="inlineStr"><is><t>PO for HV-118</t></is></c>'
              '</row></sheetData></worksheet>')
    state = ' state="hidden"' if hidden else ""
    parts = {
        "xl/workbook.xml": f'<workbook {SNS} {RNS}><sheets><sheet name="PM plan" sheetId="1" r:id="rId1"/>'
                           f'<sheet name="Bob\'s POs" sheetId="2" r:id="rId2"{state}/></sheets></workbook>',
        "xl/_rels/workbook.xml.rels": rels(("rId1", "worksheet", "worksheets/sheet1.xml"),
                                           ("rId2", "worksheet", "/xl/worksheets/sheet2.xml"),
                                           ("rId3", "sharedStrings", "sharedStrings.xml")),
        "xl/sharedStrings.xml": sst,
        "xl/worksheets/sheet1.xml": sheet1,
        "xl/worksheets/sheet2.xml": sheet2,
    }
    parts.update(extra or {})
    return write_zip(path, parts)


def make_pptx(path):
    def slide(*paras, show=None):
        attr = f' show="{show}"' if show is not None else ""
        body = "".join(f"<a:p>{p}</a:p>" for p in paras)
        return (f'<p:sld {PNS} {ANS}{attr}><p:cSld><p:spTree><p:sp><p:txBody>{body}</p:txBody></p:sp></p:spTree>'
                '</p:cSld></p:sld>')
    parts = {
        "ppt/presentation.xml": f'<p:presentation {PNS} {RNS}><p:sldIdLst><p:sldId id="256" r:id="rId7"/>'
                                '<p:sldId id="257" r:id="rId2"/></p:sldIdLst></p:presentation>',
        # relationship order differs from slide order on purpose: sldIdLst decides
        "ppt/_rels/presentation.xml.rels": rels(("rId2", "slide", "slides/slide2.xml"),
                                                ("rId7", "slide", "slides/slide1.xml")),
        "ppt/slides/slide1.xml": slide("<a:r><a:t>PHA kickoff</a:t></a:r>"),
        "ppt/slides/slide2.xml": slide("<a:r><a:t>Node 3: pump </a:t></a:r><a:r><a:t>P-101</a:t></a:r>",
                                       "<a:r><a:t>line one</a:t></a:r><a:br/><a:r><a:t>TT-2207</a:t></a:r>",
                                       show="0"),
        "ppt/slides/_rels/slide2.xml.rels": rels(("rId1", "notesSlide", "../notesSlides/notesSlide2.xml")),
        "ppt/notesSlides/notesSlide2.xml": f'<p:notes {PNS} {ANS}><p:cSld><p:spTree><p:sp><p:txBody>'
                                           '<a:p><a:r><a:t>Ask about FDV-2210</a:t></a:r></a:p>'
                                           '<a:p><a:fld type="slidenum"><a:t>2</a:t></a:fld></a:p>'
                                           '</p:txBody></p:sp></p:spTree></p:cSld></p:notes>',
    }
    return write_zip(path, parts)


def make_pdf(path, pages):
    """A minimal hand-built PDF: each page is a list of text lines, or [] for a page with no text layer."""
    objects = ["<< /Type /Catalog /Pages 2 0 R >>", None, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    kids = []
    for lines in pages:
        ops = "".join(f"BT /F1 12 Tf {ln[1]} {ln[2]} Td ({ln[0]}) Tj ET\n" if isinstance(ln, tuple)  # (text, x, y)
                      else f"BT /F1 12 Tf 72 {720 - 20 * i} Td ({ln}) Tj ET\n" for i, ln in enumerate(lines))
        objects.append(f"<< /Length {len(ops)} >>\nstream\n{ops}endstream")
        content = len(objects)
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents {content} 0 R "
                       "/Resources << /Font << /F1 3 0 R >> >> >>")
        kids.append(f"{len(objects)} 0 R")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>"
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for n, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{n} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    out += "".join(f"{o:010d} 00000 n \n" for o in offsets).encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    Path(path).write_bytes(bytes(out))
    return path


def has_pypdf():
    try:
        import pypdf  # noqa: F401
    except ImportError:
        return False
    return True


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()


class Formats(Base):
    def test_docx_paragraphs_table_cells_and_page_header(self):
        r = et.extract(make_docx(self.dir / "SOP-7.docx"))
        self.assertEqual(r.status, et.OK, r.warnings)
        self.assertEqual(r.format, "docx")
        tags = tags_at(r)
        self.assertEqual(tags["P-101"], ["paragraph 2"])
        self.assertEqual(tags["TT-2207"], ["page header 1 paragraph 1", "table 1 row 2"])
        self.assertEqual(tags["FDV-2210"], ["table 1 row 3"])
        self.assertEqual(tags["LT-400"], ["page footer 2 paragraph 1"])
        self.assertEqual(tags["HV-118"], ["footnote 1"])
        self.assertEqual(dict(r.segments)["table 1 row 2"], "TT-2207 | Feed temperature")
        # text-box text read once (the VML fallback copy is skipped); tracked deletions are not text
        self.assertEqual(sum(t.count("PSV-3301") for _, t in r), 1)
        self.assertNotIn("XV-9999", tags)
        self.assertTrue(any("tracked deletions" in w for w in r.warnings))
        self.assertEqual(r.sha256, __import__("hashlib").sha256((self.dir / "SOP-7.docx").read_bytes()).hexdigest())

    def test_xlsx_cells_named_by_sheet_and_reference(self):
        r = et.extract(make_xlsx(self.dir / "pm.xlsx", hidden=True))
        self.assertEqual(r.status, et.OK, r.warnings)
        tags = tags_at(r)
        self.assertEqual(tags["TT-2207"], ["sheet 'PM plan' cell B7"])
        self.assertEqual(tags["P-101"], ["sheet 'PM plan' cell A8"])
        self.assertEqual(tags["FDV-2210"], ["sheet 'PM plan' cell B8"])  # cell without r: position after A8
        self.assertEqual(tags["LIC-300"], ["sheet 'PM plan' cell E8"])   # cached formula result
        self.assertEqual(tags["HV-118"], ["sheet 'Bob''s POs' cell AA2"])
        self.assertNotIn("PHONETIC-999", tags)
        cells = dict(r.segments)
        self.assertEqual(cells["sheet 'PM plan' cell C7"], "42.5")
        self.assertEqual(cells["sheet 'PM plan' cell D8"], "TRUE")
        self.assertTrue(any("hidden" in w for w in r.warnings))

    def test_xlsm_macros_are_reported_never_run(self):
        r = et.extract(make_xlsx(self.dir / "pm.xlsm", extra={"xl/vbaProject.bin": b"\x00Attribute VB_Name"}))
        self.assertEqual(r.status, et.OK)
        self.assertTrue(any("macros" in w and "not run" in w for w in r.warnings))
        self.assertIn("TT-2207", tags_at(r))

    def test_pptx_slides_in_presentation_order_with_notes(self):
        r = et.extract(make_pptx(self.dir / "pha.pptx"))
        self.assertEqual(r.status, et.OK, r.warnings)
        self.assertEqual([loc for loc, _ in r], ["slide 1", "slide 2", "slide 2 notes"])
        tags = tags_at(r)
        self.assertEqual(tags["P-101"], ["slide 2"])
        self.assertEqual(tags["TT-2207"], ["slide 2"])
        self.assertEqual(tags["FDV-2210"], ["slide 2 notes"])
        self.assertEqual(dict(r.segments)["slide 2 notes"], "Ask about FDV-2210")  # slide-number field skipped
        self.assertTrue(any("slide 2 is hidden" in w for w in r.warnings))

    def test_text_markdown_csv_lines(self):
        (self.dir / "wo.csv").write_text("order,tag\nWO-1,P-101\n\nWO-2,TT-2207\n", encoding="utf-8")
        (self.dir / "notes.md").write_bytes("﻿# CAPA\r\nReplace FDV-2210 seal\r\n".encode("utf-8"))
        csv_tags = tags_at(et.extract(self.dir / "wo.csv"))
        self.assertEqual(csv_tags["P-101"], ["line 2"])
        self.assertEqual(csv_tags["TT-2207"], ["line 4"])
        self.assertEqual(tags_at(et.extract(self.dir / "notes.md"))["FDV-2210"], ["line 2"])

    def test_non_utf8_text_is_decoded_with_a_warning(self):
        (self.dir / "old.txt").write_bytes("Pump P-101 – café".encode("cp1252"))
        r = et.extract(self.dir / "old.txt")
        self.assertEqual(r.segments, [("line 1", "Pump P-101 – café")])
        self.assertTrue(any("Windows-1252" in w for w in r.warnings))

    def test_html_blocks_and_table_rows(self):
        (self.dir / "proc.html").write_text(
            "<html><head><title>Procedure</title><script>var x='P-999';</script></head><body>\n"
            "<h1>Isolate P-101</h1>\n<p>Check<br>the vent</p>\n"
            "<table><tr><th>Tag</th><th>Note</th></tr>\n<tr><td>TT-2207</td><td>&lt;ok&gt;</td></tr></table>\n"
            "<p>Then FDV-2210</p></body></html>", encoding="utf-8")
        r = et.extract(self.dir / "proc.html")
        tags = tags_at(r)
        self.assertEqual(tags["P-101"], ["line 2"])
        self.assertEqual(tags["TT-2207"], ["table 1 row 2"])
        self.assertEqual(tags["FDV-2210"], ["line 6"])
        self.assertNotIn("P-999", tags)  # script text is not document text
        self.assertEqual(dict(r.segments)["table 1 row 2"], "TT-2207 | <ok>")


@unittest.skipUnless(has_pypdf(), "SKIP pypdf not installed: PDF text-layer test (pip install pypdf)")
class PdfWithPypdf(Base):
    def test_pages_and_needs_ocr_page(self):
        path = make_pdf(self.dir / "pha.pdf", [["Node 1 feed pump P-101"], ["Table: TT-2207 high"], []])
        r = et.extract(path, pdf_engine="pypdf")
        self.assertEqual(r.engine, "pypdf")
        self.assertEqual(r.status, et.PARTIAL)
        self.assertEqual(tags_at(r), {"P-101": ["page 1"], "TT-2207": ["page 2"]})
        self.assertIn("no text layer, needs OCR: page 3 of 3", r.warnings)

    def test_scanned_pdf_reports_needs_ocr_without_error(self):
        r = et.extract(make_pdf(self.dir / "scan.pdf", [[], []]), pdf_engine="pypdf")
        self.assertEqual(r.status, et.NEEDS_OCR)
        self.assertEqual(r.segments, [])
        self.assertIn("no text layer, needs OCR: pages 1-2 of 2", r.warnings)

    def test_password_protected_pdf_is_unsupported_with_a_remedy(self):
        import pypdf
        writer = pypdf.PdfWriter(clone_from=str(make_pdf(self.dir / "plain.pdf", [["P-101"]])))
        writer.encrypt("secret", algorithm="RC4-128")
        with open(self.dir / "locked.pdf", "wb") as stream:
            writer.write(stream)
        engines = ["pypdf"] + (["pdftotext"] if shutil.which("pdftotext") else [])
        for engine in engines:
            r = et.extract(self.dir / "locked.pdf", pdf_engine=engine)
            self.assertEqual(r.status, et.UNSUPPORTED, (engine, r.warnings))
            self.assertIn("password-protected PDF", r.warnings[0])

    def test_corrupt_pdf_is_an_error_not_a_crash(self):
        (self.dir / "bad.pdf").write_bytes(b"%PDF-1.4\nthis is not a pdf body")
        r = et.extract(self.dir / "bad.pdf", pdf_engine="pypdf")
        self.assertEqual(r.status, et.ERROR)
        self.assertIn("not a readable PDF", r.warnings[0])
        self.assertEqual((r.engine, r.segments), ("pypdf", []))


@unittest.skipUnless(shutil.which("pdftotext"), "SKIP pdftotext not on PATH: fallback PDF test")
class PdfWithPdftotext(Base):
    def test_fallback_program_gives_the_same_pages(self):
        path = make_pdf(self.dir / "pha.pdf", [["Pump P-101"], ["FDV-2210 trip"], []])
        r = et.extract(path, pdf_engine="pdftotext")
        self.assertEqual(r.engine, "pdftotext")
        self.assertEqual(tags_at(r), {"P-101": ["page 1"], "FDV-2210": ["page 2"]})
        self.assertIn("no text layer, needs OCR: page 3 of 3", r.warnings)


class Limits(Base):
    def test_pdf_without_pypdf_or_pdftotext_says_how_to_get_text(self):
        path = make_pdf(self.dir / "a.pdf", [["P-101"]])
        with mock.patch.object(et, "_pypdf", return_value=None), mock.patch.object(et.shutil, "which",
                                                                                   return_value=None):
            r = et.extract(path)
        self.assertEqual(r.status, et.NEEDS_DEPENDENCY)
        self.assertEqual(r.segments, [])
        self.assertIn("PDF text needs pypdf (pip install pypdf)", r.warnings[0])

    def test_legacy_and_disguised_office_files(self):
        (self.dir / "old.doc").write_bytes(et.OLE_MAGIC + b"\x00" * 64)
        r = et.extract(self.dir / "old.doc")
        self.assertEqual(r.status, et.UNSUPPORTED)
        self.assertIn("convert it to .docx", r.warnings[0])
        self.assertEqual(et.extract(self.dir / "old.doc").sha256, r.sha256)
        (self.dir / "locked.xlsx").write_bytes(et.OLE_MAGIC + b"\x00" * 64)
        r = et.extract(self.dir / "locked.xlsx")
        self.assertEqual(r.status, et.UNSUPPORTED)
        self.assertIn("password-protected", r.warnings[0])
        (self.dir / "drawing.dwg").write_bytes(b"AC1032")
        self.assertEqual(et.extract(self.dir / "drawing.dwg").status, et.UNSUPPORTED)

    def test_corrupt_missing_and_oversized_files_are_errors(self):
        (self.dir / "bad.docx").write_bytes(b"PK\x03\x04garbage")
        self.assertEqual(et.extract(self.dir / "bad.docx").status, et.ERROR)
        (self.dir / "notzip.docx").write_text("hello", encoding="utf-8")
        self.assertEqual(et.extract(self.dir / "notzip.docx").status, et.ERROR)
        missing = et.extract(self.dir / "nope.pdf")
        self.assertEqual(missing.status, et.ERROR)
        self.assertEqual(missing.sha256, "")
        (self.dir / "big.txt").write_text("P-101\n" * 100, encoding="utf-8")
        big = et.extract(self.dir / "big.txt", max_bytes=50)
        self.assertEqual(big.status, et.ERROR)
        self.assertIn("byte limit", big.warnings[0])
        self.assertEqual(et.extract(self.dir).status, et.ERROR)  # a folder

    def test_zip_bomb_and_oversized_part_are_refused(self):
        bomb = write_zip(self.dir / "bomb.docx", {"word/document.xml": b"<" + b"\x00" * (3 * 1024 * 1024)})
        r = et.extract(bomb)
        self.assertEqual(r.status, et.ERROR)
        self.assertIn("zip bomb", r.warnings[0])
        with mock.patch.object(et, "MAX_MEMBER_BYTES", 100):
            r = et.extract(make_docx(self.dir / "a.docx"))
        self.assertEqual(r.status, et.ERROR)
        self.assertIn("limit", r.warnings[0])
        self.assertEqual(r.segments, [])

    def test_dtd_and_entities_are_refused(self):
        body = ('<?xml version="1.0"?><!DOCTYPE lol [<!ENTITY a "aaaaaaaaaa"><!ENTITY b "&a;&a;&a;&a;">]>'
                f'<w:document {WNS}><w:body><w:p><w:r><w:t>&b;</w:t></w:r></w:p></w:body></w:document>')
        path = write_zip(self.dir / "dtd.docx", {"word/document.xml": body})
        r = et.extract(path)
        self.assertEqual(r.status, et.ERROR)
        self.assertIn("DTD", r.warnings[0])

    def test_dtd_in_a_streamed_worksheet_is_refused(self):
        sheet = (f'<?xml version="1.0"?><!DOCTYPE x [<!ENTITY e "P-101">]><worksheet {SNS}><sheetData>'
                 '<row r="1"><c r="A1" t="inlineStr"><is><t>&e;</t></is></c></row></sheetData></worksheet>')
        r = et.extract(make_xlsx(self.dir / "dtd.xlsx", extra={"xl/worksheets/sheet1.xml": sheet}))
        self.assertEqual(r.status, et.ERROR)
        self.assertIn("DTD", r.warnings[0])

    def test_file_is_closed_and_tab_stops_are_not_text(self):
        body = ('<w:p><w:pPr><w:tabs><w:tab w:val="left" w:pos="720"/></w:tabs></w:pPr>'
                '<w:r><w:t>Pump</w:t></w:r><w:r><w:tab/><w:t>P-101</w:t></w:r></w:p>')
        path = make_docx(self.dir / "tabs.docx", body=body)
        r = et.extract(path)
        self.assertEqual(r.segments[0], ("paragraph 1", "Pump\tP-101"))
        path.unlink()  # on Windows this fails if the zip were left open

    def test_relationship_targets_cannot_leave_the_package(self):
        path = make_xlsx(self.dir / "escape.xlsx", extra={
            "xl/_rels/workbook.xml.rels": rels(("rId1", "worksheet", "../../../../etc/passwd"),
                                               ("rId2", "worksheet", "/xl/worksheets/sheet2.xml"),
                                               ("rId3", "sharedStrings", "sharedStrings.xml"))})
        r = et.extract(path)
        self.assertEqual(r.status, et.OK)
        self.assertTrue(any("sheet 'PM plan': worksheet part not found" in w for w in r.warnings))
        self.assertIn("HV-118", tags_at(r))

    def test_character_cap_gives_partial_result(self):
        (self.dir / "long.txt").write_text("P-101 line\n" * 50, encoding="utf-8")
        r = et.extract(self.dir / "long.txt", max_chars=25)
        self.assertEqual(r.status, et.PARTIAL)
        self.assertEqual(sum(len(t) for _, t in r), 25)
        self.assertTrue(any("character limit" in w for w in r.warnings))


class Cli(Base):
    def run_cli(self, *args):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
            code = et.main([str(a) for a in args])
        return code, stdout.getvalue()

    def inputs(self):
        sub = self.dir / "in" / "sub"
        sub.mkdir(parents=True)
        docx = make_docx(self.dir / "in" / "SOP-7.docx")
        xlsx = make_xlsx(self.dir / "in" / "pm.xlsx")
        (self.dir / "in" / "old.doc").write_bytes(et.OLE_MAGIC)
        (sub / "SOP-7.docx").write_bytes(docx.read_bytes() + b"")  # same name, same bytes, other folder
        return [docx, xlsx, self.dir / "in" / "old.doc", sub / "SOP-7.docx"]

    def test_outputs_manifest_and_exit_codes(self):
        files = self.inputs()
        code, _ = self.run_cli(*files, "--out", self.dir / "out")
        self.assertEqual(code, 0)  # an unsupported legacy file is reported, not an error
        manifest = json.loads((self.dir / "out" / "manifest.json").read_text(encoding="utf-8"))
        rows = manifest["files"]
        self.assertEqual([r["status"] for r in rows], ["ok", "ok", "unsupported", "ok"])
        self.assertEqual(len({r["out"] for r in rows}), 4)
        self.assertTrue(all(r["sha256"] and r["extractor"] == "extract_text 1" for r in rows))
        self.assertEqual(rows[0]["segments"], len(et.extract(files[0]).segments))
        text = (self.dir / "out" / rows[0]["out"]).read_text(encoding="utf-8")
        self.assertIn("## table 1 row 3\nFDV-2210 | Flame detector vent", text)
        self.assertIn(f"sha256: {rows[0]['sha256']}", text)
        self.assertIn("convert it to .docx", rows[2]["warnings"][0])

    def test_deterministic_output(self):
        files = self.inputs()
        self.run_cli(*files, "--out", self.dir / "a")
        self.run_cli(*files, "--out", self.dir / "b")
        a = {p.name: p.read_bytes() for p in (self.dir / "a").iterdir()}
        b = {p.name: p.read_bytes() for p in (self.dir / "b").iterdir()}
        self.assertEqual(a, b)
        self.assertNotIn(b"\r\n", a["manifest.json"])

    def test_real_error_exits_nonzero_but_writes_the_rest(self):
        good = make_docx(self.dir / "a.docx")
        code, out = self.run_cli(good, self.dir / "missing.xlsx", "--out", self.dir / "out")
        self.assertEqual(code, 1)
        rows = json.loads((self.dir / "out" / "manifest.json").read_text(encoding="utf-8"))["files"]
        self.assertEqual([r["status"] for r in rows], ["ok", "error"])
        self.assertIsNone(rows[1]["out"])
        self.assertTrue((self.dir / "out" / "a.docx.txt").is_file())
        self.assertIn("1 error(s)", out)

    @unittest.skipUnless(has_pypdf(), "SKIP pypdf not installed: needs-OCR CLI exit-code test")
    def test_needs_ocr_is_not_an_error(self):
        scan = make_pdf(self.dir / "scan.pdf", [[]])
        code, _ = self.run_cli(scan, "--out", self.dir / "out", "--pdf-engine", "pypdf")
        self.assertEqual(code, 0)


class WorkedExample(Base):
    """examples/document-text: regenerate the fictional samples, read them, compare every output byte for byte."""
    EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "document-text"

    def test_expected_outputs_reproduce(self):
        sys.path.insert(0, str(self.EXAMPLE))
        try:
            import make_samples
        finally:
            sys.path.remove(str(self.EXAMPLE))
        cwd = Path.cwd()
        try:
            os.chdir(self.dir)
            make_samples.build("samples")
            with contextlib.redirect_stdout(io.StringIO()):
                code = et.main(["samples", "--out", "expected"])
        finally:
            os.chdir(cwd)
        self.assertEqual(code, 0)
        got = {p.name: p.read_bytes() for p in (self.dir / "expected").iterdir()}
        want = {p.name: p.read_bytes() for p in (self.EXAMPLE / "expected").iterdir()}
        self.assertEqual(sorted(got), sorted(want))
        for name in want:
            self.assertEqual(got[name], want[name], name)
        found = tags_at(et.extract(self.dir / "samples" / "SOP-104-feed-pump-isolation.docx"))
        self.assertEqual(found["TT-2207"], ["page header 1 paragraph 1", "table 1 row 2"])
        self.assertEqual(found["FDV-2210"], ["table 1 row 3"])



# ---------------------------------------------------------------- optional add-ons

FAKE_TOOL = r'''
import os, sys, time, zipfile
log = os.environ.get("FAKE_TOOL_LOG")
tool, args = sys.argv[1], sys.argv[2:]
if log:
    with open(log, "a", encoding="utf-8") as f:
        f.write(repr([tool, args, os.environ.get("OMP_THREAD_LIMIT")]) + "\n")
if tool == "tesseract":
    if args == ["--version"]:
        print("tesseract 5.9.9-fake")
        sys.exit(0)
    data = open(args[0], "rb").read()
    if b"SLEEP" in data:
        hold = open(args[0], "rb")  # keeps the image open: the folder cannot be removed until this is killed
        time.sleep(60)
    words = data.split(b"TEXT:", 1)[1].decode() if b"TEXT:" in data else ""
    print("level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext")
    for page, line in enumerate(words.split("|"), 1):
        for n, word in enumerate(line.split(), 1):
            print(f"5\t{page}\t1\t1\t1\t{n}\t0\t0\t1\t1\t{90 + n}\t{word}")
elif tool == "pdftoppm":
    if args == ["-v"]:
        sys.stderr.write("pdftoppm version 99.1.0\n")
        sys.exit(0)
    page = args[args.index("-f") + 1]
    import struct
    png = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", 2550, 3300)
    png += b"\x08\x00\x00\x00\x00"
    with open(args[-1] + ".png", "wb") as f:
        f.write(png + (b"" if page == "4" else f"TEXT:Scanned page {page} pump P-10{page}".encode()))
elif tool == "soffice":
    if "--version" in args:
        print("LibreOffice 9.9.9.9 fake")
        sys.exit(0)
    out, src = args[args.index("--outdir") + 1], args[-1]
    target = args[args.index("--convert-to") + 1]
    text = open(src, "rb").read().decode("latin-1").split("TEXT:", 1)[-1]
    if target == "docx":
        with zipfile.ZipFile(os.path.join(out, "source.docx"), "w") as z:
            z.writestr("word/document.xml", '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/'
                       f'2006/main"><w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>')
'''


def fake_tools(folder, *tools):
    """Stand-in programs on a private PATH folder, so the real subprocess path (argument lists, timeouts, process
    trees, temporary folders) runs in tests without Tesseract, Poppler or LibreOffice installed."""
    folder.mkdir(parents=True, exist_ok=True)
    script = folder / "fake_tool.py"
    script.write_text(FAKE_TOOL, encoding="utf-8")
    for tool in tools:
        if os.name == "nt":
            (folder / f"{tool}.cmd").write_text(f'@"{sys.executable}" "{script}" {tool} %*\n', encoding="utf-8")
        else:
            launcher = folder / tool
            launcher.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" {tool} "$@"\n', encoding="utf-8")
            launcher.chmod(0o755)
    return folder


def png_bytes(width=400, height=100, text=""):
    import struct
    return (b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height)
            + b"\x08\x00\x00\x00\x00" + (b"TEXT:" + text.encode() if text else b""))


class AddonBase(Base):
    def setUp(self):
        super().setUp()
        et._tool_version.cache_clear()
        et._soffice_version.cache_clear()
        self.log = self.dir / "tool-log.txt"
        self.scratch = self.dir / "scratch"  # where the extractor's temporary folders go during the test
        self.scratch.mkdir()
        patches = [mock.patch.object(tempfile, "tempdir", str(self.scratch)),
                   mock.patch.dict(os.environ, {"FAKE_TOOL_LOG": str(self.log)})]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def only_path(self, *tools):
        """PATH holding only the named fake programs (no real pdftotext/tesseract/soffice)."""
        folder = fake_tools(self.dir / "bin", *tools) if tools else self.dir / "empty-bin"
        folder.mkdir(exist_ok=True)
        return mock.patch.dict(os.environ, {"PATH": str(folder)})

    def calls(self, tool):
        if not self.log.exists():
            return []
        rows = [eval(line) for line in self.log.read_text(encoding="utf-8").splitlines()]  # noqa: S307 (own log)
        return [(args, threads) for name, args, threads in rows if name == tool]

    def assert_scratch_clean(self):
        self.assertEqual(sorted(p.name for p in self.scratch.iterdir()), [])


@unittest.skipUnless(has_pypdf(), "SKIP pypdf not installed: OCR-of-scanned-PDF tests read the text layer with pypdf")
class OcrScannedPdf(AddonBase):
    def scan(self):
        return make_pdf(self.dir / "packet.pdf", [["Cover sheet P-100"], [], [], []])

    def test_default_is_unchanged_and_never_runs_ocr(self):
        with self.only_path("tesseract", "pdftoppm"):
            r = et.extract(self.scan(), pdf_engine="pypdf")
        self.assertEqual(r.status, et.PARTIAL)
        self.assertIn("no text layer, needs OCR: pages 2-4 of 4", r.warnings)
        self.assertEqual(self.calls("tesseract") + self.calls("pdftoppm"), [])
        self.assertNotIn("ocr", r.manifest_entry())

    def test_ocr_auto_reads_scanned_pages_with_engine_and_confidence(self):
        with self.only_path("tesseract", "pdftoppm"):
            r = et.extract(self.scan(), pdf_engine="pypdf", ocr="auto", ocr_dpi=200)
        self.assertEqual([loc for loc, _ in r], ["page 1", "page 2", "page 3"])
        self.assertEqual(dict(r.segments)["page 2"], "Scanned page 2 pump P-102")
        # page 4 rendered but OCR found nothing: still a page a person must look at
        self.assertEqual(r.status, et.PARTIAL)
        self.assertIn("OCR found no text: page 4 of 4 (a blank page, or an image OCR could not read)", r.warnings)
        self.assertFalse(any("no text layer" in w for w in r.warnings))
        self.assertEqual(r.ocr, {"page 2": 93.0, "page 3": 93.0})
        self.assertEqual(r.ocr_engine, "tesseract 5.9.9-fake (eng, 200 dpi; pages rendered by pdftoppm 99.1.0)")
        entry = r.manifest_entry()
        self.assertEqual(entry["ocr"]["mean_word_confidence"], {"page 2": 93.0, "page 3": 93.0})
        self.assertEqual(entry["applied"], ["ocr"])
        self.assertIn("# ocr: engine: tesseract 5.9.9-fake (eng, 200 dpi; pages rendered by pdftoppm 99.1.0) | "
                      "mean word confidence: page 2 93.0; page 3 93.0", et.render_text(r))
        renders = self.calls("pdftoppm")[1:]  # after the version query
        self.assertEqual([args[args.index("-f") + 1] for args, _ in renders], ["2", "3", "4"])
        for args, _ in renders:  # fixed names in the private folder, never the user's file name
            self.assertEqual(Path(args[-2]).name, "source.pdf")
            self.assertTrue(Path(args[-2]).is_absolute())
            self.assertEqual(args[args.index("-r") + 1], "200")
        for args, threads in self.calls("tesseract")[1:]:
            self.assertEqual((args[1], args[args.index("-l") + 1], args[-1], threads), ("stdout", "eng", "tsv", "1"))
        self.assert_scratch_clean()

    def test_every_page_ocred_is_ok_ocr(self):
        with self.only_path("tesseract", "pdftoppm"):
            r = et.extract(make_pdf(self.dir / "s.pdf", [["P-100"], []]), pdf_engine="pypdf", ocr="auto")
        self.assertEqual(r.status, et.OK_OCR)
        self.assertEqual(r.warnings, [])

    def test_missing_programs_keep_the_needs_ocr_report_and_say_what_is_missing(self):
        with self.only_path("tesseract"):
            r = et.extract(self.scan(), pdf_engine="pypdf", ocr="auto")
        self.assertEqual(r.status, et.PARTIAL)
        self.assertIn("no text layer, needs OCR: pages 2-4 of 4", r.warnings)
        self.assertIn("OCR not run: no pdftoppm program on PATH to render PDF pages (install Poppler)", r.warnings)
        with self.only_path():
            r = et.extract(make_pdf(self.dir / "all.pdf", [[]]), pdf_engine="pypdf", ocr="auto")
        self.assertEqual(r.status, et.NEEDS_OCR)
        self.assertTrue(any(w.startswith("OCR not run: no tesseract program on PATH") for w in r.warnings))


class OcrImages(AddonBase):
    def test_default_off_keeps_todays_unsupported_report(self):
        (self.dir / "nameplate.png").write_bytes(png_bytes(text="P-101"))
        with self.only_path("tesseract"):
            r = et.extract(self.dir / "nameplate.png")
        self.assertEqual(r.status, et.UNSUPPORTED)
        self.assertIn("no text reader for '.png' files", r.warnings[0])
        self.assertEqual(self.calls("tesseract"), [])

    def test_png_and_multipage_tiff_with_fake_tesseract(self):
        (self.dir / "nameplate.png").write_bytes(png_bytes(text="Pump P-101 tag"))
        with self.only_path("tesseract"):
            r = et.extract(self.dir / "nameplate.png", ocr="auto", ocr_lang="eng+deu")
        self.assertEqual((r.status, r.engine, r.engine_version), (et.OK_OCR, "tesseract", "5.9.9-fake"))
        self.assertEqual(r.segments, [("page 1", "Pump P-101 tag")])
        self.assertEqual(r.ocr, {"page 1": 92.0})
        args = self.calls("tesseract")[-1][0]
        self.assertEqual((Path(args[0]).name, args[args.index("-l") + 1]), ("image.png", "eng+deu"))
        self.assert_scratch_clean()

    def test_ocr_timeout_ends_the_program_and_removes_the_temporary_folder(self):
        fake_tools(self.dir / "bin", "tesseract")
        (self.dir / "photo.png").write_bytes(png_bytes(text="SLEEP"))
        start = __import__("time").monotonic()
        with self.only_path("tesseract"), mock.patch.object(et, "OCR_TIMEOUT", 3):
            r = et.extract(self.dir / "photo.png", ocr="auto")
        self.assertLess(__import__("time").monotonic() - start, 45)
        self.assertEqual(r.status, et.ERROR)
        self.assertIn("tesseract did not finish within 3 s", r.warnings[0])
        # on Windows the folder cannot be deleted while the sleeping program still holds the image open
        self.assert_scratch_clean()

    def test_temporary_folder_failure_is_reported_not_raised(self):
        (self.dir / "nameplate.png").write_bytes(png_bytes(text="P-101"))
        with self.only_path("tesseract"), mock.patch.object(et, "_temp_dir", side_effect=OSError("disk full")):
            r = et.extract(self.dir / "nameplate.png", ocr="auto")
        self.assertEqual(r.status, et.ERROR)
        self.assertIn("disk full", r.warnings[0])

    def test_image_without_tesseract_needs_a_dependency(self):
        (self.dir / "scan.jpg").write_bytes(b"\xff\xd8\xff\xc0\x00\x11\x08\x00\x64\x01\x90" + b"\x00" * 16)
        with self.only_path():
            r = et.extract(self.dir / "scan.jpg", ocr="auto")
        self.assertEqual(r.status, et.NEEDS_DEPENDENCY)
        self.assertIn("no tesseract program on PATH", r.warnings[0])

    def test_image_size_limits_and_disguised_files(self):
        self.assertEqual(et.image_size(png_bytes(640, 480), "png"), [(640, 480)])
        self.assertEqual(et.image_size(b"\xff\xd8\xff\xe0\x00\x04ab\xff\xc0\x00\x11\x08\x01\xe0\x02\x80" + b"\x00" * 9,
                                       "jpeg"), [(640, 480)])
        tiff = (b"II*\x00\x08\x00\x00\x00" + b"\x02\x00" + b"\x00\x01\x03\x00\x01\x00\x00\x00\x80\x02\x00\x00"
                + b"\x01\x01\x04\x00\x01\x00\x00\x00\xe0\x01\x00\x00" + b"\x26\x00\x00\x00"
                + b"\x01\x00" + b"\x00\x01\x03\x00\x01\x00\x00\x00\x10\x00\x00\x00" + b"\x00\x00\x00\x00")
        self.assertEqual(et.image_size(tiff, "tiff"), [(640, 480), (16, 0)])
        (self.dir / "bomb.png").write_bytes(png_bytes(60000, 60000))
        (self.dir / "fake.png").write_bytes(b"GIF89a")
        with self.only_path("tesseract"):
            bomb = et.extract(self.dir / "bomb.png", ocr="auto")
            fake = et.extract(self.dir / "fake.png", ocr="auto")
        self.assertEqual(bomb.status, et.ERROR)
        self.assertIn("OCR is limited to", bomb.warnings[0])
        self.assertEqual((fake.status, fake.warnings), (et.ERROR, ["not a PNG file"]))
        self.assertEqual(self.calls("tesseract"), [])

    def test_bad_ocr_arguments_are_refused_before_anything_runs(self):
        for kwargs in ({"ocr": "on"}, {"ocr_lang": "-l"}, {"ocr_lang": "eng;rm"}, {"ocr_dpi": 5}):
            with self.assertRaises(ValueError):
                et.extract(self.dir / "x.png", **kwargs)

    def test_tesseract_tsv_keeps_lines_and_blocks(self):
        tsv = ("level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
               "5\t1\t1\t1\t1\t1\t0\t0\t0\t0\t96\tFeed\n5\t1\t1\t1\t1\t2\t0\t0\t0\t0\t90\tpump\n"
               "5\t1\t1\t1\t2\t1\t0\t0\t0\t0\t80\tP-101\n4\t1\t2\t1\t1\t0\t0\t0\t0\t0\t-1\t\n"
               "5\t1\t2\t1\t1\t1\t0\t0\t0\t0\t-1\t \n5\t1\t2\t1\t1\t2\t0\t0\t0\t0\t70\tTT-2207\n")
        self.assertEqual(et.parse_tesseract_tsv(tsv), {1: ("Feed pump\nP-101\n\nTT-2207", 84.0)})


@unittest.skipUnless(et._tesseract(), "SKIP tesseract not on PATH: real OCR test (install Tesseract OCR)")
class OcrRealTesseract(Base):
    def test_rendered_tag_is_read(self):
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            self.skipTest("SKIP Pillow not installed: cannot draw the OCR test image")
        image = Image.new("L", (900, 200), 255)
        try:
            font = ImageFont.load_default(size=72)
        except TypeError:
            self.skipTest("SKIP Pillow too old to draw a large default font")
        ImageDraw.Draw(image).text((30, 50), "PUMP P-101", fill=0, font=font)
        image.save(self.dir / "tag.png")
        r = et.extract(self.dir / "tag.png", ocr="auto")
        self.assertEqual(r.status, et.OK_OCR, r.warnings)
        self.assertIn("P-101", r.segments[0][1].replace(" ", ""))
        self.assertTrue(r.engine_version and r.engine_version != "?")


class ConvertLegacy(AddonBase):
    def test_default_and_missing_libreoffice_keep_the_conversion_hint(self):
        (self.dir / "old.doc").write_bytes(et.OLE_MAGIC + b"TEXT:Isolate P-101")
        default = et.extract(self.dir / "old.doc")
        with mock.patch.object(et, "_soffice", return_value=None):
            r = et.extract(self.dir / "old.doc", convert_legacy=True)
        self.assertEqual(default.status, et.UNSUPPORTED)
        self.assertEqual(r.status, et.UNSUPPORTED)
        self.assertEqual(r.warnings[0], default.warnings[0])
        self.assertIn("no LibreOffice (soffice) program found", r.warnings[1])

    def test_conversion_in_a_private_folder_with_its_own_profile(self):
        (self.dir / "-rf old.doc").write_bytes(et.OLE_MAGIC + b"TEXT:Isolate P-101 before work")
        with self.only_path("soffice"):
            r = et.extract(self.dir / "-rf old.doc", convert_legacy=True)
        self.assertEqual(r.status, et.OK, r.warnings)
        self.assertEqual(r.segments, [("paragraph 1", "Isolate P-101 before work")])
        self.assertEqual(r.converted, "docx by LibreOffice 9.9.9.9")
        self.assertEqual(r.format, "doc")
        self.assertIn("converted from .doc to .docx by LibreOffice 9.9.9.9", r.warnings[0])
        args = self.calls("soffice")[-1][0]
        self.assertTrue(args[0].startswith("-env:UserInstallation=file:"))
        self.assertEqual(Path(args[-1]).name, "source.doc")  # never the user's (option-like) file name
        self.assertIn("--headless", args)
        self.assertEqual(r.manifest_entry()["converted"], "docx by LibreOffice 9.9.9.9")
        self.assert_scratch_clean()

    def test_no_output_is_unsupported_with_the_manual_step(self):
        (self.dir / "sheet.xls").write_bytes(et.OLE_MAGIC)
        with self.only_path("soffice"):
            r = et.extract(self.dir / "sheet.xls", convert_legacy=True)  # the fake makes only .docx
        self.assertEqual(r.status, et.UNSUPPORTED)
        self.assertIn("LibreOffice did not convert the file", r.warnings[0])
        self.assertIn("convert it to .xlsx", r.warnings[0])
        self.assert_scratch_clean()


@unittest.skipUnless(et._soffice(), "SKIP LibreOffice (soffice) not installed: real legacy-conversion test")
class ConvertLegacyReal(Base):
    def test_rtf_is_converted_and_read(self):
        (self.dir / "proc.rtf").write_text(r"{\rtf1\ansi Stop pump P-101.\par}", encoding="ascii")
        r = et.extract(self.dir / "proc.rtf", convert_legacy=True)
        self.assertEqual(r.status, et.OK, r.warnings)
        self.assertIn("P-101", tags_at(r))
        self.assertTrue(r.converted.startswith("docx by LibreOffice"))


def pdf_two_columns(path):
    """A page with two text columns side by side, the case plain extraction interleaves."""
    return make_pdf(path, [[("Left column line one", 72, 700), ("Left column line two", 72, 680),
                            ("Right column P-101", 330, 700), ("Right column TT-2207", 330, 680)]])


class PdfLayout(Base):
    def check(self, engine):
        path = pdf_two_columns(self.dir / "cols.pdf")
        plain = et.extract(path, pdf_engine=engine)
        laid = et.extract(path, pdf_engine=engine, pdf_layout=True)
        self.assertEqual(laid.status, et.OK, laid.warnings)
        self.assertNotIn("applied", plain.manifest_entry())
        self.assertEqual(laid.manifest_entry()["applied"], ["pdf layout"])
        rows = [ln for ln in laid.segments[0][1].splitlines() if "Left column line one" in ln]
        self.assertEqual(len(rows), 1)
        self.assertRegex(rows[0], r"Left column line one {2,}Right column P-101")
        return laid

    @unittest.skipUnless(has_pypdf(), "SKIP pypdf not installed: pypdf layout-mode test")
    def test_pypdf_layout_mode(self):
        self.check("pypdf")

    @unittest.skipUnless(shutil.which("pdftotext"), "SKIP pdftotext not on PATH: pdftotext -layout test")
    def test_pdftotext_layout_and_auto_prefers_it(self):
        self.check("pdftotext")
        auto = et.extract(pdf_two_columns(self.dir / "c2.pdf"), pdf_layout=True)
        self.assertEqual(auto.engine, "pdftotext")


def make_cfb(streams):
    """A minimal OLE compound file (MS-CFB v3) holding named streams; small ones go in the mini stream."""
    import struct
    sector, end, free = 512, 0xFFFFFFFE, 0xFFFFFFFF
    big = [(n, d) for n, d in streams if len(d) >= 4096]
    small = [(n, d) for n, d in streams if len(d) < 4096]
    mini, minifat, starts = b"", [], {}
    for name, data in small:
        starts[name] = len(mini) // 64
        count = max(1, -(-len(data) // 64))
        minifat += [starts[name] + k + 1 for k in range(count - 1)] + [end]
        mini += data.ljust(count * 64, b"\x00")
    blobs = [("minifat", struct.pack(f"<{len(minifat)}I", *minifat) if minifat else b""),
             ("ministream", mini)] + big
    entries = [("Root Entry", 5)] + [(n, 2) for n, _ in streams]
    directory_size = -(-len(entries) * 128 // sector) * sector
    layout, nxt = {}, 2  # sector 0 = FAT, sector 1.. = directory
    dir_sectors = directory_size // sector
    nxt = 1 + dir_sectors
    for name, data in blobs:
        count = -(-len(data) // sector)
        layout[name] = (nxt if count else end, count)
        nxt += count
    fat = [0xFFFFFFFD] + [k + 2 if k + 1 < dir_sectors else end for k in range(dir_sectors)]
    for name, data in blobs:
        start, count = layout[name]
        fat += [start + k + 1 if k + 1 < count else end for k in range(count)]
    fat += [free] * (128 - len(fat))
    body = b""
    for name, data in blobs:
        body += data.ljust(layout[name][1] * sector, b"\x00")
    directory = b""
    for name, kind in entries:
        raw = name.encode("utf-16-le") + b"\x00\x00"
        if kind == 5:
            start, size = layout["ministream"][0], len(mini)
        elif name in starts:
            start, size = starts[name], len(dict(streams)[name])
        else:
            start, size = layout[name][0], len(dict(streams)[name])
        child = 1 if kind == 5 and len(entries) > 1 else free
        index = entries.index((name, kind)) + 1
        right = index if kind == 2 and index < len(entries) else free
        directory += (raw.ljust(64, b"\x00") + struct.pack("<HBB", len(raw), kind, 1)
                      + struct.pack("<III", free, right, child) + b"\x00" * 36 + struct.pack("<IIi", start, size, 0))
    directory = directory.ljust(directory_size, b"\x00")
    header = (et.OLE_MAGIC + b"\x00" * 16 + struct.pack("<HHHH", 0x3E, 3, 0xFFFE, 9) + struct.pack("<H", 6)
              + b"\x00" * 6 + struct.pack("<I", 0) + struct.pack("<I", 1) + struct.pack("<I", 1)
              + struct.pack("<I", 0) + struct.pack("<I", 4096)
              + struct.pack("<II", layout["minifat"][0], layout["minifat"][1])
              + struct.pack("<II", end, 0) + struct.pack("<I", 0) + struct.pack("<I", free) * 108)
    assert len(header) == 512, len(header)
    return header + struct.pack("<128I", *fat) + directory + body


def ole_package(name, data):
    """An Ole10Native stream: how Office's Packager embeds an arbitrary file (here a PDF) under its file name."""
    import struct
    label = name.encode("cp1252") + b"\x00"
    inner = (struct.pack("<H", 2) + label + b"C:\\tmp\\" + label + struct.pack("<I", 0x00030000)
             + struct.pack("<I", len(label)) + label + struct.pack("<I", len(data)) + data)
    return struct.pack("<I", len(inner)) + inner


ONS = 'xmlns:o="urn:schemas-microsoft-com:office:office"'


def make_embedding_docx(path, embeds, body_extra=""):
    """A Word file whose body anchors each embedded part: table 1 holds the first, paragraph 2 the second."""
    obj = '<w:r><w:object><o:OLEObject r:id="{}"/></w:object></w:r>'
    body = (w_p("Spec sheet for P-101 follows.")
            + "<w:tbl><w:tr><w:tc><w:p>" + obj.format("rId11") + "</w:p></w:tc></w:tr></w:tbl>"
            + '<w:p><w:r><w:t>See attached datasheet</w:t></w:r>' + obj.format("rId12") + "</w:p>" + body_extra)
    parts = {"word/document.xml": f'<?xml version="1.0"?><w:document {WNS} {RNS} {ONS}><w:body>{body}'
                                  '</w:body></w:document>',
             "word/_rels/document.xml.rels": rels(*[(f"rId{11 + n}", "oleObject", f"embeddings/{name}")
                                                    for n, name in enumerate(embeds)])}
    parts.update({f"word/embeddings/{name}": data for name, data in embeds.items()})
    return write_zip(path, parts)


class Embedded(Base):
    def inner_xlsx(self):
        return make_xlsx(self.dir / "inner.xlsx").read_bytes()

    def test_embedded_workbook_is_read_with_its_place(self):
        path = make_embedding_docx(self.dir / "spec.docx", {"Microsoft_Excel_Worksheet.xlsx": self.inner_xlsx(),
                                                             "oleObject2.bin": et.OLE_MAGIC + b"\x00" * 600})
        r = et.extract(path)
        tags = tags_at(r)
        self.assertEqual(tags["TT-2207"], ["embedded 'Microsoft_Excel_Worksheet.xlsx' (in table 1) sheet 'PM plan' "
                                           "cell B7"])
        self.assertEqual(tags["P-101"][0], "embedded 'Microsoft_Excel_Worksheet.xlsx' (in table 1) sheet 'PM plan' "
                                           "cell A8")
        self.assertIn("paragraph 1", tags["P-101"])
        # a broken OLE object is reported, the rest is kept
        self.assertEqual(r.status, et.PARTIAL)
        self.assertTrue(any(w.startswith("embedded 'oleObject2.bin' (in paragraph 2): not read") for w in r.warnings))
        entry = r.manifest_entry()["embedded"][0]
        self.assertEqual((entry["name"], entry["format"], entry["status"]), ("Microsoft_Excel_Worksheet.xlsx", "xlsx",
                                                                             "ok"))
        self.assertEqual(entry["sha256"], __import__("hashlib").sha256(self.inner_xlsx()).hexdigest())

    @unittest.skipUnless(has_pypdf() or shutil.which("pdftotext"), "SKIP no PDF engine: embedded PDF test")
    def test_pdf_packaged_in_an_ole_object_is_read_under_its_own_name(self):
        pdf = make_pdf(self.dir / "spec.pdf", [["Datasheet cover"], ["Pump P-101 curve"]]).read_bytes()
        small = make_cfb([("\x01Ole10Native", ole_package("spec.pdf", pdf))])          # in the mini stream
        big_pdf = make_pdf(self.dir / "big.pdf", [["Datasheet cover"] + [f"Curve point {n}" for n in range(30)],
                                                  ["Pump P-101 curve"] + [f"Note {n}" for n in range(200)]])
        self.assertGreater(len(big_pdf.read_bytes()), 4096)
        large = make_cfb([("\x01Ole10Native", ole_package("big spec.pdf", big_pdf.read_bytes()))])  # big sectors
        for blob, name in ((small, "spec.pdf"), (large, "big spec.pdf")):
            path = make_embedding_docx(self.dir / "d.docx", {"oleObject1.bin": b"PK-not-used",
                                                              "oleObject2.bin": blob})
            r = et.extract(path)
            self.assertEqual(r.status, et.PARTIAL)  # oleObject1.bin is a broken package
            self.assertIn(f"embedded '{name}' (in paragraph 2) page 2", [loc for loc, _ in r])
            self.assertIn("P-101", dict(r.segments)[f"embedded '{name}' (in paragraph 2) page 2"])

    def test_off_switch_and_files_without_embeds_are_unchanged(self):
        path = make_embedding_docx(self.dir / "spec.docx", {"Microsoft_Excel_Worksheet.xlsx": self.inner_xlsx()})
        off = et.extract(path, embedded=False)
        self.assertIn("1 embedded object(s) not read (e.g. word/embeddings/Microsoft_Excel_Worksheet.xlsx)",
                      off.warnings)
        self.assertFalse(any(loc.startswith("embedded") for loc, _ in off))
        plain = make_docx(self.dir / "plain.docx")
        self.assertEqual(et.extract(plain).manifest_entry(), et.extract(plain, embedded=False).manifest_entry())

    def test_unreadable_objects_keep_the_old_warning_in_its_place(self):
        path = make_xlsx(self.dir / "visio.xlsx", extra={"xl/embeddings/oleObject1.bin": make_cfb(
            [("VisioDocument", b"\x00" * 100)])})
        on, off = et.extract(path), et.extract(path, embedded=False)
        self.assertEqual(on.warnings, off.warnings)
        self.assertEqual(on.segments, off.segments)

    def test_depth_limit(self):
        level3 = make_docx(self.dir / "l3.docx").read_bytes()
        level2 = make_embedding_docx(self.dir / "l2.docx", {"deep.docx": level3}).read_bytes()
        level1 = make_embedding_docx(self.dir / "l1.docx", {"middle.docx": level2}).read_bytes()
        top = make_embedding_docx(self.dir / "top.docx", {"outer.docx": level1})
        r = et.extract(top)
        locs = [loc for loc, _ in r]
        self.assertIn("embedded 'outer.docx' (in table 1) embedded 'middle.docx' (in table 1) paragraph 1", locs)
        self.assertFalse(any("deep.docx" in loc for loc in locs))
        self.assertTrue(any("more than 2 levels deep (e.g. word/embeddings/deep.docx)" in w for w in r.warnings))

    def test_embedded_zip_bomb_and_dtd_are_refused_like_top_level_files(self):
        bomb = write_zip(self.dir / "bomb.docx", {"word/document.xml": b"<" + b"\x00" * (3 * 1024 * 1024)})
        dtd = write_zip(self.dir / "dtd.docx", {"word/document.xml": '<?xml version="1.0"?><!DOCTYPE x []>'
                                                                     f'<w:document {WNS}/>'})
        r = et.extract(make_embedding_docx(self.dir / "t.docx", {"a.docx": bomb.read_bytes(),
                                                                  "b.docx": dtd.read_bytes()}))
        self.assertEqual(r.status, et.PARTIAL)
        self.assertTrue(any("zip bomb" in w for w in r.warnings))
        self.assertTrue(any("DTD" in w for w in r.warnings))
        self.assertFalse(any(loc.startswith("embedded") for loc, _ in r))

    def test_looping_ole_sector_chain_is_refused(self):
        blob = bytearray(make_cfb([("Package", b"PK" + b"\x00" * 5000)]))
        fat_at = 512
        blob[fat_at + 4 * 3:fat_at + 4 * 4] = (3).to_bytes(4, "little")  # a sector that points at itself
        r = et.extract(make_embedding_docx(self.dir / "loop.docx", {"oleObject1.bin": bytes(blob)}))
        self.assertTrue(any("not read" in w for w in r.warnings))


def make_styled_xlsx(path, date1904=False):
    styles = (f'<styleSheet {SNS}><numFmts count="3"><numFmt numFmtId="164" formatCode="0.0%"/>'
              '<numFmt numFmtId="165" formatCode="[&gt;=100]0"/>'
              '<numFmt numFmtId="166" formatCode="#,##0.00\\ &quot;m3/h&quot;"/></numFmts>'
              '<cellXfs count="7"><xf numFmtId="0"/><xf numFmtId="14"/><xf numFmtId="164"/><xf numFmtId="4"/>'
              '<xf numFmtId="165"/><xf numFmtId="166"/><xf numFmtId="22"/></cellXfs></styleSheet>')
    sheet = (f'<worksheet {SNS}><sheetData><row r="1">'
             '<c r="A1" s="1"><v>46330</v></c><c r="B1" s="2"><v>0.256</v></c><c r="C1" s="3"><v>1234567.891</v></c>'
             '<c r="D1" s="4"><v>150</v></c><c r="E1" s="5"><v>12.5</v></c><c r="F1" s="6"><v>46330.75</v></c>'
             '<c r="G1"><v>42.5</v></c><c r="H1" s="1" t="inlineStr"><is><t>P-101</t></is></c></row>'
             '</sheetData></worksheet>')
    pr = '<workbookPr date1904="1"/>' if date1904 else ""
    return write_zip(path, {
        "xl/workbook.xml": f'<workbook {SNS} {RNS}>{pr}<sheets><sheet name="Log" sheetId="1" r:id="rId1"/></sheets>'
                           '</workbook>',
        "xl/_rels/workbook.xml.rels": rels(("rId1", "worksheet", "worksheets/sheet1.xml"),
                                           ("rId2", "styles", "styles.xml")),
        "xl/styles.xml": styles, "xl/worksheets/sheet1.xml": sheet})


class ExcelDisplay(Base):
    def test_default_keeps_stored_values(self):
        cells = dict(et.extract(make_styled_xlsx(self.dir / "log.xlsx")).segments)
        self.assertEqual(cells["sheet 'Log' cell A1"], "46330")
        self.assertEqual(cells["sheet 'Log' cell B1"], "0.256")

    def test_display_applies_the_workbook_number_formats(self):
        r = et.extract(make_styled_xlsx(self.dir / "log.xlsx"), excel_display=True)
        cells = {loc.split()[-1]: text for loc, text in r}
        self.assertEqual(cells, {"A1": "2026-11-04", "B1": "25.6%", "C1": "1,234,567.89", "D1": "150",
                                 "E1": "12.50 m3/h", "F1": "2026-11-04 18:00", "G1": "42.5", "H1": "P-101"})
        self.assertIn("1 number cell(s) kept their stored value: number format not applied (e.g. '[>=100]0')",
                      r.warnings)
        self.assertEqual(r.manifest_entry()["applied"], ["excel display"])
        r1904 = et.extract(make_styled_xlsx(self.dir / "mac.xlsx", date1904=True), excel_display=True)
        self.assertEqual(dict(r1904.segments)["sheet 'Log' cell A1"], "2030-11-05")

    def test_format_rules(self):
        cases = [("46330", "d-mmm-yy h:mm AM/PM", "4-Nov-26 12:00 AM"), ("46330.75", "dddd d mmmm yyyy",
                                                                         "Wednesday 4 November 2026"),
                 ("-1234.5", "#,##0.00;(#,##0.00)", "(1,234.50)"), ("-1234.5", "#,##0.00", "-1,234.50"),
                 ("12345", "0.00E+00", "1.23E+04"), ("0.000123", "0.00E+00", "1.23E-04"),
                 ("1.5", "[h]:mm", "36:00"), ("0.0001", "mm:ss.0", "00:08.6"), ("7", "00000", "00007"),
                 ("1500000", '#,##0,"k"', "1,500k"), ("2.5", "0", "3"), ("0.125", "0.00", "0.13"),
                 ("1234", "[$€-407] #,##0.00", "€ 1,234.00"), ("46330", "[$-409]mmm-yy", "Nov-26"),
                 ("61", "yyyy-mm-dd", "1900-03-01"), ("59", "yyyy-mm-dd", "1900-02-28"),
                 ("12", "# ?/?", None), ("60", "yyyy-mm-dd", None), ("-1", "yyyy-mm-dd", None),
                 ("5", "0;;", "5"), ("0", "0;-0;", None), ("x", "0.00", None), ("3", "General", "3")]
        for value, code, want in cases:
            self.assertEqual(et.format_excel(value, code), want, (value, code))

    def test_a_number_too_long_to_format_keeps_its_stored_value(self):
        display = et._ExcelDisplay.__new__(et._ExcelDisplay)
        display.codes, display.xf, display.date1904 = {4: "#,##0.00"}, [4], False
        display.kept, display.example = 0, None
        self.assertEqual(display.show("1E+300", "0"), "1E+300")
        self.assertEqual(display.kept, 1)


class CliAddons(Base):
    def run_cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return et.main([str(a) for a in args])

    def test_options_recorded_only_when_asked_for(self):
        (self.dir / "in").mkdir()
        make_docx(self.dir / "in" / "a.docx")
        self.run_cli(self.dir / "in", "--out", self.dir / "plain")
        self.run_cli(self.dir / "in", "--out", self.dir / "opts", "--excel-display", "--ocr", "auto")
        plain = json.loads((self.dir / "plain" / "manifest.json").read_text(encoding="utf-8"))
        opts = json.loads((self.dir / "opts" / "manifest.json").read_text(encoding="utf-8"))
        self.assertNotIn("options", plain)
        self.assertEqual(opts["options"], {"ocr": "auto", "excel_display": True})
        self.assertEqual(plain["files"], opts["files"])  # nothing in a .docx without embeds changes

    def test_bad_addon_arguments_exit_2(self):
        for bad in (["--ocr", "yes"], ["--ocr-lang", "eng;x"], ["--ocr-dpi", "5"], ["--embedded", "maybe"]):
            with self.assertRaises(SystemExit) as ctx:
                self.run_cli(self.dir, "--out", self.dir / "o", *bad)
            self.assertEqual(ctx.exception.code, 2)

if __name__ == "__main__":
    unittest.main()
