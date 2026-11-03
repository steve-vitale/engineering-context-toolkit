# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/source-policy/models/C2-01-no-controllers.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
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

### C2: What do existing records establish about these measurements' purpose, readers and remaining source/logic coverage?

**About:** PT-A, TT-B  

**Finding reference (JSON string):** `"C2@model"`
**Asset IDs (JSON array):** `["PT-A", "TT-B"]`

**Evidence on the drawing / model**

- instrument PT-A reads "PT-A Supplied fictional instrument" (`instruments[PT-A]`)
- instrument TT-B reads "TT-B Supplied fictional instrument" (`instruments[TT-B]`)
- Supplied candidate field: `"PT-A fictional_record = true; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.fictional_record"`)
- Supplied candidate field: `"PT-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.record_source"`)
- Supplied candidate field: `"PT-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.record_revision"`)
- Supplied candidate field: `"PT-A record_available = true; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.record_available"`)
- Supplied candidate field: `"PT-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.record_authority"`)
- Supplied candidate field: `"PT-A purpose = \"unknown\"; blank; meaning and suitability unverified"` (`"instruments[PT-A].facts.purpose"`)
- Supplied candidate field: `"PT-A source_coverage = \"partialdrawing\"; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.source_coverage"`)
- Supplied candidate field: `"PT-A logic_coverage = null; blank; meaning and suitability unverified"` (`"instruments[PT-A].facts.logic_coverage"`)
- Supplied candidate field: `"TT-B fictional_record = true; present; meaning and suitability unverified"` (`"instruments[TT-B].facts.fictional_record"`)
- Supplied candidate field: `"TT-B record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"instruments[TT-B].facts.record_source"`)
- Supplied candidate field: `"TT-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[TT-B].facts.record_revision"`)
- Supplied candidate field: `"TT-B record_available = true; present; meaning and suitability unverified"` (`"instruments[TT-B].facts.record_available"`)
- Supplied candidate field: `"TT-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[TT-B].facts.record_authority"`)
- Supplied candidate field: `"TT-B purpose = \"indicationdeclared\"; present; meaning and suitability unverified"` (`"instruments[TT-B].facts.purpose"`)
- Supplied candidate field: `"TT-B source_coverage = \"partialdrawing\"; present; meaning and suitability unverified"` (`"instruments[TT-B].facts.source_coverage"`)
- Supplied candidate field: `"TT-B manual_adjustments = 0; present; meaning and suitability unverified"` (`"instruments[TT-B].facts.manual_adjustments"`)
- On drawing: Supplied candidate fact, basis unverified: PT-A fictional_record = True (`instruments[PT-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TT-B fictional_record = True (`instruments[TT-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_source = Fictional pre-call record, no company or human approval (`instruments[PT-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TT-B record_source = Fictional pre-call record, no company or human approval (`instruments[TT-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_revision = R1 (`instruments[PT-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TT-B record_revision = R1 (`instruments[TT-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_available = True (`instruments[PT-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TT-B record_available = True (`instruments[TT-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_authority = unverified (`instruments[PT-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TT-B record_authority = unverified (`instruments[TT-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TT-B purpose = indicationdeclared (`instruments[TT-B].facts.purpose`)
- On drawing: Supplied candidate fact, basis unverified: PT-A source_coverage = partialdrawing (`instruments[PT-A].facts.source_coverage`)
- On drawing: Supplied candidate fact, basis unverified: TT-B source_coverage = partialdrawing (`instruments[TT-B].facts.source_coverage`)
- On drawing: Supplied candidate fact, basis unverified: TT-B manual_adjustments = 0 (`instruments[TT-B].facts.manual_adjustments`)
- On drawing: Supplied candidate fact, basis unverified: PT-A fictional_record = True (`instruments[PT-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TT-B fictional_record = True (`instruments[TT-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_source = Fictional pre-call record, no company or human approval (`instruments[PT-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TT-B record_source = Fictional pre-call record, no company or human approval (`instruments[TT-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_revision = R1 (`instruments[PT-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TT-B record_revision = R1 (`instruments[TT-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_available = True (`instruments[PT-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TT-B record_available = True (`instruments[TT-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_authority = unverified (`instruments[PT-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TT-B record_authority = unverified (`instruments[TT-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TT-B purpose = indicationdeclared (`instruments[TT-B].facts.purpose`)
- On drawing: Supplied candidate fact, basis unverified: PT-A source_coverage = partialdrawing (`instruments[PT-A].facts.source_coverage`)
- On drawing: Supplied candidate fact, basis unverified: TT-B source_coverage = partialdrawing (`instruments[TT-B].facts.source_coverage`)
- On drawing: Supplied candidate fact, basis unverified: TT-B manual_adjustments = 0 (`instruments[TT-B].facts.manual_adjustments`)

**Data to collect**

- Whether operators adjust anything by hand from these readings [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PT-A (PT-A) fictional_record = true [instruments[PT-A].facts.fictional_record]; TT-B (TT-B) fictional_record = true [instruments[TT-B].facts.fictional_record]; PT-A (PT-A) record_source = "Fictional pre-call record, no company or human approval" [instruments[PT-A].facts.record_source]; TT-B (TT-B) record_source = "Fictional pre-call record, no company or human approval" [instruments[TT-B].facts.record_source]; PT-A (PT-A) record_revision = "R1" [instruments[PT-A].facts.record_revision]; TT-B (TT-B) record_revision = "R1" [instruments[TT-B].facts.record_revision]; PT-A (PT-A) record_available = true [instruments[PT-A].facts.record_available]; TT-B (TT-B) record_available = true [instruments[TT-B].facts.record_available]; PT-A (PT-A) record_authority = "unverified" [instruments[PT-A].facts.record_authority]; TT-B (TT-B) record_authority = "unverified" [instruments[TT-B].facts.record_authority]; TT-B (TT-B) purpose = "indicationdeclared" [instruments[TT-B].facts.purpose]; PT-A (PT-A) source_coverage = "partialdrawing" [instruments[PT-A].facts.source_coverage]; TT-B (TT-B) source_coverage = "partialdrawing" [instruments[TT-B].facts.source_coverage]; TT-B (TT-B) manual_adjustments = 0 [instruments[TT-B].facts.manual_adjustments]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact measurement/source identity and quantity, actual indication/control/alarm/protection/recording purpose, normal and abnormal decisions, operator logs/round sheets and current availability/quality/coverage; retain per-subject association and source/revision.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Frequent manual adjustment can justify a control investigation, not automatic automation. A reading with no routine manual action may have a legitimate abnormal/alarm/protection/indication purpose; do not close it solely because nobody regularly acts. Acknowledge suitable existing purpose, manual or automatic operation, and record unresolved function/source suitability. No operator trial, live change or benefit is inferred.
- The control system's own loop list [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PT-A (PT-A) fictional_record = true [instruments[PT-A].facts.fictional_record]; TT-B (TT-B) fictional_record = true [instruments[TT-B].facts.fictional_record]; PT-A (PT-A) record_source = "Fictional pre-call record, no company or human approval" [instruments[PT-A].facts.record_source]; TT-B (TT-B) record_source = "Fictional pre-call record, no company or human approval" [instruments[TT-B].facts.record_source]; PT-A (PT-A) record_revision = "R1" [instruments[PT-A].facts.record_revision]; TT-B (TT-B) record_revision = "R1" [instruments[TT-B].facts.record_revision]; PT-A (PT-A) record_available = true [instruments[PT-A].facts.record_available]; TT-B (TT-B) record_available = true [instruments[TT-B].facts.record_available]; PT-A (PT-A) record_authority = "unverified" [instruments[PT-A].facts.record_authority]; TT-B (TT-B) record_authority = "unverified" [instruments[TT-B].facts.record_authority]; TT-B (TT-B) purpose = "indicationdeclared" [instruments[TT-B].facts.purpose]; PT-A (PT-A) source_coverage = "partialdrawing" [instruments[PT-A].facts.source_coverage]; TT-B (TT-B) source_coverage = "partialdrawing" [instruments[TT-B].facts.source_coverage]; TT-B (TT-B) manual_adjustments = 0 [instruments[TT-B].facts.manual_adjustments]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing current loop/point list, cause/effect, alarm/sequence/configuration and represented reader/interlock/source records; preserve exact endpoints and identify missing model coverage before concluding indication-only.; then DCS/PLC configuration: Review a permitted current loop/point/configuration export, if available, as an existing source rather than a complete plant-truth inventory.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A controller or interlock reference is useful supplied evidence, not proof of complete current logic, correct process meaning, safety adequacy or measurement authority. A partial model without controllers can still prompt existing-record clarification; it does not prove no installed controls or require a fabricated loop list. S19 printed30 is broad monitoring/process-control guidance, not a per-reading automation acceptance test.

**How it is decided:** Review measurement purpose and actual normal/abnormal decisions, represented readers and source/logic coverage with the responsible specialist. Neither a missing model controller nor a represented reader settles installed control completeness or the need for automation. Suitable existing use or nonapplicability can be acknowledged; unresolved records remain explicit. No automatic upgrade, safety acceptance or source-reported saving is assigned.

**What the source says (S19):** "energy and cost savings are around 5% or more for many industrial applications of process control systems" (for plants without updated controls). Process control: "Typically 2-18% savings." The source says these figures "cannot be added".

**Limits:** Source review: S19 originalLBNL56183 official mirror printed30/PDF38, monitoring/process-control section and historical nonadditive table. This supports a bounded records investigation, not an automation decision, current control-system completeness or a measurement's safety/function truth. Six existing variable classes retained; other instrument classes remain outside this selector. Generic historical savings are not this plant's benefit.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
