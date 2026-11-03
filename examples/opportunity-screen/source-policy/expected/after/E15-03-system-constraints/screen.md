# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/source-policy/models/E15-03-system-constraints.json`. Questions: `data/questions.json`.

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
**Asset IDs (JSON array):** `["B-A", "W-A"]`

**Evidence on the drawing / model**

- equipment B-A reads "B-A Fictional gas boiler" (`units[B-A]`)
- Unverified receiving-water record; compatibility not inferred: equipment W-A reads "W-A MAKEUP WATER load" (`units[W-A]`)
- Supplied candidate field: `"B-A fictional_record = true; present; meaning and suitability unverified"` (`"units[B-A].facts.fictional_record"`)
- Supplied candidate field: `"B-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_source"`)
- Supplied candidate field: `"B-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_revision"`)
- Supplied candidate field: `"B-A record_available = true; present; meaning and suitability unverified"` (`"units[B-A].facts.record_available"`)
- Supplied candidate field: `"B-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_authority"`)
- Supplied candidate field: `"B-A service = \"steamwaterflue\"; present; meaning and suitability unverified"` (`"units[B-A].facts.service"`)
- Supplied candidate field: `"B-A existing_recovery = \"suppliedexistingcondensingunit\"; present; meaning and suitability unverified"` (`"units[B-A].facts.existing_recovery"`)
- Supplied candidate field: `"B-A acid_treatment = \"unassessed\"; present; meaning and suitability unverified"` (`"units[B-A].facts.acid_treatment"`)
- Supplied candidate field: `"B-A stack_dispersion = \"unassessed\"; present; meaning and suitability unverified"` (`"units[B-A].facts.stack_dispersion"`)
- Supplied candidate field: `"B-A steam_balance = \"deaerator/turbineeffectsunknown\"; present; meaning and suitability unverified"` (`"units[B-A].facts.steam_balance"`)
- Supplied candidate field: `"B-A operating_hours = 4000; present; meaning and suitability unverified"` (`"units[B-A].facts.operating_hours"`)
- Supplied candidate field: `"W-A fictional_record = true; present; meaning and suitability unverified"` (`"units[W-A].facts.fictional_record"`)
- Supplied candidate field: `"W-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[W-A].facts.record_source"`)
- Supplied candidate field: `"W-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[W-A].facts.record_revision"`)
- Supplied candidate field: `"W-A record_available = true; present; meaning and suitability unverified"` (`"units[W-A].facts.record_available"`)
- Supplied candidate field: `"W-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[W-A].facts.record_authority"`)
- Supplied candidate field: `"W-A load_target = \"localsystemprovisional\"; present; meaning and suitability unverified"` (`"units[W-A].facts.load_target"`)
- Supplied candidate field: `"W-A load_duty = \"steadysourceassertion\"; present; meaning and suitability unverified"` (`"units[W-A].facts.load_duty"`)
- Supplied candidate field: `"W-A load_temperature = 60; present; meaning and suitability unverified"` (`"units[W-A].facts.load_temperature"`)
- Supplied candidate field: `"W-A temperature_unit = \"F\"; present; meaning and suitability unverified"` (`"units[W-A].facts.temperature_unit"`)
- Supplied candidate field: `"W-A load_flow = 100; present; meaning and suitability unverified"` (`"units[W-A].facts.load_flow"`)
- Supplied candidate field: `"W-A flow_unit = \"gpm\"; present; meaning and suitability unverified"` (`"units[W-A].facts.flow_unit"`)
- On drawing: Supplied candidate fact, basis unverified: B-A fictional_record = True (`units[B-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_source = Fictional development record; no company or human approval (`units[B-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_revision = R1 (`units[B-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_available = True (`units[B-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_authority = unverified (`units[B-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-A service = steamwaterflue (`units[B-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-A existing_recovery = suppliedexistingcondensingunit (`units[B-A].facts.existing_recovery`)
- On drawing: Supplied candidate fact, basis unverified: B-A acid_treatment = unassessed (`units[B-A].facts.acid_treatment`)
- On drawing: Supplied candidate fact, basis unverified: B-A stack_dispersion = unassessed (`units[B-A].facts.stack_dispersion`)
- On drawing: Supplied candidate fact, basis unverified: B-A steam_balance = deaerator/turbineeffectsunknown (`units[B-A].facts.steam_balance`)
- On drawing: Supplied candidate fact, basis unverified: B-A operating_hours = 4000 (`units[B-A].facts.operating_hours`)
- On drawing: Supplied candidate fact, basis unverified: B-A fictional_record = True (`units[B-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_source = Fictional development record; no company or human approval (`units[B-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_revision = R1 (`units[B-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_available = True (`units[B-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_authority = unverified (`units[B-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-A service = steamwaterflue (`units[B-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-A existing_recovery = suppliedexistingcondensingunit (`units[B-A].facts.existing_recovery`)
- On drawing: Supplied candidate fact, basis unverified: B-A acid_treatment = unassessed (`units[B-A].facts.acid_treatment`)
- On drawing: Supplied candidate fact, basis unverified: B-A stack_dispersion = unassessed (`units[B-A].facts.stack_dispersion`)
- On drawing: Supplied candidate fact, basis unverified: B-A steam_balance = deaerator/turbineeffectsunknown (`units[B-A].facts.steam_balance`)
- On drawing: Supplied candidate fact, basis unverified: B-A operating_hours = 4000 (`units[B-A].facts.operating_hours`)

**Data to collect**

- Existing boiler/flue/fuel and installed-recovery operating basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-A (B-A) fictional_record = true [units[B-A].facts.fictional_record]; B-A (B-A) record_source = "Fictional development record; no company or human approval" [units[B-A].facts.record_source]; B-A (B-A) record_revision = "R1" [units[B-A].facts.record_revision]; B-A (B-A) record_available = true [units[B-A].facts.record_available]; B-A (B-A) record_authority = "unverified" [units[B-A].facts.record_authority]; B-A (B-A) service = "steamwaterflue" [units[B-A].facts.service]; B-A (B-A) existing_recovery = "suppliedexistingcondensingunit" [units[B-A].facts.existing_recovery]; B-A (B-A) acid_treatment = "unassessed" [units[B-A].facts.acid_treatment]; B-A (B-A) stack_dispersion = "unassessed" [units[B-A].facts.stack_dispersion]; B-A (B-A) steam_balance = "deaerator/turbineeffectsunknown" [units[B-A].facts.steam_balance]; B-A (B-A) operating_hours = 4000 [units[B-A].facts.operating_hours]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-subject actual boiler/flue/fuel and recovery arrangement, capacity/load/hours/fuel use, stack temperature/moisture and gas condition, source/revision/units/time/availability and unknowns.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Establish relevant actual flue/boiler service first; known nonflue/electric or nonwater helper scope is not applicable and unknown service remains conditional. Missing GAS text, an unrecorded sink or unknown fuel is not proof that no records investigation is needed. S7 covers natural-gas and light-oil examples with different acid/material/treatment qualifications, not automatic suitability for any fuel. Acknowledge suitable existing recovery before considering further work.
- Existing matched receiving duty, water quality and whole-system feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-A (B-A) fictional_record = true [units[B-A].facts.fictional_record]; B-A (B-A) record_source = "Fictional development record; no company or human approval" [units[B-A].facts.record_source]; B-A (B-A) record_revision = "R1" [units[B-A].facts.record_revision]; B-A (B-A) record_available = true [units[B-A].facts.record_available]; B-A (B-A) record_authority = "unverified" [units[B-A].facts.record_authority]; B-A (B-A) service = "steamwaterflue" [units[B-A].facts.service]; B-A (B-A) existing_recovery = "suppliedexistingcondensingunit" [units[B-A].facts.existing_recovery]; B-A (B-A) acid_treatment = "unassessed" [units[B-A].facts.acid_treatment]; B-A (B-A) stack_dispersion = "unassessed" [units[B-A].facts.stack_dispersion]; B-A (B-A) steam_balance = "deaerator/turbineeffectsunknown" [units[B-A].facts.steam_balance]; B-A (B-A) operating_hours = 4000 [units[B-A].facts.operating_hours]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual receiving-water/process duty, temperature/flow/timing, exact association/source/quality and practical access; condensate acidity/treatment/materials, emissions/stack dispersion, deaerator/steam/turbine/blowdown-heat interactions and economic constraints.; then site records: The following receiving-water tag/series locations are candidate-only lookup aids from supplied records; boiler/system association, source identity, availability, compatible duty and water quality remain unverified. Do not treat a foreign or unknown candidate as this boiler's measured heat sink.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A nearby or anywhere MAKEUP/PROCESS/HOT WATER label is not proof of a cold, available, compatible or steady heat sink. Review source and receiving duty together with acid-condensate/water-quality treatment, design/material and whole-steam-system effects. S7 explicitly requires site-specific engineering and water-chemistry understanding; direct/indirect configurations and source examples are not interchangeable site prescriptions. Acknowledge suitable existing basis or unknowns without compulsory flue analysis, new measurements, equipment quotes or retrofit; no current site saving is calculated.

**How it is decided:** Review actual service/fuel, installed recovery and matched receiving duty/quality/timing with acid-condensate, materials, dispersion, whole-system and economic constraints before a feasibility decision. Do not obtain quotes or prescribe a condensing economizer from a GAS label plus nearby water, nor silently close unknown/oil/missing-sink records. Suitable existing function or nonapplicability may be acknowledged. No chemical, hardware, operating or site-benefit authorization follows.

**What the source says (S7):** Can "increase overall heat recovery and steam system efficiency by up to 10%." "Simple paybacks... are often less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description).

**Limits:** Source review: complete S7/Tip26B pp1–3 includes natural-gas/light-oil table qualifications, acid water/treatment/materials, system/stack-dispersion interactions and explicit site-specific engineering. Inherited up-to efficiency and payback examples are not present-day quotes or this site's outcomes. Supplied field/association values are unverified candidates, not completion.

### E15: What do existing records establish about this boiler/steam-generator candidate's applicable condensing-recovery function, receiving duty and system constraints?

**About:** B-B  

**Finding reference (JSON string):** `"E15@B-B"`
**Asset IDs (JSON array):** `["B-B", "W-A"]`

**Evidence on the drawing / model**

- equipment B-B reads "B-B Fictional gas boiler" (`units[B-B]`)
- Unverified receiving-water record; compatibility not inferred: equipment W-A reads "W-A MAKEUP WATER load" (`units[W-A]`)
- Supplied candidate field: `"B-B fictional_record = true; present; meaning and suitability unverified"` (`"units[B-B].facts.fictional_record"`)
- Supplied candidate field: `"B-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_source"`)
- Supplied candidate field: `"B-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_revision"`)
- Supplied candidate field: `"B-B record_available = true; present; meaning and suitability unverified"` (`"units[B-B].facts.record_available"`)
- Supplied candidate field: `"B-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_authority"`)
- Supplied candidate field: `"B-B service = \"steamwaterflue\"; present; meaning and suitability unverified"` (`"units[B-B].facts.service"`)
- Supplied candidate field: `"B-B existing_recovery = null; blank; meaning and suitability unverified"` (`"units[B-B].facts.existing_recovery"`)
- Supplied candidate field: `"B-B acid_treatment = \"suppliedmaterials/treatmentrecord notapproved\"; present; meaning and suitability unverified"` (`"units[B-B].facts.acid_treatment"`)
- Supplied candidate field: `"B-B stack_dispersion = \"qualifiedsourceincomplete\"; present; meaning and suitability unverified"` (`"units[B-B].facts.stack_dispersion"`)
- Supplied candidate field: `"B-B steam_balance = \"blowdownheatinteractionunknown\"; present; meaning and suitability unverified"` (`"units[B-B].facts.steam_balance"`)
- Supplied candidate field: `"W-A fictional_record = true; present; meaning and suitability unverified"` (`"units[W-A].facts.fictional_record"`)
- Supplied candidate field: `"W-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[W-A].facts.record_source"`)
- Supplied candidate field: `"W-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[W-A].facts.record_revision"`)
- Supplied candidate field: `"W-A record_available = true; present; meaning and suitability unverified"` (`"units[W-A].facts.record_available"`)
- Supplied candidate field: `"W-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[W-A].facts.record_authority"`)
- Supplied candidate field: `"W-A load_target = \"localsystemprovisional\"; present; meaning and suitability unverified"` (`"units[W-A].facts.load_target"`)
- Supplied candidate field: `"W-A load_duty = \"steadysourceassertion\"; present; meaning and suitability unverified"` (`"units[W-A].facts.load_duty"`)
- Supplied candidate field: `"W-A load_temperature = 60; present; meaning and suitability unverified"` (`"units[W-A].facts.load_temperature"`)
- Supplied candidate field: `"W-A temperature_unit = \"F\"; present; meaning and suitability unverified"` (`"units[W-A].facts.temperature_unit"`)
- Supplied candidate field: `"W-A load_flow = 100; present; meaning and suitability unverified"` (`"units[W-A].facts.load_flow"`)
- Supplied candidate field: `"W-A flow_unit = \"gpm\"; present; meaning and suitability unverified"` (`"units[W-A].facts.flow_unit"`)
- On drawing: Supplied candidate fact, basis unverified: B-B fictional_record = True (`units[B-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_source = Fictional development record; no company or human approval (`units[B-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_revision = R1 (`units[B-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_available = True (`units[B-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_authority = unverified (`units[B-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-B service = steamwaterflue (`units[B-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-B acid_treatment = suppliedmaterials/treatmentrecord notapproved (`units[B-B].facts.acid_treatment`)
- On drawing: Supplied candidate fact, basis unverified: B-B stack_dispersion = qualifiedsourceincomplete (`units[B-B].facts.stack_dispersion`)
- On drawing: Supplied candidate fact, basis unverified: B-B steam_balance = blowdownheatinteractionunknown (`units[B-B].facts.steam_balance`)
- On drawing: Supplied candidate fact, basis unverified: B-B fictional_record = True (`units[B-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_source = Fictional development record; no company or human approval (`units[B-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_revision = R1 (`units[B-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_available = True (`units[B-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_authority = unverified (`units[B-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-B service = steamwaterflue (`units[B-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-B acid_treatment = suppliedmaterials/treatmentrecord notapproved (`units[B-B].facts.acid_treatment`)
- On drawing: Supplied candidate fact, basis unverified: B-B stack_dispersion = qualifiedsourceincomplete (`units[B-B].facts.stack_dispersion`)
- On drawing: Supplied candidate fact, basis unverified: B-B steam_balance = blowdownheatinteractionunknown (`units[B-B].facts.steam_balance`)

**Data to collect**

- Existing boiler/flue/fuel and installed-recovery operating basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-B (B-B) fictional_record = true [units[B-B].facts.fictional_record]; B-B (B-B) record_source = "Fictional development record; no company or human approval" [units[B-B].facts.record_source]; B-B (B-B) record_revision = "R1" [units[B-B].facts.record_revision]; B-B (B-B) record_available = true [units[B-B].facts.record_available]; B-B (B-B) record_authority = "unverified" [units[B-B].facts.record_authority]; B-B (B-B) service = "steamwaterflue" [units[B-B].facts.service]; B-B (B-B) acid_treatment = "suppliedmaterials/treatmentrecord notapproved" [units[B-B].facts.acid_treatment]; B-B (B-B) stack_dispersion = "qualifiedsourceincomplete" [units[B-B].facts.stack_dispersion]; B-B (B-B) steam_balance = "blowdownheatinteractionunknown" [units[B-B].facts.steam_balance]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-subject actual boiler/flue/fuel and recovery arrangement, capacity/load/hours/fuel use, stack temperature/moisture and gas condition, source/revision/units/time/availability and unknowns.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Establish relevant actual flue/boiler service first; known nonflue/electric or nonwater helper scope is not applicable and unknown service remains conditional. Missing GAS text, an unrecorded sink or unknown fuel is not proof that no records investigation is needed. S7 covers natural-gas and light-oil examples with different acid/material/treatment qualifications, not automatic suitability for any fuel. Acknowledge suitable existing recovery before considering further work.
- Existing matched receiving duty, water quality and whole-system feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-B (B-B) fictional_record = true [units[B-B].facts.fictional_record]; B-B (B-B) record_source = "Fictional development record; no company or human approval" [units[B-B].facts.record_source]; B-B (B-B) record_revision = "R1" [units[B-B].facts.record_revision]; B-B (B-B) record_available = true [units[B-B].facts.record_available]; B-B (B-B) record_authority = "unverified" [units[B-B].facts.record_authority]; B-B (B-B) service = "steamwaterflue" [units[B-B].facts.service]; B-B (B-B) acid_treatment = "suppliedmaterials/treatmentrecord notapproved" [units[B-B].facts.acid_treatment]; B-B (B-B) stack_dispersion = "qualifiedsourceincomplete" [units[B-B].facts.stack_dispersion]; B-B (B-B) steam_balance = "blowdownheatinteractionunknown" [units[B-B].facts.steam_balance]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual receiving-water/process duty, temperature/flow/timing, exact association/source/quality and practical access; condensate acidity/treatment/materials, emissions/stack dispersion, deaerator/steam/turbine/blowdown-heat interactions and economic constraints.; then site records: The following receiving-water tag/series locations are candidate-only lookup aids from supplied records; boiler/system association, source identity, availability, compatible duty and water quality remain unverified. Do not treat a foreign or unknown candidate as this boiler's measured heat sink.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A nearby or anywhere MAKEUP/PROCESS/HOT WATER label is not proof of a cold, available, compatible or steady heat sink. Review source and receiving duty together with acid-condensate/water-quality treatment, design/material and whole-steam-system effects. S7 explicitly requires site-specific engineering and water-chemistry understanding; direct/indirect configurations and source examples are not interchangeable site prescriptions. Acknowledge suitable existing basis or unknowns without compulsory flue analysis, new measurements, equipment quotes or retrofit; no current site saving is calculated.

**How it is decided:** Review actual service/fuel, installed recovery and matched receiving duty/quality/timing with acid-condensate, materials, dispersion, whole-system and economic constraints before a feasibility decision. Do not obtain quotes or prescribe a condensing economizer from a GAS label plus nearby water, nor silently close unknown/oil/missing-sink records. Suitable existing function or nonapplicability may be acknowledged. No chemical, hardware, operating or site-benefit authorization follows.

**What the source says (S7):** Can "increase overall heat recovery and steam system efficiency by up to 10%." "Simple paybacks... are often less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description).

**Limits:** Source review: complete S7/Tip26B pp1–3 includes natural-gas/light-oil table qualifications, acid water/treatment/materials, system/stack-dispersion interactions and explicit site-specific engineering. Inherited up-to efficiency and payback examples are not present-day quotes or this site's outcomes. Supplied field/association values are unverified candidates, not completion.

## Sources cited above

- S7: Steam Tip #26B, Considerations When Selecting a Condensing Economizer (DOE/GO-102012-3397). https://www.energy.gov/sites/prod/files/2014/05/f16/steam26b_condensing.pdf (license: Public domain)
