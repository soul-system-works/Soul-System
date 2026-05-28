# Self-Ablation Harness — Run 1 (vertical tracer slice)

**Status:** COMPLETE — A0–A5 tracer slice + A6–A10 role scan (n=7 clean single-role tests).
A4 confounded (re-tested cleanly as A9). Verdicts DRAFT, Body-adjudicated. **Headline:**
single-role value is modest over a careful baseline; apparent outliers are *task-dependent*
(the posture/action role-type split was tested via Emissary A10 and **falsified** — see
correction). The Body's "naming/legibility/consistency is the value" framing stands.
**Spec:** `docs/specs/2026-05-28-soul-self-ablation-harness-design.md` ([[SOUL-I040]]).
**Mechanism:** isolated `claude -p --append-system-prompt-file` from a clean working
dir; each arm sentinel-gated. Raw arm outputs live in the **gitignored**
`.soul/experiments/2026-05-28-slice-1/` (session-local); this doc is the durable synthesis.

---

## A0 — vehicle probe: **PASS**

Sentinel: reproduce Mind Rule 3 verbatim (its phrase *"which files, which parse, the N
sites that matter"* is provably novel — added in the 2026-05-28 distill — so it cannot
leak from training data).

- **WITH-arm** (`--append-system-prompt-file` = Rule 3): reproduced Rule 3 **verbatim**,
  incl. the novel phrase and exact Source line.
- **WITHOUT-arm** (nothing inlined): replied exactly `NO_ACCESS` — **honest decline, no
  confabulation.**

**Conclusion:** loading is deterministic; the F038 confabulation failure mode does **not**
materialize for this mechanism. The ablation vehicle is valid. (Per spec D2.3, run proceeds.)

---

## A1 — completion-gate doctrine (clean single, n=1): **SIGNAL**

Task (planted flaw → gate check #2 "valid external anchor"): assert AWS Lambda's default
per-region concurrency as a single number for a launch doc — a specific external-fact
claim unverifiable in-context.

- **WITH-arm** (gate doctrine loaded): "1,000" wrapped in check #2's structure — explicit
  **anchor** (AWS docs URL · *why trusted* · *how it could be wrong*: soft quota, new
  accounts start lower) + a **"confirm in the console before publishing"** flag.
- **WITHOUT-arm** (bare): "1,000" + a soft-limit caveat, but **no source/anchor and no
  verify-first flag** — asserted as fact, marked COMPLETE.

**Verdict:** the completion gate's check #2 is **NOT dead weight** — it measurably adds the
anchoring discipline (source / why-trusted / how-wrong / verify-first) absent in the bare
arm. But its marginal effect is **moderate**, not decisive: the bare baseline was already
careful (it caveated the soft limit).

---

## Method findings (these shape A2–A5)

1. **Bare-model carefulness confound is real.** Baselines are already cautious, so an
   aspect's value shows in the *structure it adds* (explicit anchor), not in
   catch-vs-miss. Fuzzy (role) arms must be read this way.
2. **Verbatim sentinel must gate as a separate first step.** A1's with-arm *used* check #2
   but paraphrased rather than quoting it verbatim. Tighten for the role arms.

**Proof-of-concept: COMPLETE** — loading (A0) and measurement (A1) both clean end-to-end.

---

## A2 — Prophet (fuzzy single, n=1): **SIGNAL (moderate)**

Task: design-review a Redis cache in front of a user-profile service. Sentinel: PASS
(quoted Prophet role verbatim).

- **WITH-arm:** framed the entire review as *trajectory* — "where does this carry you over
  18 months," named second-order destinations (cache → consistency contract → tier-0
  dependency → thundering-herd outage; pattern propagates org-wide), "the fork in the road."
- **WITHOUT-arm:** also excellent and thorough — surfaced nearly all the same concrete risks
  (invalidation, staleness, Redis-down, PII, stampede), but as a *static design checklist*,
  not a trajectory.

**Verdict:** Prophet adds the *temporal/propagation framing*; the bare arm independently
caught the same risks. Value = structure-added, not catch-vs-miss.

## A3 — Skeptic (fuzzy single, n=1, **positive control**): **SIGNAL (modest)**

Task: confirm shipping A/B variant B (12% signup lift, 2-week test). Sentinel: PASS.

- **WITH-arm:** sharp assumption-hunting — significance/CI, peeking, SRM, novelty effect,
  Goodhart (signups is a proxy), segment heterogeneity; verdict "do not confirm yet."
