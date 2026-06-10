# The Experiment Harness Discipline

How to run measurement experiments — A/B comparisons, sentinel-driven
verification, any `claude -p` invocation that depends on prompt content — without
getting silently fooled by a half-loaded context.

The Soul already requires *"verify the invariant the whole must satisfy"* and
*"any claim about reality needs an external anchor proportionate to its weight"*.
This file does not add an obligation. It names the **specific failure mode** that
defeats those obligations during measurement work, and the **specific recipe**
that survives it.

---

## Why it exists

`@-imports` inside a `CLAUDE.md` look deterministic — they read like file
includes. They are not, under `claude -p`. SOUL-F038 measured a ~43% silent
failure rate (3 confabulations in 7 runs) for the **failure topology**: working
directory in `/tmp/...`, cross-project absolute `@-import`, `--add-dir` on
target, `-p` mode. When the import does not resolve, the agent reads the
`@`-line as raw text (recognises that a file is *referenced*) but the file's
**content** never loads — and the agent **confabulates** plausible-sounding
content as if it had. The three observed confabulations were each *different*
plausible rules; the failure cannot be detected by content-shape pattern
matching.

The worst combination is confirmed: intermittent failure + confabulation that
passes casual review. More alarming than deterministic failure, not less,
because a single successful run under this topology cannot be assumed reliable.

Interactive `claude` sessions (no `-p`) appear reliable at small N (Probe 2 in
SOUL-F038: 3/3 success). The failure is `-p`-specific so far.

---

## The rule

**Under `claude -p`, never rely on cross-project `@-imports` for measurement.**

Two parts, both mandatory:

1. **Inline content via `--append-system-prompt-file <path>`** instead of
   `@-import`. This Claude Code flag delivers the file's raw bytes into the
   system prompt deterministically. No path-resolution magic, no auto-discovery,
   no cross-project ambiguity.

2. **Sentinel-test import loading on every arm**, before trusting any result.
   A sentinel is a short, specific question whose correct answer can ONLY come
   from the file's actual content — typically "quote a specific known line
   verbatim." A confabulation that re-phrases the line is a failure; the
   sentinel demands verbatim. If the sentinel fails, the arm is discarded; the
   measurement is not run against a half-loaded context.

The methodological discipline is F028 anchor-validity applied to the loading
itself, not just to the user-facing claim — verify what loaded before
verifying what the loaded content produced.

Three additions from the v1.0 evaluation study (SOUL-155/156, A019):

3. **Assert the executor exists before any quality gate runs.** A missing
   toolchain once produced eight asserted-but-never-run build+test checks —
   `bash -n` passes, `command -v` was never asked. Verify the verifier.

4. **Arm validity is judged from artifact CONTENT, never exit codes.** A
   session-limit storm stubbed 33 arms while every sweep exited 0. Check
   `is_error` fields, sizes, and sentinel presence; an exit code is not an
   anchor.

5. **Sentinels go MID-output, not output-first.** Frontier models override
   format-first instructions with sandbox-honesty disclosures ("the working
   directory is empty…") — 9/40 Opus arms failed an open-with-quote sentinel
   while demonstrably carrying the content. Ask for the quote after the work,
   or score sentinel-fails by content inspection before discarding.

---

## When it fires

- Any measurement experiment using `claude -p` with prompt content that includes
  imports, references, or context files.
- Any A/B comparison where the arms differ by what's loaded.
- Any harness invocation where the cost of a silently-fake arm is the entire
  measurement (which is most of them — a fake arm doesn't fail loudly).

## When it does not fire

- Ordinary interactive Soul sessions (no `-p`). Probe 2 shows 3/3 reliability
  at small N; future evidence may sharpen this bound.
- Single-file prompts with no imports — nothing to silently fail.
- Work that does not depend on which content loaded (rare in measurement; common
  outside it).

---

## Failure modes this prevents

| Mode | What goes wrong without the rule |
|---|---|
| **Silent half-load** | `@-import` fails to resolve; agent reads the `@`-line as raw text without loading content. Looks identical to success at output level. |
| **Confabulation under load-failure** | Agent generates plausible-sounding rules that look like the missing file's contents. Three observed confabulations in F038 were each different, ruling out detection by content-shape. |
| **Anchor-citation camouflage** | One observed confabulation cited `SOUL-F012` and `/soul-verify` by name — confabulations can wear Soul-System anchors as authentic dressing. Anchor citation is not evidence the cited content loaded. |
| **Result-pollution at the headline** | A single half-loaded arm in a multi-arm experiment poisons the headline; without sentinels, the arm is indistinguishable from a successful one. |

---

## Sentinel pattern (worked example)

For an experiment comparing Mind-on vs Mind-off arms:

1. Pick a specific identifiable line from `mind.md` that the arm should know
   (e.g. a particular rule number plus its first six words).
2. Add a sentinel question at the start of the arm's prompt:
   *"Quote rule N from the Mind verbatim."*
3. Inline the Mind via `--append-system-prompt-file mind.md` on the Mind-on
   arm.
4. Compare the arm's first turn output against the verbatim line.
5. **If verbatim:** loading succeeded; arm is valid; proceed with the
   measurement.
6. **If paraphrased or different:** loading failed; arm is invalid; discard
   the run, do not include in results.
7. The Mind-off arm uses the same sentinel but expects the agent to say it
   cannot quote — a paraphrase from an unloaded Mind-off arm is also a failure
   indicator (confabulation from no source).

Sentinel cost: one extra turn per arm. Measurement integrity: complete coverage
of the silent-failure mode F038 named.

---

**Source:** Built from SOUL-F038 (cross-project @-imports silent fail under -p)
in its bounded form (SOUL-077: Probe 2 interactive 3/3 clean; Probe 3 -p
topology 4/7 with 3/7 confabulation). The `--append-system-prompt-file`
workaround was discovered by the Artificer in the same arc and verified across
all subsequent measurement runs. **Adopted:** 2026-05-26 (as part of the F038
amendment, landed as A1 — operations-level rule rather than seed/Mind line, per
default-simplicity and the always-on token budget discipline in Mind rule 5).
**Status:** active. **Open question:** rate point-estimate is binomial-95%-CI
wide at N=7 (~10–80%); direction is clear, magnitude is not. Future runs of
the failure topology would tighten the estimate.
