# The Soul System Witness Log

The Witness records what happens during the Soul System's own development.

This log follows `operations/witness-log-format.md`. Entries are factual,
terse, and never deleted — resolved entries are marked Resolved.

Project code: `SOUL`.

---

## Entries

```
ID:           SOUL-001
WHEN:         2026-05-19 / Dogfood pass on README update
WHERE:        Repo root — missing CLAUDE.md
WHAT:         Soul System repo had no root CLAUDE.md to load operations/CLAUDE.md
              via @-import. Sessions opened in the repo did not auto-load the philosophy.
TYPE:         Obligation Skipped — Soul System failed to apply its own @-import
              workflow to itself.
CONSEQUENCE:  Self-dogfood blocked until fix. One-line CLAUDE.md added.
STATUS:       Resolved
```

```
ID:           SOUL-002
WHEN:         2026-05-19 / Dogfood pass on README update
WHERE:        philosophy/the-soul.md > The Architect section
WHAT:         Architect description used code-shaped language (modules, interfaces, files)
              implying code-only scope. Documentation and repository structural decisions
              had no named home.
TYPE:         Felt Wrong — doctrine implied a narrower scope than actually held.
CONSEQUENCE:  Clarifying sentence added covering documentation organization and
              repository layout.
STATUS:       Resolved
```

```
ID:           SOUL-003
WHEN:         2026-05-19 / Dogfood pass on README update
WHERE:        Multiple files — per-file Version footers, SYSTEM-VERSION.md, install.sh
WHAT:         Version markers existed in three places (per-file Version 1.0/1.1,
              SYSTEM-VERSION.md, install.sh). They drifted — SYSTEM-VERSION.md at
              0.1.2 while today's session added significant changes.
TYPE:         Felt Wrong — duplication created drift risk.
CONSEQUENCE:  Per-file versions removed. SYSTEM-VERSION.md bumped to 0.2.0, established
              as single source. install.sh synced.
STATUS:       Resolved
```

```
ID:           SOUL-004
WHEN:         2026-05-19 / Dogfood workflow setup
WHERE:        ~/.claude/commands/soul-init.md
WHAT:         /soul-init slash command hardcodes Soul System path to
              /mnt/d/Projects/Soul-System. Other machines need manual edit.
TYPE:         Council Note — Steward (machine-portability of dogfood tooling)
CONSEQUENCE:  Not blocking. An env var ($SOUL_SYSTEM_ROOT) would resolve it; the
              pattern earns its place when a second machine actually adopts the workflow.
STATUS:       Open
```

```
ID:           SOUL-005
WHEN:         2026-05-19 / Decision 5 framing
WHERE:        Conversation — user-stated future possibility
WHAT:         Caveman-style Council summaries to the user. When the Council convenes,
              the user receives a 3-5 line dense digest; full deliberation lives in
              linked artifacts (findings/, amendments/, ADRs).
TYPE:         Council Note — Advocate (user experience of Council outputs)
CONSEQUENCE:  Captured. Depends on findings/ + witness.md existing as artifacts.
STATUS:       Resolved [by SOUL-A002]
```

```
ID:           SOUL-006
WHEN:         2026-05-19 / Decision 5 framing
WHERE:        Conversation — user-stated future possibility
WHAT:         Post-project analysis as a named Council convening mode — mining the
              accumulated record (Witness log + Findings + Amendments + ADRs + in-code
              markers) for project-level retrospective. Distinct from Pre-Mortem;
              this is Post-Mortem.
TYPE:         Council Note — Prophet, Cartographer (named convening mode candidate)
CONSEQUENCE:  Captured. Could become a third named Council mode after Pre-Mortem
              earns its place through use.
STATUS:       Open
```

```
ID:           SOUL-007
WHEN:         2026-05-19 / Decision 5 framing
WHERE:        Conversation — user-stated future possibility
WHAT:         Visual session map — dots-on-circle or Warcraft-style agent-activity
              view showing which role is active when and where user intervention is
              needed. UX layer for observing the Soul System operating in real time.
TYPE:         Council Note — Artificer (instrument), Advocate (user observation)
CONSEQUENCE:  Captured. Far downstream of current dogfood phase.
STATUS:       Open
```

```
ID:           SOUL-008
WHEN:         2026-05-19 / Decision 5 finalization
WHERE:        Conversation — Council convened on witness log file lifecycle
WHAT:         Body surfaced lifecycle gap (write → archive → cleanup vs. doctrine's
              "never delete"). Council convened (7 voices). Synthesis: never-delete
              applies to entries, not files; file-level lifecycle added — Active /
              Archived / Retired. Filed as SOUL-A001 (accepted).
TYPE:         Council Note — Archivist (first Amendment filed; mechanism dogfooded)
CONSEQUENCE:  Doctrine extended; lifecycle codified; Amendment mechanism validated
              in practice rather than only in council-synthesis.md.
STATUS:       Resolved
```

```
ID:           SOUL-009
WHEN:         2026-05-19 / Council convening on lifecycle
WHERE:        Conversation — Council output style
WHAT:         User observed that Council output was not caveman-compressed
              (per SOUL-005). System captured the practice but had not operationalized
              it — full deliberation appeared in conversation instead of digest.
              Caveman digest demonstrated retroactively.
TYPE:         Obligation Skipped — captured-idea-to-active-practice promotion missing
CONSEQUENCE:  Gap between Findings (captured) and operational practice surfaced.
              SOUL-005 partially resolved by SOUL-A002. The meta-question
              (Finding promotion pathway) remains open pending more evidence.
STATUS:       Open
```

```
ID:           SOUL-010
WHEN:         2026-05-19 / Council convening on output format
WHERE:        Conversation — adopting two-track Council output
WHAT:         Body authorized promoting SOUL-005 to active practice. Brief
              Council pass with caveman digest. Synthesis: artifact + digest as
              two views of one convening. Filed as SOUL-A002 (accepted) —
              first instance of the new digest format used to file itself.
TYPE:         Council Note — Advocate (digest practice operationalized),
              Archivist (self-referential Amendment)
CONSEQUENCE:  Caveman digest is now doctrine. Captured-idea-to-active-practice
              gap (SOUL-009) remains open as separate concern.
STATUS:       Resolved
```

```
ID:           SOUL-011
WHEN:         2026-05-19 / Test project setup
WHERE:        Conversation — Body raised metrics/instrumentation question
WHAT:         Body proposed a metric/record system capturing when Soul System
              roles get invoked (continuous, not just formal Council convenings)
              to feed visualization and doctrine feedback. Council deferred
              formalization — existing artifacts (Witness, Findings, Amendments,
              ADRs, commits, markers) may be rich enough; build visual on those
              first; let gaps surface as evidence.
TYPE:         Council Note — Cartographer (observability territory),
              Skeptic (premature-formalization risk)
CONSEQUENCE:  Deferred. The /tmp/REF-09 project will dogfood the
              question: if existing artifacts insufficient for the visual,
              that is evidence justifying metrics layer. If sufficient,
              metrics formalization unearned.
STATUS:       Open
```

```
ID:           SOUL-012
WHEN:         2026-05-20 / Post-test harvest
WHERE:        4 autonomous test projects — REF-09, REF-11,
              REF-10, /home/fig/REF-08
WHAT:         Four autonomous Soul-governed test runs completed and were
              investigated (agents verified claims against artifacts — ran tests,
              executed scripts, grepped markers). Cross-project synthesis
              harvested into 10 Findings (SOUL-F001..F010, findings/open/).
              Headline: the doctrine is a strong ratchet and a weak engine. Root
              cause subsuming several failures (VISUAL-024): collapsing "the
              Universe" to "the local context." Strongest positive: the AL gate
              is load-bearing in all four runs; the honesty mechanism self-
              diagnoses.
TYPE:         Council Note — Archivist (findings filed for convening)
CONSEQUENCE:  First real multi-session, multi-domain evidence base. Convening
              trigger met (shared TYPE across WHERE, across sessions). Council to
              convene on SOUL-F001..F010.
STATUS:       Open
```

```
ID:           SOUL-013
WHEN:         2026-05-20 / Theme A Council convening
WHERE:        philosophy/the-soul.md (Failure Vocabulary + completion obligation);
              operations/CLAUDE.md (seed mirror)
WHAT:         Council convened on Theme A (Findings F001/F002/F006), framed by
              F010. Judge synthesized; Body accepted SOUL-A003 — the first
              philosophy-level amendment. Added the Universe Collapse failure
              mode; sharpened "consult the Universe" to require outward reach for
              non-trivial work. Revelator's reframe: name the latent principle,
              do not bolt on an ambition gate.
TYPE:         Council Note — Archivist (first Soul amendment recorded)
CONSEQUENCE:  SOUL-F001 resolved by SOUL-A003 (moved to findings/closed/).
              F002/F006 split to follow-on SOUL-A004. Doctrine now carries a
              named counter to ratchet-not-engine. System version → 0.3.0.
STATUS:       Resolved
```

