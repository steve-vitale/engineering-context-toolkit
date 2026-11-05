# Running the map at a plant

This is for the people who would keep a site's map current: the map owner and the owners of each record. It says
which existing plant routines update the map, who does what, which command to run and what the toolkit cannot do
yet. The commands are described in [ONE_MAP.md](ONE_MAP.md); the record formats in
[CONTEXT_MAP_FORMAT.md](CONTEXT_MAP_FORMAT.md). A worked example of one management of change (MOC) on a fictional
pasteurizer is in [examples/one-map](../examples/one-map/README.md#the-pasteurizer-through-an-moc-pid-revision-moc-open-and-close-work-order-walkdown).

The rule is no new process. The map is updated as a side effect of work the plant already does, by the people who
already own that work. Each owner keeps their own record (the maintenance equipment export, the instrument index,
the HACCP plan, the relief device register and so on) where it lives today; the map reads exports of those records,
compares them and sends each disagreement to the owner of the record that should change. It decides nothing:
approvals, sign-off and the history of a discussion stay in your company's existing systems or a governed service.

## Which routine updates what

`build` below is `python scripts/one_map.py build site.json --out map/` (the map); the other commands are
`one_map.py` subcommands on the graph it writes. Keep the previous `map/` (or its `graph.json`) when you rebuild, so
there is something to compare against.

| Routine | Trigger | Records touched | Owner | What to run | Not supported yet |
|---|---|---|---|---|---|
| **P&ID revision** | Doc control releases a new revision of a P&ID sheet | The drawing register (sheet index), that sheet's read, documents `based_on` the old revision | Doc control; engineering for the content | Update the drawing register and the sheet read, `build` (only the changed sheet is re-read; documents based on the old revision are reopened), then `changes OLD/graph.json NEW/graph.json --out release/` and attach `changes.md` to the release | Reading the new sheet image is the drawing reader's job (`sheet-from-prediction`), and its output is a draft to review; redlines are not captured |
| **MOC open** | An MOC is raised for some tags or a unit | None yet: this report is the starting point | The MOC owner; each department's representative | `affected --map map/graph.json --tags T1 T2 --out moc-open/`: every record and document that holds or names the tags, per owner, with open conflicts, expectation gaps and change flags (HACCP reassessment, PHA revalidation, criticality review). Tags not on the map yet are reported as new | The MOC record itself, its approvals and actions stay in your MOC system or a governed service; a document that names an item only in words the map cannot match is not in the report |
| **MOC close / pre-startup review** | The change is installed and records are said to be updated | Every record in the MOC-open report | Each record owner; the MOC owner checks | Refresh the exports, `build`, then `affected --tags ... --closeout OPEN/graph.json CLOSE/graph.json --out moc-close/` (changed vs still unchanged, per owner) and `changes OPEN CLOSE --tags ... --out moc-pack/` (before/after pack) | "Changed" does not prove the change is right, and "unchanged" may be correct; flags are not tracked; no pre-startup review checklist |
| **Work order closeout** | A work order that replaced equipment is closed | Work order history (`work_order` register: `installed_manufacturer`, `installed_model`, `installed_serial_number`, `installed_size`), the maintenance equipment export, the datasheet | Maintenance (planner or supervisor at closeout); engineering for datasheets | Export closed work orders to the work order CSV and `build`: an installed value that differs from the maintenance equipment export or instrument index is a conflict to that record's owner; one that differs from the datasheet is a "replacement may not be like-for-like" row to the datasheet owner (a possible MOC trigger, never decided) | No connection to the maintenance system; the export is a CSV you produce; part numbers and spares are not compared |
| **PM and calibration** | A calibration is done or falls overdue | Calibration records, PM plan | Maintenance; I&C; Quality for CCP instruments | Refresh the calibration record and PM plan exports and `build`: certified expectation rules raise "expected but missing" rows (a CCP instrument with an out-of-date calibration, a critical item with no PM plan) | Dates are judged against the site file's `as_of`; no scheduling or reminders |
| **Turnaround / outage** | Scope frozen for an outage | Every item in the scope | Turnaround planner; each record owner | Before: `affected --map map/graph.json --scope S1/P1/UNIT --out pre/` (records, open conflicts and gaps for the scope). After: `build`, `changes PRE POST --scope S1/P1/UNIT --out post/` and walkdown rulings (below) | Scope is given as tags or unit ids (no import of a turnaround scope file); redlines and as-left findings are entered by hand |
| **Walkdown / field verification** | A disputed conflict needs someone to look | The conflict; afterwards the record that was wrong | Whoever walks it down (engineering, operations, maintenance) | Fill a row of the `ruling` template with `authority` `field`, the date, who, the reason and `evidence` (photo file, nameplate reading or locator); `build --decisions rulings.csv`. The conflict is settled with a history line, and the owner of any record that still disagrees gets a "record differs from a ruling" row | No mobile capture; photos are stored wherever you keep them today |
| **HACCP verification and reassessment** | Annual reassessment, or a change on a CCP | HACCP plan CCPs (`ccp` register), calibration records, verification documents | Quality / food safety | `build` with the certified CCP rule: each CCP needs a critical limit, a monitoring instrument, an in-date calibration and a verification document. `changes` and `affected` flag "HACCP reassessment" when a changed item is a CCP's monitoring instrument or is named in a CCP row | The reassessment and any critical limit validation are the HACCP team's work |
| **CAPA** | A deviation, audit finding or incident raises a corrective action | CAPA register (`capa`) | Quality | Add the CAPA register export as a `records` entry: rows with a tag are listed in `affected` for that item | No CAPA rule; no count of open CAPAs per unit |
| **PHA / HAZOP revalidation** | The revalidation is due, or a major MOC | Relief device register, interlock list, the P&IDs since the last PHA | Process safety | Keep the graph from the last PHA and run `changes LAST_PHA/graph.json NOW/graph.json --scope S1/P1/UNIT` for what changed since; the certified relief rule checks each relief device protects something and has a test date; `changes` and `affected` flag "PHA revalidation" on relief devices and interlock causes and effects | PHA nodes, deviations and safeguards are not in the format (only as documents) |
| **Incident investigation** | An incident | Incident report (a document), the items involved | Safety | Add the report to the document manifest and `build`: its tag mentions link to items; `ask --question-kind documents --item TAG` lists every document about an item | No incident register |
| **Procurement and receiving** | A purchase order or receipt for a tagged item | Purchase order lines and MRO items (read-only copies in the format) | Procurement; stores | Purchase order lines with a tag are listed in `affected` for that item | No like-for-like check on purchase orders or receipts yet (only on work order closeout) |
| **New or revised document** | A controlled document is released | The document manifest (covers, based_on), the document's text | The document's owner | Add or update its manifest entry and `build`: tag and glossary mentions are found with a page, cell or line locator; documents based on an older revision are reopened | Text read by OCR never links (a person confirms each one); scanned pages are read only with `document_text.ocr` set to `auto` in the site file |
| **Onboarding an engineer** | A new person joins | None (read only) | Their lead | `ask --map map/graph.json --question-kind connects --item TAG` (also `measured-by`, `documents`, `disagreements`, `complete`): each answer carries its source, or says which record is missing | Answers only what the map holds |
| **Audit preparation** (food safety, insurer, process safety) | An audit is scheduled | CCP, relief device, calibration, CAPA records | Quality; process safety | `report.md` lists expectation results by rule; `affected --scope S1/P1/UNIT` gives the records per owner for the audited unit | No audit pack export |

## Operating model

**Owners.** One map owner, usually whoever owns the P&IDs (doc control or engineering). Each record keeps its
existing owner, named in the site file's `record_owners`. Each owner works only their own queue: the review queue is
split by owner (`queues/by-owner/`), and every conflict goes to the owner of the record that should change.

**Event-driven first.** The routines above update the map when they happen. Between them, about 15 minutes a week
per owner is enough to work their queue: settle or correct the oldest rows first.

**Monthly export refresh.** Once a month, export the maintenance equipment export, the instrument index and the
other records again and `build`. The map compares them with the P&IDs and with each other; `changes` against last
month's graph shows what moved.

**Two numbers to watch.**

1. Open review rows by owner and age (count the rows in each `queues/by-owner/*.csv`; keep last month's to see the
   age). The oldest row getting older means the routine is failing, not the people.
2. Expectation coverage by unit: how many subjects of each certified rule are complete (the expectation results in
   `report.md` and `graph.json`), for example CCPs complete and relief devices complete.

**Roll out one unit and one rule at a time.** Start with the unit that has work coming (an MOC or a turnaround).
Expectation rules ship as drafts: a draft rule only raises one summary row per unit. A person certifies a rule
(status, by, on) to let it raise rows; `rollout.scopes` limits it to the first units and `rollout.owners` to the
owners who are ready; `limit_per_scope` caps how many rows one unit gets at once. Certify the CCP rule for one
pasteurizer, read its rows, fix the rule or the records, widen the rollout, then certify the next rule. Glossary
terms work the same way: a draft term only produces rows to confirm.

**What stays outside the map.** Who approves, who signs off, reminders and escalation, and the record of a
discussion belong to your company's existing systems or a governed service. The map keeps each disagreement, the
ruling that settled it and the reason.

## Does this add work?

It should replace work, not add it. The MOC-open report replaces each representative searching their own records for
the tags; the closeout check replaces asking each owner "did you update it?"; the work order check replaces finding
out at the next walkdown that the maintenance equipment export is wrong. It adds work in three places, which a site
should plan for:

- someone has to export the records (monthly, and at MOC close) in the documented CSV formats;
- record owners have to settle the rows sent to them, including the false alarms: a record that names a tag in
  words the map cannot match is missed, and some rows will need nothing changed;
- the map owner keeps the site file (plants, units, record owners) and the drawing register current.

Nothing here is proven at a real plant: the examples are fictional and the time estimates above are not measured.
