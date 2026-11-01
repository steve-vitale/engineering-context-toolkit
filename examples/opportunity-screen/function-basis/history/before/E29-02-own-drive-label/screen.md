# Opportunity screen: ILLUSTRATIVE source-adequacy counterexample

Model: `E29-02-own-drive-label.json`. Questions: `data/questions.json`.

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

### E29: Does this refrigeration compressor carry part load on its slide valve (or hot gas bypass) with no speed control?

**About:** K-B  

**Finding reference (JSON string):** `"E29@K-B"`
**Asset IDs (JSON array):** `["K-B"]`

**Evidence on the drawing / model**

- equipment K-B reads "K-B Ammonia R-717 screw compressor B" (`units[K-B]`)
- Checked, none found: no variable speed drive or speed controller drawn on this compressor (`applies_when.without`)

**Data to collect**

- Slide valve (capacity) position over normal operation [not on drawing]. Where: DCS/PLC configuration: slide valve position or percent capacity per compressor from the refrigeration plant controls, a month or more. How: Hours spent below full load, by load band.
- Compressor power and run hours [not on drawing]. Where: a walkdown: power logger on the compressor motor across a normal week. How: Power at each load band, so part-load efficiency can be seen.
- How the compressors are sequenced [not on drawing]. Where: DCS/PLC configuration: which compressor trims, and the order and pressures at which they load and unload. How: Note whether more than one machine trims at the same time.

**How it is decided:** Worth a look when screws spend long hours part-loaded on the slide valve while another could be off, or when no machine on a suction level has speed control to trim. Close it if each runs near full load or a sequencer already keeps one machine trimming.

**What the source says (S25):** Among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003): "Slide valve unloading of oversized screw compressors." and "Hot gas bypass of compressors." Speed control (S25, p. 63): "ASDs used on compressors below a part-load ratio of about 95% will deliver performance equal to a fixed speed compressor but with lower electricity requirements. However, at near full (i.e., 100%) load, ASDs are approximately 3% less efficient than fixed speed drives".

**Limits:** A drive or sequencing change goes through the compressor vendor (minimum speed, oil management, vibration). Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not.

## Sources cited above

- S25: Brush, Masanet and Worrell, Energy Efficiency Improvement and Cost Saving Opportunities for the Dairy Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-6261E, Oct 2011). https://www.osti.gov/servlets/purl/1171534 (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
