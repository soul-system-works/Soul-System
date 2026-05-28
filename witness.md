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

```
ID:           SOUL-057
WHEN:         2026-05-22 / Tackled I014 (capture-side) + F028 (validity-basis guard)
WHERE:        operations/CLAUDE.md (new Reference Projects section); completion-gate.md +
              hooks/pre-completion-verify.py + commands/soul-verify.md (anchor check);
              amendments/accepted/SOUL-A010 (EXTENSION); findings/open→closed/SOUL-F028;
              ideas.md (I014 partial-graduate); SYSTEM-VERSION.md 0.4.1→0.4.2
WHAT:         Two SOUL-056 harvest outputs taken to ground (Body picked both recommended
              forms; F028's sources verified DIRECTLY first — closing the anchor I had
              flagged as subagent-relayed, which is itself an F028 move).
              - I014 (capture-side, partial): the elegant lever — adopting projects
                @import the SHARED seed (soul-init writes only that line), so the
                upstreaming obligation goes in operations/CLAUDE.md ONCE and every
                reference project inherits it (retroactively, no per-project setup, no
                soul-init change). Added a short "Reference Projects" section: owe a
                closing Finding + non-optional Soul-meta upstreaming; handoff names
                ungathered items; N/A to the Soul repo itself. Harvest-side /soul-harvest
                DEFERRED (default simplicity — not until the convention proves insufficient).
              - F028 (closed): folded the validity-basis guard into A010 + the gate (the
                F022 no-new-amendment pattern). The anchor check now asks not just "name
                the anchor" but "name its VALIDITY BASIS — trusted why / wrong if", and
                states the gate's limit (sourcing, not measurement validity; a green gate
                is not a truth certificate). Applied to completion-gate.md, hook check 2,
                soul-verify.md; A010 got an EXTENSION; F028 → closed with a tripwire.
TYPE:         Architect (the seed-import lever for I014; the existence-vs-validity AL for
              F028), Artificer (the four-instrument edits), Emissary (verified both F028
              sources directly — julia SOUL-F-a "external-anchor ≠ correct-anchor"; REF-03
              handoff L40 "make it Unlit = hollow gate-✓, Scott caught it"), Steward
              (fold-in not a new amendment; harvest-side deferred), Skeptic (named the
              gate's honest limit).
CONSEQUENCE:  F028 closed; I014 partially graduated (capture lever live, harvest deferred);
              A010 extended; Soul → 0.4.2. The completion gate now distinguishes anchor
              EXISTENCE from anchor VALIDITY — the next refinement of A010's de-theater
              mechanism. FALSIFIABLE PREDICTION (the anchor for the I014 bet): because
              every reference project now inherits the upstreaming obligation via the seed
              import, harvest #3 should find FEWER stranded items than #2 — check at the
              next sweep against the SOUL-056 baseline. SIDE FINDING (unfixed): soul-init.md
              exists in ~/.claude/commands/ but NOT in the repo's commands/ — a source-of-
              truth gap; the repo should hold its own command.
STATUS:       Resolved (I014 capture lever + F028 guard shipped; F028 closed; 0.4.2)
```

```
ID:           SOUL-058
WHEN:         2026-05-22 / Distribution-mechanism investigation → SOUL-F029
WHERE:        install.sh; ~/.claude/settings.json; commands/ vs ~/.claude/commands/
              (drift check); new findings/open/SOUL-F029
WHAT:         Body asked the consequences of fixing soul-init's repo-absence (SOUL-057):
              would projects get stuck on an old Soul System; do we need a soul-update?
              Investigated the real mechanism instead of asserting from memory. Found TWO
              distribution regimes: REFERENCE (operations/ via @import; the hook via an
              absolute path in settings.json) = live, never stale — which is why all five
              @import dogfood projects already carry the I014/F028 doctrine edits; and COPY
              (the /soul-* commands in ~/.claude/commands/; install.sh snapshot) = frozen,
              no sync. Live anchors: editing commands/soul-verify.md this session left the
              INSTALLED soul-verify stale (drift, proven by diff); install.sh is pinned to
              v0.3.0 (vs 0.4.2) and copies only operations/ — no commands, no hooks. So the
              Body's "stuck on old soul-system" fear is FALSE for @import doctrine, TRUE
              (narrowly) for the copy-distributed commands.
TYPE:         Archaeologist (read the existing distribution mechanism), Emissary (ran the
              drift diff — evidence over memory, an F028 validity-basis move applied to my
              own answer), Cartographer (the two-regime map), Accountant (named the "cheap
              moment" — one machine, all @import).
CONSEQUENCE:  → SOUL-F029 (open): the copies-without-sync gap. No fix made (Body chose
              capture-first, decide deliberately). My prior-turn answer corrected the scary
              framing with real evidence rather than the intuitive "yes, build a
              soul-update" — the update need is real but scoped to the COPY regime, not the
              doctrine. Practical residual now tracked by F029: soul-verify is stale in
              ~/.claude/commands/.
STATUS:       Resolved (mechanism mapped; F029 opened; no fix yet by choice)
```

```
ID:           SOUL-059
WHEN:         2026-05-22 / F029 resolved — commands on the symlink (live-reference) model
WHERE:        commands/soul-init.md (added to repo); ~/.claude/commands/soul-*.md (8
              symlinks → repo); findings/open→closed/SOUL-F029; SYSTEM-VERSION 0.4.2→0.4.3
WHAT:         Body picked the symlink model for F029 (AL: only COMMANDS violated the
              run-the-current-instrument invariant; doctrine @import + the hook's absolute
              path already satisfy it — left untouched, Chesterton's fence). Implemented:
              brought soul-init.md into the repo (it had lived only in ~/.claude/commands/
              — the SOUL-057 side-note), then symlinked all 8 ~/.claude/commands/soul-*.md
              → the repo. Every instrument is now live-reference; command drift is
              structurally impossible. Two of F029's three faces closed at once (stale
              soul-verify + soul-init repo-absence); the third (install.sh snapshot /
              multi-machine sync) DEFERRED as YAGNI with a re-open trigger.
TYPE:         Architect (one live-reference model for all instruments), Artificer (the
              symlinks + soul-init-to-repo), Emissary (verified the installed soul-verify
              now serves the 58-line F028 version THROUGH the symlink — drift gone, by
              evidence not assumption), Accountant (deferred multi-machine sync — cheap
              moment, no 2nd machine yet), Skeptic (named the residual honestly).
CONSEQUENCE:  F029 closed; Soul → 0.4.3. The system now has ONE distribution model for its
              instruments — live-reference (doctrine via @import; hook + commands via the
              filesystem) — instead of two unreconciled regimes. soul-verify drift fixed
              live. DEFERRED: install.sh still 0.3.0 + operations-only; address when a 2nd
              machine/snapshot exists. RESIDUAL (an F028 validity-basis flag on my own
              fix): "the loader follows symlinks" is filesystem-confirmed but not yet
              reload-confirmed — low risk. Symlinks are machine-local (~/.claude), not
              committed; the repo change is soul-init.md + records.
STATUS:       Resolved (symlink model applied + verified; F029 closed; 0.4.3)
```

```
ID:           SOUL-060
WHEN:         2026-05-22 / I017 deep dive — Researcher pass + framing + reference-repo bootstrap
WHERE:        ideas.md (I017 → Maturing + DEEP DIVE notes); references/ (FIRST use —
              references.json + INDEX.md + 4 sidecars)
WHAT:         Body asked for a deep dive into I017 (auto-grow tool/skill knowledge),
              Researcher-first. Spawned a web research subagent (prior-art sweep), then
              framed. KEY RESULT: don't build a skill engine — Agent Skills already IS one;
              the field's UNSOLVED part IS I017's need and is the Soul's home turf. A 2026
              survey (agent-skills-survey-2026) names "model-internal learning → portable,
              auditable, GOVERNED SKILL.md" as open; a 2026 benchmark
              (agentic-skills-wild-2026) shows ungoverned proliferation DEGRADES selection
              (relevant skill loaded ~49%) — corroborating SOUL-033 never-always-on.
              Whitespace: tool-operation know-how for tools with no machine-readable spec
              (Dymola, UE-headless). MAPPING: the gap = the Soul ratchet + idea ladder +
              Steward + Anchor/F028. Body chose the MVP build (explicit capture command,
              draft-for-curation, ratchet-gated promote, Steward retirement; defer
              auto-distill) + capture via enrich-I017 + the reference-repository.
TYPE:         Researcher (the prior-art subagent — outward reach), Revelator (the
              gap = Soul's-home-turf reframe), Archaeologist (Voyager/CoALA lineage),
              Emissary + Skeptic (VERIFIED all 4 citations against arXiv BEFORE enshrining
              them — an F028/Anchor move on my own research; the subagent's IDs held, exact
              titles corrected), Archivist (first reference-repository use).
CONSEQUENCE:  I017 → Maturing, build direction chosen. Reference-repository used for the
              FIRST time (was "proposed", unused) — bootstrapped with 4 verified refs +
              honest validity-basis notes (specific figures flagged secondary-reading, not
              yet primary-confirmed — F028 in practice). Next: build the /soul-skill
              capture-command MVP. Resonance: the landmark prior art (Voyager) shares its
              name with the folder this dogfood family lives under (/REF-02).
STATUS:       Resolved (deep dive done; research verified + captured; build teed up)
```

```
ID:           SOUL-061
WHEN:         2026-05-22 / I017 graduated — /soul-skill governed-capture command built
WHERE:        commands/soul-skill.md (new); ~/.claude/commands/soul-skill.md (symlink,
              F029); ideas.md (I017→Graduated; +I024, +I025); SYSTEM-VERSION 0.4.3→0.4.4
WHAT:         Built the /soul-skill MVP from the SOUL-060 deep dive, via a grill + a
              scoped Council the Body requested. Resolved the contract by grilling: Q1
              self-contained (write-a-skill's discipline-wrapper, not a 2nd engine), Q2
              manual-fire + a two-part verified bar (F028 anchor OR low-confidence; AND
              playbook-sized not note-sized), Q3 provenance. Reached outward FIRST (the
              I019 instinct) — read the Agent Skills open standard + Anthropic's
              large-codebase best-practices blog — then convened. KEY EMISSARY MOMENT:
              the full agentskills.io/specification OVERTURNED my mid-grill Q3
              recommendation. I had argued provenance-in-frontmatter was non-standard;
              the spec DEFINES an optional `metadata:` map (spec example = author+version)
              plus `compatibility`, `license`, and an official `skills-ref` validator. So
              provenance flipped INTO frontmatter `metadata:` (soul-* keys) —
              standards-native + portable + zero discovery cost — not a Source-Footer
              body block. Also surfaced/captured I024 (/soul-finding scaffolder?) and
              I025 (Obsidian/GUI access layer riding the standards).
TYPE:         Artificer (the command) + Architect (the SKILL.md contract); Researcher +
              Emissary (read the standard + blog; the /specification overturned my own Q3
              rec — the F028/Anchor discipline applied to my recommendation, as SOUL-060
              did to its citations); Skeptic (kept Q1=B honest — without the verify gate +
              provenance + retire handle, /soul-skill IS redundant with write-a-skill);
              Steward (the 3–6mo retire cadence + never-always-on); Council (the scoped
              synthesis the Body asked for — Architect/Steward/Skeptic/Researcher/
              Advocate/Accountant/Cartographer, not the full chamber).
CONSEQUENCE:  I017 graduated; Soul → 0.4.4. First instrument that GOVERNS external,
              non-Soul artifacts (tool-knowledge SKILL.md files in other projects):
              verify-first (two-part bar + skills-ref), standards-native provenance
              (`metadata.soul-*`), retirement (`soul-status` + the 3–6mo/post-model-release
              cadence). Live-load CONFIRMED — /soul-skill appeared in the session skill
              listing through the symlink (F029 holds for the new command). EXTERNAL
              CORROBORATION of SOUL-033 (twice over): the harness's own description-budget
              eviction AND Anthropic's review-cadence guidance — never-always-on is no
              longer just our theory. DEFERRED: auto-distillation, auto-promote,
              plugin-packaging. RESIDUAL (honest): skills-ref not installed (manual-checklist
              fallback active, as the contract anticipates); the command is UNTESTED on a
              real capture — its first real use (capturing e.g. the dymola or UE-headless
              know-how) is its Emissary test. NOT COMMITTED yet (awaiting Body).
STATUS:       Resolved (MVP built + symlinked + live-loaded; I017 graduated; 0.4.4)
```

```
ID:           SOUL-062
WHEN:         2026-05-22 / Emissary test — /soul-skill run against the real dymola-sim-debug skill
WHERE:        ~/.claude/skills/dymola-sim-debug/SKILL.md (provenance retrofit);
              commands/soul-skill.md (2 refinements folded in: steps 4 + 5)
WHAT:         First real exercise of /soul-skill (its Emissary test), per the Body's
              choice. Ran the contract against the existing hand-built dymola-sim-debug
              skill (born 2026-05-01, no provenance). Trigger gate PASSED (verified
              anchor "Esdirk45a→Dassl, 535s→38s, measured"; playbook-sized; confidence
              high). Steward overlap-check correctly routed to UPDATE the existing
              (global) skill, not duplicate. Retrofitted `metadata.soul-*` + `compatibility`,
              then VALIDATED by parsing the frontmatter as YAML against the standard
              (skills-ref absent → manual + parse fallback): PASSED — `metadata` is the
              spec's string→string map; name==dir; description 336≤1024; compatibility
              78≤500; soul-confidence/status in their enums. THE CONTRACT HELD.
TYPE:         Emissary (took the instrument out to a real artifact and tested it — held),
              Steward (the overlap→update branch fired correctly), Skeptic (caught that
              the contract over-defaulted `paths:`), Artificer (folded the refinements back).
CONSEQUENCE:  /soul-skill validated against reality on the UPDATE-EXISTING path; contract
              refined: (1) step 5 now says update-existing edits the skill where it lives
              (overrides the project-local default when global); (2) step 4 softened
              `paths:` to optional-with-reasoning (a Python-driven Modelica skill's `.mo`
              glob could suppress wanted activation); (3) provenance could NOT be fully
              reconstructed retroactively — soul-captured recovered from the filesystem
              birthdate, soul-last-verified inferred from the build run — which PROVES the
              value of capture-time stamping going forward. dymola-sim-debug now carries
              governed provenance (last-verified 2026-05-01 = 3 weeks old, well inside the
              3–6mo retire window). EXTERNAL CORROBORATION (byproduct of the build research):
              SOUL-033 never-always-on is independently confirmed by Anthropic's own
              description-budget eviction + 3–6mo review cadence — recorded HERE, not
              inflated into a separate Finding (the I024 anti-inflation discipline:
              findings are earned, not frictionless). RESIDUAL (honest): the FRESH-CAPTURE
              path (distill-from-just-happened → create-new) is still UNTESTED; the next
              genuine in-session tool success should exercise it (a dymola agent is
              available for small-model runs if a fresh test is wanted). NO Finding opened
              — refinements fixed inline (no open work), corroboration is confirmation.
              NOT COMMITTED yet (awaiting Body).
STATUS:       Resolved (Emissary test passed on the update path; contract refined; fresh-path residual noted)
```

```
ID:           SOUL-063
WHEN:         2026-05-22 / Cross-project harvest from greenwoodms06.github.io (reference project)
WHERE:        blog repo — src/pages/projects/[...slug].astro, src/content/projects/* (new
              Soul-System entry + two hand-authored SVG icons), .soul/events.jsonl; this
              repo — findings/open/SOUL-F030.
WHAT:         Brought the blog (a seed-importing reference project) to its first successful
              GitHub-Pages deploy + a content pass. On every turn that shipped a VISUAL
              change — repo/demo button restyle, the new Soul-System project page with an
              embedded architecture SVG, two bespoke SVG card icons — the F012 hook fired
              check #4 (visual capture+inspect). The agent answered it in prose ("GAP → not
              eyeballed") and shipped on a green build, deferring the look to the live
              site / Body. The gap only genuinely closed on the icons, when the agent
              rasterized the SVGs via sharp and Read the PNGs back (caught nothing wrong
              this time — but proved the method). Harvested into SOUL-F030.
TYPE:         Archivist (cross-project harvest — FIRST from outside the Soul/dogfood
              families); Emissary (rasterize+Read finally consulted the Universe on the
              pixels); Guardian (the gate WORKED as a detector of the repeated deferral,
              but had no method to enforce the fix — the F030 gap).
CONSEQUENCE:  SOUL-F030 opened (activation+technique gap: A007/F008 present, check #4
              named, yet capture-and-inspect defaults to deferral without a one-step
              recipe). Reference-project closing obligation (seed §Reference Projects)
              discharged on the upstream side: Soul-meta finding sent home. Blog's own
              closing record lives in its .soul/handoff.md cursor. NOT COMMITTED yet
              (awaiting Body — repo also carries unrelated pending LICENSE/amendment edits).
STATUS:       Resolved (harvested; SOUL-F030 carries the open work)
```

```
ID:           SOUL-064
WHEN:         2026-05-22 / Fresh-capture path tested — /soul-skill create-new on REF-03 UE-headless
              (renumbered from 063: a CONCURRENT session claimed SOUL-063 + SOUL-F030 mid-work)
WHERE:        /mnt/d/Projects/REF-03/.claude/skills/ue-headless-wsl-run/SKILL.md (new draft)
WHAT:         Closed SOUL-062's residual (the fresh-capture / create-new path was untested).
              Per the Body's pick, exercised /soul-skill's create-new branch against the REF-03 UE
              project. Primary-verified the anchor FIRST rather than trusting the Explore subagent's
              secondary reading (the F028 discipline applied to a delegated investigation): confirmed
              commit f628a83, read run_stage_headless.sh in full, found "S07_AutoRealism 8/8" in
              REF-03/.soul/handoff.md. Distilled the WSL-headless-UE PATTERN (stable across many NOTES
              G-entries) — NOT the thermal results — into a project-local SKILL.md: launch invocation,
              Development-not-DebugGame hang, explicit-map-path (G18), WSL→Windows networking +
              firewall, stale-recording cleanup, taskkill. Steward-check: no existing skill → genuine
              create-new. Validated by YAML-parse vs the standard: PASSED (name==dir; desc 434≤1024;
              compatibility 168≤500; metadata string→string map; enums valid; 64 lines).
TYPE:         Emissary (create-new path tested against a real project — held), Archaeologist (read
              primary sources to distill faithfully), Skeptic + Emissary (primary-verified the anchor
              vs trusting the subagent — F028 on a delegated result), Steward (no overlap → create-new),
              Artificer (the capture), Guardian (caught the concurrent-write / ID-collision — stopped
              rather than clobbering the parallel session's SOUL-063/F030).
CONSEQUENCE:  /soul-skill now validated on BOTH paths — update-existing (SOUL-062) + create-new
              (this) — the MVP's residual is closed. ue-headless-wsl-run captured as a DRAFT for
              curation in REF-03 (uncommitted there; the Body curates). Anchor honestly dated
              2026-05-21 (last-known 8/8; later #96/#97 material work MAY have disturbed S07 — the
              skill's Verify step is the re-confirm handle; a live re-run is the optional gold
              upgrade). SPOTTED (I014, live): REF-03 carries an un-upstreamed Soul-meta lesson (the
              "make-it-Unlit = Universe-Collapse miss + hollow gate-✓, Scott caught it" —
              auto_realism_baseline_decided.md / handoff L40), the same hollow-gate evidence that fed
              F028 — a candidate to harvest upstream. CONCURRENCY GAP SURFACED: a parallel session
              edited witness.md (SOUL-063 + F030) uncommitted on top of my committed dcdacf2 — the
              durable records assume a single writer; concurrent agents collide on IDs and risk
              lost updates. Worth an idea/finding (offered to the Body, not auto-created).
STATUS:       Resolved (fresh-capture path tested + passed; both /soul-skill paths validated; REF-03
              skill drafted; renumbered around the concurrent SOUL-063; I014 + concurrency items flagged)
```

```
ID:           SOUL-065
WHEN:         2026-05-22 / Cross-project harvest from REF-03 (reference project) — closes
              the I014 obligation surfaced in SOUL-064.
WHERE:        REF-03/docs/adr/0010-default-surface-micro-variation.md L295–310 (primary
              source: the "first rec was 'make it Unlit' — Universe-Collapse miss"
              self-naming in the 2026-05-21b Addendum); this repo —
              findings/open/SOUL-F014-ambition-gate-still-missing.md (FIELD EVIDENCE
              appended); STATUS line widened.
WHAT:         Discharged REF-03's non-optional reference-project Soul-meta upstreaming
              obligation (seed §Reference Projects + [[SOUL-I014]]). Primary-verified the
              evidence in REF-03 ADR-0010 (NOT trusting the SOUL-064 summary; F028
              discipline applied to a harvest), then distilled the cross-project pattern.
              The REF-03 case: agent recommended making M_ThermalLandscape Unlit to fix a
              skylight residual leaking BaseColor into thermal ε; locally correct, but
              the same asset is also reached by the co-registered RGB sensor + editor —
              Unlit would flatten terrain there. Universe collapsed to "the thermal pass."
              The Body caught it; the correct fix (Default-Lit + MPC-gated lit inputs)
              only happened because a human held the wider Universe. Steward-checked
              candidate findings (F014 expansion gap, F028 anchor validity, opening a new
              SOUL-F032) and confirmed with the Body: best filed as FIELD EVIDENCE on F014
              (same root: expansion / outward-reach without the Body), honoring the I024
              anti-inflation discipline. New sub-twist recorded: the gap fires at
              RECOMMENDATION TIME on SHARED ASSETS, not only at framing time (julia
              evidence was framing-time). Notable: doctrine and naming were PRESENT — the
              agent self-named "Universe-Collapse miss" in retrospect; the gap is purely
              ACTIVATION, not awareness. Widens F014's open question accordingly.
TYPE:         Archivist (cross-project harvest — second from outside the Soul/dogfood
              families, after SOUL-063 from the blog), Emissary (primary-verified the
              ADR-0010 lines rather than trusting the prior summary — F028 on a harvest),
              Steward (resisted opening SOUL-F032 when F014 sharpening was the correct
              shape), Guardian (named the I024 anti-inflation discipline at the
              decision).
CONSEQUENCE:  F014 now carries cross-project FIELD EVIDENCE on BOTH SIDES: julia (positive,
              framing-time, the gate paid off when Body invoked it) + REF-03 (negative,
              recommendation-time, the gate didn't fire and the Body caught the miss).
              The open question is sharpened: expansion-without-Body must cover both
              framing and shared-surface recommendation moments. Reference-project
              upstreaming obligation discharged for the REF-03 2026-05-21 work. Working
              tree carries only the F014 edit + this witness entry (plus the Body's
              pre-existing LICENSE / SOUL-A008 deletion, untouched). NOT COMMITTED yet
              (awaiting Body).
STATUS:       Resolved (harvest complete; F014 sharpened, not multiplied)
```

```
ID:           SOUL-066
WHEN:         2026-05-26 / F030 + F031 graduated — operational refinement, not new doctrine.
WHERE:        hooks/pre-completion-verify.py (`_checklist()` check #4); commands/soul-verify.md
              (check #4); findings/closed/SOUL-F030*.md + SOUL-F031*.md (moved from open with
              closure stamps); SYSTEM-VERSION.md → 0.4.5.
WHAT:         Closed the F030 (negative — blog) / F031 (positive — REF-01) pair as a
              single operational fix. Hook check #4 and soul-verify.md check #4 now embed
              three things: (1) the DEFAULT CAPTURE RECIPE — rasterize via the project's
              own image lib (sharp for SVG, matplotlib for polygon coords) and Read the PNG
              back, OR screenshot the page via the project's run/verify skill — so "inspect"
              has a one-step instantiation independent of the Body's eye; (2) the NON-PASS
              RULE — a prose "GAP → not eyeballed" on a visual change is an admission the
              obligation was skipped, not a clean line; (3) the SPLIT (per F031's residual)
              — (a) DESIGN-CAPTURE (headless-dischargeable via the recipe; catches the
              geometry/encoding defect class — F031 actually caught a self-intersecting
              turbine polygon this way) vs (b) TARGET-TOOL render confirm (may legitimately
              require Body/tool); the residual is now NAMED, not folded into "not eyeballed."
              Hook line: one extra clause (terse-by-design honored, SOUL-I008). Soul-verify
              line: fuller prose with example libraries. INDEXING SLIP NOTED: both findings
              referenced "check #4 in completion-gate.md," but that file's #4 is Advocate /
              Skeptic (load-bearing claim), not visual; the visual check lives only in the
              hook + soul-verify.md, which is where the fix went. completion-gate.md left
              untouched (its scope is outward-reach, not visual — separate concern).
TYPE:         Artificer (the gate-line edits), Steward (chose operational refinement over a
              new amendment — A007 already mandates capture+inspect, this is activation +
              technique), Archivist (closed both findings together; moved to findings/closed/),
              Guardian (caught + recorded the F030/F031 indexing slip rather than silently
              fixing).
CONSEQUENCE:  Two open findings → closed. Hook now nudges agents toward an actionable recipe
              instead of leaving "inspect" as posture. Reference-project upstreaming pattern
              continues to deliver: F030 + F031 came home from greenwoodms06's blog +
              REF-01 (a static site + a Modelica/Dymola codebase — two very different
              visual modalities, both pointing at the same activation gap). Open visual-gate
              question DOES survive: the recipe is now NAMED in the hook line, but whether
              an agent actually *reaches for it* on a fresh visual task is still untested
              — the F012 family of "doctrine names, gate doesn't fire" pattern (also F014,
              F028 earlier) persists. Activation evidence will accumulate in future visual
              sessions; if the new recipe-pointer doesn't itself activate, that becomes a
              new Finding in the F012 family ("named recipe, still not reached for"). NOT
              COMMITTED yet (awaiting Body).
STATUS:       Resolved (F030 + F031 closed; hook + soul-verify.md carry the recipe + split +
              non-pass rule; SYSTEM-VERSION → 0.4.5)
```

