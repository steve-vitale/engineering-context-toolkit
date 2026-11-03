# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/source-policy/models/E8-01-pressure-program.json`. Questions: `data/questions.json`.

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

**About:** TR-A, TR-B  

**Finding reference (JSON string):** `"E8@model"`
**Asset IDs (JSON array):** `["TR-A", "TR-B"]`

**Evidence on the drawing / model**

- equipment TR-A reads "TR-A Steam trap smallpopulation" (`units[TR-A]`)
- equipment TR-B reads "TR-B Steam trap largepopulation" (`units[TR-B]`)
- Supplied candidate field: `"TR-A fictional_record = true; present; meaning and suitability unverified"` (`"units[TR-A].facts.fictional_record"`)
- Supplied candidate field: `"TR-A record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[TR-A].facts.record_source"`)
- Supplied candidate field: `"TR-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[TR-A].facts.record_revision"`)
- Supplied candidate field: `"TR-A record_available = true; present; meaning and suitability unverified"` (`"units[TR-A].facts.record_available"`)
- Supplied candidate field: `"TR-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[TR-A].facts.record_authority"`)
- Supplied candidate field: `"TR-A steam_service = true; present; meaning and suitability unverified"` (`"units[TR-A].facts.steam_service"`)
- Supplied candidate field: `"TR-A represented_population = 20; present; meaning and suitability unverified"` (`"units[TR-A].facts.represented_population"`)
- Supplied candidate field: `"TR-A pressure = 200; present; meaning and suitability unverified"` (`"units[TR-A].facts.pressure"`)
- Supplied candidate field: `"TR-A pressure_unit = \"psig\"; present; meaning and suitability unverified"` (`"units[TR-A].facts.pressure_unit"`)
- Supplied candidate field: `"TR-A last_survey = \"fictional lastmonth\"; present; meaning and suitability unverified"` (`"units[TR-A].facts.last_survey"`)
- Supplied candidate field: `"TR-A survey_scope = \"oneunitonly\"; present; meaning and suitability unverified"` (`"units[TR-A].facts.survey_scope"`)
- Supplied candidate field: `"TR-A condition = \"unknown\"; blank; meaning and suitability unverified"` (`"units[TR-A].facts.condition"`)
- Supplied candidate field: `"TR-B fictional_record = true; present; meaning and suitability unverified"` (`"units[TR-B].facts.fictional_record"`)
- Supplied candidate field: `"TR-B record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[TR-B].facts.record_source"`)
- Supplied candidate field: `"TR-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[TR-B].facts.record_revision"`)
- Supplied candidate field: `"TR-B record_available = true; present; meaning and suitability unverified"` (`"units[TR-B].facts.record_available"`)
- Supplied candidate field: `"TR-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[TR-B].facts.record_authority"`)
- Supplied candidate field: `"TR-B steam_service = true; present; meaning and suitability unverified"` (`"units[TR-B].facts.steam_service"`)
- Supplied candidate field: `"TR-B represented_population = 1000; present; meaning and suitability unverified"` (`"units[TR-B].facts.represented_population"`)
- Supplied candidate field: `"TR-B pressure = 15; present; meaning and suitability unverified"` (`"units[TR-B].facts.pressure"`)
- Supplied candidate field: `"TR-B pressure_unit = \"psig\"; present; meaning and suitability unverified"` (`"units[TR-B].facts.pressure_unit"`)
- Supplied candidate field: `"TR-B last_survey = null; blank; meaning and suitability unverified"` (`"units[TR-B].facts.last_survey"`)
- On drawing: Supplied candidate fact, basis unverified: TR-A fictional_record = True (`units[TR-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TR-B fictional_record = True (`units[TR-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TR-A record_source = Fictional development packet; no plant or human approval (`units[TR-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TR-B record_source = Fictional development packet; no plant or human approval (`units[TR-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TR-A record_revision = R1 (`units[TR-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TR-B record_revision = R1 (`units[TR-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TR-A record_available = True (`units[TR-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TR-B record_available = True (`units[TR-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TR-A record_authority = unverified (`units[TR-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TR-B record_authority = unverified (`units[TR-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TR-A steam_service = True (`units[TR-A].facts.steam_service`)
- On drawing: Supplied candidate fact, basis unverified: TR-B steam_service = True (`units[TR-B].facts.steam_service`)
- On drawing: Supplied candidate fact, basis unverified: TR-A represented_population = 20 (`units[TR-A].facts.represented_population`)
- On drawing: Supplied candidate fact, basis unverified: TR-B represented_population = 1000 (`units[TR-B].facts.represented_population`)
- On drawing: Supplied candidate fact, basis unverified: TR-A pressure = 200 (`units[TR-A].facts.pressure`)
- On drawing: Supplied candidate fact, basis unverified: TR-B pressure = 15 (`units[TR-B].facts.pressure`)
- On drawing: Supplied candidate fact, basis unverified: TR-A pressure_unit = psig (`units[TR-A].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: TR-B pressure_unit = psig (`units[TR-B].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: TR-A last_survey = fictional lastmonth (`units[TR-A].facts.last_survey`)
- On drawing: Supplied candidate fact, basis unverified: TR-A survey_scope = oneunitonly (`units[TR-A].facts.survey_scope`)
- On drawing: Supplied candidate fact, basis unverified: TR-A fictional_record = True (`units[TR-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TR-B fictional_record = True (`units[TR-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TR-A record_source = Fictional development packet; no plant or human approval (`units[TR-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TR-B record_source = Fictional development packet; no plant or human approval (`units[TR-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TR-A record_revision = R1 (`units[TR-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TR-B record_revision = R1 (`units[TR-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TR-A record_available = True (`units[TR-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TR-B record_available = True (`units[TR-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TR-A record_authority = unverified (`units[TR-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TR-B record_authority = unverified (`units[TR-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TR-A steam_service = True (`units[TR-A].facts.steam_service`)
- On drawing: Supplied candidate fact, basis unverified: TR-B steam_service = True (`units[TR-B].facts.steam_service`)
- On drawing: Supplied candidate fact, basis unverified: TR-A represented_population = 20 (`units[TR-A].facts.represented_population`)
- On drawing: Supplied candidate fact, basis unverified: TR-B represented_population = 1000 (`units[TR-B].facts.represented_population`)
- On drawing: Supplied candidate fact, basis unverified: TR-A pressure = 200 (`units[TR-A].facts.pressure`)
- On drawing: Supplied candidate fact, basis unverified: TR-B pressure = 15 (`units[TR-B].facts.pressure`)
- On drawing: Supplied candidate fact, basis unverified: TR-A pressure_unit = psig (`units[TR-A].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: TR-B pressure_unit = psig (`units[TR-B].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: TR-A last_survey = fictional lastmonth (`units[TR-A].facts.last_survey`)
- On drawing: Supplied candidate fact, basis unverified: TR-A survey_scope = oneunitonly (`units[TR-A].facts.survey_scope`)

**Data to collect**

- Existing steam-trap identity, service and inventory/program coverage [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TR-A (TR-A) fictional_record = true [units[TR-A].facts.fictional_record]; TR-B (TR-B) fictional_record = true [units[TR-B].facts.fictional_record]; TR-A (TR-A) record_source = "Fictional development packet; no plant or human approval" [units[TR-A].facts.record_source]; TR-B (TR-B) record_source = "Fictional development packet; no plant or human approval" [units[TR-B].facts.record_source]; TR-A (TR-A) record_revision = "R1" [units[TR-A].facts.record_revision]; TR-B (TR-B) record_revision = "R1" [units[TR-B].facts.record_revision]; TR-A (TR-A) record_available = true [units[TR-A].facts.record_available]; TR-B (TR-B) record_available = true [units[TR-B].facts.record_available]; TR-A (TR-A) record_authority = "unverified" [units[TR-A].facts.record_authority]; TR-B (TR-B) record_authority = "unverified" [units[TR-B].facts.record_authority]; TR-A (TR-A) steam_service = true [units[TR-A].facts.steam_service]; TR-B (TR-B) steam_service = true [units[TR-B].facts.steam_service]; TR-A (TR-A) represented_population = 20 [units[TR-A].facts.represented_population]; TR-B (TR-B) represented_population = 1000 [units[TR-B].facts.represented_population]; TR-A (TR-A) pressure = 200 [units[TR-A].facts.pressure]; TR-B (TR-B) pressure = 15 [units[TR-B].facts.pressure]; TR-A (TR-A) pressure_unit = "psig" [units[TR-A].facts.pressure_unit]; TR-B (TR-B) pressure_unit = "psig" [units[TR-B].facts.pressure_unit]; TR-A (TR-A) last_survey = "fictional lastmonth" [units[TR-A].facts.last_survey]; TR-A (TR-A) survey_scope = "oneunitonly" [units[TR-A].facts.survey_scope]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named trap/service inventory, represented versus actual population, pressure ranges, inspection/maintenance dates and coverage; retain each source/revision, availability and authority limits.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Establish steam-trap service before applying steam guidance; known grease/oil/sand/air traps are not steam traps, and ambiguous TRAP/ST labels need conditional service review. The source500-trap and3–5year loss examples are not universal program thresholds or actual population/failure estimates. Its pressure-dependent intervals are source guidance to review in context, not automatic site schedules.
- Existing qualified inspection results and remaining uncertainty [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TR-A (TR-A) fictional_record = true [units[TR-A].facts.fictional_record]; TR-B (TR-B) fictional_record = true [units[TR-B].facts.fictional_record]; TR-A (TR-A) record_source = "Fictional development packet; no plant or human approval" [units[TR-A].facts.record_source]; TR-B (TR-B) record_source = "Fictional development packet; no plant or human approval" [units[TR-B].facts.record_source]; TR-A (TR-A) record_revision = "R1" [units[TR-A].facts.record_revision]; TR-B (TR-B) record_revision = "R1" [units[TR-B].facts.record_revision]; TR-A (TR-A) record_available = true [units[TR-A].facts.record_available]; TR-B (TR-B) record_available = true [units[TR-B].facts.record_available]; TR-A (TR-A) record_authority = "unverified" [units[TR-A].facts.record_authority]; TR-B (TR-B) record_authority = "unverified" [units[TR-B].facts.record_authority]; TR-A (TR-A) steam_service = true [units[TR-A].facts.steam_service]; TR-B (TR-B) steam_service = true [units[TR-B].facts.steam_service]; TR-A (TR-A) represented_population = 20 [units[TR-A].facts.represented_population]; TR-B (TR-B) represented_population = 1000 [units[TR-B].facts.represented_population]; TR-A (TR-A) pressure = 200 [units[TR-A].facts.pressure]; TR-B (TR-B) pressure = 15 [units[TR-B].facts.pressure]; TR-A (TR-A) pressure_unit = "psig" [units[TR-A].facts.pressure_unit]; TR-B (TR-B) pressure_unit = "psig" [units[TR-B].facts.pressure_unit]; TR-A (TR-A) last_survey = "fictional lastmonth" [units[TR-A].facts.last_survey]; TR-A (TR-A) survey_scope = "oneunitonly" [units[TR-A].facts.survey_scope]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing per-trap testing methods, service/pressure and operating conditions, observed condition with uncertainty, repair/retest/report history and unresolved coverage.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Review suitable existing records before any new field survey. Temperature, sound, visual or electronic indications require service/method interpretation and do not turn a symbol into failed-open/closed truth. Preserve unknown or foreign results for each candidate; one survey cannot clear another source/population. A suitable current program may be acknowledged without a new measurement or blanket retrofit.

**How it is decided:** Review the applicable steam-trap service, pressure, importance and existing inspection/repair reporting coverage with the responsible engineer. No universal500-trap or3–5year cutoff establishes whether a program is worthwhile, current, complete or unnecessary, and historical source failure percentages are not this site's condition. Acknowledge suitable existing program or nonapplicability; retain missing identity, method or coverage as a records question rather than a compulsory survey or failure diagnosis.

**What the source says (S3, S19, S24):** Unmaintained 3-5 years: "between 15% to 30% of the installed steam traps may have failed." With a program, "less than 5%." LBNL refinery table (as reported in LBNL-56183): trap maintenance 10-15% fuel saved, 0.5 yr payback.
IAC/ITAC recommendation code: 2.2113 (IAC/ITAC browse page: 445 recommendations, 0.6 yr average payback, 80.1% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S3 pp1–2 includes systematic reporting, testing-method qualification and pressure-dependent suggested intervals. Represented count is not installed population. S19/S24 figures are inherited historical context, not reverified here or transferred to a site.

## Sources cited above

- S3: Steam Tip #1, Inspect and Repair Steam Traps (DOE/GO-102012-3401). https://www.energy.gov/sites/prod/files/2014/05/f16/steam1_traps.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
