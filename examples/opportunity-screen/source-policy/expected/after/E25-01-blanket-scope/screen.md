# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/source-policy/models/E25-01-blanket-scope.json`. Questions: `data/questions.json`.

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
| Emissions | 2 |
| Safety questions to verify | 0 |

## Emissions

### E25: What do existing records establish about this tank/vent candidate's actual product, vapor sources and recovery/control coverage?

**About:** TK-A  

**Finding reference (JSON string):** `"E25@TK-A"`
**Asset IDs (JSON array):** `["TK-A", "BG-X"]`

**Evidence on the drawing / model**

- equipment TK-A reads "TK-A TANK TO ATM" (`units[TK-A]`)
- Unverified recovery/blanketing record; actual capture and tank coverage not established: equipment BG-X reads "BG-X BLANKET GAS" (`units[BG-X]`)
- Supplied candidate field: `"TK-A fictional_record = true; present; meaning and suitability unverified"` (`"units[TK-A].facts.fictional_record"`)
- Supplied candidate field: `"TK-A record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[TK-A].facts.record_source"`)
- Supplied candidate field: `"TK-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[TK-A].facts.record_revision"`)
- Supplied candidate field: `"TK-A record_available = true; present; meaning and suitability unverified"` (`"units[TK-A].facts.record_available"`)
- Supplied candidate field: `"TK-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[TK-A].facts.record_authority"`)
- Supplied candidate field: `"TK-A service = \"hydrocarbonunknown\"; present; meaning and suitability unverified"` (`"units[TK-A].facts.service"`)
- Supplied candidate field: `"TK-A existing_recovery = null; blank; meaning and suitability unverified"` (`"units[TK-A].facts.existing_recovery"`)
- Supplied candidate field: `"BG-X fictional_record = true; present; meaning and suitability unverified"` (`"units[BG-X].facts.fictional_record"`)
- Supplied candidate field: `"BG-X record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_source"`)
- Supplied candidate field: `"BG-X record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_revision"`)
- Supplied candidate field: `"BG-X record_available = false; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_available"`)
- Supplied candidate field: `"BG-X record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_authority"`)
- Supplied candidate field: `"BG-X record_scope = \"foreignTK-C\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_scope"`)
- Supplied candidate field: `"BG-X blanketing_purpose = \"inertatmosphere, notvaporcapture\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.blanketing_purpose"`)
- On drawing: Supplied candidate fact, basis unverified: TK-A fictional_record = True (`units[TK-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_source = Fictional pre-call record, no company or human approval (`units[TK-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_revision = R1 (`units[TK-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_available = True (`units[TK-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_authority = unverified (`units[TK-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TK-A service = hydrocarbonunknown (`units[TK-A].facts.service`)

**Data to collect**

- Vapor volume and composition [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TK-A (TK-A) fictional_record = true [units[TK-A].facts.fictional_record]; TK-A (TK-A) record_source = "Fictional pre-call record, no company or human approval" [units[TK-A].facts.record_source]; TK-A (TK-A) record_revision = "R1" [units[TK-A].facts.record_revision]; TK-A (TK-A) record_available = true [units[TK-A].facts.record_available]; TK-A (TK-A) record_authority = "unverified" [units[TK-A].facts.record_authority]; TK-A (TK-A) service = "hydrocarbonunknown" [units[TK-A].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact tank/product/composition and vent/control/recovery source associations, current service and upstream/tank pressure-temperature/throughput/ambient cycles, flash/working/standing loss sources, quantity/rate/reference/peak-versus-total/uncertainty basis and compatible outlet/operability/environmental constraints.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A blanket-gas label is not vapor recovery, and a VRU record elsewhere cannot settle this tank's actual capture/coverage. S20 concerns crudeoil/condensate storage: known clean potable-water or inert-only service can be nonapplicable, but unknown or produced-water service must not be declared clean merely by name. Review existing qualified measurements/estimates and their limits before proposing new observations. EPA's simple GOR/throughput example does not provide composition/speciation, low-pressure total-volume metering or verified peak duty; actual pressure/temperature/composition/time and outlet matter. Suitable existing controls can be acknowledged. Any new sample, vent measurement or recovery change requires responsible safety/environmental review, not a generic instruction from this screen.

**How it is decided:** Review actual product/vent/loss-source and existing control/recovery coverage, qualified quantity/composition/peak/time basis, compatible outlet and operating/environmental constraints with the responsible specialist. Blanketing or another VRU label is not proof of capture or global coverage. Suitable current control or nonapplicability can be acknowledged; unresolved service/source/duty remains explicit without mandated sampling, recovery equipment or site payback.

**What the source says (S20):** S20 reports high hydrocarbon-vapor capture and partner economics for particular crude-oil/condensate storage-tank VRU applications. These historical examples depend on vapor source, quantity/composition, operating conditions and a suitable outlet; no universal recovery fraction, payback or site benefit is assigned.

**Limits:** Source review: complete S20 EPA NaturalGasSTAR LessonsLearned Oct2006 pp1-9. Original95%/two-month headline remains historical; partner reports/examples are not this tank's verified capture or economics. Flash/working/standing and maximum versus total emissions differ; low tank pressures, control/vacuum prevention and outlet constraints matter. Additional measurement/sampling/design or emission-control decisions need applicable safety/environmental review. No current legal compliance or installed emissions are determined.

### E25: What do existing records establish about this tank/vent candidate's actual product, vapor sources and recovery/control coverage?

**About:** TK-B  

**Finding reference (JSON string):** `"E25@TK-B"`
**Asset IDs (JSON array):** `["TK-B", "BG-X"]`

**Evidence on the drawing / model**

- equipment TK-B reads "TK-B TANK TO ATM" (`units[TK-B]`)
- Unverified recovery/blanketing record; actual capture and tank coverage not established: equipment BG-X reads "BG-X BLANKET GAS" (`units[BG-X]`)
- Supplied candidate field: `"TK-B fictional_record = true; present; meaning and suitability unverified"` (`"units[TK-B].facts.fictional_record"`)
- Supplied candidate field: `"TK-B record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[TK-B].facts.record_source"`)
- Supplied candidate field: `"TK-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[TK-B].facts.record_revision"`)
- Supplied candidate field: `"TK-B record_available = true; present; meaning and suitability unverified"` (`"units[TK-B].facts.record_available"`)
- Supplied candidate field: `"TK-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[TK-B].facts.record_authority"`)
- Supplied candidate field: `"TK-B service = null; blank; meaning and suitability unverified"` (`"units[TK-B].facts.service"`)
- Supplied candidate field: `"BG-X fictional_record = true; present; meaning and suitability unverified"` (`"units[BG-X].facts.fictional_record"`)
- Supplied candidate field: `"BG-X record_source = \"Fictional pre-call record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_source"`)
- Supplied candidate field: `"BG-X record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_revision"`)
- Supplied candidate field: `"BG-X record_available = false; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_available"`)
- Supplied candidate field: `"BG-X record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_authority"`)
- Supplied candidate field: `"BG-X record_scope = \"foreignTK-C\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.record_scope"`)
- Supplied candidate field: `"BG-X blanketing_purpose = \"inertatmosphere, notvaporcapture\"; present; meaning and suitability unverified"` (`"units[BG-X].facts.blanketing_purpose"`)
- On drawing: Supplied candidate fact, basis unverified: TK-B fictional_record = True (`units[TK-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TK-B record_source = Fictional pre-call record, no company or human approval (`units[TK-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TK-B record_revision = R1 (`units[TK-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TK-B record_available = True (`units[TK-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TK-B record_authority = unverified (`units[TK-B].facts.record_authority`)

**Data to collect**

- Vapor volume and composition [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TK-B (TK-B) fictional_record = true [units[TK-B].facts.fictional_record]; TK-B (TK-B) record_source = "Fictional pre-call record, no company or human approval" [units[TK-B].facts.record_source]; TK-B (TK-B) record_revision = "R1" [units[TK-B].facts.record_revision]; TK-B (TK-B) record_available = true [units[TK-B].facts.record_available]; TK-B (TK-B) record_authority = "unverified" [units[TK-B].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact tank/product/composition and vent/control/recovery source associations, current service and upstream/tank pressure-temperature/throughput/ambient cycles, flash/working/standing loss sources, quantity/rate/reference/peak-versus-total/uncertainty basis and compatible outlet/operability/environmental constraints.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A blanket-gas label is not vapor recovery, and a VRU record elsewhere cannot settle this tank's actual capture/coverage. S20 concerns crudeoil/condensate storage: known clean potable-water or inert-only service can be nonapplicable, but unknown or produced-water service must not be declared clean merely by name. Review existing qualified measurements/estimates and their limits before proposing new observations. EPA's simple GOR/throughput example does not provide composition/speciation, low-pressure total-volume metering or verified peak duty; actual pressure/temperature/composition/time and outlet matter. Suitable existing controls can be acknowledged. Any new sample, vent measurement or recovery change requires responsible safety/environmental review, not a generic instruction from this screen.

**How it is decided:** Review actual product/vent/loss-source and existing control/recovery coverage, qualified quantity/composition/peak/time basis, compatible outlet and operating/environmental constraints with the responsible specialist. Blanketing or another VRU label is not proof of capture or global coverage. Suitable current control or nonapplicability can be acknowledged; unresolved service/source/duty remains explicit without mandated sampling, recovery equipment or site payback.

**What the source says (S20):** S20 reports high hydrocarbon-vapor capture and partner economics for particular crude-oil/condensate storage-tank VRU applications. These historical examples depend on vapor source, quantity/composition, operating conditions and a suitable outlet; no universal recovery fraction, payback or site benefit is assigned.

**Limits:** Source review: complete S20 EPA NaturalGasSTAR LessonsLearned Oct2006 pp1-9. Original95%/two-month headline remains historical; partner reports/examples are not this tank's verified capture or economics. Flash/working/standing and maximum versus total emissions differ; low tank pressures, control/vacuum prevention and outlet constraints matter. Additional measurement/sampling/design or emission-control decisions need applicable safety/environmental review. No current legal compliance or installed emissions are determined.

## Sources cited above

- S20: EPA Natural Gas STAR Lessons Learned, Installing Vapor Recovery Units on Storage Tanks. https://19january2017snapshot.epa.gov/sites/production/files/2016-06/documents/ll_final_vap.pdf (license: Public domain (archived EPA snapshot))
