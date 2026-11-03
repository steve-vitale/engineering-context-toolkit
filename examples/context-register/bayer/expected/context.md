# Engineering context register

Draft for engineering review. Source match and plant truth are separate explicit verdicts; unknown is never upgraded by this tool.

## E18@model: What do existing records establish about these cooling/steam-labelled candidates' process-stream duties and any system-level heat-integration question?

State: **unanswered**; owner: **needs owner**; present in current input: yes.

Collection prompts from the screen. These are not per-request completion records; an answer does not automatically satisfy or clear them.

- **Existing exact process-stream identities, temperature-enthalpy and duty basis**
  Candidate scope: anchors
  Screen-time candidate facts; meaning and suitability unverified in the original screen. Current per-request completion is not tracked here.
  No candidate values found in the selected model records.
  How: A CW or steam valve/instrument label is a proxy, not measured process heat rejection/heating, a process-stream identity or a flow signal. Retain each owner/source separately, including related steam-record values shown as candidate evidence. Review actual comparable process duties and uncertainty before inferring any match; command values, foreign data or incompatible units/periods cannot settle it.
  Where: only a valve (HV-112) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve
  Where: historian or DCS trend for FT-106 (no historian tag is mapped in this model for these)
  Where: site records: Existing process/utility identities and directions, actual supply/target temperatures, flows, heat-capacity/phase/duty and operating coverage for each represented cooling and steam candidate; source/revision/availability, quantity units and matching sample periods retained.
  Where: a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.

- **Existing process-wide targets and time-aware operating constraints**
  Candidate scope: anchors
  Screen-time candidate facts; meaning and suitability unverified in the original screen. Current per-request completion is not tracked here.
  No candidate values found in the selected model records.
  How: S19 printed43-45 describes process-wide composite curves, approach/capital-energy tradeoffs and developments for batch/time-aware integration and heat pumps/transformers. Do not replace that analysis with a rule that all hot temperatures must exceed all cold temperatures, or automatically close every non-simultaneous/batch pair. Conversely, overlapping ideal profiles or an alternative technology name is not proof of feasible recovery. Review the appropriate system and timing model before deciding.
  Where: site records: Existing heat/material balance, process-wide temperature-enthalpy/composite profiles and utility targets, batch sequences and timing, current studies and alternatives, with source scope and economic/operating assumptions.
  Where: a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.

- **Existing physical, material, fouling and hazard/feasibility basis**
  Candidate scope: anchors
  Screen-time candidate facts; meaning and suitability unverified in the original screen. Current per-request completion is not tracked here.
  No candidate values found in the selected model records.
  How: Existing suitable studies may be acknowledged without new measurements or a compulsory exchanger study. On reactive service an integration change needs the applicable hazard review; a missing review, supplied Boolean or source label is not protection acceptance. No piping connection, operating change, whole-process completeness or site saving follows from the represented pair.
  Where: site records: Existing layout/routing and fouling/cleaning records, composition/pressure/material and cross-contamination constraints, reactive/process hazard review, existing exchanger/network function and economic/practical basis; authority and missing records remain explicit.
  Where: a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.

Decision rule from the screen: Review the actual process-wide temperature-enthalpy/utility targets, stream identities and duty/time basis, practical approach/capital tradeoffs and physical/material/hazard constraints before an integration decision. Do not prescribe a connection or automatically close a question from a pairwise temperature-range, simultaneity, hours or distance shortcut. Suitable existing analysis or nonapplicability may be acknowledged; missing or contradictory source/units/time remains explicit.

Limits from the screen: The represented cooling-water and other-unit steam labels are screening proxies, not established process-stream duties or a feasible heat match. Review process-wide temperature-enthalpy targets, duty/time coverage and practical constraints; pairwise temperature ranges or simultaneity alone do not decide broader integration potential. On a reactive system any heat-integration change needs a hazard review first. IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: original LBNL-56183 printed43-45/PDF51-53 from the official ENERGY STAR mirror; raw equivalence to inaccessible catalog OSTI bytes is not claimed. The original far-exceeds comparative quotation remains historical; it is not evidence for this pair or a guarantee. Reactive-system hazard-review requirement is retained.

- `published-control-sequence`: **stale**, proposed, partial; `intended-heating-cooling-sequence` = **steam closed; recirculation redirected at setpoint**.
  The published narrative describes the intended sequence: at the temperature setpoint, steam flow closes and recirculation is redirected from the heater to the cooler. This is useful operating context, but it does not establish actual simultaneous duties, their duration, or an available heat-recovery opportunity.
  Source: CSB-2008-08-I-WV, revision final report; exact file pinned by SHA-256, PDF page 37 (printed page 29), temperature-control paragraph above Figure 10; narrative only; SHA-256 `6b4c944c7c5c8b5537c32e86d247064c164fe50c15d08ea64083975e574cf619`.
  Source match: unknown; plant truth: unknown; reviewer: not recorded, reviewed on: not recorded; owner at decision: needs owner.
  Reopened because: question content.
  Note: AI-authored proposed source interpretation; no owner, reviewer or site decision. Still collect representative temperatures/flows/duties, time alignment and overlap under comparable operating states, and layout/fouling evidence. Do not close E18 or calculate savings from this narrative. AI-authored re-proposal against expanded item evidence; prior proposal retained. No new human or plant review.

Immutable history: 2 decisions, 0 ownership assignments. Full old evidence snapshots are in context.json.

A repeated answer_id explicitly revises that answer. Independent answers need different answer ids. Different canonical values under one claim_key remain disputed until an engineer explicitly revises or rejects an answer. Prose wording is not compared for agreement.
