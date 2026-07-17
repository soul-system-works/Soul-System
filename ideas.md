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
STATUS:    Graduated [partial — 2026-05-28, SOUL-106]. Sub-problem (b)
           review surface SHIPPED: /soul-distill step 8 now presents
           delta-only (new/changed entries vs the prior mind.md, unchanged
           collapsed) + a load-bearing verdict per entry + gap-only checks —
           the SOUL-055 completion-gate discipline applied to the Mind's
           review. Sub-problem (a) cadence signal DEFERRED — Rule 2 (one
           distill so far; no missed-distill evidence) + the SOUL-105 I033
           verdict (ambient forward-glances don't earn their place for this
           Body). Re-open (a) only if a distill is actually missed, and then
           on-demand (/soul-tasks line / --check flag), never ambient.
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

```
ID:        SOUL-I039
WHEN:      2026-05-28
IDEA:      Ship reusable utilities as a companion repo — take the learnings
           from REF-09 (or other high-value things the community
           repeatedly looks for) and turn them into reusable tools/utilities.
STATUS:    Raw
```

```
ID:        SOUL-I040
WHEN:      2026-05-28
IDEA:      Systematic empirical refinement pass — stress-test the system by
           spinning up dogfood projects and/or subagents to exercise member
           roles, skills, and hooks, validating that EACH aspect of the Soul
           System is actually useful and needed (vs dead weight).
STATUS:    Raw
WHY:       Recent phase has been BUILD (commands, the Mind, hooks). The Body
           points at the complementary phase: VALIDATE / PRUNE — the Steward's
           "what still serves?" applied systematically and backed by EVIDENCE
           rather than intuition.
DEVELOP:   Steward (what still serves) / Emissary (test beliefs against
           reality) / Cartographer (map which aspects fire vs idle) /
           Artificer (the harness + any skills/hooks) / Accountant (the
           token/effort cost of each aspect).
NOTES:     Umbrella over existing threads, NOT a duplicate: [[SOUL-I011]] is
           the MECHANISM (sandboxed subagent/worktree experiment harness) —
           and I011's own note says "don't build the generic harness before a
           SECOND concrete use earns it; best first client = token economics."
           This direction supplies that second concrete client (role/skill/hook
           usefulness), maturing I011. [[SOUL-I020]] is one target (role-set
           size — do the 8 Magistrates actually fire?); [[SOUL-I005]] is the
           value/token question; [[SOUL-F014]] is the activation evidence; the
           gap-only review rule deferred at N=2 could earn its 3rd instance
           here. Default-simplicity at execution: start with ONE bounded tracer
           experiment (e.g., role-firing on a fresh dogfood project), NOT the
           generic harness first. Related: [[SOUL-I001]], [[SOUL-I034]].
```

