# Opportunity screen: FICTIONAL valve feedback/source-adequacy development control

Model: `examples/opportunity-screen/valve-feedback-basis/models/C3-06-working-performance.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 0 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 1 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Controls and automation

### C3: What valve-position feedback and diagnostic records are available for these control valves?

**About:** FCV-A, FCV-B  

**Finding reference (JSON string):** `"C3@model"`
**Asset IDs (JSON array):** `["FCV-A", "FCV-B", "ZSO-A", "ZSC-A", "ZT-B", "HIST-B", "FIC-A", "FIC-B"]`

**Evidence on the drawing / model**

- valve FCV-A reads "FCV-A Fictional control-valve subject A" at U-A (`final_elements[FCV-A]`)
- valve FCV-B reads "FCV-B Fictional control-valve subject B" at U-B (`final_elements[FCV-B]`)
- Supplied position-tag candidate; valve/function association unverified: instrument ZSO-A reads "ZSO-A Supplied valve feedback/diagnostic record; declared quantity="discrete_open_limit"; declared target="FCV-A"" at U-A (`instruments[ZSO-A]`)
- Supplied position-tag candidate; valve/function association unverified: instrument ZSC-A reads "ZSC-A Supplied valve feedback/diagnostic record; declared quantity="discrete_closed_limit"; declared target="FCV-A"" at U-A (`instruments[ZSC-A]`)
- Supplied position-tag candidate; valve/function association unverified: instrument ZT-B reads "ZT-B Supplied valve feedback/diagnostic record; declared quantity="measured_stem_travel"; declared target="FCV-B"" at U-B (`instruments[ZT-B]`)
- Supplied feedback/diagnostic record candidate; association and suitability unverified: instrument HIST-B reads "HIST-B Supplied valve feedback/diagnostic record; declared quantity="command_travel_process_history"; declared target="FCV-B"" at U-B (`instruments[HIST-B]`)
- Controller-command candidate; not measured valve travel: controller FIC-A reads "FIC-A Fictional controller command target, not measured valve travel" at U-A (`controllers[FIC-A]`)
- Controller-command candidate; not measured valve travel: controller FIC-B reads "FIC-B Fictional controller command target, not measured valve travel" at U-B (`controllers[FIC-B]`)
- Supplied candidate field: `"FCV-A control_room_feedback_available = true; present; meaning and suitability unverified"` (`"final_elements[FCV-A].facts.control_room_feedback_available"`)
- Supplied candidate field: `"FCV-A declared_duty = \"on/off control\"; present; meaning and suitability unverified"` (`"final_elements[FCV-A].facts.declared_duty"`)
- Supplied candidate field: `"FCV-A endpoint_return_available = true; present; meaning and suitability unverified"` (`"final_elements[FCV-A].facts.endpoint_return_available"`)
- Supplied candidate field: `"FCV-A record_revision = \"A\"; present; meaning and suitability unverified"` (`"final_elements[FCV-A].facts.record_revision"`)
- Supplied candidate field: `"FCV-A source_kind = \"fictional record\"; present; meaning and suitability unverified"` (`"final_elements[FCV-A].facts.source_kind"`)
- Supplied candidate field: `"FCV-A underlying_claim_verified = false; present; meaning and suitability unverified"` (`"final_elements[FCV-A].facts.underlying_claim_verified"`)
- Supplied candidate field: `"FCV-B control_room_feedback_available = true; present; meaning and suitability unverified"` (`"final_elements[FCV-B].facts.control_room_feedback_available"`)
- Supplied candidate field: `"FCV-B feedback_enabled = true; present; meaning and suitability unverified"` (`"final_elements[FCV-B].facts.feedback_enabled"`)
- Supplied candidate field: `"FCV-B record_revision = \"A\"; present; meaning and suitability unverified"` (`"final_elements[FCV-B].facts.record_revision"`)
- Supplied candidate field: `"FCV-B source_kind = \"fictional record\"; present; meaning and suitability unverified"` (`"final_elements[FCV-B].facts.source_kind"`)
- Supplied candidate field: `"FCV-B underlying_claim_verified = false; present; meaning and suitability unverified"` (`"final_elements[FCV-B].facts.underlying_claim_verified"`)
- Supplied candidate field: `"ZSO-A endpoint_state = true; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.endpoint_state"`)
- Supplied candidate field: `"ZSO-A id = \"ZSO-A\"; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.id"`)
- Supplied candidate field: `"ZSO-A measures_valve = \"FCV-A\"; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.measures_valve"`)
- Supplied candidate field: `"ZSO-A quality = \"supplied_good\"; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.quality"`)
- Supplied candidate field: `"ZSO-A record_ref = \"ZSO-A-fictional-record\"; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.record_ref"`)
- Supplied candidate field: `"ZSO-A record_revision = \"A\"; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.record_revision"`)
- Supplied candidate field: `"ZSO-A signal_quantity = \"discrete_open_limit\"; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.signal_quantity"`)
- Supplied candidate field: `"ZSO-A source_kind = \"fictional record\"; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.source_kind"`)
- Supplied candidate field: `"ZSO-A underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[ZSO-A].facts.underlying_claim_verified"`)
- Supplied candidate field: `"ZSC-A endpoint_state = false; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.endpoint_state"`)
- Supplied candidate field: `"ZSC-A id = \"ZSC-A\"; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.id"`)
- Supplied candidate field: `"ZSC-A measures_valve = \"FCV-A\"; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.measures_valve"`)
- Supplied candidate field: `"ZSC-A quality = \"supplied_good\"; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.quality"`)
- Supplied candidate field: `"ZSC-A record_ref = \"ZSC-A-fictional-record\"; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.record_ref"`)
- Supplied candidate field: `"ZSC-A record_revision = \"A\"; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.record_revision"`)
- Supplied candidate field: `"ZSC-A signal_quantity = \"discrete_closed_limit\"; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.signal_quantity"`)
- Supplied candidate field: `"ZSC-A source_kind = \"fictional record\"; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.source_kind"`)
- Supplied candidate field: `"ZSC-A underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[ZSC-A].facts.underlying_claim_verified"`)
- Supplied candidate field: `"ZT-B feedback_enabled = true; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.feedback_enabled"`)
- Supplied candidate field: `"ZT-B id = \"ZT-B\"; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.id"`)
- Supplied candidate field: `"ZT-B measures_valve = \"FCV-B\"; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.measures_valve"`)
- Supplied candidate field: `"ZT-B quality = \"supplied_good\"; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.quality"`)
- Supplied candidate field: `"ZT-B record_ref = \"ZT-B-fictional-record\"; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.record_ref"`)
- Supplied candidate field: `"ZT-B record_revision = \"A\"; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.record_revision"`)
- Supplied candidate field: `"ZT-B signal_quantity = \"measured_stem_travel\"; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.signal_quantity"`)
- Supplied candidate field: `"ZT-B source_kind = \"fictional record\"; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.source_kind"`)
- Supplied candidate field: `"ZT-B underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[ZT-B].facts.underlying_claim_verified"`)
- Supplied candidate field: `"HIST-B id = \"HIST-B\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.id"`)
- Supplied candidate field: `"HIST-B measures_valve = \"FCV-B\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.measures_valve"`)
- Supplied candidate field: `"HIST-B operating_period = \"fictional steady-production interval\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.operating_period"`)
- Supplied candidate field: `"HIST-B record_owner = \"fictional maintenance role\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.record_owner"`)
- Supplied candidate field: `"HIST-B record_ref = \"HIST-B-fictional-record\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.record_ref"`)
- Supplied candidate field: `"HIST-B record_revision = \"A\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.record_revision"`)
- Supplied candidate field: `"HIST-B reported_condition = \"oscillation observed in report; cause unverified\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.reported_condition"`)
- Supplied candidate field: `"HIST-B signal_quantity = \"command_travel_process_history\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.signal_quantity"`)
- Supplied candidate field: `"HIST-B source_kind = \"fictional record\"; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.source_kind"`)
- Supplied candidate field: `"HIST-B underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[HIST-B].facts.underlying_claim_verified"`)
- Supplied candidate field: `"FIC-A record_revision = \"A\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_revision"`)
- Supplied candidate field: `"FIC-A source_kind = \"fictional record\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.source_kind"`)
- Supplied candidate field: `"FIC-A underlying_claim_verified = false; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.underlying_claim_verified"`)
- Supplied candidate field: `"FIC-B record_revision = \"A\"; present; meaning and suitability unverified"` (`"controllers[FIC-B].facts.record_revision"`)
- Supplied candidate field: `"FIC-B source_kind = \"fictional record\"; present; meaning and suitability unverified"` (`"controllers[FIC-B].facts.source_kind"`)
- Supplied candidate field: `"FIC-B underlying_claim_verified = false; present; meaning and suitability unverified"` (`"controllers[FIC-B].facts.underlying_claim_verified"`)
- On drawing: Supplied candidate fact, basis unverified: FCV-A control_room_feedback_available = True (`final_elements[FCV-A].facts.control_room_feedback_available`)
- On drawing: Supplied candidate fact, basis unverified: FCV-B control_room_feedback_available = True (`final_elements[FCV-B].facts.control_room_feedback_available`)
- On drawing: Supplied candidate fact, basis unverified: FCV-A endpoint_return_available = True (`final_elements[FCV-A].facts.endpoint_return_available`)
- On drawing: Supplied candidate fact, basis unverified: FCV-B feedback_enabled = True (`final_elements[FCV-B].facts.feedback_enabled`)
- On drawing: Supplied candidate fact, basis unverified: FCV-A declared_duty = on/off control (`final_elements[FCV-A].facts.declared_duty`)
- On drawing: Supplied candidate fact, basis unverified: FCV-A record_revision = A (`final_elements[FCV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FCV-B record_revision = A (`final_elements[FCV-B].facts.record_revision`)

**Data to collect**

- Existing valve/loop feedback and diagnostic records [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): FCV-A (FCV-A) control_room_feedback_available = true [final_elements[FCV-A].facts.control_room_feedback_available]; FCV-B (FCV-B) control_room_feedback_available = true [final_elements[FCV-B].facts.control_room_feedback_available]; FCV-A (FCV-A) endpoint_return_available = true [final_elements[FCV-A].facts.endpoint_return_available]; FCV-B (FCV-B) feedback_enabled = true [final_elements[FCV-B].facts.feedback_enabled]; FCV-A (FCV-A) declared_duty = "on/off control" [final_elements[FCV-A].facts.declared_duty]; FCV-A (FCV-A) record_revision = "A" [final_elements[FCV-A].facts.record_revision]; FCV-B (FCV-B) record_revision = "A" [final_elements[FCV-B].facts.record_revision]. The collection/review request remains open; supplied values or document references do not settle it. Where: DCS/PLC configuration: approved existing valve/positioner configuration and point definitions for each named valve and loop; then maintenance records: existing valve, positioner and calibration records; then site records: approved loop drawings, I/O mappings, source revisions and locators. How: For each named valve/loop, review the record target, revision/locator, declared signal function, units, enabled return path and diagnostic capability. Keep command/current/travel setpoint separate from measured stem or shaft travel; local positioner feedback does not establish control-room or historian availability. Nearby Z tags and shared unit/stream membership do not establish valve association. Acknowledge appropriate existing coverage, including endpoint indication for an on/off duty, and retain unresolved source questions. Supplied fields do not complete this review.
- Existing valve performance and diagnostic history [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian or DCS trend for FCV-A, FCV-B (no historian tag is mapped in this model for these); then maintenance records: existing diagnostic, inspection and work-order reports for the named valve; then site records: previously acquired command, measured-travel and process-response history with its operating basis. How: Review available history first. Retain valve/loop identity, source revision/locator, time and operating conditions, enabled state, quality/calibration and readability. Where suitable, compare command, independently described travel and process response over coincident periods. Position indication, endpoint states or oscillation alone do not diagnose stiction or its cause. Keep disabled, bad-quality, unavailable, foreign and unknown records as qualified candidates; ask the responsible record owner for the missing basis. This screen specifies no new manual step test, loop-mode change or operating experiment.

**How it is decided:** Record appropriate existing feedback/diagnostics as coverage with its source scope and remaining gaps. Route a named valve/loop request to the responsible record owner where function, association, availability or performance evidence is unresolved. Configuration, tuning, process and assembly causes remain open when investigating reported behavior. Any further test or change requires a separate company-approved method and operating/outage decision; this finding prescribes no retrofit, retune, new connection or mode change.

**What the source says (S13, S29, S30, S31, S32):** S13 discusses backlash/stiction and variability in highly throttled/oversized pumping systems, not a universal feedback retrofit. S29-S32 distinguish feedback routes and vendor-specific diagnostic/history examples. They establish no quantified benefit for this investigation or the supplied plant.

**Limits:** P&IDs can omit fitted positioners. Drawing omission, local feedback, an enabled control-room return, historian availability and verified plant conditions are separate claims. Discrete endpoint feedback is not a continuous travel trace and is not automatically unsuitable for an on/off duty. Supplied source/quality flags and reported abnormalities are unverified evidence, not installed-state checks, unique diagnoses or permission to test/change equipment.

## Sources cited above

- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
- S29: Emerson Automation Experts, Providing Operators Process Control Valve Position Feedback (2014-01-10; vendor guidance). https://www.emersonautomationexperts.com/2014/valves-actuators-regulators/providing-operators-process-control-valve-position-feedback/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S30: Emerson, Valve Positioners (product overview and digital-controller FAQ; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/valve-positioners (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S31: Emerson, Control Valve Diagnostics (product capabilities and status monitor; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-software/control-valve-diagnostics (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S32: Emerson Automation Experts, Impacts of Control Valve Diagnostics (2011-02-14; vendor guidance). https://www.emersonautomationexperts.com/2011/asset-management/impacts_of_cont/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