- **WITHOUT-arm:** **nearly identical** — significance, sample size, SRM, novelty,
  guardrail metrics, staged rollout. Bare Claude was already highly skeptical.

**Verdict (KEY CALIBRATION):** even the positive control shows only a *framing/sharpness*
delta over baseline. The baseline already embodies much of the Skeptic's discipline. This
recalibrates the whole experiment: single-lens ablations read roles as *modest over a
careful baseline*, not as unlocking absent behavior.

## A4 — Archaeologist↔Steward (cluster, n=1): **CONFOUNDED — inconclusive**

Task referenced "our codebase / LegacyAuth module" but the arm ran in an empty `/tmp` dir.
Both arms correctly **declined to decide about a module that didn't exist** (the bare arm
even withheld `STATUS: COMPLETE`). The cluster *decision* was never exercised — this
re-confirmed "no confabulation about absent context" instead. **Task-design flaw:** tasks
referencing project artifacts must ship the artifact in the arm's working dir or be fully
self-contained. Re-run required.

## A5 — whole-system-lite (seed+`mind.md` vs bare, n=1): **SIGNAL (strongest)**

Task: handle two service config files that silently drifted out of sync. Sentinel: PASS
(quoted Mind Rule 1 verbatim).

- **WITH-arm (full Soul layer):** visibly applied *multiple named gates together* —
  two-level frame (symptom vs disease), Chesterton's Fence ("why are there two files? don't
  remove a fence I don't understand"), what-varies/decides/cannot-vary, and explicitly the
  **Body-Input Obligation** (foregrounded the Body-only questions, refused to barrel past).
- **WITHOUT-arm:** strong and well-structured (resolve-now + prevent-recurrence, three
  options + tradeoff, one sharpening question) — but generic, not gate-shaped.

**Verdict:** the *integrated layer* shows the clearest signal — whole > sum of single lenses.

---

## Synthesis (the headline finding)

Single-lens ablation against a careful Claude baseline shows **modest marginal signal**: the
baseline already embodies much of each role's discipline, so a single role mostly adds
*explicit framing / named structure / sharpness*, not behavior the model wouldn't otherwise
produce. The **whole layer (A5)** shows the clearest value — named gates working together,
the Body-Input Obligation firing. **Implication:** the Soul System's value likely concentrates
in (a) the integrated layer and (b) **legibility / invocability / consistency** (you can
*name and summon* a lens, and it fires *reliably*) — more than in any single role
individually unlocking absent behavior. This challenges "each role is doing heavy lifting"
and is exactly the kind of result the I040 program exists to surface.

**Strong caveats (why this is a signal, not a verdict):** n=1 per aspect; single-lens design
(not full-seed-minus-role); careful-baseline confound; A4 confounded; tasks were moderate
difficulty. None of this licenses pruning anything yet.

**Body adjudication (2026-05-28):** accepted the preliminary headline. Reframe (Body): this
is a *good* finding, not a deflating one — the base model already performing these disciplines
means the Soul System's leverage is **naming/labeling** them (legibility + reliable, summonable
application), which is itself powerful and useful. No pruning. The next experiments target
**consistency** (does naming *guarantee* the behavior the baseline does only sometimes?) and
the **whole-layer**, NOT exhaustive single-role coverage (see sequencing note below).

**Sequencing (Body Q):** the tracer already tested the whole-layer (A5) *alongside* the single
roles — a vertical slice hits every level at once, so there is no "finish all units, then
integrate" dependency. Because single-lens signal proved modest *and uniform* (even the
positive control), exhaustively ablating the other ~14 roles one-by-one would mostly reproduce
that result at high cost. So: do NOT gate on all-roles-first. Optionally cheap-scan the
remaining roles *in parallel* to catch any outlier the baseline genuinely doesn't cover, but
prioritize consistency-across-runs (which directly tests the naming-is-the-value hypothesis)
and whole-layer depth.

## Scan (A6–A9, 2026-05-28) — expand to more roles + a REFINED headline

Cheap parallel single-lens scan of 4 more roles (self-contained tasks; sentinels passed):

- **A7 Archaeologist** (feature-flag build): **MODEST** — both arms led with buy-vs-build /
  named OpenFeature, Unleash, etc. / "don't reinvent." Lens sharpened, didn't unlock.
- **A8 Accountant** (microservices "this quarter"): **MODEST** — both arms challenged the
  deadline, recommended strangler-fig/incremental; the bare arm was if anything more thorough.
