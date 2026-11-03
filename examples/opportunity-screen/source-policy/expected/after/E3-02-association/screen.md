# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/source-policy/models/E3-02-association.json`. Questions: `data/questions.json`.

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

### E3: What do existing records establish about this pump candidate's minimum-flow protection, return-line duty and remaining recirculation question?

**About:** P-A  

**Finding reference (JSON string):** `"E3@P-A"`
**Asset IDs (JSON array):** `["P-A", "RO-A"]`

**Evidence on the drawing / model**

- equipment P-A reads "P-A Fictional pumpA" (`units[P-A]`)
- Minimum-flow line: hand valve RO-A reads "RO-A RO sample line, not verified return" at P-A (`manual_valves[RO-A]`)
- Supplied candidate field: `"P-A fictional_record = true; present; meaning and suitability unverified"` (`"units[P-A].facts.fictional_record"`)
- Supplied candidate field: `"P-A record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[P-A].facts.record_source"`)
- Supplied candidate field: `"P-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[P-A].facts.record_revision"`)
- Supplied candidate field: `"P-A record_available = true; present; meaning and suitability unverified"` (`"units[P-A].facts.record_available"`)
- Supplied candidate field: `"P-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[P-A].facts.record_authority"`)
- Supplied candidate field: `"P-A line_purpose = \"sameunitRO sample/reverseosmosis, actualreturn unknown\"; present; meaning and suitability unverified"` (`"units[P-A].facts.line_purpose"`)
- Supplied candidate field: `"RO-A fictional_record = true; present; meaning and suitability unverified"` (`"manual_valves[RO-A].facts.fictional_record"`)
- Supplied candidate field: `"RO-A record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"manual_valves[RO-A].facts.record_source"`)
- Supplied candidate field: `"RO-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[RO-A].facts.record_revision"`)
- Supplied candidate field: `"RO-A record_available = true; present; meaning and suitability unverified"` (`"manual_valves[RO-A].facts.record_available"`)
- Supplied candidate field: `"RO-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"manual_valves[RO-A].facts.record_authority"`)
- Supplied candidate field: `"RO-A line_purpose = \"source-declared candidate; exactdischarge-return association unverified\"; present; meaning and suitability unverified"` (`"manual_valves[RO-A].facts.line_purpose"`)
- On drawing: Supplied candidate fact, basis unverified: P-A fictional_record = True (`units[P-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_source = Fictional development packet; no plant or human approval (`units[P-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_revision = R1 (`units[P-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_available = True (`units[P-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_authority = unverified (`units[P-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: P-A line_purpose = sameunitRO sample/reverseosmosis, actualreturn unknown (`units[P-A].facts.line_purpose`)
- On drawing: Supplied candidate fact, basis unverified: P-A fictional_record = True (`units[P-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_source = Fictional development packet; no plant or human approval (`units[P-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_revision = R1 (`units[P-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_available = True (`units[P-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_authority = unverified (`units[P-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: P-A line_purpose = sameunitRO sample/reverseosmosis, actualreturn unknown (`units[P-A].facts.line_purpose`)

**Data to collect**

- Existing named-pump service, protective minimum-flow and line-association basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): P-A (P-A) fictional_record = true [units[P-A].facts.fictional_record]; P-A (P-A) record_source = "Fictional development packet; no plant or human approval" [units[P-A].facts.record_source]; P-A (P-A) record_revision = "R1" [units[P-A].facts.record_revision]; P-A (P-A) record_available = true [units[P-A].facts.record_available]; P-A (P-A) record_authority = "unverified" [units[P-A].facts.record_authority]; P-A (P-A) line_purpose = "sameunitRO sample/reverseosmosis, actualreturn unknown" [units[P-A].facts.line_purpose]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing pump/vendor minimum-flow and service/curve records, actual return-line purpose and routing, protective control function and operating modes; retain exact pump/source/revision/availability and uncertainty.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: A nearby MIN FLOW, RO or automatic-recirculation label is a candidate, not proof of measured continuous discharge-return flow. Establish the actual pump/service and association first, and retain the vendor minimum-flow protection. Known positive-displacement/vacuum/metering or helper equipment is outside this bounded centrifugal-pump investigation; unknown eligible service stays conditional. Suitable protective operation and existing reviewed records may be acknowledged without a new measurement.
- Existing comparable forward/return flow and duration records [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): P-A (P-A) fictional_record = true [units[P-A].facts.fictional_record]; P-A (P-A) record_source = "Fictional development packet; no plant or human approval" [units[P-A].facts.record_source]; P-A (P-A) record_revision = "R1" [units[P-A].facts.record_revision]; P-A (P-A) record_available = true [units[P-A].facts.record_available]; P-A (P-A) record_authority = "unverified" [units[P-A].facts.record_authority]; P-A (P-A) line_purpose = "sameunitRO sample/reverseosmosis, actualreturn unknown" [units[P-A].facts.line_purpose]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual forward and recirculation flow/operating logs with quantities, units, measurement versus valve command, sampling/availability and matching periods/ranges.; then only a valve (RO-A) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Preserve source and units; do not substitute valve command for measured flow or divide unconverted/nonmatching records. Review whether sustained bypass is necessary for protection or system function before investigating a remaining energy question. This does not prescribe changing flow, a speed drive, bypass position or protection.

**How it is decided:** Review the whole pump/system duty and actual operating records with the responsible engineer. Continuous recirculation, an open orifice or missing model data alone is not a diagnosis or instruction to remove/restrict protection. Acknowledge appropriate automatic low-flow operation or suitable existing basis; unresolved minimum-flow, association, quantities or coverage remains a records question. No automatic action or site savings follow.

**What the source says (S13):** "the energy needed to push fluid through bypass lines is wasted." No % stated.

**Limits:** Minimum flow protects the pump; never remove it without the pump vendor's minimum continuous flow. Source review: S13 printed8,15,26,51–52 supports vendor minimum-flow protection and system-dependent bypass analysis, not a universal retrofit. The inherited bypass-energy quotation omits this surrounding protective/system context and is not site savings. Candidate values/labels are not accepted operating evidence.

### E3: What do existing records establish about this pump candidate's minimum-flow protection, return-line duty and remaining recirculation question?

**About:** P-B  

**Finding reference (JSON string):** `"E3@P-B"`
**Asset IDs (JSON array):** `["P-B", "HV-B"]`

**Evidence on the drawing / model**

- equipment P-B reads "P-B Fictional pumpB" (`units[P-B]`)
- Minimum-flow line: hand valve HV-B reads "HV-B Minimum-flow recirculation candidate" at P-B (`manual_valves[HV-B]`)
- Supplied candidate field: `"P-B fictional_record = true; present; meaning and suitability unverified"` (`"units[P-B].facts.fictional_record"`)
- Supplied candidate field: `"P-B record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[P-B].facts.record_source"`)
- Supplied candidate field: `"P-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[P-B].facts.record_revision"`)
- Supplied candidate field: `"P-B record_available = true; present; meaning and suitability unverified"` (`"units[P-B].facts.record_available"`)
- Supplied candidate field: `"P-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[P-B].facts.record_authority"`)
- Supplied candidate field: `"P-B line_purpose = \"declared minflow label, topology unavailable\"; present; meaning and suitability unverified"` (`"units[P-B].facts.line_purpose"`)
- Supplied candidate field: `"HV-B fictional_record = true; present; meaning and suitability unverified"` (`"manual_valves[HV-B].facts.fictional_record"`)
- Supplied candidate field: `"HV-B record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-B].facts.record_source"`)
- Supplied candidate field: `"HV-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-B].facts.record_revision"`)
- Supplied candidate field: `"HV-B record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-B].facts.record_available"`)
- Supplied candidate field: `"HV-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"manual_valves[HV-B].facts.record_authority"`)
- Supplied candidate field: `"HV-B line_purpose = \"source-declared candidate; exactdischarge-return association unverified\"; present; meaning and suitability unverified"` (`"manual_valves[HV-B].facts.line_purpose"`)
- On drawing: Supplied candidate fact, basis unverified: P-B fictional_record = True (`units[P-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_source = Fictional development packet; no plant or human approval (`units[P-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_revision = R1 (`units[P-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_available = True (`units[P-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_authority = unverified (`units[P-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: P-B line_purpose = declared minflow label, topology unavailable (`units[P-B].facts.line_purpose`)
- On drawing: Supplied candidate fact, basis unverified: P-B fictional_record = True (`units[P-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_source = Fictional development packet; no plant or human approval (`units[P-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_revision = R1 (`units[P-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_available = True (`units[P-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_authority = unverified (`units[P-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: P-B line_purpose = declared minflow label, topology unavailable (`units[P-B].facts.line_purpose`)

**Data to collect**

- Existing named-pump service, protective minimum-flow and line-association basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): P-B (P-B) fictional_record = true [units[P-B].facts.fictional_record]; P-B (P-B) record_source = "Fictional development packet; no plant or human approval" [units[P-B].facts.record_source]; P-B (P-B) record_revision = "R1" [units[P-B].facts.record_revision]; P-B (P-B) record_available = true [units[P-B].facts.record_available]; P-B (P-B) record_authority = "unverified" [units[P-B].facts.record_authority]; P-B (P-B) line_purpose = "declared minflow label, topology unavailable" [units[P-B].facts.line_purpose]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing pump/vendor minimum-flow and service/curve records, actual return-line purpose and routing, protective control function and operating modes; retain exact pump/source/revision/availability and uncertainty.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: A nearby MIN FLOW, RO or automatic-recirculation label is a candidate, not proof of measured continuous discharge-return flow. Establish the actual pump/service and association first, and retain the vendor minimum-flow protection. Known positive-displacement/vacuum/metering or helper equipment is outside this bounded centrifugal-pump investigation; unknown eligible service stays conditional. Suitable protective operation and existing reviewed records may be acknowledged without a new measurement.
- Existing comparable forward/return flow and duration records [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): P-B (P-B) fictional_record = true [units[P-B].facts.fictional_record]; P-B (P-B) record_source = "Fictional development packet; no plant or human approval" [units[P-B].facts.record_source]; P-B (P-B) record_revision = "R1" [units[P-B].facts.record_revision]; P-B (P-B) record_available = true [units[P-B].facts.record_available]; P-B (P-B) record_authority = "unverified" [units[P-B].facts.record_authority]; P-B (P-B) line_purpose = "declared minflow label, topology unavailable" [units[P-B].facts.line_purpose]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual forward and recirculation flow/operating logs with quantities, units, measurement versus valve command, sampling/availability and matching periods/ranges.; then only a valve (HV-B) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Preserve source and units; do not substitute valve command for measured flow or divide unconverted/nonmatching records. Review whether sustained bypass is necessary for protection or system function before investigating a remaining energy question. This does not prescribe changing flow, a speed drive, bypass position or protection.

**How it is decided:** Review the whole pump/system duty and actual operating records with the responsible engineer. Continuous recirculation, an open orifice or missing model data alone is not a diagnosis or instruction to remove/restrict protection. Acknowledge appropriate automatic low-flow operation or suitable existing basis; unresolved minimum-flow, association, quantities or coverage remains a records question. No automatic action or site savings follow.

**What the source says (S13):** "the energy needed to push fluid through bypass lines is wasted." No % stated.

**Limits:** Minimum flow protects the pump; never remove it without the pump vendor's minimum continuous flow. Source review: S13 printed8,15,26,51–52 supports vendor minimum-flow protection and system-dependent bypass analysis, not a universal retrofit. The inherited bypass-energy quotation omits this surrounding protective/system context and is not site savings. Candidate values/labels are not accepted operating evidence.

## Sources cited above

- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
