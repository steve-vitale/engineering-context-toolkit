"""Read the text inside plant documents (PDF, Word, Excel, PowerPoint, HTML, plain text) as ordered segments, each
with a locator a person can use to find it again ("page 3", "table 2 row 4", "sheet 'PM plan' cell B7", "slide 4").

    python scripts/extract_text.py FILE... --out DIR [--pdf-engine auto|pypdf|pdftotext] [--max-mb N]
        [--ocr auto|off] [--ocr-lang eng] [--ocr-dpi 300] [--convert-legacy] [--pdf-layout] [--excel-display]
        [--embedded on|off]

Writes one UTF-8 .txt per input (a "## <locator>" header before each segment) and DIR/manifest.json (file, sha256,
format, status, engine, segment count, warnings). Exit 0 when every file was read or its limit was reported
(needs OCR, needs pypdf, unsupported legacy format); exit 1 only on a real error (missing, unreadable, corrupt,
over a size limit); exit 2 on bad arguments.

Library use (the call a tag matcher makes):

    result = extract(path)            # -> Extraction; never raises for a bad or unsupported file
    for locator, text in result:      # same as result.segments, an ordered list of (locator, text) tuples
        ...
    result.sha256, result.status, result.warnings, result.engine, result.engine_version

Office files are read with the standard library (zipfile + ElementTree) from their XML parts only: macros and
external links are never run, opened or followed. Embedded Word/Excel/PowerPoint/PDF files inside an Office file are
read the same way (two levels deep, same limits); other embedded objects are only counted. PDF text comes from the
file's text layer through the optional pypdf package, else a `pdftotext` program; scanned pages without a
text layer are reported as needing OCR. Files are treated as untrusted: size, archive-member, member-count,
compression-ratio and DTD checks refuse hostile inputs with a clear message.

Optional add-ons, each off unless asked for and each used only when its program is installed (the default output
does not change): --ocr auto runs Tesseract on scanned PDF pages (rendered by Poppler's pdftoppm) and on .png/.jpg/
.tif images; --convert-legacy converts .doc/.xls/.ppt/.rtf with LibreOffice (soffice) in a temporary folder and
reads the result; --pdf-layout keeps PDF columns apart (pdftotext -layout, else pypdf layout mode); --excel-display
shows Excel numbers and dates as their number format displays them. Programs are found through TESSERACT_CMD /
SOFFICE_CMD (the program) or POPPLER_BIN (Poppler's folder) when set, else PATH, else on Windows their standard
install folders (Program Files, the per-user Tesseract folder, winget's Poppler package). See docs/DOCUMENT_TEXT.md.
"""
import argparse
import datetime
import functools
import hashlib
import html.parser
import io
import json
import logging
import os
import posixpath
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, localcontext
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
OCR_TIMEOUT = 300                         # one Tesseract run (one image, or one PDF page)
RENDER_TIMEOUT = 120                      # one pdftoppm page render
CONVERT_TIMEOUT = 300                     # one LibreOffice conversion
MAX_OCR_PAGES = 500                       # scanned PDF pages OCRed per file; the rest stay "needs OCR"
MAX_OCR_SIDE = 14000                      # rendered page width/height cap in pixels (cropped beyond)
MAX_OCR_PIXELS = 150_000_000              # image size cap for OCR (an E-size sheet at 300 dpi is ~135 MP)
MAX_EMBED_DEPTH = 2                       # a file embedded in a file embedded in the input is the deepest read
MAX_OLE_ENTRIES = 10000                   # directory entries in one embedded OLE container

# status values, in the order a reader should care about
OK, PARTIAL, NEEDS_OCR, NEEDS_DEPENDENCY, UNSUPPORTED, ERROR = (
    "ok", "partial", "needs OCR", "needs dependency", "unsupported", "error")
OK_OCR = "ok (ocr)"   # every page has text and some of it came from OCR (only with --ocr auto)

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
IMAGE_SUFFIXES = {".png": "png", ".jpg": "jpeg", ".jpeg": "jpeg", ".tif": "tiff", ".tiff": "tiff"}
CONVERT_TO = {".doc": "docx", ".rtf": "docx", ".xls": "xlsx", ".ppt": "pptx"}
OCR_LANG = re.compile(r"[A-Za-z0-9_]{1,32}(\+[A-Za-z0-9_]{1,32}){0,7}")
ZIP_FORMATS = (("word/document.xml", "docx"), ("xl/workbook.xml", "xlsx"), ("ppt/presentation.xml", "pptx"))

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


@dataclass(frozen=True)
class Options:
    """Optional add-ons. The defaults reproduce the plain reader exactly; see docs/DOCUMENT_TEXT.md."""
    pdf_engine: str = "auto"
    ocr: str = "off"                # "auto": OCR scanned PDF pages and image files when Tesseract is installed
    ocr_lang: str = "eng"
    ocr_dpi: int = 300
    convert_legacy: bool = False    # .doc/.xls/.ppt/.rtf through LibreOffice when it is installed
    pdf_layout: bool = False
    excel_display: bool = False
    embedded: bool = True           # read Office/PDF files embedded in Office files (only files that have them)

    def non_default(self):
        default = Options()
        return {k: getattr(self, k) for k in self.__dataclass_fields__
                if k != "pdf_engine" and getattr(self, k) != getattr(default, k)}


@dataclass
class Extraction:
    """What was read from one file. Iterating yields (locator, text) segments in document order."""
    path: str
    sha256: str = ""
    bytes: int = 0
    format: str = ""
    status: str = OK
    engine: str = "stdlib"          # "pypdf" or "pdftotext" for PDF text, "tesseract" for an OCRed image
    engine_version: str = ""        # the PDF/OCR engine version; the extractor version is VERSION
    segments: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    ocr: dict = field(default_factory=dict)         # locator -> mean word confidence (0-100) or None
    ocr_engine: str = ""            # "tesseract 5.3.0 (eng, 300 dpi)" when any segment came from OCR
    converted: str = ""             # "docx by LibreOffice 7.6.4.1" when --convert-legacy converted the file
    applied: list = field(default_factory=list)     # add-ons that changed how this file was read
    embedded: list = field(default_factory=list)    # one entry per embedded file read

    def __iter__(self):
        return iter(self.segments)

    def __len__(self):
        return len(self.segments)

    def manifest_entry(self):
        entry = {"file": self.path, "sha256": self.sha256, "bytes": self.bytes, "format": self.format,
                 "status": self.status, "extractor": f"{EXTRACTOR} {VERSION}", "engine": self.engine,
                 "engine_version": self.engine_version, "segments": len(self.segments),
                 "characters": sum(len(t) for _, t in self.segments), "warnings": list(self.warnings)}
        # add-on keys appear only when an add-on acted, so the default output is unchanged
        if self.converted:
            entry["converted"] = self.converted
        if self.ocr_engine:
            entry["ocr"] = {"engine": self.ocr_engine, "mean_word_confidence": dict(self.ocr)}
        if self.applied:
            entry["applied"] = list(self.applied)
        if self.embedded:
            entry["embedded"] = list(self.embedded)
        return entry

    def mark(self, addon):
        if addon not in self.applied:
            self.applied.append(addon)


class _Prefixed:
    """A collector view that puts the embedded file's locator in front of every segment it adds."""

    def __init__(self, out, prefix):
        self.out, self.prefix = out, prefix

    @property
    def full(self):
        return self.out.full

    def add(self, locator, text):
        self.out.add(self.prefix + locator, text)


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
        if self.parent is not None:  # an embedded package counts against the file that contains it
            self.parent.count(n)

    def __init__(self, path, parent=None):
        """`path` is a file path or, for an embedded package, a bytes buffer already read under the caps."""
        self.parent = parent
        try:
            self.zip = zipfile.ZipFile(io.BytesIO(path) if isinstance(path, bytes) else path)
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

    def inspect(self, result, macro_part, embed_prefixes, opts):
        """Warn about macros and embedded objects. Returns the embedded part names when they are to be read (the
        warning about any that cannot be is then inserted here, after reading, at the same position)."""
        names = self.names()
        if any(n.lower().endswith(macro_part) for n in names):
            result.warnings.append("contains macros (vbaProject.bin); not run and not read")
        embedded = [n for n in names if n.startswith(embed_prefixes) and not n.endswith("/")]
        if embedded and opts.embedded:
            return embedded, len(result.warnings)
        if embedded:
            result.warnings.append(f"{len(embedded)} embedded object(s) not read (e.g. {embedded[0]})")
        return [], len(result.warnings)


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


