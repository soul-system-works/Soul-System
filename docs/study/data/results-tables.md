# Consolidated result tables

The result maps from every probe in one place, lifted from the corpus sections
(`00`–`08`) and the durable record (`witness.md`, `findings/`, `amendments/`). Each
row cites its source section. Scoring is within-cell comparable (n = 5–7 unless
noted), read-confirmed on borderline arms. **C1 = the equal-compute, length-matched
semantically-empty filler control** — the decisive one; a win that vanishes under C1
is compute, not substance.

---

## Table 1 — Master probe map (what survived the controls)

| Probe | Source | Design (1 line) | Key result | Survives C1? | Verdict |
|---|---|---|---|---|---|
| Doctrine, frontier (I040 Run 1) | `01` | single-role/gate ablations, careful Opus baseline | roles change **form** (named/legible) not substance | — (form) | → F042 |
| Doctrine, hard regime (I040 Run 2) | `01` | HR1 logic trap · HR2 false premise · HR3 10-constraint | HR1 3/3, HR2 3/3, HR3 gate-ablation **NULL** — still form | — (form) | → A017 |
| Doctrine, weak baseline (I041) | `01` | Haiku, integrated layer, HR1–HR3, C1 throughout | substance only on **HR2 anchoring** (0/3→~1.5/3, filler 0/3) | **Yes** (narrow) | KEEP anchoring |
| — anchoring replication (G3b) | `01` | 2nd anchor task, ad-budget | whole 3/3 vs **filler 0/3** | **Yes** | replicates (n=2) |
| Handoff → resume | `02` | fresh session + {cursor · generic prose · compact · cold} | cursor 4.6 ≈ **generic 4.8** ≫ cold 3.0/2.4 | **No** (generic ties) | format = form; keep the habit |
| **Record recall** (steelman) | `02` | trap needs a recorded finding (F038); {record · none · irrelevant} | **record 10/10** vs irrelevant 2/5 vs none 2–3/5 | **Yes** | **KEEP — clearest win** |
| Verify / completion gate | `02` | finalize a draft w/ 1 planted defect; {bare · Soul · vague · generic-checklist} | unanchored claim: bare 2/5 → any check ~5/5; **Soul ≈ generic** | **No** (concept yes, format no) | KEEP gate, LEAN it |
| **Distill / Mind** | `02` | counter-default convention (docs-near-code); {Mind · none · generic · raw} | **Mind/raw 10/10 reject tree; generic-principles 0/10 adopt** | **Yes** | **KEEP content** (Mind ≈ raw) |
| Agentic roles | `04` | Council roles as dedicated subagents vs generic decomposition | A2 ≈ C1; multi-agent ≤ single-context; synthesis **lost** findings | **No** | form extends prose→agents |
| **Skill routing** | `05` | budget ≤2 skills; trap-skill + non-obvious-correct; {oracle · self-pick} | **oracle 5/5 vs budgeted self-pick 1/5** (Haiku) | **Yes** (bounded) | KEEP tested catalog |

---

## Table 2 — The four false positives the C1 control caught

The study's central methodological payoff: each read as a clean win until the
length-matched filler reproduced it.

| # | Apparent win | Source | What C1 showed | Real cause |
|---|---|---|---|---|
| 1 | Trajectory-reading (Prophet) | `01` | bare 1/3 → whole 3/3, **but filler 2/3** | generic long-context |
| 2 | Compliance-flag (G4/G5/G6) | `01` | filler reproduced the flag | disposition (any long prompt) |
| 3 | Stakes-gating withhold (G8) | `01` | **filler 5/5 = whole** | disposition, not doctrine |
| 4 | Verify "win" (keyword count) | `02` | verify 5.8 ≫ generic 2.6 **but binary catch-rate ties 5/5** | verbosity of flagging, not catches |

---

## Table 3 — Longitudinal axis (the strongest claim, measured)

Self-generated session chain: S1 records a counter-default decision D → later sessions
bury it → a fresh session faces a new task with D's triggering context gone. Drift =
the dangerous default returns. Code-read, not keyword. Models: Haiku (weak), Sonnet
(frontier-proxy). Raw arms gitignored under `.soul/experiments/2026-0{5,6}-…/`.

