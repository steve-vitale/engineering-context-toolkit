# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/control-vent-records/models/C2-03-abnormal-purpose.json`. Questions: `data/questions.json`.

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
| Controls and automation | 1 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Controls and automation

### C2: Which measurements have no controller (read by people, or by nothing)?

**About:** PT-B  

**Finding reference (JSON string):** `"C2@model"`
**Asset IDs (JSON array):** `["PT-B", "IL-B"]`

**Evidence on the drawing / model**

- instrument PT-B reads "PT-B Supplied fictional instrument" at U-A (`instruments[PT-B]`)
- Interlock that reads it: interlock IL-B reads "IL-B Fictional pressurecondition Fictional valveaction, notapproved" (`interlocks[IL-B]`)
- Checked, none found: no controller in the model or loop list reads these measurements (`applies_when.without`)

**Data to collect**

- Whether operators adjust anything by hand from these readings [not on drawing]. Where: site records: operator logs and round sheets; then ask the operators which of these they act on, and how often. How: Note manual adjustments per shift tied to each reading.
- The control system's own loop list [not on drawing]. Where: DCS/PLC configuration: export the loop and point list. How: Confirm the reading is indication-only and not read by logic the model lacks.

**How it is decided:** Worth automating a reading that operators adjust by hand often, on a service where steadier control saves energy or quality; indication-only readings nobody acts on close the question.

**What the source says (S19):** "energy and cost savings are around 5% or more for many industrial applications of process control systems" (for plants without updated controls). Process control: "Typically 2-18% savings." The source says these figures "cannot be added".

**Limits:** The model or loop list may be incomplete; an uncontrolled reading may be read by logic not in the model.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