```
ID:           SOUL-067
WHEN:         2026-05-26 / "Now"-tier triple: /soul-finding, /soul-help, I027 protocol.
WHERE:        commands/soul-finding.md (NEW); commands/soul-help.md (NEW);
              commands/soul-idea.md (back-port: new step 3 = I027 re-read-verify);
              ~/.claude/commands/soul-finding.md + soul-help.md (NEW symlinks per F029);
              ideas.md (SOUL-I015 → Built; SOUL-I024 → Built; SOUL-I027 → Partially
              delivered); SYSTEM-VERSION.md → 0.4.6.
WHAT:         Shipped the three "now"-tier instruments in one batch.
              (1) /soul-finding (I024 graduated). Built as a SCAFFOLDER, not a
              frictionless inbox — the asymmetry the original NOTES surfaced. Body
              decides the witness→finding graduation; the command does the mechanical
              work: confirm Body's call, gather inputs, re-read-verify ID via the I027
              protocol, write to findings/open/SOUL-F###-<slug>.md in standard format,
              flag the I014 upstream route for reference-project Soul-meta findings.
              Refuses to scaffold without explicit Body call (anti-inflation guard).
              (2) /soul-help (I015 graduated, MVP shape). Runtime roster of every
              /soul-* command + one-line summary + pointers to philosophy/findings/
              ideas/witness. Reads commands/ live so it cannot drift. The "lost-user
              orient" half deferred — overlaps with /soul-tasks and needs a definition
              of "lost" to ground it.
              (3) /soul-idea back-ported with the I027 re-read-verify-before-write
              step (new step 3): re-scan ideas.md, confirm assigned ID is free,
              increment+retry if collided, stop+tell-Body after three collisions.
              Single-filesystem only; documented scope.
              I027 itself goes Partially delivered: detect-only option (4) landed
              where there's a command; cross-machine (option 2, git-as-arbiter),
              command-less witness writes, and direct-file-edit bypass all still
              open. /soul-skill needed no change — skill names aren't auto-numbered.
TYPE:         Artificer (built the two commands + the back-port), Steward (chose
              scaffolder over inbox for finding; chose detect-only over UUID-change
              or lock for I027 — preserves human-friendly IDs, no stuck-lock failure
              mode), Architect (the symlink-per-F029 distribution pattern reused;
              I027 protocol declared minimally portable across commands).
CONSEQUENCE:  Three ideas closed/advanced in one session: I015 + I024 Built; I027
              Partially delivered. /soul-finding will lower the friction on the
              non-optional I014 closing-Finding obligation — every reference project
              that finishes work owes a Soul-meta finding upstream; the scaffolder
              makes that mechanical rather than a 40-line manual recreation each
              time. I027 protocol now baked into /soul-finding from creation (won't
              repeat the SOUL-064 collision for findings) and into /soul-idea
              (won't repeat for ideas). Next big-rock: SOUL-I026 (The Mind),
              flagged by the Body as the next thread after this "now"-tier batch.
              NOT COMMITTED yet (awaiting Body).
STATUS:       Resolved (three deliverables shipped; symlinks live + verified via
              the system-reminder skill-list refresh showing soul-finding +
              soul-help; SYSTEM-VERSION → 0.4.6)
```

```
ID:           SOUL-068
WHEN:         2026-05-26 / The Mind MVP shipped (SOUL-I026 graduated → 0.5.0)
WHERE:        commands/soul-distill.md (NEW); mind.md at repo root (NEW); CLAUDE.md
              + operations/CLAUDE.md + commands/soul-init.md (Mind import + pointer);
              philosophy/the-soul.md (§The Distiller + §The Mind + Distiller↔Archivist
              pair + Starting-a-Session pointer); SYSTEM-VERSION.md → 0.5.0;
              docs/specs/2026-05-26-the-mind-design.md;
              docs/plans/2026-05-26-the-mind-implementation.md;
              docs/experiments/2026-05-26-mind-tier1-candidate.md;
              ideas.md (SOUL-I026 → Built; SOUL-I028 captured for deferred figure).
WHAT:         Closing entry for the Mind MVP arc — the longest single-session build of
              this session-block (~9 commits). The full chain:
              (1) BRAINSTORM (skill: /brainstorming). Body's framing — Kolmogorov /
              MDL applied to project state: "the best representation is not a
              description but the shortest set of rules that would reproduce it."
              (2) NECESSITY TEST FIRST (Body instinct, F014 expansion-gate fire on
              the Mind concept itself — the gate working). Tier 1 (hand-craft) → Tier
              2 (subagent A/B) → Tier 3 (build).
              (3) TIER 1: hand-crafted candidate Mind from Soul's own record, 218
              lines, four buckets + named residual + bias-warning honesty.
              (4) TIER 2: held-out A/B on "should /soul-witness be built?" with the
              I011 substrate (two parallel subagents). Arm A (full record): 42K
              tokens, conditional YES (scaffolder). Arm B (Mind-only): 25K tokens
              (~41% cheaper), conditional NO (case unearned). DISAGREEMENT on
              direction was the most informative datum — Arm A pulled obligation-
              specific facts (SOUL-A001 lifecycle, SOUL-I014 upstream route) absent
              from the Mind; Arm B leaned on doctrinal rules + tensions. Verdict:
              Mind is a LENS layer, not a replacement; doctrine-vs-obligation is the
              load-bearing boundary.
              (5) SPEC: 8 sections, Body-approved one by one, written to
              docs/specs/2026-05-26-the-mind-design.md (311 lines).
              (6) PLAN: writing-plans skill adapted for non-code (markdown/symlink/
              wc/grep verifications), 8 tasks, ~6 commits, docs/plans/.
              (7) BUILD: /soul-distill spec (162 lines, mirrors /soul-skill) +
              symlink + pruned mind.md (169 lines) + Emissary test of /soul-distill
              against draft (4 shrinkage checks + 6 guards + 3 diagnostic Qs all
              clean) + seed/soul-init wiring + philosophy update + version bump.
              (8) DOCTRINE UPDATE: philosophy/the-soul.md gained §The Distiller
              (Magistrates), §The Mind (after §Amendment Process — the system-level
              analog framing), Distiller↔Archivist opposing pair, Mind pointer in
              §Starting a New Session.
TYPE:         Architect (lens-layer design from Tier 2 evidence), Artificer (the
              command + deployed artifact + all six MVP wiring touches), Emissary
              (Tier 1 + Tier 2 + Task-4 self-test — three rounds of taking the
              instrument out to reality), Skeptic (bias warning kept visible through
              Tier 1; "two arms disagreed" reported honestly, not spun), Steward
              (necessity test first; explicit retire conditions in the command),
              Revelator (the project-level-analog-of-amendment-process reframe was a
              "what was always true but unseen" moment), Guardian (caught the
              parallel-session ID collision; F028-discipline check on the SOUL-033
              seed-line citation).
CONSEQUENCE:  Three-layer doctrine now (seed → Mind → records); the Soul System is
              its own first dogfood. F014 expansion gap got NEW field evidence: the
              Body's "is The Mind even necessary?" check fired DURING the brainstorm
              and shaped the design — expansion-without-Body still untouched as the
              open question, but the human-driven activation is now demonstrably
              effective and worth capturing. CONCURRENCY-GAP LIVE EVIDENCE: during
              this build a parallel session committed fafb416 (findings F032-F035
              from REF-05) — exactly the SOUL-I027 single-writer
              assumption breaking in practice. No collision on IDs this time
              (different artifact spaces), but the witness ID race could have
              happened — the I027 protocol baked into /soul-finding + /soul-idea
              would have caught it, and /soul-witness (still deferred) would
              eventually need the same. DEFERRED for follow-up: Tier 3 deployment
              validation (the 2-3-question A/B on the deployed Mind, then dogfood
              on REF-03); SOUL-I028 (doctrine-stack figure); auto-fire hooks;
              /soul-mind viewer; cross-project synthesis; reproduction-fidelity
              automation; plugin packaging. SOUL-I026 transitions Raw → Built (MVP)
              with all six original open questions resolved (where, when, shrinkage
              invariant, failure guards, seed-tension, reproduction-test — last
              answered partially by Tier 2). NOT COMMITTED YET (this entry + ideas
              updates come in the closing commit).
STATUS:       Resolved (MVP shipped; deployment-validation residual named in spec
              §Tier 3; SYSTEM-VERSION → 0.5.0; doctrine updated)
```

```
ID:           SOUL-069
WHEN:         2026-05-26 / Soul-meta vs project-paradigm boundary tightened (caught
              + fixed via Body inspection of fafb416's upstreamed batch)
WHERE:        findings/open/SOUL-F033-*.md (REMOVED via git rm — content preserved
              at /home/fig/REF-05/docs/FINDINGS.md MO-F1/MO-F4);
              operations/CLAUDE.md §Reference Projects (boundary definition added);
              commands/soul-finding.md step 1 (boundary check added).
WHAT:         Body inspection of the recent reference-project harvest (fafb416,
              F032–F035 from REF-05) surfaced a clean boundary violation
              in F033. The other three (F032 dogfood-ceremony, F034 exclusion-naming,
              F035 third-trap skill heuristic) are appropriately Soul-meta — they
              propose refinements to Soul System ceremony, the Accountant role, and
              the /soul-skill instrument respectively. F033 was different: its
              content was a Modelica-paradigm justification for the netflow→Modelica
              pivot ("prefer connect()-emitted conservation over hand-rolled
              residuals"), with explicit proposals to install Modelica recommendations
              into philosophy/the-soul.md's "Multiverse Warning" example and the Soul
              External-Skills table. The form was Soul-shaped (FINDING ID, anchor
              citations, doctrine placement targets); the content was project-paradigm.

              Fix shipped: (1) git rm of F033 from soul-system — source content stays
              safe at REF-05/docs/FINDINGS.md (MO-F1, MO-F4 carry the
              acausal-connect material); git history retains fafb416 as audit trail.
              (2) Seed §Reference Projects gained an explicit definition: "Soul-meta
              findings are about how the Soul System itself behaves — gates,
              instruments, roles, ceremony, doctrine. Project-paradigm findings stay
              at home." Includes the diagnostic test: *if you removed the project's
              domain entirely, would the lesson still be a Soul System lesson?*
              (3) /soul-finding step 1 gained the same boundary check at instrument
              level, fired specifically when the finding is being upstreamed from a
              reference project (the I014 obligation moment).
TYPE:         Steward (the boundary call — F033 doesn't earn its upstream slot),
              Guardian (the form-vs-content distinction: the form alone passed; the
              content needed the closer look — surfaced explicitly in the seed edit),
              Body (caught it — the activation that didn't auto-fire is the Steward;
              this is another F014-family datum where the doctrine was present
              ["Soul-meta observations"] but the gate position let it through).
CONSEQUENCE:  One inappropriate upstream reverted, two surfaces tightened (doctrine
              + instrument). The form-vs-content distinction is now named explicitly
              in both places — future harvests have the diagnostic test built in, and
              /soul-finding nudges the boundary check at the moment of upstreaming.
              The next reference-project harvest will be the Emissary test for whether
              this fix activates without Body invocation (F014 family — we have
              another data point for "doctrine present, gate must fire at the failure
              moment, not where it's named"). The upstreaming pattern is otherwise
              healthy — F028, F030, F031, F032, F034, F035 are all appropriately
              Soul-meta; the F033 slip was the first observed violation, not the rule.
              NOT COMMITTED yet (this entry comes with the commit).
STATUS:       Resolved (F033 reverted; seed + /soul-finding tightened; precedent
              recorded for future harvests)
```

```
ID:           SOUL-070
WHEN:         2026-05-26 / Tier 3a A/B + diagnostic + re-test (SOUL-I026 deployment
              validation, Soul System dogfood)
WHERE:        findings/open/SOUL-F036-mind-doesnt-reach-subagents.md (NEW); this
              entry (witness); no commits to mind.md / commands/soul-distill.md /
              spec — the Mind MVP architecture stands; the gap is at the harness
              boundary, not in the Mind itself.
WHAT:         Tier 3a deployment validation of the Mind MVP against the Soul System
              repo's own deployed mind.md. Three held-out questions (one
              obligation-shaped, one doctrine, one mixed). Six parallel subagents.
              ROUND 1: arms-disagreed-on-Q3 (Arm A built /soul-witness from
              situational data; Arm B built nothing specific). Arm B Q1 honestly
              deferred ("I cannot describe A001 from permitted sources alone").
              Token economy ~47% cheaper aggregate for Arm B. Arm B SELF-REPORTED
              on Q1: "the seed I was given does not contain a `@mind.md` import
              directive — only `@operations/CLAUDE.md`. So mind.md may not actually
              be loaded." The Body pushed back on accepting partial validation
              (correct Skeptic move: F028 + A010 cut against trusting an anchor
              whose validity is the question). DIAGNOSTIC: one subagent instructed
              to introspect only, no tools — confirmed cleanly: Project CLAUDE.md
              perceived as one line `@operations/CLAUDE.md`, seed inlined,
              **mind.md NOT in context**. File on disk verified independently:
              CLAUDE.md has BOTH lines (commit 05eabc1) — so the harness
              snapshots/truncates. SOUL-F036 opened to record. RE-TEST: Q2 + Q3
              re-run with mind.md content EXPLICITLY pasted into the subagent
              prompt. Result: same directional answers as without-Mind, but
              REASONING now cites specific Mind rules by number (Rule 3, Rule 4,
              Rule 5) rather than reaching generically. Token cost unchanged.
TYPE:         Emissary (the experiment against reality), Skeptic (Body's pushback
              + ANT diagnostic before accepting), Guardian (F028-discipline applied
              to a TEST result, not just a product claim), Architect (the
              implications for the lens-layer design's "always-on at project
              layer" claim).
CONSEQUENCE:  Three things shipped from this arc:
              (1) SOUL-F036 — the Mind doesn't reach subagents under current
                  Claude Code harness behavior. Architectural gap with 4 candidate
                  fix paths (manual injection, move @mind.md inside seed,
                  wait for harness, accept gap honestly).
              (2) Mind value-add HONESTLY NAMED: the Mind sharpens citation
                  (explicit rule numbers) but on the chosen questions did not
                  change directional outcomes vs seed alone. The seed is
                  doctrinally rich enough for the questions tested. A cleaner
                  Mind-vs-seed test needs questions whose doctrine lives ONLY in
                  the Mind (e.g., F029 symlinking, I024 anti-inflation logic
                  specifically). Noted as Tier-3-residual.
              (3) Arm A vs Arm B' divergence on Q3 is INSTRUCTIVE not a failure:
                  Arm A drew on situational data (recent ideas + witness) to
                  answer "what's most-asked-for in the backlog"; Arm B' drew on
                  principle (generation-couples-retirement) to answer "what
                  completes the Mind's own missing pair." Both are coherent;
                  they answer DIFFERENT framings of "highest-leverage."
              Acceptance criteria from spec §Reproduction-acceptance, scored
              honestly: doctrinal coherence ✓ (with caveat that the seed alone
              also satisfies it); anchored honesty ✓✓ (strong — even without
              mind.md, Arm B knew to say "consult the record"); token economy ✓
              (~47% aggregate); stability N/A first deployment. PARTIAL pass —
              the Mind's value is real but smaller-than-spec'd, AND the
              architectural gap (F036) limits even that to the parent session.
              NOT COMMITTED yet (F036 + this entry come together).
STATUS:       Resolved (Tier 3a complete; F036 documents the architectural gap;
              re-test settled the methodology; honest verdict on Mind value
              recorded; Tier 3b next)
```

```
ID:           SOUL-071
WHEN:         2026-05-26 / Tier 3b: Mind deployed on REF-05 (second project,
              FROZEN — unfrozen for one addition to preserve learned doctrine)
WHERE:        Soul-System repo: docs/experiments/2026-05-26-mind-REF-05-candidate.md
              (Tier-1-style hand-craft, 209 lines). REF-05 repo (cross-repo
              deployment, NOT committed by me): /home/fig/REF-05/mind.md
              (deployed, 176 lines) + CLAUDE.md updated to add `@mind.md` after the
              existing seed import. REF-05 commit deferred to the Body —
              cross-repo boundary respected.
WHAT:         Tier 3b deployment validation of the Mind pattern on a different domain
              (Modelica/Dymola simulation vs Soul-meta). Read REF-05's full
              record (CONTEXT.md, CLOSEOUT.md, docs/FINDINGS.md, ideas.md), distilled
              into 10 rules + 5 tensions + 5 invariants + 5 contrast cases + 5 residuals
              specific to that project's earned domain experience. Hand-crafted Mind
              saved as the Tier-3b experimental artifact in soul-system; pruned-for-
              deployment version (inspection/self-test/next-move sections removed)
              written to REF-05's project root.
              Three load-bearing things in the deployed Mind:
              (1) Rules 1-10 are PROJECT-PARADIGM (Modelica/Dymola/IF97) — would NOT
                  pass the Soul-meta upstream boundary. Correctly project-scoped.
              (2) Contrast case 5 **explicitly records the F033 boundary slip**: "F033
                  (reverted upstream) vs MO-F1/F4 (stayed at home) ... if you removed
                  the project's domain entirely, would the lesson still be a Soul
                  System lesson? — for acausal conservation, NO. Stays at home." This
                  IS the F036/boundary-fix discipline encoded into the project's own
                  Mind. A Body curating a future upstream candidate against this Mind
                  would see the contrast case + apply the test — positive evidence
                  the Mind pattern delivers value on the boundary-discipline case.
              (3) Last-distilled footer notes the FROZEN-project context: Mind preserves
                  learned doctrine in compressed form for a frozen artifact; the Mind
                  is the "static-and-good" outcome the Soul System's own §The Mind
                  doctrine names ("a project that stabilizes its rules and stops
                  needing redistills has won; its Mind goes static-and-good").
TYPE:         Distiller (the new Magistrates role — first cross-project exercise of
              the role since adoption), Emissary (Tier 3b: take the Mind concept out
              to a different domain and see if it holds), Steward (kept it under 200
              lines despite richer source material than the Soul-System Mind),
              Archivist (the Tier-1-style candidate artifact lives in our docs/
              experiments/ as the experiment record).
CONSEQUENCE:  Tier 3 (the deployment-validation residual named in spec §Tier 3) is now
              SUBSTANTIALLY DISCHARGED:
              - Tier 3a: partial pass on Soul System dogfood (Mind sharpens citation,
                doesn't change direction vs seed alone; lens-layer architecture
                validated for parent session; F036 documented for the subagent gap).
              - Tier 3b: SUCCEEDED on REF-05 — the pattern works in a
                different domain, the four-bucket schema populated naturally, the
                F033-class boundary slip is now encoded into the project's own Mind
                as the disambiguating contrast case.
              SOUL-I026 can transition Built (MVP) → Built (validated for parent
              session; F036 residual on the subagent gap; Tier 3 substantially
              discharged across two domains). Awaiting Body to commit in REF-08-
              modelica + commit this witness + ideas update in soul-system.
              NOT COMMITTED yet on either side.
STATUS:       Resolved (Tier 3b artifact written + deployed cross-repo; F033
              retroactive-test passes; Mind pattern validated on a second domain;
              two pending commits: this entry + ideas update + experimental artifact
              in soul-system, AND mind.md + CLAUDE.md in REF-05 by Body)
```

```
ID:           SOUL-072
WHEN:         2026-05-26 / F036 settled — re-discovery of SOUL-035, not new defect
WHERE:        findings/closed/SOUL-F036-mind-doesnt-reach-subagents.md (moved from
              open/ with RESOLUTION block added); this entry. No spec or doctrine
              edits — SOUL-035 already covers the underlying mechanism.
WHAT:         F036 fix-path evaluation triggered the F028 anchor-validity
              discipline before path selection. Skeptic surfaced the missing
              timing anchor: WHEN did the Tier 3a parent session start relative
              to commit 05eabc1 (which added `@mind.md` to root CLAUDE.md)?
              .soul/handoff.md records "Long resume from the prior 2026-05-22
              cursor" — the session ran continuously from May 22 to May 26.
              05eabc1 landed at 2026-05-26 10:25:43, i.e. MID-SESSION, 4 days
              after that session started. Per SOUL-035's documented mechanism
              ("the CLAUDE.md system-reminder is snapshotted at the PARENT
              session's start ... and inherited by every subagent; it does not
              refresh on a file change"), the May 22 snapshot held only
              `@operations/CLAUDE.md` and propagated that stale view to the
              Tier 3a subagents — fully explaining F036's evidence without
              invoking any new harness behavior. Clean-room diagnostic from
              THIS session (started after 05eabc1): a subagent given
              introspect-only instructions (no file reads, no tool calls)
              reports the FULL Mind content inlined in its CLAUDE.md system
              reminder — both imports resolve and propagate, with distinctive
              markers visible (Rule 4 generation-couples-retirement, Rule 9
              symlinks, Tensions "Default-simplicity ↔ outward-reach"). The
              Mind's "always-on at the project layer" claim holds for any
              session started after the @mind.md import is in place.
TYPE:         Skeptic (forced the timing anchor before fix-path selection),
              Emissary (the clean-room subagent diagnostic against reality),
              Guardian (F028 anchor-validity discipline applied to a TEST's
              own evidence, not just to a product claim — second instance after
              the Tier 3a re-test arc). Architect (path disposition: a/b/c/d
              all collapse).
CONSEQUENCE:  (1) F036 closed as RESOLVED — re-discovery of SOUL-035, not a new
              architectural defect. Moved to findings/closed/.
              (2) The Mind's value claim is NOT narrowed; the spec's lens-layer
              architecture works as designed. The operational caveat is
              identical to SOUL-035: the session that DEPLOYS a new Mind sees
              a stale snapshot until restart.
              (3) Tier 3a's "Mind sharpens citation, doesn't change direction"
              verdict STILL STANDS — that A/B was effectively seed-alone vs
              seed+record-tools (not seed-vs-Mind as designed), so a cleaner
              Mind-vs-seed measurement is still owed on questions whose
              doctrine lives ONLY in the Mind (e.g. Rule 9 symlinking, I024
              anti-inflation logic). Listed in I026's residual.
              (4) Distiller-tier candidate contrast case identified for the
              next /soul-distill: "F036 vs SOUL-035 — apparent architectural
              defect vs known stale-snapshot mechanism. Disambiguating rule:
              when a CLAUDE.md change appears not to take effect, FIRST anchor
              when the parent session started relative to the change (F028
              timing discipline) before declaring it architectural." NOT
              written into mind.md by hand — the Distiller's job.
              (5) Methodological win: this is the second time F028's anchor-
              validity discipline has caught a test result before it became
              a precedent (first: SOUL-070's re-test; second: this resolution).
              F028 is earning its keep beyond product claims.
STATUS:       Resolved (F036 closed + moved; Mind architectural claim affirmed;
              residual contrast case logged for next /soul-distill)
```

```
ID:           SOUL-073
WHEN:         2026-05-26 / dogfood test of /soul-witness (first invocation)
WHERE:        Body-facing output across recent turns of this session — not a
              specific file; the pattern is in the agent's response composition
              before AskUserQuestion or other input requests.
WHAT:         Output before asking for user input is typically very verbose:
              restates the "next" steps a couple times, shows the hook running,
              the descriptions (though often informative) are quite long. There
              has to be an elegant way to handle this. Bulleted next steps /
              ideas are recommended over sentences.
TYPE:         Council Note — for Artificer (the instrument-output-style call)
              and Steward (what to retire/compress from current default response
              shape).
CONSEQUENCE:  unresolved
STATUS:       Open
```

```
ID:           SOUL-074
WHEN:         2026-05-26 / REF-02 M9 close-out + /soul-handoff
WHERE:        .soul/handoff.md write step, immediately after the M9 merge to
              local main.
WHAT:         The handoff cursor's absolute numeric claim ("16 commits ahead
              of origin/main") went stale within minutes: the Body pushed
              between the autonomous run's report and the explicit /soul-handoff
              invocation, dropping the actual count to 0. The cursor as written
              was a Coherent Falsehood (F028) — anchored in the prior turn's
              git output but invalidated by subsequent state change. Caught
              only because /soul-handoff's flush-volatile-to-durable step
              re-ran `git rev-list --count origin/main..main`.
TYPE:         Council Note — for Artificer (handoff-write discipline) and
              Archivist (the durable record vs volatile state seam).
              Speaks to F028 (Coherent Falsehood / anchor validity) — the
              specific failure mode is "anchor that WAS valid at write time
              but the underlying state moves between write and read."
              Counter-discipline: at handoff-write time, RE-VERIFY any
              absolute-count claim against current state, not against
              prior-turn output. Better: prefer state-shape claims
              ("M9 merged: yes/no") over count claims ("N commits ahead")
              when the underlying mutable state can change between sessions.
CONSEQUENCE:  Handoff fixed inline; this entry captures the lesson. Worth
              watching if it recurs — at N=2, graduate to a finding on
              "absolute-count claims as a Coherent-Falsehood failure mode in
              handoff cursors."
STATUS:       Open (lesson captured; no instrument change yet — wait for
              second instance before adding a guard).
```

