# Opportunity screen: FICTIONAL paired combustion/control collection development fixture

Model: `examples/opportunity-screen/combustion-control-basis/models/COMB-05-air-fuel-metering-record.json`. Questions: `data/questions.json`.

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
| Controls and automation | 2 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Controls and automation

### C5: What boiler service and control functions apply, and what do existing records establish about any applicable steam-water level-control basis?

**About:** F-A  

**Finding reference (JSON string):** `"C5@F-A"`
**Asset IDs (JSON array):** `["F-A", "FT-FUEL-A", "FT-AIR-A", "stream:FUEL-A", "stream:FLUE-A", "stream:AIR-A"]`

**Evidence on the drawing / model**

- equipment F-A reads "F-A Fired unit A" (`units[F-A]`)
- Represented air or fuel metering record candidate: instrument FT-FUEL-A reads "FT-FUEL-A Fuel-flow indication for fired unit A" at F-A (`instruments[FT-FUEL-A]`)
- Represented air or fuel metering record candidate: instrument FT-AIR-A reads "FT-AIR-A Combustion-air-flow indication for fired unit A" at F-A (`instruments[FT-AIR-A]`)
- Represented fuel, air or flue stream context: stream FUEL-A (asset stream:FUEL-A) reads "Natural gas fuel A" at F-A (`streams[FUEL-A]`)
- Represented fuel, air or flue stream context: stream FLUE-A (asset stream:FLUE-A) reads "Flue gas A" (`streams[FLUE-A]`)
- Represented fuel, air or flue stream context: stream AIR-A (asset stream:AIR-A) reads "Combustion air A" (`streams[AIR-A]`)
- Supplied candidate field: `"F-A fuel_service = \"natural gas\"; present; meaning and suitability unverified"` (`"units[F-A].facts.fuel_service"`)
- Supplied candidate field: `"F-A operating_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"units[F-A].facts.operating_basis"`)
- Supplied candidate field: `"FT-FUEL-A source_document = \"FICT-AIR-FUEL-A\"; present; meaning and suitability unverified"` (`"instruments[FT-FUEL-A].facts.source_document"`)
- Supplied candidate field: `"FT-FUEL-A source_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[FT-FUEL-A].facts.source_revision"`)
- Supplied candidate field: `"FT-FUEL-A equipment_scope = \"F-A only\"; present; meaning and suitability unverified"` (`"instruments[FT-FUEL-A].facts.equipment_scope"`)
- Supplied candidate field: `"FT-FUEL-A operating_range_basis = \"fictional low/high firing paired flow records\"; present; meaning and suitability unverified"` (`"instruments[FT-FUEL-A].facts.operating_range_basis"`)
- Supplied candidate field: `"FT-FUEL-A underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[FT-FUEL-A].facts.underlying_claim_verified"`)
- Supplied candidate field: `"FT-FUEL-A record_service = \"combustion fuel flow\"; present; meaning and suitability unverified"` (`"instruments[FT-FUEL-A].facts.record_service"`)
- Supplied candidate field: `"FT-AIR-A source_document = \"FICT-AIR-FUEL-A\"; present; meaning and suitability unverified"` (`"instruments[FT-AIR-A].facts.source_document"`)
- Supplied candidate field: `"FT-AIR-A source_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[FT-AIR-A].facts.source_revision"`)
- Supplied candidate field: `"FT-AIR-A equipment_scope = \"F-A only\"; present; meaning and suitability unverified"` (`"instruments[FT-AIR-A].facts.equipment_scope"`)
- Supplied candidate field: `"FT-AIR-A underlying_claim_verified = false; present; meaning and suitability unverified"` (`"instruments[FT-AIR-A].facts.underlying_claim_verified"`)
- Supplied candidate field: `"FT-AIR-A record_service = \"combustion air flow\"; present; meaning and suitability unverified"` (`"instruments[FT-AIR-A].facts.record_service"`)
- Supplied candidate field: `"FT-AIR-A association_claim = \"paired with FT-FUEL-A in fictional record\"; present; meaning and suitability unverified"` (`"instruments[FT-AIR-A].facts.association_claim"`)
- On drawing: Supplied candidate fact, basis unverified: F-A fuel_service = natural gas (`units[F-A].facts.fuel_service`)

**Data to collect**

