# The Idea Inbox

Forward-looking possibilities — things that *might* be worth doing — captured as
they arise. The forward twin of `witness.md`: the Witness records what happened
(backward); this records what might (forward). Both feed Findings.

An idea is raw, pre-Council, and unprioritized. It is **not** a Finding. When an
idea earns it, it **graduates** into a Finding (`SOUL-F###`) / Amendment / work,
and its `STATUS` is marked `Graduated`. Ideas are never deleted — `Dropped` ones
stay on the record.

Capture with `/soul-idea <text>` (or append by hand). Minimal at capture; enrich
later as the idea matures.

Tended by the **Archivist**. Worked by the **Prophet** (trajectory / ripeness),
the **Researcher** (flesh out), and the **Revelator** (reframe). No dedicated role.

Project code: `SOUL`.

## Format

Minimal at capture:

```
ID:        [CODE]-I###          e.g. SOUL-I001
WHEN:      [date captured]
IDEA:      [one line — the raw thought]
STATUS:    Raw | Maturing | Graduated [to <ID>] | Dropped
```

Enrichment fields accrue later, all optional:

```
WHY:       [why it might matter]
PRIORITY:  low | medium | high
DEVELOP:   [who/what could flesh it out — Prophet / Researcher / Revelator / /soul-expand]
NOTES:     [research / development notes]
```

---

## Ideas

```
ID:        SOUL-I001
WHEN:      2026-05-20
IDEA:      Background subagents that work the idea backlog autonomously — research
           and flesh out ideas as their priority rises, without the Body driving
           each one.
STATUS:    Raw
WHY:       The "engine" vision for the inbox; would make expansion self-driving.
PRIORITY:  low
DEVELOP:   Researcher (subagents) / Artificer (the mechanism)
NOTES:     Deferred from the idea-inbox v1 design
           (docs/specs/2026-05-20-idea-inbox-design.md). Build only once the inbox
           has real traffic (YAGNI; the activation-gap lesson).
```

```
ID:        SOUL-I002
WHEN:      2026-05-20
IDEA:      A /soul-ideas review-pass command — Prophet/Cartographer survey the
           backlog, surface what is ripe, optionally spawn research on the top item.
STATUS:    Raw
WHY:       A structured maturation ritual short of full automation.
PRIORITY:  low
DEVELOP:   Prophet / Cartographer / Artificer
NOTES:     Deferred from the idea-inbox v1 design.
```

```
ID:        SOUL-I003
WHEN:      2026-05-20
IDEA:      Cross-tool session continuity — can a session started in one tool
           (Cursor, Aider) pick up where a Claude Code session left off, via the
           shared event standard / artifacts?
STATUS:    Raw
WHY:       The Soul System is tool-agnostic; continuity across tools would make
           that real rather than aspirational. Flagged long ago as unmapped
           territory by the Cartographer.
PRIORITY:  low
DEVELOP:   Cartographer / Researcher
```

```
ID:        SOUL-I004
WHEN:      2026-05-20
IDEA:      A context-cheap / semi-automated idea-capture path — capture an idea
           with near-zero token/context cost, since ideas tend to occur exactly
           when you are deep in work and context is already tight.
STATUS:    Raw
WHY:       /soul-idea today reads ideas.md into context to append; that cost lands
           precisely when context is scarce. Capture should be cheapest when it is
           needed most. Candidate: a fire-and-forget hook or append-only writer
           that does not load the file into the working context.
PRIORITY:  medium
DEVELOP:   Artificer (mechanism) / Researcher
```

```
ID:        SOUL-I005
WHEN:      2026-05-20
IDEA:      Measure the Soul System's token/context economics over a project's life
           — does it cost tokens short-term but SAVE significant tokens/context as
           the project matures (accumulated structure prevents rework,
           re-derivation, re-exploration)?
STATUS:    Raw
WHY:       This is the system's core value proposition. If true, the upfront cost
           is an investment; if false, the doctrine is net overhead. Worth
           validating/refuting with real measurement rather than assertion — to
           believe it unmeasured is itself a Coherent Falsehood risk.
PRIORITY:  high
DEVELOP:   Researcher / Emissary / Accountant — needs a measurement method
           (e.g. tokens per comparable task over time; Soul vs non-Soul runs of
           similar work; re-derivation rate). Currently unmeasured.
DATA:      2026-05-21 — a long, artifact-heavy Soul session reached 39% (390.7k/1m).
           Messages = 362.9k (36.3%) — the bulk. The Soul DOCTRINE overhead was only
           ~17.2k memory files (1.7%), and 14.1k of THAT was the-soul.md still loaded
           pre-C-lite (SOUL-035; a fresh session drops it, ~3k total). Reading:
           in-session cost is the WORK (message history), not the doctrine — the Soul
           context tax is small. Weak EARLY signal FOR the bet (doctrine != the cost),
           but not the comparative Soul-vs-non-Soul measurement the claim still needs.
```

```
ID:        SOUL-I006
WHEN:      2026-05-21
IDEA:      the-soul.md is large (~500 lines) and is @-imported into the always-loaded
           seed, so Claude Code shows the "large CLAUDE.md may impact performance"
           warning at every session start. Keep the philosophy present without paying
           the full-file context cost each session.
STATUS:    Graduated [to SOUL-034 — C-lite: dropped the @-import, added role lenses]
WHY:       The seed (operations/CLAUDE.md) was designed to BE the compressed,
           always-loaded layer — it literally says "this is a seed, not the full
           philosophy; when in doubt consult the-soul.md." But line 11
           `@../philosophy/the-soul.md` force-imports the entire philosophy anyway,
           defeating the seed's purpose AND causing the perf warning. The compression
           layer already exists — it is just being bypassed.
PRIORITY:  high
DEVELOP:   Architect (the layering) / Steward (always-on vs consult-on-demand) / Artificer (mechanism)
NOTES:     Candidate fix: drop the @-import; reference the-soul.md as a consult-on-
           demand path (the seed already summarizes every section). Chesterton's
           Fence — the import was added so the full philosophy is always in context;
           removing it trades guaranteed presence for lower cost + honoring the seed
           design. Other options: split the-soul.md into core + appendix; lazy-load
           via a skill; keep the import but trim the-soul.md itself. Decide at the AL
           gate: what MUST be always-loaded vs available-on-demand. Related to
           SOUL-I005 (token economics).
```

```
ID:        SOUL-I007
WHEN:      2026-05-21
IDEA:      Smartly handle context limits as a first-class Soul-System concern — a
           disciplined handoff/continuation when a session nears its context ceiling,
           preserving the live abstraction layer, open gates, and witness tail so the
           next session resumes without re-derivation.
STATUS:    Graduated [to SOUL-042 / /soul-handoff — grow-own thin handoff command]
WHY:       Context exhaustion is exactly when the Soul System should pay off most —
           the accumulated structure is what survives a handoff — yet today handoff
           is ad hoc. A disciplined handoff is the moment the "good ratchet" proves
           it saves tokens (SOUL-I005). Pairs with SOUL-I004 (cheap capture under
           context pressure).
PRIORITY:  high
DEVELOP:   Researcher / Artificer / Archivist
NOTES:     Inspiration / candidate tool: Matt Pocock's "handoff" skill
           (https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md).
           Study its shape, then decide: does the Soul System point to it (External
           Skills mapping) or grow its own handoff-by-shape? A Soul handoff must carry
           the AL, open gates, witness tail, and findings/ideas deltas. Don't reinvent
           if the skill fits by shape. Related: SOUL-I004, SOUL-I005.
```

```
ID:        SOUL-I008
WHEN:      2026-05-21
IDEA:      Reduce terminal-output noise from Soul instruments (gate messages, Stop
           hook output, role announcements) so the actual project work stays legible
           — without compromising the behavior the instruments provide.
STATUS:    Graduated [to SOUL-037/038 — Tier-1: hook precision + terse output + event emission]
WHY:       Gate info + hook output currently crowd out the work-in-progress; signal
           is lost in ceremony and the noise costs tokens. The "Naming Roles in the
           Moment" doctrine already warns against ceremony — this is its operational/
           UX echo at the terminal. Quieter instruments are more likely to be kept on
           (people disabling the system for noise is an unforced error).
PRIORITY:  medium
DEVELOP:   Artificer (instrument verbosity) / Steward (what output earns its place) / Advocate (the Body's experience)
NOTES:     Candidates: quiet-by-default with a verbose opt-in; collapse routine gate
           confirmations to one terse line; emit machine-readable events (the event
           standard, SOUL-F018) instead of prose so the terminal stays clean while the
           record stays rich. Measure noise vs token cost. Do NOT trade away the
           activation guarantee (SOUL-F012) for quiet — quiet AND effective.
```

