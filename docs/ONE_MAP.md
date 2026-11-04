# One map: the plant half and the document half in one graph

`scripts/one_map.py` is a prototype that puts a site's plant records and its documents into one graph
(`twin-graph-2`, an additive extension of [twin-graph-1](GRAPH_EXPORT.md)). Each department keeps its own records.
The tool connects them, keeps every disagreement as a conflict record, and sends that record to the person who owns
it. It is deterministic, runs offline on the Python standard library and calls no model. The worked example is
fictional: [examples/one-map](../examples/one-map/README.md).

**Start from structured lists where you have them; drawings locate and connect; people review disagreements.**
Where you have no lists yet, start from the drawings and generate draft lists in the same formats. Both starts
produce the same map, the same conflict records and the same review queues, and a site can mix them scope by scope.

## The two halves

**The plant half** is a hierarchy with a site-qualified identity: `SITE/PLANT/UNIT/TAG` (`S1/P1/200/P-101`).
The same legacy tag in two plants stays two items (`S1/P1/200/P-101`, `S1/P2/300/P-101`); nothing is renumbered,
and earlier tags stay as aliases (`former_tag`). A site scope that is not a plant (site utilities) owns shared
systems: a shared system such as cooling water has exactly one owning scope, and each plant that uses it reaches it
through a boundary node (`S1/P1/BND-CW references S1/UTIL/CW`). A sheet that draws the shared system as its own
raises a boundary conflict; it never gains a second owner.

**The document half** holds document nodes: id, revision, `draft` or `released`, owning department and a raw-byte
fingerprint. The registered drawings are documents too (`PID-P1-200-01` rev D). Three relations join the halves:

| Edge | From | To | Means |
|---|---|---|---|
| `covers` | document | the smallest scope it is about (equipment, system, unit, plant or site) | declared in the document manifest by exact id; never guessed |
| `mentions` | document | an item on the map | an exact tag, alias or site-qualified id found in the text; keeps file, locator (line, column), matched text and confidence |
| `based_on` | document | another document | with the revision it was based on |

A mention is asserted only when it is unambiguous: a tag unique on the map, a tag unique inside the document's
`covers` scope, or a site-qualified id. A tag that exists in two scopes the document does not choose between becomes
an `ambiguous_reference` conflict. Near misses (`P101` or `PSV 204` for `P-101`/`PSV-204`; `P-101` when the map has
only `P-101A`; `P-101A` when the map has only `P-101`) become review items. Nothing is fuzzily matched.

## Start A: from lists

| Input | Format | Role |
|---|---|---|
| Maintenance equipment export | CSV `tag,plant,unit[,system,description,status,former_tag,...]` | equipment, valves and relief devices |
| Instrument index | CSV `tag,plant,unit[,description,status,...]` | transmitters, controllers and other instruments |
| Loop list / control-system export | [loop_audit.py's contract](../examples/loop-audit/README.md) (`controller,measurement,output`), optional `status`; one list per unit | the loops |
| Drawing register | CSV `sheet,rev,plant,unit,owner,path[,status]` | which sheets exist, their revisions and owners |
| Sheet reads | `one-map-sheet-1` JSON per sheet: tags with zone/box, lines, signal lines, off-page connectors | what each drawing shows |
| Documents | a [context register](CONTEXT_REGISTER.md) `context-sources-1` manifest plus `owner`, `status`, `covers`, `based_on` | the document half |

Each list row becomes an item with its list's status. Each sheet then **locates** listed tags (sheet and zone),
supplies piping (`connects`), placement (`measures`, `acts_on`, `protects`) and drawn signal lines. A match gets a
green queue row and a deterministic spot-check sample flag instead of full review. Mismatches become conflicts:

- drawn but in no list → `asset_presence`, routed to the list that should hold it;
- listed but on no registered sheet of a covered unit → `asset_presence`, routed to the drawings' owner (a unit with
  no registered sheet yet is reported, not flagged item by item);
- the same attribute with two values → `value_disagreement`, routed to the list's owner.

