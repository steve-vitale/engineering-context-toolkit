# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/integration-air-records/models/E18-01-overlap-profile.json`. Questions: `data/questions.json`.

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

### E18: Is heat rejected to cooling water in one place while steam heats a colder stream in another (a heat-integration question)?

**About:** FT-A  

**Finding reference (JSON string):** `"E18@model"`
**Asset IDs (JSON array):** `["FT-A", "FV-B"]`

**Evidence on the drawing / model**

- instrument FT-A reads "FT-A COOLING WATER supply candidate" at U-A (`instruments[FT-A]`)
- Steam-heated user: valve FV-B reads "FV-B STEAM heating supply candidate" at U-B (`final_elements[FV-B]`)

**Data to collect**

- Temperatures and duties of the cooled and the heated streams [not on drawing]. Where: historian or DCS trend for FT-A (no historian tag is mapped in this model for these); then only a valve (FV-B) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: heat and material balance. How: For each stream: supply and target temperature and duty.
- Whether the duties overlap in time [not on drawing]. Where: site records: operating sequence: are both duties needed at the same time?. How: Mark each duty continuous, batch or startup-only.
- Layout distance and fouling [not on drawing]. Where: a walkdown: distance between the two exchangers; then maintenance records: cleaning history. How: Note pipe run and fouling service.

**How it is decided:** Worth a pinch or exchanger study only when the hot stream's temperature range sits above the cold stream's with a practical approach, both run at the same time for long hours, and they are close enough to connect. Otherwise close this screening investigation.

**What the source says (S19, S24):** Pinch potential "far exceeds that from well-known conventional techniques such as heat recovery from boiler flue gas, insulation and steam trap management." No % stated in that section.
IAC/ITAC recommendation code: 2.243x; 2.244x (IAC/ITAC browse page: 2.243x: 3,673 recommendations, 1.4 yr average payback, 31.2% implemented; 2.244x: 1,466 recommendations, 1.7 yr, 28.6%; average dollar figure omitted).

**Limits:** A screen pairs any cooling-water-cooled item with any steam-heated item; the temperatures decide. On a reactive system any heat-integration change needs a hazard review first. IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
