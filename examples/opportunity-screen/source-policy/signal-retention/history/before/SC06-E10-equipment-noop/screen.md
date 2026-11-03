# Opportunity screen: Fictional source-series locator control

Model: `examples/opportunity-screen/source-policy/signal-retention/models/SC06-E10-equipment-noop.json`. Questions: `examples/opportunity-screen/source-policy/signal-retention/history/catalog-before.json`.

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

**About:** TK-A  

**Finding reference (JSON string):** `"E10@TK-A"`
**Asset IDs (JSON array):** `["TK-A"]`

**Evidence on the drawing / model**

- equipment TK-A reads "TK-A FLASH TANK receiver" (`units[TK-A]`)
- Supplied candidate field: `"TK-A fictional_record = true; present; meaning and suitability unverified"` (`"units[TK-A].facts.fictional_record"`)
- Supplied candidate field: `"TK-A record_source = \"Fictional signal-locator source note, Figure 11; no actual series or plant record\"; present; meaning and suitability unverified"` (`"units[TK-A].facts.record_source"`)
- Supplied candidate field: `"TK-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[TK-A].facts.record_revision"`)
- Supplied candidate field: `"TK-A record_available = false; present; meaning and suitability unverified"` (`"units[TK-A].facts.record_available"`)
- Supplied candidate field: `"TK-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[TK-A].facts.record_authority"`)
- On drawing: Supplied candidate fact, basis unverified: TK-A fictional_record = True (`units[TK-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`units[TK-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_revision = R1 (`units[TK-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_available = False (`units[TK-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_authority = unverified (`units[TK-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TK-A fictional_record = True (`units[TK-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`units[TK-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_revision = R1 (`units[TK-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_available = False (`units[TK-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TK-A record_authority = unverified (`units[TK-A].facts.record_authority`)

**Data to collect**

- Existing source-specific condensate service, vent/recovery and actual operating basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TK-A (TK-A) fictional_record = true [units[TK-A].facts.fictional_record]; TK-A (TK-A) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [units[TK-A].facts.record_source]; TK-A (TK-A) record_revision = "R1" [units[TK-A].facts.record_revision]; TK-A (TK-A) record_available = false [units[TK-A].facts.record_available]; TK-A (TK-A) record_authority = "unverified" [units[TK-A].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-vessel/condensate source service and current vent/recovery/route records, actual pressure/temperature, flow and duration with quantity/units, sample time, revision, availability and operating coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A FLASH TANK/VESSEL/DRUM label is not proof of steam-water service, atmospheric venting, measured steam loss or an unused recovery opportunity. Establish actual current function and distinguish known nonsteam/hydrocarbon context from unknown applicable service. Review suitable existing recovery before requesting more data; pressure ratings or a plume alone do not establish a flash fraction or source quality.
- Existing compatible receiving-duty, association and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TK-A (TK-A) fictional_record = true [units[TK-A].facts.fictional_record]; TK-A (TK-A) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [units[TK-A].facts.record_source]; TK-A (TK-A) record_revision = "R1" [units[TK-A].facts.record_revision]; TK-A (TK-A) record_available = false [units[TK-A].facts.record_available]; TK-A (TK-A) record_authority = "unverified" [units[TK-A].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-source low-pressure user pressure/quality, flow/heat duty and operating-time requirements, piping/route/distance and system/practical/economic constraints.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Review actual source/receiving pressure, timing and compatible duty together; a nearby or foreign/seasonal low-pressure label is not a matched sink. Supplemental original DOE Tip12 pp1–2 requires flow/duration, compatible uses and cost-effective equipment/piping, with return alternatives and availability/use considered. Acknowledge an existing suitable route or nonapplicability without a new field task. No recovery installation, physical connection, flash calculation or site savings follow from this screen.

**How it is decided:** Review actual steam-water condensate service, current vent/recovery and matched source/receiving duty, routing and economic constraints with the responsible engineer. Steady flow or a close low-pressure label alone does not establish unused recoverable steam or justify hardware/operating changes. Suitable existing recovery or nonapplicability may be acknowledged; unknown route, units, source or timing remains a qualified records question.

**What the source says (S8, S24):** Flash vessels allow "recovery of steam... used in low-pressure steam applications." No % stated.
IAC/ITAC recommendation code: 2.2127 (IAC/ITAC browse page: 31 recommendations, 1.0 yr average payback, 39.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S8 printed21 and supplemental original DOE Tip12 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam12_lowpressure_steam.pdf), completepp1–2, admitted before criteria. Its pressure/flow/duty/economic example is not this site's result. Missing representation is not installed absence.

## Sources cited above

- S8: Improving Steam System Performance: A Sourcebook for Industry, 2nd ed. (DOE/GO-102012-3423, rev. Oct 2012). https://www.energy.gov/sites/prod/files/2014/05/f15/steamsourcebook.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
