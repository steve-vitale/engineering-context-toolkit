# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/source-policy/models/E22-04-role-package.json`. Questions: `data/questions.json`.

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

### E22: What do existing records establish about this air-system candidate's demand events, controls and existing storage coverage/adequacy?

**About:** C-B  

**Finding reference (JSON string):** `"E22@C-B"`
**Asset IDs (JSON array):** `["C-B"]`

**Evidence on the drawing / model**

- equipment C-B reads "C-B AIR COMPRESSOR package with DRYER" (`units[C-B]`)
- Supplied candidate field: `"C-B fictional_record = true; present; meaning and suitability unverified"` (`"units[C-B].facts.fictional_record"`)
- Supplied candidate field: `"C-B record_source = \"Fictional pre-call development record, no company or human approval\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_source"`)
- Supplied candidate field: `"C-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_revision"`)
- Supplied candidate field: `"C-B record_available = true; present; meaning and suitability unverified"` (`"units[C-B].facts.record_available"`)
- Supplied candidate field: `"C-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[C-B].facts.record_authority"`)
- Supplied candidate field: `"C-B service = \"compressedair\"; present; meaning and suitability unverified"` (`"units[C-B].facts.service"`)
- On drawing: Supplied candidate fact, basis unverified: C-B fictional_record = True (`units[C-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_source = Fictional pre-call development record, no company or human approval (`units[C-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_revision = R1 (`units[C-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_available = True (`units[C-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: C-B record_authority = unverified (`units[C-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: C-B service = compressedair (`units[C-B].facts.service`)

**Data to collect**

- Existing system/end-use demand, control and storage basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): C-B (C-B) fictional_record = true [units[C-B].facts.fictional_record]; C-B (C-B) record_source = "Fictional pre-call development record, no company or human approval" [units[C-B].facts.record_source]; C-B (C-B) record_revision = "R1" [units[C-B].facts.record_revision]; C-B (C-B) record_available = true [units[C-B].facts.record_available]; C-B (C-B) record_authority = "unverified" [units[C-B].facts.record_authority]; C-B (C-B) service = "compressedair" [units[C-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor/system, critical end-use pressure and air quality, control/capacity mode, receiver volumes and location/coverage, peak magnitude/duration and interval, pressure differential, available compressor supply during events and replenishment/recovery time; source, units and comparable operating periods retained.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A receiver/storage label anywhere is not this air system's coverage or sufficient capacity, and missing representation is not installed absence. Review actual demand patterns, controls and current receivers first; the appropriate strategy depends on quantity/quality and pressure requirements, event and refill timing and compressor/control characteristics. S11 printed43-44 does not endorse a universal gallons-per-cfm rule. A known compressor package is not excluded merely because its name mentions a dryer; helpers and known nonair machines are not air subjects. Acknowledge suitable existing coverage before additional work; no obligatory one-week logging, receiver installation, compressor stop or pressure change is authorized.

**How it is decided:** Review actual system and critical end-use requirements, existing receiver coverage, pressure/demand/event and refill profiles and interacting compressor/control constraints with the responsible specialist. Short peaks or an extra unit starting are not by themselves an instruction to add storage. Suitable existing strategy or nonapplicability can be acknowledged; unresolved service, source, quantity, quality, pressure or timing remains a records question, not a sizing or vessel-safety approval.

**What the source says (S10, S24):** Storage "may allow such a compressor to be turned off." No % stated.
IAC/ITAC recommendation code: 2.422x (category only) (IAC/ITAC browse page: 8,589 recommendations, 1.2 yr average payback, 46.5% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S10 complete pp1-2 and S11 printed43-44/PDF48-49 make storage conditional on demand/quality/control and location/replenishment constraints; existing generic storage does not clear all systems. Pressure-vessel safety, relief, condensate/drain and maintenance constraints remain engineering responsibilities. No universal receiver volume or site savings is computed.

## Sources cited above

- S10: Compressed Air Tip #9, Compressed Air Storage Strategies (DOE/GO-102004-1965). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air9.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
