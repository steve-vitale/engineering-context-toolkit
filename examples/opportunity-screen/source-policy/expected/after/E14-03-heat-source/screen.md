# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/source-policy/models/E14-03-heat-source.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
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

### E14: What do existing records establish about this boiler/steam-generator candidate's flue/feedwater service and current heat-recovery coverage?

**About:** E-A  

**Finding reference (JSON string):** `"E14@E-A"`
**Asset IDs (JSON array):** `["E-A"]`

**Evidence on the drawing / model**

- equipment E-A reads "E-A Electric boiler" (`units[E-A]`)
- Supplied candidate field: `"E-A fictional_record = true; present; meaning and suitability unverified"` (`"units[E-A].facts.fictional_record"`)
- Supplied candidate field: `"E-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[E-A].facts.record_source"`)
- Supplied candidate field: `"E-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[E-A].facts.record_revision"`)
- Supplied candidate field: `"E-A record_available = true; present; meaning and suitability unverified"` (`"units[E-A].facts.record_available"`)
- Supplied candidate field: `"E-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[E-A].facts.record_authority"`)
- Supplied candidate field: `"E-A service = \"steamwater electric, noflue\"; present; meaning and suitability unverified"` (`"units[E-A].facts.service"`)
- Supplied candidate field: `"E-A stack_temperature = null; blank; meaning and suitability unverified"` (`"units[E-A].facts.stack_temperature"`)
- On drawing: Supplied candidate fact, basis unverified: E-A fictional_record = True (`units[E-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: E-A record_source = Fictional development record; no company or human approval (`units[E-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: E-A record_revision = R1 (`units[E-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: E-A record_available = True (`units[E-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: E-A record_authority = unverified (`units[E-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: E-A service = steamwater electric, noflue (`units[E-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: E-A fictional_record = True (`units[E-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: E-A record_source = Fictional development record; no company or human approval (`units[E-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: E-A record_revision = R1 (`units[E-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: E-A record_available = True (`units[E-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: E-A record_authority = unverified (`units[E-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: E-A service = steamwater electric, noflue (`units[E-A].facts.service`)

**Data to collect**

- Existing named-boiler flue/feedwater service and recovery association [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): E-A (E-A) fictional_record = true [units[E-A].facts.fictional_record]; E-A (E-A) record_source = "Fictional development record; no company or human approval" [units[E-A].facts.record_source]; E-A (E-A) record_revision = "R1" [units[E-A].facts.record_revision]; E-A (E-A) record_available = true [units[E-A].facts.record_available]; E-A (E-A) record_authority = "unverified" [units[E-A].facts.record_authority]; E-A (E-A) service = "steamwater electric, noflue" [units[E-A].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-subject boiler/steam-water, heat-source/flue and feedwater duty, installed recovery/route/coverage and source/revision/availability records; retain foreign or uncertain economizer associations explicitly.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: One economizer label anywhere cannot establish installed coverage, suitability or closure for every boiler. Establish relevant actual service and named coverage; known dry furnace/nonwater helper or electric/no-flue service is not this flue/feedwater task, and unknown service remains conditional. A source-labelled steam generator is reviewed for its actual function without inventing a fuel or drum. Acknowledge suitable existing records or nonapplicability before new observations.
- Existing tuned operating, receiving-feedwater and cold-end feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): E-A (E-A) fictional_record = true [units[E-A].facts.fictional_record]; E-A (E-A) record_source = "Fictional development record; no company or human approval" [units[E-A].facts.record_source]; E-A (E-A) record_revision = "R1" [units[E-A].facts.record_revision]; E-A (E-A) record_available = true [units[E-A].facts.record_available]; E-A (E-A) record_authority = "unverified" [units[E-A].facts.record_authority]; E-A (E-A) service = "steamwater electric, noflue" [units[E-A].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual stack temperature/load/hours after appropriate tuning/cleaning, fuel/composition, feedwater/receiving duty, dewpoint/corrosion/material and practical/economic constraints, with matched units/time and source coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: S4 describes reviewing stack operation after tuning to manufacturer specifications, suitable excess air and clean heat-transfer surfaces; design/high stack temperature alone is not a recovery decision. Review fuel, dewpoint/cold-end corrosion and useful receiving duty before considering a remaining opportunity. Its example temperatures, efficiency increments and savings/paybacks are contextual, not universal limits or this site's benefit. Existing suitable operation can be acknowledged without a compulsory thermometer, quote or retrofit.

**How it is decided:** Review actual boiler/flue/feedwater function, existing named recovery coverage, tuned operating/load records and cold-end/receiving/economic constraints with the responsible engineer. No global economizer label, high temperature or fuel label alone establishes absence, adequacy or a reason to obtain equipment quotes. Suitable existing coverage or nonapplicability may be acknowledged; unknown basis remains a records question with no operating or hardware authorization.

**What the source says (S4, S24):** Efficiency "can be increased by 1% for every 40°F reduction in flue gas temperature." An economizer "can often reduce fuel requirements by 5% to 10% and pay for itself in less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description) (IAC/ITAC browse page: 635 recommendations, 2.1 yr average payback, 24.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S4/Tip3 pp1–2 is steam-boiler/feedwater guidance, conditional on tuning/cleanliness, fuel/cold-end and system economics. The inherited general efficiency/payback examples are not universal temperature targets or transferred site savings. Unknown heat-source/service does not establish applicability.

### E14: What do existing records establish about this boiler/steam-generator candidate's flue/feedwater service and current heat-recovery coverage?

**About:** SG-B  

**Finding reference (JSON string):** `"E14@SG-B"`
**Asset IDs (JSON array):** `["SG-B"]`

**Evidence on the drawing / model**

- equipment SG-B reads "SG-B Steam Generator" (`units[SG-B]`)
- Supplied candidate field: `"SG-B fictional_record = true; present; meaning and suitability unverified"` (`"units[SG-B].facts.fictional_record"`)
- Supplied candidate field: `"SG-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[SG-B].facts.record_source"`)
- Supplied candidate field: `"SG-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[SG-B].facts.record_revision"`)
- Supplied candidate field: `"SG-B record_available = true; present; meaning and suitability unverified"` (`"units[SG-B].facts.record_available"`)
- Supplied candidate field: `"SG-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[SG-B].facts.record_authority"`)
- Supplied candidate field: `"SG-B service = \"declaredcombustionsteamwater\"; present; meaning and suitability unverified"` (`"units[SG-B].facts.service"`)
- Supplied candidate field: `"SG-B feedwater_basis = \"unknown\"; blank; meaning and suitability unverified"` (`"units[SG-B].facts.feedwater_basis"`)
- Supplied candidate field: `"SG-B fuel_basis = null; blank; meaning and suitability unverified"` (`"units[SG-B].facts.fuel_basis"`)
- On drawing: Supplied candidate fact, basis unverified: SG-B fictional_record = True (`units[SG-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: SG-B record_source = Fictional development record; no company or human approval (`units[SG-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: SG-B record_revision = R1 (`units[SG-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: SG-B record_available = True (`units[SG-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: SG-B record_authority = unverified (`units[SG-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: SG-B service = declaredcombustionsteamwater (`units[SG-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: SG-B fictional_record = True (`units[SG-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: SG-B record_source = Fictional development record; no company or human approval (`units[SG-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: SG-B record_revision = R1 (`units[SG-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: SG-B record_available = True (`units[SG-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: SG-B record_authority = unverified (`units[SG-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: SG-B service = declaredcombustionsteamwater (`units[SG-B].facts.service`)

**Data to collect**

- Existing named-boiler flue/feedwater service and recovery association [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): SG-B (SG-B) fictional_record = true [units[SG-B].facts.fictional_record]; SG-B (SG-B) record_source = "Fictional development record; no company or human approval" [units[SG-B].facts.record_source]; SG-B (SG-B) record_revision = "R1" [units[SG-B].facts.record_revision]; SG-B (SG-B) record_available = true [units[SG-B].facts.record_available]; SG-B (SG-B) record_authority = "unverified" [units[SG-B].facts.record_authority]; SG-B (SG-B) service = "declaredcombustionsteamwater" [units[SG-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-subject boiler/steam-water, heat-source/flue and feedwater duty, installed recovery/route/coverage and source/revision/availability records; retain foreign or uncertain economizer associations explicitly.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: One economizer label anywhere cannot establish installed coverage, suitability or closure for every boiler. Establish relevant actual service and named coverage; known dry furnace/nonwater helper or electric/no-flue service is not this flue/feedwater task, and unknown service remains conditional. A source-labelled steam generator is reviewed for its actual function without inventing a fuel or drum. Acknowledge suitable existing records or nonapplicability before new observations.
- Existing tuned operating, receiving-feedwater and cold-end feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): SG-B (SG-B) fictional_record = true [units[SG-B].facts.fictional_record]; SG-B (SG-B) record_source = "Fictional development record; no company or human approval" [units[SG-B].facts.record_source]; SG-B (SG-B) record_revision = "R1" [units[SG-B].facts.record_revision]; SG-B (SG-B) record_available = true [units[SG-B].facts.record_available]; SG-B (SG-B) record_authority = "unverified" [units[SG-B].facts.record_authority]; SG-B (SG-B) service = "declaredcombustionsteamwater" [units[SG-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual stack temperature/load/hours after appropriate tuning/cleaning, fuel/composition, feedwater/receiving duty, dewpoint/corrosion/material and practical/economic constraints, with matched units/time and source coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: S4 describes reviewing stack operation after tuning to manufacturer specifications, suitable excess air and clean heat-transfer surfaces; design/high stack temperature alone is not a recovery decision. Review fuel, dewpoint/cold-end corrosion and useful receiving duty before considering a remaining opportunity. Its example temperatures, efficiency increments and savings/paybacks are contextual, not universal limits or this site's benefit. Existing suitable operation can be acknowledged without a compulsory thermometer, quote or retrofit.

**How it is decided:** Review actual boiler/flue/feedwater function, existing named recovery coverage, tuned operating/load records and cold-end/receiving/economic constraints with the responsible engineer. No global economizer label, high temperature or fuel label alone establishes absence, adequacy or a reason to obtain equipment quotes. Suitable existing coverage or nonapplicability may be acknowledged; unknown basis remains a records question with no operating or hardware authorization.

**What the source says (S4, S24):** Efficiency "can be increased by 1% for every 40°F reduction in flue gas temperature." An economizer "can often reduce fuel requirements by 5% to 10% and pay for itself in less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description) (IAC/ITAC browse page: 635 recommendations, 2.1 yr average payback, 24.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S4/Tip3 pp1–2 is steam-boiler/feedwater guidance, conditional on tuning/cleanliness, fuel/cold-end and system economics. The inherited general efficiency/payback examples are not universal temperature targets or transferred site savings. Unknown heat-source/service does not establish applicability.

## Sources cited above

- S4: Steam Tip #3, Use Feedwater Economizers for Waste Heat Recovery. https://www.energy.gov/sites/prod/files/2014/05/f16/steam3_recovery.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
