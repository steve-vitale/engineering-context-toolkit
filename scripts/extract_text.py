"""Read the text inside plant documents (PDF, Word, Excel, PowerPoint, HTML, plain text) as ordered segments, each
with a locator a person can use to find it again ("page 3", "table 2 row 4", "sheet 'PM plan' cell B7", "slide 4").

    python scripts/extract_text.py FILE... --out DIR [--pdf-engine auto|pypdf|pdftotext] [--max-mb N]

Writes one UTF-8 .txt per input (a "## <locator>" header before each segment) and DIR/manifest.json (file, sha256,
format, status, engine, segment count, warnings). Exit 0 when every file was read or its limit was reported
(needs OCR, needs pypdf, unsupported legacy format); exit 1 only on a real error (missing, unreadable, corrupt,
over a size limit); exit 2 on bad arguments.

Library use (the call a tag matcher makes):

    result = extract(path)            # -> Extraction; never raises for a bad or unsupported file
    for locator, text in result:      # same as result.segments, an ordered list of (locator, text) tuples
        ...
    result.sha256, result.status, result.warnings, result.engine, result.engine_version

Office files are read with the standard library (zipfile + ElementTree) from their XML parts only: macros,
embedded objects and external links are never run, opened or followed. PDF text comes from the file's text layer
through the optional pypdf package, else a `pdftotext` program on PATH; scanned pages without a text layer are
reported as needing OCR, which this tool does not do. Files are treated as untrusted: size, archive-member,
member-count, compression-ratio and DTD checks refuse hostile inputs with a clear message. See
docs/DOCUMENT_TEXT.md.
"""
import argparse
import hashlib
import html.parser
import json
import logging
import posixpath
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

EXTRACTOR = "extract_text"
VERSION = "1"

MAX_FILE_BYTES = 100 * 1024 * 1024        # input file size cap (CLI --max-mb)
MAX_MEMBER_BYTES = 64 * 1024 * 1024       # largest single uncompressed archive part parsed whole
MAX_STREAM_BYTES = 1024 * 1024 * 1024     # largest worksheet / shared-strings part, read as a stream
MAX_TOTAL_UNCOMPRESSED = 2 * 1024 * 1024 * 1024  # all parts read from one archive together
MAX_ZIP_MEMBERS = 20000
MAX_RATIO = 200                           # uncompressed/compressed above this (for parts > 1 MiB) is refused
MAX_CHARS = 20_000_000                    # total extracted characters per file; beyond it the result is partial
MAX_PDF_PAGES = 5000
PDFTOTEXT_TIMEOUT = 120

# status values, in the order a reader should care about
OK, PARTIAL, NEEDS_OCR, NEEDS_DEPENDENCY, UNSUPPORTED, ERROR = (
    "ok", "partial", "needs OCR", "needs dependency", "unsupported", "error")

TEXT_SUFFIXES = {".txt": "text", ".md": "markdown", ".csv": "csv"}
HTML_SUFFIXES = {".html": "html", ".htm": "html"}
OFFICE_SUFFIXES = {".docx": "docx", ".docm": "docx", ".xlsx": "xlsx", ".xlsm": "xlsx", ".pptx": "pptx",
                   ".pptm": "pptx"}
LEGACY = {
    ".doc": "legacy Word .doc is not read; convert it to .docx (Word: Save As .docx, or "
            "`soffice --headless --convert-to docx FILE`) and run again",
    ".xls": "legacy Excel .xls is not read; convert it to .xlsx (Excel: Save As .xlsx, or "
            "`soffice --headless --convert-to xlsx FILE`) and run again",
    ".ppt": "legacy PowerPoint .ppt is not read; convert it to .pptx (PowerPoint: Save As .pptx, or "
            "`soffice --headless --convert-to pptx FILE`) and run again",
    ".rtf": "RTF is not read; convert it to .docx or .txt and run again",
}
OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"
MC = "{http://schemas.openxmlformats.org/markup-compatibility/2006}"


class Refused(Exception):
    """The file is corrupt, hostile or over a limit; the message says which and why."""


class Unsupported(Refused):
    """The file is valid but cannot be read as it is (password protection); the message says what to do."""


