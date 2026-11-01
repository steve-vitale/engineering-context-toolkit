# Keep a model correction in the next question screen

A model-review decision can withdraw a supplied meter, drive or recovery candidate while its machine's question
remains open. The next screen must reflect that decision: retain the investigation, remove the rejected record
from eligible evidence and keep the source/history for the company reviewer. Rejection does not establish that
physical equipment is absent.

This example uses the existing [synthetic food model](../food_plant_model.json) and **fictional decisions**.
Every tag is invented. No person reviewed a plant, no equipment was removed and no savings were established.
It is a maintenance control, not an additional public corpus or an extraction-accuracy result.

```sh
python -S examples/opportunity-screen/review-refresh/demonstrate.py
```

The command copies the model into a temporary directory, runs the actual `apply_review.py` and
`question_engine.py` CLIs, and checks the three committed [expected files](expected/expected.json). It makes no
network or model calls and leaves the original model unchanged. `--write` deliberately regenerates those files
after the named behavior checks pass; the default only checks them.

| Fictional decision | Observable change in the next screen |
|---|---|
| Reject power meter JT-201 | JT-201 disappears from C12 candidate evidence. K-201 remains in the question before and after rejection because actual real-input suitability stays open even with a supplied power reading. |
| Reject speed drive SC-203 | E29 retains K-203's function/part-load investigation before and after review; SC-203 disappears as a candidate. A drive label never settled actual function. |
| Reject recovery exchanger HX-303 | E31 and H6 retain the fryer's source/coverage questions before and after review; HX-303 disappears from eligible recovery evidence. Its prior label never settled residual supply, availability or a source/sink match. |

The [generated screen](expected/screen.md) and [question JSON](expected/questions.json) run only C12, E29, E31
and H6. The source model retains its historical quiet-control metadata; current collection questions do not
turn those labels into accepted operating or recovery evidence. The revised check expects the same finding IDs
before and after these candidate rejections, with the corresponding eligible records removed. The actual exercise checks its regenerated
expected files with the current catalog.
Repeating the review changes no model bytes. Explicit reconfirmation restores the candidates and pre-review
screen while retaining the intermediate decisions in history. This is not proof of plant truth or authority.

## Apply the same sequence to your private bundle

Fill the review sheet from the drawing and appropriate authoritative records. Apply the decisions, then regenerate
the screen using the same loop list, schedule files and selected questions used for your prior screen:

```sh
python -S scripts/apply_review.py my-bundle/plant_model.json my-review.csv --reviewer "Name and role" --record-dir my-records
python -S scripts/question_engine.py --model my-bundle/plant_model.json --out my-screen
```

The second command above has no supplemental loops or schedules; add your previous `--loops`, `--schedule` and
`--question` options when applicable. Compare the questions and collection requests before continuing the work.
If you maintain a context register, preserve the previous packet and source manifest. Withdraw finding IDs absent
from the new screen from the current manifest's locator `questions` lists (an empty list withdraws a binding).
Otherwise the manifest is refused for naming an unknown finding. Then refresh against the new model and screen
**with the existing `--register`**: [exact command and absence handling](../../../docs/CONTEXT_REGISTER.md#incoming-revisions-reopen-affected-answers).

Explicit `ops_review.status = rejected` records are excluded from triggers, evidence, required model kinds and
relationships. JSON and Markdown list those rejections with the recorded reviewer, date and notes. A rejected
unit, parent or stream does not recursively reject its children: eligible children lose those references for
this screen, with no replacement inferred. The raw model and history remain intact.

A supplemental loop list cannot reinstate an explicitly rejected controller. A live duplicate with the same tag
remains eligible; the screen does not resolve that identity ambiguity for you. A missing review or `unverified`
status remains eligible. Malformed review metadata refuses before writing output. This local workflow adds no
watcher, automatic reapproval, authenticated reviewer or organizational synchronization.
