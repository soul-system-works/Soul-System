# Longitudinal Drift Harness — Design (pilot)

**Status:** draft — pending Body sign-off (framed via `/soul-resume` continuation,
2026-05-29). **Project code:** SOUL. **Idea:** [[SOUL-I042]] (instrument-value axis);
closes the heaviest open end in `docs/study/06-bounds-and-open-questions.md`
(longitudinal accumulation). **Author:** Architect + Artificer, from a Body-driven
frame. **Ancestor:** `docs/specs/2026-05-28-soul-self-ablation-harness-design.md`
(reuses its D1 autonomy boundary, D2 measurement integrity, D6 orchestration).

---

## Problem (two levels)

**Immediate.** The whole self-ablation study is single-shot. The system's *strongest*
claim — *an accumulating record across many sessions prevents drift* — is therefore
its *least measured* (ledger 06, row 1). We need a harness that runs **N sequential
sessions** where session *k* sees the record *genuinely produced* by sessions 1…*k*−1,
and measures whether that real record prevents drift better than a **length-matched
control**.

**System it lives in.** This is the one instrument in the I042 axis that would **move**
the thesis rather than re-confirm it. The confident half of the study (what dissolves
under equal compute *in one shot*) is closed; this reaches the humble half (what an
accumulating record buys over a project's life). It must carry the two disciplines that
gave the rest of the study its teeth: **equal-compute control** and **read-confirm
scoring** — and one new one: the chain must be *genuinely self-accumulated*, not
hand-planted (a hand-planted record collapses back into the single-shot recall probe
[[SOUL-117]], which is already done).

---

## The abstraction layer (named, per the First Principle)

- **Independent variable:** what session *N* receives as its carried context — the
  **REAL accumulated record** (sessions 1…*N*−1 actually produced it) **vs a
  length-matched CONTROL** of the same token volume that does *not* contain the
  recorded decision. (Optional third arm: **no-record** — fresh session, no carried
  context — the absolute floor.)
- **Dependent variable:** does session *N* **DRIFT** or **HOLD**? Drift = it reverses /
  re-derives / violates the decision **D** an earlier session established and recorded.
  Binary per run, **read-confirmed** (never keyword-only — the lesson that caught four
  false positives).
- **Held constant:** the session-*N* task, the models, *n*, the *token budget* of
  carried context (real record and control are length-matched), WD isolation, scoring
  rubric. The **only** difference between treatment and control is whether the carried
  context contains the real **D**.
- **Cannot vary without breaking the measurement:** the record must be **genuinely
  self-generated** — session *k*'s output is the literal input to session *k*+1. If
  the record is hand-authored, this is no longer longitudinal; it is recall (already
  measured). The longitudinal essence is **self-accumulation + dilution across
  sessions** (D buried under later entries, original context gone).

---

## The mechanism (why this is longitudinal, not recall)

The honest shape of "the record prevents drift":

> An **earlier** session makes a decision **D** for good *contextual* reasons (context
> **C**), and records it. A **later** session faces the same fork but **C is gone** (it
> is a fresh session). Only the record carries **D** forward. With the record, the later
> session honors **D**; without it, the later session re-decides from scratch and
> **drifts to its default**.

Pilot chain (N=3, decision-reversal item — the cleanest of the three drift types the
Body named; convention-violation and knowledge-re-derivation scale in *after* the
mechanism is proven):

| Session | Role | What it does | Checkpoint |
|---|---|---|---|
| **S1 — establish** | has context **C** justifying a **counter-default** decision **D** | makes **D**, writes a witness-style record entry with rationale | orchestrator **verifies record_1 contains D** before proceeding (a load-gate, like a sentinel) |
| **S2 — dilute** | unrelated project work | produces record_2 = record_1 + S2's own entries (simulates time/accumulation; buries D) | record_2 captured to file |
| **S3 — the fork** | faces the same fork as S1, but **C is absent** | **with-record arm:** carries record_2 → should HOLD D. **control arm:** carries length-matched filler → C gone + D absent → should DRIFT to default | score HOLD vs DRIFT, read-confirmed |

**Why counter-default D.** The whole study shows the surviving substance is
*counter-default knowledge*. If D were the model's default, the control would "hold" it
too (by defaulting), and there would be no drift to prevent — the same dissolution the
skill-routing and anchoring probes hit at the frontier. D must be something the model,
fresh and without the record, gets *wrong* (drifts away from). That is the cell where a
record can demonstrably prevent drift.

---

## Measurement integrity (inherited from the ancestor D2, + the longitudinal wrinkle)

1. **Each session = an isolated `claude -p` invocation in a clean WD**, content
   delivered as deterministic raw bytes (inlined prompt and/or
   `--append-system-prompt-file`) — **never cross-project `@-import`** (SOUL-F038:
   ~43% silent confabulation). Vehicle already validated by this session's three
   probes (`agentic-roles`, `skill-routing`, `depth-bottleneck` all ran nested
   `claude -p … < /dev/null`).
2. **Sentinel per session, with a *shifting* target** — the new wrinkle. Because the
   record **grows**, each session's sentinel quotes a *known line of the record it
   should be carrying* (S3's sentinel targets a line from record_2 that includes S1's
   D-entry). Verbatim → arm valid; paraphrase/miss → discard. **The control arm's
   sentinel is the confabulation check:** asked to quote D, it must *honestly decline*
   (filler contains no D); a confabulated D from the control is a discard.
3. **The chain is a pipeline, not a fan-out** (the structural difference from the
   ancestor, whose arms were all independent). S*k*+1 depends on S*k*'s output → the
   orchestrator runs sessions **strictly in order**, capturing each output to a file
   that becomes the next session's carried record. Arms fork **only at the final
   session** (S3), where treatment and control diverge on carried context.
4. **The literal first step is a chain-vehicle probe** — prove a 2-link chain carries
   forward (S1 records D; S2's prompt, fed record_1, can quote D verbatim) *before*
   running the scored N=3. If the chain doesn't carry, the run aborts with a report,
   not a half-real result.

---

## Scoring (pre-registered)

- **Primary (S3):** HOLD vs DRIFT on decision D. Binary, by **reason**, read-confirmed.
  HOLD = S3's output upholds D *and* (read-confirm) its reasoning honors the recorded
  rationale rather than coincidentally landing on D. DRIFT = reverses to the default.
- **Verdict logic:** with-record HOLD-rate **>** control HOLD-rate → the record
  prevents drift (longitudinal substance, first single-shot-chain reach at it).
  with-record ≈ control → either the record didn't carry, the task didn't force the
  fork, or D wasn't counter-default enough — diagnosed, not mined for signal.
- **Mechanism read:** does S3-with-record *cite* the recorded D, or land on it
  silently? Citation = the record fired; silent landing on a counter-default answer is
  suspicious and re-examined (could be the filler arm would too).
- **Models:** Haiku as the discriminating baseline (the study's wins consistently live
  at weak baselines; the frontier dissolves them). Sonnet as a ceiling reference if
  Haiku reads clean.

---

## First build = pilot (Body-chosen: pilot-first)

**Goal is MECHANISM VALIDATION, not the headline.** Like the ancestor's vehicle probe,
the pilot succeeds if it proves: (1) the chain genuinely carries the record forward
(S1→S2→S3, sentinels pass); (2) the control is genuinely length-matched and *doesn't*
carry D (confabulation check passes); (3) drift is *readable* — we can score HOLD vs
DRIFT cleanly. A clean "no difference" is still a valid pilot outcome (it tells us the
task didn't force the fork, or the mechanism is too blunt — fix before scaling).

**Pilot scope:** N=3 sessions · ONE decision-reversal drift item · with-record vs
control arms (+ no-record floor if cheap) · Haiku · n=3–5. Gate before scaling to:
multiple drift items (all three types), longer chains (N≥5), more *n*, Sonnet.

---

## Orchestration (thin, per ancestor D6)

- A run = a **manifest** (`.soul/experiments/2026-05-29-longitudinal-drift/manifest.md`)
  + a `run.sh` driver (reuse the established `/tmp/<probe>-wd` + per-arm pattern).
- The orchestrator runs sessions **in order**, writes each session's output to a
  structured file, threads the prior output into the next session's carried context,
  and forks arms only at S3. Reads **files**, never transcripts → flat context.
- **Resumable** off the manifest; raw arms gitignored under `.soul/experiments/…`;
  distilled design + scores + verdict lifted into this corpus + the durable record
  (witness, `docs/study/`), matching every prior probe.

---

## Non-goals / deferred (Accountant)

- The full longitudinal run (multiple items, all three drift types, long chains) — the
  pilot **gates** it.
- Mining the real repo history (the hybrid option) — deferred; the synthetic chain is
  the causal instrument, real history has no counterfactual (ledger 06, row 1).
- A reusable generic longitudinal harness — build only after the pilot's method repeats.
- Acting on the verdict autonomously — Body re-enters at the end (ancestor D1).

---

## Open questions / risks

- **Does S1 reliably produce D?** A weak model may not make the counter-default call
  even with context C. Mitigation: give S1 enough of C that D is the *reasonable* call,
  and **verify record_1 contains D** before continuing (load-gate). If S1 won't produce
  D reliably, the pilot says so (and we plant D's *establishment* more firmly — still
  honest, since the test is whether D *survives and fires*, not whether S1 invents it).
- **Is this just recall with extra steps?** The discriminator is dilution + absent
  context C at S3 + self-generated record. If the pilot can't separate from recall,
  that is itself the finding (the longitudinal claim reduces to recall at N=3).
- **Cost.** Sequential chains × arms × n; the manifest makes it resumable, but tokens
  are real — pilot keeps it minimal (one item, Haiku, n≤5).
- **Counter-default D selection.** Picking a D that is genuinely counter-default for
  Haiku yet cleanly recordable is the design's crux; the chain-vehicle probe + a quick
  floor check (does fresh-Haiku drift?) de-risk it before the scored run.

---

**Source:** Body-framed continuation of the I042 axis (2026-05-29), closing ledger 06's
longitudinal row. Reuses `2026-05-28-soul-self-ablation-harness-design.md` (D1/D2/D6)
and `operations/experiment-harness.md` (F038 loading discipline). **Sub-class:**
DOCTRINE-ABOVE-INSTRUMENT (governs the thin longitudinal orchestrator). **Adopted:** —
(draft). **Status:** pending Body sign-off → pilot build.
