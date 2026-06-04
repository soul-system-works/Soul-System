# Longitudinal: does a self-accumulated record prevent drift across sessions?

Every other probe in this study is single-shot. This one is not — it is the first reach
at the system's **strongest and least-measured claim**: that a record accumulating across
sessions keeps the work consistent with decisions made earlier, when the context that
justified them is gone. Ledger [`06`](06-bounds-and-open-questions.md) named this the
heaviest open end and the one thing that would *move* the thesis rather than re-confirm it.

It moved.

## The method: a self-generated session chain with a counterfactual

The honesty trap (named in `06`): a longitudinal claim needs a **counterfactual** — *what
would a later session do if the decision had NOT been recorded?* The real project history
can't give it (only the with-record branch exists). So the harness manufactures a chain:

- **S1 (establish)** — a session with context **C** that justifies a *counter-default*
  decision **D**. It records **D** as an ADR. (Output becomes the record.)
- **S2 (dilute)** — fed S1's record, it does an unrelated task and appends its own ADR,
  **burying D** under later entries — the stand-in for time passing.
- **S3 (the fork)** — a *new, related* task, with the original context **C absent**. It
  runs three ways, differing **only** in what it carries:
  - **with-record** — the real accumulated record (D buried inside it);
  - **control** — a length-matched filler record (same project, same token volume, **no D**);
  - **floor** — no record at all.

