# Opportunity screen: Fictional source-led C4/E24 control

Model: `examples/opportunity-screen/water-valve-records/models/CT-05-service-boundary.json`. Questions: `data/questions.json`.

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

### E24: What do existing records establish about this cooling-tower candidate's water service, chemistry-limited cycles, control and water balance?

**About:** UNKNOWN  

**Finding reference (JSON string):** `"E24@UNKNOWN"`
**Asset IDs (JSON array):** `["UNKNOWN"]`

**Evidence on the drawing / model**

- equipment UNKNOWN reads "UNKNOWN Fictional cooling tower service not established" (`units[UNKNOWN]`)
- Supplied candidate field: `"UNKNOWN fictional_record = true; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.fictional_record"`)
- Supplied candidate field: `"UNKNOWN record_source = \"Fictional training record, no plant or human approval\"; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.record_source"`)
- Supplied candidate field: `"UNKNOWN record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.record_revision"`)
- Supplied candidate field: `"UNKNOWN record_available = true; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.record_available"`)
- Supplied candidate field: `"UNKNOWN record_authority = \"not authenticated\"; present; meaning and suitability unverified"` (`"units[UNKNOWN].facts.record_authority"`)
- Supplied candidate field: `"UNKNOWN water_service = null; blank; meaning and suitability unverified"` (`"units[UNKNOWN].facts.water_service"`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN fictional_record = True (`units[UNKNOWN].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN record_source = Fictional training record, no plant or human approval (`units[UNKNOWN].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN record_revision = R1 (`units[UNKNOWN].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN record_available = True (`units[UNKNOWN].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: UNKNOWN record_authority = not authenticated (`units[UNKNOWN].facts.record_authority`)

**Data to collect**

- Existing tower-water service, treatment target, conductivity and makeup/blowdown balance records [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): UNKNOWN (UNKNOWN) fictional_record = true [units[UNKNOWN].facts.fictional_record]; UNKNOWN (UNKNOWN) record_source = "Fictional training record, no plant or human approval" [units[UNKNOWN].facts.record_source]; UNKNOWN (UNKNOWN) record_revision = "R1" [units[UNKNOWN].facts.record_revision]; UNKNOWN (UNKNOWN) record_available = true [units[UNKNOWN].facts.record_available]; UNKNOWN (UNKNOWN) record_authority = "not authenticated" [units[UNKNOWN].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named tower/system service and water-treatment logs, chemistry limits/target basis, conductivity and makeup/blowdown flow or volume records, installed control/meter function and loss/component records. Retain source/revision, actual subject association, units, calibration/availability, sample times and matching operating intervals.; then a walkdown: Only if existing records leave an applicable question unresolved: agree safe observations with the responsible water-treatment/engineering specialist. No compulsory new meter, measurement, chemical treatment or operating change.. How: Establish evaporative recirculating-water applicability first; known dry-only air-cooled service is not applicable and unknown service remains conditional. A nearby generic analyzer or meter label does not prove the water function, suitability or absence of other meters. For comparable quantities/units and matched periods, review conductivity/concentration ratio together with the makeup-to-blowdown flow/volume ratio, the treatment specialist's chemistry-limited target and operating coverage. Preserve conversions and uncertainty; raw incompatible quantities or periods cannot be divided as if comparable. Disagreement calls for records/component/loss review including leaks, overflow, drift or other draw-off, not an automatic higher target. Complete suitable existing records or a justified chemistry limit may be acknowledged without a new measurement/retrofit; source examplecycles are not site targets.

**How it is decided:** Review existing chemistry/treatment limits, matched water balance and conductivity evidence, installed functions and unresolved losses with the responsible specialist before any change. Do not raise cycles, install a controller/meter or alter treatment from a manual/no-analyzer pattern or a source example alone. Existing suitable control and chemistry-limited operation may be acknowledged. Unknown source, association, units or time coverage remains explicit; this screen is not a hardware decision or site saving.

**What the source says (S21, S24):** "Increasing cycles from three to six reduces cooling tower make-up water by 20% and cooling tower blowdown by 50%." Recommends a conductivity controller and makeup/blowdown flow meters. No energy % stated.
IAC/ITAC recommendation code: 2.2611 (IAC/ITAC browse page: 55 recommendations, 0.9 yr average payback, 45.7% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source-informed records review: S21 applies to evaporative tower-water management and requires chemistry-constrained targets, matched conductivity/flow logs and loss/component checks. Named instruments and filled fields are unverified candidates, not completion or source authority; inherited example benefits are not site savings.

## Sources cited above

- S21: DOE FEMP, Best Management Practice #10: Cooling Tower Management. https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
