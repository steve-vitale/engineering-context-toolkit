# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/source-policy/models/E7-01-screening-thresholds.json`. Questions: `data/questions.json`.

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

### E7: What do existing records establish about this header-letdown candidate's steam service and any backpressure-generation feasibility question?

**About:** PCV-A  

**Finding reference (JSON string):** `"E7@PCV-A"`
**Asset IDs (JSON array):** `["PCV-A"]`

**Evidence on the drawing / model**

- Trigger: `"valve PCV-A reads \"PCV-A Steam PRV HP HEADER to LP HEADER\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"PCV-A\", \"kind\": \"final_element\", \"unit\": null, \"source\": \"Fictional candidate station, not installed-state proof\", \"assigned_tag\": true, \"unplaced_reason\": \"Fictional explicitly unplaced station; no inventoried equipment owner\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[PCV-A]"`)
- Supplied candidate field: `"PCV-A fictional_record = true; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.fictional_record"`)
- Supplied candidate field: `"PCV-A record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.record_source"`)
- Supplied candidate field: `"PCV-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.record_revision"`)
- Supplied candidate field: `"PCV-A record_available = true; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.record_available"`)
- Supplied candidate field: `"PCV-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.record_authority"`)
- Supplied candidate field: `"PCV-A service = \"steam\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.service"`)
- Supplied candidate field: `"PCV-A station_flow = 3000; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.station_flow"`)
- Supplied candidate field: `"PCV-A flow_unit = \"lb/hr\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.flow_unit"`)
- Supplied candidate field: `"PCV-A inlet_pressure = 200; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.inlet_pressure"`)
- Supplied candidate field: `"PCV-A outlet_pressure = 100; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.outlet_pressure"`)
- Supplied candidate field: `"PCV-A pressure_unit = \"psig\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.pressure_unit"`)
- Supplied candidate field: `"PCV-A duty = \"constant sourceassertion, notverified\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.duty"`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A fictional_record = True (`unplaced[PCV-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_source = Fictional development packet; no plant or human approval (`unplaced[PCV-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_revision = R1 (`unplaced[PCV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_available = True (`unplaced[PCV-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_authority = unverified (`unplaced[PCV-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A service = steam (`unplaced[PCV-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A station_flow = 3000 (`unplaced[PCV-A].facts.station_flow`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A flow_unit = lb/hr (`unplaced[PCV-A].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A inlet_pressure = 200 (`unplaced[PCV-A].facts.inlet_pressure`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A outlet_pressure = 100 (`unplaced[PCV-A].facts.outlet_pressure`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A pressure_unit = psig (`unplaced[PCV-A].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A duty = constant sourceassertion, notverified (`unplaced[PCV-A].facts.duty`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A fictional_record = True (`unplaced[PCV-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_source = Fictional development packet; no plant or human approval (`unplaced[PCV-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_revision = R1 (`unplaced[PCV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_available = True (`unplaced[PCV-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_authority = unverified (`unplaced[PCV-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A service = steam (`unplaced[PCV-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A station_flow = 3000 (`unplaced[PCV-A].facts.station_flow`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A flow_unit = lb/hr (`unplaced[PCV-A].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A inlet_pressure = 200 (`unplaced[PCV-A].facts.inlet_pressure`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A outlet_pressure = 100 (`unplaced[PCV-A].facts.outlet_pressure`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A pressure_unit = psig (`unplaced[PCV-A].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A duty = constant sourceassertion, notverified (`unplaced[PCV-A].facts.duty`)

**Data to collect**

- Existing station service, steam balance and flow-duration records [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PCV-A (PCV-A) fictional_record = true [unplaced[PCV-A].facts.fictional_record]; PCV-A (PCV-A) record_source = "Fictional development packet; no plant or human approval" [unplaced[PCV-A].facts.record_source]; PCV-A (PCV-A) record_revision = "R1" [unplaced[PCV-A].facts.record_revision]; PCV-A (PCV-A) record_available = true [unplaced[PCV-A].facts.record_available]; PCV-A (PCV-A) record_authority = "unverified" [unplaced[PCV-A].facts.record_authority]; PCV-A (PCV-A) service = "steam" [unplaced[PCV-A].facts.service]; PCV-A (PCV-A) station_flow = 3000 [unplaced[PCV-A].facts.station_flow]; PCV-A (PCV-A) flow_unit = "lb/hr" [unplaced[PCV-A].facts.flow_unit]; PCV-A (PCV-A) inlet_pressure = 200 [unplaced[PCV-A].facts.inlet_pressure]; PCV-A (PCV-A) outlet_pressure = 100 [unplaced[PCV-A].facts.outlet_pressure]; PCV-A (PCV-A) pressure_unit = "psig" [unplaced[PCV-A].facts.pressure_unit]; PCV-A (PCV-A) duty = "constant sourceassertion, notverified" [unplaced[PCV-A].facts.duty]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-station service and current steam balance, actual flow-duration/operating coverage and represented PRV/turbine arrangement; exact source/revision, quantity units, sample period and availability.; then only a valve (PCV-A) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Establish steam service first: a PRV/PCV or HP/MP/LP/header label alone does not prove steam or two-sided physical topology. Known nonsteam service is not applicable to this steam-turbine question; acknowledge that without a compulsory steam measurement. Missing/unknown data remains qualified. Review existing suitable function before proposing further study.
- Existing actual pressure/thermal, boiler, electrical and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PCV-A (PCV-A) fictional_record = true [unplaced[PCV-A].facts.fictional_record]; PCV-A (PCV-A) record_source = "Fictional development packet; no plant or human approval" [unplaced[PCV-A].facts.record_source]; PCV-A (PCV-A) record_revision = "R1" [unplaced[PCV-A].facts.record_revision]; PCV-A (PCV-A) record_available = true [unplaced[PCV-A].facts.record_available]; PCV-A (PCV-A) record_authority = "unverified" [unplaced[PCV-A].facts.record_authority]; PCV-A (PCV-A) service = "steam" [unplaced[PCV-A].facts.service]; PCV-A (PCV-A) station_flow = 3000 [unplaced[PCV-A].facts.station_flow]; PCV-A (PCV-A) flow_unit = "lb/hr" [unplaced[PCV-A].facts.flow_unit]; PCV-A (PCV-A) inlet_pressure = 200 [unplaced[PCV-A].facts.inlet_pressure]; PCV-A (PCV-A) outlet_pressure = 100 [unplaced[PCV-A].facts.outlet_pressure]; PCV-A (PCV-A) pressure_unit = "psig" [unplaced[PCV-A].facts.pressure_unit]; PCV-A (PCV-A) duty = "constant sourceassertion, notverified" [unplaced[PCV-A].facts.duty]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual inlet/exhaust pressures and steam condition, process heat requirements, boiler-throughput/capacity implications, annual duty, fuel/electricity/voltage and practical/economic constraints; distinguish design ratings from operating records.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: The DOE Tip20 source screening figures (3000lb/hr and100psi) describe when to consider further study in its stated context, not automatic install/close thresholds. Do not close an unresolved investigation because data are variable, below an example, unconverted or absent. A backpressure turbine is generally considered in parallel with a PRV and removes energy needed downstream; source prices, graph assumptions/efficiencies and installation percentages are historical examples, not current site savings. Acknowledge an existing suitable function without new measurements or replacement.

**How it is decided:** Review actual named-station steam service, current balance/flow-duration, process pressure/heat, boiler, electrical and economic constraints before any backpressure-generation feasibility decision. Do not install a turbine or automatically close an unresolved investigation from source thresholds, design pressures or a label alone. Known nonsteam scope can be acknowledged as not applicable; unknown source, association or operating basis remains explicit. No site benefit or operating authorization is calculated.

**What the source says (S6):** Consider when a PRV has "constant steam flows of at least 3,000 pounds per hour (lb/hr), and when the steam pressure drop is at least 100 psi." Installation costs "typically average 75% of equipment costs".

**Limits:** S6 also quotes cost per kW figures; they are deliberately not repeated here. No IAC code maps to turbines (2.2134 covers PRV-station leaks). Source review: complete S6 pp1–2 includes current steam balance/actual process requirements, parallel arrangement, downstream heat/boiler-throughput implications and historical calculation assumptions. Inherited source threshold/cost quotation is not a universal cutoff, present-day quotation or engineering approval.

### E7: What do existing records establish about this header-letdown candidate's steam service and any backpressure-generation feasibility question?

**About:** PCV-B  

**Finding reference (JSON string):** `"E7@PCV-B"`
**Asset IDs (JSON array):** `["PCV-B"]`

**Evidence on the drawing / model**

- Trigger: `"valve PCV-B reads \"PCV-B Steam PRV HP HEADER to LP HEADER\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"PCV-B\", \"kind\": \"final_element\", \"unit\": null, \"source\": \"Fictional candidate station, not installed-state proof\", \"assigned_tag\": true, \"unplaced_reason\": \"Fictional explicitly unplaced station; no inventoried equipment owner\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[PCV-B]"`)
- Supplied candidate field: `"PCV-B fictional_record = true; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.fictional_record"`)
- Supplied candidate field: `"PCV-B record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.record_source"`)
- Supplied candidate field: `"PCV-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.record_revision"`)
- Supplied candidate field: `"PCV-B record_available = true; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.record_available"`)
- Supplied candidate field: `"PCV-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.record_authority"`)
- Supplied candidate field: `"PCV-B service = \"steam\"; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.service"`)
- Supplied candidate field: `"PCV-B station_flow = 2500; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.station_flow"`)
- Supplied candidate field: `"PCV-B flow_unit = \"lb/hr\"; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.flow_unit"`)
- Supplied candidate field: `"PCV-B inlet_pressure = 180; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.inlet_pressure"`)
- Supplied candidate field: `"PCV-B outlet_pressure = 100; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.outlet_pressure"`)
- Supplied candidate field: `"PCV-B pressure_unit = \"psig\"; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.pressure_unit"`)
- Supplied candidate field: `"PCV-B duty = \"variableduty, incompleteperiod\"; present; meaning and suitability unverified"` (`"unplaced[PCV-B].facts.duty"`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B fictional_record = True (`unplaced[PCV-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B record_source = Fictional development packet; no plant or human approval (`unplaced[PCV-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B record_revision = R1 (`unplaced[PCV-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B record_available = True (`unplaced[PCV-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B record_authority = unverified (`unplaced[PCV-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B service = steam (`unplaced[PCV-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B station_flow = 2500 (`unplaced[PCV-B].facts.station_flow`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B flow_unit = lb/hr (`unplaced[PCV-B].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B inlet_pressure = 180 (`unplaced[PCV-B].facts.inlet_pressure`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B outlet_pressure = 100 (`unplaced[PCV-B].facts.outlet_pressure`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B pressure_unit = psig (`unplaced[PCV-B].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B duty = variableduty, incompleteperiod (`unplaced[PCV-B].facts.duty`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B fictional_record = True (`unplaced[PCV-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B record_source = Fictional development packet; no plant or human approval (`unplaced[PCV-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B record_revision = R1 (`unplaced[PCV-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B record_available = True (`unplaced[PCV-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B record_authority = unverified (`unplaced[PCV-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B service = steam (`unplaced[PCV-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B station_flow = 2500 (`unplaced[PCV-B].facts.station_flow`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B flow_unit = lb/hr (`unplaced[PCV-B].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B inlet_pressure = 180 (`unplaced[PCV-B].facts.inlet_pressure`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B outlet_pressure = 100 (`unplaced[PCV-B].facts.outlet_pressure`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B pressure_unit = psig (`unplaced[PCV-B].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: PCV-B duty = variableduty, incompleteperiod (`unplaced[PCV-B].facts.duty`)

**Data to collect**

- Existing station service, steam balance and flow-duration records [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PCV-B (PCV-B) fictional_record = true [unplaced[PCV-B].facts.fictional_record]; PCV-B (PCV-B) record_source = "Fictional development packet; no plant or human approval" [unplaced[PCV-B].facts.record_source]; PCV-B (PCV-B) record_revision = "R1" [unplaced[PCV-B].facts.record_revision]; PCV-B (PCV-B) record_available = true [unplaced[PCV-B].facts.record_available]; PCV-B (PCV-B) record_authority = "unverified" [unplaced[PCV-B].facts.record_authority]; PCV-B (PCV-B) service = "steam" [unplaced[PCV-B].facts.service]; PCV-B (PCV-B) station_flow = 2500 [unplaced[PCV-B].facts.station_flow]; PCV-B (PCV-B) flow_unit = "lb/hr" [unplaced[PCV-B].facts.flow_unit]; PCV-B (PCV-B) inlet_pressure = 180 [unplaced[PCV-B].facts.inlet_pressure]; PCV-B (PCV-B) outlet_pressure = 100 [unplaced[PCV-B].facts.outlet_pressure]; PCV-B (PCV-B) pressure_unit = "psig" [unplaced[PCV-B].facts.pressure_unit]; PCV-B (PCV-B) duty = "variableduty, incompleteperiod" [unplaced[PCV-B].facts.duty]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-station service and current steam balance, actual flow-duration/operating coverage and represented PRV/turbine arrangement; exact source/revision, quantity units, sample period and availability.; then only a valve (PCV-B) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Establish steam service first: a PRV/PCV or HP/MP/LP/header label alone does not prove steam or two-sided physical topology. Known nonsteam service is not applicable to this steam-turbine question; acknowledge that without a compulsory steam measurement. Missing/unknown data remains qualified. Review existing suitable function before proposing further study.
- Existing actual pressure/thermal, boiler, electrical and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PCV-B (PCV-B) fictional_record = true [unplaced[PCV-B].facts.fictional_record]; PCV-B (PCV-B) record_source = "Fictional development packet; no plant or human approval" [unplaced[PCV-B].facts.record_source]; PCV-B (PCV-B) record_revision = "R1" [unplaced[PCV-B].facts.record_revision]; PCV-B (PCV-B) record_available = true [unplaced[PCV-B].facts.record_available]; PCV-B (PCV-B) record_authority = "unverified" [unplaced[PCV-B].facts.record_authority]; PCV-B (PCV-B) service = "steam" [unplaced[PCV-B].facts.service]; PCV-B (PCV-B) station_flow = 2500 [unplaced[PCV-B].facts.station_flow]; PCV-B (PCV-B) flow_unit = "lb/hr" [unplaced[PCV-B].facts.flow_unit]; PCV-B (PCV-B) inlet_pressure = 180 [unplaced[PCV-B].facts.inlet_pressure]; PCV-B (PCV-B) outlet_pressure = 100 [unplaced[PCV-B].facts.outlet_pressure]; PCV-B (PCV-B) pressure_unit = "psig" [unplaced[PCV-B].facts.pressure_unit]; PCV-B (PCV-B) duty = "variableduty, incompleteperiod" [unplaced[PCV-B].facts.duty]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual inlet/exhaust pressures and steam condition, process heat requirements, boiler-throughput/capacity implications, annual duty, fuel/electricity/voltage and practical/economic constraints; distinguish design ratings from operating records.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: The DOE Tip20 source screening figures (3000lb/hr and100psi) describe when to consider further study in its stated context, not automatic install/close thresholds. Do not close an unresolved investigation because data are variable, below an example, unconverted or absent. A backpressure turbine is generally considered in parallel with a PRV and removes energy needed downstream; source prices, graph assumptions/efficiencies and installation percentages are historical examples, not current site savings. Acknowledge an existing suitable function without new measurements or replacement.

**How it is decided:** Review actual named-station steam service, current balance/flow-duration, process pressure/heat, boiler, electrical and economic constraints before any backpressure-generation feasibility decision. Do not install a turbine or automatically close an unresolved investigation from source thresholds, design pressures or a label alone. Known nonsteam scope can be acknowledged as not applicable; unknown source, association or operating basis remains explicit. No site benefit or operating authorization is calculated.

**What the source says (S6):** Consider when a PRV has "constant steam flows of at least 3,000 pounds per hour (lb/hr), and when the steam pressure drop is at least 100 psi." Installation costs "typically average 75% of equipment costs".

**Limits:** S6 also quotes cost per kW figures; they are deliberately not repeated here. No IAC code maps to turbines (2.2134 covers PRV-station leaks). Source review: complete S6 pp1–2 includes current steam balance/actual process requirements, parallel arrangement, downstream heat/boiler-throughput implications and historical calculation assumptions. Inherited source threshold/cost quotation is not a universal cutoff, present-day quotation or engineering approval.

## Sources cited above

- S6: Steam Tip #20, Replace Pressure-Reducing Valves with Backpressure Turbogenerators (DOE/GO-102012-3409). https://www.energy.gov/sites/prod/files/2014/05/f16/steam20_turbogenerators.pdf (license: Public domain)
