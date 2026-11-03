# Opportunity screen: Fictional E13 development control; not a plant record

Model: `examples/opportunity-screen/water-valve-records/models/BD02-generic-analyzer.json`. Questions: `data/questions.json`.

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

### E13: What do existing records establish about this boiler's blowdown function, water-treatment control and any remaining heat-recovery opportunity?

**About:** FLUE  

**Finding reference (JSON string):** `"E13@FLUE"`
**Asset IDs (JSON array):** `["FLUE", "HV-1", "AT-1"]`

**Evidence on the drawing / model**

- equipment FLUE reads "FLUE FLUE fictional boiler" (`units[FLUE]`)
- Blowdown: hand valve HV-1 reads "HV-1 Blowdown valve, fictional declared connection" at FLUE (`manual_valves[HV-1]`)
- Unverified analyzer/control candidate: instrument AT-1 reads "AT-1 flue-gas oxygen" at FLUE (`instruments[AT-1]`)
- Supplied candidate field: `"FLUE water_service = \"steam-water boiler; explicit source declaration\"; present; meaning and suitability unverified"` (`"units[FLUE].facts.water_service"`)
- Supplied candidate field: `"FLUE blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[FLUE].facts.blowdown_function"`)
- Supplied candidate field: `"FLUE control_basis = \"unknown water-control basis\"; present; meaning and suitability unverified"` (`"units[FLUE].facts.control_basis"`)
- Supplied candidate field: `"FLUE record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"units[FLUE].facts.record_source"`)
- Supplied candidate field: `"FLUE record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[FLUE].facts.record_revision"`)
- Supplied candidate field: `"FLUE record_available = true; present; meaning and suitability unverified"` (`"units[FLUE].facts.record_available"`)
- Supplied candidate field: `"FLUE source_is_fictional = true; present; meaning and suitability unverified"` (`"units[FLUE].facts.source_is_fictional"`)
- Supplied candidate field: `"HV-1 blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.blowdown_function"`)
- Supplied candidate field: `"HV-1 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_source"`)
- Supplied candidate field: `"HV-1 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_revision"`)
- Supplied candidate field: `"HV-1 record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_available"`)
- Supplied candidate field: `"HV-1 source_is_fictional = true; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.source_is_fictional"`)
- Supplied candidate field: `"AT-1 analyzer_purpose = \"flue-gas oxygen\"; present; meaning and suitability unverified"` (`"instruments[AT-1].facts.analyzer_purpose"`)
- Supplied candidate field: `"AT-1 analyzer_target = \"flue duct; not boiler water\"; present; meaning and suitability unverified"` (`"instruments[AT-1].facts.analyzer_target"`)
- Supplied candidate field: `"AT-1 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"instruments[AT-1].facts.record_source"`)
- Supplied candidate field: `"AT-1 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[AT-1].facts.record_revision"`)
- Supplied candidate field: `"AT-1 record_available = true; present; meaning and suitability unverified"` (`"instruments[AT-1].facts.record_available"`)
- Supplied candidate field: `"AT-1 source_is_fictional = true; present; meaning and suitability unverified"` (`"instruments[AT-1].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: FLUE water_service = steam-water boiler; explicit source declaration (`units[FLUE].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: FLUE blowdown_function = surface (`units[FLUE].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: FLUE control_basis = unknown water-control basis (`units[FLUE].facts.control_basis`)
- On drawing: Supplied candidate fact, basis unverified: FLUE record_source = Fictional training packet; no plant or engineering approval (`units[FLUE].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FLUE record_revision = R1 (`units[FLUE].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FLUE record_available = True (`units[FLUE].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: FLUE source_is_fictional = True (`units[FLUE].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): FLUE (FLUE) water_service = "steam-water boiler; explicit source declaration" [units[FLUE].facts.water_service]; FLUE (FLUE) blowdown_function = "surface" [units[FLUE].facts.blowdown_function]; FLUE (FLUE) control_basis = "unknown water-control basis" [units[FLUE].facts.control_basis]; FLUE (FLUE) record_source = "Fictional training packet; no plant or engineering approval" [units[FLUE].facts.record_source]; FLUE (FLUE) record_revision = "R1" [units[FLUE].facts.record_revision]; FLUE (FLUE) record_available = true [units[FLUE].facts.record_available]; FLUE (FLUE) source_is_fictional = true [units[FLUE].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

### E13: What do existing records establish about this boiler's blowdown function, water-treatment control and any remaining heat-recovery opportunity?

**About:** WATER  

**Finding reference (JSON string):** `"E13@WATER"`
**Asset IDs (JSON array):** `["WATER", "HV-2", "CT-2"]`

**Evidence on the drawing / model**

- equipment WATER reads "WATER WATER fictional boiler" (`units[WATER]`)
- Blowdown: hand valve HV-2 reads "HV-2 Blowdown valve, fictional declared connection" at WATER (`manual_valves[HV-2]`)
- Unverified analyzer/control candidate: instrument CT-2 reads "CT-2 boiler-water conductivity" at WATER (`instruments[CT-2]`)
- Supplied candidate field: `"WATER water_service = \"steam-water boiler; explicit source declaration\"; present; meaning and suitability unverified"` (`"units[WATER].facts.water_service"`)
- Supplied candidate field: `"WATER blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[WATER].facts.blowdown_function"`)
- Supplied candidate field: `"WATER control_basis = \"supplied water conductivity control record; not engineering-approved\"; present; meaning and suitability unverified"` (`"units[WATER].facts.control_basis"`)
- Supplied candidate field: `"WATER record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"units[WATER].facts.record_source"`)
- Supplied candidate field: `"WATER record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[WATER].facts.record_revision"`)
- Supplied candidate field: `"WATER record_available = true; present; meaning and suitability unverified"` (`"units[WATER].facts.record_available"`)
- Supplied candidate field: `"WATER source_is_fictional = true; present; meaning and suitability unverified"` (`"units[WATER].facts.source_is_fictional"`)
- Supplied candidate field: `"HV-2 blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.blowdown_function"`)
- Supplied candidate field: `"HV-2 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_source"`)
- Supplied candidate field: `"HV-2 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_revision"`)
- Supplied candidate field: `"HV-2 record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_available"`)
- Supplied candidate field: `"HV-2 source_is_fictional = true; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.source_is_fictional"`)
- Supplied candidate field: `"CT-2 analyzer_purpose = \"boiler-water conductivity\"; present; meaning and suitability unverified"` (`"instruments[CT-2].facts.analyzer_purpose"`)
- Supplied candidate field: `"CT-2 analyzer_target = \"WATER surface blowdown\"; present; meaning and suitability unverified"` (`"instruments[CT-2].facts.analyzer_target"`)
- Supplied candidate field: `"CT-2 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"instruments[CT-2].facts.record_source"`)
- Supplied candidate field: `"CT-2 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[CT-2].facts.record_revision"`)
- Supplied candidate field: `"CT-2 record_available = true; present; meaning and suitability unverified"` (`"instruments[CT-2].facts.record_available"`)
- Supplied candidate field: `"CT-2 source_is_fictional = true; present; meaning and suitability unverified"` (`"instruments[CT-2].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: WATER water_service = steam-water boiler; explicit source declaration (`units[WATER].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: WATER blowdown_function = surface (`units[WATER].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: WATER control_basis = supplied water conductivity control record; not engineering-approved (`units[WATER].facts.control_basis`)
- On drawing: Supplied candidate fact, basis unverified: WATER record_source = Fictional training packet; no plant or engineering approval (`units[WATER].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: WATER record_revision = R1 (`units[WATER].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: WATER record_available = True (`units[WATER].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: WATER source_is_fictional = True (`units[WATER].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): WATER (WATER) water_service = "steam-water boiler; explicit source declaration" [units[WATER].facts.water_service]; WATER (WATER) blowdown_function = "surface" [units[WATER].facts.blowdown_function]; WATER (WATER) control_basis = "supplied water conductivity control record; not engineering-approved" [units[WATER].facts.control_basis]; WATER (WATER) record_source = "Fictional training packet; no plant or engineering approval" [units[WATER].facts.record_source]; WATER (WATER) record_revision = "R1" [units[WATER].facts.record_revision]; WATER (WATER) record_available = true [units[WATER].facts.record_available]; WATER (WATER) source_is_fictional = true [units[WATER].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

## Sources cited above

- S5: Steam Tip #9, Minimize Boiler Blowdown (DOE/GO-102012-3406). https://www.energy.gov/sites/prod/files/2014/05/f16/steam9_blowdown.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