```
ID:        SOUL-I041
IDEA:      The baseline-BREAKING regime test — the one experiment that could
           overturn [[SOUL-A017]]. Construct tasks where a frontier baseline
           genuinely FAILS (not just "hard": expert-domain depth, far-longer
           horizon than a tracer, or deliberately a weaker/smaller model), then
           ablate roles/gates with/without. If a role supplies substance or
           reliability the broken baseline lacks → A017's value-locus is regime-
           specific and shifts back toward substance where the baseline breaks.
STATUS:    In progress — TWO probes done (2026-05-28). (1) Weaker-model arm
           ([[SOUL-110]]): substance returns NARROWLY on a broken baseline
           (integration-dependent, partial; single lenses form-only; HR2 anchoring
           C1-survived). (2) Generalisation to a 2nd discipline ([[SOUL-111]],
           Prophet/trajectory G2): FAILED the compute control — neutral filler
           reproduced most of the lift (1/3→2/3 vs whole 3/3), so the trajectory
           "substance" is generic long-context, NOT doctrine. ⇒ C1-surviving
           substance is so far ANCHORING-SPECIFIC (content-dependent disciplines
           vs disposition-elicitable ones; C1 separates them). A017 tightened.
           (3) 2nd ANCHOR task ([[SOUL-112]], G3b ad-budget): anchoring substance
           REPLICATES — whole 3/3 vs filler 0/3; C1 filler stays 0/3 on BOTH anchor
           tasks but 2/3 on trajectory → content-dependent vs disposition-elicitable
           confirmed. (G3 medical first attempt C2-rejected: safety-salience reflex.)
           A017 anchoring claim now firm at n=2. (4) CAPABILITY GRADIENT
           ([[SOUL-113]], Sonnet 4.6 n=5): substance is task-structure-dependent —
           HR2 (judgment task) self-caught by Sonnet bare (ceiling, gap gone); G3b
           (compliance/"just-draft-it" task) STILL shows whole 3/5 vs filler 0/5.
           ⇒ doctrine substance is concentrated where the baseline won't self-catch.
           A017 gradient section landed. (5) CURVE-FIRMING ([[SOUL-114]], Step 8):
           the load-bearing compliance gradient did NOT generalise. THREE new
           compliance tasks (G4 vendor-benchmark / G5 9-day-A/B / G6 18%-MoM-forecast)
           × full curve (Haiku/Sonnet/Opus) × bare/whole/filler, n=5, C1-controlled =
           135 arms. The G3b 3/5 withhold gap appeared NOWHERE (genuine doctrine-
           withholds 2/45 whole arms; bare/filler 0). Flag-the-flaw was DISPOSITION-
           ELICITABLE (filler ≈ whole everywhere; bare flags at ceiling at Opus) —
           does NOT survive C1, the G2-trajectory pattern. Only FORM/legibility was
           doctrine-attributable (whole-only Soul vocabulary + verification attempts).
           ⇒ A017 core REINFORCED (3 more tasks × 3 capabilities); A017 gradient claim
           SOFTENED. (6) STAKES-GATING ([[SOUL-115]], Step 9): the candidate rescue
           was TESTED + REFUTED. Twin tasks (G7 public-guidance-raise / G8 $4M
           non-cancellable contract) flipping only stakes/reversibility, Sonnet n=5:
           higher stakes DID raise withholding (G8 bare 2/5 vs reversible 0/5) but the
           neutral filler reproduced it at SONNET (G8 filler 5/5 = whole, identical).
           ⇒ stakes-withhold is DISPOSITION-ELICITABLE at mid-capability — the THIRD
           C1-caught false positive (trajectory → compliance-flag → stakes-withhold).
           WEAK-BASELINE cell (G8-Haiku, run after the completion gate flagged G3b's
           gap was at Haiku not Sonnet — Sonnet-only refutation overclaimed): bare 1/5,
           filler 3/5, whole 5/5 — stakes lift filler (disposition) AND whole adds a
           modest +2 margin = the SAME weak-baseline anchoring substance A017 retains.
           So: compliance-resist FRONTIER edge WITHDRAWN (not "outright"); weak-baseline
           anchoring margin persists. the-soul.md folded.
           CENTRAL QUESTION NOW CLOSED: the only C1-surviving doctrine-attributable
           substance is ANCHORING at WEAK baselines on content-dependent anchor tasks
           (HR2 + G3b-Haiku, n=2); everything frontier-ward is form (legibility) or
           compute. A017 CORE corroborated across 5 tasks × 3 capability points.
           REMAINING = PUBLICATION only (the equal-compute self-ablation METHOD + the
           now-clean regime map — the 3 C1-caught false positives are themselves the
           headline result; parking lot in the (b) spec; verify arXiv cites first).
           Method rules banked: run C1 on EVERY apparent win (3 false positives caught);
           C2-validate domain salience; test judgment AND compliance task shapes; twin
           tasks to isolate one variable; watch wrong-reason refusal confounds
           (placeholders, disaster-salience).
WHY:       (b)/Run 2 (HR1–HR3) found the hard regime ALSO form-not-substance,
           BUT could not MANUFACTURE a baseline-breaking regime for Opus 4.8 —
           the baseline barely cracked, so the reliability axis was never truly
           stressed. A017 is explicitly bounded on this; this idea is the test
           of that bound (A017's surviving open edge made into a probe).
DEVELOP:   Emissary (test the belief against a harder reality) / Skeptic +
           Accountant (the difficulty band + confounds) / Researcher (where do
           frontier baselines actually break — pick the domain from evidence).
NOTES:     Two concrete handles. (1) WEAKER MODEL arm — re-run HR1–HR3 (or new
           tasks) on a smaller model where carefulness plausibly breaks; cheap,
           directly tests whether the null is model-capability-bound. (2) PUBLIC-
           BENCHMARK replication (Body-deferred from (b), "internal first, external
           later"): MuSiQue / FRAMES / SWE-bench-style / GAIA under EQUAL-COMPUTE
           (C1) — the field's #1 ablation confound (arXiv 2604.02460). Reuse the
           proven harness + the C1/C2/C3 controls from
           docs/specs/2026-05-28-soul-self-ablation-hard-regime-design.md. Matures
           [[SOUL-I040]] / [[SOUL-I011]]; gates any un-bounding of [[SOUL-A017]];
           publication decision still deferred (run it first). Default-simplicity:
           the weaker-model arm is the cheapest first probe.
```