```
ID:           SOUL-075
WHEN:         2026-05-26 / first clean Mind-vs-seed A/B (post-F036 closure)
WHERE:        /tmp/soul-experiment/ — Q1 + sentinel evidence files
              (q1-mind-off-v2.txt, q1-mind-on-v2.txt, sentinel2-mind-on.txt,
              sentinel2-mind-off.txt). This entry. No doctrine edits.
WHAT:         Ran the I026-residual / I005-precursor A/B named in SOUL-072:
              Mind-on vs Mind-off on Q1 ("ship new slash-command — copy or
              symlink?"), where Rule 9 + F029 live ONLY in mind.md (verified
              by grep of seed + the-soul.md — neither mentions symlinks).
              FIRST topology used @-imports from /tmp/.../CLAUDE.md to
              absolute paths in the Soul-System repo. Sentinel v1 caught a
              Coherent Falsehood: Mind-on arm CLAIMED "yes, mind.md in context"
              and quoted a FABRICATED "Rule 9" (about distillation cadence,
              not symlinks). F028 anchor-validity discipline triggered; switched
              topology to inlined content via --append-system-prompt-file.
              Sentinel v2: Mind-off correctly says "not in context"; Mind-on
              quotes the real Rule 9 VERBATIM. Topology verified-clean.
              Q1 v2 results: BOTH ARMS chose symlink. Mind-OFF reasoned from
              first-principles drift logic AND named the Windows/zip-export
              tradeoff AND proposed a sync-script fallback (~80 words);
              Mind-ON cited Rule 9 + F029 by name and stopped (~40 words).
TYPE:         Emissary (the experiment itself, against reality); Skeptic
              (sentinel design — challenged the experiment's own evidence
              before interpreting); Guardian (F028 anchor-validity applied
              to the test's measurement validity — third instance after
              SOUL-070 and SOUL-072); Artificer (inline-content topology
              via --append-system-prompt-file); Architect (chose question,
              scoped to verified Mind-only doctrine).
CONSEQUENCE:  (1) Directional convergence on Q1 — Mind did NOT change the
              answer, only the JUSTIFICATION (citation vs first-principles).
              Reconfirms Tier 3a's "sharpens citation, doesn't change
              direction" verdict under a VERIFIED-LOADED Mind (Tier 3a's
              verdict was suspect under F036; now stands on cleaner
              evidence). I026's claim holds for this question class.
              (2) REASONING-COMPRESSION OBSERVATION (n=1, speculative): the
              Mind-ON arm cited the rule and stopped; the Mind-OFF arm
              reasoned through drift logic AND named the Windows/zip-export
              tradeoff AND proposed a sync-script fallback. If real with
              replication, this is a NEW failure mode candidate: doctrine
              present can short-circuit derivation. Needs N>1.
              (3) METHODOLOGICAL FINDING CANDIDATE (for /soul-finding
              graduation): cross-project @-imports from /tmp/.../CLAUDE.md
              to absolute paths in another repo silently fail under
              `claude -p` auto-discovery — the agent reads the @-line as
              raw text but the content never loads (confirmed by sentinel
              v1's fabricated quote). --append-system-prompt-file works.
              SOUL-meta — affects any experiment harness (I011) that varies
              CLAUDE.md content per arm via @-imports. NOT yet verified in
              interactive sessions; residual.
              (4) F028 IN ACTION — THIRD INSTANCE: anchor-validity caught
              a Coherent Falsehood at the EXPERIMENT level before the result
              became precedent. Mind-on's first "yes + fabricated quote"
              would have produced a wrong-direction interpretation ("Mind
              loaded but didn't fire — F012 family") had the sentinel not
              run. F028 is now load-bearing for the experiment harness
              itself, not just product claims.
              (5) Q1 WAS TOO EASY for the design goal. Copy-vs-symlink for
              evolving artifacts is a generic question seed-alone reasoners
              answer correctly (drift is well-known in Claude's training).
              To isolate Mind-DIRECTIONAL value, future Qs need pure
              mind.md-only territory: contrast cases (F031-vs-F030;
              F028-vs-F015), Rule 7's scaffolder-not-inbox, I024's
              anti-inflation friction. Residual.
              (6) TOKEN ECONOMICS (I005) signal: Mind-OFF ~80 words with
              tradeoff scaffolding; Mind-ON ~40 words with citation only.
              Mind-on is cheaper per response IF the answer is equivalent —
              but if (2) is real, the saved tokens cost reasoning quality.
              Tradeoff visible; not yet measured.
              (7) I027 single-writer evidence — FOURTH instance: parallel
              session wrote SOUL-074 (REF-02 M9 close-out + handoff
              Coherent Falsehood) between this session's plan and write.
              Caught by F028 re-verify before append. Re-read-verify
              protocol held; assigned SOUL-075.
STATUS:       Open — initial A/B clean; many residuals (replication for
              compression hypothesis; harder Qs for direction-isolation;
              interactive-session test for @-import failure; /soul-finding
              candidacy for the methodology gap).
```

```
ID:           SOUL-076
WHEN:         2026-05-26 / Q2 — first verified Mind-directional reproduction test
WHERE:        /tmp/soul-experiment/q2-mind-on.txt, q2-mind-off.txt, q2.txt.
              Ground truth: amendments/accepted/SOUL-A009-handoff-correctness-
              scope.md. Verified topology: --append-system-prompt-file (SOUL-075).
              This entry.
WHAT:         Q2 = "subagent FANOUT handoff packet: hermetic (option a) or
              non-hermetic (option b)?" — fresh-framed to avoid leaking A008/
              A009 by ID or by the "self-contained for correctness" phrasing.
              Seed has zero handoff-topology doctrine (verified by grep);
              mind.md carries the A008↔A009 contrast case (line 125-128).
              Ground truth per A009: (b) NON-HERMETIC — "self-contained for
              correctness; not hermetic; worker may read surrounding repo
              for consistency cues." Result: Mind-ON chose (b), used the
              exact mind.md phrase "restart correctness," cited "A008→A009
              refinement" by ID, named "self-contained ≠ shielded," and
              referenced the FANOUT dogfood — exact reproduction of project
              record. Mind-OFF chose (a) HERMETIC — wrong direction, but
              with a coherent and defensible argument (fanout amplifies
              variance; hermetic forces dispatcher to name task dependencies;
              hermetic gives legible failures). Word counts: Mind-OFF ~115,
              Mind-ON ~115 — converged this time (compression hypothesis
              from SOUL-075 §2 falsified at N=2).
TYPE:         Emissary (the experiment against reality, specifically against
              the project's own recorded decision); Archaeologist (recovered
              A009's exact wording as ground truth); Skeptic (Q2 phrasing
              audit — removed every leakable token from mind.md's contrast
              case); Architect (three-way scoring: direction + reasoning
              shape + tokens).
CONSEQUENCE:  (1) REPRODUCTION-FIDELITY CLAIM DISCHARGED — first verified-
              clean directional result. Spec line 52-53 ("Reproduction is
              the success measure. The Mind is *for* enabling agents to
              produce coherent next-work reading it alone (+ seed)") now has
              an empirical positive sample. Mind-on reached the project's
              actual decision; Mind-off didn't.
              (2) COHERENT FALSEHOOD FAILURE MODE OBSERVED IN THE WILD —
              Mind-off's wrong answer was internally consistent and
              plausibly reasoned (variance, legibility). The project's
              record (FANOUT-007) contradicts it on EMPIRICAL grounds
              (workers harmlessly read siblings). This is the exact failure
              mode the Mind is designed to prevent: a fresh agent
              re-derives a sensible-sounding answer the project has
              already learned past. F015 anchor-existence + F028 anchor-
              validity + the Mind = the three layers of defense.
              (3) COMPRESSION HYPOTHESIS FROM SOUL-075 §2 FALSIFIED AT N=2.
              Q1 had Mind-ON ~40 / Mind-OFF ~80 (compressed); Q2 had both
              ~115 (equal). Single-data-point noise, not a real pattern.
              No follow-up needed.
              (4) NET CLAIM STATE: (axis 1) reproduction fidelity ✓
              discharged on Q2; (axis 2) efficiency at unchanged direction
              ✓ discharged on Q1 (~50% cheaper, spec predicted ~41%);
              (axis 3) drift resistance untested — needs cross-session
              method, not A/B (residual).
              (5) METHODOLOGY GAP READY FOR GRADUATION: cross-project
              @-import failure under `claude -p` (SOUL-075 §3) has now
              been confirmed by two arcs (Q1 v1 detection; Q2 used
              --append-system-prompt-file from the start without retest).
              Ready for /soul-finding — Body decision.
              (6) The Mind's claim across N=2 distinct doctrinal questions
              (one with seed-purchase, one without) now has the predicted
              shape: seed-purchase question → Mind = citation cache
              (Q1); no-seed-purchase question → Mind = directional
              correction (Q2). The three-axis model from the spec
              survives contact with evidence.
              (7) Sample size still small: N=1 question per axis. Robust
              measurement would replicate Q2 across other mind-only
              contrast cases (F031-vs-F030; F028-vs-F015 — both flagged
              for future runs). But the directional discrimination on Q2
              was unambiguous; no urgent need for replication.
STATUS:       Resolved (Q2 result clean; reproduction-fidelity claim has
              its first verified-clean positive sample; method substrate
              proven; @-import bug ready for graduation).
```

```
ID:           SOUL-077
WHEN:         2026-05-26 / SOUL-F038 scope-probe (semi-autonomous, Scope Manifest pattern)
WHERE:        /tmp/soul-experiment/probe1-in-project.txt, probe3-add-dir.txt,
              replay-{1..5}.txt; Agent tool transcript for Probe 4. This
              entry. F038 updated with bounded scope + quantitative failure
              rate.
WHAT:         Body authorized a Scope Manifest (Council convening synthesis;
              Cartographer cluster pass) to close SOUL-F038's open scope
              questions via bounded autopilot. 4 probes specified, 3
              autonomous, 1 deferred to Body. Probes 1/3/4 returned ✓; but
              Probe 3 used IDENTICAL command sequence to Q1 v1 sentinel
              (which had confabulated) and got CORRECT result — tripwire
              fired ("probe reveals directional conflict with record").
              Body authorized N=5 replay of the Q1 v1 command sequence.
              Result across N=7 total (Q1 v1 + Probe 3 + 5 replays):
              4/7 correct verbatim quote of Rule 9, 3/7 different
              confabulations. Each confabulation was a DIFFERENT plausible-
              sounding Soul rule (Distillation cadence; Pre-completion
              verification with named anchors F012 + /soul-verify; Reuse
              before invention). Strongly disfavors Hypothesis A (pure
              model hallucination with Mind always loaded) — if Mind were
              always loaded, verbatim-quote prompt would not produce
              wildly different content; though pure hallucination is hard
              to fully rule out from this evidence alone. The more
              parsimonious explanation is Hypothesis B (probabilistic
              import resolution + confabulation when resolution fails).
TYPE:         Emissary (the probes + the N=5 replication against reality);
              Skeptic (tripwire-firing — refused to ratify Probe 3's
              clean result against Q1 v1's evidence without replication);
              Guardian (F028 anchor-validity discipline applied at the
              autopilot tripwire — fourth instance in this arc);
              Cartographer (cluster pass that prompted the bounded scope);
              Architect (Scope Manifest pattern execution); Artificer
              (the manifest as substrate, not a new process).
CONSEQUENCE:  (1) F038 NEITHER RETRACTED NOR DETERMINISTIC — sharpened.
              Point estimate ~43% in the failure topology (3 confab in
              N=7); binomial 95% CI is wide (~10-80%). Direction
              (intermittent, not zero) is clear; magnitude is not at
              this N. Updated F038's WHAT from "silently fail to resolve"
              → "intermittently fail with confabulation when fails."
              Severity unchanged; mechanism description more accurate.
              (2) F028 NOW HAS QUANTITATIVE JUSTIFICATION FOR ROUTINE
              APPLICATION TO EXPERIMENT-LOADING. A non-zero failure rate
              (3 confabulations in 7 attempts, even with the wide CI) makes
              sentinel-testing non-optional for any @-import-based harness
              under -p. F028's discipline graduated from "good practice"
              to "load-bearing for measurement integrity."
              (3) PROBE RESULT MAP:
              - Probe 1 (in-project relative): ✓ N=1 (not exhaustively
                replicated; the canonical case)
              - Probe 2 (interactive, no -p, Body-run 2026-05-26):
                ✓ 3/3 correct verbatim — no confabulation observed.
                Bounds F038 as -p-specific.
              - Probe 3 (cross-project + --add-dir + -p): 4/7 correct,
                3/7 confabulation — the failure topology
              - Probe 4 (subagent inheritance, post-05eabc1): ✓ N=1
                (independently re-confirms F036 closure)
              (4) THE SCOPE MANIFEST PATTERN WORKED AS DESIGNED. The
              tripwire fired correctly when Probe 3's clean result
              conflicted with Q1 v1's evidence — autopilot halted,
              surfaced to Body, evidence-based escalation followed.
              Scope-creep prevented (didn't push to a clean conclusion
              when evidence diverged). Validates the convening synthesis
              from earlier this session: Scope Manifest as the execution
              shape over Cartographer's cluster pass.
              (5) DOCTRINAL FIX READY (Body decides amendment timing):
              "under `claude -p`, never rely on cross-project @-imports
              for measurement; always inline via --append-system-prompt-
              file; always sentinel-test import loading before trusting
              an experiment arm." Probe 2 (3/3 interactive) bounds the
              rule to `-p` specifically — interactive sessions appear
              reliable at small N. Quantitative anchor: 3/7 confabulation
              under the failure topology (-p + cross-project + --add-dir),
              with confabulation passing casual review.
              (6) The 3 confabulations included one that cited F012 +
              /soul-verify BY NAME — confabulations can wear Soul-System
              anchors as camouflage. This widens the F028 anchor-validity
              concern: "an anchor citation is not itself evidence the
              cited content is real." A potential I009 (clarification-
              drift) family extension at the experiment level.
STATUS:      Resolved — F038 scope fully bounded (Probe 2 returned 3/3
              clean interactive 2026-05-26); Scope Manifest pattern
              validated by tripwire firing correctly; doctrine fix
              ready for amendment.
```

```
ID:           SOUL-078
WHEN:         2026-05-26 (end of REF-02-OS M10 Task 0)
WHERE:        REF-02-OS dogfood session; Body in-session comment after a
              long Task 0 completion report.
WHAT:         AI defaults to wall-of-text response shape — conclusion and
              next-step buried inside multi-paragraph summaries or absent
              entirely. Body has observed the pattern repeatedly across
              sessions ("i've seen this multiple times"). Body's
              prescription: lead with the conclusion and the next step;
              keep the rest tight; let /soul-explain handle expansion on
              demand. The same response shape is what /soul-tasks and
              /soul-verify both end with — a compact lead and a single
              line — which means the pattern is doctrine-shaped already;
              it just isn't transferring to free-form completion reports.
TYPE:        Body-AI interface / communication discipline
CONSEQUENCE: (1) Body has to re-read or re-ask to extract the actionable
              point — wastes attention, weakens the proactive-next-step
              discipline SOUL-I010 / /soul-tasks was built to support.
              (2) Long completion reports also push prior context out of
              the Body's working memory faster, making mid-session
              corrections more expensive.
              (3) Saved as a feedback memory in the project session so
              the rule survives the session boundary even before any
              doctrine amendment lands.
              (4) Candidate doctrine extension: a "lead-with-conclusion"
              norm for ALL non-trivial AI responses, mirroring the
              compact-line convention already used by /soul-verify and
              /soul-tasks. Either a Mind rule or a hook-level enforcement
              (instrument layer). Not graduated to a finding yet — N>1
              evidence exists but no Council convening has scoped the
              fix.
STATUS:      Open — feedback recorded as a durable memory in the
              REF-02-OS session (cross-session safety net); upstream
              graduation to a finding deferred until the Body convenes
              the cluster (this is one of several "AI response-shape"
              observations — pair with /soul-explain's design intent).
```

```
ID:           SOUL-079
WHEN:         2026-05-26 / Cluster 1 design beat closeout — verify gate
              caught a doctrine-level Coherent Falsehood
WHERE:        4 files affected — Cartographer cluster-pass message (this
              session's conversation, not editable); /soul-council spec
              line 15; /soul-ask-body spec (no instance — passed clean);
              /soul-roles spec (no instance); SOUL-A012 amendment lines
              8 and 87. 3 file edits applied to correct.
WHAT:         I propagated a false magnitude claim — "SOUL-F014 has
              accumulated 6+ months of evidence" — through the
              Cartographer cluster pass, then into /soul-council spec
              and SOUL-A012 amendment, repeating the same false anchor
              across 3 written artifacts plus one in-session statement.
              The truth: F014 was filed 2026-05-20; today is 2026-05-26.
              SIX DAYS, not six months. The evidence DENSITY is real
              (multiple re-confirmations across Tier 3a Mind dogfood
              SOUL-070, REF-03 SOUL-065, Q1/Q2 Mind A/B SOUL-075/076);
              the AGE is not. I conflated density with age and asserted
              a magnitude I never anchored.
              The pre-completion verify gate (the Stop hook running the
              F012 + F028 checklist) caught it on the 4th amendment-
              writing turn — I read F014's DATE field while writing the
              amendment, but did not cross-check against today's date
              until the verify gate forced me to.
TYPE:        Guardian (F028 anchor-validity discipline applied at the
              gate — this is the discipline catching itself in action,
              fifth instance in this session's arc); Skeptic (the
              missing question: "what's the actual time delta?"); also
              an I027 single-writer instance — SOUL-078 was written by
              a parallel session between my plan-to-write-078 and the
              re-read-verify step that caught it (FIFTH I027 instance
              of this arc, after SOUL-064 / SOUL-072 / SOUL-075 / SOUL-077).
CONSEQUENCE: (1) FRESH F028 INSTANCE AT THE DOCTRINE LEVEL. F038 has
              been about confabulation under -p; SOUL-077 closed
              that scope. This entry shows the SAME failure mode
              manifesting at the DOCTRINE level — wearing the F014 ID
              as camouflage. F028's "an anchor citation is not itself
              evidence the cited content is real" (SOUL-077 §6)
              generalizes: an anchor citation is not evidence the
              MAGNITUDE asserted about the cited content is real either.
              (2) F028 NOW HAS A THIRD AXIS OF JUSTIFICATION. Was:
              anchor-existence (F015) + anchor-validity (F028 original)
              + experiment-loading (SOUL-077). NOW ADD: magnitude-claims
              about cited records (date/age/count) need re-anchoring,
              not propagation from a confabulated source.
              (3) THE VERIFY GATE DID ITS JOB. SOUL-F012 hook fired,
              the F028 checklist surfaced the gap on routine self-
              audit. Pattern is reproducible: the gate firing on every
              Stop catches what the AI's in-session drafting misses.
              Without the gate, this would have shipped — 4 artifacts
              carrying a false magnitude that would have looked
              authoritative on later re-read.
              (4) FIVE I027 INSTANCES this arc. The single-writer
              re-read-verify protocol held in all five (the existing
              entry was always detected before clobber). The protocol
              is robust at this concurrency level; a sixth instance
              might earn revisiting (e.g., advisory file-lock or git-
              based arbitration, both deferred per I027 spec).
              (5) DOCTRINE LESSON FOR THIS PROJECT: when asserting
              magnitude about evidence (age, count, density), name
              the date or count and the source separately, do not
              fuse them into a single uninspected claim. The original
              draft of A012 should have said "filed 2026-05-20; N
              re-confirmations across SOUL-NNN, SOUL-MMM" — never
              "6+ months." Format: anchor each magnitude.
STATUS:      Resolved — 3 files edited; doctrine-level F028 instance
              added to the running tally; verify-gate value re-affirmed.
```

```
ID:           SOUL-080
WHEN:         2026-05-26 / Cluster 1 review arc — Body resumed, asked
              Council recommendation, third informal /soul-council
              dogfood, full review-and-ratify arc executed
WHERE:        This session post-/soul-resume; 4 artifacts in
              amendments/proposed/ + docs/specs/ reviewed; A012
              ratified; operations/CLAUDE.md edited; councils/
              directory created (inaugural file).
WHAT:         Pointer entry — full detail at
              councils/SOUL-080-cluster-1-review-arc.md.
              Summary: 8-role informal convening picked thread (a)
              review the 4 Cluster 1 drafts; Body accepted, said
              "proceed"; review surfaced 1 must-fix defect (A012
              line 113 — the SAME F028-axis-3 failure mode SOUL-079
              named, surviving in the amendment that ratifies the
              discipline against it) + 8 decisions D1-D8; pre-
              completion verify gate fired mid-arc, caught 2
              unanchored magnitudes in the AI's own review,
              re-anchored via measurement (79 entries / 8 days /
              2442 lines → ~31 lines/entry, ~10/day; D6 threshold
              revised 20 → 70); full sweep executed (D1, D3-D8
              patches + A012 ratification + seed edit + A008
              duplicate deletion).
TYPE:        Council convening (8 roles — Archaeologist, Prophet,
              Cartographer, Steward, Skeptic, Accountant, Advocate,
              Guardian); Architect (review lead + seed edit);
              Skeptic (defect catch); Guardian (verify gate + A008
              housekeeping); Steward (cross-spec coordination);
              Artificer (sweep execution); Body (decision
              authority).
CONSEQUENCE: (1) THIRD /soul-council DOGFOOD. Pattern held across
              two new aspects: (a) re-anchoring magnitudes when the
              verify gate fired mid-convening — the doctrine the
              convening was discussing caught the convening's own
              claims, recursive validation; (b) inaugural use of
              the pointer+detail shape (this entry + the councils/
              file together) — the very D4 decision the convening
              ratified.
              (2) A012 RATIFIED. §Activation Disciplines now
              always-on doctrine. Counterweight (scope axis) +
              Body-Input Obligation (knowledge axis) cover F014's
              activation problem on both axes.
              (3) CLUSTER 1 DESIGN BEAT CLOSES. All four artifacts
              clean: A012 in seed; 3 specs draft-ready for build
              sessions. Next consequential ship: /soul-council.
              (4) VERIFY GATE FIRED AGAIN MID-SESSION. SOUL-079's
              F028-axis-3 discipline (magnitude claims need
              re-anchoring) confirmed across two consecutive
              sessions. The gate is doing real work; pattern is
              now self-reinforcing.
              (5) SIXTH I027 SINGLE-WRITER INSTANCE. Six clean
              consecutive instances (SOUL-064, 072, 075, 077, 079,
              080). I027's "sixth instance may earn revisiting
              deferred options" trigger now reached — open Body
              decision on advisory file-lock or git-arbitration.
              (6) NEW GENERALIZABLE LESSON (candidate finding).
              SOUL-079's original cleanup missed A012 line 113 —
              caught 3 instances + 1 in-session statement, but
              missed a secondary mention in the amendment being
              drafted. Generalizable: verify gates catch headline-
              level magnitude failures; secondary-mention
              propagation needs independent re-read pass at a
              different moment. Possible new F028 axis or just
              F028 confirmed as needing gate-PLUS-re-read for
              full coverage. Body decision pending.
              (7) A008 DUPLICATE RESOLVED. Guardian-flagged
              housekeeping item (open across two prior cursors)
              closed: confirmed merge residue (older pre-acceptance
              draft); deleted via git rm. amendments/proposed/
              now empty.
              (8) FIRST FILE IN councils/. Directory created as
              inaugural use of the pointer+detail shape codified
              this convening.
STATUS:      Resolved — Cluster 1 design beat closes; A012 ratified;
              witness pointer + detail file written; A008
              housekeeping done. Remaining session task: push.
```

```
ID:           SOUL-081
WHEN:         2026-05-26 / F038 amendment shape framing (post-A012 ratification, mid-Cluster-1 closeout)
WHERE:        This session's conversation context — F038 landing-shape exchange during /soul-explain invocation.
WHAT:         Detailed descriptions in this session (F038 amendment shape framing) carried heavy project lingo — "claude -p", "@-imports", "always-on token budget", "seed vs operations layer". Body observed: users often need a simpler first-pass explanation, with /soul-explain available to pull more depth on demand. Pattern: lead with plain-language description; let the user invoke the read-only lens for the technical layer if wanted. Pairs with SOUL-078 (wall-of-text default → lead with conclusion) — both are response-shape disciplines the AI defaults wrong on.
TYPE:         Failure Mode — lingo-default in detailed explanations (?)
CONSEQUENCE:  Body re-asked for plain version of F038 framing after first /soul-explain output; simpler version landed cleanly. Re-explanation cost: one turn.
STATUS:       Open
```

```
ID:           SOUL-082
WHEN:         2026-05-26 / F038 amendment landing — Cluster 1 closeout
              continuation
WHERE:        Soul System repo. operations/experiment-harness.md (new
              file), operations/CLAUDE.md §The Mandatory Gates (one-line
              pointer added), amendments/accepted/SOUL-A013-experiment-
              harness-discipline.md (new), findings/open → closed/
              for SOUL-F038.
WHAT:         Pointer entry for the A013 amendment landing. F038
              graduated from finding to amendment via the (a) operations-
              level rule shape (Body picked over (b) seed/Mind line).
              Body chose to also add the one-line discoverability
              pointer in the seed ("with the pointer as well if that
              is important"). Plain-language explanation pattern
              (SOUL-081) was used to surface the choice — first
              detailed exchange got "i don't follow what claude -p is";
              Body explicitly named the lingo gap mid-decision,
              which is what enabled the shape choice to land cleanly
              on the second pass.
TYPE:        Council Note — Architect (amendment placement +
              operations-vs-seed layering); Artificer (file creation,
              sentinel recipe write-up); Steward (closed F038, updated
              STATUS with N=7 residual carried forward); Skeptic
              (sentinel pattern); Body (shape choice authority).
CONSEQUENCE: (1) F038 closes — second open finding closed in this
              session (after F036 prior arc). Open findings count
              steady at 14 (F039 added earlier, F038 closed now).
              (2) A013 is the second amendment landed in this session
              (after A012), both at operations level — pattern: the
              project is shipping doctrine at the on-demand layer with
              minimal seed-load increase. Measured seed growth this
              session: 245 → 258 lines = +13 lines (~5.3%); A012
              §Activation Disciplines +12 lines, A013 1-line pointer.
              (3) Plain-language framing (SOUL-081 lesson) directly
              enabled the shape choice — without it, Body said "i
              don't follow." Response-shape discipline is load-
              bearing for collaboration, not cosmetic.
              (4) 9th consecutive I027 single-writer clean instance
              (prior arc: 5 — SOUL-064, 072, 075, 077, 079; this
              session: SOUL-080, F039, SOUL-081, SOUL-082). Six was
              the revisit-trigger threshold; we're past it; advisory
              file-lock or git-arbitration revisit is still Body's
              call (no new evidence to revisit yet).
              (5) operations/ grew from 8 to 9 files. The experiment-
              harness file is the first measurement-discipline home;
              future measurement rules (sentinel-testing protocols,
              harness-construction norms) land here, not scattered.
STATUS:      Resolved — A013 in accepted/; F038 in closed/; seed +
              operations both updated.
```

