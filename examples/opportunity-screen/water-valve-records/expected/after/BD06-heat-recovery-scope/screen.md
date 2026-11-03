# Opportunity screen: Fictional E13 development control; not a plant record

Model: `examples/opportunity-screen/water-valve-records/models/BD06-heat-recovery-scope.json`. Questions: `data/questions.json`.

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

**About:** CONTINUOUS  

**Finding reference (JSON string):** `"E13@CONTINUOUS"`
**Asset IDs (JSON array):** `["CONTINUOUS", "HV-1"]`

**Evidence on the drawing / model**

- equipment CONTINUOUS reads "CONTINUOUS CONTINUOUS fictional boiler" (`units[CONTINUOUS]`)
- Blowdown: hand valve HV-1 reads "HV-1 Blowdown valve, fictional declared connection" at CONTINUOUS (`manual_valves[HV-1]`)
- Supplied candidate field: `"CONTINUOUS water_service = \"steam-water boiler; explicit source declaration\"; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.water_service"`)
- Supplied candidate field: `"CONTINUOUS blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.blowdown_function"`)
- Supplied candidate field: `"CONTINUOUS operation_mode = \"continuous\"; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.operation_mode"`)
- Supplied candidate field: `"CONTINUOUS pressure_psig = 150; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.pressure_psig"`)
- Supplied candidate field: `"CONTINUOUS blowdown_rate = \"fictional 400 lb/h\"; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.blowdown_rate"`)
- Supplied candidate field: `"CONTINUOUS operating_hours = 4000; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.operating_hours"`)
- Supplied candidate field: `"CONTINUOUS recovery_status = \"unknown\"; blank; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.recovery_status"`)
- Supplied candidate field: `"CONTINUOUS receiving_duty = \"potential feedwater sink, suitability unverified\"; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.receiving_duty"`)
- Supplied candidate field: `"CONTINUOUS record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.record_source"`)
- Supplied candidate field: `"CONTINUOUS record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.record_revision"`)
- Supplied candidate field: `"CONTINUOUS record_available = true; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.record_available"`)
- Supplied candidate field: `"CONTINUOUS source_is_fictional = true; present; meaning and suitability unverified"` (`"units[CONTINUOUS].facts.source_is_fictional"`)
- Supplied candidate field: `"HV-1 blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.blowdown_function"`)
- Supplied candidate field: `"HV-1 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_source"`)
- Supplied candidate field: `"HV-1 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_revision"`)
- Supplied candidate field: `"HV-1 record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.record_available"`)
- Supplied candidate field: `"HV-1 source_is_fictional = true; present; meaning and suitability unverified"` (`"manual_valves[HV-1].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS water_service = steam-water boiler; explicit source declaration (`units[CONTINUOUS].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS blowdown_function = surface (`units[CONTINUOUS].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS operation_mode = continuous (`units[CONTINUOUS].facts.operation_mode`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS pressure_psig = 150 (`units[CONTINUOUS].facts.pressure_psig`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS blowdown_rate = fictional 400 lb/h (`units[CONTINUOUS].facts.blowdown_rate`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS operating_hours = 4000 (`units[CONTINUOUS].facts.operating_hours`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS receiving_duty = potential feedwater sink, suitability unverified (`units[CONTINUOUS].facts.receiving_duty`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS record_source = Fictional training packet; no plant or engineering approval (`units[CONTINUOUS].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS record_revision = R1 (`units[CONTINUOUS].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS record_available = True (`units[CONTINUOUS].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: CONTINUOUS source_is_fictional = True (`units[CONTINUOUS].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): CONTINUOUS (CONTINUOUS) water_service = "steam-water boiler; explicit source declaration" [units[CONTINUOUS].facts.water_service]; CONTINUOUS (CONTINUOUS) blowdown_function = "surface" [units[CONTINUOUS].facts.blowdown_function]; CONTINUOUS (CONTINUOUS) operation_mode = "continuous" [units[CONTINUOUS].facts.operation_mode]; CONTINUOUS (CONTINUOUS) pressure_psig = 150 [units[CONTINUOUS].facts.pressure_psig]; CONTINUOUS (CONTINUOUS) blowdown_rate = "fictional 400 lb/h" [units[CONTINUOUS].facts.blowdown_rate]; CONTINUOUS (CONTINUOUS) operating_hours = 4000 [units[CONTINUOUS].facts.operating_hours]; CONTINUOUS (CONTINUOUS) receiving_duty = "potential feedwater sink, suitability unverified" [units[CONTINUOUS].facts.receiving_duty]; CONTINUOUS (CONTINUOUS) record_source = "Fictional training packet; no plant or engineering approval" [units[CONTINUOUS].facts.record_source]; CONTINUOUS (CONTINUOUS) record_revision = "R1" [units[CONTINUOUS].facts.record_revision]; CONTINUOUS (CONTINUOUS) record_available = true [units[CONTINUOUS].facts.record_available]; CONTINUOUS (CONTINUOUS) source_is_fictional = true [units[CONTINUOUS].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

### E13: What do existing records establish about this boiler's blowdown function, water-treatment control and any remaining heat-recovery opportunity?

**About:** INTERMITTENT  

**Finding reference (JSON string):** `"E13@INTERMITTENT"`
**Asset IDs (JSON array):** `["INTERMITTENT", "HV-2"]`

**Evidence on the drawing / model**

- equipment INTERMITTENT reads "INTERMITTENT INTERMITTENT fictional boiler" (`units[INTERMITTENT]`)
- Blowdown: hand valve HV-2 reads "HV-2 Blowdown valve, fictional declared connection" at INTERMITTENT (`manual_valves[HV-2]`)
- Supplied candidate field: `"INTERMITTENT water_service = \"steam-water boiler; explicit source declaration\"; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.water_service"`)
- Supplied candidate field: `"INTERMITTENT blowdown_function = \"bottom\"; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.blowdown_function"`)
- Supplied candidate field: `"INTERMITTENT operation_mode = \"intermittent low duty\"; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.operation_mode"`)
- Supplied candidate field: `"INTERMITTENT pressure_psig = 15; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.pressure_psig"`)
- Supplied candidate field: `"INTERMITTENT blowdown_rate = \"unknown\"; blank; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.blowdown_rate"`)
- Supplied candidate field: `"INTERMITTENT operating_hours = 10; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.operating_hours"`)
- Supplied candidate field: `"INTERMITTENT recovery_status = \"not established\"; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.recovery_status"`)
- Supplied candidate field: `"INTERMITTENT receiving_duty = \"unrelated non-water process; no qualified sink\"; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.receiving_duty"`)
- Supplied candidate field: `"INTERMITTENT record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.record_source"`)
- Supplied candidate field: `"INTERMITTENT record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.record_revision"`)
- Supplied candidate field: `"INTERMITTENT record_available = true; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.record_available"`)
- Supplied candidate field: `"INTERMITTENT source_is_fictional = true; present; meaning and suitability unverified"` (`"units[INTERMITTENT].facts.source_is_fictional"`)
- Supplied candidate field: `"HV-2 blowdown_function = \"bottom\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.blowdown_function"`)
- Supplied candidate field: `"HV-2 record_source = \"Fictional training packet; no plant or engineering approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_source"`)
- Supplied candidate field: `"HV-2 record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_revision"`)
- Supplied candidate field: `"HV-2 record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.record_available"`)
- Supplied candidate field: `"HV-2 source_is_fictional = true; present; meaning and suitability unverified"` (`"manual_valves[HV-2].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT water_service = steam-water boiler; explicit source declaration (`units[INTERMITTENT].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT blowdown_function = bottom (`units[INTERMITTENT].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT operation_mode = intermittent low duty (`units[INTERMITTENT].facts.operation_mode`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT pressure_psig = 15 (`units[INTERMITTENT].facts.pressure_psig`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT operating_hours = 10 (`units[INTERMITTENT].facts.operating_hours`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT recovery_status = not established (`units[INTERMITTENT].facts.recovery_status`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT receiving_duty = unrelated non-water process; no qualified sink (`units[INTERMITTENT].facts.receiving_duty`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT record_source = Fictional training packet; no plant or engineering approval (`units[INTERMITTENT].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT record_revision = R1 (`units[INTERMITTENT].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT record_available = True (`units[INTERMITTENT].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: INTERMITTENT source_is_fictional = True (`units[INTERMITTENT].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): INTERMITTENT (INTERMITTENT) water_service = "steam-water boiler; explicit source declaration" [units[INTERMITTENT].facts.water_service]; INTERMITTENT (INTERMITTENT) blowdown_function = "bottom" [units[INTERMITTENT].facts.blowdown_function]; INTERMITTENT (INTERMITTENT) operation_mode = "intermittent low duty" [units[INTERMITTENT].facts.operation_mode]; INTERMITTENT (INTERMITTENT) pressure_psig = 15 [units[INTERMITTENT].facts.pressure_psig]; INTERMITTENT (INTERMITTENT) operating_hours = 10 [units[INTERMITTENT].facts.operating_hours]; INTERMITTENT (INTERMITTENT) recovery_status = "not established" [units[INTERMITTENT].facts.recovery_status]; INTERMITTENT (INTERMITTENT) receiving_duty = "unrelated non-water process; no qualified sink" [units[INTERMITTENT].facts.receiving_duty]; INTERMITTENT (INTERMITTENT) record_source = "Fictional training packet; no plant or engineering approval" [units[INTERMITTENT].facts.record_source]; INTERMITTENT (INTERMITTENT) record_revision = "R1" [units[INTERMITTENT].facts.record_revision]; INTERMITTENT (INTERMITTENT) record_available = true [units[INTERMITTENT].facts.record_available]; INTERMITTENT (INTERMITTENT) source_is_fictional = true [units[INTERMITTENT].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

## Sources cited above

- S5: Steam Tip #9, Minimize Boiler Blowdown (DOE/GO-102012-3406). https://www.energy.gov/sites/prod/files/2014/05/f16/steam9_blowdown.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