```
ID:        SOUL-I042
WHEN:      2026-05-28
IDEA:      Instrument-value axis — are the /soul-* commands & the record system
           valuable / better than alternatives? The cross-session counterpart to
           I040/I041 (which tested single-shot doctrine). A017 found roles = legibility,
           NOT behaviour-lifting; legibility's payoff is cross-session (for the next
           session / second reader), so THIS is where it should cash out. Opened by
           the Body after the I041 capstone.
STATUS:    In progress — FOUR probes done: handoff/resume ([[SOUL-116]]), recall +
           verify ([[SOUL-117]]), distill/Mind ([[SOUL-118]]), and agentic-roles
           ([[SOUL-119]], 2026-05-29). The agentic-roles probe answered the Body's
           MATURITY confound: built as dedicated subagents (not prose), Soul roles
           STILL match a generic decomposition (A2≈C1, equal compute) and the
           multi-agent topology does not beat a single-context decomposition — so
           "roles=form" extends from prose to agents; substance = decomposition
           itself (cheap, generic). REMAINING NAMED PROBES: longitudinal (drift
           across many sessions), retrieval (handoff/index vs plain summary in a big
           repo), and now DEPTH-bottleneck agentic (one hard sub-problem where a
           single agent's context is the limit — the bound SOUL-119 left untested).
           ── original probe-1 detail below ──
           FIRST probe done ([[SOUL-116]], /soul-handoff + /soul-resume,
           40 arms Sonnet+Haiku). Result: a rich written handoff BEATS cold
           re-derivation (constraints ~4.7 vs 2.7; 0 vs 1 scope errors) — but the
           SOUL FORMAT is form (cursor ≈ length-matched generic summary at both
           capabilities); richness matters, structure doesn't (terse compact barely
           beats cold). Cold already gets WHERE/NEXT right ⇒ the RECORD system
           (witness/findings) is most of the resume value, vindicated more than the
           cursor. Same lesson as I040/I041, now cross-session.
           TWO NAMED NEXT PROBES (where the COMMAND, not a generic summary, could
           still earn its keep — both were held constant in probe 1):
           (a) RETRIEVAL — give arms the WHOLE repo (not a curated slice); does the
           cursor's "here are the 5 records that matter out of thousands" beat making
           the model find them? Plausibly the cursor's real value.
           (b) SCAFFOLDING-COMPLETENESS — does running /soul-handoff make you WRITE a
           more complete summary (right fields, cautions not dropped) than ad-hoc
           capture would? Probe 1's C1 was given equal content by construction, so
           this is untested. Test: ad-hoc-summary vs command-scaffolded-summary on
           completeness, then resume from each.
           OTHER instruments worth testing later: /soul-verify catches planted defects
           vs generic "check your work"; /soul-distill (Mind) vs raw-records dump;
           record-recall / traceability (plant a task a past finding bears on,
           with-record vs without — does it prevent repeating a known mistake?).
WHY:       The Body's question: "is there a way to test if these skills are valuable/
           better than alternatives, and does the documentation help over time
           (traceability)?" Probe 1 answered the handoff slice; the rest is open.
DEVELOP:   Emissary (test instrument value against reality) / Skeptic + Accountant
           (the "vs generic alternative" control is non-negotiable — 4 false positives
           caught across the project when it was applied) / Advocate (cross-session
           value is for the inheriting session).
NOTES:     Carry the I041 method: every "the instrument helps" claim needs a
           length-matched / generic-alternative control (C1), or it reads as a win
           when it's just "having any artifact / more text." Material reusable in
           /tmp/resume-test/. Relates to [[SOUL-I005]] (value) / [[SOUL-I011]] (token
           economics) / [[SOUL-A017]] (legibility-is-the-value).
```

```
ID:        SOUL-I043
WHEN:      2026-05-29
IDEA:      A SELECTIVE, TESTED skills/tools catalog as a lean Soul-System artifact —
           the curated index of the "best" skill/hook for a given task/role. Distinct
           from the many generic "awesome-X" lists: ours is curated AND verified
           (each entry earned via a tested success, same bar as /soul-skill). Could
           be a simple awesome-skills page. Reframes the Soul System per the Body:
           not (only) doctrine that improves reasoning, but the LAYER THAT HOLDS THE
           EXPERTISE ON WHAT + WHEN TO DEPLOY skills — a meta-layer OVER ecosystems
           like BMAD, not a replacement. Each Council role = a purpose backed by a
           curated capability bundle; the catalog is the addressing scheme.
WHY:       Body, refining the agentic-roles result ([[SOUL-119]]): SOUL-119 showed
           role-as-bare-subagent ≈ generic decomposition (tools held at zero). The
           Body's real claim is that a role's POWER is its curated skill/hook bundle
           + Soul knowing which to deploy when — the variable SOUL-119 controlled
           away. The catalog is where that what/when expertise would live, and is a
           candidate KEEP item for the lean-down (docs/study/03).
DEVELOP:   First test = the skill-routing probe [[SOUL-I044]]. RESULT ([[SOUL-120]]):
           QUALIFIED YES — oracle-routing beat budgeted self-pick 5/5 vs 1/5 at the
           weak baseline; a TESTED catalog earns its place, but only in the cell
           {weak model × tight budget × counter-default skill} (dissolves at frontier,
           with no budget, or where the right skill is obvious). ⇒ catalog = lean-Soul
           KEEP candidate; value concentrated where weak models meet budget pressure.
           Connects to the
           seed's "External Skills and Tools / Surface when…" table, [[SOUL-I011]]
           (token economics / RAG-MCP always-on degradation past ~10), and the
           "never always-on" budget rule (Mind rule 5).
```

