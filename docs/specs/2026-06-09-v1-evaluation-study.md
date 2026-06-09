# The v1.0 Evaluation Study — pre-registration (grilled)

**Date:** 2026-06-09 · **Status:** awaiting Body launch approval · **Grilled:** yes (8 branches resolved)
**Runs on:** paired branches `study/v1-evaluation` in Soul-System (corpus) and soul-benchmark (lab)

## Purpose

Evaluate Soul System 1.0 — its values, defects, and improvement targets — as a single
long-running autonomous study. Not a new benchmark from scratch: the study pays the
**named measurement debts** the 0.x study (SOUL-116→129, `docs/study/`) left open, plus
the one debt 1.0 itself created (THE CUT was a compression event; F045 predicts
compression strips force).

## Glossary (terms crystallised in the grill)

- **Erosion audit** — re-running proven probes against the post-cut 1.0 artifacts vs
  their pre-cut versions to test whether THE CUT stripped force (F045 applied to our
  own release).
- **Record-don't-repair** — on a failed validity gate the orchestrator records the
  finding and adds a *candidate* repair as an experimental arm; it never modifies
  doctrine. Graduation is the Body's, at merge.
- **Merge-time graduation** — the study drafts witness entries / finding candidates in
  its own corpus; the Body appends to `witness.md` (re-read-verify) and graduates
  findings after reviewing the merged branch. Preserves the append-only sequential-ID
  invariant across the branch fork.
- **Twin-arm in-vivo** — one pre-registered greenfield project built twice in parallel
  session chains (seed-on vs length-matched generic CLAUDE.md), giving real
  multi-session history AND a counterfactual (closes the SOUL-144 gap).
- **Lab/product split** — per SOUL-149, experiment harnesses and raw arms live in
  soul-benchmark; study claims and reports live here. This study honors the split.

## Resolved design decisions (the grill record)

| # | Decision | Resolution | Why |
|---|----------|-----------|-----|
| 1 | Objective | All four candidates, phased composite | Each pays a distinct named debt |
| 2 | Sequencing | Gated pipeline; Phase 1 is a validity gate; record-don't-repair on failure | Phase 1 validates the instrument every other phase loads |
| 3 | In-vivo vehicle | Seeded greenfield, twin arms | Only design giving both real history and a counterfactual |
| 4 | Model matrix | Haiku 4.5 + Sonnet 4.6 + Opus 4.8, n=5; adaptive n→10 on non-unanimous cells | Sonnet kept for comparability with 0.x study; Fable 5 excluded (no prior calibration) |
| 5 | Record protocol | Branch-local study log (STUDY-NNN), merge-time graduation | Branch fork = two timelines; re-read-verify can't span them |
| 6 | Layout | Harness/arms in soul-benchmark branch; corpus in Soul-System branch | Lab/product split (SOUL-149, same-day precedent) |
| 7 | Runner | One orchestrator agent in worktrees; `run.sh` + `claude -p` arms; notify at phase gates, never wait; never push | Proven SOUL-122→129 pattern; pushes are Body-owned (outward-facing) |
| 8 | Stopping | Capped + null-honoring (see Stopping rules) | Unwatched compute needs ceilings; null is a publishable result |

## Phases

### Phase 1 — Erosion audit of THE CUT  *(validity gate for all else)*

**Question:** did the 263→168-line seed cut (and Mind 174→113, gate 130→58) strip the
force of the unguessable content, per the F045 mechanism?

- **Artifact pair:** pre-cut = `e4e26d0~1` (last 0.x state), post-cut = the study
  branch's fork point on main. Diff scope note: post-cut also includes the
  commands→skills migration (4f2f668) — the audit targets the always-on doctrine
  artifacts (seed, mind.md, completion-gate doctrine), not command plumbing.
- **Probes** (all are re-runs of proven instruments):
  - **P1.1 trap-recall** — does the post-cut record still prevent the F038 trap?
    (0.x result: 10/10 vs 2/5 filler.)
  - **P1.2 fact-carry** — SOUL-123-style buried counter-default fact under the
    post-cut scaffold vs pre-cut. (0.x result: 5/5 hold.)
  - **P1.3 gate-fire conformance** — fresh-agent orientation + completion-gate firing
    under the 1.0 seed. (Cut-time spot check: 6/6; this is the full version.)
  - **P1.4 force-preservation** — sample mind.md rules whose source findings carry
    incident force (F045's instrument); does the distilled rule still stop the frontier
    model, or does it fabricate?
- **Cells:** 4 probes × {pre, post} × 3 models × n=5 ≈ 120 arms (cap 180).
- **Pass rule:** post ≥ pre per probe/model cell. Non-unanimous regression → extend to
  n=10. Confirmed regression → record-don't-repair: draft finding + a candidate
  force-restored seed becomes an **extra arm** in Phases 2–4 (both seed variants run).

### Phase 2 — F044 open rungs  *(parallel with Phase 4 after Phase 1 passes)*

The bounds ledger's named rungs, on the SOUL-123 harness (template already in
soul-benchmark):

