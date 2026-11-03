# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/source-policy/models/C7-02-separate-systems.json`. Questions: `data/questions.json`.

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

### C7: What do existing records establish about these air-compressor candidates' shared-system operation and coordinated control strategy?

**About:** C-A, C-B  

**Finding reference (JSON string):** `"C7@model"`
**Asset IDs (JSON array):** `["C-A", "C-B"]`

**Evidence on the drawing / model**

- equipment C-A reads "C-A AIR COMPRESSOR" (`units[C-A]`)
- equipment C-B reads "C-B AIR COMPRESSOR" (`units[C-B]`)
- Supplied candidate field: `"C-A fictional_record = true; present; meaning and suitability unverified"` (`"units[C-A].facts.fictional_record"`)
- Supplied candidate field: `"C-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_source"`)
- Supplied candidate field: `"C-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_revision"`)
- Supplied candidate field: `"C-A record_available = true; present; meaning and suitability unverified"` (`"units[C-A].facts.record_available"`)
- Supplied candidate field: `"C-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[C-A].facts.record_authority"`)
- Supplied candidate field: `"C-A system_id = \"A\"; present; meaning and suitability unverified"` (`"units[C-A].facts.system_id"`)
- Supplied candidate field: `"C-A shared_header = false; present; meaning and suitability unverified"` (`"units[C-A].facts.shared_header"`)
- Supplied candidate field: `"C-A simultaneous_operation = false; present; meaning and suitability unverified"` (`"units[C-A].facts.simultaneous_operation"`)
- Supplied candidate field: `"C-A control_mode = \"localcascade\"; present; meaning and suitability unverified"` (`"units[C-A].facts.control_mode"`)
- Supplied candidate field: `"C-A load_fraction = 0.4; present; meaning and suitability unverified"` (`"units[C-A].facts.load_fraction"`)
- Supplied candidate field: `"C-A power = 20; present; meaning and suitability unverified"` (`"units[C-A].facts.power"`)
- Supplied candidate field: `"C-A power_unit = \"kW\"; present; meaning and suitability unverified"` (`"units[C-A].facts.power_unit"`)
- Supplied candidate field: `"C-A sample_period = \"periodA\"; present; meaning and suitability unverified"` (`"units[C-A].facts.sample_period"`)
- Supplied candidate field: `"C-B fictional_record = true; present; meaning and suitability unverified"` (`"units[C-B].facts.fictional_record"`)
- Supplied candidate field: `"C-B record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_source"`)
- Supplied candidate field: `"C-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_revision"`)
- Supplied candidate field: `"C-B record_available = true; present; meaning and suitability unverified"` (`"units[C-B].facts.record_available"`)
- Supplied candidate field: `"C-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_authority"`)
- Supplied candidate field: `"C-B system_id = \"B\"; present; meaning and suitability unverified"` (`"units[C-B].facts.system_id"`)
- Supplied candidate field: `"C-B shared_header = false; present; meaning and suitability unverified"` (`"units[C-B].facts.shared_header"`)
- Supplied candidate field: `"C-B simultaneous_operation = false; present; meaning and suitability unverified"` (`"units[C-B].facts.simultaneous_operation"`)
- Supplied candidate field: `"C-B control_mode = \"VSDtrim\"; present; meaning and suitability unverified"` (`"units[C-B].facts.control_mode"`)
- Supplied candidate field: `"C-B load_fraction = 0.4; present; meaning and suitability unverified"` (`"units[C-B].facts.load_fraction"`)
- Supplied candidate field: `"C-B power = 5; present; meaning and suitability unverified"` (`"units[C-B].facts.power"`)
- Supplied candidate field: `"C-B power_unit = \"kW\"; present; meaning and suitability unverified"` (`"units[C-B].facts.power_unit"`)
- Supplied candidate field: `"C-B sample_period = \"periodB\"; present; meaning and suitability unverified"` (`"units[C-B].facts.sample_period"`)
- On drawing: Supplied candidate fact, basis unverified: C-A fictional_record = True (`units[C-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-B fictional_record = True (`units[C-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_source = Fictional pre-call record, no company or human approval (`units[C-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_source = Fictional pre-call record, no company or human approval (`units[C-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_revision = R1 (`units[C-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_revision = R1 (`units[C-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_available = True (`units[C-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_available = True (`units[C-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-A record_authority = unverified (`units[C-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_authority = unverified (`units[C-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: C-A system_id = A (`units[C-A].facts.system_id`)
- On drawing: Supplied candidate fact, basis unverified: C-B system_id = B (`units[C-B].facts.system_id`)
- On drawing: Supplied candidate fact, basis unverified: C-A shared_header = False (`units[C-A].facts.shared_header`)
- On drawing: Supplied candidate fact, basis unverified: C-B shared_header = False (`units[C-B].facts.shared_header`)
- On drawing: Supplied candidate fact, basis unverified: C-A simultaneous_operation = False (`units[C-A].facts.simultaneous_operation`)
- On drawing: Supplied candidate fact, basis unverified: C-B simultaneous_operation = False (`units[C-B].facts.simultaneous_operation`)
- On drawing: Supplied candidate fact, basis unverified: C-A control_mode = localcascade (`units[C-A].facts.control_mode`)
- On drawing: Supplied candidate fact, basis unverified: C-B control_mode = VSDtrim (`units[C-B].facts.control_mode`)
- On drawing: Supplied candidate fact, basis unverified: C-A load_fraction = 0.4 (`units[C-A].facts.load_fraction`)
- On drawing: Supplied candidate fact, basis unverified: C-B load_fraction = 0.4 (`units[C-B].facts.load_fraction`)
- On drawing: Supplied candidate fact, basis unverified: C-A power = 20 (`units[C-A].facts.power`)
- On drawing: Supplied candidate fact, basis unverified: C-B power = 5 (`units[C-B].facts.power`)
- On drawing: Supplied candidate fact, basis unverified: C-A power_unit = kW (`units[C-A].facts.power_unit`)
- On drawing: Supplied candidate fact, basis unverified: C-B power_unit = kW (`units[C-B].facts.power_unit`)
- On drawing: Supplied candidate fact, basis unverified: C-A sample_period = periodA (`units[C-A].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: C-B sample_period = periodB (`units[C-B].facts.sample_period`)

**Data to collect**

- Control narrative and load/unload history [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): C-A (C-A) fictional_record = true [units[C-A].facts.fictional_record]; C-B (C-B) fictional_record = true [units[C-B].facts.fictional_record]; C-A (C-A) record_source = "Fictional pre-call record, no company or human approval" [units[C-A].facts.record_source]; C-B (C-B) record_source = "Fictional pre-call record, no company or human approval" [units[C-B].facts.record_source]; C-A (C-A) record_revision = "R1" [units[C-A].facts.record_revision]; C-B (C-B) record_revision = "R1" [units[C-B].facts.record_revision]; C-A (C-A) record_available = true [units[C-A].facts.record_available]; C-B (C-B) record_available = true [units[C-B].facts.record_available]; C-A (C-A) record_authority = "unverified" [units[C-A].facts.record_authority]; C-B (C-B) record_authority = "unverified" [units[C-B].facts.record_authority]; C-A (C-A) system_id = "A" [units[C-A].facts.system_id]; C-B (C-B) system_id = "B" [units[C-B].facts.system_id]; C-A (C-A) shared_header = false [units[C-A].facts.shared_header]; C-B (C-B) shared_header = false [units[C-B].facts.shared_header]; C-A (C-A) simultaneous_operation = false [units[C-A].facts.simultaneous_operation]; C-B (C-B) simultaneous_operation = false [units[C-B].facts.simultaneous_operation]; C-A (C-A) control_mode = "localcascade" [units[C-A].facts.control_mode]; C-B (C-B) control_mode = "VSDtrim" [units[C-B].facts.control_mode]; C-A (C-A) load_fraction = 0.4 [units[C-A].facts.load_fraction]; C-B (C-B) load_fraction = 0.4 [units[C-B].facts.load_fraction]; C-A (C-A) power = 20 [units[C-A].facts.power]; C-B (C-B) power = 5 [units[C-B].facts.power]; C-A (C-A) power_unit = "kW" [units[C-A].facts.power_unit]; C-B (C-B) power_unit = "kW" [units[C-B].facts.power_unit]; C-A (C-A) sample_period = "periodA" [units[C-A].facts.sample_period]; C-B (C-B) sample_period = "periodB" [units[C-B].facts.sample_period]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact compressor/service/system and shared-header boundaries, current local/network/master narrative/settings/capability and source coverage, matched demand/pressure/load/power/time and storage/treatment records, base/trim roles, requirements and manufacturer/compatibility constraints.; then DCS/PLC configuration: Review permitted existing compressor control settings/narratives with their coverage and active modes.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Two names or part-load scalar values do not show shared system or concurrent operation, and a global MASTER/SEQUENCER label does not cover every machine. S11 printed34-39/42 supports different local/network/master arrangements depending on equipment, requirements, demand/storage and complexity; part-loading of a suitable trim unit is not automatically waste. Known helper/nonair types are not air machines, but a compressor package is not omitted merely because its name mentions a dryer. Review suitable existing strategy and source/units/operating coverage before further work, consulting specialists for mixed/variable-speed arrangements. No automatic master addition, compressor stop or new logging is required.

**How it is decided:** Review actual shared-system membership and concurrency, requirements, current local/network/master coordination, base/trim capabilities, demand/storage/pressure/power and source/time coverage with the responsible specialist. Multiple names or simultaneous part-load labels alone do not require sequencing hardware. Suitable existing strategy or nonapplicability can be acknowledged; unresolved scope/operation remains explicit without pressure/control or equipment-change authority.

**What the source says (S11, S24):** Control objective "is also to shut off unneeded compressors or delay bringing on additional compressors until needed." No % stated.
IAC/ITAC recommendation code: 2.423x (operations, category only) (IAC/ITAC browse page: 20,819 recommendations, 0.5 yr average payback, 67.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S11 printed34-39/PDF39-44 and42/PDF47, full relevant control pages. Model-level at-least2 candidates is a records prompt, not inferred topology/concurrency or a claim the installed system lacks master control. Existing strategies and compatible operating requirements matter; source objective and IAC history are not site savings.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