@dataclass
class Extraction:
    """What was read from one file. Iterating yields (locator, text) segments in document order."""
    path: str
    sha256: str = ""
    bytes: int = 0
    format: str = ""
    status: str = OK
    engine: str = "stdlib"          # "pypdf" or "pdftotext" for PDF text
    engine_version: str = ""        # the PDF engine version; the extractor version is VERSION
    segments: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    def __iter__(self):
        return iter(self.segments)

    def __len__(self):
        return len(self.segments)

    def manifest_entry(self):
        return {"file": self.path, "sha256": self.sha256, "bytes": self.bytes, "format": self.format,
                "status": self.status, "extractor": f"{EXTRACTOR} {VERSION}", "engine": self.engine,
                "engine_version": self.engine_version, "segments": len(self.segments),
                "characters": sum(len(t) for _, t in self.segments), "warnings": list(self.warnings)}


class _Collector:
    """Accumulates segments, enforcing the character cap."""

    def __init__(self, result, max_chars):
        self.result, self.left, self.full = result, max_chars, False

    def add(self, locator, text):
        if self.full:
            return
        text = clean(text)
        if not text:
            return
        if len(text) > self.left:
            text = text[:self.left]
            self.full = True
            self.result.warnings.append(f"stopped at {locator}: more than the character limit was extracted; "
                                        "the rest of the file was not read")
        self.left -= len(text)
        if text:
            self.result.segments.append((locator, text))


