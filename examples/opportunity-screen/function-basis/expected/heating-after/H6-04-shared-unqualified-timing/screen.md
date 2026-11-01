# Opportunity screen: ILLUSTRATIVE source-informed exhaust recovery development case

Model: `examples/opportunity-screen/function-basis/models/H6-04-shared-unqualified-timing.json`. Questions: `data/questions.json`.

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
| Heat grade (high-grade heat for low-grade duty) | 2 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Heat grade (high-grade heat for low-grade duty)

### H6: What do existing records establish about this oven, dryer or fryer recovery already provided and any unresolved residual supply for the named external heating-duty lead?

**About:** D-A  

**Finding reference (JSON string):** `"H6@D-A"`
**Asset IDs (JSON array):** `["D-A", "W-1", "stream:EX-A", "HX-S"]`

**Evidence on the drawing / model**

- equipment D-A reads "D-A Product dryer A" (`units[D-A]`)
- Low-grade heating duty: equipment W-1 reads "W-1 Facility wash hot water" (`units[W-1]`)
- Exhaust: stream EX-A (asset stream:EX-A) reads "Dryer A exhaust" (`streams[EX-A]`)
- Represented recovery candidate: equipment HX-S reads "HX-S Exhaust heat recovery exchanger" (`units[HX-S]`)
- Supplied candidate field: `"D-A exhaust_temperature_C = 110; present; meaning and suitability unverified"` (`"units[D-A].facts.exhaust_temperature_C"`)
- Supplied candidate field: `"D-A operating_window = \"night\"; present; meaning and suitability unverified"` (`"units[D-A].facts.operating_window"`)
- Supplied candidate field: `"W-1 required_temperature_C = 50; present; meaning and suitability unverified"` (`"units[W-1].facts.required_temperature_C"`)
- Supplied candidate field: `"W-1 duty_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"units[W-1].facts.duty_basis"`)
- Supplied candidate field: `"W-1 coincident_demand = \"unknown\"; blank; meaning and suitability unverified"` (`"units[W-1].facts.coincident_demand"`)
- Supplied candidate field: `"W-1 operating_window = \"day\"; present; meaning and suitability unverified"` (`"units[W-1].facts.operating_window"`)
- Supplied candidate field: `"W-1 alternative_heat_supply = \"existing steam supply; comparative basis unknown\"; present; meaning and suitability unverified"` (`"units[W-1].facts.alternative_heat_supply"`)
- Supplied candidate field: `"HX-S enabled = true; present; meaning and suitability unverified"` (`"units[HX-S].facts.enabled"`)
- Supplied candidate field: `"HX-S source_revision = \"C\"; present; meaning and suitability unverified"` (`"units[HX-S].facts.source_revision"`)
- Supplied candidate field: `"HX-S coverage_claim = {\"D-A\": \"unknown\", \"D-B\": \"unknown\"}; present; meaning and suitability unverified"` (`"units[HX-S].facts.coverage_claim"`)
- Supplied candidate field: `"HX-S gas_compatibility = \"corrosive/particulates unresolved\"; present; meaning and suitability unverified"` (`"units[HX-S].facts.gas_compatibility"`)
- Supplied candidate field: `"HX-S pressure_loss_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"units[HX-S].facts.pressure_loss_basis"`)

**Data to collect**

