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
STATUS:          Resolved — RE-DISCOVERY of SOUL-035, not a new architectural
                 defect. See RESOLUTION below and witness SOUL-072.

RESOLUTION:      Settled 2026-05-26 by Architect + Skeptic per the F028 anchor-
                 validity discipline. The original F036 evidence came from a
                 session started 2026-05-22 (per .soul/handoff.md "Long resume
                 from the prior 2026-05-22 cursor"). The `@mind.md` line was
                 added to root CLAUDE.md at 2026-05-26 10:25:43 (commit 05eabc1)
                 — mid-session, 4 days after that session started. Per
                 [[SOUL-035]] ("the CLAUDE.md system-reminder is snapshotted at
                 the PARENT session's start … and inherited by every subagent;
                 it does not refresh on a file change"), the May 22 snapshot
                 captured only `@operations/CLAUDE.md`, and the subagents in
                 Tier 3a inherited that stale snapshot — fully explaining the
                 observed evidence without invoking any new harness behavior.

                 Clean-room confirmation (witness SOUL-072): a diagnostic
                 subagent spawned from a fresh session started AFTER 05eabc1
                 reports the full Mind content inlined in its CLAUDE.md system
                 reminder — both `@operations/CLAUDE.md` and `@mind.md` resolve
                 and propagate. Distinctive Mind markers (Rule 4 generation-
                 couples-retirement, Rule 9 symlinks, Tensions section
                 "Default-simplicity ↔ outward-reach") were directly visible.

                 The Mind's "always-on at the project layer" claim therefore
                 HOLDS for any session started after the `@mind.md` import is
                 in place. The operational caveat is the same as for ANY
                 CLAUDE.md change: the session in which the file is modified
                 sees a stale snapshot; subsequent sessions are clean. This is
                 already documented doctrine via SOUL-035.

                 Disposition of the four candidate fix paths in WHY NOT YET
                 AMENDMENT above:
                 (a) Manual injection — unnecessary for the steady state;
                     workaround only for the in-session-deployment edge case.
                 (b) Move `@mind.md` inside seed — REJECTED (layering violation,
                     and unnecessary now that the gap is shown to not exist).
                 (c) Wait for harness — unnecessary; current behavior is fine.
                 (d) Narrow the Mind's value claim — REJECTED as a permanent
                     narrowing; the claim was correct. A one-line operational
                     note ("after deploying or modifying the Mind, restart the
                     session for it to reach this session and its subagents")
                     belongs near the deployment doctrine — already implicit
                     via SOUL-035; possibly worth surfacing in the Mind spec
                     §Deployment as a courtesy note.

                 RESIDUAL: A Distiller-tier candidate contrast case for mind.md
                 — "F036 vs SOUL-035: apparent architectural defect vs known
                 stale-snapshot mechanism. Disambiguating rule: when a CLAUDE.md
                 change appears not to take effect, FIRST anchor when the parent
                 session started relative to the change (F028 timing discipline)
                 before declaring it architectural." Defer to next `/soul-distill`.
```
