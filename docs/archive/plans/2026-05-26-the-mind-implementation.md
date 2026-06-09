# The Mind / `/soul-distill` MVP — Implementation Plan

> **For agentic workers:** Execute task-by-task. Steps use checkbox (`- [ ]`) syntax. Verifications adapted from TDD: this is a markdown/spec/symlink build, not code — verifications use `grep`/`wc`/`ls`/structure checks against the artifacts.

**Goal:** Ship the MVP of The Mind — a project-scoped, always-on, compressed-rules artifact (`mind.md`) and the `/soul-distill` command that maintains it. Soul System repo is the first dogfood target.

**Architecture:** Three-layer doctrine — seed (`operations/CLAUDE.md`, universal, always-on) → Mind (`mind.md` at project root, project-specific, always-on, ≤200 lines) → records (witness/findings/ideas/amendments, on-demand). `/soul-distill` is a Body-invoked slash command (no auto-fire MVP) that reads the records, applies the 4-bucket-plus-residual schema, runs 4 shrinkage checks + 6 failure-mode guards, and produces a draft `mind.md` for Body curation. Mirrors `/soul-skill`'s draft-for-curation pattern.

**Tech Stack:** Markdown slash-command spec (Agent Skills-adjacent). Symlinked per F029. No new runtime — Claude executes the command by reading the spec.

**Spec anchor:** `docs/specs/2026-05-26-the-mind-design.md` (committed `ad43695`).
**Seed material:** `docs/experiments/2026-05-26-mind-tier1-candidate.md` (218 lines, hand-crafted).

---

## File Structure

**Create:**
- `commands/soul-distill.md` — the slash-command spec (mirrors `/soul-skill` shape).
- `mind.md` (repo root) — the deployed Mind, seeded from the Tier 1 candidate (pruned).
- Symlink: `~/.claude/commands/soul-distill.md` → repo file (per F029).

**Modify:**
- `operations/CLAUDE.md` — add a short pointer paragraph about the optional Mind layer + the `@mind.md` import pattern for projects.
- `commands/soul-init.md` — surface the Mind option when initializing a new project (optional `@mind.md` line in the generated CLAUDE.md template).
- `SYSTEM-VERSION.md` — bump to 0.5.0 with changelog entry.
- `ideas.md` — update SOUL-I026 status to "Built (MVP)" with the deployed-artifact reference.
- `witness.md` — append SOUL-068 (or next free per I027 re-read-verify) recording the brainstorm → Tier1 → Tier2 → spec → build arc.

**No code files.** No tests in the executable sense — verifications are structural checks (grep, wc, file-existence).

---

## Task 1: Write `commands/soul-distill.md`

**Files:**
- Create: `commands/soul-distill.md`

- [ ] **Step 1.1: Write the slash-command spec.** Mirrors `/soul-skill` shape (read `commands/soul-skill.md` for the pattern first if not in context). Content must cover: trigger (Body-invoked, no auto-fire); inputs read (witness.md, ideas.md, findings/open/+closed/, amendments/, existing mind.md); the 4-bucket-plus-residual schema; the 4 shrinkage-invariant checks (line budget ≤200/cap 300, anchor requirement, generator test, growth check); the 6 failure-mode guards (drift, force-fit, renamed-seed, renamed-CLAUDE.md, doctrine-obligation collapse, stale); draft-for-curation output (NOT auto-commit); the three diagnostic self-test questions from the Tier 1 candidate (moved from artifact to command per spec §Schema).

Full content shape:

```markdown
---
description: Distill the project's accumulated record (witness + findings + ideas + amendments) into a compressed mind.md — rules + tensions + invariants + contrast cases + incompressible residual. Use on-demand when the record has accumulated enough new rule-evidence to warrant a refresh. Produces a draft for Body curation; never auto-commits. Mirrors /soul-skill's draft-for-curation discipline.
---

# /soul-distill — refresh the Mind

The Distiller's instrument. Reads the project's durable record; compresses it into
the Mind's four buckets + residual; runs the shrinkage invariant + failure-mode
guards; presents a draft for the Body to curate and commit.

[... full spec body covering all the above. Use /soul-skill as the structural template. ...]
```

