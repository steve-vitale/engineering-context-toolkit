# Opportunity screen: Fictional E13 development control; not a plant record

Model: `examples/opportunity-screen/water-valve-records/models/BD01-bottom-versus-surface.json`. Questions: `data/questions.json`.

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

**About:** BOTTOM  

**Finding reference (JSON string):** `"E13@BOTTOM"`
**Asset IDs (JSON array):** `["BOTTOM", "HV-1"]`

**Evidence on the drawing / model**

- equipment BOTTOM reads "BOTTOM BOTTOM fictional boiler" (`units[BOTTOM]`)
- Blowdown: hand valve HV-1 reads "HV-1 Blowdown valve, fictional declared connection" at BOTTOM (`manual_valves[HV-1]`)
- Supplied candidate field: `"BOTTOM water_service = \"steam-water boiler; explicit source declaration\"; present; meaning and suitability unverified"` (`"units[BOTTOM].facts.water_service"`)
- Supplied candidate field: `"BOTTOM blowdown_function = \"bottom/mud suspended-solids removal\"; present; meaning and suitability unverified"` (`"units[BOTTOM].facts.blowdown_function"`)
- Supplied candidate field: `"BOTTOM operation_mode = \"manual intermittent normal practice; adequacy not reviewed\"; present; meaning and suitability unverified"` (`"units[BOTTOM].facts.operation_mode"`)
- Supplied candidate field: `"BOTTOM record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"units[BOTTOM].facts.record_source"`)
- Supplied candidate field: `"BOTTOM record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[BOTTOM].facts.record_revision"`)
- Supplied candidate field: `"BOTTOM record_available = true; present; meaning and suitability unverified"` (`"units[BOTTOM].facts.record_available"`)
- Supplied candidate field: `"BOTTOM source_is_fictional = true; present; meaning and suitability unverified"` (`"units[BOTTOM].facts.source_is_fictional"`)
- Supplied candidate field: `"HV-1 blowdown_function = \"bottom/mud suspended-solids removal\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.blowdown_function"`)
- Supplied candidate field: `"HV-1 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_source"`)
- Supplied candidate field: `"HV-1 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_revision"`)
- Supplied candidate field: `"HV-1 record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_available"`)
- Supplied candidate field: `"HV-1 source_is_fictional = true; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: BOTTOM water_service = steam-water boiler; explicit source declaration (`units[BOTTOM].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: BOTTOM blowdown_function = bottom/mud suspended-solids removal (`units[BOTTOM].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: BOTTOM operation_mode = manual intermittent normal practice; adequacy not reviewed (`units[BOTTOM].facts.operation_mode`)
- On drawing: Supplied candidate fact, basis unverified: BOTTOM record_source = Fictional training packet; no plant or engineering approval (`units[BOTTOM].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: BOTTOM record_revision = R1 (`units[BOTTOM].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: BOTTOM record_available = True (`units[BOTTOM].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: BOTTOM source_is_fictional = True (`units[BOTTOM].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): BOTTOM (BOTTOM) water_service = "steam-water boiler; explicit source declaration" [units[BOTTOM].facts.water_service]; BOTTOM (BOTTOM) blowdown_function = "bottom/mud suspended-solids removal" [units[BOTTOM].facts.blowdown_function]; BOTTOM (BOTTOM) operation_mode = "manual intermittent normal practice; adequacy not reviewed" [units[BOTTOM].facts.operation_mode]; BOTTOM (BOTTOM) record_source = "Fictional training packet; no plant or engineering approval" [units[BOTTOM].facts.record_source]; BOTTOM (BOTTOM) record_revision = "R1" [units[BOTTOM].facts.record_revision]; BOTTOM (BOTTOM) record_available = true [units[BOTTOM].facts.record_available]; BOTTOM (BOTTOM) source_is_fictional = true [units[BOTTOM].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

### E13: What do existing records establish about this boiler's blowdown function, water-treatment control and any remaining heat-recovery opportunity?

**About:** SURFACE  

**Finding reference (JSON string):** `"E13@SURFACE"`
**Asset IDs (JSON array):** `["SURFACE", "HV-2"]`

**Evidence on the drawing / model**

- equipment SURFACE reads "SURFACE SURFACE fictional boiler" (`units[SURFACE]`)
- Blowdown: hand valve HV-2 reads "HV-2 Blowdown valve, fictional declared connection" at SURFACE (`manual_valves[HV-2]`)
- Supplied candidate field: `"SURFACE water_service = \"steam-water boiler; explicit source declaration\"; present; meaning and suitability unverified"` (`"units[SURFACE].facts.water_service"`)
- Supplied candidate field: `"SURFACE blowdown_function = \"surface/skimming dissolved-solids removal\"; present; meaning and suitability unverified"` (`"units[SURFACE].facts.blowdown_function"`)
- Supplied candidate field: `"SURFACE operation_mode = \"continuous; chemistry basis unknown\"; present; meaning and suitability unverified"` (`"units[SURFACE].facts.operation_mode"`)
- Supplied candidate field: `"SURFACE record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"units[SURFACE].facts.record_source"`)
- Supplied candidate field: `"SURFACE record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[SURFACE].facts.record_revision"`)
- Supplied candidate field: `"SURFACE record_available = true; present; meaning and suitability unverified"` (`"units[SURFACE].facts.record_available"`)
- Supplied candidate field: `"SURFACE source_is_fictional = true; present; meaning and suitability unverified"` (`"units[SURFACE].facts.source_is_fictional"`)
- Supplied candidate field: `"HV-2 blowdown_function = \"surface/skimming dissolved-solids removal\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.blowdown_function"`)
- Supplied candidate field: `"HV-2 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_source"`)
- Supplied candidate field: `"HV-2 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_revision"`)
- Supplied candidate field: `"HV-2 record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_available"`)
- Supplied candidate field: `"HV-2 source_is_fictional = true; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: SURFACE water_service = steam-water boiler; explicit source declaration (`units[SURFACE].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: SURFACE blowdown_function = surface/skimming dissolved-solids removal (`units[SURFACE].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: SURFACE operation_mode = continuous; chemistry basis unknown (`units[SURFACE].facts.operation_mode`)
- On drawing: Supplied candidate fact, basis unverified: SURFACE record_source = Fictional training packet; no plant or engineering approval (`units[SURFACE].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: SURFACE record_revision = R1 (`units[SURFACE].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: SURFACE record_available = True (`units[SURFACE].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: SURFACE source_is_fictional = True (`units[SURFACE].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): SURFACE (SURFACE) water_service = "steam-water boiler; explicit source declaration" [units[SURFACE].facts.water_service]; SURFACE (SURFACE) blowdown_function = "surface/skimming dissolved-solids removal" [units[SURFACE].facts.blowdown_function]; SURFACE (SURFACE) operation_mode = "continuous; chemistry basis unknown" [units[SURFACE].facts.operation_mode]; SURFACE (SURFACE) record_source = "Fictional training packet; no plant or engineering approval" [units[SURFACE].facts.record_source]; SURFACE (SURFACE) record_revision = "R1" [units[SURFACE].facts.record_revision]; SURFACE (SURFACE) record_available = true [units[SURFACE].facts.record_available]; SURFACE (SURFACE) source_is_fictional = true [units[SURFACE].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

## Sources cited above

- S5: Steam Tip #9, Minimize Boiler Blowdown (DOE/GO-102012-3406). https://www.energy.gov/sites/prod/files/2014/05/f16/steam9_blowdown.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
