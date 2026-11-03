# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/control-vent-records/models/C10-02-local-monitor.json`. Questions: `data/questions.json`.

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

### C10: Are critical steam traps monitored automatically?

**About:** TM-X  

**Finding reference (JSON string):** `"C10@model"`
**Asset IDs (JSON array):** `["TM-X"]`

**Evidence on the drawing / model**

- equipment TM-X reads "TM-X TRAP MONITOR" (`units[TM-X]`)
- Checked, none found: no trap monitoring shown (`applies_when.without`)

**Data to collect**

- Which traps are critical [not on drawing]. Where: site records: trap list with service. How: Mark traps whose failure costs most.

**How it is decided:** Monitor the most important traps online; survey the rest.

**What the source says (S19, S3, S24):** LBNL (as reported in LBNL-56183): "Automatic Steam Trap Monitoring 5%", 1 yr. DOE tip sheet: "Consider online monitoring of the most important steam traps".
IAC/ITAC recommendation code: 2.211x (category only).

## Sources cited above

- S3: Steam Tip #1, Inspect and Repair Steam Traps (DOE/GO-102012-3401). https://www.energy.gov/sites/prod/files/2014/05/f16/steam1_traps.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
