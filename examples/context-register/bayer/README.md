# A generated question retains its earlier answers for review

This example connects the question engine to retained engineering context. It uses the existing sourced Bayer
model and public CSB report as development evidence, with no human owner, reviewer, sign-off or plant-truth verdict.

E18 investigates whether rejected cooling heat could serve another heating duty. Its screen has six exact
asset/stream references and three collection requests. The published operating narrative provides useful sequence
context; it does not establish simultaneous duties or an available opportunity.

Read the [current screen](screen/screen.md) and [retained report](expected/context.md). Both earlier proposed
decisions remain in history. The latest answer's recorded state is **partial**, while current E18 is **unanswered**:
its evidence fingerprint no longer matches the clarified decision-rule wording in the current question content.
The model and source report are unchanged. This wording revision does not prove the earlier engineering
interpretation wrong; it requires review of whether that answer still addresses the current screening basis.

From the repository root:

```sh
python scripts/question_engine.py --model data/bayer_rt/process_model.json --question E18 --out my-bayer-question/screen
```

If the original report is not cached, this existing explicit fetch downloads it from csb.gov and checks its pinned
SHA-256; it does not digitize or publish a figure:

```sh
python scripts/digitize_bayer_fig11.py fetch
```

Refresh the full retained register without supplying a new answer:

```sh
python -S scripts/context_register.py apply --model data/bayer_rt/process_model.json --questions my-bayer-question/screen/questions.json --sources examples/context-register/bayer/sources.json --source-root data/external --register examples/context-register/bayer/expected/context.json --out my-bayer-question/current
```

This refresh is idempotent against the current supplied register. It adds no decision or ownership record: both
proposals stay intact, ownership remains `needs_owner`, plant truth stays unknown, and the latest response remains
stale for `question content`. The source key cites PDF page 37 (printed page 29), the temperature-control narrative.
Its historical sequence and the model's caveats are not revalidated by this software refresh.

The [supplied proposed CSV](proposed_answer.csv) keeps its earlier fingerprint and is historical input. Applying it
against the current basis refuses; do not replace its fingerprint or copy it into a new approval. The
[prior register](history/before-appearances.context.json) and [older sheet](history/before-appearances.answers.csv)
also remain unchanged.

When an owner is ready to review the current question and evidence basis, prepare a **new** sheet from the
retained current register:

```sh
python -S scripts/context_register.py prepare --model data/bayer_rt/process_model.json --questions my-bayer-question/screen/questions.json --sources examples/context-register/bayer/sources.json --source-root data/external --register my-bayer-question/current/context.json --out my-bayer-question/review
```

Review the operating sequence, existing duty/timing records and remaining requests before authoring a new answer.
That review determines applicability; the tool does not convert a wording edit into an engineering verdict or
complete each collection prompt. Keep earlier decisions and independently sourced responses rather than
overwriting them. No saving or engineering change is established here.

Use the [first-pilot brief](../../first-pilot/README.md) for one decision worth investigating. The
[maintenance guide](../../../docs/CONTEXT_REGISTER.md) covers ownership, revisions and portable handoff.