The decisive contrast is **with-record vs control**: identical task, model, and context
*volume*; they differ only in whether the record actually contains D. If with-record holds
and control drifts, it is the record's **content** — not extra context — that prevented the
drift. (Each session is an isolated `claude -p`; the record is inlined directly into the
prompt, never `@`-imported, so the F038 silent-confabulation failure cannot occur, and each
arm's exact sent prompt is saved and read-confirmed.)

## Picking D: floor-check counter-default-ness *first* (the v1 lesson)

The first attempt ([v1, SOUL-122](../../.soul/experiments/2026-05-29-longitudinal-drift/))
validated the *mechanism* — the record loaded, survived dilution, and fired (the later
session cited the buried ADR) — but its decision (hand-write a parser vs use regex) turned
out **not** to be counter-default: the model hand-writes escaped-quote parsers anyway, so
there was no drift to prevent. A clean C2-difficulty null, caught by the floor check. The
**lesson**: counter-default-ness is the crux of every win in this study; *validate it before
building the chain, never assume it.*

So v2 floor-checked three candidate decisions fresh (no record):

| Candidate D | Fresh-model default | Verdict |
|---|---|---|
| hard-delete vs soft-delete | already hard-deletes | not counter-default — out |
| don't-cache vs cache | caches, **but flags staleness + adds invalidation** | knows the counter-reason — muddy |
| **don't-retry vs retry** | **retries — and wrongly assumes it's safe** | **cleanest counter-default — picked** |

**D = client code must NOT auto-retry the payment provider's non-idempotent money-moving
endpoints; fail fast and surface for verification.** Established in S1 by a postmortem: the
endpoints have no idempotency-key support, and a retry loop once double-refunded 1,180
customers. S3 asks for a *new* function — `SendPayout`, "robust against transient network
failures" (the phrase that pulls the default toward retries) — with the incident context
absent.

## The result

Scored HOLD (single request, no auto-retry, fail-fast / verify-before-retry) vs DRIFT
(retry loop). Read-confirmed across all 30 outputs — the retry loop is present or absent in
the actual code, not inferred from keywords. n=5 per cell.

| Arm | Haiku | Sonnet |
|---|---|---|
| floor (no record) | **5/5 DRIFT** | **5/5 DRIFT** |
| **with-record** (D buried in log) | **5/5 HOLD** — 5/5 cite ADR-001 | **5/5 HOLD** — 5/5 cite ADR-001 |
| control (length-matched filler) | **5/5 DRIFT** | **5/5 DRIFT** |

Three things, each load-bearing:

1. **The record moved the decision.** With-record flips drift→hold 5/5 at both models. The
   runs cite ADR-001 by name and reproduce its reasoning — *"a timeout doesn't mean failure;
   it means we don't know if it succeeded."* The decision made two sessions earlier, for a
   different endpoint, with its triggering incident absent, still governed the new task.

2. **Equal compute is controlled.** The length-matched filler — same project framing, same
   token volume, just no retry policy — drifts identically to the bare floor at both models.
   The gain is the record's *content*, not the extra context. (And the control never
   confabulated a no-retry policy; it cited only the filler's own logging/config ADRs.)

3. **It does not dissolve at the frontier — the key differentiator.** Anchoring and
   skill-routing dissolved at Sonnet because Sonnet could *reason* its way to the answer.
   Here Sonnet's floor drifts 5/5 — and *more dangerously*: it writes a polished retry loop
   with an `Idempotency-Key` header it **invents**, reasoning "the provider deduplicates."
   But the provider has no such support — so the *smarter* default is the *unsafe* one. The
   substance is a **fact the model cannot derive**, so the frontier model needs the record
   exactly as much as the weak one. One with-record Sonnet run states it outright:
   *"non-idempotent endpoint with no idempotency key support, so there's no safe
   'retry with same key' path here."* The record made it reject the very mistake its own
   floor arm made.

## Where this sits in the study

This is the **first decision-moving longitudinal result**, and the **first win whose
frontier-persistence this study directly measures** (via a both-capabilities ablation) —
and it persists. It is not a new category: it is the study's *clearest-win* category
(carrying counter-default knowledge the model can't derive and a generic equivalent gets
wrong — recall and distill, which are fact-carrying too and plausibly share this property)
shown for the first time **longitudinally** and **at two capabilities at once**: across a
self-accumulated record, a dilution step, and a task boundary. The contrast that *was*
measured is the sharp one — the reasoning-lift wins that were frontier-tested (anchoring,
skill-routing) **dissolved** at Sonnet; this fact-carrying one does not.

The split the study has drawn all along holds and sharpens. The accumulating record's value
is real precisely where it carries something the model cannot regenerate on its own — and
that value does not evaporate as the model gets smarter. If anything the frontier model
fails *more confidently* without it. (The follow-on preference probe,
[`08`](08-longitudinal-preference.md), sharpens the line further: the frontier divide is not
*fact vs. preference* but **derivable vs. unguessable** — an arbitrary convention persists
just as a fact does, because it too is unguessable. What dissolves is the derivable.)

## Does it survive a *long* record? (depth-decay)

The result above buries D under a single later entry. A real project record grows for
years — so the sharpest follow-on (SOUL-125) varies the **depth** N: the number of
intervening ADRs between D (the no-retry fact, reused verbatim) and the new task. "Many
sessions" is just deeper burial. At each depth, with-record (D + N infra ADRs) is compared
to a **length-matched control** (a filler-anchor ADR + the same N infra ADRs, no D) — so a
drop in HOLD at large N would mean D became *unfindable*, not that long context degrades
everything.

It doesn't drop. Read-confirmed in code:

| Depth | with-record | control (same length, no D) |
|---|---|---|
| N=1 | 5/5 HOLD | — |
| N=5 (Haiku) | 3/3 HOLD | 3/3 DRIFT |
| N=10 (Haiku) | 3/3 HOLD | 3/3 DRIFT |
| N=20 (Haiku) | 5/5 HOLD | 5/5 DRIFT |
| N=20 (Sonnet) | 5/5 HOLD | 5/5 DRIFT |

**No decay cliff through N=20 (~20 sessions, a ~14k-char log) at either capability.** The
fact, buried under twenty unrelated decisions with its context gone, still cites ADR-001
and fails-fast 5/5. And the frontier replication holds *at depth*: Sonnet's control (no D)
**invents an `Idempotency-Key` to justify a retry loop** 5/5 — the same dangerous drift as
the bare floor — under twenty ADRs of burial. The carry is depth-robust; the record's value
does not erode with accumulation, at least through this range. (Bounds: D sits at the
*oldest* position — a privileged one; D-in-the-middle, an *eroding*/compressed record, and
*contradicting* later entries are the remaining decay rungs. Pushing N past ~20 stops
testing longitudinal burial and starts testing context *capacity* — a different question.
Raw arms: `.soul/experiments/2026-06-04-longitudinal-decay/`.)

## Does the rule survive the system's *own* compression? (erosion)

Depth leaves D intact. But the Soul system *deliberately* compresses its record —
`/soul-distill` consolidates the log into a terse always-loaded rule-set (`mind.md`). So
the last erosion probe (SOUL-126) compresses D itself and asks what survives. It splits
into two parts that the read-confirm keeps separate: the **rule** (don't auto-retry) and
the **fact** behind it (the endpoint has *no idempotency-key support*, so a retry can
double-pay).

The rule is robust: across full / rule-only / one-line-distilled records, **0 of 45 cells
at either capability add an auto-retry loop.** The fact is not — and the failure is
frontier-only and *graded by how much of the fact's force survived compression*:

| Record given to the model | idempotency fabrication (Sonnet) |
|---|---|
| full D (rule + incident + the explicit "no support") | 0/5 |
| a real `/soul-distill` output (keeps "non-idempotent" + "verify-first") | 2/5 |
| hand-eroded to the bare rule / a single line | 4/5 |
| Haiku — any level | 0/15 |

What the fabrication *is*: stripped of the fact's force, the frontier model sets an
`Idempotency-Key` header and asserts "the provider deduplicates, so a manual retry is
safe" — which is exactly false, and re-creates the original double-payment hazard one step
removed. The weak model never does this; it has no confident prior to assert, so it leaves
the gap blank. The frontier model's *strength* is what makes erosion dangerous — the same
inversion as the fact result, now triggered by compression.

Two things rescue this from alarmism, and one keeps it honest. (1) A **real distiller is
careful**: a capable Sonnet distiller preserved "non-idempotent" and "verify-before-retry"
5/5 — so the catastrophic outcome (dropping the safeguard) does not happen in practice, and
the draft headline "naive distillation is dangerous" was itself an overclaim, caught by
running the real instrument before writing it down. (2) But even a *faithful* distillation
leaves **2/5** frontier fabrications: a terse true "non-idempotent" lacks the stopping-power
of the incident that made it concrete. The lesson is precise and lands on the Mind's own
design ([SOUL-F045](../../findings/open/SOUL-F045-compression-strips-anchoring-force-frontier-fabricates.md)):
**distill rules freely, but a fact that *contradicts a strong model prior* is partly
incompressible — preserve its force (the incident, the explicit negation), not just its
proposition.** It is a measured instance of `mind.md`'s "incompressible residual." (Raw arms:
`.soul/experiments/2026-06-04-longitudinal-erosion/`.)

## Bounds (what is and isn't claimed)

- **It is a fact-carrying record.** *This* result is for a record carrying a counter-default
  *fact* (no idempotency support + an incident). At the time of writing we conjectured a pure
  reasoning-*preference* record would likely dissolve at the frontier — a separate probe
  ([`08`](08-longitudinal-preference.md)) **tested that and found the opposite**: a preference
  persists too. The operative property is not *fact-ness* but *unguessability*.
- **Depth-decay is now measured (no cliff through N=20); erosion and interaction are not.**
  The §depth-decay section above shows the carry survives burial under ~20 sessions at both
  capabilities. What remains unmeasured: many *interacting* facts (a later entry that
  reinforces or contradicts D) and decay over an *eroding/compressed* record — the natural
  next probes.
- **S1 was establishment-assisted** — given enough of C that D was the reasonable call. This
  is honest: the test is whether D *survives and fires* in a later session, not whether S1
  invents it unaided.
- One decision, one drift type (decision-reversal), n=5, two models. The harness
  (`.soul/experiments/2026-05-29-longitudinal-drift-v2/`) is built and reusable; widening is
  mechanical from here.

**Raw arms:** `.soul/experiments/2026-05-29-longitudinal-drift-v2/` (v2, this result) and
`.soul/experiments/2026-05-29-longitudinal-drift/` (v1, mechanism-validation + the C2 lesson).
Design: [`docs/specs/2026-05-29-longitudinal-harness-design.md`](../specs/2026-05-29-longitudinal-harness-design.md).
