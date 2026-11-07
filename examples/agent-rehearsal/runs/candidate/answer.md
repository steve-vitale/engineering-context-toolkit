The repository can compare your equipment register with completed replacement-job records and prepare a sourced review request.

For **REHEARSAL/P1/NORTH/M-410**, the records disagree:

| Source | Original locator | Serial |
|---|---|---|
| EQ revision R1 | [equipment.csv](C:/Users/Steve/industrial-context-toolkit/examples/agent-rehearsal/inputs/equipment.csv), CSV record 2 | `00041` |
| WO revision R1, J-901 closed 2026-11-02 | [orders.csv](C:/Users/Steve/industrial-context-toolkit/examples/agent-rehearsal/inputs/orders.csv), CSV record 2 | `00042` |

This is a record discrepancy requiring Maintenance review. It does not prove which serial is physically installed today.

J-902's `00999` ([orders.csv](C:/Users/Steve/industrial-context-toolkit/examples/agent-rehearsal/inputs/orders.csv), CSV record 3) was excluded from installation evidence because Closed is blank. SOUTH/M-410 is a separate position, serial `00099` ([equipment.csv](C:/Users/Steve/industrial-context-toolkit/examples/agent-rehearsal/inputs/equipment.csv), CSV record 3). No SOUTH work-order rows were supplied.

I ran the reusable maintenance intake with the supplied approved profile, preserving text serials and exact original file bytes. It produced **one disagreement and two review-queue entries**: the disagreement and a warning that a bare M-410 tag is ambiguous across units. Open the [offline report](C:/Users/Steve/.cp-scratch/ict-rehearsal-candidate-output/packet/REPORT.html), inspect [findings and source origins](C:/Users/Steve/.cp-scratch/ict-rehearsal-candidate-output/packet/findings.json), and use [proposed-actions.csv](C:/Users/Steve/.cp-scratch/ict-rehearsal-candidate-output/packet/proposed-actions.csv) for review. Keep the whole packet and receipt together. The packet's retained `originals/work_orders.csv` is the exact supplied `orders.csv`, renamed by the tool.

For **missing-unit.csv, CSV record 2**, Zone is blank. A separate intake run rejected it with “missing/invalid tag or unknown unit; no identity guessed” (observed shell exit 1), and published no packet. **Maintenance must supply the authoritative Zone/unit or a corrected export with a new revision.** Matching serial `00041` does not authorize assigning NORTH. The original remains unchanged.

Next, Maintenance should name a reviewer and due date, verify J-901's asset association and installed serial against permitted evidence, then propose any needed source correction and retain company-system acceptance/readback. No correction has been accepted or performed. A later comparison should retain this packet and use a fresh output directory with `--previous`; changed source bytes require new source revisions.

Scope is the declared selected records as of 2026-11-06; manufacturer, model and size were unavailable, and Comment was not interpreted. This draft establishes no physical installation, PM adequacy, engineering approval or measured human benefit. No network, account, package installation or source-system write was used. The repository-relative `instructions/prompt-interpretation.md` was missing; the repository AGENTS, task guide and intake contract were read. Actual commands and failures are retained in [result.json](C:/Users/Steve/.cp-scratch/ict-rehearsal-candidate-output/result.json).

