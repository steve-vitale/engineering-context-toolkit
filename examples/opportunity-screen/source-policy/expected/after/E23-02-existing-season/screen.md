# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/source-policy/models/E23-02-existing-season.json`. Questions: `data/questions.json`.

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
- Supplied candidate field: `"C-A record_available = true; present; meaning and suitability unverified"` (`"units[C-A].facts.record_available"`)
- Supplied candidate field: `"C-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_authority"`)
- Supplied candidate field: `"C-A service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[C-A].facts.service"`)
- Supplied candidate field: `"C-A heat_unit = \"kW\"; present; meaning and suitability unverified"` (`"units[C-A].facts.heat_unit"`)
- Supplied candidate field: `"C-A existing_recovery = \"suppliedspaceheating\"; present; meaning and suitability unverified"` (`"units[C-A].facts.existing_recovery"`)
- Supplied candidate field: `"C-A operating_schedule = \"summeronly\"; present; meaning and suitability unverified"` (`"units[C-A].facts.operating_schedule"`)
- Supplied candidate field: `"C-A receiver_schedule = \"winteronly\"; present; meaning and suitability unverified"` (`"units[C-A].facts.receiver_schedule"`)
- Supplied candidate field: `"C-A heat_duty = 10; present; meaning and suitability unverified"` (`"units[C-A].facts.heat_duty"`)
- Supplied candidate field: `"C-A bypass_control = \"suppliednotapproved\"; present; meaning and suitability unverified"` (`"units[C-A].facts.bypass_control"`)
- On drawing: Supplied candidate fact, basis unverified: C-A fictional_record = True (`units[C-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_source = Fictional pre-call development record, no company or human approval (`units[C-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_revision = R1 (`units[C-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_available = True (`units[C-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_authority = unverified (`units[C-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: C-A service = compressedair (`units[C-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: C-A heat_unit = kW (`units[C-A].facts.heat_unit`)
- On drawing: Supplied candidate fact, basis unverified: C-A existing_recovery = suppliedspaceheating (`units[C-A].facts.existing_recovery`)
- On drawing: Supplied candidate fact, basis unverified: C-A operating_schedule = summeronly (`units[C-A].facts.operating_schedule`)
- On drawing: Supplied candidate fact, basis unverified: C-A receiver_schedule = winteronly (`units[C-A].facts.receiver_schedule`)
- On drawing: Supplied candidate fact, basis unverified: C-A heat_duty = 10 (`units[C-A].facts.heat_duty`)
- On drawing: Supplied candidate fact, basis unverified: C-A bypass_control = suppliednotapproved (`units[C-A].facts.bypass_control`)

**Data to collect**

- Existing compressor/cooling, recovery and receiving-duty basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): C-A (C-A) fictional_record = true [units[C-A].facts.fictional_record]; C-A (C-A) record_source = "Fictional pre-call development record, no company or human approval" [units[C-A].facts.record_source]; C-A (C-A) record_revision = "R1" [units[C-A].facts.record_revision]; C-A (C-A) record_available = true [units[C-A].facts.record_available]; C-A (C-A) record_authority = "unverified" [units[C-A].facts.record_authority]; C-A (C-A) service = "compressedair" [units[C-A].facts.service]; C-A (C-A) heat_unit = "kW" [units[C-A].facts.heat_unit]; C-A (C-A) existing_recovery = "suppliedspaceheating" [units[C-A].facts.existing_recovery]; C-A (C-A) operating_schedule = "summeronly" [units[C-A].facts.operating_schedule]; C-A (C-A) receiver_schedule = "winteronly" [units[C-A].facts.receiver_schedule]; C-A (C-A) heat_duty = 10 [units[C-A].facts.heat_duty]; C-A (C-A) bypass_control = "suppliednotapproved" [units[C-A].facts.bypass_control]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor type/cooling arrangement and performance, available thermal quantity/temperature and load/run schedule, existing recovery/coverage and receiving heat duty/temperature/time/seasonality, displaced energy and quality/material/cooling/ventilation/backpressure/control constraints, with exact units/source/owner/revision/availability.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S11 printed58-59 describes heat fractions and different air-cooled/water-cooled arrangements. Electrical input converted to heat and a recovered fraction of available thermal energy are not electrical savings or a useful site duty. Establish compatible temperatures, coincident demand and source/configuration first; the source says this heat is usually insufficient for direct steam production. Nearby load or long hours alone is insufficient. Retain required compressor cooling, ventilation/backpressure, water-quality/material and control constraints and added fan/exchanger effects. Acknowledge suitable existing recovery or nonapplicability; missing coverage remains conditional rather than a forced field test or new exchanger.

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
- Supplied candidate field: `"C-B service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[C-B].facts.service"`)
- Supplied candidate field: `"C-B existing_recovery = null; blank; meaning and suitability unverified"` (`"units[C-B].facts.existing_recovery"`)
- Supplied candidate field: `"C-B operating_schedule = \"longhours\"; present; meaning and suitability unverified"` (`"units[C-B].facts.operating_schedule"`)
- Supplied candidate field: `"C-B receiver_schedule = null; blank; meaning and suitability unverified"` (`"units[C-B].facts.receiver_schedule"`)
- On drawing: Supplied candidate fact, basis unverified: C-B fictional_record = True (`units[C-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_source = Fictional pre-call development record, no company or human approval (`units[C-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_revision = R1 (`units[C-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_available = True (`units[C-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_authority = unverified (`units[C-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: C-B service = compressedair (`units[C-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: C-B operating_schedule = longhours (`units[C-B].facts.operating_schedule`)

**Data to collect**

- Existing compressor/cooling, recovery and receiving-duty basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): C-B (C-B) fictional_record = true [units[C-B].facts.fictional_record]; C-B (C-B) record_source = "Fictional pre-call development record, no company or human approval" [units[C-B].facts.record_source]; C-B (C-B) record_revision = "R1" [units[C-B].facts.record_revision]; C-B (C-B) record_available = true [units[C-B].facts.record_available]; C-B (C-B) record_authority = "unverified" [units[C-B].facts.record_authority]; C-B (C-B) service = "compressedair" [units[C-B].facts.service]; C-B (C-B) operating_schedule = "longhours" [units[C-B].facts.operating_schedule]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor type/cooling arrangement and performance, available thermal quantity/temperature and load/run schedule, existing recovery/coverage and receiving heat duty/temperature/time/seasonality, displaced energy and quality/material/cooling/ventilation/backpressure/control constraints, with exact units/source/owner/revision/availability.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S11 printed58-59 describes heat fractions and different air-cooled/water-cooled arrangements. Electrical input converted to heat and a recovered fraction of available thermal energy are not electrical savings or a useful site duty. Establish compatible temperatures, coincident demand and source/configuration first; the source says this heat is usually insufficient for direct steam production. Nearby load or long hours alone is insufficient. Retain required compressor cooling, ventilation/backpressure, water-quality/material and control constraints and added fan/exchanger effects. Acknowledge suitable existing recovery or nonapplicability; missing coverage remains conditional rather than a forced field test or new exchanger.

**How it is decided:** Review actual compressor/cooling performance, existing recovery and useful receiving duty, temperature, timing and operating/material/control constraints with the responsible specialist. Do not infer feasibility, useful output or a required retrofit from proximity/run hours or source heat percentages. Suitable existing recovery or nonapplicability may be acknowledged; unresolved source, service, units or duty remains explicit. No heat-recovery design, steam promise or site savings is produced.

**What the source says (S11):** "As much as 80 to 93 percent of the electrical energy" becomes heat; recovery "anywhere from 50 to 90 percent of this".
IAC/ITAC recommendation code: 2.243x (by description).

**Limits:** Source review: S11 printed58-59/PDF63-64, full heat-recovery context. Its80-93% electrical-to-heat fraction and50-90% recovery of available thermal energy are contextual source figures, not electricity or site savings; compressor/cooling/design and compatible receiving duty matter. The worked example omits additional fan power and warns of exchanger effects. Actual energy displacement and ventilation/cooling/quality constraints require review.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
