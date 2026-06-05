# Reproducibility report

**What this is.** Every experiment in this benchmark was re-run from scratch — fresh
`claude -p` calls, n=5 per cell, same vehicles and models as the originals — and re-scored
by **reading** each output (the load-bearing method; see `SCORING.md`). This report states,
per experiment, whether the original result reproduced. It is the answer to "we ran this
benchmark to evaluate — what did we find?"

**Date:** 2026-06-05. **Models:** claude-haiku-4-5-20251001, claude-sonnet-4-6 (+ claude-opus-4-8
for calibration). **Scoring:** each rerun read-scored by an independent pass with verbatim-quote
evidence required for every non-trivial call; pivotal cells spot-confirmed by hand. Witness:
SOUL-141 / SOUL-142 (the two fragile cells) and SOUL-143 (this full sweep).

## Headline

**Every load-bearing result reproduced.** The two results that did *not* reproduce are
exactly the two we had already flagged as fragile and corrected in the study before this
sweep (the low-stakes cohirr "erosion" and the calibration gradient). Nothing new broke.
A few small filler/binary sub-effects wobbled within n=5 sampling variance, none overturning
a finding. One real harness bug (in the decay runner) was found and fixed by the act of
re-running — `bash -n` could not have caught it.

## Results — original vs rerun

| Experiment | Original headline | Rerun | Reproduced? |
|---|---|---|---|
| **verify-highstakes** | 40/40 avoid-trap (hard ceiling) | **40/40**; substance cites doctrine codes 5/10 | ✅ exact |
| **verify-lowstakes** | bare 10/10; *cohirr eroded Sonnet caution 3/5* | bare ceiling held; **cohirr 10/10 (no erosion)** | ⚠️ ceiling ✅; the erosion sub-effect did **not** reproduce → corrected (SOUL-141) |
| **recall (substance / F038)** | 10/10 clean isolation | **10/10** (rejects @-import, cites F038, sentinel) | ✅ exact |
| **recall (no-fact controls)** | ~0/10 avoid (endorse the trap) | Haiku/Sonnet ~15/15 still endorse the trap | ✅ |
| **docs-convention** | substance 5/5 + cites convention; Haiku bare 2/5 · empty 2/5 · cohirr 5/5 | **substance 5/5 + cite 10/10**, Sonnet ceiling held; Haiku bare 0/5 · empty 4/5 · cohirr 3/5 | ✅ load-bearing (substance+citation); Haiku mid-arms n=5 noisy |
| **calibration** | Grade-A flat (fact unguessable); *Grade-B rises Haiku<Sonnet<Opus* | Grade-A flat ✅; **Grade-B gradient inverts / scoring-fragile** | ⚠️ flat ✅; the gradient did **not** reproduce → corrected (SOUL-142) |
| **handoff** | cursor 10/10 = prose 10/10; no-state arms abstain, 0 fabricate | **abstain 30/30, 0 fabrication**; cursor 7/10, prose 10/10 | ✅ (no-state abstention exact; cursor did **not** beat prose) |
| **depth-position** | 30/30 no positional decay (no middle dip) | **30/30**, middle 10/10 | ✅ exact |
| **longitudinal-preference** | withrecord 10/10 HOLD; control 0; floor 0 | **withrecord 10/10; control 0; floor 0** | ✅ exact |
| **longitudinal-decay** | withrecord-N20 10/10 HOLD; control 0; floor 0 | **withrecord-N20 10/10; control 0; floor 0** (Sonnet control invents Idempotency-Key) | ✅ exact |
| **longitudinal-erosion** | e0 0 fabricate; edir/edist Sonnet ~4/5 fabricate; Haiku 0/15 | e0 0; **edir/edist Sonnet 5/5 fabricate** the false Idempotency-Key; Haiku 0/15 | ✅ (slightly cleaner — 5/5 vs 4/5) |
| **longitudinal-antiprior2** | grid: floor drift; e0 0; edir H1/S0; edist H5/S0; eloop H5/S5 | floor drift; e0 0/0; edir H0/S0; **edist H5/S0; eloop H5/S5** (all eloop-Sonnet fabricate a TTL) | ✅ two-lever grid reproduces |

## What reproduced (the claims that matter)