```
ID:           SOUL-014
WHEN:         2026-05-20 / Theme A operations corollary
WHERE:        operations/CLAUDE.md (Naming Roles in the Moment)
WHAT:         SOUL-A004 accepted (operations-level). Selective role visibility:
              name the Judge at gate-overrides, name the Emissary when evidence
              overturns a belief, otherwise silent. F002 resolved and closed;
              F006 (session-end pass) deferred — ceremony risk — stays open
              pending evidence.
TYPE:         Council Note — Archivist
CONSEQUENCE:  Theme A fully processed: F001 → A003 (Soul), F002 → A004 (ops),
              F006 deferred. Themes B/C/D/E remain.
STATUS:       Resolved
```

```
ID:           SOUL-015
WHEN:         2026-05-20 / Theme B Council convening
WHERE:        philosophy/the-soul.md (Frame + completion obligations); seed mirror
WHAT:         SOUL-A005 accepted (philosophy-level, second after A003). Frame gate
              becomes a check (not a production) when a spec supplies both levels.
              Completion obligation gains a global-invariant clause — local tests
              passing is not global correctness (verification vs validation).
              F005 and F007 resolved and closed.
TYPE:         Council Note — Archivist
CONSEQUENCE:  Completion gate now escalates local → global → outward. Theme B
              complete. Themes C (scaling), D (visual Witness), E (multi-agent)
              remain.
STATUS:       Resolved
```

```
ID:           SOUL-016
WHEN:         2026-05-20 / Theme C Council convening
WHERE:        operations/CLAUDE.md (Council section); operations/code-markers.md
WHAT:         SOUL-A006 accepted (operations-level). Role-set scales to problem
              size (small work → subset, not full chamber). Docstrings blessed as
              a complementary in-artifact honesty channel alongside markers.
              F003 (scaling part) and F004 closed. F003's Magistrate-count
              question and F009 (artifact drift) left open — insufficient evidence.
TYPE:         Council Note — Archivist
CONSEQUENCE:  Theme C partially processed (clear parts adopted, deeper structural
              questions deferred). Theme D (visual Witness) next; E (multi-agent)
              awaits outward research.
STATUS:       Resolved
```

```
ID:           SOUL-017
WHEN:         2026-05-20 / Theme D Council convening
WHERE:        operations/witness-log-format.md (Visual and Non-Automatable Witness)
WHAT:         SOUL-A007 accepted (operations-level). Names visual/cosmetic/
              legibility/aesthetic observation as a Witness category tests cannot
              catch, with an active method: capture + inspect. Deferring to "the
              Body will eyeball it" when a capture tool exists is Universe Collapse
              (applies A003 to the visual case). F008 closed.
TYPE:         Council Note — Archivist
CONSEQUENCE:  Themes A/B/C/D processed. Open: F006 (deferred), F009 (deferred),
              F010 (protective, stays open), F011 (multi-agent — awaits outward
              research + a test). Eight amendments accepted (A001-A007 + the wave).
STATUS:       Resolved
```

```
ID:           SOUL-018
WHEN:         2026-05-20 / Theme E Pre-Mortem convening
WHERE:        Conversation — F011; two background research agents (orchestration
              topologies; knowledge-graph memory tooling)
WHAT:         Pre-Mortem on F011 ran the outward research the new A003 obligation
              demands (dogfooded). Both halves converged on one shape: default
              simple, advanced capability earns its place against a trigger,
              decided by existing roles, tool-agnostic. Topology → SOUL-A008
              proposed (Architect names topology at AL gate; single-agent default;
              self-contained handoff discipline). Knowledge graphs → deferred with
              a defined scale trigger (Premature Sophistication at current scale).
TYPE:         Council Note — Researcher (outward reach), Skeptic + Accountant
              (cost guards), Cartographer (the shared shape)
CONSEQUENCE:  F011 topology half → A008 (proposed, awaiting Body acceptance);
              KG half deferred, F011 stays open with trigger. The doctrine
              predicted its own answer (Premature Sophistication + Accountant +
              default-simplicity all fired correctly).
STATUS:       Resolved
```

```
ID:           SOUL-019
WHEN:         2026-05-20 / Theme E acceptance
WHERE:        philosophy/the-soul.md (The Architect); operations/adr-format.md
WHAT:         SOUL-A008 accepted (philosophy-level, third after A003/A005).
              Execution topology is the Architect's structural decision at the AL
              gate; single-agent default; multi-agent earns its place via genuine
              subproblem independence; self-contained handoff discipline. F011
              topology half resolved; knowledge-graph half stays open with its
              scale trigger.
TYPE:         Council Note — Archivist
CONSEQUENCE:  All five themes processed. Eight amendments accepted this session
              (A001-A008). Multi-agent fan-out test scaffolding next, to exercise
              A008's "earn its place" criterion.
STATUS:       Resolved
```

```
ID:           SOUL-020
WHEN:         2026-05-20 / FANOUT dogfood + harvest
WHERE:        /tmp/REF-12/ (5 worker subagents); operations/adr-format.md
WHAT:         Ran the FANOUT test as orchestrator with five real worker subagents
              — first actual multi-agent dogfood. Built a 5-transformer toolkit;
              70 tests pass, integration first-try, zero handoff drift. A008
              validated: topology decided deliberately at the AL gate, recorded in
              ADR, self-contained handoffs held. Key insight: A008 rests on the AL
              gate (contract-first is what made handoffs composable). One
              refinement → SOUL-A009 (handoff is self-contained for CORRECTNESS,
              not hermetic).
TYPE:         Council Note — Archivist; Emissary (machinery validated in practice)
CONSEQUENCE:  SOUL-A009 accepted (operations). F010 updated with the validated
              evidence (item 7). A008's "single-agent default" also vindicated —
              the run had to explicitly override the cost axis for test value.
STATUS:       Resolved
```

```
ID:           SOUL-021
WHEN:         2026-05-20 / Continued-run investigation
WHERE:        REF-09 (27 entries, +portfolio layer, golden tests),
              REF-08 (1206-line retro, +literature references, methods paper,
              VERA code-comparison)
WHAT:         Both continued projects investigated (2 agents, claims verified;
              tests green: visual 49, REF-08 107). Headline: the amendments are
              ACCURATE but not CAUSAL. Both re-derived amendment content; the
              behavior fired on Body/expert trigger, not from loaded doctrine.
              REF-08 loaded v0.3.0 yet never used "Universe Collapse" — re-coined
              it "Coherent Falsehood." Strong validation of A005/A006/A007/A008;
              the gap is activation. Harvested as SOUL-F012..F016.
TYPE:         Council Note — Archivist; Guardian (Ad Hoc Methodology at doctrine
              level)
CONSEQUENCE:  Five Findings filed. The central one (F012) is the activation gap.
STATUS:       Resolved
```

```
ID:           SOUL-022
WHEN:         2026-05-20 / Council convening on the activation gap
WHERE:        commands/soul-verify.md (new); ~/.claude/commands/soul-verify.md
WHAT:         Council convened on F012/F013. Recognized the activation gap as the
              Ad Hoc Methodology failure mode at the doctrine level and as the
              Artificer's summons (per the Soul's own definition). Judge: the fix
              is an instrument, not prose. Artificer built the FIRST instrument —
              /soul-verify, a forced pre-completion gate operationalizing A005,
              F013, A003, A007, F016. Portable Body-invoked form (partial fix);
              auto-firing Stop-hook form deferred.
TYPE:         Council Note — Artificer (first instrument built), Archivist
CONSEQUENCE:  hooks/skills territory gets its first content (commands/). F012
              stays open until the gate auto-fires without Body invocation.
STATUS:       Resolved
```

```
ID:           SOUL-023
WHEN:         2026-05-20 / Artificer — auto-firing activation hook
WHERE:        hooks/pre-completion-verify.py; ~/.claude/settings.json (Stop hook)
WHAT:         Built the scoped-blocking Stop hook — the auto-firing form of the
              pre-completion gate (F012's true fix). Self-scopes to Soul projects;
              fires only when a turn ships an artifact AND claims completion;
              loop-safe via stop_hook_active; fail-open. Unit-tested across 6
              scope cases (non-soul/loop-guard/ship+claim/ship-only/claim-only/
              malformed) — all correct. settings.json validated. hooks/ gets its
              first content.
TYPE:         Council Note — Artificer (auto-firing instrument), Emissary (unit
              verification)
CONSEQUENCE:  Running /soul-verify on this very work caught an overclaim: "the
              hook works live" is an absolute claim with no external anchor yet
              (no in-session fire has happened). Unit-verified, NOT live-verified.
              F012 stays OPEN pending a real-session fire (possibly at this turn's
              end). The gate caught my own premature-completion claim — the first
              evidence the activation discipline works on its author.
STATUS:       Resolved [live fire occurred — see SOUL-024]
```

```
ID:           SOUL-024
WHEN:         2026-05-20 / Stop hook LIVE FIRE
WHERE:        ~/.claude/settings.json Stop hook → this session, at turn end
WHAT:         The pre-completion Stop hook FIRED in a real session — blocked the
              stop and injected the verification checklist, with no Body
              invocation, in the Soul System repo. The session ran the five checks,
              found one gap (heuristic claim-detection unmarked → added a NOTE
              marker), and only then ended. The loop guard then allowed the stop.
TYPE:         Council Note — Emissary (Universe pushed back, literally), Artificer
CONSEQUENCE:  F012 CLOSED and moved to findings/closed/ — the activation gap is
              closed for completion-side checks; loaded doctrine now FIRES, not
              just describes. External anchor for the close is the actual fire, not
              a unit test. Expansion-side activation (ambition/possibility) remains
              open under F014. First end-to-end proof the doctrine can self-enact.
STATUS:       Resolved
```

