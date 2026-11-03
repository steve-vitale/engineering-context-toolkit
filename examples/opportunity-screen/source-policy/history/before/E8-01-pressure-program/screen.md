# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/steam-pump-records/models/E8-01-pressure-program.json`. Questions: `data/questions.json`.

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

### E8: Is there a steam trap population large enough to justify a trap survey program?

**About:** TR-A, TR-B  

**Finding reference (JSON string):** `"E8@model"`
**Asset IDs (JSON array):** `["TR-A", "TR-B"]`

**Evidence on the drawing / model**

- equipment TR-A reads "TR-A Steam trap smallpopulation" (`units[TR-A]`)
- equipment TR-B reads "TR-B Steam trap largepopulation" (`units[TR-B]`)

**Data to collect**

- Trap inventory and last survey date [not on drawing]. Where: site records: trap list; then maintenance records: trap survey history. How: Count traps by type and service.
- Trap condition [not on drawing]. Where: a walkdown: ultrasonic or thermal survey of each trap. How: Classify each trap working / failed open / failed closed.

**How it is decided:** A survey is likely worthwhile above about 500 traps or when no survey has been done in 3 to 5 years; otherwise fold traps into routine maintenance.

**What the source says (S3, S19, S24):** Unmaintained 3-5 years: "between 15% to 30% of the installed steam traps may have failed." With a program, "less than 5%." LBNL refinery table (as reported in LBNL-56183): trap maintenance 10-15% fuel saved, 0.5 yr payback.
IAC/ITAC recommendation code: 2.2113 (IAC/ITAC browse page: 445 recommendations, 0.6 yr average payback, 80.1% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S3: Steam Tip #1, Inspect and Repair Steam Traps (DOE/GO-102012-3401). https://www.energy.gov/sites/prod/files/2014/05/f16/steam1_traps.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
