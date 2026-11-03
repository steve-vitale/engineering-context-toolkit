# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/source-policy/models/E19-01-missing-control.json`. Questions: `data/questions.json`.

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

### E19: What do existing records establish about this air-system candidate's pressure requirements, losses and control/storage constraints?

**About:** C-A  

**Finding reference (JSON string):** `"E19@C-A"`
**Asset IDs (JSON array):** `["C-A"]`

**Evidence on the drawing / model**

- equipment C-A reads "C-A Fictional AIR COMPRESSOR" (`units[C-A]`)
- Supplied candidate field: `"C-A fictional_record = true; present; meaning and suitability unverified"` (`"units[C-A].facts.fictional_record"`)
- Supplied candidate field: `"C-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_source"`)
- Supplied candidate field: `"C-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_revision"`)
- Supplied candidate field: `"C-A record_available = true; present; meaning and suitability unverified"` (`"units[C-A].facts.record_available"`)
- Supplied candidate field: `"C-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_authority"`)
- Supplied candidate field: `"C-A service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[C-A].facts.service"`)
- Supplied candidate field: `"C-A discharge_pressure = 150; present; meaning and suitability unverified"` (`"units[C-A].facts.discharge_pressure"`)
- Supplied candidate field: `"C-A required_end_pressure = 110; present; meaning and suitability unverified"` (`"units[C-A].facts.required_end_pressure"`)
- Supplied candidate field: `"C-A pressure_unit = \"psig\"; present; meaning and suitability unverified"` (`"units[C-A].facts.pressure_unit"`)
- Supplied candidate field: `"C-A sample_period = null; blank; meaning and suitability unverified"` (`"units[C-A].facts.sample_period"`)
- On drawing: Supplied candidate fact, basis unverified: C-A fictional_record = True (`units[C-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_source = Fictional development record; no company or human approval (`units[C-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_revision = R1 (`units[C-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_available = True (`units[C-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_authority = unverified (`units[C-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: C-A service = compressedair (`units[C-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: C-A discharge_pressure = 150 (`units[C-A].facts.discharge_pressure`)
- On drawing: Supplied candidate fact, basis unverified: C-A required_end_pressure = 110 (`units[C-A].facts.required_end_pressure`)
- On drawing: Supplied candidate fact, basis unverified: C-A pressure_unit = psig (`units[C-A].facts.pressure_unit`)

**Data to collect**

- Existing named-system service, pressure/end-use and dynamic control/storage basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): C-A (C-A) fictional_record = true [units[C-A].facts.fictional_record]; C-A (C-A) record_source = "Fictional development record; no company or human approval" [units[C-A].facts.record_source]; C-A (C-A) record_revision = "R1" [units[C-A].facts.record_revision]; C-A (C-A) record_available = true [units[C-A].facts.record_available]; C-A (C-A) record_authority = "unverified" [units[C-A].facts.record_authority]; C-A (C-A) service = "compressedair" [units[C-A].facts.service]; C-A (C-A) discharge_pressure = 150 [units[C-A].facts.discharge_pressure]; C-A (C-A) required_end_pressure = 110 [units[C-A].facts.required_end_pressure]; C-A (C-A) pressure_unit = "psig" [units[C-A].facts.pressure_unit]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor/system and controls, pressure location and discharge/header/point-of-use profiles, actual end-use requirements, distribution/treatment losses, peak/transient demand, storage/control range and manufacturer constraints; exact source/owner/revision, units/time/availability and coverage retained.; then site records: The following pressure/control tag/series locations are candidate-only lookup aids from supplied records; compressor/system association, source identity, availability, measurement location and requirements remain unverified. Do not treat a foreign or unknown candidate as this compressor's measured header pressure or minimum end-use requirement.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A pressure record anywhere is not this compressor's control or another user's requirement, and missing control representation is not closure. Known helpers/process-gas/refrigeration compressors are not air subjects; an air-compressor package is not disqualified merely because its name also mentions a dryer. Establish actual service/requirements and match quantities, locations and dynamic operating coverage. Review appropriate existing records and component/storage/control constraints before considering pressure changes. Suitable requirements or existing configuration can be acknowledged without new tests or lower-setpoint instructions.

**How it is decided:** Review actual system/end-use requirements and matched pressure/location/time records, peak demand, distribution/component drops, storage/control and manufacturer constraints with the responsible specialist before a pressure decision. Highest scalar need plus an assumed loss alone does not authorize lowering a setpoint. Unknown scope or dynamic basis remains a records question, and suitable existing operation or nonapplicability may be acknowledged; no operating change or site savings are calculated.

**What the source says (S11, S24):** S11 explains that pressure can affect compressor power and unregulated demand, with effects depending on compressor/control type, pressure range and operating conditions. Review manufacturer/system performance and required end-use pressure; no universal saving per pressure step or site benefit is asserted.
IAC/ITAC recommendation code: 2.4231 (IAC/ITAC browse page: 6,522 recommendations, 0.5 yr average payback, 51.6% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S11 printed28-36/PDF33-41, including full pressure/control context. Its printed31 increase and printed34 decrease passages give inconsistent combined percentage ranges; no corrected number is chosen. Original numeric wording remains historical, not a universal target or a reason to compromise minimum end-use pressure.

### E19: What do existing records establish about this air-system candidate's pressure requirements, losses and control/storage constraints?

**About:** C-B  

**Finding reference (JSON string):** `"E19@C-B"`
**Asset IDs (JSON array):** `["C-B"]`

**Evidence on the drawing / model**

- equipment C-B reads "C-B Fictional AIR COMPRESSOR" (`units[C-B]`)
- Supplied candidate field: `"C-B fictional_record = true; present; meaning and suitability unverified"` (`"units[C-B].facts.fictional_record"`)
- Supplied candidate field: `"C-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_source"`)
- Supplied candidate field: `"C-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_revision"`)
- Supplied candidate field: `"C-B record_available = true; present; meaning and suitability unverified"` (`"units[C-B].facts.record_available"`)
- Supplied candidate field: `"C-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_authority"`)
- Supplied candidate field: `"C-B service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[C-B].facts.service"`)
- Supplied candidate field: `"C-B discharge_pressure = null; blank; meaning and suitability unverified"` (`"units[C-B].facts.discharge_pressure"`)
- Supplied candidate field: `"C-B required_end_pressure = null; blank; meaning and suitability unverified"` (`"units[C-B].facts.required_end_pressure"`)
- On drawing: Supplied candidate fact, basis unverified: C-B fictional_record = True (`units[C-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_source = Fictional development record; no company or human approval (`units[C-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_revision = R1 (`units[C-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_available = True (`units[C-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_authority = unverified (`units[C-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: C-B service = compressedair (`units[C-B].facts.service`)

**Data to collect**

- Existing named-system service, pressure/end-use and dynamic control/storage basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): C-B (C-B) fictional_record = true [units[C-B].facts.fictional_record]; C-B (C-B) record_source = "Fictional development record; no company or human approval" [units[C-B].facts.record_source]; C-B (C-B) record_revision = "R1" [units[C-B].facts.record_revision]; C-B (C-B) record_available = true [units[C-B].facts.record_available]; C-B (C-B) record_authority = "unverified" [units[C-B].facts.record_authority]; C-B (C-B) service = "compressedair" [units[C-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor/system and controls, pressure location and discharge/header/point-of-use profiles, actual end-use requirements, distribution/treatment losses, peak/transient demand, storage/control range and manufacturer constraints; exact source/owner/revision, units/time/availability and coverage retained.; then site records: The following pressure/control tag/series locations are candidate-only lookup aids from supplied records; compressor/system association, source identity, availability, measurement location and requirements remain unverified. Do not treat a foreign or unknown candidate as this compressor's measured header pressure or minimum end-use requirement.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A pressure record anywhere is not this compressor's control or another user's requirement, and missing control representation is not closure. Known helpers/process-gas/refrigeration compressors are not air subjects; an air-compressor package is not disqualified merely because its name also mentions a dryer. Establish actual service/requirements and match quantities, locations and dynamic operating coverage. Review appropriate existing records and component/storage/control constraints before considering pressure changes. Suitable requirements or existing configuration can be acknowledged without new tests or lower-setpoint instructions.

**How it is decided:** Review actual system/end-use requirements and matched pressure/location/time records, peak demand, distribution/component drops, storage/control and manufacturer constraints with the responsible specialist before a pressure decision. Highest scalar need plus an assumed loss alone does not authorize lowering a setpoint. Unknown scope or dynamic basis remains a records question, and suitable existing operation or nonapplicability may be acknowledged; no operating change or site savings are calculated.

**What the source says (S11, S24):** S11 explains that pressure can affect compressor power and unregulated demand, with effects depending on compressor/control type, pressure range and operating conditions. Review manufacturer/system performance and required end-use pressure; no universal saving per pressure step or site benefit is asserted.
IAC/ITAC recommendation code: 2.4231 (IAC/ITAC browse page: 6,522 recommendations, 0.5 yr average payback, 51.6% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S11 printed28-36/PDF33-41, including full pressure/control context. Its printed31 increase and printed34 decrease passages give inconsistent combined percentage ranges; no corrected number is chosen. Original numeric wording remains historical, not a universal target or a reason to compromise minimum end-use pressure.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
