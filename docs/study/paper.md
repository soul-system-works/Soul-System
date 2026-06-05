# Does a meta-doctrine system change model behaviour, or just make it legible? A self-ablation study under equal compute

## Abstract

"Agentic" coding setups increasingly ship a *meta-doctrine layer*: a body of always-on
guidance — roles, gates, principles — plus a record that accumulates across sessions,
on the premise that this scaffolding improves the work. We ablate one such system (the
"Soul System") against the confound that dominates this class of claim: loading
doctrine also loads *tokens*, and additional context alone can make a model more
thorough. Every apparent gain is therefore re-run against a **length-matched,
semantically-empty filler** of equal token budget; a gain that vanishes under this
control was compute, not doctrine. Across ten doctrine probes and six instrument
probes (Haiku 4.5, Sonnet 4.6, Opus 4.8; n = 5–7 per cell), the equal-compute control
catches four false positives, and the surviving substance collapses onto a single
axis: the system changes the model's *decisions* only when it carries **project-specific
knowledge or counter-default conventions the model cannot regenerate and a generic
equivalent gets wrong** (record-recall 10/10 vs. 2/5 for a length-matched irrelevant
record; convention-transmission flips a counter-default decision 10/10 where generic
principles give the default answer 0/10). Everything aimed at generic reasoning-lift —
forced roles (as prose *and* as dedicated sub-agents), trajectory-reading,
compliance-resistance, the handoff and verification *formats* — is reproduced by the
filler. A synthetic multi-session harness extends this to the system's strongest claim:
a counter-default fact recorded early and buried under later work prevents a dangerous
drift 5/5 → 0/5 in a later session, and — uniquely among our results — **does not
dissolve at the frontier**: the strong model, lacking the recorded fact, fails *more*
confidently, fabricating a non-existent API affordance to justify the unsafe path. The
organizing principle is **derivable-dissolves, unguessable-persists**. We give the
resulting keep/cut decision and a precise ledger of what a single-shot method cannot
settle.

---

## 1. Introduction

A growing class of tooling wraps a language model in a *meta-doctrine layer*: standing
instructions loaded into every session (personas or "roles," verification gates, design
principles) together with a durable project record (decision logs, findings,
conventions) that grows over time. The implicit and often-stated promise is that this
layer *improves the work* — the model reasons more carefully, catches more defects, and
stays coherent across a long project.

This promise is unusually hard to falsify by inspection, because the layer reliably
changes the *surface* of the output: longer, more structured, more self-aware-sounding
text. That surface change is consistent both with the layer genuinely improving the
*substance* of decisions and with it doing nothing but making the model verbose and the
work legible. Distinguishing the two requires a control the field rarely applies.

We study one mature instance — an open meta-doctrine system we call the Soul System,
comprising ~16 commands, a three-layer always-on doctrine, and an append-only record —
and ask a deliberately deflationary question: **which parts change what the model
decides, and which only change how the work reads?** Our contributions are:

1. **An equal-compute ablation protocol** (Section 3) that re-runs every apparent win
   against a length-matched, semantically-empty filler, isolating doctrine-substance
   from the compute that any long prompt supplies.
2. **A behavioural map** (Section 4) across doctrine and instruments, capability tiers,
   and task structures, including four wins that the control falsifies.
3. **A single organizing axis** — *derivable-dissolves, unguessable-persists* — that
   predicts what survives, and a synthetic multi-session result showing the surviving
   value is the first in the study that does not dissolve at the frontier.
4. **A keep/cut decision** for a lean version (Section 5) and an explicit ledger of
   what a single-shot method cannot measure (Section 6).

The result is not a defence of the system and not a debunking. It is a separation: a
narrow, real, capability-robust value (carrying the unguessable) from a larger body of
legibility that a generic equivalent matches.

---

## 2. Related work

**Context quantity as a confound, and what filler does.** The premise of our control is
that added tokens can change a model's output independent of their content. The
direction of that effect is not simple, and the literature is split in a way that
matters for interpretation (Section 6). Pfau et al. [14] show that even
*semantically-empty* filler tokens can supply usable parallel computation — small
transformers solve problems with filler they cannot solve answering immediately — though
the ability is hard to acquire and was absent in commercial models of that era. In the
opposite direction, and more robustly, *irrelevant* context **degrades** reasoning: Shi
et al. [15] ("distracted by irrelevant context") find accuracy drops sharply when
in-topic but irrelevant information is added. So extra tokens are not free, and their
sign depends on model and content — which makes a length-matched filler the right
instrument but its bias direction something to argue, not assume.

**Roles and personas.** Assigning static personas in system prompts does not reliably
improve accuracy; Zheng et al. [1] test 162 roles across model families and find no
general benefit, and Kim et al. [7] show role-play *degrades* reasoning on a third of
datasets even at the frontier, with bidirectional, near-zero net effect. The boundary:
Kong et al. [8] find an engineered multi-turn *role-immersion* prompt helps zero-shot
reasoning — but as an implicit chain-of-thought trigger, a different intervention than
a static persona. This matches and bounds our doctrine result (Sections 4.1, 4.3).

