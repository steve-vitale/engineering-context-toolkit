# Opportunity screen: E6 fictional collection-scope development: E6-04-existing-period-coverage-B

Model: `examples/opportunity-screen/compressor-recycle-basis/models/E6-04-existing-period-coverage-B.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 1 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 1 |

## Energy

### E6: What do existing records show about this compressor's recycle or blow-off duty?

**About:** K-A  

**Finding reference (JSON string):** `"E6@K-A"`
**Asset IDs (JSON array):** `["K-A", "RV-A"]`

**Evidence on the drawing / model**

- equipment K-A reads "K-A Fictional compressor subject K-A" (`units[K-A]`)
- Recycle valve: final element RV-A reads "RV-A Recycle/bypass candidate; fictional unverified model association" at K-A (`final_elements[RV-A]`)
- Supplied candidate field: `"K-A control_records = [{\"record_id\": \"REC-PERIOD-B\", \"revision\": \"R1\", \"locator\": \"fictional record rows2-5\", \"machine_id\": \"K-A\", \"valve_id\": \"RV-A\", \"source_scope\": \"fictional training packet\", \"plant_truth\": \"unknown\", \"approval\": false, \"period\": \"same fictional6h\", \"covered_modes\": [\"normal\"], \"representative_basis\": null, \"known_missing\": [\"relevant turndown and upset context\"]}]; present; meaning and suitability unverified"` (`"units[K-A].facts.control_records"`)

**Data to collect**

- Existing control records, machine/service and operating-mode basis [not on drawing]. Where: site records: retained operating/control records with exact machine and valve IDs, record revision and locator; then historian or DCS trend for RV-A (no historian tag is mapped in this model for these); then DCS/PLC configuration: existing approved control documentation, if applicable; controller demand/output is not measured travel or flow. How: Start with existing records and check machine class, service and duty. Keep exact machine, valve and record IDs, revision, locator and supplied limitations. Resolve foreign, unknown or shared targets with the record owner; a model association does not verify installed pairing or sibling coverage. Distinguish controller demand/output, actual valve travel and measured flow, including units, quality and reference conditions. Select a representative period from demand and relevant normal, turndown, startup/shutdown and upset coverage, not a fixed month. Acknowledge suitable existing evidence and request only the remaining gaps.
- Applicable machine-protection basis and qualified review [not on drawing]. Where: site records: current site protection/control basis, applicable revision, conditions and responsible reviewer; then the vendor datasheet: the appropriate machine-specific operating envelope and protection guidance for the declared service. How: Review existing manufacturer/site records with the responsible machinery and controls engineers. Establish applicability to this machine, service, conditions and revision before interpreting a surge line or controller margin. A generic, obsolete or other-machine map cannot establish an excessive margin. Retain unresolved applicability and missing review; do not change settings, operate a valve or induce surge to answer this screen.
- Time-aligned real-power, pressure and flow evidence [not on drawing]. Where: site records: existing energy/operating records with measurement basis, units, quality, time and individual/shared machine coverage. How: Check existing records for time-aligned real input power, pressure, flow and operating conditions over the selected duty. Separate measured real power from estimates, nameplate ratings and apparent quantities. Check each record against the exact machine(s) and time covered. Reuse a shared record when its reviewed scope covers the named machines and time; do not infer missing individual coverage from a sibling trace. Keep zero, null and unknown values and limitations explicit. Agree any remaining evidence plan with the responsible owner; no new export, walkdown or test is compulsory when suitable records already exist.

**How it is decided:** Review the evidence and remaining gaps with the responsible process, controls and machinery engineers. Recycle/blow-off activity can reflect protection and demand; an open valve or a generic margin alone does not establish waste. Turndown/upset-only opening alone neither closes the investigation nor proves a deficiency. Acknowledge suitable working evidence and record the basis for concluding or continuing this screening investigation, its next owner and unresolved questions. No retrofit or quantified saving follows from this screen.

**What the source says (S11):** Blow-off "is a waste of energy and should be used only where necessary to avoid surge." Inlet throttling: "Capacity can typically be reduced from 100 percent capacity to about 70-80 percent with reasonable energy reduction." No % saving stated.

**Limits:** S11 describes compressed-air systems, including centrifugal-air controls; its examples and figures do not automatically apply to process gas, rotary or unknown machines. Establish machine/service applicability first. Supplied machine_class, service and control_records values are unverified claims, including approval/quality fields; showing them does not authenticate their source or establish installed function, protection adequacy or complete coverage. Keep unmatched records, unclear shared coverage and missing reference conditions unresolved. This screen authorizes no operation, test or protection/settings change; any proposed change needs responsible machinery/vendor expertise and the company change-review process.

## Safety questions to verify

### C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified?

**About:** K-A  

**Finding reference (JSON string):** `"C9@model"`
**Asset IDs (JSON array):** `["K-A"]`

**Evidence on the drawing / model**

- equipment K-A reads "K-A Fictional compressor subject K-A" (`units[K-A]`)

**Data to collect**

- Cause-and-effect matrix and HAZOP/LOPA records [not on drawing]. Where: site records: cause-and-effect matrix, HAZOP and LOPA reports; then DCS/PLC configuration: safety system configuration. How: Review existing cause-and-effect, governing requirements and configuration records for each named machine, with their revisions and applicability. Retain supplied trip/switch indications as candidates; a drawing label or an unrelated function does not settle the records or establish effective, tested protection. Missing model information is not evidence that installed protection is absent.
- Machine/function association and current evidence [not on drawing]. Where: site records: source-labelled function identifiers, initiating measurements, final elements and protected-machine targets, shared scope and revisions; governing requirements and validation/test evidence where applicable; then DCS/PLC configuration: existing configuration and its documented measurement/action/final-element identities, read through the approved site process. How: Keep each machine in the review even where a switch or trip is supplied. Retain all explicit shared targets and supplied qualifiers; unknown or contradictory targets remain unresolved. Same-model text or nearby equipment does not prove function coverage. Record a responsible person or authority separately from protected-machine association; neither is inferred here. This requests record review, not a new test, safety design or operating action.

**How it is decided:** A qualified site review may resolve the source-labelled machine/function associations and remaining record requests using applicable current evidence. A supplied trip, switch, cause/effect row or shared-function label alone establishes neither complete coverage nor installed protection adequacy. This screen grants no acceptance or authority and performs no safety validation.

**What the source says (no source):** Safety benefit; no energy source. Present it as a question to verify, not a finding.

**Limits:** P&IDs often leave trips to separate cause-and-effect records. Missing or unknown model evidence does not establish missing installed protection. Supplied associations, shared targets, revisions and contradictions require review; no machine, person owner, approval, tested condition or effective protection is inferred. C9 has no primary safety-design source cited in the catalog and remains a question for record review, not safety design, SIL assignment, a legal-compliance assessment or an operating recommendation.

## Not checked

- C2: the model holds no controllers; give a loop list with --loops (controller,measurement,output) to check this
- C6: the model holds no controllers; give a loop list with --loops to check this

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E2, E3, E4, E5, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, H1, H2, H3, H4, C1, C3, C4, C5, C7, C10, C8, E25, E26, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
