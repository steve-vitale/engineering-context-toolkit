# Document text: read what procedures, PHAs and work orders say

Procedures, HACCP plans, PHAs, CAPAs, work orders and purchase orders name the same pumps, transmitters and valves
as the P&ID and the instrument index. They live in Word, Excel, PowerPoint and PDF files, which a plain text search
cannot see. `scripts/extract_text.py` reads the text inside those files and puts a locator in front of every piece,
so a tag found in a document can be traced back to the exact page, table row, cell or slide.

It is a reading step only. It does not decide what a tag means, match tags to the map, or change any source.
The [one map](ONE_MAP.md) is the intended consumer: today it reads mentions from UTF-8 text documents only.

## Run it

```sh
python scripts/extract_text.py procedures/SOP-104.docx "PM plan.xlsx" PHA/ --out doc-text
```

Arguments can be files, folders (read recursively, in sorted order) or wildcards. The output folder gets one
UTF-8 `.txt` per input (a `## <locator>` header before each piece of text) and `manifest.json` with, for each
file: the path as given, SHA-256 of its bytes, size, format, status, the extractor version, the PDF engine and its
version, the number of segments and characters, and every warning. Outputs use LF line endings and contain no
timestamps, so the same inputs give the same bytes.

Exit codes: `0` when every file was read or its limit was reported (needs OCR, needs pypdf, unsupported legacy
format, password protection); `1` when at least one file was a real error (missing, unreadable, corrupt, over a
size limit, refused as hostile); `2` for bad arguments. Errors get no `.txt`, but they are in the manifest.

