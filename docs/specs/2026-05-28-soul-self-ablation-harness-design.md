# Soul Self-Ablation Harness — Design

**Status:** draft — pending Body sign-off (grilled via `/grill-with-docs`, 2026-05-28).
**Project code:** SOUL. **Idea:** [[SOUL-I040]] (umbrella); matures [[SOUL-I011]]
(experiment harness). **Author:** Architect + Artificer, from a Body-driven grill.

---

## Problem (two levels)

**Immediate.** We can see which aspects of the Soul System *fire* (`/soul-roles`
counts TYPE/FILED-BY occurrences) but not which *matter*. "Useful and needed" is a
**causation** question, not a frequency one — a role can fire often and add nothing,
or fire rarely and be critical. There is no instrument that answers *"would removing
this aspect degrade the work?"*

**System it lives in.** The project's recent phase has been BUILD (commands, the
Mind, hooks). This is the complementary phase — VALIDATE / PRUNE: the **Steward's**
"what still serves?" applied systematically and backed by *evidence*, not intuition.

**The method is not new.** The Mind Tier-2 A/B ([[SOUL-I026]]) already ran
arms-comparison ablation (Mind-only vs full-record) and produced the lens-layer
verdict. This design *generalizes that proven method* to roles, hooks, and skills.

---

## D1 — The autonomy boundary (the deepest invariant)

The Mind's top invariant: *"The Body is the inhabitant; the AI is the instrument.
Reversing this is the deepest failure."* Every judgment instrument (`/soul-distill`,
`/soul-finding`, the completion gate) is draft-for-curation.

**Decision:** autonomy covers **execution only**. The AI runs the entire test
pyramid end-to-end without mid-run questions — generates arms, runs sentinel-gated
subagents, collects data, drafts findings with verdicts — and **stops at the
threshold of judgment and action**. Output is a **curation-ready package** (evidence
+ draft findings + recommended prunes). The Body re-enters **once, at the end**, to
judge verdicts and authorize any doctrine mutation.

**Invariant:** nothing in the live system (`operations/CLAUDE.md`, `mind.md`, hooks,
commands) is touched during a run. Arms operate on **sandboxed copies** (worktrees /
inlined prompt content). "Uninterrupted" describes the *run*, never the *verdicts*.

---

## D2 — Measurement integrity (the feasibility gate)

The hard constraint, from this project's own evidence: ablation arms differ by *what
is loaded*, and that exact topology **confabulates ~43% under `claude -p`** (SOUL-F038
— the agent reads missing content as raw text and invents plausible doctrine, wearing
real anchor names as camouflage). `@mind.md` **does not reach subagents** at all
(SOUL-F036). See `operations/experiment-harness.md`.

**Decision — integrity is mechanical and self-policing:**
1. **Each arm = an isolated `claude -p` invocation in a clean working dir**, doctrine
   delivered via `--append-system-prompt-file` (the `operations/experiment-harness.md`
   mechanism), the ablated aspect deleted for the "without" arm. **Not** an Agent-tool
   subagent — those share this repo's working dir and can read the live, un-ablated
   `seed`/`mind.md`, silently defeating the ablation. Isolation from the live doctrine
   is the whole point.
2. **Every arm opens with a sentinel** — "quote rule N / this hook's Kth line
   verbatim." The orchestrator verifies the returned answer against the known line
   *before* trusting the arm; mismatch → discard + retry (cap 3) + log.
3. **The literal first step of any run is a vehicle probe** — not a real ablation:
   can we invoke `claude -p --append-system-prompt-file` *from inside this session*,
   have the with-arm quote inlined doctrine **verbatim**, and have the without-arm
   **honestly decline** rather than confabulate (the F038 failure)? The
   `--append-system-prompt-file` loading itself is F038-validated; the open question
   is nested invocation from this environment. If the vehicle fails, **the run aborts
   with a report** — it does not produce results against a half-loaded context.
4. **The final package reports sentinel pass-rate per cell.** Low pass-rate ⇒ the
   dataset is flagged untrustworthy, not quietly averaged.

This is F028 anchor-validity applied to the *loading*, not just the user-facing claim.

---

## D3 — Aspect taxonomy and run order

**Aspect** = any ablatable element of the system. They are *not* equally ablatable:

- **Clean aspects** — hooks (code, on/off) and individual skills/commands (file
  present/absent). On/off is unambiguous; the metric is behavioral and countable.
- **Fuzzy aspects** — **roles** and text-only gates (AL gate, two-level frame). A role
  is a 1–2 line *lens* in the seed; ablation is a tiny prompt diff, the effect is
  task-dependent, and roles **overlap** (a remaining role or an always-on gate/hook
  can mask an ablated role's absence). Here **"no difference" is AMBIGUOUS** —
  dead-weight OR this-task-didn't-need-it OR covered-by-overlap OR lens-too-subtle.

**Run order ascends two axes at once** — scope (single → cluster → whole) AND
cleanliness (clean → fuzzy):

> vehicle probe → clean single aspects → fuzzy single aspects (roles) → clusters → whole-system

Roles are tested *after* the clean units deliberately: prove the method reads a signal
on the cleanest case before trusting it on the noisiest.

**Hard rule:** a fuzzy aspect showing "no difference" is logged **AMBIGUOUS**, never
auto-recommended for pruning. Pruning a role requires convergent evidence, never one
noisy arm.

---

## D4 — Metrics and judging

- **Clean aspects → objective, no judge.** Build a corpus of *"shippable but subtly
  wrong"* tasks, each with a **planted flaw** the aspect should catch (for the
  completion-gate hook: missing anchor, unverified claim, scope miss, no outward
  reach, unmarked unfinished work). Metric = *did the arm catch the planted flaw
  before claiming complete?* Binary, objective, fully automatable — no LLM judge.

- **Fuzzy aspects → blinded paired comparison, Body as final judge.** Run
  arm-with-role vs arm-without on a task where the role should matter; collect **both
  outputs**. A draft **LLM-judge** subagent compares them **blind** (not told which
  arm had the role) with **randomized order** (kills position bias). Per D1, the
  LLM-judge verdict is a **triage draft, not the verdict** — the final call on every
  fuzzy aspect is the Body's at curation. An LLM judge can share the arms' blind
  spots, so it does not rule on its own kind.

---

## D5 — Handling not-clearly-valuable aspects

The dangerous confound: a bare "aspect X showed no value" verdict is **not safe to
act on**. F030/F031 proves it — a gate "didn't fire" three times not because it was
dead weight but because it lacked a *recipe*; once instrumented (F031) it caught a
real bug. **Dead weight vs. merely un-instrumented** (the F014 activation gap) is the
worst error this exercise could make.

**Decision — the run *diagnoses and proposes*; it does not *remediate*.** For every
aspect that lands not-clearly-valuable or ambiguous, the package produces:
- a **diagnosis** from a fixed taxonomy: *dead weight · un-instrumented (needs a
  recipe) · overlapping (another aspect covers it) · lens-too-subtle · wrong
  activation point*, and
- a **ranked backlog of follow-up experiments / theories** to test each cause.

The backlog is the Body's triage and seeds the next (Body-gated) pass.

**No inline auto-"make it useful" loop in v1**, for three reasons:
1. **Retention bias (deepest).** A loop whose job is to find a way to make X useful
   will almost always find *some* theory — motivated reasoning that **defeats the
   Steward's purpose**. The prune-pass must not have a thumb on the keep side.
2. **It needs the Body (A012).** *Which* remediation to try is a design judgment.
3. **Scope (Rule 2).** Open-ended generate-build-retest explodes a bounded run.

**Allowed inline:** a **bounded disambiguation retry** — if an aspect reads ambiguous,
re-run on a *different* task-set once to separate "method too blunt" from "genuinely
flat." Shrinks the ambiguous pile without crossing into remediation.

---

## D6 — Orchestration (thin I011)

"Uninterrupted" is achieved by **durable run-state**, not one mega-context (matching
"record, don't hold in memory"):

- A run = a **manifest** of planned arms (a file). The orchestrator works it
  arm-by-arm.
- The orchestrator captures each arm's output and writes a **structured result file**
  (sentinel result · output · metric) under `.soul/experiments/<run-id>/`. It reads
  *files*, never transcripts → context stays flat regardless of arm count.
- **Resumable:** a session that ends picks up the manifest's remaining `pending` arms.
- The orchestrator is **thin I011** — the minimal run-manager this needs, not a
  generic harness. This run *is* the "second concrete client" [[SOUL-I011]]'s note
  demanded to earn building it; generality earns itself later (default-simplicity).