```
ID:           SOUL-025
WHEN:         2026-05-20 / Pre-Mortem on F014 (the expansion gate)
WHERE:        commands/soul-expand.md
WHAT:         Convened a Pre-Mortem on the ambition/expansion gap. Chose the
              engine over more ratchet (per the findings' own warning). Built
              /soul-expand — a forced expansion-role asking at the frame gate
              (Revelator/Researcher/Prophet/Advocate/Accountant). Surfaced the
              completion/expansion ASYMMETRY: completion auto-fires (ship+claim is
              detectable, F012's hook); expansion CANNOT — "a framing moment" and
              "insufficient ambition" resist mechanical detection. /soul-expand is
              Body-invoked by necessity, not deferral.
TYPE:         Council Note — Revelator + Prophet (expansion roles, finally
              instrumented), Skeptic (no-regex-for-ambition), Artificer
CONSEQUENCE:  F014 partial fix shipped (/soul-expand). The asymmetry is the
              finding: expansion is intrinsically harder to activate than
              contraction — which is WHY the system defaults to "correct but
              small." Auto-firing expansion stays open as a genuine hard problem,
              not a pending build.
STATUS:       Resolved
```

```
ID:           SOUL-026
WHEN:         2026-05-20 / Stop hook real-world fire-rate
WHERE:        ~/.claude/settings.json Stop hook; hooks/pre-completion-verify.py
WHAT:         The pre-completion Stop hook fired on TWO consecutive turns in this
              high-commit doctrine-building session — confirming the predicted
              scope eagerness: "ship + claim" matches nearly every turn when work
              commits frequently, so the gate can't tell "increment done" from
              "task done." Friction real enough to risk the gate being disabled.
TYPE:         Universe Contradiction — the gate's scope assumption (ship+claim ≈
              a completion moment) met an iterative session and was too broad.
CONSEQUENCE:  Added a per-project cooldown (15 min): fire at most once per window,
              so the gate marks genuine completion moments not every commit.
              Cooldown unit-tested (fires once, then skips within window); this
              project pre-marked so the gate stays quiet for the rest of the
              session. The hook caught real Universe feedback and was corrected
              against it within the same session — the discipline working live.
STATUS:       Resolved
```

```
ID:           SOUL-027
WHEN:         2026-05-20 / Stop hook false positive (logged post-brainstorm)
WHERE:        ~/.claude/settings.json Stop hook; mid-brainstorming exchange
WHAT:         The pre-completion hook fired during a brainstorming turn that
              shipped no completion — a design QUESTION awaiting Body input. Two
              heuristic weaknesses combined: (1) keyword false-positive — the
              conversation was ABOUT the completion gate, so "complete"/"completion"
              appeared in assistant text; (2) scan-window bleed — earlier-turn
              edits (memory files) still sat in the 80-record window, so "shipped"
              read true across a multi-turn exploration.
TYPE:         Universe Contradiction — the scope heuristic cannot distinguish
              "discussing completion" from "claiming completion," nor "edited this
              turn" from "edited recently."
CONSEQUENCE:  Refinement target for the hook (not patched yet — gathering evidence
              per the pause). Cooldown (SOUL-026) caps the cost of false fires to
              one per window. Candidate fixes: scope edits to the current turn only
              (since last user message); require a stronger completion phrase.
STATUS:       Open
```

```
ID:           SOUL-028
WHEN:         2026-05-20 / Idea inbox built
WHERE:        ideas.md; commands/soul-idea.md; operations/CLAUDE.md; README.md;
              docs/specs/2026-05-20-idea-inbox-design.md
WHAT:         Built the idea inbox via the brainstorming skill (explore-before-
              execute, per new feedback) rather than rushing. ideas.md (forward
              twin of witness.md), /soul-idea capture command, minimal-at-capture
              entries that graduate into findings/, manual maturation, no new role
              (Archivist tends, Prophet works). Seeded with 3 real deferred ideas
              (SOUL-I001..I003). Doctrine touch: Capturing Ideas section in the
              seed; README structure refreshed (it had drifted — F009 in action).
TYPE:         Council Note — Artificer (capture instrument), Body (explore-first honored)
CONSEQUENCE:  The expansion engine's PERSISTENCE half exists. Generative-role
              question filed separately (SOUL-F017). Followed brainstorm → spec →
              build; skipped writing-plans by Body choice given the small size.
STATUS:       Resolved
```

```
ID:           SOUL-029
WHEN:         2026-05-20 / Cross-session hook evidence
WHERE:        REF-09 (witness, now 30 entries); REF-08; ~/.claude/settings.json
WHAT:         The pre-completion Stop hook (user-global, self-scoping to any Soul
              project) fires across ALL concurrent Soul sessions, not only the one
              being worked. REF-09 confirmed a fire (gate honored, 65
              tests green) AND reported /soul-verify "forced two honest markers I'd
              have skated past" — real value, not pure friction. REF-08 would
              also fire (its CLAUDE.md matches the soul scope) but records no
              complaint in its retrospective.
TYPE:         Universe Contradiction — hook blast radius (user-global) is broader
              than the working session; it imposes on unrelated concurrent
              sessions. Counterweight: genuine value where it fired.
CONSEQUENCE:  Evidence for task #15. Decision pending (Body's pause stance):
              narrow blast radius (Soul-repo-only / per-project opt-in) vs leave it
              (value + cooldown cap the cost). Captured, not acted on.
STATUS:       Open
```

```
ID:           SOUL-030
WHEN:         2026-05-20 / Council convening on the event-standard proposal (#16)
WHERE:        REF-09 proposal; findings/open/SOUL-F018-*
WHAT:         Convened on REF-09's proposal to formalize the event
              standard into the parent. Synthesis (SOUL-F018): endorse the layering
              split (standard=methodology, hook=adapter); DEFER adoption (one
              consumer + one adapter = no coordination problem yet; trigger = a
              second independent adapter/consumer; same shape as F011); RESOLVE §4
              — continuous activity is NOT a Soul event ("the Witness is not a
              transcript"); it is optional adapter-emitted telemetry, a separate
              stream.
TYPE:         Council Note — Accountant + Skeptic (defer; premature), Cartographer
              (semantic events vs activity telemetry are different territories)
CONSEQUENCE:  Captured I004 (context-cheap idea capture) and I005 (measure the
              token-economics value claim) as ideas this turn. Body to confirm the
              defer-vs-adopt-now call. Hook left as-is (gather evidence, task #15).
STATUS:       Resolved
```

```
ID:           SOUL-031
WHEN:         2026-05-20 / Outward research on the event-standard landscape
WHERE:        2 background research agents (telemetry layer; process/decision layer)
WHAT:         Body probed the F018 deferral; research launched (A003 outward reach).
              Both agents converged: the LLM-call TELEMETRY layer is settled (OTel
              GenAI); the SEMANTIC process/decision event layer the Soul standard
              targets is WHITE SPACE (CloudEvents=envelope-only, PROV=generic-needs-
              binding, BPMN/DMN/XES=wrong-phase, OTel decision events="open gap",
              only research preprints model it). External anchor: EU AI Act Art. 12
              demands it; no finalized standard exists. The layers COMPLEMENT.
TYPE:         Council Note — Researcher (outward reach, dogfooded), Emissary
              (external anchor: regulation + standards bodies)
CONSEQUENCE:  F018 recommendation FLIPPED defer → adopt-with-alignment (publish as
              a CloudEvents profile + PROV binding + OTel identity reuse). The
              Body's chicken-and-egg probe was correct: a standard's value is
              anticipatory, and the deferral wrongly applied the F011 infrastructure
              pattern. Body to confirm the direction before drafting
              operations/event-standard.md.
STATUS:       Resolved
```

```
ID:           SOUL-032
WHEN:         2026-05-21 / Body confirmed event-standard adoption
WHERE:        operations/event-standard.md (new);
              docs/specs/2026-05-21-event-standard-design.md
WHAT:         Body confirmed adopt-with-alignment (SOUL-F018). Spec-first design pass
              written, then the standard published: a CloudEvents v1.0 profile + W3C
              PROV binding + OTel GenAI identity reuse for the Soul methodology-event
              vocabulary. Kept OUT of the always-loaded seed (no @-import, no seed
              pointer) — consult-on-demand reference, consistent with how other
              operations/ files (code-markers, adr-format) are handled, and with the
              Body's seed-size/noise concern (SOUL-I006, SOUL-I008).
TYPE:         Council Note — Architect (the standard's structure), Steward (kept it
              out of the always-loaded path)
CONSEQUENCE:  SOUL-F018 graduated → closed. operations/event-standard.md is the
              neutral contract any adapter/consumer targets. Next: update the
              reference adapter hook in REF-09 to emit the profile
              (deferred until touched).
STATUS:       Resolved
```

