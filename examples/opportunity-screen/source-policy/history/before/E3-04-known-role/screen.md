# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/steam-pump-records/models/E3-04-known-role.json`. Questions: `data/questions.json`.

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

### E3: Does this pump recirculate flow continuously through a minimum-flow line?

**About:** P-A  

**Finding reference (JSON string):** `"E3@P-A"`
**Asset IDs (JSON array):** `["P-A", "HV-A"]`

**Evidence on the drawing / model**

- equipment P-A reads "P-A Fictional pumpA" (`units[P-A]`)
- Minimum-flow line: hand valve HV-A reads "HV-A Minimum-flow recirculation candidate" at P-A (`manual_valves[HV-A]`)

**Data to collect**

- Recirculation flow versus forward flow [not on drawing]. Where: only a valve (HV-A) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then a walkdown: clamp-on ultrasonic flow meter on the recirculation line. How: Measure both flows at normal operation.
- Hours the recirculation is open [not on drawing]. Where: only a valve (HV-A) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: operator logs. How: Count hours with recirculation flow.

**How it is decided:** Worth action when recirculation flows continuously at normal throughput (an orifice that is always open, or a valve that never closes); an automatic valve that only opens at low forward flow is doing its job.

**What the source says (S13):** "the energy needed to push fluid through bypass lines is wasted." No % stated.

**Limits:** Minimum flow protects the pump; never remove it without the pump vendor's minimum continuous flow.

### E3: Does this pump recirculate flow continuously through a minimum-flow line?

**About:** P-B  

**Finding reference (JSON string):** `"E3@P-B"`
**Asset IDs (JSON array):** `["P-B", "HV-B"]`

**Evidence on the drawing / model**

- equipment P-B reads "P-B Fictional pumpB" (`units[P-B]`)
- Minimum-flow line: hand valve HV-B reads "HV-B Minimum-flow recirculation candidate" at P-B (`manual_valves[HV-B]`)

**Data to collect**

- Recirculation flow versus forward flow [not on drawing]. Where: only a valve (HV-B) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then a walkdown: clamp-on ultrasonic flow meter on the recirculation line. How: Measure both flows at normal operation.
- Hours the recirculation is open [not on drawing]. Where: only a valve (HV-B) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: operator logs. How: Count hours with recirculation flow.

**How it is decided:** Worth action when recirculation flows continuously at normal throughput (an orifice that is always open, or a valve that never closes); an automatic valve that only opens at low forward flow is doing its job.

**What the source says (S13):** "the energy needed to push fluid through bypass lines is wasted." No % stated.

**Limits:** Minimum flow protects the pump; never remove it without the pump vendor's minimum continuous flow.

## Sources cited above

- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
