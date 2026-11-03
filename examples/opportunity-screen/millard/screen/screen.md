# Opportunity screen: Millard historical evaporator control-bank source subset

Model: `examples/opportunity-screen/millard/model.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
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

### E30: What records support this evaporator's defrost applicability, initiation and termination?

**About:** EVAP-GROUP  

**Finding reference (JSON string):** `"E30@EVAP-GROUP"`
**Asset IDs (JSON array):** `["EVAP-GROUP", "HG-MAIN"]`

**Evidence on the drawing / model**

- equipment EVAP-GROUP reads "EVAP-GROUP Ammonia blast freezer evaporator group" (`units[EVAP-GROUP]`)
- Defrost: final element HG-MAIN reads "HG-MAIN Hot gas main valve for defrost" at EVAP-GROUP (`final_elements[HG-MAIN]`)

**Data to collect**

- Applicability and actual initiation per named evaporator [not on drawing]. Where: DCS/PLC configuration: permitted current defrost configuration: target coil/unit, initiation and fallback mode, enabled/disabled state and revision; then site records: existing source-owner or supplier records establishing whether defrost applies to this unit and which indications actually initiate it. How: Keep timer/demand labels and DP readings as candidates. An indication, termination sensor or unit name does not prove active demand initiation; do not borrow another evaporator's control basis.
- Representative need and event/termination evidence [not on drawing]. Where: site records: approved existing frost/coil-pressure and defrost-event records, initiation reason, duration, termination and coincident conditions; then maintenance records: relevant recorded inspection or sensor/function checks and their dates. How: Separate evidence of need from initiation and termination. Retain quantity/location/units/time and missing history explicitly; no pressure threshold, event count or universal observation duration is supplied.
- Affected room/product constraints and review route [not on drawing]. Where: historian or DCS trend for HG-MAIN (no historian tag is mapped in this model for these); then site records: permitted room/product requirements, operating restrictions and existing reviewed defrost basis for the identified unit; then the vendor datasheet: applicable unit and control constraints and responsible reviewer. How: Use an existing-record fallback when no suitable mapped signal is supplied. Establish relevant effects and constraints through the company review route; no inspection, defrost or setting change is authorized.

**How it is decided:** Pursue missing applicability, source/function or representative event evidence. A drawn DP instrument or demand label does not settle whether defrost is initiated by actual need. Close only a qualified source investigation; no installed-control acceptance or operating change follows.

**What the source says (S25):** Demand defrost (S25, p. 66): "Evaporators should be defrosted only when necessary, as opposed to on timed schedules where defrosting occurs regardless of need." "Too frequent defrosts." is listed among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003). No % stated.

**Limits:** S25 printed p.66 discusses need-based defrost; per-unit keep-open collection and accepting an anchor's own description as a candidate are authored software/engineering policy. Neither absence nor presence of a DP/demand/termination label establishes actual use. Applicability, initiation, termination, source revision and operating/product constraints require review. The screen does not infer frost, installed timers, thresholds or permission.

## Sources cited above

- S25: Brush, Masanet and Worrell, Energy Efficiency Improvement and Cost Saving Opportunities for the Dairy Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-6261E, Oct 2011). https://www.osti.gov/servlets/purl/1171534 (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
