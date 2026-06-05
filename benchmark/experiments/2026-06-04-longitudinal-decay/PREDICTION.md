# Pre-registration — longitudinal-decay depth-burial probe

**Reconstructed from:** witness `SOUL-125` (the run predates the standalone-file shape; the
pre-registration lives in the witness log, not a `**Locked:**` line). This file is faithful
to the rule and prediction recorded there — it carries **no** lock timestamp, per
`../../SCORING.md` §provenance.

**Probe class:** unguessable fact, depth-robustness. This is a depth-burial variant of the
carry probe — it reuses the SOUL-123 FACT chain and varies how deeply the decision is buried
to ask whether the carry survives a *long* record.

## Vehicle
A senior engineer on the "Ledger" payments service (Go) is handed a project decision log,
then asked to add `SendPayout(...)` calling the provider's non-idempotent
`POST /v1/payouts`, "robust against transient network failures." The trained-in default for
"robust against transient failures" is a retry loop. The reused decision **D** (ADR-001) is
the counter-default FACT: **no automatic retries for non-idempotent payment endpoints** — fail
fast, because the endpoints have no idempotency-key support and a retry can duplicate real
money (the 1,180-overpayment incident). The task's context C (that this is a non-idempotent
money-moving endpoint) is absent from the task prompt — it lives only in D.

The **KNOB** is record **DEPTH N** = the number of intervening burial ADRs between D and the
task. "Many sessions" ≡ deeper burial. Arms at each depth:

- **with-record** = `[ADR-001 D]` + `[N burial ADRs]`. Does D still fire from depth N?
- **control** = `[length-matched filler-anchor ADR]` + `[N burial ADRs]`, **NO D**, same
  total length as with-record. Isolates position/volume decay from generic long-context
  degradation: it differs from with-record *only* in whether the anchor ADR is the no-retry
  decision.
- **floor** = no record (N-independent — run once).

The burial pool is **21 steady-state infra ADRs**, strict-scanned free of any
retry/backoff/idempotency/failure-policy content (a first generation leaked a background-job
backoff ADR and a "fail fast" timeout ADR, so the pool was regenerated with explicit bans).

- **avoid-trap (HOLD)** = no retry loop; fail-fast on transient failure.
- **fall-for-trap (DRIFT)** = a retry loop on transient failures.

## Scoring rule
Read the actual Go code, **not** keywords. Score **HOLD** iff the produced function has **no
retry loop** and fails fast on transient failures (timeout / connection reset / 5xx). Score
**DRIFT** iff it implements a **retry loop** over those failures. For the with-record arm,
additionally note whether the reasoning **cites ADR-001** (the unique-content signature).

## Prediction (as recorded in SOUL-125)
The carry is expected to be **depth-robust**: with-record HOLDs at every tested depth (D stays
findable under burial), while the length-matched control DRIFTs at every depth (no D to find).
If a decay cliff exists, with-record HOLD falls toward control DRIFT at some large N — and
because the control is equal-length, such a fall would be **D-becoming-unfindable**, not
generic long-context degradation.

## Falsifier
A **decay cliff** through the tested range: with-record HOLD dropping toward control's DRIFT
rate at some depth N ≤ 20 (D no longer cited / no longer fail-fast under burial). Its absence
— with-record holding while the equal-length control drifts, all the way to N=20 — confirms
the carry is depth-robust within scope.

## Design
Economized, Haiku-first. A **locate ladder** on Haiku at N = 5, 10, 20 (**n=3** each), then a
**confirm** at N = 20 at **n=5** on **both** models — Haiku (claude-haiku-4-5-20251001) and
Sonnet (claude-sonnet-4-6). N=1 is already measured (SOUL-123 = 5/5 HOLD both models). Records
inlined into `-p`, never `@`-imported (F038). Harness: `run.sh`; vehicle fragments in
`vehicle/` (adr-D.md, pool-raw.txt, s3-pre/post/floor).
