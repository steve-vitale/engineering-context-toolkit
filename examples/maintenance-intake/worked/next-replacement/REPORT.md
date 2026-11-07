# Maintenance record review

Scope: SIM/P1; units U1, U2; as of 2026-11-06.

1 detected disagreements; 2 total review queue entries. Equipment rows: 2; work-order rows: 3.

Draft comparison of the supplied exports. Absence of a finding does not establish complete coverage, installed state or accepted corrections.

## SIM/P1/U1/P-101 — serial_number (C-cde5629da5)

Review role: Maintenance. Status: open.

- NEXT-101 — WO-EXPORT rev 2 row 4; original work_orders.csv CSV record 4 (ends at physical line 4)
- NEW-101 — EQ-EXPORT rev 2 row 2

## Review boundaries and next steps

- Review queue includes scope ambiguities and other checks: map/queues/review_queue.csv.
- No field inspection, engineering approval, MOC determination, PM validation or company-system write/readback has occurred.
- Open work orders (blank closed_on) supply history only, not evidence of installation. Latest dated closed order per attribute is the comparison basis; owners must confirm its meaning.
- Only mapped fields are interpreted; ignored columns remain in originals. Text is trimmed in prepared CSVs; exact original bytes and CSV-record/physical-line locators remain.
- Proposed actions need a named person, due date and accepted source readback. No action has been assigned or completed by this tool.
- Compared with verified previous packet: 1 new, 0 still detected, 0 no longer detected. See changes.md and findings.json; disappearance is not acceptance.
- equipment: EQ-EXPORT rev 2; owner Maintenance; declared coverage: Selected U1/U2 fictional equipment positions
- equipment attributes absent in some/all rows (not compared where unavailable): manufacturer, size.
- work_orders: WO-EXPORT rev 2; owner Maintenance; declared coverage: Selected U1/U2 fictional replacement history; open orders retained
- Coverage gap: work_orders has no rows for declared units U2. No conclusions there.
- work_orders attributes absent in some/all rows (not compared where unavailable): manufacturer, size.

Open REPORT.html offline; proposed-actions.csv is a draft review form. Retain this whole folder and receipt.json for the next revision.
