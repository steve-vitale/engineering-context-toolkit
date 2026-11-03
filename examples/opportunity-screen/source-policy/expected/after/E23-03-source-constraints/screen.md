# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/source-policy/models/E23-03-source-constraints.json`. Questions: `data/questions.json`.

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

### E23: What do existing records establish about this air-compressor candidate's actual heat availability, existing recovery and compatible receiving duty?

**About:** C-A  

**Finding reference (JSON string):** `"E23@C-A"`
**Asset IDs (JSON array):** `["C-A"]`

**Evidence on the drawing / model**

- equipment C-A reads "C-A AIR COMPRESSOR" (`units[C-A]`)
- Supplied candidate field: `"C-A fictional_record = true; present; meaning and suitability unverified"` (`"units[C-A].facts.fictional_record"`)
- Supplied candidate field: `"C-A record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_source"`)
- Supplied candidate field: `"C-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_revision"`)
- Supplied candidate field: `"C-A record_available = false; present; meaning and suitability unverified"` (`"units[C-A].facts.record_available"`)
- Supplied candidate field: `"C-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_authority"`)
- Supplied candidate field: `"C-A record_scope = \"foreignC-A\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_scope"`)
- Supplied candidate field: `"C-A service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[C-A].facts.service"`)
- Supplied candidate field: `"C-A existing_recovery = \"foreignrecord\"; present; meaning and suitability unverified"` (`"units[C-A].facts.existing_recovery"`)
- Supplied candidate field: `"C-A ventilation_backpressure = \"unassessed\"; present; meaning and suitability unverified"` (`"units[C-A].facts.ventilation_backpressure"`)
- Supplied candidate field: `"C-A cooling_constraint = \"mustretaincooling\"; present; meaning and suitability unverified"` (`"units[C-A].facts.cooling_constraint"`)
- Supplied candidate field: `"C-A water_quality = \"unknown\"; blank; meaning and suitability unverified"` (`"units[C-A].facts.water_quality"`)
- Supplied candidate field: `"C-A displaced_energy = \"unknown\"; blank; meaning and suitability unverified"` (`"units[C-A].facts.displaced_energy"`)
- On drawing: Supplied candidate fact, basis unverified: C-A fictional_record = True (`units[C-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_source = Fictional pre-call development record, no company or human approval (`units[C-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_revision = R1 (`units[C-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_available = False (`units[C-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_authority = unverified (`units[C-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_scope = foreignC-A (`units[C-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: C-A service = compressedair (`units[C-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: C-A existing_recovery = foreignrecord (`units[C-A].facts.existing_recovery`)
- On drawing: Supplied candidate fact, basis unverified: C-A ventilation_backpressure = unassessed (`units[C-A].facts.ventilation_backpressure`)
- On drawing: Supplied candidate fact, basis unverified: C-A cooling_constraint = mustretaincooling (`units[C-A].facts.cooling_constraint`)

**Data to collect**

- Existing compressor/cooling, recovery and receiving-duty basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): C-A (C-A) fictional_record = true [units[C-A].facts.fictional_record]; C-A (C-A) record_source = "Fictional pre-call development record, no company or human approval" [units[C-A].facts.record_source]; C-A (C-A) record_revision = "R1" [units[C-A].facts.record_revision]; C-A (C-A) record_available = false [units[C-A].facts.record_available]; C-A (C-A) record_authority = "unverified" [units[C-A].facts.record_authority]; C-A (C-A) record_scope = "foreignC-A" [units[C-A].facts.record_scope]; C-A (C-A) service = "compressedair" [units[C-A].facts.service]; C-A (C-A) existing_recovery = "foreignrecord" [units[C-A].facts.existing_recovery]; C-A (C-A) ventilation_backpressure = "unassessed" [units[C-A].facts.ventilation_backpressure]; C-A (C-A) cooling_constraint = "mustretaincooling" [units[C-A].facts.cooling_constraint]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor type/cooling arrangement and performance, available thermal quantity/temperature and load/run schedule, existing recovery/coverage and receiving heat duty/temperature/time/seasonality, displaced energy and quality/material/cooling/ventilation/backpressure/control constraints, with exact units/source/owner/revision/availability.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S11 printed58-59 describes heat fractions and different air-cooled/water-cooled arrangements. Electrical input converted to heat and a recovered fraction of available thermal energy are not electrical savings or a useful site duty. Establish compatible temperatures, coincident demand and source/configuration first; the source says this heat is usually insufficient for direct steam production. Nearby load or long hours alone is insufficient. Retain required compressor cooling, ventilation/backpressure, water-quality/material and control constraints and added fan/exchanger effects. Acknowledge suitable existing recovery or nonapplicability; missing coverage remains conditional rather than a forced field test or new exchanger.

**How it is decided:** Review actual compressor/cooling performance, existing recovery and useful receiving duty, temperature, timing and operating/material/control constraints with the responsible specialist. Do not infer feasibility, useful output or a required retrofit from proximity/run hours or source heat percentages. Suitable existing recovery or nonapplicability may be acknowledged; unresolved source, service, units or duty remains explicit. No heat-recovery design, steam promise or site savings is produced.

**What the source says (S11):** "As much as 80 to 93 percent of the electrical energy" becomes heat; recovery "anywhere from 50 to 90 percent of this".
IAC/ITAC recommendation code: 2.243x (by description).

**Limits:** Source review: S11 printed58-59/PDF63-64, full heat-recovery context. Its80-93% electrical-to-heat fraction and50-90% recovery of available thermal energy are contextual source figures, not electricity or site savings; compressor/cooling/design and compatible receiving duty matter. The worked example omits additional fan power and warns of exchanger effects. Actual energy displacement and ventilation/cooling/quality constraints require review.

### E23: What do existing records establish about this air-compressor candidate's actual heat availability, existing recovery and compatible receiving duty?

**About:** C-B  

**Finding reference (JSON string):** `"E23@C-B"`
**Asset IDs (JSON array):** `["C-B"]`

**Evidence on the drawing / model**

- equipment C-B reads "C-B AIR COMPRESSOR" (`units[C-B]`)
- Supplied candidate field: `"C-B fictional_record = true; present; meaning and suitability unverified"` (`"units[C-B].facts.fictional_record"`)
- Supplied candidate field: `"C-B record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_source"`)
- Supplied candidate field: `"C-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_revision"`)
- Supplied candidate field: `"C-B record_available = true; present; meaning and suitability unverified"` (`"units[C-B].facts.record_available"`)
- Supplied candidate field: `"C-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_authority"`)
- Supplied candidate field: `"C-B service = null; blank; meaning and suitability unverified"` (`"units[C-B].facts.service"`)
- Supplied candidate field: `"C-B compressor_type = null; blank; meaning and suitability unverified"` (`"units[C-B].facts.compressor_type"`)
- Supplied candidate field: `"C-B cooling_medium = null; blank; meaning and suitability unverified"` (`"units[C-B].facts.cooling_medium"`)
- Supplied candidate field: `"C-B heat_temperature = null; blank; meaning and suitability unverified"` (`"units[C-B].facts.heat_temperature"`)
- On drawing: Supplied candidate fact, basis unverified: C-B fictional_record = True (`units[C-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_source = Fictional pre-call development record, no company or human approval (`units[C-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_revision = R1 (`units[C-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_available = True (`units[C-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_authority = unverified (`units[C-B].facts.record_authority`)

**Data to collect**

- Existing compressor/cooling, recovery and receiving-duty basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): C-B (C-B) fictional_record = true [units[C-B].facts.fictional_record]; C-B (C-B) record_source = "Fictional pre-call development record, no company or human approval" [units[C-B].facts.record_source]; C-B (C-B) record_revision = "R1" [units[C-B].facts.record_revision]; C-B (C-B) record_available = true [units[C-B].facts.record_available]; C-B (C-B) record_authority = "unverified" [units[C-B].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor type/cooling arrangement and performance, available thermal quantity/temperature and load/run schedule, existing recovery/coverage and receiving heat duty/temperature/time/seasonality, displaced energy and quality/material/cooling/ventilation/backpressure/control constraints, with exact units/source/owner/revision/availability.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S11 printed58-59 describes heat fractions and different air-cooled/water-cooled arrangements. Electrical input converted to heat and a recovered fraction of available thermal energy are not electrical savings or a useful site duty. Establish compatible temperatures, coincident demand and source/configuration first; the source says this heat is usually insufficient for direct steam production. Nearby load or long hours alone is insufficient. Retain required compressor cooling, ventilation/backpressure, water-quality/material and control constraints and added fan/exchanger effects. Acknowledge suitable existing recovery or nonapplicability; missing coverage remains conditional rather than a forced field test or new exchanger.

**How it is decided:** Review actual compressor/cooling performance, existing recovery and useful receiving duty, temperature, timing and operating/material/control constraints with the responsible specialist. Do not infer feasibility, useful output or a required retrofit from proximity/run hours or source heat percentages. Suitable existing recovery or nonapplicability may be acknowledged; unresolved source, service, units or duty remains explicit. No heat-recovery design, steam promise or site savings is produced.

**What the source says (S11):** "As much as 80 to 93 percent of the electrical energy" becomes heat; recovery "anywhere from 50 to 90 percent of this".
IAC/ITAC recommendation code: 2.243x (by description).

**Limits:** Source review: S11 printed58-59/PDF63-64, full heat-recovery context. Its80-93% electrical-to-heat fraction and50-90% recovery of available thermal energy are contextual source figures, not electricity or site savings; compressor/cooling/design and compatible receiving duty matter. The worked example omits additional fan power and warns of exchanger effects. Actual energy displacement and ventilation/cooling/quality constraints require review.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