**Single- vs. multi-agent decomposition.** Under matched compute the case for
multi-agent orchestration weakens. Tran and Kiela [2] show single-agent LLMs *outperform*
multi-agent systems on multi-hop reasoning at equal thinking-token budgets and argue
reported multi-agent advantages are "better explained by unaccounted computation"; Gao
et al. [3] find the advantage diminishes as base models improve. Notably the canonical
multi-agent-debate result [9] reports gains *without* a compute-matched baseline — the
exact confound our method targets. Our agentic-roles probe (Section 4.3) reaches the
same conclusion for Soul's roles rebuilt as sub-agents.

**Knowledge vs. reasoning; retrieval over parametric memory.** Our organizing axis —
*derivable dissolves, unguessable persists* — restates a robust result. Lewis et al.
[10] (RAG) show parametric models have "limited ability to access and precisely
manipulate knowledge" and that adding a non-parametric retrieved store beats the
parametric model; Ovadia et al. [11] find retrieval "consistently outperforms"
unsupervised fine-tuning for injecting facts the model lacks. Gan and Sun [4] (RAG-MCP)
extend the same retrieve-don't-preload logic to tool selection, underwriting both our
never-load-everything doctrine and the skill-routing probe (Section 4.4).

**Calibration and confident fabrication.** Our longitudinal result turns on a model
*fabricating* a missing fact rather than abstaining. The GPT-4 technical report [12]
documents that the model "can be confidently wrong... not taking care to double-check
when it is likely to make a mistake," and that RLHF post-training *degrades* calibration
(expected calibration error rising roughly tenfold from the pre-trained model). Kadavath
et al. [13] show models have partial but imperfect self-knowledge of what they know. We
return in Section 6 to what this does and does not license about *scale*.

**Positional use of long context.** Liu et al. [5] ("lost in the middle") show models
use information at the beginning and end of long inputs far better than the middle — the
degradation a record-burial probe must control for, and a caveat on our depth result
(Section 6).

**Self-critique limits.** Verification gates assume a model can catch its own errors;
Huang et al. [16] find LLMs "cannot self-correct reasoning yet" without external
feedback — consistent with our result that the gate *concept* helps but its
elaborateness does not (Section 4.2).

**Persistent memory and rules.** External-memory agents (MemGPT [17]; generative agents
with a memory stream [18]) make the cross-session-record hypothesis concrete, though
neither isolates record-content from compute as we do. Constitutional AI [6] steers
behaviour from a small explicit rule-set rather than dense supervision; the Soul
System's compressed always-on rules are a project-level analogue (Section 4.2).

We position this as an *engineering self-ablation*, not a survey: its contribution is
the equal-compute discipline applied uniformly and the longitudinal harness, not breadth
of coverage.

---

## 3. Method

### 3.1 Arms and models

The unit of measurement is an **arm**: a tuple `(task, condition, model, run-index)`.
Each arm is an isolated, non-interactive model call (`claude -p "<task>" < /dev/null`,
fresh process, no chat history); the thing under test (doctrine, a role lens, a gate
checklist, a handoff cursor, a record) is supplied via the system prompt or pasted into
the task, and the bare arm receives the task alone. We run n ≥ 5 per cell unless noted,
across a capability range — Haiku 4.5 (weak), Sonnet 4.6 (mid), Opus 4.8 (frontier) —
because the effect size of any aid depends on whether the bare baseline already
succeeds.

### 3.2 The three controls

**C1 — Equal-compute control (decisive).** The dominant confound in this class of claim
is that loading the system also loads tokens. Every apparent win is re-run against a
**length-matched, semantically-empty filler** of the same budget: ~26 KB of unrelated
warehouse-logistics prose in place of ~26 KB of doctrine; a generic "double-check your
work" in place of a named gate checklist; a plain summary in place of a structured
cursor. *A substance verdict that vanishes under equal compute is not substance.* C1
caught four false positives here (Section 4.1–4.2).

A direction caveat (developed in Section 6). The filler is not a neutral inflator: the
literature shows added irrelevant tokens more often *degrade* than improve a model [15],
while empty filler can occasionally *supply* compute [14] — both effects are model- and
content-dependent. This makes C1 a **conservative** control rather than a symmetric one:
a gain that *survives* the filler is real a fortiori (the filler, if anything, biased
against the bare-plus-filler arm), but a gain that *vanishes* is ambiguous between "was
compute" and "the filler actively hurt the control arm." Our four filler types are
*coherent-but-irrelevant* (warehouse prose) or *generic-nudge* ("double-check"); where
they tied doctrine they generally also beat the bare baseline (Section 4.2), so they were
not degrading in those cells. We run the clean separation — a three-arm control with a
coherent-irrelevant distractor alongside empty padding — in Section 4.6, and it confirms
on-model that coherent-irrelevant filler is not neutral while empty padding ≈ bare.

**C2 — Difficulty validation.** A task measures an aid only if the bare baseline
plausibly fails it. Before scoring, the bare arm is run n ≥ 5; if it already succeeds,
the task measures ceiling, not the aid, and is discarded or sharpened. A corollary
learned the hard way: a high-salience domain (e.g. patient safety) can trigger a
caution reflex that *substitutes* for the discipline under test, passing the baseline
for the wrong reason; one medical task was discarded for exactly this. Domains are kept
low-salience.

