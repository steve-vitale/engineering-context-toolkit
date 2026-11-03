# Opportunity screen: Fictional source-informed E13 controls; not a plant record

Model: `examples/opportunity-screen/water-valve-records/models/AX05-conflicting-service.json`. Questions: `data/questions.json`.

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

**About:** DRY  

**Finding reference (JSON string):** `"E13@DRY"`
**Asset IDs (JSON array):** `["DRY", "HV-AX-1"]`

**Evidence on the drawing / model**

- equipment DRY reads "DRY BOILER-labelled dry-service record" (`units[DRY]`)
- Blowdown: hand valve HV-AX-1 reads "HV-AX-1 Declared blowdown candidate" at DRY (`manual_valves[HV-AX-1]`)
- Supplied candidate field: `"DRY water_service = \"explicit dry/non-water process; boiler label conflicts with service record\"; present; meaning and suitability unverified"` (`"units[DRY].facts.water_service"`)
- Supplied candidate field: `"DRY blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[DRY].facts.blowdown_function"`)
- Supplied candidate field: `"DRY record_source = \"Fictional explicit original record, no company approval\"; present; meaning and suitability unverified"` (`"units[DRY].facts.record_source"`)
- Supplied candidate field: `"DRY record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[DRY].facts.record_revision"`)
- Supplied candidate field: `"DRY source_is_fictional = true; present; meaning and suitability unverified"` (`"units[DRY].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: DRY water_service = explicit dry/non-water process; boiler label conflicts with service record (`units[DRY].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: DRY blowdown_function = surface (`units[DRY].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: DRY record_source = Fictional explicit original record, no company approval (`units[DRY].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: DRY record_revision = R1 (`units[DRY].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: DRY source_is_fictional = True (`units[DRY].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): DRY (DRY) water_service = "explicit dry/non-water process; boiler label conflicts with service record" [units[DRY].facts.water_service]; DRY (DRY) blowdown_function = "surface" [units[DRY].facts.blowdown_function]; DRY (DRY) record_source = "Fictional explicit original record, no company approval" [units[DRY].facts.record_source]; DRY (DRY) record_revision = "R1" [units[DRY].facts.record_revision]; DRY (DRY) source_is_fictional = true [units[DRY].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

### E13: What do existing records establish about this boiler's blowdown function, water-treatment control and any remaining heat-recovery opportunity?

**About:** UNKNOWN  

**Finding reference (JSON string):** `"E13@UNKNOWN"`
**Asset IDs (JSON array):** `["UNKNOWN", "HV-AX-2"]`

**Evidence on the drawing / model**

- equipment UNKNOWN reads "UNKNOWN BOILER-labelled unknown service" (`units[UNKNOWN]`)
- Blowdown: hand valve HV-AX-2 reads "HV-AX-2 Declared blowdown candidate" at UNKNOWN (`manual_valves[HV-AX-2]`)
- Supplied candidate field: `"UNKNOWN water_service = \"unknown\"; blank; meaning and suitability unverified"` (`"units[UNKNOWN].facts.water_service"`)
- Supplied candidate field: `"UNKNOWN blowdown_function = \"surface\"; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.blowdown_function"`)
- Supplied candidate field: `"UNKNOWN record_source = \"Fictional explicit original record, no company approval\"; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.record_source"`)
- Supplied candidate field: `"UNKNOWN record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.record_revision"`)
- Supplied candidate field: `"UNKNOWN source_is_fictional = true; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.source_is_fictional"`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN blowdown_function = surface (`units[UNKNOWN].facts.blowdown_function`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN record_source = Fictional explicit original record, no company approval (`units[UNKNOWN].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN record_revision = R1 (`units[UNKNOWN].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN source_is_fictional = True (`units[UNKNOWN].facts.source_is_fictional`)

**Data to collect**

- Existing boiler blowdown service, treatment/control and recovery basis (qualified records first) [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): UNKNOWN (UNKNOWN) blowdown_function = "surface" [units[UNKNOWN].facts.blowdown_function]; UNKNOWN (UNKNOWN) record_source = "Fictional explicit original record, no company approval" [units[UNKNOWN].facts.record_source]; UNKNOWN (UNKNOWN) record_revision = "R1" [units[UNKNOWN].facts.record_revision]; UNKNOWN (UNKNOWN) source_is_fictional = true [units[UNKNOWN].facts.source_is_fictional]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Named boiler operating and water-treatment records: distinguish bottom/mud removal of suspended solids from surface/skimming removal of dissolved solids; retain asset/source/revision, sample time, availability, quantity/units and operating coverage. Review existing suitable control and recovery before requesting more data.; then a walkdown: Only if the relevant records cannot settle an applicable boiler-water question: agree with the responsible engineer what safe observation or measurement is still needed; no blanket new field measurement or hardware instruction.. How: First establish the actual steam/water service and bottom versus surface function. Normally manual intermittent bottom blowdown alone is not an automation fault. An analyzer tag or nearby location does not prove boiler-water association, suitable control or adequate operation. Keep TDS and conductivity units, representative sampling and feedwater/makeup/condensate distinctions explicit. Any calculated blowdown fraction or percent must state its justified balance, denominator and time basis; do not impose the source's contextual range as a target. For applicable continuous surface duty, review pressure, actual rate/hours, installed recovery, receiving duty and constraints before considering an investigation. Known dry/non-water service is not applicable; unknown service needs clarification. Complete suitable records can be acknowledged without a new measurement or retrofit. Proportional makeup-water-flow control can be an existing surface-control arrangement; absence of a conductivity probe alone is not a control defect. Keep steam-flow and feedwater-flow rate denominators distinct; neither a source screening sentence nor its worked table supplies a universal target.

**How it is decided:** Review records and unresolved applicability with the responsible engineer. Distinguish bottom/mud and surface/skimming functions; manual practice or a missing/generic analyzer does not authorize automation. Consider further control or heat-recovery investigation only if applicable service, treatment needs, actual operation and recovery/sink constraints establish a remaining question. No hardware decision, operating change, chemistry target or site saving follows from this screen.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** Source-informed records review: DOE Steam Tip 9, pp. 1–2, distinguishes bottom and surface functions and includes proportional makeup-water-flow control. Supplemental Tip 10, pp. 1–2 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam10_boiler_blowdown.pdf), qualifies recovery by actual source and receiving duty; its opening steam-rate screen and feedwater-based example have different denominators. Historical S19/S24/IAC benefit figures are inherited, not reverified, site-specific or current-standard acceptance. Supplied candidate fields do not establish engineering adequacy or source authority.

## Sources cited above

- S5: Steam Tip #9, Minimize Boiler Blowdown (DOE/GO-102012-3406). https://www.energy.gov/sites/prod/files/2014/05/f16/steam9_blowdown.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
