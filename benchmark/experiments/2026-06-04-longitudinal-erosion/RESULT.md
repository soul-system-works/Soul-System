# Result — longitudinal erosion (the /soul-distill stress test) (2026-06-04)

**Source of record:** witness `SOUL-126` + `SOUL-127`. This is the experiment behind finding
**F045** (anti-prior facts are partly *incompressible*: their FORCE, not just their
proposition, must survive compression). Pre-registration in `PREDICTION.md`.

The probe ablates decision D across compression levels at fixed depth N=1. The headline is a
**gradient of anchoring force, not a binary of content** — and the experiment caught the
project nearly over-claiming ("naive distill ships a Coherent Falsehood"), then corrected it
against the real instrument.

## The two outcomes

### 1. The directive survives compression (30/30)
The no-auto-retry rule ("must NOT auto-retry; fail fast") holds across **every** hand-authored
compression level, both models, both capabilities — even compressed to a single distilled
line in a 6-rule set. The *rule* is carryable-compressed.

### 2. The unguessable FACT does not — fabrication is a gradient (Sonnet reader)
"Drift" here = the Sonnet reader fabricates idempotency-dedup: sets `Idempotency-Key: payoutID`
and reasons "provider deduplicates, so manual retry is safe." It does not — the full D records
no idempotency support.

| level | Sonnet reader (fabricates idempotency-dedup) |
|---|---|
| e0 — full D (decision + rationale + 1,180 incident + the FACT) | **0/5** |
| real Sonnet-distill (faithful, terse) → fed downstream | **2/5** |
| real Haiku-distill → fed downstream | **5/5** |
| edir / edist — hand-erosion (FACT stripped) | **4/5** (4/5 edir, 4/5 edist) |

**Haiku reader: 0/15 at every level** — the weak model never fabricates. It lacks the
confident generation, so it defers retry to the caller *without* claiming false safety. No
strong prior to assert, no Coherent Falsehood.

## Read-confirmed findings

1. **The full FACT prevents the fabrication.** e0 Sonnet 0/5; some outputs explicitly reject
   the idempotency path (as in SOUL-123). The 1,180-customer incident + explicit "NO support"
   is what stops the frontier model.

2. **Strip it and the frontier fabricates.** Hand-erosion (edir/edist) → Sonnet 8/10 sets a
   false `Idempotency-Key` and reasons the provider deduplicates. A latent double-payment
   falsehood — the original danger (caller-driven retry) one level removed.

3. **The smart model's strength is what makes fact-erosion dangerous.** Haiku 0/15: the weak
   model never regenerates the missing reason. Compressing a rule while dropping its
   unguessable rationale preserves the rule but lets the *frontier* model regenerate the
   missing reason as a Coherent Falsehood (A010).

4. **The real distiller is more careful than the hand-authored erosion — but force still
   leaks.** The honest correction the experiment forced:
   - The real **Sonnet** distiller (n=5, neutral prompt on the 21-ADR log) **preserves the
     anchor 5/5**: every rule-set keeps "non-idempotent" (4/5) and "verify status before any
     manual retry" (5/5). So "naive distill ships a Coherent Falsehood" was *itself* heading
     toward a Coherent Falsehood.
   - The real **Haiku** distiller (n=5) keeps the anchor **proposition** too: no-auto-retry
     5/5, verify-before-retry guard 5/5, explicit "non-idempotent" 3/5 (Sonnet kept it 4/5).
   - **But feeding either distilled record back downstream still fabricates:** Sonnet-distill
     → 2/5; Haiku-distill → 5/5. The record *says* non-idempotent and keeps the verify guard,
     yet the frontier reader fabricates anyway. What compression strips is the **stopping
     force** of a fact that contradicts the model's strong prior, not the proposition.

## Prediction scorecard (PREDICTION.md)

- Directive compression-robust → **confirmed** (30/30).
- Unguessable FACT not compression-robust; frontier fabricates under erosion → **confirmed**
  (edir/edist 4/5 each).
- Full FACT prevents it → **confirmed** (e0 Sonnet 0/5).
- Weak model never fabricates → **confirmed** (Haiku 0/15).
- Real-instrument open question → **resolved, and it corrected the framing:** the real
  distiller *preserves the proposition* (Sonnet 5/5, Haiku keeps it too), yet downstream
  fabrication persists (2/5, 5/5). The headline is therefore a **gradient of force**
  (full D 0/5 → faithful Sonnet-distill 2/5 → Haiku-distill 5/5 → hand-erosion 4/5; Haiku
  reader 0/15), **not** a binary of content. The naive "naive distill ships a falsehood"
  claim was caught and downgraded.

## Verdict

This is the experiment behind **F045**: facts that **contradict a strong model prior are
partly incompressible** — their *force*, not just their proposition, must survive compression,
or the frontier model re-asserts its prior as a Coherent Falsehood. Compression preserves
rules *and* safeguards (the verify guard) but strips the stopping-force of the anti-prior
fact. The implication for `/soul-distill` + `mind.md`: preserve the unguessable FACT's force
— keep the incident and the explicit "NO support" — especially for facts that **preclude a
plausible-but-wrong approach**. This sharpens derivable-vs-unguessable: the rule is
carryable-compressed; the unguessable fact behind it is not safely compressible. The weak
distiller is not strictly worse (see bounds), but its output carries no more stopping force —
if anything less — and the frontier reader fabricates regardless of which model distilled.

## Bounds (Skeptic)

- One D, one prior (idempotency), one fabrication type, n=5, two models, hand-authored erosion
  levels plus one Haiku distillation fed downstream.
- The 5/5-vs-2/5 (Haiku-distill vs Sonnet-distill downstream) is **directionally consistent**
  with "harder compression → less stopping-force" but is **confounded**: haiku-1's rule 1 is
  terser (drops the endpoint list `POST /charges,/refunds,/payouts` and the "explicitly" that
  sonnet-1 kept), so phrasing and full 20-rule context differ, and it is noisy at n=5. **Not
  claimed:** "Haiku distiller strictly worse."
- A genuine model-distilled compression was tested (the real-instrument stages); the gradient
  rests on a single Haiku distillation routed downstream.
- Primacy position; context C absent by design.

**Raw arms gitignored** (`arms/` is regenerable via `run.sh`). Models:
claude-haiku-4-5-20251001, claude-sonnet-4-6.
