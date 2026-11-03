# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/source-policy/models/E21-01-cyclic-vacuum.json`. Questions: `data/questions.json`.

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

### E21: What do existing records establish about these air-labelled end-use candidates, their required function and any suitable alternative?

**About:** V-A, V-B  

**Finding reference (JSON string):** `"E21@model"`
**Asset IDs (JSON array):** `["V-A", "V-B"]`

**Evidence on the drawing / model**

- equipment V-A reads "V-A AIR VENTURI vacuum" (`units[V-A]`)
- equipment V-B reads "V-B AIR VENTURI vacuum" (`units[V-B]`)
- Supplied candidate field: `"V-A fictional_record = true; present; meaning and suitability unverified"` (`"units[V-A].facts.fictional_record"`)
- Supplied candidate field: `"V-A record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[V-A].facts.record_source"`)
- Supplied candidate field: `"V-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[V-A].facts.record_revision"`)
- Supplied candidate field: `"V-A record_available = true; present; meaning and suitability unverified"` (`"units[V-A].facts.record_available"`)
- Supplied candidate field: `"V-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[V-A].facts.record_authority"`)
- Supplied candidate field: `"V-A service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[V-A].facts.service"`)
- Supplied candidate field: `"V-A end_use = \"cyclicvacuum\"; present; meaning and suitability unverified"` (`"units[V-A].facts.end_use"`)
- Supplied candidate field: `"V-A duty_percent = 20; present; meaning and suitability unverified"` (`"units[V-A].facts.duty_percent"`)
- Supplied candidate field: `"V-A shutoff_control = true; present; meaning and suitability unverified"` (`"units[V-A].facts.shutoff_control"`)
- Supplied candidate field: `"V-A safety_function = \"declaredsparkingconstraint, notapproved\"; present; meaning and suitability unverified"` (`"units[V-A].facts.safety_function"`)
- Supplied candidate field: `"V-A lifecycle_basis = null; blank; meaning and suitability unverified"` (`"units[V-A].facts.lifecycle_basis"`)
- Supplied candidate field: `"V-B fictional_record = true; present; meaning and suitability unverified"` (`"units[V-B].facts.fictional_record"`)
- Supplied candidate field: `"V-B record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[V-B].facts.record_source"`)
- Supplied candidate field: `"V-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[V-B].facts.record_revision"`)
- Supplied candidate field: `"V-B record_available = true; present; meaning and suitability unverified"` (`"units[V-B].facts.record_available"`)
- Supplied candidate field: `"V-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[V-B].facts.record_authority"`)
- Supplied candidate field: `"V-B service = null; blank; meaning and suitability unverified"` (`"units[V-B].facts.service"`)
- Supplied candidate field: `"V-B end_use = \"unknownvacuum\"; present; meaning and suitability unverified"` (`"units[V-B].facts.end_use"`)
- Supplied candidate field: `"V-B duty_percent = null; blank; meaning and suitability unverified"` (`"units[V-B].facts.duty_percent"`)
- Supplied candidate field: `"V-B shutoff_control = null; blank; meaning and suitability unverified"` (`"units[V-B].facts.shutoff_control"`)
- On drawing: Supplied candidate fact, basis unverified: V-A fictional_record = True (`units[V-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: V-B fictional_record = True (`units[V-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_source = Fictional pre-call development record, no company or human approval (`units[V-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: V-B record_source = Fictional pre-call development record, no company or human approval (`units[V-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_revision = R1 (`units[V-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: V-B record_revision = R1 (`units[V-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_available = True (`units[V-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: V-B record_available = True (`units[V-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: V-A record_authority = unverified (`units[V-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: V-B record_authority = unverified (`units[V-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: V-A service = compressedair (`units[V-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: V-A end_use = cyclicvacuum (`units[V-A].facts.end_use`)
- On drawing: Supplied candidate fact, basis unverified: V-B end_use = unknownvacuum (`units[V-B].facts.end_use`)
- On drawing: Supplied candidate fact, basis unverified: V-A duty_percent = 20 (`units[V-A].facts.duty_percent`)
- On drawing: Supplied candidate fact, basis unverified: V-A shutoff_control = True (`units[V-A].facts.shutoff_control`)
- On drawing: Supplied candidate fact, basis unverified: V-A safety_function = declaredsparkingconstraint, notapproved (`units[V-A].facts.safety_function`)

**Data to collect**

- Existing end-use, function, demand and alternative/lifecycle basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): V-A (V-A) fictional_record = true [units[V-A].facts.fictional_record]; V-B (V-B) fictional_record = true [units[V-B].facts.fictional_record]; V-A (V-A) record_source = "Fictional pre-call development record, no company or human approval" [units[V-A].facts.record_source]; V-B (V-B) record_source = "Fictional pre-call development record, no company or human approval" [units[V-B].facts.record_source]; V-A (V-A) record_revision = "R1" [units[V-A].facts.record_revision]; V-B (V-B) record_revision = "R1" [units[V-B].facts.record_revision]; V-A (V-A) record_available = true [units[V-A].facts.record_available]; V-B (V-B) record_available = true [units[V-B].facts.record_available]; V-A (V-A) record_authority = "unverified" [units[V-A].facts.record_authority]; V-B (V-B) record_authority = "unverified" [units[V-B].facts.record_authority]; V-A (V-A) service = "compressedair" [units[V-A].facts.service]; V-A (V-A) end_use = "cyclicvacuum" [units[V-A].facts.end_use]; V-B (V-B) end_use = "unknownvacuum" [units[V-B].facts.end_use]; V-A (V-A) duty_percent = 20 [units[V-A].facts.duty_percent]; V-A (V-A) shutoff_control = true [units[V-A].facts.shutoff_control]; V-A (V-A) safety_function = "declaredsparkingconstraint, notapproved" [units[V-A].facts.safety_function]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact end-use/system and compressed-air service, process and safety purpose, required quality/pressure/flow and duty/load pattern, shutoff/control and current solution, source/owner/revision/availability and lifecycle/system constraints.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S11 printed24-27 describes potentially inappropriate uses and context-dependent alternatives, not an equipment replacement instruction from a name. Establish actual compressed-air service and task requirements. Cabinet cooling is not protective panel purging. Intermittent/cyclic vacuum with suitable control and safety/practical constraints can justify a venturi; a generic load-factor example alone does not decide this installation or establish a central-pump alternative. Review existing suitable arrangements and full-system/lifecycle implications with the responsible specialist. Retain foreign, missing, zero and uncertain values; no blanket blower/fan/pump substitution or compulsory new survey follows.

**How it is decided:** Review actual compressed-air end-use/function, safety and quality requirements, matched demand/control records and practical lifecycle/system alternatives with the responsible specialist. A source list of potentially inappropriate uses is a collection prompt, not proof of waste. Suitable existing use or nonapplicability can be acknowledged; unknown service, scope or duty remains explicit without mandatory replacement or transferred source savings.

**What the source says (S11, S24):** S11 identifies potentially inappropriate compressed-air uses and discusses task-specific alternatives and lifecycle/system tradeoffs. The pressure-sensitive unregulated-demand share is not the fraction removable by substitution. No generic end-use saving, avoidable share or site benefit is asserted.
IAC/ITAC recommendation code: 2.4239; 2.4237; 2.4238 (IAC/ITAC browse page: 2.4239: 2,697 recommendations, 1.0 yr average payback, 48.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S11 printed24-27/PDF29-32 includes intermittent vacuum and explicitly distinguishes cabinet cooling from panel purging. Its historical unregulated-demand percentage concerns pressure-sensitive demand, not automatically inappropriate use, retrofit eligibility or savings. Known non-compressed-air and protective-purge roles are not cooling/sparging/vacuum subjects; unknown service is conditional.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
