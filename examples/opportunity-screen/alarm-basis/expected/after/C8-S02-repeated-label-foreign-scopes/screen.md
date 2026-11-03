# Opportunity screen: C8-S02-repeated-label-foreign-scopes

Model: `examples/opportunity-screen/alarm-basis/models/C8-S02-repeated-label-foreign-scopes.json`. Questions: `data/questions.json`.

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
| Safety questions to verify | 1 |

## Controls and automation

### C2: What do existing records establish about these measurements' purpose, readers and remaining source/logic coverage?

**About:** PAH-101, LAHH-201  

**Finding reference (JSON string):** `"C2@model"`
**Asset IDs (JSON array):** `["PAH-101", "LAHH-201"]`

**Evidence on the drawing / model**

- instrument PAH-101 reads "PAH-101 Fictional alarm candidate, not installed configuration" at U-A (`instruments[PAH-101]`)
- instrument LAHH-201 reads "LAHH-201 Fictional alarm candidate, not installed configuration" at U-B (`instruments[LAHH-201]`)
- Supplied candidate field: `"PAH-101 record_revision = \"r1\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_revision"`)
- Supplied candidate field: `"LAHH-201 record_revision = \"r1\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_revision"`)
- On drawing: Supplied candidate fact, basis unverified: PAH-101 record_revision = r1 (`instruments[PAH-101].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: LAHH-201 record_revision = r1 (`instruments[LAHH-201].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PAH-101 record_revision = r1 (`instruments[PAH-101].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: LAHH-201 record_revision = r1 (`instruments[LAHH-201].facts.record_revision`)

**Data to collect**

- Whether operators adjust anything by hand from these readings [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PAH-101 (PAH-101) record_revision = "r1" [instruments[PAH-101].facts.record_revision]; LAHH-201 (LAHH-201) record_revision = "r1" [instruments[LAHH-201].facts.record_revision]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact measurement/source identity and quantity, actual indication/control/alarm/protection/recording purpose, normal and abnormal decisions, operator logs/round sheets and current availability/quality/coverage; retain per-subject association and source/revision.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Frequent manual adjustment can justify a control investigation, not automatic automation. A reading with no routine manual action may have a legitimate abnormal/alarm/protection/indication purpose; do not close it solely because nobody regularly acts. Acknowledge suitable existing purpose, manual or automatic operation, and record unresolved function/source suitability. No operator trial, live change or benefit is inferred.
- The control system's own loop list [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PAH-101 (PAH-101) record_revision = "r1" [instruments[PAH-101].facts.record_revision]; LAHH-201 (LAHH-201) record_revision = "r1" [instruments[LAHH-201].facts.record_revision]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing current loop/point list, cause/effect, alarm/sequence/configuration and represented reader/interlock/source records; preserve exact endpoints and identify missing model coverage before concluding indication-only.; then DCS/PLC configuration: Review a permitted current loop/point/configuration export, if available, as an existing source rather than a complete plant-truth inventory.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A controller or interlock reference is useful supplied evidence, not proof of complete current logic, correct process meaning, safety adequacy or measurement authority. A partial model without controllers can still prompt existing-record clarification; it does not prove no installed controls or require a fabricated loop list. S19 printed30 is broad monitoring/process-control guidance, not a per-reading automation acceptance test.

**How it is decided:** Review measurement purpose and actual normal/abnormal decisions, represented readers and source/logic coverage with the responsible specialist. Neither a missing model controller nor a represented reader settles installed control completeness or the need for automation. Suitable existing use or nonapplicability can be acknowledged; unresolved records remain explicit. No automatic upgrade, safety acceptance or source-reported saving is assigned.

**What the source says (S19):** "energy and cost savings are around 5% or more for many industrial applications of process control systems" (for plants without updated controls). Process control: "Typically 2-18% savings." The source says these figures "cannot be added".

**Limits:** Source review: S19 originalLBNL56183 official mirror printed30/PDF38, monitoring/process-control section and historical nonadditive table. This supports a bounded records investigation, not an automation decision, current control-system completeness or a measurement's safety/function truth. Six existing variable classes retained; other instrument classes remain outside this selector. Generic historical savings are not this plant's benefit.

## Safety questions to verify

### C8: What do existing records show about alarm workload and response for each responsible operator scope?

**About:** PAH-101, LAHH-201  

**Finding reference (JSON string):** `"C8@model"`
**Asset IDs (JSON array):** `["PAH-101", "LAHH-201"]`

**Evidence on the drawing / model**

- instrument PAH-101 reads "PAH-101 Fictional alarm candidate, not installed configuration" at U-A (`instruments[PAH-101]`)
- instrument LAHH-201 reads "LAHH-201 Fictional alarm candidate, not installed configuration" at U-B (`instruments[LAHH-201]`)
- Supplied candidate field: `"PAH-101 record_reference = \"fictional:workload-report-B\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_reference"`)
- Supplied candidate field: `"PAH-101 record_revision = \"r1\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_revision"`)
- Supplied candidate field: `"PAH-101 operator_role = \"console-operator\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.operator_role"`)
- Supplied candidate field: `"PAH-101 console_id = \"CON-1\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.console_id"`)
- Supplied candidate field: `"PAH-101 underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.underlying_claim_verified"`)
- Supplied candidate field: `"PAH-101 record_console_id = \"CON-1\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_console_id"`)
- Supplied candidate field: `"PAH-101 site_namespace = \"fictional-site-A\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.site_namespace"`)
- Supplied candidate field: `"PAH-101 source_namespace = \"fictional-source-A\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.source_namespace"`)
- Supplied candidate field: `"PAH-101 workload_scope = \"fictional-site-A/CON-1/console-operator\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.workload_scope"`)
- Supplied candidate field: `"PAH-101 plant_truth = \"unknown\"; blank; meaning and suitability unverified"` (`"instruments[PAH-101].facts.plant_truth"`)
- Supplied candidate field: `"PAH-101 record_site_namespace = \"fictional-site-B\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_site_namespace"`)
- Supplied candidate field: `"PAH-101 record_source_namespace = \"fictional-source-B\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_source_namespace"`)
- Supplied candidate field: `"PAH-101 record_operator_role = \"console-operator\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_operator_role"`)
- Supplied candidate field: `"PAH-101 record_workload_scope = \"fictional-site-B/CON-1/console-operator\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_workload_scope"`)
- Supplied candidate field: `"PAH-101 record_coverage = \"provided record belongs to the other site/source scope despite matching console and role labels\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_coverage"`)
- Supplied candidate field: `"PAH-101 record_review_status = \"scope association unresolved; not actual company approval\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_review_status"`)
- Supplied candidate field: `"PAH-101 record_owner = \"fictional owner fictional-site-B\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_owner"`)
- Supplied candidate field: `"PAH-101 next_recipient = \"fictional operations-console owner fictional-site-A with alarm-system owner\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.next_recipient"`)
- Supplied candidate field: `"LAHH-201 record_reference = \"fictional:workload-report-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_reference"`)
- Supplied candidate field: `"LAHH-201 record_revision = \"r1\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_revision"`)
- Supplied candidate field: `"LAHH-201 operator_role = \"console-operator\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.operator_role"`)
- Supplied candidate field: `"LAHH-201 console_id = \"CON-1\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.console_id"`)
- Supplied candidate field: `"LAHH-201 underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.underlying_claim_verified"`)
- Supplied candidate field: `"LAHH-201 record_console_id = \"CON-1\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_console_id"`)
- Supplied candidate field: `"LAHH-201 site_namespace = \"fictional-site-B\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.site_namespace"`)
- Supplied candidate field: `"LAHH-201 source_namespace = \"fictional-source-B\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.source_namespace"`)
- Supplied candidate field: `"LAHH-201 workload_scope = \"fictional-site-B/CON-1/console-operator\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.workload_scope"`)
- Supplied candidate field: `"LAHH-201 plant_truth = \"unknown\"; blank; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.plant_truth"`)
- Supplied candidate field: `"LAHH-201 record_site_namespace = \"fictional-site-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_site_namespace"`)
- Supplied candidate field: `"LAHH-201 record_source_namespace = \"fictional-source-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_source_namespace"`)
- Supplied candidate field: `"LAHH-201 record_operator_role = \"console-operator\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_operator_role"`)
- Supplied candidate field: `"LAHH-201 record_workload_scope = \"fictional-site-A/CON-1/console-operator\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_workload_scope"`)
- Supplied candidate field: `"LAHH-201 record_coverage = \"provided record belongs to the other site/source scope despite matching console and role labels\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_coverage"`)
- Supplied candidate field: `"LAHH-201 record_review_status = \"scope association unresolved; not actual company approval\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_review_status"`)
- Supplied candidate field: `"LAHH-201 record_owner = \"fictional owner fictional-site-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_owner"`)
- Supplied candidate field: `"LAHH-201 next_recipient = \"fictional operations-console owner fictional-site-B with alarm-system owner\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.next_recipient"`)

**Data to collect**

- Alarm rate, floods and standing alarms [not on drawing]. Where: site records: existing alarm philosophy/register, defined-response procedures and scoped alarm journal or performance-review records; then site records: the responsible operations/console owner and alarm-system owner; existing operator feedback and record-scope review. How: Start with existing approved records. Confirm each record's operator responsibility, console/area, site/source, revision and operating periods. Distinguish presented alarms from status events, acknowledgements and returns to normal; retain journal filters, time basis and gaps. Review representative normal and available upset periods separately, including standing count/duration, nuisance patterns, required responses and operator feedback. Reuse a record when its reviewed scope covers several alarms or units; matching labels alone do not establish coverage. Acknowledge available evidence and ask only for missing records, scope clarification or interpretation. Record unavailable upset evidence as a limitation.

**How it is decided:** Agree the next review with the operations and alarm-system owners using the site alarm philosophy, operator concerns and unresolved evidence. Existing suitable records can be acknowledged without a new export or compulsory project. The quoted historical rate targets guide investigation; they do not establish alarm quality. Keep partial answers and remaining needs in the company records process or context register.

**What the source says (S23):** HSE: "the long-term average alarm rate during normal operation should be no more than one every ten minutes; and no more than ten displayed in the first ten minutes following a major plant upset."

**Limits:** Drawing tags are candidates, not a complete alarm inventory or proof of operator workload. Scope, coverage and approval fields remain supplied claims; this screen calculates no alarm metrics, matches no records automatically, assigns no ownership and authorizes no operating changes. A quiet screen does not establish alarm absence or adequacy. CHIS6 is introductory guidance dated March 2000, not a replacement standard or universal compliance threshold. Current HSE guidance identifies BS EN 62682 as the benchmark: https://www.hse.gov.uk/eci/functional.htm. Review against the site's applicable requirements.

## Not checked

- C6: the model holds no controllers; give a loop list with --loops to check this

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, H1, H2, H3, H4, C1, C3, C4, C5, C7, C10, C9, E25, E26, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S23: UK HSE, Better Alarm Handling, Chemicals Information Sheet No. 6 (CHIS6, 3/00). https://www.hse.gov.uk/pubns/chis6.pdf (license: Crown copyright; HSE content is generally under the Open Government Licence, but verify)
