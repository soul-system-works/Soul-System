# Pre-registration — token-scale + position depth test (§6.1 #4)

**Locked:** 2026-06-05, before any output read. Closes the depth rung the paper brackets:
the original depth result (fact fires 5/5 buried under ~20 record UNITS, **primacy only**)
is in a different regime than 'lost in the middle' [5], which is a large-TOKEN phenomenon
and shows MIDDLE position degrades most. This probe matches token scale (~6.6k tokens) and
varies needle POSITION.

## Vehicle
The F038 recall trap (SOUL-134): an engineering record carries the fact that `@`-imports
fail silently under `claude -p`; the task tempts endorsing an `@`-import for DRY shared
doctrine. The record is a ~6.6k-token corpus of 200 diverse, mutually-independent
engineering findings (none touch `@`-imports). The F038 needle is inserted at:
- **early** = 8% depth (record 16/201)
- **middle** = 50% depth (record 100/201)
- **late** = 92% depth (record 184/201)

The record is INLINED into `-p` (never `@`-imported — that mechanism is the fact under test).

- **avoid-trap** = the recommendation USES the buried fact: rejects `@`-import under `-p` /
  inlines / `--append-system-prompt-file` / sentinel load-test.
- **fall-for-trap** = endorses the `@`-import as reliable (the fact was not recalled/used).

Score by reading the recommendation, NOT keywords (SOUL-134 lesson: path-relativity and
fallback language are not the same as recalling the F038 silent-fail).

## Prediction (locked)
1. **If [5] generalizes to record-units at this token scale:** middle degrades —
   avoid-trap(middle) < avoid-trap(early) ≈ avoid-trap(late). A U-shape (primacy + recency
   preserved, middle lost).
2. **My actual expectation (locked):** at ~6.6k tokens — an order of magnitude below where
   [5]'s middle-loss becomes severe — I expect the fact still fires at ALL THREE positions
   on both models (no decay cliff), consistent with the project's prior primacy-only result
   and because the needle is *semantically unique* (no filler competes on its topic), which
   blunts positional loss. I predict avoid-trap ≈ ceiling (≈5/5) at early and late, and
   **at most a mild dip at middle** (e.g. 5/5 → 3–4/5 on the weak model), NOT a collapse.
3. **Falsifier of the project's no-decay claim:** if middle drops to ≤2/5 while early/late
   hold at ≥4/5 on either model, 'lost in the middle' DOES bite at this scale and the
   paper's depth claim must be narrowed to primacy placement.
4. **Capability:** the frontier (Sonnet) should be MORE position-robust than Haiku; if any
   middle-loss appears it should be larger on Haiku.

This probe can only FALSIFY (find decay) or BOUND (no decay up to ~6.6k tokens). It cannot
prove no-decay at arbitrary scale — a residual the paper keeps.

## Design
n=5 × {Haiku-4.5, Sonnet-4.6} × 3 positions = 30 runs. Corpus deterministic (gen.py, no RNG).
Needle identical across positions; only placement varies. F038: record inlined.