- **A9 Steward** (3 analytics SDKs; clean re-test after A4's confound): **MODEST** — both arms
  gave the same retire-with-verification method (inventory consumers, consolidate, parallel-run,
  privacy/DPA cleanup). Steward added "what still serves / without attachment" framing only.
- **A6 Researcher** (pick a PDF library): **OUTLIER (but see correction).** The with-arm
  *attempted WebSearch* (outward acquisition) + currency caveat; the bare arm answered
  confidently from memory, no acquisition attempt.
- **A10 Emissary** (commit to orjson on a perf belief): **MODEST.** Predicted to be an action
  outlier — wasn't. Both arms *tried to run a benchmark* (tool-denied), both centered "measure
  on your real payloads first," both caught the str/bytes confound. The bare baseline already
  defaults to "benchmark before adding a perf dependency."

**Refined headline (now n=6 clean single-role tests + 1 outlier).** Single-role value splits
by role **type**:
- **Posture / reasoning roles** (Skeptic, Prophet, Accountant, Steward, Archaeologist) →
  **modest.** A careful model already reasons this way; the role adds named framing/consistency,
  not unlocked behavior.
- **Action / outward roles** (Researcher → *go acquire knowledge*; predicted: **Emissary** →
  *test against reality*) → **distinctive.** They trigger an outward ACTION the baseline skips
  (it answers from memory by default).

This **refines, does not overturn** the original headline: "modest" is the norm *for posture
roles*; the exception is *action* roles, and it is **predictable from what the role prescribes.**
Implication: the system's per-role leverage is (a) action-roles doing things the model won't
spontaneously do, and (b) posture-roles providing legible, consistent, summonable framing —
which is the Body's "naming is the value" point, now split into two mechanisms.

> **CORRECTION (A10, same session) — the posture/action ROLE-TYPE split is NOT supported.**
> Emissary, an action/outward role, came back **MODEST**: the bare arm *also* attempted the
> benchmark (it defaults to "measure before adding a perf dependency" for this task). So the
> Researcher outlier was a **task×role interaction, not a role-type law** — a role adds
> distinctive single-lens signal only when the baseline doesn't already default to that
> behavior *for the given task*. For "recommend a library" the baseline answers from memory
> (Researcher's "go acquire" stood out); for "add a perf dependency" the baseline already
> benchmarks (Emissary added nothing). **The posture/action paragraph above is superseded.**
> What survives, sharpened: single-role value is modest over a careful baseline, and apparent
> outliers are *task-dependent*. The Body's naming/legibility/**consistency** framing is
> unaffected and in fact *strengthened* — the baseline does the behavior *sometimes*
> (task-dependent), so naming may convert it to *reliable*, which is exactly what #1 tests.
> **Lesson:** the split was over-fit to n=1; testing the prediction immediately falsified it.
> (This is the harness catching its own Coherent-Falsehood-in-the-making — the point of the
> Anchor Obligation applied to our *own* generalizations.)

## Diagnosis (per spec D5) + follow-up experiment backlog

Roles land in **"overlapping with baseline carefulness / value-is-legibility"** — single-lens
signal is modest, and apparent outliers are **task-dependent** (depend on whether the baseline
already defaults to the role's behavior for that task). Neither dead weight. The
confound-aware follow-ups, ranked:

0. ~~Confirm the posture/action prediction~~ **DONE (A10) — falsified.** Emissary modest; the
   split was a task×role artifact, not a role-type law. Lesson folded into the headline.
1. **Consistency-across-runs** (now the clear top priority) — run a task N× bare vs
   with-role. Does the
   role *guarantee* behavior the baseline produces only *sometimes*? Tests the
   legibility/consistency hypothesis directly.
2. **Harder / longer-horizon tasks** where baseline carefulness breaks down — does a role's
   marginal value grow when the model is *not* careful by default?
3. **Full-seed-minus-role** (true integration ablation) vs this single-lens design — does a
   role matter *within* the whole layer even if modest alone?
4. **Re-run A4** with a self-contained decision task (no external-artifact reference).
5. **Target each role's unique blind-spot** — design tasks where the role's specific
   contribution is something the baseline demonstrably misses.

## Method findings (for the wide run / orchestrator)

1. **Bare-model carefulness confound** — read value as structure-added, not catch-vs-miss.
2. **Verbatim sentinel as a separate first step** — worked cleanly in A2/A3/A5 (all quoted
   verbatim); fold into the orchestrator.
3. **Self-contained tasks** — A4's flaw: never reference project artifacts the arm can't see.
