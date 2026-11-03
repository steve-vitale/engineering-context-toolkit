# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/steam-pump-records/models/E7-01-screening-thresholds.json`. Questions: `data/questions.json`.

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

### E7: Does a steam pressure-reducing valve between headers pass enough steam to drive a backpressure turbogenerator instead?

**About:** PCV-A  

**Finding reference (JSON string):** `"E7@PCV-A"`
**Asset IDs (JSON array):** `["PCV-A"]`

**Evidence on the drawing / model**

- Trigger: `"valve PCV-A reads \"PCV-A Steam PRV HP HEADER to LP HEADER\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"PCV-A\", \"kind\": \"final_element\", \"unit\": null, \"source\": \"Fictional candidate station, not installed-state proof\", \"assigned_tag\": true, \"unplaced_reason\": \"Fictional explicitly unplaced station; no inventoried equipment owner\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[PCV-A]"`)

**Data to collect**

- Steam flow through the station over a year [not on drawing]. Where: only a valve (PCV-A) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: steam balance. How: "Develop steam flow/duration curves for each PRV station".
- Upstream and downstream pressures [not on drawing]. Where: a walkdown: gauges either side of the station; then site records: header design pressures. How: Record both at normal operation.

**How it is decided:** Consider a backpressure turbogenerator only if the station passes a constant flow of at least 3,000 lb/hr with a pressure drop of at least 100 psi (S6's condition); otherwise close this screening investigation.

**What the source says (S6):** Consider when a PRV has "constant steam flows of at least 3,000 pounds per hour (lb/hr), and when the steam pressure drop is at least 100 psi." Installation costs "typically average 75% of equipment costs".

**Limits:** S6 also quotes cost per kW figures; they are deliberately not repeated here. No IAC code maps to turbines (2.2134 covers PRV-station leaks).

### E7: Does a steam pressure-reducing valve between headers pass enough steam to drive a backpressure turbogenerator instead?

**About:** PCV-B  

**Finding reference (JSON string):** `"E7@PCV-B"`
**Asset IDs (JSON array):** `["PCV-B"]`

**Evidence on the drawing / model**

- Trigger: `"valve PCV-B reads \"PCV-B Steam PRV HP HEADER to LP HEADER\"; owning equipment unknown; no unit inferred; supplied source interpretation, not installed truth; Recorded qualifiers: {\"tag\": \"PCV-B\", \"kind\": \"final_element\", \"unit\": null, \"source\": \"Fictional candidate station, not installed-state proof\", \"assigned_tag\": true, \"unplaced_reason\": \"Fictional explicitly unplaced station; no inventoried equipment owner\"}; Assigned identifier; an operating tag has not been verified"` (`"unplaced[PCV-B]"`)

**Data to collect**

- Steam flow through the station over a year [not on drawing]. Where: only a valve (PCV-B) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: steam balance. How: "Develop steam flow/duration curves for each PRV station".
- Upstream and downstream pressures [not on drawing]. Where: a walkdown: gauges either side of the station; then site records: header design pressures. How: Record both at normal operation.

**How it is decided:** Consider a backpressure turbogenerator only if the station passes a constant flow of at least 3,000 lb/hr with a pressure drop of at least 100 psi (S6's condition); otherwise close this screening investigation.

**What the source says (S6):** Consider when a PRV has "constant steam flows of at least 3,000 pounds per hour (lb/hr), and when the steam pressure drop is at least 100 psi." Installation costs "typically average 75% of equipment costs".

**Limits:** S6 also quotes cost per kW figures; they are deliberately not repeated here. No IAC code maps to turbines (2.2134 covers PRV-station leaks).

## Sources cited above

- S6: Steam Tip #20, Replace Pressure-Reducing Valves with Backpressure Turbogenerators (DOE/GO-102012-3409). https://www.energy.gov/sites/prod/files/2014/05/f16/steam20_turbogenerators.pdf (license: Public domain)