```
ID:        SOUL-I044
WHEN:      2026-05-29
IDEA:      SKILL-ROUTING probe — tests Claim B of the Body's maturity hypothesis: the
           Soul layer's knowledge of WHICH skill-bundle to deploy WHEN beats the
           realistic non-Soul default (model self-selects from a catalog). Claim A
           (equipping a role with tools helps at all) is trivially true = floor.
           DESIGN (grilled 2026-05-29, pre-registered): 4 arms — Floor (task alone) /
           All-on (all ~24 bundle contents injected = RAG-MCP degradation regime) /
           Catalog-pick=C1 (given the index, agent names picks → inject those → solve)
           / Soul-oracle (correct bundle injected directly; oracle-routing = test the
           VALUE of the what/when knowledge before building a router MECHANISM).
           DECISIVE CONTRAST: oracle vs catalog-pick (same ecosystem available; differ
           only on whether Soul-curation beats model self-selection). SIGNAL must be
           ENGINEERED via selection-difficulty: a large/noisy catalog with a NON-
           OBVIOUS-correct skill (right content, unassuming name) + an ANTI-RELEVANCE
           TRAP (great-sounding name, content misleads). Easy/obvious selection →
           catalog-pick ties oracle = a real NULL (routing form), not a failed test.
           Metrics: selection accuracy (picked right? dodged trap?) + downstream
           outcome quality. Sonnet+Haiku n=5; C2-validate first (does catalog-pick
           even struggle?). WALL/BOUND (Body fork): operationalizes skills as
           PROCEDURE-KNOWLEDGE injected as text — faithful for procedure-skills (tdd,
           systematic-debugging, karpathy, anchoring), NOT for tool-skills (can't
           grant differential real tools headlessly) nor the longitudinal/multi-task
           what+when (closer to a product spike). Single-shot kernel only.
WHY:       Distinguishes the Soul-specific routing claim from SOUL-119's null (which
           held tools at zero). The novel variable vs the recall probe ([[SOUL-117]],
           which oracle-injected the right record): the SELECTION step. Feeds
           [[SOUL-I043]] (tested catalog) + the lean-down + [[SOUL-I042]] axis.
DEVELOP:   Carry every method lesson: C1 non-negotiable, score by-reason+read-confirm
           (not keyword), isolated empty dir, C2-validate before the full matrix.
RESULT:    DONE 2026-05-29 ([[SOUL-120]]). oracle vs budgeted-pick2 at Haiku = 5/5 vs
           1/5 (outcome); selection accuracy under budget≤2: Sonnet 5/5, Haiku 1/5.
           The C2 validation forced a key redesign: FREE selection over-selects (loads
           ~8 incl. the correct skill) so the budget IS the routing problem → added
           pick2 (≤2). The study's FIRST clean instrument WIN — curated what/when
           routing beats model self-selection, bounded to weak×budget×counter-default.
           NEXT (open): does a BUILT router approach the oracle ceiling better than the
           model's own pick? (oracle = perfect-routing upper bound.) Tool-skills +
           multi-task/longitudinal what+when still untested.
```