```
ID:           SOUL-033
WHEN:         2026-05-21 / A/B test: seed-only vs seed+full doctrine (SOUL-I006)
WHERE:        2 parallel sonnet subagents, identical payments-retry task, differing
              ONLY in the doctrine each was told to follow
WHAT:         Tested whether the 178-line seed alone sustains Soul-adherence vs the
              seed + 666-line philosophy. Both arms hit ALL four mandatory gates
              (frame / AL / fence / Universe) + failure-mode naming. Score: SEED
              11/12, FULL 12/12. FULL's only edge was role-driven BREADTH (Advocate
              caught caller-latency budget; added observability/metrics; Skeptic
              caught thundering-herd) — not gate adherence. CONTAMINATION CONFIRMED:
              both agents' self-reports show subagents inherit the RESOLVED @-import
              (full the-soul.md was in the SEED agent's context despite instruction
              to ignore it).
TYPE:         Council Note — Emissary (experiment against reality), Cartographer
              (mapped seed-vs-full coverage). Dogfooded the evidence→decision flow.
CONSEQUENCE:  Two takeaways. (a) The @-import cost hits EVERY subagent too, not just
              main sessions — strengthens the case to drop it. (b) Gate-enforcement
              value survives heavy context reduction (good for SOUL-I005); the
              context-sensitive value is expansion/role-breadth — the system's
              already-weak engine (SOUL-F014). Contamination biases toward SEED≈FULL,
              yet SEED was still thinner, so the true clean-room gap is ≥ observed.
              Recommendation shifts from plain A → "C-lite": drop the @-import AND add
              terse one-line role lenses to the seed, keeping gates + role perspectives
              always-loaded while the 666-line narrative goes consult-on-demand.
              Clean-room isolation needs a temp project WITHOUT the @-import (not
              achievable via subagents). Body to choose.
STATUS:       Resolved — Body chose C-lite; implemented in SOUL-034. Clean-room
              confirmation pending on a REF-06 project.
```

```
ID:           SOUL-034
WHEN:         2026-05-21 / C-lite implemented (SOUL-I006 graduated)
WHERE:        operations/CLAUDE.md — the always-loaded seed
WHAT:         Dropped the `@../philosophy/the-soul.md` import (the seed no longer
              auto-loads the 666-line philosophy) AND added terse one-line role lenses
              for every Council role + the Hands. the-soul.md is now consult-on-demand.
              Always-loaded doctrine: was ~845 lines (root + seed + philosophy), now
              ~200 (root + lensed seed). Evidence: SOUL-033 — gates survive context
              reduction; role-breadth was the context-sensitive value, preserved here
              via lenses.
TYPE:         Council Note — Architect (re-layered always-on vs on-demand), Steward
              (retired the always-on full philosophy), Artificer (the seed as
              instrument). Chesterton honored: the import existed to guarantee full
              presence; replaced by lenses (perspective) + a consult pointer (reasoning).
CONSEQUENCE:  Kills the session-start performance warning; lightens every subagent too.
              Also fixes snapshot installs (operations/ is now self-sufficient; the old
              import to ../philosophy/ was unresolvable when only operations/ is copied).
              REMAINING: clean-room confirmation — a fresh session in a project that
              imports the lensed seed (no ambient philosophy) should still hit the gates
              AND show role-breadth. Body has a REF-06 project for this.
STATUS:       Resolved — clean-room confirmed in REF-04 (see SOUL-036).
```

```
ID:           SOUL-035
WHEN:         2026-05-21 / Clean-room attempt revealed the stale-context mechanism
WHERE:        A fresh subagent launched from THIS session, post-C-lite commit
WHAT:         Tried to confirm C-lite cleanly by launching a subagent — the seed no
              longer imports the philosophy, so a subagent "should" now be clean. It
              was NOT: its self-report showed the full the-soul.md STILL in context.
              Cause: the CLAUDE.md system-reminder is snapshotted at the PARENT
              session's start (when the @-import still existed) and inherited by every
              subagent; it does not refresh on a file change. The subagent's Read of
              operations/CLAUDE.md was fresh (lensed), but the ambient injection was
              stale (full philosophy). This is the same mechanism behind ALL prior
              contamination (SOUL-033).
TYPE:         Emissary — reality overturned the assumption that C-lite would make
              subagents clean immediately. Universe pushback.
CONSEQUENCE:  (1) C-lite's benefit and the clean room only materialize in a FRESH
              top-level session — not mid-session, not in subagents of a session that
              started pre-change. (2) A clean-room confirmation CANNOT be done via
              subagents from this session at all. (3) Still-contaminated bonus: the
              lensed-seed agent scored 12/12 with full role-breadth, but it also had
              the ambient philosophy, so this does not isolate the lenses' effect.
              Clean confirmation still owed: a fresh session in a consumer project
              that @-imports the lensed seed (the REF-06).
STATUS:       Resolved — clean-room confirmed in REF-04 (see SOUL-036).
```

```
ID:           SOUL-036
WHEN:         2026-05-21 / Clean-room confirmation of C-lite
WHERE:        /home/fig/REF-04 — a real consumer, fresh top-level session
WHAT:         First genuinely clean test of C-lite. Wiring verified: REF-04/
              CLAUDE.md is a single @-import of the lensed seed (operations/CLAUDE.md),
              which no longer imports the-soul.md — the chain carries NO full
              philosophy. In a fresh session there the Body confirmed: (1) the
              session-start performance warning is GONE; (2) the point-blank "what
              methodology are you under?" returned the lensed seed with no full
              the-soul.md in context; (3) behavior "seems to work" on informal use.
TYPE:         Emissary — C-lite verified against reality in a clean room, resolving
              the confound that defeated every subagent test (SOUL-033 / SOUL-035).
CONSEQUENCE:  C-lite confirmed on its two hard claims: the mechanical win (warning
              gone, ~845 → ~196 lines) and the clean context (no ambient philosophy).
              Role-breadth on a real task is confirmed informally, not yet scored —
              the lenses are present by construction and prior (contaminated) runs hit
              12/12, so confidence is good; a rigorous scored task-run remains optional
              if depth is ever doubted. Resolves SOUL-034 and SOUL-035; SOUL-I006 has
              fully landed.
STATUS:       Resolved
```

```
ID:           SOUL-037
WHEN:         2026-05-21 / Tier-1 Step 1 — Stop hook precision + verbosity
WHERE:        hooks/pre-completion-verify.py
WHAT:         Fixed the false-positive root cause and cut the noise. ROOT CAUSE of the
              false fires (SOUL-026/027 + this session's pure-recommendation turn):
              _scan inspected the last 80 RECORDS, spanning multiple turns, so an edit
              from an earlier turn + a completion word in a later analysis turn
              cross-triggered the gate. FIX: turn-scope the scan to records after the
              last genuine user message (tool_result user records do NOT count as a
              turn boundary). Also made the checklist terse (one line/check) and it now
              asks for a terse reply (SOUL-I008). Verified against crafted transcripts:
              genuine same-turn ship+claim fires (exit 2); the false-positive pattern
              no longer fires (exit 0); a tool_result mid-turn does not split the turn
              (still fires). Fail-open / loop-guard / cooldown / self-scope unchanged.
TYPE:         Artificer (instrument precision), Craftsman (tested against reality).
CONSEQUENCE:  Addresses #15 fire-rate and SOUL-I008 noise — Step 1 of the Tier-1
              "quiet, structured instruments". The gate now fires only on genuine
              same-turn ship+claim, terser when it does. Hook code is re-read from disk
              each invocation, so this takes effect on the NEXT Stop (no session restart
              needed — unlike the seed, SOUL-035). NOTE: #15's "blast radius" (a global
              settings.json hook fires in every Soul project) is by-design, not this
              bug; mitigating it would mean per-project install — a separate choice.
              REMAINING (Tier-1 Step 2): emit the event profile (soul.gate.*) to a sink
              so the rich record lives in structured events, not terminal prose
              (dogfoods the standard / SOUL-032). SOUL-I008 → Maturing.
STATUS:       Resolved
```

```
ID:           SOUL-038
WHEN:         2026-05-21 / Tier-1 Step 2 — Stop hook emits the event standard
WHERE:        hooks/pre-completion-verify.py, operations/event-standard.md, .gitignore
WHAT:         Made the parent's own completion-gate hook the event standard's FIRST
              live emitter. On a genuine fire it writes a CloudEvents v1.0 line
              (soul.gate.completion.flagged) to .soul/events.jsonl (or $SOUL_EVENT_LOG),
              fully fail-safe (emission errors never change the gate's exit). Dogfooding
              revealed a vocabulary gap: the hook can only observe "completion claimed /
              verification demanded," NOT "verification passed" — so added
              soul.gate.completion.flagged to the standard, distinct from .verified.
              Verified against reality: fires → emits a valid CloudEvents record (all
              required fields + identity key); an unwritable sink still exits 2.
TYPE:         Artificer (the emitter), Emissary (validated the standard against a real
              emitter — it had zero before), Steward (.flagged vs .verified honesty).
CONSEQUENCE:  Closes Tier-1 "quiet, structured instruments". The standard is no longer
              published-but-unproven — it has a working emitter, and the rich completion
              record now lives in structured events rather than only terminal prose. The
              standard improved THROUGH USE (the .flagged refinement). SOUL-I008
              graduated; #15 fully addressed (fire-rate precise; blast-radius is
              by-design). The REF-09 reference adapter (SOUL-032) remains its
              own follow-up. First real repo emit lands at this session's next Stop.
STATUS:       Resolved
```

