# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/source-policy/models/E21-03-purpose-source.json`. Questions: `data/questions.json`.

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

**About:** S-A, B-B  

**Finding reference (JSON string):** `"E21@model"`
**Asset IDs (JSON array):** `["S-A", "B-B"]`

**Evidence on the drawing / model**

- equipment S-A reads "S-A AIR SPARGING" (`units[S-A]`)
- equipment B-B reads "B-B AIR BLOWING" (`units[B-B]`)
- Supplied candidate field: `"S-A fictional_record = true; present; meaning and suitability unverified"` (`"units[S-A].facts.fictional_record"`)
- Supplied candidate field: `"S-A record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[S-A].facts.record_source"`)
- Supplied candidate field: `"S-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[S-A].facts.record_revision"`)
- Supplied candidate field: `"S-A record_available = false; present; meaning and suitability unverified"` (`"units[S-A].facts.record_available"`)
- Supplied candidate field: `"S-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[S-A].facts.record_authority"`)
- Supplied candidate field: `"S-A record_scope = \"foreignS-A\"; present; meaning and suitability unverified"` (`"units[S-A].facts.record_scope"`)
- Supplied candidate field: `"S-A service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[S-A].facts.service"`)
- Supplied candidate field: `"S-A end_use = \"oxygenation/agitationunknown\"; present; meaning and suitability unverified"` (`"units[S-A].facts.end_use"`)
- Supplied candidate field: `"S-A quality_requirement = \"notreviewed\"; present; meaning and suitability unverified"` (`"units[S-A].facts.quality_requirement"`)
- Supplied candidate field: `"S-A flow = 0; present; meaning and suitability unverified"` (`"units[S-A].facts.flow"`)
- Supplied candidate field: `"S-A flow_unit = \"scfm,referenceunknown\"; present; meaning and suitability unverified"` (`"units[S-A].facts.flow_unit"`)
- Supplied candidate field: `"S-A pressure = 90; present; meaning and suitability unverified"` (`"units[S-A].facts.pressure"`)
- Supplied candidate field: `"S-A pressure_unit = \"psig\"; present; meaning and suitability unverified"` (`"units[S-A].facts.pressure_unit"`)
- Supplied candidate field: `"B-B fictional_record = true; present; meaning and suitability unverified"` (`"units[B-B].facts.fictional_record"`)
- Supplied candidate field: `"B-B record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_source"`)
- Supplied candidate field: `"B-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_revision"`)
- Supplied candidate field: `"B-B record_available = true; present; meaning and suitability unverified"` (`"units[B-B].facts.record_available"`)
- Supplied candidate field: `"B-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_authority"`)
- Supplied candidate field: `"B-B service = null; blank; meaning and suitability unverified"` (`"units[B-B].facts.service"`)
- Supplied candidate field: `"B-B end_use = \"unknown\"; blank; meaning and suitability unverified"` (`"units[B-B].facts.end_use"`)
- Supplied candidate field: `"B-B flow = null; blank; meaning and suitability unverified"` (`"units[B-B].facts.flow"`)
- Supplied candidate field: `"B-B process_requirement = null; blank; meaning and suitability unverified"` (`"units[B-B].facts.process_requirement"`)
- On drawing: Supplied candidate fact, basis unverified: S-A fictional_record = True (`units[S-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-B fictional_record = True (`units[B-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_source = Fictional pre-call development record, no company or human approval (`units[S-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_source = Fictional pre-call development record, no company or human approval (`units[B-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_revision = R1 (`units[S-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_revision = R1 (`units[B-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_available = False (`units[S-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_available = True (`units[B-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_authority = unverified (`units[S-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_authority = unverified (`units[B-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: S-A record_scope = foreignS-A (`units[S-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: S-A service = compressedair (`units[S-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: S-A end_use = oxygenation/agitationunknown (`units[S-A].facts.end_use`)
- On drawing: Supplied candidate fact, basis unverified: S-A quality_requirement = notreviewed (`units[S-A].facts.quality_requirement`)
- On drawing: Supplied candidate fact, basis unverified: S-A flow = 0 (`units[S-A].facts.flow`)
- On drawing: Supplied candidate fact, basis unverified: S-A flow_unit = scfm,referenceunknown (`units[S-A].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: S-A pressure = 90 (`units[S-A].facts.pressure`)
- On drawing: Supplied candidate fact, basis unverified: S-A pressure_unit = psig (`units[S-A].facts.pressure_unit`)

**Data to collect**

- Existing end-use, function, demand and alternative/lifecycle basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): S-A (S-A) fictional_record = true [units[S-A].facts.fictional_record]; B-B (B-B) fictional_record = true [units[B-B].facts.fictional_record]; S-A (S-A) record_source = "Fictional pre-call development record, no company or human approval" [units[S-A].facts.record_source]; B-B (B-B) record_source = "Fictional pre-call development record, no company or human approval" [units[B-B].facts.record_source]; S-A (S-A) record_revision = "R1" [units[S-A].facts.record_revision]; B-B (B-B) record_revision = "R1" [units[B-B].facts.record_revision]; S-A (S-A) record_available = false [units[S-A].facts.record_available]; B-B (B-B) record_available = true [units[B-B].facts.record_available]; S-A (S-A) record_authority = "unverified" [units[S-A].facts.record_authority]; B-B (B-B) record_authority = "unverified" [units[B-B].facts.record_authority]; S-A (S-A) record_scope = "foreignS-A" [units[S-A].facts.record_scope]; S-A (S-A) service = "compressedair" [units[S-A].facts.service]; S-A (S-A) end_use = "oxygenation/agitationunknown" [units[S-A].facts.end_use]; S-A (S-A) quality_requirement = "notreviewed" [units[S-A].facts.quality_requirement]; S-A (S-A) flow = 0 [units[S-A].facts.flow]; S-A (S-A) flow_unit = "scfm,referenceunknown" [units[S-A].facts.flow_unit]; S-A (S-A) pressure = 90 [units[S-A].facts.pressure]; S-A (S-A) pressure_unit = "psig" [units[S-A].facts.pressure_unit]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact end-use/system and compressed-air service, process and safety purpose, required quality/pressure/flow and duty/load pattern, shutoff/control and current solution, source/owner/revision/availability and lifecycle/system constraints.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S11 printed24-27 describes potentially inappropriate uses and context-dependent alternatives, not an equipment replacement instruction from a name. Establish actual compressed-air service and task requirements. Cabinet cooling is not protective panel purging. Intermittent/cyclic vacuum with suitable control and safety/practical constraints can justify a venturi; a generic load-factor example alone does not decide this installation or establish a central-pump alternative. Review existing suitable arrangements and full-system/lifecycle implications with the responsible specialist. Retain foreign, missing, zero and uncertain values; no blanket blower/fan/pump substitution or compulsory new survey follows.

**How it is decided:** Review actual compressed-air end-use/function, safety and quality requirements, matched demand/control records and practical lifecycle/system alternatives with the responsible specialist. A source list of potentially inappropriate uses is a collection prompt, not proof of waste. Suitable existing use or nonapplicability can be acknowledged; unknown service, scope or duty remains explicit without mandatory replacement or transferred source savings.

**What the source says (S11, S24):** S11 identifies potentially inappropriate compressed-air uses and discusses task-specific alternatives and lifecycle/system tradeoffs. The pressure-sensitive unregulated-demand share is not the fraction removable by substitution. No generic end-use saving, avoidable share or site benefit is asserted.
IAC/ITAC recommendation code: 2.4239; 2.4237; 2.4238 (IAC/ITAC browse page: 2.4239: 2,697 recommendations, 1.0 yr average payback, 48.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S11 printed24-27/PDF29-32 includes intermittent vacuum and explicitly distinguishes cabinet cooling from panel purging. Its historical unregulated-demand percentage concerns pressure-sensitive demand, not automatically inappropriate use, retrofit eligibility or savings. Known non-compressed-air and protective-purge roles are not cooling/sparging/vacuum subjects; unknown service is conditional.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