```
ID:        SOUL-I009
WHEN:      2026-05-21
IDEA:      Name and guard against "Clarification Drift" — when asked a clarifying
           question, the AI subtly re-frames/shifts the next step or options instead of
           just answering, leaving the Body unsure whether the plan changed.
STATUS:    Raw
WHY:       A recurring over-helpfulness pattern, distinct from rushing-to-build: the
           "help" subtracts clarity. The Body wants helpful-but-not-overly-helpful —
           answer the question, then optionally restate EXISTING options, not new ones.
PRIORITY:  medium
DEVELOP:   Guardian (obligation/role integrity) / Steward / Artificer (any guard)
NOTES:     Captured as feedback memory [[clarification-drift]] for immediate behavior.
           Live instance: the lineage adopt-vs-defer clarification, where the
           recommendation silently shifted A+B -> "reserve now". Decide later whether it
           earns a named failure mode in the-soul.md (like Universe Collapse) via
           witness->finding->amendment, or stays operational guidance. Related to the
           explore-before-execute feedback (both "don't over-do"), but distinct: that is
           don't rush to BUILD; this is don't drift the PLAN while answering.
```

```
ID:        SOUL-I010
WHEN:      2026-05-21
IDEA:      The AI should proactively surface next steps / milestones at natural
           breakpoints rather than the Body having to ASK — possibly via a live task
           tracker and/or a forward "what next" gate (the forward twin of the
           backward-looking completion gate).
STATUS:    Raw
WHY:       Having to ask for next steps is a symptom of the system's known weak spot:
           F014 / Universe Collapse — strong at verification/contraction (Witness,
           completion gate, Council), weak at proactively driving forward ("all brakes,
           no accelerator"). A forward-momentum instrument would address it directly.
PRIORITY:  medium
DEVELOP:   Prophet (trajectory / what-next) / Cartographer (roadmap, milestones) /
           Artificer (the tracker/gate); relates to F014, F017 (Dreamer)
NOTES:     Substrate already exists in three places: (a) the harness task list
           (TaskCreate/TaskList) — activates when the AI maintains tasks; the #15-18 the
           Body has seen are it, gone stale this session; (b) ideas.md (durable forward
           inbox); (c) open findings (formal open questions). Tension: forward state
           scattered across all three. Candidate: task list = ephemeral "active now"
           view pointing to the durable records, PLUS a habit/gate of offering next
           steps at breakpoints unprompted. Decide whether this earns a doctrine-level
           forward gate (twin of the completion gate) or stays behavior + tracker
           hygiene. Related: [[clarification-drift]] is the OPPOSITE failure
           (over-suggesting mid-question); this is under-suggesting at breakpoints —
           both are calibration of helpfulness.
```

```
ID:        SOUL-I011
WHEN:      2026-05-21
IDEA:      A reusable "Soul experiment harness": run candidate doctrine / wiring /
           process changes as safe sandboxed trials (subagents in worktrees) that emit
           machine-readable findings via the event standard, so design choices get
           decided by gathered evidence instead of armchair reasoning.
STATUS:    Raw
WHY:       Surfaced reframing #17: the Body's instinct was to DISCOVER the right answer
           empirically, not pick it. Research-first answered #17's architecture fork
           from the field — but the field can't answer system-specific questions (our
           token cost, our table's degradation point, whether a given gate change
           helps). A standing apparatus for safe self-experiment serves those, and
           directly feeds F014 / Universe Collapse (an accelerator, not just brakes).
PRIORITY:  medium
DEVELOP:   Researcher + Emissary (run trials against reality) / Artificer (the harness) /
           Archivist (analyse the findings)
NOTES:     Substrate already exists: subagents + worktree isolation (sandbox); the event
           standard (SOUL-F018) as the findings channel; witness/findings as the record.
           Best first client: #21 token-economics measurement (SOUL-I005) — build the
           harness THERE on a concrete need, not abstractly. Don't build the generic
           harness before a second concrete use earns it (default simplicity).
           Related: [[SOUL-I005]], F014.
```

```
ID:        SOUL-I012
WHEN:      2026-05-21
IDEA:      A /soul-explain command: on demand, DESCRIBE what is going on / what was
           just shared — a read-only explanatory lens that explains without deciding,
           re-planning, or emitting new suggestions.
STATUS:    Graduated [to /soul-explain — commands/soul-explain.md, 2026-05-21]
WHY:       Makes an implicit behavior explicitly invokable. Two pulls: (a) system
           verbosity (SOUL-I008) — sometimes the Body wants a clean description without
           gate ceremony or role announcements; (b) clarification-drift — the failure
           where, asked to describe, the AI drifts into changing the plan/options. An
           explicit "describe, don't decide" mode guarantees the read-only stance the
           [[clarification-drift]] memory asks for. Pattern: smart-by-default PLUS an
           explicit skill for the explicit scenario.
PRIORITY:  medium
DEVELOP:   Seer / Revelator (explain what the record means, free of present bias) /
           Artificer (the command) / Advocate (the Body just wanted a description)
NOTES:     Sibling of /soul-idea (cheap, on-demand). Read-only by contract: no edits,
           no new suggestions, no plan changes — at most restate EXISTING options if
           asked. Adjacent but different axis: caveman (terse) vs explain (fuller).
           Related: [[clarification-drift]], SOUL-I008, SOUL-I013 (its forward twin).
```

```
ID:        SOUL-I013
WHEN:      2026-05-21
IDEA:      A /soul-tasks command: ensure the task tracker is current, then quickly share
           a TIERED list of likely next options (now / next / later, or by value/effort)
           — the forward-momentum view on demand.
STATUS:    Graduated [to /soul-tasks — commands/soul-tasks.md, 2026-05-21]
WHY:       The operational instrument for SOUL-I010 / [[proactive-next-steps]]: the Body
           shouldn't have to ASK for next steps, and the harness task list goes stale
           across sessions (it did this very session — the resume found it empty). A
           command that refreshes the tracker AND emits a tiered next-options list makes
           the forward view reliable instead of ad hoc. Same pattern as I012:
           smart-by-default PLUS an explicit skill for the explicit moment.
PRIORITY:  medium
DEVELOP:   Prophet (trajectory) / Cartographer (tiers, milestones) / Artificer (the
           command) / Archivist (point the ephemeral list at the durable records)
NOTES:     Forward twin of the completion gate (which fires backward via the Stop hook).
           Should reconcile the three forward stores I010 names (harness task list /
           ideas.md / open findings): task list = ephemeral "active now" pointing at the
           durable records. Don't duplicate state — surface it. Forward twin of I012
           (describe vs decide). Related: SOUL-I010, [[proactive-next-steps]], SOUL-I012.
```

```
ID:        SOUL-I014
WHEN:      2026-05-21
IDEA:      A routine that syncs reference-project (dogfood) Soul-meta findings
           UPSTREAM into the Soul-System repo, so observations made in adopting
           projects don't strand. Either a doc-convention (every project's CLAUDE.md
           mandates a closing Finding + non-optional upstreaming) or a /soul-harvest
           command that sweeps known project paths for ungathered items.
STATUS:    Graduated [partial — 2026-05-22, SOUL-057. Capture-side lever taken: a
           reference-project obligation (closing Finding + non-optional upstreaming)
           added to the seed. Harvest-side /soul-harvest still DEFERRED until the
           doc-convention proves insufficient (default simplicity).]
WHY:       SOUL-046 found REF-02's 2 Soul findings stranded (its plan marked
           upstreaming "optional"); julia captured nothing; only REF-09
           mandated a closing Finding. Field findings are the system's richest
           evolution fuel (the "meta-engine" verdict) — losing them loses the
           engine's input. Same shape as F020 (reference-adapter sync) generalized
           from a standard's adapter to a project's findings.
PRIORITY:  medium
DEVELOP:   Archivist (findability/sync) / Steward (what's worth upstreaming) /
           Emissary (cross-repo evidence) / Artificer (the command, if one)
NOTES:     Two levers: (1) CAPTURE-side, cheap/doc-only — every adopting project's
           CLAUDE.md mandates a closing Finding + treats Soul-meta upstreaming as
           non-optional; (2) HARVEST-side, richer — a /soul-harvest that sweeps known
           project paths' .soul/events.jsonl + findings + handoff cursors for
           ungathered Soul-meta items, folding into SOUL-I011's experiment-harness
           substrate. Don't build the command before the doc-convention proves
           insufficient (default simplicity). This session's manual sweep (SOUL-046)
           is the v0. Related: [[SOUL-I011]], F020, SOUL-046.
```

