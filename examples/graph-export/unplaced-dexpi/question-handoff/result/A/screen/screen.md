# Opportunity screen: DEXPI XML I04V01-VER.EX01.xml

Model: `examples/graph-export/unplaced-dexpi/question-handoff/result/A/model.json`. Questions: `data/questions.json`.

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

**About:** FV-04  

**Finding reference (JSON string):** `"C3@model"`
**Asset IDs (JSON array):** `["FV-04", "FIC-04"]`

**Evidence on the drawing / model**

- Trigger: `"valve FV-04 reads \"FV-04 Globe valve operated by actuating system FV-04\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"FV-04\", \"kind\": \"final_element\", \"unit\": null, \"stream\": \"PipingNetworkSystem-1\", \"source\": \"DEXPI XML GlobeValve-1 (GlobeValve), operated by ActuatingSystem-1 (ActuatingSystem)\", \"dexpi_id\": \"GlobeValve-1\", \"dexpi_class\": \"GlobeValve\", \"tag_basis\": \"PipingComponentNumberAssignmentClass of the operated valve\", \"unit_basis\": \"no unit reachable through the piping from GlobeValve-1\", \"unplaced_reason\": \"final_elements need a unit; no unit reachable through the piping from GlobeValve-1\"}"` (`"unplaced[FV-04]"`)
- Controller-command candidate; not measured valve travel: `"controller FIC-04 reads \"FIC-04 FIC-04: flow, indicate, control (central location)\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"FIC-04\", \"source\": \"DEXPI XML ProcessInstrumentationFunction-1 (ProcessInstrumentationFunction)\", \"dexpi_id\": \"ProcessInstrumentationFunction-1\", \"dexpi_class\": \"ProcessInstrumentationFunction\", \"tag_basis\": \"category + functions + number attributes\"}; Exact recorded endpoint fields: {\"measurement_unplaced\": \"FT-04\", \"output_unplaced\": \"FV-04\", \"output\": {}}; Exact endpoints retained for this screen: {\"measurements\": [\"FT-04\"], \"outputs\": [\"FV-04\"], \"sets\": []}; Referenced instrument \"FT-04\": {\"tag\": \"FT-04\", \"kind\": \"instrument\", \"unit\": null, \"stream\": \"PipingNetworkSystem-2\", \"source\": \"DEXPI XML ProcessSignalGeneratingFunction-1 (ProcessSignalGeneratingFunction) in ProcessInstrumentationFunction-1\", \"dexpi_id\": \"ProcessSignalGeneratingFunction-1\", \"dexpi_class\": \"ProcessSignalGeneratingFunction\", \"tag_basis\": \"ASSIGNED here: the sensor has no number in the file\", \"assigned_tag\": true, \"unit_basis\": \"no unit reachable through the piping from FlowMeasuringElement-1\", \"unplaced_reason\": \"instruments need a unit; no unit reachable through the piping from FlowMeasuringElement-1\", \"variable\": \"flow\", \"part_of\": \"FIC-04\"}; \"FT-04\" has an assigned identifier, not a verified operating tag; Referenced final_element \"FV-04\": {\"tag\": \"FV-04\", \"kind\": \"final_element\", \"unit\": null, \"stream\": \"PipingNetworkSystem-1\", \"source\": \"DEXPI XML GlobeValve-1 (GlobeValve), operated by ActuatingSystem-1 (ActuatingSystem)\", \"dexpi_id\": \"GlobeValve-1\", \"dexpi_class\": \"GlobeValve\", \"tag_basis\": \"PipingComponentNumberAssignmentClass of the operated valve\", \"unit_basis\": \"no unit reachable through the piping from GlobeValve-1\", \"unplaced_reason\": \"final_elements need a unit; no unit reachable through the piping from GlobeValve-1\"}; A supplied command/process-measurement path is not measured valve travel or a verified physical signal path"` (`"controllers[FIC-04]"`)

**Data to collect**

- Existing valve/loop feedback and diagnostic records [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: DCS/PLC configuration: approved existing valve/positioner configuration and point definitions for each named valve and loop; then maintenance records: existing valve, positioner and calibration records; then site records: approved loop drawings, I/O mappings, source revisions and locators. How: For each named valve/loop, review the record target, revision/locator, declared signal function, units, enabled return path and diagnostic capability. Keep command/current/travel setpoint separate from measured stem or shaft travel; local positioner feedback does not establish control-room or historian availability. Nearby Z tags and shared unit/stream membership do not establish valve association. Acknowledge appropriate existing coverage, including endpoint indication for an on/off duty, and retain unresolved source questions. Supplied fields do not complete this review.
- Existing valve performance and diagnostic history [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian or DCS trend for FV-04 (no historian tag is mapped in this model for these); then maintenance records: existing diagnostic, inspection and work-order reports for the named valve; then site records: previously acquired command, measured-travel and process-response history with its operating basis. How: Review available history first. Retain valve/loop identity, source revision/locator, time and operating conditions, enabled state, quality/calibration and readability. Where suitable, compare command, independently described travel and process response over coincident periods. Position indication, endpoint states or oscillation alone do not diagnose stiction or its cause. Keep disabled, bad-quality, unavailable, foreign and unknown records as qualified candidates; ask the responsible record owner for the missing basis. This screen specifies no new manual step test, loop-mode change or operating experiment.

**How it is decided:** Record appropriate existing feedback/diagnostics as coverage with its source scope and remaining gaps. Route a named valve/loop request to the responsible record owner where function, association, availability or performance evidence is unresolved. Configuration, tuning, process and assembly causes remain open when investigating reported behavior. Any further test or change requires a separate company-approved method and operating/outage decision; this finding prescribes no retrofit, retune, new connection or mode change.

**What the source says (S13, S29, S30, S31, S32):** S13 discusses backlash/stiction and variability in highly throttled/oversized pumping systems, not a universal feedback retrofit. S29-S32 distinguish feedback routes and vendor-specific diagnostic/history examples. They establish no quantified benefit for this investigation or the supplied plant.

**Limits:** P&IDs can omit fitted positioners. Drawing omission, local feedback, an enabled control-room return, historian availability and verified plant conditions are separate claims. Discrete endpoint feedback is not a continuous travel trace and is not automatically unsuitable for an on/off duty. Supplied source/quality flags and reported abnormalities are unverified evidence, not installed-state checks, unique diagnoses or permission to test/change equipment.

## Sources cited above

- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
- S29: Emerson Automation Experts, Providing Operators Process Control Valve Position Feedback (2014-01-10; vendor guidance). https://www.emersonautomationexperts.com/2014/valves-actuators-regulators/providing-operators-process-control-valve-position-feedback/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S30: Emerson, Valve Positioners (product overview and digital-controller FAQ; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/valve-positioners (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S31: Emerson, Control Valve Diagnostics (product capabilities and status monitor; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-software/control-valve-diagnostics (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S32: Emerson Automation Experts, Impacts of Control Valve Diagnostics (2011-02-14; vendor guidance). https://www.emersonautomationexperts.com/2011/asset-management/impacts_of_cont/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