def _anchor(element, where, anchors):
    """Remember the first block that refers to each relationship id (an embedded object's place in the body)."""
    if anchors is None:
        return
    for node in element.iter():
        rid = node.get(R + "id")
        if rid and rid not in anchors:
            anchors[rid] = where


def _word_blocks(container, out, prefix, counters, anchors=None):
    """Walk a body/header/footer in order: paragraphs and tables, each with its own locator."""
    for child in container:
        if child.tag == W + "p":
            text = _word_text(child)
            if text.strip():
                counters["paragraph"] += 1
                out.add(f"{prefix}paragraph {counters['paragraph']}", text)
                _anchor(child, f"in paragraph {counters['paragraph']}", anchors)
            else:
                n = counters["paragraph"]
                _anchor(child, f"after paragraph {n}" if n else "before paragraph 1", anchors)
        elif child.tag == W + "tbl":
            counters["table"] += 1
            table = counters["table"]
            _anchor(child, f"in table {table}", anchors)
            row = 0
            for tr in child.findall(W + "tr"):  # nested tables are read inside their parent cell
                row += 1
                cells = [" ".join(_word_text(tc).split()) for tc in tr.findall(W + "tc")]
                if any(cells):
                    out.add(f"{prefix}table {table} row {row}", " | ".join(cells))
        elif child.tag == W + "sdt":
            content = child.find(W + "sdtContent")
            if content is not None:
                _word_blocks(content, out, prefix, counters, anchors)
        elif child.tag in (MC + "AlternateContent",):
            choice = child.find(MC + "Choice")
            if choice is not None:
                _word_blocks(choice, out, prefix, counters, anchors)


def _numbered(names, pattern):
    found = []
    for name in names:
        m = re.fullmatch(pattern, name)
        if m:
            found.append((int(m.group(1)), name))
    return sorted(found)


def read_docx(path, out, result, opts=None, depth=0):
    with _Package(path) as pkg:
        _read_docx(pkg, out, result, opts or Options(), depth)


def _read_docx(pkg, out, result, opts, depth):
    embeds, at = pkg.inspect(result, "vbaproject.bin", ("word/embeddings/",), opts)
    doc = pkg.xml("word/document.xml")
    if doc is None:
        raise Refused("no word/document.xml; not a Word document")
    body = doc.find(W + "body")
    anchors = {} if embeds else None
    if body is not None:
        _word_blocks(body, out, "", {"paragraph": 0, "table": 0}, anchors)
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
    if embeds:
        rels = pkg.rels("word/document.xml")
        places = {rels[rid][1]: where for rid, where in (anchors or {}).items() if rid in rels}
        _read_embedded(pkg, embeds, at, places, out, result, opts, depth)


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


def read_xlsx(path, out, result, opts=None, depth=0):
    with _Package(path) as pkg:
        _read_xlsx(pkg, out, result, opts or Options(), depth)


def _read_xlsx(pkg, out, result, opts, depth):
    embeds, at = pkg.inspect(result, "vbaproject.bin", ("xl/embeddings/",), opts)
    book = pkg.xml("xl/workbook.xml")
    if book is None:
        raise Refused("no xl/workbook.xml; not an Excel workbook")
    rels = pkg.rels("xl/workbook.xml")
    strings = next((part for kind, part in sorted(rels.values()) if kind == "sharedStrings"),
                   "xl/sharedStrings.xml")
    shared = [_si_text(si) for si in pkg.stream(strings, S + "si")]
    display = _ExcelDisplay(pkg, book, rels) if opts.excel_display else None
    places = {}
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
        if embeds:
            for _, part in sorted(pkg.rels(target[1]).values()):
                places.setdefault(part, f"on {label}")
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
                    elif kind == "n" and display is not None and value:
                        value = display.show(value, cell.get("s"))
                out.add(f"{label} cell {ref}", value)
    if display is not None:
        display.report(result)
    if embeds:
        _read_embedded(pkg, embeds, at, places, out, result, opts, depth)


def read_pptx(path, out, result, opts=None, depth=0):
    with _Package(path) as pkg:
        _read_pptx(pkg, out, result, opts or Options(), depth)


def _read_pptx(pkg, out, result, opts, depth):
    embeds, at = pkg.inspect(result, "vbaproject.bin", ("ppt/embeddings/",), opts)
    places = {}
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
            elif embeds:
                places.setdefault(part, f"on slide {number}")
    if embeds:
        _read_embedded(pkg, embeds, at, places, out, result, opts, depth)


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


# ---------------------------------------------------------------- Excel displayed values (--excel-display)

# Built-in number formats (ECMA-376 Part 1, 18.8.30). 14 and 22 follow the reader's locale in Excel; they are
# written here as ISO dates so the output does not depend on the machine that runs this.
BUILTIN_NUMFMT = {1: "0", 2: "0.00", 3: "#,##0", 4: "#,##0.00", 9: "0%", 10: "0.00%", 11: "0.00E+00",
                  14: "yyyy-mm-dd", 15: "d-mmm-yy", 16: "d-mmm", 17: "mmm-yy", 18: "h:mm AM/PM",
                  19: "h:mm:ss AM/PM", 20: "h:mm", 21: "h:mm:ss", 22: "yyyy-mm-dd hh:mm",
                  37: "#,##0 ;(#,##0)", 38: "#,##0 ;(#,##0)", 39: "#,##0.00;(#,##0.00)",
                  40: "#,##0.00;(#,##0.00)", 45: "mm:ss", 46: "[h]:mm:ss", 47: "mm:ss.0", 49: "@"}
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_COLORS = re.compile(r"(black|blue|cyan|green|magenta|red|white|yellow|color\s*\d{1,2})", re.I)


class _ExcelDisplay:
    """Applies a workbook's number formats (xl/styles.xml) to stored numbers: dates, times, percentages, fixed
    decimals, thousands separators, scientific notation and literal text. Anything else keeps its stored value
    and is counted in one warning."""

    def __init__(self, pkg, book, rels):
        pr = book.find(S + "workbookPr")
        self.date1904 = pr is not None and (pr.get("date1904") or "").lower() in ("1", "true")
        part = next((part for kind, part in sorted(rels.values()) if kind == "styles"), "xl/styles.xml")
        root = pkg.xml(part)
        self.codes, self.xf, self.kept, self.example = dict(BUILTIN_NUMFMT), [], 0, None
        if root is not None:
            fmts = root.find(S + "numFmts")
            for fmt in (fmts if fmts is not None else []):
                try:
                    self.codes[int(fmt.get("numFmtId"))] = fmt.get("formatCode") or ""
                except (TypeError, ValueError):
                    continue
            xfs = root.find(S + "cellXfs")
            for xf in (xfs if xfs is not None else []):
                try:
                    self.xf.append(int(xf.get("numFmtId") or 0))
                except ValueError:
                    self.xf.append(-1)

    def show(self, value, style):
        try:
            fmt_id = self.xf[int(style)] if style is not None else 0
        except (ValueError, IndexError):
            fmt_id = 0
        if fmt_id == 0:
            return value  # General: the stored value is what Excel shows (up to its 11-digit rounding)
        code = self.codes.get(fmt_id)
        try:
            shown = format_excel(value, code, self.date1904) if code is not None else None
        except (ArithmeticError, ValueError):  # e.g. 1E+300 with two decimals: more digits than are kept
            shown = None
        if shown is None:
            self.kept += 1
            if self.example is None:
                self.example = code if code is not None else f"numFmtId {fmt_id}"
            return value
        return shown

    def report(self, result):
        result.mark("excel display")
        if self.kept:
            result.warnings.append(f"{self.kept} number cell(s) kept their stored value: number format not applied "
                                   f"(e.g. {self.example!r})")


def _format_sections(code):
    """Split a format code into its ;-separated sections, ignoring ; inside quotes, brackets or after a backslash."""
    sections, buf, quoted, bracket, i = [], [], False, False, 0
    while i < len(code):
        ch = code[i]
        if ch == "\\" and not quoted and i + 1 < len(code):
            buf.append(code[i:i + 2])
            i += 2
            continue
        if ch == '"':
            quoted = not quoted
        elif ch == "[" and not quoted:
            bracket = True
        elif ch == "]" and not quoted:
            bracket = False
        elif ch == ";" and not quoted and not bracket:
            sections.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    sections.append("".join(buf))
    return sections