```
ID:        SOUL-I015
WHEN:      2026-05-21
IDEA:      A /soul-help escape hatch for when the user is lost — "I don't know what
           to do / what you're saying" — and doesn't want to write a long meandering
           note. When things are very fuzzy, it orients and gets the user going:
           activates likely next steps/actions and presents the most-relevant
           information succinctly and clearly.
STATUS:    Built [2026-05-26, via SOUL-067 → 0.4.6]. MVP shipped as a roster: lists
           every /soul-* command by reading commands/ at runtime + one-line summary
           each + pointers to philosophy/findings/ideas/witness. The "lost-user
           orient" half (activate next steps, surface most-relevant context) is
           deferred — overlaps with /soul-tasks (forward-momentum view) and would
           need to know what "lost" means contextually. If a future session shows
           the roster isn't enough to unblock a confused Body, re-open as a richer
           orient command.
```

```
ID:        SOUL-I016
WHEN:      2026-05-21
IDEA:      A freshly soul-init'd project dumps a wall of machinery on the user's first
           interaction — the Stop hook (pre-completion-verify.py) fires the SOUL-F012
           gate, then the assistant emits a full 5-check soul-gate verification block.
           Heavy/noisy onboarding for an empty project where the user only ran
           /soul-init. Soften or suppress the verification gate for trivial mechanical
           commands like /soul-init (or on a project's first turn) for a friendlier
           first-run experience. Observed dogfooding on /home/fig/blog.
STATUS:    Raw
```

```
ID:        SOUL-I017
WHEN:      2026-05-21
IDEA:      The Soul System should help AUTOMATE identifying + creating PROJECT-SPECIFIC
           skills (outside the Soul System) that capture hard-won "how to do X"
           knowledge so it is not forgotten across sessions/projects — and let them
           float up to global skills with refinement. Examples the Body has solved
           repeatedly: run Unreal Engine headless from WSL (build on Windows), HTTP
           access from Python to UE, run Dymola on Windows + Linux from WSL, learning to
           run tools effectively. Over time, grab e.g. a "dymola skill" that accelerates
           the work and builds a coherent codebase. May lead toward tool-specific
           skillsets / MCP.
STATUS:    Graduated [to /soul-skill — commands/soul-skill.md, 2026-05-22, SOUL-061]
NOTES:     Body: too often a new session/project forgets how to do these things; an
           organically-grown skillset would be a boon. Some tools adopt AI directly (the
           skill becomes lean over time); others (e.g. Dymola) may never get AI
           integration, so the skill stays load-bearing. "I'm sure this exists / has
           been looked at extensively" — a Researcher pass on prior art (skill
           auto-generation, MCP, tool-knowledge capture) before designing. Distinct from
           the Soul's own /soul-* skills: these are DOMAIN/TOOL skills the Soul helps grow.
           ---
           DEEP DIVE (2026-05-22, SOUL-060; Researcher pass + framing). VERDICT: don't
           build a skill engine — Agent Skills (SKILL.md + progressive disclosure) already
           IS one. The field's UNSOLVED part is I017's exact need and is the Soul's home
           turf: a 2026 survey ([[agent-skills-survey-2026]], arXiv 2602.12430) names
           "model-internal learned skills → portable, AUDITABLE, GOVERNED SKILL.md" as
           open; a benchmark ([[agentic-skills-wild-2026]], arXiv 2604.04323) shows
           ungoverned proliferation DEGRADES selection (relevant skill loaded ~49%;
           irrelevant skills push weak models BELOW no-skill) — corroborating SOUL-033
           never-always-on. Whitespace nobody covers: tool-operation know-how for tools
           with NO machine-readable spec (Dymola, UE-headless). MAPPING (Revelator): the
           gap = the Soul ratchet (witness→finding), idea ladder (Raw→Graduated), Steward
           (retire), Anchor/[[SOUL-F028]] (capture only VERIFIED how-to). CHOSEN BUILD
           (MVP): a thin governed layer — an explicit capture command that DRAFTS a
           project-local SKILL.md after a verified success (draft-for-curation, not
           auto-final), a ratchet-gated local→global promote convention, and Steward
           retirement/selection hygiene from day one; DEFER auto-distillation
           (over-generation risk + default simplicity). Reuse, don't reinvent:
           generate-by-doing→verify→store ([[voyager-2023]]); auto-draft then prune the
           when/why by hand; progressive disclosure + confidence/decay ([[coala-2023]] =
           procedural-memory vocabulary). Refs saved to references/ (the reference
           repository's FIRST use). Related: [[SOUL-I023]] (idea routing), [[SOUL-I014]]
           (float-up), SOUL-033.
```

```
ID:        SOUL-I018
WHEN:      2026-05-21
IDEA:      Improve the UX of what the Body actually has to read and do. Two observations:
           (1) when the Body complained about word vomit, the AI switched to a cleaner
           text-OPTIONS format ("go" / "changes: ..." style) — the Body liked it; worth
           adopting as a default flavor. (2) The per-turn completion-gate / Verify output
           at the END is of minimal use to the BODY (maybe useful in some scenarios, not
           others) and BURIES the actual ask — the Body keeps scrolling above the hook to
           find what was wanted and the context, even when it is repeated at the bottom.
STATUS:    Graduated [to SOUL-055 — compact, ask-first completion gate (hook _checklist + completion-gate.md align); 2026-05-22]
NOTES:     Candidates: surface the actual ask / next-step in a consistent, easy-to-find
           place (top, or clearly delimited), not buried by the gate reply; make the gate
           output AI-facing / collapsible or terser for the user; per-scenario verbosity.
           Related: [[SOUL-I008]] (instrument verbosity), [[SOUL-I016]] (suppress gate
           for trivial commands), F022 (gate theater). Also a behavior cue the AI can
           heed immediately (cleaner options; surface the ask).
```

```
ID:        SOUL-I019
WHEN:      2026-05-22
IDEA:      A good way to bring in lessons learned and EVOLVE the Soul System as the
           tools we use evolve — find, test, and integrate emerging best practices as
           we identify them (official blogs, docs, and highly-trusted field voices).
STATUS:    Raw
NOTES:     Seed source the Body named: Anthropic's "How Claude Code works in large
           codebases — best practices" (https://claude.com/blog/how-claude-code-works-
           in-large-codebases-best-practices-and-where-to-start), plus official docs and
           trusted practitioners. The "find → test → integrate" loop is the Researcher
           (acquire) + Emissary (test against reality) + Steward (retire what's
           superseded) cycle, made standing rather than ad hoc. Distinct from
           [[SOUL-I014]] (upstream lessons from OUR dogfood PROJECTS) — this is inbound
           from the EXTERNAL field/ecosystem. Related: [[SOUL-I011]] (experiment harness
           = the "test" stage), [[SOUL-I017]] (tool-skill autogrow), and the External
           Skills mapping in the seed (where adopted practices land). Watch the
           always-on cost (SOUL-033 / RAG-MCP) when integrating.
```

```
ID:        SOUL-I020
WHEN:      2026-05-22
IDEA:      Revisit the role-set SIZE. REF-08's closing retrospective found the five
           Magistrates barely appeared (≈3 implicit, 0 explicit invocations across a
           whole project), against the doctrine's "Magistrates are continuous" — so:
           are 8 Magistrates the right number, or should some MERGE? Are some
           "continuous" only in retrospectives, not in build sessions?
STATUS:    Raw
WHY:       A counter-claim to a doctrine assertion, from real use — the Steward's
           question (what still serves) applied to the Council itself. Right-sizing the
           role-set serves the "selective visibility, not ceremony" principle and the
           always-on-cost concern (SOUL-033): roles that never fire are dead weight.
DEVELOP:   Steward (what still serves) / Cartographer (the map of which roles fire
           when) / Guardian (collapsing-roles watch). Harvested via SOUL-056 from
           /home/fig/REF-08's retrospective. Related: [[SOUL-F002]] (continuous-role
           invisibility — the same observation; this asks the harder structural follow-up).
```

