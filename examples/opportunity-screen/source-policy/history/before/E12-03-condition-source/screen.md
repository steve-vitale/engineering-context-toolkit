# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/thermal-recovery-records/models/E12-03-condition-source.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
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

### E12: Are large valves and flanges on hot service left bare?

**About:** HV-A, HV-B  

**Finding reference (JSON string):** `"E12@model"`
**Asset IDs (JSON array):** `["HV-A", "HV-B"]`

**Evidence on the drawing / model**

- Trigger: `"hand valve HV-A reads \"HV-A Fictional hotservicevalve candidate\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"HV-A\", \"kind\": \"manual_valve\", \"unit\": null, \"source\": \"Fictional record, not measuredplantstate\", \"assigned_tag\": true, \"unplaced_reason\": \"Fictional valve; no inventoried equipmentowner\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[HV-A]"`)
- Trigger: `"hand valve HV-B reads \"HV-B Fictional hotservicevalve candidate\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"HV-B\", \"kind\": \"manual_valve\", \"unit\": null, \"source\": \"Fictional record, not measuredplantstate\", \"assigned_tag\": true, \"unplaced_reason\": \"Fictional valve; no inventoried equipmentowner\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[HV-B]"`)

**Data to collect**

- Bare valves and flanges by size [not on drawing]. Where: a walkdown: count bare valves and flanges by size; infrared camera. How: Count by size and temperature.

**How it is decided:** Fit removable jackets on bare hot valves and flanges that are not opened often.

**What the source says (S1, S2):** "a 6-inch gate valve may have more than 6 square feet of surface area." The source tabulates heat saved by valve size and temperature. No % stated.
IAC/ITAC recommendation code: 2.2136 (by description).

## Sources cited above

- S1: DOE AMO Steam Tip Sheet #2, Insulate Steam Distribution and Condensate Return Lines (DOE/GO-102012-3404, Jan 2012). https://www.energy.gov/sites/default/files/2014/05/f16/steam2_insulate.pdf (license: Public domain (US federal))
- S2: Steam Tip #17, Install Removable Insulation on Valves and Fittings (DOE/GO-102012-3403). https://www.energy.gov/sites/prod/files/2014/05/f16/steam17_valves_fittings.pdf (license: Public domain)