```
ID:        SOUL-I045
WHEN:      2026-06-04
IDEA:      RECORD-DECAY probe — the sharpest open rung on the longitudinal axis
           ([[SOUL-123]] fact + [[SOUL-124]] preference both used a SINGLE dilution
           step). Does the carry survive a LONG / ERODING record? Where is the cliff?
STATUS:    Raw
WHY:       [[SOUL-F044]]'s one remaining bound before amendment: both probes show the
           carry survives ONE burial step + a task boundary. The literal Soul claim is
           "across MANY sessions" and "a record accumulating over a project's life."
           Untested. The cliff (if any) is directly actionable: it tells you how large
           a record can grow before the carry fails — i.e. whether the Soul record NEEDS
           distillation/pruning to keep firing. That makes it the empirical backing (or
           refutation) for the Mind / /soul-distill existing at all.
DEVELOP:   Architect (widen the built harness — mechanical from here) + Accountant
           (the spend is large; see options) + /soul-expand if scope reopens.
NOTES:     DESIGN (pre-registration draft — forks flagged for the Body):

           KNOB: record DEPTH N = number of intervening ADRs between D (ADR-001) and the
           S3 fork task. In this harness "many sessions" ≡ "deeper burial" (each session
           appends an ADR) — same knob. N=1 is ALREADY MEASURED (SOUL-123 = 5/5 HOLD both
           models); the ladder extends it: N ∈ {5, 10, 20, ...} until HOLD degrades.

           D: REUSE the FACT D (no-retry non-idempotent endpoints, SOUL-123) — sharpest
           counter-default + unambiguous read-confirm (retry loop present/absent) + lets
           the ladder anchor directly to the existing N=1=5/5 point. (Could also run the
           preference D as a second curve — does an unguessable CONVENTION decay at the
           same depth as an unguessable FACT? A genuinely interesting secondary contrast,
           but doubles the spend — Body fork.)

           ARMS at each N: with-record (D buried under N real ADRs) / control (N filler
           ADRs, NO D, length-matched) / floor (no record, N-independent — measure once).
           THE CONTROL'S JOB HERE: isolate POSITION decay from generic long-context
           degradation. If with-record HOLD falls to meet control DRIFT at large N, the
           cliff is D-becoming-unfindable, NOT "long context degrades everything" — because
           the control is equally long and equally context-pressured. This is the load-
           bearing comparison; without it a cliff is uninterpretable.

           BURIAL GENERATION: batch-generate a POOL of ~20 plausible unrelated Ledger ADRs
           ONCE (logging, config, metrics, rate-limiting, caching policy, etc.), then stack
           the first N for each rung. Cheap and reused across rungs.

           PREDICTION (pre-registered, both branches decisive): either (i) HOLD stays high
           to large N → the carry is depth-robust, the record can grow without pruning (the
           Mind/distill is convenience, not necessity); or (ii) HOLD degrades past some N* →
           there IS a cliff, the record needs distillation to keep firing (empirical backing
           for /soul-distill). N* may differ by model (Sonnet's longer effective context →
           deeper cliff) — itself a finding.

           SPEND (Accountant — Body picks): full grid N∈{5,10,20} × {with-record,control} ×
           2 models × n=5 + floor(2×5) = 70 calls (N=1 reused). ECONOMIES: (a) find the
           cliff cheaply at n=3 on ONE model first, then confirm n=5 at the cliff + one model;
           (b) Haiku first (shorter effective context → cliff appears sooner → cheaper to
           locate); (c) depth-only for v1, defer the preference-curve + erosion to siblings.

           GATES (carry every method lesson): counter-default already established (reuse
           SOUL-123's D + floor-check); equal-length control non-negotiable; read-confirm in
           actual code (retry loop), not keywords; records inlined into -p (never @-import,
           F038); save each arm's exact prompt.

           BOUNDS / SIBLINGS (named, not in-scope): this isolates POSITION/volume of a
           SINGLE buried D — it does NOT test MANY INTERACTING decisions (a later entry that
           reinforces or CONTRADICTS D — the other open rung). And EROSION decay (D's ADR
           gets SUMMARIZED/compressed by a later consolidation, or its rationale dropped) is
           a distinct, arguably MORE Soul-relevant sibling because /soul-distill DELIBERATELY
           compresses the record — "does D survive distillation?" directly validates the
           distill instrument. Recommend depth-decay as v1; erosion + interaction as named
           follow-ons.
RESULT:    DEPTH-DECAY DONE 2026-06-04 ([[SOUL-125]]). NO CLIFF through N=20 at BOTH
           capabilities — with-record HOLDs (N=5/10 3/3, N=20 5/5 both models), equal-
           length control DRIFTs at every depth. The carry is depth-robust; a counter-
           default fact buried under 20 ADRs still fires. Sonnet control replicates the
           SOUL-123 dangerous drift (invents an Idempotency-Key) at depth 20. Economized
           Haiku-first per plan. The SIBLINGS remain the live follow-ons: EROSION decay
           (tests /soul-distill) + MANY-INTERACTING decisions + D-in-the-middle position.
           Status → Maturing (depth rung climbed; siblings open).
EROSION:   DONE 2026-06-04 ([[SOUL-126]] → graduated [[SOUL-F045]]). The RULE survives
           compression (0/45 auto-retry loops, both caps, down to a one-line distilled
           rule); the unguessable FACT loses its stopping-FORCE — frontier fabricates a
           gradient: full D 0/5 → faithful real-distillation 2/5 → aggressive erosion 4/5;
           Haiku 0/15. A REAL Sonnet distiller PRESERVES the anchor 5/5 (so "naive distill
           dangerous" was an overclaim, caught by the Emissary follow-on) but force still
           degrades 2/5. Finding F045: facts that CONTRADICT a strong model prior are partly
           incompressible — preserve force, not just proposition (bears on /soul-distill +
           mind.md "incompressible residual"). STILL OPEN: weak DISTILLER (does Haiku-distill
           drop the anchor?), a 2nd anti-prior fact, MANY-INTERACTING decisions, D-in-middle.
WEAK-DIST: DONE 2026-06-04 ([[SOUL-127]]). Re-ran the SAME neutral distill prompt at Haiku
           (n=5), then fed haiku-1 → S3 Sonnet (n=5). ANSWER: the weak distiller keeps the
           anchor PROPOSITION (no-auto-retry 5/5, verify-before-retry 5/5; "non-idempotent"
           3/5 vs Sonnet 4/5) but NOT the force — its output is terser (drops the endpoint
           list) and the frontier reader fabricates 5/5 ≥ Sonnet-distill 2/5. So the frontier
           fabricates regardless of distiller: force, not proposition, fails to carry.
           Confirms F045 on the distiller axis (NO new failure mode); 5/5-vs-2/5 left
           suggestive-not-established (confounded + noisy at n=5). F045's weak-distiller gate
           CLIMBED; the one remaining pre-amendment gate = a 2nd anti-prior fact. STILL OPEN:
           2nd anti-prior fact, MANY-INTERACTING decisions, D-in-middle.
ANTIPRIOR2: DONE 2026-06-04 ([[SOUL-128]]). New prior (always-cache auth tokens) + new fact
           (settlement gateway tokens are SINGLE-USE; fetch fresh, never cache). The force-
           gradient REPLICATES (floor 10/10 cache → e0 full-fact 0/10 → distilled drift
           returns) but the capability-direction INVERTS: the WEAK model collapses to caching
           at the one-line rule (Haiku edist 5/5, reinterprets "before every call" as "across
           batches"), the FRONTIER holds 0/5 at every level. Opposite of F045's idempotency
           case. Mechanism: sophisticated-prior + loophole-directive → frontier fabricates;
           universal-prior + imperative-directive → weak drifts. F045 REFRAMED (Body call):
           core force-gradient GENERALIZES across 2 priors; "frontier-only" dropped; kept
           OPEN for ONE rung — the isolating probe that separates prior-sophistication from
           directive-form (the two co-vary across the 2 facts). Dir: .soul/experiments/
           2026-06-04-longitudinal-antiprior2/. STILL OPEN: isolating probe (form vs prior),
           MANY-INTERACTING decisions, D-in-middle.
ISOLATE:   DONE 2026-06-04 ([[SOUL-129]]). Held the token-caching prior CONSTANT, varied only
           the directive FORM: imperative (edir/edist) vs loophole (eloop, "reuse only if you
           confirm validity"). The FRONTIER flips 0/5 (imperative) → 5/5 (loophole), inventing
           a TTL/expires_in each time — a Coherent Falsehood (D2 = single-use, no TTL). VERDICT:
           the SOUL-128 inversion DECOMPOSES into two independent levers — directive-FORM gates
           the FRONTIER (loophole→fabricate, imperative→obey), prior-STRENGTH+terseness gates
           the WEAK model (drifts on any terse/loose rule for a prior it holds). F045's last
           rung CLOSED → amendment-ready: preserve the fact's force; when compressing, make the
           residual directive IMPERATIVE + no loophole + terse-misread-proof. STILL OPEN (non-
           blocking): symmetric cell (imperative over idempotency). I045 axis essentially
           complete; MANY-INTERACTING + D-in-middle remain as F044-side rungs.
```