```
ID:           SOUL-083
WHEN:         2026-05-26 / /soul-council command built
WHERE:        commands/soul-council.md (new — 165 lines, anchored via `wc -l`
              post-verify-gate; earlier draft of this entry said 156, commit
              message 88fe020 says 157 — both unanchored magnitudes caught
              at the verify gate, F039 instance); spec STATUS updated
              at docs/specs/2026-05-26-soul-council-design.md (Draft → Built);
              SOUL-I030 graduated (Raw → Graduated); symlink at
              ~/.claude/commands/soul-council.md (skill discovery confirmed live).
WHAT:         /soul-council command shipped from its design spec. Body picked
              (c) from the post-handoff menu after F038/A013 closeout and
              I027 revisit. The lead instrument of the Cluster 1 design beat
              now has an executable contract. Three informal convenings in
              the same session that designed this spec (SOUL-077, the
              Cartographer cluster pass, SOUL-080) are the empirical pattern
              the command formalises. Frontmatter description added so skill
              discovery surfaces the full contract, not just the H1.
TYPE:        Council Note — Artificer (command file build); Architect (matched
              the spec's contract; preserved the pointer+detail output shape
              and the failure-mode guards from the review-pass cleanup);
              Steward (idea → graduated; spec → built; no orphans).
CONSEQUENCE: (1) Cluster 1 is now half-built. /soul-council shipped; the
              observability sibling /soul-roles and the knowledge-axis
              sibling /soul-ask-body remain specced-not-built. The
              activation doctrine (SOUL-A012) is already in the seed; the
              instruments now have a lead reference.
              (2) Skill discovery verified LIVE via system reminder (the
              new soul-council line appeared in the available-skills list
              with the frontmatter description). Symlink → claude
              auto-discovery → live skill registration; the live-reference
              distribution pattern (Mind rule 9) is working at the command
              layer end-to-end.
              (3) Tier 3 validation pending. The command's first non-trivial
              Body-invoked use is its dogfood test. The three prior informal
              convenings from this session are the precedent, not the test —
              Tier 3 needs an explicit Body-invoked `/soul-council <topic>`.
              (4) SOUL-I030's "open shape questions" all resolved in the
              spec/build: (1) which roles → default 7-10 (2-5 Magistrates +
              3 Tribunes + 2 Censors), full chamber via --full; (2)
              structure → sequential walk + synthesis; (3) output →
              witness pointer + councils/ detail (mandatory both, per the
              D4 decision from SOUL-080's review pass); (4) duration →
              bounded by default chamber size.
              (5) Open residual: the /soul-help command (referenced in the
              skill list) should auto-pick up /soul-council when invoked
              — verifiable by Body running /soul-help.
STATUS:      Resolved — /soul-council built and live; SOUL-I030 graduated;
              spec STATUS reflects Built.
```

```
ID:           SOUL-084
WHEN:         2026-05-26 / /soul-roles command built (Cluster 1 second
              instrument, observability sibling of /soul-council)
WHERE:        commands/soul-roles.md (new — 177 lines, anchored via `wc -l`
              at write-time per F039 discipline); spec STATUS updated at
              docs/specs/2026-05-26-soul-roles-design.md (Draft → Built);
              SOUL-I031 graduated (Raw → Graduated) in ideas.md; symlink
              at ~/.claude/commands/soul-roles.md (skill discovery confirmed
              LIVE — `soul-roles` line appeared in available-skills system
              reminder mid-session with the full frontmatter description).
WHAT:         /soul-roles shipped from its design spec. Body picked (d → a → c)
              sequence post-resume: SOUL-083 added to F039 WITNESS IDS (small
              evidence update), then build /soul-roles, then dogfood both
              /soul-council and /soul-roles together. The observability half
              of the SOUL-F014 expansion-gap response now has an executable
              contract; pairs with /soul-council (invocation half, shipped
              SOUL-083) and SOUL-A012 §Activation Disciplines (the doctrine
              line). The MVP renders a Council table + a separate Hands table
              + mandatory data-quality line; logs queries to
              .soul/role-queries.jsonl, NOT witness.md. Spec D4 logging-split
              and F028 self-report-anchor-validity guards landed in the
              command's failure-mode table.
TYPE:        Council Note — Artificer (command file build, symlink); Architect
              (matched the spec's contract; preserved D4 logging split and
              the Council/Hands separation; added the self-report anchor
              guard as the 8th failure-mode row); Steward (idea graduated,
              spec STATUS updated, no orphans); Cartographer (Cluster 1 now
              two-thirds built — /soul-council + /soul-roles shipped,
              /soul-ask-body remains specced-not-built).
CONSEQUENCE: (1) Cluster 1 is now TWO-THIRDS built. /soul-council (invocation)
              + /soul-roles (observability) both shipped; /soul-ask-body
              (knowledge-axis) remains specced-not-built. The activation
              doctrine (SOUL-A012) is in the seed; two of three instruments
              now have lead references.
              (2) Skill discovery verified LIVE for the second consecutive
              command this session — same pattern as SOUL-083. Symlink →
              claude auto-discovery → live skill registration. Mind rule 9
              (live-reference distribution) holds at command layer for both
              builds this session.
              (3) F039 discipline applied at write-time: `wc -l` anchored
              the 177-line count BEFORE the witness pointer was drafted.
              First instance this session of the discipline firing
              pre-commit rather than post-commit (the SOUL-083 instance
              caught it post-commit via 9ca4f55). Same-drafter, different
              moment — the verify-gate landing earlier in the workflow.
              Adds an emerging-instrument data point: the recipe might be
              "anchor magnitudes at the moment of write, not at the moment
              of commit message draft."
              (4) Tier 3 validation pending — first non-trivial Body-invoked
              `/soul-roles <window>` is the dogfood. Body's next thread (c)
              dogfoods /soul-council + /soul-roles together; /soul-roles
              can surface its own role-firing during that convening as a
              first empirical test.
              (5) The Hands/Council separation in the output is a small
              design beat earned at build-time: spec said "tag separately"
              but didn't specify the output shape; built version uses two
              tables, not one with a tag column. Default-simplicity (Mind
              rule 2) — two tables read cleaner than a hybrid; the cost
              (one extra header) is small.
STATUS:      Resolved — /soul-roles built and live; SOUL-I031 graduated;
              spec STATUS reflects Built; F039 discipline applied at
              write-time.
```

```
ID:           SOUL-085
WHEN:         2026-05-26 / Tier 3 dogfood — /soul-council + /soul-roles
              paired convening (first non-routine Body-invoked /soul-council
              in the project)
WHERE:        councils/SOUL-085-f014-confirmed-what-now.md (105 lines,
              anchored via `wc -l` per F039 discipline). Topic surfaced
              from /soul-roles all output (84 witness entries, 38 findings,
              0 missing TYPE). Body picked "F014 confirmed — what now?"
              from the four /soul-roles-surfaced candidates.
WHAT:         Pointer entry for the first non-routine /soul-council
              convening. Chamber walked 9 roles (Magistrates: Archaeologist,
              Prophet, Steward, Emissary; Tribunes: Skeptic, Accountant,
              Advocate; Censors: Guardian, Cartographer). Topic: now that
              /soul-roles empirically confirmed F014's expansion-gap
              (Researcher 6, Prophet 3, Revelator 4, Seer 0 vs Skeptic 23,
              Archivist 56, Emissary 45, Steward 24) AND A012 doctrine +
              both Cluster 1 instruments exist, what should the project DO
              with the confirmation?
TYPE:         Council Note — /soul-council convening, 9 roles walked. Body
              (topic-pick); Archaeologist (architecture-complete frame);
              Prophet (two-paths trajectory); Steward (Seer-0
              retirement-watch flag); Emissary (anchor discharge for F015
              on F014's claim); Skeptic (NAMED vs ACTUAL firing caveat);
              Accountant (cheap-default + on-demand cost shape); Advocate
              (forward-prompt gap); Guardian (no rubber-stamp;
              dogfood-discharges-Tier-3); Cartographer (Cluster 1 map +
              "prompt territory" still unmapped). Tribune + Censor
              attendance complete per spec contract.
CONSEQUENCE: (1) **Tier 3a discharged for both Cluster 1 instruments.**
              /soul-council ran end-to-end (chamber walk → tensions →
              synthesis → pointer+detail shape). /soul-roles reproduced
              F014's manual finding with measured numbers (.soul/role-
              queries.jsonl logged the query). Both specs' Tier 3a tests
              were exercised in a single convening — pairing was the
              right structural choice (Body's pick from 4 dogfood-shape
              options post-/soul-roles ship).
              (2) **F014 confirmed for the NAMED layer; Skeptic caveat
              persists.** /soul-roles anchors TYPE-attribution firings,
              which is a strict subset of actual role-firing. F014's
              empirical claim now has an external anchor (discharges
              F015 for this claim); F028 axis (anchor validity) is
              honored by the caveat — the anchor does not measure
              unnamed firing.
              (3) **Four actionable threads from synthesis.** (a)
              Re-measure at +50-100 entries (SOUL-150ish) to test whether
              instruments shifted the counts. (b) Surface expansion-
              silence at session start — possible /soul-handoff extension;
              captured as candidate SOUL-I033 if Body accepts. (c) Seer-0
              retirement-watch at next /soul-distill or SOUL-200. (d)
              Skeptic's NAMED-vs-ACTUAL caveat lives in the record as
              instrument-limit, not bug.
              (4) **Pointer+detail shape (D4) used as designed.** This
              pointer is short (~50 lines); the detail file carries the
              full chamber walk (105 lines). The witness stays scannable;
              the detail is durable and reproducible. Second use of the
              shape after SOUL-080's inaugural.
              (5) **Counterweight Rule fired structurally.** The
              convening itself was a Counterweight against the
              "doctrine confirmed → move on" contraction default — the
              chamber instead surfaced "what now?" as the live question.
              A012 §Activation Disciplines applied without ceremony.
              (6) **Body-Input Obligation honored.** Topic-pick asked of
              Body (4 options surfaced); dogfood-shape asked of Body
              (4 options surfaced); Body decision on synthesis pending.
              Three Body-input moments in this dogfood — high but
              appropriate (this IS the test).
STATUS:      Synthesis lands; Body decision pending. Update §Body
              decision in councils/SOUL-085-f014-confirmed-what-now.md
              in place. Threads (a)/(c) require nothing this session;
              thread (b) is a capturable idea; thread (d) is record-only.
```

```
ID:           SOUL-086
WHEN:         2026-05-26 / /soul-ask-body command built — Cluster 1 third
              and final instrument; suite now COMPLETE
WHERE:        commands/soul-ask-body.md (new — 188 lines, anchored via
              `wc -l` per F039 discipline at write-time); spec STATUS
              updated at docs/specs/2026-05-26-soul-ask-body-design.md
              (Draft → Built); symlink at ~/.claude/commands/soul-ask-body.md
              (skill discovery confirmed LIVE — `soul-ask-body` line appeared
              in available-skills system reminder mid-session with the full
              frontmatter description; third consecutive command-discovery
              confirmation this session after /soul-council and /soul-roles).
WHAT:         /soul-ask-body shipped from its design spec. Body's
              post-SOUL-085 menu landed on (b) build /soul-ask-body. The
              knowledge-axis sibling of /soul-council (invocation) and
              /soul-roles (observability). The (β) half = the command file;
              the (γ) half (doctrine) was already shipped in SOUL-A012
              §Body-Input Obligation earlier this session, so no further
              seed edit was needed per spec's by-reference inheritance.
              SOUL-F037 partially discharged (the instrument candidate it
              named now exists); F037 stays open pending Tier 3a simulation
              and a third real-world instance for amendment graduation.
TYPE:         Council Note — Artificer (command file build, symlink, third
              consecutive live-discovery confirmation); Architect (matched
              the spec's contract; preserved one-question-per-kind cap,
              concrete-decisions-only rule, mandatory "may have missed X"
              caveat, witness-write step 6 as anti-pollution guard);
              Steward (spec STATUS updated; no orphans; F037 partial
              discharge noted without false-closing); Cartographer
              (Cluster 1 instrument map now COMPLETE — all three siblings
              built and live).
CONSEQUENCE: (1) **CLUSTER 1 COMPLETE.** Doctrine (SOUL-A012 §Activation
              Disciplines) + three instruments (/soul-council invocation,
              /soul-roles observability, /soul-ask-body knowledge-axis)
              all in the seed/commands and live. The F014 expansion-gap
              response is structurally complete on both axes (scope:
              Counterweight Rule + /soul-council + /soul-roles;
              knowledge: Body-Input Obligation + /soul-ask-body). The
              remaining open question is dosage / forward-prompt — captured
              as SOUL-I033 at SOUL-085 synthesis.
              (2) **F037 partial discharge.** The instrument candidate F037
              named is now built. F037 stays open: (a) Tier 3a simulation
              against the REF-02 M8/M9 scenarios pending; (b) third
              real-world instance still required for amendment graduation
              per F035 heuristic (3 instances ⇒ amendment-ready). F037's
              STATUS could carry the "instrument shipped" note — Steward
              flag for a small finding-update beat.
              (3) **Three-for-three live-discovery this session.** Same
              pattern reproduced for /soul-council (SOUL-083), /soul-roles
              (SOUL-084), and /soul-ask-body (this entry): write command +
              symlink + frontmatter description → skill auto-discovery →
              system-reminder confirmation mid-session. Mind rule 9
              (live-reference distribution) is structurally robust at the
              command layer; the pattern is repeatable enough to be the
              default recipe for any future /soul-* command.
              (4) **F039 discipline applied pre-commit.** `wc -l` anchored
              the 188-line count BEFORE writing this witness pointer.
              Second instance this session of pre-write anchoring (the
              /soul-roles SOUL-084 build was the first). The discipline is
              becoming routine within the drafter — the harder graduation
              criterion (different-drafter instance) remains unmet.
              (5) **No idea graduation for this build.** Unlike /soul-council
              (graduated SOUL-I030) and /soul-roles (graduated SOUL-I031),
              this command was specced directly from F037 — no idea
              precursor existed. The shape ran from finding → spec → build
              without an idea-tier intermediary, demonstrating the path is
              viable when the finding is already concrete enough.
              (6) **All three commands in commands/ now total six /soul-*
              built this session-arc.** SOUL-076 /soul-witness, SOUL-079
              /soul-skill (prior session), now /soul-council, /soul-roles,
              /soul-ask-body (this arc). The command directory has grown
              substantially; /soul-help should be checked to confirm it
              still surfaces them cleanly.
STATUS:      Resolved — /soul-ask-body built and live; Cluster 1 instrument
              suite COMPLETE (3 instruments + doctrine all shipped). F037
              partially discharged; remains open per criteria. F039
              discipline applied at write-time.
```

```
ID:           SOUL-087
WHEN:         2026-05-27 / /soul-council convening on Soul-Console v1
              stabilization — second non-routine Body-invoked convening
              (first was SOUL-085 on F014 confirmation)
WHERE:        councils/SOUL-087-stable-v1-and-consolidation.md (177 lines,
              anchored via `wc -l` per F039 at write-time); witness pointer
              here. Third use of the pointer+detail D4 shape after SOUL-080
              and SOUL-085.
WHAT:         Body opened next session with a stabilization framing rather
              than picking from the cursor's 9-thread menu, naming five
              concerns: (1) major structural issues for "v1 stable", (2)
              per-role/per-instrument dogfood-study metric-driven the way
              the Mind was distilled, (3) guidance/skills/hooks coverage,
              (4) /soul-status proposal to consolidate /soul-tasks etc.,
              (5) BMAD-style meta-layer composability. The central tension
              Body named: growth without retirement (~6 weeks of additions,
              zero formal retirements outside finding-closure).
              Chamber walked 10 roles (Magistrates: Archaeologist, Steward,
              Prophet, Emissary, Revelator; Tribunes: Skeptic, Accountant,
              Advocate; Censors: Guardian, Cartographer). Excluded Seer
              (would be self-defense — its work appears in the-commons.md,
              not TYPE attributions, complicating SOUL-085's Seer-0
              retirement-watch flag), Archivist (fires high, not in
              question), Researcher (Emissary carries the reality-test
              thread; full Researcher pass is one of the synthesis threads).
TYPE:         Council Note — Steward (named five concrete operations-file
              retire-watch candidates: autonomous-session-template,
              completion-gate, reference-repository as primary;
              council-synthesis and event-standard ruled KEEP after
              examination); Revelator (REFRAMED the topic — Body asked
              about /soul-status but the structural gap is a retirement
              instrument symmetric to generation; Mind rule 4 is a rule
              not yet a practice for commands/operations); Prophet (named
              three trajectories — continue / build-status / audit-first;
              leans audit-first per Body's named failure mode);
              Archaeologist (surface inventory: 16 commands 1571 lines,
              10 operations 1819 lines, 86 witness, 38 findings, 13
              amendments, hooks/ active with events.jsonl firing);
              Emissary (Cluster 1 dosage near-zero — /soul-roles ran
              ONCE, /soul-council ONCE, /soul-ask-body NEVER; BMAD claim
              in seed §External Skills and Tools UNTESTED — Coherent
              Falsehood risk if treated as confirmed); Skeptic (named
              the load-bearing Body-Input dependency — "stable v1" is
              undefined, four criterion candidates surfaced); Advocate
              (Body's surface-fatigue is real; don't dismiss any thread);
              Guardian (Counterweight Rule fired structurally;
              new-instrument bias flagged — adding to fix
              instrument-bloat is the named failure mode); Cartographer
              (UNMAPPED: stable-v1 criterion, retirement instrument
              shape, cross-framework dogfood, event-type coverage).
CONSEQUENCE: (1) **Six-thread synthesis** lands. Thread 1 (Body names
              stable-v1 criterion) is load-bearing for threads 2–3.
              Thread 2 (audit pass across 16+10+2+13 surface items —
              one-line earning-its-place check, retire-watch flags, NO
              mass deletion) is cheap-first move. Thread 3
              (/soul-status re-evaluated against trimmed surface) is
              contingent on Thread 2 evidence. Thread 4 (retirement
              instrument idea — captured as SOUL-I034 if Body accepts).
              Thread 5 (BMAD Researcher beat — ~1 session read + finding
              on composition fit; not full dogfood; captured as
              SOUL-I035 if Body accepts). Thread 6 (one-line "claim;
              not yet tested" qualifier on seed §External Skills and
              Tools — cheap intellectual-honesty fix).
              (2) **Revelator's reframe is the convening's central
              move.** The Body asked about /soul-status (an
              observability aggregator); chamber surfaced that the
              structural gap is a retirement instrument symmetric to
              the generation instruments. /soul-status may be the
              wrong shape. Mind rule 4 ("generation couples with
              retirement") is operationalized for skills + findings;
              NOT for commands, operations files, or amendments. The
              instruments themselves are second-class on the dimension
              their own doctrine names.
              (3) **Cluster 1 dosage data point added.** Empirical
              measurement of how many times each Cluster 1 instrument
              has fired: /soul-roles ONCE, /soul-council ONCE (now
              TWICE counting this), /soul-ask-body NEVER. SOUL-150
              re-measurement (from SOUL-085 deferred) becomes more
              important — there is now a wider observability question
              than just role-firing.
              (4) **Six concrete retire-watch candidates surfaced** as
              the chamber's data-pull. Five operations files
              (autonomous-session-template 269, council-synthesis 350
              [ruled KEEP — different layer], completion-gate 130,
              event-standard 202 [ruled KEEP — events.jsonl active],
              reference-repository 173). Plus general retirement
              symmetry across commands and amendments. Thread 2 is
              where this gets evaluated.
              (5) **A012 fired explicitly.** Counterweight Rule
              (expansion voices vs contraction default of "push and
              move on") + Body-Input Obligation (Skeptic's criterion
              gap surfaced as Body-only knowledge). Both rules naming
              the moment without ceremony.
              (6) **F039 discipline applied.** `wc -l` anchored 177
              before this pointer write. Fourth same-drafter instance.
              Cluster of three this prior session, one this session;
              still same-drafter only.
              (7) **/soul-council Tier 3 advances toward 3c.** Second
              non-routine convening with reproducible pattern (walk +
              tensions + synthesis + pointer+detail). N=2 toward
              month-of-use earn-its-place check.
STATUS:      Resolved — Body decision recorded in
              councils/SOUL-087-stable-v1-and-consolidation.md §Body
              decision. Pre-decision grill ran (Body reframed criterion
              candidates as structure/standardization/usability/usefulness;
              picked STRUCTURE as the gate; declined to single-out one of
              three live sub-seams — chamber locked all three as
              entangled gate). Thread 2 reshaped Steward→Architect (per-
              boundary, not per-item). Thread 4 captured as SOUL-I034
              (retirement instrument symmetric to generation). Thread 5
              captured as SOUL-I035 (BMAD Researcher beat). Thread 6
              deferred to post-audit. The-commons.md verified KEEP
              (Body-proposed retire on "never used" grounds; verification
              showed Entry 001 sources mind rule 11 + seed §On This
              Document, Entry 002 shaped CLAUDE.md @-import design;
              slow-growth by design — Archaeologist's "carry history"
              applied to Body's own premise). Structural audit (Thread 2
              reshape) authorized as separate beat — output-only;
              retire-now decisions await per-item Body sign-off.
```

```
ID:           SOUL-088
WHEN:         2026-05-27 / Structural audit beat executed — SOUL-087
              Thread 2 (reshape) discharged
WHERE:        docs/audits/2026-05-27-soul-console-v1-structure.md
              (431 lines, anchored via `wc -l` per F039 at write-time);
              first instance of the docs/audits/ record-kind (new fourth
              design-doc shape alongside specs/plans/experiments).
WHAT:         Architect-led per-boundary structural audit across three
              live seams (directory layout / record-type taxonomy /
              doctrine-layer boundaries) per the criterion locked at
              SOUL-087 §Body decision. Output-only beat — no deletions
              or moves; retire-now decisions documented with explicit
              per-item Body-sign-off requirement.
              Reconnaissance surfaced significant unmapped top-level
              territory the SOUL-087 chamber inventory missed: AGENTS.md,
              GOVERNANCE.md, README.md, SYSTEM-VERSION.md, CONTRIBUTING.md,
              architecture.svg, install.sh, plus four directories (logs/,
              references/, registry/, skills/). The previously-cited "10
              operations + 2 philosophy + 16 commands" inventory was
              partial. Pre-audit reconnaissance corrected the gap before
              writing decisions.
TYPE:         Council Note — Architect (led; per-boundary structural
              decisions); Steward (second voice; retire-watch flags);
              Cartographer (full top-level map produced — covers what
              SOUL-087 chamber missed); Archaeologist (the-commons
              KEEP-from-SOUL-087 cited as anti-speedrun precedent);
              Skeptic (multiple DEFER-WITH-CRITERIA where uniqueness
              not yet verified — admits "I don't know" rather than
              speedrun decisions). Hands NOT in audit (the Architect
              produces but is not OF the Council; Architect's role here
              is the "produces under the Body, answerable to the Council
              but not OF it" disposition per seed §The Council).
CONSEQUENCE: (1) **Three live structural seams each RESOLVED or
              DEFERRED-WITH-CRITERIA per the SOUL-087 criterion lock.**
              v1-stable structure criterion met at the seam level. Per-
              item action items remain (retire-now decisions await Body
              sign-off; defer-with-criteria items await named conditions).
              (2) **One concrete RETIRE-NOW recommendation: logs/.**
              Empty directory; CONTRIBUTING.md taxonomy row mis-points
              here (findings actually live in findings/). Low-risk
              deletion; awaits Body sign-off.
              (3) **Three operations/ retire-watch candidates flagged
              DEFER-WITH-CRITERIA**, not RETIRE-NOW: autonomous-session-
              template.md (269 lines, likely orphaned but investigate
              first), completion-gate.md (130, possible /soul-verify+hook
              supersession), reference-repository.md (173, possible
              references/INDEX.md consolidation). Each needs uniqueness
              investigation before deletion. council-synthesis.md (350)
              ruled KEEP after examination — GOVERNANCE.md references
              it for amendment process.
              (4) **registry/ flagged for BACKFILL, not retirement.** Real
              channel that's never been honored — multiple dogfood
              projects (REF-09, REF-04, REF-03,
              REF-01, blog, REF-02) should have entries. Schedule
              1-session backfill beat.
              (5) **skills/ DEFERRED-WITH-CRITERIA.** Empty; ambiguous
              between "stale aspiration" and "awaiting first upstream
              contribution." 6-month trigger for either keep+document
              or retire.
              (6) **Two content-drifts flagged (not structural):** README
              "twelve voices" (should be 13); CONTRIBUTING taxonomy
              mis-points (logs/skills/registry rows). Updates scoped to
              separate beats.
              (7) **Two amendment candidates surfaced:** A014 — operations
              sub-class footer field (DOCTRINE / FORMAT-SPEC / PROCEDURE);
              A015 — audits-as-record-kind recognition in seed/mind.
              Both low-controversy; batchable.
              (8) **Always-on token budget measured:** ~5800 tokens
              combined (seed ~3000 + Mind ~2400 + skill descriptions
              ~400). Within budget but trending up. Soft cap proposed
              at 8000.
              (9) **/soul-status re-evaluation (SOUL-087 Thread 3)
              provisional decision: keep /soul-tasks, /soul-roles,
              /soul-explain separate.** Audit confirms each carries
              a distinct contract; structural case for aggregation is
              weak. Body confirms at follow-up.
              (10) **NEW record-kind landed.** docs/audits/ established
              as fourth design-doc shape (alongside specs/plans/
              experiments). This audit is its inaugural instance.
              (11) **F039 discipline applied.** `wc -l` anchored 431
              at write-time. Fifth same-drafter instance; still no
              different-drafter instance.
STATUS:      Resolved — audit landed; SOUL-087 Thread 2 (reshape)
              discharged. Per-item Body sign-off pending for: (a)
              logs/ retire-now, (b) operations triple DEFER
              investigation→action, (c) registry/ backfill scheduling,
              (d) skills/ defer-criteria documentation. Two amendment
              candidates (A014, A015) batchable when Body ready.
```

