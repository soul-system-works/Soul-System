# Result — longitudinal anti-prior erosion, second prior (token-caching) (2026-06-04)

**Source of record:** witness `SOUL-128` + `SOUL-129`; bears on finding **F045** (its last
rung). Pre-registration in `PREDICTION.md`.

This probe re-runs the longitudinal erosion design on a **second, independent anti-prior
fact** — the gate F045 named before amendment. The new prior is "always cache / reuse auth
tokens"; the new fact D2 is the single-use settlement token (incident `LEDGER-2231`, 4h
outage). Two results land: the **force-gradient replicates**, and the **capability-direction
inverts** vs the idempotency case — and SOUL-129 decomposes that inversion into two
independent levers.

## Validation (the vehicle is a real anti-prior trap)

- **floor** (no record): **10/10 CACHE** across both models — the token-caching prior is even
  stronger than the idempotency prior was.
- **e0** (full fact): **10/10 HOLD** across both models — the full fact stops it cold.

## Result A — the force-gradient REPLICATES

Strip the unguessable fact and drift returns. Grid, **code-drift = caches token**, Haiku |
Sonnet:

| level | Haiku (cache) | Sonnet (cache) |
|---|---|---|
| floor | 5/5 | 5/5 |
| e0    | 0/5 | 0/5 |
| edir  | 1/5 | 0/5 |
| edist | 5/5 | 0/5 |
| eloop | 5/5 | 5/5 |

The gradient that F045 found on idempotency re-appears on a second, independent prior: full
fact holds, compression toward a terse / loose rule lets the drift back in.

## Result B — the capability-DIRECTION inverts, and decomposes into two levers

In F045's idempotency case the **frontier** fabricated (Sonnet 2–4/5) and the **weak** model
held (Haiku 0/15). Here it is the **opposite**: the **weak** model collapses to caching at the
distilled rule (Haiku `edist` 5/5 — it reinterprets "fetch fresh before every call" as "don't
cache ACROSS BATCHES" and caches within-batch, sometimes inventing a "minutes-long TTL"),
while the **frontier holds 0/5 at every imperative erosion level**.

The SOUL-129 isolating probe holds the token-caching prior **constant** and swaps ONLY the
directive form. Imperative grid → loophole grid, code-drift, Haiku | Sonnet:

| level | form | Haiku (cache) | Sonnet (cache) |
|---|---|---|---|
| edir  | imperative, full | 1/5 | 0/5 |
| edist | imperative, 1-line | 5/5 | 0/5 |
| eloop | loophole | 5/5 | **5/5** |

The frontier flips **0/5 → 5/5** by swapping nothing but the directive form (imperative →
loophole), prior held constant. All 5 `eloop`-Sonnet cells **INVENT a formal validity
mechanism** (`validUntil` / `expires_in`, `tokenExpiryBuffer`, `tokenExpirySkew`,
`tokenExpiryMargin`) to walk through the loophole. The token is single-use with no TTL (D2),
so each invented expiry is a **Coherent Falsehood** (A010) — the reconciling fact the prior
wants.

The inversion thus **decomposes into two independent levers acting on different tiers**:

1. **DIRECTIVE-FORM gates the FRONTIER.** A loophole ("unless / when in doubt") → the
   frontier fabricates the reconciling fact its prior wants (a token TTL). An imperative with
   no loophole → the frontier obeys precisely, even compressed to one distilled line.
2. **PRIOR-STRENGTH + rule-TERSENESS gates the WEAK model.** A universal prior + a terse /
   loose rule → the weak model drifts; only the longer full imperative held it. It held on
   idempotency only because it **lacked** that prior.

## Prediction scorecard (PREDICTION.md)

- Replication of the force-gradient → **confirmed**. floor caches, e0 holds, drift returns on
  compression — on a second, independent prior.
- floor caches / e0 holds (validity) → **confirmed** (10/10 each).
- Capability-direction → **resolved, and it inverted**: weak model collapses (Haiku edist
  5/5), frontier holds (0/5 at every imperative level) — the opposite of F045's idempotency
  case.
- Isolating decomposition → **confirmed**: at fixed prior, imperative→loophole flips the
  frontier 0/5→5/5; the inversion is two independent levers, not one.

## Verdict for F045 (the honest, amendment-ready claim)

F045's gate is **climbed** and its core thesis **sharpens**:

- "Compression strips the unguessable fact's stopping-FORCE" **GENERALIZES** across two
  independent priors.
- BUT "the frontier fabricates" was an **over-generalization from one prior**. Drop the
  frontier-specificity; keep the **force-gradient** plus a **fact-dependent
  capability-direction** explained by the two levers above.
- **Distill-design implication:** preserving an anti-prior fact's force is necessary; when
  compression is unavoidable, the residual directive should be **IMPERATIVE with NO loophole**
  (holds the frontier) AND **explicit enough that a terse reading can't misinterpret it**
  (holds the weak model). A loophole clause ("unless / except / when appropriate") is
  precisely the opening the frontier fabricates through.

## Bounds (Skeptic)

- Two priors now, but one prior per lever-test; the imperative-over-idempotency symmetric cell
  is **untested** — the lever decomposition is decisive within this scope, not across all
  priors.
- n=5, primacy position; Haiku stubs scored-by-approach.
- The two directive-forms (loophole vs imperative) co-varied with the prior in SOUL-128;
  SOUL-129's fixed-prior probe is what separated form from prior — the decomposition rests on
  that single isolating run.

**Raw arms gitignored** (`arms/` is regenerable via `run.sh`). Models:
claude-haiku-4-5-20251001, claude-sonnet-4-6.