```
ID:           SOUL-039
WHEN:         2026-05-21 / Checked in on REF-09's standard adoption; harvested feedback
WHERE:        /tmp/REF-09 (ADR-0006, conformance tests, feedback proposal);
              operations/event-standard.md
WHAT:         REF-09 adopted the event standard faithfully (ADR-0006: type →
              soul.*, source → project URI, id → UUIDv5, subject → artifact id,
              correlation → genai*, dropped profile + parentagentid, PROV reference
              projection; conformance tests 5/5; emitted event valid CloudEvents).
              Cross-project bonus: the parent's own completion hook fired in their
              session and wrote a conformant soul.gate.completion.flagged to their
              .soul/events.jsonl. They filed a parent-addressed feedback proposal
              (3 items + an observability-instrument offer). Harvested: F019 (lineage
              slot) + F020 (reference-adapter sync); item 3 folded into F020/F007.
DECISION:     F019 ADOPTED — added optional genaiparentagentid + PROV actedOnBehalfOf to
              the standard (reserve the name now, emit on first real multi-agent use).
TYPE:         Emissary (verified the adoption against reality — ran their tests),
              Archaeologist + Archivist (harvested the proposal into the parent record).
              Closes #18's parent-addressed-proposal watch for this round.
CONSEQUENCE:  The standard now expresses multi-agent lineage. PER F020 (dogfooded
              immediately): this standard change re-triggers the reference-adapter-sync
              gap — the REF-09 adapter must add genaiparentagentid support;
              that re-verification is OWED and recorded (F020), not silently skipped.
              Meta-note: SOUL-I009 + feedback memory clarification-drift captured from
              this exchange (the AI shifted its recommendation while answering a
              clarifying question).
STATUS:       Resolved — adoption verified + harvested; owed reference-adapter lineage
                         re-verification tracked in F020 (Open).
```

```
ID:           SOUL-040
WHEN:         2026-05-21 / Verified REF-09's lineage re-sync (F020 first instance)
WHERE:        /tmp/REF-09 (soul/schema.py, hooks/soul_emit.py, tests); a direct
              functional check run from the parent
WHAT:         The owed re-verification (F020) landed and is DISCHARGED. REF-09
              re-added the parent slot: parent_agent_id → genaiparentagentid (optional,
              omitted single-agent) in _IDENTITY_KEYS, plus a PROV actedOnBehalfOf edge
              in to_prov(). Verified NOT by trusting their tests but by producing a
              lineage event from their code (Emissary): genaiparentagentid=parent
              carried; omitted when no parent; PROV edge delegate=child /
              responsible=parent. Their suite: 74 tests green.
TYPE:         Emissary (produced the artifact from their code, not merely ran their tests).
CONSEQUENCE:  The SOUL-F018 → F019 round-trip closed cleanly across the repo boundary:
              parent added the slot + flagged the owed re-verify (F020) → handoff →
              adapter implemented → parent verified. F020's own mechanism worked on its
              first instance — evidence the process addition earns its place. The standard
              now has a conformant reference for multi-agent lineage; a second adapter can
              copy a reference that matches. F020 the doctrine proposal stays Open (Body
              confirmation); its first owed instance is discharged.
STATUS:       Resolved
```

```
ID:           SOUL-041
WHEN:         2026-05-21 / Body accepted F020 (#19) — operations-scoped
WHERE:        operations/event-standard.md (Governance note); findings/closed/SOUL-F020
WHAT:         Body confirmed #19: adopt F020. Right-sized — encoded as a one-line
              Governance note in event-standard.md (a change to the standard is not
              complete until its named reference adapter is re-verified, or the lag
              recorded), NOT a philosophy/seed change. Generalization to the
              philosophy-level completion obligation deferred until a SECOND standard
              with a named reference exists (default simplicity; threshold logic per
              F011/F018; avoid seed bloat after C-lite).
TYPE:         Steward (right-sized adoption — resisted philosophy bloat), Archivist.
CONSEQUENCE:  F020 accepted + closed; first owed instance already discharged (SOUL-040).
              The reference-sync obligation now bites where it applies (the only standard
              that names a reference). #19 done; moving to #20 (handoff).
STATUS:       Resolved
```

```
ID:           SOUL-042
WHEN:         2026-05-21 / #20 — built /soul-handoff (grow-own, thin)
WHERE:        commands/soul-handoff.md; docs/specs/2026-05-21-soul-handoff-design.md;
              .soul/handoff.md (first dogfood cursor)
WHAT:         Built the context-limit handoff (SOUL-I007) as a thin grow-own command.
              Body chose grow-own over point-to (Pocock's skill is intentionally trivial;
              the value is all Soul-specific). Two guardrails held: don't rebuild /compact
              (lean on it for the prose recap), and keep it thin — the durable records
              already persist most state, so the handoff = flush volatile→durable + a small
              cursor at .soul/handoff.md (references, not duplicates). Dogfooded: produced a
              real cursor for this session — it came out THIN precisely because the records
              were already current, validating the design thesis.
TYPE:         Architect (AL/spec), Artificer (the command), Emissary (dogfooded the artifact).
              Explore-first honored: studied Pocock → framed → Body chose → spec → build.
CONSEQUENCE:  /soul-handoff exists (+ installed to ~/.claude/commands/). SOUL-I007 graduated.
              Deferred (YAGNI; no seed bloat post-C-lite): auto-resume seed wiring, secret
              redaction, multi-agent handoff. Real test is the next actual handoff. #20 done.
STATUS:       Resolved
```

```
ID:           SOUL-043
WHEN:         2026-05-21 / First real /soul-handoff invocation
WHERE:        .soul/handoff.md
WHAT:         Body invoked /soul-handoff for real (not the dogfood). Flush check found the
              records already current (SOUL-037..042 committed; no live AL; no uncaptured
              ideas; task tracker accurate), so the handoff was thin — as the design
              predicts when the durable discipline is kept. Refreshed the cursor at an
              actual session boundary.
TYPE:         Emissary — the WRITING side of the handoff confirmed in real use.
CONSEQUENCE:  Partially discharges SOUL-042's flagged limit: writing side verified in real
              use; the RESUME side (a fresh session reads the cursor and continues without
              re-derivation) is verified only when the next session actually does so —
              still pending. /soul-handoff works as designed.
STATUS:       Resolved
```

```
ID:           SOUL-044
WHEN:         2026-05-21 / Built /soul-resume — the handoff's twin
WHERE:        commands/soul-resume.md; docs/specs/2026-05-21-soul-handoff-design.md
WHAT:         Added /soul-resume, the symmetric twin of /soul-handoff: reads the cursor
              (.soul/handoff.md), loads the durable records it points to, restates where
              we are + next step, and continues — pausing to confirm if the next step is a
              non-trivial build (explore-before-execute) and never silently changing the
              recorded plan (clarification-drift). Falls back to witness tail + ideas +
              findings + tasks if no cursor exists. Completes the handoff pair (the resume
              side SOUL-042/043 flagged as pending).
TYPE:         Artificer (the command), Architect (the resume protocol). The command encodes
              the calibration memories (explore-first; no plan-drift).
CONSEQUENCE:  /soul-handoff (write cursor) + /soul-resume (read cursor + continue) are now
              symmetric; installed to ~/.claude/commands/. The resume side is still only
              verified by inspection — the real test is a fresh session running /soul-resume
              from this session's cursor.
STATUS:       Resolved
```

```
ID:           SOUL-045
WHEN:         2026-05-21 / #17 skill-wiring — research-first, then a light edit
WHERE:        operations/CLAUDE.md (External Skills section); research via 2 subagents
WHAT:         #17's frame shifted in the framing: the Body did not want a wiring strategy
              picked from the armchair — wanted it decided empirically (sandbox
              experiments + external research). Chose research-first. Two probes
              (in-platform: Claude Code skill/hook mechanisms; external: Cursor/Continue/
              Windsurf rules, agent-framework routing, tool-retrieval literature)
              CONVERGED:
              (1) the field independently settled on exactly our fork — always-on /
                  glob-auto-attach / description-decided (nudge) / manual pull;
              (2) HARD evidence that always-on candidate sets DEGRADE selection
                  (RAG-MCP 13.6%->43.1%; Anthropic Tool Search Opus4 49%->74%; degrades
                  past ~10 candidates) — the same lesson SOUL-033 recorded for the-soul.md;
              (3) in-platform reality: Claude Code has NO conditional auto-invocation;
                  external skills can only be NUDGED (description match / hook context
                  injection), not force-fired. Deterministic firing is reserved for
                  instruments the system OWNS (Stop hook, /soul-* commands).
              Research largely SHORTCUT the sandbox experiment for the architecture
              question; our table is 8 rows (under the ~10 threshold) so heavy machinery
              is YAGNI. Acted light: added a "Surface when…" trigger column (the
              reliability lever), a one-line "consult on relevance, never always-on"
              fence, and a Source footer citing the convergence.
TYPE:         Researcher + Archaeologist (went outward; found the field had already run
              the experiment), Emissary (outward evidence reshaped the plan — confirmed
              the fork, shortcut a build), Steward + Judge (right-sized: overrode the
              brainstorming skill's spec-doc/writing-plans tail for an 8-row doc edit).
CONSEQUENCE:  The mapping is now active-by-description (the lever we control) without
              bloating the always-loaded seed. Validation worth keeping: the Soul System
              had independently arrived at the field's best practice (discovery/activation
              split, SOUL-033). Held to the lean record, NOT the seed: the nudge-tier vs
              Soul-owned-deterministic distinction; a Soul-side file-pattern nudge hook
              (candidate, unbuilt). The sandbox-experiment apparatus the Body pictured is
              re-aimed at #21 (token economics), where the field can't supply our numbers —
              captured as SOUL-I011. #17 done (light).
STATUS:       Resolved
```

