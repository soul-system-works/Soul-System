# Result — token-scale + position depth test (§6.1 #4, 2026-06-05)

> **Reproduced 2026-06-05** (full rerun, n=5, read-scored): the headline result held. Full cross-experiment report: [`../../REPRODUCIBILITY.md`](../../REPRODUCIBILITY.md) (witness SOUL-143).

Closes the depth rung the paper brackets: the original depth result (fact fires buried
under ~20 record UNITS, **primacy only**) vs 'lost in the middle' [5] (a large-TOKEN
phenomenon where MIDDLE position degrades most). Vehicle = the F038 recall trap; the needle
is placed at 8% / 50% / 92% depth in a ~6.6k-token record of 200 diverse, independent
engineering findings (none touch `@`-imports). Record INLINED (the `@`-mechanism is the fact
under test). n=5 × {Haiku-4.5, Sonnet-4.6} × 3 positions = 30. Pre-registration in `PREDICTION.md`.

## Outcome (avoid-trap = uses the buried fact: rejects `@`-import / inline / sentinel)

| position (depth) | Haiku | Sonnet | total |
|---|---|---|---|
| early (8%)   | 5/5 | 5/5 | 10/10 |
| middle (50%) | 5/5 | 5/5 | 10/10 |
| late (92%)   | 5/5 | 5/5 | 10/10 |

**30/30 — no decay cliff at any position, either model.** Every cell recalled F038 *by name*
and rejected the `@`-import, citing the silent-fail and the ~43% confabulation rate. The
middle cells (the worst case per [5]) are as clean as primacy/recency: 10/10.

## Finding

At ~6.6k tokens — an order of magnitude above the original ~20-unit probe, with needle
position varied across the full depth range — **'lost in the middle' did not appear** for a
*semantically-unique* needle. The fact fired at primacy, middle, and recency identically.
The most likely mechanism (pre-registered): the needle is the only record on its topic
(non-interactive `@`-import loading), so no filler competes for it; positional degradation
[5] is strongest when distractors are semantically similar to the needle, which is not the
case here. This **bounds the project's no-decay depth claim**: it holds across position up
to ~6.6k tokens for a distinctive fact.

## Prediction scorecard (PREDICTION.md) — CONFIRMED

- Predicted no decay cliff; fact fires at all three positions; at most a mild middle dip →
  confirmed, and even stronger: **no dip at all** (middle 10/10, not the predicted 3–4/5 on
  the weak model).
- Falsifier (middle ≤2/5 while early/late ≥4/5) → did NOT occur.
- Predicted frontier more position-robust than weak → untestable (both ceilinged 10/10).

## Bounds (Skeptic)

- This probe can only FALSIFY (find decay) or BOUND (no decay up to the tested scale). It
  does NOT prove no-decay at arbitrary scale — at much larger token counts, or with a
  needle *camouflaged* among semantically-similar distractors (the regime where [5] bites
  hardest), positional loss could still appear. That residual stays in the paper.
- ~6.6k tokens is still below the 10k–100k regime of the strongest [5] effects. One fact,
  n=5, two models, deterministic single filler corpus (no needle/topic variation).

## Net for the study

The depth claim is **strengthened and bounded**: §4.5's no-decay result, previously
primacy-only at ~20 units, now holds with needle position varied (early/middle/late) at
~6.6k tokens. The paper should narrow its claim precisely — *no positional decay up to the
tested token scale for a distinctive needle* — and keep the arbitrary-scale /
camouflaged-needle case as the standing residual.

Raw arms gitignored. gen.py is deterministic (no RNG). Models: claude-haiku-4-5-20251001,
claude-sonnet-4-6.
