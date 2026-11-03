# Opportunity screen: Fictional source-series locator control

Model: `examples/opportunity-screen/source-policy/signal-retention/models/SC05-E10-instrument-trigger.json`. Questions: `examples/opportunity-screen/source-policy/signal-retention/history/catalog-before.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 3 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Energy

### E10: What do existing records establish about this flash-vessel candidate's actual service, vent/recovery route and compatible low-pressure duty?

**About:** PT-A  

**Finding reference (JSON string):** `"E10@PT-A"`
**Asset IDs (JSON array):** `["PT-A"]`

**Evidence on the drawing / model**

- instrument PT-A reads "PT-A FLASH TANK condensate source pressure" (`instruments[PT-A]`)
- Supplied candidate field: `"PT-A fictional_record = true; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.fictional_record"`)
- Supplied candidate field: `"PT-A record_source = \"Fictional signal-locator source note, Figure 11; no actual series or plant record\"; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.record_source"`)
- Supplied candidate field: `"PT-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.record_revision"`)
- Supplied candidate field: `"PT-A record_available = false; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.record_available"`)
- Supplied candidate field: `"PT-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[PT-A].facts.record_authority"`)
- On drawing: Supplied candidate fact, basis unverified: PT-A fictional_record = True (`instruments[PT-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`instruments[PT-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_revision = R1 (`instruments[PT-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_available = False (`instruments[PT-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_authority = unverified (`instruments[PT-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: PT-A fictional_record = True (`instruments[PT-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`instruments[PT-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_revision = R1 (`instruments[PT-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_available = False (`instruments[PT-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: PT-A record_authority = unverified (`instruments[PT-A].facts.record_authority`)

**Data to collect**

- Existing source-specific condensate service, vent/recovery and actual operating basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PT-A (PT-A) fictional_record = true [instruments[PT-A].facts.fictional_record]; PT-A (PT-A) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [instruments[PT-A].facts.record_source]; PT-A (PT-A) record_revision = "R1" [instruments[PT-A].facts.record_revision]; PT-A (PT-A) record_available = false [instruments[PT-A].facts.record_available]; PT-A (PT-A) record_authority = "unverified" [instruments[PT-A].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-vessel/condensate source service and current vent/recovery/route records, actual pressure/temperature, flow and duration with quantity/units, sample time, revision, availability and operating coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A FLASH TANK/VESSEL/DRUM label is not proof of steam-water service, atmospheric venting, measured steam loss or an unused recovery opportunity. Establish actual current function and distinguish known nonsteam/hydrocarbon context from unknown applicable service. Review suitable existing recovery before requesting more data; pressure ratings or a plume alone do not establish a flash fraction or source quality.
- Existing compatible receiving-duty, association and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): PT-A (PT-A) fictional_record = true [instruments[PT-A].facts.fictional_record]; PT-A (PT-A) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [instruments[PT-A].facts.record_source]; PT-A (PT-A) record_revision = "R1" [instruments[PT-A].facts.record_revision]; PT-A (PT-A) record_available = false [instruments[PT-A].facts.record_available]; PT-A (PT-A) record_authority = "unverified" [instruments[PT-A].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-source low-pressure user pressure/quality, flow/heat duty and operating-time requirements, piping/route/distance and system/practical/economic constraints.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Review actual source/receiving pressure, timing and compatible duty together; a nearby or foreign/seasonal low-pressure label is not a matched sink. Supplemental original DOE Tip12 pp1–2 requires flow/duration, compatible uses and cost-effective equipment/piping, with return alternatives and availability/use considered. Acknowledge an existing suitable route or nonapplicability without a new field task. No recovery installation, physical connection, flash calculation or site savings follow from this screen.

**How it is decided:** Review actual steam-water condensate service, current vent/recovery and matched source/receiving duty, routing and economic constraints with the responsible engineer. Steady flow or a close low-pressure label alone does not establish unused recoverable steam or justify hardware/operating changes. Suitable existing recovery or nonapplicability may be acknowledged; unknown route, units, source or timing remains a qualified records question.

**What the source says (S8, S24):** Flash vessels allow "recovery of steam... used in low-pressure steam applications." No % stated.
IAC/ITAC recommendation code: 2.2127 (IAC/ITAC browse page: 31 recommendations, 1.0 yr average payback, 39.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S8 printed21 and supplemental original DOE Tip12 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam12_lowpressure_steam.pdf), completepp1–2, admitted before criteria. Its pressure/flow/duty/economic example is not this site's result. Missing representation is not installed absence.

### E10: What do existing records establish about this flash-vessel candidate's actual service, vent/recovery route and compatible low-pressure duty?

**About:** FT-B  

**Finding reference (JSON string):** `"E10@FT-B"`
**Asset IDs (JSON array):** `["FT-B"]`

**Evidence on the drawing / model**

- instrument FT-B reads "FT-B FLASH VESSEL condensate source flow" (`instruments[FT-B]`)
- Supplied candidate field: `"FT-B fictional_record = true; present; meaning and suitability unverified"` (`"instruments[FT-B].facts.fictional_record"`)
- Supplied candidate field: `"FT-B record_source = \"Fictional signal-locator source note, Figure 11; no actual series or plant record\"; present; meaning and suitability unverified"` (`"instruments[FT-B].facts.record_source"`)
- Supplied candidate field: `"FT-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[FT-B].facts.record_revision"`)
- Supplied candidate field: `"FT-B record_available = false; present; meaning and suitability unverified"` (`"instruments[FT-B].facts.record_available"`)
- Supplied candidate field: `"FT-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[FT-B].facts.record_authority"`)
- On drawing: Supplied candidate fact, basis unverified: FT-B fictional_record = True (`instruments[FT-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: FT-B record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`instruments[FT-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FT-B record_revision = R1 (`instruments[FT-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FT-B record_available = False (`instruments[FT-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: FT-B record_authority = unverified (`instruments[FT-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: FT-B fictional_record = True (`instruments[FT-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: FT-B record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`instruments[FT-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FT-B record_revision = R1 (`instruments[FT-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FT-B record_available = False (`instruments[FT-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: FT-B record_authority = unverified (`instruments[FT-B].facts.record_authority`)

**Data to collect**

- Existing source-specific condensate service, vent/recovery and actual operating basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): FT-B (FT-B) fictional_record = true [instruments[FT-B].facts.fictional_record]; FT-B (FT-B) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [instruments[FT-B].facts.record_source]; FT-B (FT-B) record_revision = "R1" [instruments[FT-B].facts.record_revision]; FT-B (FT-B) record_available = false [instruments[FT-B].facts.record_available]; FT-B (FT-B) record_authority = "unverified" [instruments[FT-B].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-vessel/condensate source service and current vent/recovery/route records, actual pressure/temperature, flow and duration with quantity/units, sample time, revision, availability and operating coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A FLASH TANK/VESSEL/DRUM label is not proof of steam-water service, atmospheric venting, measured steam loss or an unused recovery opportunity. Establish actual current function and distinguish known nonsteam/hydrocarbon context from unknown applicable service. Review suitable existing recovery before requesting more data; pressure ratings or a plume alone do not establish a flash fraction or source quality.
- Existing compatible receiving-duty, association and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): FT-B (FT-B) fictional_record = true [instruments[FT-B].facts.fictional_record]; FT-B (FT-B) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [instruments[FT-B].facts.record_source]; FT-B (FT-B) record_revision = "R1" [instruments[FT-B].facts.record_revision]; FT-B (FT-B) record_available = false [instruments[FT-B].facts.record_available]; FT-B (FT-B) record_authority = "unverified" [instruments[FT-B].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-source low-pressure user pressure/quality, flow/heat duty and operating-time requirements, piping/route/distance and system/practical/economic constraints.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Review actual source/receiving pressure, timing and compatible duty together; a nearby or foreign/seasonal low-pressure label is not a matched sink. Supplemental original DOE Tip12 pp1–2 requires flow/duration, compatible uses and cost-effective equipment/piping, with return alternatives and availability/use considered. Acknowledge an existing suitable route or nonapplicability without a new field task. No recovery installation, physical connection, flash calculation or site savings follow from this screen.

**How it is decided:** Review actual steam-water condensate service, current vent/recovery and matched source/receiving duty, routing and economic constraints with the responsible engineer. Steady flow or a close low-pressure label alone does not establish unused recoverable steam or justify hardware/operating changes. Suitable existing recovery or nonapplicability may be acknowledged; unknown route, units, source or timing remains a qualified records question.

**What the source says (S8, S24):** Flash vessels allow "recovery of steam... used in low-pressure steam applications." No % stated.
IAC/ITAC recommendation code: 2.2127 (IAC/ITAC browse page: 31 recommendations, 1.0 yr average payback, 39.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S8 printed21 and supplemental original DOE Tip12 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam12_lowpressure_steam.pdf), completepp1–2, admitted before criteria. Its pressure/flow/duty/economic example is not this site's result. Missing representation is not installed absence.

### E10: What do existing records establish about this flash-vessel candidate's actual service, vent/recovery route and compatible low-pressure duty?

**About:** TT-C  

**Finding reference (JSON string):** `"E10@TT-C"`
**Asset IDs (JSON array):** `["TT-C"]`

**Evidence on the drawing / model**

- instrument TT-C reads "TT-C FLASH DRUM temperature" (`instruments[TT-C]`)
- Supplied candidate field: `"TT-C fictional_record = true; present; meaning and suitability unverified"` (`"instruments[TT-C].facts.fictional_record"`)
- Supplied candidate field: `"TT-C record_source = \"Fictional signal-locator source note, Figure 11; no actual series or plant record\"; present; meaning and suitability unverified"` (`"instruments[TT-C].facts.record_source"`)
- Supplied candidate field: `"TT-C record_revision = \"R1\"; present; meaning and suitability unverified"` (`"instruments[TT-C].facts.record_revision"`)
- Supplied candidate field: `"TT-C record_available = false; present; meaning and suitability unverified"` (`"instruments[TT-C].facts.record_available"`)
- Supplied candidate field: `"TT-C record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"instruments[TT-C].facts.record_authority"`)
- On drawing: Supplied candidate fact, basis unverified: TT-C fictional_record = True (`instruments[TT-C].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TT-C record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`instruments[TT-C].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TT-C record_revision = R1 (`instruments[TT-C].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TT-C record_available = False (`instruments[TT-C].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TT-C record_authority = unverified (`instruments[TT-C].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: TT-C fictional_record = True (`instruments[TT-C].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: TT-C record_source = Fictional signal-locator source note, Figure 11; no actual series or plant record (`instruments[TT-C].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: TT-C record_revision = R1 (`instruments[TT-C].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: TT-C record_available = False (`instruments[TT-C].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: TT-C record_authority = unverified (`instruments[TT-C].facts.record_authority`)

**Data to collect**

- Existing source-specific condensate service, vent/recovery and actual operating basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TT-C (TT-C) fictional_record = true [instruments[TT-C].facts.fictional_record]; TT-C (TT-C) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [instruments[TT-C].facts.record_source]; TT-C (TT-C) record_revision = "R1" [instruments[TT-C].facts.record_revision]; TT-C (TT-C) record_available = false [instruments[TT-C].facts.record_available]; TT-C (TT-C) record_authority = "unverified" [instruments[TT-C].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-vessel/condensate source service and current vent/recovery/route records, actual pressure/temperature, flow and duration with quantity/units, sample time, revision, availability and operating coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A FLASH TANK/VESSEL/DRUM label is not proof of steam-water service, atmospheric venting, measured steam loss or an unused recovery opportunity. Establish actual current function and distinguish known nonsteam/hydrocarbon context from unknown applicable service. Review suitable existing recovery before requesting more data; pressure ratings or a plume alone do not establish a flash fraction or source quality.
- Existing compatible receiving-duty, association and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): TT-C (TT-C) fictional_record = true [instruments[TT-C].facts.fictional_record]; TT-C (TT-C) record_source = "Fictional signal-locator source note, Figure 11; no actual series or plant record" [instruments[TT-C].facts.record_source]; TT-C (TT-C) record_revision = "R1" [instruments[TT-C].facts.record_revision]; TT-C (TT-C) record_available = false [instruments[TT-C].facts.record_available]; TT-C (TT-C) record_authority = "unverified" [instruments[TT-C].facts.record_authority]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-source low-pressure user pressure/quality, flow/heat duty and operating-time requirements, piping/route/distance and system/practical/economic constraints.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: Review actual source/receiving pressure, timing and compatible duty together; a nearby or foreign/seasonal low-pressure label is not a matched sink. Supplemental original DOE Tip12 pp1–2 requires flow/duration, compatible uses and cost-effective equipment/piping, with return alternatives and availability/use considered. Acknowledge an existing suitable route or nonapplicability without a new field task. No recovery installation, physical connection, flash calculation or site savings follow from this screen.

**How it is decided:** Review actual steam-water condensate service, current vent/recovery and matched source/receiving duty, routing and economic constraints with the responsible engineer. Steady flow or a close low-pressure label alone does not establish unused recoverable steam or justify hardware/operating changes. Suitable existing recovery or nonapplicability may be acknowledged; unknown route, units, source or timing remains a qualified records question.

**What the source says (S8, S24):** Flash vessels allow "recovery of steam... used in low-pressure steam applications." No % stated.
IAC/ITAC recommendation code: 2.2127 (IAC/ITAC browse page: 31 recommendations, 1.0 yr average payback, 39.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S8 printed21 and supplemental original DOE Tip12 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam12_lowpressure_steam.pdf), completepp1–2, admitted before criteria. Its pressure/flow/duty/economic example is not this site's result. Missing representation is not installed absence.

## Sources cited above

- S8: Improving Steam System Performance: A Sourcebook for Industry, 2nd ed. (DOE/GO-102012-3423, rev. Oct 2012). https://www.energy.gov/sites/prod/files/2014/05/f15/steamsourcebook.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