**C3 — Trap taxonomy.** When a task plants a defect, the defect is of a named kind so a
"catch" maps to a specific discipline: a false premise (anchoring), a dropped
requirement (completeness), a buried downstream consequence (trajectory), a
silently-truncated long-horizon constraint (gate). One trap per task.

### 3.3 Scoring

Rubrics and answer keys are **pre-registered** before outputs are seen. Outcomes are
scored mechanically where possible (count the behaviour; within-cell comparable
keyword patterns) and then **read-confirmed** on borderline arms. Counts are never
eyeballed, and we explicitly watch for *wrong-reason* passes (an artifact refused for
missing information, a placeholder flagged, a disaster-salience reflex) — these are
designed out or scored separately. One pass in this study *looked* like a decisive win
on a keyword count (5.8 vs. 2.6) and reversed on the binary read (both 5/5): the count
had measured verbosity of flagging, not catches.

### 3.4 Three honest value buckets

Not everything is single-shot A/B-testable, and faking a single-shot proxy for a
longitudinal or human-workflow claim would be the precise self-consistent-but-false
result the study exists to catch. Each component is assigned a bucket: **Measured**
(A/B + C1), **Reasoned** (friction/convenience, assessed by transparent cost-vs-value
argument, not a faked experiment), or **Inspected** (one-time/structural artifacts).

### 3.5 Harness and a contamination finding

Arms run from a scratch working directory; condition files are supplied via the model
CLI's system-prompt-file flag or pasted inline. **Cross-file `@`-imports are not used**
under the non-interactive mode: they fail silently and the model confabulates the
missing content ~43% of the time (this is itself one of the project's findings, and the
deciding knowledge in the recall probe), so content is inlined and a sentinel
load-test confirms it reached the model before any run is trusted. A separate
contamination was caught and fixed: non-interactive arms have tool access and read the
working directory, so arms launched from a directory containing the answer file simply
*grepped it* even in the no-record condition; every arm is therefore run from an
**isolated empty directory**, and the contaminated run is retained as evidence.

### 3.6 Known bounds of the method

The harness is single-shot / single-resume; the system's strongest claim is
intrinsically longitudinal, reached here by a synthetic session-chain harness
(Section 4.5) rather than real project history. n is small (5–7/cell); keyword scoring
is within-cell comparable, not absolute. The scorer is also the experimenter; rubrics
are pre-registered to constrain this, and where bias is plausible it runs *toward* the
system, so null results are conservative.

---

## 4. Results

### 4.1 Doctrine (the always-on layer)

Against a careful frontier baseline, single-role and single-gate ablations changed the
*form* of the work (named, legible, auditable) far more than its substance or
reliability. An engineered hard regime — a buried logic trap, a false premise under
authority pressure, and a ten-constraint long-horizon task — was also form-not-substance
at the frontier (the completion-gate ablation on the long-horizon task was null,
gate ≈ bare).

At a **weak baseline** (Haiku), with the integrated doctrine and C1 throughout,
doctrine-attributable substance survives in exactly one place: **challenging an
unverified premise** ("anchoring"). It lifted the false-premise task 0/3 → ~1.5/3 while
the filler stayed 0/3, and replicated on a second anchor task (whole 3/3 vs. filler
0/3). This substance is *content-dependent* (generic thoroughness cannot fake it),
*weak-baseline-only* (a mid-capability model self-catches), and *task-structure-gated*
(analysis-inviting tasks self-catch earlier than compliance-inviting ones).

**Everything else dissolved under C1, including three apparent generalizations:**
trajectory-reading (bare 1/3 → whole 3/3, but filler 2/3 — generic long-context),
compliance-flagging (filler reproduced it — disposition), and stakes-gated withholding
(filler 5/5 = whole — disposition, not doctrine). Without the equal-compute control the
study would have claimed a "frontier-ward compliance edge" that does not exist. The
consonance with Zheng et al. [1] (roles don't lift accuracy) is direct.

### 4.2 Instruments and the record

**Handoff/resume (Measured; form).** A fresh session given a curated record snapshot
plus one of {structured cursor, length-matched generic prose summary, terse compact,
nothing} surfaced more constraints with any rich note than cold (≈ +2 constraints; 0
vs. 1 scope-invention error) — but the *Soul format is form*: a length-matched generic
summary tied or beat the cursor (Sonnet 4.8 generic ≥ 4.6 cursor; Haiku equal).
Richness matters, structure does not.

**Record-recall (Measured; KEEP — the clearest win).** A trap task whose deciding
knowledge is a real, non-obvious project finding was run with {relevant record, no
record, length-matched *irrelevant* record (C1)}. The relevant record produced
trap-avoidance **10/10**; the irrelevant record **2/5**; no record 2–3/5 (capable arms
partially reason toward the right hedge but mostly still recommend the trap). The
*specific recorded content* — not "having a record," not the tokens — makes the model
reliably correct.

**Verification gate (Measured; concept yes, format no).** Finalizing a draft with one
planted unanchored-claim defect: bare caught it 2/5; *any* check (generic-vague,
generic-checklist, or the Soul checklist) lifted it to ~5/5. The gate *concept* earns
its place; the Soul-specific checklist does **not** beat a generic "double-check
carefully" on catch-rate (both 5/5) — it adds itemized legibility, which is form. (A
second, dropped-requirement defect was a C2 ceiling, 5/5 everywhere.)

