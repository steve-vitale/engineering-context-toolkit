# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/source-policy/models/C10-03-program.json`. Questions: `data/questions.json`.

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

### C10: What do existing records establish about these trap candidates' actual steam service, importance and maintenance/monitoring coverage?

**About:** ST-A, ST-B  

**Finding reference (JSON string):** `"C10@model"`
**Asset IDs (JSON array):** `["ST-A", "ST-B"]`

**Evidence on the drawing / model**

- equipment ST-A reads "ST-A STEAM TRAP" (`units[ST-A]`)
- equipment ST-B reads "ST-B STEAM TRAP" (`units[ST-B]`)
- Supplied candidate field: `"ST-A fictional_record = true; present; meaning and suitability unverified"` (`"units[ST-A].facts.fictional_record"`)
- Supplied candidate field: `"ST-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_source"`)
- Supplied candidate field: `"ST-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_revision"`)
- Supplied candidate field: `"ST-A record_available = true; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_available"`)
- Supplied candidate field: `"ST-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_authority"`)
- Supplied candidate field: `"ST-A service = \"steam\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.service"`)
- Supplied candidate field: `"ST-A criticality = \"declaredhigh\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.criticality"`)
- Supplied candidate field: `"ST-A failure_consequence = \"processavailability\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.failure_consequence"`)
- Supplied candidate field: `"ST-A existing_program = \"suppliedinspectionrepairverification\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.existing_program"`)
- Supplied candidate field: `"ST-A inspection_method = \"ultrasound+temperature\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.inspection_method"`)
- Supplied candidate field: `"ST-A last_result = \"unverifiedgood\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.last_result"`)
- Supplied candidate field: `"ST-A response_owner = \"fictionalmaintainer\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.response_owner"`)
- Supplied candidate field: `"ST-B fictional_record = true; present; meaning and suitability unverified"` (`"units[ST-B].facts.fictional_record"`)
- Supplied candidate field: `"ST-B record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_source"`)
- Supplied candidate field: `"ST-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_revision"`)
- Supplied candidate field: `"ST-B record_available = true; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_available"`)
- Supplied candidate field: `"ST-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_authority"`)
- Supplied candidate field: `"ST-B service = \"steam\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.service"`)
- Supplied candidate field: `"ST-B criticality = \"declaredlow\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.criticality"`)
- Supplied candidate field: `"ST-B existing_program = \"suppliedperiodicsurvey\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.existing_program"`)
- Supplied candidate field: `"ST-B last_result = null; blank; meaning and suitability unverified"` (`"units[ST-B].facts.last_result"`)
- On drawing: Supplied candidate fact, basis unverified: ST-A fictional_record = True (`units[ST-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: ST-B fictional_record = True (`units[ST-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_source = Fictional pre-call record, no company or human approval (`units[ST-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_source = Fictional pre-call record, no company or human approval (`units[ST-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_revision = R1 (`units[ST-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_revision = R1 (`units[ST-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_available = True (`units[ST-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_available = True (`units[ST-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_authority = unverified (`units[ST-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_authority = unverified (`units[ST-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: ST-A service = steam (`units[ST-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: ST-B service = steam (`units[ST-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: ST-A criticality = declaredhigh (`units[ST-A].facts.criticality`)
- On drawing: Supplied candidate fact, basis unverified: ST-B criticality = declaredlow (`units[ST-B].facts.criticality`)
- On drawing: Supplied candidate fact, basis unverified: ST-A failure_consequence = processavailability (`units[ST-A].facts.failure_consequence`)
- On drawing: Supplied candidate fact, basis unverified: ST-A existing_program = suppliedinspectionrepairverification (`units[ST-A].facts.existing_program`)
- On drawing: Supplied candidate fact, basis unverified: ST-B existing_program = suppliedperiodicsurvey (`units[ST-B].facts.existing_program`)
- On drawing: Supplied candidate fact, basis unverified: ST-A inspection_method = ultrasound+temperature (`units[ST-A].facts.inspection_method`)
- On drawing: Supplied candidate fact, basis unverified: ST-A last_result = unverifiedgood (`units[ST-A].facts.last_result`)
- On drawing: Supplied candidate fact, basis unverified: ST-A response_owner = fictionalmaintainer (`units[ST-A].facts.response_owner`)

**Data to collect**

- Which traps are critical [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): ST-A (ST-A) fictional_record = true [units[ST-A].facts.fictional_record]; ST-B (ST-B) fictional_record = true [units[ST-B].facts.fictional_record]; ST-A (ST-A) record_source = "Fictional pre-call record, no company or human approval" [units[ST-A].facts.record_source]; ST-B (ST-B) record_source = "Fictional pre-call record, no company or human approval" [units[ST-B].facts.record_source]; ST-A (ST-A) record_revision = "R1" [units[ST-A].facts.record_revision]; ST-B (ST-B) record_revision = "R1" [units[ST-B].facts.record_revision]; ST-A (ST-A) record_available = true [units[ST-A].facts.record_available]; ST-B (ST-B) record_available = true [units[ST-B].facts.record_available]; ST-A (ST-A) record_authority = "unverified" [units[ST-A].facts.record_authority]; ST-B (ST-B) record_authority = "unverified" [units[ST-B].facts.record_authority]; ST-A (ST-A) service = "steam" [units[ST-A].facts.service]; ST-B (ST-B) service = "steam" [units[ST-B].facts.service]; ST-A (ST-A) criticality = "declaredhigh" [units[ST-A].facts.criticality]; ST-B (ST-B) criticality = "declaredlow" [units[ST-B].facts.criticality]; ST-A (ST-A) failure_consequence = "processavailability" [units[ST-A].facts.failure_consequence]; ST-A (ST-A) existing_program = "suppliedinspectionrepairverification" [units[ST-A].facts.existing_program]; ST-B (ST-B) existing_program = "suppliedperiodicsurvey" [units[ST-B].facts.existing_program]; ST-A (ST-A) inspection_method = "ultrasound+temperature" [units[ST-A].facts.inspection_method]; ST-A (ST-A) last_result = "unverifiedgood" [units[ST-A].facts.last_result]; ST-A (ST-A) response_owner = "fictionalmaintainer" [units[ST-A].facts.response_owner]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact trap/service/function and criticality/failure consequence, source/current list and associations, current inspection/test/monitor/report/repair/verification program, method/interval/result and responsible response coverage.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A TRAP name is not established steam service or failure, and generic UT or another trap's monitor does not settle this record. S3 completepp1-2 calls for systematic inspection/testing/repair and considers online monitoring for important traps/processes; it describes different methods and contextual intervals, not a universal mandate. S19 printed40-42 presents automatic monitoring in conjunction with regular maintenance. Review suitable existing program and consequences first, acknowledging effective records or nonapplicability without obligatory new online hardware or survey. Foreign/old/unavailable and blank records remain explicit.

**How it is decided:** Review actual steam-trap service, importance, existing maintenance/inspection/monitor and response/verification coverage with the responsible specialist. Neither a global monitor label nor a criticality name establishes coverage, failure or a need for online monitoring. Suitable existing strategy or nonapplicability can be acknowledged; unresolved records remain a question, not an inspection/repair instruction or transferred source benefit.

**What the source says (S19, S3, S24):** LBNL (as reported in LBNL-56183): "Automatic Steam Trap Monitoring 5%", 1 yr. DOE tip sheet: "Consider online monitoring of the most important steam traps".
IAC/ITAC recommendation code: 2.211x (category only).

**Limits:** Source review: complete S3 SteamTip1 pp1-2 and S19 originalLBNL printed40-42/PDF48-50. Historical additional5% estimate is relative to regular maintenance and based on secondary reports, with contextual payback assumptions; it is not installed failure or a site benefit. UT may be an unrelated ultrasonic measurement; type/source/purpose/coverage must be reviewed. No generic-analyzer suppression or current monitoring authority is inferred.

## Sources cited above

- S3: Steam Tip #1, Inspect and Repair Steam Traps (DOE/GO-102012-3401). https://www.energy.gov/sites/prod/files/2014/05/f16/steam1_traps.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
