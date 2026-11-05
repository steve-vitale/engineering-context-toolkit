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
        ops = "".join(f"BT /F1 12 Tf 72 {720 - 20 * i} Td ({ln}) Tj ET\n" for i, ln in enumerate(lines))
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


if __name__ == "__main__":
    unittest.main()