**Distillation / the "Mind" (Measured; KEEP the content).** A decision where the
project's convention *contradicts the trained-in default* (keep docs adjacent to code,
vs. the default separate docs tree). Loading the project's rules — compressed Mind *or*
a raw-records excerpt — flipped the recommendation to the project's answer ~10/10; a
length-matched *generic-principles* set gave the opposite, default answer ~0/10. This
is the same axis as recall: carrying a counter-default convention a generic equivalent
gets wrong. Note the compressed Mind transmitted the convention no better than an
equal-size raw excerpt (`Mind ≈ raw`), so the rule *content* is the substance; whether
it needs auto-distillation versus hand-curation is not settled here. **Moderation
(Section 4.6):** under a stricter three-arm control this particular convention proved
partly *derivable* and disposition-primable — its two-arm gap was inflated by a loaded
counter-distractor. The recall result (an unguessable *fact* a generic equivalent gets
confidently wrong) is the stronger, cleaner member of this KEEP; the convention is real
but narrower.

### 4.3 Roles as agents

A natural objection to "roles = form" is that roles were measured as prose, never as
*dedicated sub-agents*. Rebuilt as agents — one sub-agent per Council role plus a
synthesis step — Soul's roles still only matched a generic decomposition at equal
compute, and the multi-agent topology did not beat a single agent told to work through
the same perspectives in one context (it tied at best and lost where the synthesis step
pruned valid findings). The substance is *decomposition into explicit perspectives* —
cheap, generic, single-context — not the Soul framing or the agentic orchestration. The
"form" verdict thus extends from prose to agents, consistent with Tran and Kiela [2] and
Gao et al. [3].

### 4.4 Skill routing (a bounded win)

One reasoning-adjacent capability survived the control: *knowing which specialized skill
to deploy when*, under a selection budget. Given a catalog with a tempting-but-wrong
trap skill and a non-obvious-correct skill, a weak model forced to pick ≤ 2 reliably
grabbed the trap and missed the right skill (self-pick 1/5); handed the right skill, it
solved 5/5 (oracle vs. budgeted self-pick = 5/5 vs. 1/5 at Haiku). It dissolves at the
frontier (the strong model knows the answer) and without a budget (free selection
over-selects and catches the skill anyway). It thus lives in the same cell as
anchoring — *weak baseline × counter-default knowledge × tight budget* — the
deployment-face of the record, and it is an oracle (perfect-routing) upper bound. The
retrieval framing matches Gan and Sun [4].

### 4.5 Longitudinal accumulation (the strongest claim)

The system's central promise is intrinsically multi-session and cannot be faked
single-shot. We reach it with a synthetic **session chain**: an early session records a
counter-default decision D (with the incident that established it); later sessions bury
D under unrelated entries; a fresh session, with D's triggering context gone, faces a
new task that tempts the dangerous default. Drift = the default returns. Outcomes are
read in the produced code, not by keyword.

**The carry prevents drift, and it persists at the frontier.** With D recorded and
carried, drift fell **5/5 → 0/5**; a length-matched filler record drifted exactly like
having no record (C1 passes). Crucially, this is the **first win in the study that does
not dissolve at the frontier**: the strong model drifts *too*, and worse — lacking the
recorded fact it does not merely choose the default, it *invents* a reassuring
affordance that does not exist (a payment idempotency key the API lacks) and explains
why that makes the unsafe retry safe — a confident fabrication rather than an
abstention, consistent with the calibration-degradation documented for post-trained
frontier models [12]. The mechanism is that D is knowledge the model *cannot
regenerate*, not a reasoning skill it can. (We are careful in Section 6 not to over-read
this as a *monotonic* "stronger ⇒ more confident fabrication" scale law — our own data,
Section 4.5 below, shows the failure direction is gated by the rule's *form*, not by
capability alone.)

**Facts and conventions both carry; the line is derivability.** A sibling probe recorded
an arbitrary *convention* (return a Result type, never raise) rather than a fact; it
persisted at the frontier too — the strong model deferred to the recorded convention
instead of overriding it with its own idiom. The organizing line is therefore
**derivable-dissolves, unguessable-persists**: what the model can re-reason
(generic anchoring, routing at the frontier) dissolves under the control; what it cannot
regenerate (a fact *or* an arbitrary convention) persists.

**The carry is depth-robust.** Varying record depth, the fact still fired 5/5 buried
under 20 intervening decision records at both capabilities, with no decay cliff through
N = 20 (the frontier control still drifted at depth). This is the regime where
lost-in-the-middle degradation [5] would predict failure; within the tested depth it did
not appear.

