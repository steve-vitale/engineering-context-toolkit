# Opportunity screen: Fictional source-informed E13 controls; not a plant record

Model: `examples/opportunity-screen/water-valve-records/models/AX02-rate-denominators.json`. Questions: `data/questions.json`.

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

**About:** STEAM  

**Finding reference (JSON string):** `"E13@STEAM"`
**Asset IDs (JSON array):** `["STEAM", "HV-AX-1"]`

**Evidence on the drawing / model**

- equipment STEAM reads "STEAM boiler steam-denominator record" (`units[STEAM]`)
- Blowdown: hand valve HV-AX-1 reads "HV-AX-1 Declared blowdown candidate" at STEAM (`manual_valves[HV-AX-1]`)
- Supplied candidate field: `"STEAM water_service = \"declared steam-water boiler\"; present; meaning and suitability unverified"` (`"units[STEAM].facts.water_service"`)
- Supplied candidate field: `"STEAM blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[STEAM].facts.blowdown_function"`)
- Supplied candidate field: `"STEAM quantity_units = \"lb/h\"; present; meaning and suitability unverified"` (`"units[STEAM].facts.quantity_units"`)
- Supplied candidate field: `"STEAM sample_period = \"fictional interval A\"; present; meaning and suitability unverified"` (`"units[STEAM].facts.sample_period"`)
- Supplied candidate field: `"STEAM fraction_denominator = \"blowdown / steam\"; present; meaning and suitability unverified"` (`"units[STEAM].facts.fraction_denominator"`)
- Supplied candidate field: `"STEAM blowdown_rate = 6; present; meaning and suitability unverified"` (`"units[STEAM].facts.blowdown_rate"`)
- Supplied candidate field: `"STEAM receiving_duty = \"unknown\"; blank; meaning and suitability unverified"` (`"units[STEAM].facts.receiving_duty"`)
- Supplied candidate field: `"STEAM record_source = \"Fictional explicit original record, no company approval\"; present; meaning and suitability unverified"` (`"units[STEAM].facts.record_source"`)
- Supplied candidate field: `"STEAM record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[STEAM].facts.record_revision"`)
- Supplied candidate field: `"STEAM source_is_fictional = true; present; meaning and suitability unverified"` (`"units[STEAM].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: STEAM water_service = declared steam-water boiler (`units[STEAM].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: STEAM blowdown_function = surface (`units[STEAM].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: STEAM quantity_units = lb/h (`units[STEAM].facts.quantity_units`)
- On drawing: Supplied candidate fact, basis unverified: STEAM sample_period = fictional interval A (`units[STEAM].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: STEAM fraction_denominator = blowdown / steam (`units[STEAM].facts.fraction_denominator`)
- On drawing: Supplied candidate fact, basis unverified: STEAM blowdown_rate = 6 (`units[STEAM].facts.blowdown_rate`)
- On drawing: Supplied candidate fact, basis unverified: STEAM record_source = Fictional explicit original record, no company approval (`units[STEAM].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: STEAM record_revision = R1 (`units[STEAM].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: STEAM source_is_fictional = True (`units[STEAM].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): STEAM (STEAM) water_service = "declared steam-water boiler" [units[STEAM].facts.water_service]; STEAM (STEAM) blowdown_function = "surface" [units[STEAM].facts.blowdown_function]; STEAM (STEAM) quantity_units = "lb/h" [units[STEAM].facts.quantity_units]; STEAM (STEAM) sample_period = "fictional interval A" [units[STEAM].facts.sample_period]; STEAM (STEAM) fraction_denominator = "blowdown / steam" [units[STEAM].facts.fraction_denominator]; STEAM (STEAM) blowdown_rate = 6 [units[STEAM].facts.blowdown_rate]; STEAM (STEAM) record_source = "Fictional explicit original record, no company approval" [units[STEAM].facts.record_source]; STEAM (STEAM) record_revision = "R1" [units[STEAM].facts.record_revision]; STEAM (STEAM) source_is_fictional = true [units[STEAM].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

### E13: What do existing records establish about this boiler's blowdown function, water-treatment control and any remaining heat-recovery opportunity?

**About:** FEED  

**Finding reference (JSON string):** `"E13@FEED"`
**Asset IDs (JSON array):** `["FEED", "HV-AX-2"]`

**Evidence on the drawing / model**

- equipment FEED reads "FEED boiler feedwater-denominator record" (`units[FEED]`)
- Blowdown: hand valve HV-AX-2 reads "HV-AX-2 Declared blowdown candidate" at FEED (`manual_valves[HV-AX-2]`)
- Supplied candidate field: `"FEED water_service = \"declared steam-water boiler\"; present; meaning and suitability unverified"` (`"units[FEED].facts.water_service"`)
- Supplied candidate field: `"FEED blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[FEED].facts.blowdown_function"`)
- Supplied candidate field: `"FEED quantity_units = \"lb/h\"; present; meaning and suitability unverified"` (`"units[FEED].facts.quantity_units"`)
- Supplied candidate field: `"FEED sample_period = \"fictional interval A\"; present; meaning and suitability unverified"` (`"units[FEED].facts.sample_period"`)
- Supplied candidate field: `"FEED fraction_denominator = \"blowdown / feedwater\"; present; meaning and suitability unverified"` (`"units[FEED].facts.fraction_denominator"`)
- Supplied candidate field: `"FEED blowdown_rate = 6; present; meaning and suitability unverified"` (`"units[FEED].facts.blowdown_rate"`)
- Supplied candidate field: `"FEED receiving_duty = \"qualified existing recovery record, not acceptance\"; present; meaning and suitability unverified"` (`"units[FEED].facts.receiving_duty"`)
- Supplied candidate field: `"FEED record_source = \"Fictional explicit original record, no company approval\"; present; meaning and suitability unverified"` (`"units[FEED].facts.record_source"`)
- Supplied candidate field: `"FEED record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[FEED].facts.record_revision"`)
- Supplied candidate field: `"FEED source_is_fictional = true; present; meaning and suitability unverified"` (`"units[FEED].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: FEED water_service = declared steam-water boiler (`units[FEED].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: FEED blowdown_function = surface (`units[FEED].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: FEED quantity_units = lb/h (`units[FEED].facts.quantity_units`)
- On drawing: Supplied candidate fact, basis unverified: FEED sample_period = fictional interval A (`units[FEED].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: FEED fraction_denominator = blowdown / feedwater (`units[FEED].facts.fraction_denominator`)
- On drawing: Supplied candidate fact, basis unverified: FEED blowdown_rate = 6 (`units[FEED].facts.blowdown_rate`)
- On drawing: Supplied candidate fact, basis unverified: FEED receiving_duty = qualified existing recovery record, not acceptance (`units[FEED].facts.receiving_duty`)
- On drawing: Supplied candidate fact, basis unverified: FEED record_source = Fictional explicit original record, no company approval (`units[FEED].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FEED record_revision = R1 (`units[FEED].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FEED source_is_fictional = True (`units[FEED].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): FEED (FEED) water_service = "declared steam-water boiler" [units[FEED].facts.water_service]; FEED (FEED) blowdown_function = "surface" [units[FEED].facts.blowdown_function]; FEED (FEED) quantity_units = "lb/h" [units[FEED].facts.quantity_units]; FEED (FEED) sample_period = "fictional interval A" [units[FEED].facts.sample_period]; FEED (FEED) fraction_denominator = "blowdown / feedwater" [units[FEED].facts.fraction_denominator]; FEED (FEED) blowdown_rate = 6 [units[FEED].facts.blowdown_rate]; FEED (FEED) receiving_duty = "qualified existing recovery record, not acceptance" [units[FEED].facts.receiving_duty]; FEED (FEED) record_source = "Fictional explicit original record, no company approval" [units[FEED].facts.record_source]; FEED (FEED) record_revision = "R1" [units[FEED].facts.record_revision]; FEED (FEED) source_is_fictional = true [units[FEED].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

## Sources cited above

- S5: Steam Tip #9, Minimize Boiler Blowdown (DOE/GO-102012-3406). https://www.energy.gov/sites/prod/files/2014/05/f16/steam9_blowdown.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