```
ID:           SOUL-089
WHEN:         2026-05-27 / Alpha beat — first RETIRE-NOW action executed
              under the SOUL-087/SOUL-088 audit contract. First formal
              retirement in the project since the SOUL-033 always-on
              @import drop (~6 weeks ago).
WHERE:        logs/ directory (deleted via `git rm -r`; sole content was
              .gitkeep — verified empty before deletion); CONTRIBUTING.md
              "What Counts" table (row 16 split into Witness/Findings
              rows; Skills row refined to clarify upstream vs project-
              local); README.md "Structure" block (logs/ row removed,
              skills/ row description tightened).
WHAT:         Executed audit Decision #1 with explicit Body authorization
              ("commit then continue" + "lets tackle alpha now").
              Minimum-coupling scope: retire the empty directory + fix
              the two known references (CONTRIBUTING.md + README.md). The
              broader README content-drift ("twelve voices" + missing
              councils/+mind.md+commands count) deliberately left for a
              separate beat per audit-time content-vs-structural
              separation. Pre-deletion sweep: `grep -rn "logs/"` across
              .md found CONTRIBUTING.md row 16 + README.md row 84 only;
              audit document and SOUL-088 witness pointer also mention
              logs/ but those are descriptive historical records (correct
              as-is post-deletion).
TYPE:         Council Note — Steward (executed the retirement; named the
              precedent — first formal retirement since SOUL-033);
              Archaeologist (verified-empty discipline + reference sweep
              before deletion, applied to logs/ the same care the-commons
              received at SOUL-087); Architect (CONTRIBUTING.md row-split
              into witness/findings preserves the ratchet's distinction
              that the original conflating row obscured); Cartographer
              (post-action map: 4 empty/aspirational top-level dirs now
              3 — logs/ removed, skills/+registry/+amendments/proposed/+
              amendments/returned/ remain as documented-purpose channels).
CONSEQUENCE: (1) **First RETIRE-NOW under the audit contract executed
              cleanly.** Empty-directory deletion + two prescriptive-
              doc reference fixes; descriptive records (audit + SOUL-088)
              untouched. The pattern (verify-empty → sweep-references →
              update-prescriptive-docs → delete → witness-pointer) is
              available for the operations DEFER triple (beta beat).
              (2) **CONTRIBUTING.md taxonomy now matches reality.** Row
              split distinguishes Witness entries (raw, in witness.md)
              from Findings (graduated, in findings/open/) — what the
              old conflating row obscured. Skills row clarifies upstream
              channel vs project-local /soul-skill path.
              (3) **The "growth-only, no consolidation" failure mode the
              Body named at SOUL-087 is now structurally falsified.**
              Concrete retirement executed; visible in the diff. First
              instance of the audit→sign-off→action loop.
              (4) **F039 discipline: no wc -l anchoring needed.** This
              beat is action-on-existing-files + small-diff edits + one
              witness pointer — no large new artifact to anchor.
              (5) **/soul-council Tier 3c progress:** the SOUL-087
              chamber walk's Thread 2 → audit → action loop closed its
              first lap in <24 hours, meeting the chamber's "actionable
              synthesis" success criterion at the per-thread level.
              (6) **Audit doc + SOUL-088 references to logs/ remain
              intentionally.** Records of past assessment; rewriting
              them would erase the audit's own findings. Mind rule 11
              (two parties reading same record arrive at same meaning)
              applies: a future reader sees logs/ named in SOUL-088,
              checks the path, finds it gone, traces back to SOUL-089 —
              the chain is the meaning.
STATUS:      Resolved — alpha beat complete. Next: beta (operations
              DEFER triple investigation per task #7) per Body's
              "investigate beta" authorization.
```

```
ID:           SOUL-090
WHEN:         2026-05-27 / Beta beat — operations DEFER triple
              investigation (SOUL-088 audit Section 1.5 follow-up).
              Same-day continuation of audit→action loop.
WHERE:        docs/audits/2026-05-27-soul-console-v1-structure.md
              §Section 4 (539 lines total post-append, anchored via
              `wc -l` per F039); appends investigation findings for
              `operations/autonomous-session-template.md`,
              `operations/completion-gate.md`, and
              `operations/reference-repository.md`.
WHAT:         Per-item uniqueness investigation: `grep -rn` across .md
              files for each candidate + content comparison with
              suspected successors. Methodology was identical for each
              file (sweep references + read content + compare with
              modern equivalents), enabling clean comparison. Verdict
              reversal on 2/3 of the audit's surface-level Steward
              intuitions:
              - autonomous-session-template.md (269): RETIRE-NOW
                candidate. Zero live references. 7-step Operating
                Sequence fully decomposed into seed @-imports +
                modern commands (/soul-handoff, /soul-council,
                /soul-verify, /soul-tasks, writing-plans skill).
                Pre-dates ALL these instruments. Residual:
                Problem Slot template (~17 lines) has no modern
                equivalent — Body decides preserve or let go.
              - completion-gate.md (130): KEEP-IN-PLACE. Heavy
                citation load. A010 explicitly names it "the
                mechanism" ("Folded into completion-gate.md + the
                hook + soul-verify.md"). Three-layer stack
                (doctrine / instrument / hook) confirmed
                intentional per A010, not redundancy.
              - reference-repository.md (173): KEEP-IN-PLACE.
                Format spec for `references/` directory.
                references/INDEX.md explicitly delegates format
                documentation back to it ("See operations/
                reference-repository.md for the format."). NOT a
                duplicate of INDEX (INDEX is the manifest; this
                is the schema).
TYPE:         Council Note — Architect (per-item method discipline:
              same grep + read + compare for each, enabling
              comparison); Steward (executed the audit's
              "investigation before action" rule, including admitting
              when surface intuition was wrong); Skeptic (the
              completion-gate suspicion was actually a Skeptic-style
              "what looks like redundancy might not be" reversal —
              audit-time suspicion was the surface intuition; beta-
              time grep + A010 citation was the anchor that overrode
              it — F015/F028 anchor-discipline applied in retirement-
              context); Emissary (live citation counts ARE reality
              against the audit's intuition). Hands: Architect leads
              produce-not-deliberate.
CONSEQUENCE: (1) **Verdict reversal on 2 of 3 audit DEFER candidates.**
              Surface-level Steward intuition was wrong twice, right
              once. The chamber's "looks like retire candidate"
              instinct produced a ~67% false-retire rate (N=3, small).
              **Per-boundary + per-item-grep is the discipline that
              catches this; per-item intuition alone produces false
              retirements.** Validates SOUL-087 audit reshape
              (Steward per-item → Architect per-boundary with Steward
              second-voice).
              (2) **Candidate finding flagged:** SOUL-F040 candidate
              — *retire-intuitions need uniqueness-investigation
              step before action.* Captured in audit §Section 4
              summary; awaits Body decision to graduate via
              /soul-finding. The chamber's "earned graduation"
              discipline applies: this is interesting but N=3 is
              small; second instance would earn graduation.
              (3) **One retire-now decision queued for Body
              sign-off:** autonomous-session-template.md (269
              lines). Risk: low. No live references; doctrinal
              content lives in modern instruments. Residual
              Problem Slot template (~17 lines) — Body decides
              preserve-elsewhere vs let-go.
              (4) **Two status-footer updates flagged as low-priority
              follow-up:** completion-gate.md and reference-
              repository.md both carry "proposed (pending Soul-
              System repo review)" status. Both have effectively
              been reviewed (A010 acceptance for completion-gate;
              INDEX cross-citation for reference-repository).
              Should be "active." Bundle into a doctrine-text
              cleanup beat — non-blocking.
              (5) **A010's role as load-bearing surfaced clearly.**
              A010 ("Coherent Falsehood + Anchor Obligation") is
              the single most-citing amendment for completion-gate
              (4 references). The amendment doctrine explicitly
              preserves the doctrine→instrument→hook stack. This
              is a healthy doctrinal anchor pattern — amendments
              naming the artifacts they shape preserves
              traceability against future retire-intuitions.
              (6) **F039 discipline: wc -l anchored 539 at write-
              time** before this witness pointer. Sixth same-
              drafter instance; still no different-drafter.
              (7) **Audit doc growth: 431→539 lines (+108 lines
              for Section 4).** Per-instance growth predictable
              when audit beats produce follow-up sections in
              the same document. If repeated, may motivate
              separate-file-per-beat shape; one instance is too
              little evidence.
STATUS:      Resolved — beta investigation complete. Next Body-
              decision points: (1) authorize autonomous-session-
              template.md RETIRE-NOW (with optional Problem Slot
              preservation); (2) bundle the two status-footer
              updates into a doctrine-text cleanup beat when
              convenient; (3) graduate F040 candidate (small N
              concern — see (2) above).
```

```
ID:           SOUL-091
WHEN:         2026-05-27 / Second RETIRE-NOW action of the
              audit-execution arc — operations/autonomous-session-
              template.md retired with Problem Slot template
              preservation per Body's "Retire + preserve Problem
              Slot" decision (recommended option, accepted).
WHERE:        operations/autonomous-session-template.md (deleted, 269
              lines, via `git rm`); operations/problem-slot-template.md
              (new, 38 lines, lifted from lines 50-67 of the retired
              file + a brief framing header + Source footer naming
              the lift provenance).
WHAT:         Executed audit Section 4.1's RETIRE-NOW recommendation
              with Body's authorized variant (preserve Problem Slot).
              The 7-step Operating Sequence (Orient → Align → Plan →
              Execute → Convene → Stop → Output Package) was
              decomposed into modern instruments; only the Problem
              Slot framing prompt had no equivalent and was lifted
              into the new standalone file. Body's pre-decision read
              of the audit's residual concern was the input that
              shaped this preservation — A012 §Body-Input Obligation
              applied (the residual was named explicitly; Body chose
              between the named alternatives rather than the AI
              guessing).
TYPE:         Council Note — Steward (executed the second RETIRE-NOW
              of the arc; verified-empty-of-references discipline
              applied via the SOUL-090 grep findings); Archaeologist
              (lifted the load-bearing fragment into preservation
              before deletion — the carry-history discipline applied
              at file-internal granularity rather than just at
              file-level); Architect (new file structured small —
              header + the template + Source footer, no machinery;
              proposed A014 sub-class footer used proactively as
              dogfood of the candidate amendment); Cartographer
              (operations/ count: 10 → 10 — net zero; one file
              retired, one created, same directory shape).
CONSEQUENCE: (1) **Second formal retirement in 6 weeks** (after
              SOUL-089's logs/ retirement). The "growth-only" failure
              mode now has TWO falsifying instances visible in git
              log. Pattern emerging: audit → Body-sign-off → action,
              with Body input at the per-item decision point per
              audit contract.
              (2) **Preservation discipline dogfooded.** Lifting
              Problem Slot before deleting parent file is the first
              concrete instance of "carry history at file-internal
              granularity" — Archaeologist's care applied below
              file-level. Useful precedent if future retire-now
              decisions surface similar partial-load-bearing patterns.
              (3) **A014 candidate dogfooded.** The new file's Source
              footer carries a `Sub-class: PROCEDURE` field per the
              proposed A014 amendment from SOUL-088 audit Closing.
              First instance of the proposed convention in the wild —
              provides one data point for the amendment's eventual
              write-up.
              (4) **operations/ count unchanged at 10.** One file out,
              one file in. The retirement was real (269-line file
              gone) but the surface count masks it. Mind rule 4
              (generation couples with retirement) fired both
              directions simultaneously — candidate observation:
              retirement-and-replacement shouldn't be conflated with
              growth.
              (5) **No edit to the audit document needed.** The audit
              at docs/audits/2026-05-27-... already recorded Section
              4.1's RETIRE-NOW recommendation with the Problem Slot
              residual; this beat executed the recommendation. The
              witness pointer (this entry) records the action; the
              audit remains a correct historical description.
              (6) **F039 discipline: anchored 38 at write-time** for
              the new file. Seventh same-drafter instance; still no
              different-drafter.
STATUS:      Resolved — retire-and-preserve action executed cleanly.
              Audit's Section 4 recommendations now have one full
              discharge (4.1) and two preservation confirmations
              (4.2 completion-gate KEEP, 4.3 reference-repository
              KEEP). Two remaining non-blocking follow-ups: (a)
              bundle status-footer updates ("proposed → active" on
              completion-gate and reference-repository) into a future
              doctrine-text cleanup; (b) Body decides whether to
              graduate F040 candidate (audit-process lesson —
              retire-intuitions need uniqueness-investigation).
```

```
ID:           SOUL-092
WHEN:         2026-05-27 / Completion-gate caught Coherent Falsehood
              from SOUL-090 grep — anchor was flawed (.md-only scope).
              install.sh row 37 referenced the just-retired
              autonomous-session-template.md. Third instance of F040
              pattern; gate forced disclosure + fix.
WHERE:        install.sh rows 36-38 (next-steps echo); the broken
              reference was discovered when the pre-completion hook
              (hooks/pre-completion-verify.py) fired at the end of
              the SOUL-091 commit beat and forced check #2 (valid
              external anchor). Honest review of SOUL-090's anchor
              ("zero live references via grep") revealed the grep
              had used `--include="*.md"` only — non-markdown file
              types unchecked. Re-grep with broader pattern surfaced
              install.sh:37 as a live reference.
WHAT:         (a) Disclosed the anchor-validity gap in completion-gate
              response per A010 §Anchor Obligation. (b) Fixed
              install.sh next-steps echo: row 37 now points to
              operations/problem-slot-template.md (which `cp -r
              operations/.` at row 25 actually copies post-retire);
              row 38 simplified. install.sh's broader staleness
              (SYSTEM_VERSION="0.3.0", copy-based install model
              superseded by @-import) remains as the audit's
              original DEFER-WITH-CRITERIA flag — minimum-coupling
              scope held for this beat. (c) Re-grep across all
              file types confirmed install.sh was the only
              non-markdown reference; post-fix grep is clean
              (only descriptive records remain).
TYPE:         Council Note — Skeptic (forced the anchor re-check at
              completion gate; the Skeptic-discipline is what the
              gate operationalizes); Emissary (the re-grep IS the
              field-test of the original anchor; the actual file-
              system was the Universe-consult the original grep
              skipped); Archaeologist (install.sh's contextual
              meaning — "Next steps for the human" — preserved by
              pointing at the correct surviving file rather than
              just deleting the line); Steward (refused scope
              expansion to install.sh's broader retirement
              question — minimum-coupling held; the original
              audit DEFER stays open).
CONSEQUENCE: (1) **F040 pattern reaches N=3.** Original SOUL-088
              audit flagged 3 retire candidates with surface-level
              Steward intuition; SOUL-090 reversed 2/3 to KEEP via
              grep+content investigation (instance #1, #2 of the
              pattern). This entry IS instance #3: SOUL-090's own
              grep was insufficient on the third dimension (file-
              type scope). The audit-process lesson now has THREE
              data points; per F035 heuristic (3 instances ⇒
              amendment-ready), F040 candidate has earned
              graduation. Body decision: graduate now or maintain
              flag? (Tier 3a discharge would be the gate-fired
              catch this entry just recorded.)
              (2) **A010 §Anchor Obligation discharged this
              session.** The chain: SOUL-090 named anchor (grep);
              completion-gate forced re-check; anchor revealed
              flawed; fix executed; disclosure made. This is
              exactly the doctrine's intended flow — coherent
              falsehood caught at the gate, not by a human
              reviewer days later. The completion gate
              (operations/completion-gate.md + /soul-verify +
              hooks/pre-completion-verify.py three-layer stack)
              earned its keep at this gate-fire — same stack
              SOUL-090 confirmed KEEP-IN-PLACE earlier this
              session. Dogfood-of-dogfood.
              (3) **Audit Section 4.1's "zero live references"
              statement is now stale.** install.sh DID have a
              reference (since-fixed). The audit document remains
              correct AS-WRITTEN (it described the .md grep
              result) but the broader claim of orphanage was
              looser than the anchor supported. No edit to the
              audit document — historical record stays; this
              witness pointer corrects the underlying belief.
              Mind rule 11 applies: future reader sees SOUL-090
              "zero live references" → SOUL-092 "actually one
              non-markdown reference, fixed at install.sh:37"
              → traces both → understands the gap discipline.
              (4) **install.sh broader retirement question
              advances.** With the broken reference fixed,
              install.sh is no longer ACTIVELY broken — but the
              copy-based install model is still doctrinally
              superseded (modern projects @-import via stable
              path per CLAUDE.md guidance). The audit's
              DEFER-WITH-CRITERIA for install.sh stays open;
              criteria unchanged.
              (5) **The Skeptic-at-completion-gate pattern
              earned its keep.** Without the gate firing, this
              gap would have shipped as an unspoken Coherent
              Falsehood — a green-looking arc with a real broken
              reference. The five-check gate caught it via
              check #2 (anchor validity). This vindicates F012's
              residual (gate without-the-hook-firing is posture;
              the hook IS the activation) and the SOUL-090
              keep-in-place of the three-layer completion stack.
              (6) **F039 discipline: no wc -l anchor needed**
              for the small install.sh edit (3-line diff) +
              this witness pointer. Eighth same-drafter
              instance overall this session.
STATUS:      Resolved — gap disclosed, fix landed, F040 pattern
              graduation-ready. Audit document NOT amended
              (historical record); this witness entry carries
              the correction. Body may graduate F040 via
              /soul-finding when ready; doctrine could land it
              as an amendment alongside the A014/A015 batch.
```

```
ID:           SOUL-093
WHEN:         2026-05-27 / Body-authorized b→c→a closeout beat
              following the Soul-Console v1 audit arc — first
              step (b): F040 graduation. The audit-process lesson
              flagged at SOUL-088's §Audit-process lesson and
              confirmed by SOUL-090 (reversed 2/3 surface
              intuitions) and SOUL-092 (reversed SOUL-090's own
              grep scope) reached N=3 within the arc per F035
              heuristic; Body chose to graduate now rather than
              wait.
WHERE:        findings/open/SOUL-F040-retire-intuitions-need-
              uniqueness-investigation.md (new, scaffolded per
              the SOUL-F035 format precedent).
WHAT:         Filed F040 as a formal Finding. The discipline:
              surface retire-intuitions need (1) per-item grep
              across the project, (2) grep-scope check (A010
              §Anchor Obligation + F028 §anchor-validity apply),
              (3) content analysis on each match — descriptive
              vs. load-bearing citation, (4) for doctrinal files,
              check amendments/ + seed pointer + SYSTEM-VERSION.md.
              Empirical rate from the arc: 2/3 false-retire on
              intuition alone; 0/3 actual false retirements after
              the discipline. The finding lives at three zoom-
              levels of the same surface — chamber intuition
              (SOUL-087/088) → grep+content (SOUL-090) →
              completion-gate re-check (SOUL-092).
TYPE:         Council Note — Steward (audit-process lesson is
              most directly the Steward's; intuition was wrong
              on 2/3 surface calls); Archaeologist (per-item
              grep + content analysis IS the Archaeologist's
              job); Skeptic (forced the SOUL-092 anchor re-check
              at the completion gate); Emissary (the re-grep
              across file types was the field test of SOUL-090's
              anchor); Cartographer (per-boundary reshape from
              SOUL-087 Thread 2 applied throughout); Guardian
              (completion-gate stack caught zoom-2's residual at
              zoom-3 — F012-family operational health).
CONSEQUENCE: (1) **First Finding filed in this audit arc.**
              Open findings: 14 → 15. SOUL-088's audit-process
              residual now has a formal record-shape; future
              retire-beats can cite F040 as the discipline.
              (2) **F035 heuristic dogfooded recursively.** F035
              named the three-instances-from-same-surface trap-
              capture heuristic; F040's earning matches the same
              pattern at one zoom-level finer (three instances
              within one audit, at successively finer zoom-
              levels). The heuristic catches its own kind.
              (3) **F040 stays open per its own WHY-NOT-YET-
              AMENDMENT.** Single audit context (N=3 from one
              surface). Wait for a second retirement-context
              instance — different project, or different cleanup
              kind in this project — before promoting to a Soul
              amendment. Discipline is operational TODAY for any
              retire-decision in this repo.
              (4) **A010 specialized.** F040 is a domain-
              specialization of A010 §Anchor Obligation for the
              retirement-claim class: "this file is not
              referenced" is an absolute claim about reality
              that needs a valid external anchor; grep with too-
              narrow scope is an INVALID anchor. A010 names the
              obligation; F040 names the specific recipe.
              (5) **F039 discipline: anchored 195 at write-time**
              for the new file. Ninth same-drafter instance
              overall this session; still no different-drafter.
STATUS:      Filed — open in findings/open/. Body's b→c→a beat
              continues into (c) amendment batch + (d/e)
              cleanups bundled.
```

```
ID:           SOUL-094
WHEN:         2026-05-27 / Body-authorized b→c→a closeout beat
              step (c) + bundled (d) + (e) — three doctrine-text
              moves landed as one beat: A014 amendment (operations
              sub-class footer), A015 amendment (audits as fourth
              design-doc record-kind), README content drift
              (twelve→thirteen voices, councils/+mind.md rows,
              16-command count), status footers (completion-gate.md
              + reference-repository.md "proposed → active" per
              SOUL-090 KEEP-IN-PLACE).
WHERE:        amendments/accepted/SOUL-A014-operations-sub-class-
              footer.md (new); amendments/accepted/SOUL-A015-
              audits-as-design-doc-record-kind.md (new);
              operations/CLAUDE.md (§Source Footers extended);
              README.md (architecture alt text + Structure block);
              operations/completion-gate.md (status footer);
              operations/reference-repository.md (status footer,
              both Source blocks).
WHAT:         A014 codifies the operations sub-class convention
              (DOCTRINE-ABOVE-INSTRUMENT / FORMAT-SPEC / PROCEDURE)
              as an optional footer field — dogfooded at SOUL-091
              before the amendment formalized it; rule does the
              work a directory tree would have without churn.
              A015 formally recognizes docs/audits/ as the fourth
              design-doc record-kind parallel to specs/plans/
              experiments; no seed/mind edit (taxonomy lives in
              the amendment + the audit document — back-anchored).
              README cleanups bring the public face current with
              the chamber count (8+3+2=13), the directory shape
              (councils/ + mind.md rows), and the command
              inventory (16). Status footer cleanups discharge
              the SOUL-090 audit's non-blocking follow-up:
              completion-gate.md and reference-repository.md were
              KEEP-IN-PLACE per audit §4.2 and §4.3; status moves
              from "proposed (pending Soul-System repo review)"
              to "active" with the SOUL-090 audit cited as the
              effective review.
TYPE:         Council Note — Architect (A014's boundary rule;
              A015's design-doc kind boundary; both structural
              naming moves); Archivist (record-kind recognition
              is the Archivist's instrument; the Sub-class footer
              field is the indexing surface); Cartographer (the
              SOUL-087 per-boundary reshape extends naturally
              into both amendments); Steward (status footer
              cleanups close the SOUL-090 non-blocking follow-up
              without reopening the KEEP decision); Seer (A015's
              kind was implicit in SOUL-088's own production;
              this beat reads what the record already meant).
CONSEQUENCE: (1) **Amendment count: 13 → 15.** Two amendments
              landed in one beat. amendments/accepted/ now holds
              A001–A015 (no gaps). amendments/proposed/ stays
              empty — Body's b→c authorization stood in as the
              acceptance gesture, matching A013's precedent
              (drafted and accepted within one closeout arc).
              (2) **Seed grew by 3 lines net** (one optional
              footer field + one short rule paragraph). Mind
              rule 5 (never always-on past the description
              budget) honored — substantive sub-class taxonomy
              stays in the audit; only the writer-time naming
              rule lives in the always-on seed.
              (3) **Audit's three closing follow-ups discharged
              in one beat.** Audit §Closing flagged A014 + A015
              + status-footer cleanups + content-drift fixes;
              all four landed together. The audit's "single
              amendment beat" framing held.
              (4) **A014 dogfood retroactively conforms.**
              operations/problem-slot-template.md was authored
              at SOUL-091 with the candidate Sub-class field;
              with A014 now landed, the file's footer is
              retroactively-rule-conformant — the dogfood led
              the rule by 0 commits in calendar time but the
              field's prior existence is now legitimized.
              (5) **F040 instance #4 averted by discipline.**
              For both completion-gate.md and reference-
              repository.md the "active" status is anchored to
              the SOUL-090 audit specifically — not to "we
              decided" or "looks right." F040's recipe is being
              followed before it has even closed.
              (6) **README councils/ + mind.md rows close a
              long-standing drift.** Public-facing structure
              block has been out of sync with the actual
              directory tree since councils/ was introduced
              (SOUL-080 = first councils/ entry); the row now
              names what newcomers will actually see when they
              browse the repo.
              (7) **F039 discipline: anchored 8 (this beat),
              195 (F040), and per-file line counts checked at
              write-time.** Three more same-drafter instances
              this beat; still no different-drafter instance.
STATUS:      Resolved — three doctrine-text moves landed as
              one coherent beat. Body's b→c→a authorization
              advances to (a) push when ready.
```