**Compression preserves the rule but not the fact's force.** Distilling D exposes a
limit relevant to any always-on rule-set. The *directive* survives compression to a
single line (0 violations across 45 cells, both capabilities). The unguessable *fact*
behind it does not: strip the incident and the explicit negation, leave the terse rule,
and the frontier model fabricates a replacement justification on a gradient by how much
force survived — full record 0/5, faithful distillation 2/5, aggressive erosion 4/5,
while the weak model never fabricates (0/15, it lacks the confident prior). A second,
independent counter-prior fact replicated the gradient but *inverted* the
capability-direction (the weak model drifted where the frontier held), and an isolating
probe — holding the prior constant and varying only the directive's *form* — resolved
the mechanism: the frontier flips 0/5 → 5/5 when an imperative rule is replaced by a
*loophole* ("reuse only if validity is confirmed"), fabricating the affordance to walk
through the opening; **directive form gates the frontier, prior-strength gates the weak
model.** The operational consequence (adopted as a doctrine amendment): when compressing
a fact that contradicts a strong model prior, preserve its *force* — the incident, the
explicit negation — not merely its proposition, and keep the residual directive
imperative and loophole-free.

### 4.6 The three-arm control (separating compute, distraction, substance)

Motivated by the literature in Section 2, we ran the three-arm extension of C1 — adding
**empty padding** (length-matched lorem = pure compute) and **coherent-but-irrelevant**
prose (length-matched off-topic operations text = distraction) alongside bare and the
substance arm. We ran it on four vehicles in all; the first two were chosen to differ on
one axis — whether the project's answer is *derivable* — and that pair is the clearest
single illustration of the study's organizing thesis.

On a **derivable convention** (the project keeps documentation adjacent to code, vs. the
common default of a separate `docs/` tree), the binary outcome did *not* isolate
substance. The frontier model already gave the project's answer at baseline (it
re-derives "central docs drift"), and at the weak baseline a *coherent-irrelevant* filler
drove the project's answer 5/5 — its disciplined operational register primed a cautious
disposition that re-derived the same conclusion — while empty padding sat at the bare
level (2/5). Only the *reasoning* distinguished the substance arm (it cited the specific
recorded incident; the distractor re-derived generically). This is a direct, on-model
confirmation of Section 2's warning that coherent-irrelevant tokens are not neutral, and
it **moderates the convention-transmission result of Section 4.2**: a project answer that
is also a defensible generic answer is partly derivable and disposition-primable, so its
two-arm "win" overstated the isolable substance (the original generic-principles control
there was a *loaded* counter-distractor, which inflated the gap).

