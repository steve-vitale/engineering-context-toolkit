# Opportunity screen: C8-S01-shared-operator-record

Model: `C8-S01-shared-operator-record.json`. Questions: `data/questions.json`.

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
| Emissions | 0 |
| Safety questions to verify | 1 |

## Safety questions to verify

### C8: Are there more alarms per operator area than an operator can handle?

**About:** PAH-101, LAHH-201  

**Finding reference (JSON string):** `"C8@model"`
**Asset IDs (JSON array):** `["PAH-101", "LAHH-201"]`

**Evidence on the drawing / model**

- instrument PAH-101 reads "PAH-101 Fictional alarm candidate, not installed configuration" at U-A (`instruments[PAH-101]`)
- instrument LAHH-201 reads "LAHH-201 Fictional alarm candidate, not installed configuration" at U-B (`instruments[LAHH-201]`)

**Data to collect**

- Alarm rate, floods and standing alarms [not on drawing]. Where: site records: alarm journal export. How: Count alarms per 10 minutes in normal operation and after upsets.

**How it is decided:** Rationalize when the long-term rate or the upset flood exceeds the HSE guidance.

**What the source says (S23):** HSE: "the long-term average alarm rate during normal operation should be no more than one every ten minutes; and no more than ten displayed in the first ten minutes following a major plant upset."

**Limits:** ISA-18.2 / IEC 62682 are not openly accessible; HSE CHIS6 is the citable open alternative.

## Not checked

- C2: the model holds no controllers; give a loop list with --loops (controller,measurement,output) to check this
- C6: the model holds no controllers; give a loop list with --loops to check this

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, H1, H2, H3, H4, C1, C3, C4, C5, C7, C10, C9, E25, E26, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S23: UK HSE, Better Alarm Handling, Chemicals Information Sheet No. 6 (CHIS6, 3/00). https://www.hse.gov.uk/PuBns/chis6.pdf (license: Crown copyright; HSE content is generally under the Open Government Licence, but verify)
