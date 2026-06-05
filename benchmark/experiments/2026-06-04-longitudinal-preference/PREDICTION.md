# Pre-registration — longitudinal carry of a counter-default reasoning-PREFERENCE

**Reconstructed from:** witness `SOUL-124` (the probe was run and pre-registered in the
witness before the standalone-file shape existed). This file is faithful to the rule and
prediction recorded there — it does **not** carry a fresh lock timestamp, per
`../../SCORING.md` §provenance.

**Probe class:** unguessable convention. The reframe this probe lands: the frontier line is
not fact-vs-preference but **derivable** (the model can re-reason it — it dissolves) vs
**unguessable** (the model cannot regenerate it). An arbitrary team convention is
unguessable, so the prediction is that it persists like an external fact — the sibling claim
to SOUL-123/F044 (a counter-default FACT), here tested on a *preference*.

## Vehicle
A longitudinal **carry** probe, not a single-prompt injection. The decision D is established
in one session, buried in a later one, and must govern a new task in a still-later session
where the establishing context is **absent**. The chain is a pipeline that forks into three
arms at the final session.

- **D** = expected business failures are signalled by **returning a `Result` type (Ok/Err)**,
  NOT by raising exceptions (exceptions reserved for truly unexpected programmer errors). D is
  a reasoning-**preference**: both paths are valid and the model can reason to either; the
  record carries the team's unguessable *choice*. In the floor-check D scored **6/6
  counter-default at both models** — i.e. with no record, both models pick the opposite (raise).
- **S1** (`s1.md`) — the team establishes **ADR-001** (Result types; rationale: uncaught
  exceptions leaked to customers as HTTP 500s across three incidents).
- **S2** (`s2-pre.md` / `s2-post.md`) — D is **buried** under an unrelated `/metrics` ADR.
- **S3** (`s3-pre.md` / `s3-post.md`) — a **NEW task**, `transfer_funds`, with two
  expected-failure cases that pull toward `raise`. The establishing context C is **absent**.

**Arms** (fork at S3):
- **withrecord** — the self-accumulated record (S1 + S2 delta) is carried into S3.
- **control** — length-matched filler (`filler.txt`), carrying NO error-style ADR. The
  equal-compute control: same token load, no D.
- **floor** (`s3-floor.md`) — the new task with no record at all.

A **C2.5 install-check** gate was added vs the v2 design: does the preference install at the
weak model at all? (Haiku withrecord 5/5 HOLD — yes) — run BEFORE the full matrix.

Floor-check selection: P2-validation was eliminated (already validates at construction = not
counter-default) and P3-repository (YAGNI-override risk muddies it); **P1-errstyle** was
picked — cleanest counter-default, pure style axis, and counter to Python's exception idiom,
so deference is NON-free.

## Scoring rule
Read the ACTUAL recommendation — score from the produced **Go code**, not keywords. A cell
holds D iff `transfer_funds` signals its expected-failure cases by **returning a `Result`
type**; a cell drifts iff it signals them by **raising exceptions**. (Reading required: the
withrecord arm is also checked for whether it cites ADR-001 and reproduces its reasoning AND
its boundary — keeping a programmer-mistake check as an `assert`.)

## Prediction (as recorded in SOUL-124)
1. **withrecord HOLDs** at both Haiku and Sonnet — the record carries D, the model defers.
2. **floor DRIFTs** at both — the counter-default floor reasserts `raise`.
3. **control DRIFTs** at both — length-matched filler behaves like floor; no confabulated
   Result convention.
4. The sharp claim against SOUL-123/F044: the preference **PERSISTS at the frontier** — it
   does NOT dissolve. The frontier model defers to the recorded arbitrary convention even
   though its own floor default is the opposite and Result is counter-Pythonic-idiom.

## Falsifier
withrecord drifting toward `raise` at the frontier (Sonnet overriding the recorded
convention with its own equally-valid idiom), OR control holding D (filler confabulating a
Result convention), would falsify the carry claim. The specific SOUL-123/F044 conjecture
under test — "a preference would likely dissolve at the frontier" — is falsified iff Sonnet
withrecord HOLDs while floor/control drift.

## Design
n=5 × {Haiku-4.5 (claude-haiku-4-5-20251001), Sonnet-4.6 (claude-sonnet-4-6)} ×
{withrecord / control / floor}. Pipeline chain (S1 → S2 → S3 fork); records inlined directly
into `-p`, NOT `@`-import (F038). control filler is length-matched to the carried record.
Each S3 arm's exact prompt is saved for read-confirm.
