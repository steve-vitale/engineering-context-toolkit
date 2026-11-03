# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/source-policy/models/E15-02-oil-unknown-sink.json`. Questions: `data/questions.json`.

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

### E15: What do existing records establish about this boiler/steam-generator candidate's applicable condensing-recovery function, receiving duty and system constraints?

**About:** B-A  

**Finding reference (JSON string):** `"E15@B-A"`
**Asset IDs (JSON array):** `["B-A"]`

**Evidence on the drawing / model**

- equipment B-A reads "B-A Light oil boiler" (`units[B-A]`)
- Supplied candidate field: `"B-A fictional_record = true; present; meaning and suitability unverified"` (`"units[B-A].facts.fictional_record"`)
- Supplied candidate field: `"B-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_source"`)
- Supplied candidate field: `"B-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_revision"`)
- Supplied candidate field: `"B-A record_available = true; present; meaning and suitability unverified"` (`"units[B-A].facts.record_available"`)
- Supplied candidate field: `"B-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_authority"`)
- Supplied candidate field: `"B-A service = \"steamwaterflue\"; present; meaning and suitability unverified"` (`"units[B-A].facts.service"`)
- Supplied candidate field: `"B-A fuel_basis = \"lightoil\"; present; meaning and suitability unverified"` (`"units[B-A].facts.fuel_basis"`)
- Supplied candidate field: `"B-A sink_basis = null; blank; meaning and suitability unverified"` (`"units[B-A].facts.sink_basis"`)
- Supplied candidate field: `"B-A condensate_quality = \"acid/treatmentunreviewed\"; present; meaning and suitability unverified"` (`"units[B-A].facts.condensate_quality"`)
- On drawing: Supplied candidate fact, basis unverified: B-A fictional_record = True (`units[B-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_source = Fictional development record; no company or human approval (`units[B-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_revision = R1 (`units[B-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_available = True (`units[B-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_authority = unverified (`units[B-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-A service = steamwaterflue (`units[B-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-A fuel_basis = lightoil (`units[B-A].facts.fuel_basis`)
- On drawing: Supplied candidate fact, basis unverified: B-A condensate_quality = acid/treatmentunreviewed (`units[B-A].facts.condensate_quality`)
- On drawing: Supplied candidate fact, basis unverified: B-A fictional_record = True (`units[B-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_source = Fictional development record; no company or human approval (`units[B-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_revision = R1 (`units[B-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_available = True (`units[B-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_authority = unverified (`units[B-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-A service = steamwaterflue (`units[B-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-A fuel_basis = lightoil (`units[B-A].facts.fuel_basis`)
- On drawing: Supplied candidate fact, basis unverified: B-A condensate_quality = acid/treatmentunreviewed (`units[B-A].facts.condensate_quality`)

**Data to collect**

- Existing boiler/flue/fuel and installed-recovery operating basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-A (B-A) fictional_record = true [units[B-A].facts.fictional_record]; B-A (B-A) record_source = "Fictional development record; no company or human approval" [units[B-A].facts.record_source]; B-A (B-A) record_revision = "R1" [units[B-A].facts.record_revision]; B-A (B-A) record_available = true [units[B-A].facts.record_available]; B-A (B-A) record_authority = "unverified" [units[B-A].facts.record_authority]; B-A (B-A) service = "steamwaterflue" [units[B-A].facts.service]; B-A (B-A) fuel_basis = "lightoil" [units[B-A].facts.fuel_basis]; B-A (B-A) condensate_quality = "acid/treatmentunreviewed" [units[B-A].facts.condensate_quality]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-subject actual boiler/flue/fuel and recovery arrangement, capacity/load/hours/fuel use, stack temperature/moisture and gas condition, source/revision/units/time/availability and unknowns.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Establish relevant actual flue/boiler service first; known nonflue/electric or nonwater helper scope is not applicable and unknown service remains conditional. Missing GAS text, an unrecorded sink or unknown fuel is not proof that no records investigation is needed. S7 covers natural-gas and light-oil examples with different acid/material/treatment qualifications, not automatic suitability for any fuel. Acknowledge suitable existing recovery before considering further work.
- Existing matched receiving duty, water quality and whole-system feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-A (B-A) fictional_record = true [units[B-A].facts.fictional_record]; B-A (B-A) record_source = "Fictional development record; no company or human approval" [units[B-A].facts.record_source]; B-A (B-A) record_revision = "R1" [units[B-A].facts.record_revision]; B-A (B-A) record_available = true [units[B-A].facts.record_available]; B-A (B-A) record_authority = "unverified" [units[B-A].facts.record_authority]; B-A (B-A) service = "steamwaterflue" [units[B-A].facts.service]; B-A (B-A) fuel_basis = "lightoil" [units[B-A].facts.fuel_basis]; B-A (B-A) condensate_quality = "acid/treatmentunreviewed" [units[B-A].facts.condensate_quality]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual receiving-water/process duty, temperature/flow/timing, exact association/source/quality and practical access; condensate acidity/treatment/materials, emissions/stack dispersion, deaerator/steam/turbine/blowdown-heat interactions and economic constraints.; then site records: The following receiving-water tag/series locations are candidate-only lookup aids from supplied records; boiler/system association, source identity, availability, compatible duty and water quality remain unverified. Do not treat a foreign or unknown candidate as this boiler's measured heat sink.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A nearby or anywhere MAKEUP/PROCESS/HOT WATER label is not proof of a cold, available, compatible or steady heat sink. Review source and receiving duty together with acid-condensate/water-quality treatment, design/material and whole-steam-system effects. S7 explicitly requires site-specific engineering and water-chemistry understanding; direct/indirect configurations and source examples are not interchangeable site prescriptions. Acknowledge suitable existing basis or unknowns without compulsory flue analysis, new measurements, equipment quotes or retrofit; no current site saving is calculated.

**How it is decided:** Review actual service/fuel, installed recovery and matched receiving duty/quality/timing with acid-condensate, materials, dispersion, whole-system and economic constraints before a feasibility decision. Do not obtain quotes or prescribe a condensing economizer from a GAS label plus nearby water, nor silently close unknown/oil/missing-sink records. Suitable existing function or nonapplicability may be acknowledged. No chemical, hardware, operating or site-benefit authorization follows.

**What the source says (S7):** Can "increase overall heat recovery and steam system efficiency by up to 10%." "Simple paybacks... are often less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description).

**Limits:** Source review: complete S7/Tip26B pp1–3 includes natural-gas/light-oil table qualifications, acid water/treatment/materials, system/stack-dispersion interactions and explicit site-specific engineering. Inherited up-to efficiency and payback examples are not present-day quotes or this site's outcomes. Supplied field/association values are unverified candidates, not completion.

### E15: What do existing records establish about this boiler/steam-generator candidate's applicable condensing-recovery function, receiving duty and system constraints?

**About:** B-B  

**Finding reference (JSON string):** `"E15@B-B"`
**Asset IDs (JSON array):** `["B-B"]`

**Evidence on the drawing / model**

- equipment B-B reads "B-B Boiler unknown fuel" (`units[B-B]`)
- Supplied candidate field: `"B-B fictional_record = true; present; meaning and suitability unverified"` (`"units[B-B].facts.fictional_record"`)
- Supplied candidate field: `"B-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_source"`)
- Supplied candidate field: `"B-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_revision"`)
- Supplied candidate field: `"B-B record_available = true; present; meaning and suitability unverified"` (`"units[B-B].facts.record_available"`)
- Supplied candidate field: `"B-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_authority"`)
- Supplied candidate field: `"B-B service = \"steamwaterflueunverified\"; present; meaning and suitability unverified"` (`"units[B-B].facts.service"`)
- Supplied candidate field: `"B-B fuel_basis = null; blank; meaning and suitability unverified"` (`"units[B-B].facts.fuel_basis"`)
- Supplied candidate field: `"B-B sink_basis = null; blank; meaning and suitability unverified"` (`"units[B-B].facts.sink_basis"`)
- On drawing: Supplied candidate fact, basis unverified: B-B fictional_record = True (`units[B-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_source = Fictional development record; no company or human approval (`units[B-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_revision = R1 (`units[B-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_available = True (`units[B-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_authority = unverified (`units[B-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-B service = steamwaterflueunverified (`units[B-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-B fictional_record = True (`units[B-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_source = Fictional development record; no company or human approval (`units[B-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_revision = R1 (`units[B-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_available = True (`units[B-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_authority = unverified (`units[B-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-B service = steamwaterflueunverified (`units[B-B].facts.service`)

**Data to collect**

- Existing boiler/flue/fuel and installed-recovery operating basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-B (B-B) fictional_record = true [units[B-B].facts.fictional_record]; B-B (B-B) record_source = "Fictional development record; no company or human approval" [units[B-B].facts.record_source]; B-B (B-B) record_revision = "R1" [units[B-B].facts.record_revision]; B-B (B-B) record_available = true [units[B-B].facts.record_available]; B-B (B-B) record_authority = "unverified" [units[B-B].facts.record_authority]; B-B (B-B) service = "steamwaterflueunverified" [units[B-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-subject actual boiler/flue/fuel and recovery arrangement, capacity/load/hours/fuel use, stack temperature/moisture and gas condition, source/revision/units/time/availability and unknowns.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Establish relevant actual flue/boiler service first; known nonflue/electric or nonwater helper scope is not applicable and unknown service remains conditional. Missing GAS text, an unrecorded sink or unknown fuel is not proof that no records investigation is needed. S7 covers natural-gas and light-oil examples with different acid/material/treatment qualifications, not automatic suitability for any fuel. Acknowledge suitable existing recovery before considering further work.
- Existing matched receiving duty, water quality and whole-system feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-B (B-B) fictional_record = true [units[B-B].facts.fictional_record]; B-B (B-B) record_source = "Fictional development record; no company or human approval" [units[B-B].facts.record_source]; B-B (B-B) record_revision = "R1" [units[B-B].facts.record_revision]; B-B (B-B) record_available = true [units[B-B].facts.record_available]; B-B (B-B) record_authority = "unverified" [units[B-B].facts.record_authority]; B-B (B-B) service = "steamwaterflueunverified" [units[B-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual receiving-water/process duty, temperature/flow/timing, exact association/source/quality and practical access; condensate acidity/treatment/materials, emissions/stack dispersion, deaerator/steam/turbine/blowdown-heat interactions and economic constraints.; then site records: The following receiving-water tag/series locations are candidate-only lookup aids from supplied records; boiler/system association, source identity, availability, compatible duty and water quality remain unverified. Do not treat a foreign or unknown candidate as this boiler's measured heat sink.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A nearby or anywhere MAKEUP/PROCESS/HOT WATER label is not proof of a cold, available, compatible or steady heat sink. Review source and receiving duty together with acid-condensate/water-quality treatment, design/material and whole-steam-system effects. S7 explicitly requires site-specific engineering and water-chemistry understanding; direct/indirect configurations and source examples are not interchangeable site prescriptions. Acknowledge suitable existing basis or unknowns without compulsory flue analysis, new measurements, equipment quotes or retrofit; no current site saving is calculated.

**How it is decided:** Review actual service/fuel, installed recovery and matched receiving duty/quality/timing with acid-condensate, materials, dispersion, whole-system and economic constraints before a feasibility decision. Do not obtain quotes or prescribe a condensing economizer from a GAS label plus nearby water, nor silently close unknown/oil/missing-sink records. Suitable existing function or nonapplicability may be acknowledged. No chemical, hardware, operating or site-benefit authorization follows.

**What the source says (S7):** Can "increase overall heat recovery and steam system efficiency by up to 10%." "Simple paybacks... are often less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description).

**Limits:** Source review: complete S7/Tip26B pp1–3 includes natural-gas/light-oil table qualifications, acid water/treatment/materials, system/stack-dispersion interactions and explicit site-specific engineering. Inherited up-to efficiency and payback examples are not present-day quotes or this site's outcomes. Supplied field/association values are unverified candidates, not completion.

## Sources cited above

- S7: Steam Tip #26B, Considerations When Selecting a Condensing Economizer (DOE/GO-102012-3397). https://www.energy.gov/sites/prod/files/2014/05/f16/steam26b_condensing.pdf (license: Public domain)
