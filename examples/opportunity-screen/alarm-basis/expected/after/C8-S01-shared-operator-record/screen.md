# Opportunity screen: C8-S01-shared-operator-record

Model: `examples/opportunity-screen/alarm-basis/models/C8-S01-shared-operator-record.json`. Questions: `data/questions.json`.

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
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 1 |

## Safety questions to verify

### C8: What do existing records show about alarm workload and response for each responsible operator scope?

**About:** PAH-101, LAHH-201  

**Finding reference (JSON string):** `"C8@model"`
**Asset IDs (JSON array):** `["PAH-101", "LAHH-201"]`

**Evidence on the drawing / model**

- instrument PAH-101 reads "PAH-101 Fictional alarm candidate, not installed configuration" at U-A (`instruments[PAH-101]`)
- instrument LAHH-201 reads "LAHH-201 Fictional alarm candidate, not installed configuration" at U-B (`instruments[LAHH-201]`)
- Supplied candidate field: `"PAH-101 record_reference = \"fictional:shared-workload-report-A\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_reference"`)
- Supplied candidate field: `"PAH-101 record_revision = \"r1\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_revision"`)
- Supplied candidate field: `"PAH-101 operator_role = \"console-operator\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.operator_role"`)
- Supplied candidate field: `"PAH-101 console_id = \"CON-1\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.console_id"`)
- Supplied candidate field: `"PAH-101 underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.underlying_claim_verified"`)
- Supplied candidate field: `"PAH-101 record_console_id = \"CON-1\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_console_id"`)
- Supplied candidate field: `"PAH-101 site_namespace = \"fictional-site-A\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.site_namespace"`)
- Supplied candidate field: `"PAH-101 source_namespace = \"fictional-source-A\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.source_namespace"`)
- Supplied candidate field: `"PAH-101 workload_scope = \"fictional-site-A/CON-1/console-operator\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.workload_scope"`)
- Supplied candidate field: `"PAH-101 plant_truth = \"unknown\"; blank; meaning and suitability unverified"` (`"instruments[PAH-101].facts.plant_truth"`)
- Supplied candidate field: `"PAH-101 record_site_namespace = \"fictional-site-A\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_site_namespace"`)
- Supplied candidate field: `"PAH-101 record_source_namespace = \"fictional-source-A\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_source_namespace"`)
- Supplied candidate field: `"PAH-101 record_operator_role = \"console-operator\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_operator_role"`)
- Supplied candidate field: `"PAH-101 record_subjects = [\"PAH-101\", \"LAHH-201\"]; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_subjects"`)
- Supplied candidate field: `"PAH-101 record_units = [\"U-A\", \"U-B\"]; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_units"`)
- Supplied candidate field: `"PAH-101 record_workload_scope = \"fictional-site-A/CON-1/console-operator\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_workload_scope"`)
- Supplied candidate field: `"PAH-101 record_coverage = \"one record claims the complete shared responsibility across both units\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_coverage"`)
- Supplied candidate field: `"PAH-101 record_review_status = \"AUTHOR-ILLUSTRATED approved for this scoped review; not actual company approval\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_review_status"`)
- Supplied candidate field: `"PAH-101 record_review_basis = \"Fictional operations and alarm-owner review says this record covers both named units and subjects; suitability and source authority remain supplied claims\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_review_basis"`)
- Supplied candidate field: `"PAH-101 record_period_basis = \"declared normal and upset record periods, identities to be reviewed; no fixed duration or computed metric\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_period_basis"`)
- Supplied candidate field: `"PAH-101 record_owner = \"fictional operations-console owner A\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.record_owner"`)
- Supplied candidate field: `"PAH-101 next_recipient = \"fictional operations-console owner A with alarm-system owner\"; present; meaning and suitability unverified"` (`"instruments[PAH-101].facts.next_recipient"`)
- Supplied candidate field: `"LAHH-201 record_reference = \"fictional:shared-workload-report-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_reference"`)
- Supplied candidate field: `"LAHH-201 record_revision = \"r1\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_revision"`)
- Supplied candidate field: `"LAHH-201 operator_role = \"console-operator\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.operator_role"`)
- Supplied candidate field: `"LAHH-201 console_id = \"CON-1\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.console_id"`)
- Supplied candidate field: `"LAHH-201 underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.underlying_claim_verified"`)
- Supplied candidate field: `"LAHH-201 record_console_id = \"CON-1\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_console_id"`)
- Supplied candidate field: `"LAHH-201 site_namespace = \"fictional-site-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.site_namespace"`)
- Supplied candidate field: `"LAHH-201 source_namespace = \"fictional-source-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.source_namespace"`)
- Supplied candidate field: `"LAHH-201 workload_scope = \"fictional-site-A/CON-1/console-operator\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.workload_scope"`)
- Supplied candidate field: `"LAHH-201 plant_truth = \"unknown\"; blank; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.plant_truth"`)
- Supplied candidate field: `"LAHH-201 record_site_namespace = \"fictional-site-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_site_namespace"`)
- Supplied candidate field: `"LAHH-201 record_source_namespace = \"fictional-source-A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_source_namespace"`)
- Supplied candidate field: `"LAHH-201 record_operator_role = \"console-operator\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_operator_role"`)
- Supplied candidate field: `"LAHH-201 record_subjects = [\"PAH-101\", \"LAHH-201\"]; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_subjects"`)
- Supplied candidate field: `"LAHH-201 record_units = [\"U-A\", \"U-B\"]; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_units"`)
- Supplied candidate field: `"LAHH-201 record_workload_scope = \"fictional-site-A/CON-1/console-operator\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_workload_scope"`)
- Supplied candidate field: `"LAHH-201 record_coverage = \"one record claims the complete shared responsibility across both units\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_coverage"`)
- Supplied candidate field: `"LAHH-201 record_review_status = \"AUTHOR-ILLUSTRATED approved for this scoped review; not actual company approval\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_review_status"`)
- Supplied candidate field: `"LAHH-201 record_review_basis = \"Fictional operations and alarm-owner review says this record covers both named units and subjects; suitability and source authority remain supplied claims\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_review_basis"`)
- Supplied candidate field: `"LAHH-201 record_period_basis = \"declared normal and upset record periods, identities to be reviewed; no fixed duration or computed metric\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_period_basis"`)
- Supplied candidate field: `"LAHH-201 record_owner = \"fictional operations-console owner A\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.record_owner"`)
- Supplied candidate field: `"LAHH-201 next_recipient = \"fictional operations-console owner A with alarm-system owner\"; present; meaning and suitability unverified"` (`"instruments[LAHH-201].facts.next_recipient"`)

