# Three revisions of a maintenance review

This fictional example runs the [reusable intake tool](../../docs/MAINTENANCE_INTAKE.md) on ordinary equipment
and work-order exports. Its fixtures and expected conditions are exposed development controls. It is not a
manager trial or accepted company correction.

```sh
python -S examples/maintenance-intake/reproduce.py --out out/maintenance-intake-demo
```

Open `out/maintenance-intake-demo/initial/REPORT.html`. The U1 equipment serial OLD-101 disagrees with the
closed order's NEW-101. U2/P-101 remains separate and an open order's FUTURE-101 is not installation evidence.
The corrected packet no longer detects that disagreement; it retains the old finding without declaring it
accepted. The next-replacement packet finds NEW-101 versus NEXT-101 at the same functional position.

Read the committed [first report](worked/initial/REPORT.md), [corrected report](worked/corrected/REPORT.md),
[next replacement](worked/next-replacement/REPORT.md) and [actual replay receipt](worked/replay.json).

The original files and profile are in [inputs](inputs/profile.json); the simulated returned exports are created
inside the replay output. The tool's regression suite also exercises semicolon exports, explicit date formats,
leading zeros, multiline rows, changed headers, missing inputs, duplicate identities, tampered previous packets
and output collisions. No source-system write, field verification or human effort measurement occurs.

For your own records, use `scripts/maintenance_intake.py` with your paths and an explicitly reviewed profile;
the reproduction script above remains fixed to this fictional case. Keep private files out of this public repo.