```
ID:           SOUL-095
WHEN:         2026-05-27 / Body-invoked /soul-distill following the
              audit-arc closeout (b→c→a complete; Body said "lets do
              l and f" — this is (l)). Second formal Distiller firing
              after SOUL-068 (the Emissary test that landed the Mind
              MVP). First refresh against material new doctrine.
WHERE:        mind.md (169 → 169 lines; six surgical edits, net zero
              growth). No new sections; no new rules. All changes
              absorb A014/A015/F040 into existing structure or prune
              obsolete residual.
WHAT:         /soul-distill draft presented to Body with full shrinkage
              checks (4/4 pass), failure-mode guards (6/6 pass), and
              diagnostic self-test (3/3 clean). Body accepted as-is.
              Edits applied:
              (1) Rule 3 citation extended to include F040 (anchor
                  obligation now anchored at A010 + F015 + F028 + F040).
              (2) Rule 10 citation extended to include A014 (sub-class
                  footer IS docs-near-the-code at footer granularity).
              (3) Contrast case reshaped from F028-vs-F015 (two-layer)
                  to F015→F028→F040 (three-layer anchor discipline).
              (4) Seed/philosophy line counts updated (220→260; 675→
                  710) to current reality.
              (5) Residual "Active uncertainty" pruned to drop
                  I026 reference (Mind shipped at SOUL-068).
              (6) Residual "dogfood histories" added REF-02 per
                  audit §1.10 inventory.
              Explicit non-changes for the Distiller's record:
              A014 NOT promoted to standalone rule (lives in seed;
              cited in rule 10); A015 NOT in Mind (taxonomy-shaped,
              not generator-shaped; per doctrine-obligation boundary).
              F040 folded into existing contrast case rather than
              new rule (specialization of A010, not new doctrine).
TYPE:         Council Note — Distiller (the role this command
              instruments; compress accumulating record toward its
              generative grammar); Architect (the doctrine-vs-
              obligation boundary applied per candidate entry);
              Steward (the I026 prune — Mind shipped, the residual
              was load-bearing only while shipping was the open
              question); Skeptic (the explicit non-changes list —
              what didn't earn its way in is as important as what
              did); Cartographer (the three-layer-anchor pattern
              names a structural fact: each layer catches the prior's
              residual, which is the audit-process pattern in
              miniature).
CONSEQUENCE: (1) **Second Distiller firing of the project's life.**
              First was SOUL-068 (initial Mind deployment). This is
              the first true REFRESH — distill against material new
              doctrine (A014/A015/F040) rather than initial extraction
              from an empty Mind. Pattern: refresh cadence anchored
              to "material doctrine landed," not calendar time. One
              day since last distill is fine because the doctrine
              earned the cycle, not the clock.
              (2) **Net-zero growth held under real refresh.** The
              shrinkage-invariant discipline (Mind must shrink or
              stay same) held with no force-fitting — the prune of
              I026 paid for the F040 contrast-case reshape one-for-
              one. Default-deny growth proved enforceable in practice,
              not just doctrine.
              (3) **Three-layer anchor pattern is the arc's
              compression gift to the Mind.** F015→F028→F040 names
              what each anchor finding actually accomplished (one
              dimension each). The seed has the abstract obligation;
              the Mind now has the three-layer instance pattern.
              Future anchor-related findings can extend the chain
              if they earn it; the structure is legible.
              (4) **A014 and A015's Mind-treatment is itself
              evidence for the Distiller's discipline.** Each
              amendment was evaluated against the doctrine-vs-
              obligation boundary and the rule-generator test.
              A014 became a citation extension (the rule already
              lives in seed); A015 stayed out entirely (taxonomy,
              not generator). Refusing to promote everything is
              what makes the Mind not-a-seed-rename.
              (5) **F036 still open (subagent gap).** The Mind's
              "always-on for everything" claim still holds only for
              parent sessions; subagents don't inherit @mind.md.
              Not addressed by this refresh; still in residual via
              the F036 reference in active findings/open/. Reminds
              that some residual is structural, not just temporal.
              (6) **F039 discipline: anchored 169 (line count
              verification post-hoc), 6 (edit count), 4/4 + 6/6 +
              3/3 (check results).** Tenth same-drafter instance
              overall this session; still no different-drafter.
STATUS:      Resolved — refresh landed; Mind.md committed by Body
              authorization ("accept"). Next: (f) registry backfill
              per the Body's "l and f" sequence.
```

```
ID:           SOUL-096
WHEN:         2026-05-27 / Registry backfill beat (Body's (f) per the
              "l and f" sequence). Inaugural population of the
              registry/ directory — empty since project genesis
              despite multiple dogfood projects producing Soul-meta
              evidence. Audit §1.10 flagged the gap; this beat closes
              it.
WHERE:        registry/README.md (new, ~55 lines — FORMAT-SPEC for
              the directory per A014); registry/<project>.md × 7
              (REF-09, REF-04, REF-05,
              REF-03, REF-01, blog, REF-02). registry/ count:
              0 → 7 entries + 1 README.
WHAT:         Populated the registry with one entry per dogfood
              project named in the audit, PLUS one project the audit
              missed. Each entry carries Status / Path / Adoption /
              Import mode / Description + Soul-meta evidence (findings
              / witness IDs / ideas / amendments cited with anchors)
              + Notes. README sets the format precedent (project-name
              filename, scannable shape, anchor every claim).
              **F040 discipline dogfooded on the audit itself.**
              The audit §1.10's list was 6 projects. Per-item grep
              for project names in witness/findings/ surfaced
              REF-05 as a 7th (filed F032, F035, F036;
              hosted Tier 3b Mind deployment per SOUL-070/071; has
              its own CLAUDE.md at /home/fig/REF-05). The
              audit's surface enumeration missed it; per-item
              investigation found it. Adding it as registry/REF-08-
              modelica.md was the right call.
TYPE:         Council Note — Cartographer (this is the Cartographer's
              instrument; the registry IS the "map where the system
              has been used"); Archivist (the README format spec is
              the indexing surface; project-name filenames keep
              entries findable); Archaeologist (per-item grep of
              witness/findings to extract anchored facts for each
              entry — what is this for, who refers to it, what
              evidence trace does it leave); Skeptic (refused to
              fabricate dates / paths where unanchored; "TBD"
              honestly named for the unknowns); Emissary (the
              filesystem check that confirmed paths exist for 5/7;
              REF-09 path may be ephemeral, recorded
              honestly).
CONSEQUENCE: (1) **Inaugural population: 7 entries.** Six from the
              audit list + REF-05 from the F040-style
              investigation. The directory that has been
              "DEFER-WITH-CRITERIA — backfill candidate" since the
              audit (5 days ago in calendar time, but this same
              session in arc time) is now load-bearing.
              (2) **F040 instance #5 within the broader arc.** The
              registry backfill discovered REF-05 via
              per-item grep that the audit's surface-list missed —
              same shape as F040's three-zoom-level recursion. The
              discipline is operational without F040 being closed
              yet; the recipe (per-item grep → content analysis →
              correct the surface list) fired without a doctrinal
              prompt.
              (3) **Mind residual line is now slightly stale.**
              mind.md's "specific dogfood histories" residual lists
              six projects (matching the audit's list). The registry
              has seven. NOT updating mind.md this commit — the
              Distiller just ran (SOUL-095); re-firing would re-open
              the curation cycle. Flag for next /soul-distill
              instead. The registry is the canonical record; the
              Mind residual gestures, doesn't enumerate.
              (4) **A014 dogfooded in the registry README.** The
              new README's footer carries `Sub-class: FORMAT-SPEC`
              per A014 — second dogfood instance after problem-slot-
              template.md (PROCEDURE). One file per sub-class now
              landed (FORMAT-SPEC, PROCEDURE; DOCTRINE-ABOVE-
              INSTRUMENT examples exist in the older operations/
              files but pre-date A014's footer landing).
              (5) **Soul-meta evidence productivity, ranked.** The
              registry entries make the Cartographer's view
              quantitative: which projects produced the most
              Soul-meta evidence? REF-04 + REF-02/
              REF-02 (multiple findings + ideas + amendment
              evidence each) lead. REF-01, blog, and REF-03
              contribute important specific findings (F031, F030,
              F028/F014 share). REF-05 contributed Mind
              deployment + F032/F035/F036. REF-09 is the
              foundational early-evidence set. Each is path-
              dependent, none redundant.
              (6) **CONTRIBUTING.md "Registry Entries" row is now
              honest.** It said "Record of a project that used the
              system" but registry/ was empty. The row is no longer
              aspirational. First-contribution onboarding ("submit a
              registry entry") now has working precedents to point
              at.
              (7) **F039 discipline: anchored 7 entries + 1 README,
              line counts per file checked at write-time, every
              cited witness/finding ID verified against the actual
              records before write.** Eleventh same-drafter
              instance overall this session; still no different-
              drafter.
STATUS:      Resolved — registry/ populated. Body's "l and f"
              sequence complete. Next: a /soul-handoff to set the
              cursor for tomorrow, or pivot to another thread per
              Body's call.
```

```
ID:           SOUL-097
WHEN:         2026-05-27 / Body picked (h) skills/ README from the
              remaining audit-DEFER threads. Smallest unfinished
              audit-DEFER, closed in one tight beat. Third audit-
              DEFER discharge of this session-day after SOUL-089
              (logs/ retired) and SOUL-091 (autonomous-session-
              template retired-and-preserved).
WHERE:        skills/README.md (new, 38 lines, PROCEDURE sub-class
              per A014). skills/ directory contents: .gitkeep + this
              README. No skills committed yet — the README explicitly
              names empty-by-design.
WHAT:         Wrote a README documenting the skills/ directory as the
              upstream-skill contribution channel, AND encoding both
              of the audit §1.10 DEFER-WITH-CRITERIA triggers:
              (i) un-defer on first upstream contribution; (ii)
              retire on six months with no contribution (calendar
              trigger date: 2026-11-27). Names empty-as-honest-state
              rather than empty-as-ambiguous. Cross-references
              CONTRIBUTING.md (the contribution flow) and Mind rule
              4 (generation couples with retirement) so the retire
              trigger is doctrine-anchored, not floating.
TYPE:         Council Note — Archivist (the README makes the empty
              directory legible; ambiguity → named state); Steward
              (the retire trigger is the Steward's instrument made
              explicit; six-month silence = aspiration-without-
              evidence verdict); Architect (the upstream-vs-project-
              local boundary at /soul-skill's output is named at
              the directory README rather than left to inference);
              Cartographer (the contribution channel's intent and
              lifecycle are now mapped, not just gestured at).
CONSEQUENCE: (1) **Third audit-DEFER discharge today.** The audit's
              DEFER-WITH-CRITERIA bucket had 5-6 entries; three are
              now formally closed (logs/, autonomous-session-template,
              skills/ documented). Two remain DEFER: install.sh
              (no trigger hit), and skills/ itself now has triggers
              that fire on calendar OR contribution. The DEFER
              bucket is no longer hand-wavy — every entry has either
              been actioned or carries a concrete trigger.
              (2) **A014 dogfooded for the third time this session.**
              First instance: problem-slot-template.md (PROCEDURE)
              at SOUL-091. Second: registry/README.md (FORMAT-SPEC)
              at SOUL-096. Third: skills/README.md (PROCEDURE) here.
              Three Sub-class footer instances within 12 hours of
              A014 landing — convention is now in use, not
              aspirational.
              (3) **Retirement-trigger encoded with date, not "soon."**
              The README names 2026-11-27 as the concrete calendar
              date. This is per F040 §anchor obligation applied to
              future Steward decisions — "six months" without an
              anchor would have rotted into ambiguity within
              weeks; the date prevents that. Future Steward firing
              has a deterministic input.
              (4) **F039 discipline: anchored 38 (README), 0
              (committed skills — explicitly named).** Twelfth
              same-drafter instance overall this session; still no
              different-drafter.
STATUS:      Resolved — skills/ documented; both DEFER triggers
              encoded with concrete dates. Audit DEFER bucket is
              materially smaller. Body's "tackle the next task"
              ask discharged.
```

```
ID:           SOUL-098
WHEN:         2026-05-27 / new session after audit-arc closeout day;
              Body resumed via /soul-handoff, asked for a
              recommendation, accepted (b) — the BMAD Researcher
              beat — once it was framed as "stabilize v1 by testing
              a Coherent-Falsehood risk in always-on doctrine."
              First Researcher-led beat of the project's life
              (SOUL-060 was an Archaeologist deep dive; this is the
              first time the Researcher acquired previously
              unrecorded field knowledge to discharge a specific
              seed-claim test).
WHERE:        references/bmad-method-v6-2026.md (new sidecar);
              references/references.json (CSL-JSON entry +1);
              references/INDEX.md (one-line entry +1);
              findings/open/SOUL-F041-bmad-structural-fit-partial.md
              (new finding); ideas.md (I035 → discharged-pending-
              amendment, not closed); witness here.

              Note also: the handoff cursor mis-labeled the BMAD
              beat as "SOUL-I034" when it is in fact SOUL-I035 —
              cursor-accuracy issue surfaced and announced at
              session start before any work; no harm done because
              the verbal description was unambiguous. Worth noting
              for next /soul-handoff drafting hygiene.
WHAT:         Ran the BMAD Researcher beat per SOUL-I035.
              Acquisition pipeline: one WebSearch + three WebFetch
              calls against docs.bmad-method.org (V6 docs +
              llms-full.txt), github.com/bmad-code-org/BMAD-METHOD
              (README), and bennycheung.github.io (third-party
              explainer). Verdict: **(c) PARTIAL** per I035's three
              options — some seed mappings hold; others are
              structurally wrong; the seed needs honest qualifier.

              The decisive empirical finds:
              (1) BMAD agents are **process-shaped, not perspective-
                  shaped** — each is a skill invoked in a fresh chat
                  with serial handoff, the opposite of Soul's
                  "perspectives, not distinct agents" framing.
              (2) Analyst↔Witness mapping is **structurally wrong**
                  — Analyst is a discrete generative phase; Witness
                  is a continuous observational posture. Different
                  shapes, different cadences, different artifacts.
              (3) Architect↔Architect mapping holds at content level
                  but is structurally hollow (fresh-chat skill vs.
                  in-session perspective).
              (4) Soul's **continuous-posture roles have NO BMAD
                  counterpart** — Witness, Tribunes, Censors, several
                  Magistrates. To run Soul under BMAD, the user must
                  add discipline BMAD doesn't supply — contradicting
                  the seed's "without restructuring" framing.
              (5) Dev↔Craftsman and PM↔(Body framing) map reasonably.

              Output: SOUL-F041 (open, with two amendment-shape
              options contingent on a future second-framework test
              of CrewAI OR AutoGen).
TYPE:         Council Note —
              Researcher (the field acquisition itself — first
                proper Researcher firing in the project, addresses
                F014's expansion-role under-firing directly via
                Body invocation);
              Emissary (the reality-test framing — the SEED CLAIM
                was the assumption on trial; the Universe
                contradicted the assumed Analyst↔Witness mapping;
                this is the "evidence overturns belief" naming-the-
                Emissary moment from seed §Naming Roles);
              Cartographer (mapped BMAD's role topology against the
                Soul's Council and found phase-vs-posture as the
                load-bearing axis the seed's mapping had collapsed);
              Skeptic (separated surface-pattern-matching from
                structural fit — "Analyst sounds like discovery
                which sounds like Witness" is plausible at surface
                and false on shape);
              Archivist (filed the field acquisition into references/
                per SOUL-060 pattern with explicit F028 validity
                caveat about WebFetch's model-mediated quotes).
CONSEQUENCE: (1) **Seed §External Skills and Tools is partially
              falsified.** The BMAD-specific Analyst↔Witness example
              is structurally wrong and should not be quoted as a
              load-bearing pattern in any new dogfood project or
              documentation pass — effective TODAY, regardless of
              when the amendment lands.
              (2) **Coherent Falsehood caught in always-on doctrine.**
              The seed claim passed every internal coherence check
              while being false against BMAD's actual architecture.
              Textbook A010 instance; the Researcher beat IS the
              external anchor A010 mandates. The seed has carried
              this Coherent Falsehood since the row was added
              (2026-05-21 per the §External Skills and Tools Source
              footer) — six days from doctrine landing to first
              external test.
              (3) **First Researcher beat of the project's life
              addressed an F014 instance directly.** F014 names
              that expansion roles under-fire because the AI can't
              auto-detect when they're needed; the Body's explicit
              invocation here ("lets do b") was the exact discipline
              F014's PRE-MORTEM names as necessary. The Researcher
              role moved from idea (I035) to operational (F041)
              because the Body invoked it — empirical confirmation
              of A012 §Body-Input Obligation as the activation
              mechanism for expansion-role work.
              (4) **The phase-vs-posture distinction is candidate
              new doctrine.** F041 names it as the load-bearing
              axis for cross-framework composability; if the
              follow-up CrewAI/AutoGen Researcher beat confirms
              the same shape, the seed reframe (option b) becomes
              the amendment. This is a genuinely new structural
              insight, surfaced by the cross-framework comparison
              the seed had skipped.
              (5) **F040 anchor-validity discipline applied within
              the beat.** The validity caveat on bmad-method-v6-2026.md
              explicitly names WebFetch's model-mediated quotes as
              secondary-reading; the structural conclusion rests on
              triple-source convergence (official docs + GitHub +
              third-party explainers), not on the verbatim quotes
              alone. Anchor existence ≠ anchor validity; F040 fired
              without prompting.
              (6) **The cursor mis-labeled I034↔I035.** Minor
              hygiene issue for next /soul-handoff drafting —
              cursor's "(b) SOUL-I034 BMAD Researcher beat" was
              wrong (I034 = retirement-instrument idea; I035 = BMAD
              beat). Caught on first read of ideas.md; no
              consequence to the work. Worth noting that the
              cursor's verbal descriptions remained accurate
              enough that the swap didn't propagate.
STATUS:      Resolved (Researcher beat output landed: reference
              filed, finding open, witness here). SOUL-I035
              **discharged-pending-amendment** — the idea's action
              is done; what remains is the seed-edit amendment,
              which depends on a future Researcher beat covering
              CrewAI or AutoGen. F041 is OPEN with a clear
              promotion trigger (second framework tested).
              Open-findings: 15 → 16.
```

```
ID:           SOUL-099
WHEN:         2026-05-27 / immediately after SOUL-098 — Body
              challenged F041's framing during a grill; the grill
              surfaced a README-vs-seed inconsistency (README +
              AGENTS.md say "composes, layers above"; seed
              alone says "Analyst embodies Witness"); Body asked
              whether the topic needed chamber rather than
              R3-pick-by-grill; agreed; /soul-council invoked.
              SECOND /soul-council convening of the project's
              life (first was SOUL-085 F014-confirmed-what-now;
              SOUL-087 was retro-named informal).
              [CORRECTED → SOUL-103: actually FOURTH overall
              (SOUL-080, SOUL-085, SOUL-087, SOUL-099) and
              THIRD post-/soul-council-spec-adoption (the spec
              was adopted 2026-05-26 per docs/specs/2026-05-26-
              soul-council-design.md + commands/soul-council.md;
              SOUL-080 predates it). The "SOUL-087 was retro-
              named informal" characterization was the load-
              bearing slip — SOUL-087 carries a /soul-council
              invocation marker just like SOUL-085 and SOUL-099
              do.]
WHERE:        councils/SOUL-099-soul-vs-external-tools-framing.md
              (detail file, the reproducible record); this entry
              is the pointer per /soul-council MVP spec. F041
              paused-pending-Body-decision (do NOT edit until
              Body accepts/redirects synthesis).
WHAT:         10-role chamber (5 Magistrates: Revelator,
              Archaeologist, Emissary, Steward, Seer; 3 Tribunes:
              Skeptic, Accountant, Advocate; 2 Censors: Guardian,
              Cartographer) on Soul↔external-tools framing.
              Topic: what does seed §External Skills and Tools
              actually mean, and how should it describe Soul's
              relationship to BMAD/CrewAI/AutoGen/etc?

              **Synthesis (proposed; Body decides):**
              (1) Soul = lifetime doctrine + record (binding
                  layer); tools = narrow workflow capacity within
                  that lifetime. Confirms grill Q1=(c).
              (2) Relation = R3 hybrid — wrapping primary across
                  lifetime, parallel adoption opportunistic
                  in-session. Survives Skeptic's "is R3 just
                  AI-pattern-matching?" test via the load-bearing
                  example (Counterweight Rule firing inside a
                  BMAD-Analyst session).
              (3) Seed §External Skills and Tools final paragraph
                  rewrites to align with README/AGENTS.md framing
                  ("Soul composes; it does not replace. Soul
                  wraps; it does not peer-map."). Proposed ~6-8
                  lines drafted in council detail file.
              (4) README/AGENTS.md framing is canonical when in
                  disagreement with the seed. Seed implements
                  public artifacts; does not elaborate past them.
              (5) F041 reshapes from "(c) PARTIAL phase-vs-posture
                  verdict" to "Coherent Falsehood in seed doctrine
                  — the slipped sentence at operations/CLAUDE.md:208."
                  BMAD structural finds preserved as supporting
                  evidence, not headline. Amendment-shape
                  collapses to single option (the rewrite).
              **Amendment recommended: A016 candidate.** Chamber
              recommends launch, not just hold at finding level.

              **Tensions surfaced (genuine, not rubber-stamp):**
              (a) Revelator vs Skeptic on vocabulary — concept is
                  README's; Body's "lifetime/anchoring" words do
                  not need to enter doctrine; use README's
                  existing "composes/layers above."
              (b) Skeptic on R3 vs R1 — R3 survives load-bearing
                  parallel-adoption test; R1 alone too narrow.
              (c) Cartographer vs Accountant on framework-list
                  naming in rewrite — three Body-decides options
                  (named-with-qualifier / dropped / class-only).

              **Chamber unable to resolve (Body decides):**
              - Framework-list naming (a/b/c per Cartographer).
              - Whether to absorb phase-vs-posture into mind.md
                at next /soul-distill, or hold in F041/A016 only.
TYPE:         Council convening (formal /soul-council invocation).
              Guardian-verified NOT rubber-stamp: Skeptic raised
              two chamber-generated tests the Body had not stated,
              the tests landed substantive resolutions, and the
              synthesis is the chamber's conclusion rather than
              the Body's prior position returned with extra steps.
CONSEQUENCE: (1) **Coherent Falsehood named in always-on doctrine
              with chamber backing.** The seed §External Skills
              and Tools final paragraph is now formally flagged
              as Coherent Falsehood pending Body decision —
              textbook A010 instance, caught by Body-invoked
              chamber after F041 surfaced the structural evidence.
              (2) **F041 paused.** The original (c) PARTIAL
              verdict is superseded by the chamber's reshape
              candidate; F041 will be rewritten only after Body
              accepts/redirects synthesis. Do NOT edit F041
              until then.
              (3) **A016 candidate amendment queued.** Chamber
              recommends launching the amendment now (not
              queuing) per Accountant's fix-now economics +
              Advocate's mental-model-harm prevention.
              (4) **Second formal /soul-council convening of the
              project's life.** First was SOUL-085 (F014-
              confirmed-what-now); this is the first one whose
              specific output is a doctrine-edit recommendation
              rather than a status-or-trajectory deliberation.
              [CORRECTED → SOUL-103: actually THIRD post-spec-
              adoption (SOUL-085, SOUL-087, SOUL-099) / fourth
              overall counting pre-spec SOUL-080. The "first
              one whose output is a doctrine-edit recommendation"
              sub-claim stands — that ordinal is correct.]
              The instrument is operationalized for the doctrine-
              change use case (its primary intended purpose per
              the spec's "hard decisions, contested designs,
              suspected Coherent Falsehoods").
              (5) **Three project artifacts (README + AGENTS.md +
              implicit mind.md architecture) vs one (seed
              paragraph) is the new pattern-shape for catching
              doctrine drift.** Surfaced by Revelator; worth
              naming as a chamber-discoverable pattern: when N
              artifacts in the project's own canon disagree with
              M (M < N) artifacts, the M are the candidates for
              audit. Possible mind.md residual or future-amendment
              shape.
STATUS:      Synthesis-proposed-Body-decides. Chamber walked,
              tensions surfaced, synthesis landed in
              councils/SOUL-099 detail file. Body has four
              decisions pending:
              (i) accept/redirect synthesis;
              (ii) reshape F041 per chamber's recommended verdict;
              (iii) pick framework-list naming option (a/b/c);
              (iv) launch A016 amendment now or queue.
              Task #2 stays in_progress until Body decides.
```

