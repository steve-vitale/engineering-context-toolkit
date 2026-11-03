# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/source-policy/models/E12-02-access-purpose.json`. Questions: `data/questions.json`.

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

### E12: What do existing records establish about these hot-service valve candidates' actual temperature, insulation condition and access requirements?

**About:** HV-A, HV-B  

**Finding reference (JSON string):** `"E12@model"`
**Asset IDs (JSON array):** `["HV-A", "HV-B"]`

**Evidence on the drawing / model**

- Trigger: `"hand valve HV-A reads \"HV-A Fictional hotservicevalve candidate\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"HV-A\", \"kind\": \"manual_valve\", \"unit\": null, \"source\": \"Fictional record, not measuredplantstate\", \"assigned_tag\": true, \"unplaced_reason\": \"Fictional valve; no inventoried equipmentowner\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[HV-A]"`)
- Trigger: `"hand valve HV-B reads \"HV-B Fictional hotservicevalve candidate\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"HV-B\", \"kind\": \"manual_valve\", \"unit\": null, \"source\": \"Fictional record, not measuredplantstate\", \"assigned_tag\": true, \"unplaced_reason\": \"Fictional valve; no inventoried equipmentowner\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[HV-B]"`)
- Supplied candidate field: `"HV-A fictional_record = true; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.fictional_record"`)
- Supplied candidate field: `"HV-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.record_source"`)
- Supplied candidate field: `"HV-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.record_revision"`)
- Supplied candidate field: `"HV-A record_available = true; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.record_available"`)
- Supplied candidate field: `"HV-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.record_authority"`)
- Supplied candidate field: `"HV-A operating_temperature_C = 100; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.operating_temperature_C"`)
- Supplied candidate field: `"HV-A insulation_status = \"bare sourceassertion\"; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.insulation_status"`)
- Supplied candidate field: `"HV-A access_need = \"periodicinspectionandrepair\"; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.access_need"`)
- Supplied candidate field: `"HV-A inspection_frequency = \"weeklyfictional\"; present; meaning and suitability unverified"` (`"unplaced[HV-A].facts.inspection_frequency"`)
- Supplied candidate field: `"HV-A manufacturer_requirement = \"unknown\"; blank; meaning and suitability unverified"` (`"unplaced[HV-A].facts.manufacturer_requirement"`)
- Supplied candidate field: `"HV-B fictional_record = true; present; meaning and suitability unverified"` (`"unplaced[HV-B].facts.fictional_record"`)
- Supplied candidate field: `"HV-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"unplaced[HV-B].facts.record_source"`)
- Supplied candidate field: `"HV-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"unplaced[HV-B].facts.record_revision"`)
- Supplied candidate field: `"HV-B record_available = true; present; meaning and suitability unverified"` (`"unplaced[HV-B].facts.record_available"`)
- Supplied candidate field: `"HV-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"unplaced[HV-B].facts.record_authority"`)
- Supplied candidate field: `"HV-B operating_temperature_C = 100; present; meaning and suitability unverified"` (`"unplaced[HV-B].facts.operating_temperature_C"`)
- Supplied candidate field: `"HV-B insulation_status = \"bare sourceassertion\"; present; meaning and suitability unverified"` (`"unplaced[HV-B].facts.insulation_status"`)
- Supplied candidate field: `"HV-B access_need = \"rareopening\"; present; meaning and suitability unverified"` (`"unplaced[HV-B].facts.access_need"`)
- Supplied candidate field: `"HV-B inspection_frequency = \"unknown\"; blank; meaning and suitability unverified"` (`"unplaced[HV-B].facts.inspection_frequency"`)
- On drawing: Supplied candidate fact, basis unverified: HV-A fictional_record = True (`unplaced[HV-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: HV-B fictional_record = True (`unplaced[HV-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: HV-A record_source = Fictional development record; no company or human approval (`unplaced[HV-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: HV-B record_source = Fictional development record; no company or human approval (`unplaced[HV-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: HV-A record_revision = R1 (`unplaced[HV-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: HV-B record_revision = R1 (`unplaced[HV-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: HV-A record_available = True (`unplaced[HV-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: HV-B record_available = True (`unplaced[HV-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: HV-A record_authority = unverified (`unplaced[HV-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: HV-B record_authority = unverified (`unplaced[HV-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: HV-A operating_temperature_C = 100 (`unplaced[HV-A].facts.operating_temperature_C`)
- On drawing: Supplied candidate fact, basis unverified: HV-B operating_temperature_C = 100 (`unplaced[HV-B].facts.operating_temperature_C`)
- On drawing: Supplied candidate fact, basis unverified: HV-A insulation_status = bare sourceassertion (`unplaced[HV-A].facts.insulation_status`)
- On drawing: Supplied candidate fact, basis unverified: HV-B insulation_status = bare sourceassertion (`unplaced[HV-B].facts.insulation_status`)
- On drawing: Supplied candidate fact, basis unverified: HV-A access_need = periodicinspectionandrepair (`unplaced[HV-A].facts.access_need`)
- On drawing: Supplied candidate fact, basis unverified: HV-B access_need = rareopening (`unplaced[HV-B].facts.access_need`)
- On drawing: Supplied candidate fact, basis unverified: HV-A inspection_frequency = weeklyfictional (`unplaced[HV-A].facts.inspection_frequency`)

**Data to collect**

- Existing valve service, actual insulation/temperature and safe-access basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): HV-A (HV-A) fictional_record = true [unplaced[HV-A].facts.fictional_record]; HV-B (HV-B) fictional_record = true [unplaced[HV-B].facts.fictional_record]; HV-A (HV-A) record_source = "Fictional development record; no company or human approval" [unplaced[HV-A].facts.record_source]; HV-B (HV-B) record_source = "Fictional development record; no company or human approval" [unplaced[HV-B].facts.record_source]; HV-A (HV-A) record_revision = "R1" [unplaced[HV-A].facts.record_revision]; HV-B (HV-B) record_revision = "R1" [unplaced[HV-B].facts.record_revision]; HV-A (HV-A) record_available = true [unplaced[HV-A].facts.record_available]; HV-B (HV-B) record_available = true [unplaced[HV-B].facts.record_available]; HV-A (HV-A) record_authority = "unverified" [unplaced[HV-A].facts.record_authority]; HV-B (HV-B) record_authority = "unverified" [unplaced[HV-B].facts.record_authority]; HV-A (HV-A) operating_temperature_C = 100 [unplaced[HV-A].facts.operating_temperature_C]; HV-B (HV-B) operating_temperature_C = 100 [unplaced[HV-B].facts.operating_temperature_C]; HV-A (HV-A) insulation_status = "bare sourceassertion" [unplaced[HV-A].facts.insulation_status]; HV-B (HV-B) insulation_status = "bare sourceassertion" [unplaced[HV-B].facts.insulation_status]; HV-A (HV-A) access_need = "periodicinspectionandrepair" [unplaced[HV-A].facts.access_need]; HV-B (HV-B) access_need = "rareopening" [unplaced[HV-B].facts.access_need]; HV-A (HV-A) inspection_frequency = "weeklyfictional" [unplaced[HV-A].facts.inspection_frequency]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing per-valve/fitting service and size, operating/design/surface temperature distinction and units, actual installed insulation condition, access/periodic inspection/repair and manufacturer instructions, source/revision/availability and any removal/material hazards.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: A stated hot/design temperature or missing insulation field is not proof of a bare surface or heat loss. Review existing suitable insulation and records first. DOE Tip17 explicitly describes removable reusable covers for periodic inspection or repair, so frequent access does not itself rule them out. Review actual fit/material/function/access and applicable manufacturer guidance; existing insulation removal must follow qualified safe procedures, including potential hazardous-material assessment. A suitable current arrangement may be acknowledged without new field measurement or jacket installation. Source table temperatures, sizes and heat-loss examples are not automatic site prescriptions or savings.

**How it is decided:** Review actual service/temperature, installed condition, periodic access, manufacturer/function and safe-handling requirements before any insulation decision. Do not infer bare valves or automatically fit jackets from a model temperature, and do not reject removable covers merely because inspection/repair access is frequent. Acknowledge suitable existing insulation or unresolved applicability; no compulsory removal, retrofit or site benefit is authorized.

**What the source says (S1, S2):** "a 6-inch gate valve may have more than 6 square feet of surface area." The source tabulates heat saved by valve size and temperature. No % stated.
IAC/ITAC recommendation code: 2.2136 (by description).

**Limits:** Source review: complete S1/Tip2 and S2/Tip17 pp1–2. Removable-cover guidance includes periodic inspection/repair; trap-specific manufacturer instructions and existing-material hazards are conditional where applicable, not a blanket instruction to cover/remove every surface. Existing source examples depend on declared size/temperature/ambient/material/time conditions, not current installed truth.

## Sources cited above

- S1: DOE AMO Steam Tip Sheet #2, Insulate Steam Distribution and Condensate Return Lines (DOE/GO-102012-3404, Jan 2012). https://www.energy.gov/sites/default/files/2014/05/f16/steam2_insulate.pdf (license: Public domain (US federal))
- S2: Steam Tip #17, Install Removable Insulation on Valves and Fittings (DOE/GO-102012-3403). https://www.energy.gov/sites/prod/files/2014/05/f16/steam17_valves_fittings.pdf (license: Public domain)