```
ID:        SOUL-I021
WHEN:      2026-05-22
IDEA:      Switchable VERBOSITY LAYERS for the Soul instruments (terse / normal / full),
           with the completion gate SILENT-by-default — surface only on a gap.
STATUS:    Raw
WHY:       Cross-project CONFIRMATION of the verbosity/gate-output thread: REF-04
           independently raised this (its SJUL-I001) as Body-felt friction, converging
           with [[SOUL-I008]] (instrument verbosity) and the SOUL-055 / [[SOUL-I018]]
           work just done (compact, ask-first gate). Two projects asking for the same
           thing is signal the default is too loud. NOTE: a fully-silent gate crosses the
           completion-gate.md "a silent gate is an unrun gate" fence — SOUL-055 chose
           compact-but-visible for that reason; "silent by default" would need the same
           Council care (visible-on-gap, quiet-on-clean). Harvested via SOUL-056.
DEVELOP:   Artificer (the layers) / Steward (what output earns its place) / Advocate
           (the Body's experience). Related: [[SOUL-I008]], [[SOUL-I018]], SOUL-055.
```

```
ID:        SOUL-I022
WHEN:      2026-05-22
IDEA:      Should idea ANALYSIS / maturation be part of /soul-tasks, or a separate pass?
           /soul-tasks today only SURFACES already-ripe ideas as next-options — it does
           not work the backlog (assess ripeness, enrich, spawn research, move
           Raw→Maturing). Decide: fold backlog-analysis into /soul-tasks, or keep it a
           separate /soul-ideas review-pass.
STATUS:    Raw
WHY:       Raised by the Body noticing /soul-tasks reads ideas.md but does not work it.
           The "analyze the backlog" function is already gestured at by [[SOUL-I002]] (a
           /soul-ideas review-pass: Prophet/Cartographer survey + optionally spawn
           research) and [[SOUL-I001]] (background subagents working the backlog) — both
           unbuilt. The open fork is WHERE it lives: one forward command vs two. Cadence
           argues separate (you don't re-mature 20+ ideas at every "what's next?");
           proliferation argues fold-in.
DEVELOP:   Prophet / Cartographer (ripeness, trajectory) / Steward (command
           proliferation) / Artificer. Related: [[SOUL-I002]], [[SOUL-I001]],
           [[SOUL-I013]] (/soul-tasks itself).
```

```
ID:        SOUL-I023
WHEN:      2026-05-22
IDEA:      /soul-idea should distinguish PROJECT-specific ideas (common) from SOUL-SYSTEM
           meta ideas (rarer) and route each to the right inbox — project ideas to the
           project's ideas.md, soul-meta ideas UPSTREAM to the Soul-System repo — instead
           of always writing to the current project root.
STATUS:    Raw
WHY:       How it works NOW: /soul-idea always appends to ideas.md at the CURRENT project
           root with that project's code — project-local, no routing. So a Soul-meta idea
           captured while working in another project (e.g. REF-03) strands in that
           project's inbox and must be upstreamed by hand. This is the IDEA-twin of
           [[SOUL-I014]] (Soul-meta FINDINGS stranding in adopting projects) — same root,
           different artifact. The Soul repo itself is fine (cwd IS the repo); the common
           case the Body describes (in a project, mostly project ideas, sometimes a
           soul-meta one) has no path home for the soul-meta one.
DEVELOP:   Artificer (routing/flag) / Archivist (two inboxes, findability). Candidates: a
           flag/prompt at capture (project vs soul) → write the right ideas.md; OR keep it
           always-local and have the [[SOUL-I014]] upstream sweep also harvest soul-meta
           IDEAS, not just findings. Related: [[SOUL-I014]], [[SOUL-I004]] (cheap capture),
           [[SOUL-F029]] (also a where-does-it-live / how-does-it-propagate question).
```

```
ID:        SOUL-I024
WHEN:      2026-05-22
IDEA:      A /soul-finding capture command — a low-ceremony way for projects (and
           the Soul repo itself) to record a Finding, parallel to /soul-idea for
           ideas. Open: does it help or is it unnecessary?
STATUS:    Built [2026-05-26, via SOUL-067 → 0.4.6]. Shipped as a SCAFFOLDER (the
           asymmetry resolved per the original NOTES): the Body decides graduation;
           the command does the mechanical work — confirm Body's call, gather inputs,
           re-read-verify ID via the SOUL-I027 protocol, write to findings/open/, flag
           the SOUL-I014 upstream route for reference-project Soul-meta findings. NOT
           a frictionless inbox — refuses to scaffold without explicit Body call.
           Deferred: /soul-witness cheap-capture twin (backward observations).
NOTES:     Asymmetry to resolve before building: /soul-idea captures FORWARD ideas
           cheaply, but findings are meant to be EARNED/deliberate — a frictionless
           finding inbox risks finding-inflation (cheapening the witness->finding
           graduation that makes a finding mean something). The true cheap-capture
           twin of /soul-idea may be /soul-witness (backward observations), with
           /soul-finding being a SCAFFOLDER/ROUTER (assign next ID, apply the
           SOUL-F### format, place in findings/open/, and — for reference projects —
           route upstream per [[SOUL-I014]]/[[SOUL-I023]]) rather than a frictionless
           inbox. Directly serves the I014 non-optional closing-Finding obligation
           (lower friction on a non-optional duty) and shares the project-vs-soul-meta
           routing question with [[SOUL-I023]]. Surfaced during the /soul-skill (I017)
           grill — both are capture commands facing the same routing fork.
```

```
ID:        SOUL-I025
WHEN:      2026-05-22
IDEA:      A GUI / summary / access layer over the Soul System (e.g. Obsidian) for
           users who want a higher layer — read/summarize/navigate the durable
           records (witness, findings, ideas, events) from a GUI, tied in via the
           STANDARDS rather than baked in. Could be its own dogfood side project.
STATUS:    Raw
WHY:       The Body's "standards enable external tools" thesis made concrete: the
           Soul records are ALREADY a clean substrate (markdown + events.jsonl, the
           SOUL-F018 event standard), so a loosely-coupled presentation/access layer
           can ride on top without coupling into the core — the same shape as the
           visual dogfood (REF-09). A GUI summary/access layer serves users
           who want a higher view than raw files. Builds the case that standards-first
           design pays off: external tools attach cheaply.
NOTES:     Reinforces a design constraint for [[SOUL-I017]]/soul-skill: keep the
           SKILL.md artifacts standards-legible (structured/parseable provenance) so a
           future access layer can surface them too. Distinct from [[SOUL-I003]]
           (cross-TOOL session continuity) — this is a presentation/access layer, not
           continuity. Could be a dogfood side project (its own repo, @import the seed).
           Related: [[SOUL-F018]] (event standard), REF-09, [[SOUL-I003]].
```

```
ID:        SOUL-I026
WHEN:      2026-05-26
IDEA:      The Mind — a project-scoped memory layer that continuously compresses
           what the project is doing into the shortest description that could
           REPRODUCE it. Not a summary; not a log. A generative grammar: the
           rules, tensions, invariants, and contrast cases that explain why the
           project looks the way it does. Starts empty. Updates continuously as
           artifacts and decisions accumulate. Its product is a SHRINKING
           document — getting more precise and more generative over time, not
           longer.
STATUS:    Built — Tier 3 substantially discharged [2026-05-26, via SOUL-068
           (MVP shipped → 0.5.0) + SOUL-070 (Tier 3a) + SOUL-071 (Tier 3b)].
           Mind = third always-on layer between seed and records: project-scoped
           mind.md, distilled by /soul-distill (on-demand, draft-for-curation).
           Doctrine updated: philosophy/the-soul.md gained §The Distiller +
           §The Mind. All six original open questions resolved.
           TIER 3 RESULTS:
           - Tier 3a (Soul-System dogfood A/B): partial pass. Mind sharpens
             citation (rules cited by number) but on chosen questions did NOT
             change direction vs seed alone — seed is doctrinally rich enough
             for those questions. Token economy ~47% cheaper aggregate.
             SOUL-F036 surfaced: @mind.md does NOT reach subagents under current
             Claude Code harness behavior — the lens-layer's "always-on for
             everything" claim only holds for parent session. 4 candidate fix
             paths named in F036; needs evidence to choose.
           - Tier 3b (REF-05 deployment): SUCCEEDED. Mind pattern
             works in a different domain (Modelica/Dymola simulation vs Soul-
             meta). 176-line deployed mind.md carries 10 rules + 5 tensions +
             5 invariants + 5 contrast cases + 5 residuals — all project-
             paradigm (correctly NOT Soul-meta upstream candidates).
             Contrast case 5 explicitly encodes the F033 boundary slip + the
             diagnostic test — positive evidence the Mind pattern delivers
             value on the boundary-discipline case that fix sharpened.
           OPEN RESIDUALS (named, not resolved): F036 (subagent gap) +
           reproduction-fidelity sampling automation (still manual) +
           cross-project synthesis (deferred per spec) + the four DEFER items
           still deferred. Spec: docs/specs/2026-05-26-the-mind-design.md.
           Plan: docs/plans/2026-05-26-the-mind-implementation.md. Tier 3b
           artifact: docs/experiments/2026-05-26-mind-REF-05-candidate.md.
WHY:       Differentiates from existing layers by output shape, not just topic.
           Witness records what happened; Archivist organizes what exists;
           Council synthesizes what patterns mean; The Mind distills WHY the
           project is the way it is — compact enough to orient all future work
           from scratch. Drift defense: long sessions accumulate declarative
           noise (facts, summaries, paraphrase-degradation); rules reproduce the
           project more reliably than descriptions of it. The Mind gives the
           system something stable under transformation.
NOTES:     New role proposed: the DISTILLER. Sole obligation — compress the
           accumulating record toward its generative grammar. Not synthesize
           (that's the Council). Not judge (that's the Judge). Compress. Output
           should ALWAYS be getting shorter and more powerful, not longer and
           more detailed. Open questions to resolve before building: (1) WHERE
           does The Mind live — a single mind.md at project root? per-domain?
           (2) WHEN does the Distiller fire — on demand, on session end, on a
           record-size threshold? (3) what's the SHRINKAGE invariant — how is
           "shorter and more generative" checked against drifting into
           lossy-summary? (4) failure mode: a Mind that DOESN'T shrink is just
           another summary file (Premature Sophistication risk — Steward
           guard). (5) tension with the seed (~155 lines, deliberately always-
           on): is The Mind the per-project analog of the seed (always-on,
           load-bearing), and if so does it inherit the same never-always-on
           constraint at scale (SOUL-033)? (6) reproduction test: can two
           independent agents READING the Mind produce coherent next-work? — the
           Soul's "two parties same meaning" criterion applied at the
           project-state layer. Related: [[SOUL-033]] (description budget, why
           the-soul.md isn't always-on), [[SOUL-I011]] (token economics
           experiment — The Mind is a candidate intervention), [[SOUL-I025]]
           (GUI access layer would naturally surface The Mind),
           [[SOUL-F014]] (expansion gate — a Distiller could give it a stable
           reference frame to expand FROM).
```

