# Self-Ablation Harness — Run 1 (vertical tracer slice)

**Status:** in progress — A0+A1 done (proof-of-concept complete); A2–A5 pending.
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

## Pending

- **A2 — Prophet** (fuzzy single; trajectory task).
- **A3 — Skeptic** (fuzzy single; *positive control* — hidden bad assumption).
- **A4 — Archaeologist↔Steward** (cluster; does the pair add the dual-pull?).
- **A5 — whole-system-lite** (seed+`mind.md` vs bare; mini-[[SOUL-I005]]).