- Existing source routing, recovery-purpose and residual-supply basis [not on drawing]. Where: site records: approved existing exhaust routing, current recovery purpose, source revision/locator and coverage/bypass/availability records for this identified source; then maintenance records: existing recovery operation, cleaning, fouling and unavailable/disabled records with equipment and period identity. How: Separate own-inlet recovery from external-duty coverage. Retain full, partial, shared, zero and unknown claims literally; a recoverer label or nominal temperature does not establish actual residual transferable heat or allocate shared duty.
- Existing named-duty requirements and source/demand quantity and timing basis [not on drawing]. Where: site records: approved existing identity/purpose, temperature, heat-demand and operating schedules for the named duty, paired with source-period records where available, including quantities, locations, units, dates and responsible owners. How: The anywhere-found duty is an unassociated lead, not a physical connection, nearby user or suitable sink. Review amount, thermal suitability and timing separately. A pair of nominal temperatures, common name or schedule mismatch does not by itself settle all practical alternatives or establish viability.
- Existing route, compatibility and alternative-heat constraints [not on drawing]. Where: site records: existing layout/distance and transport options; cleanliness/corrosion/particulate compatibility; condensation and pressure-loss/ventilation constraints; and the available alternative heating-supply and comparative basis; then the vendor datasheet: applicable documented source and receiving-equipment limits, prior assessments and the qualified engineering review route. How: Use the source/sink questions in S28 to identify what existing evidence supports or leaves unresolved. No universal temperature-difference threshold, mandatory field task, fixed sampling period or cost ranking is imposed. Qualified owners decide any further data plan and whether a study should proceed, be answered or be deferred.

**How it is decided:** Review actual residual supply, named-duty amount/thermal requirements and coincident timing together with route losses, compatibility, condensation, pressure resistance and alternative heating basis. Distinguish documented working full coverage from unresolved partial, disabled, shared or internal-only recovery. A qualified company review can answer or defer the question from existing records; unknown evidence is not an automatic otherwise-close result, a feasible project or a mandate for a new project.

**What the source says (S28, S26):** S28 (p. 1): "many companies install heat exchangers on the exhaust stacks of furnaces and ovens to produce hot water or to generate hot air for space heating." The same sheet: "The temperature difference between the primary and secondary process should be high enough (at least 200°F), and there should be a sufficient amount of usable waste heat." Fryers (S26, p. 107): "Heat can be recovered indirectly from a fryer's fat-laden exhaust gases via a heat exchange system and used for pre-heating air and water for use in other facility processes." No % stated.

**Limits:** E31 addresses own-inlet/process-use recovery; it does not establish H6 external residual or duty coverage. The unchanged with-clause requires a named external duty somewhere in the model, not a nearby or connected sink. A supplied fully-covered working external claim may be quiet in new-opportunity triage; when shown here, its literal existing coverage and unverified basis must be acknowledged. The source-informed records-review policy does not impose a universal 200-degree threshold or authenticate supplied claims. Company engineering and safety/quality review govern feasibility and any actual work.

### H6: What do existing records establish about this oven, dryer or fryer recovery already provided and any unresolved residual supply for the named external heating-duty lead?

**About:** D-B  

**Finding reference (JSON string):** `"H6@D-B"`
**Asset IDs (JSON array):** `["D-B", "W-1", "stream:EX-B", "HX-S"]`

**Evidence on the drawing / model**

- equipment D-B reads "D-B Product dryer B" (`units[D-B]`)
- Low-grade heating duty: equipment W-1 reads "W-1 Facility wash hot water" (`units[W-1]`)
- Exhaust: stream EX-B (asset stream:EX-B) reads "Dryer B exhaust" (`streams[EX-B]`)
- Represented recovery candidate: equipment HX-S reads "HX-S Exhaust heat recovery exchanger" (`units[HX-S]`)
- Supplied candidate field: `"W-1 required_temperature_C = 50; present; meaning and suitability unverified"` (`"units[W-1].facts.required_temperature_C"`)
- Supplied candidate field: `"W-1 duty_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"units[W-1].facts.duty_basis"`)
- Supplied candidate field: `"W-1 coincident_demand = \"unknown\"; blank; meaning and suitability unverified"` (`"units[W-1].facts.coincident_demand"`)
- Supplied candidate field: `"W-1 operating_window = \"day\"; present; meaning and suitability unverified"` (`"units[W-1].facts.operating_window"`)
- Supplied candidate field: `"W-1 alternative_heat_supply = \"existing steam supply; comparative basis unknown\"; present; meaning and suitability unverified"` (`"units[W-1].facts.alternative_heat_supply"`)
- Supplied candidate field: `"HX-S enabled = true; present; meaning and suitability unverified"` (`"units[HX-S].facts.enabled"`)
- Supplied candidate field: `"HX-S source_revision = \"C\"; present; meaning and suitability unverified"` (`"units[HX-S].facts.source_revision"`)
- Supplied candidate field: `"HX-S coverage_claim = {\"D-A\": \"unknown\", \"D-B\": \"unknown\"}; present; meaning and suitability unverified"` (`"units[HX-S].facts.coverage_claim"`)
- Supplied candidate field: `"HX-S gas_compatibility = \"corrosive/particulates unresolved\"; present; meaning and suitability unverified"` (`"units[HX-S].facts.gas_compatibility"`)
- Supplied candidate field: `"HX-S pressure_loss_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"units[HX-S].facts.pressure_loss_basis"`)

