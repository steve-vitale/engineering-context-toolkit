# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/air-utility-records/models/E22-04-role-package.json`. Questions: `data/questions.json`.

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

### E22: Does the air compressor lack enough storage for intermittent large users?

**About:** D-A  

**Finding reference (JSON string):** `"E22@D-A"`
**Asset IDs (JSON array):** `["D-A"]`

**Evidence on the drawing / model**

- equipment D-A reads "D-A AIR COMPRESSOR helper" (`units[D-A]`)
- Checked, none found: no receiver or air storage anywhere in the model (`applies_when.without`)

**Data to collect**

- Demand profile [not on drawing]. Where: a walkdown: data-log compressor load and header pressure for a week. How: Find short high-demand events.

**How it is decided:** Add storage when short peaks force an extra compressor on.

**What the source says (S10, S24):** Storage "may allow such a compressor to be turned off." No % stated.
IAC/ITAC recommendation code: 2.422x (category only) (IAC/ITAC browse page: 8,589 recommendations, 1.2 yr average payback, 46.5% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E22: Does the air compressor lack enough storage for intermittent large users?

**About:** G-C  

**Finding reference (JSON string):** `"E22@G-C"`
**Asset IDs (JSON array):** `["G-C"]`

**Evidence on the drawing / model**

- equipment G-C reads "G-C INSTRUMENT AIR candidate" (`units[G-C]`)
- Checked, none found: no receiver or air storage anywhere in the model (`applies_when.without`)

**Data to collect**

- Demand profile [not on drawing]. Where: a walkdown: data-log compressor load and header pressure for a week. How: Find short high-demand events.

**How it is decided:** Add storage when short peaks force an extra compressor on.

**What the source says (S10, S24):** Storage "may allow such a compressor to be turned off." No % stated.
IAC/ITAC recommendation code: 2.422x (category only) (IAC/ITAC browse page: 8,589 recommendations, 1.2 yr average payback, 46.5% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S10: Compressed Air Tip #9, Compressed Air Storage Strategies (DOE/GO-102004-1965). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air9.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
