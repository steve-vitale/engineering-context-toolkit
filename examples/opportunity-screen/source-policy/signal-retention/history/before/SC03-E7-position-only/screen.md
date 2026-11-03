# Opportunity screen: Fictional source-series locator control

Model: `examples/opportunity-screen/source-policy/signal-retention/models/SC03-E7-position-only.json`. Questions: `examples/opportunity-screen/source-policy/signal-retention/history/catalog-before.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 1 |
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

- Trigger: `"valve PCV-A reads \"PCV-A PRV HP HEADER letdown\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"PCV-A\", \"kind\": \"final_element\", \"unit\": null, \"source\": \"Fictional valve command pointer, not measured flow\", \"assigned_tag\": true, \"unplaced_reason\": \"Explicit fictional partial record; no inventoried owning equipment supplied\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[PCV-A]"`)
- Supplied candidate field: `"PCV-A fictional_record = true; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.fictional_record"`)
- Supplied candidate field: `"PCV-A record_source = \"Fictional signal-locator source note, Figure 11; no actual series or plant record\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.record_source"`)
- Supplied candidate field: `"PCV-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.record_revision"`)
- Supplied candidate field: `"PCV-A record_available = false; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.record_available"`)
- Supplied candidate field: `"PCV-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.record_authority"`)
- Supplied candidate field: `"PCV-A service = null; blank; meaning and suitability unverified"` (`"unplaced[PCV-A].facts.service"`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A fictional_record = True (`unplaced[PCV-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`unplaced[PCV-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_revision = R1 (`unplaced[PCV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_available = False (`unplaced[PCV-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_authority = unverified (`unplaced[PCV-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A fictional_record = True (`unplaced[PCV-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`unplaced[PCV-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_revision = R1 (`unplaced[PCV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_available = False (`unplaced[PCV-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PCV-A record_authority = unverified (`unplaced[PCV-A].facts.record_authority`)

**Data to collect**

- Existing station service, steam balance and flow-duration records [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PCV-A (PCV-A) fictional_record = true [unplaced[PCV-A].facts.fictional_record]; PCV-A (PCV-A) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [unplaced[PCV-A].facts.record_source]; PCV-A (PCV-A) record_revision = "R1" [unplaced[PCV-A].facts.record_revision]; PCV-A (PCV-A) record_available = false [unplaced[PCV-A].facts.record_available]; PCV-A (PCV-A) record_authority = "unverified" [unplaced[PCV-A].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-station service and current steam balance, actual flow-duration/operating coverage and represented PRV/turbine arrangement; exact source/revision, quantity units, sample period and availability.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Establish steam service first: a PRV/PCV or HP/MP/LP/header label alone does not prove steam or two-sided physical topology. Known nonsteam service is not applicable to this steam-turbine question; acknowledge that without a compulsory steam measurement. Missing/unknown data remains qualified. Review existing suitable function before proposing further study.
- Existing actual pressure/thermal, boiler, electrical and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PCV-A (PCV-A) fictional_record = true [unplaced[PCV-A].facts.fictional_record]; PCV-A (PCV-A) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [unplaced[PCV-A].facts.record_source]; PCV-A (PCV-A) record_revision = "R1" [unplaced[PCV-A].facts.record_revision]; PCV-A (PCV-A) record_available = false [unplaced[PCV-A].facts.record_available]; PCV-A (PCV-A) record_authority = "unverified" [unplaced[PCV-A].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual inlet/exhaust pressures and steam condition, process heat requirements, boiler-throughput/capacity implications, annual duty, fuel/electricity/voltage and practical/economic constraints; distinguish design ratings from operating records.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: The DOE Tip20 source screening figures (3000lb/hr and100psi) describe when to consider further study in its stated context, not automatic install/close thresholds. Do not close an unresolved investigation because data are variable, below an example, unconverted or absent. A backpressure turbine is generally considered in parallel with a PRV and removes energy needed downstream; source prices, graph assumptions/efficiencies and installation percentages are historical examples, not current site savings. Acknowledge an existing suitable function without new measurements or replacement.

**How it is decided:** Review actual named-station steam service, current balance/flow-duration, process pressure/heat, boiler, electrical and economic constraints before any backpressure-generation feasibility decision. Do not install a turbine or automatically close an unresolved investigation from source thresholds, design pressures or a label alone. Known nonsteam scope can be acknowledged as not applicable; unknown source, association or operating basis remains explicit. No site benefit or operating authorization is calculated.

**What the source says (S6):** Consider when a PRV has "constant steam flows of at least 3,000 pounds per hour (lb/hr), and when the steam pressure drop is at least 100 psi." Installation costs "typically average 75% of equipment costs".

**Limits:** S6 also quotes cost per kW figures; they are deliberately not repeated here. No IAC code maps to turbines (2.2134 covers PRV-station leaks). Source review: complete S6 pp1–2 includes current steam balance/actual process requirements, parallel arrangement, downstream heat/boiler-throughput implications and historical calculation assumptions. Inherited source threshold/cost quotation is not a universal cutoff, present-day quotation or engineering approval.

## Sources cited above

- S6: Steam Tip #20, Replace Pressure-Reducing Valves with Backpressure Turbogenerators (DOE/GO-102012-3409). https://www.energy.gov/sites/prod/files/2014/05/f16/steam20_turbogenerators.pdf (license: Public domain)
