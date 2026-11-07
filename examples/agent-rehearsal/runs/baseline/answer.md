# Maintenance export comparison

The repository turned your exports into a sourced disagreement and an owner review packet.

For **REHEARSAL/P1/NORTH/M-410**, equipment source **EQ R1** records serial **00041**, while closed work order **J-901**, source **WO R1**, records fitted serial **00042** and closure **2026-11-02**. These supplied records need reconciliation; they do not establish what is physically installed today.

| Evidence | Original locator | Value |
|---|---|---|
| Equipment record | equipment.csv, CSV data record 1, line 2; Serial | 00041 |
| Closed job J-901 | orders.csv, CSV data record 1, line 2; Fitted | 00042 |

Scope: profile.json declares REHEARSAL/P1, NORTH and SOUTH, as of 2026-11-06; equipment coverage is “Selected two positions” and work-order coverage is “Selected replacement history.” Both sources are R1. Serial values were preserved as text, including leading zeroes. Comment was ignored.

SOUTH/M-410 is a separate position: equipment.csv data record 2 (line 3) records 00099. No supplied closed SOUTH job was compared. J-902 (orders.csv data record 2, line 3) has Fitted 00999 but blank Closed, so it is not evidence of a completed installation and was excluded from closeout comparison.

**Missing identity:** missing-unit.csv data record 1 (line 2) has blank Zone. I withheld it from the comparison. Maintenance must confirm its authored unit or provide an explicit identity crosswalk/revised export before it can be qualified and compared. Neither the shared M-410 tag nor matching serial 00041 establishes NORTH identity. The original remains unchanged.

**Next action — Maintenance:** verify J-901’s asset association and closeout evidence against the equipment record and field evidence as needed; record the authoritative decision and propose a correction in the company system. A named reviewer remains to be assigned. Retain both R1 sources and obtain a returned revision plus company receipt/readback to establish acceptance. The missing-unit request is separate.

The review packet is in **packet/**: open **packet/conflicts.md** for both retained values and **packet/queues/review_queue.csv** for ownership. Conflict C-9ea4537117 is open and routed to Maintenance. The queue also warns that bare M-410 is ambiguous across NORTH and SOUTH. **source-map.json** maps derived rows to original files and contains original hashes; **originals/** holds byte copies.

I prepared comma-delimited working copies using profile.json, built the one-map packet, validated its graph (0 problems), and ran a sourced disagreements query. Build, check and query all exited 0. No drawing was supplied; the empty drawing register does not imply no plant drawing exists. The optional prompt-interpretation file was absent in this baseline checkout; that read failed and was logged.

This is a draft comparison of these fictional exports, not an accepted correction, engineering verification, site accuracy guarantee, live integration, or measured human benefit. No installation status or physical truth was inferred, and no original or company record was changed.
