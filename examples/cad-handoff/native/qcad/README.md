# Native attribute edit and a failed preservation check

QCAD Professional 3.33.1 public Windows trial, Qt5 portable package. No account or paid license used for this
bounded experiment. Binaries are not redistributed. This is a native engine/API experiment on one fictional
fixture, not an interactive editor acceptance test or a qualified general CAD adapter.

The [native script](attribute-edit.js) imports the original DXF, finds its unique ICT_ID under a parent insert,
checks the three planned before values, edits MODEL/SERIAL/SIZE, exports a separate file, destroys the document
and imports that returned DXF into a fresh native document. Its [readback](readback.json) retains the stable ID,
TAG, new values and unfamiliar VENDOR_NOTE. A separate ezdxf-based comparator then examines the actual return.

**The declared preservation gate fails:** [comparison.json](comparison.json) reports 335 differences outside the
three permitted edits: one DXF-version difference (AC1015 to AC1024), one whole-header difference, 333 entity
records. These are strict decoded-record differences, including rewrites/handles; they are not 335 demonstrated
engineering losses. Do not discard or waive them because the six attribute values survived. Native GUI edit,
interactive usability, geometry/display acceptance, classified preservation differences and company acceptance
remain open. No context revision from this failed exchange was promoted.

[returned.dxf](returned.dxf), [native log](native-edit.log), exact package URLs/hashes and [receipt](receipt.json)
retain the result. The first Qt6 package exited zero with no script handler; its failed help output is retained.
Dependency inspection found an absent Qt6Positioning.dll candidate; this is a diagnosis, not a proven repair.
The Qt5 official package loaded scripting. The first helper mistakenly filtered EntityBlockRefAttr (insert with
attributes) rather than EntityAttribute; it reported Identity not unique and wrote no return. Its failure is retained,
then the corrected helper actually ran. Both errors can exit zero, so replay requires the readback marker and strict
comparison. Native logs use the local trial clock; repository journal dates use the host date.

Optional replay with a separately obtained compatible edition (ezdxf required):

```sh
python examples/cad-handoff/native/qcad/reproduce.py --qcad /path/to/qcadcmd.com --out out/qcad-native
```

It deliberately returns exit 1 when preservation differences remain, retains logs, and never overwrites a destination.
The initial saved run invoked the script directly. The wrapper was then actually rerun: native readback completed and it returned exit 1 with the same 335 strict differences, as intended.
CI verifies retained bytes, values and strict failure, without downloading or invoking commercial trial software.

Primary references: [headless scripting](https://qcad.org/en/tutorials/development/command_line_tool_scripts/),
[attribute API](https://qcad.org/api/classes/RAttributeEntity/), [entity-type definitions](https://qcad.org/api/classes/RS/),
[edition features](https://qcad.org/en/features/) and [isolated portable settings](https://qcad.org/en/tutorials/installation/qcad_portable/).
Block-attribute editing is a Professional feature; this does not establish Community Edition support or a free
production workflow. The public trial and isolated config were sufficient for this short experiment only.
