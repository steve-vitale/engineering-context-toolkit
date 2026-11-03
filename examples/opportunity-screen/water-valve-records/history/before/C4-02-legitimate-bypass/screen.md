# Opportunity screen: Fictional source-led C4/E24 control

Model: `examples/opportunity-screen/water-valve-records/models/C4-02-legitimate-bypass.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 0 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 2 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Controls and automation

### C4: Is a control valve bypassed, or oversized for its line?

**About:** FV-A  

**Finding reference (JSON string):** `"C4@FV-A"`
**Asset IDs (JSON array):** `["FV-A", "HV-A"]`

**Evidence on the drawing / model**

- valve FV-A reads "FV-A Fictional flow control valve" at U-A (`final_elements[FV-A]`)
- Bypass valve: hand valve HV-A reads "HV-A Fictional bypass valve" at U-A (`manual_valves[HV-A]`)

**Data to collect**

- Valve %-open history and bypass position [not on drawing]. Where: historian or DCS trend for FV-A (no historian tag is mapped in this model for these); then a walkdown: bypass valve position. How: Note typical opening.

**How it is decided:** Resize or trim when the valve normally runs well under half open or the bypass is cracked open.

**What the source says (S13):** "Many control valves normally operate at less than 50% open... a high degree of nonlinearity and thus inconsistent control performance." No % stated.

### C4: Is a control valve bypassed, or oversized for its line?

**About:** FV-B  

**Finding reference (JSON string):** `"C4@FV-B"`
**Asset IDs (JSON array):** `["FV-B", "HV-B"]`

**Evidence on the drawing / model**

- valve FV-B reads "FV-B Fictional flow control valve" at U-B (`final_elements[FV-B]`)
- Bypass valve: hand valve HV-B reads "HV-B Fictional bypass valve" at U-B (`manual_valves[HV-B]`)

**Data to collect**

- Valve %-open history and bypass position [not on drawing]. Where: historian or DCS trend for FV-B (no historian tag is mapped in this model for these); then a walkdown: bypass valve position. How: Note typical opening.

**How it is decided:** Resize or trim when the valve normally runs well under half open or the bypass is cracked open.

**What the source says (S13):** "Many control valves normally operate at less than 50% open... a high degree of nonlinearity and thus inconsistent control performance." No % stated.

## Sources cited above

- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
