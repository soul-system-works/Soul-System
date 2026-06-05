# Result — docs-convention three-arm filler control (2026-06-04)

**Source of record:** witness `SOUL-133`; bears on study `docs/study/02` (distill KEEP),
`03` (lean-down), `paper.md` §4.2/§6. Pre-registration in `PREDICTION.md`.

This is experiment #1 — the probe that validated the three-arm control by **catching a
contamination in the project's own claim**. The naive prior was "the convention arm wins";
the control showed the win was partly derivable and partly a priming effect.

## Binary outcome (avoid-trap = reject the central docs tree, keep co-location)

Haiku is the discriminating model — Sonnet's `bare` already rejects the tree (the convention
is **derivable at the frontier**, a C2 ceiling), so the arm separation only shows on Haiku:

| arm | Haiku (reject-tree) |
|---|---|
| bare      | 2/5 |
| empty     | 2/5 |
| cohirr    | **5/5** |
| substance | **5/5** |

(Sonnet `bare` ≈ ceiling — rejects without any injected context.)

## Three read-confirmed findings

1. **empty ≈ bare (2/5).** Pure compute/length did not move the decision. The inflation
   confound the equal-compute control guards against did not even fire here — length alone
   neither helped nor hurt.

2. **Coherent-irrelevant filler is NOT neutral.** The warehouse-ops prose pushed Haiku to
   5/5 reject (vs bare/empty 2/5). Its disciplined "drift / variance / quarantine" register
   primed a **cautious disposition** that re-derived "co-locate docs" — with no docs content
   in it at all. This is the SOUL-132 literature warning (irrelevant tokens aren't neutral)
   confirmed on our own model, and is exactly why the original two-arm probes (which used a
   coherent-irrelevant filler as the control) needed this third arm.

3. **The outcome is derivable → docs is a WEAK substance vehicle.** Both Sonnet (ceiling)
   and disposition-primed Haiku reach "reject" *without* the convention. The convention's
   unique contribution shows only in the **reasoning**: the `substance` arm cites the
   specific rule/incident; the `cohirr` arm cites nothing yet reaches the same answer. So the
   binary does not isolate substance on this vehicle.

## Prediction scorecard (PREDICTION.md)

The falsifier-side outcome occurred — the naive "substance ≫ all" reading was **complicated**,
as the three-arm control was designed to detect:

- empty ≈ bare → **confirmed**.
- substance rejects → confirmed, but **not uniquely**: cohirr also reaches 5/5, and Sonnet
  bare ceilings. The binary is derivable.
- cohirr's role → **resolved against the clean-isolation reading**: cohirr *primes* the
  answer (5/5), it does not stay at bare. Distraction has a sign here, and it is positive.

## Verdict for the study (the honest moderation)

The distill / docs-near-code "Mind 10/10 vs generic 0/10" headline (corpus 02) **overstated
the substance**: the original generic-principles counter-arm was a *loaded* distractor
(pro-central-docs) that pulled toward the default; a neutral/cautious distractor reaches the
project answer generically. The docs-near-code convention's answer is *generically
defensible*, hence derivable + primable. The right vehicle for a clean substance isolation is
a **counter-default FACT** (where generic reasoning is confidently wrong), not a defensible
**convention** — which is exactly the paired recall/F038 probe (`2026-06-04-recall`, 10/10 vs
0). This experiment's value is the contamination it caught in our own KEEP.

## Bounds (Skeptic)

- One task, n=5, two models, **one** coherent-irrelevant register (the warehouse "disciplined"
  tone may be a stronger caution-primer than a neutral one — the cohirr sign could differ
  with a flatter register).
- The binary hides the real split; the finding lives in the read-confirmed *reasoning*, not
  the count.
- Sonnet's ceiling makes the empty/cohirr/bare separation unmeasurable at the frontier — the
  discrimination only exists because Haiku had headroom.

**Raw arms gitignored** (`arms/` is regenerable via `run.sh`). Models:
claude-haiku-4-5-20251001, claude-sonnet-4-6.