**Data to collect**

- Existing source routing, recovery-purpose and residual-supply basis [not on drawing]. Where: site records: approved existing exhaust routing, current recovery purpose, source revision/locator and coverage/bypass/availability records for this identified source; then maintenance records: existing recovery operation, cleaning, fouling and unavailable/disabled records with equipment and period identity. How: Separate own-inlet recovery from external-duty coverage. Retain full, partial, shared, zero and unknown claims literally; a recoverer label or nominal temperature does not establish actual residual transferable heat or allocate shared duty.
- Existing named-duty requirements and source/demand quantity and timing basis [not on drawing]. Where: site records: approved existing identity/purpose, temperature, heat-demand and operating schedules for the named duty, paired with source-period records where available, including quantities, locations, units, dates and responsible owners. How: The anywhere-found duty is an unassociated lead, not a physical connection, nearby user or suitable sink. Review amount, thermal suitability and timing separately. A pair of nominal temperatures, common name or schedule mismatch does not by itself settle all practical alternatives or establish viability.
- Existing route, compatibility and alternative-heat constraints [not on drawing]. Where: site records: existing layout/distance and transport options; cleanliness/corrosion/particulate compatibility; condensation and pressure-loss/ventilation constraints; and the available alternative heating-supply and comparative basis; then the vendor datasheet: applicable documented source and receiving-equipment limits, prior assessments and the qualified engineering review route. How: Use the source/sink questions in S28 to identify what existing evidence supports or leaves unresolved. No universal temperature-difference threshold, mandatory field task, fixed sampling period or cost ranking is imposed. Qualified owners decide any further data plan and whether a study should proceed, be answered or be deferred.

**How it is decided:** Review actual residual supply, named-duty amount/thermal requirements and coincident timing together with route losses, compatibility, condensation, pressure resistance and alternative heating basis. Distinguish documented working full coverage from unresolved partial, disabled, shared or internal-only recovery. A qualified company review can answer or defer the question from existing records; unknown evidence is not an automatic otherwise-close result, a feasible project or a mandate for a new project.

**What the source says (S28, S26):** S28 (p. 1): "many companies install heat exchangers on the exhaust stacks of furnaces and ovens to produce hot water or to generate hot air for space heating." The same sheet: "The temperature difference between the primary and secondary process should be high enough (at least 200°F), and there should be a sufficient amount of usable waste heat." Fryers (S26, p. 107): "Heat can be recovered indirectly from a fryer's fat-laden exhaust gases via a heat exchange system and used for pre-heating air and water for use in other facility processes." No % stated.

**Limits:** E31 addresses own-inlet/process-use recovery; it does not establish H6 external residual or duty coverage. The unchanged with-clause requires a named external duty somewhere in the model, not a nearby or connected sink. A supplied fully-covered working external claim may be quiet in new-opportunity triage; when shown here, its literal existing coverage and unverified basis must be acknowledged. The source-informed records-review policy does not impose a universal 200-degree threshold or authenticate supplied claims. Company engineering and safety/quality review govern feasibility and any actual work.

## Sources cited above

- S26: Masanet, Worrell, Graus and Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for the Fruit and Vegetable Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-59289-Revision, Mar 2008). https://eta-publications.lbl.gov/sites/default/files/lbnl-59289-rev.pdf (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
- S28: DOE Industrial Technologies Program, Process Heating Tip Sheet #10, Using Waste Heat for External Processes (DOE/GO-102006-2225, Jan 2006). https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/38853.pdf (license: Public domain (US federal))
