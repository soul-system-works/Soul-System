```
FINDING ID:      SOUL-F038
DATE:            2026-05-26
WITNESS IDS:     SOUL-075 (initial detection — Q1 v1 sentinel caught a
                 fabricated "Rule 9" about distillation cadence when the real
                 Rule 9 is about symlinks); SOUL-076 (--append-system-prompt-
                 file workaround confirmed by Q2's absence-of-recurrence);
                 SOUL-077 (scope-probe results — N=7 replication established
                 INTERMITTENT failure rate ~43% under the failure topology,
                 not deterministic; plus probes 1/3/4 bounding which
                 topologies are affected).
WHAT:            `@-imports` of absolute paths from a CLAUDE.md OUTSIDE a
                 project (e.g. `/tmp/soul-experiment/mind-on/CLAUDE.md`
                 containing `@/mnt/d/Projects/Soul-System/mind.md`)
                 INTERMITTENTLY fail to resolve under `claude -p` auto-
                 discovery — measured ~43% failure rate (3 confabulations
                 in 7 runs) under the failure topology
                 (cwd in `/tmp/...` + cross-project absolute @-import +
                 `--add-dir` on target + `-p`). When the import does NOT
                 resolve, the agent reads the @-line as raw text
                 (recognises "mind.md is referenced") but the file's CONTENT
                 doesn't load — and the agent then CONFABULATES plausible-
                 sounding Soul-shaped content. The three observed
                 confabulations were each DIFFERENT plausible rules
                 ("Distillation cadence is Body-judged"; "Pre-completion
                 verification is a gate" — cited F012 + /soul-verify by name;
                 "Reuse before invention"), demonstrating that the failure
                 cannot be detected by content-shape pattern matching —
                 confabulations look like real rules. The 4/7 correct runs
                 quoted Rule 9 VERBATIM, indicating the import DID load in
                 those runs. The fix `--append-system-prompt-file <path>`
                 delivers raw file content into the system prompt
                 deterministically (verified by Q1 v2 + Q2 sentinels and
                 all subsequent uses — no recurrence observed).

                 The worst combination is confirmed: intermittent failure +
                 confabulation that passes casual review. More alarming than
                 deterministic failure, not less, because a successful run
                 under this topology cannot be assumed reliable from a
                 single sample.

                 This is SOUL-meta: any experiment harness (SOUL-I011) that
                 wants to vary CLAUDE.md content per arm via @-imports
                 across repo boundaries will produce mostly-clean runs with
                 occasional silently-fake-Mind arms — INDISTINGUISHABLE from
                 success without a sentinel test on every arm.

                 What SHOULD be: either cross-project @-imports resolve
                 deterministically, or failure surfaces an error. What IS:
                 stochastic resolution + confabulation when resolution fails.

SCOPE BOUNDED:   Probe results (SOUL-077, 2026-05-26):
                 - Probe 1 (in-project relative @-imports under `-p`): N=1,
                   SUCCESS. Not exhaustively replicated; may also be
                   intermittent but the canonical case.
                 - Probe 2 (cross-project @-imports under INTERACTIVE
                   `claude`, no -p): N=3, SUCCESS (Body-run 2026-05-26).
                   No confabulation observed. Bounds F038 as `-p`-specific
                   at the small N=3 level.
                 - Probe 3 (cross-project + `--add-dir` + `-p`): N=7 with
                   Q1 v1 + replays. 4/7 correct, 3/7 confabulation. This is
                   the failure-topology evidence. Point estimate ~43%
                   confabulation; binomial 95% CI wide (~10-80% at N=7).
                 - Probe 4 (subagent inheritance from post-05eabc1 session):
                   N=1, SUCCESS. Confirms F036 closure independently.

WHY NOT YET AMENDMENT:  Scope now bounded across all 4 probes. The
                 DOCTRINAL FIX is clear, actionable, and narrowed to `-p`:
                 "under `claude -p`, never rely on cross-project @-imports
                 for measurement; always inline via
                 `--append-system-prompt-file`, and always sentinel-test
                 import loading before trusting an experiment arm.
                 Interactive `claude` sessions appear reliable at small N
                 (Probe 2: 3/3); the failure is `-p`-specific so far."

                 Ready for amendment review. Two amendment shapes for
                 Body to choose between: (a) operations-level rule in a
                 measurement-method or experiment-harness doc, lightest
                 footprint; (b) a finding-derived line in the Mind /
                 the seed about CLAUDE.md import topology under -p,
                 heavier footprint but loads always-on.

                 The METHODOLOGICAL fix (F028 anchor-validity applied to
                 the loading itself, not just the user-facing claim) is
                 already standing practice from this arc — every
                 `--append-system-prompt-file` run has been sentinel-tested.

                 Residual: N=7 magnitude is point-estimate-only (binomial
                 95% CI ~10-80%); direction (intermittent, not zero) is
                 clear, rate is not. Future runs of the failure topology
                 would tighten the estimate.

FILED BY:        Skeptic (designed the sentinel that exposed the silent
                 failure); Guardian (F028 anchor-validity discipline
                 applied to the experiment's own evidence — third
                 instance in two arcs); Emissary (the run-against-reality
                 that surfaced the gap, then N=7 replication);
                 Artificer (`--append-system-prompt-file` workaround).
                 Cartographer (cluster pass surfacing the bounded scope;
                 prompted the replication that distinguished hypothesis A
                 from B).
RELATED:         [[SOUL-I011]] (experiment harness — this finding directly
                 shapes its substrate); [[SOUL-F028]] (anchor-validity —
                 the discipline that caught the confabulation, AND now has
                 quantitative justification: 43% failure rate makes
                 sentinel-testing non-optional for any @-import-based
                 harness); [[SOUL-F036]] (closed: Mind-doesn't-reach-
                 subagents — same failure family of "CLAUDE.md imports
                 don't always propagate the way doctrine assumes"; F036
                 was about subagent snapshot timing, F038 is about
                 cross-project cwd-anchored resolution under -p);
                 [[SOUL-I005]] (token economics — the broader claim this
                 experiment serves); [[SOUL-075]], [[SOUL-076]],
                 [[SOUL-077]] (witness anchors).
STATUS:          Closed — codified as SOUL-A013 (2026-05-26). Discipline lives
                 in operations/experiment-harness.md (rule + sentinel recipe +
                 worked example); seed pointer added at §The Mandatory Gates
                 "Before calling anything complete." N=7 magnitude residual
                 (binomial 95% CI wide) remains for future tightening; does
                 not affect the discipline itself.
```
