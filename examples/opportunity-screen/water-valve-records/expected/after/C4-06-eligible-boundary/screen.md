# Opportunity screen: Fictional source-led C4/E24 control

Model: `examples/opportunity-screen/water-valve-records/models/C4-06-eligible-boundary.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 0 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 1 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Controls and automation

### C4: What do existing valve, bypass and operating records establish about this candidate's control performance and sizing basis?

**About:** FV-A  

**Finding reference (JSON string):** `"C4@FV-A"`
**Asset IDs (JSON array):** `["FV-A", "HV-A"]`

**Evidence on the drawing / model**

- valve FV-A reads "FV-A Fictional flow control valve" at U-A (`final_elements[FV-A]`)
- Bypass valve: hand valve HV-A reads "HV-A Fictional bypass valve" at U-A (`manual_valves[HV-A]`)
- Supplied candidate field: `"FV-A fictional_record = true; present; meaning and suitability unverified"` (`"final_elements[FV-A].facts.fictional_record"`)
- Supplied candidate field: `"FV-A record_source = \"Fictional training record, no plant or human approval\"; present; meaning and suitability unverified"` (`"final_elements[FV-A].facts.record_source"`)
- Supplied candidate field: `"FV-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"final_elements[FV-A].facts.record_revision"`)
- Supplied candidate field: `"FV-A record_available = true; present; meaning and suitability unverified"` (`"final_elements[FV-A].facts.record_available"`)
- Supplied candidate field: `"FV-A record_authority = \"not authenticated\"; present; meaning and suitability unverified"` (`"final_elements[FV-A].facts.record_authority"`)
- Supplied candidate field: `"FV-A position_value = 40; present; meaning and suitability unverified"` (`"final_elements[FV-A].facts.position_value"`)
- Supplied candidate field: `"FV-A position_unit = \"percent\"; present; meaning and suitability unverified"` (`"final_elements[FV-A].facts.position_unit"`)
- Supplied candidate field: `"FV-A actual_travel = null; blank; meaning and suitability unverified"` (`"final_elements[FV-A].facts.actual_travel"`)
- Supplied candidate field: `"HV-A fictional_record = true; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.fictional_record"`)
- Supplied candidate field: `"HV-A record_source = \"Fictional training record, no plant or human approval\"; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.record_source"`)
- Supplied candidate field: `"HV-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.record_revision"`)
- Supplied candidate field: `"HV-A record_available = true; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.record_available"`)
- Supplied candidate field: `"HV-A record_authority = \"not authenticated\"; present; meaning and suitability unverified"` (`"manual_valves[HV-A].facts.record_authority"`)
- On drawing: Supplied candidate fact, basis unverified: FV-A fictional_record = True (`final_elements[FV-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: FV-A record_source = Fictional training record, no plant or human approval (`final_elements[FV-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: FV-A record_revision = R1 (`final_elements[FV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: FV-A record_available = True (`final_elements[FV-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: FV-A record_authority = not authenticated (`final_elements[FV-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: FV-A position_value = 40 (`final_elements[FV-A].facts.position_value`)
- On drawing: Supplied candidate fact, basis unverified: FV-A position_unit = percent (`final_elements[FV-A].facts.position_unit`)

**Data to collect**

- Existing named-valve and bypass function, characteristic and operating basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): FV-A (FV-A) fictional_record = true [final_elements[FV-A].facts.fictional_record]; FV-A (FV-A) record_source = "Fictional training record, no plant or human approval" [final_elements[FV-A].facts.record_source]; FV-A (FV-A) record_revision = "R1" [final_elements[FV-A].facts.record_revision]; FV-A (FV-A) record_available = true [final_elements[FV-A].facts.record_available]; FV-A (FV-A) record_authority = "not authenticated" [final_elements[FV-A].facts.record_authority]; FV-A (FV-A) position_value = 40 [final_elements[FV-A].facts.position_value]; FV-A (FV-A) position_unit = "percent" [final_elements[FV-A].facts.position_unit]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named-valve sizing/Cv and characteristic, process/system/pump duty and pressure/flow range, control-performance and bypass function/normal-position records. Retain exact asset/source/revision, availability and operating/sample coverage; do not substitute another site or valve.; then historian or DCS trend for FV-A (no historian tag is mapped in this model for these); then a walkdown: Only if existing records cannot settle an applicable question: agree safe observations with the responsible engineer, including actual bypass function/position or measured travel association. No automatic field test, bypass closure or equipment change.. How: First establish the actual valve/bypass service and association: same-stream presence does not prove a physical bypass around this valve. Distinguish command/indication from measured valve travel, and review the valve characteristic and matched operating/control-performance basis. Low opening, an open/cracked bypass or a source example alone does not prove oversizing or justify resize/trim; bypasses can perform legitimate differential-pressure protection or temperature control. Acknowledge suitable existing records without compulsory new measurement; retain unknown or foreign/unavailable evidence as qualified context.

**How it is decided:** Review whether existing service, valve characteristic, system/pump operating range, control performance and actual bypass purpose establish a remaining investigation. No universal 50%-open criterion, commanded position, cracked bypass or absent record authorizes resize/trim, bypass closure or other hardware/operating change. Suitable existing records may be acknowledged; unresolved applicability or association remains a records question for the responsible engineer.

**What the source says (S13):** S13, printed pp. 25–26: highly throttled operation is a clue to review pump/system duty, valve sizing, characterization and control performance. Bypasses can have protective or temperature-control functions. This source supports investigation, not a universal opening threshold or a quantified site benefit.

**Limits:** Source-informed records review: S13 printed pp. 25–26 / PDF pp. 29–30, including valve-characterization qualifications and protective/temperature bypass functions. The earlier ellipsis omitted intervening characterization context; its exact old wording remains in history. Opening or a bypass label alone does not establish suitability, source authority or permission to modify equipment. Supplied fields remain candidates.

## Sources cited above

- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
