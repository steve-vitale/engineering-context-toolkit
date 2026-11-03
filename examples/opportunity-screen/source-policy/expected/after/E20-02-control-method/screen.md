# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/source-policy/models/E20-02-control-method.json`. Questions: `data/questions.json`.

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

**About:** FRL-A, TD-B  

**Finding reference (JSON string):** `"E20@model"`
**Asset IDs (JSON array):** `["FRL-A", "TD-B"]`

**Evidence on the drawing / model**

- equipment FRL-A reads "FRL-A FRL" (`units[FRL-A]`)
- equipment TD-B reads "TD-B TIMER DRAIN" (`units[TD-B]`)
- Supplied candidate field: `"FRL-A fictional_record = true; present; meaning and suitability unverified"` (`"units[FRL-A].facts.fictional_record"`)
- Supplied candidate field: `"FRL-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[FRL-A].facts.record_source"`)
- Supplied candidate field: `"FRL-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[FRL-A].facts.record_revision"`)
- Supplied candidate field: `"FRL-A record_available = true; present; meaning and suitability unverified"` (`"units[FRL-A].facts.record_available"`)
- Supplied candidate field: `"FRL-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[FRL-A].facts.record_authority"`)
- Supplied candidate field: `"FRL-A service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[FRL-A].facts.service"`)
- Supplied candidate field: `"FRL-A control_mode = \"loadunload\"; present; meaning and suitability unverified"` (`"units[FRL-A].facts.control_mode"`)
- Supplied candidate field: `"FRL-A onload_time = 5; present; meaning and suitability unverified"` (`"units[FRL-A].facts.onload_time"`)
- Supplied candidate field: `"FRL-A offload_time = 95; present; meaning and suitability unverified"` (`"units[FRL-A].facts.offload_time"`)
- Supplied candidate field: `"FRL-A time_unit = \"minutes\"; present; meaning and suitability unverified"` (`"units[FRL-A].facts.time_unit"`)
- Supplied candidate field: `"FRL-A all_enduses_off = true; present; meaning and suitability unverified"` (`"units[FRL-A].facts.all_enduses_off"`)
- Supplied candidate field: `"FRL-A production_stopped = true; present; meaning and suitability unverified"` (`"units[FRL-A].facts.production_stopped"`)
- Supplied candidate field: `"TD-B fictional_record = true; present; meaning and suitability unverified"` (`"units[TD-B].facts.fictional_record"`)
- Supplied candidate field: `"TD-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[TD-B].facts.record_source"`)
- Supplied candidate field: `"TD-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[TD-B].facts.record_revision"`)
- Supplied candidate field: `"TD-B record_available = true; present; meaning and suitability unverified"` (`"units[TD-B].facts.record_available"`)
- Supplied candidate field: `"TD-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[TD-B].facts.record_authority"`)
- Supplied candidate field: `"TD-B service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[TD-B].facts.service"`)
- Supplied candidate field: `"TD-B control_mode = \"VSD/modulating\"; present; meaning and suitability unverified"` (`"units[TD-B].facts.control_mode"`)
- Supplied candidate field: `"TD-B onload_time = 5; present; meaning and suitability unverified"` (`"units[TD-B].facts.onload_time"`)
- Supplied candidate field: `"TD-B offload_time = 95; present; meaning and suitability unverified"` (`"units[TD-B].facts.offload_time"`)
- Supplied candidate field: `"TD-B time_unit = \"minutes\"; present; meaning and suitability unverified"` (`"units[TD-B].facts.time_unit"`)
- Supplied candidate field: `"TD-B all_enduses_off = false; present; meaning and suitability unverified"` (`"units[TD-B].facts.all_enduses_off"`)
- Supplied candidate field: `"TD-B production_stopped = true; present; meaning and suitability unverified"` (`"units[TD-B].facts.production_stopped"`)
- Supplied candidate field: `"TD-B authorized_purge = \"active\"; present; meaning and suitability unverified"` (`"units[TD-B].facts.authorized_purge"`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A fictional_record = True (`units[FRL-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TD-B fictional_record = True (`units[TD-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A record_source = Fictional development record; no company or human approval (`units[FRL-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TD-B record_source = Fictional development record; no company or human approval (`units[TD-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A record_revision = R1 (`units[FRL-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TD-B record_revision = R1 (`units[TD-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A record_available = True (`units[FRL-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TD-B record_available = True (`units[TD-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A record_authority = unverified (`units[FRL-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TD-B record_authority = unverified (`units[TD-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A service = compressedair (`units[FRL-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: TD-B service = compressedair (`units[TD-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A control_mode = loadunload (`units[FRL-A].facts.control_mode`)
- On drawing: Supplied candidate fact, basis unverified: TD-B control_mode = VSD/modulating (`units[TD-B].facts.control_mode`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A onload_time = 5 (`units[FRL-A].facts.onload_time`)
- On drawing: Supplied candidate fact, basis unverified: TD-B onload_time = 5 (`units[TD-B].facts.onload_time`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A offload_time = 95 (`units[FRL-A].facts.offload_time`)
- On drawing: Supplied candidate fact, basis unverified: TD-B offload_time = 95 (`units[TD-B].facts.offload_time`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A time_unit = minutes (`units[FRL-A].facts.time_unit`)
- On drawing: Supplied candidate fact, basis unverified: TD-B time_unit = minutes (`units[TD-B].facts.time_unit`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A all_enduses_off = True (`units[FRL-A].facts.all_enduses_off`)
- On drawing: Supplied candidate fact, basis unverified: TD-B all_enduses_off = False (`units[TD-B].facts.all_enduses_off`)
- On drawing: Supplied candidate fact, basis unverified: FRL-A production_stopped = True (`units[FRL-A].facts.production_stopped`)
- On drawing: Supplied candidate fact, basis unverified: TD-B production_stopped = True (`units[TD-B].facts.production_stopped`)
- On drawing: Supplied candidate fact, basis unverified: TD-B authorized_purge = active (`units[TD-B].facts.authorized_purge`)

**Data to collect**

- Existing component/service, leak-measurement and repair/verification program basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): FRL-A (FRL-A) fictional_record = true [units[FRL-A].facts.fictional_record]; TD-B (TD-B) fictional_record = true [units[TD-B].facts.fictional_record]; FRL-A (FRL-A) record_source = "Fictional development record; no company or human approval" [units[FRL-A].facts.record_source]; TD-B (TD-B) record_source = "Fictional development record; no company or human approval" [units[TD-B].facts.record_source]; FRL-A (FRL-A) record_revision = "R1" [units[FRL-A].facts.record_revision]; TD-B (TD-B) record_revision = "R1" [units[TD-B].facts.record_revision]; FRL-A (FRL-A) record_available = true [units[FRL-A].facts.record_available]; TD-B (TD-B) record_available = true [units[TD-B].facts.record_available]; FRL-A (FRL-A) record_authority = "unverified" [units[FRL-A].facts.record_authority]; TD-B (TD-B) record_authority = "unverified" [units[TD-B].facts.record_authority]; FRL-A (FRL-A) service = "compressedair" [units[FRL-A].facts.service]; TD-B (TD-B) service = "compressedair" [units[TD-B].facts.service]; FRL-A (FRL-A) control_mode = "loadunload" [units[FRL-A].facts.control_mode]; TD-B (TD-B) control_mode = "VSD/modulating" [units[TD-B].facts.control_mode]; FRL-A (FRL-A) onload_time = 5 [units[FRL-A].facts.onload_time]; TD-B (TD-B) onload_time = 5 [units[TD-B].facts.onload_time]; FRL-A (FRL-A) offload_time = 95 [units[FRL-A].facts.offload_time]; TD-B (TD-B) offload_time = 95 [units[TD-B].facts.offload_time]; FRL-A (FRL-A) time_unit = "minutes" [units[FRL-A].facts.time_unit]; TD-B (TD-B) time_unit = "minutes" [units[TD-B].facts.time_unit]; FRL-A (FRL-A) all_enduses_off = true [units[FRL-A].facts.all_enduses_off]; TD-B (TD-B) all_enduses_off = false [units[TD-B].facts.all_enduses_off]; FRL-A (FRL-A) production_stopped = true [units[FRL-A].facts.production_stopped]; TD-B (TD-B) production_stopped = true [units[TD-B].facts.production_stopped]; TD-B (TD-B) authorized_purge = "active" [units[TD-B].facts.authorized_purge]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact component/system compressed-air service, authorized purge/drain/end-use demands, measurement method/control mode/pressure/capacity or volume/time basis, survey/repair/verification history and continuing program coverage; source/revision/units/availability and scope retained.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: Names/counts are potential inspection clues, not actual leaks or a rate. Known hydraulic/steam components are not compressed-air leak subjects; unknown service remains conditional. Review existing suitable records first. S11 printed28-30 permits load/unload or start/stop timing estimates only with the appropriate control and actual no-demand conditions; production stopped alone does not establish that. VSD/modulating/unknown control, intentional purges/drains, active end uses and unverified boundaries require a suitable different basis, not blind use of the same timing quotient. Distinguish capacity/flow percentage from power savings and retain uncertainty. S9/S11 describe ongoing identification, repair and verification, not a program started or stopped solely by a universal5%-10% cutoff. No compulsory survey, shutdown or control adjustment is authorized.

**How it is decided:** Review actual compressed-air service, qualified leak evidence and authorized demands, repair/verification and ongoing program coverage with the responsible specialist. Do not diagnose leakage from component labels, apply an incompatible no-load timing method or mandate a program only above a generic target. Suitable existing prevention or nonapplicability may be acknowledged; unresolved measurement/source/control/scope remains explicit. No production stop, repair instruction, compressor adjustment or site benefit follows from this screen.

**What the source says (S9, S24):** Leaks are "often wasting as much as 20%-30% of the compressor's output"; target "5%-10% of total system flow."
IAC/ITAC recommendation code: 2.4236 (IAC/ITAC browse page: 11,223 recommendations, 0.5 yr average payback, 81.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S9 compressed-air Tip3 pp1-2, with S11 printed28-30 leak methods/program and printed35-36 controls. Typical source leak percentages and example energy costs are not this system's leakage, targets or savings; scope/quantity and legitimate demand must be established.

## Sources cited above

- S9: Compressed Air Tip #3, Minimize Compressed Air Leaks (DOE/GO-102004-1964, Aug 2004). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air3.pdf (license: Public domain; the sheet cites Compressed Air Challenge material)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