def _format_tokens(section):
    """-> list of ("lit", text) and ("code", char) items; brackets give ("elapsed", "h"|"m"|"s") or literals.
    Returns None for what is not applied here (conditions, fractions handled later, unknown brackets)."""
    items, i = [], 0
    while i < len(section):
        ch = section[i]
        if ch == '"':
            end = section.find('"', i + 1)
            if end < 0:
                return None
            items.append(("lit", section[i + 1:end]))
            i = end + 1
        elif ch == "\\" and i + 1 < len(section):
            items.append(("lit", section[i + 1]))
            i += 2
        elif ch == "_" and i + 1 < len(section):
            items.append(("lit", " "))
            i += 2
        elif ch == "*" and i + 1 < len(section):
            i += 2  # fill character: no fixed width here
        elif ch == "[":
            end = section.find("]", i)
            if end < 0:
                return None
            inner = section[i + 1:end]
            low = inner.lower()
            if low and len(set(low)) == 1 and low[0] in "hms":
                items.append(("elapsed", low[0]))
            elif inner.startswith("$"):
                symbol = inner[1:].split("-", 1)[0]
                if symbol:
                    items.append(("lit", symbol))
            elif _COLORS.fullmatch(inner):
                pass
            else:
                return None  # conditions such as [>=100] and other locale codes
            i = end + 1
        else:
            items.append(("code", ch))
            i += 1
    return items


def format_excel(value, code, date1904=False):
    """The text Excel displays for stored number `value` under format `code`, or None if not supported here."""
    try:
        number = Decimal(value)
    except (InvalidOperation, ValueError):
        return None
    if not number.is_finite():
        return None
    sections = _format_sections(code)
    sign = ""
    if number < 0 and len(sections) >= 2:
        section, number = sections[1], -number  # the section's own text (e.g. parentheses) shows the sign
    elif number == 0 and len(sections) >= 3:
        section = sections[2]
    else:
        section = sections[0]
        sign = "-" if number < 0 else ""
        number = abs(number)
    if not section.strip():
        return None  # a hidden section: keep the value rather than lose it
    items = _format_tokens(section)
    if items is None:
        return None
    codes = "".join(c for kind, c in items if kind == "code").lower()
    if codes.strip() in ("general", "@"):
        return sign + value.lstrip("-")
    if any(kind == "elapsed" for kind, _ in items) or re.search(r"[ydhs]|am/pm|a/p", codes) \
            or ("m" in codes and not re.search(r"[0#?]", codes)):
        if sign:
            return None  # Excel shows ##### for a negative date
        return _format_date(number, items, date1904)
    return _format_number(number, items, sign)


def _format_number(number, items, sign):
    pattern = set("0#?.,")
    kinds = []  # ("lit", text) | ("pat", char) | ("exp", "E+"/"E-")
    i = 0
    while i < len(items):
        kind, ch = items[i]
        if kind == "code" and ch in "Ee" and i + 1 < len(items) and items[i + 1][1] in "+-":
            kinds.append(("exp", "E" + items[i + 1][1]))
            i += 2
            continue
        if kind == "code" and ch in pattern:
            kinds.append(("pat", ch))
        elif kind == "code" and ch == "/":
            return None  # fractions are not applied
        elif kind == "code" and ch.isalpha():
            return None  # letters that are not a number placeholder
        else:
            kinds.append(("lit", ch))
        i += 1
    places = [n for n, (kind, _) in enumerate(kinds) if kind in ("pat", "exp")]
    if not places:
        return None
    first, last = places[0], places[-1]
    if any(kind == "lit" for kind, _ in kinds[first:last + 1]):
        return None  # text inside the number pattern (e.g. phone or part-number masks)
    prefix = "".join(t for _, t in kinds[:first])
    suffix = "".join(t for _, t in kinds[last + 1:])
    core = "".join(t for _, t in kinds[first:last + 1])
    percent = (prefix + suffix).count("%")
    mantissa, _, exponent = core.partition("E+") if "E+" in core else core.partition("E-")
    exp_sign = "+" if "E+" in core else "-"
    scale = len(mantissa) - len(mantissa.rstrip(","))
    mantissa = mantissa.rstrip(",")
    int_part, _, frac = mantissa.partition(".")
    if "." in frac or "," in frac:
        return None
    int_min = int_part.count("0")
    frac_min, frac_max = frac.count("0"), sum(frac.count(c) for c in "0#?")
    grouping = "," in int_part
    with localcontext() as ctx:
        ctx.prec = 80
        number = number * (Decimal(100) ** percent) / (Decimal(1000) ** scale)
        exp_text = ""
        if exponent:
            if sum(int_part.count(c) for c in "0#?") != 1:
                return None  # engineering notation is not applied
            power = number.adjusted() if number else 0
            mant = (number.scaleb(-power)).quantize(Decimal(1).scaleb(-frac_max), ROUND_HALF_UP)
            if mant >= 10:
                power += 1
                mant = (number.scaleb(-power)).quantize(Decimal(1).scaleb(-frac_max), ROUND_HALF_UP)
            number = mant
            digits = str(abs(power)).rjust(exponent.count("0"), "0")
            exp_text = "E" + ("-" if power < 0 else ("+" if exp_sign == "+" else "")) + digits
        rounded = number.quantize(Decimal(1).scaleb(-frac_max), ROUND_HALF_UP)
    text = f"{rounded:f}"
    whole, _, decimals = text.partition(".")
    decimals = decimals.rstrip("0").ljust(frac_min, "0") if frac_max else ""
    if whole == "0" and int_min == 0:
        whole = ""
    whole = whole.rjust(int_min, "0")
    if grouping and whole:
        whole = f"{int(whole):,}".rjust(int_min, "0")
    body = whole + ("." + decimals if "." in mantissa else "")  # "0.##" shows "5." for 5, as Excel does
    if rounded == 0:
        sign = ""
    return sign + prefix + body + exp_text + suffix


def _excel_datetime(number, date1904, digits):
    """Serial number -> (datetime, fraction-of-second digits string) or None outside Excel's date range."""
    if number < 0 or number >= 2958466:
        return None
    days = int(number)
    unit = Decimal(10) ** digits
    ticks = ((number - days) * 86400 * unit).quantize(Decimal(1), ROUND_HALF_UP)
    if ticks >= 86400 * unit:
        days, ticks = days + 1, ticks - 86400 * unit
    seconds, fraction = divmod(int(ticks), int(unit))
    if date1904:
        base = datetime.datetime(1904, 1, 1)
    elif days == 60:
        return None  # 29 February 1900, a day Excel counts but the calendar does not have
    else:
        base = datetime.datetime(1899, 12, 31) if days < 60 else datetime.datetime(1899, 12, 30)
    return base + datetime.timedelta(days=days, seconds=seconds), str(fraction).rjust(digits, "0") if digits else ""


