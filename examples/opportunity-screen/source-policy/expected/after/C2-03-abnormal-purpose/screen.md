# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/source-policy/models/C2-03-abnormal-purpose.json`. Questions: `data/questions.json`.

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

**About:** FT-A, PT-B  

**Finding reference (JSON string):** `"C2@model"`
**Asset IDs (JSON array):** `["FT-A", "PT-B", "IL-B", "FIC-A"]`

**Evidence on the drawing / model**

- instrument FT-A reads "FT-A Supplied fictional instrument" at U-A (`instruments[FT-A]`)
- instrument PT-B reads "PT-B Supplied fictional instrument" at U-A (`instruments[PT-B]`)
- Interlock that reads it: interlock IL-B reads "IL-B Fictional pressurecondition Fictional valveaction, notapproved" (`interlocks[IL-B]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-A reads "FIC-A Fictional supplied controller" at U-A (`controllers[FIC-A]`)
- Supplied candidate field: `"FT-A fictional_record = true; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.fictional_record"`)
- Supplied candidate field: `"FT-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_source"`)
- Supplied candidate field: `"FT-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_revision"`)
- Supplied candidate field: `"FT-A record_available = true; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_available"`)
- Supplied candidate field: `"FT-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_authority"`)
- Supplied candidate field: `"FT-A purpose = \"normalcontrol\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.purpose"`)
- Supplied candidate field: `"PT-B fictional_record = true; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.fictional_record"`)
- Supplied candidate field: `"PT-B record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.record_source"`)
- Supplied candidate field: `"PT-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.record_revision"`)
- Supplied candidate field: `"PT-B record_available = true; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.record_available"`)
- Supplied candidate field: `"PT-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.record_authority"`)
- Supplied candidate field: `"PT-B purpose = \"abnormalprotectiveindication\"; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.purpose"`)
- Supplied candidate field: `"PT-B logic_coverage = \"notreviewed\"; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.logic_coverage"`)
- Supplied candidate field: `"PT-B manual_adjustments = 0; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.manual_adjustments"`)
- Supplied candidate field: `"PT-B alarm_action = \"sourceclaimedoperatorresponse\"; present; meaning and suitability unverified"` (`"instruments[PT-B].facts.alarm_action"`)
- Supplied candidate field: `"IL-B fictional_record = true; present; meaning and suitability unverified"` (`"interlocks[IL-B].facts.fictional_record"`)
- Supplied candidate field: `"IL-B record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"interlocks[IL-B].facts.record_source"`)
- Supplied candidate field: `"IL-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"interlocks[IL-B].facts.record_revision"`)
- Supplied candidate field: `"IL-B record_available = true; present; meaning and suitability unverified"` (`"interlocks[IL-B].facts.record_available"`)
- Supplied candidate field: `"IL-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"interlocks[IL-B].facts.record_authority"`)
- Supplied candidate field: `"IL-B record_scope = \"proposedprotection\"; present; meaning and suitability unverified"` (`"interlocks[IL-B].facts.record_scope"`)
- Supplied candidate field: `"FIC-A fictional_record = true; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.fictional_record"`)
- Supplied candidate field: `"FIC-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_source"`)
- Supplied candidate field: `"FIC-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_revision"`)
- Supplied candidate field: `"FIC-A record_available = true; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_available"`)
- Supplied candidate field: `"FIC-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_authority"`)
- Supplied candidate field: `"FIC-A mode = \"auto\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.mode"`)
- On drawing: Supplied candidate fact, basis unverified: FT-A fictional_record = True (`instruments[FT-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PT-B fictional_record = True (`instruments[PT-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: FT-A record_source = Fictional pre-call record, no company or human approval (`instruments[FT-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PT-B record_source = Fictional pre-call record, no company or human approval (`instruments[PT-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FT-A record_revision = R1 (`instruments[FT-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PT-B record_revision = R1 (`instruments[PT-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FT-A record_available = True (`instruments[FT-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PT-B record_available = True (`instruments[PT-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: FT-A record_authority = unverified (`instruments[FT-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: PT-B record_authority = unverified (`instruments[PT-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: FT-A purpose = normalcontrol (`instruments[FT-A].facts.purpose`)
- On drawing: Supplied candidate fact, basis unverified: PT-B purpose = abnormalprotectiveindication (`instruments[PT-B].facts.purpose`)
- On drawing: Supplied candidate fact, basis unverified: PT-B logic_coverage = notreviewed (`instruments[PT-B].facts.logic_coverage`)
- On drawing: Supplied candidate fact, basis unverified: PT-B manual_adjustments = 0 (`instruments[PT-B].facts.manual_adjustments`)
- On drawing: Supplied candidate fact, basis unverified: PT-B alarm_action = sourceclaimedoperatorresponse (`instruments[PT-B].facts.alarm_action`)
- On drawing: Supplied candidate fact, basis unverified: FT-A fictional_record = True (`instruments[FT-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PT-B fictional_record = True (`instruments[PT-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: FT-A record_source = Fictional pre-call record, no company or human approval (`instruments[FT-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PT-B record_source = Fictional pre-call record, no company or human approval (`instruments[PT-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FT-A record_revision = R1 (`instruments[FT-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PT-B record_revision = R1 (`instruments[PT-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FT-A record_available = True (`instruments[FT-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PT-B record_available = True (`instruments[PT-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: FT-A record_authority = unverified (`instruments[FT-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: PT-B record_authority = unverified (`instruments[PT-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: FT-A purpose = normalcontrol (`instruments[FT-A].facts.purpose`)
- On drawing: Supplied candidate fact, basis unverified: PT-B purpose = abnormalprotectiveindication (`instruments[PT-B].facts.purpose`)
- On drawing: Supplied candidate fact, basis unverified: PT-B logic_coverage = notreviewed (`instruments[PT-B].facts.logic_coverage`)
- On drawing: Supplied candidate fact, basis unverified: PT-B manual_adjustments = 0 (`instruments[PT-B].facts.manual_adjustments`)
- On drawing: Supplied candidate fact, basis unverified: PT-B alarm_action = sourceclaimedoperatorresponse (`instruments[PT-B].facts.alarm_action`)

**Data to collect**

- Whether operators adjust anything by hand from these readings [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): FT-A (FT-A) fictional_record = true [instruments[FT-A].facts.fictional_record]; PT-B (PT-B) fictional_record = true [instruments[PT-B].facts.fictional_record]; FT-A (FT-A) record_source = "Fictional pre-call record, no company or human approval" [instruments[FT-A].facts.record_source]; PT-B (PT-B) record_source = "Fictional pre-call record, no company or human approval" [instruments[PT-B].facts.record_source]; FT-A (FT-A) record_revision = "R1" [instruments[FT-A].facts.record_revision]; PT-B (PT-B) record_revision = "R1" [instruments[PT-B].facts.record_revision]; FT-A (FT-A) record_available = true [instruments[FT-A].facts.record_available]; PT-B (PT-B) record_available = true [instruments[PT-B].facts.record_available]; FT-A (FT-A) record_authority = "unverified" [instruments[FT-A].facts.record_authority]; PT-B (PT-B) record_authority = "unverified" [instruments[PT-B].facts.record_authority]; FT-A (FT-A) purpose = "normalcontrol" [instruments[FT-A].facts.purpose]; PT-B (PT-B) purpose = "abnormalprotectiveindication" [instruments[PT-B].facts.purpose]; PT-B (PT-B) logic_coverage = "notreviewed" [instruments[PT-B].facts.logic_coverage]; PT-B (PT-B) manual_adjustments = 0 [instruments[PT-B].facts.manual_adjustments]; PT-B (PT-B) alarm_action = "sourceclaimedoperatorresponse" [instruments[PT-B].facts.alarm_action]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact measurement/source identity and quantity, actual indication/control/alarm/protection/recording purpose, normal and abnormal decisions, operator logs/round sheets and current availability/quality/coverage; retain per-subject association and source/revision.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Frequent manual adjustment can justify a control investigation, not automatic automation. A reading with no routine manual action may have a legitimate abnormal/alarm/protection/indication purpose; do not close it solely because nobody regularly acts. Acknowledge suitable existing purpose, manual or automatic operation, and record unresolved function/source suitability. No operator trial, live change or benefit is inferred.
- The control system's own loop list [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): FT-A (FT-A) fictional_record = true [instruments[FT-A].facts.fictional_record]; PT-B (PT-B) fictional_record = true [instruments[PT-B].facts.fictional_record]; FT-A (FT-A) record_source = "Fictional pre-call record, no company or human approval" [instruments[FT-A].facts.record_source]; PT-B (PT-B) record_source = "Fictional pre-call record, no company or human approval" [instruments[PT-B].facts.record_source]; FT-A (FT-A) record_revision = "R1" [instruments[FT-A].facts.record_revision]; PT-B (PT-B) record_revision = "R1" [instruments[PT-B].facts.record_revision]; FT-A (FT-A) record_available = true [instruments[FT-A].facts.record_available]; PT-B (PT-B) record_available = true [instruments[PT-B].facts.record_available]; FT-A (FT-A) record_authority = "unverified" [instruments[FT-A].facts.record_authority]; PT-B (PT-B) record_authority = "unverified" [instruments[PT-B].facts.record_authority]; FT-A (FT-A) purpose = "normalcontrol" [instruments[FT-A].facts.purpose]; PT-B (PT-B) purpose = "abnormalprotectiveindication" [instruments[PT-B].facts.purpose]; PT-B (PT-B) logic_coverage = "notreviewed" [instruments[PT-B].facts.logic_coverage]; PT-B (PT-B) manual_adjustments = 0 [instruments[PT-B].facts.manual_adjustments]; PT-B (PT-B) alarm_action = "sourceclaimedoperatorresponse" [instruments[PT-B].facts.alarm_action]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing current loop/point list, cause/effect, alarm/sequence/configuration and represented reader/interlock/source records; preserve exact endpoints and identify missing model coverage before concluding indication-only.; then DCS/PLC configuration: Review a permitted current loop/point/configuration export, if available, as an existing source rather than a complete plant-truth inventory.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A controller or interlock reference is useful supplied evidence, not proof of complete current logic, correct process meaning, safety adequacy or measurement authority. A partial model without controllers can still prompt existing-record clarification; it does not prove no installed controls or require a fabricated loop list. S19 printed30 is broad monitoring/process-control guidance, not a per-reading automation acceptance test.

**How it is decided:** Review measurement purpose and actual normal/abnormal decisions, represented readers and source/logic coverage with the responsible specialist. Neither a missing model controller nor a represented reader settles installed control completeness or the need for automation. Suitable existing use or nonapplicability can be acknowledged; unresolved records remain explicit. No automatic upgrade, safety acceptance or source-reported saving is assigned.

**What the source says (S19):** "energy and cost savings are around 5% or more for many industrial applications of process control systems" (for plants without updated controls). Process control: "Typically 2-18% savings." The source says these figures "cannot be added".

**Limits:** Source review: S19 originalLBNL56183 official mirror printed30/PDF38, monitoring/process-control section and historical nonadditive table. This supports a bounded records investigation, not an automation decision, current control-system completeness or a measurement's safety/function truth. Six existing variable classes retained; other instrument classes remain outside this selector. Generic historical savings are not this plant's benefit.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
