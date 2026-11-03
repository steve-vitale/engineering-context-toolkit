# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/source-policy/models/C6-02-dual-writer.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 0 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 1 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Controls and automation

### C6: What do existing records establish about this direct temperature-to-steam-valve control candidate's configuration, disturbances and suitable dynamics?

**About:** TV-A  

**Finding reference (JSON string):** `"C6@TV-A"`
**Asset IDs (JSON array):** `["TV-A", "TIC-A", "FT-A", "FIC-A"]`

**Evidence on the drawing / model**

- valve TV-A reads "TV-A STEAM valve" at U-A (`final_elements[TV-A]`)
- Temperature controller: controller TIC-A reads "TIC-A Fictional supplied controller" at U-A (`controllers[TIC-A]`)
- Steam flow measurement: instrument FT-A reads "FT-A STEAM flow" at U-A (`instruments[FT-A]`)
- Supplied flow-controller output; nested setpoint cascade and effective mode not established: controller FIC-A reads "FIC-A Fictional supplied controller" at U-A (`controllers[FIC-A]`)
- Supplied candidate field: `"TV-A fictional_record = true; present; meaning and suitability unverified"` (`"final_elements[TV-A].facts.fictional_record"`)
- Supplied candidate field: `"TV-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"final_elements[TV-A].facts.record_source"`)
- Supplied candidate field: `"TV-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"final_elements[TV-A].facts.record_revision"`)
- Supplied candidate field: `"TV-A record_available = true; present; meaning and suitability unverified"` (`"final_elements[TV-A].facts.record_available"`)
- Supplied candidate field: `"TV-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"final_elements[TV-A].facts.record_authority"`)
- Supplied candidate field: `"TV-A service = \"steamsupply\"; present; meaning and suitability unverified"` (`"final_elements[TV-A].facts.service"`)
- Supplied candidate field: `"TIC-A fictional_record = true; present; meaning and suitability unverified"` (`"controllers[TIC-A].facts.fictional_record"`)
- Supplied candidate field: `"TIC-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"controllers[TIC-A].facts.record_source"`)
- Supplied candidate field: `"TIC-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"controllers[TIC-A].facts.record_revision"`)
- Supplied candidate field: `"TIC-A record_available = true; present; meaning and suitability unverified"` (`"controllers[TIC-A].facts.record_available"`)
- Supplied candidate field: `"TIC-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"controllers[TIC-A].facts.record_authority"`)
- Supplied candidate field: `"TIC-A mode = \"auto\"; present; meaning and suitability unverified"` (`"controllers[TIC-A].facts.mode"`)
- Supplied candidate field: `"TIC-A output_role = \"directvalve\"; present; meaning and suitability unverified"` (`"controllers[TIC-A].facts.output_role"`)
- Supplied candidate field: `"FT-A fictional_record = true; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.fictional_record"`)
- Supplied candidate field: `"FT-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_source"`)
- Supplied candidate field: `"FT-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_revision"`)
- Supplied candidate field: `"FT-A record_available = true; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_available"`)
- Supplied candidate field: `"FT-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_authority"`)
- Supplied candidate field: `"FT-A quantity = \"massflow\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.quantity"`)
- Supplied candidate field: `"FT-A flow_unit = \"kg/h\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.flow_unit"`)
- Supplied candidate field: `"FIC-A fictional_record = true; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.fictional_record"`)
- Supplied candidate field: `"FIC-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_source"`)
- Supplied candidate field: `"FIC-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_revision"`)
- Supplied candidate field: `"FIC-A record_available = false; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_available"`)
- Supplied candidate field: `"FIC-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_authority"`)
- Supplied candidate field: `"FIC-A record_scope = \"foreignFIC-A\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.record_scope"`)
- Supplied candidate field: `"FIC-A mode = \"manualunknown\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.mode"`)
- Supplied candidate field: `"FIC-A output_role = \"secondwriter, notsetpointslave\"; present; meaning and suitability unverified"` (`"controllers[FIC-A].facts.output_role"`)
- On drawing: Supplied candidate fact, basis unverified: TV-A fictional_record = True (`final_elements[TV-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TV-A record_source = Fictional pre-call record, no company or human approval (`final_elements[TV-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TV-A record_revision = R1 (`final_elements[TV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TV-A record_available = True (`final_elements[TV-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TV-A record_authority = unverified (`final_elements[TV-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TV-A service = steamsupply (`final_elements[TV-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: TV-A fictional_record = True (`final_elements[TV-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TV-A record_source = Fictional pre-call record, no company or human approval (`final_elements[TV-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TV-A record_revision = R1 (`final_elements[TV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TV-A record_available = True (`final_elements[TV-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TV-A record_authority = unverified (`final_elements[TV-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TV-A service = steamsupply (`final_elements[TV-A].facts.service`)

**Data to collect**

- Loop behaviour [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TV-A (TV-A) fictional_record = true [final_elements[TV-A].facts.fictional_record]; TV-A (TV-A) record_source = "Fictional pre-call record, no company or human approval" [final_elements[TV-A].facts.record_source]; TV-A (TV-A) record_revision = "R1" [final_elements[TV-A].facts.record_revision]; TV-A (TV-A) record_available = true [final_elements[TV-A].facts.record_available]; TV-A (TV-A) record_authority = "unverified" [final_elements[TV-A].facts.record_authority]; TV-A (TV-A) service = "steamsupply" [final_elements[TV-A].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact measurement/controller/output and setpoint-chain/configuration, active modes, source/coverage, process objective and matched primary/secondary response, flow measurement/actuator suitability and existing load-disturbance histories.; then DCS/PLC configuration: Review existing controller configuration, tuning/modes and output history; no change is requested.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A flow-controller reference sharing the valve does not prove a nested cascade or justify suppression of conflicting/unknown configuration. The explicit additional Siemens AD353-128 rev2 April2012 pp1-4 describes a measurable/controllable secondary affecting the primary, encompassing the relevant disturbance and responding substantially faster. It also identifies disturbances outside that secondary loop and alternative secondary variables. Review the actual chain/dynamics, operating range and required behavior first; neither an oscillation nor a pressure swing alone authorizes a flow slave or tuning test. Suitable existing operation can be acknowledged.
- Steam header pressure swings [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TV-A (TV-A) fictional_record = true [final_elements[TV-A].facts.fictional_record]; TV-A (TV-A) record_source = "Fictional pre-call record, no company or human approval" [final_elements[TV-A].facts.record_source]; TV-A (TV-A) record_revision = "R1" [final_elements[TV-A].facts.record_revision]; TV-A (TV-A) record_available = true [final_elements[TV-A].facts.record_available]; TV-A (TV-A) record_authority = "unverified" [final_elements[TV-A].facts.record_authority]; TV-A (TV-A) service = "steamsupply" [final_elements[TV-A].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing comparable header/valve/flow/primary-variable pressure and disturbance records, sample periods and units, control ranges/limits, transfer/tracking/reset/anti-windup and actuator/measurement constraints.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: The manufacturer example is contextual application engineering, not a universal speed ratio, procurement or tuning requirement. Confirm that a secondary could address the relevant disturbance before any proposed design. Preserve limits and suitable transfer/reset/operating modes; a proper represented temperature-to-flow-setpoint chain is outside this direct-output pattern, not proof every cascade is adequate. No step test, setpoint/pressure change or equipment addition follows.

**How it is decided:** Review actual direct-output versus nested setpoint configuration, modes, relevant disturbance paths, measurement/actuator suitability and relative process dynamics with the responsible control engineer. Shared output labels or supply-pressure variation do not establish a cascade, its absence or a requirement to add one. Suitable existing control or nonapplicability can be acknowledged; unresolved configuration/source evidence remains a records question without tuning or operating authority.

**What the source says (no source):** No public numeric source found. Report as qualitative only.

**Limits:** Explicit additional source: Siemens Procidia CascadeControl AD353-128 rev2 April2012, complete pp1-4 and6-7, https://cache.industry.siemens.com/dl/files/372/51436372/att_88120/v1/AD353-128_r2.pdf . Manufacturer example, not independent plant or procurement acceptance. Existing direct-temperature/steam-valve and represented-controller scope retained; no claim to automatically detect heating/cooling controller fighting or all existing cascades. Numeric benefit object unchanged and no universal tuning ratio imposed.