def _format_date(number, items, date1904):
    tokens, i = [], 0  # ("y"|"m"|"d"|"h"|"s"|"ampm"|"ap"|"frac"|"elapsed"|"lit", text)
    while i < len(items):
        kind, ch = items[i]
        if kind == "lit":
            tokens.append(("lit", ch))
            i += 1
            continue
        if kind == "elapsed":
            tokens.append(("elapsed", ch))
            i += 1
            continue
        low = ch.lower()
        rest = "".join(c for _, c in items[i:i + 5]).lower()
        if rest.startswith("am/pm"):
            tokens.append(("ampm", "".join(c for _, c in items[i:i + 5])))
            i += 5
        elif rest.startswith("a/p"):
            tokens.append(("ap", "".join(c for _, c in items[i:i + 3])))
            i += 3
        elif low in "ymdhs":
            j = i
            while j < len(items) and items[j][0] == "code" and items[j][1].lower() == low:
                j += 1
            tokens.append((low, low * (j - i)))
            i = j
        elif ch == "." and tokens and tokens[-1][0] in ("s", "elapsed") and i + 1 < len(items) \
                and items[i + 1][1] == "0":
            j = i + 1
            while j < len(items) and items[j][1] == "0":
                j += 1
            tokens.append(("frac", "0" * (j - i - 1)))
            i = j
        elif ch.isalpha():
            return None  # e.g. Buddhist-calendar or era codes
        else:
            tokens.append(("lit", ch))
            i += 1
    digits = max((len(t) for k, t in tokens if k == "frac"), default=0)
    found = _excel_datetime(number, date1904, digits)
    if found is None:
        return None
    moment, fraction = found
    if any(k in ("y", "d") or (k == "m" and len(t) > 2) for k, t in tokens) and number < 1 and not date1904:
        return None  # a date before 1 January 1900 (Excel shows a "day 0" date)
    twelve = any(k in ("ampm", "ap") for k, _ in tokens)
    whole_seconds = int(((number * 86400 * Decimal(10) ** digits).quantize(Decimal(1), ROUND_HALF_UP))
                        // (Decimal(10) ** digits))
    out = []
    timed = [n for n, (k, _) in enumerate(tokens) if k not in ("lit",)]
    for pos, (kind, text) in enumerate(tokens):
        if kind == "lit":
            out.append(text)
        elif kind == "y":
            out.append(f"{moment.year % 100:02d}" if len(text) <= 2 else f"{moment.year:04d}")
        elif kind == "m":
            before = [tokens[n][0] for n in timed if n < pos]
            after = [tokens[n][0] for n in timed if n > pos]
            minute = len(text) <= 2 and ((before and before[-1] in ("h", "elapsed")) or (after and after[0] == "s"))
            if minute:
                out.append(f"{moment.minute:02d}" if len(text) == 2 else str(moment.minute))
            elif len(text) <= 2:
                out.append(f"{moment.month:02d}" if len(text) == 2 else str(moment.month))
            elif len(text) == 3:
                out.append(MONTHS[moment.month - 1][:3])
            elif len(text) == 4:
                out.append(MONTHS[moment.month - 1])
            else:
                out.append(MONTHS[moment.month - 1][0])
        elif kind == "d":
            if len(text) <= 2:
                out.append(f"{moment.day:02d}" if len(text) == 2 else str(moment.day))
            else:
                name = WEEKDAYS[moment.weekday()]
                out.append(name[:3] if len(text) == 3 else name)
        elif kind == "h":
            hour = moment.hour % 12 or 12 if twelve else moment.hour
            out.append(f"{hour:02d}" if len(text) >= 2 else str(hour))
        elif kind == "s":
            out.append(f"{moment.second:02d}" if len(text) >= 2 else str(moment.second))
        elif kind == "frac":
            out.append("." + fraction[:len(text)])
        elif kind == "elapsed":
            total = {"h": whole_seconds // 3600, "m": whole_seconds // 60, "s": whole_seconds}[text]
            out.append(str(total).rjust(2, "0") if text != "h" else str(total))
        elif kind == "ampm":
            pm = moment.hour >= 12
            out.append(("PM" if pm else "AM") if text[:1].isupper() else ("pm" if pm else "am"))
        elif kind == "ap":
            pm = moment.hour >= 12
            out.append(("P" if pm else "A") if text[:1].isupper() else ("p" if pm else "a"))
    # after an elapsed hour/minute, the following minutes/seconds are of the remainder, which moment already gives
    return "".join(out)


# ---------------------------------------------------------------- embedded files (Office/PDF inside Office)

class _Cfb:
    """Bounded, read-only reader for the OLE compound files Office wraps embedded objects in (MS-CFB). Only named
    streams are read; every sector chain is checked against the file size and for loops."""
    END, FREE = 0xFFFFFFFE, 0xFFFFFFFF

    def __init__(self, data):
        if len(data) < 512 or not data.startswith(OLE_MAGIC):
            raise Refused("not an OLE compound file")
        shift = int.from_bytes(data[30:32], "little")
        if shift not in (9, 12) or int.from_bytes(data[32:34], "little") != 6:
            raise Refused("OLE compound file has an invalid sector size")
        self.data, self.size = data, 1 << shift
        self.sectors = max(0, (len(data) - self.size) // self.size)
        u32 = lambda off: int.from_bytes(data[off:off + 4], "little")  # noqa: E731
        fat_count, dir_start, self.cutoff = u32(44), u32(48), u32(56)
        mini_start, mini_count, difat_start, difat_count = u32(60), u32(64), u32(68), u32(72)
        if fat_count > self.sectors or difat_count > self.sectors or mini_count > self.sectors:
            raise Refused("OLE compound file header declares more sectors than the file has")
        fat_sectors = [u32(76 + 4 * k) for k in range(109)]
        sector, seen = difat_start, set()
        for _ in range(difat_count):
            if sector >= self.sectors or sector in seen:
                raise Refused("OLE compound file has a broken sector list")
            seen.add(sector)
            block = self._sector(sector)
            fat_sectors += [int.from_bytes(block[k:k + 4], "little") for k in range(0, self.size - 4, 4)]
            sector = int.from_bytes(block[-4:], "little")
        self.fat = []
        for sector in fat_sectors[:fat_count]:
            if sector >= self.sectors:
                raise Refused("OLE compound file has a broken sector list")
            block = self._sector(sector)
            self.fat += [int.from_bytes(block[k:k + 4], "little") for k in range(0, self.size, 4)]
        directory = self._chain_bytes(self.fat, dir_start, self.size, self._sector, None)
        self.entries = []
        for off in range(0, min(len(directory), 128 * MAX_OLE_ENTRIES), 128):
            entry = directory[off:off + 128]
            name_len = min(int.from_bytes(entry[64:66], "little"), 64)
            name = entry[:max(0, name_len - 2)].decode("utf-16-le", "replace")
            kind, start = entry[66], int.from_bytes(entry[116:120], "little")
            length = int.from_bytes(entry[120:128], "little")
            if self.size == 512:
                length &= 0xFFFFFFFF
            self.entries.append((name, kind, start, length))
        root = next((e for e in self.entries if e[1] == 5), None)
        self.mini = b""
        self.minifat = []
        if root is not None and root[3]:
            self.mini = self._chain_bytes(self.fat, root[2], self.size, self._sector, root[3])
            raw = self._chain_bytes(self.fat, mini_start, self.size, self._sector, mini_count * self.size)
            self.minifat = [int.from_bytes(raw[k:k + 4], "little") for k in range(0, len(raw), 4)]

    def _sector(self, n):
        return self.data[(n + 1) * self.size:(n + 2) * self.size]

    def _mini_sector(self, n):
        return self.mini[n * 64:(n + 1) * 64]

    def _chain_bytes(self, table, start, size, read, length):
        limit = len(self.data) // size + 1 if read == self._sector else len(self.mini) // 64 + 1
        parts, sector, seen = [], start, set()
        while sector not in (self.END, self.FREE):
            if sector >= len(table) or sector in seen or len(seen) > limit:
                raise Refused("OLE compound file has a broken or looping sector chain")
            seen.add(sector)
            parts.append(read(sector))
            if length is not None and len(parts) * size >= length:
                break
            sector = table[sector]
        data = b"".join(parts)
        if length is not None:
            if len(data) < length:
                raise Refused("OLE compound file stream is shorter than declared")
            data = data[:length]
        return data

    def stream(self, name):
        for entry_name, kind, start, length in self.entries:
            if kind == 2 and entry_name.lower() == name.lower():
                if length > MAX_MEMBER_BYTES:
                    raise Refused(f"embedded stream {name!r} is larger than the {MAX_MEMBER_BYTES} byte limit")
                if length < self.cutoff:
                    return self._chain_bytes(self.minifat, start, 64, self._mini_sector, length)
                return self._chain_bytes(self.fat, start, self.size, self._sector, length)
        return None


def _ole10native(buf):
    """(file name, bytes) from an OLE Packager stream (how Office embeds an arbitrary file such as a PDF)."""
    try:
        pos = 6
        ends = []
        for _ in range(2):  # label, then original path: NUL-terminated ANSI strings
            end = buf.index(b"\x00", pos)
            ends.append(buf[pos:end])
            pos = end + 1
        pos += 4
        temp_len = int.from_bytes(buf[pos:pos + 4], "little")
        pos += 4 + temp_len
        size = int.from_bytes(buf[pos:pos + 4], "little")
        pos += 4
        if size > len(buf) - pos or pos > len(buf):
            return None
        name = (ends[0] or ends[1]).decode("cp1252", "replace")
        return name, buf[pos:pos + size]
    except ValueError:
        return None


def _display_name(name, fallback):
    name = re.split(r"[\\/]", name or "")[-1]
    name = "".join(ch for ch in name if ch.isprintable()).strip()[:120]
    return name or fallback


def _embedded_payload(data, part):
    """-> (display name, "zip"|"pdf", bytes) for an embedded Office/PDF file, else None (not readable here)."""
    name = posixpath.basename(part)
    if data.startswith(b"PK"):
        return name, "zip", data
    if b"%PDF-" in data[:1024]:
        return name, "pdf", data
    if not data.startswith(OLE_MAGIC):
        return None
    cfb = _Cfb(data)
    native = cfb.stream("\x01Ole10Native")
    if native is not None:
        found = _ole10native(native)
        if found is not None:
            inner = _embedded_payload(found[1], found[0] or part)
            if inner is not None:
                return _display_name(found[0], name), inner[1], inner[2]
    for stream in ("Package", "CONTENTS"):
        payload = cfb.stream(stream)
        if payload is not None and (payload.startswith(b"PK") or b"%PDF-" in payload[:1024]):
            return name, "zip" if payload.startswith(b"PK") else "pdf", payload
    return None


def _root_collector(out):
    while isinstance(out, _Prefixed):
        out = out.out
    return out


def _merge_status(result, sub_status):
    if sub_status == OK_OCR and result.status == OK:
        result.status = OK_OCR
    elif sub_status not in (OK, OK_OCR) and result.status in (OK, OK_OCR):
        result.status = PARTIAL


def _read_embedded(pkg, parts, at, places, out, result, opts, depth):
    """Read the Office/PDF files embedded in `pkg` with the same readers and limits, each segment's locator
    prefixed with the file and its place: "embedded 'spec.pdf' (in table 3) page 2". Objects that are not
    Office/PDF files (or are nested too deep) are counted in one warning at position `at`, as before."""
    order = {part: n for n, part in enumerate(places)}
    unread, too_deep = [], []
    for part in sorted(parts, key=lambda n: (order.get(n, len(order)), n)):
        if depth + 1 > MAX_EMBED_DEPTH:
            too_deep.append(part)
            continue
        where = places.get(part)
        fallback = posixpath.basename(part)
        label = f"embedded '{fallback}'" + (f" ({where})" if where else "")
        try:
            found = _embedded_payload(pkg.read(part), part)
            if found is None:
                unread.append(part)
                continue
            name, kind, payload = found
            label = f"embedded '{name.replace(chr(39), chr(39) * 2)}'" + (f" ({where})" if where else "")
            sub = Extraction(path=name, sha256=hashlib.sha256(payload).hexdigest(), bytes=len(payload))
            root = _root_collector(out)
            mark = (len(root.result.segments), root.left, root.full, len(root.result.warnings))
            sub_out = _Prefixed(out, label + " ")
            try:
                if kind == "pdf":
                    sub.format = "pdf"
                    with _temp_dir() as tmp:
                        copy = Path(tmp) / "embedded.pdf"
                        copy.write_bytes(payload)
                        read_pdf(copy, sub_out, sub, opts.pdf_engine, opts)
                else:
                    with _Package(payload, parent=pkg) as inner:
                        sub.format = next((fmt for marker, fmt in ZIP_FORMATS if marker in inner.info), "")
                        if not sub.format:
                            unread.append(part)
                            continue
                        {"docx": _read_docx, "xlsx": _read_xlsx, "pptx": _read_pptx}[sub.format](
                            inner, sub_out, sub, opts, depth + 1)
            except (Refused, RecursionError) as exc:
                # like a top-level file: nothing from a refused embedded file is kept
                del root.result.segments[mark[0]:]
                del root.result.warnings[mark[3]:]
                root.left, root.full = mark[1], mark[2]
                sub.status = UNSUPPORTED if isinstance(exc, Unsupported) else ERROR
                sub.warnings = [str(exc) if isinstance(exc, Refused) else "document structure nested too deeply"]
        except Refused as exc:
            result.warnings.append(f"{label}: not read: {exc}")
            _merge_status(result, ERROR)
            continue
        result.warnings += [f"{label}: {w}" for w in sub.warnings]
        _merge_status(result, sub.status)
        for loc, conf in sub.ocr.items():
            result.ocr[f"{label} {loc}"] = conf
        result.ocr_engine = result.ocr_engine or sub.ocr_engine
        for addon in sub.applied:
            result.mark(addon)
        result.embedded.append({"locator": label, "name": name, "format": sub.format, "sha256": sub.sha256,
                                "bytes": sub.bytes, "status": sub.status,
                                "engine": " ".join(x for x in (sub.engine, sub.engine_version) if x)})
        result.embedded += [dict(e, locator=f"{label} {e['locator']}") for e in sub.embedded]
    notes = []
    if unread:
        notes.append(f"{len(unread)} embedded object(s) not read (e.g. {unread[0]})")
    if too_deep:
        notes.append(f"{len(too_deep)} embedded object(s) not read: more than {MAX_EMBED_DEPTH} levels deep "
                     f"(e.g. {too_deep[0]})")
    result.warnings[at:at] = notes


# ---------------------------------------------------------------- external programs (optional add-ons)

def _temp_dir():
    """A private temporary folder removed afterwards, even after an error or a killed program."""
    return tempfile.TemporaryDirectory(prefix="extract_text_", ignore_cleanup_errors=True)


def _kill_tree(proc):
    """End a program and everything it started (LibreOffice starts a second process; a timeout must end both)."""
    try:
        if os.name == "nt":
            taskkill = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "taskkill.exe"
            subprocess.run([str(taskkill), "/F", "/T", "/PID", str(proc.pid)], capture_output=True, timeout=30)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        proc.kill()
    except OSError:
        pass


def _run(cmd, timeout, env=None):
    """Run a program from an argument list (never through a shell) with no input, in its own process group, and
    end the whole group if it runs longer than `timeout` seconds (raises subprocess.TimeoutExpired)."""
    kwargs = {"stdin": subprocess.DEVNULL, "stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "env": env}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | getattr(subprocess, "CREATE_NO_WINDOW", 0)
    else:
        kwargs["start_new_session"] = True
    proc = subprocess.Popen(cmd, **kwargs)
    try:
        out, err = proc.communicate(timeout=timeout)
    except BaseException:
        _kill_tree(proc)
        try:
            proc.communicate(timeout=30)
        except (subprocess.SubprocessError, OSError, ValueError):
            pass
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


@functools.lru_cache(maxsize=None)
def _tool_version(binary, flag, pattern):
    try:
        run = _run([binary, flag], 60)
    except (OSError, subprocess.SubprocessError):
        return "?"
    m = re.search(pattern.encode(), run.stdout + run.stderr)
    return m.group(1).decode("ascii", "replace") if m else "?"


def _last_line(run):
    lines = (run.stderr or b"").decode("utf-8", "replace").strip().splitlines()
    return lines[-1] if lines else f"exit {run.returncode}"


# Where an add-on program is looked for, in order: an environment override set by the operator, PATH, then a fixed
# list of standard install folders (Windows installers for Tesseract, Poppler and LibreOffice do not add themselves
# to PATH). Paths are never taken from a document.
TOOL_ENV = {"tesseract": "TESSERACT_CMD", "soffice": "SOFFICE_CMD",   # the program file
            "pdftoppm": "POPPLER_BIN", "pdftotext": "POPPLER_BIN"}    # the folder holding Poppler's programs


def _version_key(path):
    return tuple(int(n) for n in re.findall(r"\d+", Path(path).name)[:4])


def _standard_locations(name):
    """Fixed install locations for an add-on program on Windows, newest Poppler first; nothing elsewhere."""
    if os.name != "nt":
        return []
    roots = [os.environ.get(v) for v in ("ProgramFiles", "ProgramFiles(x86)", "ProgramW6432")]
    roots = [Path(r) for r in dict.fromkeys(roots) if r]
    local = Path(os.environ["LOCALAPPDATA"]) if os.environ.get("LOCALAPPDATA") else None
    found = []
    if name == "tesseract":  # UB Mannheim installer: all users, or just me
        found += [r / "Tesseract-OCR" / "tesseract.exe" for r in roots]
        found += [local / "Programs" / "Tesseract-OCR" / "tesseract.exe"] if local else []
    elif name == "soffice":
        found += [r / "LibreOffice" / "program" / exe for r in roots for exe in ("soffice.com", "soffice.exe")]
    elif name in ("pdftoppm", "pdftotext"):
        folders = []
        if local:  # winget installs Poppler as a package folder; its Links folder may or may not hold a shim
            folders.append(local / "Microsoft" / "WinGet" / "Links")
            packages = local / "Microsoft" / "WinGet" / "Packages"
            folders += sorted(packages.glob("oschwartz10612.Poppler_*/poppler-*/Library/bin"),
                              key=lambda b: _version_key(b.parent.parent), reverse=True)
        for r in roots:  # an unzipped release (poppler-25.07.0/Library/bin) under Program Files
            folders += sorted(r.glob("poppler*/Library/bin"), key=lambda b: _version_key(b.parent.parent),
                              reverse=True)
        found += [f / f"{name}.exe" for f in folders]
    return [str(p) for p in found]


def _find_tool(name):
    """The add-on program to run, or None: the TOOL_ENV override if set (and only it), else PATH, else a standard
    install folder."""
    var = TOOL_ENV.get(name)
    override = os.environ.get(var, "").strip().strip('"') if var else ""
    if override:
        if var == "POPPLER_BIN":
            return shutil.which(name, path=override)
        allowed = (name, "libreoffice") if name == "soffice" else (name,)  # the variable names a program, nothing else
        return shutil.which(override) if Path(override).name.lower().split(".")[0] in allowed else None
    found = shutil.which(name) or (shutil.which("libreoffice") if name == "soffice" else None)
    if found:
        return found
    for candidate in _standard_locations(name):
        if Path(candidate).is_file():
            return candidate
    return None


def _not_found(name, install):
    var = TOOL_ENV[name]
    return f"no {name} program found (on PATH, in {var} or the standard install folder; install {install})"


def _tesseract():
    """The tesseract program (_find_tool), else the one pytesseract is configured to use (pytesseract runs it too)."""
    found = _find_tool("tesseract")
    if found or os.environ.get("TESSERACT_CMD", "").strip():
        return found
    try:
        import pytesseract  # optional; only to find a configured tesseract program
    except ImportError:
        return None
    cmd = getattr(getattr(pytesseract, "pytesseract", None), "tesseract_cmd", None)
    return shutil.which(cmd) if isinstance(cmd, str) and cmd else None


def _ocr_file(tess, image, opts, dpi=None):
    """OCR one image file -> {page number: (text, mean word confidence or None)}."""
    cmd = [tess, str(Path(image).resolve()), "stdout", "-l", opts.ocr_lang, "--psm", "3"]
    if dpi:
        cmd += ["--dpi", str(dpi)]
    env = dict(os.environ, OMP_THREAD_LIMIT="1")  # one thread: the same image gives the same text
    try:
        run = _run(cmd + ["tsv"], OCR_TIMEOUT, env)
    except subprocess.TimeoutExpired:
        raise Refused(f"tesseract did not finish within {OCR_TIMEOUT} s") from None
    except OSError as exc:
        raise Refused(f"tesseract could not run: {exc}") from None
    if run.returncode != 0:
        raise Refused("tesseract could not read the image: " + _last_line(run))
    return parse_tesseract_tsv(run.stdout.decode("utf-8", "replace"))


def parse_tesseract_tsv(tsv):
    """Tesseract TSV output -> {page: (text, mean word confidence)}; lines, paragraphs and blocks keep their breaks."""
    pages = {}
    for row in tsv.splitlines()[1:]:
        cols = row.split("\t")
        if len(cols) < 12 or cols[0] != "5" or not cols[11].strip():
            continue
        try:
            page, key, conf = int(cols[1]), tuple(int(c) for c in cols[2:5]), float(cols[10])
        except ValueError:
            continue
        pages.setdefault(page, []).append((key, cols[11].strip(), conf))
    out = {}
    for page, words in sorted(pages.items()):
        parts, previous = [], None
        for key, word, _ in words:
            if previous is not None:
                parts.append(" " if key == previous else ("\n\n" if key[0] != previous[0] else "\n"))
            parts.append(word)
            previous = key
        confs = [c for _, _, c in words if c >= 0]
        out[page] = ("".join(parts), round(sum(confs) / len(confs), 1) if confs else None)
    return out


def image_size(data, fmt):
    """[(width, height), ...] per page from a PNG, JPEG or TIFF header, without decoding the image."""
    import struct
    if fmt == "png":
        if not data.startswith(b"\x89PNG\r\n\x1a\n") or data[12:16] != b"IHDR":
            raise Refused("not a PNG file")
        return [struct.unpack(">II", data[16:24])]
    if fmt == "jpeg":
        if not data.startswith(b"\xff\xd8"):
            raise Refused("not a JPEG file")
        i = 2
        while i + 9 <= len(data):
            if data[i] != 0xFF:
                raise Refused("JPEG file structure is broken")
            marker = data[i + 1]
            if marker == 0xFF:
                i += 1
                continue
            if marker in (0x01, 0xD8) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                height, width = struct.unpack(">HH", data[i + 5:i + 9])
                return [(width, height)]
            i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
        raise Refused("JPEG file has no image size")
    order = {b"II": "<", b"MM": ">"}.get(data[:2])
    if order is None or struct.unpack(order + "H", data[2:4])[0] != 42:
        raise Refused("not a TIFF file (or a BigTIFF, which is not read)")
    sizes, offset, seen = [], struct.unpack(order + "I", data[4:8])[0], set()
    while offset and offset not in seen and len(sizes) <= MAX_OCR_PAGES:
        seen.add(offset)
        if offset + 2 > len(data):
            raise Refused("TIFF file structure is broken")
        count = struct.unpack(order + "H", data[offset:offset + 2])[0]
        width = height = 0
        for k in range(count):
            entry = data[offset + 2 + 12 * k:offset + 14 + 12 * k]
            if len(entry) < 12:
                raise Refused("TIFF file structure is broken")
            tag, kind = struct.unpack(order + "HH", entry[:4])
            value = struct.unpack(order + ("H" if kind == 3 else "I"), entry[8:10] if kind == 3 else entry[8:12])[0]
            if tag == 256:
                width = value
            elif tag == 257:
                height = value
        sizes.append((width, height))
        end = offset + 2 + 12 * count
        offset = struct.unpack(order + "I", data[end:end + 4])[0] if end + 4 <= len(data) else 0
    return sizes


def read_image(data, suffix, out, result, opts):
    """OCR an image file (only with --ocr auto). Each page of a multi-page TIFF is "page N"; a PNG/JPEG is page 1."""
    sizes = image_size(data, IMAGE_SUFFIXES[suffix])
    if len(sizes) > MAX_OCR_PAGES:
        raise Refused(f"image has more than {MAX_OCR_PAGES} pages")
    for n, (width, height) in enumerate(sizes, 1):
        if not width or not height or width * height > MAX_OCR_PIXELS:
            raise Refused(f"image page {n} is {width} x {height} pixels; OCR is limited to {MAX_OCR_PIXELS} pixels")
    tess = _tesseract()
    if tess is None:
        result.status = NEEDS_DEPENDENCY
        result.warnings.append("image text needs OCR: " + _not_found("tesseract", "Tesseract OCR"))
        return
    version = _tool_version(tess, "--version", r"tesseract v?([\w.\-]+)")
    result.engine, result.engine_version = "tesseract", version
    result.ocr_engine = f"tesseract {version} ({opts.ocr_lang})"
    with _temp_dir() as tmp:
        copy = Path(tmp) / ("image" + suffix)  # the bytes that were hashed, under a name no program can misread
        copy.write_bytes(data)
        pages = _ocr_file(tess, copy, opts)
    empty = []
    for n in range(1, len(sizes) + 1):
        text, conf = pages.get(n, ("", None))
        if text.strip():
            out.add(f"page {n}", text)
            result.ocr[f"page {n}"] = conf
        else:
            empty.append(n)
    result.mark("ocr")
    if empty:
        result.warnings.append(f"OCR found no text: page{'s' if len(empty) > 1 else ''} {_ranges(empty)} of "
                               f"{len(sizes)} (a blank page, or an image OCR could not read)")
    result.status = OK_OCR if not empty else (NEEDS_OCR if len(empty) == len(sizes) else PARTIAL)


def _ocr_pdf(path, pages, result, opts):
    """Render each listed page with pdftoppm and OCR it. -> ({page: (text, conf)}, [pages OCR found empty],
    [pages not OCRed]) or None when a program is missing (a warning says which)."""
    tess, ppm = _tesseract(), _find_tool("pdftoppm")
    missing = ([] if tess else [_not_found("tesseract", "Tesseract OCR")]) + \
              ([] if ppm else [_not_found("pdftoppm", "Poppler") + " to render PDF pages"])
    if missing:
        result.warnings.append("OCR not run: " + "; ".join(missing))
        return None
    todo, skipped = pages[:MAX_OCR_PAGES], pages[MAX_OCR_PAGES:]
    if skipped:
        result.warnings.append(f"OCR stopped after {MAX_OCR_PAGES} pages")
    texts, empty, failed = {}, [], list(skipped)
    with _temp_dir() as tmp:
        # the programs only ever see fixed names in a private folder: no option-like or shell-special file names
        source = str(Path(tmp) / "source.pdf")
        try:
            shutil.copyfile(path, source)
        except OSError as exc:
            result.warnings.append(f"OCR not run: the PDF could not be copied to a temporary folder ({exc})")
            return None
        version = _tool_version(tess, "--version", r"tesseract v?([\w.\-]+)")
        ppm_version = _tool_version(ppm, "-v", r"version ([\w.\-]+)")
        result.ocr_engine = (f"tesseract {version} ({opts.ocr_lang}, {opts.ocr_dpi} dpi; pages rendered by "
                             f"pdftoppm {ppm_version})")
        for n in todo:
            base = Path(tmp) / f"page{n}"
            image = base.with_name(base.name + ".png")
            try:
                run = _run([ppm, "-r", str(opts.ocr_dpi), "-gray", "-png", "-singlefile", "-f", str(n), "-l", str(n),
                            "-W", str(MAX_OCR_SIDE), "-H", str(MAX_OCR_SIDE), source, str(base)], RENDER_TIMEOUT)
                if run.returncode != 0 or not image.is_file():
                    raise Refused("pdftoppm could not render it: " + _last_line(run))
                with open(image, "rb") as stream:
                    width, height = image_size(stream.read(32), "png")[0]
                if max(width, height) >= MAX_OCR_SIDE:
                    result.warnings.append(f"page {n}: rendered image cropped at {MAX_OCR_SIDE} pixels; lower "
                                           "--ocr-dpi to OCR the whole page")
                got = _ocr_file(tess, image, opts, opts.ocr_dpi).get(1, ("", None))
            except subprocess.TimeoutExpired:
                result.warnings.append(f"page {n}: pdftoppm did not finish within {RENDER_TIMEOUT} s; not OCRed")
                failed.append(n)
                continue
            except (Refused, OSError) as exc:
                result.warnings.append(f"page {n}: not OCRed: {exc}")
                failed.append(n)
                continue
            finally:
                try:
                    image.unlink(missing_ok=True)  # one page image at a time; the folder goes afterwards
                except OSError:
                    pass
            if got[0].strip():
                texts[n] = got
            else:
                empty.append(n)
    return texts, empty, failed


def _soffice():
    return _find_tool("soffice")


@functools.lru_cache(maxsize=None)
def _soffice_version(soffice):
    with _temp_dir() as tmp:
        try:
            run = _run([soffice, f"-env:UserInstallation={(Path(tmp) / 'profile').as_uri()}", "--version"], 120)
        except (OSError, subprocess.SubprocessError):
            return "?"
    m = re.search(rb"LibreOffice ([\d.]+)", run.stdout + run.stderr)
    return m.group(1).decode("ascii") if m else "?"


def read_converted(data, suffix, out, result, opts, max_bytes):
    """--convert-legacy: convert a .doc/.xls/.ppt/.rtf copy with LibreOffice in a private temporary folder (its own
    profile, no window), then read the converted file with the normal reader."""
    soffice = _soffice()
    if soffice is None:
        result.status = UNSUPPORTED
        result.warnings += [LEGACY[suffix], "--convert-legacy: no LibreOffice (soffice) program found (on PATH, in "
                                            "SOFFICE_CMD or the standard install folder)"]
        return
    target = CONVERT_TO[suffix]
    version = _soffice_version(soffice)
    with _temp_dir() as tmp:
        tmp = Path(tmp)
        source, folder, profile = tmp / ("source" + suffix), tmp / "out", tmp / "profile"
        source.write_bytes(data)  # the bytes that were hashed, under a fixed name
        folder.mkdir()
        cmd = [soffice, f"-env:UserInstallation={profile.as_uri()}", "--headless", "--invisible", "--nologo",
               "--norestore", "--nolockcheck", "--nodefault", "--convert-to", target, "--outdir", str(folder),
               str(source)]
        try:
            run = _run(cmd, CONVERT_TIMEOUT)
        except subprocess.TimeoutExpired:
            raise Refused(f"LibreOffice did not finish converting within {CONVERT_TIMEOUT} s") from None
        except OSError as exc:
            raise Refused(f"LibreOffice could not run: {exc}") from None
        produced = folder / f"source.{target}"
        if not produced.is_file():
            raise Unsupported(f"LibreOffice did not convert the file ({_last_line(run)}); "
                              + LEGACY[suffix].split("; ", 1)[-1])
        if produced.stat().st_size > max_bytes:
            raise Refused(f"converted file is larger than the {max_bytes} byte limit")
        result.converted = f"{target} by LibreOffice {version}"
        result.mark("convert legacy")
        result.warnings.append(f"converted from {suffix} to .{target} by LibreOffice {version}; locators refer to "
                               "the converted file (paragraph and table numbers can differ from the original)")
        {"docx": read_docx, "xlsx": read_xlsx, "pptx": read_pptx}[target](produced, out, result, opts, 0)


# ---------------------------------------------------------------- PDF (text layer, optional OCR)

def _pypdf():
    try:
        import pypdf  # optional; see docs/DEPENDENCIES.md
    except ImportError:
        return None
    return pypdf


def read_pdf(path, out, result, engine="auto", opts=None):
    opts = opts or Options()
    pypdf = _pypdf() if engine in ("auto", "pypdf") else None
    binary = _find_tool("pdftotext") if engine in ("auto", "pdftotext") else None
    if opts.pdf_layout and engine == "auto" and binary:
        pypdf = None  # layout mode prefers pdftotext -layout, which keeps columns apart best
    if pypdf is not None:
        pages = _pdf_pypdf(pypdf, path, result, opts.pdf_layout)
    elif binary:
        pages = _pdf_pdftotext(binary, path, result, opts.pdf_layout)
    else:
        result.status = NEEDS_DEPENDENCY
        need = {"pypdf": "pypdf is not installed", "pdftotext": _not_found("pdftotext", "Poppler")}.get(engine)
        result.warnings.append("PDF text needs pypdf (pip install pypdf)"
                               + (f"; {need}" if need else " or a pdftotext program (Poppler)"))
        return
    if opts.pdf_layout:
        result.mark("pdf layout")
    if not pages:
        result.warnings.append("PDF has no pages")
    blank = [n for n, text in enumerate(pages, 1) if not text.strip()]
    ocr, empty, not_ocred = {}, [], blank
    if blank and opts.ocr == "auto":
        got = _ocr_pdf(path, blank, result, opts)
        if got is not None:
            ocr, empty, not_ocred = got
            result.mark("ocr")
    for n, text in enumerate(pages, 1):
        if n in ocr:
            out.add(f"page {n}", ocr[n][0])
            result.ocr[f"page {n}"] = ocr[n][1]
        elif text.strip():
            out.add(f"page {n}", text)
    if not_ocred:
        result.warnings.append(f"no text layer, needs OCR: page{'s' if len(not_ocred) > 1 else ''} "
                               + _ranges(not_ocred) + f" of {len(pages)}")
    if empty:
        result.warnings.append(f"OCR found no text: page{'s' if len(empty) > 1 else ''} {_ranges(empty)} of "
                               f"{len(pages)} (a blank page, or an image OCR could not read)")
    unresolved = len(not_ocred) + len(empty)
    if unresolved:
        result.status = NEEDS_OCR if unresolved == len(pages) else PARTIAL
    elif ocr:
        result.status = OK_OCR


def _ranges(numbers):
    spans, start = [], numbers[0]
    for a, b in zip(numbers, numbers[1:] + [None]):
        if b != a + 1:
            spans.append(str(start) if start == a else f"{start}-{a}")
            start = b
    return ", ".join(spans)


def _pdf_pypdf(pypdf, path, result, layout=False):
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
    if layout and "extraction_mode" not in __import__("inspect").signature(pypdf.PageObject.extract_text).parameters:
        result.warnings.append(f"pypdf {result.engine_version} has no layout mode (pypdf 3.17 or later has); "
                               "plain text order used")
        layout = False
    pages = []
    for i in range(count):
        try:
            page = reader.pages[i]
            pages.append((page.extract_text(extraction_mode="layout") if layout else page.extract_text()) or "")
        except Exception as exc:
            result.warnings.append(f"page {i + 1}: text could not be read ({type(exc).__name__}: {exc})")
            pages.append("")
    return pages


def _pdf_pdftotext(binary, path, result, layout=False):
    result.engine = "pdftotext"
    try:
        ver = subprocess.run([binary, "-v"], capture_output=True, timeout=30)
        m = re.search(rb"version ([\w.\-]+)", ver.stdout + ver.stderr)
        result.engine_version = m.group(1).decode() if m else "?"
        # an absolute path, so a file named like an option ("-foo.pdf") is never read as one
        run = subprocess.run([binary, "-enc", "UTF-8", "-eol", "unix"] + (["-layout"] if layout else [])
                             + [str(Path(path).resolve()), "-"], capture_output=True, timeout=PDFTOTEXT_TIMEOUT)
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


def _refused(result, status, message):
    """Nothing read from a refused file is kept: no text, no OCR confidences, no embedded-file entries."""
    result.status = status
    result.warnings.append(message)
    result.segments, result.ocr, result.embedded = [], {}, []
    return result


def extract(path, *, pdf_engine="auto", max_bytes=MAX_FILE_BYTES, max_chars=MAX_CHARS, ocr="off", ocr_lang="eng",
            ocr_dpi=300, convert_legacy=False, pdf_layout=False, excel_display=False, embedded=True):
    """Read one file -> Extraction (iterate it for ordered (locator, text) segments).

    Never raises for a missing, corrupt, hostile, unsupported or image-only file: the result's status says what
    happened ("ok", "ok (ocr)", "partial", "needs OCR", "needs dependency", "unsupported", "error") and warnings
    say why. The keyword add-ons (all off except `embedded`) are described in docs/DOCUMENT_TEXT.md; a bad add-on
    value raises ValueError.
    """
    opts = Options(pdf_engine=pdf_engine, ocr=ocr, ocr_lang=ocr_lang, ocr_dpi=ocr_dpi,
                   convert_legacy=convert_legacy, pdf_layout=pdf_layout, excel_display=excel_display,
                   embedded=embedded)
    if opts.ocr not in ("off", "auto"):
        raise ValueError("ocr must be 'auto' or 'off'")
    if not OCR_LANG.fullmatch(opts.ocr_lang or ""):
        raise ValueError("ocr_lang must be Tesseract language names such as 'eng' or 'eng+deu'")
    if not isinstance(opts.ocr_dpi, int) or not 70 <= opts.ocr_dpi <= 1200:
        raise ValueError("ocr_dpi must be a whole number from 70 to 1200")
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
        if suffix in LEGACY and opts.convert_legacy:
            read_converted(data, suffix, out, result, opts, max_bytes)
        elif suffix in LEGACY:
            result.status = UNSUPPORTED
            result.warnings.append(LEGACY[suffix])
        elif fmt is None and suffix in IMAGE_SUFFIXES and opts.ocr == "auto":
            read_image(data, suffix, out, result, opts)
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
                {"docx": read_docx, "xlsx": read_xlsx, "pptx": read_pptx}[fmt](path, out, result, opts)
        elif fmt == "pdf":
            if b"%PDF-" not in data[:1024]:
                raise Refused("not a PDF (no %PDF- header)")
            read_pdf(path, out, result, opts.pdf_engine, opts)
        elif fmt == "html":
            read_html(data, out, result)
        else:
            read_text(data, out, result)
    except Refused as exc:
        return _refused(result, UNSUPPORTED if isinstance(exc, Unsupported) else ERROR, str(exc))
    except RecursionError:
        return _refused(result, ERROR, "document structure nested too deeply; refused")
    except OSError as exc:  # only the add-ons write files (to a private temporary folder)
        return _refused(result, ERROR, f"an add-on step failed (temporary folder or program): {exc}")
    if out.full and result.status in (OK, OK_OCR):
        result.status = PARTIAL
    return result


# ---------------------------------------------------------------- CLI

def render_text(result):
    engine = " ".join(x for x in (result.engine, result.engine_version) if x)
    lines = [f"# {EXTRACTOR} {VERSION} | file: {Path(result.path).name} | sha256: {result.sha256 or '-'} | "
             f"format: {result.format} | status: {result.status} | engine: {engine}"]
    if result.converted:
        lines.append(f"# converted: {result.converted}")
    if result.ocr_engine:
        confidence = "; ".join(f"{loc} {'n/a' if c is None else c}" for loc, c in result.ocr.items())
        lines.append(f"# ocr: engine: {result.ocr_engine} | mean word confidence: {confidence or '-'}")
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
                    help="auto: pypdf if installed, else a pdftotext program (PATH, POPPLER_BIN or standard folder)")
    ap.add_argument("--max-mb", type=float, default=MAX_FILE_BYTES / (1024 * 1024),
                    help=f"refuse inputs larger than this (default {MAX_FILE_BYTES // (1024 * 1024)})")
    ap.add_argument("--ocr", choices=("auto", "off"), default="off",
                    help="auto: OCR scanned PDF pages (Tesseract + pdftoppm) and .png/.jpg/.tif images when the "
                         "programs are installed (default off)")
    ap.add_argument("--ocr-lang", default="eng", help="Tesseract language(s), e.g. eng or eng+deu (default eng)")
    ap.add_argument("--ocr-dpi", type=int, default=300, help="PDF page render resolution for OCR (default 300)")
    ap.add_argument("--convert-legacy", action="store_true",
                    help="convert .doc/.xls/.ppt/.rtf with LibreOffice (soffice) when installed, then read them")
    ap.add_argument("--pdf-layout", action="store_true",
                    help="keep PDF columns apart: pdftotext -layout, else pypdf layout mode")
    ap.add_argument("--excel-display", action="store_true",
                    help="show Excel numbers and dates as their number format displays them, not stored values")
    ap.add_argument("--embedded", choices=("on", "off"), default="on",
                    help="read Word/Excel/PowerPoint/PDF files embedded in Office files (default on)")
    args = ap.parse_args(argv)
    if args.max_mb <= 0:
        ap.error("--max-mb must be positive")
    if not OCR_LANG.fullmatch(args.ocr_lang):
        ap.error("--ocr-lang must be Tesseract language names such as eng or eng+deu")
    if not 70 <= args.ocr_dpi <= 1200:
        ap.error("--ocr-dpi must be from 70 to 1200")
    addons = {"ocr": args.ocr, "ocr_lang": args.ocr_lang, "ocr_dpi": args.ocr_dpi,
              "convert_legacy": args.convert_legacy, "pdf_layout": args.pdf_layout,
              "excel_display": args.excel_display, "embedded": args.embedded == "on"}
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")  # file names the console cannot show must not crash
    out = Path(args.out)
    out_resolved = out.resolve()
    files = [f for f in expand_inputs(args.files)  # never re-read our own earlier output
             if not (f.exists() and out_resolved in f.resolve().parents)]
    out.mkdir(parents=True, exist_ok=True)
    results = [extract(f, pdf_engine=args.pdf_engine, max_bytes=int(args.max_mb * 1024 * 1024), **addons)
               for f in files]
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
    manifest = {"extractor": EXTRACTOR, "version": VERSION}
    chosen = Options(**addons).non_default()
    if chosen:
        manifest["options"] = chosen  # only when an add-on was asked for, so the default manifest is unchanged
    manifest["files"] = entries
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8", newline="\n")
    errors = sum(r.status == ERROR for r in results)
    print(f"{len(results)} file(s); {errors} error(s); manifest: {(out / 'manifest.json').as_posix()}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
