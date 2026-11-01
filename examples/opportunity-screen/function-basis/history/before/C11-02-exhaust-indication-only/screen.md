# Opportunity screen: ILLUSTRATIVE source-adequacy counterexample

Model: `C11-02-exhaust-indication-only.json`. Questions: `data/questions.json`.

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

### C11: Is this dryer's or oven's exhaust (and make-up air) rate set by hand rather than by exhaust humidity?

**About:** D-B  

**Finding reference (JSON string):** `"C11@D-B"`
**Asset IDs (JSON array):** `["D-B"]`

**Evidence on the drawing / model**

- equipment D-B reads "D-B Continuous product dryer B" (`units[D-B]`)
- Checked, none found: no humidity, dew point or moisture measurement drawn on this unit (`applies_when.without`)

**Data to collect**

- Exhaust humidity and temperature over a production run [not on drawing]. Where: a walkdown: humidity or dew point logger in the exhaust duct for a full run. How: Compare the exhaust humidity with what the product and the process allow.
- Exhaust damper or fan setting and how it is set [not on drawing]. Where: DCS/PLC configuration: exhaust damper position or fan speed, and whether anything adjusts it; then a walkdown: damper position marks. How: Note whether it moves with production rate or product.
- Product moisture at the exit and its specification [not on drawing]. Where: site records: quality records: product moisture out of the dryer or oven against specification. How: Over-drying shows as moisture well below specification.

**How it is decided:** Worth a look when the exhaust leaves well below the humidity the product and the safety limits allow, so heated air is thrown away unsaturated. Close it if the exhaust is already near the allowed humidity or the rate is set by a solvent (LEL) or dust limit.

**What the source says (S26):** S26 (p. 104): "Process controls, such as feedback controllers, feed forward controllers, and model-based predictive controllers, can help to minimize dryer energy consumption by more precisely controlling energy inputs to meet the needs of the product being processed." The sensors it lists include "absorption capacitive sensors (for air humidity)". No % stated.

**Limits:** Exhaust rates on ovens that bake off solvents, or dryers with combustible dust, are set by safety limits: any change goes through the safety review. Fryers are left out: their exhaust is set by the vapour they boil off.

## Sources cited above

- S26: Masanet, Worrell, Graus and Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for the Fruit and Vegetable Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-59289-Revision, Mar 2008). https://eta-publications.lbl.gov/sites/default/files/lbnl-59289-rev.pdf (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
