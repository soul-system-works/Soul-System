```
FINDING ID:      SOUL-F036
DATE:            2026-05-26
WITNESS IDS:     SOUL-068 (Mind MVP shipped); SOUL-070-pending (Tier 3a diagnostic
                 + re-test arc). The Mind MVP shipped with the architectural claim
                 "always-on at the project layer" via `@mind.md` in the project
                 root CLAUDE.md. Tier 3a's first A/B (six subagents on three
                 held-out questions) surfaced a self-report from one Arm B
                 subagent: "the seed I was given does not contain a `@mind.md`
                 import directive — only `@operations/CLAUDE.md`. So mind.md may
                 not actually be loaded." A direct diagnostic subagent confirmed
                 it (instructed not to read any files, only introspect): saw the
                 project CLAUDE.md as a single line `@operations/CLAUDE.md`, the
                 seed inlined, but NO mind.md content present. File on disk
                 verified separately: root CLAUDE.md contains both
                 `@operations/CLAUDE.md` AND `@mind.md` (commit 05eabc1).
WHAT:            The Mind's "always-on at the project layer" claim holds for the
                 PARENT SESSION but fails for AGENT-TOOL-SPAWNED SUBAGENTS in
                 current Claude Code harness behavior. Subagents inherit the
                 project's root CLAUDE.md content as snapshotted/processed by the
                 harness, and in observed behavior only the FIRST @-import line
                 propagates — `@operations/CLAUDE.md` (the seed) is inlined,
                 `@mind.md` is not. The cause cannot be distinguished from inside
                 the subagent (snapshot-at-session-start vs first-import-only vs
                 some other resolution rule), but the observed effect is the
                 same: the deployed `mind.md` does NOT reach subagent context.

                 Practical consequences:
                 (1) Tier 3a's first A/B effectively tested "seed alone" vs
                     "seed + full record" — not "seed + Mind" vs "seed + full
                     record" as designed. The Mind's value claim remains
                     unmeasured from that round.
                 (2) Any Council/Distiller/Skeptic work delegated to subagents
                     operates without the project's distilled rules. The Mind
                     benefits only the parent session's reasoning.
                 (3) The spec's lens-layer architecture (`seed → Mind → records`)
                     is only realized in the parent session; subagents see only
                     `seed → records`.

WHY NOT YET AMENDMENT:  Architectural defect with multiple candidate fixes; needs
                 evidence to choose. Candidate paths:
                 (a) Parent session explicitly injects mind.md content into every
                     Agent prompt (workaround at the call site — manual but works
                     today; what the re-test in this finding's witness will use).
                 (b) Move `@mind.md` inside `operations/CLAUDE.md` so it
                     propagates with the seed (architectural — but mixes universal
                     seed with project-specific Mind, violating the layering).
                 (c) Wait for / request harness behavior that follows ALL root
                     CLAUDE.md @-imports recursively (out of the Soul System's
                     direct control).
                 (d) Accept the gap and revise the Mind's value claim to
                     "always-on for the parent session only" — narrower but
                     honest.
                 Decision needs the re-test evidence (does the Mind, when
                 explicitly fed, actually change subagent reasoning vs seed
                 alone?) before picking a path.

FILED BY:        Emissary (subagent self-report surfaced the suspicion) +
                 Skeptic (Body pushed back on accepting partial validation) +
                 Guardian (the test's anchor existed but its validity was the
                 question — F028 discipline applied to a test result, not a
                 product claim).
RELATED:         [[SOUL-I026]] (The Mind — the architectural claim this challenges),
                 [[SOUL-068]] (Mind MVP shipped with this claim unmeasured at the
                 subagent boundary), [[SOUL-033]] (subagent @-import inheritance
                 evidence — but for imports FROM the seed, not the project root —
                 may explain the gap: only seed-level imports propagate),
                 [[SOUL-F028]] (anchor validity not just existence — applied here
                 to the Tier 3a test result itself), [[SOUL-F014]] (activation
                 gap family — the Mind has a parallel activation problem: present
                 in doctrine + deployed on disk, but doesn't fire where intended),
                 docs/specs/2026-05-26-the-mind-design.md (the spec whose
                 architecture claim this challenges).
STATUS:          Open — operational. Re-test in progress with explicit mind.md
                 feed to subagent prompts (workaround path (a) above) to settle
                 whether the Mind adds value when actually present. The
                 architectural fix (which path of a-d) decides after that evidence.
```
