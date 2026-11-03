# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/control-vent-records/models/E25-03-quantity-time.json`. Questions: `data/questions.json`.

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
| Controls and automation | 0 |
| Emissions | 2 |
| Safety questions to verify | 0 |

## Emissions

### E25: Are tank vapors vented to atmosphere with no vapor recovery?

**About:** TK-A  

**Finding reference (JSON string):** `"E25@TK-A"`
**Asset IDs (JSON array):** `["TK-A"]`

**Evidence on the drawing / model**

- equipment TK-A reads "TK-A TANK TO ATM" (`units[TK-A]`)
- Checked, none found: no vapor recovery or blanket gas anywhere in the model (`applies_when.without`)

**Data to collect**

- Vapor volume and composition [not on drawing]. Where: a walkdown: vent flow measurement and a gas sample; then site records: tank throughput and product vapor pressure. How: Estimate vented volume from throughput and breathing.

**How it is decided:** Worth a VRU study when hydrocarbon vapor volume is steady and large.

**What the source says (S20):** "VRUs can recover over 95 percent of the hydrocarbon..." vapors; "payback in as little as two months" (partner experience).

**Limits:** The source also quotes a partner's annual dollar figure; it is deliberately not repeated.

### E25: Are tank vapors vented to atmosphere with no vapor recovery?

**About:** TK-B  

**Finding reference (JSON string):** `"E25@TK-B"`
**Asset IDs (JSON array):** `["TK-B"]`

**Evidence on the drawing / model**

- equipment TK-B reads "TK-B TANK TO ATM" (`units[TK-B]`)
- Checked, none found: no vapor recovery or blanket gas anywhere in the model (`applies_when.without`)

**Data to collect**

- Vapor volume and composition [not on drawing]. Where: a walkdown: vent flow measurement and a gas sample; then site records: tank throughput and product vapor pressure. How: Estimate vented volume from throughput and breathing.

**How it is decided:** Worth a VRU study when hydrocarbon vapor volume is steady and large.

**What the source says (S20):** "VRUs can recover over 95 percent of the hydrocarbon..." vapors; "payback in as little as two months" (partner experience).

**Limits:** The source also quotes a partner's annual dollar figure; it is deliberately not repeated.

## Sources cited above

- S20: EPA Natural Gas STAR Lessons Learned, Installing Vapor Recovery Units on Storage Tanks. https://19january2017snapshot.epa.gov/sites/production/files/2016-06/documents/ll_final_vap.pdf (license: Public domain (archived EPA snapshot))