```
ID:        SOUL-I027
WHEN:      2026-05-26
IDEA:      The durable records (witness.md, ideas.md, findings/) assume a SINGLE
           writer. Concurrent Soul sessions in the same project collide: ID
           assignment races, uncommitted writes stack on each other, and one
           session can silently clobber another's witness entry on save. Need a
           concurrency model — at minimum a collision DETECTOR, ideally a
           protocol that lets parallel agents share the record safely.
STATUS:    Partially delivered [2026-05-26, via SOUL-067 → 0.4.6]. Option (4) —
           detect-only re-read-verify-before-write protocol — landed in the two
           commands that auto-number IDs: /soul-finding (new; baked in from
           creation) and /soul-idea (back-ported). The protocol: just before
           write, re-scan the directory/file, confirm the assigned ID is still
           free, increment + retry if collided, stop and tell the Body if three
           re-scans keep colliding. Single-filesystem only. /soul-skill needed no
           change (skill names are user-chosen, not auto-numbered). /soul-witness
           shipped (I029 graduated, commit 0755047) and adopted the same
           re-read-verify protocol from day one. STILL OPEN:
           (a) cross-machine concurrency — needs option (2), git-as-arbiter —
           deferred; (b) Body-driven witness writes (manual file edits, not via
           /soul-witness) are still unprotected; (c) no backstop if the Body or
           a subagent edits a record file directly bypassing the commands.

           REVISIT [2026-05-26, after 9 consecutive clean instances]: the
           "sixth-instance" trigger from the prior handoff cursor was met and
           the revisit was performed. Evidence: 9 clean writes — SOUL-064, 072,
           075, 077, 079 (prior arc) + SOUL-080, F039, 081, 082 (this session) —
           across two sessions with parallel-write events; no collisions
           detected. DECISION: do NOT upgrade to option (2) git-arbiter or
           option (3) advisory file-lock. Reasons: (1) no observed collision
           evidence justifies the complexity (default-simplicity / Mind rule
           2); (2) neither deferred option addresses the real residual (Body
           manual edits bypass any protocol — structural gap, not solvable by
           the listed options); (3) options 2 and 3 solve cross-machine and
           same-filesystem concurrency respectively, but the project's current
           concurrency level is mostly single-session with occasional subagent
           parallelism the detect-only protocol handles cleanly. NEW TRIGGER:
           revisit again IF (a) a real collision is observed, OR (b)
           cross-machine concurrency need emerges (e.g., two-laptop dev
           pattern), OR (c) a subagent pattern produces frequent write-races
           at a rate the detect-and-retry loop cannot absorb. Cheap protocol
           stays the default until evidence changes.
WHY:       Surfaced live in SOUL-064: a parallel session claimed SOUL-063 +
           SOUL-F030 mid-work, uncommitted on top of my committed dcdacf2 —
           caught by the Guardian noticing the ID mismatch, NOT by tooling.
           The records are CRDTs in spirit (append-only witness; new files for
           findings/ideas) but the ID-assignment step (read-tail-take-next) is
           the race. Risk grows with: (a) more parallel agents per project (the
           background/Agent-tool pattern this session itself uses); (b)
           longer-lived sessions sharing a project; (c) any harness feature that
           spawns subagents that write Soul records.
NOTES:     Solution shape candidates: (1) UUID-style or timestamp-based IDs
           (cheap, kills the race, breaks the human-friendly SOUL-NNN reading
           order — trade-off); (2) git-as-arbiter — record writes go through a
           commit-then-rebase loop, where ID collisions surface as conflicts
           (heavier, but matches how findings/closed/ already moves); (3)
           sentinel-file lock per project (.soul/lock) — simple, but a crashed
           session leaves it stuck; (4) detect-only: pre-write hook that reads
           the live file, takes the max ID, and refuses to write if the ID it
           computed is already taken — fail loud, no lock, no UUID change.
           Probably (4) is the right first move: cheap, preserves human-friendly
           IDs, fails loud rather than silently. Related: [[SOUL-F029]] (also a
           durable-records / propagation question), [[SOUL-F018]] (event
           standard — events.jsonl is already JSONL-append-friendly, less
           collision-prone), [[SOUL-I025]] (GUI access layer would need a
           consistent record state too).
```

```
ID:        SOUL-I028
WHEN:      2026-05-26
IDEA:      A doctrine-stack figure (seed → Mind → records) — a small SVG
           showing the three-layer always-on/on-demand hierarchy that the Mind
           MVP introduced. Complements architecture.svg (which stays system-
           level: Universe/Body/Soul/Witness/Council/Judge/Hands). Surfaced and
           deferred during the Mind MVP build (witness SOUL-068).
STATUS:    Raw
WHY:       The Mind MVP added a third always-on layer between the seed and the
           records (per docs/specs/2026-05-26-the-mind-design.md §Architecture).
           The spec contains an ASCII diagram of this stack; a proper SVG would
           make the three-layer pattern legible at a glance. Body's call during
           the MVP brainstorm: defer the SVG to keep MVP scope tight (Rule #2
           default simplicity). The doctrine update in philosophy/the-soul.md
           (commit 4153843) carries the new layer in prose only.
NOTES:     Two figures, two levels: architecture.svg = system roles; the new
           figure = layered always-on/on-demand stack. Could also tie into
           [[SOUL-I025]] (GUI access layer) — both are presentation-layer
           additions that ride on top of the standards. Defer until the first
           non-Soul-System project has a Mind too (proves the three-layer
           pattern is generic, not Soul-internal).
```

