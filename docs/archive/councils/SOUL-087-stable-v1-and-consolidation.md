# Council convening — Soul-Console v1 stabilization: consolidation, metrics, BMAD meta-layer

**Witness ID:** SOUL-087
**Date:** 2026-05-27
**Invocation:** `/soul-council` (Body-invoked, post-Cluster-1 closure)
**Topic origin:** Body opened next session with a stabilization question rather than picking a thread from the cursor's menu. The framing names what the chamber has not yet faced as a single topic: the system has grown for ~6 weeks without a consolidation pass.

## Topic

Body wants to converge on a "stable Soul-Console v1." The framing names five threads:

1. **Major structural issues** blocking a "v1 stable" claim.
2. **Per-role / per-instrument dogfood-study** — are they actually firing, or are some present without earning their place? Metric-driven, the way the Mind was distilled.
3. **Guidance / skills / hooks coverage** — appropriate? gaps? redundancy?
4. **`/soul-status` proposal** — condense `/soul-tasks` (and possibly others) under one observability command to reduce user-facing surface area.
5. **Meta-layer composability** — how does the Soul System interact on top of advanced agent frameworks like BMAD?

The chamber walks all five threads, but the central tension Body named is **growth without retirement** — the system has only added.

## Chamber walked (10 roles — within 7–10 default)

- **Magistrates (5):** Archaeologist, Steward, Prophet, Emissary, Revelator
- **Tribunes (3):** Skeptic, Accountant, Advocate *(mandatory)*
- **Censors (2):** Guardian, Cartographer *(mandatory)*
- **Not invoked:** Seer, Archivist, Researcher (selected against). **Seer** would be self-defense — the topic includes the question of whether empirically-low roles still earn their place, and SOUL-085 set the precedent of excluding the audited role. **Archivist** fires high; record-keeping does not bear on consolidation directly. **Researcher** is the right voice for BMAD fieldwork but the topic is *whether to schedule that* — Emissary carries the "test what we claim" thread inside this convening. Hands (Architect, Craftsman, Artificer) never sit in council per seed.

## Magistrate statements

**Archaeologist** — *what already exists?*
The surface area, by direct count: 16 `/soul-*` commands (1571 lines), 10 operations files (1819 lines), 2 philosophy files (782 lines: `the-soul.md` 707 + `the-commons.md` 75), `mind.md` (~190 lines), 38 findings (24 closed, 14 open), 13 amendments accepted, 9 specs, 34 ideas, 86 witness entries. Hooks/ exists with two scripts (`pre-completion-verify.py`, `resume-cost.py`); `.soul/events.jsonl` shows active firing (gate.completion.flagged) — the hook channel is alive, not just specced. Cluster 1 instruments built in the last session-arc are the four largest commands (162–188 lines each). The system is no longer "young," but its retirement pass has not happened. **The lineage shows consistent growth + zero formal retirements outside of finding-closure.**