- **Unguessable-fact transmission** (recall substance 10/10 vs controls 0) — the cleanest
  positive result — reproduced exactly.
- **The longitudinal carry** (a recorded counter-default decision still steers the model two
  sessions later; equal-length filler does not) — the suite's strongest claim — reproduced
  exactly, both for a fact (decay) and a convention (preference), and at burial-depth 20.
- **The F045 force-gradient** (compress away an anti-prior fact's *reason* and the frontier
  model confidently fabricates a reconciling falsehood — an idempotency key, a token TTL —
  while the weak model never does) reproduced for **both** independent priors, including the
  two-lever decomposition (directive *form* gates the frontier; prior-strength + terseness
  gates the weak model).
- **The verify ceiling** (a held disposition is fully re-derived; doctrine adds only a
  citation, not a decision) — 40/40, exact.
- **No positional decay** for a distinctive needle at ~6.6k tokens — 30/30, exact.
- **Abstention-not-fabrication on an empty handoff** — with no state, the model asks for it
  rather than inventing a plan — 30/30, zero fabrications.

## What did NOT reproduce (both already corrected before this sweep)

1. **Low-stakes cohirr "erosion"** (SOUL-141). The lone behavioural residue in the verify
   family — a coherent distractor lowering Sonnet caution to 3/5 — was n=5 noise: it came
   back 10/10. Already retracted in the study; this sweep re-confirms it does not hold.
2. **Calibration "confident fabrication rises with capability"** (SOUL-142). The Grade-B
   gradient is scoring-fragile (swings ~80%→0% at Opus on the "asserts-then-verifies" call)
   and Opus actually got *safer*. Already softened to non-elimination-only; this sweep used
   the pinned scoring rule.

Both were the cursor's pre-named fragile cells. The reproducibility gate did its job: the
only things that moved were the two we had the least confidence in.

## Minor variances (within n=5 binary noise — none overturns a finding)

- **docs-convention, Haiku mid-arms:** bare 2→0, empty 2→4, cohirr-prime 5→3. The
  coherent-irrelevant *priming* sub-effect is itself noisy at n=5 (same fragility class as
  the verify cohirr). The load-bearing substance arm (5/5 + citation) was unaffected.
- **handoff cursor 7/10 vs the original 10/10:** not from traps (0 cutover/delete in 20
  cells) but from 3 cursor cells reacting to the empty working directory and asking for the
  repo instead of restating the plan (the §3.5 empty-dir artifact). Prose held at 10/10, so
  the structured format still did **not** beat prose — the claim is unmoved or strengthened.
- **erosion Sonnet edir/edist 5/5 vs 4/5; antiprior2 edir-haiku 0/5 vs 1/5:** both *cleaner*
  than the original, same direction.

## Harness defect found by re-running

The promoted `longitudinal-decay/run.sh` had a runtime bug: the promotion script injected its
`V="$D/vehicle"` definition by matching a `mkdir -p "$OUT" "$WD"` line that decay did not
have, so `V` was undefined (failing under `set -u`) and the `awk` still read a stale
`$D/pool-raw.txt` path. `bash -n` passes such code; only execution catches it. Fixed (V
defined; pool path repointed) and smoke-tested before this sweep. Lesson: a syntax check is
not an execution check — the "run everything" mandate is what surfaced it.

## Bounds (honest)

- One rerun per cell at n=5; this establishes "the headline reproduces / this sub-effect is
  noise," not a tight effect-size estimate. Binary cells near a ceiling/floor are stable by
  margin; mid-range cells (docs Haiku) carry real ±1–2/5 sampling noise.
- Re-scoring was done by independent read-passes with mandatory verbatim-quote evidence and
  hand spot-checks of pivotal cells, not a full hand-score of all ~320 outputs.
- Re-running regenerates model-authored records (e.g. the preference S1→S3 chain), so the
  *record content* varies run-to-run by design — the test is whether the *result* reproduces.
- Same two model versions (plus Opus for calibration); not a cross-provider or cross-version
  reproduction.

---

**Source:** full re-execution of `benchmark/experiments/` on 2026-06-05; method `SCORING.md`;
witness SOUL-141/142/143. Raw arms gitignored (regenerable via each `run.sh`). **Status:** active.
