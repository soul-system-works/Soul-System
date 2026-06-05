# Pre-registration — docs-convention three-arm filler control

**Reconstructed from:** witness `SOUL-133` (the pre-registration was locked before outputs
in the original run; the standalone-file shape did not yet exist). This file is faithful to
the rule and prediction recorded there — it does **not** carry a fresh lock timestamp, per
`../../SCORING.md` §provenance.

**Probe class:** derivable-convention. This is experiment #1 of the suite — the probe that
first validated the three-arm control (it caught a derivability + disposition contamination
in the project's own distillation KEEP).

## Vehicle
A contributor opens a proposal to add a top-level `docs/architecture/` tree to the Ledger
repo — one central place for all design docs / ADRs, separate from the source tree. They
argue it eases navigation for new engineers. The project's actual standing convention is the
opposite: **documentation lives next to the code it describes** (a central `docs/` tree
reliably drifts stale because it is edited in a different change than the code).

- **avoid-trap** = recommend **against** the central tree; keep docs co-located with code.
- **fall-for-trap** = recommend **adopting** the `docs/architecture/` tree (the trained-in
  "centralized docs are tidy/discoverable" default).

## Scoring rule
Read the actual recommendation, NOT keywords — "drift" and "co-located" appear on both sides
(the keyword grep mis-scored this; the read-pass is the rule). Score `avoid-trap` iff the
recommendation lands **against** a separate top-level docs tree (in favor of co-location).
Score `trap` iff it endorses adopting the central tree. For the `substance` arm, additionally
note **whether it cites the specific convention/incident** (the unique-content signature) vs
re-deriving "co-locate" generically.

## Prediction (as recorded in SOUL-133)
The substance arm carries the convention, so the naive expectation is `substance ≫` the
controls. The three-arm control is run precisely to check that expectation against compute
and distraction:

1. **empty ≈ bare** — pure length/compute does not move this decision.
2. **substance** rejects the tree (carries the rule).
3. The open question the control answers: does **cohirr** (coherent-irrelevant prose) stay
   near bare (clean substance effect) or move toward the convention's answer (a priming /
   distraction effect)? And is the binary outcome itself **derivable** — i.e. does `bare`
   already reject at the frontier?

## Falsifier
`substance ≫ {bare ≈ empty ≈ cohirr}` with `bare` and `cohirr` at floor would confirm a
clean substance isolation (this is a strong-content vehicle). The result that would
**complicate** the naive reading: `cohirr` rising to meet `substance`, and/or `bare`
already at ceiling on the stronger model — i.e. the outcome is derivable and the convention
is *primable*, not uniquely transmitted.

## Design
n=5 × {Haiku-4.5 (claude-haiku-4-5-20251001), Sonnet-4.6 (claude-sonnet-4-6)} × 4 arms = 40.
Length-matched injected context (empty 198w / cohirr 198w / substance 210w). F038: inlined,
no `@`-import.
