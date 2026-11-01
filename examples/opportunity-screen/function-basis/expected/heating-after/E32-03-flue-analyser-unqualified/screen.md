# Opportunity screen: Fictional E32 source-adequacy development control

Model: `examples/opportunity-screen/function-basis/models/E32-03-flue-analyser-unqualified.json`. Questions: `data/questions.json`.

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

### E32: What do existing records establish about this represented burner air-fuel operating basis, the supplied analysis or metering candidates and applicable process-air constraints?

**About:** O-A  

**Finding reference (JSON string):** `"E32@O-A"`
**Asset IDs (JSON array):** `["O-A", "F-A", "O2-A"]`

**Evidence on the drawing / model**

- equipment O-A reads "O-A Batch product oven A" (`units[O-A]`)
- Burner or fuel supply: instrument F-A reads "F-A Natural gas burner fuel supply; installed ratio and operating basis unknown" at O-A (`instruments[F-A]`)
- Unclassified oxygen or analysis record candidate: instrument O2-A reads "O2-A Flue oxygen analyser candidate; as-operated suitability unresolved" at O-A (`instruments[O2-A]`)
- Supplied candidate field: `"O2-A enabled = false; present; meaning and suitability unverified"` (`"instruments[O2-A].facts.enabled"`)
- Supplied candidate field: `"O2-A calibration_current = \"unknown\"; blank; meaning and suitability unverified"` (`"instruments[O2-A].facts.calibration_current"`)
- Supplied candidate field: `"O2-A last_verified_load_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"instruments[O2-A].facts.last_verified_load_basis"`)
- Supplied candidate field: `"O2-A reported_oxygen_percent = 0; present; meaning and suitability unverified"` (`"instruments[O2-A].facts.reported_oxygen_percent"`)

**Data to collect**

- Existing air-fuel or flue-analysis, tuning and calibration records [not on drawing]. Where: site records: approved existing burner tuning, paired air/fuel flow-metering or flue-analysis reports, or their combination, with equipment, author/owner, date, quantity, sampling location, units/basis and high/low-fire or representative load coverage; then maintenance records: existing analyser/meter calibration, maintenance and suitability records and the reported flue oxygen/combustibles and exhaust-temperature context where available. How: Use an appropriate flow-metering, flue-analysis or combined method; a permanently installed O2 analyser is not mandatory. An oxygen/composition label may refer to product or another purpose and is not a flue-combustion basis. Preserve supplied false, zero and unknown values without qualifying them as actual function, calibration or performance.
- Existing ratio-control function and applicable equipment guidance [not on drawing]. Where: site records: approved existing burner/ratio-control configuration, active/fallback or manual mode, linkage or trim basis, revision and identified responsible owner; then the vendor datasheet: applicable burner/equipment guidance and documented air-fuel/excess-air requirements across its operating range; then DCS/PLC configuration: permitted existing burner-management and ratio-control configuration records, only through the company-approved access route. How: Separate a named ratio, analyser or enabled flag from reviewed as-operated evidence. Compare only on an applicable documented fuel, operating and method basis; this screen supplies no universal O2 target, ratio setting or adjustment permission.
- Existing fuel and production records for an appropriate operating basis [not on drawing]. Where: site records: approved existing identified fuel/input and production/load records over a justified representative period, including dates, units and relevant conditions; then historian or DCS trend for F-A (no historian tag is mapped in this model for these); then utility bills or the site energy report: existing identified unit fuel sub-meter records where suitable for the proposed comparison. How: Keep high/low-fire or other representative load evidence distinct from a nominal rating or an isolated number. No fixed month, new logging task, efficiency result or fuel-saving estimate is inferred.
- Existing process-air constraints and qualified review disposition [not on drawing]. Where: site records: approved existing drying, moisture/solvent removal, dilution/exhaust and product/safety basis, including any applicable flammable-vapour constraints and their revision/owner; then the vendor datasheet: applicable equipment minimum process-air/exhaust requirements and the qualified company burner/process review route. How: Combustion air and process drying/dilution needs are not interchangeable. Review applicable documented limits rather than minimizing air from an O2 label. Return evidence, unresolved basis and next owner; any new measurement or adjustment is separately approved qualified work.

**How it is decided:** Use qualified existing records to establish the applicable combustion and process-air basis and identify unresolved method, calibration, load or constraint evidence. Either appropriate air/fuel metering, flue analysis or a combination can support the review. Neither presence nor absence of a label establishes efficiency, a fault or need for adjustment. A responsible company reviewer can answer from adequate records or define a separately approved follow-up; this screen does not select operating settings.

**What the source says (S27):** S27 (p. 1): "Periodic checking and resetting of air-fuel ratios for burners is one of the simplest ways to get maximum efficiency out of fuel-fired process heating equipment such as furnaces, ovens, heaters, and boilers." And: "Processes that evaporate moisture or solvents need large amounts of excess air to dilute flammable solvents to noncombustible levels, to ensure adequate drying rates, and to carry vapors out of the oven. Lowering excess air to minimal levels can slow down the process and create an explosion hazard." No typical % stated (the sheet's worked example is one furnace).

**Limits:** DOE S27 supports periodic suitable-basis checks and notes differing high/low-fire and drying/solvent-removal conditions. Keeping this represented fuel-fired subject in records review is authored collection policy, not a universal mandatory project or quoted always-open rule. The unchanged hard gate requires a separate same-unit burner/fuel record; own gas-fired unit name alone remains outside this measured repair. Same-unit oxygen/composition records are unclassified context until their actual purpose/location is qualified; foreign records do not establish this unit basis. Calibration/load-quality checks are engineering interpretation. Company access, burner-management and qualified engineering procedures govern any actual field or operational work.

## Sources cited above

- S27: DOE Industrial Technologies Program, Process Heating Tip Sheet #2, Check Burner Air to Fuel Ratios (Nov 2007). https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/42110.pdf (license: Public domain (US federal))
