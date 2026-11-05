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

## Inputs

| File | What it stands for |
|---|---|
| [site.json](inputs/site.json) | Site, plants, units, the site-utilities scope, the shared cooling water system, record owners and which records cover which scopes; the default authority map applies |
| [drawing_register.csv](inputs/drawing_register.csv) | The sheet index: P&ID 200-01 rev D, 200-02 rev B, 300-01 rev A, CW-01 rev C |
| [sheets/](inputs/sheets/) | Hand-written sheet reads: tags with zones, lines, signal lines, off-page connectors, two printed values |
| [lists/](inputs/lists/) | Plant 1/utilities maintenance equipment export, Plant 1 instrument index, Unit 200 loop list, Plant 1 equipment datasheets; `plant2-reviewed/` holds Plant 2's reviewed drafts |
| [documents.json](inputs/documents.json), [docs/](inputs/docs/) | Four short documents in a `context-sources-1` manifest with owner, status, covers and based_on |

The documents: the *P-101 design basis rev 3* (Process, released) is based on P&ID 200-01 **rev C**; procedure
OP-200-07 (Operations) mentions P-102, which the maintenance equipment export lacks, plus `P101` and `PSV 204`; the
cooling water note (Site utilities, draft) mentions a bare `P-101`, which exists in both plants; a Unit 300 check
sheet (Maintenance, draft) mentions `P-101` inside its own unit and `P-101A`, which is in no record and on no P&ID.

## What it produces (start)

63 nodes and 113 edges, 14 of the nodes conflicts. Items in an equipment or instrument record: 19, of which 15 are
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

Review queue: 39 rows, split by owner (Maintenance 14, I&C 13, Doc control 6, Site utilities 3, Operations 2,
Process 1), by plant and by unit. PSV-204 stays amber under the safety floor; matches are green with a 1-in-4
deterministic spot-check sample.

After review, Plant 2's reviewed records cover Unit 300: its five items are located matches (green), its loop is
located and consistent, and the conflict set is unchanged.

## Limits

The sheet reads are written by hand, not read from images; the example measures the bookkeeping, not reading
accuracy. The zones here (`B2`, `C1`) are hand-written labels, not the `sheet_zone.py` convention a converted read
uses. Mentions are exact tag matches; a document that writes a tag in another style is a review item, not a link.
Values compare as text. Conflicts are records for a person to settle; nothing here confirms any value or plant
condition.
