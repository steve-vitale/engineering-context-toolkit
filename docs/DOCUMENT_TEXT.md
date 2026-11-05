# Document text: read what procedures, PHAs and work orders say

Procedures, HACCP plans, PHAs, CAPAs, work orders and purchase orders name the same pumps, transmitters and valves
as the P&ID and the instrument index. They live in Word, Excel, PowerPoint and PDF files, which a plain text search
cannot see. `scripts/extract_text.py` reads the text inside those files and puts a locator in front of every piece,
so a tag found in a document can be traced back to the exact page, table row, cell or slide.

It is a reading step only. It does not decide what a tag means, match tags to the map, or change any source.
The [one map](ONE_MAP.md) reads every document in its manifest through `extract_text.extract()` and matches tags
piece by piece ([matching rules and statuses](ONE_MAP.md#the-two-halves)).

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
| PDF (`.pdf`) | The text layer, page by page, through optional pypdf, else a `pdftotext` program on PATH | `page 3` | Images, scanned pages (reported as needing OCR), annotations and form fields |
| Word (`.docx`, `.docm`) | Body paragraphs and tables in order, text boxes, content controls, page headers and footers, footnotes, endnotes, comments | `paragraph 12`, `table 2 row 4` (cells joined with ` \| `), `page header 1 paragraph 1`, `page footer 2 paragraph 1`, `footnote 3`, `comment 1` | Tracked deletions (warned), field codes, embedded objects (counted in a warning), macros |
| Excel (`.xlsx`, `.xlsm`) | Every non-empty cell of every worksheet in workbook order, including hidden sheets (warned) | `sheet 'PM plan' cell B7` (an apostrophe in a sheet name is doubled, as Excel does) | Comments, charts, chart sheets, pivot caches, embedded objects, macros. Formulas give their saved result. Numbers and dates are the stored value (a date is a serial number such as 46330), not the displayed format |
| PowerPoint (`.pptx`, `.pptm`) | Slides in presentation order, and each slide's speaker notes | `slide 4`, `slide 4 notes` | Slide-number fields, images, charts, embedded objects, macros. Hidden slides are read and warned |
| HTML (`.html`, `.htm`) | Visible text by block; table rows | `line 9` (source line where the block starts), `table 1 row 2` | Scripts, styles, attributes, linked files |
| Text (`.txt`, `.md`, `.csv`) | Every non-blank line; UTF-8, UTF-16 with a byte-order mark, else Windows-1252 (warned) | `line 9` | Nothing is interpreted: a CSV row with a quoted line break spans two lines |

Paragraph and table numbers count from the start of the document body. Paragraph numbers skip empty paragraphs.
Word does not show these numbers, so open the document and search for the text. Header and footer numbers come from
the file parts (`header1.xml`), not from section numbers. A Word table nested in a cell is read inside that cell.

Legacy binary `.doc`, `.xls` and `.ppt` files, RTF, and Office files or PDFs saved with a password are reported
as `unsupported` with the step to take (Save As `.docx`/`.xlsx`/`.pptx`, `soffice --headless --convert-to docx
FILE`, or save an unprotected copy). Any other extension is reported as `unsupported` too.

## Scanned PDFs: no OCR here

A page with no text layer is reported, not guessed: `no text layer, needs OCR: pages 4-6 of 12`. The status is
`partial` when some pages had text and `needs OCR` when none did; neither is an error. Run your approved OCR tool
to produce a searchable PDF, then run this again. A page whose only text is a stamp or page number counts as having
a text layer, so check page counts against the manifest for scanned packets.

Text from a PDF comes out in the order it was written into the file, which is usually reading order but not
always: columns, tables and rotated text can come out interleaved. On a P&ID exported as PDF, the letters and the
number of an instrument tag in a bubble come out on separate lines (`PI` then `P0020`), so a tag search misses
them; read P&IDs through the [P&ID image route](../examples/own-drawing/README.md) instead.

## Optional PDF dependency

PDF text needs [pypdf](https://pypi.org/project/pypdf/) (BSD-3-Clause; tested with 6.14.2, pinned in
[requirements-documents.txt](../requirements-documents.txt)): `pip install -r requirements-documents.txt`. Without
it, the tool uses a `pdftotext` program on PATH (Poppler or Xpdf); without either, each PDF is reported as
`needs dependency` with `PDF text needs pypdf (pip install pypdf)`. `--pdf-engine pypdf|pdftotext` picks one. The
manifest records which engine and version read each PDF, because different engines and versions can split or space
text differently. Everything else uses the Python standard library only.

## Files are treated as untrusted

- Office files are opened as zip archives and only their XML text parts are parsed. Nothing is extracted to disk.
  Macros (`vbaProject.bin`), embedded objects, OLE links and external relationships are never run, opened or
  followed. Their presence is reported as a warning.
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

## For the one map (integration)

```python
import extract_text
result = extract_text.extract(path)        # never raises for a bad or unsupported file
for locator, text in result:               # ordered (locator, text) segments; same as result.segments
    ...                                    # run the tag matcher on text; locator + line/column inside it
result.sha256, result.status, result.warnings, result.engine, result.engine_version
```

`status` is one of `ok`, `partial`, `needs OCR`, `needs dependency`, `unsupported`, `error`. A segment's text can
span several lines (a PDF page, a slide), so a mention's full locator is the segment locator plus the line and column
inside it, for example `page 3, line 14, column 9`.

## Limits

- Tested on fictional files built by the test and example, and on two public PDFs (a CSB investigation report and
  a DEXPI example P&ID exported as PDF). Not tested on a plant's documents. Files written by other producers
  (LibreOffice, Google Docs exports, older Office versions) can arrange the same content differently.
- Text only: no OCR, no images, no handwriting, no embedded documents, no layout (columns, merged cells, reading
  order of floating shapes). Excel numbers and dates are stored values, not the displayed format.
- Finding text is not finding meaning: a tag in a document is a mention to be reviewed, not a confirmed reference.