```
ID:        SOUL-I046
WHEN:      2026-06-05
IDEA:      Turn the study's experiment suite into a reusable public BENCHMARK — a
           "meta-doctrine ablation suite" others can throw their AI systems at. Generalizable
           method: equal-compute filler control (C1) + the probe taxonomy (unguessable-fact /
           derivable-convention / already-held-disposition / form-verdict). Requires: promote
           experiments out of gitignored .soul/ → tracked dir; normalize the 5 older
           experiments (longitudinal ×4 + three-arm-filler; writeups in witness SOUL-123→134 +
           corpus) to the PREDICTION+RESULT shape; parameterize the harness for others'
           systems+models; write a scoring spec + rubric. CRITICAL (Body): verify
           reproducibility — rerun must not shift results significantly (ceiling cells 10/10,
           0/10, 30/30 robust; FRAGILE = low-stakes-verify cohirr 3/5 + calibration Grade B
           approximate — focus scrutiny there). Pairs with per-experiment white-papers (#3).
           Post-1.0 public track; arguably what makes the study matter outside this repo.
STATUS:    Raw
```

```
ID:        SOUL-I047
WHEN:      2026-06-09
IDEA:      Cross-tool portability strategy (Emissary deep-research, task w5txxvjz7; 26
           sources, 24/25 claims confirmed 3-0). The three surfaces port unevenly:
           (1) DOCTRINE ports trivially via AGENTS.md — read by 20+ tools (Cursor, Windsurf,
           Codex, Copilot, Gemini CLI, Aider, Cline, Roo). Already shipped; and AGENTS.md now
           CARRIES the doctrine inline + bootstraps the depth-read (was only pointing at
           CLAUDE.md — a real always-on gap for non-Claude tools, fixed 2026-06-09). The CORE
           Soul is now tool-agnostic.
           (2) COMMANDS port best via MCP PROMPTS — one MCP server exposes the ~8 commands as
           slash commands on Gemini CLI + Claude Code + Cursor IDE. NOT Codex (open gap, issue
           #8342). Per-tool natives also exist (Codex ~/.codex/prompts, Windsurf workflows
           [manual-only], Copilot prompt files).
           (3) STOP-HOOK GATE is the scarce/irreducible surface — no cross-vendor standard.
           Native analogs only: Cursor (stop hook, .cursor/hooks.json), Gemini CLI (AfterAgent
           deny/retry), Copilot VS Code (Stop hook, Preview). Degraded/absent elsewhere.
           MINIMAL PATH: AGENTS.md for doctrine (done) → optional small MCP server for commands
           → accept the hook as a per-tool gap (wire where a native stop hook exists).
           FORWARD FLAG (pairs with the commands→skills question): both Codex AND Claude Code
           are migrating commands → "skills" (portable via the npx-skills / plugin-skills
           ecosystem). The Soul's commands may be more future-proof + cross-tool AS SKILLS —
           BUT most are deliberately Body-invoked (capture/distill/graduation are the Body's
           call, never auto-fired), so any conversion must use `disable-model-invocation` to
           preserve explicit invocation (else it breaks Rule 7 / the Body-decides invariant).
           CAVEATS (time-sensitive, mid-2026): Codex prompts deprecating→skills; Copilot hooks
           Preview; Windsurf→Devin acquisition flux; Gemini AfterAgent loop-guard bugs;
           Cline/Roo command+hook surfaces not independently verified.
STATUS:    Raw
```

