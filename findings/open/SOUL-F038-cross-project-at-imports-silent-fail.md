```
FINDING ID:      SOUL-F038
DATE:            2026-05-26
WITNESS IDS:     SOUL-075 (caught en route during Q1 v1 sentinel verification —
                 Mind-on arm CLAIMED mind.md was in context and quoted a
                 FABRICATED "Rule 9" about distillation cadence when the real
                 Rule 9 is about symlinks); SOUL-076 (Q2 ran with the
                 --append-system-prompt-file workaround from the start, anchoring
                 the fix by absence-of-recurrence).
WHAT:            `@-imports` of absolute paths from a CLAUDE.md OUTSIDE a project
                 (e.g. `/tmp/soul-experiment/mind-on/CLAUDE.md` containing
                 `@/mnt/d/Projects/Soul-System/mind.md`) silently fail to resolve
                 under `claude -p` auto-discovery. The agent reads the @-line as
                 RAW TEXT — recognising "mind.md is referenced" — but the imported
                 file's CONTENT never loads into context. The agent then
                 confabulates plausible-sounding content when asked to quote from
                 the "loaded" file (Q1 v1: fabricated a "Rule 9" about
                 distillation cadence — coherent, Soul-shaped, false). The fix is
                 `--append-system-prompt-file <path>` which delivers raw file
                 content into the system prompt reliably (verified by Q1 v2 and
                 Q2 sentinels). This is SOUL-meta: any experiment harness
                 (SOUL-I011) that wants to vary CLAUDE.md content per arm via
                 @-imports across repo boundaries will silently produce
                 Mind-off-vs-Mind-off runs and call them Mind-on-vs-Mind-off.
                 What SHOULD be: either cross-project @-imports resolve (so the
                 obvious harness design works) or the failure surfaces an error
                 (so it can't masquerade as success). What IS: silent failure
                 plus model confabulation — the worst combination.
WHY NOT YET AMENDMENT:  Scope unbounded. We've verified the failure under exactly
                 ONE topology: `claude -p` with auto-discovered CLAUDE.md from a
                 `/tmp/...` cwd, importing files inside a different project root.
                 Unknown: (a) interactive `claude` sessions — do they resolve the
                 same imports? (b) `claude -p` with the imports staying INSIDE
                 the project root — does relative-path import work where absolute
                 doesn't? (c) what about `--add-dir` on the import target's
                 project — does that change resolution? (d) does subagent
                 inheritance behave the same way as parent-snapshot loading? An
                 amendment would either tighten doctrine ("never rely on
                 cross-project @-imports for measurement; always inline via
                 `--append-system-prompt-file`") or change the harness design
                 (SOUL-I011 spec). Either move wants the scope known first. 1–2
                 more targeted probes would close it.
FILED BY:        Skeptic (designed the sentinel that exposed the silent failure);
                 Guardian (F028 anchor-validity discipline applied to the
                 experiment's own evidence — third instance in two arcs);
                 Emissary (the run-against-reality that surfaced the gap);
                 Artificer (`--append-system-prompt-file` workaround).
RELATED:         [[SOUL-I011]] (experiment harness — this finding directly shapes
                 its substrate); [[SOUL-F028]] (anchor-validity — the discipline
                 that caught the confabulation); [[SOUL-F036]] (closed: Mind-
                 doesn't-reach-subagents — same failure family of "CLAUDE.md
                 imports don't always propagate the way doctrine assumes"; F036
                 was about subagent snapshot timing, F038 is about cross-project
                 cwd-anchored resolution); [[SOUL-I005]] (token economics — the
                 broader claim this experiment serves); [[SOUL-075]], [[SOUL-076]]
                 (witness anchors).
STATUS:          Open
```
