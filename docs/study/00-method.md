# Method — self-ablation under equal compute

## The design

Each measurement is an **isolated, non-interactive model call** (`claude -p "<task>"
< /dev/null`, fresh process, no chat history). The thing under test (doctrine,
a role lens, a gate checklist, a handoff cursor, a record) is supplied via the
system prompt or pasted into the task; the *bare* arm gets the task alone. Arms are
compared on a pre-registered, mechanically-checkable outcome.

The unit of comparison is an **arm**: `(task, condition, model, run-index)`. We run
n≥5 per cell unless noted. Models span a capability range — Haiku 4.5 (weak),
Sonnet 4.6 (mid), Opus 4.8 (frontier) — because the effect size of any aid depends
on whether the bare baseline already succeeds.

## The three controls

**C1 — Equal-compute control (the decisive one).** The field's most common ablation
confound is that "loading the system" also loads tokens, and more context alone can
make a model more thorough. So every apparent win is re-run against a **length-matched,
semantically-empty filler** of the same token budget (e.g. ~26 KB of unrelated
warehouse-logistics prose in place of the ~26 KB doctrine; a generic "double-check
your work" in place of the specific gate checklist; a plain summary in place of the
structured cursor). **A "substance" verdict that vanishes under equal compute is not
substance.** This control caught four false positives in this study (see below).

**C2 — Difficulty validation.** A task only measures an aid if the bare baseline
*plausibly fails it*. Before scoring, run the bare arm n≥5: if it already succeeds,
the task is measuring ceiling, not the aid. Discard or sharpen. (Corollary learned
the hard way: a high-salience domain — e.g. patient safety — can trigger a caution
reflex that *substitutes* for the discipline under test, making the bare baseline
pass for the wrong reason. Keep the domain low-salience; one medical task was thrown
out for exactly this.)

**C3 — Trap taxonomy.** When a task plants a defect, the defect is of a *named kind*
so a "catch" maps to a specific discipline: a false premise (anchoring), a dropped
requirement (completeness), a buried downstream consequence (trajectory), a
silently-truncated long-horizon constraint (gate). One trap per task, labelled with
the discipline that *should* catch it.

## Scoring discipline

- **Pre-register** the rubric and the answer key before seeing outputs.
- **Score mechanically** where possible (count the behaviour; grep within-cell
  comparable patterns), then **read-confirm** the borderline arms. Never eyeball a
  count.
- Watch for **wrong-reason** passes (an artifact refused for missing-info, a
  placeholder name flagged, a disaster-salience reflex) — these confound the signal
  and must be designed out or scored separately.

## What "value" means — and that not everything is measurable this way

Three honest buckets:

- **Measured** — single-shot or fresh-session outcomes A/B-testable with a C1
  control (doctrine ablation, handoff/resume, verify-gate, recall, distill).
- **Reasoned** — instruments whose value is friction-reduction or human-workflow
  convenience (capture commands, read-only utilities); assessed by transparent
  cost-vs-plausible-value argument, *not* a faked experiment.
- **Inspected** — one-time or structural artifacts (init, the doctrine files
  themselves); judged by inspection.

Faking a single-shot experiment for a longitudinal or workflow instrument would be
the precise failure (a coherent-but-false result) the study exists to catch. The
audit states, per instrument, which bucket it is in.

## Known bounds of the method

- Single-shot / single-resume. The system's strongest claim is **longitudinal**
  (accumulated record across many sessions); the harness reaches it only indirectly
  (the recall/traceability probe). This is named, not hidden.
- n is small (5–7/cell); keyword scoring is within-cell comparable, not absolute.
- The scorer is also the experimenter; rubrics are pre-registered to constrain this,
  and the bias, when present, runs *toward* the system (so nulls are conservative).

## Harness specifics (reproducibility)

Arms run from a scratch working directory. Doctrine/condition files are supplied via
`--append-system-prompt-file` or pasted inline. **@-imports are not used under
`-p`** — they fail silently and the model confabulates the missing content ~43% of
the time (finding SOUL-F038); content is inlined and a sentinel load-test confirms
it reached the model before any run is trusted. Raw arm outputs are retained under
`.soul/experiments/<date>-<probe>/`.
