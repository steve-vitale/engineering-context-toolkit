# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/steam-pump-records/models/E9-02-balance-boundaries.json`. Questions: `data/questions.json`.

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

### E9: Is condensate going to drain instead of back to the boiler?

**About:** CR-A, CR-B  

**Finding reference (JSON string):** `"E9@model"`
**Asset IDs (JSON array):** `["CR-A", "CR-B"]`

**Evidence on the drawing / model**

- equipment CR-A reads "CR-A CONDENSATE TO DRAIN candidate" (`units[CR-A]`)
- equipment CR-B reads "CR-B CONDENSATE TO DRAIN candidate" (`units[CR-B]`)

**Data to collect**

- Condensate return percentage and makeup flow [not on drawing]. Where: site records: boiler house makeup and feedwater meters; then utility bills or the site energy report: water and fuel. How: Return % = 1 - makeup flow / feedwater flow.
- Contamination risk of each drained stream [not on drawing]. Where: site records: process knowledge of possible leaks into the condensate. How: List what could contaminate it.

**How it is decided:** Worth returning where the drained condensate is clean and the flow is steady; contaminated or tiny streams stay at drain.

**What the source says (S8, S19, S24):** Enthalpy difference "generally over 120 Btu/lb, an amount of energy that is often more than 10% of the energy in the boiler generated steam." LBNL (as reported in LBNL-56183): "Condensate Return Alone 10%", 1.1 yr.
IAC/ITAC recommendation code: 2.2121 (IAC/ITAC browse page: 354 recommendations, 1.2 yr average payback, 50.9% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S8: Improving Steam System Performance: A Sourcebook for Industry, 2nd ed. (DOE/GO-102012-3423, rev. Oct 2012). https://www.energy.gov/sites/prod/files/2014/05/f15/steamsourcebook.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
