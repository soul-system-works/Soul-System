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