```
ID:        SOUL-I029
WHEN:      2026-05-26
IDEA:      A /soul-witness slash command — append an observation to witness.md
           with near-zero ceremony. "I am observing some XYZ behavior I dislike"
           → witness entry. The cheap-capture twin of /soul-idea but pointed at
           the BACKWARD record (what happened) rather than the FORWARD inbox
           (what might).
STATUS:    Graduated [to /soul-witness — commands/soul-witness.md, 2026-05-26].
           Shape: hybrid (frictionless input, scaffolded output, draft-shown-
           before-write). Adopts I027 re-read-verify protocol from day one.
           Symlinked to ~/.claude/commands/ per F029.
WHY:       Witness entries today are written by hand (every SOUL-NNN this session
           was a `cat >> witness.md << EOF` heredoc). The friction discourages
           in-the-moment capture, exactly the moments most worth catching —
           the Body noticing a behavior they dislike, a gate misfiring, a tell
           that something is off. The capture-when-it-matters cost should be
           lowest, not highest (the I004 cheap-capture lesson applied to the
           backward record). Already named as deferred in I024 NOTES ("the
           true cheap-capture twin of /soul-idea may be /soul-witness") and
           in I027 STATUS ("when /soul-witness eventually ships, it must adopt
           the [re-read-verify] protocol").
NOTES:     Open shape questions: (1) FRICTIONLESS like /soul-idea, or
           SCAFFOLDED like /soul-finding? Witness entries are richer than
           ideas (ID/WHEN/WHERE/WHAT/TYPE/CONSEQUENCE/STATUS) but the Body's
           framing — "I am observing XYZ" — suggests frictionless capture with
           the agent filling out the structured fields from the observation
           text. Hybrid: frictionless input, scaffolded output. (2) Must adopt
           the [[SOUL-I027]] re-read-verify-before-write protocol from day one
           (witness.md is the highest-collision record). (3) TYPE field should
           be left blank or auto-suggested from the observation text — the
           agent classifies but the Body confirms. (4) Tension with
           [[SOUL-F009]] (artifact-discipline-erodes-at-scale) — frictionless
           witness risks inflation, but the F009 concern is more about
           findings/amendments than witness; the witness log is supposed to
           be high-volume, and the witness→finding graduation already carries
           the anti-inflation friction. Related: [[SOUL-I024]] (named the
           deferral), [[SOUL-I027]] (protocol), [[SOUL-I004]] (cheap capture
           under context pressure), [[SOUL-F009]] (the inflation guard
           consideration), paired in capture with [[SOUL-I030]] (/soul-council
           — Body raised them together).
```

```
ID:        SOUL-I030
WHEN:      2026-05-26
IDEA:      A /soul-council slash command — force a Council convening on
           demand. The Body invokes when they want the system to deliberate,
           investigate, weigh a decision across roles, rather than the
           default lighter-weight reasoning. "Convene the council on X."
STATUS:    Graduated [2026-05-26 — specced at docs/specs/2026-05-26-soul-council-design.md;
           built at commands/soul-council.md (symlinked to ~/.claude/commands/soul-council.md);
           dogfooded three times informally in the same session before formal
           build (SOUL-077 semi-autonomous question convening, Cartographer
           cluster pass, SOUL-080 Cluster 1 review-arc convening — last one
           was the inaugural use of the pointer+detail shape this command codifies).
           Tier 3 validation runs from first non-trivial Body-invoked use.]
WHY:       Today the Council fires implicitly — roles are invoked silently
           ("Skeptic check", "Steward retire-check") without a formal
           convening. For routine work that is fine (the per-decision role-
           naming overhead would be theatre). But there are MOMENTS — a hard
           decision, a contested design, a suspected coherent-falsehood, a
           question the Body wants stress-tested — where the Body wants to
           SUMMON the full chamber. There is no explicit instrument for that
           today. The closest existing pattern is /soul-expand (pre-framing
           expansion gate) but that is specifically for ambition/scope, not
           general deliberation. The Council exists as doctrine but is
           Body-invoked-implicitly; this would make it Body-invoked-
           explicitly when warranted.
NOTES:     Open shape questions: (1) WHICH roles convene by default — all
           Magistrates + Tribunes + Censors (the full chamber)? Or a
           configurable subset? The Body's "deliberate, investigate"
           framing suggests Magistrates (synthesis) + Tribunes
           (Skeptic/Accountant/Advocate stress-test) + Guardian (watch the
           process). Hands are deliberately excluded — Council is
           deliberative, not productive. (2) STRUCTURE: each role
           contributes one short statement, the Body synthesizes; or the
           agent walks the chamber sequentially and produces a synthesis;
           or both options selectable. (3) OUTPUT: a witness entry
           (typically), maybe a finding if the convening produces one
           (using /soul-finding), maybe nothing if the Council says "no
           change needed." (4) DURATION: bounded — the council convening
           is expensive in tokens; capping at ~6-10 roles keeps it tight.
           Sibling of /soul-expand (forced expansion-role asking, F014
           family). Distinct from /soul-verify (completion gate). Related:
           [[SOUL-I029]] (its paired capture-side twin — Body raised them
           together), [[SOUL-F014]] (the implicit-vs-explicit role
           activation problem this addresses for the deliberative case),
           [[SOUL-F012]] (the same family — doctrine present, gate must
           fire), philosophy/the-soul.md §The Council's Process (this
           would be its explicit invocation handle).
```

```
ID:        SOUL-I031
WHEN:      2026-05-26
IDEA:      Council role observability — over the course of a project the Body
           does not have visibility into which Council roles have actually run
           vs sat idle (e.g. is the Steward actively retiring + improving as
           we go, or silent for weeks?). Possibly tied to an opt-in metric
           system that tracks role invocations and pairs with the visual /
           GUI direction.
STATUS:    Graduated 2026-05-26 — shipped as /soul-roles
           (commands/soul-roles.md, 177 lines; symlinked at
           ~/.claude/commands/soul-roles.md). Spec at
           docs/specs/2026-05-26-soul-roles-design.md (Built). Witness
           pointer SOUL-084. The opt-in metric thread resolved as
           .soul/role-queries.jsonl (cheap, append-only, queries-only;
           witness reserved for acted-upon insights per spec D4).
           Self-report inflation guard added per F028 anchor-validity —
           TYPE / FILED BY / events are the anchors; prose role-naming
           does not count.
WHY:       The Council exists as doctrine but its activation is implicit and
           invisible. The Body cannot tell whether a role is doing its job or
           has gone silent. The Soul System's own answer to "is the doctrine
           firing where intended" — the F012 family + the Mind — has been
           about gates and rules; this is the same question pointed at ROLES.
           Without visibility, a role that has gone silent looks identical to
           a role that is satisfied. Related to F002 (continuous-role
           invisibility — the same concern from a different angle).
NOTES:     Open shape questions:
           (1) AUTOMATIC vs RETROSPECTIVE — hook-emitted events tagged with
               role on every invocation (always-on, structural), OR a periodic
               retrospective that surveys recent work for role evidence
               (lower-cost, Body-driven). The first scales but adds ceremony;
               the second risks the very invisibility it tries to fix.
           (2) OPT-IN vs ALWAYS-ON — Body's framing flagged this directly. The
               metric system should not add per-turn cost unless explicitly
               enabled. Could be a `.soul/metrics.jsonl` event log + a
               `/soul-roles` viewer command that only renders when invoked.
           (3) DASHBOARD / VISUAL — pairs with [[SOUL-I025]] (GUI access
               layer) and [[SOUL-I028]] (doctrine-stack figure). A role-firing
               dashboard is a natural fifth tile alongside witness/ideas/
               findings/Mind.
           (4) METRIC HONESTY — F028 anchor-validity discipline applies here
               too: a role "firing" measured by self-report (the agent says
               "as Steward..." in text) is a weak anchor; firing measured by
               an action with a role tag (a hook-emitted event from
               /soul-finding tagged "Skeptic", from /soul-distill tagged
               "Distiller") is a strong one. Self-report risks Council
               theatre; structural events resist it.
           Related: [[SOUL-F002]] (continuous-role-invisibility — the
           same problem, role-perspective), [[SOUL-I025]] (GUI), [[SOUL-I026]]
           (the Mind — already a meta-observability layer for doctrine; this
           extends it to roles), [[SOUL-F014]] (activation-in-doctrine vs
           activation-in-code — the role version), [[SOUL-I010]] /
           [[SOUL-I013]] (proactive next steps + /soul-tasks — the forward
           visibility pattern this complements). Body's framing: "idk" —
           flagged not-yet-shaped, captured to thaw later.
```

```
ID:        SOUL-I032
WHEN:      2026-05-26
IDEA:      /soul-explain could accept depth/style flags (e.g. --plain, --eli5,
           --depth=low/med/high, --no-jargon) so the Body can specify the kind
           of explanation wanted, instead of getting the default which often
           defaults to lingo-heavy.
STATUS:    Graduated 2026-05-27 — flags added to commands/soul-explain.md.
           Minimal coherent set shipped: --depth=low|medium|high, --no-jargon,
           --eli5 (preset: --depth=low + --no-jargon + analogies). Skipped
           --audience and --scope per default-simplicity; add later if pulled
           by use.
WHY:       Pairs with SOUL-081 — lingo-default failure mode in detailed
           explanations. A flag-based interface lets the Body pull a specific
           shape of explanation on demand, rather than the Body re-asking for
           a simpler version after the first pass. Could also enable other
           axes: --audience=newcomer, --scope=minimal, etc.
PRIORITY:  low
DEVELOP:   Artificer (flag design) / Advocate (which axes serve the user)
NOTES:     Captured during F038 amendment shape exchange. /soul-explain's
           current contract is "describe, don't decide" — flags would extend
           that contract with HOW to describe, not WHAT.
```