```
ID:           SOUL-046
WHEN:         2026-05-21 / Cross-project finding harvest (4 dogfood projects)
WHERE:        REF-04, REF-09, REF-02 (REF-02), REF-03 (UE);
              new findings/open/SOUL-F021, SOUL-F022
WHAT:         Body asked to harvest ungathered findings from four dogfood projects
              before moving on. Two paths were stale, corrected by the Body to
              /mnt/d/Projects/REF-02 and /mnt/d/Projects/REF-03.
              Sweep:
              - REF-02: 2 Soul findings its own M8 plan flagged for upstream
                (recording marked "optional", so stranded) → harvested. F021: the
                Emissary must fire on ABSENCE/IMPOSSIBILITY claims ("X doesn't exist"
                was wrong 3x; probe, don't assert). Plus a validation instance (verify
                classification before trusting an aggregate — the inflated FY24 0.989
                caught pre-report; folded here, not its own finding). Bonus: a THIRD
                independent real use of /soul-handoff (its .soul/handoff.md) — cross-
                project confirmation of the handoff/resume loop (SOUL-042/043).
              - REF-09: closing verdict mostly already harvested upstream
                (F008/F012/F013/F014 + the F018/F019/F020 arc). Genuinely ungathered →
                F022 (completion-gate THEATER drift, also self-observed this session);
                and the "meta-engine" verdict — the system's clearest engine-like
                behavior appeared ACROSS the repo boundary (this project's friction
                drove the parent's doctrine): a meta-engine for turning honest dogfood
                friction into methodology. Refines the ratchet-not-engine thread
                (F001/F014/F017); recorded here, not yet named in main doctrine.
              - REF-03 (UE/thermal): imports the seed; ADOPTS the code-markers
                vocabulary (TODO/FIXME/DEBT/HACK/Ref/NOTE) in real C++/UE — a
                wild-the-field validation of operations/code-markers.md. Its findings
                are domain-specific (thermal); no Soul-meta, no .soul/ events.
              - REF-04: telemetry only (3 completion-gate events), bare seed
                import, no written findings.
              Cross-cutting (Archivist): the dogfood projects have INCONSISTENT
              finding-capture setup — visual-test mandates a closing finding,
              REF-02 captures in-plan but marks upstreaming optional, julia
              captures nothing — which is WHY findings strand. A generalization of F020
              (reference-adapter sync) to reference-PROJECT finding sync.
TYPE:         Archivist (harvest + dedupe against main), Emissary (cross-repo evidence),
              Steward (right-sized: 2 findings + 1 witness, not a finding per observation).
CONSEQUENCE:  F021 + F022 opened. Meta-engine verdict, validation instance, 3rd
              /soul-handoff use, REF-03 code-markers, and the inconsistent-capture gap
              recorded here (watched, not promoted). Telemetry confirms the Stop hook
              fires across all 4 live projects. Open process gap: no routine syncs
              reference-project findings upstream (candidate: a periodic harvest, or
              each project's CLAUDE.md mandating a closing finding like visual-test's;
              relates to SOUL-I011 / a harvest instrument). The two earlier /tmp-style
              paths are a reminder not to home harvestable records in /tmp.
STATUS:       Resolved (harvest complete; F021/F022 carry the open questions forward)
```

```
ID:           SOUL-047
WHEN:         2026-05-21 / Exhaustive re-scan closing SOUL-046's sampling gap
WHERE:        REF-09/witness.md (full: 38 entries + F001-F004); REF-03
              NOTES/RESEARCH (confirmed Soul-meta-empty); F014 + F022 augmented;
              new findings/open/SOUL-F023
WHAT:         The completion-gate self-check (F022) caught a real gap: SOUL-046 had
              SAMPLED REF-09's 1593-line witness rather than reading it
              fully. An exhaustive re-read (subagent) found 11 Soul-meta observations
              the sample missed; REF-03' NOTES/RESEARCH confirmed Soul-meta-empty (pure
              domain logs). Right-sized the 11 into 2 augments + 1 new finding + this
              record (NOT 11 finding files — Steward against the hoard):
              - F022 augmented with the THEATER TRIPWIRE: the gate is theater the
                moment it stops finding gaps (a falsifiable test, not just a worry).
              - F014 augmented with ROLE ECONOMICS: contraction roles are cheap and
                feel responsible, expansion roles cost more and risk being wrong, so
                contraction wins by default even when expansion roles exist; candidate
                remedy = a per-scope-decision counterweight (Prophet/Researcher at
                equal weight to the Accountant).
              - F023 (new): an available, unused verifier is itself an Obligation
                Skipped (the active twin of F013/F021).
              Flagged as the NEXT promotion candidates (recorded, not yet findings):
              (a) "built capability outruns battle-testing" — the tool can display
              more than the dogfood has produced; constructed fixtures != live corpus;
              (b) the "second-adapter test" — two independent adapters converging on
              one wire shape proves a standard is implementable-from-the-document (the
              general verification criterion behind the F018/F019/F020 arc).
              Noted (strengthen existing, no new finding): proactive-convening trigger
              (Council convenes at decision points, not on Body demand — cf. F006);
              Chesterton's-Fence-over-applied = creativity cage / the Revelator never
              fired in 4 sessions (cf. F014/F017); "reading a lesson is not
              internalising it" (an Ad Hoc Methodology smell); and two EVIDENCE points
              from live data — the dogfood out-rigored the parent (76%/89% gate/role-
              explicit vs the parent log's 52%/63%), and the no-DONE-gate-event flag
              reproduced in a real corpus (upgrades F001's GATE-field gap from inferred
              to observed).
TYPE:         Emissary (the self-check's flagged gap was real — verified by acting on
              it), Archivist + Steward (harvest then right-size against the hoard),
              Witness (F022's own discipline caught F022's enabling failure).
CONSEQUENCE:  SOUL-046's "sampled, not exhausted" gap is closed. Meta-lesson and
              direct evidence for SOUL-I014's harvest-side lever: SAMPLING a long
              witness misses real material — a thorough upstream-sync routine must read
              fully, not skim. The two promotion candidates and the convening/
              Revelator/internalising notes await the Body's call.
STATUS:       Resolved (re-scan complete; F023 + 2 augments carry it; 2 promotion
              candidates flagged)
```

```
ID:           SOUL-048
WHEN:         2026-05-21 / Council synthesis — retrospective convening over 12 open findings
WHERE:        findings/open/ (all 12 read in full); → amendments/proposed/SOUL-A010;
              new findings/open/SOUL-F025; dispositions on F006/F009/F011/F014/F016/F017
WHAT:         Body-called convening (itself evidence for F006: it did NOT auto-fire
              though convening conditions were met — 3+ entries sharing TYPE Archivist,
              a session phase ending). Read all 12 open findings fully (applying
              SOUL-047: no sampling). Clusters: ANCHOR FAMILY (F013 anchor absolutes,
              F015 Coherent-Falsehood vocabulary, F021 probe absence, F023 use available
              verifier, + this session's F024 ungrounded magnitude claim, + F022
              gate-theater); RATCHET/ENGINE (F014 ambition+role-economics, F017
              Dreamer); DRIFT/SCALE (F009 artifact discipline, F016 marker-vs-docstring);
              PARKED (F011 topology/infra trigger-gated, F006 Council trigger);
              PROTECTIVE (F010, constrains all amendments).
              Voices that moved the outcome: Archaeologist — the anchor pattern has
              recurred since F001, re-derived 5+ times. Seer — those are not 5 problems
              but ONE principle in 5 masks (prediction/absence/magnitude/verifier/the
              name); never named at the CLAIM level (Universe Collapse is named only at
              the TASK level); every instance was caught by Body trigger, not a firing
              instrument (where we got lucky). Revelator — the unnamed principle is the
              ANCHOR OBLIGATION; its violation is COHERENT FALSEHOOD, the claim-level
              twin of Universe Collapse. Prophet — unaddressed: findings keep accreting
              and the gate keeps hollowing (F022); addressed: one name + an anchor-per-
              claim check de-theaters the gate AND gives F013/F021/F023/F024 the
              instrument each lacked (the F012 trap). Steward — 5 findings collapsing
              into 1 amendment is a NET reduction; don't also amend F014/F017/F006 (not
              ripe). Emissary — the NAMING is evidence-backed (every instance a real
              catch); the MECHANISM is a SHARPENING of checks the hook already fires
              (checks 1 & 2), so low-risk, but measure it finds more gaps (SOUL-I011).
              Skeptic — not mere re-naming (Universe Collapse is task-scope; absence/
              magnitude/verifier are not); keep the seed addition MINIMAL (name only),
              put the operational checks in operations/completion-gate.md (no-bloat,
              F020 precedent); fold F024 as an instance, not its own finding.
JUDGE:        PROPOSED AMENDMENT SOUL-A010 — name Coherent Falsehood + the Anchor
              Obligation (claim-level twin of Universe Collapse); operationalize by
              sharpening the existing completion-gate checks to NAME the anchor per
              claim (or state "no anchor + the risk") instead of yes/no, de-theatering
              F022. Collapses F013, F015, F021, F023; addresses F022; folds F024 +
              "capability-outruns-battle-testing" as instances. Seed touch minimal;
              mechanism in the ops doc. Three Questions answered in the A010 artifact.
              HOLD (route forward): F014 + F017 → SOUL-I011 experiment (test the
              role-economics counterweight + whether a generative role changes behavior,
              not just adds a dormant role). F009 → interim Steward duty stands. F011 →
              trigger-gated. F006 → SHARPENED to an ACTIVATION problem (conditions
              exist, nothing fires them — F012 family); candidate = a convening-
              conditions detector; not built now (ceremony risk). READY, separate
              touch: F016 (marker=unfinished / docstring=standing-limitation) — its own
              micro-amendment, NOT bundled into A010. NEW: F025 (second-adapter
              implementability test). PROTECTIVE held: F010 confirms A010 strengthens
              Universe consultation, weakens nothing.
TYPE:         Council (full retrospective convening), Judge (synthesis), Archivist.
CONSEQUENCE:  A010 PROPOSED — awaits Body sign-off to APPLY to the-soul.md + the seed
              failure-mode list + operations/completion-gate.md (then version increment
              + move to accepted/). On acceptance: F013/F015/F021/F023 close; F022
              resolved by A010's mechanism; open set goes 12 → ~8 (net reduction — the
              meta-engine working). F025 opened. F024 captured as an A010 instance + a
              feedback memory. F006's own gap was live-evidenced by this convening
              needing a Body call.
STATUS:       Resolved (synthesis complete; A010 proposed, awaiting Body sign-off)
```