- **Interaction** — does fact D survive a later *contradicting* record entry?
- **Middle-position** — D not at primacy; does it still fire?
- **Multi-fact** — several interacting planted decisions, not one.
- **Long decay** — N ∈ {50, 100} burial depth (current max evidence: N=20, no cliff).

**Cells:** 4 rungs × {with-record, length-matched control, floor} × 3 models × n=5
≈ 180 arms (cap 270). Read-confirmed outcomes (artifact inspection, never keywords).

### Phase 3 — Sequential stream → conditional soul-bench

Honors the archived pre-registration (`docs/archive/specs/2026-05-21-token-economics-stream-experiment.md`,
design locked 2026-05-21): 8 linked tasks, Soul-on vs Soul-off, cost-per-task vs
position, conformance instrumented. **Gate:** only if the stream shows a cost/quality
slope does the orchestrator extend the soul-benchmark suite toward the standalone
bench (Step 3 of `docs/archive/specs/2026-05-21-token-economics-measurement-design.md`).
No slope → record the null, close the question.

### Phase 4 — Twin-arm in-vivo greenfield  *(parallel with Phase 2; wall-clock-bound)*

- **Vehicle:** pre-registered spec for a realistic small project (~12 feature
  increments; CLI tool or small service — orchestrator drafts the spec as its first
  Phase-4 act, before any arm runs).
- **Arms:** A = 1.0 seed content inlined (F038 discipline); B = length-matched generic
  CLAUDE.md. Same increments, same order, separate session chains, **Opus 4.8** driver.
- **Planted signal:** counter-default decisions established in increments 2–3;
  temptation events (natural opportunities to violate them) in later increments.
- **Measures:** drift/hold on planted decisions (read-confirmed in code); unplanned
  divergence mined post-hoc; per-increment cost (feeds Phase 3's question).

## Measurement discipline (non-negotiable, every arm)

1. **Inline, never @-import** (`--append-system-prompt-file`) — F038.
2. **Sentinel-test every arm** — verbatim-quote check before trusting any result.
3. **Length-matched controls** at every comparison (content, not volume).
4. **Read-confirm outcomes** in the artifact, never keyword-grep.
5. **PREDICTION.md before the first arm** of each probe (benchmark repo convention);
   RESULT.md after. Pre-registration locks hypotheses; no mining for positives.
6. **Null honored** — "no effect" is recorded and the probe closes.

## Stopping rules

- Per-phase arm caps as listed (estimates +50% headroom for adaptive extension).
- **5-day wall-clock ceiling** for the whole study.
- ≤2 retries per failed arm.
- **Sentinel failure rate >10% in a phase → halt that phase** (instrument broken —
  F038 territory; Multiverse Warning applies: name it, don't patch around it).
- Rate-limit storms → exponential backoff; persistent walls → halt phase, log.
- Anything unfinished at a ceiling enters the **open-rung ledger** in the final
  report — explicitly, never silently dropped.

## Orchestrator protocol

- Worktrees + branch `study/v1-evaluation` in both repos; **no pushes** of any
  branch (outward-facing actions are Body-owned).
- Writes only to: soul-benchmark `experiments/` (harness, arms, raw results) and
  Soul-System `docs/study/2026-06-v1-eval/` (this corpus: study-log.md with STUDY-NNN
  ids, phase reports, drafted witness entries / finding candidates).
- Never touches: `witness.md`, `findings/`, `ideas.md`, `mind.md`, seed, hooks,
  anything on main.
- At each phase gate: write phase report → push notification to the Body → continue
  (does not wait).
- Final deliverable: `99-summary.md` — per-phase results, finding candidates ranked,
  drafted witness entries, open-rung ledger, and a recommended graduation list for
  the Body's merge review.

## Launch

Body reviews this spec → says go → orchestrator creates the worktrees and begins
Phase 1.
