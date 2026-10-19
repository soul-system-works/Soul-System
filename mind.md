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

2. **The same lean, on reports of finished work: counts come out generous.** Each
   release row from 2.1.1 to 2.3.2 records a confident number about its own work
   that was wrong in the flattering direction — "six of six" (five), "nineteen
   projects" (one depth-2 sweep), 18/47 misfiled (12/47), F070's four instances
   reaching the owner (two) — and fresh-context review, not the author, caught each.
   Before writing a count or "verified" about work just done, name its scope and
   re-check it at the source; then have a fresh-context reviewer read it.

3. **Measurement under `claude -p`** (SOUL-F038, SOUL-190): `@`-imports from outside
   the project do not reliably load, and a session confabulates the missing content
   (~43% cross-project). Even the home-relative import `/soul-init` writes answered
   NO-CONTRACT 3/3. Inline the contract (`--append-system-prompt-file`; in
   `claude plugin eval`, `append_system_prompt`, kept current by
   `evals/sync-contract.py`) and sentinel-test that it loaded. Harness doctrine:
   `operations/experiment-harness.md` — exit codes lie (SOUL-160/161); **arm repos
   must be git-isolated**, reads above the repo root denied (SOUL-164).

4. **The fabrication axis** (SOUL-164): given bare rules, a doctrine-free session
   INVENTED incident history for its records ("a reviewer conflated the two" —
   no reviewer existed); doctrine-bearing sessions declined and marked unknowns.
   This is the contract's "never invent history" sentence's origin — preserve the
   incident with the sentence (Rule-13 force preservation, F045/A018).

5. **Zero gate fires is not a broken gate.** On current models the completion
   gate's claim regex almost never matches a natural closing line — 0/10 Opus
   headless runs (SOUL-189), 0/4 Sonnet eval runs (SOUL-192) — because replies end
   "— Bottom line: … verified". Do NOT broaden the regex to make it fire: the
   word-presence version fired on every turn (F063) and a bare-word scope match
   voided an endpoint (SOUL-160). `evals/gate-fires` is the proof it fires (SOUL-193).

6. **Repo conventions that live nowhere else.** (a) Branch-per-release: main is
   the plugin DISTRIBUTION CHANNEL — record captures (witness/ideas/findings/
   amendments) commit to main; new WORK ships on a branch until release.
   (b) NEVER run `git filter-repo` on the drvfs mount (/mnt/d) — it silently
   stalls; the identical rewrite took 0.6 s on ext4, and the stall caused the
   SOUL-169 public exposure window (~2 h). Clone to ext4 for any history surgery.
   (c) Before EVERY push, scan the diff AND every commit message,
   case-insensitively, against column 2 of the gitignored
   `registry/NAME-MAP.md`; main is public and adopting projects appear only as
   codenames (PLANT-BOP, ROUTER-LAB). The message is the surface the SOUL-169
   rewrite never covered; one leaked all three names for eight weeks (SOUL-175).
   (d) **A ref-scan CANNOT verify a redaction.** Unreachable is not deleted:
   GitHub serves unreachable objects by SHA indefinitely and says so, so no
   refs-only move removes one — not force-push, not branch deletion, not an
   orphan root. Only deleting the repository (or a Support gc request) empties
   the object store. Verify BOTH ways or not at all: a fresh clone scanned across
   every revision, message and tag object, AND a fetch-by-SHA probe of the
   known-bad commits decided on OBJECT PRESENCE with a passing control — never a
   piped exit code, which reported "fetchable" by testing `head`. SOUL-175
   recorded three SHAs as unfetchable; all three still fetched three months
   later, and its local tag re-adoption had not taken either (SOUL-178).

7. **Transcript-measurement traps** (SOUL-173 — each returned a plausible WRONG
   number in one session). Count the TURN, not the text block: one turn emits
   several text records around tool calls, so per-block the median reply reads
   170 chars against 2,537 per turn — a gap that nearly killed a valid finding.
   Exclude `isSidechain` and the `subagents` dir, or subagent reports inflate
   Body-facing volume (951k → 702k tokens). Classify by each transcript's recorded
   `cwd`, NEVER the directory name — hyphenated names silently misfile (it put
   Soul-System in its own control arm). Method: `tools/gate-cost-measure.py`.

---
**Last distilled:** 2026-10-19 against SOUL-197 / A026 / F073 (delta window
SOUL-176→197, F064–F073, A026, I055–I066; prior form at commit ed46727). New: items
2 and 5; item 3 gains SOUL-190. Cut to pay: the dual-use clause (SOUL-155/159) — it
described instances and generated no decision. Rules 9–10 still NOT carried (doctrine).
