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
```

```
ID:        SOUL-I006
WHEN:      2026-05-21
IDEA:      the-soul.md is large (~500 lines) and is @-imported into the always-loaded
           seed, so Claude Code shows the "large CLAUDE.md may impact performance"
           warning at every session start. Keep the philosophy present without paying
           the full-file context cost each session.
STATUS:    Raw
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
STATUS:    Raw
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
STATUS:    Raw
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
