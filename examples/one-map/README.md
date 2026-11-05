# One map for two fictional plants

A fictional site, *Riverbend*, with Plant 1 (Unit 200), Plant 2 (Unit 300) and a cooling water header owned by
site utilities. Every tag, person, record and document here is invented. Both plants go down the same path
([docs/ONE_MAP.md](../../docs/ONE_MAP.md#the-path)); they differ only in what exists when they start:

- **Plant 1 and the utilities** have a maintenance equipment export, an instrument index, a loop list for Unit 200
  and equipment datasheets. The P&IDs locate each tag and supply piping and signal lines; the datasheets hold values.
- **Plant 2** has only its P&ID, so step 3 has work in it: `draft-lists` writes its draft maintenance equipment
  export, draft instrument index and draft loop list. After a (fictional) review those drafts become ordinary
  records and the same run applies.

The sheet reads here are written by hand. For a sheet read converted from the drawing reader's output on a real
P&ID, see [examples/drawing-to-map](../drawing-to-map/README.md).

## Run it

From the repository root, with Python 3.10+ (standard library only):

```sh
python scripts/one_map.py build examples/one-map/inputs/site.json --out out/one-map
python scripts/one_map.py draft-lists examples/one-map/inputs/site.json --out out/one-map-drafts
python scripts/one_map.py build examples/one-map/inputs/site-after-review.json --out out/one-map-after-review
python scripts/one_map.py check out/one-map/graph.json
```

Run `build` again with the same `--out`: all four sheets are reused. Edit one sheet and only that sheet is re-read.
The committed results are in [expected/](expected/): [start](expected/start/report.md),
[Plant 2 drafts](expected/drafts/p2-300/) and [after review](expected/after-review/report.md).

### With Office documents

The same site with two more documents, a Word start-up procedure and an Excel PM plan. They are generated, not
committed (the repository holds no binary documents); the bytes are the same on every run:

```sh
python examples/one-map/make_office_docs.py examples/one-map/inputs/docs/office
python scripts/one_map.py build examples/one-map/inputs/site-office.json --out out/one-map-office
```

Committed results: [report](expected/office/report.md), [review queue](expected/office/queues/review_queue.csv),
[graph](expected/office/graph.json), [conflicts](expected/office/conflicts.md).

## The pasteurizer: classes, expectations, glossary

A second fictional site, *Lakeside dairy*: one plant with an HTST pasteurizer (unit PAST1), a CIP skid (CIP1) and a
filler (FILL1, no P&ID registered yet). Beside the P&IDs, the maintenance equipment export, the instrument index, a
loop list and pump datasheets, it supplies `records` (the HACCP plan's CCPs, calibration records and the relief device
register for PAST1, the criticality ranking, the PM plan, the glossary) and its own copy of the expectation rules,
four of them certified by fictional people, one left draft, one rolled out to PAST1 only. See
[Expectations](../../docs/CONTEXT_MAP_FORMAT.md#expectations) and [Glossary](../../docs/CONTEXT_MAP_FORMAT.md#glossary).

```sh
python scripts/one_map.py build examples/one-map/inputs/pasteurizer/site.json --out out/pasteurizer
python scripts/one_map.py ask --map out/pasteurizer/graph.json --question-kind complete --item FT-2203
python scripts/one_map.py ask --map out/pasteurizer/graph.json --question-kind measured-by --item "hold tube"
python scripts/one_map.py jsonld --map out/pasteurizer/graph.json --out out/pasteurizer/map.jsonld
```

Committed results: [report](expected/pasteurizer/report.md), [review queue](expected/pasteurizer/queues/review_queue.csv),
[graph](expected/pasteurizer/graph.json), [answers](expected/pasteurizer/answers.md),
[JSON-LD view](expected/pasteurizer/map.jsonld). What it shows:

| Piece | Result |
|---|---|
| Classes | P-101 positive displacement pump (prefix P, datasheet `rotary lobe`), P-102 centrifugal pump, HT-100 hold tube, PHE-2201 plate heat exchanger, E-2215 shell and tube (the export's `class` column), FDV-2210 divert valve; FL-401 left unset |
| Link check | `PI-2240 measures TIC-2207` (a misread placement): "link doesn't fit what it connects" to Doc control; the link stays |
| R-CCP-COMPLETE | CCP-1 (TT-2207) complete; CCP-2 (FT-2203) expected but missing: no critical limit, calibration overdue (next due 2026-08-01), no verification document; to Quality |
| R-RELIEF-PROTECTS | PSV-2216 drawn on nothing and in no relief device register: one row to Process safety; PSV-3101 on CIP1 not evaluable (no relief device register covers CIP1) |
| R-CRITICAL-PM | P-101 and FDV-2210 ranked A with no PM plan: two rows to Maintenance; P-301 on CIP1 ranked A, not rolled out there, counted only |
| R-LOOP-COMPLETE (draft) | one summary row: it would raise one row in PAST1 (PIC-2240's measurement is an indicator) |
| Glossary | `HTST`, `hold tube`, `divert valve` and `FDV` link in the HACCP plan and the start-up SOP; `timing pump` (draft) and `product pump` (two pumps) are review rows to Production |
| Answers | `connects FL-401`: can't answer from this map, no P&ID covers S1/P1/FILL1 |

## The pasteurizer through an MOC: P&ID revision, MOC open and close, work order, walkdown

The same dairy through one fictional management of change, MOC-0412: replace the flow diversion valve FDV-2210 with a
DN65 valve (model SRC-3) and add TT-2208, an independent hold tube outlet temperature transmitter. Three builds of the
map stand for three moments; the inputs are files beside the pasteurizer's own (`site-revD.json`,
`site-moc-close.json` and the files they name). How plant teams run this: [RUNNING_THE_MAP.md](../../docs/RUNNING_THE_MAP.md).

```sh
python scripts/one_map.py build examples/one-map/inputs/pasteurizer/site.json --out out/moc/open  # MOC open: P&ID rev C
python scripts/one_map.py build examples/one-map/inputs/pasteurizer/site-revD.json --out out/moc/revd  # P&ID PAST1-01 rev D released
python scripts/one_map.py build examples/one-map/inputs/pasteurizer/site-moc-close.json --out out/moc/close --decisions examples/one-map/inputs/pasteurizer/walkdown_rulings.csv
python scripts/one_map.py changes out/moc/open/graph.json out/moc/revd/graph.json --out out/moc/release
python scripts/one_map.py affected --map out/moc/open/graph.json --tags FDV-2210 TT-2208 --out out/moc/moc-open
python scripts/one_map.py changes out/moc/open/graph.json out/moc/close/graph.json --tags FDV-2210 TT-2208 --out out/moc/moc-pack
python scripts/one_map.py affected --tags FDV-2210 TT-2208 --closeout out/moc/open/graph.json out/moc/close/graph.json --out out/moc/moc-close
```

Committed results in [expected/pasteurizer-moc/](expected/pasteurizer-moc/):

| Moment | Report | What it shows |
|---|---|---|
| P&ID rev D released | [release/changes.md](expected/pasteurizer-moc/release/changes.md) | TT-2208 added (measures HT-100); FDV-2210 now has `size DN65` printed; P&ID PAST1-01 rev C -> D; two new conflicts: TT-2208 is not in the instrument index (I&C), the HACCP plan rev 7 is based on rev C (Quality); FDV-2210 flagged `HACCP reassessment` (CCP-1's corrective action names it) and `criticality review` (ranked A) |
| MOC open | [moc-open/affected.md](expected/pasteurizer-moc/moc-open/affected.md) | 12 rows for 6 owners: the P&ID sheet (Doc control), the valve datasheet (Engineering), loop TIC-2207 in the loop list (I&C), the maintenance equipment export row, criticality ranking and the missing PM plan (Maintenance), the start-up SOP that mentions the FDV (Production), the CCP row, glossary term and HACCP plan (Quality), plus the two flags; TT-2208 "not on the map yet"; linked items HT-100, PHE-2201, TIC-2207 |
| MOC close | [close/review_queue.csv](expected/pasteurizer-moc/close/queues/review_queue.csv), [close/conflicts.md](expected/pasteurizer-moc/close/conflicts.md) | Work order WO-60311 records SRC-3, serial AV-88412, DN65 installed. The maintenance equipment export has the new model but the old serial: a value_disagreement to Maintenance. The valve datasheet still says DN50: `replacement may not be like-for-like` to Engineering (a possible MOC trigger, not decided). The walkdown ruling R-0101 (authority `field`, nameplate photo) settles the serial conflict, keeps a history line, and asks Maintenance to update the export (`record differs from a ruling`) |
| MOC close | [moc-pack/changes.md](expected/pasteurizer-moc/moc-pack/changes.md) | Before/after pack for the two tags: FDV-2210 model SRC-2 -> SRC-3, TT-2208 added, WO-60311 added, P&ID rev C -> D, HACCP plan 7 -> 8 (now mentions TT-2208), the serial conflict (resolved) |
| MOC close | [moc-close/closeout.md](expected/pasteurizer-moc/moc-close/closeout.md) | 7 affected rows changed, 7 unchanged, 1 expectation gap still open (no PM plan for FDV-2210), 2 flags to confirm by hand. Of the unchanged, the valve datasheet is the record not yet updated (its DN50 contradicts the work order); the loop list, criticality ranking, CCP row, glossary and SOP are for their owners to confirm |

The P&ID value note (DN65 printed, DN50 on the datasheet) goes to Doc control because values printed on a P&ID are
reference only; here the datasheet is the record that is behind, which the like-for-like row and the closeout show.

## Inputs

| File | What it stands for |
|---|---|
| [site.json](inputs/site.json) | Site, plants, units, the site-utilities scope, the shared cooling water system, record owners and which records cover which scopes; the default authority map applies |
| [drawing_register.csv](inputs/drawing_register.csv) | The sheet index: P&ID 200-01 rev D, 200-02 rev B, 300-01 rev A, CW-01 rev C |
| [sheets/](inputs/sheets/) | Hand-written sheet reads: tags with zones, lines, signal lines, off-page connectors, two printed values |
| [lists/](inputs/lists/) | Plant 1/utilities maintenance equipment export, Plant 1 instrument index, Unit 200 loop list, Plant 1 equipment datasheets; `plant2-reviewed/` holds Plant 2's reviewed drafts |
| [documents.json](inputs/documents.json), [docs/](inputs/docs/) | Four short documents in a `context-sources-1` manifest with owner, status, covers and based_on |
| [pasteurizer/](inputs/pasteurizer/) | The dairy: site file, P&IDs PAST1-01 rev C and CIP1-01, maintenance equipment export (with manufacturer, model, serial number), instrument index, loop list, pump and valve datasheets, work order history, `records`, glossary, expectation rules, three documents |
| [pasteurizer/site-revD.json](inputs/pasteurizer/site-revD.json), [site-moc-close.json](inputs/pasteurizer/site-moc-close.json), [walkdown_rulings.csv](inputs/pasteurizer/walkdown_rulings.csv) | MOC-0412: P&ID rev D (`sheets/PAST1-01-revD.json`), then the close state (`*-moc.*` records, `documents-moc.json` with HACCP plan rev 8) and the walkdown ruling |
| [site-office.json](inputs/site-office.json), [documents-office.json](inputs/documents-office.json), [make_office_docs.py](make_office_docs.py) | The Office variant: the same site and the four documents plus SU-200-03 (`.docx`) and PM-200 (`.xlsx`), written into `inputs/docs/office/` |

The documents: the *P-101 design basis rev 3* (Process, released) is based on P&ID 200-01 **rev C**; procedure
OP-200-07 (Operations) mentions P-102, which the maintenance equipment export lacks, plus `P101` and `PSV 204`
(other styles of `P-101` and `PSV-204`); the cooling water note (Site utilities, draft) mentions a bare `P-101`, which exists in both plants; a Unit 300 check
sheet (Maintenance, draft) mentions `P-101` inside its own unit and `P-101A`, which is in no record and on no P&ID.

## What it produces (start)

63 nodes and 114 edges, 14 of the nodes conflicts. Items in an equipment or instrument record: 19, of which 15 are
located on a P&ID sheet; 7 items are on a P&ID and in no record (5 of them in Plant 2, which has no records yet).

| Record owner | Conflicts |
|---|---|
| Doc control | 4 in a record but on no P&ID (P-103, LT-2204, LIC-2204, LV-2204) |
| Maintenance | 2 on a P&ID but not in the maintenance equipment export (P-102, PV-2210); P-102 mentioned by OP-200-07; P-101 rated flow 45 m3/h on its datasheet (the authority for ratings) vs 40 m3/h in the maintenance equipment export |
| I&C | PIC-2210's drawn signal line goes to PV-2210, the loop list says PV-2211; TT/TIC/TV-2205 drawn as a loop the loop list lacks |
| Process | the design basis cites P&ID 200-01 rev C; the current revision is D |
| Site utilities | the cooling water note's bare `P-101`; supply size 6 in on 300-01 vs 8 in on CW-01; 300-01 draws cooling water as Plant 2's own |

P&ID 200-01 prints P-101's rated flow as 45 m3/h, which agrees with the datasheet, so it raises nothing. It prints
V-204's design pressure as 12 barg against 10 barg on the datasheet: that is a low-priority **P&ID value note** to
Doc control (amber, last of the amber rows), not a value conflict, because values printed on a P&ID are reference
only.

Loops from the Unit 200 loop list: FIC-2203 is **located and consistent** on 200-01 (zones C1, C2) and goes to
spot-check; PIC-2210 is **partly located** (routed to I&C: PV-2211 is in no record); LIC-2204 is **not found on any
sheet** (routed to Doc control: its tags are recorded but not drawn). Plant 2's FIC-3101 loop is a review item for
its draft loop list, not a conflict, because no loop list covers Unit 300 yet.

Mentions: `PSV 204` in OP-200-07 is `PSV-204` written another way and is the only PSV-204 on the map, so it links
with `matched: format-insensitive`. `P101` in the same procedure is P-101 written another way, but both plants have a
P-101: it is a review row `possible mention, confirm` for Operations, naming both candidates and the Unit 200 one
the procedure's covers point to; it is not linked. `P-101A` in the Unit 300 check sheet is a `possible mention,
confirm` row for Maintenance (no record and no P&ID has that suffix).

Review queue: 38 rows, split by owner (Maintenance 14, I&C 13, Doc control 6, Site utilities 3, Operations 1,
Process 1), by plant and by unit. PSV-204 stays amber under the safety floor; matches are green with a 1-in-4
deterministic spot-check sample.

After review, Plant 2's reviewed records cover Unit 300: its five items are located matches (green), its loop is
located and consistent, and the conflict set is unchanged.

## What the Office documents add

Both documents are read by [extract_text.py](../../docs/DOCUMENT_TEXT.md); each mention keeps the place it was found.

| Document | Text | Linked to | Locator | How matched |
|---|---|---|---|---|
| SU-200-03 start-up procedure (`.docx`, Operations) | `TT2205` | S1/P1/200/TT-2205 | paragraph 2, column 41 | format-insensitive |
| | `FP01` | S1/P1/200/P-101 | paragraph 3, column 37 | format-insensitive, via its former tag FP-01 in the maintenance equipment export |
| | `ft-2203` | S1/P1/200/FT-2203 | table 1 row 2, column 1 | format-insensitive |
| | `PSV-204` | S1/P1/200/PSV-204 | table 1 row 3, column 1 | exact |
| PM-200 PM plan (`.xlsx`, Maintenance) | `e-205` | S1/P1/200/E-205 | sheet 'PM plan' cell A2, column 1 | format-insensitive |
| | `FV 2203` | S1/P1/200/FV-2203 | sheet 'PM plan' cell A3, column 1 | format-insensitive |
| | `LV2204` | S1/P1/200/LV-2204 | sheet 'PM plan' cell A4, column 1 | format-insensitive |

One new review row: `P 101` in SU-200-03 (paragraph 1, column 26) is `possible mention, confirm` for Operations,
because both plants have a P-101; the row names the Unit 200 candidate the procedure covers. The run has 65 nodes,
123 edges (21 mentions), 39 review rows and the same 14 conflicts. Both documents read with status `ok`; a document
that is not fully read (a scan, a legacy `.doc`, a corrupt file) would instead be a low-priority `document text note`
to its owner ([statuses](../../docs/ONE_MAP.md#the-two-halves)).

## Limits

The sheet reads are written by hand, not read from images; the example measures the bookkeeping, not reading
accuracy. The zones here (`B2`, `C1`) are hand-written labels, not the `sheet_zone.py` convention a converted read
uses. A tag written in another style links only when it names exactly one item on the map; otherwise it is a review
row. The Office documents are small generated files, not real procedures or PM plans exported from Word or Excel.
Values compare as text. Conflicts are records for a person to settle; nothing here confirms any value or plant
condition.
