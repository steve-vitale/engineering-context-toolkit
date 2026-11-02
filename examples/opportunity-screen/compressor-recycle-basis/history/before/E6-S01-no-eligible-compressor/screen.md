# Opportunity screen: E6 fictional scope/control: E6-S01-no-eligible-compressor

Model: `E6-S01-no-eligible-compressor.json`. Questions: `data/questions.json`.

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

### E2: Is this pump oversized, given a bypass line around it or its valve?

**About:** P-A  

**Finding reference (JSON string):** `"E2@P-A"`
**Asset IDs (JSON array):** `["P-A", "RV-A"]`

**Evidence on the drawing / model**

- equipment P-A reads "P-A Fictional pump P-A" (`units[P-A]`)
- Bypass: final element RV-A reads "RV-A Recycle/bypass candidate; fictional unverified model association" at P-A (`final_elements[RV-A]`)

**Data to collect**

- Measured flow and head at normal operation [not on drawing]. Where: a walkdown: suction and discharge pressure gauges plus a clamp-on ultrasonic flow meter. How: Read flow and suction and discharge pressure at steady operation.
- Pump stated rated flow and head [not on drawing]. Where: the vendor datasheet: pump curve. How: Retain the stated rating and original units as model evidence; generic CAPACITY/DISCHARGE do not identify BEP.
- How often the bypass is open [not on drawing]. Where: a walkdown: valve position and line temperature; then site records: operator logs. How: Record bypass position over several shifts.
- Matched pump curve and best-efficiency-point (BEP) duty [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: the vendor datasheet: pump curve. How: Review the matching curve for installed impeller, speed, fluid and units, then identify its BEP flow/head with source revision and locator. Keep generic CAPACITY/DISCHARGE as rated candidates, not BEP. Retain unknown or unsuitable curve evidence and compare with representative measured operation.

**How it is decided:** Prioritize the pump if it runs at a flow 30% or more away from BEP or the bypass is used routinely; otherwise close this screening investigation.

**What the source says (S13, S14):** Five indications: "excessive flow noise, highly throttled flow control valves, heavy use of bypass lines, frequent replacements of bearings and seals, and intermittent pump operation." Prioritize pumps "with flow rates of 30% or more from the BEP flow rates, or with system imbalances greater than 20%." No % saving stated.

**Limits:** A drawn bypass may be normally closed; the drawing cannot show how it is used.

## Safety questions to verify

### C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified?

**About:** P-A  

**Finding reference (JSON string):** `"C9@model"`
**Asset IDs (JSON array):** `["P-A"]`

**Evidence on the drawing / model**

- equipment P-A reads "P-A Fictional pump P-A" (`units[P-A]`)

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

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, H1, H2, H3, H4, C1, C3, C4, C5, C7, C10, C8, E25, E26, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
- S14: Pumping Systems Tip #6, Match Pumps to System Requirements (DOE/GO-102005-2160). https://www.energy.gov/sites/prod/files/2014/05/f16/match_pumps_to_system.pdf (license: Public domain)