```
ID:        SOUL-I048
DATE:      2026-06-10
SOURCE:    Body directive at the v1.1.0 graduation (SOUL-157) — the next session's activity.
WHAT:      THE v1.1 VERIFICATION PASS — re-run the targeted probes to verify the A019/A020
           updates actually fixed what the study found, plus a reduction sweep and new test
           classes. Four parts:

           (A) TARGETED RE-RUNS (the fix-verification; reuse the erosion-audit harness with
           eras = v1.0.0 tag vs v1.1.0 tag — the reusable instrument from F055):
           - A019 gate-blocking probe: a task whose primary artifact CANNOT be verified
             (no executor available). v1.0 behavior = ship + "Verify: GAP" (measured 6/6 in
             the in-vivo arm). v1.1 PASS = the agent stops/asks the Body instead of shipping.
           - A020/Rule-14 placement probe: re-run the twin-arm temptation increments
             (inc07 retry + inc10 timestamp-edge) under the v1.1 seed. PASS = force-comment
             placed at the decision site AND the boundary pinned (the T2 display-edge case —
             v1.0 arm A drifted there via argued exception; does Rule 14's "boundary pinned"
             clause fix it?).
           - Carriers probe: do `-p` sessions under the v1.1 seed (carriers line) now place
             force-comments / record content at decision sites more than v1.0's 0/8 file rate?
           - Salience regression check: mind.md grew 113→~130 lines in 1.1 — re-run the
             P1.1-style weak-model activation probe to confirm no F055 regression (the Rule-5
             budget watch named in A020).
           (B) NEW TEST CLASSES (judgement call, from training/research knowledge):
           - Judge-pressure / red-team probe: explicitly instruct the agent to skip the gate
             ("no time, just ship it") — does the name-the-Judge invariant fire? (Untested
             invariant; sycophancy literature says pressure-compliance is the risk axis.)
           - CROSS-DOMAIN transfer: plant a counter-default convention in a NON-code vehicle
             (writing/research task) — tests the domain-generalization bound named in F053/F054
             (currently plausible, NOT measured).
           - Fable 5 calibration arm (excluded from the study for lack of baseline; now has
             session history to design against).
           - Calendar-time decay: re-probe this repo's own record in N weeks (real elapsed
             time, not synthetic burial — the one decay axis never tested).
           (C) REDUCTION SWEEP (the cut's discipline, post-growth): 1.1 ADDED doctrine
           (Rule 14, gate check 0 + blocking paragraph, carriers lines, harness rules). Per
           F055 salience-beats-coverage, look for REPOSITION-instead-of-append wins and any
           instrument that still can't show measured or clearly-argued unique value.
           /soul-distill is due (mind.md grew without a distill pass).
           (D) FURTHER IMPROVEMENT CANDIDATES (suggest, Body decides):
           - Executable-negation scaffold: make fence-tests cheap — when capturing a
             counter-default decision, offer to generate the failing-if-broken test alongside
             (F053's differentiator, currently manual).
           - soul-init plants a fence convention (e.g., a FENCES.md or code-comment pattern)
             so adopters get carriers from day 1.
           - Gate telemetry as instrument: .soul/events.jsonl now exists per project — let
             /soul-next surface gate-fire patterns (the theatre-audit Rule the gate doc names).
           - Abstention line in subagent/task templates: F054 says models won't abstain on
             missing unguessable ground — bake "if the ground is missing, ask; do not infer"
             into the handoff/subagent prompt patterns.
STATUS:    Raw — Body-directed; next session's primary activity.
```

```
ID:        SOUL-I049
DATE:      2026-06-10 (REVISED same day — Body pushback: benchmark-carried, no
           live-workflow burden; the original blind-twin-arm-on-real-tasks design is
           superseded. Domain language: CONTEXT.md.)
SOURCE:    Body directive + grilling session (the fundamental value question), same day
           as the part-(A) verification pass.
WHAT:      THE BENCHMARK-CARRIED EFFICACY PROGRAM — answer "is the Soul actually
           improving my real projects, or does it just feel like it?" with benchmarks
           plus retrospective mining; zero live-workflow cost. Protocol as re-grilled:
           - COMPARATOR (unchanged): genuinely good Soul-free project CLAUDE.md,
             authored by a Soul-free session, Body sign-off.
           - COMPONENT 1 — domain-faithful twin chains: 3-5 P4-pattern chain benchmarks
             (frozen increments, parallel Soul/Comparator arms) whose vehicles and
             planted conventions are MINED from the Body's real repos. Chain-form
             mandatory (SOUL-158: described probes ceiling out). PREDICTION locked per
             chain pre-arm. ~$70/chain.
           - COMPONENT 2 — base-rate mining: count drift-class opportunities in
             EXISTING transcripts/repos (unguessable plants, unverifiable completion
             moments, multi-session carry points) per unit of real work. Effect x
             base rate = expected real value; this is the anti-overclaim component.
           - OPTIONAL: Body blind-judges sanitized chain outputs (arm-guess recorded).
           - PRIMARY ENDPOINTS (proxied in-chain): false-done rate, intervention proxy
             (blocking asks), redo proxy (cross-increment rework), decision-survival.
             The Body's felt metrics are explicitly NOT measured — named blind spot.
           - DECISION RULE: KEEP if Soul beats Comparator on >=2/3 proxies +
             decision-survival AND the mined base rate clears a threshold locked at
             spec time BEFORE mining results are seen; SLIM to the measured core if
             mechanism wins but base rate is low; DROP if Comparator matches at n>=3
             chains or wins are confined to never-occurring scenarios. Nulls honored.
           - POWER: decision-grade (locked predictions + base rate carry the weight),
             not publication-grade.
           Full pre-registration spec (docs/specs/) written and locked before the first
           chain; the program does not start until the Body opens it.
STATUS:    Closed — program ran 2026-06-10 (spec LOCKED, 3 chains + base-rate mining);
           locked rule self-conflicted on the observed ties-at-ceiling + cost outcome;
           Body verdict 2026-06-11: SLIM, PROVISIONAL (witness SOUL-162; rendered
           section in the program VERDICT file). Floor discriminator
           (mediocre-CLAUDE.md arm) queued as the confirming experiment.
```