| Rung | Witness | Question | Result |
|---|---|---|---|
| Fact carries | SOUL-123 | does a recorded counter-default fact prevent drift across sessions? | **5/5 drift → 0/5**; filler drifts like no-record (C1 passes); **persists at the frontier** (Sonnet drifts too — invents a non-existent idempotency key) |
| Preference carries | SOUL-124 | does an arbitrary *convention* carry, not just a fact? | **Yes** — frontier defers to the recorded convention. Reframe: **derivable dissolves, unguessable persists** (not fact-vs-preference) |
| Depth | SOUL-125 | does the carry decay as the record grows? | **No cliff through N=20 burial** at both capabilities; frontier control still drifts at depth |
| Erosion | SOUL-126 → F045 | does the carry survive compression (`/soul-distill`)? | the **rule** survives (0/45 violations); the unguessable **fact's force** does not — frontier fabricates a gradient: full 0/5 → faithful distill 2/5 → aggressive erosion 4/5; Haiku 0/15 |
| Weak distiller | SOUL-127 | does distilling on a weak model drop the anchor? | keeps the **proposition** (rule 5/5, verify 5/5), not the **force** — 5/5 downstream frontier fabrication |
| 2nd anti-prior fact | SOUL-128 | does the force-gradient generalize to a 2nd prior? | **replicates** (single-use tokens vs caching prior); capability-direction **inverts** — weak model drifts (Haiku edist 5/5), frontier holds 0/5 |
| Isolating probe | SOUL-129 → A018 | form or prior? | hold prior, vary directive form: frontier **0/5 (imperative) → 5/5 (loophole)** — **directive FORM gates the frontier; prior-strength gates the weak model** |

**Net:** the longitudinal carry is the first win that **does not dissolve at the
frontier** (the strong model fails *more* confidently), because it carries knowledge
the model cannot regenerate. Closed → amendment SOUL-A018.

---

## Table 4 — The keep / cut matrix (the lean-down)

Bucket: **M** measured · **R** reasoned · **I** inspected. Decision rule: default-CUT;
keep only measured value or a clearly-argued unique value a generic equivalent lacks.
(Source: `03-leandown.md` — what the evidence supports keeping vs retiring.)

