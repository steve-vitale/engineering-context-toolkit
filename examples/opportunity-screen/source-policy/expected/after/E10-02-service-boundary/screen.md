# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/source-policy/models/E10-02-service-boundary.json`. Questions: `data/questions.json`.

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

### E10: What do existing records establish about this flash-vessel candidate's actual service, vent/recovery route and compatible low-pressure duty?

**About:** F-B  

**Finding reference (JSON string):** `"E10@F-B"`
**Asset IDs (JSON array):** `["F-B"]`

**Evidence on the drawing / model**

- equipment F-B reads "F-B FLASH VESSEL water" (`units[F-B]`)
- Supplied candidate field: `"F-B fictional_record = true; present; meaning and suitability unverified"` (`"units[F-B].facts.fictional_record"`)
- Supplied candidate field: `"F-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[F-B].facts.record_source"`)
- Supplied candidate field: `"F-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[F-B].facts.record_revision"`)
- Supplied candidate field: `"F-B record_available = true; present; meaning and suitability unverified"` (`"units[F-B].facts.record_available"`)
- Supplied candidate field: `"F-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[F-B].facts.record_authority"`)
- Supplied candidate field: `"F-B service = \"steamwatercondensate\"; present; meaning and suitability unverified"` (`"units[F-B].facts.service"`)
- Supplied candidate field: `"F-B pressure = 200; present; meaning and suitability unverified"` (`"units[F-B].facts.pressure"`)
- Supplied candidate field: `"F-B pressure_unit = \"designratingnotoperating\"; present; meaning and suitability unverified"` (`"units[F-B].facts.pressure_unit"`)
- Supplied candidate field: `"F-B flow = 5000; present; meaning and suitability unverified"` (`"units[F-B].facts.flow"`)
- Supplied candidate field: `"F-B flow_unit = \"lb/hr\"; present; meaning and suitability unverified"` (`"units[F-B].facts.flow_unit"`)
- Supplied candidate field: `"F-B sample_period = null; blank; meaning and suitability unverified"` (`"units[F-B].facts.sample_period"`)
- On drawing: Supplied candidate fact, basis unverified: F-B fictional_record = True (`units[F-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_source = Fictional development record; no company or human approval (`units[F-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_revision = R1 (`units[F-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_available = True (`units[F-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_authority = unverified (`units[F-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: F-B service = steamwatercondensate (`units[F-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: F-B pressure = 200 (`units[F-B].facts.pressure`)
- On drawing: Supplied candidate fact, basis unverified: F-B pressure_unit = designratingnotoperating (`units[F-B].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: F-B flow = 5000 (`units[F-B].facts.flow`)
- On drawing: Supplied candidate fact, basis unverified: F-B flow_unit = lb/hr (`units[F-B].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: F-B fictional_record = True (`units[F-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_source = Fictional development record; no company or human approval (`units[F-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_revision = R1 (`units[F-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_available = True (`units[F-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_authority = unverified (`units[F-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: F-B service = steamwatercondensate (`units[F-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: F-B pressure = 200 (`units[F-B].facts.pressure`)
- On drawing: Supplied candidate fact, basis unverified: F-B pressure_unit = designratingnotoperating (`units[F-B].facts.pressure_unit`)
- On drawing: Supplied candidate fact, basis unverified: F-B flow = 5000 (`units[F-B].facts.flow`)
- On drawing: Supplied candidate fact, basis unverified: F-B flow_unit = lb/hr (`units[F-B].facts.flow_unit`)

**Data to collect**

- Existing source-specific condensate service, vent/recovery and actual operating basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): F-B (F-B) fictional_record = true [units[F-B].facts.fictional_record]; F-B (F-B) record_source = "Fictional development record; no company or human approval" [units[F-B].facts.record_source]; F-B (F-B) record_revision = "R1" [units[F-B].facts.record_revision]; F-B (F-B) record_available = true [units[F-B].facts.record_available]; F-B (F-B) record_authority = "unverified" [units[F-B].facts.record_authority]; F-B (F-B) service = "steamwatercondensate" [units[F-B].facts.service]; F-B (F-B) pressure = 200 [units[F-B].facts.pressure]; F-B (F-B) pressure_unit = "designratingnotoperating" [units[F-B].facts.pressure_unit]; F-B (F-B) flow = 5000 [units[F-B].facts.flow]; F-B (F-B) flow_unit = "lb/hr" [units[F-B].facts.flow_unit]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-vessel/condensate source service and current vent/recovery/route records, actual pressure/temperature, flow and duration with quantity/units, sample time, revision, availability and operating coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A FLASH TANK/VESSEL/DRUM label is not proof of steam-water service, atmospheric venting, measured steam loss or an unused recovery opportunity. Establish actual current function and distinguish known nonsteam/hydrocarbon context from unknown applicable service. Review suitable existing recovery before requesting more data; pressure ratings or a plume alone do not establish a flash fraction or source quality.
- Existing compatible receiving-duty, association and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): F-B (F-B) fictional_record = true [units[F-B].facts.fictional_record]; F-B (F-B) record_source = "Fictional development record; no company or human approval" [units[F-B].facts.record_source]; F-B (F-B) record_revision = "R1" [units[F-B].facts.record_revision]; F-B (F-B) record_available = true [units[F-B].facts.record_available]; F-B (F-B) record_authority = "unverified" [units[F-B].facts.record_authority]; F-B (F-B) service = "steamwatercondensate" [units[F-B].facts.service]; F-B (F-B) pressure = 200 [units[F-B].facts.pressure]; F-B (F-B) pressure_unit = "designratingnotoperating" [units[F-B].facts.pressure_unit]; F-B (F-B) flow = 5000 [units[F-B].facts.flow]; F-B (F-B) flow_unit = "lb/hr" [units[F-B].facts.flow_unit]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-source low-pressure user pressure/quality, flow/heat duty and operating-time requirements, piping/route/distance and system/practical/economic constraints.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Review actual source/receiving pressure, timing and compatible duty together; a nearby or foreign/seasonal low-pressure label is not a matched sink. Supplemental original DOE Tip12 pp1–2 requires flow/duration, compatible uses and cost-effective equipment/piping, with return alternatives and availability/use considered. Acknowledge an existing suitable route or nonapplicability without a new field task. No recovery installation, physical connection, flash calculation or site savings follow from this screen.

**How it is decided:** Review actual steam-water condensate service, current vent/recovery and matched source/receiving duty, routing and economic constraints with the responsible engineer. Steady flow or a close low-pressure label alone does not establish unused recoverable steam or justify hardware/operating changes. Suitable existing recovery or nonapplicability may be acknowledged; unknown route, units, source or timing remains a qualified records question.

**What the source says (S8, S24):** Flash vessels allow "recovery of steam... used in low-pressure steam applications." No % stated.
IAC/ITAC recommendation code: 2.2127 (IAC/ITAC browse page: 31 recommendations, 1.0 yr average payback, 39.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S8 printed21 and supplemental original DOE Tip12 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam12_lowpressure_steam.pdf), completepp1–2, admitted before criteria. Its pressure/flow/duty/economic example is not this site's result. Missing representation is not installed absence.

## Sources cited above

- S8: Improving Steam System Performance: A Sourcebook for Industry, 2nd ed. (DOE/GO-102012-3423, rev. Oct 2012). https://www.energy.gov/sites/prod/files/2014/05/f15/steamsourcebook.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