Optional add-ons (each described [below](#optional-add-ons); all off by default except reading embedded files, and
none of them needs anything installed unless you turn it on):

```sh
python scripts/extract_text.py scans/ --out doc-text --ocr auto              # Tesseract on scanned pages and images
python scripts/extract_text.py old/ --out doc-text --convert-legacy          # .doc/.xls/.ppt/.rtf via LibreOffice
python scripts/extract_text.py PHA.pdf --out doc-text --pdf-layout           # keep PDF columns apart
python scripts/extract_text.py "PM plan.xlsx" --out doc-text --excel-display # dates and numbers as displayed
```

Worked example on fictional documents: `examples/document-text/make_samples.py` builds a Word procedure, an Excel
PM plan, a PowerPoint PHA review, an HTML CAPA, a work-order export and a legacy `.doc` placeholder (generated, so
no binary files are committed). The committed results are in `examples/document-text/expected/`; the test
regenerates them byte for byte.

```sh
cd examples/document-text
python make_samples.py samples
python ../../scripts/extract_text.py samples --out expected
```

## What is read, and the locators

| Format | Read from | Locator | Not read |
|---|---|---|---|
| PDF (`.pdf`) | The text layer, page by page, through optional pypdf, else a `pdftotext` program on PATH | `page 3` | Images, scanned pages (reported as needing OCR; read with `--ocr auto`), annotations and form fields |
| Word (`.docx`, `.docm`) | Body paragraphs and tables in order, text boxes, content controls, page headers and footers, footnotes, endnotes, comments, embedded Office/PDF files | `paragraph 12`, `table 2 row 4` (cells joined with ` \| `), `page header 1 paragraph 1`, `page footer 2 paragraph 1`, `footnote 3`, `comment 1`, `embedded 'spec.pdf' (in table 3) page 2` | Tracked deletions (warned), field codes, other embedded objects (counted in a warning), macros |
| Excel (`.xlsx`, `.xlsm`) | Every non-empty cell of every worksheet in workbook order, including hidden sheets (warned); embedded Office/PDF files | `sheet 'PM plan' cell B7` (an apostrophe in a sheet name is doubled, as Excel does), `embedded 'datasheet.docx' (on sheet 'PM plan') paragraph 2` | Comments, charts, chart sheets, pivot caches, other embedded objects, macros. Formulas give their saved result. Numbers and dates are the stored value (a date is a serial number such as 46330) unless `--excel-display` is given |
| PowerPoint (`.pptx`, `.pptm`) | Slides in presentation order, each slide's speaker notes, embedded Office/PDF files | `slide 4`, `slide 4 notes`, `embedded 'Worksheet.xlsx' (on slide 4) sheet 'Data' cell A2` | Slide-number fields, images, charts, other embedded objects, macros. Hidden slides are read and warned |
| HTML (`.html`, `.htm`) | Visible text by block; table rows | `line 9` (source line where the block starts), `table 1 row 2` | Scripts, styles, attributes, linked files |
| Text (`.txt`, `.md`, `.csv`) | Every non-blank line; UTF-8, UTF-16 with a byte-order mark, else Windows-1252 (warned) | `line 9` | Nothing is interpreted: a CSV row with a quoted line break spans two lines |
| Images (`.png`, `.jpg`, `.jpeg`, `.tif`, `.tiff`) | Only with `--ocr auto` and Tesseract installed | `page 1` (each page of a multi-page TIFF is its own page) | Without OCR they are reported as `unsupported`, as before |

Paragraph and table numbers count from the start of the document body. Paragraph numbers skip empty paragraphs.
Word does not show these numbers, so open the document and search for the text. Header and footer numbers come from
the file parts (`header1.xml`), not from section numbers. A Word table nested in a cell is read inside that cell.

Legacy binary `.doc`, `.xls` and `.ppt` files, RTF, and Office files or PDFs saved with a password are reported
as `unsupported` with the step to take (Save As `.docx`/`.xlsx`/`.pptx`, `soffice --headless --convert-to docx
FILE`, or save an unprotected copy), unless `--convert-legacy` converts them. Any other extension is reported as
`unsupported` too.

A page with no text layer is reported, not guessed: `no text layer, needs OCR: pages 4-6 of 12`. The status is
`partial` when some pages had text and `needs OCR` when none did; neither is an error. Use `--ocr auto` (below) or
your approved OCR tool to produce a searchable PDF, then run this again. A page whose only text is a stamp or page
number counts as having a text layer, so check page counts against the manifest for scanned packets.

Text from a PDF comes out in the order it was written into the file, which is usually reading order but not
always: columns, tables and rotated text can come out interleaved (`--pdf-layout` helps with columns). On a P&ID
exported as PDF, the letters and the number of an instrument tag in a bubble come out on separate lines (`PI` then
`P0020`), so a tag search misses them; read P&IDs through the [P&ID image route](../examples/own-drawing/README.md)
instead.

## Embedded files

Word, Excel and PowerPoint files often carry other documents inside them: a datasheet PDF dropped into a procedure,
a calculation workbook pasted into a PHA slide. Those are read with the same readers and the same limits, and every
piece keeps the place it came from: `embedded 'spec.pdf' (in table 3) page 2`, `embedded 'Worksheet.xlsx' (on slide
4) sheet 'Data' cell A2`. In Word the place is the paragraph or table that holds the object (`after paragraph 5` for
an object on a line of its own); in Excel the sheet; in PowerPoint the slide. Office files embedded as packages
(`.docx`/`.xlsx`/`.pptx`) are read, and so are PDFs and Office files wrapped in an OLE object (Office's Packager or
Acrobat object), named by the file name stored inside the object where there is one.

- Reading goes two levels deep (a file inside a file inside the input). Deeper ones are counted in a warning.
- Embedded objects that are not Office or PDF files (Visio drawings, legacy `.doc`/`.xls` objects, images, other
  programs' objects) keep the old warning: `2 embedded object(s) not read (e.g. word/embeddings/oleObject1.bin)`.
- An embedded file that is corrupt, encrypted or refused as hostile is reported (`embedded 'x.pdf' (in table 2): not
  read: ...`), none of its text is kept, and the containing file's status becomes `partial`.
- The manifest lists each embedded file read, with its locator, name, format, SHA-256, size, status and engine.
- This is on by default because it cannot change the output for a file that has no embedded objects (the worked
  example's outputs are unchanged byte for byte). `--embedded off` restores the old behaviour for every file.

## Optional add-ons

Each add-on is off unless asked for, needs nothing installed until it is, and uses a program only when that program
is present; otherwise the file is reported exactly as before plus a warning naming what is missing. When any add-on
is asked for, `manifest.json` records the options at the top (`"options": {...}`), and each file that an add-on acted
on lists it under `"applied"`. Without add-ons the output is byte for byte what it was before they existed.

### OCR: `--ocr auto` (default `off`)

Pages with no text layer, and image files (`.png`, `.jpg`/`.jpeg`, `.tif`/`.tiff`), are read with
[Tesseract](https://github.com/tesseract-ocr/tesseract) (Apache-2.0). PDF pages are first rendered to images with
`pdftoppm` from [Poppler](https://poppler.freedesktop.org/) (GPL; a separate program, not linked).

- Install: Tesseract (Windows: the UB Mannheim installer, then add its folder to PATH; macOS: `brew install
  tesseract`; Debian/Ubuntu: `apt install tesseract-ocr`) and, for PDFs, Poppler (`brew install poppler`, `apt install
  poppler-utils`; on Windows a Poppler build on PATH). `pip install pytesseract` is not needed; if it is installed and
  configured with a `tesseract_cmd`, that program is used when none is on PATH.
- What it changes: only pages that had no text (and image files) are OCRed; pages with a text layer are read as
  before. OCR text gets the same `page N` locator. The status is `ok (ocr)` when every page has text and some came
  from OCR. A page OCR finds nothing on stays a page to look at (`OCR found no text: page 7 of 12`, status
  `partial`). The `.txt` header gets a line such as `# ocr: engine: tesseract 5.3.4 (eng, 300 dpi; pages rendered by
  pdftoppm 24.02.0) | mean word confidence: page 3 91.2; page 4 88.0`, and the manifest gets the same under `"ocr"`.
  For an image file the engine is `tesseract <version>`.
- Options: `--ocr-lang eng+deu` (installed Tesseract language data; letters, digits, `_` and `+` only) and
  `--ocr-dpi 300` (70-1200). Up to 500 pages per file are OCRed; a rendered page is cropped at 14,000 pixels a side
  (lower `--ocr-dpi` for huge sheets) and an image file over 150 megapixels is refused before Tesseract sees it.
- Determinism: Tesseract runs with one thread (`OMP_THREAD_LIMIT=1`), so the same image, Tesseract version and
  language data give the same text. The manifest records the Tesseract and Poppler versions and the language and
  resolution, but not a hash of the language data; record the installed `tessdata` files for an audit trail.
  Different versions can give different text.
- Without Tesseract: images are reported `needs dependency` (`image text needs OCR: no tesseract program on PATH`);
  scanned PDF pages keep `no text layer, needs OCR` plus `OCR not run: no tesseract program on PATH` or `no pdftoppm
  program on PATH to render PDF pages (install Poppler)`.

### Legacy Office and RTF: `--convert-legacy`

`.doc`, `.xls`, `.ppt` and `.rtf` files are converted to `.docx`/`.xlsx`/`.pptx` by
[LibreOffice](https://www.libreoffice.org/) (MPL-2.0) and the converted file is read with the normal reader.

- Install: LibreOffice; `soffice` (or `libreoffice`) on PATH, or on Windows the default
  `C:\Program Files\LibreOffice\program` folder, which is found without PATH.
- How it runs: a copy of the file's bytes (the ones hashed in the manifest) is written under a fixed name into a new
  private temporary folder, converted there with `soffice --headless --convert-to ... --outdir` and a throwaway
  LibreOffice profile in that folder (so a running LibreOffice and your own settings are not touched), then the folder
  is deleted.
- What it changes: the file is read instead of reported `unsupported`; a warning says it was converted, and the
  manifest records `"converted": "docx by LibreOffice 7.6.4.1"`. Locators refer to the converted file; paragraph
  and table numbers can differ from what an old version of Word would count.
- Determinism: the text depends on the LibreOffice version, which is recorded. Without LibreOffice the file stays
  `unsupported` with the same conversion hint plus `--convert-legacy: no LibreOffice (soffice) program found on PATH`.

### PDF columns: `--pdf-layout`

Reads PDF text in layout mode, which places text by its position on the page so side-by-side columns and table
cells stay on their own lines (`Left column text      Right column text`) instead of interleaving. With
`--pdf-engine auto` it uses `pdftotext -layout` when a `pdftotext` program is on PATH, else pypdf's layout mode
(pypdf 3.17 or later). The manifest marks such files `"applied": ["pdf layout"]`. Layout text has runs of spaces;
the tag matcher is unaffected, but character positions inside a page differ from the default mode, so compare
locators only between runs made with the same setting.

### Excel displayed values: `--excel-display`

Numbers are shown as the cell's number format displays them, read from the workbook's own styles with the standard
library: dates and times (`46330` with `d-mmm-yy` gives `4-Nov-26`), percentages, fixed decimals, thousands
separators, scientific notation, currency symbols, literal text (`12.50 m3/h`), negative-number sections such as
`(1,234.50)` and elapsed times (`[h]:mm`). Dates follow the workbook's 1900 or 1904 date system.

- Built-in formats 14 and 22, which Excel shows in the reader's regional format, are written as ISO dates
  (`2026-11-04`, `2026-11-04 18:00`) so the output does not depend on the machine. Month and day names are English.
  Rounding is half away from zero, as Excel does.
- Formats not applied here (conditions such as `[>=100]`, fractions, engineering notation, East Asian calendars)
  keep the stored value and are counted in one warning: `3 number cell(s) kept their stored value: number format not
  applied (e.g. '# ?/?')`. Cell text, booleans and formula results that are text are not changed.

## Files are treated as untrusted

- Office files are opened as zip archives and only their XML text parts are parsed. Nothing is extracted to disk.
  Macros (`vbaProject.bin`), OLE links and external relationships are never run, opened or followed; macros are
  reported as a warning. Embedded Office and PDF files are read with the same readers and limits, counted against
  the containing file's limits; OLE wrappers are parsed by a bounded reader that checks every sector chain against
  the file size and for loops, and never runs the object.
- Limits, each refused with a message naming it: input file 100 MB (`--max-mb`), 20,000 archive parts, 64 MB per
  uncompressed part parsed whole and compression above 200:1 on those parts when over 1 MB (a zip bomb), 1 GB per
  Excel worksheet or shared-strings part (read as a stream, row by row), 2 GB of parts per archive, 5,000 PDF
  pages and 120 s for `pdftotext`. The bytes actually read are counted; declared sizes are not trusted. A
  100,000-row by 10-column worksheet (66 MB of XML, one million cells) read in about 7 seconds on one desktop.
- XML parts that declare a DTD or entities are refused (Office files never do), so entity expansion is never
  attempted. Relationship targets that point outside the archive are ignored.
- More than 20 million characters from one file stops reading; the result is `partial` and says where it stopped.
- pypdf parses PDFs in this process with its own limits; there is no timeout around it. Use `--pdf-engine
  pdftotext` for PDFs from a source you do not trust.
- Add-on programs (Tesseract, pdftoppm, LibreOffice) are started from an argument list, never through a shell, with
  no input, in their own process group, and only ever see fixed file names (`source.pdf`, `image.png`, `source.doc`)
  in a new private temporary folder, so a file name that looks like an option or contains shell characters cannot
  change what they do. Language and resolution values are checked before anything runs. Each run has a time limit
  (Tesseract 300 s per image or page, pdftoppm 120 s per page, LibreOffice 300 s); on a timeout the program and
  everything it started are ended (`taskkill /T` on Windows, the process group elsewhere) and the file is reported
  as an error. The temporary folder is removed afterwards, also after an error.
- LibreOffice parses the legacy file with its full import filters, which have had security bugs, and a document
  can contain links to remote images or data. Its default macro security does not run unsigned macros, but convert
  files from a source you do not trust only on a machine or container without network access. Tesseract and Poppler
  likewise parse untrusted images and PDFs; the size checks above limit, but do not remove, that exposure.

## For the one map (integration)

```python
import extract_text
result = extract_text.extract(path)        # never raises for a bad or unsupported file
for locator, text in result:               # ordered (locator, text) segments; same as result.segments
    ...                                    # run the tag matcher on text; locator + line/column inside it
result.sha256, result.status, result.warnings, result.engine, result.engine_version
result.ocr                                 # locator -> mean OCR word confidence, for OCR text only
extract_text.extract(path, ocr="auto", convert_legacy=True, pdf_layout=True, excel_display=True, embedded=False)
```

`status` is one of `ok`, `ok (ocr)`, `partial`, `needs OCR`, `needs dependency`, `unsupported`, `error`. A segment's
text can span several lines (a PDF page, a slide), so a mention's full locator is the segment locator plus the line
and column inside it, for example `page 3, line 14, column 9`. A mention found in OCR text (its locator is in
`result.ocr`) is a reading of an image and deserves a look at the page before it is relied on.

## Limits

- Tested on fictional files built by the test and example, and on two public PDFs (a CSB investigation report and
  a DEXPI example P&ID exported as PDF). Not tested on a plant's documents. Files written by other producers
  (LibreOffice, Google Docs exports, older Office versions) can arrange the same content differently.
- The OCR, conversion and PDF-rendering paths are tested with stand-in programs that check the arguments, time
  limits, process cleanup and temporary folders; tests with the real Tesseract and LibreOffice skip when they are
  not installed, and were skipped on the machine where this was written (pdftotext and pypdf were present, so both
  layout modes were exercised). OCR quality on real scans has not been measured here.
- OCR reads printed text; handwriting, stamps, rotated or very small text and drawings are unreliable. OCR text
  is a draft reading with a confidence, not a transcript.
- No layout beyond `--pdf-layout` (merged cells, reading order of floating shapes). Excel display covers the common
  number formats only; the rest keep stored values with a warning.
- Embedded objects that are not Office or PDF files, and anything more than two levels deep, are not read.
- Finding text is not finding meaning: a tag in a document is a mention to be reviewed, not a confirmed reference.
