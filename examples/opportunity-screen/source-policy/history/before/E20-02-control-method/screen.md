# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/integration-air-records/models/E20-02-control-method.json`. Questions: `data/questions.json`.

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

### E20: Are compressed air leaks likely, given many quick-disconnects, hose drops or timer drains?

**About:** FRL-A, TD-B  

**Finding reference (JSON string):** `"E20@model"`
**Asset IDs (JSON array):** `["FRL-A", "TD-B"]`

**Evidence on the drawing / model**

- equipment FRL-A reads "FRL-A FRL" (`units[FRL-A]`)
- equipment TD-B reads "TD-B TIMER DRAIN" (`units[TD-B]`)

**Data to collect**

- Leak rate [not on drawing]. Where: a walkdown: ultrasonic leak survey; a no-load test with production stopped. How: Leakage % from load/unload times at no demand.

**How it is decided:** Run a leak program when leakage is well above the 5-10% target.

**What the source says (S9, S24):** Leaks are "often wasting as much as 20%-30% of the compressor's output"; target "5%-10% of total system flow."
IAC/ITAC recommendation code: 2.4236 (IAC/ITAC browse page: 11,223 recommendations, 0.5 yr average payback, 81.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S9: Compressed Air Tip #3, Minimize Compressed Air Leaks (DOE/GO-102004-1964, Aug 2004). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air3.pdf (license: Public domain; the sheet cites Compressed Air Challenge material)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
