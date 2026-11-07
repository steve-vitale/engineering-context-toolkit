# Maintenance record review

Scope: REHEARSAL/P1; units NORTH, SOUTH; as of 2026-11-06.

1 detected disagreements; 2 total review queue entries. Equipment rows: 2; work-order rows: 2.

Draft comparison of the supplied exports. Absence of a finding does not establish complete coverage, installed state or accepted corrections.

## REHEARSAL/P1/NORTH/M-410 — serial_number (C-9ea4537117)

Review role: Maintenance. Status: open.

- 00042 — WO rev R1 row 2; original work_orders.csv CSV record 2 (ends at physical line 2)
- 00041 — EQ rev R1 row 2

## Review boundaries and next steps

- Review queue includes scope ambiguities and other checks: map/queues/review_queue.csv.
- No field inspection, engineering approval, MOC determination, PM validation or company-system write/readback has occurred.
- Open work orders (blank closed_on) supply history only, not evidence of installation. Latest dated closed order per attribute is the comparison basis; owners must confirm its meaning.
- Only mapped fields are interpreted; ignored columns remain in originals. Text is trimmed in prepared CSVs; exact original bytes and CSV-record/physical-line locators remain.
- Proposed actions need a named person, due date and accepted source readback. No action has been assigned or completed by this tool.
- equipment: EQ rev R1; owner Maintenance; declared coverage: Selected two positions
- equipment attributes absent in some/all rows (not compared where unavailable): manufacturer, model, size.
- work_orders: WO rev R1; owner Maintenance; declared coverage: Selected replacement history
- Coverage gap: work_orders has no rows for declared units SOUTH. No conclusions there.
- work_orders attributes absent in some/all rows (not compared where unavailable): manufacturer, model, size.

Open REPORT.html offline; proposed-actions.csv is a draft review form. Retain this whole folder and receipt.json for the next revision.
