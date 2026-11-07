# Replacement records review — manager brief

**Fictional example · draft handoff · decision still open**

Scope: Lakeside dairy, S1/P1/PAST1, FDV-2210 and TT-2208. Fictional source cut-off: 2026-11-04.
Question: after the valve replacement and drawing revision, do the selected records describe the same equipment,
and what remains for record owners to check before the company considers closeout?

## Decision requested

Assign the correction/review actions below and require receiving evidence before accepting this record handoff.
This packet does not establish operating/startup readiness, installed size, an appropriate PM program or MOC approval.
No person, due date, spending authorization or engineering acceptance is supplied by the example.

## What the evidence says

Inspect the original fictional [closed work orders](sources/records/work_orders-moc.csv),
[equipment export](sources/lists/maintenance_equipment-moc.csv), [valve datasheet](sources/lists/valve_datasheets.csv),
[PM export](sources/records/pm_plan.csv) and [supplied ruling](sources/walkdown_rulings.csv) alongside the reports.
The packet retains authored inputs; sheet reads are JSON, with no original plant CAD or valve photo.

- **Serial dispute settled in the supplied history; record correction outstanding.** Closed WO-60311 records
  AV-88412; equipment export CMMS-2026-10 row 7 still has AV-51007. Fictional ruling R-0101 chooses AV-88412.
  The ruling cites a fictional photo reference, not a retained photograph. Maintenance still needs an accepted
  correction and readback from its receiving system. [Conflict/history](evidence/conflicts.md),
  [queue](evidence/review_queue.csv), row with kind `record differs from a ruling`.
- **Size/design question open.** The closed work order and revised drawing reference DN65; the valve datasheet
  still says DN50. Engineering must reconcile applicability and design/field evidence and use the existing
  company change process. The tool flags a possible difference; it does not choose a size or decide MOC applicability.
- **PM evidence missing from the selected export.** Rule R-CRITICAL-PM finds no PM-plan row for this valve. Confirm
  export coverage and the existing approved maintenance strategy; this is not proof that the plant has no PM.
- **A green location row also exists for this valve.** It means the equipment was found on drawing PAST1-01:D3.
  It supplies no overall readiness verdict and does not settle the issues above.

## Proposed owner actions

All eight are **needs named owner / due date / recipient verification**. IDs below are authored for this packet.
They consolidate the selected source findings; they are not eight automatically created CMMS tasks.

| ID / department | Requested follow-up | Evidence and condition for accepting the handoff |
|---|---|---|
| M01 · Maintenance | Confirm the field ruling's identity/evidence and correct the equipment serial through the CMMS process. | Queue `record differs from a ruling`; R-0101/C-3e4451aaab. Retain accepted equipment ID/value, export/revision, reviewer and date. |
| E01 · Engineering | Reconcile DN65 versus DN50 and document the applicable design/installed basis and required company review. | Queue `replacement may not be like-for-like` and `P&ID value note`. Retain the disposition and updated datasheet/drawing, or the reason no change is required. |
| M02 · Maintenance | Establish whether the PM export covers this position and whether its approved plan is represented. | Queue `expected but missing`; R-CRITICAL-PM. Supply the existing approved record or a responsible disposition of the gap; do not invent a task or interval. |
| M03 · Maintenance | Confirm whether the equipment criticality needs review after the replacement. | Closeout `flag: criticality review`: not checked here. Retain the responsible person's actual review/disposition. |
| I01 · I&C | Confirm whether the unchanged loop record needs correction for the selected change. | Closeout LOOPS-PAST1: unchanged. Retain reviewed applicability or accepted revised record. |
| P01 · Production | Confirm the unchanged SOP remains applicable to the two selected tags. | Closeout SOP-PAST1-02: unchanged. Record the owner's basis or accepted correction. |
| Q01 · Quality | Confirm the HACCP reassessment and disposition of the unchanged CCP-related records. | Closeout `flag: HACCP reassessment`: not checked here; HACCP-P1-01: unchanged. Actual assessment and acceptance stay with the responsible team. |
| D01 · Doc control | Verify the selected released drawing and instrument-index handoff with Engineering/I&C. | Closeout shows drawing and instrument-index changes. Read the selected revision/IDs back from the agreed receiver; changed content alone is not acceptance. |

See the [complete selected closeout](evidence/closeout.md). It reports **7 changed, 7 unchanged, 2 reviews not
checked here and 1 still-open expectation gap** across record/item entries. These are not counts of assets,
completed actions or accepted corrections. The source queue has 33 rows across the broader fictional example,
including green rows; its row total is not the maintenance backlog.

## What a manager receives next

The coordinator returns a [review log](templates/review-log.md) with named people, due dates, evidence requests
and receiving verification. The manager and responsible record owners decide which unresolved matters block
the declared handoff; this packet supplies no operational approval. Preserve earlier versions, then repeat one
selected source change without losing the history.

Use the [scope form](templates/scope.md) before a real assignment and
[effort/outcome form](templates/effort-and-outcome.md) to decide whether the approach earns further work.
Human usefulness, review time, company readback and a subsequent accepted revision are **not observed** here.

For help scoping your own maintenance or engineering information job,
[connect with me on LinkedIn and message me there](https://www.linkedin.com/in/steve-vitale/).
This packet is part of the [Industrial Context Toolkit](https://github.com/steve-vitale/industrial-context-toolkit),
shared with its [MIT license](LICENSE.txt).
