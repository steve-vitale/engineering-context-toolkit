# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/source-policy/models/E20-01-program-existing.json`. Questions: `data/questions.json`.

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

**About:** QD-A, HD-B  

**Finding reference (JSON string):** `"E20@model"`
**Asset IDs (JSON array):** `["QD-A", "HD-B"]`

**Evidence on the drawing / model**

- equipment QD-A reads "QD-A QUICK-DISCONNECT" (`units[QD-A]`)
- equipment HD-B reads "HD-B HOSE DROP" (`units[HD-B]`)
- Supplied candidate field: `"QD-A fictional_record = true; present; meaning and suitability unverified"` (`"units[QD-A].facts.fictional_record"`)
- Supplied candidate field: `"QD-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[QD-A].facts.record_source"`)
- Supplied candidate field: `"QD-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[QD-A].facts.record_revision"`)
- Supplied candidate field: `"QD-A record_available = true; present; meaning and suitability unverified"` (`"units[QD-A].facts.record_available"`)
- Supplied candidate field: `"QD-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[QD-A].facts.record_authority"`)
- Supplied candidate field: `"QD-A service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[QD-A].facts.service"`)
- Supplied candidate field: `"QD-A program_status = \"suppliedrepaired/verifiedrecord\"; present; meaning and suitability unverified"` (`"units[QD-A].facts.program_status"`)
- Supplied candidate field: `"QD-A leakage_percent = 3; present; meaning and suitability unverified"` (`"units[QD-A].facts.leakage_percent"`)
- Supplied candidate field: `"QD-A measurement_basis = \"qualifiedsourceassertion, notacceptedsite\"; present; meaning and suitability unverified"` (`"units[QD-A].facts.measurement_basis"`)
- Supplied candidate field: `"HD-B fictional_record = true; present; meaning and suitability unverified"` (`"units[HD-B].facts.fictional_record"`)
- Supplied candidate field: `"HD-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[HD-B].facts.record_source"`)
- Supplied candidate field: `"HD-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[HD-B].facts.record_revision"`)
- Supplied candidate field: `"HD-B record_available = true; present; meaning and suitability unverified"` (`"units[HD-B].facts.record_available"`)
- Supplied candidate field: `"HD-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[HD-B].facts.record_authority"`)
- Supplied candidate field: `"HD-B service = null; blank; meaning and suitability unverified"` (`"units[HD-B].facts.service"`)
- Supplied candidate field: `"HD-B program_status = null; blank; meaning and suitability unverified"` (`"units[HD-B].facts.program_status"`)
- On drawing: Supplied candidate fact, basis unverified: QD-A fictional_record = True (`units[QD-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: HD-B fictional_record = True (`units[HD-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: QD-A record_source = Fictional development record; no company or human approval (`units[QD-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: HD-B record_source = Fictional development record; no company or human approval (`units[HD-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: QD-A record_revision = R1 (`units[QD-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: HD-B record_revision = R1 (`units[HD-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: QD-A record_available = True (`units[QD-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: HD-B record_available = True (`units[HD-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: QD-A record_authority = unverified (`units[QD-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: HD-B record_authority = unverified (`units[HD-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: QD-A service = compressedair (`units[QD-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: QD-A program_status = suppliedrepaired/verifiedrecord (`units[QD-A].facts.program_status`)
- On drawing: Supplied candidate fact, basis unverified: QD-A leakage_percent = 3 (`units[QD-A].facts.leakage_percent`)
- On drawing: Supplied candidate fact, basis unverified: QD-A measurement_basis = qualifiedsourceassertion, notacceptedsite (`units[QD-A].facts.measurement_basis`)

**Data to collect**

- Existing component/service, leak-measurement and repair/verification program basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): QD-A (QD-A) fictional_record = true [units[QD-A].facts.fictional_record]; HD-B (HD-B) fictional_record = true [units[HD-B].facts.fictional_record]; QD-A (QD-A) record_source = "Fictional development record; no company or human approval" [units[QD-A].facts.record_source]; HD-B (HD-B) record_source = "Fictional development record; no company or human approval" [units[HD-B].facts.record_source]; QD-A (QD-A) record_revision = "R1" [units[QD-A].facts.record_revision]; HD-B (HD-B) record_revision = "R1" [units[HD-B].facts.record_revision]; QD-A (QD-A) record_available = true [units[QD-A].facts.record_available]; HD-B (HD-B) record_available = true [units[HD-B].facts.record_available]; QD-A (QD-A) record_authority = "unverified" [units[QD-A].facts.record_authority]; HD-B (HD-B) record_authority = "unverified" [units[HD-B].facts.record_authority]; QD-A (QD-A) service = "compressedair" [units[QD-A].facts.service]; QD-A (QD-A) program_status = "suppliedrepaired/verifiedrecord" [units[QD-A].facts.program_status]; QD-A (QD-A) leakage_percent = 3 [units[QD-A].facts.leakage_percent]; QD-A (QD-A) measurement_basis = "qualifiedsourceassertion, notacceptedsite" [units[QD-A].facts.measurement_basis]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact component/system compressed-air service, authorized purge/drain/end-use demands, measurement method/control mode/pressure/capacity or volume/time basis, survey/repair/verification history and continuing program coverage; source/revision/units/availability and scope retained.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: Names/counts are potential inspection clues, not actual leaks or a rate. Known hydraulic/steam components are not compressed-air leak subjects; unknown service remains conditional. Review existing suitable records first. S11 printed28-30 permits load/unload or start/stop timing estimates only with the appropriate control and actual no-demand conditions; production stopped alone does not establish that. VSD/modulating/unknown control, intentional purges/drains, active end uses and unverified boundaries require a suitable different basis, not blind use of the same timing quotient. Distinguish capacity/flow percentage from power savings and retain uncertainty. S9/S11 describe ongoing identification, repair and verification, not a program started or stopped solely by a universal5%-10% cutoff. No compulsory survey, shutdown or control adjustment is authorized.

**How it is decided:** Review actual compressed-air service, qualified leak evidence and authorized demands, repair/verification and ongoing program coverage with the responsible specialist. Do not diagnose leakage from component labels, apply an incompatible no-load timing method or mandate a program only above a generic target. Suitable existing prevention or nonapplicability may be acknowledged; unresolved measurement/source/control/scope remains explicit. No production stop, repair instruction, compressor adjustment or site benefit follows from this screen.

**What the source says (S9, S24):** Leaks are "often wasting as much as 20%-30% of the compressor's output"; target "5%-10% of total system flow."
IAC/ITAC recommendation code: 2.4236 (IAC/ITAC browse page: 11,223 recommendations, 0.5 yr average payback, 81.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S9 compressed-air Tip3 pp1-2, with S11 printed28-30 leak methods/program and printed35-36 controls. Typical source leak percentages and example energy costs are not this system's leakage, targets or savings; scope/quantity and legitimate demand must be established.

## Sources cited above

- S9: Compressed Air Tip #3, Minimize Compressed Air Leaks (DOE/GO-102004-1964, Aug 2004). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air3.pdf (license: Public domain; the sheet cites Compressed Air Challenge material)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