Each listed loop becomes `controls` (or `sets_point_of`, for a cascade) edges sourced to the loop list, then is
located: **located and consistent** (all three tags on the unit's sheets and both signal lines drawn), **partly
located** or **not found on any sheet**. Only the last two go to review: to the loop list's owner when a tag is held
by no list, otherwise to the drawings' owner. A drawn signal line that pairs a listed controller differently
becomes a `loop_pairing` conflict.

Loop-number grouping on the drawings is secondary. Inside one unit only, instruments sharing a loop number with
compatible letters (`FT-2203`, `FIC-2203`, `FV-2203`; `TE-2207A/B`; split-range `FV-10A/B`), or joined by a drawn
signal line, form a candidate. A candidate the list lacks is flagged to the list's owner (`unlisted_loop`); it is
never asserted. Two units with the same loop number are never grouped.

## Start B: from drawings

`python scripts/one_map.py draft-lists site.json --out drafts` writes, for every scope no list covers, a draft
equipment list, instrument index and loop list in the formats above. Loops come from the same grouping and signal
lines, with `how_found` (`loop_number`, `signal_line`) and a confidence; a controller with more than one candidate
measurement or output is written as a comment for review, not as a loop. Every row is `unverified`, tiered
green/amber for review, and safety-relevant tags (the [twin's safety floor](TWIN_OUTPUTS.md)) are never green.
In the map, items from an unlisted scope are review items (`drawn, not yet listed`), not conflicts.

After a person reviews a draft and sets each row's status, add it to the site file as an ordinary list (with
`scopes`). From then on start A applies on every revision. The example shows Plant 1 starting from lists and
Plant 2 starting from its drawing, then the same site after Plant 2's lists were reviewed.

## Conflicts and their owners

A conflict is a graph node (kind `conflict`) with a `concerns` edge to its subject. It keeps what source A says,
what source B says (each with its source and locator), the attribute, the record owner, other parties, a status
`open`, `disputed` or `resolved`, and a decision history. The record owner comes from the site file's
`record_owners` map (record type to department: `pid` → Doc control, `maintenance_export` → Maintenance,
`instrument_index` and `loop_list` → I&C), a document's own owner, or the owning scope of a shared system. An
optional `routing` table overrides the record type per conflict type.

| Type | Raised when |
|---|---|
| `asset_presence` | an item is in a list but on no sheet, or on a sheet but in no list |
| `value_disagreement` | a list and a drawing (or two drawings) give different values for one attribute |
| `mention_not_in_register` | a document mentions a tag the covering list lacks |
| `ambiguous_reference` | a document names a tag in two scopes and its covers do not choose |
| `superseded_basis` | a document's `based_on` revision is not the current one |
| `loop_pairing` | a drawn signal line pairs a listed controller with another tag |
| `unlisted_loop` | the drawings show a possible loop the unit's loop list lacks |
| `boundary` | off-page connectors do not point back at each other, disagree on an attribute, or a sheet claims a shared system |

Software never resolves a conflict. `--decisions decisions.csv` (`conflict_id,status,by,on,note`) records a
person's decision; it persists across runs. A conflict that is no longer detected keeps its last status with
`detected: false` until a person resolves it.

## Queues

`queues/review_queue.csv` holds every row, risk-sorted: red (conflicts), amber (review items, partly located or not
found loops, safety-relevant items), green (matches, with `spot_check` = `sample` on a deterministic 1-in-N sample;
`spot_check_every` in the site file). `queues/by-owner/`, `by-plant/` and `by-unit/` split it, preserving order;
the split refuses to write a safety-relevant row as green. `split-queue` applies the same order-preserving split to
an existing `generate.py` `review_queue.csv` by any column, refusing an input whose safety floor is broken.

## Incremental runs and reopening

`build --out DIR` keeps `DIR/state.json`. On the next run, only sheets whose revision, raw bytes, plant, unit or
owner changed are re-read (a change to the tool's code re-reads all); assembly, pairing and checks are rerun over
the whole map with dictionary lookups, linear in items. Off-page connectors pair across sheets and plants by
`(plant, sheet, connector)`.

When a document's revision or bytes change, every document `based_on` it reopens, transitively. With `--register
context.json`, answers in a [context register](CONTEXT_REGISTER.md) whose evidence cites a changed or reopened
document are listed to reopen; the register's own refresh then marks them stale. The document manifest is the same
`context-sources-1` file the register reads.

## Limits

- A prototype tested only on the fictional example and synthetic cases. No plant's lists, drawings or documents
  have been run through it, and no one has timed a review with these queues.
- Sheet reads are hand-authored stand-ins for a drawing reader's output; this tool does not read images.
  `loops-from-graph` runs the grouping on an existing graph export; on the public OPEN100 sheet 0 it finds
  loop-number groups (`TE 14089A/B`; `TCV 1401` with `FT 1401`) but no controller bubbles and no
  instrument-to-instrument signal paths, so it proposes no loop ([result](../examples/one-map/expected/open100-sheet0-loops.md)).
- Letters decide roles by a short rule (controller `?[D]IC`, measurement `?[D]T`/`?E`, final element `?[C]V`);
  plant-coded or unusual letters are left unclassified. Tags need two or more digits.
- Values compare as exact text; units and synonyms are not normalized.
- Identity is the qualified id. A tag that moves between units, or a list that uses different plant/unit codes
  from the site file, needs an explicit mapping first; the tool does not guess one.
- The graph is `twin-graph-2`; tools that read only `twin-graph-1` (`graph_export.py --check`, context register,
  snapshot) do not read it yet.
- Mentions match upper-case tags with two or more digits; lower-case or differently punctuated tags are review
  items or are missed. Paths in the register and site file are relative to that file's folder.

## For agents

```text
schema: twin-graph-2 = twin-graph-1 + node kinds site, unit, scope, document, conflict
                       + edge types covers, mentions, based_on, references, signal_line, concerns
ids:    SITE/PLANT/UNIT/TAG; documents SITE/DOC/<id>; conflicts SITE/CONFLICT/C-<hash>; off-page SCOPE/@<sheet>/<id>
inputs: site.json (one-map-site-1) -> drawing register, sheet reads (one-map-sheet-1), maintenance export,
        instrument index, loop lists (loop_audit contract), documents (context-sources-1 + owner/status/covers/based_on)
paths:  A lists-first: lists are the skeleton; drawings locate (sheet, zone), connect and confirm
        B drawings-first: draft-lists writes the same list formats; reviewed drafts become lists for path A
never:  asserts an ambiguous or near-miss mention; asserts a loop from drawings; groups across units;
        resolves a conflict; renumbers a tag; gives a shared system two owners
check:  python scripts/one_map.py check graph.json   (every twin-graph-1 rule plus the one-map rules;
        graph_export.py --check still accepts only twin-graph-1)
graph:  graph["loops"] lists each listed loop's outcome; node.appearances lists sheet/zone locations;
        node.listed_in names the lists holding an item ([] = drawing-only)
```
