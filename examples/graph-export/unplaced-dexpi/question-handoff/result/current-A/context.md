# Engineering context register

Draft for engineering review. Source match and plant truth are separate explicit verdicts; unknown is never upgraded by this tool.

## C3@model: What valve-position feedback and diagnostic records are available for these control valves?

State: **partial**; owner: **Fictional controls-records owner**; present in current input: yes.

Owner assigned by Fictional task coordinator on 2026-11-01.

Collection prompts from the screen. These are not per-request completion records; an answer does not automatically satisfy or clear them.

- **Existing valve/loop feedback and diagnostic records**
  Candidate scope: anchors
  Screen-time candidate facts; meaning and suitability unverified in the original screen. Current per-request completion is not tracked here.
  No candidate values found in the selected model records.
  How: For each named valve/loop, review the record target, revision/locator, declared signal function, units, enabled return path and diagnostic capability. Keep command/current/travel setpoint separate from measured stem or shaft travel; local positioner feedback does not establish control-room or historian availability. Nearby Z tags and shared unit/stream membership do not establish valve association. Acknowledge appropriate existing coverage, including endpoint indication for an on/off duty, and retain unresolved source questions. Supplied fields do not complete this review.
  Where: DCS/PLC configuration: approved existing valve/positioner configuration and point definitions for each named valve and loop
  Where: maintenance records: existing valve, positioner and calibration records
  Where: site records: approved loop drawings, I/O mappings, source revisions and locators

- **Existing valve performance and diagnostic history**
  Candidate scope: anchors
  Screen-time candidate facts; meaning and suitability unverified in the original screen. Current per-request completion is not tracked here.
  No candidate values found in the selected model records.
  How: Review available history first. Retain valve/loop identity, source revision/locator, time and operating conditions, enabled state, quality/calibration and readability. Where suitable, compare command, independently described travel and process response over coincident periods. Position indication, endpoint states or oscillation alone do not diagnose stiction or its cause. Keep disabled, bad-quality, unavailable, foreign and unknown records as qualified candidates; ask the responsible record owner for the missing basis. This screen specifies no new manual step test, loop-mode change or operating experiment.
  Where: historian or DCS trend for FV-04 (no historian tag is mapped in this model for these)
  Where: maintenance records: existing diagnostic, inspection and work-order reports for the named valve
  Where: site records: previously acquired command, measured-travel and process-response history with its operating basis

Decision rule from the screen: Record appropriate existing feedback/diagnostics as coverage with its source scope and remaining gaps. Route a named valve/loop request to the responsible record owner where function, association, availability or performance evidence is unresolved. Configuration, tuning, process and assembly causes remain open when investigating reported behavior. Any further test or change requires a separate company-approved method and operating/outage decision; this finding prescribes no retrofit, retune, new connection or mode change.

Limits from the screen: P&IDs can omit fitted positioners. Drawing omission, local feedback, an enabled control-room return, historian availability and verified plant conditions are separate claims. Discrete endpoint feedback is not a continuous travel trace and is not automatically unsuitable for an on/off duty. Supplied source/quality flags and reported abnormalities are unverified evidence, not installed-state checks, unique diagnoses or permission to test/change equipment.

- `n114-partial-command-1`: **current**, accepted, partial; `command-basis-not-travel` = **logical command interpretation only; installed travel feedback unknown**.
  The supplied reader model represents a logical FT-04 -> FIC-04 -> FV-04 command/process-measurement chain. FT-04 is assigned flow context, not measured valve travel. Owning equipment, operating tag identity, positioner/travel feedback, control-room return and historian availability remain unverified. Request existing loop, I/O, positioner and maintenance records from the responsible role; no field test or retrofit is authorized.
  Source: N114-FICTIONAL-NOTE, revision A, lines 3–5; SHA-256 `7f90972cd32cad65e58b901934be4946506e74a51e562f692d030d259d0e8cb4`.
  Source match: match; plant truth: unknown; reviewer: Fictional source-review role, reviewed on: 2026-11-01; owner at decision: Fictional controls-records owner.
  Note: Entire note, actors and decision are fictional software fixtures; no authenticated review or operating authorization.

Immutable history: 1 decisions, 1 ownership assignments. Full old evidence snapshots are in context.json.

A repeated answer_id explicitly revises that answer. Independent answers need different answer ids. Different canonical values under one claim_key remain disputed until an engineer explicitly revises or rejects an answer. Prose wording is not compared for agreement.