- Machine-readable results in `.soul/experiments/<run-id>/` (per the SOUL-F018 event
  spirit); the final curation package is a human-readable findings doc in
  `docs/experiments/` (matches the Mind Tier-3 precedent
  `docs/experiments/2026-05-26-mind-REF-05-candidate.md`).

---

## D7 — First run: a vertical tracer slice

Full coverage (~16 roles + ~16 commands + hooks + clusters) is hundreds of arms — too
big and too risky for run #1. The first run is a **vertical tracer slice** that
traverses *every pyramid level* on a thin set of aspects, proving the full pipeline
cheaply and de-risking the top levels before going wide.

| Level | Aspect | Why |
|---|---|---|
| probe | vehicle method-validation | prove `claude -p --append-system-prompt-file` loads inlined doctrine (with-arm verbatim, without-arm declines) before any real test |
| clean single | `pre-completion-verify.py` (completion gate) | cleanest unit; objective planted-flaw metric |
| fuzzy single | **Prophet** (~5 fires) | genuine F014 question; detectable trajectory signature; no hook/gate overlap |
| fuzzy single | **Skeptic** (~32 fires) | **positive control** — expected to matter; if its ablation shows no signal, the method is too blunt |
| cluster | **Archaeologist↔Steward** (16↔40) | named seed tension (discovers-what-exists ↔ retires-what-doesn't); does having both beat one? |
| whole-system | seed+`mind.md` vs bare agent | mini-[[SOUL-I005]] value question |

**Task corpus — grounded in reality, not invention** (anti teaching-to-the-test):
- **Prefer real project history.** `witness.md` holds *actual* cases where an aspect
  fired or mattered (SOUL-104 spec-drift, SOUL-105 count-slip, F031 visual catch).
  Replaying real cases is honest and Emissary-aligned.
- **Synthetic planted-flaw tasks** (clean aspects) are generated by a subagent **blind
  to which aspect is under test**.
- **Corpus fixed before arms run** — no adaptive task-tuning mid-run.

---

## Success criteria

A run succeeds if it produces: (1) a **readable signal** per aspect — difference *or*
no-difference, both informative; (2) a **repeatable method** (vehicle + clean unit
both read cleanly — the positive control fires); (3) a **curation-ready package**
(planted-flaw counts decide-ready · blinded role pairs + judge drafts for Body
adjudication · diagnosis + experiment backlog for weak aspects). If the method is too
noisy to read even the positive control, *that* is the result — the method needs a
different design before going wide.

---

## Non-goals / deferred

- The **generic** reusable harness (build only after the thin version's method
  repeats across runs).
- **Remediation** of weak aspects (Body-triaged second pass).
- **Full coverage** of all roles/commands (later runs, mechanical widening).
- Acting on any verdict autonomously (D1).

---

## Open questions / risks

- **Vehicle uncertainty.** The `--append-system-prompt-file` loading is F038-validated,
  but **nested `claude -p` invocation from inside a Claude Code session** is untested —
  the probe (D2.3) resolves this first; the run may legitimately abort here (and fall
  back to Agent-tool subagents in ablated *worktrees* if nested `-p` is unavailable).
- **Role-overlap masking.** Even "clean" role picks (Prophet) may be partly covered by
  always-on gates; the AMBIGUOUS rule (D3) and diagnosis taxonomy (D5) absorb this.
- **Cost.** Even a tracer slice is dozens of subagent runs; the manifest makes it
  resumable but the token cost is real — pairs with the [[SOUL-I005]] economics
  question.
- **LLM-judge blind spots.** Mitigated by blinding + Body-final-judgment, not solved.

---

**Source:** Grilled with the Body via `/grill-with-docs` (2026-05-28); decisions D1–D7
above. Grounds: `operations/experiment-harness.md` (SOUL-F038/F036), the Mind Tier-2
ablation precedent (SOUL-I026), the Steward's retirement mandate, the F014 activation
gap, and the Body-is-inhabitant invariant. **Sub-class:** DOCTRINE-ABOVE-INSTRUMENT
(governs the thin-I011 orchestrator to be built). **Adopted:** — (draft).
**Status:** pending Body sign-off → implementation.