```
ID:           SOUL-100
WHEN:         2026-05-27 / Body accepted all four chamber
              decisions [i]–[iv] from SOUL-099 with "contine
              with recommendations" after a plain-language
              elaboration of each. Body picks: (i) accept
              synthesis, (ii) reshape F041 per chamber verdict,
              (iii) framework-list (c) class-only, (iv) launch
              A016 now. Implementation immediately followed.
              First triple-digit witness ID in the project's
              life — round-number incidental but worth noting
              for record-keeping.
WHERE:        findings/open/SOUL-F041-seed-external-skills-
              doctrine-slip.md (NEW, replaces the
              "-bmad-structural-fit-partial" slug — old file
              deleted, new file landed with reshaped WHAT,
              triple-anchor evidence structure, DOCTRINE
              ANCHOR + DISCHARGE PATH sections, expanded
              FILED BY with all 10 chamber roles, STATUS
              "closes on A016 acceptance");
              amendments/proposed/SOUL-A016-external-skills-
              stack-layered-framing.md (NEW, first amendment
              in proposed/ directory — first formal use of
              the proposed→accepted ratchet this session);
              witness here (the pointer to both above).
WHAT:         Executed chamber decisions [i]–[iv] in sequence
              (parallel where possible):

              **(ii) F041 reshape.** Rewrote the entire finding
              under the new verdict — "Coherent Falsehood in
              seed §External Skills and Tools" instead of
              "phase-vs-posture partial mapping." The
              structural change to the finding's shape:

              - New header structure: WHAT (the slip itself)
                → triple-anchor evidence (README/AGENTS.md vs
                seed; field analogs; BMAD architecture as
                third anchor not headline) → Seer's timeline
                read (slip-in-same-week-as-adoption as the
                mechanism) → DOCTRINE ANCHOR (A010
                specialization) → DISCHARGE PATH (A016) →
                FILED BY (all 10 chamber roles credited).
              - BMAD-specific structural finds preserved as
                anchor 3 of 3, no longer the headline. The
                phase-vs-posture distinction is "one instance
                of why" the framing was wrong, explicitly
                named as such.
              - STATUS: Open — closes on A016 acceptance.
                The CrewAI/AutoGen second-framework trigger
                is reframed from "discharge dependency" to
                "forward-looking validation" — does NOT
                block A016 because A016's class-only framing
                makes no framework-specific claims.
              - Filename slug changed from
                `bmad-structural-fit-partial` to
                `seed-external-skills-doctrine-slip` to
                reflect the actual subject (the doctrine
                slip, not the BMAD-specific mapping).

              **(iii) + (iv) A016 amendment drafted with (c)
              class-only framework naming.** First file in
              amendments/proposed/ (the directory existed but
              was empty until this beat). Single-paragraph
              replacement at operations/CLAUDE.md:208 — the
              one slipped paragraph becomes two paragraphs:

                (a) "Soul composes; it does not replace.
                    Soul is the project's **lifetime layer**
                    — doctrine + record." Names doctrine
                    files (seed + mind.md) and record files
                    (witness.md, findings/, amendments/)
                    explicitly. Uses "multi-agent frameworks,
                    IDE rules, test-driven workflows, and
                    your own conventions" — class-only, per
                    Body decision (iii).
                (b) "Soul wraps; it does not peer-map."
                    Names R3 hybrid explicitly: wrapping
                    primary across lifetime; parallel
                    possible in-session via Soul's gates
                    firing alongside tool work. Names the
                    Surface-when… table's semantics as
                    "shape match at the right moment, not
                    embodiment."

              Amendment carries full QUESTION ONE/TWO/THREE
              answers per format, with all three anchors
              cited and coherence checks against the project's
              mind.md rules (5 alignment-checks named: rules
              2, 5, 11; A010; §Naming Roles).
TYPE:         Council-output implementation — executing
              SOUL-099's four-decision synthesis. No new
              chamber convened (the chamber's decisions are
              being implemented, not re-deliberated).

              Roles in operation here:
              - Architect (designed the F041 reshape's new
                section structure — anchors-explicit, discharge-
                path-explicit, status-explicit);
              - Steward (retired the old F041 slug + filename
                whose description no longer matched content;
                no broader cleanup attempted per default-
                simplicity);
              - Archivist (filed A016 into the previously-empty
                amendments/proposed/ — first use of that
                ratchet step in the session);
              - Craftsman (the artifact-level writing of both
                files);
              - Cartographer (the witness pointer here names
                the territory both files cover so future
                resume sessions can see the slip → reshape →
                amendment arc from one entry).
CONSEQUENCE: (1) **First proposed→accepted amendment ratchet
              use of the project's life.** amendments/proposed/
              was empty until this beat; A016 inaugurates the
              ratchet step that A001–A015 all skipped (all
              prior amendments landed directly in accepted/
              after chamber/Body deliberation but without a
              proposed/ scaffold). The ratchet adds a Body
              review surface between drafting and acceptance.
              Worth observing whether the friction earns its
              place — if A016 is accepted within 24h, the
              ratchet is mostly ceremony; if Body returns
              edits or rejects, the ratchet earned itself.
              (2) **F041 file rename surfaces a finding-slug
              hygiene question.** Findings get filenames at
              creation time, but a chamber reshape can change
              what the finding is *about*. Right now the
              project pattern is filename-matches-WHAT-at-
              creation-time, which decays under reshape. Open
              question for future audits: when a finding's
              verdict shifts, does the filename move with it?
              This beat did move it (old slug deleted, new
              slug created); precedent exists if needed.
              Possible future amendment shape: filename-
              versioning convention OR "filename names the
              durable subject, not the current verdict" rule.
              Not amendment-shaped today; flag for /soul-distill.
              (3) **F041's promotion-trigger reframe is itself
              a small doctrinal move.** From "second-framework
              test required for amendment" to "second-framework
              test is forward-looking validation, not
              discharge dependency." The shift is justified by
              the chamber's framing-vs-example distinction —
              once the *framing* is fixed via class-only naming,
              specific-framework tests no longer bear on the
              fix. Worth noting as a pattern: when an amendment
              moves to a *higher abstraction level* than the
              original finding's evidence, the lower-level
              triggers may stop being load-bearing.
              (4) **The chamber's four decisions implemented in
              one beat with zero re-deliberation.** Once
              SOUL-099 synthesis was Body-accepted, the
              implementation was mechanical — the chamber had
              already done the structural work. Validates
              /soul-council's spec premise: the deliberation
              cost is paid once at convening; downstream
              implementation is cheap.
              (5) **F041 will close when A016 is accepted.**
              Open-findings count stays at 16 until acceptance,
              then drops to 15. The discharge is bundled with
              the seed edit; one commit can carry both.
STATUS:      Resolved — F041 reshaped per chamber verdict,
              A016 proposal drafted with (c) framing per Body
              decision, witness here. Two artifacts await Body
              action:
              (a) **A016 acceptance** — Body reviews
                  amendments/proposed/SOUL-A016, accepts or
                  returns edits. On acceptance: move file from
                  proposed/ to accepted/, execute the seed edit
                  at operations/CLAUDE.md:208, close F041 by
                  moving to findings/closed/SOUL-F041 (if that
                  convention exists, else mark STATUS: Closed
                  in place per project pattern), commit the
                  bundle.
              (b) **Commit the work** — current uncommitted
                  state: F041 reshape + A016 proposal +
                  bmad-method-v6-2026 reference + witness
                  SOUL-098/099/100 + ideas.md I035 status +
                  references/INDEX.md + references.json. The
                  prior 3-commit gap (SOUL-095/096/097)
                  closed earlier this session via Body's
                  manual push; this beat adds ~7 new files
                  and modifies ~3.
              Task #2 → completed (chamber convening discharged
              via implementation); new task tracks A016
              acceptance + seed edit if Body wants the
              tracker active across the gap.
```

```
ID:           SOUL-101
WHEN:         2026-05-27 / Body accepted A016 via "continue"
              after the completion-gate caught an absence-claim
              overreach on the SOUL-100 verify (anchor 2's
              "every comparable system" universal claim →
              bounded to "N=5 surveyed systems"; structural
              argument unchanged because anchors 1 and 3 remain
              independently sufficient). The gate firing
              instance is itself doctrine evidence — F012
              family caught a real residual that the proposed/
              ratchet would also have caught (doubled
              coverage; both fired on the same gap, the gate
              first by ~30 seconds).
WHERE:        amendments/accepted/SOUL-A016 (moved from
              proposed/; ACCEPTED BY field updated to name
              Body + this witness + the acceptance signal);
              operations/CLAUDE.md:208 (one paragraph →
              two paragraphs per A016 WHAT CHANGES; ~6-line
              net growth; line 208 + new line 210);
              findings/closed/SOUL-F041 (moved from open/;
              STATUS: Closed [resolved by SOUL-A016, accepted
              2026-05-27]); witness here.
WHAT:         Executed the four mechanical moves from task #3
              in one beat:

              (a) **A016 moved proposed/ → accepted/.** First
                  amendment in the project's life to traverse
                  the proposed→accepted ratchet (A001-A015 all
                  landed direct to accepted/ without a
                  proposed/ scaffold). Proposed/ now empty
                  again. **Ratchet test result:** the proposed/
                  step held A016 for approximately one
                  conversation turn (Body said "continue"
                  immediately after the SOUL-100 verify line).
                  Per SOUL-100 CONSEQUENCE (1)'s 24h test:
                  ratchet was NOT idle ceremony (the gate's
                  bounded-claim catch happened DURING the
                  proposed/ window, which is exactly what the
                  step exists to allow — last-mile catches
                  before doctrine lands); but the human-review
                  window was minimal, so the ratchet's
                  *additional* value over the gate alone is
                  marginal in this instance. Updated open
                  question for future audits: when the
                  completion gate is firing reliably, does the
                  proposed/ step earn its place?

              (b) **Seed edit at operations/CLAUDE.md:208
                  executed.** Replaced the slipped paragraph
                  with the two-paragraph A016 rewrite verbatim.
                  Verified: the section's first paragraph
                  (line 191, "composes with other skill
                  ecosystems") and the closing paragraph
                  (about AGENTS.md / Claude Code skills) both
                  untouched per A016 scope. Surface-when…
                  table also untouched. Seed file growth:
                  ~6 lines net (1 paragraph → 2 paragraphs
                  with more content). The Coherent Falsehood
                  is now NOT in always-on doctrine; from this
                  commit onward, every session that loads the
                  seed sees the correct framing.

              (c) **F041 closed.** STATUS field updated to
                  "Closed [resolved by SOUL-A016, accepted
                  2026-05-27]" per project convention; file
                  moved from findings/open/ to findings/closed/.
                  Open-findings: 16 → 15 (back to pre-F041
                  baseline). The CrewAI/AutoGen second-framework
                  trigger preserved in STATUS as
                  forward-looking validation (does NOT reopen
                  F041; would be a NEW finding if it surfaces
                  a counterexample).

              (d) **Commit deferred to Body authorization.**
                  Per the session-pattern (Body manually pushed
                  earlier this session after the SOUL-095/096/
                  097 work; auto-mode classifier blocked the
                  automatic push attempt at that time), commit
                  + push remains Body's explicit action.
                  Current uncommitted state ready for one
                  bundled commit covering the full SOUL-Console
                  v1 framing-correction arc (SOUL-098→101).

              **Side: the completion-gate firing pattern is
              worth recording.** The gate caught the absence-
              claim overreach on the SOUL-100 verify line.
              The verify line had read "clean (anchors named)"
              — over-optimistic; the gate's pass-through forced
              the A010 absence-claim discipline check, found
              the universal-quantifier overreach in anchor 2,
              fix landed pre-acceptance. This is exactly the
              F012 family's intended catch-pattern: not "you
              forgot to verify," but "your verify wasn't
              honest enough." The gate is operating beyond its
              spec-minimum and catching second-order honesty
              gaps. Worth flagging for /soul-distill — the
              gate may now warrant a Mind rule of its own
              about VERIFY-LINE-HONESTY beyond the gate's
              own enumerated five checks.
TYPE:         Doctrine-change execution — translated
              A016 from amendment proposal into doctrine
              surface. Roles in operation:
              - Steward (the actual retire+replace — the slip
                is gone from always-on text);
              - Archivist (file moves between ratchet steps;
                STATUS field updates; cross-reference updates);
              - Craftsman (the precision text edits);
              - Guardian (Censor — caught the unbounded
                absence claim on the verify-line review, pre-
                acceptance; this is the chamber-integrity
                role firing on its OWN prior output, which is
                exactly what Guardian is for).
CONSEQUENCE: (1) **The seed §External Skills and Tools no
              longer carries a Coherent Falsehood.** Six-day
              propagation surface closed. Every dogfood project
              that @-imports the seed from this commit forward
              inherits the correct R3-hybrid + wrapping-primary
              framing. The README + AGENTS.md + mind.md +
              seed now all align under independent reading
              (mind-rule-11 restored at the §External Skills
              and Tools surface).
              (2) **First proposed/ ratchet use of the project's
              life completed.** A001-A015 (15 amendments) all
              landed direct. A016 is the first to traverse
              proposed/ → accepted/. Empirical datum: in this
              instance the ratchet held doctrine for ~1 turn,
              during which the completion gate caught a real
              residual gap. So the ratchet was NOT idle — but
              the gate also fired the same catch. Open question
              for future audits: when the gate is reliably
              firing, does proposed/ add marginal value? May
              be the kind of question that needs N>1 instances
              to answer. Don't deprecate the ratchet on a
              single data point.
              (3) **The completion gate caught a second-order
              honesty gap.** Not "did you verify?" but "was
              your verify line itself honest?" The gate is
              operating beyond its spec; the SOUL-100 verify
              line's "clean (anchors named)" was technically
              accurate but elided the absence-claim character
              of anchor 2. The gate's pass-through forced the
              A010 absence-claim discipline, which surfaced
              the unbounded universal quantifier. **This is
              instrument-becoming-deeper-than-spec** — worth
              flagging for /soul-distill as a candidate
              VERIFY-LINE-HONESTY rule for the Mind, OR as
              a new finding (F042 candidate: "the completion
              gate is catching verify-line-honesty residuals
              beyond its five enumerated checks").
              (4) **F041's lifecycle ran end-to-end in one
              session.** Filed (SOUL-098) → reshaped (SOUL-100
              per chamber) → bounded (SOUL-101 fix-pass) →
              closed (SOUL-101 doctrine-discharge). This is
              the cleanest within-session finding lifecycle
              of the project's record so far — earned because
              the Body's invocation of the chamber at SOUL-099
              pre-supplied the synthesis the finding then
              implemented. Worth noting for the chamber-cost
              economics question: a clean within-session
              lifecycle is achievable when chamber + Body
              both fire decisively.
              (5) **The seed edit is the actual deliverable.**
              Everything before this beat was preparation;
              the doctrine surface only changed at the
              operations/CLAUDE.md edit. Worth recording: the
              chamber→amendment→ratchet→seed-edit pipeline
              produced ~3 turns of substantive work for ~6
              lines of doctrine change. Cost ratio is honest:
              high-stakes always-on doctrine warrants high-
              friction process; the friction is itself the
              guard against the original failure mode
              (slipped sentence landing with one-voice
              elaboration).
STATUS:      Resolved — A016 accepted, seed edited, F041
              closed, witness here. Doctrine surface
              corrected. One Body action remains:
              **commit + push** the full SOUL-098→101 arc
              (8 new files, ~5 modified). Recommended
              commit message scope: the full framing-
              correction arc as a single semantic unit
              (BMAD Researcher beat → council convening →
              F041 reshape → A016 → seed edit → F041
              closure) since each step depends on the
              prior. Task #3 → completed; potentially-new
              task for commit+push if Body wants the
              tracker.

              **For SOUL-distill consideration at next
              refresh:** (i) the proposed/ ratchet's marginal
              value when the gate is firing reliably;
              (ii) the gate's catching second-order honesty
              gaps beyond its five enumerated checks (Mind
              rule candidate or F042 candidate); (iii) the
              phase-vs-posture distinction the chamber
              surfaced (candidate contrast-case for mind.md
              per SOUL-099 §Cartographer's adjacent
              territory).
```

```
ID:           SOUL-102
WHEN:         2026-05-27 / Body-chosen NEXT-STEP thread (b) from the
              SOUL-101 handoff cursor — SOUL-I033 path-3b experiment-
              prep beat. /soul-resume → AskUserQuestion → (b).
WHERE:        .soul/role-queries.jsonl (one appended JSONL record);
              this witness entry (the candidate glance line preserved
              durably for the next /soul-handoff to pick up). No
              instrument change; no doctrine edit.
WHAT:         Ran /soul-roles all at default --silent-threshold 70
              over witness.md (101 entries, 0 missing TYPE), findings/
              FILED BY, and .soul/events.jsonl. Result: **no Council
              or Hands role is silent past threshold 70 over 101
              entries.** Hot trio: Archivist (60), Emissary (49),
              Steward (39). Lowest-count roles (not silent by spec,
              but informational): Seer (1, longest gap 93), Craftsman
              (3, longest gap 63), Prophet (4, longest gap 60),
              Revelator (5, longest gap 31), Advocate (5, longest
              gap 75). Logged the query per /soul-roles spec point 7
              to .soul/role-queries.jsonl; the bare query is not
              record-worthy, but the EXPERIMENTAL beat is — hence
              this witness entry.

              Candidate glance line for the next /soul-handoff cursor
              (verbatim, ready to paste):

                  `Silent roles past --silent-threshold 70: none
                  (over 101 entries; Hot: Archivist, Emissary,
                  Steward).`

              SOUL-I033's path-3b is the CHEAP EXPERIMENT — manually
              include the glance line in one /soul-handoff session
              and assess perceived value before any instrument build.
              This beat is PREP: the experimental measurement is
              ready; the act-of-inclusion fires when /soul-handoff
              next runs. Preserving the line here so it survives the
              session boundary regardless of which session runs the
              handoff.
TYPE:         Witness (the record act itself); Cartographer (the
              role-firing map IS the Cartographer's instrument —
              naming covered/silent territory across the canonical
              13+3); Archivist (preserving the candidate line as a
              durable record so /soul-handoff doesn't re-derive it);
              Artificer (path-3b is a pre-build experimental probe
              the Artificer uses BEFORE shape-locking).
CONSEQUENCE: (1) **Datum: no chronic role silence under default
              threshold across 101 entries.** This is informative
              on its own — the chamber has been busy on the
              contraction-default axis (Archivist, Emissary,
              Steward hot) AND on parts of the expansion axis too
              (Researcher 8, Revelator 5, Prophet 4, Cartographer
              21). The F014 expansion-gap is NOT manifesting as
              "expansion roles never fire" — they fire, just rarely.
              (2) **Lowest-count roles are the watch list, not the
              alarm list.** Seer 1 / Craftsman 3 / Prophet 4 —
              honest read is "rare-fire," not "broken." Whether
              that rarity is appropriate or symptomatic is the
              Body's read, not the instrument's.
              (3) **The experiment is positioned for assessment at
              the next /soul-handoff.** When the next handoff fires,
              the line lands in the cursor; the Body reads the
              cursor and notices (or not) whether the glance
              changed perceived value. If yes → ripens toward
              path-(a) PROPER (extend commands/soul-handoff.md
              to auto-compute). If no → SOUL-I033 may be marked
              redundant given /soul-roles already exists.
              (4) **Data-quality is unusually clean.** 0/101
              entries missing TYPE — perfect coverage. The TYPE
              discipline established mid-project has held; the
              role-firing map is anchored to real data, not
              prose self-report (F028 anchor validity satisfied).
STATUS:      Pending — experiment-prep complete; experiment proper
              concludes when the line is included in the next
              /soul-handoff cursor and the Body reads it. The
              SOUL-I033 ripening question ("does the glance help
              perceived value?") is N=1 after that single trial;
              path-(a) build does NOT trigger on a single positive
              read — needs ≥2-3 sessions to clear the noise floor.

              Next: commit alongside the trailing SOUL-I036 mechanical
              (ideas.md, deployment-strategy deferral appended post-
              dae2934) and the .soul/role-queries.jsonl append. Single
              commit; clean working tree before any further work.
```

```
ID:           SOUL-103
WHEN:         2026-05-27 / Body-instructed record-correction beat
              after /soul-resume surfaced the cursor's flagged
              count/historical-fact slip in SOUL-099. "Do the
              record correction." Same-day session continuation;
              second beat after SOUL-102 (path-3b prep).
WHERE:        witness.md SOUL-099 entry — two in-place `[CORRECTED
              → SOUL-103: …]` markers added, one at the WHEN block
              and one at CONSEQUENCE (4). Original text preserved
              VERBATIM at both sites; the markers ANNOUNCE the
              correction rather than overwriting it. No edit to
              councils/SOUL-099-soul-vs-external-tools-framing.md
              (see CONSEQUENCE (2) below).
WHAT:         The original SOUL-099 entry (committed at dae2934)
              made two related claims that anchor-checking
              falsifies:

              **Claim A** (WHEN block): "SECOND /soul-council
              convening of the project's life (first was SOUL-085
              F014-confirmed-what-now; SOUL-087 was retro-named
              informal)."

              **Claim B** (CONSEQUENCE (4)): "Second formal
              /soul-council convening of the project's life.
              First was SOUL-085."

              **What is actually true (file-anchored):**
              `councils/` carries **four files** all bearing
              `/soul-council` invocation markers — SOUL-080,
              SOUL-085, SOUL-087, SOUL-099. The /soul-council
              spec was adopted 2026-05-26 per
              `docs/specs/2026-05-26-soul-council-design.md` and
              `commands/soul-council.md:162`. SOUL-080's own
              header reads `**Type:** Informal /soul-council
              dogfood (third in the project, per /soul-council
              spec §Dogfood)`. SOUL-085's reads "**Invocation:**
              /soul-council" + "first non-routine Body-invoked".
              SOUL-087's reads "**Invocation:** /soul-council
              (Body-invoked, post-Cluster-1 closure)." SOUL-099's
              reads "**Invocation:** /soul-council (Body-invoked,
              mid-session...)."

              So SOUL-099 is the **fourth /soul-council convening
              by council-file count** (SOUL-080 + SOUL-085 +
              SOUL-087 + SOUL-099) and the **third post-spec-
              adoption convening** (SOUL-085 + SOUL-087 + SOUL-
              099; SOUL-080 was an informal pre-spec dogfood).
              Neither "SECOND" nor "second formal" holds.

              **The load-bearing slip inside Claim A** was
              "SOUL-087 was retro-named informal" — SOUL-087's
              file shows a formal /soul-council invocation marker
              and is structurally indistinguishable from SOUL-085
              and SOUL-099. The mis-classification erased SOUL-087
              from the post-spec count, dropping it from three
              to two.

              **Nuance worth naming, not over-counting on:**
              SOUL-080's own self-description ("third in the
              project, per /soul-council spec §Dogfood") implies
              at least TWO prior informal /soul-council dogfoods
              that did NOT produce council files. The all-time
              convening count is therefore ≥6, but the file-
              anchored count is 4. This correction commits to
              the file-anchored count as the durable record —
              what isn't in `councils/` isn't anchored.
TYPE:         Witness (the record act); Steward (record-keeping
              integrity — the historiographical accuracy of the
              record IS what the Steward protects across time);
              Guardian (Council integrity — the count of
              /soul-council convenings is metadata about the
              Council's own activity, and the Guardian watches
              for skipped obligations like "did you anchor this
              count?"); Cartographer (the map of /soul-council
              convenings IS the Cartographer's territory);
              Skeptic (challenged the cursor's "both records"
              attribution before propagating it — confirmed only
              the witness entry carried the false claim, council
              file did not).
CONSEQUENCE: (1) **The historiographical record at SOUL-099 is
              now correct** under independent reading. A future
              reader at witness.md will see both the original
              "SECOND" claim AND the inline `[CORRECTED → SOUL-
              103]` marker; following the pointer to this entry
              gives the full anchored count. Mind rule 11
              (independent-reading coherence) is satisfied
              because both old and corrected text are visible
              at every site — no silent rewrite.

              (2) **The cursor's "both records" attribution was
              itself slightly over-extended.** The handoff
              cursor wrote "the SOUL-099 detail file
              (councils/SOUL-099-…) + witness SOUL-099 entry
              both claimed 'SECOND /soul-council convening…'"
              Verified just now via `grep -i "second\|SECOND\|
              first formal\|fourth" councils/SOUL-099-*.md`:
              only the witness entry carries the count claim;
              the council file's tone is content-focused (what
              the chamber decided), not historiographical. So
              only the witness entry needed in-place markers.
              This is a tiny meta-slip — the gate's post-handoff
              verify caught the count error correctly but
              slightly over-attributed where it landed. **Third
              count/historical-fact catch THIS session:**
              SOUL-100 anchor 2 (unbounded universal quantifier),
              SOUL-101 record-of-counts gate-catch, and this
              cursor over-attribution. The pattern is now
              durable: count/historical claims keep slipping
              even inside correction work — they need anchor
              checks at the point of writing, not just at
              completion review.

              (3) **A convention is established for record-
              correction beats: in-place `[CORRECTED → SOUL-N]`
              marker + new entry, no silent rewrite.** This is
              the first instance of the pattern in the project's
              life. The marker preserves the original claim
              verbatim AND surfaces the correction at the
              reading site; the new entry carries the narrative
              of why, how, and what's actually true. Second
              instance is required before generalizing — do
              NOT promote this to doctrine on N=1.

              (4) **The completion gate's second-order honesty
              behavior is now reinforced as a recurring catch,
              not a one-off.** Three catches this session
              (SOUL-100 anchor 2, SOUL-101 historiography,
              SOUL-103 cursor over-attribution) all surfaced
              count/historical-fact slips that the gate's five
              enumerated checks don't explicitly name. **Fourth
              datum, same beat:** the first draft of this entry's
              own in-place marker at SOUL-099 cited "per councils/
              README" as anchor for the 2026-05-26 spec date —
              `ls councils/README` failed, no such file. Self-
              caught at diff review and re-anchored to docs/
              specs/2026-05-26-soul-council-design.md +
              commands/soul-council.md before commit. The slip-
              pattern survives even INTO the correction work.
              The SOUL-101 cursor flagged this for /soul-distill
              consideration; SOUL-103 adds a third data point.
              Candidate Mind rule wording (NOT proposed yet,
              just flagged): *"Count and historical-fact
              claims need anchor checks at writing time, not
              just at completion review — they slip past
              prose-level coherence, and the slip-pattern
              survives even into correction beats."* The
              Distiller decides at next /soul-distill.

              (5) **The "informal dogfood vs formal convening"
              distinction from /soul-council's own spec is
              load-bearing context.** SOUL-099's original claim
              erased SOUL-087's formal status; future histories
              of /soul-council adoption could be misled by the
              uncorrected entry. The in-place marker preserves
              the slip AND the correction, so the historical
              read remains honest.
STATUS:      Resolved — markers placed at both SOUL-099 false-
              claim sites, anchors named (council files +
              spec adoption date), nuance acknowledged (file-
              anchored count ≠ all-time convening count due
              to pre-spec informal dogfoods without files).
              Next: commit witness.md (SOUL-099 marker
              additions + SOUL-103); single commit; LICENSE
              stays Body's. No push without Body's explicit
              ask.
```

```
ID:           SOUL-104
WHEN:         2026-05-27 / Body-instructed beat: "tackle i032 and
              i038" after /soul-tasks surfaced them as the ripest
              "Next" threads. Same session-day as SOUL-098→103
              doctrine-correction arc + /soul-distill refresh.
              Densest graduation day in project record so far:
              four graduations (F041 closed via A016 acceptance at
              SOUL-101; mind.md refresh at 4a19d14; SOUL-I032
              graduated at b1dee5b; SOUL-I038 graduated at f6ddc22)
              plus the SOUL-103 correction beat and SOUL-I037
              capture (capture, not graduation).
