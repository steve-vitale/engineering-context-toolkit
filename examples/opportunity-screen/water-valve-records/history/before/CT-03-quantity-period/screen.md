# Opportunity screen: Fictional source-led C4/E24 control

Model: `examples/opportunity-screen/water-valve-records/models/CT-03-quantity-period.json`. Questions: `data/questions.json`.

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

### E24: Is cooling tower blowdown manual, with no conductivity control or makeup and blowdown metering?

**About:** T-A  

**Finding reference (JSON string):** `"E24@T-A"`
**Asset IDs (JSON array):** `["T-A"]`

**Evidence on the drawing / model**

- equipment T-A reads "T-A Fictional cooling tower T-A" (`units[T-A]`)
- Checked, none found: no conductivity element or controller near the tower (`applies_when.without`)

**Data to collect**

- Cycles of concentration [not on drawing]. Where: site records: water treatment log; then a walkdown: conductivity of makeup and tower water. How: Cycles = tower conductivity / makeup conductivity.

**How it is decided:** Raise cycles with a conductivity controller where the water chemistry allows.

**What the source says (S21, S24):** "Increasing cycles from three to six reduces cooling tower make-up water by 20% and cooling tower blowdown by 50%." Recommends a conductivity controller and makeup/blowdown flow meters. No energy % stated.
IAC/ITAC recommendation code: 2.2611 (IAC/ITAC browse page: 55 recommendations, 0.9 yr average payback, 45.7% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E24: Is cooling tower blowdown manual, with no conductivity control or makeup and blowdown metering?

**About:** T-B  

**Finding reference (JSON string):** `"E24@T-B"`
**Asset IDs (JSON array):** `["T-B"]`

**Evidence on the drawing / model**

- equipment T-B reads "T-B Fictional cooling tower T-B" (`units[T-B]`)
- Checked, none found: no conductivity element or controller near the tower (`applies_when.without`)

**Data to collect**

- Cycles of concentration [not on drawing]. Where: site records: water treatment log; then a walkdown: conductivity of makeup and tower water. How: Cycles = tower conductivity / makeup conductivity.

**How it is decided:** Raise cycles with a conductivity controller where the water chemistry allows.

**What the source says (S21, S24):** "Increasing cycles from three to six reduces cooling tower make-up water by 20% and cooling tower blowdown by 50%." Recommends a conductivity controller and makeup/blowdown flow meters. No energy % stated.
IAC/ITAC recommendation code: 2.2611 (IAC/ITAC browse page: 55 recommendations, 0.9 yr average payback, 45.7% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S21: DOE FEMP, Best Management Practice #10: Cooling Tower Management. https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
