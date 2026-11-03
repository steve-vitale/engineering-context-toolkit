# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/air-utility-records/models/E21-02-purge-cooling.json`. Questions: `data/questions.json`.

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

### E21: Is compressed air used for open blowing, sparging, venturi vacuum or cabinet cooling?

**About:** P-A, C-B  

**Finding reference (JSON string):** `"E21@model"`
**Asset IDs (JSON array):** `["P-A", "C-B"]`

**Evidence on the drawing / model**

- equipment P-A reads "P-A AIR CABINET COOL label" (`units[P-A]`)
- equipment C-B reads "C-B AIR CABINET COOL" (`units[C-B]`)

**Data to collect**

- End-use inventory with flow [not on drawing]. Where: a walkdown: list every air end use and estimate its flow. How: Flag uses a blower, pump or fan could do.

**How it is decided:** Replace inappropriate uses with a blower, vacuum pump or fan where practical.

**What the source says (S11, S24):** "unregulated usage is commonly as high as 30 to 50 percent of air demand."
IAC/ITAC recommendation code: 2.4239; 2.4237; 2.4238 (IAC/ITAC browse page: 2.4239: 2,697 recommendations, 1.0 yr average payback, 48.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