- Existing service and control-applicability basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): F-A (F-A) fuel_service = "natural gas" [units[F-A].facts.fuel_service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: permitted existing equipment/service description and design/control narrative identifying heat source, water/steam service, drum or no-drum configuration, intended operating modes and source revision/owner. How: Establish boiler service and applicability before any drum task. A boiler name alone does not establish a steam-water drum. For supplied hot-water or other no-drum service, acknowledge the applicable scope instead of imposing drum-control work. Unknown service requires clarification, not an inferred missing controller. Unfired waste-heat steam-drum equipment may still need level-control review despite having no fuel or combustion scope.
- Applicable control configuration, operating modes and review disposition [not on drawing]. Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: existing design/control narratives and operating evidence for the functions actually applicable to this boiler; where steam-water level control applies, retain level, steam-flow and feedwater-flow relationships and normal/startup/low-load modes; then DCS/PLC configuration: applicable approved existing controller, measurement/output and mode records, through the company-approved access route. How: Keep indication labels distinct from configured and active control. S8 describes level-only and additional steam/feedwater-flow inputs, including response to abrupt load changes; it does not mandate three-element control on every boiler. Review intended normal/startup/low-load modes and relevant load/feedwater conditions without declaring a single-element mode faulty. Adequate existing evidence may settle or defer the job without a project; new work belongs to the responsible company reviewer.

**How it is decided:** First establish service and applicable control functions. Review combustion only where relevant; review steam-water level control only where that service applies, including waste-heat steam-drum equipment without a burner. Three depicted measurements do not prove an active three-element loop, and a missing depicted element does not establish an upgrade need. Existing supported design/mode and operating records may answer or defer the investigation; retain unresolved evidence and next owner.

**What the source says (S8, S19, S24):** S8 describes boiler combustion and water-level control functions and differing levels of control complexity. S19’s historical broad boiler process-control estimate is not a three-element drum-control gain; no percentage or payback is assigned to this applicability review.
IAC/ITAC recommendation code: 2.121x (category only).

**Limits:** C5 uses S8 printed6–7/PDFindices11–12 explicitly for boiler functional/service review. The boiler selector does not infer a drum, combustion or missing control; dry furnaces/kilns are outside this boiler-specific question and may use E16 where eligible. Unfired waste-heat steam-drum equipment remains eligible without fuel evidence. S19/S24 do not establish a universal three-element requirement or drum-specific benefit. Supplied Boolean/service/qualification fields are literal claims, not installed-state, adequate performance or company authority.

### C5: What boiler service and control functions apply, and what do existing records establish about any applicable steam-water level-control basis?

**About:** F-B  

**Finding reference (JSON string):** `"C5@F-B"`
**Asset IDs (JSON array):** `["F-B", "stream:FUEL-B", "stream:FLUE-B"]`

**Evidence on the drawing / model**

- equipment F-B reads "F-B Fired unit B" (`units[F-B]`)
- Represented fuel, air or flue stream context: stream FUEL-B (asset stream:FUEL-B) reads "Natural gas fuel B" at F-B (`streams[FUEL-B]`)
- Represented fuel, air or flue stream context: stream FLUE-B (asset stream:FLUE-B) reads "Flue gas B" (`streams[FLUE-B]`)
- Supplied candidate field: `"F-B fuel_service = \"natural gas\"; present; meaning and suitability unverified"` (`"units[F-B].facts.fuel_service"`)
- Supplied candidate field: `"F-B operating_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"units[F-B].facts.operating_basis"`)
- On drawing: Supplied candidate fact, basis unverified: F-B fuel_service = natural gas (`units[F-B].facts.fuel_service`)

**Data to collect**

- Existing service and control-applicability basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): F-B (F-B) fuel_service = "natural gas" [units[F-B].facts.fuel_service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: permitted existing equipment/service description and design/control narrative identifying heat source, water/steam service, drum or no-drum configuration, intended operating modes and source revision/owner. How: Establish boiler service and applicability before any drum task. A boiler name alone does not establish a steam-water drum. For supplied hot-water or other no-drum service, acknowledge the applicable scope instead of imposing drum-control work. Unknown service requires clarification, not an inferred missing controller. Unfired waste-heat steam-drum equipment may still need level-control review despite having no fuel or combustion scope.
- Applicable control configuration, operating modes and review disposition [not on drawing]. Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: existing design/control narratives and operating evidence for the functions actually applicable to this boiler; where steam-water level control applies, retain level, steam-flow and feedwater-flow relationships and normal/startup/low-load modes; then DCS/PLC configuration: applicable approved existing controller, measurement/output and mode records, through the company-approved access route. How: Keep indication labels distinct from configured and active control. S8 describes level-only and additional steam/feedwater-flow inputs, including response to abrupt load changes; it does not mandate three-element control on every boiler. Review intended normal/startup/low-load modes and relevant load/feedwater conditions without declaring a single-element mode faulty. Adequate existing evidence may settle or defer the job without a project; new work belongs to the responsible company reviewer.

**How it is decided:** First establish service and applicable control functions. Review combustion only where relevant; review steam-water level control only where that service applies, including waste-heat steam-drum equipment without a burner. Three depicted measurements do not prove an active three-element loop, and a missing depicted element does not establish an upgrade need. Existing supported design/mode and operating records may answer or defer the investigation; retain unresolved evidence and next owner.

**What the source says (S8, S19, S24):** S8 describes boiler combustion and water-level control functions and differing levels of control complexity. S19’s historical broad boiler process-control estimate is not a three-element drum-control gain; no percentage or payback is assigned to this applicability review.
IAC/ITAC recommendation code: 2.121x (category only).

**Limits:** C5 uses S8 printed6–7/PDFindices11–12 explicitly for boiler functional/service review. The boiler selector does not infer a drum, combustion or missing control; dry furnaces/kilns are outside this boiler-specific question and may use E16 where eligible. Unfired waste-heat steam-drum equipment remains eligible without fuel evidence. S19/S24 do not establish a universal three-element requirement or drum-specific benefit. Supplied Boolean/service/qualification fields are literal claims, not installed-state, adequate performance or company authority.

## Sources cited above

- S8: Improving Steam System Performance: A Sourcebook for Industry, 2nd ed. (DOE/GO-102012-3423, rev. Oct 2012). https://www.energy.gov/sites/prod/files/2014/05/f15/steamsourcebook.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
