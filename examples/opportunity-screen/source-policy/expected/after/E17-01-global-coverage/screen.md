# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/source-policy/models/E17-01-global-coverage.json`. Questions: `data/questions.json`.

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

### E17: What do existing records establish about this heating candidate's actual fired/flue service, recovery coverage and remaining compatible duty?

**About:** F-A  

**Finding reference (JSON string):** `"E17@F-A"`
**Asset IDs (JSON array):** `["F-A", "HX-A"]`

**Evidence on the drawing / model**

- equipment F-A reads "F-A Fictional FURNACE" (`units[F-A]`)
- Unverified recovery record; coverage not inferred: equipment HX-A reads "HX-A FURNACE RECUPERATOR sourceA" (`units[HX-A]`)
- Supplied candidate field: `"F-A fictional_record = true; present; meaning and suitability unverified"` (`"units[F-A].facts.fictional_record"`)
- Supplied candidate field: `"F-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[F-A].facts.record_source"`)
- Supplied candidate field: `"F-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[F-A].facts.record_revision"`)
- Supplied candidate field: `"F-A record_available = true; present; meaning and suitability unverified"` (`"units[F-A].facts.record_available"`)
- Supplied candidate field: `"F-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[F-A].facts.record_authority"`)
- Supplied candidate field: `"F-A service = \"firedflue\"; present; meaning and suitability unverified"` (`"units[F-A].facts.service"`)
- Supplied candidate field: `"F-A existing_recovery = \"suppliedrecoveryforAonly\"; present; meaning and suitability unverified"` (`"units[F-A].facts.existing_recovery"`)
- Supplied candidate field: `"HX-A fictional_record = true; present; meaning and suitability unverified"` (`"units[HX-A].facts.fictional_record"`)
- Supplied candidate field: `"HX-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.record_source"`)
- Supplied candidate field: `"HX-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.record_revision"`)
- Supplied candidate field: `"HX-A record_available = false; present; meaning and suitability unverified"` (`"units[HX-A].facts.record_available"`)
- Supplied candidate field: `"HX-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.record_authority"`)
- Supplied candidate field: `"HX-A target_subject = \"F-Aforeignsite\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.target_subject"`)
- On drawing: Supplied candidate fact, basis unverified: F-A fictional_record = True (`units[F-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: F-A record_source = Fictional development record; no company or human approval (`units[F-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: F-A record_revision = R1 (`units[F-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: F-A record_available = True (`units[F-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: F-A record_authority = unverified (`units[F-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: F-A service = firedflue (`units[F-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: F-A existing_recovery = suppliedrecoveryforAonly (`units[F-A].facts.existing_recovery`)
- On drawing: Supplied candidate fact, basis unverified: F-A fictional_record = True (`units[F-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: F-A record_source = Fictional development record; no company or human approval (`units[F-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: F-A record_revision = R1 (`units[F-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: F-A record_available = True (`units[F-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: F-A record_authority = unverified (`units[F-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: F-A service = firedflue (`units[F-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: F-A existing_recovery = suppliedrecoveryforAonly (`units[F-A].facts.existing_recovery`)

**Data to collect**

- Existing actual heating/flue service and recovery/loss-reduction coverage [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): F-A (F-A) fictional_record = true [units[F-A].facts.fictional_record]; F-A (F-A) record_source = "Fictional development record; no company or human approval" [units[F-A].facts.record_source]; F-A (F-A) record_revision = "R1" [units[F-A].facts.record_revision]; F-A (F-A) record_available = true [units[F-A].facts.record_available]; F-A (F-A) record_authority = "unverified" [units[F-A].facts.record_authority]; F-A (F-A) service = "firedflue" [units[F-A].facts.service]; F-A (F-A) existing_recovery = "suppliedrecoveryforAonly" [units[F-A].facts.existing_recovery]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-subject service, heat source and flue/recovery routing, installed function/coverage, prior loss-reduction and source/revision/availability records.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A heating name is not proof of combustion or hot gas vented straight to a stack. One recovery label anywhere does not settle another subject or demonstrate complete useful coverage. Known noncombustion/electric and typed recovery helpers are not fired subjects; unknown service remains conditional without inventing fuel or flue flow. Review existing suitable function and avoidable losses first, acknowledging suitable coverage or nonapplicability before further work.
- Existing source/receiving duty, schedule and feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): F-A (F-A) fictional_record = true [units[F-A].facts.fictional_record]; F-A (F-A) record_source = "Fictional development record; no company or human approval" [units[F-A].facts.record_source]; F-A (F-A) record_revision = "R1" [units[F-A].facts.record_revision]; F-A (F-A) record_available = true [units[F-A].facts.record_available]; F-A (F-A) record_authority = "unverified" [units[F-A].facts.record_authority]; F-A (F-A) service = "firedflue" [units[F-A].facts.service]; F-A (F-A) existing_recovery = "suppliedrecoveryforAonly" [units[F-A].facts.existing_recovery]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual exhaust temperature/flow/composition/cleanliness, load and operating schedule, receiving air/water/steam/load requirements, compatibility/timing and practical/material/economic constraints, with exact units/time/source coverage.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: S18 distinguishes combustion-air, steam/water and load-preheating methods. A continuous-load-preheating preference does not exclude every batch recovery option: waste-heat steam is available only while its fired source operates, and useful receiving duty must match. Hot/clean gas, proximity, a source example or an unconverted value alone does not authorize recovery equipment, field tests or site savings. Suitable existing records can be acknowledged.

**How it is decided:** Review actual heating/flue service, existing recovery and prior loss-reduction coverage, source/receiving duty and operating schedules with the responsible engineer. Do not infer installed absence or wasted heat from names or global labels, and do not automatically close batch service or prescribe a retrofit from a continuous/clean pattern. Suitable existing basis or nonapplicability may be acknowledged; unresolved source, function, time or units remains a records question.

**What the source says (S18, S24):** "Energy consumption can typically be reduced 5% to 30%." Load preheating is "best suited for continuous rather than batch furnaces."
IAC/ITAC recommendation code: 2.241x (IAC/ITAC browse page: 1,936 recommendations, 2.0 yr average payback, 20.0% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S18 process-heating Tip8 pp1-2 distinguishes recovery methods, prior loss reduction and operating constraints; S4 Tip3 pp1-2 additionally bounds boiler-flue/feedwater function. Source 5%-30% is contextual historical guidance, not this subject's measured savings. Named records and capabilities are unverified candidates.

### E17: What do existing records establish about this heating candidate's actual fired/flue service, recovery coverage and remaining compatible duty?

**About:** F-B  

**Finding reference (JSON string):** `"E17@F-B"`
**Asset IDs (JSON array):** `["F-B", "HX-A"]`

**Evidence on the drawing / model**

- equipment F-B reads "F-B Fictional FURNACE" (`units[F-B]`)
- Unverified recovery record; coverage not inferred: equipment HX-A reads "HX-A FURNACE RECUPERATOR sourceA" (`units[HX-A]`)
- Supplied candidate field: `"F-B fictional_record = true; present; meaning and suitability unverified"` (`"units[F-B].facts.fictional_record"`)
- Supplied candidate field: `"F-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[F-B].facts.record_source"`)
- Supplied candidate field: `"F-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[F-B].facts.record_revision"`)
- Supplied candidate field: `"F-B record_available = true; present; meaning and suitability unverified"` (`"units[F-B].facts.record_available"`)
- Supplied candidate field: `"F-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[F-B].facts.record_authority"`)
- Supplied candidate field: `"F-B service = \"firedflue\"; present; meaning and suitability unverified"` (`"units[F-B].facts.service"`)
- Supplied candidate field: `"F-B existing_recovery = null; blank; meaning and suitability unverified"` (`"units[F-B].facts.existing_recovery"`)
- Supplied candidate field: `"HX-A fictional_record = true; present; meaning and suitability unverified"` (`"units[HX-A].facts.fictional_record"`)
- Supplied candidate field: `"HX-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.record_source"`)
- Supplied candidate field: `"HX-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.record_revision"`)
- Supplied candidate field: `"HX-A record_available = false; present; meaning and suitability unverified"` (`"units[HX-A].facts.record_available"`)
- Supplied candidate field: `"HX-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.record_authority"`)
- Supplied candidate field: `"HX-A target_subject = \"F-Aforeignsite\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.target_subject"`)
- On drawing: Supplied candidate fact, basis unverified: F-B fictional_record = True (`units[F-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_source = Fictional development record; no company or human approval (`units[F-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_revision = R1 (`units[F-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_available = True (`units[F-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_authority = unverified (`units[F-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: F-B service = firedflue (`units[F-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: F-B fictional_record = True (`units[F-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_source = Fictional development record; no company or human approval (`units[F-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_revision = R1 (`units[F-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_available = True (`units[F-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: F-B record_authority = unverified (`units[F-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: F-B service = firedflue (`units[F-B].facts.service`)

**Data to collect**

- Existing actual heating/flue service and recovery/loss-reduction coverage [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): F-B (F-B) fictional_record = true [units[F-B].facts.fictional_record]; F-B (F-B) record_source = "Fictional development record; no company or human approval" [units[F-B].facts.record_source]; F-B (F-B) record_revision = "R1" [units[F-B].facts.record_revision]; F-B (F-B) record_available = true [units[F-B].facts.record_available]; F-B (F-B) record_authority = "unverified" [units[F-B].facts.record_authority]; F-B (F-B) service = "firedflue" [units[F-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-subject service, heat source and flue/recovery routing, installed function/coverage, prior loss-reduction and source/revision/availability records.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A heating name is not proof of combustion or hot gas vented straight to a stack. One recovery label anywhere does not settle another subject or demonstrate complete useful coverage. Known noncombustion/electric and typed recovery helpers are not fired subjects; unknown service remains conditional without inventing fuel or flue flow. Review existing suitable function and avoidable losses first, acknowledging suitable coverage or nonapplicability before further work.
- Existing source/receiving duty, schedule and feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): F-B (F-B) fictional_record = true [units[F-B].facts.fictional_record]; F-B (F-B) record_source = "Fictional development record; no company or human approval" [units[F-B].facts.record_source]; F-B (F-B) record_revision = "R1" [units[F-B].facts.record_revision]; F-B (F-B) record_available = true [units[F-B].facts.record_available]; F-B (F-B) record_authority = "unverified" [units[F-B].facts.record_authority]; F-B (F-B) service = "firedflue" [units[F-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual exhaust temperature/flow/composition/cleanliness, load and operating schedule, receiving air/water/steam/load requirements, compatibility/timing and practical/material/economic constraints, with exact units/time/source coverage.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: S18 distinguishes combustion-air, steam/water and load-preheating methods. A continuous-load-preheating preference does not exclude every batch recovery option: waste-heat steam is available only while its fired source operates, and useful receiving duty must match. Hot/clean gas, proximity, a source example or an unconverted value alone does not authorize recovery equipment, field tests or site savings. Suitable existing records can be acknowledged.

**How it is decided:** Review actual heating/flue service, existing recovery and prior loss-reduction coverage, source/receiving duty and operating schedules with the responsible engineer. Do not infer installed absence or wasted heat from names or global labels, and do not automatically close batch service or prescribe a retrofit from a continuous/clean pattern. Suitable existing basis or nonapplicability may be acknowledged; unresolved source, function, time or units remains a records question.

**What the source says (S18, S24):** "Energy consumption can typically be reduced 5% to 30%." Load preheating is "best suited for continuous rather than batch furnaces."
IAC/ITAC recommendation code: 2.241x (IAC/ITAC browse page: 1,936 recommendations, 2.0 yr average payback, 20.0% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S18 process-heating Tip8 pp1-2 distinguishes recovery methods, prior loss reduction and operating constraints; S4 Tip3 pp1-2 additionally bounds boiler-flue/feedwater function. Source 5%-30% is contextual historical guidance, not this subject's measured savings. Named records and capabilities are unverified candidates.

## Sources cited above

- S18: Process Heating Tip #8, Install Waste Heat Recovery Systems for Fuel-Fired Furnaces (DOE/GO-102005-2181, Sep 2005). https://www.energy.gov/sites/prod/files/2014/05/f16/install_waste_heat_process_htgts8.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