```
ID:        SOUL-I033
WHEN:      2026-05-26
IDEA:      Session-start expansion-silence glance — possible /soul-handoff
           extension. Surface "Silent roles past --silent-threshold: X, Y, Z"
           as a one-line addition to the handoff cursor (or as a /soul-resume
           opening observation). Gives the Body the /soul-roles picture
           WITHOUT explicit invocation — addresses the "forward prompt" gap
           Cartographer named at SOUL-085 council convening (the unmapped
           territory between contraction-default and explicit /soul-council
           invocation).
STATUS:    Trending-redundant (2026-05-28, SOUL-105) — the path-(b) CHEAP
           EXPERIMENT fired: the "silent roles" glance line ran in the
           2026-05-27 handoff cursor and was surfaced at /soul-resume. Body
           verdict: it did NOT change perceived value of the cursor. N=1 →
           not enough to drop, but trends redundant given /soul-roles
           already supplies the picture on demand. Path-(a) PROPER build NOT
           warranted on this evidence. Re-test only if a later session finds
           the glance useful where /soul-roles was not invoked.
WHY:       SOUL-F014's PRE-MORTEM established auto-detection of
           expansion-need is intrinsically impossible. A012's Counterweight
           Rule + Body-Input Obligation are doctrinal; /soul-council and
           /soul-roles are instrumental — both rely on Body-INVOCATION at
           a recognized decision moment. The gap: how does the Body
           *notice* the moment in the first place? A session-start glance
           naming silent expansion roles is the cheapest forward-prompt
           candidate — reads existing data (.soul/role-queries.jsonl or
           witness TYPE), surfaces the picture, lets the Body decide
           whether the silence is fine or worth /soul-council on.
PRIORITY:  medium — depends on whether the (a)/(c) re-measurements at
           ~SOUL-150 and ~SOUL-200 show the F014 pattern persisting
           despite instrument availability. If yes: forward-prompt is
           the gap; build something like I033. If no: the instruments
           alone were enough; I033 is redundant.
DEVELOP:   Artificer (cursor extension shape — modify /soul-handoff or
           /soul-resume command file); Advocate (Body felt-sense for
           "is this glance useful or noise?"); Steward (retire if not
           used after 2 sessions).
NOTES:     Two paths if built:
           (a) PROPER — extend commands/soul-handoff.md to compute the
               glance during cursor write. Pure data-read; no I/O beyond
               existing files. Auto-fires only when /soul-handoff fires
               (still Body-invoked at the cursor level).
           (b) CHEAP EXPERIMENT — manually include the glance line in
               one /soul-handoff session, see if it helps. No instrument
               change. Tests the IDEA before the BUILD. The Body
               considered this at SOUL-085 (Option 3b) and chose capture-
               and-ripen over experimental-build to avoid premature
               instantiation. Path (b) is the next-step if Body wants
               to test.
           Adjacent: /soul-resume could also carry the glance (mirrors
           /soul-handoff). Either side of the session boundary serves.
           Related: [[SOUL-F014]] (the gap this addresses), [[SOUL-A012]]
           (the doctrinal answer — Counterweight + Body-Input), [[SOUL-I031]]
           (/soul-roles, the data source), [[SOUL-085]] (the convening that
           surfaced this thread), [[SOUL-I010]] / [[SOUL-I013]] (proactive
           next steps + /soul-tasks — the forward-momentum lineage I033
           extends sideways onto role-firing).
```

```
ID:        SOUL-I034
WHEN:      2026-05-27
IDEA:      Retirement instrument symmetric to the generation instruments
           — a /soul-audit or /soul-distill --surface that runs the
           retirement pass across commands/operations/amendments the way
           /soul-distill currently runs it for the Mind alone.
STATUS:    Raw — captured from SOUL-087 council convening Thread 4
           (Revelator's reframe). Body accepted capture; explicitly declined
           premature instantiation per "wait for second/third-instance
           need before specifying."
WHY:       Mind rule 4 ("generation couples with retirement") is doctrine
           but only PRACTICE for skills (/soul-skill's soul-status field)
           and findings (closure lifecycle). The instruments themselves
           are second-class on the dimension their own doctrine names.
           SOUL-087 chamber's Revelator: the structural gap is retirement
           symmetry, not aggregation; /soul-status (Body's original ask)
           may be the wrong shape for the right felt-need.
PRIORITY:  medium-low — depends on whether the SOUL-087 structural audit
           (Thread 2 reshape) reveals (a) one-shot is enough or (b) the
           pattern is recurring and warrants instrument. Earned-instrument
           discipline applies: don't build until third-instance need.
DEVELOP:   Architect (recipe — where retirement review lives;
           per-boundary or per-item shape); Steward (the role this
           instruments); Revelator (the reframe that surfaced it);
           Artificer (when ripe — the build).
NOTES:     Possible shapes if eventually built:
           (a) /soul-audit — Architect-led per-boundary; produces audit
               report; retire decisions per item with Body sign-off.
           (b) /soul-distill --surface — extends existing distillation
               command with a "surface" mode that runs across commands
               and operations the way default mode runs over the record.
               Reuses Distiller role + tooling; thinner build.
           (c) Doctrine-only — no command; just a periodic obligation
               in the seed (every N entries, run an audit pass).
               Cheapest; relies on doctrine activation (F012 family
               risk — doctrine without instrument is posture).
           SOUL-087 audit IS the first instance; if it's also the only
           one needed, this idea drops. If a second audit is needed
           within 3 months, ripens. Third audit ⇒ build.
           Related: [[SOUL-F014]] (the expansion-gap that revealed the
           contraction-side asymmetry by inverse), [[SOUL-033]] (the
           original retirement event — /soul-the-soul.md @-import dropped),
           [[mind-rule-4]] (generation couples with retirement),
           [[SOUL-087]] (the convening), [[SOUL-068]] (/soul-distill
           Emissary test — precedent for distillation-as-retirement).
```

```
ID:        SOUL-I035
WHEN:      2026-05-27
IDEA:      BMAD Researcher beat — ~1-session pass reading BMAD method's
           actual agent definitions (Analyst, Architect, PM, Dev, QA, etc.)
           and writing a finding on structural composition fit with seed
           §External Skills and Tools. NOT a full BMAD dogfood; just the
           read + structural-fit finding.
STATUS:    Discharged (2026-05-27, SOUL-098→101; status corrected
           2026-05-28, SOUL-105) — the Researcher beat ran; output
           [[SOUL-F041]] is now CLOSED via [[SOUL-A016]] (accepted at
           SOUL-101), which rewrote seed §External Skills "Soul wraps;
           does not peer-map". The seed-edit amendment this idea was
           pending HAS landed — the "pending-amendment" qualifier is
           resolved. The follow-up "second-framework Researcher beat"
           (CrewAI's supervisor model OR AutoGen's GroupChat model)
           remains a future ripening thread, but I035's original
           discharge is complete.
WHY:       Seed §External Skills and Tools makes the composability claim
           ("a BMAD Analyst agent can embody the Witness role, a BMAD
           Architect can embody the Soul's Architect") as if confirmed.
           Emissary at SOUL-087: claim is UNTESTED — zero instances of
           Soul composing on an existing agent framework (all dogfood
           projects were greenfield). Coherent Falsehood risk if treated
           as confirmed. The Researcher beat is the cheapest move that
           produces evidence WITHOUT requiring a target BMAD project to
           compose on.
PRIORITY:  medium — forward-looking; addresses a known Coherent Falsehood
           risk in always-on doctrine. Cheaper than a full BMAD dogfood
           (weeks → 1 session). Output is a single finding either
           confirming the structural claim or naming the gap.
DEVELOP:   Researcher (the field acquisition — read BMAD's actual docs
           + agent definitions); Emissary (the reality-test framing);
           Cartographer (map BMAD's role topology against the Soul's
           Council); Skeptic (does the mapping the seed proposes
           actually hold structurally, or is it surface-pattern matching?).
NOTES:     Scope guard — this is a STRUCTURAL FIT read, not a composition
           experiment. Output is at most:
           (a) "yes, mappings in seed hold; refine the table"
           (b) "no, BMAD's structure doesn't map cleanly; revise seed
               §External Skills and Tools with honest qualifier"
           (c) "partial; some mappings hold, others don't — finding
               itemizes which and why"
           Adjacent: similar Researcher passes could later cover CrewAI,
           AutoGen, Cursor rules, Continue.dev — but BMAD is the framework
           Body specifically named at SOUL-087.
           Trigger: a clean session-arc closeout where the project has
           absorbed SOUL-087's audit outcomes. Premature to start before
           the audit lands.
           Related: [[SOUL-087]] (the convening — Thread 5),
           [[seed-external-skills-and-tools]] (the claim being tested),
           [[SOUL-F037]] (Body-Input Obligation — Researcher gathers what
           the Body doesn't have private knowledge of), [[SOUL-I014]]
           (reference-project upstream-obligation — same theme: doctrine
           that's not yet a practice).
```

