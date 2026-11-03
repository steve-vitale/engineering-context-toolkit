# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/source-policy/models/C1-03-existing-fit.json`. Questions: `data/questions.json`.

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
| Metering | 1 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Metering

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** U-A  

**Finding reference (JSON string):** `"C1@U-A"`
**Asset IDs (JSON array):** `["U-A", "stream:S-A", "FT-A"]`

**Evidence on the drawing / model**

- stream S-A (asset stream:S-A) reads "STEAM SUPPLY" at U-A (`streams[S-A]`)
- Unverified flow/quantity candidate; utility/user coverage and usable data not established: instrument FT-A reads "FT-A STEAM flow candidate" at U-A (`instruments[FT-A]`)
- Equipment: equipment U-A reads "U-A Fictional utility user" (`units[U-A]`)
- Supplied candidate field: `"S-A fictional_record = true; present; meaning and suitability unverified"` (`"streams[S-A].facts.fictional_record"`)
- Supplied candidate field: `"S-A record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"streams[S-A].facts.record_source"`)
- Supplied candidate field: `"S-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"streams[S-A].facts.record_revision"`)
- Supplied candidate field: `"S-A record_available = true; present; meaning and suitability unverified"` (`"streams[S-A].facts.record_available"`)
- Supplied candidate field: `"S-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"streams[S-A].facts.record_authority"`)
- Supplied candidate field: `"S-A utility_quantity = \"massflow\"; present; meaning and suitability unverified"` (`"streams[S-A].facts.utility_quantity"`)
- Supplied candidate field: `"FT-A fictional_record = true; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.fictional_record"`)
- Supplied candidate field: `"FT-A record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_source"`)
- Supplied candidate field: `"FT-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_revision"`)
- Supplied candidate field: `"FT-A record_available = true; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_available"`)
- Supplied candidate field: `"FT-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_authority"`)
- Supplied candidate field: `"FT-A record_scope = \"localstreamdeclared\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_scope"`)
- Supplied candidate field: `"FT-A flow = 7; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.flow"`)
- Supplied candidate field: `"FT-A flow_unit = \"kg/h\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.flow_unit"`)
- Supplied candidate field: `"FT-A measurement_target = \"S-Adeclared\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.measurement_target"`)
- Supplied candidate field: `"FT-A quantity = \"compensatedmassflow\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.quantity"`)
- Supplied candidate field: `"FT-A sample_period = \"fictionalrepresentativeinterval\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.sample_period"`)
- Supplied candidate field: `"FT-A quality = \"declaredgoodunverified\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.quality"`)
- Supplied candidate field: `"FT-A calibration_basis = \"suppliedcurrentrecord, notaccepted\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.calibration_basis"`)
- Supplied candidate field: `"FT-A meter_range = \"1-10kg/h\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.meter_range"`)
- Supplied candidate field: `"FT-A installation_basis = \"suppliednotverified\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.installation_basis"`)
- Supplied candidate field: `"FT-A data_gaps = []; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.data_gaps"`)
- Supplied candidate field: `"FT-A report_use = \"suppliedweeklyproductionreport\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.report_use"`)
- Supplied candidate field: `"U-A fictional_record = true; present; meaning and suitability unverified"` (`"units[U-A].facts.fictional_record"`)
- Supplied candidate field: `"U-A record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[U-A].facts.record_source"`)
- Supplied candidate field: `"U-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[U-A].facts.record_revision"`)
- Supplied candidate field: `"U-A record_available = true; present; meaning and suitability unverified"` (`"units[U-A].facts.record_available"`)
- Supplied candidate field: `"U-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[U-A].facts.record_authority"`)
- Supplied candidate field: `"U-A metering_purpose = \"suppliedweeklyproductionreport\"; present; meaning and suitability unverified"` (`"units[U-A].facts.metering_purpose"`)
- Supplied candidate field: `"U-A data_owner = \"fictionalenergyreviewer\"; present; meaning and suitability unverified"` (`"units[U-A].facts.data_owner"`)
- On drawing: Supplied candidate fact, basis unverified: S-A fictional_record = True (`streams[S-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_source = Fictional pre-call development record, no company or human approval (`streams[S-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_revision = R1 (`streams[S-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_available = True (`streams[S-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_authority = unverified (`streams[S-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: S-A utility_quantity = massflow (`streams[S-A].facts.utility_quantity`)
- On drawing: Supplied candidate fact, basis unverified: S-A fictional_record = True (`streams[S-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_source = Fictional pre-call development record, no company or human approval (`streams[S-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_revision = R1 (`streams[S-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_available = True (`streams[S-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_authority = unverified (`streams[S-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: S-A utility_quantity = massflow (`streams[S-A].facts.utility_quantity`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): S-A (stream:S-A) fictional_record = true [streams[S-A].facts.fictional_record]; S-A (stream:S-A) record_source = "Fictional pre-call development record, no company or human approval" [streams[S-A].facts.record_source]; S-A (stream:S-A) record_revision = "R1" [streams[S-A].facts.record_revision]; S-A (stream:S-A) record_available = true [streams[S-A].facts.record_available]; S-A (stream:S-A) record_authority = "unverified" [streams[S-A].facts.record_authority]; S-A (stream:S-A) utility_quantity = "massflow" [streams[S-A].facts.utility_quantity]. The collection/review request remains open; supplied values or document references do not settle it. Where: historian or DCS trend for FT-A (no historian tag is mapped in this model for these); then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): S-A (stream:S-A) fictional_record = true [streams[S-A].facts.fictional_record]; S-A (stream:S-A) record_source = "Fictional pre-call development record, no company or human approval" [streams[S-A].facts.record_source]; S-A (stream:S-A) record_revision = "R1" [streams[S-A].facts.record_revision]; S-A (stream:S-A) record_available = true [streams[S-A].facts.record_available]; S-A (stream:S-A) record_authority = "unverified" [streams[S-A].facts.record_authority]; S-A (stream:S-A) utility_quantity = "massflow" [streams[S-A].facts.utility_quantity]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S22: FEMP Metering Best Practices: A Guide to Achieving Utility Resource Efficiency, Release 3.0 (PNNL-23892, Mar 2015). https://www.wbdg.org/FFC/DOE/NLCRIT/mbpg_2015.pdf (license: Contractor-prepared federal guide: unclear. Its savings figures are buildings-focused)
