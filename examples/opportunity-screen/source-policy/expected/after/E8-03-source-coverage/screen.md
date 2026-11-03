# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/source-policy/models/E8-03-source-coverage.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
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
| Safety questions to verify | 0 |

## Energy

### E8: What do existing records establish about the represented trap candidates' steam service, inventory coverage and current inspection program?

**About:** ST-A, ST-B  

**Finding reference (JSON string):** `"E8@model"`
**Asset IDs (JSON array):** `["ST-A", "ST-B"]`

**Evidence on the drawing / model**

- equipment ST-A reads "ST-A Steam trap sourceA" (`units[ST-A]`)
- equipment ST-B reads "ST-B Steam trap sourceB" (`units[ST-B]`)
- Supplied candidate field: `"ST-A fictional_record = true; present; meaning and suitability unverified"` (`"units[ST-A].facts.fictional_record"`)
- Supplied candidate field: `"ST-A record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_source"`)
- Supplied candidate field: `"ST-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_revision"`)
- Supplied candidate field: `"ST-A record_available = false; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_available"`)
- Supplied candidate field: `"ST-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_authority"`)
- Supplied candidate field: `"ST-A record_scope = \"foreignsiteST-A\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.record_scope"`)
- Supplied candidate field: `"ST-A steam_service = true; present; meaning and suitability unverified"` (`"units[ST-A].facts.steam_service"`)
- Supplied candidate field: `"ST-A survey_method = \"oldvisualrecord\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.survey_method"`)
- Supplied candidate field: `"ST-A survey_status = \"reportedworking, notlocalverified\"; present; meaning and suitability unverified"` (`"units[ST-A].facts.survey_status"`)
- Supplied candidate field: `"ST-B fictional_record = true; present; meaning and suitability unverified"` (`"units[ST-B].facts.fictional_record"`)
- Supplied candidate field: `"ST-B record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_source"`)
- Supplied candidate field: `"ST-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_revision"`)
- Supplied candidate field: `"ST-B record_available = true; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_available"`)
- Supplied candidate field: `"ST-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_authority"`)
- Supplied candidate field: `"ST-B record_scope = \"localST-B fictionalperiod\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.record_scope"`)
- Supplied candidate field: `"ST-B steam_service = true; present; meaning and suitability unverified"` (`"units[ST-B].facts.steam_service"`)
- Supplied candidate field: `"ST-B survey_method = \"qualifiedmethod/source unknown\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.survey_method"`)
- Supplied candidate field: `"ST-B survey_status = \"suppliedprogram currentandcomplete\"; present; meaning and suitability unverified"` (`"units[ST-B].facts.survey_status"`)
- On drawing: Supplied candidate fact, basis unverified: ST-A fictional_record = True (`units[ST-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: ST-B fictional_record = True (`units[ST-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_source = Fictional development packet; no plant or human approval (`units[ST-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_source = Fictional development packet; no plant or human approval (`units[ST-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_revision = R1 (`units[ST-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_revision = R1 (`units[ST-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_available = False (`units[ST-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_available = True (`units[ST-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_authority = unverified (`units[ST-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_authority = unverified (`units[ST-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_scope = foreignsiteST-A (`units[ST-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_scope = localST-B fictionalperiod (`units[ST-B].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: ST-A steam_service = True (`units[ST-A].facts.steam_service`)
- On drawing: Supplied candidate fact, basis unverified: ST-B steam_service = True (`units[ST-B].facts.steam_service`)
- On drawing: Supplied candidate fact, basis unverified: ST-A survey_method = oldvisualrecord (`units[ST-A].facts.survey_method`)
- On drawing: Supplied candidate fact, basis unverified: ST-B survey_method = qualifiedmethod/source unknown (`units[ST-B].facts.survey_method`)
- On drawing: Supplied candidate fact, basis unverified: ST-A survey_status = reportedworking, notlocalverified (`units[ST-A].facts.survey_status`)
- On drawing: Supplied candidate fact, basis unverified: ST-B survey_status = suppliedprogram currentandcomplete (`units[ST-B].facts.survey_status`)
- On drawing: Supplied candidate fact, basis unverified: ST-A fictional_record = True (`units[ST-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: ST-B fictional_record = True (`units[ST-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_source = Fictional development packet; no plant or human approval (`units[ST-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_source = Fictional development packet; no plant or human approval (`units[ST-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_revision = R1 (`units[ST-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_revision = R1 (`units[ST-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_available = False (`units[ST-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_available = True (`units[ST-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_authority = unverified (`units[ST-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_authority = unverified (`units[ST-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: ST-A record_scope = foreignsiteST-A (`units[ST-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: ST-B record_scope = localST-B fictionalperiod (`units[ST-B].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: ST-A steam_service = True (`units[ST-A].facts.steam_service`)
- On drawing: Supplied candidate fact, basis unverified: ST-B steam_service = True (`units[ST-B].facts.steam_service`)
- On drawing: Supplied candidate fact, basis unverified: ST-A survey_method = oldvisualrecord (`units[ST-A].facts.survey_method`)
- On drawing: Supplied candidate fact, basis unverified: ST-B survey_method = qualifiedmethod/source unknown (`units[ST-B].facts.survey_method`)
- On drawing: Supplied candidate fact, basis unverified: ST-A survey_status = reportedworking, notlocalverified (`units[ST-A].facts.survey_status`)
- On drawing: Supplied candidate fact, basis unverified: ST-B survey_status = suppliedprogram currentandcomplete (`units[ST-B].facts.survey_status`)

**Data to collect**

- Existing steam-trap identity, service and inventory/program coverage [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): ST-A (ST-A) fictional_record = true [units[ST-A].facts.fictional_record]; ST-B (ST-B) fictional_record = true [units[ST-B].facts.fictional_record]; ST-A (ST-A) record_source = "Fictional development packet; no plant or human approval" [units[ST-A].facts.record_source]; ST-B (ST-B) record_source = "Fictional development packet; no plant or human approval" [units[ST-B].facts.record_source]; ST-A (ST-A) record_revision = "R1" [units[ST-A].facts.record_revision]; ST-B (ST-B) record_revision = "R1" [units[ST-B].facts.record_revision]; ST-A (ST-A) record_available = false [units[ST-A].facts.record_available]; ST-B (ST-B) record_available = true [units[ST-B].facts.record_available]; ST-A (ST-A) record_authority = "unverified" [units[ST-A].facts.record_authority]; ST-B (ST-B) record_authority = "unverified" [units[ST-B].facts.record_authority]; ST-A (ST-A) record_scope = "foreignsiteST-A" [units[ST-A].facts.record_scope]; ST-B (ST-B) record_scope = "localST-B fictionalperiod" [units[ST-B].facts.record_scope]; ST-A (ST-A) steam_service = true [units[ST-A].facts.steam_service]; ST-B (ST-B) steam_service = true [units[ST-B].facts.steam_service]; ST-A (ST-A) survey_method = "oldvisualrecord" [units[ST-A].facts.survey_method]; ST-B (ST-B) survey_method = "qualifiedmethod/source unknown" [units[ST-B].facts.survey_method]; ST-A (ST-A) survey_status = "reportedworking, notlocalverified" [units[ST-A].facts.survey_status]; ST-B (ST-B) survey_status = "suppliedprogram currentandcomplete" [units[ST-B].facts.survey_status]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named trap/service inventory, represented versus actual population, pressure ranges, inspection/maintenance dates and coverage; retain each source/revision, availability and authority limits.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Establish steam-trap service before applying steam guidance; known grease/oil/sand/air traps are not steam traps, and ambiguous TRAP/ST labels need conditional service review. The source500-trap and3–5year loss examples are not universal program thresholds or actual population/failure estimates. Its pressure-dependent intervals are source guidance to review in context, not automatic site schedules.
- Existing qualified inspection results and remaining uncertainty [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): ST-A (ST-A) fictional_record = true [units[ST-A].facts.fictional_record]; ST-B (ST-B) fictional_record = true [units[ST-B].facts.fictional_record]; ST-A (ST-A) record_source = "Fictional development packet; no plant or human approval" [units[ST-A].facts.record_source]; ST-B (ST-B) record_source = "Fictional development packet; no plant or human approval" [units[ST-B].facts.record_source]; ST-A (ST-A) record_revision = "R1" [units[ST-A].facts.record_revision]; ST-B (ST-B) record_revision = "R1" [units[ST-B].facts.record_revision]; ST-A (ST-A) record_available = false [units[ST-A].facts.record_available]; ST-B (ST-B) record_available = true [units[ST-B].facts.record_available]; ST-A (ST-A) record_authority = "unverified" [units[ST-A].facts.record_authority]; ST-B (ST-B) record_authority = "unverified" [units[ST-B].facts.record_authority]; ST-A (ST-A) record_scope = "foreignsiteST-A" [units[ST-A].facts.record_scope]; ST-B (ST-B) record_scope = "localST-B fictionalperiod" [units[ST-B].facts.record_scope]; ST-A (ST-A) steam_service = true [units[ST-A].facts.steam_service]; ST-B (ST-B) steam_service = true [units[ST-B].facts.steam_service]; ST-A (ST-A) survey_method = "oldvisualrecord" [units[ST-A].facts.survey_method]; ST-B (ST-B) survey_method = "qualifiedmethod/source unknown" [units[ST-B].facts.survey_method]; ST-A (ST-A) survey_status = "reportedworking, notlocalverified" [units[ST-A].facts.survey_status]; ST-B (ST-B) survey_status = "suppliedprogram currentandcomplete" [units[ST-B].facts.survey_status]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing per-trap testing methods, service/pressure and operating conditions, observed condition with uncertainty, repair/retest/report history and unresolved coverage.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Review suitable existing records before any new field survey. Temperature, sound, visual or electronic indications require service/method interpretation and do not turn a symbol into failed-open/closed truth. Preserve unknown or foreign results for each candidate; one survey cannot clear another source/population. A suitable current program may be acknowledged without a new measurement or blanket retrofit.

**How it is decided:** Review the applicable steam-trap service, pressure, importance and existing inspection/repair reporting coverage with the responsible engineer. No universal500-trap or3–5year cutoff establishes whether a program is worthwhile, current, complete or unnecessary, and historical source failure percentages are not this site's condition. Acknowledge suitable existing program or nonapplicability; retain missing identity, method or coverage as a records question rather than a compulsory survey or failure diagnosis.

**What the source says (S3, S19, S24):** Unmaintained 3-5 years: "between 15% to 30% of the installed steam traps may have failed." With a program, "less than 5%." LBNL refinery table (as reported in LBNL-56183): trap maintenance 10-15% fuel saved, 0.5 yr payback.
IAC/ITAC recommendation code: 2.2113 (IAC/ITAC browse page: 445 recommendations, 0.6 yr average payback, 80.1% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S3 pp1–2 includes systematic reporting, testing-method qualification and pressure-dependent suggested intervals. Represented count is not installed population. S19/S24 figures are inherited historical context, not reverified here or transferred to a site.

## Sources cited above

- S3: Steam Tip #1, Inspect and Repair Steam Traps (DOE/GO-102012-3401). https://www.energy.gov/sites/prod/files/2014/05/f16/steam1_traps.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
