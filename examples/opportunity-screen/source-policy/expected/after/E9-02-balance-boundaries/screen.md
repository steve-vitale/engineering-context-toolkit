# Opportunity screen: Fictional original-source question control

Model: `examples/opportunity-screen/source-policy/models/E9-02-balance-boundaries.json`. Questions: `data/questions.json`.

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

### E9: What do existing records establish about these drain-labelled condensate candidates' actual service, route and any suitable recovery question?

**About:** CR-A, CR-B  

**Finding reference (JSON string):** `"E9@model"`
**Asset IDs (JSON array):** `["CR-A", "CR-B"]`

**Evidence on the drawing / model**

- equipment CR-A reads "CR-A CONDENSATE TO DRAIN candidate" (`units[CR-A]`)
- equipment CR-B reads "CR-B CONDENSATE TO DRAIN candidate" (`units[CR-B]`)
- Supplied candidate field: `"CR-A fictional_record = true; present; meaning and suitability unverified"` (`"units[CR-A].facts.fictional_record"`)
- Supplied candidate field: `"CR-A record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[CR-A].facts.record_source"`)
- Supplied candidate field: `"CR-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[CR-A].facts.record_revision"`)
- Supplied candidate field: `"CR-A record_available = true; present; meaning and suitability unverified"` (`"units[CR-A].facts.record_available"`)
- Supplied candidate field: `"CR-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[CR-A].facts.record_authority"`)
- Supplied candidate field: `"CR-A service = \"steamwater\"; present; meaning and suitability unverified"` (`"units[CR-A].facts.service"`)
- Supplied candidate field: `"CR-A flow_unit = \"allmasslb/hr\"; present; meaning and suitability unverified"` (`"units[CR-A].facts.flow_unit"`)
- Supplied candidate field: `"CR-A sample_period = \"samefictionalinterval\"; present; meaning and suitability unverified"` (`"units[CR-A].facts.sample_period"`)
- Supplied candidate field: `"CR-A makeup_flow = 20; present; meaning and suitability unverified"` (`"units[CR-A].facts.makeup_flow"`)
- Supplied candidate field: `"CR-A feedwater_flow = 100; present; meaning and suitability unverified"` (`"units[CR-A].facts.feedwater_flow"`)
- Supplied candidate field: `"CR-A blowdown_flow = 10; present; meaning and suitability unverified"` (`"units[CR-A].facts.blowdown_flow"`)
- Supplied candidate field: `"CR-A balance_boundary = \"includesblowdown; returnpercentdenominatornotdeclared\"; present; meaning and suitability unverified"` (`"units[CR-A].facts.balance_boundary"`)
- Supplied candidate field: `"CR-B fictional_record = true; present; meaning and suitability unverified"` (`"units[CR-B].facts.fictional_record"`)
- Supplied candidate field: `"CR-B record_source = \"Fictional development packet; no plant or human approval\"; present; meaning and suitability unverified"` (`"units[CR-B].facts.record_source"`)
- Supplied candidate field: `"CR-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[CR-B].facts.record_revision"`)
- Supplied candidate field: `"CR-B record_available = true; present; meaning and suitability unverified"` (`"units[CR-B].facts.record_available"`)
- Supplied candidate field: `"CR-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[CR-B].facts.record_authority"`)
- Supplied candidate field: `"CR-B service = \"steamwater\"; present; meaning and suitability unverified"` (`"units[CR-B].facts.service"`)
- Supplied candidate field: `"CR-B flow_unit = \"makeupm3/h; feedwaterlb/hr\"; present; meaning and suitability unverified"` (`"units[CR-B].facts.flow_unit"`)
- Supplied candidate field: `"CR-B sample_period = \"differentintervals\"; present; meaning and suitability unverified"` (`"units[CR-B].facts.sample_period"`)
- Supplied candidate field: `"CR-B makeup_flow = 20; present; meaning and suitability unverified"` (`"units[CR-B].facts.makeup_flow"`)
- Supplied candidate field: `"CR-B feedwater_flow = 100; present; meaning and suitability unverified"` (`"units[CR-B].facts.feedwater_flow"`)
- On drawing: Supplied candidate fact, basis unverified: CR-A fictional_record = True (`units[CR-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: CR-B fictional_record = True (`units[CR-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: CR-A record_source = Fictional development packet; no plant or human approval (`units[CR-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: CR-B record_source = Fictional development packet; no plant or human approval (`units[CR-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: CR-A record_revision = R1 (`units[CR-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: CR-B record_revision = R1 (`units[CR-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: CR-A record_available = True (`units[CR-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: CR-B record_available = True (`units[CR-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: CR-A record_authority = unverified (`units[CR-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: CR-B record_authority = unverified (`units[CR-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: CR-A service = steamwater (`units[CR-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: CR-B service = steamwater (`units[CR-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: CR-A flow_unit = allmasslb/hr (`units[CR-A].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: CR-B flow_unit = makeupm3/h; feedwaterlb/hr (`units[CR-B].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: CR-A sample_period = samefictionalinterval (`units[CR-A].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: CR-B sample_period = differentintervals (`units[CR-B].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: CR-A makeup_flow = 20 (`units[CR-A].facts.makeup_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-B makeup_flow = 20 (`units[CR-B].facts.makeup_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-A feedwater_flow = 100 (`units[CR-A].facts.feedwater_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-B feedwater_flow = 100 (`units[CR-B].facts.feedwater_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-A blowdown_flow = 10 (`units[CR-A].facts.blowdown_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-A balance_boundary = includesblowdown; returnpercentdenominatornotdeclared (`units[CR-A].facts.balance_boundary`)
- On drawing: Supplied candidate fact, basis unverified: CR-A fictional_record = True (`units[CR-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: CR-B fictional_record = True (`units[CR-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: CR-A record_source = Fictional development packet; no plant or human approval (`units[CR-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: CR-B record_source = Fictional development packet; no plant or human approval (`units[CR-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: CR-A record_revision = R1 (`units[CR-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: CR-B record_revision = R1 (`units[CR-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: CR-A record_available = True (`units[CR-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: CR-B record_available = True (`units[CR-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: CR-A record_authority = unverified (`units[CR-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: CR-B record_authority = unverified (`units[CR-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: CR-A service = steamwater (`units[CR-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: CR-B service = steamwater (`units[CR-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: CR-A flow_unit = allmasslb/hr (`units[CR-A].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: CR-B flow_unit = makeupm3/h; feedwaterlb/hr (`units[CR-B].facts.flow_unit`)
- On drawing: Supplied candidate fact, basis unverified: CR-A sample_period = samefictionalinterval (`units[CR-A].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: CR-B sample_period = differentintervals (`units[CR-B].facts.sample_period`)
- On drawing: Supplied candidate fact, basis unverified: CR-A makeup_flow = 20 (`units[CR-A].facts.makeup_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-B makeup_flow = 20 (`units[CR-B].facts.makeup_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-A feedwater_flow = 100 (`units[CR-A].facts.feedwater_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-B feedwater_flow = 100 (`units[CR-B].facts.feedwater_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-A blowdown_flow = 10 (`units[CR-A].facts.blowdown_flow`)
- On drawing: Supplied candidate fact, basis unverified: CR-A balance_boundary = includesblowdown; returnpercentdenominatornotdeclared (`units[CR-A].facts.balance_boundary`)

**Data to collect**

- Existing per-candidate service, route and comparable water/mass-balance records [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): CR-A (CR-A) fictional_record = true [units[CR-A].facts.fictional_record]; CR-B (CR-B) fictional_record = true [units[CR-B].facts.fictional_record]; CR-A (CR-A) record_source = "Fictional development packet; no plant or human approval" [units[CR-A].facts.record_source]; CR-B (CR-B) record_source = "Fictional development packet; no plant or human approval" [units[CR-B].facts.record_source]; CR-A (CR-A) record_revision = "R1" [units[CR-A].facts.record_revision]; CR-B (CR-B) record_revision = "R1" [units[CR-B].facts.record_revision]; CR-A (CR-A) record_available = true [units[CR-A].facts.record_available]; CR-B (CR-B) record_available = true [units[CR-B].facts.record_available]; CR-A (CR-A) record_authority = "unverified" [units[CR-A].facts.record_authority]; CR-B (CR-B) record_authority = "unverified" [units[CR-B].facts.record_authority]; CR-A (CR-A) service = "steamwater" [units[CR-A].facts.service]; CR-B (CR-B) service = "steamwater" [units[CR-B].facts.service]; CR-A (CR-A) flow_unit = "allmasslb/hr" [units[CR-A].facts.flow_unit]; CR-B (CR-B) flow_unit = "makeupm3/h; feedwaterlb/hr" [units[CR-B].facts.flow_unit]; CR-A (CR-A) sample_period = "samefictionalinterval" [units[CR-A].facts.sample_period]; CR-B (CR-B) sample_period = "differentintervals" [units[CR-B].facts.sample_period]; CR-A (CR-A) makeup_flow = 20 [units[CR-A].facts.makeup_flow]; CR-B (CR-B) makeup_flow = 20 [units[CR-B].facts.makeup_flow]; CR-A (CR-A) feedwater_flow = 100 [units[CR-A].facts.feedwater_flow]; CR-B (CR-B) feedwater_flow = 100 [units[CR-B].facts.feedwater_flow]; CR-A (CR-A) blowdown_flow = 10 [units[CR-A].facts.blowdown_flow]; CR-A (CR-A) balance_boundary = "includesblowdown; returnpercentdenominatornotdeclared" [units[CR-A].facts.balance_boundary]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-source/stream steam-water service and actual route/revision, return/makeup/feedwater/blowdown and other-loss/inventory records, temperatures/pressures/flash, actual flow/duration, quantity units and matching sample/operating boundaries.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: A drain caption may be historical or nonwater; establish service/current route before interpreting it as lost boiler-water condensate. Known hydrocarbon condensate is not this boiler-return task; unknown service remains conditional. Do not present1-makeup/feedwater as exact return percent without a justified boundary, denominator, losses/blowdown/inventory and matched quantities/units/time/conversions. Preserve source-qualified values and uncertainty, not an automatic quotient.
- Existing quality, treatment, receiving-system and feasibility basis [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): CR-A (CR-A) fictional_record = true [units[CR-A].facts.fictional_record]; CR-B (CR-B) fictional_record = true [units[CR-B].facts.fictional_record]; CR-A (CR-A) record_source = "Fictional development packet; no plant or human approval" [units[CR-A].facts.record_source]; CR-B (CR-B) record_source = "Fictional development packet; no plant or human approval" [units[CR-B].facts.record_source]; CR-A (CR-A) record_revision = "R1" [units[CR-A].facts.record_revision]; CR-B (CR-B) record_revision = "R1" [units[CR-B].facts.record_revision]; CR-A (CR-A) record_available = true [units[CR-A].facts.record_available]; CR-B (CR-B) record_available = true [units[CR-B].facts.record_available]; CR-A (CR-A) record_authority = "unverified" [units[CR-A].facts.record_authority]; CR-B (CR-B) record_authority = "unverified" [units[CR-B].facts.record_authority]; CR-A (CR-A) service = "steamwater" [units[CR-A].facts.service]; CR-B (CR-B) service = "steamwater" [units[CR-B].facts.service]; CR-A (CR-A) flow_unit = "allmasslb/hr" [units[CR-A].facts.flow_unit]; CR-B (CR-B) flow_unit = "makeupm3/h; feedwaterlb/hr" [units[CR-B].facts.flow_unit]; CR-A (CR-A) sample_period = "samefictionalinterval" [units[CR-A].facts.sample_period]; CR-B (CR-B) sample_period = "differentintervals" [units[CR-B].facts.sample_period]; CR-A (CR-A) makeup_flow = 20 [units[CR-A].facts.makeup_flow]; CR-B (CR-B) makeup_flow = 20 [units[CR-B].facts.makeup_flow]; CR-A (CR-A) feedwater_flow = 100 [units[CR-A].facts.feedwater_flow]; CR-B (CR-B) feedwater_flow = 100 [units[CR-B].facts.feedwater_flow]; CR-A (CR-A) blowdown_flow = 10 [units[CR-A].facts.blowdown_flow]; CR-A (CR-A) balance_boundary = "includesblowdown; returnpercentdenominatornotdeclared" [units[CR-A].facts.balance_boundary]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing stream-specific quality/contamination and sampling records, potential dissolved/particulate sources, treatment/cleanup options, routing/receiving capacity and pressure, flash/safety/material constraints and economic/operating coverage; source/revision/availability retained.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new field test, operating change or retrofit.. How: Clean or steady alone does not authorize return equipment, and contaminated or small streams are not automatically required to remain at drain: review suitable treatment, route, receiving and economic constraints with the responsible engineer. S8 printed20–21 and supplemental DOE Tip8 pp1–2 discuss actual recovery equipment, cleanup and explicit example assumptions. Acknowledge an existing suitable route/treatment without new measurements or changes; source examples are not site savings.

**How it is decided:** Review actual steam-water service, current route and stream-specific quality/treatment, flow/duty, temperature/pressure/flash and receiving/economic constraints before a recovery decision. Do not automatically return clean/steady flow or permanently reject contaminated/small flow; neither label nor a simple unqualified makeup quotient establishes suitability or benefit. Existing suitable basis or nonapplicability may be acknowledged; unresolved data remains a records question with no operational/hardware authorization.

**What the source says (S8, S19, S24):** Enthalpy difference "generally over 120 Btu/lb, an amount of energy that is often more than 10% of the energy in the boiler generated steam." LBNL (as reported in LBNL-56183): "Condensate Return Alone 10%", 1.1 yr.
IAC/ITAC recommendation code: 2.2121 (IAC/ITAC browse page: 354 recommendations, 1.2 yr average payback, 50.9% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S8 printed20–21 covers condensate recovery/cleanup and system constraints. Supplemental original DOE Tip8 (https://www.energy.gov/sites/prod/files/2014/05/f16/steam8_boiler.pdf), completepp1–2, was admitted before criteria and provides conditional data-driven recovery/treatment and explicit heat/flash/economic examples. Inherited S19/S24 figures are not reverified here or current site benefits.

## Sources cited above

- S8: Improving Steam System Performance: A Sourcebook for Industry, 2nd ed. (DOE/GO-102012-3423, rev. Oct 2012). https://www.energy.gov/sites/prod/files/2014/05/f15/steamsourcebook.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
