# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/source-policy/models/E26-03-existing-records.json`. Questions: `data/questions.json`.

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
| Controls and automation | 0 |
| Emissions | 1 |
| Safety questions to verify | 0 |

## Emissions

### E26: What do existing records establish about these relief/flare/vent candidates' actual events, measurement/composition and source coverage?

**About:** V-A  

**Finding reference (JSON string):** `"E26@model"`
**Asset IDs (JSON array):** `["stream:V-A", "FT-A"]`

**Evidence on the drawing / model**

- stream V-A (asset stream:V-A) reads "PROCESS VENT HEADER" (`streams[V-A]`)
- Unverified flow candidate; quantity/composition/event/source coverage not established: instrument FT-A reads "FT-A Vent flow" at U-A (`instruments[FT-A]`)
- Supplied candidate field: `"V-A fictional_record = true; present; meaning and suitability unverified"` (`"streams[V-A].facts.fictional_record"`)
- Supplied candidate field: `"V-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.record_source"`)
- Supplied candidate field: `"V-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.record_revision"`)
- Supplied candidate field: `"V-A record_available = true; present; meaning and suitability unverified"` (`"streams[V-A].facts.record_available"`)
- Supplied candidate field: `"V-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.record_authority"`)
- Supplied candidate field: `"V-A record_scope = \"currentdeclaredV-A\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.record_scope"`)
- Supplied candidate field: `"V-A service = \"processgas\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.service"`)
- Supplied candidate field: `"V-A event_mode = \"plannedintermittent+background\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.event_mode"`)
- Supplied candidate field: `"V-A composition = \"suppliedbutunverified\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.composition"`)
- Supplied candidate field: `"V-A flow = 5; present; meaning and suitability unverified"` (`"streams[V-A].facts.flow"`)
- Supplied candidate field: `"V-A flow_unit = \"kg/h\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.flow_unit"`)
- Supplied candidate field: `"V-A quality = \"declaredgoodunverified\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.quality"`)
- Supplied candidate field: `"V-A sample_period = \"fictionalinterval\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.sample_period"`)
- Supplied candidate field: `"V-A measurement_basis = \"suppliedexistingmeter\"; present; meaning and suitability unverified"` (`"streams[V-A].facts.measurement_basis"`)
- Supplied candidate field: `"FT-A fictional_record = true; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.fictional_record"`)
- Supplied candidate field: `"FT-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_source"`)
- Supplied candidate field: `"FT-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_revision"`)
- Supplied candidate field: `"FT-A record_available = true; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_available"`)
- Supplied candidate field: `"FT-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_authority"`)
- Supplied candidate field: `"FT-A record_scope = \"declaredlocal\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.record_scope"`)
- Supplied candidate field: `"FT-A measurement_target = \"V-Adeclared\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.measurement_target"`)
- Supplied candidate field: `"FT-A quantity = \"massflow\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.quantity"`)
- Supplied candidate field: `"FT-A flow_unit = \"kg/h\"; present; meaning and suitability unverified"` (`"instruments[FT-A].facts.flow_unit"`)
- On drawing: Supplied candidate fact, basis unverified: V-A fictional_record = True (`streams[V-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_source = Fictional pre-call record, no company or human approval (`streams[V-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_revision = R1 (`streams[V-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_available = True (`streams[V-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_authority = unverified (`streams[V-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_scope = currentdeclaredV-A (`streams[V-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: V-A service = processgas (`streams[V-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: V-A event_mode = plannedintermittent+background (`streams[V-A].facts.event_mode`)
- On drawing: Supplied candidate fact, basis unverified: V-A composition = suppliedbutunverified (`streams[V-A].facts.composition`)
- On drawing: Supplied candidate fact, basis unverified: V-A flow = 5 (`streams[V-A].facts.flow`)
- On drawing: Supplied candidate fact, basis unverified: V-A flow_unit = kg/h (`streams[V-A].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: V-A quality = declaredgoodunverified (`streams[V-A].facts.quality`)
- On drawing: Supplied candidate fact, basis unverified: V-A sample_period = fictionalinterval (`streams[V-A].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: V-A measurement_basis = suppliedexistingmeter (`streams[V-A].facts.measurement_basis`)

**Data to collect**

- Flare or vent flow and composition [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): V-A (stream:V-A) fictional_record = true [streams[V-A].facts.fictional_record]; V-A (stream:V-A) record_source = "Fictional pre-call record, no company or human approval" [streams[V-A].facts.record_source]; V-A (stream:V-A) record_revision = "R1" [streams[V-A].facts.record_revision]; V-A (stream:V-A) record_available = true [streams[V-A].facts.record_available]; V-A (stream:V-A) record_authority = "unverified" [streams[V-A].facts.record_authority]; V-A (stream:V-A) record_scope = "currentdeclaredV-A" [streams[V-A].facts.record_scope]; V-A (stream:V-A) service = "processgas" [streams[V-A].facts.service]; V-A (stream:V-A) event_mode = "plannedintermittent+background" [streams[V-A].facts.event_mode]; V-A (stream:V-A) composition = "suppliedbutunverified" [streams[V-A].facts.composition]; V-A (stream:V-A) flow = 5 [streams[V-A].facts.flow]; V-A (stream:V-A) flow_unit = "kg/h" [streams[V-A].facts.flow_unit]; V-A (stream:V-A) quality = "declaredgoodunverified" [streams[V-A].facts.quality]; V-A (stream:V-A) sample_period = "fictionalinterval" [streams[V-A].facts.sample_period]; V-A (stream:V-A) measurement_basis = "suppliedexistingmeter" [streams[V-A].facts.measurement_basis]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact service/path and measurement/source/event associations; quantity/rate/total/reference units, sample periods and quality/availability/gaps, composition/variability and planned intermittent/continuous versus upset/blowdown/relief records, purge/pilot/manufacturer requirements and safety/environmental basis.; then site records: Review existing relief-valve lift, flare/vent and operating-event records with their actual time/source coverage.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Same-stream flow labeling is useful candidate evidence, not complete current flow/composition/event coverage. Retain foreign, inaccessible, FAULT or unqualified totalizer data without treating it as suitable. S19 printed34-35 distinguishes planned intermittent/continuous background from upset-blowdown and describes manufacturer minimum-flow context; rare relief events or a zero lift count alone do not automatically close source/safety/environmental review. Review suitable existing records first; no generic analyzer or meter closes all quantities. Any additional measurement/recovery proposal must preserve safety paths and undergo responsible hazard/environmental review, not be imposed from a drawing clue.

**How it is decided:** Review exact relief/vent/flare service, planned and abnormal event coverage and usable quantity/composition/time/source records with the responsible safety/environmental and operating specialists. A flow candidate or rare-event label does not establish suitable data, completeness or safe closure. Existing appropriate records/nonapplicability can be acknowledged; unresolved evidence remains explicit. No live metering, recovery modification, reduced purge/minimum flow or operating change is authorized.

**What the source says (S19):** S19 reports that background flaring in offshore cases can be as much as50% of all flared gas, while refinery shares generally depend on individual practices and are lower. This historical reported share is neither a recovery fraction nor a site benefit or a reason to compromise required flare operation.

**Limits:** Source review: S19 originalLBNL56183 printed34-35/PDF42-43 full flaregas section. Offshore versus refinery source scope, planned/intermittent/continuous versus upset/blowdown and manufacturer minimum-flow context retained. Existing dryer/oven/fryer/exhaust-air exclusions remain. Relief paths are safety systems; additional observation, metering or recovery changes require appropriate hazard/environmental review, not automatic closure from rare operation or an inferred saving.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
