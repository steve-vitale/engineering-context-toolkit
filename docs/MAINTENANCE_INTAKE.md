# Turn your exports into a maintenance review packet

Use two permitted CSV exports: an equipment register and work-order history containing explicitly recorded
installed values. No drawing, account, network or MCP server is needed. Python 3.10+; standard library only.
Your agent can prepare the small profile with you, run the comparison and explain the original rows.

```sh
python -S scripts/maintenance_intake.py --profile my-profile.json --equipment equipment.csv --work-orders work-orders.csv --out review-01
```

Open `review-01/REPORT.html` offline or read `REPORT.md`. It contains detected disagreements, original source-row
links, coverage limits and proposed owner actions. The complete queue is `map/queues/review_queue.csv`;
`findings.json` retains both values and their provenance. Keep the whole folder together. The output is a draft
comparison; a clean report does not prove records complete or equipment correct.

## Define the mapping and scope

Copy [the fictional profile](../examples/maintenance-intake/inputs/profile.json). Supply explicit site, plant and
unit IDs, ISO `as_of`, distinct stable document IDs, source revisions, owner roles and a precise description of
what each export covers. These declarations need the record owner's confirmation. The source filenames can
be anything; the packet retains their exact bytes as `originals/equipment.csv` and `originals/work_orders.csv`.
The profile maps **original header â†’ canonical field**:

| Export | Required mapped fields | Optional interpreted fields |
|---|---|---|
| Equipment | `tag`, `unit` | `description`, `class`, `manufacturer`, `model`, `serial_number`, `size` |
| Work orders | `work_order`, `tag`, `unit`, `closed_on` | `description`, `installed_manufacturer`, `installed_model`, `installed_serial_number`, `installed_size` |

Map installed fields only when the export actually describes what was installed. A parts request, estimated
material or proposed replacement does not establish installation. Blank `closed_on` means open/unconfirmed;
its installed fields remain history and are not installation evidence. Do not map a generic status column to
a closure date. Multiple rows per order/position must be reconciled explicitly before intake; no grouping guess
or automatic line-item aggregation is provided.

`columns` must account for each header. List unneeded headers in `ignored_columns`; their bytes remain but are
not interpreted. Duplicate/blank headers, ragged rows, duplicate record identities, blank tags, unknown units,
ambiguous dates, future closure dates and conflicting same-day installation values stop the run before a packet
is published. Headers are case sensitive. Missing files and empty exports fail, preserving earlier packets.

Optional per-export settings: `delimiter` is comma (default), semicolon, tab or pipe; `encoding` is `utf-8-sig`
(default), `utf-8` or `cp1252`; `date_format` is `%Y-%m-%d` (default), `%m/%d/%Y` or `%d/%m/%Y`. Dates must match
exactly, including zero padding. No locale is guessed. Values are strings, so leading zeros survive. Prepared
values are trimmed; exact original text is retained. `row-origins.json` records logical CSV record number
(header is record 1) and ending physical line, including quoted multiline records.

## Return with a corrected export or another replacement

```sh
python -S scripts/maintenance_intake.py --profile next-profile.json --equipment returned-equipment.csv --work-orders next-orders.csv --previous review-01 --out review-02
```

Use a new output directory for every run. The previous inventory must verify. Same-site/unit/source/owner/coverage
bindings must agree and the date cannot move backwards. Change a source revision whenever its bytes change;
header mappings can change explicitly with it. A changed scope or authority needs a separately reviewed comparison,
not an implicit continuation. Prior packets, original serials, work orders and observations remain unchanged.

`changes.md` compares the actual graphs. Finding history distinguishes new, still detected and no longer detected
IDs; an ID includes compared values, so a changed value produces a new finding. **No longer detected is not
accepted or closed.** Confirm whether a changed/omitted value, revised history or accepted correction explains
the difference. A later replacement retains the same scoped functional position and its earlier work orders.
The latest dated closed order **per attribute** supplies the comparison value. An old order can still supply an
attribute missing from a newer one; that is a review basis, not a claim of physical current state.

Before interpreting a disappearance, read the **comparison basis** section near the top of the returned report.
`comparison-basis.json` compares loaded local code hashes, recorded Python version, cutoff, effective column/date/
encoding settings, source revisions and original bytes. It also lists added, removed and changed normalized records,
with exact before/after values and original row origins. A reordered row is not a changed value. A missing order is
not evidence that its installation was reversed. Older packets without usable method/runtime pins report unknown
continuity. Hashes do not authenticate a receipt or fully lock the environment.

A warning means the basis changed and needs explanation; ordinary corrected exports also produce it. An unchanged
recorded basis does not establish acceptance or completeness. Compare the finding history with the row and mapping
changes before asking owners to accept a correction. The [two disappearance controls](../examples/maintenance-intake/BASIS_CONTROLS.md)
show identical bytes with an ignored serial column, and omitted closed history, against a retained older packet.

No earlier authenticated decisions are imported automatically. This tool creates observations and draft action
rows; record owners accept corrections in their own systems and read them back. Retain their acceptance evidence
in the company workflow. PM/spares, photos, datasheets and MOC need the broader [maintenance workflow](MAINTENANCE_START.md).
Do not infer a validated PM strategy, approved engineering change or plant health from this two-export check.

## Evidence and limits

The packet pins all generated files, originals, profile, previous receipt/inventory, loaded local Python modules
and Python version. Inventory verification detects ordinary modification; these are hashes, not authenticated
signatures. The full prior packet must be retained to reopen its original rows. No automatic watcher, connector,
concurrent shared editing, source-system write or complete environment lock is supplied.

The [worked example](../examples/maintenance-intake/README.md) exercises a corrected export and a second replacement.
Regression controls also cover changed headers, missing inputs, partial coverage, dates and preserved originals.
These are exposed fictional software checks. No manager benefit or company acceptance is measured.
