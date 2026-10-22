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
   re-check it at the source; then have a fresh-context reviewer read it. It fired
   three more times on 2026-10-21 alone — probe arms named "Comparator", the asking
   standard, "31 sessions" for 66 — each caught at the source (SOUL-213/214).

3. **Measurement under `claude -p`** (SOUL-F038, SOUL-190): `@`-imports from outside
   the project do not reliably load, and a session confabulates the missing content
   (~43% cross-project). Even the home-relative import `/soul-init` writes answered
   NO-CONTRACT 3/3. Inline the contract (`--append-system-prompt-file`; in
   `claude plugin eval`, `append_system_prompt`, kept current by
   `evals/sync-contract.py`) and sentinel-test that it loaded. Harness doctrine:
   `operations/experiment-harness.md` — exit codes lie (SOUL-160/161); **arm repos
   must be git-isolated**, reads above the repo root denied (SOUL-164). Under
   subscription auth `--bare` is unavailable, and `--setting-sources project` STILL
   loads `~/.claude/CLAUDE.md` and per-arm auto-memory: pass `--settings` with
   `claudeMdExcludes` and `"autoMemoryEnabled": false`, and prove it with a leak
   sentinel (two global-only lines asked verbatim) — both controls leaked without
   it (soul-benchmark 2026-10-21 RESULT-phase0-isolation, SOUL-210).

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

8. **What Soul measurably does on current models — design tests on that.** Chain
   quality ties at ceiling, the five-minute floor file included (June; 2026-10-21,
   11/11 at every planted cell; v3 2/2). Measured differences: cost — Soul is cheaper
   than the long Comparator on every multi-step chain, but the floor is cheaper than
   Soul, and Soul is dearer on single sessions (SOUL-213/214); and handing the owner
   the call only at chain R's judgment step on Sonnet (3/3 vs 0/4). On the stale-rule
   quiz, scored to one standard, a careful CLAUDE.md asked first 5/5 and Soul 2/5 (v2
   and v3) — this is NOT Soul's edge; the earlier "10/10 vs 0/5" was looser scoring
   against a bare note (SOUL-214). Any grade that favours an arm gets a second blind
   scorer before it is reported: both 2026-10-21 false-done flags dissolved on the
   second read. Headless plugin arms measure "installed", not "used", unless the
   prompt names the practice; then the skills fired 12/12, and Pocock's `tdd` stops
   for the owner (SOUL-211).

9. **A probe that runs git here can damage this repo.** During the secret-guard
   reviews a probe's `cd` failed and it ran in Soul-System: it committed a file `y`
   (ed5d305, never pushed) and wrote a `.git/hooks/pre-commit` that failed every
   commit; the reviewer's own undo was refused and the Body ran it (SOUL-207). Any
   brief that runs git or hook probes requires `cd <dir> || exit 1` on every `cd`
   and ends by checking that HEAD and `.git/hooks` here are unchanged.

10. **Read what each arm actually received; score every arm to one standard.** Two
    plausible wrong headlines in one day (SOUL-213/214): the campaign's probe
    "Comparator" cells carried only a 25–43-word project note (`run-probe.sh` copies
    the note alone), and "Soul asks 5/5" came from round-2 scorers counting
    conditional handovers that a second pair, grading all arms to one standard,
    scored 2/5. Before naming an arm in prose, read the runner script; before
    comparing two arms' grades, have the same scorers grade both in one pass.

---
**Last distilled:** 2026-10-22 against SOUL-214 / A029 / F074 / v3.1.0 (delta window
SOUL-212→214, I071–I080, v3.0–v3.1; prior form at commit 77a70a1). Changed: item 8
(the asking claim withdrawn, the floor's tie and cost added) and item 2 (three new
instances). New: item 10. Nothing cut. Rules 9–10 still NOT carried (doctrine).
