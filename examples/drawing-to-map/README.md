# A P&ID read by the drawing reader, on the map

Step 1 of the [one-map path](../../docs/ONE_MAP.md#the-path) on a real P&ID: the drawing reader's committed reading
of public PID2Graph OPEN100 sheet 0 (Energy Impact Center OPEN100, P&ID 140 Main Steam System, rev A as printed) is
converted into a sheet read, built into a one-sheet site, and reviewed in the same review queue as the
[two-plant example](../one-map/README.md). No equipment or instrument records exist for this site, so step 3 writes
their drafts. **Sheet 0 is a development sheet**: the reader's method was built on it, so nothing here is an
accuracy claim. The site, plant (`NPP`) and unit (`MSS`) ids are labels chosen here, not the design's own.

## Run it

From the repository root, Python 3.10+, standard library only, offline:

```sh
python scripts/one_map.py sheet-from-prediction predictions/r2-tiles-trace/codex/0.json --sheet 140 --rev A \
    --plant NPP --unit MSS --zone-frame 9.4,19.5,857.1,981.1 --out examples/drawing-to-map/inputs/sheets/open100-0.json
python scripts/one_map.py build examples/drawing-to-map/inputs/site.json --out out/drawing-to-map
python scripts/one_map.py draft-lists examples/drawing-to-map/inputs/site.json --out out/drawing-to-map-drafts
python scripts/one_map.py check out/drawing-to-map/graph.json
```

The first command rewrites the committed [sheet read](inputs/sheets/open100-0.json) byte for byte; the others
reproduce [expected/](expected/) (`scripts/test_sheet_from_prediction.py` checks both).

| Input | What it is |
|---|---|
| [`predictions/r2-tiles-trace/codex/0.json`](../../predictions/r2-tiles-trace/codex/0.json) | The reader's prediction for sheet 0: 2x2 tiles with `extraction/prompt_v2.md` on `gpt-6.1-sol`, then the code line tracer. The same reading the [own-drawing](../own-drawing/README.md) and [plug-in-a-reader](../plug-in-a-reader/README.md) examples import |
| `--zone-frame 9.4,19.5,857.1,981.1` | The sheet's printed border in 0-1000 units, measured on the image (frame lines at x 24.5-2232 of 2604 px, y 34-1711 of 1744 px). With the default 8 x 12 grid, A at the bottom and 1 at the right, the zones match the numbers and letters printed on the border |
| [site.json](inputs/site.json), [drawing_register.csv](inputs/drawing_register.csv) | One site, one plant, one unit; the sheet index holds sheet 140 rev A. No maintenance equipment export, instrument index, loop list or datasheet |

## What the conversion produced

100 symbols and 345 connections in; every symbol lands in exactly one section:

| Section | Count | What |
|---|---|---|
| `equipment` | 2 | MSS-XSS-140 (D-9), RCS-SG-100 (C-11) |
| `instruments` | 37 | 36 tagged instrument bubbles and one tagged valve, MSCV-XXX |
| `offpage` | 9 | the continuation flags on the right edge; their printed reference kept as `drawing_reference` (`ES PID 180-1`, `HPD PID 190-1`, ...) |
| `untagged` | 52 | 34 valves and 18 fittings with no usable tag (nozzle labels `N1`/`N2` and operator letters `H`, `M`, `T` are kept as printed text) |
| `lines` | 38 | piping runs between tagged ends (the two vessels, MSCV-XXX, the 9 off-page connectors) traced through untagged valves and fittings |
| `signal_lines` | 0 | the prediction format has no line type |

Tags are joined from the bubble text (`TCV` over `1401` is `TCV-1401`, printed text kept). Flags carried, not
dropped: **placeholder tags** AORV-XXX and MSCV-XXX; **duplicate tag** FT-1401 (the sheet does print two FT 1401
bubbles side by side, so a person confirms both). Zones checked by eye against the printed border include PSV-1404
G-6, RCS-SG-100 C-11, MSS-XSS-140 D-9, TCV-1401 E-10 and TCV-1409 D-4.

### Piping between tags

The reader's 345 connections meet at untagged valves and fittings, and the line tracer joins every symbol touching
one drawn header to every other, so the main steam header reads as two dense networks with MSCV-XXX between them.
The conversion collapses paths through untagged in-line items into runs between tagged ends, one run per pair of
ends a network joins ([rules](../../docs/ONE_MAP.md#connectivity-from-a-reader-prediction)):

| Network | Run ends | Runs |
|---|---|---|
| upstream of MSCV-XXX (29 untagged in-line symbols) | RCS-SG-100, MSS-XSS-140, MSCV-XXX, two HPD PID 190-1 drain connectors | 10 |
| downstream of MSCV-XXX (21) | MSCV-XXX, ES PID 180-1, both TBS PID 240-1, MAIN STEAM BY-PASS, FWS PID 170-1, two HPD PID 190-1 | 28 |

Each run says what it passes (`through`: "2 valves and 3 other in-line symbols"), which symbols (`via_symbols`), and
which of the reader's connections it was built from (`prediction_connections`, indexes into the prediction). Runs
are connections between tagged ends, not line numbers: the printed line numbers (`SIZE-MSS-140076-...`) are not
read, and in these branched networks the path written is one shortest path; others exist.

Checked by eye against the sheet image (`data/external/pid2graph/PID2Graph/Complete/PID2Graph OPEN100/0.png`):

| Run | Through | On the P&ID |
|---|---|---|
| RCS-SG-100 to MSS-XSS-140 | nozzles N2, N1 | right: line 100075 from the generator's N2 to the superheater's N1 |
| MSCV-XXX to ES PID 180-1 | 1 valve | right: the branch up to the extraction steam flag, one valve |
| MSCV-XXX to TBS PID 240-1 (upper) | 2 valves | right: MSV-1404 and MSV-1405 on line 140076 to the turbine flag |
| MSCV-XXX to TBS PID 240-1 (lower) | direct | right: branch 140077, no valve |
| MSCV-XXX to MAIN STEAM BY-PASS | 1 valve | right: down 140080, through MSBV-1407 on 140081 |
| MSCV-XXX to FWS PID 170-1 | 2 valves | right as a connection: 140083 through TCV-1408 joins the bypass line at MSBV-1407 |
| RCS-SG-100 to HPD PID 190-1 (row B) | 2 valves, 3 others | right: N2, TCV-1401, flow element FT 1401, RE 1402 element on the header, TCV-1402 down drain 140078 |
| MSS-XSS-140 to MSCV-XXX | 2 valves, 3 others | connected, but the route written is not the main one: the reader joined the superheater only at N1 (its outlet nozzle is read but not joined to it), so the path goes back through the TCV-1401 bypass, and over the MS-4010 loop instead of MSIV-1402 |

### What the conversion could not do

All listed in the sheet read's `conversion` block:

- **Placement.** No instrument is placed. 20 bubbles reach the header networks, where every in-line item lies on
  many runs (6 to 32 candidates within 2 hops), so each is a `placement unclear` review row with its candidates; for
  MSV-1404/1405 every candidate ends at the upper TBS PID 240-1 connector and for RE-1403 at MSCV-XXX, and the row
  says so. 18 symbols (16 instrument bubbles, 2 fittings) have no connection at all.
- **Signal lines and loops.** The prediction format has no line type and the reader has no field that marks a
  signal line, so none is written and no loop is proposed from connectivity. Loops come from the loop list or a
  format that carries line types (e.g. DEXPI).
- **Off-page pairing.** The flags name P&IDs 180-1, 190-1, 240-1 and 170-1, none in this one-sheet site's sheet
  index; MAIN STEAM BY-PASS has no reference read (the sheet prints ACC PID 150-1). All 9 stay `off-page connector
  unpaired` review rows; they pair when the sheets they name are registered and read.

## What the map and review queue show

51 nodes, 79 edges (40 `contains`, 1 `covers`, 38 `connects`), no conflicts: with no equipment or instrument
records there is nothing to disagree with. The [review queue](expected/map/queues/review_queue.csv) has 71 rows, all
amber:

- 38 items on the P&ID but in no record: 24 `on the P&ID, not in the instrument index` (to I&C) and 14 `on the P&ID,
  not in the maintenance equipment export` (to Maintenance);
- 20 `placement unclear` and 9 `off-page connector unpaired` rows for Doc control;
- 2 `placeholder tag` and 1 `duplicate tag` rows for Doc control;
- 1 `untagged in-line symbols` row for the 52 untagged symbols.

The 12 safety-relevant rows come first: PSV-1404 to PSV-1407 and MSV-1404/1405, each as an unrecorded item and as a
placement to settle. The letter rule reads MSV-1404/1405 as relief devices although on this sheet they are main
steam valves (a false alarm the floor keeps amber for a person to clear).

The [draft maintenance equipment export](expected/drafts/npp-mss/equipment.csv) has 14 rows (the 6 relief rows amber)
and the [draft instrument index](expected/drafts/npp-mss/instrument_index.csv) 24 (the two placeholders and FT-1401
amber). No draft loop list is written: the sheet has no controller bubbles, so the loop-number groups in the
[report](expected/map/report.md) (`TE-14089A/B`, `FT-1401` with `TCV-1401`, ...) pair nothing.

## What this shows, and what it does not

It shows that a P&ID read by the reader reaches the map end to end: every tag located by sheet zone, the piping
between tags filled in where the reader's connections join them (38 runs, each traceable to the prediction's
connections), every uncertain read flagged in the same review queue, and nothing the format cannot carry silently
invented. The
existing scorer reports this reading (as an answer, not through the map) at review load 7.4 per 100 key items,
symbol F1 0.970 (rough; 0.931 strict) and connection F1 0.960 ([PLUG_IN_A_READER.md](../../docs/PLUG_IN_A_READER.md));
the OPEN100 keys carry no tag text, so tag readings and zones are not scored. The runs were checked by eye only (the
eight above); no run-level accuracy is measured. It does not show instrument placement, signal lines or loops from
this reading: the tracer's dense header networks leave every connected bubble ambiguous, and the format has no line
type. A reader that returns instrument attachments or line types would need a richer format or adapter first.

Licence: the sheet read and outputs are derived from a PID2Graph sheet and are CC BY-SA 4.0
([predictions/README.md](../../predictions/README.md#provenance-and-licence)).
