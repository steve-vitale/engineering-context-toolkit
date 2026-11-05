# Conflicts, routed to the owner of the record

Each conflict keeps what both sources say. None is resolved by software; a person records a decision (`--decisions`).

## Doc control

| Id | Type | Status | About | Source A says | Source B says |
|---|---|---|---|---|---|
| C-2782ddd066 | asset_presence | open | S1/P1/200/LT-2204 drawn | listed in INSTRUMENT-INDEX (INSTRUMENT-INDEX, row 4) | not on any registered sheet of S1/P1/200 (drawing register) |
| C-730af068af | asset_presence | open | S1/P1/200/LV-2204 drawn | listed in CMMS-EQUIPMENT (CMMS-EQUIPMENT, row 8) | not on any registered sheet of S1/P1/200 (drawing register) |
| C-7bc05b6a56 | asset_presence | open | S1/P1/200/P-103 drawn | listed in CMMS-EQUIPMENT (CMMS-EQUIPMENT, row 3) | not on any registered sheet of S1/P1/200 (drawing register) |
| C-b0fa510a9a | asset_presence | open | S1/P1/200/LIC-2204 drawn | listed in INSTRUMENT-INDEX (INSTRUMENT-INDEX, row 5) | not on any registered sheet of S1/P1/200 (drawing register) |

## I&C

| Id | Type | Status | About | Source A says | Source B says |
|---|---|---|---|---|---|
| C-66ae68aef5 | loop_pairing | open | S1/P1/200/PIC-2210 output | PV-2210 (S1/DOC/PID-P1-200-01, sheet 200-01 zone E3) | PV-2211 (DCS-LOOPS-200, lists/dcs_loops_unit200.csv line 4) |
| C-b2244b1b07 | unlisted_loop | open | S1/P1/200/TIC-2205 loop | TIC-2205 with TT-2205, TV-2205 (loop_number + signal_line) (S1/DOC/PID-P1-200-02, sheet 200-02 zone D1) | not listed (DCS-LOOPS-200) |

## Maintenance

| Id | Type | Status | About | Source A says | Source B says |
|---|---|---|---|---|---|
| C-ce7c3162b0 | asset_presence | open | S1/P1/200/P-102 listed | drawn on 200-02 rev B (S1/DOC/PID-P1-200-02, sheet 200-02 zone E2) | no row for this tag in this unit (CMMS-EQUIPMENT) |
| C-eee8a6a0d3 | asset_presence | open | S1/P1/200/PV-2210 listed | drawn on 200-01 rev D (S1/DOC/PID-P1-200-01, sheet 200-01 zone E3) | no row for this tag in this unit (CMMS-EQUIPMENT) |
| C-2b9e55fceb | mention_not_in_register | open | S1/P1/200/P-102 listed | OP-200-07 mentions P-102 (S1/DOC/OP-200-07, line 5, column 10) | no row for this tag (maintenance_export) |
| C-72b8f2dcce | value_disagreement | open | S1/P1/200/P-101 rated_flow | 45 m3/h (EQUIPMENT-DATASHEETS, row 2) | 40 m3/h (CMMS-EQUIPMENT, row 2) |

## Process

| Id | Type | Status | About | Source A says | Source B says |
|---|---|---|---|---|---|
| C-b6f2b34e21 | superseded_basis | open | S1/DOC/DB-P101 based_on PID-P1-200-01 | rev C (S1/DOC/DB-P101) | current rev D (S1/DOC/PID-P1-200-01) |

## Site utilities

| Id | Type | Status | About | Source A says | Source B says |
|---|---|---|---|---|---|
| C-faf476ece2 | ambiguous_reference | open | S1/DOC/CW-N-01 mention P-101 | P-101 (S1/DOC/CW-N-01, line 5, column 27) | exists as S1/P1/200/P-101, S1/P2/300/P-101 (one map) |
| C-328949de42 | boundary | open | S1/P2/300/@300-01/OPC-CWS size | 6 in (S1/DOC/PID-P2-300-01, sheet 300-01) | 8 in (S1/DOC/PID-UTIL-CW-01, sheet CW-01) |
| C-8577ab1f7b | boundary | open | S1/UTIL/CW owner_scope | S1/P2/300 (S1/DOC/PID-P2-300-01, sheet 300-01) | S1/UTIL (site.json) |