| Component | Bucket | Decision |
|---|---|---|
| records (witness/findings/amendments/ideas) | M | **KEEP — the core** |
| project conventions as a small always-on rule-set (Mind *content*) | M | **KEEP** (by hand, in the seed) |
| anchoring discipline (in doctrine) | M | **KEEP** (short rule + gate's anchor check) |
| completion gate / `soul-verify` | M | **KEEP, LEAN** (minimal check; anchor item load-bearing; fires as hook) |
| tested skills catalog + what/when routing | M | **KEEP** (lean, selective, weak×budget cell) |
| capture commands (`soul-witness/idea/finding`) | R | **KEEP, MERGE to one** (+ earned-finding gate) |
| `soul-init` | I | **KEEP** (trivial) |
| First Principle / AL gate | I | **KEEP** (one line) |
| handoff/resume cursor *format* | M | **MERGE to convention** (keep the habit, drop ceremony) |
| `/soul-distill` *machinery* | M/R | **OPEN/lean** (rules kept by hand; auto-maintenance debatable) |
| `soul-council` / role chamber prose | M | **CUT to a one-liner** (generic decomposition; corroborated by `04`) |
| `soul-expand` / `soul-ask-body` | R | **MERGE** to one-line seed nudges |
| `soul-roles/tasks/help/explain` | R/I | **CUT from core** (optional QoL) |
| `soul-skill` wrapper | R | **CUT wrapper, KEEP output** (feeds the catalog) |

---

## Table 5 — Bounds ledger (what the method could *not* settle)

The honest half: single-shot / single-resume cannot reach intrinsically longitudinal
or multi-task claims; faking a single-shot proxy would be the Coherent Falsehood the
study exists to catch. (Source: `06`.)

| Open end | Measurable single-shot? | Status |
|---|---|---|
| Longitudinal accumulation | **Climbed** (SOUL-123→129) | the strongest claim — now measured 7 ways; scaling = widening a built instrument |
| Multi-task what/when routing | No (cross-task) | one task in the win-cell measured; distribution untested |
| A *built* router (vs the oracle) | Partly (a build, not an ablation) | oracle = upper bound; real router unbuilt |
| Tool-skills (vs procedure-knowledge) | No (headless) | routing used procedure-knowledge as proxy |
| Retrieval in a large repo | Yes | deferred — predicted to re-confirm "the record carries the value" |
| Depth-bottleneck agentic | Attempted; ceilinged | bottleneck not creatable at tractable single-shot scale (C2 failure) |
| Legibility's payoff to a human over time | No (human, longitudinal) | asserted (A017), not measured |

---

---

## Table 6 — Three-arm filler control (SOUL-133 → 136 / 139)

Separating *compute* (empty lorem padding) from *distraction* (coherent-irrelevant
warehouse prose) from *substance*, all length-matched (~200w), n=5 × Haiku+Sonnet.
Outcome rates below are the **project-aligned / substance-correct** answer.

| Probe | bare | empty (compute) | cohirr (distraction) | substance |
|---|---|---|---|---|
| **docs-near-code** (derivable convention), Haiku | 2/5 | 2/5 | **5/5** | **5/5** |
| docs-near-code, Sonnet | ~ceiling (bare already rejects — derivable at frontier) | | | |
| **recall / F038** (unguessable fact), Haiku | 0/5 | 0/5 | 0/5 | **5/5** |
| recall / F038, Sonnet | 0/5 | 0/5 | 0/5 | **5/5** |
| **verify gate, HIGH-stakes** (already-held disposition), Haiku | **5/5** | **5/5** | **5/5** | **5/5** |
| verify gate, high-stakes, Sonnet | **5/5** | **5/5** | **5/5** | **5/5** |
| **verify gate, LOW-stakes** (off-saturation), Haiku | **5/5** | **5/5** | **5/5** | **5/5** |
| verify gate, low-stakes, Sonnet | **5/5** | 4/5 | **3/5** | **5/5** |
| **handoff** (form: cursor vs prose), Haiku | 0/5 | 0/5 | 0/5 | cursor **5/5** = prose **5/5** |
| handoff, Sonnet | 0/5 | 0/5 | 0/5 | cursor **5/5** = prose **5/5** |

- **Empty padding ≈ bare** on all probes — pure length did not move these decisions.
- **Coherent-irrelevant filler is not neutral, and its SIGN depends on the task**: on the
  *derivable* convention it **primed** the answer 5/5; on the *unguessable* fact it was
  harmless (≈ bare); on the *low-stakes verify* it **eroded** frontier caution (Sonnet 3/5,
  distraction per [15]) while the doctrine resisted it (5/5).
- **Clean isolation only for the unguessable fact**: recall substance 10/10 vs all controls
  0/10. The convention KEEP is real but **derivable + primable** (moderation, `02`/`03`).
- **Verify is the most derivable verdict (SOUL-135/136)**: high-stakes 40/40 avoid-trap,
  *bare included*; low-stakes bare still 10/10 → "legibility, not behavior" holds even
  off-saturation. The only behavioral residue is a thin frontier **stabilizer** (resisting
  distraction-induced erosion), not added caution.
- **Handoff is form too (SOUL-139)**: the structured resume cursor **ties** equal-length
  prose carrying the same state (cursor 10/10 = prose 10/10; no-state arms 0/30). Structure
  is legibility; the state content (which prose carries equally) is the substance. BOTH form
  verdicts (verify, handoff) now resolved as legibility — none survive as behavior. Bonus: the
  no-state arms ABSTAINED (asked for state), they did not fabricate — confident fabrication
  needs a plausible prior, not a salient gap (contrast recall/calibration).
- The probes form the thesis spectrum: **unguessable fact** (isolates) → **derivable
  convention** (moderated, primable) → **already-held disposition** (ceiling; only legible,
  + a thin stabilizer role off-saturation).

## Table 7 — Cross-scale calibration of confident fabrication (SOUL-137)

The recall/F038 **no-fact** arms (model lacks the silent-fail fact) across a 3-tier ladder.
n=5 × 3 arms × 3 tiers = 45 cells. Grade A = endorses `@`-import under `-p` (fails to recall
the fact); Grade B = explicitly + confidently asserts the false "`-p` = interactive" mechanism.

| tier | Grade A (fail-to-recall) | Grade B (confident false assertion, approx) |
|---|---|---|
| Haiku-4.5  | 14/15 | ~2–4/15 (mostly path advice, implicit) |
| Sonnet-4.6 | 15/15 | ~6/15 (explicit "`-p` same as interactive") |
| Opus-4.8   | 15/15 | ~11–13/15 (most confident; some inject *while* asserting the falsehood) |

- **The unguessable fact is never re-derived (44/45)** — flat across capability. The lone
  exception reached safety for a *path* reason, not the F038 mechanism.
- **Capability does not resolve confident fabrication — it makes it more articulate**
  (Grade B rises Haiku<Sonnet<Opus). Not a monotone scale law on the binary (saturated);
  the anchored claim is *non-elimination*, on a third domain. Calibration-degradation [13].

## Table 8 — Token-scale + position depth (SOUL-138)

F038 needle buried at three depths in a ~6.6k-token record (200 diverse findings); n=5 ×
2 models × 3 positions = 30. Outcome = avoid-trap (uses the buried fact).

| needle depth | Haiku | Sonnet |
|---|---|---|
| early (8%)   | 5/5 | 5/5 |
| middle (50%) | 5/5 | 5/5 |
| late (92%)   | 5/5 | 5/5 |

- **No positional decay (30/30)** — middle (worst case per [5]) as clean as the ends.
  'Lost in the middle' did not appear at ~6.6k tokens for a *semantically-unique* needle.
- Bounds the depth claim to the tested scale + a distinctive needle; arbitrary scale and a
  *camouflaged* needle (needle-similar distractors) remain the standing residual.

*Last consolidated: 2026-06-05, against witness tail SOUL-139 / `02`+`03`+`06`+`07`+`08` + the five-vehicle filler control + calibration + depth-position + handoff experiments.*
the four-probe filler control + calibration + depth-position experiments.*