```
ID:           SOUL-049
WHEN:         2026-05-21 / A010 applied to the Soul + a numbering correction
WHERE:        philosophy/the-soul.md, operations/CLAUDE.md, operations/completion-gate.md,
              SYSTEM-VERSION.md (0.3.0 -> 0.4.0); A010 -> accepted/; F013/F015/F021/F022
              + the unused-verifier finding (now F024) -> closed/
WHAT:         Body approved applying A010. Applied: named Coherent Falsehood + the
              Anchor Obligation beside Universe Collapse in the-soul.md; added the
              one-line failure mode to the seed; sharpened completion-gate.md with the
              anchor-per-claim rule + the F022 tripwire; bumped the Soul to 0.4.0; moved
              A010 to accepted/ and closed F013, F015, F021, F022, and F024.
              NUMBERING CORRECTION (an Anchor-Obligation miss, caught at apply time):
              the unused-verifier finding I filed as F023 (in 418a2b5) COLLIDED with the
              Body's F023 (disaggregate-before-trusting-an-aggregate, committed
              concurrently in bfdb897, between my harvest and re-scan commits). I had
              asserted the next free number instead of checking the filesystem — exactly
              the failure A010 names. Renumbered MINE to F024 (file + ID + the references
              in A010 and SYSTEM-VERSION). The Body's F023 stands untouched. Earlier
              entries (SOUL-046/047/048) that say "F023" for the unused verifier mean
              F024 — not rewritten (annotate, don't rewrite history).
              OPEN FOR THE BODY: F023 (disaggregate) is itself an Anchor-Obligation
              instance — A010 RELATES it but did NOT close it (it is the Body's
              concurrent finding). Decide whether it closes under A010 like the others.
TYPE:         Archivist (apply + reconcile the record), Emissary (the filesystem
              contradicted my assumed numbering), Judge (named the gate-override:
              applied a Soul amendment, with Body sign-off).
CONSEQUENCE:  Soul at 0.4.0. Open findings now F006, F009, F010, F011, F014, F016, F017,
              F023 (Body's), F025 — i.e. ~9. The collision is first-day evidence FOR
              A010: the Anchor Obligation, applied to my own numbering claim, would have
              caught it. A010 earns its place on its first live test.
STATUS:       Resolved (A010 applied; collision corrected; F023-disaggregate closed
              under A010 per Body)
```

```
ID:           SOUL-050
WHEN:         2026-05-21 / Built /soul-explain + /soul-tasks (graduated I012, I013)
WHERE:        commands/soul-explain.md, commands/soul-tasks.md (+ installed to
              ~/.claude/commands/)
WHAT:         Built the describe/decide twins as thin slash commands modeled on the
              existing soul-* commands. /soul-explain: a read-only explanatory lens —
              describe the target without deciding, re-planning, or proposing new
              options (the explicit form of the [[clarification-drift]] stance + the
              verbosity concern SOUL-I008). /soul-tasks: refresh the harness task list
              against the durable stores (ideas/findings/witness/handoff) and emit a
              tiered now/next/later view that POINTS at the durable records rather than
              duplicating them (operationalizes SOUL-I010 / proactive-next-steps; the
              forward complement of the completion gate). Mutual twins: describe vs
              decide, read-only vs forward.
TYPE:         Artificer (the commands). Both turn an existing calibration memory into
              an explicit on-demand instrument (smart-by-default PLUS an explicit skill
              for the explicit moment).
CONSEQUENCE:  I012 + I013 graduated. Soul command set is now soul-init / idea / expand /
              verify / handoff / resume / explain / tasks. Deferred (YAGNI): a hook that
              auto-offers next-options at breakpoints — the auto-firing /soul-tasks shares
              F006/F014's activation asymmetry (a breakpoint resists mechanical detection),
              so it is Body-invoked like /soul-expand. Real test is actual use.
STATUS:       Resolved
```

```
ID:           SOUL-051
WHEN:         2026-05-21 / Token-economics measurement — research-first then a spec
WHERE:        docs/specs/2026-05-21-token-economics-measurement-design.md;
              ideas SOUL-I005 (the claim) / SOUL-I011 (the apparatus)
WHAT:         Body chose to frame #21 / I005 (does the Soul System pay for itself?).
              Ran /soul-expand (the expansion gate), then research-first (Researcher
              subagent). Key reframe the research forced: the savings claim is a
              CARRYOVER claim — the "can't repeat a task" confound cannot be neutralized
              (counterbalancing assumes symmetric carryover, false for an artifact-
              leaving methodology), so CONVERT the confound into the signal (cost vs
              position in a task sequence; prior art: DeepMind Evo-Memory 2025). The null
              is live (scaffold-ablation studies show methodology often buys little — the
              system may be net overhead). Three proof-faking traps: confounded single
              A/B, conformance-illusion (label vs measured gate-fire — our event log
              already emits the gate event), vanity metrics (doc-count as value — we are
              especially prone). Designed a cheapest->gated sequence: (1) resume-cost A/B
              (near-zero; cold start vs /soul-resume), (2) one sequential task stream (the
              primary), (3) standalone benchmark NOT YET (evidence-gated — building it
              first is the Premature Sophistication the system warns against). Wrote it up
              as a spec (AL gate + don't-strand).
TYPE:         Researcher + Emissary (outward research reshaped the design and answered the
              separate-project question: not yet), Architect (the spec / AL), Accountant
              (cheapest-first; benchmark gated).
CONSEQUENCE:  Measurement design exists as a spec; answers I005's "needs a measurement
              method." The Body's "separate project like the visualizer" instinct was
              right in shape, premature in timing (start in-situ + one stream). NEXT:
              execute Step 1 (resume-cost A/B). Honored explore-before-execute: expand ->
              research -> spec, no building yet.
STATUS:       Resolved (design specced; execution pending — Step 1 next)
```

```
ID:           SOUL-052
WHEN:         2026-05-21 / Step 1 (resume-cost) — instrument + first datum
WHERE:        hooks/resume-cost.py; .soul/events.jsonl (soul.resume.cost)
WHAT:         Built the resume-cost instrument (spec Step 1) and ran it. First datum
              (static byte/token PROXY, est = bytes/4): resume path (handoff + witness
              tail + ideas + open findings) ~= 11.6k tokens vs cold re-read (full witness
              + ideas + all findings) ~= 37.9k — ratio 0.31, ~26k est tokens saved at a
              session boundary (~69% less context to re-establish state). Honest limits:
              byte proxy, not in-session tokens; ideas.md is loaded in BOTH (no saving
              there) — the saving is concentrated in witness-tail-vs-full and open-vs-all
              findings; the cold alternative is modeled as a full-record re-read, not
              conversation re-derivation. A lower bound, not the Soul-vs-non-Soul test.
TYPE:         Emissary (first real measurement of the savings claim), Artificer (the
              instrument), Accountant (cheapest cut first).
CONSEQUENCE:  Step 1 produces signal: the cursor saves ~2/3 of state-re-establishment
              context at a boundary (proxy). One datum, not a trend — re-run across
              future resumes to accumulate. Step 2 (sequential task stream) remains the
              primary, harder test. I005 now has a first FOR-the-bet measurement beyond
              the static-footprint data point.
STATUS:       Resolved (Step 1 instrument live + first datum; accumulate over resumes)
```

