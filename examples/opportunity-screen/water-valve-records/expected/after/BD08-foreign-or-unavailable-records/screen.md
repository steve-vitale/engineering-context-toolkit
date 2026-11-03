# Opportunity screen: Fictional E13 development control; not a plant record

Model: `examples/opportunity-screen/water-valve-records/models/BD08-foreign-or-unavailable-records.json`. Questions: `data/questions.json`.

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

**About:** SITE-A  

**Finding reference (JSON string):** `"E13@SITE-A"`
**Asset IDs (JSON array):** `["SITE-A", "HV-1", "AT-8"]`

**Evidence on the drawing / model**

- equipment SITE-A reads "SITE-A SITE-A fictional boiler" (`units[SITE-A]`)
- Blowdown: hand valve HV-1 reads "HV-1 Blowdown valve, fictional declared connection" at SITE-A (`manual_valves[HV-1]`)
- Unverified analyzer/control candidate: instrument AT-8 reads "AT-8 supplied conductivity record" at SITE-A (`instruments[AT-8]`)
- Supplied candidate field: `"SITE-A water_service = \"steam-water boiler; explicit source declaration\"; present; meaning and suitability unverified"` (`"units[SITE-A].facts.water_service"`)
- Supplied candidate field: `"SITE-A blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[SITE-A].facts.blowdown_function"`)
- Supplied candidate field: `"SITE-A record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"units[SITE-A].facts.record_source"`)
- Supplied candidate field: `"SITE-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[SITE-A].facts.record_revision"`)
- Supplied candidate field: `"SITE-A record_available = true; present; meaning and suitability unverified"` (`"units[SITE-A].facts.record_available"`)
- Supplied candidate field: `"SITE-A record_scope = \"site A boiler label B1\"; present; meaning and suitability unverified"` (`"units[SITE-A].facts.record_scope"`)
- Supplied candidate field: `"SITE-A source_is_fictional = true; present; meaning and suitability unverified"` (`"units[SITE-A].facts.source_is_fictional"`)
- Supplied candidate field: `"HV-1 blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.blowdown_function"`)
- Supplied candidate field: `"HV-1 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_source"`)
- Supplied candidate field: `"HV-1 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_revision"`)
- Supplied candidate field: `"HV-1 record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_available"`)
- Supplied candidate field: `"HV-1 source_is_fictional = true; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.source_is_fictional"`)
- Supplied candidate field: `"AT-8 analyzer_purpose = \"supplied conductivity record\"; present; meaning and suitability unverified"` (`"instruments[AT-8].facts.analyzer_purpose"`)
- Supplied candidate field: `"AT-8 analyzer_target = \"foreign site C B1\"; present; meaning and suitability unverified"` (`"instruments[AT-8].facts.analyzer_target"`)
- Supplied candidate field: `"AT-8 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"instruments[AT-8].facts.record_source"`)
- Supplied candidate field: `"AT-8 record_revision = \"R0\"; present; meaning and suitability unverified"` (`"instruments[AT-8].facts.record_revision"`)
- Supplied candidate field: `"AT-8 record_available = false; present; meaning and suitability unverified"` (`"instruments[AT-8].facts.record_available"`)
- Supplied candidate field: `"AT-8 record_scope = \"foreign site C, not SITE-A\"; present; meaning and suitability unverified"` (`"instruments[AT-8].facts.record_scope"`)
- Supplied candidate field: `"AT-8 source_is_fictional = true; present; meaning and suitability unverified"` (`"instruments[AT-8].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: SITE-A water_service = steam-water boiler; explicit source declaration (`units[SITE-A].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: SITE-A blowdown_function = surface (`units[SITE-A].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: SITE-A record_source = Fictional training packet; no plant or engineering approval (`units[SITE-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: SITE-A record_revision = R1 (`units[SITE-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: SITE-A record_available = True (`units[SITE-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: SITE-A record_scope = site A boiler label B1 (`units[SITE-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: SITE-A source_is_fictional = True (`units[SITE-A].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): SITE-A (SITE-A) water_service = "steam-water boiler; explicit source declaration" [units[SITE-A].facts.water_service]; SITE-A (SITE-A) blowdown_function = "surface" [units[SITE-A].facts.blowdown_function]; SITE-A (SITE-A) record_source = "Fictional training packet; no plant or engineering approval" [units[SITE-A].facts.record_source]; SITE-A (SITE-A) record_revision = "R1" [units[SITE-A].facts.record_revision]; SITE-A (SITE-A) record_available = true [units[SITE-A].facts.record_available]; SITE-A (SITE-A) record_scope = "site A boiler label B1" [units[SITE-A].facts.record_scope]; SITE-A (SITE-A) source_is_fictional = true [units[SITE-A].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

### E13: What do existing records establish about this boiler's blowdown function, water-treatment control and any remaining heat-recovery opportunity?

**About:** SITE-B  

**Finding reference (JSON string):** `"E13@SITE-B"`
**Asset IDs (JSON array):** `["SITE-B", "HV-2"]`

**Evidence on the drawing / model**

- equipment SITE-B reads "SITE-B SITE-B fictional boiler" (`units[SITE-B]`)
- Blowdown: hand valve HV-2 reads "HV-2 Blowdown valve, fictional declared connection" at SITE-B (`manual_valves[HV-2]`)
- Supplied candidate field: `"SITE-B water_service = \"steam-water boiler; explicit source declaration\"; present; meaning and suitability unverified"` (`"units[SITE-B].facts.water_service"`)
- Supplied candidate field: `"SITE-B blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[SITE-B].facts.blowdown_function"`)
- Supplied candidate field: `"SITE-B record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"units[SITE-B].facts.record_source"`)
- Supplied candidate field: `"SITE-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[SITE-B].facts.record_revision"`)
- Supplied candidate field: `"SITE-B record_available = true; present; meaning and suitability unverified"` (`"units[SITE-B].facts.record_available"`)
- Supplied candidate field: `"SITE-B record_scope = \"site B boiler label B1; no available matching record\"; present; meaning and suitability unverified"` (`"units[SITE-B].facts.record_scope"`)
- Supplied candidate field: `"SITE-B source_is_fictional = true; present; meaning and suitability unverified"` (`"units[SITE-B].facts.source_is_fictional"`)
- Supplied candidate field: `"HV-2 blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.blowdown_function"`)
- Supplied candidate field: `"HV-2 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_source"`)
- Supplied candidate field: `"HV-2 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_revision"`)
- Supplied candidate field: `"HV-2 record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_available"`)
- Supplied candidate field: `"HV-2 source_is_fictional = true; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: SITE-B water_service = steam-water boiler; explicit source declaration (`units[SITE-B].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: SITE-B blowdown_function = surface (`units[SITE-B].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: SITE-B record_source = Fictional training packet; no plant or engineering approval (`units[SITE-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: SITE-B record_revision = R1 (`units[SITE-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: SITE-B record_available = True (`units[SITE-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: SITE-B record_scope = site B boiler label B1; no available matching record (`units[SITE-B].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: SITE-B source_is_fictional = True (`units[SITE-B].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): SITE-B (SITE-B) water_service = "steam-water boiler; explicit source declaration" [units[SITE-B].facts.water_service]; SITE-B (SITE-B) blowdown_function = "surface" [units[SITE-B].facts.blowdown_function]; SITE-B (SITE-B) record_source = "Fictional training packet; no plant or engineering approval" [units[SITE-B].facts.record_source]; SITE-B (SITE-B) record_revision = "R1" [units[SITE-B].facts.record_revision]; SITE-B (SITE-B) record_available = true [units[SITE-B].facts.record_available]; SITE-B (SITE-B) record_scope = "site B boiler label B1; no available matching record" [units[SITE-B].facts.record_scope]; SITE-B (SITE-B) source_is_fictional = true [units[SITE-B].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

## Sources cited above

- S5: Steam Tip #9, Minimize Boiler Blowdown (DOE/GO-102012-3406). https://www.energy.gov/sites/prod/files/2014/05/f16/steam9_blowdown.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