- [ ] **Step 1.2: Verify the file parses and contains required sections.**

Run:
```bash
grep -E "^## " commands/soul-distill.md
```
Expected output (order/exact names may vary; ALL must appear):
```
## What to do
## What not to do
```
(or whatever section structure the spec uses — match /soul-skill's pattern.)

Run:
```bash
grep -c "shrinkage" commands/soul-distill.md && grep -c "residual" commands/soul-distill.md
```
Expected: both ≥ 1.

- [ ] **Step 1.3: Verify line budget.** A slash-command spec at ≤200 lines is healthy; >300 means we're rewriting the spec doc, not the command.

Run:
```bash
wc -l commands/soul-distill.md
```
Expected: ≤200 lines.

- [ ] **Step 1.4: Commit.**

```bash
git add commands/soul-distill.md
git commit -m "feat(soul): /soul-distill command spec (Mind MVP, part 1/6)"
```

---

## Task 2: Symlink `/soul-distill.md` to `~/.claude/commands/`

**Files:**
- Create: `~/.claude/commands/soul-distill.md` → `/mnt/d/Projects/Soul-System/commands/soul-distill.md` (symlink, per F029)

- [ ] **Step 2.1: Create the symlink.**

```bash
ln -s /mnt/d/Projects/Soul-System/commands/soul-distill.md ~/.claude/commands/soul-distill.md
```

- [ ] **Step 2.2: Verify the symlink resolves.**

```bash
ls -la ~/.claude/commands/soul-distill.md
```
Expected: `lrwxrwxrwx ... ~/.claude/commands/soul-distill.md -> /mnt/d/Projects/Soul-System/commands/soul-distill.md`

```bash
readlink ~/.claude/commands/soul-distill.md && test -f $(readlink ~/.claude/commands/soul-distill.md) && echo OK
```
Expected: prints the target path, then `OK`.

- [ ] **Step 2.3: No commit.** Symlinks in `~/.claude/commands/` are user-machine state, not repo state. Per F029, the repo file is the source of truth and the symlink is install-time. (Commit 33cae6d set this precedent.)

---

## Task 3: Prune the Tier 1 candidate into a deployed `mind.md` draft

**Files:**
- Source: `docs/experiments/2026-05-26-mind-tier1-candidate.md` (218 lines)
- Create: `mind.md` (repo root, draft)

- [ ] **Step 3.1: Read the Tier 1 candidate in full.**

Run:
```bash
cat docs/experiments/2026-05-26-mind-tier1-candidate.md
```
(Or `Read` the file.)

- [ ] **Step 3.2: Identify pruning targets.** The spec (§MVP build scope item 2) names what to prune: bias warning, self-assessment, Tier-test framing. Specifically: the opening "Status: Experimental / Tier 1" header lines; the "Bias warning (Skeptic)" block; the "Initial self-assessment (mine, biased)" block; the "Self-test (the three diagnostic questions)" block (those move to /soul-distill); the closing "Next move (Body's call)" block.

KEEP: the four buckets (Rules / Tensions / Invariants / Contrast cases) and the Incompressible residual bucket, AS-IS.

REPLACE: the header should now read as a deployed artifact, not an experimental one. Pattern:

```markdown
# The Mind — Soul System

This is the project-specific compressed-rules artifact for the Soul System repo
(per the lens-layer architecture in `docs/specs/2026-05-26-the-mind-design.md`).
Always-on (loaded after the seed via `@mind.md` in `CLAUDE.md`). Maintained by
the Distiller (`/soul-distill`). Test: produces coherent doctrinal reasoning
from itself + the seed alone — obligation-specific facts stay in the records.

[four buckets here]

## Incompressible residual (named, not forced)

[residual entries here]

---
**Last distilled:** 2026-05-26 (hand-pruned from the Tier 1 candidate; first /soul-distill Emissary test pending).
```

- [ ] **Step 3.3: Write the pruned `mind.md`.** Apply the cuts and the new header.

- [ ] **Step 3.4: Verify line budget.**

```bash
wc -l mind.md
```
Expected: ≤200 lines (target). If >200, prune further — the budget is load-bearing per spec §Shrinkage invariant.

- [ ] **Step 3.5: Verify the four buckets + residual are present.**

```bash
grep -E "^## " mind.md
```
Expected (exact names per the schema):
```
## Rules (generators)
## Tensions (rules that pull against each other)
## Invariants (cannot vary without breaking the project)
## Contrast cases (disambiguating examples)
## Incompressible residual (named, not forced)
```

- [ ] **Step 3.6: Verify the anchor requirement.** Each Rule entry should cite at least one anchor (SOUL-NNN, SOUL-INNN, SOUL-FNNN, A0NN, or a named source).

```bash
grep -A1 "^[0-9]\+\." mind.md | grep -Eo "(SOUL-[FI]?[0-9]+|A0[0-9]+|F0[0-9]+|feedback_[a-z_]+)" | sort -u | head
```
Expected: several anchor IDs surface (the Tier 1 candidate already had them).

- [ ] **Step 3.7: Do NOT commit yet.** The next task is an Emissary test of `/soul-distill` against this draft; commit after the validation.

---

## Task 4: Emissary test — invoke `/soul-distill` against the draft `mind.md`

This is the equivalent of /soul-skill's first test on dymola-sim-debug (witness SOUL-062): the instrument's first real use against a real artifact, refining the contract if gaps surface.

**Files:**
- Read: `commands/soul-distill.md`, `mind.md` (draft from Task 3), `witness.md`, `ideas.md`, `findings/open/`, `findings/closed/`, `amendments/accepted/`
- May modify: `commands/soul-distill.md` (if gaps surface in the contract), `mind.md` (if the Distiller suggests refinements)

- [ ] **Step 4.1: Read the `/soul-distill` command spec.** The instrument the Body would invoke.

```bash
cat commands/soul-distill.md
```

- [ ] **Step 4.2: Apply the command's procedure to the current state.** Read the durable records (witness tail, ideas.md, open + closed findings, accepted amendments), the existing draft `mind.md`, and the seed. Apply the four-bucket-plus-residual schema. Run the 4 shrinkage checks. Run the 6 failure-mode guards. Produce a refinement proposal (if any) for the draft `mind.md`.

- [ ] **Step 4.3: Record the Emissary test outcome.** In one paragraph: did the contract hold? Did any guard fire? What was refined? This will feed the witness entry in Task 8.

- [ ] **Step 4.4: Apply refinements if any.** If the Distiller surfaced real refinements to either `commands/soul-distill.md` or the draft `mind.md`, apply them.

- [ ] **Step 4.5: Verify shrinkage checks pass on the refined `mind.md`.**

```bash
wc -l mind.md
```
Expected: ≤200 lines (target), ≤300 (hard cap).

```bash
grep -E "^## " mind.md
```
Expected: the five required section headers from Task 3.5.

```bash
# Each rule has at least one anchor:
awk '/^## Rules/,/^## Tensions/' mind.md | grep -E "^[0-9]+\." | wc -l
awk '/^## Rules/,/^## Tensions/' mind.md | grep -E "(SOUL-[FI]?[0-9]+|A0[0-9]+|F0[0-9]+|feedback_)" | wc -l
```
Expected: anchor-citation count ≥ rule count.

- [ ] **Step 4.6: Do NOT commit yet.** Body curates next.

---

## Task 5: Body curation gate

**Files:** none (review-only)

- [ ] **Step 5.1: Present the refined `mind.md` + the Emissary outcome to the Body.** Explicit ask: review the deployed Mind before commit. The /soul-skill pattern (commit `dcdacf2` / witness SOUL-061) is the precedent: agent drafts, Body curates, agent commits after sign-off.

- [ ] **Step 5.2: Apply Body's edits if any.** Iterate until the Body says ship.

- [ ] **Step 5.3: Commit the deployed `mind.md`.**

```bash
git add mind.md
git commit -m "feat(soul): deploy mind.md (Soul System dogfood, Mind MVP part 3/6)"
```

---

## Task 6: Add `@mind.md` to the Soul System's own `CLAUDE.md` import chain + seed/init pointer

**Files:**
- Modify: `CLAUDE.md` (repo root)
- Modify: `operations/CLAUDE.md` (seed — add a short pointer about the optional Mind layer)
- Modify: `commands/soul-init.md` (template should mention the Mind layer as opt-in)

- [ ] **Step 6.1: Read current root `CLAUDE.md`.**

```bash
cat CLAUDE.md
```

- [ ] **Step 6.2: Add `@mind.md` after `@operations/CLAUDE.md` in root `CLAUDE.md`.**

If the current file is exactly `@operations/CLAUDE.md`, change it to:
```
@operations/CLAUDE.md
@mind.md
```

- [ ] **Step 6.3: Verify the imports resolve.**

```bash
ls -la operations/CLAUDE.md mind.md
```
Expected: both files exist.

- [ ] **Step 6.4: Add the optional-Mind paragraph to `operations/CLAUDE.md` (the seed).** Place it near the end, before the "On This Document" section. Content:

```markdown
## The Mind (optional project layer)

A project may carry a `mind.md` at its root — a compressed rule-set distilled from
its own accumulated record (witness, findings, ideas, amendments). When present,
import it after this seed (`@mind.md`) so its rules become part of the always-on
context. Maintained by the Distiller (`/soul-distill`). The Mind holds doctrine
(rules across contexts); specific obligations stay in the records. See
`docs/specs/2026-05-26-the-mind-design.md` for the architecture.
```

- [ ] **Step 6.5: Verify the seed didn't bloat past budget.** The seed was 223 lines pre-Mind; this addition is ~8 lines. SOUL-033 budget is the constraint — keep it under ~240.

```bash
wc -l operations/CLAUDE.md
```
Expected: ≤240.

- [ ] **Step 6.6: Update `commands/soul-init.md`.** Read the current spec; add a brief note (1-2 sentences) that the generated project `CLAUDE.md` may include `@mind.md` if the project intends to use the Mind layer (or that it can be added later when first distilled).

```bash
cat commands/soul-init.md
```
Then apply a minimal edit — do NOT rewrite the spec.

- [ ] **Step 6.7: Commit.**

```bash
git add CLAUDE.md operations/CLAUDE.md commands/soul-init.md
git commit -m "feat(soul): wire Mind layer into seed + soul-init (Mind MVP part 4/6)"
```

---

## Task 7: SYSTEM-VERSION bump to 0.5.0

**Files:**
- Modify: `SYSTEM-VERSION.md`

- [ ] **Step 7.1: Read current `SYSTEM-VERSION.md`.**

```bash
head -15 SYSTEM-VERSION.md
```
Confirm current version is 0.4.6 (it should be, from commit `05528e4`).

- [ ] **Step 7.2: Bump `Current:` to 0.5.0.** Edit the line `Current: **0.4.6**` → `Current: **0.5.0**`.

- [ ] **Step 7.3: Add changelog entry above the 0.4.6 row.**

Content (paste verbatim):

```
| 0.5.0 | 2026-05-26 | **The Mind — `/soul-distill` MVP (SOUL-I026 graduated).** New always-on architectural layer: project-scoped `mind.md` at the project root, loaded after the seed via `@mind.md`. Holds compressed rules / tensions / invariants / contrast cases + named incompressible residual. Distilled from the project's accumulated record (witness + findings + ideas + amendments) by the Distiller, invoked on-demand via `/soul-distill`. Draft-for-curation, never auto-commits (mirrors `/soul-skill`). Includes the 4 shrinkage-invariant checks (≤200-line target, anchor requirement, generator test, default-deny growth) and 6 failure-mode guards (drift, force-fit, renamed-seed, renamed-CLAUDE.md, doctrine-obligation collapse, stale). Three-layer doctrine now: seed (universal, always-on) → Mind (project, always-on) → records (specific, on-demand). Necessity established before instrument: Tier 1 (hand-crafted candidate, 218 lines) + Tier 2 (held-out A/B, Mind-only arm was ~41% cheaper than full-record arm, arms disagreed on direction — informative datum confirming doctrine-vs-obligation boundary). Deferred: auto-fire hooks, `/soul-mind` viewer, cross-project synthesis, reproduction-fidelity automation, plugin packaging. Spec: `docs/specs/2026-05-26-the-mind-design.md`. Plan: `docs/plans/2026-05-26-the-mind-implementation.md`. Witness SOUL-068. |
```

- [ ] **Step 7.4: Verify.**

```bash
head -15 SYSTEM-VERSION.md
```
Expected: `Current: **0.5.0**` and the new row immediately after the header.

- [ ] **Step 7.5: Commit.**

```bash
git add SYSTEM-VERSION.md
git commit -m "feat(soul): bump to 0.5.0 (Mind MVP part 5/6)"
```

---

## Task 8: Witness entry + ideas.md status update

**Files:**
- Modify: `witness.md` (append)
- Modify: `ideas.md` (update SOUL-I026 status)

- [ ] **Step 8.1: Determine next witness ID via I027 re-read-verify protocol.**

```bash
grep -c "^ID:" witness.md
# Then check the highest ID:
grep "^ID:" witness.md | tail -3
```
Expected: SOUL-067 is the last (from commit `05528e4`). Next is SOUL-068.

I027 protocol: re-read just before write; if anything has been appended in the meantime, increment.

- [ ] **Step 8.2: Append the witness entry to `witness.md`.** Content covers the whole arc: brainstorm decision → Tier 1 hand-craft → Tier 2 A/B (with the disagreement-on-direction datum, ~41% token savings) → lens-layer architectural decision → spec → plan → MVP build → Emissary test outcome (from Task 4) → deployment. Use the existing witness format (read SOUL-067 for shape).

```
ID:           SOUL-068
WHEN:         2026-05-26 / The Mind MVP shipped (SOUL-I026 graduated)
WHERE:        commands/soul-distill.md (NEW); mind.md at repo root (NEW); CLAUDE.md
              + operations/CLAUDE.md + commands/soul-init.md (Mind import + pointer);
              SYSTEM-VERSION.md → 0.5.0; docs/specs/2026-05-26-the-mind-design.md;
              docs/plans/2026-05-26-the-mind-implementation.md;
              docs/experiments/2026-05-26-mind-tier1-candidate.md.
WHAT:         [Fill in the full arc: brainstorm with /brainstorming → Tier 1 hand-craft
              of candidate Mind → Tier 2 held-out A/B on /soul-witness? question (Mind-
              only ~41% cheaper, arms DISAGREED on direction — informative datum
              showing Mind handles doctrine well, records carry obligations) → lens-
              layer architectural decision → 8-section spec → implementation plan →
              MVP build (commands/soul-distill.md + deployed mind.md from pruned Tier
              1 + @-import wiring + version bump) → Task-4 Emissary test outcome
              (state plainly: did the contract hold? any refinement?).]
TYPE:         Architect (lens-layer design), Artificer (the command + the deployed
              artifact), Emissary (Tier 1 + Tier 2 experiments against the record),
              Skeptic (kept the bias warning visible through Tier 1), Steward
              (necessity test first; explicit retire conditions in the command).
CONSEQUENCE:  Three-layer doctrine now (seed → Mind → records). Soul System is its
              own first dogfood. Tier 3 deployment validation (the 2-3-question A/B
              on the deployed Mind, plus dogfood on a second project — REF-03
              candidate) is the next thread, NOT part of this MVP. SOUL-I026
              transitions Raw → Built (MVP). NOT COMMITTED yet (final commit comes
              from Task 8.5).
STATUS:       Resolved (MVP shipped; deployment-validation residual named in spec
              §Tier 3; SYSTEM-VERSION → 0.5.0)
```

- [ ] **Step 8.3: Update SOUL-I026 status in `ideas.md`.** Read the entry around line 587+ (the I026 block). Add a Status line / change the STATUS field to:

```
STATUS:    Built (MVP) [2026-05-26, via SOUL-068 → 0.5.0]. The Mind is now a third
           always-on layer between the seed and the records: project-scoped mind.md
           distilled by /soul-distill (on-demand, draft-for-curation). All six open
           questions from this idea's NOTES were resolved during the brainstorm:
           (1) WHERE = project root, single file; (2) WHEN = on-demand MVP (auto-fire
           deferred); (3) SHRINKAGE invariant = 4 mechanical checks (≤200-line budget,
           anchor requirement, generator test, default-deny growth); (4) failure-mode
           guards = 6 named (drift, force-fit, renamed-seed, renamed-CLAUDE.md,
           doctrine-obligation collapse, stale) + retirement protocol; (5) seed-tension
           = yes always-on at the project layer, ~200-line budget honoring SOUL-033;
           (6) reproduction-test = partial — Tier 2 showed Mind reproduces doctrinal
           reasoning faithfully + ~41% cheaper, NOT obligation-specific reasoning
           (lens-layer architecture is the answer). Tier 3 deployment validation is
           the open residual.
```

- [ ] **Step 8.4: Verify witness + ideas.**

```bash
tail -50 witness.md | head -45
# And:
grep -A2 "^ID:        SOUL-I026" ideas.md | head -5
```
Expected: SOUL-068 entry visible; I026 STATUS now shows "Built (MVP)".

- [ ] **Step 8.5: Final commit.**

```bash
git add witness.md ideas.md
git commit -m "$(cat <<'EOF'
feat(soul): The Mind MVP shipped — SOUL-068 + I026 graduated -> 0.5.0

Closing commit of the Mind MVP arc. Witness SOUL-068 records the full
brainstorm → Tier 1 → Tier 2 (~41% cheaper Mind-only, arms disagreed —
informative) → lens-layer design → spec → plan → build chain. SOUL-I026
transitions Raw → Built (MVP); all 6 original open questions resolved.
Tier 3 deployment validation deferred to a follow-up arc.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 8.6: Verify clean working tree (modulo the Body's pre-existing LICENSE/SOUL-A008).**

```bash
git status --short
```
Expected: ONLY ` M LICENSE` and ` D amendments/proposed/SOUL-A008-execution-topology.md` (the Body's pre-existing churn that has stayed untouched the whole session).

```bash
git log --oneline -8
```
Expected: 6 new commits from this plan (Tasks 1, 5, 6, 7, 8 — Task 2 is a symlink not commit, Task 3 commits with 5, Task 4 may commit if it refined the command), preceded by `ad43695 docs(spec): SOUL-I026 The Mind` and earlier.

---

## Self-Review

1. **Spec coverage:** Every spec §MVP build scope item maps to a task — (1) command → Task 1; (2) mind.md → Tasks 3-5; (3) CLAUDE.md pattern → Task 6; (4) symlink → Task 2; (5) version bump → Task 7; (6) witness → Task 8. ✓

2. **Placeholder scan:** One conditional in Task 4 ("if gaps surface in the contract") — this is the Emissary-test pattern, not a placeholder; the conditional resolves at execution time. Step 4.3 instructs to record outcomes in plain prose. Step 8.2 has bracketed instruction text inside the witness entry shape ("[Fill in the full arc: ...]") — that IS a placeholder, deliberately, because the agent has to fill it from Task 4's recorded outcome. ✓ acceptable (instruction, not a TBD).

3. **Type/identifier consistency:** `mind.md` (singular, root, lowercase) used throughout. `/soul-distill` (no underscore, no .md extension when referenced as a command). `SOUL-068` is the predicted next witness ID — if I027 re-read-verify says it's taken, increment. ✓

4. **Ambiguity:** Task 4's "apply refinements if any" leaves discretion to the executor — appropriate, since the Emissary test's outcome can't be pre-known. Task 8.3's I026 STATUS rewrite includes specific resolutions for the 6 open questions — those come from the spec, not invented at execution. ✓

5. **Frequency of commits:** 6 commits across 8 tasks (Task 2 is symlink-only, Task 4 conditional). Each commit is a coherent unit of progress. ✓

6. **DRY/YAGNI:** Only the MVP scope from spec §MVP build scope is built; all 5 DEFER items remain deferred. Task 4 dogfoods the command immediately — no extra rigging. ✓

---

## Execution

**Mode:** Inline execution in the current session (we are already mid-arc; no fresh worktree). The Body's prior commits and the spec are all in the current branch. Pause for the Body at Task 5 (curation gate) and at the final commit confirmation.
