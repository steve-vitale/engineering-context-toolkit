# Opportunity screen: FICTIONAL paired combustion/control collection development fixture

Model: `examples/opportunity-screen/combustion-control-basis/models/COMB-06-drum-boiler-versus-dry-furnace.json`. Questions: `data/questions.json`.

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

### C5: Does the boiler lack O2 trim or three-element drum level control?

**About:** F-A  

**Finding reference (JSON string):** `"C5@F-A"`
**Asset IDs (JSON array):** `["F-A"]`

**Evidence on the drawing / model**

- equipment F-A reads "F-A Steam drum boiler A" (`units[F-A]`)

**Data to collect**

- Control narrative [not on drawing]. Where: DCS/PLC configuration: combustion and drum level configuration. How: Note O2 trim and level control elements.

**How it is decided:** Worth an upgrade where O2 trim or feed/steam flow in the level loop is missing on a large boiler.

**What the source says (S19, S24):** LBNL boiler table (as reported in LBNL-56183): "Improved Process Control 3%", 0.6 yr payback.
IAC/ITAC recommendation code: 2.121x (category only).

### C5: Does the boiler lack O2 trim or three-element drum level control?

**About:** F-B  

**Finding reference (JSON string):** `"C5@F-B"`
**Asset IDs (JSON array):** `["F-B"]`

**Evidence on the drawing / model**

- equipment F-B reads "F-B Dry process furnace B" (`units[F-B]`)

**Data to collect**

- Control narrative [not on drawing]. Where: DCS/PLC configuration: combustion and drum level configuration. How: Note O2 trim and level control elements.

**How it is decided:** Worth an upgrade where O2 trim or feed/steam flow in the level loop is missing on a large boiler.

**What the source says (S19, S24):** LBNL boiler table (as reported in LBNL-56183): "Improved Process Control 3%", 0.6 yr payback.
IAC/ITAC recommendation code: 2.121x (category only).

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
