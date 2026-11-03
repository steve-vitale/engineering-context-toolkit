# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/source-policy/models/E3-03-units-source.json`. Questions: `data/questions.json`.

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
**Asset IDs (JSON array):** `["P-A", "HV-A"]`

**Evidence on the drawing / model**

- equipment P-A reads "P-A Fictional pumpA" (`units[P-A]`)
- Minimum-flow line: hand valve HV-A reads "HV-A Minimum-flow recirculation candidate" at P-A (`manual_valves[HV-A]`)
- Supplied candidate field: `"P-A fictional_record = true; present; meaning and suitability unverified"` (`"units[P-A].facts.fictional_record"`)
- Supplied candidate field: `"P-A record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[P-A].facts.record_source"`)
- Supplied candidate field: `"P-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[P-A].facts.record_revision"`)
- Supplied candidate field: `"P-A record_available = false; present; meaning and suitability unverified"` (`"units[P-A].facts.record_available"`)
- Supplied candidate field: `"P-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[P-A].facts.record_authority"`)
- Supplied candidate field: `"P-A record_scope = \"foreignsiteP-A\"; present; meaning and suitability unverified"` (`"units[P-A].facts.record_scope"`)
- Supplied candidate field: `"P-A vendor_min_flow = \"curveforforeignpump\"; present; meaning and suitability unverified"` (`"units[P-A].facts.vendor_min_flow"`)
- Supplied candidate field: `"P-A flow_quantity = \"valvecommand, notflow\"; present; meaning and suitability unverified"` (`"units[P-A].facts.flow_quantity"`)
- Supplied candidate field: `"P-A flow_unit = \"commandpercent\"; present; meaning and suitability unverified"` (`"units[P-A].facts.flow_unit"`)
- Supplied candidate field: `"P-A forward_flow = 20; present; meaning and suitability unverified"` (`"units[P-A].facts.forward_flow"`)
- Supplied candidate field: `"P-A return_flow = null; blank; meaning and suitability unverified"` (`"units[P-A].facts.return_flow"`)
- Supplied candidate field: `"HV-A fictional_record = true; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.fictional_record"`)
- Supplied candidate field: `"HV-A record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.record_source"`)
- Supplied candidate field: `"HV-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.record_revision"`)
- Supplied candidate field: `"HV-A record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.record_available"`)
- Supplied candidate field: `"HV-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.record_authority"`)
- Supplied candidate field: `"HV-A line_purpose = \"source-declared candidate; exactdischarge-return association unverified\"; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.line_purpose"`)
- On drawing: Supplied candidate fact, basis unverified: P-A fictional_record = True (`units[P-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_source = Fictional development packet; no plant or human approval (`units[P-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_revision = R1 (`units[P-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_available = False (`units[P-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_authority = unverified (`units[P-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_scope = foreignsiteP-A (`units[P-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: P-A vendor_min_flow = curveforforeignpump (`units[P-A].facts.vendor_min_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-A flow_quantity = valvecommand, notflow (`units[P-A].facts.flow_quantity`)
- On drawing: Supplied candidate fact, basis unverified: P-A flow_unit = commandpercent (`units[P-A].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: P-A forward_flow = 20 (`units[P-A].facts.forward_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-A fictional_record = True (`units[P-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_source = Fictional development packet; no plant or human approval (`units[P-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_revision = R1 (`units[P-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_available = False (`units[P-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_authority = unverified (`units[P-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: P-A record_scope = foreignsiteP-A (`units[P-A].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: P-A vendor_min_flow = curveforforeignpump (`units[P-A].facts.vendor_min_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-A flow_quantity = valvecommand, notflow (`units[P-A].facts.flow_quantity`)
- On drawing: Supplied candidate fact, basis unverified: P-A flow_unit = commandpercent (`units[P-A].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: P-A forward_flow = 20 (`units[P-A].facts.forward_flow`)

**Data to collect**

- Existing named-pump service, protective minimum-flow and line-association basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): P-A (P-A) fictional_record = true [units[P-A].facts.fictional_record]; P-A (P-A) record_source = "Fictional development packet; no plant or human approval" [units[P-A].facts.record_source]; P-A (P-A) record_revision = "R1" [units[P-A].facts.record_revision]; P-A (P-A) record_available = false [units[P-A].facts.record_available]; P-A (P-A) record_authority = "unverified" [units[P-A].facts.record_authority]; P-A (P-A) record_scope = "foreignsiteP-A" [units[P-A].facts.record_scope]; P-A (P-A) vendor_min_flow = "curveforforeignpump" [units[P-A].facts.vendor_min_flow]; P-A (P-A) flow_quantity = "valvecommand, notflow" [units[P-A].facts.flow_quantity]; P-A (P-A) flow_unit = "commandpercent" [units[P-A].facts.flow_unit]; P-A (P-A) forward_flow = 20 [units[P-A].facts.forward_flow]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing pump/vendor minimum-flow and service/curve records, actual return-line purpose and routing, protective control function and operating modes; retain exact pump/source/revision/availability and uncertainty.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: A nearby MIN FLOW, RO or automatic-recirculation label is a candidate, not proof of measured continuous discharge-return flow. Establish the actual pump/service and association first, and retain the vendor minimum-flow protection. Known positive-displacement/vacuum/metering or helper equipment is outside this bounded centrifugal-pump investigation; unknown eligible service stays conditional. Suitable protective operation and existing reviewed records may be acknowledged without a new measurement.
- Existing comparable forward/return flow and duration records [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): P-A (P-A) fictional_record = true [units[P-A].facts.fictional_record]; P-A (P-A) record_source = "Fictional development packet; no plant or human approval" [units[P-A].facts.record_source]; P-A (P-A) record_revision = "R1" [units[P-A].facts.record_revision]; P-A (P-A) record_available = false [units[P-A].facts.record_available]; P-A (P-A) record_authority = "unverified" [units[P-A].facts.record_authority]; P-A (P-A) record_scope = "foreignsiteP-A" [units[P-A].facts.record_scope]; P-A (P-A) vendor_min_flow = "curveforforeignpump" [units[P-A].facts.vendor_min_flow]; P-A (P-A) flow_quantity = "valvecommand, notflow" [units[P-A].facts.flow_quantity]; P-A (P-A) flow_unit = "commandpercent" [units[P-A].facts.flow_unit]; P-A (P-A) forward_flow = 20 [units[P-A].facts.forward_flow]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual forward and recirculation flow/operating logs with quantities, units, measurement versus valve command, sampling/availability and matching periods/ranges.; then only a valve (HV-A) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Preserve source and units; do not substitute valve command for measured flow or divide unconverted/nonmatching records. Review whether sustained bypass is necessary for protection or system function before investigating a remaining energy question. This does not prescribe changing flow, a speed drive, bypass position or protection.

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
- Supplied candidate field: `"P-B record_scope = \"localP-B provisionalrecord\"; present; meaning and suitability unverified"` (`"units[P-B].facts.record_scope"`)
- Supplied candidate field: `"P-B vendor_min_flow = 25; present; meaning and suitability unverified"` (`"units[P-B].facts.vendor_min_flow"`)
- Supplied candidate field: `"P-B flow_unit = \"forwardm3/h; returngpm conversionnotdone\"; present; meaning and suitability unverified"` (`"units[P-B].facts.flow_unit"`)
- Supplied candidate field: `"P-B forward_flow = 70; present; meaning and suitability unverified"` (`"units[P-B].facts.forward_flow"`)
- Supplied candidate field: `"P-B return_flow = 10; present; meaning and suitability unverified"` (`"units[P-B].facts.return_flow"`)
- Supplied candidate field: `"P-B sample_period = \"nonmatchingperiods\"; present; meaning and suitability unverified"` (`"units[P-B].facts.sample_period"`)
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
- On drawing: Supplied candidate fact, basis unverified: P-B record_scope = localP-B provisionalrecord (`units[P-B].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: P-B vendor_min_flow = 25 (`units[P-B].facts.vendor_min_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-B flow_unit = forwardm3/h; returngpm conversionnotdone (`units[P-B].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: P-B forward_flow = 70 (`units[P-B].facts.forward_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-B return_flow = 10 (`units[P-B].facts.return_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-B sample_period = nonmatchingperiods (`units[P-B].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: P-B fictional_record = True (`units[P-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_source = Fictional development packet; no plant or human approval (`units[P-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_revision = R1 (`units[P-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_available = True (`units[P-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_authority = unverified (`units[P-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: P-B record_scope = localP-B provisionalrecord (`units[P-B].facts.record_scope`)
- On drawing: Supplied candidate fact, basis unverified: P-B vendor_min_flow = 25 (`units[P-B].facts.vendor_min_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-B flow_unit = forwardm3/h; returngpm conversionnotdone (`units[P-B].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: P-B forward_flow = 70 (`units[P-B].facts.forward_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-B return_flow = 10 (`units[P-B].facts.return_flow`)
- On drawing: Supplied candidate fact, basis unverified: P-B sample_period = nonmatchingperiods (`units[P-B].facts.sample_period`)

**Data to collect**

- Existing named-pump service, protective minimum-flow and line-association basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): P-B (P-B) fictional_record = true [units[P-B].facts.fictional_record]; P-B (P-B) record_source = "Fictional development packet; no plant or human approval" [units[P-B].facts.record_source]; P-B (P-B) record_revision = "R1" [units[P-B].facts.record_revision]; P-B (P-B) record_available = true [units[P-B].facts.record_available]; P-B (P-B) record_authority = "unverified" [units[P-B].facts.record_authority]; P-B (P-B) record_scope = "localP-B provisionalrecord" [units[P-B].facts.record_scope]; P-B (P-B) vendor_min_flow = 25 [units[P-B].facts.vendor_min_flow]; P-B (P-B) flow_unit = "forwardm3/h; returngpm conversionnotdone" [units[P-B].facts.flow_unit]; P-B (P-B) forward_flow = 70 [units[P-B].facts.forward_flow]; P-B (P-B) return_flow = 10 [units[P-B].facts.return_flow]; P-B (P-B) sample_period = "nonmatchingperiods" [units[P-B].facts.sample_period]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing pump/vendor minimum-flow and service/curve records, actual return-line purpose and routing, protective control function and operating modes; retain exact pump/source/revision/availability and uncertainty.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: A nearby MIN FLOW, RO or automatic-recirculation label is a candidate, not proof of measured continuous discharge-return flow. Establish the actual pump/service and association first, and retain the vendor minimum-flow protection. Known positive-displacement/vacuum/metering or helper equipment is outside this bounded centrifugal-pump investigation; unknown eligible service stays conditional. Suitable protective operation and existing reviewed records may be acknowledged without a new measurement.
- Existing comparable forward/return flow and duration records [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): P-B (P-B) fictional_record = true [units[P-B].facts.fictional_record]; P-B (P-B) record_source = "Fictional development packet; no plant or human approval" [units[P-B].facts.record_source]; P-B (P-B) record_revision = "R1" [units[P-B].facts.record_revision]; P-B (P-B) record_available = true [units[P-B].facts.record_available]; P-B (P-B) record_authority = "unverified" [units[P-B].facts.record_authority]; P-B (P-B) record_scope = "localP-B provisionalrecord" [units[P-B].facts.record_scope]; P-B (P-B) vendor_min_flow = 25 [units[P-B].facts.vendor_min_flow]; P-B (P-B) flow_unit = "forwardm3/h; returngpm conversionnotdone" [units[P-B].facts.flow_unit]; P-B (P-B) forward_flow = 70 [units[P-B].facts.forward_flow]; P-B (P-B) return_flow = 10 [units[P-B].facts.return_flow]; P-B (P-B) sample_period = "nonmatchingperiods" [units[P-B].facts.sample_period]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual forward and recirculation flow/operating logs with quantities, units, measurement versus valve command, sampling/availability and matching periods/ranges.; then only a valve (HV-B) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Preserve source and units; do not substitute valve command for measured flow or divide unconverted/nonmatching records. Review whether sustained bypass is necessary for protection or system function before investigating a remaining energy question. This does not prescribe changing flow, a speed drive, bypass position or protection.

**How it is decided:** Review the whole pump/system duty and actual operating records with the responsible engineer. Continuous recirculation, an open orifice or missing model data alone is not a diagnosis or instruction to remove/restrict protection. Acknowledge appropriate automatic low-flow operation or suitable existing basis; unresolved minimum-flow, association, quantities or coverage remains a records question. No automatic action or site savings follow.

**What the source says (S13):** "the energy needed to push fluid through bypass lines is wasted." No % stated.

**Limits:** Minimum flow protects the pump; never remove it without the pump vendor's minimum continuous flow. Source review: S13 printed8,15,26,51–52 supports vendor minimum-flow protection and system-dependent bypass analysis, not a universal retrofit. The inherited bypass-energy quotation omits this surrounding protective/system context and is not site savings. Candidate values/labels are not accepted operating evidence.

## Sources cited above

- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