**Data to collect**

- Alarm rate, floods and standing alarms [not on drawing]. Where: site records: existing alarm philosophy/register, defined-response procedures and scoped alarm journal or performance-review records; then site records: the responsible operations/console owner and alarm-system owner; existing operator feedback and record-scope review. How: Start with existing approved records. Confirm each record's operator responsibility, console/area, site/source, revision and operating periods. Distinguish presented alarms from status events, acknowledgements and returns to normal; retain journal filters, time basis and gaps. Review representative normal and available upset periods separately, including standing count/duration, nuisance patterns, required responses and operator feedback. Reuse a record when its reviewed scope covers several alarms or units; matching labels alone do not establish coverage. Acknowledge available evidence and ask only for missing records, scope clarification or interpretation. Record unavailable upset evidence as a limitation.

**How it is decided:** Agree the next review with the operations and alarm-system owners using the site alarm philosophy, operator concerns and unresolved evidence. Existing suitable records can be acknowledged without a new export or compulsory project. The quoted historical rate targets guide investigation; they do not establish alarm quality. Keep partial answers and remaining needs in the company records process or context register.

**What the source says (S23):** HSE: "the long-term average alarm rate during normal operation should be no more than one every ten minutes; and no more than ten displayed in the first ten minutes following a major plant upset."

**Limits:** Drawing tags are candidates, not a complete alarm inventory or proof of operator workload. Scope, coverage and approval fields remain supplied claims; this screen calculates no alarm metrics, matches no records automatically, assigns no ownership and authorizes no operating changes. A quiet screen does not establish alarm absence or adequacy. CHIS6 is introductory guidance dated March 2000, not a replacement standard or universal compliance threshold. Current HSE guidance identifies BS EN 62682 as the benchmark: https://www.hse.gov.uk/eci/functional.htm. Review against the site's applicable requirements.

## Not checked

- C2: the model holds no controllers; give a loop list with --loops (controller,measurement,output) to check this
- C6: the model holds no controllers; give a loop list with --loops to check this

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, H1, H2, H3, H4, C1, C3, C4, C5, C7, C10, C9, E25, E26, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S23: UK HSE, Better Alarm Handling, Chemicals Information Sheet No. 6 (CHIS6, 3/00). https://www.hse.gov.uk/pubns/chis6.pdf (license: Crown copyright; HSE content is generally under the Open Government Licence, but verify)
