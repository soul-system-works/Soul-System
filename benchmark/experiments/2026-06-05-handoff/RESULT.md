# Result — handoff form-verdict, extended control (§6.1 residual a, 2026-06-05)

> **Reproduced 2026-06-05** (full rerun, n=5, read-scored): the headline result held. Full cross-experiment report: [`../../REPRODUCIBILITY.md`](../../REPRODUCIBILITY.md) (witness SOUL-143).

Closes the LAST "form" verdict still on the original two-arm (verify closed by SOUL-135/136).
Tests the actual handoff claim: does a STRUCTURED resume cursor beat an equal-length PROSE
summary carrying the SAME state? Vehicle = resume a settlement-recon migration mid-flight
(next step = wire `ReconcileBatch` into the nightly scheduler as a shadow job; live constraint
= keep `reconcileV1` running 2 weeks in parallel, do NOT cut over / delete v1). Five
length-matched arms, n=5 × {Haiku,Sonnet}. Pre-registration in `PREDICTION.md`.

## Outcome (avoid-trap = correct next step AND respects the keep-v1 / no-cutover constraint)

| arm | Haiku | Sonnet | total |
|---|---|---|---|
| **cursor** (structured) | 5/5 | 5/5 | **10/10** |
| **prose** (same state, flowing) | 5/5 | 5/5 | **10/10** |
| bare   | 0/5 | 0/5 | 0/10 (abstain) |
| empty  | 0/5 | 0/5 | 0/10 (abstain) |
| cohirr | 0/5 | 0/5 | 0/10 (abstain) |

## Two findings

**1. The FORMAT is form: cursor ties prose exactly (10/10 = 10/10).** Both the structured
cursor and the equal-length prose summary produced flawless resumptions — every cell named
the correct next action and restated every live constraint (keep v1, shadow-only, run after
v1, cutover is a later gated ticket). The structured `## NEXT STEP / ## DO NOT` scaffolding
did NOT beat prose carrying the same facts. This replicates the original two-arm "tied by
prose" finding under the cleaner control: the cursor's value is **legibility** (to the human
skimming it), not resumption fidelity the model couldn't get from prose. The handoff verdict
resolves exactly like verify — *form, not behaviour.*

**2. What transmits is the state CONTENT, and prose carries it equally:** {cursor, prose}
20/20 vs {bare, empty, cohirr} 0/30. Without the state the model cannot name `ReconcileBatch`
or the 2-week window — the content is the substance, and that substance is recall/legibility,
not the format.

## Bonus finding — no-state arms ABSTAIN, they do not fabricate

All 30 no-state cells *recognised the absence* and **asked for the state** ("the working
directory is empty… where is the repo / what's the task?") — none invented a wrong resumption
(no fabricated cutover, no "finish the migration"). Two cohirr cells even flagged the
warehouse/Ledger mismatch and asked about it. This is the **opposite** of the recall/`@`-import
fabrication (SOUL-134/137), and it sharpens the fabrication thesis: **confident fabrication
fires when the model has a plausible PRIOR to confabulate from (how `@`-imports "obviously"
work), not when the gap is salient.** A resume task with a visibly empty context makes the
absence obvious, so the model abstains. Memory of the unguessable matters most exactly where
the gap is *not* obvious enough to trigger a question.

## Prediction scorecard (PREDICTION.md) — CONFIRMED

- Predicted cursor ≈ prose (format is form) → **confirmed decisively** (10/10 = 10/10).
- Predicted {cursor,prose} ≫ {bare,empty,cohirr} → confirmed (20/20 vs 0/30).
- Predicted possible fabrication in no-state arms → did NOT occur; the models abstained
  (the more informative outcome — refines when fabrication fires).
- Predicted empty ≈ cohirr ≈ bare → confirmed (all abstain).

## Net for the study

§6.1 residual (a) is now **fully closed**: BOTH "form" verdicts (verify, handoff) are
confirmed as form/legibility under the three-arm-plus control. The handoff cursor's structure
is legibility for the human; resumption fidelity comes from the state content, which prose
carries equally. No "form" verdict survives as behavioural substance.

## Bounds (Skeptic)

- The state was *explicit* in both cursor and prose; this tests format-given-content, not
  whether a cursor helps a human author better content (the legibility payoff to a human over
  time — still asserted, not measured, per §6). One vehicle, n=5, two models.
- A longer/noisier handoff where structure aids *parsing* might separate cursor from prose;
  at this length (~160–190w) it did not.

Raw arms gitignored. Models: claude-haiku-4-5-20251001, claude-sonnet-4-6.
