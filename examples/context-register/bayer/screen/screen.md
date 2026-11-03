# Opportunity screen: Bayer CropScience methomyl residue treater (Institute, West Virginia), as described by the CSB

Model: `data/bayer_rt/process_model.json`. Questions: `data/questions.json`.

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

### E18: What do existing records establish about these cooling/steam-labelled candidates' process-stream duties and any system-level heat-integration question?

**About:** U2, HV-112  

**Finding reference (JSON string):** `"E18@model"`
**Asset IDs (JSON array):** `["stream:U2", "HV-112", "stream:U1", "FT-106", "TV-104C", "HV-108"]`

**Evidence on the drawing / model**

- stream U2 (asset stream:U2) reads "Cooling water (80 C) supply to the cooler" at E-3 (`streams[U2]`)
- hand valve HV-112 reads "HV-112 Cooling water supply valve" at E-3 (`manual_valves[HV-112]`)
- Steam-heated user: stream U1 (asset stream:U1) reads "Steam supply to the heater" at E-2 (`streams[U1]`)
- Steam-heated user: instrument FT-106 reads "FT-106 Indicated steam flow to the heater" at E-2 (`instruments[FT-106]`)
- Steam-heated user: valve TV-104C reads "TV-104C Steam flow valve to the heater (Fig 10: Temperature Control Valve)" at E-2 (`final_elements[TV-104C]`)
- Steam-heated user: hand valve HV-108 reads "HV-108 Steam block valve, heater steam supply" at E-2 (`manual_valves[HV-108]`)

**Data to collect**

- Existing exact process-stream identities, temperature-enthalpy and duty basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: only a valve (HV-112) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then historian or DCS trend for FT-106 (no historian tag is mapped in this model for these); then site records: Existing process/utility identities and directions, actual supply/target temperatures, flows, heat-capacity/phase/duty and operating coverage for each represented cooling and steam candidate; source/revision/availability, quantity units and matching sample periods retained.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A CW or steam valve/instrument label is a proxy, not measured process heat rejection/heating, a process-stream identity or a flow signal. Retain each owner/source separately, including related steam-record values shown as candidate evidence. Review actual comparable process duties and uncertainty before inferring any match; command values, foreign data or incompatible units/periods cannot settle it.
- Existing process-wide targets and time-aware operating constraints [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing heat/material balance, process-wide temperature-enthalpy/composite profiles and utility targets, batch sequences and timing, current studies and alternatives, with source scope and economic/operating assumptions.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: S19 printed43-45 describes process-wide composite curves, approach/capital-energy tradeoffs and developments for batch/time-aware integration and heat pumps/transformers. Do not replace that analysis with a rule that all hot temperatures must exceed all cold temperatures, or automatically close every non-simultaneous/batch pair. Conversely, overlapping ideal profiles or an alternative technology name is not proof of feasible recovery. Review the appropriate system and timing model before deciding.
- Existing physical, material, fouling and hazard/feasibility basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing layout/routing and fouling/cleaning records, composition/pressure/material and cross-contamination constraints, reactive/process hazard review, existing exchanger/network function and economic/practical basis; authority and missing records remain explicit.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: Existing suitable studies may be acknowledged without new measurements or a compulsory exchanger study. On reactive service an integration change needs the applicable hazard review; a missing review, supplied Boolean or source label is not protection acceptance. No piping connection, operating change, whole-process completeness or site saving follows from the represented pair.

**How it is decided:** Review the actual process-wide temperature-enthalpy/utility targets, stream identities and duty/time basis, practical approach/capital tradeoffs and physical/material/hazard constraints before an integration decision. Do not prescribe a connection or automatically close a question from a pairwise temperature-range, simultaneity, hours or distance shortcut. Suitable existing analysis or nonapplicability may be acknowledged; missing or contradictory source/units/time remains explicit.

**What the source says (S19, S24):** The source describes systematic process-wide temperature-enthalpy targeting and matching of heating/cooling demands, including time-aware batch approaches and alternatives. Potential depends on the actual process and capital-energy tradeoffs; this screen establishes no universal superiority, quantified benefit or site saving.
IAC/ITAC recommendation code: 2.243x; 2.244x (IAC/ITAC browse page: 2.243x: 3,673 recommendations, 1.4 yr average payback, 31.2% implemented; 2.244x: 1,466 recommendations, 1.7 yr, 28.6%; average dollar figure omitted).

**Limits:** The represented cooling-water and other-unit steam labels are screening proxies, not established process-stream duties or a feasible heat match. Review process-wide temperature-enthalpy targets, duty/time coverage and practical constraints; pairwise temperature ranges or simultaneity alone do not decide broader integration potential. On a reactive system any heat-integration change needs a hazard review first. IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: original LBNL-56183 printed43-45/PDF51-53 from the official ENERGY STAR mirror; raw equivalence to inaccessible catalog OSTI bytes is not claimed. The original far-exceeds comparative quotation remains historical; it is not evidence for this pair or a guarantee. Reactive-system hazard-review requirement is retained.

## Sources cited above

- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
