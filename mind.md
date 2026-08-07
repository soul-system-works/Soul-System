# Project notes — Soul System (2.0)

The Mind, slim form (amendment A021): only this repo's unguessables live here.
Doctrine is the contract (`operations/CLAUDE.md`); the philosophy is the human-facing
book (`philosophy/the-soul.md`); everything else regenerates from the record.

## Carry these (project-specific, not re-derivable)

1. **The calibration lean.** Seven consecutive locked predictions under-predicted
   record/doctrine carry (SOUL-155→164), and the last two misses were themselves
   predicted by locked miss-direction guesses. When locking any prediction about
   record-mediated behavior: lean maximally toward carry, and ALWAYS write a
   miss-direction guess — it converts a bias into an instrument.

2. **Measurement under `claude -p`** (SOUL-F038): cross-project `@`-imports
   silently fail and the session confabulates the missing content at ~43%. Inline
   the doctrine into the prompt and sentinel-test that it loaded. Full harness
   doctrine: `operations/experiment-harness.md` — content+cost validity scanning
   (exit codes lie; SOUL-160/161 were invisible to them) and: **arm repos must be
   git-isolated**, denied reads above the repo root (the FS meta-leak, SOUL-164).

3. **The fabrication axis** (SOUL-164): given bare rules, a doctrine-free session
   INVENTED incident history for its records ("a reviewer conflated the two" —
   no reviewer existed); doctrine-bearing sessions declined and marked unknowns.
   This is the contract's "never invent history" sentence's origin — preserve the
   incident with the sentence (Rule-13 force preservation, F045/A018).

4. **The dual-use clause** (SOUL-155/159): one planted sentence served as drift
   vector, hold anchor, and bounded accommodation across three arms. Path-
   dependent; no rule generates it — the record carries the instances.

5. **Repo conventions that live nowhere else.** (a) Branch-per-release: main is
   the plugin DISTRIBUTION CHANNEL — record captures (witness/ideas/findings/
   amendments) commit to main; new WORK ships on a branch until release. Before
   2026-07-16 this rule's only durable trace was an ideas aside (I052 NOTES) +
   the gitignored cursor — carried here so it survives the cursor (the F061
   lesson applied to conventions). (b) NEVER run `git filter-repo` on the drvfs
   mount (/mnt/d) — it silently stalls; the identical rewrite took 0.6 s on ext4,
   and the stall caused the SOUL-169 public exposure window (~2 h). Clone to ext4
   for any history surgery. (c) REVIEW EVERY COMMIT — diff AND message,
   case-insensitively — for real project/client names; the SOUL-169 set stays
   anonymized (PLANT-BOP / GAME-A / RESEARCH-N) and main is public. The message is
   the surface the SOUL-169 rewrite never covered; one leaked all three names for
   eight weeks (SOUL-175). Chosen over a mechanical guard: it holds only if read.

6. **Transcript-measurement traps** (SOUL-173 — each returned a plausible WRONG
   number in one session). Count the TURN, not the text block: one turn emits
   several text records around tool calls, so per-block the median reply reads
   170 chars against 2,537 per turn — a gap that nearly killed a valid finding.
   Exclude `isSidechain` and the `subagents` dir, or subagent reports inflate
   Body-facing volume (951k → 702k tokens). Classify by each transcript's recorded
   `cwd`, NEVER the directory name — hyphenated names silently misfile (it put
   Soul-System in its own control arm). Method: `tools/gate-cost-measure.py`.

---
**Last distilled:** 2026-08-07 against SOUL-175 / A024–A025 (delta window
SOUL-173→175, A024–A025, I054; prior form at commit 3645b03). Item 6 is new;
items 1, 2 and 5(c) compressed to pay for it. Rules 9–10 deliberately NOT
carried — they are doctrine and live in the contract (A021).