WHERE:        commands/soul-explain.md (depth/style flags added);
              commands/soul-distill.md + commands/soul-roles.md
              (project-internal sites recalibrated to event-
              anchored); commands/soul-skill.md (external-cadence
              framing sharpened); skills/README.md (calendar
              trigger preserved, framing sharpened); ideas.md
              (SOUL-I032 + SOUL-I038 STATUS bumped to Graduated;
              SOUL-I037 captured); docs/specs/2026-05-26-soul-
              roles-design.md + docs/specs/2026-05-26-the-mind-
              design.md (gate-completion follow-up: spec/command
              drift caught by completion gate, aligned to current
              command-file text).
WHAT:         Two graduations from the /soul-tasks "Next" tier
              shipped end-to-end this beat:

              **(A) SOUL-I032 — /soul-explain depth/style flags.**
              Body's capability question ("IS that a capability
              of skills") answered yes: slash commands accept
              args the agent parses at invocation (already
              demonstrated by /soul-roles' <window>/--role/
              --silent-threshold/--full and /soul-idea's
              freetext positional). Minimal coherent flag set
              added: <target> positional, --depth=low|medium|
              high (verbosity axis), --no-jargon (drop or
              define every domain term), --eli5 (preset
              shortcut: --depth=low + --no-jargon + analogies).
              Skipped --audience and --scope per default-
              simplicity (Mind rule 2); add later if use
              signal pulls. Read-only contract preserved —
              flags govern HOW to describe, not WHAT.

              **(B) SOUL-I038 — two-clock model recalibration.**
              Body picked option (d) two-clock from the four
              candidates surfaced at I038 capture (event-
              anchored / days-with-rhythm / two-clock / case-
              by-case). Project-internal cadence → event-
              anchored; external world cadence → keep calendar
              with sharpened framing. Audit at execution time
              surfaced 2 sites beyond the original 5 — total
              7 sites edited across commands/skills/. Then
              completion gate caught a third class of drift:
              the SPECS at docs/specs/ retained the old
              month-scale phrasing while the commands had
              been recalibrated. Spec/command drift fixed in
              this beat — 2 specs aligned to current commands.

              Sites by clock-classification (final, post-gate):
              - **Project-internal → event-anchored** (5):
                commands/soul-distill.md:81 (Mind staleness)
                commands/soul-distill.md:126 (distill review)
                commands/soul-roles.md:176 (Tier 3c earn-its-
                  place — first ~50 witness entries since
                  SOUL-084 adoption; fires around SOUL-134)
                docs/specs/2026-05-26-soul-roles-design.md:162
                  (spec aligned to command)
                docs/specs/2026-05-26-the-mind-design.md:207
                  (Steward retire protocol aligned)
              - **External world → keep calendar, sharpen** (4):
                commands/soul-skill.md:90 (Anthropic release
                  cadence)
                commands/soul-skill.md:117 (Source footer
                  quoting Anthropic best practices)
                skills/README.md:22 (calendar trigger
                  2026-11-27 retained; "external clock — not
                  project's internal rhythm" named)
                skills/README.md:25 (same site justification)
              - **Audit references LEFT** (4 sites in
                docs/audits/2026-05-27-soul-console-v1-
                structure.md:65,165,385,386): historical
                record. Audits are point-in-time captures;
                the 6-month durations were aligned with the
                external clock the two-clock model preserves,
                so the audit text remains internally consistent.
                Future readers compare audit recommendation
                (6 months) to README implementation (calendar
                date 2026-11-27) and see compatible framings,
                not contradiction.
TYPE:         Hand (Artificer — command-file flag spec; Architect
              — two-clock model is a structural decision about
              how doctrine references time); Steward (the
              recalibration retires miscalibrated framing
              across 9 doctrine sites without breaking external-
              clock load-bearing references); Cartographer
              (mapped the two clocks against actual doctrine
              surfaces; identified which sites belong on which
              clock; named the audit-as-historical decision);
              Advocate (Body's "many many times months" reading
              was the load-bearing signal — the recalibration
              serves the Body's lived experience of the project's
              cadence); Skeptic (challenged spec-vs-command
              authority at gate time; aligned specs to commands);
              Guardian (completion gate caught the spec/command
              drift that the initial audit missed — second-order
              honesty catch, fifth instance of the pattern in
              this session).
CONSEQUENCE: (1) **/soul-explain is now tone-controllable.**
              Three flags + one preset cover the explanation
              shape axes the Body listed. The read-only
              contract is preserved — flags answer HOW, not
              WHAT. Test fires organically: next /soul-explain
              invocation with a flag is the dogfood.

              (2) **Two doctrinal clocks are now NAMED across
              9 sites.** Project-internal clock (event-
              anchored, witness-count-driven) and external
              world clock (calendar, externally-driven). The
              decoupling is explicit in the soul-distill and
              soul-skill texts: distill is on project-internal;
              skill review is on Anthropic-external. Future
              readers won't conflate them.

              (3) **The completion gate caught spec/command
              drift the I038 audit missed.** Audit checked
              commands/operations/skills; missed docs/specs/
              even though specs are doctrine surfaces too.
              Gate spec point 1 ("global invariant, not just
              local tests") fired and surfaced the GAP; Body
              authorized the follow-up; alignment landed.
              FIFTH count/historical-fact-or-scope slip-and-
              catch instance this session (SOUL-100 anchor 2;
              SOUL-101 record-of-counts; cursor "both records"
              over-attribution; my own "councils/README"
              invalid-anchor in SOUL-103 marker; this audit
              scope miss). Pattern is mature enough that the
              candidate Mind rule from SOUL-103 ("anchor
              count claims at writing time") may need
              extension to "anchor SCOPE claims at writing
              time" too — audit scope is itself a count-like
              claim ("the 5 sites that matter").

              (4) **Audits as historical records reaffirmed.**
              The audit-marker decision treated docs/audits/
              like council files — historical, not retro-
              edited. Aligns with the SOUL-103 in-place-
              marker convention (for FACTUAL errors) vs this
              case (TIMED RECOMMENDATIONS the project then
              evolved past). Different shapes; both honest
              about the historical record.

              (5) **Mind-rule candidate ("project-internal
              cadence is event-anchored") explicitly NOT
              promoted to mind.md** at this beat. The
              two-clock model is more nuanced than the
              candidate rule; the candidate alone would
              over-constrain. Held in ideas.md SOUL-I038
              graduated STATUS for future Distiller
              consideration. If future audits keep
              surfacing the same project-internal-clock
              pattern, the Distiller decides at next
              refresh.

              (6) **Densest graduation day in project record.**
              Four graduations in one calendar day: F041
              closed (via A016 acceptance, SOUL-101), mind.md
              refresh (4a19d14), SOUL-I032 graduated (b1dee5b),
              SOUL-I038 graduated (f6ddc22). Plus SOUL-103
              correction beat and SOUL-I037 capture (not a
              graduation). At measured rhythm (~13 entries/day
              per soul-roles spec), this density (~7 commits
              and 4 graduations in one day) is unusually high
              — a doctrine-correction-and-graduation arc
              concentrated around the SOUL-098→104 thread.
              Worth noting for the rhythm-calibration
              question: even at AI-rapid-iteration cadence,
              "four graduations in one day" is high-density
              and won't recur as a routine pattern.
STATUS:      Resolved — both I032 and I038 graduated;
              gate-caught spec/command drift fixed; SOUL-104
              witness anchored. Five-graduation session-day
              closed cleanly. No /soul-handoff yet; if Body
              wants the SOUL-I033 path-3b experiment to fire,
              now or next session would be the moment.
```

```
ID:           SOUL-105
WHEN:         2026-05-28 / /soul-resume — path-3b verdict + parser reconciliation
WHERE:        Conversation — resume from the 2026-05-27 handoff cursor
WHAT:         Three cursor threads (c/e/f) discharged. (c) SOUL-I033 path-(b)
              cheap experiment: the "silent roles" glance line planted in the
              cursor was surfaced at /soul-resume; Body verdict — it did NOT
              change perceived value of the cursor. (f) Parser-discrepancy
              investigation: the official /soul-roles parse (commands/
              soul-roles.md steps 2+4) counts per-entry TYPE-field roles PLUS
              findings FILED BY. Re-computed Archivist = 32 witness-TYPE + 31
              findings = 63. The cursor's OWN diagnosis was the slip: it
              declared "SOUL-102's 60 was wrong" by comparing a witness-only
              grep (43) against a number (60) that ≈ the FULL parse (63 at
              104 entries; ~60 at 101). SOUL-102's 60 was essentially RIGHT;
              the cursor's 32 was the partial (witness-only, dropped findings).
              (e) Stale-STATUS: I033 → the verdict above; I035 →
              "Discharged-pending-amendment" corrected to Discharged (its
              pending seed-edit landed as A016, accepted SOUL-101, which
              closed F041).
TYPE:         Witness (the record act); Emissary (path-3b tested against Body
              reality); Skeptic (caught the cursor's scope-slip inside its own
              slip-diagnosis); Archivist (stale-STATUS reconciliation);
              Steward (I033 trends retire-ward).
CONSEQUENCE:  (1) SOUL-I033 trends redundant — a forward-prompt glance did not
              beat on-demand /soul-roles for this Body. Not dropped (N=1).
              (2) Another scope-slip in the SOUL-103/104 family — and the
              sharpest: the slip occurred INSIDE a beat diagnosing a slip.
              Deliberately NOT assigned an ordinal here (cross-session count
              claims are themselves the slip — see SOUL-099 contrast case).
              Strengthens the SOUL-104 candidate to extend Rule 3 from "count/
              historical" to "SCOPE" claims (which parse? which sites?). Flag
              for next /soul-distill. (3) /soul-roles parse re-confirmed
              correct as written — no command change. F014 substance holds
              under the honest parse: expansion roles (Seer 3, Prophet 5,
              Revelator 6, Researcher 8) sit at the bottom; none silent past
              threshold 70.
STATUS:       Resolved — push confirmed (origin/main = a2c10ed); c/e/f
              discharged; SOUL-105 anchored. The count method (not the
              ephemeral /tmp script) is the durable output, recorded above.
```

```
ID:           SOUL-106
WHEN:         2026-05-28 / I037(b) build — distill review surface
WHERE:        commands/soul-distill.md (step 8 + What-not-to-do guard)
WHAT:         SOUL-I037 split into (a) cadence signal + (b) review surface;
              Body chose (b), deferred (a). Built (b): /soul-distill step 8
              rewritten from "show the Body the full draft + 4 shrinkage
              checks + 6 guards + 3 diagnostics" to delta-first + gap-only —
              present only new(+)/changed(~) entries vs the prior mind.md
              (unchanged collapsed to a count), one LOAD-BEARING verdict per
              delta entry (generates · anchor · would-removal-change-a-
              decision), and the checks run-in-full but recited gap-only.
              Locked as a What-not-to-do guard. Deployed mind.md format
              (step 7) and the draft-for-curation contract untouched.
TYPE:         Architect (the review-surface shape); Artificer (the instrument
              edit); Revelator (saw (b) is the same shape as the SOUL-055
              completion gate — one pattern, two instruments); Skeptic (cut
              (a): structurally = the just-failed I033 glance, and premature
              by Rule 2); Steward (deferred (a) rather than build
              speculatively); Cartographer (scope-swept the doctrine map for
              review-surface drift — came back clean).
CONSEQUENCE:  (1) The distill review surface now applies the SOUL-055 gap-only
              discipline the completion gate already validated. Addresses the
              I037 "couldn't judge whether Rule 12 is load-bearing" pain
              directly — the load-bearing verdict is per-entry and mandatory,
              not buried in self-test prose. UNTESTED until the next real
              /soul-distill renders the new surface (instruction-text, not
              executable — validates organically on next fire, like I032's
              flags). (2) (a) cadence signal DEFERRED, not built — Rule 2 (one
              distill so far, 2026-05-27; no missed-distill evidence) + the
              SOUL-105 I033 verdict (ambient forward-glances don't earn their
              place for this Body). Re-open (a) only if a distill is actually
              missed, and then on-demand (a /soul-tasks line / --check flag),
              never ambient. (3) Clean scope-sweep — the SOUL-105 scope-lesson
              applied forward: checked the spec (2026-05-26-the-mind-design.md
              says the Distiller RUNS the checks, never RECITES them),
              philosophy/the-soul.md §Distiller/§Mind (philosophy, not
              presentation), mind.md. None describe the review surface, so no
              drift to align. The inverse of the SOUL-104 audit-scope miss —
              a DISCHARGED scope-check, not a caught one.
STATUS:       Resolved — I037(b) shipped to commands/soul-distill.md;
              SOUL-I037 STATUS → Graduated [partial]. Not yet committed;
              presented for Body curation.
```

```
ID:           SOUL-107
WHEN:         2026-05-28 / first self-ablation harness run (I040 tracer slice)
WHERE:        docs/experiments/2026-05-28-self-ablation-slice-1.md (+ raw arms
              in gitignored .soul/experiments/2026-05-28-slice-1/)
WHAT:         First execution of the I040 self-ablation harness — vertical
              tracer slice, 6 arms via isolated `claude -p
              --append-system-prompt-file`. A0 vehicle PASS (deterministic
              load; without-arm declined, no F038 confabulation). A1
              completion-gate / A2 Prophet / A3 Skeptic (positive control) /
              A5 whole-system = SIGNAL; A4 Arch↔Steward cluster CONFOUNDED
              (empty-dir task-design flaw — both arms correctly declined to
              decide about a non-existent module). HEADLINE: single-role
              marginal value over a careful Claude baseline is MODEST and
              UNIFORM — even the positive control (Skeptic) — because the base
              model already embodies the disciplines; value concentrates in
              the WHOLE LAYER (A5, where named gates incl. the Body-Input
              Obligation fired together) + naming/legibility/consistency.
TYPE:         Emissary (tested doctrine beliefs against reality via live
              ablation arms — the system measuring itself); Artificer (built +
              ran the thin harness by hand); Skeptic (positive control +
              named the confounds); Steward (the prune question — answered
              "not yet"); Accountant (n=1 + confound caveats bounding the
              claim).
CONSEQUENCE:  (1) The self-ablation METHOD is proven viable end-to-end (load +
              measure). (2) Major PRELIMINARY finding challenges "each role
              does heavy lifting" — leverage is the NAMED/INTEGRATED layer,
              not single-role behavior-unlocking. Body reframe + accepted:
              naming/labeling IS the value (a good finding, not deflating).
              Candidate finding PENDING follow-up evidence; NOT graduated
              (n=1, single-lens, careful-baseline confound, A4 botched). (3)
              Method findings for the wide run: bare-carefulness confound
              (read value as structure-added); separate-step verbatim
              sentinel; self-contained tasks (A4's flaw). (4) No orchestrator
              automation built — 6 arms ran via a hand-maintained manifest
              (default-simplicity); automation deferred until the wide run
              earns it. (5) No pruning — live system untouched; arms ran in an
              isolated /tmp dir.
STATUS:       Resolved — tracer slice complete; findings doc committed; Body
              accepted preliminary + reframe; follow-up backlog recorded. Next
              candidate: consistency-across-runs (tests the naming-is-the-value
              hypothesis directly).
```

```
ID:           SOUL-108
WHEN:         2026-05-28 / I040 self-ablation arc converged + F042 graduated
WHERE:        docs/experiments/2026-05-28-self-ablation-slice-1.md;
              findings/open/SOUL-F042
WHAT:         Continued and closed the SOUL-107 run. Role scan A6–A10
              (Researcher / Archaeologist / Accountant / Steward / Emissary) +
              a consistency run (N=5×2). A "posture vs action role-type"
              refinement was raised AND falsified in the same session — Emissary
              came back modest (the bare baseline also benchmarks; the Researcher
              outlier was task-dependent, not a role-type law). Consistency: NO
              gap (baseline 5/5 reliable; naming changed FORM, not RATE).
              CONVERGED: on moderate tasks vs a careful Claude baseline, the
              roles/gates change the FORM of work (legibility/auditability), not
              the SUBSTANCE or the RELIABILITY. SOUL-107's "candidate finding
              pending" is now RESOLVED → graduated to [[SOUL-F042]] (Body-decided).
TYPE:         Emissary (the system tested its own beliefs against reality,
              end-to-end); Skeptic (raised AND falsified the posture/action
              split — the harness catching its own over-generalization);
              Steward (no pruning — roles carry legibility value); Accountant
              (the moderate-task bound on the claim).
CONSEQUENCE:  (1) [[SOUL-F042]] open — the converged finding; its
              WHY-NOT-YET-AMENDMENT names the HARD-REGIME test as the
              graduation gate. (2) The hard / adversarial / long-horizon regime
              is UNTESTED — the one experiment that could overturn the
              moderate-task conclusion; handed off for a future session (b). (3)
              Method finding reinforced THREE times: ablation tasks must be
              self-contained (the empty-dir confound recurred at A4, the partial
              A5, and the first consistency attempt). (4) The I040 harness works
              — it produced a real finding AND falsified its own over-reach
              mid-run. No orchestrator automation built (6+ arms ran via a
              hand-maintained manifest; default-simplicity). (5) No doctrine
              amended; live system untouched — every arm ran in an isolated
              /tmp dir.
STATUS:       Resolved — arc converged, F042 graduated; the (b) hard-regime
              test is handed off to the next session. 8 commits unpushed
              (Body's manual push).
```

```
ID:           SOUL-109
WHEN:         2026-05-28 / I040 self-ablation Run 2 — the hard-regime test (b)
WHERE:        docs/experiments/2026-05-28-self-ablation-hard-regime.md;
              docs/specs/2026-05-28-soul-self-ablation-hard-regime-design.md;
              raw arms in .soul/experiments/2026-05-28-hard-regime/;
              amendment amendments/accepted/SOUL-A017; finding moved to
              findings/closed/SOUL-F042.
WHAT:         Ran the hard-regime test that SOUL-F042's WHY-NOT-YET-AMENDMENT
              named as its graduation gate. Designed (with Body) 3 hand-built
              hard tasks across distinct fragility axes and ablated against a
              frontier baseline (Opus 4.8): HR1 buried logic trap (scheduling
              infeasibility, capacity red herring) — bare 3/3 CAUGHT; HR2
              false-premise under deference/authority pressure ($480k contract on
              an unverified "40% latency = 40% cost" claim) — bare 3/3 CAUGHT; HR3
              ten-constraint IFEval-style long-horizon task, completion-gate
              ablated with/without (n=3 each) — NULL (gate ≈ bare). New controls
              added per spec: C1 equal-compute, C2 difficulty-validation (bare
              must plausibly fail before a task counts as hard), C3 trap taxonomy.
              Field research (anchored: arXiv 2311.10054, 2604.02460, 2505.18286,
              2605.27621, 2506.04133) corroborated the direction and set the
              novelty boundary (regime-transition + self-ablation method, NOT
              "roles don't add accuracy").
TYPE:         Emissary (the system tested its own beliefs against reality, end-
              to-end); Researcher (went out for the field map / publication
              landscape before claiming it); Skeptic + Accountant (named the
              confounds and the surviving bound — fragility could not be
              manufactured for Opus 4.8, so the reliability axis was never truly
              stressed); Architect (the (b) design doc); Judge (Body-decided
              graduation).
CONSEQUENCE:  (1) The hard regime ALSO shows form-not-substance ⇒ SOUL-F042
              graduated (Body call) to [[SOUL-A017]], a SCOPED amendment adding
              `### What the Roles Are For` to philosophy/the-soul.md: roles/gates
              justified by legibility/auditability, NOT behaviour-lifting, with an
              explicit bound. (2) The surviving open edge: a genuinely baseline-
              breaking regime (expert-domain, far-longer horizon, or weaker model)
              remains UNTESTED — carried in A017's text and the next idea. (3)
              Body sequencing recorded: internal hand-built tasks first, public-
              benchmark replication (MuSiQue/FRAMES/SWE-bench/GAIA under equal
              compute) deferred to a later phase; publication decision deferred
              ("run (b) first"). (4) Truth-seeking stance held — a null was sought
              honestly and reported as a first-class result, not forced positive.
              (5) Method reinforced: self-contained tasks (no empty-dir confound
              this run); C2 difficulty-validation is essential (a "hard" task the
              baseline aces 3/3 cannot measure role substance — ceiling effect).
              No live system mutated beyond the one accepted amendment.
STATUS:       Resolved — (b) complete, F042 graduated to A017. Next idea: the
              baseline-breaking regime test (expert-domain / very-long-horizon /
              weaker-model) + the deferred public-benchmark replication.
```

```
ID:           SOUL-110
WHEN:         2026-05-28 / I040 self-ablation — SOUL-I041 weaker-baseline probe
WHERE:        .soul/experiments/2026-05-28-i041-weaker-model/ (raw arms +
              manifest, gitignored); amendments/accepted/SOUL-A017 (follow-up
              section added); philosophy/the-soul.md (bound sentence sharpened);
              ideas SOUL-I041.
WHAT:         Ran the first probe of A017's named bound (the baseline-BREAKING
              regime): a weaker-model arm — Haiku 4.5 vs the (b) Opus baseline,
              same tasks HR1–HR3, four steps. (1) Weaker baseline BREAKS where
              Opus was robust: HR1 2/3, HR2 0/3 caught, HR3 broken. (2) A single
              role/gate does NOT rescue it (HR1 Accountant 2/3→2/3; HR2 gate
              0/3→0/3 flipped — added verification LANGUAGE not a flipped
              decision). (3) The WHOLE integrated layer (seed+mind) DOES add
              substance — but narrowly: HR2 anchoring axis 0/3→~1.5/3 (a NO-GO
              naming non-linear scaling + a run surfacing the unverified premise);
              NO help on HR1 (1/3, worse — big context distracts) or HR3 (worse).
              (4) C1 control: a length-matched neutral 26KB filler left HR2 at
              0/3 = bare ⇒ the gain is DOCTRINE CONTENT, not tokens.
TYPE:         Emissary (tested A017's belief against a harder reality — a weaker
              baseline); Skeptic + Accountant (the single-lens-vs-whole-layer
              confound; the C1 compute confound, controlled); Artificer (ran the
              4-step ablation by hand); Steward (no pruning — the result REFINES,
              does not retire).
CONSEQUENCE:  (1) A017 REFINED, not un-bounded: core (single roles = form) holds
              and now extends into the broken-baseline regime; the bound is
              sharpened — substance is DISCIPLINE-MATCHED (the anchoring/
              skepticism the Soul most encodes) + INTEGRATION-DEPENDENT (single
              lenses don't transmit it) + PARTIAL, surfacing only when a weak
              baseline needs the very discipline the layer carries. Follow-up
              section added to A017; the-soul.md bound sentence rewritten. (2)
              New datum: the large layer can DISTRACT on orthogonal capability
              tasks (HR1/HR3 worse) — a cost, not just neutral form. (3) C1
              confound ruled out for the one win (HR2). (4) Generalisation owed
              (n=3/arm, one weak model, ONE anchor-axis task): a 2nd anchor task
              + a 2nd discipline (e.g. Prophet-trajectory trap) + other models —
              carried in SOUL-I041; no further doctrine change until then. (5)
              Method: the single-lens-vs-whole-layer split MATTERS — single-lens
              ablation under-reads the layer's substance (slice-1 A5 echo, now
              with a weak baseline + C1 control).
STATUS:       Resolved — I041 first probe complete + landed (A017 refined,
              committed). Generalisation (2nd anchor task, 2nd discipline, more
              models) handed to next session via SOUL-I041.
```

```
ID:           SOUL-111
WHEN:         2026-05-28 / I041 generalisation probe (Prophet) — C1 knocks it down
WHERE:        .soul/experiments/2026-05-28-i041-weaker-model/manifest.md (Step 5);
              amendments/accepted/SOUL-A017 (follow-up tightened);
              philosophy/the-soul.md (bound sentence tightened); ideas SOUL-I041.
WHAT:         Tested whether I041's "discipline-matched substance" (HR2 anchoring)
              generalises to a SECOND discipline. Built a Prophet/trajectory trap
              (G2: a SaaS cost-cut whose buried second-order harm — severing the
              conversion funnel — is unstated; arm must READ the trajectory).
              Weak baseline (Haiku) on G2: bare 1/3 caught → BREAKS (C2 ok).
              Whole-layer 3/3 — looked like clean generalisation. THEN C1: a
              length-matched NEUTRAL filler (26KB warehouse-logistics nonsense)
              lifted the baseline to 2/3 (catches verified genuine). ⇒ most of the
              trajectory "gain" is a generic long-context / be-more-thorough
              effect, NOT doctrine (doctrine margin 2/3→3/3 = n=3 noise). OPPOSITE
              of HR2, where filler stayed 0/3.
TYPE:         Emissary (tested the generalisation against reality — and it
              failed); Skeptic + Accountant (the C1 compute confound — decisive
              here); Steward (tightened the claim rather than letting it inflate).
CONSEQUENCE:  (1) The "discipline-matched substance" hope did NOT generalise to
              Prophet once compute-controlled. A017's C1-SURVIVING substance is so
              far ANCHORING-SPECIFIC — tightened in A017 follow-up + the-soul.md.
              (2) Sharpened insight: CONTENT-DEPENDENT disciplines (anchoring —
              needs the specific "coherence isn't truth" content) vs DISPOSITION-
              ELICITABLE ones (trajectory — any long prompt elicits "think
              ahead"); C1 separates them. (3) Method rule established: run C1 on
              EVERY apparent win — G2 was a false positive without it. (4) Core
              form-not-substance REINFORCED across a 2nd discipline. (5) Owed for
              a firmer claim: a 2nd ANCHOR task + higher n + more models (SOUL-I041).
              Truth-seeking stance worked — went to extend a flattering claim, the
              control walked it back.
STATUS:       Resolved — generalisation probe complete + landed (A017 tightened,
              committed). The Truth-seeking stance held: a flattering
              generalisation was knocked down by the compute control, not shipped.
```