**Steward** — *what retires?*
Five immediate audit candidates, in declining suspicion order:
- `operations/council-synthesis.md` (350 lines) — the Council's authority/convening doctrine. Reads NOT-superseded: it governs *when* the Council can change doctrine; `/soul-council` is the instrument *within* that authority. Different layer. KEEP, but rename's worth a thought.
- `operations/autonomous-session-template.md` (269 lines) — likely pre-dates `/soul-handoff` + `/soul-resume`. Verify whether anything still imports/cites it. If superseded, RETIRE.
- `operations/completion-gate.md` (130 lines) — pre-dates `/soul-verify`. Likely superseded; check.
- `operations/event-standard.md` (202 lines) — defines the event format `events.jsonl` uses. Hook channel IS active, so this earns its keep; KEEP.
- `operations/reference-repository.md` (173 lines) — niche; verify whether reference-project doctrine still cites it or has migrated into seed §Reference Projects.
Beyond operations: the **growth-only pattern itself is the failure mode.** Mind rule 4 says "generation couples with retirement," but the project has only operationalized that for skills (`/soul-skill`'s `soul-status` field) — not for commands, operations files, amendments, or specs. **Steward's position: the audit pass is the obligation now overdue.**

**Prophet** — *where this leads?*
Three trajectories from today's branch:
- **(1) Continue current pattern.** By SOUL-200 the surface is 25+ commands, 15+ operations files, 20+ amendments. Always-on skill list bloats; new-agent onboarding degrades; SOUL-033's description-budget problem re-emerges at the command layer. The system that solved Always-On for doctrine fails Always-On for instruments.
- **(2) Build `/soul-status` as the consolidator.** Surface shrinks (3 commands collapse to 1); description budget reclaimed. Risk: thin-aggregator pattern hides three distinct contracts (`/soul-tasks` = forward, `/soul-roles` = observability, `/soul-explain` = describe). Aggregators accumulate concerns. The Mind precedent ≠ console — the Mind is *compressed-rules*; a console is *current-state-view*. Different shape.
- **(3) Audit-and-retire pass first; aggregation deferred.** Inventory what exists, retire what no longer earns, THEN ask whether `/soul-status` is needed against the trimmed surface. Path (3) is the cheap-first sequencing; path (2) becomes contingent on what path (3) reveals.
**Prophet leans (3).** Adding instruments to fix "too many instruments" is exactly the failure mode Body named.

**Emissary** — *what reality says?*
Reality data:
- `/soul-roles ran ONCE` total (one entry in `.soul/role-queries.jsonl`). The observability instrument exists but isn't routine.
- `/soul-council fired ONCE` (SOUL-085). `/soul-ask-body NEVER` fired yet.
- `events.jsonl` shows the hook channel IS firing (gate.completion.flagged on F012, today). One event type only.
- Body's framing — *"I've only seen growth, no consolidation"* — is itself empirical evidence the chamber must take seriously. The Body is the inhabitant; that report IS the universe-anchor for the felt-need.
- **BMAD reality-test:** the seed §External Skills and Tools claims a BMAD Analyst agent could embody Witness, an Architect could embody Architect, etc. **The claim is UNTESTED.** Zero instances of Soul composing on an existing framework (all dogfood projects were greenfield). Coherent Falsehood risk: the composability claim passes internal coherence and may not survive contact with BMAD's actual agent definitions.

**Revelator** — *what was always true but unseen?*
The asymmetry the Body named is structurally encoded: **generation has instruments (`/soul-witness`, `/soul-idea`, `/soul-finding`, `/soul-skill`, `/soul-handoff`), retirement has exactly one (`/soul-distill` for the Mind alone).** Mind rule 4 ("generation couples with retirement") is a *rule*, not a *practice*. The practice exists for skills (`soul-status` field) and findings (closure lifecycle) but NOT for commands or operations files. The instruments themselves are second-class on the dimension the doctrine names. **Reframe:** Soul-Console v1 doesn't need a console; it needs a **retirement instrument symmetric to its generation instruments.** The "/soul-status" Body is asking about may be the wrong shape — what's missing is a `/soul-audit` or `/soul-distill --surface` that runs the retirement pass across the surface the way `/soul-distill` runs it for the Mind.

## Tribune statements

**Skeptic** — *what's missing?*
**"Stable v1" is undefined.** The chamber cannot conclude an audit against an undefined criterion. Candidate criteria the Body must pick from:
- (a) **Description budget** — auto-loaded content under N tokens (seed + mind + always-on skill list).
- (b) **Empirical activation** — every instrument has ≥ M real Body-uses (not Tier-3-simulation).
- (c) **Doctrine completeness** — no open finding older than F-N; F014 closed; no orphaned roles.
- (d) **Onboarding ergonomics** — new agent reaches productive state in ≤ T turns from a fresh seed read.
- (e) **Reference-project upstream-flow clean** — all Soul-meta findings from dogfood projects upstreamed.
A012 §Body-Input Obligation fires here: the criterion is Body-only knowledge. **Chamber must ASK, not push.**

**Accountant** — *what does it cost?*
- **Audit pass** (Steward thread): ~1 session for inventory + retire-watch flags; ~1 more session to execute retirements. Cheap, bounded.
- **`/soul-status` build**: ~1 session + ongoing maintenance as instruments evolve.
- **`/soul-audit` or `/soul-distill --surface` instrument**: ~2 sessions including doctrine + recipe. Medium.
- **BMAD meta-layer test**: weeks. Requires either (i) an existing BMAD project to compose on, or (ii) building a BMAD-shaped skeleton to test against. Cost is *very high* without a target.
- **Right unit-economics:** cheap-first. Audit is the smallest move that produces evidence about whether further instruments are needed. BMAD-meta is the most expensive and benefits least from being done now (no target project).

**Advocate** — *what does the Body actually need?*
The Body's framing reveals **surface-fatigue** — 16 commands is a lot to hold; the system feels heavy. The Body's specific signals:
- *"I've only seen growth"* — wants to see retirement.
- *"do we need a /soul-status"* — wants felt-relief from surface bloat.
- *"how does Soul interact with BMAD"* — wants to know the system has a future composing outward, not closing inward.
The Body does NOT need the chamber to dismiss any of these. Each reflects a real felt-experience. **Advocate position:** take each thread, but sequence them honestly — audit FIRST (Body sees retirement happen, not just promise it), aggregator question SECOND (test on trimmed surface), BMAD meta-layer as a captured forward-thread (don't build now, but don't dismiss — name a beat for it).

## Censor statements

**Guardian** — *chamber integrity?*
Two integrity risks for this convening:
- **Self-congratulation risk** — the chamber is auditing the system the chamber is part of. Watch for "everything earns its place, minor tweaks." Force at least one concrete retire-watch flag with Body's blessing OR explicit "audit revealed everything earns place" with anchor.
- **New-instrument bias** — Body named "growth without retirement" as the failure mode; chamber's reflex is to propose *another instrument* (`/soul-status`, `/soul-audit`) as the answer. **Revelator's reframe is load-bearing here:** if we add a retirement instrument, it must REPLACE existing retirement-shaped work, not pile on top. Mind rule 4 must apply to its own enforcement.
- **Counterweight Rule fire confirmed:** the convening itself surfaces expansion voices (Steward, Revelator, Prophet) against the contraction default ("we just shipped Cluster 1, push and move on"). A012 §Activation Disciplines applied without ceremony. Body-Input Obligation also fires (Skeptic's "stable v1 undefined" → Body must answer).
- **No rubber-stamp:** Body's pre-position was a genuine open question ("where are we?"), not a decided plan.

**Cartographer** — *what's the map?*
**COVERED:**
- Doctrine: seed + `the-soul.md` + `the-commons.md` + `mind.md` + 13 accepted amendments.
- Generation instruments: `/soul-witness`, `/soul-idea`, `/soul-finding`, `/soul-skill`, `/soul-handoff`, `/soul-resume`, `/soul-init`.
- Observability: `/soul-roles` (1 run), `/soul-explain`, `/soul-tasks`.
- Deliberation: `/soul-council` (1 run), `/soul-ask-body` (0 runs), `/soul-expand`, `/soul-verify`.
- Distillation: `/soul-distill` (for Mind only).
- Help: `/soul-help`.
- Hook channel: `hooks/pre-completion-verify.py`, `hooks/resume-cost.py`, `.claude/settings.local.json`, `.soul/events.jsonl` active.

**ADJACENT (named but thin):**
- Cluster 1 dosage — instruments built; usage near-zero (the cursor's own observation).
- Composition claim — seed §External Skills and Tools makes specific claims; no instance.

**UNMAPPED:**
- **"Stable v1" criterion** — Body's call.
- **Retirement instrument** for surface (commands/operations) — Revelator's reframe; no current shape.
- **Cross-framework dogfood** — every project has been greenfield; never on top of BMAD/CrewAI/AutoGen.
- **Event-type coverage** — `events.jsonl` has one event type only (gate.completion.flagged). Other gates fire silently; whether they should emit events is undecided.

## Tensions

1. **Steward ↔ Archaeologist — retire vs preserve hard-won record.**
   Steward: `autonomous-session-template`, `completion-gate`, possibly `reference-repository` are retire candidates. Archaeologist: each carries history; some may still load-bear in ways not surfaced in `grep`. **Resolution:** audit, don't speedrun. Each candidate gets a one-pass "still earning?" check with retire-watch flag if borderline; deletion is a separate Body decision.

2. **Advocate ↔ Guardian — `/soul-status` as felt-need vs new-instrument bloat.**
   Advocate: Body asked; take it seriously. Guardian: adding instruments to fix instrument-bloat is the failure mode. **Resolution (with Revelator):** `/soul-status` is the *symptom-articulation*, not the answer. The right move is to audit existing surface first, then ask whether aggregation is needed against trimmed surface OR whether a *retirement* instrument is the genuine gap (different shape).

3. **Prophet ↔ Accountant — consolidation vs BMAD meta-layer priority.**
   Prophet: BMAD-meta is forward-looking; closed-garden risk. Accountant: BMAD-meta costs weeks; consolidation is cheap and addresses immediate felt-need. **Resolution:** sequence. Audit-and-retire first (cheap, immediate, evidence-producing); BMAD-meta as a captured beat with a Researcher pass (1-session read of BMAD's actual structure → finding on fit) before any composition dogfood is proposed.

4. **Skeptic ↔ Body — "stable v1" criterion is undefined.**
   Skeptic: criterion needed. A012 §Body-Input Obligation: this is Body-only knowledge. **Resolution:** chamber surfaces candidate criteria (a)–(e); Body picks or composes. Without this, threads 2 and 3 are unbounded.

5. **Revelator ↔ Steward — what the missing instrument actually is.**
   Revelator: a retirement instrument symmetric to generation is the structural gap; `/soul-status` would be the wrong shape. Steward: maybe; first the audit *itself* might suffice as one-shot beat without needing an instrument at all. **Resolution:** run the audit AS the one-shot beat; if the pattern repeats (multiple audit passes needed over coming sessions), instrument it then. Earned-instrument discipline (don't build until pattern is third-instance).

6. **Emissary ↔ Revelator — meta-layer claim status.**
   Emissary: zero instances; aspirational. Revelator: the doctrine IS structurally composable; that's the claim's nature. **Resolution:** claim stands AS aspiration *labeled as such*. Scheduling a Researcher beat to read BMAD's structure produces a finding either confirming the claim or naming the gap. Treating untested claims as confirmed is Coherent Falsehood; treating structural claims as nothing-without-instance is too strict — the discipline is *label honestly*.

## Synthesis

The chamber's position has six threads, the first being load-bearing:

**Thread 1 (Body-Input, blocking the rest)** — **Body names the "stable v1" criterion.** Pick from (a) description budget / (b) empirical activation per instrument / (c) doctrine completeness / (d) onboarding ergonomics / (e) reference-project upstream-flow — or compose. Without this, threads 2 and 3 are unbounded. A012 §Body-Input Obligation fires explicitly.

**Thread 2 (cheap, immediate, evidence-producing)** — **Audit pass across surface.** One-session beat: inventory each of 16 commands, 10 operations files, 2 philosophy files, 13 accepted amendments. One-line "earning its place?" check per item. Flag retire-watch candidates. NOT mass deletion — earned-retirement. **Steward leads; Archaeologist guards against speedrun deletion.** Output: a single audit report (probably at `docs/audits/2026-05-27-soul-console-v1.md`) listing keep / retire-watch / retire-now with one-line rationales each.

**Thread 3 (contingent on Thread 2 evidence)** — **Re-evaluate `/soul-status` against trimmed surface.** If audit retires 3+ operations files and confirms `/soul-tasks`/`/soul-roles`/`/soul-explain` each carry distinct contracts, `/soul-status` likely doesn't earn its place — separate is right shape. If audit reveals genuinely overlapping observability, aggregate. Earned design, not anticipatory.

**Thread 4 (Revelator's reframe — captured, not built now)** — **Retirement instrument symmetric to generation.** Idea-tier capture: `/soul-audit` or `/soul-distill --surface` shape. Wait for second/third-instance need before specifying. **Capture as SOUL-I034 if Body accepts the thread.**

**Thread 5 (forward-looking, deferred)** — **BMAD meta-layer Researcher beat.** Schedule ~1-session Researcher pass to read BMAD's actual agent definitions and write a finding on composition fit (does the seed's claim hold structurally?). NOT a full BMAD dogfood — that's expensive and needs a target project. Just the read + structural-fit finding. **Capture as SOUL-I035 if Body accepts.** Alternative: pure capture-and-park if Body wants to wait for a real cross-framework opportunity.

**Thread 6 (record-only)** — **Composition claim labeled aspirational.** Seed §External Skills and Tools currently states the BMAD-Witness, BMAD-Architect mappings as if confirmed. Until the Researcher beat (Thread 5), add a one-line qualifier ("structural claim; not yet tested against an instance"). Cheap; preserves intellectual honesty.

**Chamber position:** Thread 1 is the gate. Threads 2 and 6 are the cheap-first moves once Thread 1 lands. Threads 3, 4, 5 are sequenced after Thread 2 produces evidence.

## Body decision

[2026-05-27, post-grill] — **Synthesis accepted with criterion lock + Thread 2 reshape.**

**Pre-decision grill (recorded for posterity).** Body pushed back on Skeptic's five criterion candidates (a–e) as instrument-metric-flavored; reframed in product-engineering shape: **structure, standardization, usability, usefulness.** Chamber-Skeptic counter-pushed: not co-equal at v1 — pick the gate; dependency-order suggests structure → standardization → usability → usefulness. Body picked **structure** as the gate without hedging. Further grill narrowed within structure: five sub-levels (file layout, five-layers, record types, doctrine layering, role structure). Three identified as LIVE (file/directory layout, record-type taxonomy, doctrine-layer boundaries); two SETTLED (five-layers, role ontology — recent SOUL-085 audit). Body declined to single-out one of three live seams; "no strong opinion + no churn for churn's sake." Chamber read: all three are entangled; treat as one gate.

**Locked criterion.** Stable Soul-Console v1 = each of three live structural seams is either **RESOLVED** (decision committed to seed / mind / an ADR) or **EXPLICITLY DEFERRED** with criteria for resolution. NOT "everything in its right place" (perfectionism); "every seam has a decision OR a documented reason it's parked."

**Threads:**
- **Thread 1** — RESOLVED via structure-gate lock above.
- **Thread 2** — **ACCEPTED with reshape.** Originally Steward-led per-item audit; reshaped to **Architect-led per-boundary audit.** Per-boundary catches structural drift; per-item only catches surface bloat. Output: `docs/audits/2026-05-27-soul-console-v1-structure.md` with three sections (directory layout / record taxonomy / doctrine-layer boundaries). Each seam decision: KEEP-IN-PLACE / MOVE-TO-X / RETIRE-NOW (with Body sign-off) / DEFER-WITH-CRITERIA. Steward and Cartographer second voices; Archaeologist guards against speedrun deletion.
- **Thread 3** — STAYS CONTINGENT on Thread 2 evidence. Re-evaluate `/soul-status` after audit reveals what's actually overlapping.
- **Thread 4** — **CAPTURE as SOUL-I034.** Retirement instrument symmetric to generation. Wait for second/third-instance need before specifying.
- **Thread 5** — **CAPTURE as SOUL-I035.** BMAD Researcher beat. One-session read of BMAD's actual structure → finding on composition fit; not full dogfood.
- **Thread 6** — DEFERRED to post-audit. The seed §External Skills and Tools qualifier ("structural claim; not yet tested against an instance") applies only if the audit doesn't reshape the section. Avoid double-touching.

**The-commons.md decision (Body-volunteered candidate, verified WRONG premise).** Body proposed retire on "never used" grounds. Verification: `the-commons.md` has TWO entries (Entry 001 = source of mind rule 11 + seed §On This Document; Entry 002 = shaped CLAUDE.md @-import design). Slow-growth by design ("Further entries added as they are earned"). **Verdict: KEEP.** Archaeologist's "each candidate carries history" applied — Body's own "no churn for churn's sake" caution applied to its own premise. Recorded as the convening's first concrete don't-retire-yet sign-off, validating the per-boundary > per-item reshape.

**Next move.** Body authorizes the structural audit pass (Thread 2 reshape) as a separate beat. Output-only audit; no deletions/moves in same beat; retire-now decisions await explicit Body sign-off per item.

**Discharges:**
- A012 §Counterweight Rule — expansion voices surfaced against contraction default of "push and move on" ✓
- A012 §Body-Input Obligation — Skeptic's criterion gap + grill loop ran to Body's explicit answer (not push-past) ✓
- `/soul-council` Tier 3b advances (N=2 toward 3c) ✓
- F039 — `wc -l` anchored at write-time (177) ✓
- Archaeologist's "carry history" warning — the-commons.md verification IS the dogfood instance ✓

## Tier 3 discharge

This convening:
- **`/soul-council` Tier 3b/3c (partial)** — second non-routine Body-invoked convening. Different topic from SOUL-085 (stabilization, not F014 confirmation). Pattern reproduces: chamber-walk + tensions + synthesis + pointer+detail. Tier 3c (month-of-use earn-its-place) still pending but now has N=2 toward it.
- **A012 §Counterweight Rule fired structurally** — expansion voices (Steward, Revelator, Prophet) surfaced against the contraction default of "push and move on."
- **A012 §Body-Input Obligation honored** — Skeptic's "stable v1 undefined" surfaced as a Body-only dependency; chamber asks rather than pushing past.
- **F039 discipline applied** — `wc -l` anchored at write-time before witness pointer.

## Pointers

- **Cursor:** `.soul/handoff.md` (2026-05-26 closeout; this convening picks a different thread than the menu's nine, by Body's direct framing).
- **F014:** still open; this convening is one layer up (stabilization of the whole system, of which F014 is one resolved sub-thread).
- **Mind rule 4** (generation couples with retirement) — load-bearing for Revelator's reframe.
- **Seed §Reference Projects, §External Skills and Tools** — directly addressed by Threads 5 and 6.
- **`operations/council-synthesis.md`** — the layer above this command; convening authority doctrine. NOT a retire candidate.
- **`.soul/events.jsonl`** — hook channel is active; one event type.
- **Inaugural pointer+detail file precedent:** `councils/SOUL-080-cluster-1-review-arc.md`. **Second use:** `councils/SOUL-085-f014-confirmed-what-now.md`. **Third (this):** SOUL-087.

---

**Source:** Second non-routine Body-invoked `/soul-council` in the project, on the Body's "stabilization" framing post-Cluster-1 closure. **Convened:** 2026-05-27. **Status:** Synthesis lands; Body decision pending in §Body decision (update in place).
