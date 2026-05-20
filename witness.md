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
