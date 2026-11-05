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
| `lines` | 1 | MSCV-XXX to the TBS PID 240-1 connector |
| `signal_lines` | 0 | the prediction format has no line type |

Tags are joined from the bubble text (`TCV` over `1401` is `TCV-1401`, printed text kept). Flags carried, not
dropped: **placeholder tags** AORV-XXX and MSCV-XXX; **duplicate tag** FT-1401 (the sheet does print two FT 1401
bubbles side by side, so a person confirms both). Zones checked by eye against the printed border include PSV-1404
G-6, RCS-SG-100 C-11, MSS-XSS-140 D-9, TCV-1401 E-10 and TCV-1409 D-4.

What the conversion could not do, all listed in the sheet read's `conversion` block:

- **Piping.** The reader's connections meet at 33 untagged valves and fittings that each have three or more piping
  connections (the main steam header is drawn as hubs). A branch point cannot be named in a sheet read, so items
  that meet only through one get no line. They are listed instead as two networks: the vessels and MSCV-XXX with
  two drain connectors, and MSCV-XXX with the seven right-edge connectors.
- **Placement.** None of the 36 instrument bubbles is joined directly to exactly one tagged vessel or pump, so no
  `measures`/`acts_on`/`protects` edge is written. 18 symbols (16 instrument bubbles, 2 fittings) have no connection at all.
- **Off-page pairing.** No flag names a sheet in the sheet index, so `to` stays empty.

## What the map and review queue show

51 nodes, 42 edges (40 `contains`, 1 `covers`, 1 `connects`), no conflicts: with no equipment or instrument records
there is nothing to disagree with. The [review queue](expected/map/queues/review_queue.csv) has 42 rows, all amber:

- 38 `drawn, not yet listed` items (24 to I&C for the instrument index, 14 to Maintenance for the maintenance
  equipment export). The 6 safety-relevant rows come first: PSV-1404 to PSV-1407, and MSV-1404/1405, which the letter
  rule reads as relief devices although on this sheet they are main steam valves (a false alarm the floor keeps
  amber for a person to clear);
- 2 `placeholder tag` and 1 `duplicate tag` rows for Doc control;
- 1 `untagged in-line symbols` row for the 52 untagged symbols.

The [draft maintenance equipment export](expected/drafts/npp-mss/equipment.csv) has 14 rows (the 6 relief rows amber)
and the [draft instrument index](expected/drafts/npp-mss/instrument_index.csv) 24 (the two placeholders and FT-1401
amber). No draft loop list is written: the sheet has no controller bubbles, so the loop-number groups in the
[report](expected/map/report.md) (`TE-14089A/B`, `FT-1401` with `TCV-1401`, ...) pair nothing.

## What this shows, and what it does not

It shows that a P&ID read by the reader reaches the map end to end: every tag located by sheet zone, every
uncertain read flagged in the same review queue, and nothing the format cannot carry silently invented. The
existing scorer reports this reading (as an answer, not through the map) at review load 7.4 per 100 key items,
symbol F1 0.970 (rough; 0.931 strict) and connection F1 0.960 ([PLUG_IN_A_READER.md](../../docs/PLUG_IN_A_READER.md));
the OPEN100 keys carry no tag text, so tag readings and zones are not scored. It does not show that the connectivity
on the map is usable: one piping line and no signal lines come through from this reading. A reader that returns
junctions, line types or instrument attachments would need a richer format or adapter first.

Licence: the sheet read and outputs are derived from a PID2Graph sheet and are CC BY-SA 4.0
([predictions/README.md](../../predictions/README.md#provenance-and-licence)).
