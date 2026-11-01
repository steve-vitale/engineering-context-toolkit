# Opportunity screen: ILLUSTRATIVE source-adequacy counterexample

Model: `examples/opportunity-screen/function-basis/models/E29-02-own-drive-label.json`. Questions: `data/questions.json`.

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

### E29: What records support this refrigeration compressor's part-load control, sequencing and real-input basis?

**About:** K-A  

**Finding reference (JSON string):** `"E29@K-A"`
**Asset IDs (JSON array):** `["K-A", "SC-A"]`

**Evidence on the drawing / model**

- equipment K-A reads "K-A Ammonia R-717 screw compressor A" (`units[K-A]`)
- Drive label candidate: final element SC-A reads "SC-A VFD candidate, enabled/mode/history unknown" at K-A (`final_elements[SC-A]`)
- Supplied candidate field: `"SC-A enabled = \"unknown\"; blank; meaning and suitability unverified"` (`"final_elements[SC-A].facts.enabled"`)
- Supplied candidate field: `"SC-A source_revision = \"draft-A\"; present; meaning and suitability unverified"` (`"final_elements[SC-A].facts.source_revision"`)

**Data to collect**

- Capacity-control mode and representative load for this compressor [not on drawing]. Where: DCS/PLC configuration: existing identified compressor configuration and active/fallback mode, slide-valve or bypass function, revision and responsible owner; then site records: permitted load/capacity histories with machine identity, period and coincident suction/demand conditions. How: Retain labels and enabled/disabled/unknown qualifiers as candidates. Establish actual function and a representative operating basis; a nameplate or drive label does not establish part-load behavior.
- Representative real input power on the same operating basis [not on drawing]. Where: site records: approved existing electrical-input and run/load observations with quantity, units, time and conversion basis; then the vendor datasheet: applicable compressor/drive limits and part-load performance basis. How: Compare suitable coincident input and load records. Separate ratings, electrical indications and near-full-load conditions from actual representative real input; request missing evidence without inventing a value or authorizing measurements.
- Actual sequencing, served group and applicable supplier constraints [not on drawing]. Where: DCS/PLC configuration: existing reviewed sequence/trim logic, machine-to-suction-group association, active overrides and revision; then site records: permitted operating/event records showing which machines actually trim under comparable conditions; then the vendor datasheet: applicable supplier constraints and responsible engineering review route. How: A sequencer label alone does not establish active operation or complete group coverage. Return a qualified partial answer or missing-evidence request to the responsible reviewer.

**How it is decided:** Investigate missing or conflicting source/function/operating evidence for each named machine. A drive or sequencing label does not settle efficiency, and the source describes load-dependent tradeoffs. Close only the source investigation after qualified evidence review; no drive change, operating instruction or savings estimate follows.

**What the source says (S25):** Among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003): "Slide valve unloading of oversized screw compressors." and "Hot gas bypass of compressors." Speed control (S25, p. 63): "ASDs used on compressors below a part-load ratio of about 95% will deliver performance equal to a fixed speed compressor but with lower electricity requirements. However, at near full (i.e., 100%) load, ASDs are approximately 3% less efficient than fixed speed drives".

**Limits:** This is an authored per-machine collection policy informed by S25 printed pp.59,62,63, not a quoted design requirement or installed-state diagnosis. Labels and literal facts remain unverified candidates; review actual association, operating conditions and supplier constraints. No fixed observation duration or operating limit is inferred. A drive or sequencing change goes through the compressor vendor (minimum speed, oil management, vibration). Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not.

### E29: What records support this refrigeration compressor's part-load control, sequencing and real-input basis?

**About:** K-B  

**Finding reference (JSON string):** `"E29@K-B"`
**Asset IDs (JSON array):** `["K-B"]`

**Evidence on the drawing / model**

- equipment K-B reads "K-B Ammonia R-717 screw compressor B" (`units[K-B]`)

**Data to collect**

- Capacity-control mode and representative load for this compressor [not on drawing]. Where: DCS/PLC configuration: existing identified compressor configuration and active/fallback mode, slide-valve or bypass function, revision and responsible owner; then site records: permitted load/capacity histories with machine identity, period and coincident suction/demand conditions. How: Retain labels and enabled/disabled/unknown qualifiers as candidates. Establish actual function and a representative operating basis; a nameplate or drive label does not establish part-load behavior.
- Representative real input power on the same operating basis [not on drawing]. Where: site records: approved existing electrical-input and run/load observations with quantity, units, time and conversion basis; then the vendor datasheet: applicable compressor/drive limits and part-load performance basis. How: Compare suitable coincident input and load records. Separate ratings, electrical indications and near-full-load conditions from actual representative real input; request missing evidence without inventing a value or authorizing measurements.
- Actual sequencing, served group and applicable supplier constraints [not on drawing]. Where: DCS/PLC configuration: existing reviewed sequence/trim logic, machine-to-suction-group association, active overrides and revision; then site records: permitted operating/event records showing which machines actually trim under comparable conditions; then the vendor datasheet: applicable supplier constraints and responsible engineering review route. How: A sequencer label alone does not establish active operation or complete group coverage. Return a qualified partial answer or missing-evidence request to the responsible reviewer.

**How it is decided:** Investigate missing or conflicting source/function/operating evidence for each named machine. A drive or sequencing label does not settle efficiency, and the source describes load-dependent tradeoffs. Close only the source investigation after qualified evidence review; no drive change, operating instruction or savings estimate follows.

**What the source says (S25):** Among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003): "Slide valve unloading of oversized screw compressors." and "Hot gas bypass of compressors." Speed control (S25, p. 63): "ASDs used on compressors below a part-load ratio of about 95% will deliver performance equal to a fixed speed compressor but with lower electricity requirements. However, at near full (i.e., 100%) load, ASDs are approximately 3% less efficient than fixed speed drives".

**Limits:** This is an authored per-machine collection policy informed by S25 printed pp.59,62,63, not a quoted design requirement or installed-state diagnosis. Labels and literal facts remain unverified candidates; review actual association, operating conditions and supplier constraints. No fixed observation duration or operating limit is inferred. A drive or sequencing change goes through the compressor vendor (minimum speed, oil management, vibration). Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not.

## Sources cited above

- S25: Brush, Masanet and Worrell, Energy Efficiency Improvement and Cost Saving Opportunities for the Dairy Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-6261E, Oct 2011). https://www.osti.gov/servlets/purl/1171534 (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
