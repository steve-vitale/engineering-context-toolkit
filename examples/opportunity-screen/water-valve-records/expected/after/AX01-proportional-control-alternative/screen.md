# Opportunity screen: Fictional source-informed E13 controls; not a plant record

Model: `examples/opportunity-screen/water-valve-records/models/AX01-proportional-control-alternative.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
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

**About:** PROPORTIONAL  

**Finding reference (JSON string):** `"E13@PROPORTIONAL"`
**Asset IDs (JSON array):** `["PROPORTIONAL", "HV-AX-1"]`

**Evidence on the drawing / model**

- equipment PROPORTIONAL reads "PROPORTIONAL boiler with existing proportional control" (`units[PROPORTIONAL]`)
- Blowdown: hand valve HV-AX-1 reads "HV-AX-1 Declared blowdown candidate" at PROPORTIONAL (`manual_valves[HV-AX-1]`)
- Supplied candidate field: `"PROPORTIONAL water_service = \"declared steam-water boiler\"; present; meaning and suitability unverified"` (`"units[PROPORTIONAL].facts.water_service"`)
- Supplied candidate field: `"PROPORTIONAL blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[PROPORTIONAL].facts.blowdown_function"`)
- Supplied candidate field: `"PROPORTIONAL control_basis = \"Proportional surface blowdown to makeup-water flow; named boiler record, applicability and treatment still require review\"; present; meaning and suitability unverified"` (`"units[PROPORTIONAL].facts.control_basis"`)
- Supplied candidate field: `"PROPORTIONAL sample_period = \"fictional reviewed reporting interval\"; present; meaning and suitability unverified"` (`"units[PROPORTIONAL].facts.sample_period"`)
- Supplied candidate field: `"PROPORTIONAL record_source = \"Fictional explicit original record, no company approval\"; present; meaning and suitability unverified"` (`"units[PROPORTIONAL].facts.record_source"`)
- Supplied candidate field: `"PROPORTIONAL record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[PROPORTIONAL].facts.record_revision"`)
- Supplied candidate field: `"PROPORTIONAL record_available = true; present; meaning and suitability unverified"` (`"units[PROPORTIONAL].facts.record_available"`)
- Supplied candidate field: `"PROPORTIONAL source_is_fictional = true; present; meaning and suitability unverified"` (`"units[PROPORTIONAL].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: PROPORTIONAL water_service = declared steam-water boiler (`units[PROPORTIONAL].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: PROPORTIONAL blowdown_function = surface (`units[PROPORTIONAL].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: PROPORTIONAL control_basis = Proportional surface blowdown to makeup-water flow; named boiler record, applicability and treatment still require review (`units[PROPORTIONAL].facts.control_basis`)
- On drawing: Supplied candidate fact, basis unverified: PROPORTIONAL sample_period = fictional reviewed reporting interval (`units[PROPORTIONAL].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: PROPORTIONAL record_source = Fictional explicit original record, no company approval (`units[PROPORTIONAL].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PROPORTIONAL record_revision = R1 (`units[PROPORTIONAL].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PROPORTIONAL record_available = True (`units[PROPORTIONAL].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PROPORTIONAL source_is_fictional = True (`units[PROPORTIONAL].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): PROPORTIONAL (PROPORTIONAL) water_service = "declared steam-water boiler" [units[PROPORTIONAL].facts.water_service]; PROPORTIONAL (PROPORTIONAL) blowdown_function = "surface" [units[PROPORTIONAL].facts.blowdown_function]; PROPORTIONAL (PROPORTIONAL) control_basis = "Proportional surface blowdown to makeup-water flow; named boiler record, applicability and treatment still require review" [units[PROPORTIONAL].facts.control_basis]; PROPORTIONAL (PROPORTIONAL) sample_period = "fictional reviewed reporting interval" [units[PROPORTIONAL].facts.sample_period]; PROPORTIONAL (PROPORTIONAL) record_source = "Fictional explicit original record, no company approval" [units[PROPORTIONAL].facts.record_source]; PROPORTIONAL (PROPORTIONAL) record_revision = "R1" [units[PROPORTIONAL].facts.record_revision]; PROPORTIONAL (PROPORTIONAL) record_available = true [units[PROPORTIONAL].facts.record_available]; PROPORTIONAL (PROPORTIONAL) source_is_fictional = true [units[PROPORTIONAL].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

### E13: What do existing records establish about this boiler's blowdown function, water-treatment control and any remaining heat-recovery opportunity?

**About:** MISSING  

**Finding reference (JSON string):** `"E13@MISSING"`
**Asset IDs (JSON array):** `["MISSING", "HV-AX-2"]`

**Evidence on the drawing / model**

- equipment MISSING reads "MISSING boiler with unavailable control basis" (`units[MISSING]`)
- Blowdown: hand valve HV-AX-2 reads "HV-AX-2 Declared blowdown candidate" at MISSING (`manual_valves[HV-AX-2]`)
- Supplied candidate field: `"MISSING water_service = \"declared steam-water boiler\"; present; meaning and suitability unverified"` (`"units[MISSING].facts.water_service"`)
- Supplied candidate field: `"MISSING blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[MISSING].facts.blowdown_function"`)
- Supplied candidate field: `"MISSING control_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"units[MISSING].facts.control_basis"`)
- Supplied candidate field: `"MISSING record_source = \"Fictional explicit original record, no company approval\"; present; meaning and suitability unverified"` (`"units[MISSING].facts.record_source"`)
- Supplied candidate field: `"MISSING record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[MISSING].facts.record_revision"`)
- Supplied candidate field: `"MISSING record_available = false; present; meaning and suitability unverified"` (`"units[MISSING].facts.record_available"`)
- Supplied candidate field: `"MISSING source_is_fictional = true; present; meaning and suitability unverified"` (`"units[MISSING].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: MISSING water_service = declared steam-water boiler (`units[MISSING].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: MISSING blowdown_function = surface (`units[MISSING].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: MISSING record_source = Fictional explicit original record, no company approval (`units[MISSING].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: MISSING record_revision = R1 (`units[MISSING].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: MISSING record_available = False (`units[MISSING].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: MISSING source_is_fictional = True (`units[MISSING].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): MISSING (MISSING) water_service = "declared steam-water boiler" [units[MISSING].facts.water_service]; MISSING (MISSING) blowdown_function = "surface" [units[MISSING].facts.blowdown_function]; MISSING (MISSING) record_source = "Fictional explicit original record, no company approval" [units[MISSING].facts.record_source]; MISSING (MISSING) record_revision = "R1" [units[MISSING].facts.record_revision]; MISSING (MISSING) record_available = false [units[MISSING].facts.record_available]; MISSING (MISSING) source_is_fictional = true [units[MISSING].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

## Sources cited above

- S5: Steam Tip #9, Minimize Boiler Blowdown (DOE/GO-102012-3406). https://www.energy.gov/sites/prod/files/2014/05/f16/steam9_blowdown.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
