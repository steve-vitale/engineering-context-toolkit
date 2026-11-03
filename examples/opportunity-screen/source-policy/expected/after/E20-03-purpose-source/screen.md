# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/source-policy/models/E20-03-purpose-source.json`. Questions: `data/questions.json`.

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

### E20: What do existing records establish about these connection/drain candidates' compressed-air service, measured leakage and ongoing prevention program?

**About:** TD-A, FRL-B  

**Finding reference (JSON string):** `"E20@model"`
**Asset IDs (JSON array):** `["TD-A", "FRL-B"]`

**Evidence on the drawing / model**

- equipment TD-A reads "TD-A TIMER DRAIN" (`units[TD-A]`)
- equipment FRL-B reads "FRL-B FRL" (`units[FRL-B]`)
- Supplied candidate field: `"TD-A fictional_record = true; present; meaning and suitability unverified"` (`"units[TD-A].facts.fictional_record"`)
- Supplied candidate field: `"TD-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[TD-A].facts.record_source"`)
- Supplied candidate field: `"TD-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[TD-A].facts.record_revision"`)
- Supplied candidate field: `"TD-A record_available = true; present; meaning and suitability unverified"` (`"units[TD-A].facts.record_available"`)
- Supplied candidate field: `"TD-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[TD-A].facts.record_authority"`)
- Supplied candidate field: `"TD-A record_scope = \"localdrainonly\"; present; meaning and suitability unverified"` (`"units[TD-A].facts.record_scope"`)
- Supplied candidate field: `"TD-A service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[TD-A].facts.service"`)
- Supplied candidate field: `"TD-A leakage_percent = 0; present; meaning and suitability unverified"` (`"units[TD-A].facts.leakage_percent"`)
- Supplied candidate field: `"TD-A measurement_basis = \"purposefuldraincycle, notverifiedleak\"; present; meaning and suitability unverified"` (`"units[TD-A].facts.measurement_basis"`)
- Supplied candidate field: `"TD-A authorized_purge = true; present; meaning and suitability unverified"` (`"units[TD-A].facts.authorized_purge"`)
- Supplied candidate field: `"FRL-B fictional_record = true; present; meaning and suitability unverified"` (`"units[FRL-B].facts.fictional_record"`)
- Supplied candidate field: `"FRL-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[FRL-B].facts.record_source"`)
- Supplied candidate field: `"FRL-B record_revision = \"R0\"; present; meaning and suitability unverified"` (`"units[FRL-B].facts.record_revision"`)
- Supplied candidate field: `"FRL-B record_available = false; present; meaning and suitability unverified"` (`"units[FRL-B].facts.record_available"`)
- Supplied candidate field: `"FRL-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[FRL-B].facts.record_authority"`)
- Supplied candidate field: `"FRL-B record_scope = \"foreignsiteFRL-B\"; present; meaning and suitability unverified"` (`"units[FRL-B].facts.record_scope"`)
- Supplied candidate field: `"FRL-B service = \"unknown\"; blank; meaning and suitability unverified"` (`"units[FRL-B].facts.service"`)
- Supplied candidate field: `"FRL-B program_status = \"oldsurvey10%, notlocalbasis\"; present; meaning and suitability unverified"` (`"units[FRL-B].facts.program_status"`)
- On drawing: Supplied candidate fact, basis unverified: TD-A fictional_record = True (`units[TD-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: FRL-B fictional_record = True (`units[FRL-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TD-A record_source = Fictional development record; no company or human approval (`units[TD-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FRL-B record_source = Fictional development record; no company or human approval (`units[FRL-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TD-A record_revision = R1 (`units[TD-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FRL-B record_revision = R0 (`units[FRL-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TD-A record_available = True (`units[TD-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: FRL-B record_available = False (`units[FRL-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TD-A record_authority = unverified (`units[TD-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: FRL-B record_authority = unverified (`units[FRL-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TD-A record_scope = localdrainonly (`units[TD-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: FRL-B record_scope = foreignsiteFRL-B (`units[FRL-B].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: TD-A service = compressedair (`units[TD-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: FRL-B program_status = oldsurvey10%, notlocalbasis (`units[FRL-B].facts.program_status`)
- On drawing: Supplied candidate fact, basis unverified: TD-A leakage_percent = 0 (`units[TD-A].facts.leakage_percent`)
- On drawing: Supplied candidate fact, basis unverified: TD-A measurement_basis = purposefuldraincycle, notverifiedleak (`units[TD-A].facts.measurement_basis`)
- On drawing: Supplied candidate fact, basis unverified: TD-A authorized_purge = True (`units[TD-A].facts.authorized_purge`)

**Data to collect**

- Existing component/service, leak-measurement and repair/verification program basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TD-A (TD-A) fictional_record = true [units[TD-A].facts.fictional_record]; FRL-B (FRL-B) fictional_record = true [units[FRL-B].facts.fictional_record]; TD-A (TD-A) record_source = "Fictional development record; no company or human approval" [units[TD-A].facts.record_source]; FRL-B (FRL-B) record_source = "Fictional development record; no company or human approval" [units[FRL-B].facts.record_source]; TD-A (TD-A) record_revision = "R1" [units[TD-A].facts.record_revision]; FRL-B (FRL-B) record_revision = "R0" [units[FRL-B].facts.record_revision]; TD-A (TD-A) record_available = true [units[TD-A].facts.record_available]; FRL-B (FRL-B) record_available = false [units[FRL-B].facts.record_available]; TD-A (TD-A) record_authority = "unverified" [units[TD-A].facts.record_authority]; FRL-B (FRL-B) record_authority = "unverified" [units[FRL-B].facts.record_authority]; TD-A (TD-A) record_scope = "localdrainonly" [units[TD-A].facts.record_scope]; FRL-B (FRL-B) record_scope = "foreignsiteFRL-B" [units[FRL-B].facts.record_scope]; TD-A (TD-A) service = "compressedair" [units[TD-A].facts.service]; FRL-B (FRL-B) program_status = "oldsurvey10%, notlocalbasis" [units[FRL-B].facts.program_status]; TD-A (TD-A) leakage_percent = 0 [units[TD-A].facts.leakage_percent]; TD-A (TD-A) measurement_basis = "purposefuldraincycle, notverifiedleak" [units[TD-A].facts.measurement_basis]; TD-A (TD-A) authorized_purge = true [units[TD-A].facts.authorized_purge]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact component/system compressed-air service, authorized purge/drain/end-use demands, measurement method/control mode/pressure/capacity or volume/time basis, survey/repair/verification history and continuing program coverage; source/revision/units/availability and scope retained.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: Names/counts are potential inspection clues, not actual leaks or a rate. Known hydraulic/steam components are not compressed-air leak subjects; unknown service remains conditional. Review existing suitable records first. S11 printed28-30 permits load/unload or start/stop timing estimates only with the appropriate control and actual no-demand conditions; production stopped alone does not establish that. VSD/modulating/unknown control, intentional purges/drains, active end uses and unverified boundaries require a suitable different basis, not blind use of the same timing quotient. Distinguish capacity/flow percentage from power savings and retain uncertainty. S9/S11 describe ongoing identification, repair and verification, not a program started or stopped solely by a universal5%-10% cutoff. No compulsory survey, shutdown or control adjustment is authorized.

**How it is decided:** Review actual compressed-air service, qualified leak evidence and authorized demands, repair/verification and ongoing program coverage with the responsible specialist. Do not diagnose leakage from component labels, apply an incompatible no-load timing method or mandate a program only above a generic target. Suitable existing prevention or nonapplicability may be acknowledged; unresolved measurement/source/control/scope remains explicit. No production stop, repair instruction, compressor adjustment or site benefit follows from this screen.

**What the source says (S9, S24):** Leaks are "often wasting as much as 20%-30% of the compressor's output"; target "5%-10% of total system flow."
IAC/ITAC recommendation code: 2.4236 (IAC/ITAC browse page: 11,223 recommendations, 0.5 yr average payback, 81.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S9 compressed-air Tip3 pp1-2, with S11 printed28-30 leak methods/program and printed35-36 controls. Typical source leak percentages and example energy costs are not this system's leakage, targets or savings; scope/quantity and legitimate demand must be established.

## Sources cited above

- S9: Compressed Air Tip #3, Minimize Compressed Air Leaks (DOE/GO-102004-1964, Aug 2004). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air3.pdf (license: Public domain; the sheet cites Compressed Air Challenge material)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
