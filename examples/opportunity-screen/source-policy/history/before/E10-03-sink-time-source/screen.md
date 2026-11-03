# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/thermal-recovery-records/models/E10-03-sink-time-source.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 2 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Energy

### E10: Is high-pressure condensate flashing to atmosphere when the flash steam could be used?

**About:** F-A  

**Finding reference (JSON string):** `"E10@F-A"`
**Asset IDs (JSON array):** `["F-A"]`

**Evidence on the drawing / model**

- equipment F-A reads "F-A FLASH DRUM sourceA" (`units[F-A]`)

**Data to collect**

- Condensate pressure and flow into the receiver [not on drawing]. Where: a walkdown: pressure gauge and vent plume. How: Record pressure and estimate flow.
- A low-pressure steam user nearby [not on drawing]. Where: site records: steam users list; then a walkdown: nearby LP users. How: List LP users within reach.

**How it is decided:** Worth a look when a steady high-pressure condensate flow vents and a low-pressure user is close by.

**What the source says (S8, S24):** Flash vessels allow "recovery of steam... used in low-pressure steam applications." No % stated.
IAC/ITAC recommendation code: 2.2127 (IAC/ITAC browse page: 31 recommendations, 1.0 yr average payback, 39.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E10: Is high-pressure condensate flashing to atmosphere when the flash steam could be used?

**About:** F-B  

**Finding reference (JSON string):** `"E10@F-B"`
**Asset IDs (JSON array):** `["F-B"]`

**Evidence on the drawing / model**

- equipment F-B reads "F-B FLASH TANK sourceB" (`units[F-B]`)

**Data to collect**

- Condensate pressure and flow into the receiver [not on drawing]. Where: a walkdown: pressure gauge and vent plume. How: Record pressure and estimate flow.
- A low-pressure steam user nearby [not on drawing]. Where: site records: steam users list; then a walkdown: nearby LP users. How: List LP users within reach.

**How it is decided:** Worth a look when a steady high-pressure condensate flow vents and a low-pressure user is close by.

**What the source says (S8, S24):** Flash vessels allow "recovery of steam... used in low-pressure steam applications." No % stated.
IAC/ITAC recommendation code: 2.2127 (IAC/ITAC browse page: 31 recommendations, 1.0 yr average payback, 39.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S8: Improving Steam System Performance: A Sourcebook for Industry, 2nd ed. (DOE/GO-102012-3423, rev. Oct 2012). https://www.energy.gov/sites/prod/files/2014/05/f15/steamsourcebook.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
