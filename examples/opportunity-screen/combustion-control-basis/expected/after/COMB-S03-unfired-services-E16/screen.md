# Opportunity screen: FICTIONAL electric hot-water and unfired waste-heat boiler applicability control

Model: `examples/opportunity-screen/combustion-control-basis/models/COMB-S03-unfired-services.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 2 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Energy

### E16: What heat source and combustion service apply to this unit, and what do existing records establish about any applicable air/fuel operating basis?

**About:** F-A  

**Finding reference (JSON string):** `"E16@F-A"`
**Asset IDs (JSON array):** `["F-A"]`

**Evidence on the drawing / model**

- equipment F-A reads "F-A Electric hot-water boiler A" (`units[F-A]`)
- Supplied candidate field: `"F-A source_document = \"FICT-UNFIRED-SERVICES\"; present; meaning and suitability unverified"` (`"units[F-A].facts.source_document"`)
- Supplied candidate field: `"F-A source_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[F-A].facts.source_revision"`)
- Supplied candidate field: `"F-A underlying_claim_verified = false; present; meaning and suitability unverified"` (`"units[F-A].facts.underlying_claim_verified"`)
- Supplied candidate field: `"F-A water_service = \"hot-water heating only\"; present; meaning and suitability unverified"` (`"units[F-A].facts.water_service"`)
- Supplied candidate field: `"F-A steam_water_drum_present = false; present; meaning and suitability unverified"` (`"units[F-A].facts.steam_water_drum_present"`)
- Supplied candidate field: `"F-A steam_export_present = false; present; meaning and suitability unverified"` (`"units[F-A].facts.steam_export_present"`)
- Supplied candidate field: `"F-A heat_source = \"electric resistance\"; present; meaning and suitability unverified"` (`"units[F-A].facts.heat_source"`)
- Supplied candidate field: `"F-A fuel_fired = false; present; meaning and suitability unverified"` (`"units[F-A].facts.fuel_fired"`)
- On drawing: Supplied candidate fact, basis unverified: F-A heat_source = electric resistance (`units[F-A].facts.heat_source`)
- On drawing: Supplied candidate fact, basis unverified: F-A fuel_fired = False (`units[F-A].facts.fuel_fired`)
- On drawing: Supplied candidate fact, basis unverified: F-A source_document = FICT-UNFIRED-SERVICES (`units[F-A].facts.source_document`)
- On drawing: Supplied candidate fact, basis unverified: F-A source_revision = R1 (`units[F-A].facts.source_revision`)
- On drawing: Supplied candidate fact, basis unverified: F-A underlying_claim_verified = False (`units[F-A].facts.underlying_claim_verified`)

**Data to collect**

- Existing heat-source and combustion-applicability basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): F-A (F-A) heat_source = "electric resistance" [units[F-A].facts.heat_source]; F-A (F-A) fuel_fired = false [units[F-A].facts.fuel_fired]; F-A (F-A) source_document = "FICT-UNFIRED-SERVICES" [units[F-A].facts.source_document]; F-A (F-A) source_revision = "R1" [units[F-A].facts.source_revision]; F-A (F-A) underlying_claim_verified = false [units[F-A].facts.underlying_claim_verified]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: permitted existing equipment/service description, heat-source/fuel and operating records with source/revision, asset scope and responsible owner; establish whether combustion applies before any gas-analysis request. How: A boiler or heater label and a missing fuel stream do not establish either combustion or non-combustion service. Review the existing source basis first. If the supplied scope is electric or unfired with no relevant burner, acknowledge that scope as not applicable to combustion review; do not impose flue/O2/trim work. Unknown heat/fuel service remains a qualification question, not a quiet completed result.
- Applicable existing analysis, metering, control and constraint records [not on drawing]. Where: site records: only where combustion applies: existing tuning, paired air/fuel-flow or flue-analysis records, appropriate calibration/method and representative firing/load basis, current control purpose/configuration/modes and equipment/process constraints; then DCS/PLC configuration: only applicable permitted existing configuration records for the identified unit; this request grants no access, measurement or execution permission. How: For applicable combustion service, use suitable existing air/fuel metering, flue analysis or both; permanent O2 hardware and new portable analysis are not mandatory. Preserve supplied record scope, false and unknown qualifiers. Product/headspace or foreign oxygen is not this unit’s combustion basis; analysis is not enabled feedback trim. Adequate records or documented non-applicability may settle or defer the job without new collection or a project. Do not prescribe operating settings or adjustment.

**How it is decided:** Establish heat source and combustion applicability from qualified existing records before evaluating the operating/control basis. Explicit electric or unfired scope does not create O2/trim work; unknown fuel service is not evidence of non-applicability. Where combustion applies, acknowledge existing analysis/metering and modes, then review unresolved evidence. Adequate coverage may answer or defer the job without a project. This screen neither declares installed control nor tracks completed investigation/work status.

**What the source says (S19, S27, S24):** S19 Section8.1/Table6 reports historical boiler combustion/excess-air measures, not a guaranteed benefit from adding O2 trim. S27 supports reviewing air/fuel-flow or flue-analysis methods and equipment/process constraints. No quantified benefit is assigned to this records-review question.
IAC/ITAC recommendation code: 2.12xx / 2.121x (category only).

**Limits:** This screen covers represented boilers, fired heaters, furnaces and kilns; steam generators and reactors are outside this route’s current scope. Those exclusions do not establish whether combustion review is useful for excluded equipment. Incomplete fuel records remain reviewable; missing fuel context is not proof of non-combustion service. Supplied qualifications/Booleans are not installed-state or company acceptance. S19 reviewed official ENERGY STAR122-page edition, printed37–39/PDFindices44–46, https://www.energystar.gov/sites/default/files/buildings/tools/ES_Petroleum_Energy_Guide.pdf; byte equality with the OSTI route is unverified. S27 supports alternative methods and conditional operating bases. Historical boiler figures and ARC aggregates do not establish all-fired savings or control deficiencies.

### E16: What heat source and combustion service apply to this unit, and what do existing records establish about any applicable air/fuel operating basis?

**About:** F-B  

**Finding reference (JSON string):** `"E16@F-B"`
**Asset IDs (JSON array):** `["F-B"]`

**Evidence on the drawing / model**

- equipment F-B reads "F-B Unfired waste-heat steam-drum boiler B" (`units[F-B]`)
- Supplied candidate field: `"F-B source_document = \"FICT-UNFIRED-SERVICES\"; present; meaning and suitability unverified"` (`"units[F-B].facts.source_document"`)
- Supplied candidate field: `"F-B source_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[F-B].facts.source_revision"`)
- Supplied candidate field: `"F-B underlying_claim_verified = false; present; meaning and suitability unverified"` (`"units[F-B].facts.underlying_claim_verified"`)
- Supplied candidate field: `"F-B water_service = \"steam generation with a steam-water drum\"; present; meaning and suitability unverified"` (`"units[F-B].facts.water_service"`)
- Supplied candidate field: `"F-B steam_water_drum_present = true; present; meaning and suitability unverified"` (`"units[F-B].facts.steam_water_drum_present"`)
- Supplied candidate field: `"F-B steam_export_present = true; present; meaning and suitability unverified"` (`"units[F-B].facts.steam_export_present"`)
- Supplied candidate field: `"F-B heat_source = \"recovered process heat; unfired waste-heat recovery\"; present; meaning and suitability unverified"` (`"units[F-B].facts.heat_source"`)
- Supplied candidate field: `"F-B fuel_fired = false; present; meaning and suitability unverified"` (`"units[F-B].facts.fuel_fired"`)
- Supplied candidate field: `"F-B auxiliary_burner_present = false; present; meaning and suitability unverified"` (`"units[F-B].facts.auxiliary_burner_present"`)
- Supplied candidate field: `"F-B water_level_control_configuration = \"unknown\"; blank; meaning and suitability unverified"` (`"units[F-B].facts.water_level_control_configuration"`)
- On drawing: Supplied candidate fact, basis unverified: F-B heat_source = recovered process heat; unfired waste-heat recovery (`units[F-B].facts.heat_source`)
- On drawing: Supplied candidate fact, basis unverified: F-B fuel_fired = False (`units[F-B].facts.fuel_fired`)
- On drawing: Supplied candidate fact, basis unverified: F-B auxiliary_burner_present = False (`units[F-B].facts.auxiliary_burner_present`)
- On drawing: Supplied candidate fact, basis unverified: F-B source_document = FICT-UNFIRED-SERVICES (`units[F-B].facts.source_document`)
- On drawing: Supplied candidate fact, basis unverified: F-B source_revision = R1 (`units[F-B].facts.source_revision`)
- On drawing: Supplied candidate fact, basis unverified: F-B underlying_claim_verified = False (`units[F-B].facts.underlying_claim_verified`)

**Data to collect**

- Existing heat-source and combustion-applicability basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): F-B (F-B) heat_source = "recovered process heat; unfired waste-heat recovery" [units[F-B].facts.heat_source]; F-B (F-B) fuel_fired = false [units[F-B].facts.fuel_fired]; F-B (F-B) auxiliary_burner_present = false [units[F-B].facts.auxiliary_burner_present]; F-B (F-B) source_document = "FICT-UNFIRED-SERVICES" [units[F-B].facts.source_document]; F-B (F-B) source_revision = "R1" [units[F-B].facts.source_revision]; F-B (F-B) underlying_claim_verified = false [units[F-B].facts.underlying_claim_verified]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: permitted existing equipment/service description, heat-source/fuel and operating records with source/revision, asset scope and responsible owner; establish whether combustion applies before any gas-analysis request. How: A boiler or heater label and a missing fuel stream do not establish either combustion or non-combustion service. Review the existing source basis first. If the supplied scope is electric or unfired with no relevant burner, acknowledge that scope as not applicable to combustion review; do not impose flue/O2/trim work. Unknown heat/fuel service remains a qualification question, not a quiet completed result.
- Applicable existing analysis, metering, control and constraint records [not on drawing]. Where: site records: only where combustion applies: existing tuning, paired air/fuel-flow or flue-analysis records, appropriate calibration/method and representative firing/load basis, current control purpose/configuration/modes and equipment/process constraints; then DCS/PLC configuration: only applicable permitted existing configuration records for the identified unit; this request grants no access, measurement or execution permission. How: For applicable combustion service, use suitable existing air/fuel metering, flue analysis or both; permanent O2 hardware and new portable analysis are not mandatory. Preserve supplied record scope, false and unknown qualifiers. Product/headspace or foreign oxygen is not this unit’s combustion basis; analysis is not enabled feedback trim. Adequate records or documented non-applicability may settle or defer the job without new collection or a project. Do not prescribe operating settings or adjustment.

**How it is decided:** Establish heat source and combustion applicability from qualified existing records before evaluating the operating/control basis. Explicit electric or unfired scope does not create O2/trim work; unknown fuel service is not evidence of non-applicability. Where combustion applies, acknowledge existing analysis/metering and modes, then review unresolved evidence. Adequate coverage may answer or defer the job without a project. This screen neither declares installed control nor tracks completed investigation/work status.

**What the source says (S19, S27, S24):** S19 Section8.1/Table6 reports historical boiler combustion/excess-air measures, not a guaranteed benefit from adding O2 trim. S27 supports reviewing air/fuel-flow or flue-analysis methods and equipment/process constraints. No quantified benefit is assigned to this records-review question.
IAC/ITAC recommendation code: 2.12xx / 2.121x (category only).

**Limits:** This screen covers represented boilers, fired heaters, furnaces and kilns; steam generators and reactors are outside this route’s current scope. Those exclusions do not establish whether combustion review is useful for excluded equipment. Incomplete fuel records remain reviewable; missing fuel context is not proof of non-combustion service. Supplied qualifications/Booleans are not installed-state or company acceptance. S19 reviewed official ENERGY STAR122-page edition, printed37–39/PDFindices44–46, https://www.energystar.gov/sites/default/files/buildings/tools/ES_Petroleum_Energy_Guide.pdf; byte equality with the OSTI route is unverified. S27 supports alternative methods and conditional operating bases. Historical boiler figures and ARC aggregates do not establish all-fired savings or control deficiencies.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
- S27: DOE Industrial Technologies Program, Process Heating Tip Sheet #2, Check Burner Air to Fuel Ratios (Nov 2007). https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/42110.pdf (license: Public domain (US federal))