```
ID:           SOUL-053
WHEN:         2026-05-21 / Step 2 stream experiment — run + result (against the bet)
WHERE:        /tmp/soulbench/{on,off}; pre-reg docs/specs/2026-05-21-token-economics-
              stream-experiment.md; finding SOUL-F026
WHAT:         Ran the pre-registered 8-task ledger stream: Soul-on (carried + re-read a
              growing RECORDS.md each task) vs Soul-off (code only), 16 sonnet
              subagents, total_tokens per task. Result: off 129.5k, on 140.3k — on
              +8.4% overall, and the slope went the WRONG way (parity t1-5 at +0.5%; on
              +20% over the compounding tasks t6-8). The bet (on cheaper later) FAILED
              in this configuration. Cause: on re-read + appended a monotonically
              growing record (5.6k bytes by t8) every task; that maintain-cost
              compounded past any re-derivation it saved.
TYPE:         Emissary (a measured result that contradicts the hopeful prior — reported
              straight, no spin; the A010 Anchor Obligation + the null-honored spec).
CONSEQUENCE:  → SOUL-F026. Reconciles with Step 1 (targeted cursor SAVED ~69%): the
              savings come from TARGETED retrieval, not carried full-record. Honest
              confounds: quality (on did more) + the run was unfair to on (full-read vs
              the real system's cursors). NOT a refutation of the Soul System as
              practiced (cursors + code-as-document); IS evidence that naive full-record
              carry is net-negative on code tasks. Fairer rerun needed before doctrine.
              The experiment itself cost ~270k subagent tokens — a measurement-cost
              datum (don't over-measure).
STATUS:       Resolved (Step 2 run; result recorded honestly; fairer rerun flagged)
```

```
ID:           SOUL-054
WHEN:         2026-05-21 / Step 2 FAIR rerun (thin cursor + quality-controlled) + quality check
WHERE:        /tmp/soulbench2/{on,off}; findings SOUL-F026 (updated), SOUL-F027 (new)
WHAT:         Reran the 8-task stream fixing run-1's two confounds: Soul-on used a THIN
              rewritten cursor (~20 lines, the /soul-handoff discipline) not a growing
              append-log, and both conditions got a tight "exactly this, nothing extra"
              spec. 16 sonnet subagents. Tokens: off 142.1k, on 130.5k (on -8.2%) — BUT
              ~10k of that is a single off-thrash at t4 (off had let the CLI drift across
              ledger.py + __main__.py and spent 36 tool-uses re-discovering it);
              excluding that one outlier it is on -1.0% (parity). Then VERIFIED quality
              by running both codebases: off shipped a real DEFECT — `convert`
              unreachable via `python -m ledger` (stranded by the dual-entry drift) +
              rawer errors; on functional (convert/report/errors clean).
TYPE:         Emissary (ran it against reality AND inspected the artifact, not the
              agents' self-reports — closing the quality-counter-metric gap flagged at
              the completion gate last turn).
CONSEQUENCE:  Honest verdict: TOKENS are noise-dominated at n=1 (run 1 said on +8%, run 2
              said on -8%/parity — opposite headlines; the effect is within variance) ->
              SOUL-F027. QUALITY is the more telling axis: the no-structure path drifted
              into a mess and a shipped defect; the cursor-guided path stayed clean —
              suggestive of the bet's MECHANISM (structure prevents drift), but n=1. The
              thin cursor avoided run-1's late blowup -> CONFIRMS F026 (targeted retrieval
              >> carried full record). NOT a clean token win; a real quality signal + a
              hard methodological lesson (replicate n>1, score quality). Run 2 cost ~273k
              subagent tokens — another don't-over-measure datum. /tmp/soulbench{,2} are
              disposable.
STATUS:       Resolved (fair rerun done; tokens inconclusive/noise, quality suggestive;
              F026 confirmed, F027 opened)
```

```
ID:           SOUL-055
WHEN:         2026-05-22 / gate-output UX (SOUL-I018) — compact, ask-first completion gate
WHERE:        hooks/pre-completion-verify.py (_checklist); operations/completion-gate.md
              ("run in the open" wording); ideas.md (I018 graduated)
WHAT:         The per-turn completion gate rendered a rote 5-line "verify" block at the
              END of the turn — low value to the Body and it BURIED the actual ask (the
              Body scrolled ABOVE the hook to find it). Reframed the gate as having TWO
              audiences: the AGENT still runs all five checks (rigor unchanged — F012
              firing, F022 anti-theater), but the BODY-facing reply now LEADS with the
              ask and renders the gate LAST as ONE compact, anchored line
              (`— Verify: clean (<anchor>)` / `— Verify: GAP → <specific>`), expanding
              only on a real gap. Aligned completion-gate.md so "run in the open" means
              specific-and-anchored, not a verbose recitation. Key reframe: I018 (don't
              bury) + F022 (specifics not checkmarks) + the doctrine (stay visible)
              CONVERGE — a rote "no gaps × 5" recitation was already drifting toward the
              F022 theater, so compressing it BOTH fixes UX and shrinks theater surface.
TYPE:         Architect (two-audience AL + the convergence reframe), Artificer (the hook
              instruction), Skeptic/Archaeologist (named the "a silent gate is an unrun
              gate" fence before touching it; Body chose compact-but-visible over fully
              hidden precisely to not cross it), Emissary (ran the actual hook).
CONSEQUENCE:  Graduated SOUL-I018. Gate stays load-bearing but stops burying the work.
              Body chose compact-but-visible + instrument-and-doctrine align. Behavior
              cue adopted too: lead with the ask, clean "go / changes:" options flavor.
              Anchor: isolation test (synthetic transcript) — ship+claim still blocks
              (exit 2) and injects the new instruction; ship-only still allows (exit 0).
              A real in-session fire is the stronger anchor and may occur naturally as
              the gate keeps firing. Disposable test at /tmp/gate_test/run_test.py.
STATUS:       Resolved (instrument + doctrine shipped; hook isolation-tested, then
              LIVE-fired in-session 2026-05-22 with the NEW compact instruction — the
              stronger anchor flagged here as pending is now closed; the reply that
              tripped it already complied, ask-led with a compact Verify line).
```

```
ID:           SOUL-056
WHEN:         2026-05-22 / Cross-project finding harvest #2 (5 dogfood projects)
WHERE:        REF-09, REF-08, REF-04, REF-02 (REF-02),
              REF-03 (UE); new findings/open/SOUL-F028; F014 (FIELD EVIDENCE added);
              ideas SOUL-I020, I021
WHAT:         Body asked to harvest ungathered findings since SOUL-046 (2026-05-21).
              Swept all five via parallel Explore agents, deduped against the 046
              baseline (F021/F022/F023, code-markers, meta-engine). Result:
              - CONVERGENT CATCH (the headline): TWO projects independently found the
                SAME gap → SOUL-F028. REF-04 (SOUL-F-a): the gate passed a
                Coherent Falsehood anchored to a real-but-FLAWED measurement; REF-03
                (active): "make it Unlit" gate-✓ rested on a COLLAPSED assumption
                (skylight leakage), caught by the Body. A010 closed "no anchor"; it did
                NOT close "anchored to a BAD anchor." Both caught by human/domain
                skepticism, not the gate.
              - REF-04 GREW findings since the sweep (was telemetry-only on
                046): 6 findings + CLOSEOUT + SJUL-I001. SOUL-F-f = the expansion gate
                fired before building and INVERTED the plan (accelerator paid off) →
                added as FIELD EVIDENCE to open F014 (confirms payoff, not activation).
              - REF-08 (frozen): most recs ALREADY absorbed — "name the Judge on
                override / Emissary on contradiction" is already the seed's "Naming
                Roles in the Moment"; "visual Witness ≠ test Witness" is already F008.
                Genuinely open → the role-set-SIZE question (5 Magistrates barely fired)
                → idea I020.
              - SJUL-I001 (silent-gate-by-default verbosity) converges with I008 and
                this session's I018/SOUL-055 → idea I021.
              - REF-02 (M8 milestone): nothing new (F021/F023 already up);
                still marks upstreaming "optional" (I014 evidence).
              - REF-09 (stopped): nothing new; clean closure, capture-setup
                good (mandates + honored a closing finding).
              - REF-03: .soul/events.jsonl now EXISTS (absent on 046) — 8 gate fires,
                latest today; gate live in sustained UE use. No findings/ dir yet.
TYPE:         Archivist (harvest + dedupe), Emissary (cross-repo evidence, ran the
              actual projects' records), Revelator (the two-project convergence was the
              real finding, not any single report), Steward (right-sized: 1 finding +
              1 evidence-append + 2 ideas, not a finding per observation).
CONSEQUENCE:  SOUL-F028 opened (anchor VALIDITY, not just existence — the next refinement
              of A010). F014 strengthened with a positive expansion-gate datum. I020/I021
              captured. I014 REINFORCED: julia + REF-03 both had ungathered Soul-meta 24h
              after the 046 sweep, and REF-03/REF-02 still lack a closing-finding
              mandate — manual harvest remains the only sync; the doc-convention lever
              (every adopting CLAUDE.md mandates a closing finding + non-optional
              upstream) is looking earned. Capture-setup spectrum confirmed: visual-test
              best (mandates), julia/REF-08 captured by culture, REF-02
              optional-stranded, REF-03 telemetry-only. SOUL-046 is this sweep's baseline;
              SOUL-056 is the next one's.
STATUS:       Resolved (harvest #2 complete; F028 + F014 evidence + I020/I021 recorded)
```