def clean(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    return text.strip("\n").strip()


# ---------------------------------------------------------------- plain text and HTML

def decode_text(data, warnings):
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return data.decode("utf-16")
        except UnicodeDecodeError:
            pass
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        pass
    try:
        text = data.decode("cp1252")
        warnings.append("not valid UTF-8; decoded as Windows-1252 (check accented characters)")
    except UnicodeDecodeError:
        text = data.decode("latin-1")
        warnings.append("not valid UTF-8 or Windows-1252; decoded as Latin-1 (check accented characters)")
    return text


def read_text(data, out, result):
    for n, line in enumerate(decode_text(data, result.warnings).splitlines(), 1):
        out.add(f"line {n}", line)


class _HTMLText(html.parser.HTMLParser):
    BLOCK = {"p", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "header",
             "footer", "nav", "aside", "main", "pre", "blockquote", "dt", "dd", "table", "caption", "form",
             "title", "figcaption", "hr"}
    SKIP = {"script", "style", "noscript", "template"}

    def __init__(self, out):
        super().__init__(convert_charrefs=True)
        self.out, self.buf, self.start, self.skip = out, [], None, 0
        self.tables, self.table_stack, self.cells = 0, [], None

    def flush(self):
        text = " ".join("".join(self.buf).split())
        if text:
            self.out.add(f"line {self.start}", text)
        self.buf, self.start = [], None

    def flush_row(self):
        if self.cells is not None:
            cells = [" ".join(c.split()) for c in self.cells]
            if any(cells):
                table, row = self.table_stack[-1]
                self.out.add(f"table {table} row {row}", " | ".join(cells))
        self.cells = None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
            return
        if tag == "table":
            self.flush_row() if self.table_stack else self.flush()
            self.tables += 1
            self.table_stack.append([self.tables, 0])
        elif tag == "tr" and self.table_stack:
            self.flush_row()
            self.table_stack[-1][1] += 1
            self.cells = []
        elif tag in ("td", "th") and self.table_stack:
            if self.cells is None:  # a cell outside any <tr>
                self.table_stack[-1][1] += 1
                self.cells = []
            self.cells.append("")
        elif tag == "br":
            self.data("\n")
        elif tag in self.BLOCK and not self.table_stack:
            self.flush()

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if tag == "table" and self.table_stack:
            self.flush_row()
            self.table_stack.pop()
        elif tag == "tr" and self.table_stack:
            self.flush_row()
        elif tag in self.BLOCK and not self.table_stack:
            self.flush()

    def handle_data(self, data):
        if not self.skip:
            self.data(data)

    def data(self, data):
        if self.table_stack:
            if self.cells is None:
                if data.strip():  # stray text inside <table> but outside a row
                    self.table_stack[-1][1] += 1
                    self.cells = [data]
                return
            if not self.cells:
                self.cells.append("")
            self.cells[-1] += " " if data == "\n" else data
            return
        if self.start is None and data.strip():
            self.start = self.getpos()[0]
        self.buf.append(" " if data == "\n" else data)

    def close(self):
        super().close()
        while self.table_stack:
            self.flush_row()
            self.table_stack.pop()
        self.flush()


def read_html(data, out, result):
    parser = _HTMLText(out)
    parser.feed(decode_text(data, result.warnings))
    parser.close()


# ---------------------------------------------------------------- Office Open XML (zip of XML parts)

class _CappedStream:
    """File-like view of one archive part that counts bytes, enforces the caps and refuses DTDs as it reads."""

    def __init__(self, raw, name, package, cap):
        self.raw, self.name, self.package, self.cap = raw, name, package, cap
        self.count, self.tail = 0, b""

    def read(self, size=-1):
        chunk = self.raw.read(size if size and size > 0 else 1 << 16)
        self.count += len(chunk)
        self.package.count(len(chunk))
        if self.count > self.cap:
            raise Refused(f"part {self.name} is larger than the {self.cap} byte limit")
        if _DTD.search(self.tail + chunk):
            raise Refused(f"part {self.name} declares a DTD or entities; Office XML never does, so it is refused")
        self.tail = chunk[-16:]
        return chunk


_DTD = re.compile(rb"<!(DOCTYPE|ENTITY)", re.I)


class _Package:
    """Bounded, read-only access to named parts of an untrusted zip. Nothing is extracted to disk or executed."""

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.zip.close()

    def count(self, n):
        self.read_total += n
        if self.read_total > MAX_TOTAL_UNCOMPRESSED:
            raise Refused(f"archive parts total more than {MAX_TOTAL_UNCOMPRESSED} bytes uncompressed")

    def __init__(self, path):
        try:
            self.zip = zipfile.ZipFile(path)
        except (zipfile.BadZipFile, OSError, ValueError) as exc:
            raise Refused(f"not a readable Office file (bad zip container: {exc})") from None
        infos = self.zip.infolist()
        if len(infos) > MAX_ZIP_MEMBERS:
            raise Refused(f"archive has {len(infos)} parts; more than the {MAX_ZIP_MEMBERS} limit")
        self.info = {}
        for i in infos:
            self.info.setdefault(i.filename.replace("\\", "/").lstrip("/"), i)
        self.read_total = 0

    def names(self):
        return sorted(self.info)

    def _open(self, name):
        info = self.info.get(name)
        if info is not None and info.flag_bits & 0x1:
            raise Refused(f"part {name} is encrypted")
        return info

    def read(self, name):
        info = self._open(name)
        if info is None:
            return None
        if info.file_size > MAX_MEMBER_BYTES:
            raise Refused(f"part {name} declares {info.file_size} bytes uncompressed; more than the "
                          f"{MAX_MEMBER_BYTES} byte limit")
        if info.file_size > 1024 * 1024 and info.compress_size and info.file_size / info.compress_size > MAX_RATIO:
            raise Refused(f"part {name} compresses {info.file_size // info.compress_size}:1; refused as a "
                          "possible zip bomb")
        try:
            with self.zip.open(info) as stream:  # never trust the declared size: read at most the cap + 1
                data = stream.read(MAX_MEMBER_BYTES + 1)
        except (zipfile.BadZipFile, OSError, ValueError, RuntimeError, NotImplementedError) as exc:
            raise Refused(f"part {name} cannot be read: {exc}") from None
        if len(data) > MAX_MEMBER_BYTES:
            raise Refused(f"part {name} is larger than the {MAX_MEMBER_BYTES} byte limit")
        self.count(len(data))
        return data

    def xml(self, name):
        data = self.read(name)
        if data is None:
            return None
        probe = data
        if data.startswith((b"\xff\xfe", b"\xfe\xff")):
            probe = data.decode("utf-16", "replace").encode("utf-8")
        if _DTD.search(probe):
            raise Refused(f"part {name} declares a DTD or entities; Office XML never does, so it is refused")
        try:
            return ET.fromstring(data)
        except ET.ParseError as exc:
            raise Refused(f"part {name} is not well-formed XML: {exc}") from None

    def stream(self, name, tag):
        """Yield each finished `tag` element of a large part (worksheet rows, shared strings), then free it."""
        info = self._open(name)
        if info is None:
            return
        if info.file_size > MAX_STREAM_BYTES:
            raise Refused(f"part {name} declares {info.file_size} bytes uncompressed; more than the "
                          f"{MAX_STREAM_BYTES} byte limit")
        try:
            with self.zip.open(info) as raw:
                capped = _CappedStream(raw, name, self, MAX_STREAM_BYTES)
                for _, element in ET.iterparse(capped, events=("end",)):
                    if element.tag == tag:
                        yield element
                        element.clear()
        except ET.ParseError as exc:
            raise Refused(f"part {name} is not well-formed XML: {exc}") from None
        except (zipfile.BadZipFile, OSError, ValueError, RuntimeError, NotImplementedError) as exc:
            raise Refused(f"part {name} cannot be read: {exc}") from None

    def rels(self, part):
        """Relationship id -> (type suffix, internal target part) for a part; external targets are dropped."""
        folder, base = posixpath.split(part)
        root = self.xml(posixpath.join(folder, "_rels", base + ".rels"))
        out = {}
        if root is None:
            return out
        for rel in root.iter(PR + "Relationship"):
            if rel.get("TargetMode") == "External":
                continue
            target = rel.get("Target") or ""
            joined = target.lstrip("/") if target.startswith("/") else posixpath.join(folder, target)
            norm = posixpath.normpath(joined)
            if norm.startswith("..") or norm.startswith("/"):
                continue  # points outside the package: ignored
            out[rel.get("Id")] = ((rel.get("Type") or "").rsplit("/", 1)[-1], norm)
        return out

    def inspect(self, result, macro_part, embed_prefixes):
        names = self.names()
        if any(n.lower().endswith(macro_part) for n in names):
            result.warnings.append("contains macros (vbaProject.bin); not run and not read")
        embedded = [n for n in names if n.startswith(embed_prefixes) and not n.endswith("/")]
        if embedded:
            result.warnings.append(f"{len(embedded)} embedded object(s) not read (e.g. {embedded[0]})")


_NOT_TEXT = {MC + "Fallback", W + "pPr", W + "rPr", W + "sectPr", W + "tblPr", W + "trPr", W + "tcPr"}


def _without_fallback(element):
    """Yield descendants in order, skipping mc:Fallback copies (so alternate content is not read twice) and
    formatting properties (whose w:tab elements are tab-stop definitions, not tabs)."""
    for child in element:
        if child.tag in _NOT_TEXT:
            continue
        yield child
        yield from _without_fallback(child)


def _word_text(element):
    parts = []
    for node in _without_fallback(element):
        tag = node.tag
        if tag == W + "t":
            parts.append(node.text or "")
        elif tag == W + "tab":
            parts.append("\t")
        elif tag in (W + "br", W + "cr"):
            parts.append("\n")
        elif tag == W + "noBreakHyphen":
            parts.append("-")
        elif tag == W + "p":
            if parts and not parts[-1].endswith("\n"):
                parts.append("\n")  # paragraph inside a text box or nested cell
    return "".join(parts)


def _word_blocks(container, out, prefix, counters):
    """Walk a body/header/footer in order: paragraphs and tables, each with its own locator."""
    for child in container:
        if child.tag == W + "p":
            text = _word_text(child)
            if text.strip():
                counters["paragraph"] += 1
                out.add(f"{prefix}paragraph {counters['paragraph']}", text)
        elif child.tag == W + "tbl":
            counters["table"] += 1
            table = counters["table"]
            row = 0
            for tr in child.findall(W + "tr"):  # nested tables are read inside their parent cell
                row += 1
                cells = [" ".join(_word_text(tc).split()) for tc in tr.findall(W + "tc")]
                if any(cells):
                    out.add(f"{prefix}table {table} row {row}", " | ".join(cells))
        elif child.tag == W + "sdt":
            content = child.find(W + "sdtContent")
            if content is not None:
                _word_blocks(content, out, prefix, counters)
        elif child.tag in (MC + "AlternateContent",):
            choice = child.find(MC + "Choice")
            if choice is not None:
                _word_blocks(choice, out, prefix, counters)


def _numbered(names, pattern):
    found = []
    for name in names:
        m = re.fullmatch(pattern, name)
        if m:
            found.append((int(m.group(1)), name))
    return sorted(found)


def read_docx(path, out, result):
    with _Package(path) as pkg:
        _read_docx(pkg, out, result)


def _read_docx(pkg, out, result):
    pkg.inspect(result, "vbaproject.bin", ("word/embeddings/",))
    doc = pkg.xml("word/document.xml")
    if doc is None:
        raise Refused("no word/document.xml; not a Word document")
    body = doc.find(W + "body")
    if body is not None:
        _word_blocks(body, out, "", {"paragraph": 0, "table": 0})
    names = pkg.names()
    for kind in ("header", "footer"):
        for n, name in _numbered(names, rf"word/{kind}(\d+)\.xml"):
            root = pkg.xml(name)
            if root is not None:
                _word_blocks(root, out, f"page {kind} {n} ", {"paragraph": 0, "table": 0})
    for kind, tag in (("footnote", "footnote"), ("endnote", "endnote"), ("comment", "comment")):
        root = pkg.xml(f"word/{kind}s.xml")
        if root is None:
            continue
        number = 0
        for note in root.findall(W + tag):
            if note.get(W + "type") in ("separator", "continuationSeparator", "continuationNotice"):
                continue
            number += 1
            out.add(f"{kind} {number}", _word_text(note))
    if any(True for _ in doc.iter(W + "delText")):
        result.warnings.append("tracked deletions present; deleted text is not read")


def column_letters(index):
    letters = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _split_ref(ref):
    m = re.fullmatch(r"([A-Z]{1,3})(\d+)", ref or "")
    if not m:
        return None
    col = 0
    for ch in m.group(1):
        col = col * 26 + ord(ch) - 64
    return col - 1, int(m.group(2))


def _si_text(si):
    """Plain (t) and rich-text (r/t) string content; phonetic guides (rPh) are not cell text."""
    phonetic = {id(t) for rph in si.iter(S + "rPh") for t in rph.iter(S + "t")}
    return "".join(t.text or "" for t in si.iter(S + "t") if id(t) not in phonetic)


def read_xlsx(path, out, result):
    with _Package(path) as pkg:
        _read_xlsx(pkg, out, result)


def _read_xlsx(pkg, out, result):
    pkg.inspect(result, "vbaproject.bin", ("xl/embeddings/",))
    book = pkg.xml("xl/workbook.xml")
    if book is None:
        raise Refused("no xl/workbook.xml; not an Excel workbook")
    rels = pkg.rels("xl/workbook.xml")
    strings = next((part for kind, part in sorted(rels.values()) if kind == "sharedStrings"),
                   "xl/sharedStrings.xml")
    shared = [_si_text(si) for si in pkg.stream(strings, S + "si")]
    sheets = book.find(S + "sheets")
    for sheet in (sheets if sheets is not None else []):
        name = sheet.get("name") or "?"
        label = "sheet '" + name.replace("'", "''") + "'"
        if sheet.get("state") in ("hidden", "veryHidden"):
            result.warnings.append(f"{label} is hidden in Excel; its cells are read")
        target = rels.get(sheet.get(R + "id"))
        if not target or target[0] != "worksheet":
            if target and target[0] == "chartsheet":
                continue
            result.warnings.append(f"{label}: worksheet part not found; skipped")
            continue
        if target[1] not in pkg.info:
            result.warnings.append(f"{label}: worksheet part {target[1]} missing; skipped")
            continue
        row_number = 0
        for row in pkg.stream(target[1], S + "row"):
            if out.full:
                break
            row_number = int(row.get("r")) if (row.get("r") or "").isdigit() else row_number + 1
            col = -1
            for cell in row.findall(S + "c"):
                pos = _split_ref(cell.get("r"))
                col = pos[0] if pos else col + 1
                ref = f"{column_letters(col)}{row_number}"
                kind = cell.get("t") or "n"
                if kind == "inlineStr":
                    node = cell.find(S + "is")
                    value = _si_text(node) if node is not None else ""
                else:
                    v = cell.find(S + "v")
                    value = v.text if v is not None and v.text is not None else ""
                    if kind == "s" and value:
                        try:
                            value = shared[int(value)]
                        except (ValueError, IndexError):
                            result.warnings.append(f"{label} cell {ref}: shared string {value} missing")
                            value = ""
                    elif kind == "b":
                        value = {"1": "TRUE", "0": "FALSE"}.get(value, value)
                out.add(f"{label} cell {ref}", value)


def read_pptx(path, out, result):
    with _Package(path) as pkg:
        _read_pptx(pkg, out, result)


def _read_pptx(pkg, out, result):
    pkg.inspect(result, "vbaproject.bin", ("ppt/embeddings/",))
    pres = pkg.xml("ppt/presentation.xml")
    if pres is None:
        raise Refused("no ppt/presentation.xml; not a PowerPoint file")
    rels = pkg.rels("ppt/presentation.xml")
    ids = pres.find(P + "sldIdLst")
    number = 0
    for sld in (ids if ids is not None else []):
        target = rels.get(sld.get(R + "id"))
        if not target:
            continue
        number += 1
        root = pkg.xml(target[1])
        if root is None:
            result.warnings.append(f"slide {number}: part {target[1]} missing; skipped")
            continue
        if root.get("show") == "0":
            result.warnings.append(f"slide {number} is hidden in the slide show; its text is read")
        out.add(f"slide {number}", _drawing_text(root))
        for kind, part in sorted(pkg.rels(target[1]).values()):
            if kind == "notesSlide":
                notes = pkg.xml(part)
                if notes is not None:
                    out.add(f"slide {number} notes", _drawing_text(notes))


def _drawing_text(root):
    """Paragraph text of a slide or notes page in document order; slide-number fields are skipped."""
    lines = []
    for para in root.iter(A + "p"):
        parts = []
        for child in para:
            if child.tag == A + "r" or (child.tag == A + "fld" and child.get("type") != "slidenum"):
                parts.append("".join(t.text or "" for t in child.iter(A + "t")))
            elif child.tag == A + "br":
                parts.append("\n")
        lines.append("".join(parts))
    return "\n".join(ln for ln in lines if ln.strip())


# ---------------------------------------------------------------- PDF (text layer only)

def _pypdf():
    try:
        import pypdf  # optional; see docs/DEPENDENCIES.md
    except ImportError:
        return None
    return pypdf


def read_pdf(path, out, result, engine="auto"):
    pypdf = _pypdf() if engine in ("auto", "pypdf") else None
    binary = shutil.which("pdftotext") if engine in ("auto", "pdftotext") else None
    if pypdf is not None:
        pages = _pdf_pypdf(pypdf, path, result)
    elif binary:
        pages = _pdf_pdftotext(binary, path, result)
    else:
        result.status = NEEDS_DEPENDENCY
        need = {"pypdf": "pypdf is not installed", "pdftotext": "no pdftotext program on PATH"}.get(engine)
        result.warnings.append("PDF text needs pypdf (pip install pypdf)"
                               + (f"; {need}" if need else " or a pdftotext program on PATH"))
        return
    if not pages:
        result.warnings.append("PDF has no pages")
    blank = []
    for n, text in enumerate(pages, 1):
        if text.strip():
            out.add(f"page {n}", text)
        else:
            blank.append(n)
    if blank:
        result.warnings.append(f"no text layer, needs OCR: page{'s' if len(blank) > 1 else ''} "
                               + _ranges(blank) + f" of {len(pages)}")
        result.status = NEEDS_OCR if len(blank) == len(pages) else PARTIAL


def _ranges(numbers):
    spans, start = [], numbers[0]
    for a, b in zip(numbers, numbers[1:] + [None]):
        if b != a + 1:
            spans.append(str(start) if start == a else f"{start}-{a}")
            start = b
    return ", ".join(spans)


def _pdf_pypdf(pypdf, path, result):
    logging.getLogger("pypdf").setLevel(logging.ERROR)  # recoverable-file chatter; real failures are caught below
    result.engine, result.engine_version = "pypdf", getattr(pypdf, "__version__", "?")
    try:
        reader = pypdf.PdfReader(str(path), strict=False)
        if reader.is_encrypted:
            try:
                ok = reader.decrypt("")
            except Exception as exc:  # e.g. AES encryption without the cryptography package
                raise Unsupported(f"encrypted PDF could not be opened ({type(exc).__name__}: {exc}); save an "
                                  "unprotected copy and run again") from None
            if not ok:
                raise Unsupported("password-protected PDF; save an unprotected copy and run again")
        count = len(reader.pages)
    except Refused:
        raise
    except Exception as exc:  # pypdf reports corrupt files with many exception types
        raise Refused(f"not a readable PDF: {type(exc).__name__}: {exc}") from None
    if count > MAX_PDF_PAGES:
        raise Refused(f"PDF has {count} pages; more than the {MAX_PDF_PAGES} page limit")
    pages = []
    for i in range(count):
        try:
            pages.append(reader.pages[i].extract_text() or "")
        except Exception as exc:
            result.warnings.append(f"page {i + 1}: text could not be read ({type(exc).__name__}: {exc})")
            pages.append("")
    return pages


def _pdf_pdftotext(binary, path, result):
    result.engine = "pdftotext"
    try:
        ver = subprocess.run([binary, "-v"], capture_output=True, timeout=30)
        m = re.search(rb"version ([\w.\-]+)", ver.stdout + ver.stderr)
        result.engine_version = m.group(1).decode() if m else "?"
        # an absolute path, so a file named like an option ("-foo.pdf") is never read as one
        run = subprocess.run([binary, "-enc", "UTF-8", "-eol", "unix", str(Path(path).resolve()), "-"],
                             capture_output=True, timeout=PDFTOTEXT_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise Refused(f"pdftotext did not finish within {PDFTOTEXT_TIMEOUT} s") from None
    except OSError as exc:
        raise Refused(f"pdftotext could not run: {exc}") from None
    if run.returncode != 0:
        msg = run.stderr.decode("utf-8", "replace").strip().splitlines()
        if any("password" in line.lower() for line in msg):
            raise Unsupported("password-protected PDF; save an unprotected copy and run again")
        raise Refused("pdftotext could not read the PDF: " + (msg[-1] if msg else f"exit {run.returncode}"))
    pages = run.stdout.decode("utf-8", "replace").split("\f")
    if pages and not pages[-1].strip():
        pages.pop()  # pdftotext ends every page, including the last, with a form feed
    if len(pages) > MAX_PDF_PAGES:
        raise Refused(f"PDF has {len(pages)} pages; more than the {MAX_PDF_PAGES} page limit")
    return pages


# ---------------------------------------------------------------- dispatch

def detect_format(path):
    suffix = Path(path).suffix.lower()
    for table in (TEXT_SUFFIXES, HTML_SUFFIXES, OFFICE_SUFFIXES):
        if suffix in table:
            return table[suffix]
    if suffix == ".pdf":
        return "pdf"
    return None


def extract(path, *, pdf_engine="auto", max_bytes=MAX_FILE_BYTES, max_chars=MAX_CHARS):
    """Read one file -> Extraction (iterate it for ordered (locator, text) segments).

    Never raises for a missing, corrupt, hostile, unsupported or image-only file: the result's status says what
    happened ("ok", "partial", "needs OCR", "needs dependency", "unsupported", "error") and warnings say why.
    """
    path = Path(path)
    result = Extraction(path=path.as_posix())
    result.format = detect_format(path) or path.suffix.lower().lstrip(".") or "unknown"
    try:
        size = path.stat().st_size
    except OSError as exc:
        result.status = ERROR
        result.warnings.append(f"cannot read file: {exc.strerror or exc}")
        return result
    if not path.is_file():
        result.status = ERROR
        result.warnings.append("not a regular file")
        return result
    result.bytes = size
    if size > max_bytes:
        result.status = ERROR
        result.warnings.append(f"file is {size} bytes; more than the {max_bytes} byte limit (raise --max-mb "
                               "only for a file you trust)")
        return result
    try:
        data = path.read_bytes()
    except OSError as exc:
        result.status = ERROR
        result.warnings.append(f"cannot read file: {exc.strerror or exc}")
        return result
    result.sha256 = hashlib.sha256(data).hexdigest()
    fmt = detect_format(path)
    suffix = path.suffix.lower()
    out = _Collector(result, max_chars)
    try:
        if suffix in LEGACY:
            result.status = UNSUPPORTED
            result.warnings.append(LEGACY[suffix])
        elif fmt is None:
            result.status = UNSUPPORTED
            result.warnings.append(f"no text reader for '{suffix or path.name}' files; supported: "
                                   ".pdf .docx .docm .xlsx .xlsm .pptx .pptm .html .htm .txt .md .csv")
        elif fmt in ("docx", "xlsx", "pptx"):
            if data.startswith(OLE_MAGIC):
                result.status = UNSUPPORTED
                result.warnings.append("this is a password-protected Office file or a legacy binary file "
                                       f"renamed {suffix}; remove the password or save it as {suffix} and run again")
            elif not data.startswith(b"PK"):
                raise Refused(f"not a {suffix} file (no zip container)")
            else:
                {"docx": read_docx, "xlsx": read_xlsx, "pptx": read_pptx}[fmt](path, out, result)
        elif fmt == "pdf":
            if b"%PDF-" not in data[:1024]:
                raise Refused("not a PDF (no %PDF- header)")
            read_pdf(path, out, result, pdf_engine)
        elif fmt == "html":
            read_html(data, out, result)
        else:
            read_text(data, out, result)
    except Refused as exc:
        result.status = UNSUPPORTED if isinstance(exc, Unsupported) else ERROR
        result.warnings.append(str(exc))
        result.segments = []
        return result
    except RecursionError:
        result.status = ERROR
        result.warnings.append("document structure nested too deeply; refused")
        result.segments = []
        return result
    if out.full and result.status == OK:
        result.status = PARTIAL
    return result


# ---------------------------------------------------------------- CLI

def render_text(result):
    engine = " ".join(x for x in (result.engine, result.engine_version) if x)
    lines = [f"# {EXTRACTOR} {VERSION} | file: {Path(result.path).name} | sha256: {result.sha256 or '-'} | "
             f"format: {result.format} | status: {result.status} | engine: {engine}"]
    lines += [f"# warning: {w}" for w in result.warnings]
    for locator, text in result.segments:
        lines += ["", f"## {locator}", text]
    return "\n".join(lines) + "\n"


def out_names(results):
    """One output name per input, deterministic; colliding names get the file hash (then a counter) appended."""
    counts = {}
    for r in results:
        key = Path(r.path).name.lower()
        counts[key] = counts.get(key, 0) + 1
    names, used = [], set()
    for r in results:
        base = Path(r.path).name
        name = base + ".txt" if counts[base.lower()] == 1 else f"{base}-{(r.sha256 or 'missing')[:12]}.txt"
        n = 1
        while name.lower() in used or name.lower() == "manifest.json":
            n += 1
            name = f"{base}-{(r.sha256 or 'missing')[:12]}-{n}.txt"
        used.add(name.lower())
        names.append(name)
    return names


def expand_inputs(args):
    """Folders become their files (recursively, sorted); an unmatched wildcard is expanded here for shells
    (Windows cmd/PowerShell) that pass it through. Order is deterministic."""
    files = []
    for arg in args:
        path = Path(arg)
        if path.is_dir():
            files += sorted((p for p in path.rglob("*") if p.is_file()), key=lambda p: p.as_posix())
        elif not path.exists() and any(ch in arg for ch in "*?["):
            matches = sorted(Path(m) for m in __import__("glob").glob(arg, recursive=True))
            files += [m for m in matches if m.is_file()] or [path]
        else:
            files.append(path)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="documents to read")
    ap.add_argument("--out", required=True, help="folder for one .txt per input and manifest.json")
    ap.add_argument("--pdf-engine", choices=("auto", "pypdf", "pdftotext"), default="auto",
                    help="auto: pypdf if installed, else pdftotext on PATH")
    ap.add_argument("--max-mb", type=float, default=MAX_FILE_BYTES / (1024 * 1024),
                    help=f"refuse inputs larger than this (default {MAX_FILE_BYTES // (1024 * 1024)})")
    args = ap.parse_args(argv)
    if args.max_mb <= 0:
        ap.error("--max-mb must be positive")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")  # file names the console cannot show must not crash
    out = Path(args.out)
    out_resolved = out.resolve()
    files = [f for f in expand_inputs(args.files)  # never re-read our own earlier output
             if not (f.exists() and out_resolved in f.resolve().parents)]
    out.mkdir(parents=True, exist_ok=True)
    results = [extract(f, pdf_engine=args.pdf_engine, max_bytes=int(args.max_mb * 1024 * 1024)) for f in files]
    entries = []
    for result, name in zip(results, out_names(results)):
        entry = result.manifest_entry()
        if result.status != ERROR:
            (out / name).write_text(render_text(result), encoding="utf-8", newline="\n")
            entry["out"] = name
        else:
            entry["out"] = None
        entries.append(entry)
        print(f"{result.status:16} {len(result.segments):6} segments  {result.path}"
              + (f"  ({'; '.join(result.warnings)})" if result.warnings else ""))
    manifest = {"extractor": EXTRACTOR, "version": VERSION, "files": entries}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8", newline="\n")
    errors = sum(r.status == ERROR for r in results)
    print(f"{len(results)} file(s); {errors} error(s); manifest: {(out / 'manifest.json').as_posix()}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
