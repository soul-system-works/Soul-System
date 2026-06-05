# Result — longitudinal carry of a counter-default reasoning-PREFERENCE (2026-06-04)

**Source of record:** witness `SOUL-124` (the sibling of SOUL-123). Pre-registration in
`PREDICTION.md`. This probe tests whether a self-accumulated record carries a counter-default
reasoning-**preference** across a session + task boundary, and whether that preference
survives at the frontier.

## Binary outcome (HOLD = signal expected failures by returning a `Result` type, per D)

D scored **6/6 counter-default in the floor-check at both models** — with no record, both
default to `raise`. The carried record reverses that:

| arm | Haiku (HOLD) | Sonnet (HOLD) |
|---|---|---|
| withrecord | **5/5** | **5/5** |
| control    | 0/5 | 0/5 |
| floor      | 0/5 | 0/5 |

(control = length-matched filler with NO error-style ADR; floor = no record. Both DRIFT to
`raise` at both models.)

## Read-confirmed findings

1. **withrecord 5/5 HOLD at BOTH Haiku and Sonnet.** The arm cites ADR-001 and reproduces
   its reasoning — and its **boundary**: Sonnet keeps `amount > 0` as an `assert` because it
   is "a programmer mistake, not a business condition — per ADR-001." The record transmits not
   just the decision but its scope.

2. **The equal-compute control passes.** control 5/5 DRIFT — the length-matched filler drifts
   exactly like floor, cites only its OWN (logging) ADR, and **never confabulates a Result
   convention**. So the withrecord effect is the carried D, not the token load.

3. **The preference PERSISTS at the frontier — it does NOT dissolve.** The frontier model
   defers to the recorded arbitrary convention even though its own floor default is 5/5 the
   opposite (`raise`) and Result is counter-Pythonic idiom. **0/5 expressed any
   override-reluctance** — no cell argued the convention should be overridden by the model's
   own equally-valid idiom.

## Prediction scorecard (PREDICTION.md)

- withrecord HOLDs at both models → **confirmed** (5/5, 5/5).
- floor DRIFTs at both → **confirmed** (0/5, 0/5).
- control DRIFTs at both, no confabulated Result convention → **confirmed** (0/5, 0/5).
- preference PERSISTS at the frontier (does not dissolve) → **confirmed**, and it
  **contradicts** the SOUL-123/F044 conjecture ("a preference would likely dissolve at the
  frontier") — that conjecture is now tested and **FALSE**.

## Verdict for the study (the reframe)

This moves the study's central line. The fact/preference split is **not** the frontier line.
The line is **DERIVABLE** (the model can re-reason it — anchoring, skill-routing → it
DISSOLVES) vs **UNGUESSABLE** (the model cannot regenerate it — an external FACT, SOUL-123,
OR an arbitrary CONVENTION, here → it PERSISTS). The accumulating record governs even
arbitrary team conventions at the frontier.

## Bounds (Skeptic)

- One preference, one drift type, n=5, two models, a single dilution step.
- The convention here was clearly-stated and defensible — a terse or absurd convention might
  not install, or might get overridden (untested).
- "Evidence now points to" the derivable-vs-unguessable reframe is an **inductive** reframe
  over ~4 points (F044 fact-persists, this preference-persists, anchoring + routing
  derivable-dissolve) — not proven.

**Raw arms gitignored** (`arms/` is regenerable via `run.sh`). Models:
claude-haiku-4-5-20251001, claude-sonnet-4-6.