On an **unguessable fact** (a recorded finding that a certain import mechanism fails
silently in non-interactive mode and the model confabulates around it — the recall probe
of Section 4.2), the same three-arm control isolated substance **cleanly**: the record
produced the correct, trap-avoiding recommendation **10/10**, while bare, empty padding,
and coherent-irrelevant filler each endorsed the trap **0/10** — the coherent filler was
*harmless* here (≈ bare), the opposite of the convention probe, because no disposition
re-derives a fact the model simply does not have. Two incidental confirmations: empty
padding ≈ bare on both probes (pure length did not move these decisions on our models),
and the frontier model, lacking the fact, *confidently asserted its negation* ("imports
resolve in non-interactive mode the same as interactive" — false) — a second-domain
instance of the confident-fabrication of Section 4.5.

The pair is the thesis in miniature: a coherent-irrelevant filler reproduces a
*derivable* answer and is powerless against an *unguessable* one. The recall (record)
KEEP survives the stricter control; the convention KEEP is real but narrower than its
two-arm number suggested.

A third probe extends the control to a **"form" verdict** — the completion/verify gate
("local tests passing is not global correctness; validate the invariant the whole must
satisfy before declaring done"). On a high-stakes vehicle (a payment-splitting refactor
with green unit tests, asked "ship it?"), the three-arm control did not merely moderate
the gate — it found it *fully derivable*: **all four arms avoided the trap 40/40**, bare
included. With zero injected context both models already withhold the ship and demand
real-world validation (a reconciliation invariant, shadow-replay against production data,
a canary); the substance arm's only isolable contribution is a *citation* — it names the
specific doctrine (6/10 cells) where no other arm does, and lifts the explicit "invariant"
framing from re-derived (bare 7/10) to universal — while leaving the decision unchanged.
The verify gate is thus the *most* derivable verdict measured, more so than the convention
(whose bare baseline at least sat at 2/5): its value is **legibility** (a named invariant,
an auditable citation), not behaviour change, because the disposition it records is one the
model already holds. The probes form a three-position spectrum of the organizing thesis —
*unguessable fact* (recall, clean isolation 10/10 vs 0) → *derivable convention* (docs,
moderated, disposition-primable) → *already-held disposition* (verify, fully derivable,
ceiling). One bound on the verify probe — that its high-stakes vehicle is domain-saturated
(financial-correctness maximally primes caution) — was then tested with a low-stakes vehicle
(an internal analytics dashboard, where shipping on green tests is defensible). Bare still
withheld 10/10: caution is re-derived even off-saturation, so "legibility, not behaviour"
survives the stricter test. The one behavioural residue is thin and frontier-only — a
coherent-irrelevant distractor *eroded* Sonnet's caution (3/5, two cells flipping to "ship
now, verify post-deploy"; cf. [15]) and the verify doctrine *resisted* the erosion (5/5),
so the gate acts as a weak *stabiliser* against distraction, not as a teacher of caution the
model lacks. (This is the opposite polarity to the convention probe, where the coherent
distractor *primed* a derivable answer rather than eroding vigilance — coherent-irrelevant
filler is not neutral, and its sign depends on the task.) The handoff verdict still rests on
the original two-arm control.

---

## 5. The lean-down: what survives

Applying a default-cut rule (keep only measured value or a clearly-argued unique value a
generic equivalent lacks), with one counterweight — *scaffolding that makes a good
practice reliably happen has value even when its content is not unique* (a completion
hook that fires; a capture command that lowers the friction of recording; a format that
makes knowledge findable) — the system reduces to a small core:

1. **The records** (append-only log, findings, ideas): the proven carrier of specific,
   otherwise-un-derivable knowledge. *Keep — the core.*
2. **A minimal always-on seed**: the framing principle, the anchor obligation (the one
   reasoning-substance), the project's counter-default conventions as a short rule-set
   (the distill result), and one-line expansion / ask-the-human nudges. No role-chamber
   prose.
3. **A completion gate**: a short pre-ship check whose load-bearing item is the anchor
   check, fired as a hook (activation over prose).
4. **One capture command** (plus an earned-finding gate) and setup.
5. **A tested, selective skills catalog** with budget-aware routing — the deployment
   face of the record, valuable where weak models meet selection pressure.

Cut or folded to a one-line convention: the forced-perspective council (form, as prose
*and* as agents), the role-as-subagent engine, the handoff-cursor *format*, the
read-only utilities, and the elaborate verification checklist. The bet is explicit: the
value is counter-default project knowledge in three faces — *having* it (recall),
*compressing* it (the seed rule-set), and *deploying the right piece when* it is not
obvious (routing) — plus the anchor discipline and activation, all concentrated where
the generic default is wrong; the frontier dissolves the reasoning-ceremony because it
already knows. **This is a recommendation, not an executed change**: retiring commands
and shrinking always-on doctrine is hard to reverse and affects adopters, and is held
for separate review.

---

## 6. Threats to validity and what was not settled

The method's deliberate blind spot is its honesty test. Several of the largest bets sit
on the side it cannot measure single-shot, and a faked single-shot proxy for one of them
would be the exact self-consistent falsehood the study exists to catch.

- **Longitudinal accumulation** is reached only by a *synthetic* session chain, not real
  multi-session history; seven rungs are climbed (carry, convention, depth, erosion,
  weak-distiller, second prior, form-vs-prior), but scale (many interacting facts, a long
  eroding record) remains a widening of the harness.
- **Multi-task routing** (does a curated catalog pay off across a task distribution?) and
  a **built router** (vs. the oracle upper bound) are unmeasured; the routing win is one
  task and a perfect-routing bound.
- **Tool-skills** (differential real tools) cannot be granted to headless arms; routing
  used procedure-knowledge as a faithful proxy for the selection kernel.
- **Retrieval in a large repo** is closeable but deferred as low marginal value
  (predicted to re-confirm "the record carries the value").
- **Legibility's payoff to a human over time** — the standing justification for keeping
  the record readable — is asserted, not measured; it is human and longitudinal.
- **The filler control is conservative, not symmetric.** As Section 3.2 notes and the
  literature establishes, irrelevant tokens more often degrade than inflate [15], so a
  vanished gain conflates "was compute" with "filler hurt the control." This biases
  the study toward *under*-stating doctrine, which makes the surviving wins (recall, distill,
  longitudinal) robust but leaves some "form" verdicts with a residual ambiguity. The
  three-arm control (Section 6.1) was run to address this; it confirmed the recall KEEP,
  moderated the convention KEEP, and resolved the verify verdict as derivable. The handoff
  verdict still rests on the two-arm control — the one remaining residual on this axis.
- **"Stronger ⇒ more confident fabrication" is not claimed as a scale law.** The anchored
  result [12,13] is that capability does not *eliminate* confident fabrication and that
  RLHF degrades calibration — a training-incentive effect, not a monotonic function of
  scale. The cross-scale calibration probe (Section 6.1) settled this directly on a 3-tier
  ladder: recall of the unguessable fact does not improve with capability (44/45 fail
  across tiers), and the *confident-false-assertion* rate rises with capability (Haiku <
  Sonnet < Opus) — capability makes the fabrication more articulate, not rarer. This is a
  non-elimination result, **not** a monotone scale law on the binary (which is saturated).
- **The depth result, now with needle position varied at token scale.** "Lost in the
  middle" [5] is a large-*token* phenomenon; our original no-decay result was at N = 20
  record *units* at primacy position. The token-scale probe (Section 6.1) re-ran it at
  ~6.6k tokens with the needle at 8% / 50% / 92% depth: no positional decay (30/30, both
  models; middle as clean as the ends). We bound this to the tested scale and a
  *semantically-unique* needle; arbitrary token scale and a *camouflaged* needle (the regime
  where [5] bites hardest) remain the standing residual.
- n is small; the scorer is the experimenter (bias runs toward the system, so nulls are
  conservative). Citation hygiene was itself a live test of the study's own thesis: a
  verification pass over the project record found one anchor (a review paper) cited for a
  framing slightly stronger than a review supports — downgraded to background here, with
  the load-bearing anchors retained [1,2] — and an *initial over-correction* that labelled
  it "fabricated" before re-checking showed the identifier was real and correct. Both the
  weak-anchor and the over-correction are instances of the anchor-validity discipline the
  study formalizes, applied reflexively.

For the measurable rows, closure is a probe; for the unmeasurable rows, closure is this
ledger — naming each precisely, with why it resists single-shot measurement. The study
marks the open ground rather than claiming it.

### 6.1 Experiments — all four run

The literature review surfaced four measurements that would each sharpen a result above.
All four were subsequently run (each pre-registered with a locked prediction before any
output was read); the residuals are now bounds, not blanks.

1. **Three-arm filler control** — *done, four probes* (Section 4.6). Re-running with
   {empty-padding, coherent-irrelevant, substance} confirmed the recall (record) KEEP
   cleanly (10/10 vs 0), moderated the convention KEEP (derivable + disposition-primable),
   and — extended to the **verify** "form" verdict on two vehicles — found it the *most*
   derivable verdict. A high-stakes completion-gate vehicle ceilinged at 40/40 avoid-trap
   across all four arms (bare included); a *low-stakes* vehicle, run to test whether that
   ceiling was domain-saturation, still showed bare withholding 10/10 — caution is derived
   even off-saturation, so "legibility, not behaviour" holds — with one residue: a
   coherent-irrelevant distractor *eroded* frontier caution (Sonnet 3/5) and the doctrine
   *resisted* the erosion (5/5), a thin "stabiliser" effect, not a teacher. The handoff
   verdict remains on the two-arm control.
2. **Direct empty-filler check on the study's own models** — *done*: empty padding ≈ bare on
   all probes (pure length did not move these decisions), so the inflation direction did not
   fire here. The conservative-control caveat (§3.2) therefore biases toward *under*-stating
   doctrine, as expected.
3. **Cross-scale calibration** — *done* (3-tier ladder, Haiku→Sonnet→Opus, 45 no-fact
   cells). Settled two-part: recall of the unguessable fact does *not* improve with
   capability (44/45 fail to recall it, flat across tiers), and capability does not *resolve*
   confident fabrication — it makes it more confident and articulate (the explicit-false-
   assertion rate rises Haiku < Sonnet < Opus; the strongest model states the falsehood most
   cleanly). Not a monotone scale law on the binary (the binary failure is saturated); the
   anchored claim is *non-elimination*, now on a third domain.
4. **Token-scale and position depth test** — *done* (F038 needle at 8%/50%/92% depth in a
   ~6.6k-token record). No positional decay: 30/30 recall at every position, both models;
   middle (the worst case per [5]) as clean as primacy/recency. 'Lost in the middle' did not
   appear at this scale for a *semantically-unique* needle. This bounds the depth claim to
   the tested scale and a distinctive needle; arbitrary scale and a *camouflaged* needle
   (needle-similar distractors, where [5] bites hardest) remain the standing residual.

---

## 7. Discussion

The findings collapse onto one distinction. A meta-doctrine layer can try to make a
model *reason better generically*, or it can *carry information the model cannot
regenerate*. The first is reproduced, at equal compute, by an equivalent quantity of any
content — it is legibility, disposition, or compute, and it fades as the base model
improves. The second is not: a fact about a specific API, a convention specific to a
project, an incident specific to a team — these have no generic substitute, and they
remain decisive at the frontier. And the frontier failure mode is not benign: a capable
model that lacks the fact does not abstain; it can generate a confident, plausible,
wrong justification (Section 4.5) — the precise hazard against which an external,
unguessable anchor is the only defense. We resist the stronger claim that capability
*monotonically* worsens this; our evidence is that capability does not *resolve* it, and
that whether the strong or the weak model fails is gated by the form of the surviving
rule.

This reframes what such systems are *for*. Their durable value is not a reasoning
prosthesis but a **memory of the unguessable**, plus the *activation* scaffolding that
makes recording and checking reliably happen. The reasoning-ceremony — roles, councils,
forced perspectives, structured formats — reads like substance and measures like form.
That it reads like substance is not incidental: the same verbosity that makes it
*feel* like better thinking is what a length-matched control reproduces.

The compression result sharpens the design rule. Because the dangerous failure is the
frontier model fabricating around a missing fact, an always-on rule-set must preserve
not just a rule's proposition but the *force* of the counter-prior fact behind it; a
terse rule with the incident stripped invites the very fabrication it was meant to
prevent, and a loophole in the rule is the opening the strong model takes.

---

## 8. Conclusion

Most of what makes a meta-doctrine system *feel* effective is the system making the work
legible and the model more verbose — reproduced, at equal compute, by semantically-empty
filler, and fading at the frontier. The part that genuinely changes what the model
decides is narrow and capability-robust: carrying project-specific, counter-default
knowledge the model cannot regenerate and a generic equivalent gets wrong, together with
the scaffolding that makes recording and checking reliably happen. *Derivable dissolves;
unguessable persists.* A lean system that keeps the record, a small counter-default
rule-set, a tested skills catalog, and a firing completion gate — and cuts the
reasoning-ceremony to a line — captures the measured value at a fraction of the surface.

---

## References

[1] M. Zheng, J. Pei, L. Logeswaran, M. Lee, D. Jurgens. *When "A Helpful Assistant" Is
Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large
Language Models.* arXiv:2311.10054, 2023.

[2] D. Tran, D. Kiela. *Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop
Reasoning Under Equal Thinking Token Budgets.* arXiv:2604.02460, 2026.

[3] M. Gao, Y. Li, B. Liu, Y. Yu, P. Wang, C.-Y. Lin, F. Lai. *Single-agent or
Multi-agent Systems? Why Not Both?* arXiv:2505.18286, 2025.

[4] T. Gan, Q. Sun. *RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection via
Retrieval-Augmented Generation.* arXiv:2505.03275, 2025.

[5] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, P. Liang.
*Lost in the Middle: How Language Models Use Long Contexts.* arXiv:2307.03172, 2023.

[6] Y. Bai, S. Kadavath, S. Kundu, et al. *Constitutional AI: Harmlessness from AI
Feedback.* arXiv:2212.08073, 2022.

[7] J. Kim, N. Yang, K. Jung. *Persona is a Double-edged Sword: Mitigating the Negative
Impact of Role-playing Prompts in Zero-shot Reasoning Tasks.* arXiv:2408.08631, 2024.

[8] A. Kong, et al. *Better Zero-Shot Reasoning with Role-Play Prompting.* NAACL 2024,
arXiv:2308.07702, 2024.

[9] Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, I. Mordatch. *Improving Factuality and
Reasoning in Language Models through Multiagent Debate.* arXiv:2305.14325, 2023.

[10] P. Lewis, E. Perez, A. Piktus, et al. *Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks.* NeurIPS 2020, arXiv:2005.11401, 2020.

[11] O. Ovadia, M. Brief, M. Mishaeli, O. Elisha. *Fine-Tuning or Retrieval? Comparing
Knowledge Injection in LLMs.* EMNLP 2024, arXiv:2312.05934, 2023.

[12] OpenAI. *GPT-4 Technical Report.* arXiv:2303.08774, 2023.

[13] S. Kadavath, T. Conerly, A. Askell, et al. *Language Models (Mostly) Know What They
Know.* arXiv:2207.05221, 2022.

[14] J. Pfau, W. Merrill, S. R. Bowman. *Let's Think Dot by Dot: Hidden Computation in
Transformer Language Models.* arXiv:2404.15758, 2024.

[15] F. Shi, X. Chen, K. Misra, et al. *Large Language Models Can Be Easily Distracted by
Irrelevant Context.* ICML 2023, arXiv:2302.00093, 2023.

[16] J. Huang, X. Chen, S. Mishra, et al. *Large Language Models Cannot Self-Correct
Reasoning Yet.* ICLR 2024, arXiv:2310.01798, 2023.

[17] C. Packer, S. Wooders, K. Lin, et al. *MemGPT: Towards LLMs as Operating Systems.*
arXiv:2310.08560, 2023.

[18] J. S. Park, J. C. O'Brien, C. J. Cai, et al. *Generative Agents: Interactive
Simulacra of Human Behavior.* UIST 2023, arXiv:2304.03442, 2023.

*Citation provenance: [1]–[6] were resolved directly against arXiv during drafting;
[7]–[18] were fetched and adversarially cross-checked by a multi-agent literature sweep
(22 of 25 sampled claims confirmed, 3 refuted), then — in a final per-identifier sweep
(2026-06-05) — every one of [7]–[18] was re-fetched directly against arXiv and confirmed
correct on identifier, title, and authors (zero bad identifiers). That sweep did surface
two **venue** annotations that neither the arXiv page nor a targeted search could anchor —
"[7] EMNLP 2024 Findings" and "[14] COLM 2024" — which have been softened to arXiv-only
rather than asserted; venues that were confirmed are retained ([8] NAACL 2024 main, [11]
EMNLP 2024 main, [16] ICLR 2024, [18] UIST '23). This is a third reflexive instance of the study's own
anchor-validity discipline (cf. the TRiSM downgrade and the over-correction in §6): an
unanchored attribution corrected at writing time rather than carried. The "interpretability"
framing previously cited to a review paper (TRiSM, 2506.04133) remains downgraded to
background — see §6.*

---

*Companion blog (the narrative): [`blog.md`](blog.md). Consolidated result tables:
[`data/results-tables.md`](data/results-tables.md). The format-agnostic corpus this
paper renders — every probe's full design and data — is [`00`](00-method.md)–[`08`](08-longitudinal-preference.md).*