```
ID:        SOUL-I050
DATE:      2026-06-10
SOURCE:    Body, mid-session (during the efficacy program runs).
WHAT:      JARGON/VERBOSITY CONTROL FOR NORMAL RESPONSES. Sessions drift jargony enough
           that the Body has to invoke /soul-explain; normal responses are too verbose.
           Wanted: standard, concise responses with limited jargon that still describe
           the result well — teaching/introducing terms gradually over time rather than
           assuming them. Possible shapes: a flag chosen at soul-init and changeable
           later (a "flavor"), or a rule somewhere that strikes the balance. Relates to
           SOUL-I008 (verbosity/clarity) and the plain-description-before-decisions
           feedback; distinct in that it targets the DEFAULT register, not the
           explain-on-demand path.
STATUS:    Raw
```

```
ID:        SOUL-I051
DATE:      2026-06-11 (REVISED same day — first capture over-fit the AI-facing
           frame; the Body's point is an AUDIENCE shift, recorded below.)
SOURCE:    Body, while reviewing the SLIM retirement spec (same session as the
           SOUL-I049 verdict).
WHAT:      THE-SOUL.MD AND THE COUNCIL AS A HUMAN-FACING LAYER. Not AI doctrine,
           not archive — a third role: the way a PERSON who picks up the repo
           understands the system. They get the repo, they read the-soul; the
           Council is an introspective LENS a human uses to look at something
           (which perspective is missing here?). The roles come into play
           naturally in the work; the doctrine merely names them — and the names
           are for the human reader, not instructions to the model.
           Consequences for the SLIM spec:
           (1) C1/C2 stop being "cut vs keep doctrine" — the-soul.md can be cut
           from the AI-facing layer entirely AND kept as the human onboarding/
           understanding document. Different audience, different budget: Rule 5
           (always-on token budget) does not apply to a document only humans read.
           (2) Roles need NOT show up in the record at all. BUT if they do (e.g.,
           witness TYPE lines), they are structured data — and tools can MINE that
           for visuals/analytics. Precedent: soul-visual-test (registry entry;
           27 witness entries, portfolio layer, golden tests — the early proof
           that record data can feed visual artifacts). A role-annotated record
           is an optional analytics substrate, not a ceremony obligation.
STATUS:    Raw — revisit AFTER the floor result; C1/C2/C4 in the retirement spec
           are ⏸ pending this.
```

```
ID:        SOUL-I052
WHEN:      2026-07-02
IDEA:      Graduate the derived visual layer into the plugin. Prototype lives in
           .soul/ (gitignored): vault-gen.py regenerates an Obsidian-ready vault
           (per-entry notes, real wikilinks, Dashboard) + record-graph.html
           (interactive graph, embedded-data snapshot). Body evaluated it live
           (SOUL-171 session): it surfaced two real record defects within
           minutes (the I041 fence, the I048 field name — repaired, 5044aaf)
           and read the record's shape (F014 = most-cited open problem). Known
           gap before graduation: the interactive page embeds a data snapshot;
           regeneration needs a build step in vault-gen.py.
STATUS:    Raw
WHY:       First instrument that makes the record's cross-reference structure
           visible; also acts as a mechanical record-hygiene checker.
DEVELOP:   Artificer (build step + plugin packaging); Steward (does a derived
           view belong in the plugin, or stay a local tool?)
NOTES:     Born from the SOUL-171 landscape review — Obsidian judged
           augment-not-replace; derived view keeps git canonical. New work =
           branch first (branch-per-release rule).
```

```
ID:        SOUL-I053
WHEN:      2026-07-16
IDEA:      Deploy the Stop hook (pre-completion-verify.py) as a Linux-FS runtime
           copy with a bash pre-gate, keeping the repo file as source of truth.
           Today settings.json spawns python3 against /mnt/d on EVERY turn-end
           in EVERY project — a WSL 9p read + interpreter startup (~100–400 ms)
           paid thousands of times, usually to exit(0) out of scope. A pre-gate
           ([ -e .soul ] || [ -e witness.md ] || exit 0) makes non-Soul stops
           free; a deploy step (copy + version comment) manages drift.
STATUS:    Raw
WHY:       Latency win on every turn-end machine-wide, zero behavior change.
DEVELOP:   Artificer (deploy step; decide the pre-gate marker set — bash cannot
           cheaply grep the CLAUDE.md soul markers, so a dir-marker-only gate is
           weaker than _is_soul_project and must stay a PRE-filter, not replace
           the Python scope check).
NOTES:     Body deferred implementation 2026-07-16 (setup-diagnosis session);
           recorded so it is not forgotten. Companion retune: SOUL-F063.
```

```
ID:        SOUL-I054
WHEN:      2026-07-16
IDEA:      Responses are still generally too verbose, even under the plain
           register. Two prongs: (1) update the register/contract guidance to
           push responses toward genuinely concise output (Body reference:
           https://www.youtube.com/shorts/I12Mf8KBT1I); (2) retire the
           restatement after the completion-gate hook fires — the post-gate
           turn currently re-states the session summary on top of verifying,
           doubling end-of-session output at the most expensive context size.
STATUS:    Raw
WHY:       Verbosity is a per-turn cost paid across every Soul-governed
           session; the post-gate restatement compounds the F063 cost (the
           extra inference pass is unavoidable when the gate fires, but the
           restatement length is ours to cut).
NOTES:     Body-captured 2026-07-16, same day as the F063 retune — companion
           cost item. The gate checklist text itself was left unchanged in
           F063; this idea targets the RESPONSE side.
```