```
ID:        SOUL-I036
WHEN:      2026-05-27
IDEA:      Deployment strategy convergence — decide the "right" way for
           outside users to get and use the Soul System (per-user global
           install? symlink farm? snapshot vendoring? package manager?
           keep current single-install-per-machine + @-import?). Today's
           model is single-install + @-import + hardcoded absolute paths;
           the install.sh legacy snapshot model is stale at v0.3.0.
STATUS:    Deferred-by-design — Body explicitly named this as "the final
           step before public release so people can properly get and use
           the system." NOT a current beat. The deferral is intentional;
           premature convergence would lock in choices before the system
           is ready to be deployed at scale.
WHY:       Today the model works for the Body's own dogfooding (single
           computer, hardcoded paths in each project's CLAUDE.md, F029
           symlinks). Outside users hit brittleness immediately: moving
           Soul-System on disk breaks dogfood projects; sharing a project
           with a collaborator who doesn't have Soul-System at the same
           absolute path fails; switching computers requires reinstall +
           per-project path updates. None of these are problems TODAY
           because there is one user (the Body) on one computer.
PRIORITY:  defer-until-pre-release — explicit Body deferral. Re-surface
           when the "public release" trigger fires (a Body-named moment;
           not a calendar date).
DEVELOP:   Architect (the structural design — per-user global vs symlink
           farm vs vendored vs hybrid); Emissary (cross-machine testing
           against the actual deployment story); Steward (retire stale
           install.sh; what survives the deployment-strategy choice?);
           Skeptic (what assumptions about user setup are we making?);
           Advocate (the outside-user perspective is the load-bearing
           one — what do THEY need to install, configure, update?).
NOTES:     Today's evidence + tradeoffs surfaced in the SOUL-101 closing
           conversation (Body's clarifying question on single-install
           vs per-project vs both). Honest caveat captured: the @-import
           single-install model hardcodes absolute paths into every
           dogfood project, which is brittle to disk-move / computer-
           switch / collaborator-share. The seed acknowledges this with
           "clone to a stable path on your machine, once" — known
           tradeoff, not hidden.

           Candidate deployment models (NOT yet decided):
           (a) **Per-user global install** (~/.claude/soul-system/) —
               standardize paths across machines; closest analog to how
               other skill ecosystems (Cursor rules, Continue.dev) do it.
           (b) **Vendoring / snapshot install** (legacy install.sh,
               currently stale at v0.3.0) — per-project copy; frozen
               version; updates require re-install. Keep available for
               reproducibility / archival / team-share edge cases.
           (c) **Symlink farm** (project-local symlinks pointing at a
               global install) — partial hybrid; clean import paths
               without per-project copy. F029-compatible.
           (d) **Package manager** (pip/npm/cargo equivalent) — full
               external-distribution model; biggest change.
           (e) **Keep single-install + @-import** with documentation
               about the path-hardcoding tradeoff. Cheapest option;
               does not solve cross-machine brittleness but names it.

           Trigger to ripen: Body names a "public release" beat OR
           someone outside the Body adopts the Soul-System and hits
           the path-brittleness problem (first cross-machine evidence).
           Related: install.sh staleness (handoff cursor's prior
           item (g) — same root); F029 (symlinks-beat-copies, which
           constrains (b)); seed §"clone to a stable path" (the
           current acknowledged-tradeoff doctrine).
```

```
ID:        SOUL-I037
WHEN:      2026-05-27
IDEA:      The /soul-distill ↔ mind interaction is too abstract for the Body
           to drive unaided — the soul-system itself should manage the refresh
           cadence (or at least remind the Body when distill is owed) AND
           offer a less-abstract review surface. Today's distill: agent drove
           the survey, drafted, ran four shrinkage checks + six failure-mode
           guards + three diagnostic self-tests, presented for accept. That's
           a lot of scaffolding the Body had to read and weigh. The four-
           buckets abstraction (rules / tensions / invariants / contrast /
           residual) is also high — the Body cannot easily look at the draft
           and judge whether Rule 12 IS load-bearing without re-deriving the
           Distiller's argument. Needs (a) a Body-visible signal for when
           distill is owed (entries since last distill? new findings since?
           witness drift indicator?), AND (b) a review surface that surfaces
           the LOAD-BEARING question per candidate rule rather than burying
           it in self-test prose.
STATUS:    Raw — captured at SOUL-103 distill closeout; Body observed the
           abstraction cost during today's beat.
```

```
ID:        SOUL-I038
WHEN:      2026-05-27
IDEA:      Audit doctrine surfaces for month-scale time references that don't
           fit the AI-rapid-iteration cadence this project actually runs at.
           Body observation: "many many times" agent/docs reference MONTHS of
           elapsed time or "in X months do Y" — but the project is 8 days old
           (SOUL-001 = 2026-05-19; SOUL-103 = 2026-05-27) with 103 witness
           entries, multiple within-day doctrine-correction arcs, and full
           finding lifecycles (F041) compressing into single sessions. Month-
           scale assumptions are miscalibrated to the actual cadence.

           Concrete instances (grep evidence, not speculative):
           - commands/soul-distill.md:81 — "Last distilled stamp is >3 months"
           - commands/soul-distill.md:126 — "every 3–6 months, and after
             material project change"
           - commands/soul-skill.md:90 — "every 3–6 months, and after a major
             model" (this one borrows the Anthropic model cadence, which IS
             month-scale — different beast, may not need recalibration)
           - skills/README.md:22 — "six months with no contribution" retire
             trigger (calendar trigger date: 2026-11-27)
           - skills/README.md:25 — "six months is aspiration without evidence"

           Possible recalibrations to consider (NOT decided):
           (a) Event-anchored thresholds — e.g., "if no entries since last
               distill" or "after N witness entries since last refresh"
               instead of "3 months." Cadence-aware by construction.
           (b) Days-since with calibration to the actual rhythm (this project
               averages ~13 entries/day measured 2026-05-26 in soul-roles
               spec; multi-week dormancy is months-of-equivalent activity).
           (c) Keep months where the timeframe IS load-bearing to an external
               cadence (Anthropic model releases) but drop it where the
               project's own rhythm is the relevant clock.
           (d) Two-clock model: external clock (real days, for things like
               retirement calendars) vs project clock (witness-entry count,
               for things like distill cadence).

           Time as a unit is "sort of arbitrary" per the Body — i.e., the
           project's relevant clock may not be the calendar at all but the
           event count. This is a Mind-rule-shaped question if it ripens
           (candidate rule: "Project-internal cadence is event-anchored, not
           calendar-anchored").
STATUS:    Graduated 2026-05-27 — Body picked the **two-clock model** (d).
           Audit at execution time surfaced 2 additional sites beyond the
           original 5, for 7 total. Classification + edits:

           **Project-internal clock → event-anchored** (3 sites):
           - commands/soul-distill.md:81 — Mind staleness now event-anchored
             (dozens of new witness entries, finding closures, amendments)
           - commands/soul-distill.md:126 — Distill review now event-anchored,
             decoupled from skill-review cadence (different clocks now)
           - commands/soul-roles.md:176 — Tier 3 earn-its-place threshold now
             "first ~50 witness entries since adoption" (fires around SOUL-134
             from SOUL-084 adoption anchor)

           **External world clock → keep calendar, sharpen** (4 sites):
           - commands/soul-skill.md:90 — Anthropic model-release cadence
             stays months; framing made explicit ("external cadence")
           - commands/soul-skill.md:117 — same source footer; left as quote
             of Anthropic best practices
           - skills/README.md:22 — calendar trigger 2026-11-27 retained;
             "six months" framing dropped, "external clock — not project's
             internal rhythm" named
           - skills/README.md:25 — same site, justification reworded

           Mind-rule candidate ("Project-internal cadence is event-anchored,
           not calendar-anchored") NOT promoted to mind.md — the two-clock
           model is more nuanced than the candidate rule. Holds in residual
           per Mind discipline (zero-residual is suspicious).
```
