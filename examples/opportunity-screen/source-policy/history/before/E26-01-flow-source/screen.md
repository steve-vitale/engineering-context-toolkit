# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/control-vent-records/models/E26-01-flow-source.json`. Questions: `data/questions.json`.

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
| Controls and automation | 0 |
| Emissions | 1 |
| Safety questions to verify | 0 |

## Emissions

### E26: Are relief and vent flows to the flare or atmosphere unmetered?

**About:** V-B  

**Finding reference (JSON string):** `"E26@model"`
**Asset IDs (JSON array):** `["stream:V-B"]`

**Evidence on the drawing / model**

- stream V-B (asset stream:V-B) reads "VENT HEADER TO FLARE" (`streams[V-B]`)
- Checked, none found: no flow measurement on these streams (`applies_when.without`)

**Data to collect**

- Flare or vent flow and composition [not on drawing]. Where: a walkdown: ultrasonic flare-gas meter or a temporary vent flow measurement; then site records: relief valve lift records. How: Separate continuous (background) flow from relief events.

**How it is decided:** Worth metering when background flow is continuous; relief-only lines that seldom lift close the question.

**What the source says (S19):** Background flaring "can be as much as 50% of all flared gases (Miles, 2001)." In refineries it "will generally be less than 50%." No recovery % stated.

**Limits:** Relief paths are safety systems; metering or recovery changes go through a hazard review.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
