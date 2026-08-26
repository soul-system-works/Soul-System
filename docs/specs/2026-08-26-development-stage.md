# The Development Stage — implementation plan (Soul System → 2.2.0)

> **For agentic workers:** execute with the `executing-plans` skill, task by task, in
> order. This repo's own loop applies (it held eleven-for-eleven in an adopting project,
> 2026-08-25): `implementer` with one task as the brief · `diff-reviewer` on the applied
> result before the merge, briefed with the claims below as "verify, do not trust" · the
> orchestrator runs the checks itself and commits. Steps use `- [ ]` checkboxes.

**Status:** PLANNED 2026-08-26 — grilled with the Body in-session (24 questions, all
settled; the distilled screen replaced a seven-question draft at the Body's push-back).
Execution order changed the same day at the Body's call: **release first (Task 8), live run after (Task 9)** — the override is stated in SOUL-180.

**Goal:** a project can declare its development stage — `prototype` / `pre-release` /
`released` — once, in its own `CLAUDE.md`, and every later session knows what may be
broken and what must be kept without the owner re-teaching it.

**Architecture:** the stage is a recorded answer to contract rule 7 (ask the owner what
only the owner knows), not new doctrine. A new owner-invoked skill `/soul-stage` carries
the three presets and a one-screen questionnaire, and writes a self-contained block of
≤ ~15 lines under the project's Register line. The contract gains one sentence (absent =
released-grade caution, i.e. today's behaviour). Transitions are the only events: each is
one witness entry. The completion gate, the hook, and the record's rules do not change.

**Tech stack:** Markdown skill files under `skills/` (Claude Code plugin, auto-discovered);
the Python Stop hook is untouched; git branch `v2.2.0` merged to `main` at release.

---

## Resolved in grilling (2026-08-26) — the decisions this plan implements

| # | Decision |
|---|---|
| Q1 | Include it, as a declared answer to rule 7 — a one-line declaration plus a short block; never a workflow. |
| Q2 | The skill carries questions + presets; the project's `CLAUDE.md` carries a self-contained answered block, rewritten by the skill at each transition. No imported rule file (a second external import's re-prompt behaviour is undocumented; a decline disables *all* external imports in the project with no documented re-enable). |
| Q3 | No stage line = behave as released: protect what others may depend on, ask before breaking. Nothing in existing projects changes until declared. |
| Q4 | Attribute `Stage:`; values `prototype` / `pre-release` / `released`. Not "phase" (collides with plan-milestone usage), not alpha/beta (mean different things at PyPI, Google, Kubernetes). |
| Q5 | One witness entry per transition; no per-entry field (derivable from dates; format changes are what cost — the 61-entry retrofit). |
| Q6 | Completion gate and hook untouched. |
| Q7 | Owner changes the stage; the model proposes in one sentence and holds. |
| Q8 | Project-level; a nested `CLAUDE.md` may carry its own Stage line for a sub-deliverable (Claude Code loads nested files on demand and concatenates — docs verified). |
| Q9 | `/soul-init` offers it with a skip. |
| Q10 | Three presets; `frozen` named in the skill's text, not built. |
| Q11 | One sentence in the contract. |
| Q12 | The screen: stage choice with plain one-line descriptions · Q1 "does anything outside this project rely on part of it?" (skipped for prototype, required for released) · Q2 "what would tell you it has moved to the next stage?" (optional) · "anything to change or add?" (optional). Four of the original seven were the stage restated and were cut; the old-data rule became a standing pre-release rule. |
| Q13 | Asked all at once, pre-filled from the preset. |
| Q14–16 | Preset rule texts as written in Task 1 (prototype substance credited to mattpocock-skills `prototype`). |
| Q17 | Block shape as written in Task 1; provenance in the header line. |
| Q18 | Contract sentence as written in Task 2. |
| Q19 | Proposal triggers: (i) about to add a deprecation path/alias/shim in prototype or pre-release; (ii) evidence of an outside consumer; (iii) a release is cut; (iv) undeclared + first compatibility-relevant decision. **Placement changed by a fact found after the grill:** skills with `disable-model-invocation` are invisible to the model (verified this session — exactly the five flagged skills were absent from the model's list), so (i)–(iii) live in the block's own last line and (iv) is the contract sentence. |
| Q20 | `/soul-stage` is `disable-model-invocation: true` — it writes `CLAUDE.md`, the same reason `/soul-init` is reserved. |
| Q21 | Transition entry with a fixed WHAT; `/soul-next` shows the exit trigger and asks whether it is met. |
| Q22 | First live run on RealisticSensorsForge (RSF), rewriting its hand-written `Phase: beta` block; other projects at their next visit, none forced. |
| Q23 | One locked prediction with a miss direction, checked at the next distill (mind.md item 1). |
| Q24 | Branch `v2.2.0`, merge to `main` at release (the repo convention, reaffirmed after a retracted "commit to main"). |
| carried | `/soul-resume` restates the stage; `/soul-stage` with no argument shows/refreshes; backwards moves allowed; block under Register, else under the imports; RSF's cursor OWED #11 marked delivered by the live run; init reuses the skill's text, never a copy. |

**Where the idea came from (rule 2 — real history only):** RSF's cursor OWED UPSTREAM #11
(2026-08-25) and its live `CLAUDE.md:52` block (commit `8d2b91c`); the two carve-outs are
SENSA-061/062 (a change on one side of a published seam, made as if single-repo, doubled
every sensor in the viewer's panel; its suite failed `4 == 2`) and SENSA-064 (a `.get` ordered deleted as a shim
tracebacked on a real tree written before the key existed). A UE thermal-sensing project's
witness (2026-08-24) records the owner writing the same beta rule by hand into its Python
client deliverable's own nested `CLAUDE.md` ("there are no external customers; backwards
compatibility is not a constraint") — a second hand-written copy, in different words, with
no shared source; the parent project's root `CLAUDE.md` carries nothing. (Project
identifiers deliberately omitted here and in SOUL-I061 — the private name map is the only
place they live; see Task 8 step 4. The first draft of this paragraph claimed the rule
"survived only in a witness narrative"; fresh-context review found the nested file.)

---

## File map

| File | Action | Responsibility |
|---|---|---|
| `skills/soul-stage/SKILL.md` | **create** | the screen, the three presets, the block template, the transition entry, refresh mode, the not-to-do list |
| `operations/CLAUDE.md` | modify (after the Register paragraph, line 65) | one sentence: how to declare, and that absent = released |
| `skills/soul-init/SKILL.md` | modify (new step 2b after line 77; step 4 bullet after line 150) | offer the stage once, skippable, by following the `soul-stage` skill text |
| `skills/soul-resume/SKILL.md` | modify (step 3, lines 64–66) | restate the declared stage in one phrase; silent when none |
| `skills/soul-next/SKILL.md` | modify (step 1, step 3) | read the block; show the exit trigger and ask if met |
| `skills/soul-help/SKILL.md` | modify (step 3, the hand-listed core) | add `soul-stage` |
| `docs/using-the-soul.md` | modify (Day one; Over time; Going deeper table) | the lifecycle page carries the stage |
| `README.md` | modify (lines 47–48; line 94) | init question sentence; "eight" → "ten" instruments |
| `SYSTEM-VERSION.md` | modify (Current; changelog row) | 2.2.0 |
| `.claude-plugin/plugin.json` | modify (`version`) | 2.2.0 |
| `ideas.md` | append | SOUL-I061 — the idea, pointing here |
| `witness.md` | append (at release) | SOUL-180 — the release, the live run, the locked prediction |
| `hooks/*` | **untouched** | regression-run only |
| RSF `CLAUDE.md` (other repo) | live run | `Phase: beta` block → `Stage: pre-release` block |

---

### Task 0: Branch and capture the idea

**Files:** `ideas.md` (append after the SOUL-I060 entry, which ends the file)

- [ ] **Step 1: Branch**

```bash
cd /mnt/d/Projects/Soul-System && git checkout -b v2.2.0
```
Expected: `Switched to a new branch 'v2.2.0'`

- [ ] **Step 2: Confirm the next idea id is free**

```bash
grep -c "^ID: *SOUL-I061" ideas.md
```
Expected: `0`

- [ ] **Step 3: Append SOUL-I061** (match the file's fenced format; the previous entry closes with a fence)

````markdown

```
ID:        SOUL-I061
WHEN:      2026-08-26
IDEA:      A declared DEVELOPMENT STAGE per project — prototype / pre-release /
           released — recorded once in the project's own CLAUDE.md as a standing
           answer to contract rule 7, with the short block of rules that follows
           from it (what may be broken, what must be kept). Set by a new
           owner-invoked /soul-stage; offered at /soul-init with a skip; each
           change is one witness entry; absent means released-grade caution
           (today's behaviour). Not doctrine, not a workflow, no change to the
           completion gate.
STATUS:    In build (v2.2.0) — design grilled and resolved in
           docs/specs/2026-08-26-development-stage.md
WHY:       The owner supplied the same rule by hand in two projects on
           consecutive days (RSF CLAUDE.md 8d2b91c, 2026-08-25; a UE thermal-sensing
           project's Python client deliverable, in its own nested CLAUDE.md,
           2026-08-24 — two hand-written copies in different words with no shared
           source), while a third project (that one's parent UE codebase) needs
           the INVERSE rule and nothing declares that either. The model's default
           is release-grade caution; nothing in the contract says which project
           it is in. Two carve-outs were learned by running under the
           hand-written rule (SENSA-061/062, SENSA-064) and are the unguessable
           content that justifies hosting the presets upstream. Origin: RSF
           cursor OWED UPSTREAM #11.
DEVELOP:   Steward — the one measured question is Q23's locked prediction
           (shim/deprecation churn falls after declaration; a miss would be
           over-deletion breaking a reader). Check at the next distill.
NOTES:     Captured with the Body's go at the close of the grill (A022). The
           seven-question draft was cut to one choice + two questions + a free
           line at the Body's push-back: four questions were the stage restated.
```
````

- [ ] **Step 4: Commit**

```bash
git add ideas.md docs/specs/2026-08-26-development-stage.md
git commit -m "ideas(SOUL-I061) + spec: the development stage — a declared answer to rule 7"
```

---

### Task 1: The skill — `skills/soul-stage/SKILL.md`

**Files:** Create `skills/soul-stage/SKILL.md`

- [ ] **Step 1: Write the file** with exactly this content:

````markdown
---
name: soul-stage
description: Declare or change the project's development stage — prototype, pre-release, or released — and write the short block of rules that follows from it into the project's CLAUDE.md, beside the Register line. Owner-invoked only; each change is one witness entry. Run with no argument to see the current stage or refresh the block.
disable-model-invocation: true
---

# /soul-stage — say what may be broken and what must be kept

`/soul-stage` shows the current stage and offers a refresh.
`/soul-stage <prototype|pre-release|released>` sets or changes it.

**What this is.** The contract's rule 7 says: when the right choice depends on
knowledge only the owner has, ask. Whether anyone relies on this code, and whether
its shape is settled, is exactly that knowledge. Without it a session falls back to
release-grade caution — keeping the shim, adding the alias, accepting-and-ignoring
the flag — which is right for a released project and waste in a pre-release one.
The stage is that answer, recorded once, where the pressure arrives (rule 1): the
project's own `CLAUDE.md`. It is not a workflow, it has no gates, and it changes
nothing about the completion gate or the record's rules.

**Where it writes.** The project's `CLAUDE.md` in the directory the session started
in — never the Soul System source repo (unless the session is running in that repo,
whose own `CLAUDE.md` is then the target, the same exception `/soul-capture` makes).
The block goes directly under the `**Register:**` line if there is one, otherwise
directly under the `@` import lines. One block per file. A nested `CLAUDE.md` — a
sub-deliverable with a different stage, such as a library living inside a larger
project — may carry its own block; Claude Code loads nested files when it works in
that directory and concatenates them with the root file.

**No stage line means released.** Protect what others may depend on, and ask
before breaking it. That is the contract's default and today's behaviour;
declaring a stage is how a project opts out of it.

## The screen — one choice, two facts, one free line

Show all of it at once, pre-filled from the chosen preset; the owner edits only
what differs. Plain words — the owner may never have heard of the Soul.

> **Which stage is this project in?**
> - **prototype** — throwaway code to answer a question; nothing is promised to anyone
> - **pre-release** — building the real thing; still free to rename, reorganise and delete
> - **released** — people rely on it; changes are careful and announced
>
> **1. Does anything outside this project rely on part of it?** A library other
> code imports, a command-line tool, a file format it writes. List them, or
> "nothing". *(skipped for prototype; required — must not be empty — for released)*
>
> **2. What would tell you it has moved on to the next stage?** One line, e.g.
> "first outside user", "the v1.0 tag", "we start depending on it from project X".
> *(optional)*
>
> **Anything to change or add?** *(optional — becomes the block's "Owner's
> additions" line)*

*Why only this much:* the stage the owner picks already answers who uses the code,
how settled the design is, and what a change ships with — the preset carries those.
Question 1 is the one fact no preset can know: a published seam treated as a free
rename doubled every sensor in a downstream viewer's panel until that viewer's own
suite failed `4 == 2` (an adopting project, 2026-08-24). Question 2 is the exit
trigger: an owner-gated decision with no date sits forever (SOUL-F064). Everything
else is customisation, and it gets one line.

## The presets

A preset is the rule lines the block carries. Copy them verbatim; put the owner's
changes in "Owner's additions" rather than editing preset lines, so a later refresh
can tell the two apart.

### prototype
- This code exists to answer a question. Name or place it so nobody mistakes it for the real thing.
- Make it easy to run and skip the polish: no tests beyond what makes it run, no error handling beyond that, no abstractions.
- Don't save state to disk unless saving is the question; if you must, name it so it's obviously disposable.
- Nothing here is promised to anyone — change anything freely.
- Before the code is thrown away, write down the answer it produced (`/soul-capture idea` or `witness`). The code can go; the answer can't. Main keeps only the decision.

*(Substance from Matt Pocock's `prototype` skill — mattpocock-skills,
`skills/engineering/prototype` — restated here so this does not depend on that
plugin being installed.)*

### pre-release
- Build fast, with tests.
- No backwards compatibility — except the surfaces listed in this block. Those are promises; changing one is a coordinated change with whoever relies on it.
- Old data, not old code: code that reads files may tolerate a field that didn't exist yet; code that writes never leaves it out. Anything else that only exists to keep old code paths alive gets deleted.
- Delete as you go: no-op flags and options, unused parameters, shims, dead code. No deprecation paths, aliases or migration layers.
- Rename, change signatures and reorganise freely when it makes things clearer.
- Fix the cause, not the symptom: if a bug points at a structural problem, fix the structure as part of the work.
- Refactors go in their own commits, tied to code you're already touching; call out bigger problems instead of silently widening the change.

### released
- People rely on this. The surfaces listed in this block are the public contract; changing any of them is a deliberate, announced change — never a side effect.
- Deprecate, don't delete: keep the old way working with a warning, say when it goes away, and point at the new way.
- Every change ships with tests and a changelog line; a change to a public surface also ships with upgrade instructions.
- New behaviour is opt-in; existing behaviour stays as it is unless changing it is the point.
- Fix the symptom when the structural fix is out of scope — and record the debt (`/soul-capture idea`) so it isn't lost.

`frozen` — security and critical fixes only, no refactors — exists in the wider
vocabulary (repostatus.org "inactive", Node's "legacy" stability index). No
adopting project has needed it, so it is not a preset; add it when one does.

## The block

Header, then the answers, then the preset lines, then two fixed lines. Keep it
under about fifteen lines; it is always-on text for every session in the project.

```
**Stage: pre-release** (owner, 2026-08-26 · written by /soul-stage — re-run it to change or refresh)
- Relied on from outside: common/sensor_discovery.py (SensorInstance,
  discover_sensors) · src/rsviewer_provider.py — changing these is a
  coordinated change.
- Rules:
  - Build fast, with tests.
  - <the rest of the preset's lines, verbatim>
- Next stage when: a consumer beyond the viewer appears.
- Owner's additions: none.
- Propose `/soul-stage` if something outside this project starts relying on it,
  a release is cut, or a rule above is about to be overridden — one sentence,
  then wait; only the owner changes the stage.
The contract's rules and the completion gate apply unchanged.
```

For `prototype` the "Relied on from outside" line reads `nothing — nothing is
promised`. The last bullet is where the model's proposal triggers live: this skill
is invisible to the model by design, so the always-on block has to carry them.

## What to do

1. **Find the existing block.** Read `CLAUDE.md` in the current directory (do not
   search upward). The block runs from a line starting `**Stage:` through the line
   `The contract's rules and the completion gate apply unchanged.` A line starting
   `**Phase:` from before this skill existed counts as the header of a hand-written
   block: treat everything from it to the next `##` heading (or the paragraph that
   names the published seams, whichever comes last) as the block to replace, in
   place — show the owner exactly which lines you intend to replace before doing
   it. If a block exists, show its stage, date, relied-on list, trigger and
   additions.
   - **No argument:** offer a refresh (rewrite from the current preset, keeping the
     owner's three answers) or stop. **Argument equal to the current stage:** same
     as a refresh.
2. **Show the screen**, pre-filled: preset from the argument; answers 1, 2 and the
   additions from the existing block if there is one. Wait for the owner. Check:
   `released` needs a non-empty answer to question 1 — ask again rather than write
   an empty public contract.
3. **Compose the block** from the template and show it. Wait for go / edit / cancel.
4. **Write it:** replace the existing block in place, or insert it directly under
   the `**Register:**` line, or — with no Register line — directly under the last
   `@` import line. Touch nothing else in the file.
5. **Record the transition** — one witness entry, following `/soul-capture
   witness`'s rules (this project's code from the log header, next id, re-read
   before appending, never `SOUL-` outside the Soul System repo):
   - WHEN: today · WHERE: `CLAUDE.md`, the Stage block
   - WHAT: `Stage <previous stage, or "undeclared"> → <new stage> (owner, <date>).
     Why: <the owner's words>. Changed: <what differs from the previous block —
     the relied-on list, the trigger, the additions — or "first declaration">`
   - TYPE: `Decision — stage change` · CONSEQUENCE: the preset's headline rule now
     applies (e.g. "no backwards compatibility beyond two named surfaces") ·
     STATUS: `Resolved`
   A refresh that changes neither the stage nor an answer writes no entry. Show
   the draft; append on go.
6. **Report:** the file and what changed; that the rules apply from the *next*
   session (this one loaded `CLAUDE.md` at start); and that `/soul-next` will show
   the exit trigger from now on.

## What not to do

- Do not run this on the model's own initiative. The model proposes in one
  sentence and waits; the skill is owner-invoked (`disable-model-invocation`),
  like `/soul-init` and for the same reason — it writes `CLAUDE.md`.
- Do not refuse a backwards move (released → pre-release). Stages are not one-way;
  the witness entry carries the why.
- Do not add a stage field to other witness entries. Which stage an entry fell in
  is derivable from its date and the transition entries.
- Do not touch the completion gate, the hook, or the contract's rules. The block's
  last line says they apply unchanged, and it must stay true.
- Do not commit — the owner owns the commit moment.

---

**Source:** Built 2026-08-26 from an adopting project's OWED UPSTREAM item (project
stage as a contract dimension, with two carve-outs learned by running under a
hand-written beta block, 2026-08-24/25) and a second project's owner stating the
same rule by hand the day before. Design grilled with the Body:
`docs/specs/2026-08-26-development-stage.md`. Idea: SOUL-I061. Prototype preset
substance credited to mattpocock-skills `prototype`. **Adopted:** 2026-08-26
(v2.2.0). **Status:** active.
````

- [ ] **Step 2: Check the frontmatter is the one Claude Code reads**

```bash
head -5 skills/soul-stage/SKILL.md | grep -c -E "^(name: soul-stage|disable-model-invocation: true)$"
```
Expected: `2`

- [ ] **Step 3: Check the block budget claim holds for the largest preset** (header + relied-on 3 + "Rules:" 1 + 7 preset lines + next 1 + additions 1 + propose 3 + footer 1)

```bash
awk '/^### pre-release/{f=1;next} /^### released/{f=0} f && /^- /{n++} END{print n}' skills/soul-stage/SKILL.md
```
Expected: `7` (so a pre-release block is 18 physical lines with wrapping, ~15 logical — within "about fifteen"; if it is not 7, the preset text was not copied verbatim)

- [ ] **Step 4: Commit**

```bash
git add skills/soul-stage/SKILL.md
git commit -m "skills(soul-stage): declare the development stage — presets, one-screen questionnaire, transition entry"
```

---

### Task 2: The contract sentence

**Files:** Modify `operations/CLAUDE.md` — insert a new paragraph after line 65 (the end of the Register paragraph, "...never receives an upgrade."), before line 67 (`**Projects importing this contract**`).

- [ ] **Step 1: Insert** this paragraph (blank line before and after):

```markdown
**Stage** (optional): a project declares `prototype` / `pre-release` / `released`
in its own CLAUDE.md via `/soul-stage`, and the block beneath says what may be
broken and what must be kept; undeclared means released — protect what others
may depend on, and ask before breaking it (rule 7).
```

- [ ] **Step 2: Verify placement and size**

```bash
grep -n "^\*\*Stage\*\* (optional)" operations/CLAUDE.md; wc -l operations/CLAUDE.md
```
Expected: the match at line `67`; `81 operations/CLAUDE.md` (75 + 5 lines + 1 blank — five after review finding 15 added the `/soul-stage` offer). The contract is the always-on page for every project — five lines is the whole cost, and it stays under the ~80-line budget `/soul-distill` uses for a Mind.

- [ ] **Step 3: Sentinel — the sentence must not answer `/soul-resume`'s own wiring check.** Step 0 of resume asks the session for "how many numbered rules the contract has, and what rule 3 requires"; the new paragraph mentions rule 7, not rule 3, and adds no numbered rule:

```bash
grep -c -E "^[0-9]+\. \*\*" operations/CLAUDE.md
```
Expected: `10`

- [ ] **Step 4: Commit**

```bash
git add operations/CLAUDE.md
git commit -m "contract: one sentence — a project may declare its development stage; undeclared means released"
```

---

### Task 3: `/soul-init` offers the stage once, skippable

**Files:** Modify `skills/soul-init/SKILL.md` — insert step 2b after step 2's last line (line 77, "...always-on)."), before `3. **Ask the one question that cannot be defaulted...` (line 79); add one bullet to step 4's report list (after line 150, the last line of the gitignored-CLAUDE.md bullet).

- [ ] **Step 1: Insert step 2b** (both branches of step 2 fall through to it — a pre-existing file without a Stage line is offered the same question, idempotently):

```markdown
2b. **Offer the development stage — once, skippable.** Whether `CLAUDE.md` was
   just created or already existed, if it carries no `**Stage:**` line, ask:

   > "Development stage — prototype, pre-release, released — or skip?"

   with the three one-line descriptions from `<derived-root>/skills/soul-stage/SKILL.md`
   (read that file and follow its screen, block and witness steps; do not copy its
   text here — a copy written at init never receives an upgrade, the same reason
   the register default lives in the contract). **Skip writes nothing**: no line
   means released-grade caution, which is the contract's default. A chosen stage
   writes the block directly under the Register line, or under the import when
   there is no Register line, and records the declaration as one witness entry.

   *Evidence for asking here:* two adopting projects had the owner state "no
   backwards compatibility — this is beta" by hand on consecutive days
   (2026-08-24/25), one of them only inside a witness narrative that no later
   session reloads.
```

- [ ] **Step 2: Add the report bullet** to step 4, after the gitignored-CLAUDE.md bullet:

```markdown
   - **If a stage was declared**, say which, and that its rules take effect from the
     next session; if skipped, say that `/soul-stage` declares one later and that
     until then the project is treated as released.
```

- [ ] **Step 3: Verify**

```bash
grep -n -E "^2b\. |soul-stage" skills/soul-init/SKILL.md
```
Expected: one `2b.` line; at least three `soul-stage` mentions (step 2b twice, step 4 once).

- [ ] **Step 4: Commit**

```bash
git add skills/soul-init/SKILL.md
git commit -m "skills(soul-init): step 2b offers the development stage once, skippable, via the soul-stage text"
```

---

### Task 4: `/soul-resume`, `/soul-next`, `/soul-help` learn the stage

**Files:** Modify `skills/soul-resume/SKILL.md` (step 3, lines 64–66) · `skills/soul-next/SKILL.md` (step 1, step 3) · `skills/soul-help/SKILL.md` (step 3)

- [ ] **Step 1: soul-resume step 3** — replace

```markdown
3. **Restate, in 2–3 lines:** where we are · the live design frame (if any) · the
   next step. Under a `plain` register (the project CLAUDE.md's Register line), say
   "the current design frame" rather than "the LIVE AL"; plain language throughout.
```
with
```markdown
3. **Restate, in 2–3 lines:** where we are · the live design frame (if any) · the
   next step · and, if the project's CLAUDE.md carries a `**Stage:**` line, the
   stage in one phrase ("stage: pre-release since 2026-08-26"). Say nothing about
   stage when there is no line — absence is the default, not a gap. Under a
   `plain` register (the project CLAUDE.md's Register line), say "the current
   design frame" rather than "the LIVE AL"; plain language throughout.
```

- [ ] **Step 2: soul-next step 1** — after `and `.soul/handoff.md` if present.` add the sentence:

```markdown
   Also read the project CLAUDE.md's `**Stage:**` block if there is one — its
   "Next stage when" line is the exit trigger this view exists to re-read.
```

- [ ] **Step 3: soul-next step 3** — after the `- **Later** — ...` bullet, before `Each item **points at its durable source**`, add:

```markdown
   **If a Stage block exists**, one line at the top of Next:
   `Stage: <stage> since <date> · next stage when: <trigger> — met?` When the
   records suggest it has been (an outside consumer appeared, a release was cut),
   say so and point at `/soul-stage`; do not run it. No block, no line.
```

- [ ] **Step 4: soul-help step 3** — replace `As of 1.0 the core is:` ... `soul-distill` `(refresh the Mind).` with:

```markdown
   As of 2.2 the core is: `soul-init` (set up a project), `soul-stage` (declare the
   development stage — what may be broken, what must be kept), `soul-capture
   <idea|witness|finding>` (write to the record), `soul-handoff` / `soul-resume`
   (continuity across sessions), `soul-explain` (describe the present; `council`
   mode for a multi-lens read), `soul-next` (what to do next), `soul-distill`
   (refresh the Mind).
```

- [ ] **Step 5: Verify all three**

```bash
grep -c "Stage" skills/soul-resume/SKILL.md skills/soul-next/SKILL.md; grep -c "soul-stage" skills/soul-help/SKILL.md
```
Expected: `skills/soul-resume/SKILL.md:1`, `skills/soul-next/SKILL.md:3` (step 1, step 3 twice), `1`

- [ ] **Step 6: Commit**

```bash
git add skills/soul-resume/SKILL.md skills/soul-next/SKILL.md skills/soul-help/SKILL.md
git commit -m "skills(resume/next/help): restate the stage, surface its exit trigger, list soul-stage"
```

---

### Task 5: The lifecycle page and the README

**Files:** Modify `docs/using-the-soul.md` · `README.md`

- [ ] **Step 1: using-the-soul, "Day one"** — replace the first paragraph's opening sentence

```markdown
Run `/soul-init` in your project. It asks two short questions — plain or fluent
language (plain is the default), and whether your record goes in version control
(yes is the default) — then writes one import line into your `CLAUDE.md` and
```
with
```markdown
Run `/soul-init` in your project. It asks two short questions — plain or fluent
language (plain is the default), and whether your record goes in version control
(yes is the default) — offers a third you can skip (the project's development
stage: prototype, pre-release or released; skipping means "treat it as released"),
then writes one import line into your `CLAUDE.md` and
```

- [ ] **Step 2: using-the-soul, "Over time"** — append a paragraph after the Mind paragraph ("...how you find out yours does."):

```markdown
**Declaring a stage.** When the project's situation changes — the first outside
user, a v1.0, or the day you decide the prototype is now the real thing — run
`/soul-stage <prototype|pre-release|released>`. One screen: pick the stage, name
anything outside the project that relies on part of it, say what would move it to
the next stage. It writes a short block into your `CLAUDE.md` saying what may be
broken and what must be kept, and records the change as one entry. Undeclared
projects are treated as released: nothing is broken without asking you.
```

- [ ] **Step 3: using-the-soul, table** — in the "Any command in full" row, add `soul-stage` to the examples:

```markdown
| Any command in full | `skills/<name>/SKILL.md` (e.g. [`soul-capture`](../skills/soul-capture/SKILL.md), [`soul-stage`](../skills/soul-stage/SKILL.md), [`soul-distill`](../skills/soul-distill/SKILL.md), [`soul-init`](../skills/soul-init/SKILL.md)) |
```

- [ ] **Step 4: README lines 47–48** — replace

```markdown
`/soul-init` also asks one register question — plain or fluent language; plain is
the default — and scaffolds the project's record files.
```
with
```markdown
`/soul-init` also asks one register question — plain or fluent language; plain is
the default — offers an optional development stage (`/soul-stage`: what may be
broken, what must be kept), and scaffolds the project's record files.
```

- [ ] **Step 5: README line 94** — `The eight /soul-* instruments` → `The ten /soul-* instruments`

- [ ] **Step 6: Consistency sweep (the F048 dangling-reference practice, run forward)** — every surface that enumerates the instruments names the new one, and no stale count survives:

```bash
grep -l "soul-stage" README.md docs/using-the-soul.md skills/soul-help/SKILL.md skills/soul-init/SKILL.md skills/soul-next/SKILL.md operations/CLAUDE.md | wc -l; grep -n -i "eight /soul" README.md docs/*.md; ls skills | wc -l
```
Expected: `6`; no output from the second grep; `10` — ten `soul-*` directories (`soul-prompt` has shipped since 2026-08-12 and was missing from every hand-written count; the first draft of this step said "nine" and passed on a 10). The README number must equal this count.

- [ ] **Step 7: Commit**

```bash
git add docs/using-the-soul.md README.md
git commit -m "docs: the lifecycle page and README carry the development stage"
```

---

### Task 6: Version, changelog, regression

**Files:** Modify `.claude-plugin/plugin.json` · `SYSTEM-VERSION.md`

- [ ] **Step 1: plugin.json** — `"version": "2.1.1"` → `"version": "2.2.0"`

- [ ] **Step 2: SYSTEM-VERSION.md** — `Current: **2.1.1**` → `Current: **2.2.0**`, and insert this row directly under the table header (newest first):

```markdown
| 2.2.0 | 2026-08-26 | **The development stage — a declared answer to rule 7.** A project may now declare `prototype` / `pre-release` / `released` in its own CLAUDE.md through a new owner-invoked `/soul-stage`, which writes a ≤15-line block saying what may be broken and what must be kept; `/soul-init` offers it once with a skip; `/soul-resume` restates it; `/soul-next` re-reads its exit trigger. The contract gains one sentence: undeclared means released — protect what others may depend on and ask before breaking it. Nothing else changes: not the completion gate, not the hook, not the record's rules; each stage change is one witness entry and no other entry gains a field. **Why:** the owner supplied the same "no backwards compatibility, this is beta" rule by hand in two adopting projects on consecutive days (one surviving only in a witness narrative), while a third needs the inverse; the model's default is release-grade caution and the contract never said which project it was in (SOUL-I061; origin RSF cursor OWED UPSTREAM #11, with two carve-outs learned by running under the hand-written rule — SENSA-061/062, SENSA-064). **Designed by grill**, 24 questions; a seven-question screen was cut to one choice + two questions + a free line at the Body's push-back. **Placement of the model's proposal triggers moved after the grill** on a verified fact: `disable-model-invocation` skills are invisible to the model, so the triggers live in the block's last line, not the skill. **Unrun at cut — stated as an OVERRIDE per rule 8, not merely disclosed:** the Body chose release-first so every adopting project receives it at once; the live run on RSF follows the push (SOUL-181) and any defect becomes v2.2.1. SOUL-180 carries the override and the locked prediction. Spec: `docs/specs/2026-08-26-development-stage.md`. |
```

- [ ] **Step 3: Regression — the hook is untouched and must still hold**

```bash
python3 hooks/test_scope.py; echo "exit=$?"
```
Expected: the 11 cases pass; `exit=0`. (Nothing in this release touches `hooks/`; this proves the fence still holds under the changed `operations/CLAUDE.md`, which the marker list references by path.)

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/plugin.json SYSTEM-VERSION.md
git commit -m "release-prep: v2.2.0 — version, changelog row (unrun at cut — override stated at SOUL-180; live run at SOUL-181)"
```

---

### Task 7: Fresh-context review of the applied result (SOUL-179 — self-review is structurally blind)

**Files:** none modified until findings land

- [ ] **Step 1: Dispatch `diff-reviewer`** over `git diff main...v2.2.0`, with this brief — the claims are listed as "verify, do not trust":

> Review the applied diff of the Soul System branch `v2.2.0` against the spec `docs/specs/2026-08-26-development-stage.md` (read its "Resolved in grilling" table first). Verify, do not trust, each of these claims: (1) the `soul-stage` block template and the three presets match the spec's Q12–Q17 text verbatim; (2) the contract gained exactly one paragraph and no numbered rule, and `/soul-resume`'s step-0 sentinel is still unanswerable from the contract's new text; (3) `/soul-init` step 2b follows the `soul-stage` file rather than copying its text; (4) every surface that enumerates the instruments names `soul-stage` and no stale "eight" survives; (5) the skill never instructs the model to run itself and never writes outside cwd's CLAUDE.md; (6) the witness entry it prescribes uses the project's own code, never `SOUL-` outside this repo; (7) the block's proposal line carries triggers (i)–(iii) and the contract sentence carries (iv); (8) no file invents an incident — every cited event (SENSA-061/062/064, 2026-08-24/25, SOUL-F064) exists in the named records. Report defects with file:line; do not edit.

- [ ] **Step 2: Fix every confirmed finding in the files it names**, then re-run the checks from Tasks 1–6 that cover the touched file (Step 2/3 of Task 1, Step 2/3 of Task 2, Step 3 of Task 3, Step 5 of Task 4, Step 6 of Task 5, Step 3 of Task 6).

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "review: fresh-context findings on the v2.2.0 applied result"
```
(If the review found nothing, skip this commit and say so in SOUL-180.)

---

### Task 8: Release — witness SOUL-180 (override stated), merge, tag, push, plugin update

**Files:** `witness.md` (append SOUL-180) · git · the local plugin

Order changed at the Body's call (2026-08-26): release first, so every adopting
project receives it at once; the live run follows the push. `main` is the plugin's
distribution channel, so the merge IS the release, and the skill ships unexercised
— the same shape as v2.1.0/v2.1.1, where review caught the breakage both times
(SOUL-179). A019 says a GAP on the primary artifact blocks and disclosure is not a
permissible ending; the Body waived the pre-merge exercise explicitly. That is the
override, out loud (rule 8); SOUL-180 carries it.

- [ ] **Step 1: Confirm the next witness id is free (I027 re-read-verify)**

```bash
cd /mnt/d/Projects/Soul-System && grep -c "^ID: *SOUL-180" witness.md
```
Expected: `0`

- [ ] **Step 2: Append SOUL-180** — fill the bracketed field from what Task 7 actually found; leave nothing bracketed:

````markdown

```
ID:           SOUL-180
WHEN:         2026-08-26 / v2.2.0 — the development stage
WHERE:        skills/soul-stage/SKILL.md · operations/CLAUDE.md (one paragraph) ·
              skills/soul-init, soul-resume, soul-next, soul-help ·
              docs/specs/2026-08-26-development-stage.md
WHAT:         A project can now declare prototype / pre-release / released once, in
              its own CLAUDE.md, as a standing answer to rule 7; undeclared means
              released. SHIPPED UNEXERCISED, AS AN OVERRIDE STATED PER RULE 8: the
              Body chose release-first so every adopting project receives it at
              once, and declined serving the branch locally from the marketplace
              clone; the live run on RSF follows the push (SOUL-181) and any defect
              becomes v2.2.1. Fresh-context review of the applied result found
              [N findings — one line each, or "none"].
TYPE:         Build record + override + locked prediction
CONSEQUENCE:  LOCKED PREDICTION (mind item 1 — lean to carry, always write the
              miss direction): in RSF and RS Viewer, witness entries about
              shim/deprecation/compatibility churn FALL per entry over the next
              distill window. BASELINE WITH ITS METHOD (SOUL-I060): `grep -c -i -E
              "backwards?[- ]compat|\bshim\b|deprecat|legacy path|\balias(es)?\b|
              migration layer|preserv(e|ed|ing) (the )?old"` over each log on
              2026-08-25 gave 13 matching LINES in RS Viewer's 14-entry log and 8 in
              RSF's 64-entry log (line hits, not entries; a narrower keyword set
              gives 3 and 7). The number is method-bound: the check re-runs THIS
              regex and compares hits per entry. MISS DIRECTION: if it misses, the miss is
              over-deletion — a reader broken by a removed field, the SENSA-064
              class — not under-deletion. Check at the next /soul-distill of either
              project; record the result as a witness entry there and here.
STATUS:       Resolved — v2.2.0 tagged and pushed; live run PENDING, recorded at
              SOUL-181. Standing residual: the other five adopting projects sit at
              the absent-means-released default until their owners run /soul-stage;
              none forced. Next id: SOUL-181.
```
````

- [ ] **Step 3: Commit the entry on the branch**

```bash
git add witness.md
git commit -m "witness(SOUL-180): v2.2.0 — the development stage, shipped release-first (override stated); prediction locked"
```

- [ ] **Step 4: The mind.md 5(c) check — every commit on the branch, diff AND message, for real project/client names**

```bash
git diff main...v2.2.0 > /tmp/branch.diff; git log main..v2.2.0 --format='%H %s%n%b' > /tmp/branch.msgs
python3 - <<'PY'
import re
names={}
for line in open('registry/NAME-MAP.md',encoding='utf-8'):      # PRIVATE (gitignored) — never quote its names
    m=re.match(r'^\| (REF-\d+) \| (.*?) \|',line)
    if m:
        for n in m.group(2).replace('`','').split(','):
            if n.strip(): names[n.strip()]=m.group(1)
for label,path in (('DIFF','/tmp/branch.diff'),('MSGS','/tmp/branch.msgs')):
    hits=[(i,ref) for i,l in enumerate(open(path,errors='replace'),1) for n,ref in names.items() if re.search(re.escape(n),l,re.I)]
    print(label,'hits:',len(hits),[f'line {i}: {ref}' for i,ref in hits[:20]])
PY
```
Expected: `DIFF hits: 0` and `MSGS hits: 0`. The scan reads the private map (`registry/` is gitignored) and prints only REF ids, so it can be run and its output quoted without ever writing a name. RSF and RS Viewer are the owner's own public project names and are not in the map. *This step is not ceremony:* on 2026-08-26 it caught two map names the author had written into the spec and the idea entry in local commits; the branch was replayed from `main` before anything was pushed.

- [ ] **Step 5: Merge, tag, push** — authorised by the Body's "go straight to release":

```bash
git checkout main && git merge --no-ff v2.2.0 -m "merge: v2.2.0 — the development stage" && git tag v2.2.0 && git branch -d v2.2.0 && git push origin main refs/tags/v2.2.0
```
Expected: merge commit created, tag created, push accepted. **Push the tag by explicit refspec and delete the merged branch first:** with a branch and a tag both named `v2.2.1`, `git push origin main v2.2.1` failed as "src refspec matches more than one" (2026-08-26, SOUL-182). **Never `--tags`** — it pushes EVERY local tag: as first written this step used `--tags`, and on 2026-08-26 it also published `archive/video-pipeline`, a private archive of 10 unmerged video-pilot commits (0 private-map hits, but publishing it was never the owner's choice; a deleted ref does not delete the objects — mind 5(d)). Name the tag.

- [ ] **Step 6: Bring the local plugin to the released version**

```bash
claude plugin update soul-system@soul-system && ls ~/.claude/plugins/cache/soul-system/soul-system/
```
Expected: `2.2.0/` present, built from `origin/main`. The CLI says "restart required to apply" — the restart is Task 9 step 1.

- [ ] **Step 7: `/soul-handoff`** — NEXT STEP is Task 9 (the RSF run) verbatim, with its watch-for list; NEXT-SESSION FOCUS names both unexercised surfaces: this release's `/soul-stage`, and v2.1.1's `/soul-init` on dvs-nav (independent; neither discharges the other). OPEN BODY CALLS carry forward unchanged (F064's tension; SOUL-I060; the five projects on v2.0-era wiring).

---

### Task 9: The live run on RSF, after the release (A019 — the primary artifact gets its executor)

**Files:** RSF `CLAUDE.md` lines 52–76 (the `Phase: beta` line, the "Backwards compatibility is not required" paragraph and "The one carve-out" paragraph) · RSF `witness.md` (SENSA-065) · RSF `.soul/handoff.md` (OWED UPSTREAM #11) · Soul System `witness.md` (SOUL-181)

- [ ] **Step 1: Restart Claude Code.** Open a session in `/mnt/d/Projects/RealisticSensorsForge`.

- [ ] **Step 2: Sentinel — verify the executor (A019 check 0).** Run `/soul-help`. Expected: the command list, generated from `skills/` on disk, names `soul-stage`. The 2.1.1 cache has no such skill, so its absence means the old version loaded — re-run Task 8 step 6 and restart rather than proceed.

- [ ] **Step 3: Run `/soul-stage pre-release`** and answer the screen:
  - 1 (relied on from outside): `common/sensor_discovery.py (SensorInstance, discover_sensors) · src/rsviewer_provider.py (ADR 0008)`
  - 2 (next stage when): `a consumer beyond the viewer appears`
  - additions: `none — the "Bug Fixes & Code Structure" house rules below stay as they are`

  Watch for, specifically: the skill identifies the `**Phase: beta**` line as the legacy header and proposes to replace lines 52–55 and 64–76 **in place** (the `## Bug Fixes & Code Structure` heading, "Prefer the fix...", "Keep scope honest" and the per-bug checklist are stage-independent house rules and must survive); it shows the block before writing; the block lands where the Phase line was, not under the import at line 1; the witness draft uses `SENSA-065`, WHAT begins `Stage undeclared → pre-release` (a hand-written Phase block is not a declaration this skill made), TYPE `Decision — stage change`; nothing is appended before the owner's go.

- [ ] **Step 4: Verify the write by execution, not by the skill's report**

```bash
cd /mnt/d/Projects/RealisticSensorsForge
grep -n -E "^\*\*(Stage|Phase):" CLAUDE.md; grep -c "The contract's rules and the completion gate apply unchanged." CLAUDE.md; grep -n "^## Bug Fixes" CLAUDE.md; grep -n "^ID: *SENSA-065" witness.md
```
Expected: exactly one `**Stage: pre-release**` line and no `**Phase:` line; `1`; the house-rules heading still present; the SENSA-065 header present.

- [ ] **Step 5: Mark the upstream item delivered** — in RSF's `.soul/handoff.md`, OWED UPSTREAM #11, prepend `DELIVERED 2026-08-26 as Soul System v2.2.0 (/soul-stage) — ` to the item; leave the rest of the field untouched (thirteen other items still ride).

- [ ] **Step 6: Commit RSF's side, in RSF, by the owner's call** (`CLAUDE.md`, `witness.md`; the cursor is gitignored). Suggested message: `docs(record): CLAUDE.md Phase: beta → Stage: pre-release via /soul-stage (SENSA-065)`.

- [ ] **Step 7: Record the result upstream — SOUL-181** in the Soul System repo: what the run found, in the same shape as SOUL-179's "what the review found" paragraph. **If a defect:** fix it on a `v2.2.1` branch, merge, tag, push (the v2.1.1 pattern), and SOUL-181 names the defect and the patch. **If none:** SOUL-181 says so, and the "unexercised" residual closes for this surface (not for v2.1.1's init, which is still the cursor's other gate).

---

## Applied review findings (Task 7, 2026-08-26 — `diff-reviewer`, fresh context, 16 findings, all applied)

1. **False record claim** (spec ×2, ideas.md, SYSTEM-VERSION, soul-init): "survived only in a witness narrative" — the sub-deliverable's own nested `CLAUDE.md` carries the rule (verified at the path the witness names). Reworded everywhere to the true fact: two hand-written always-on copies, two wordings, no shared source.
2. **Legacy `Phase` range rule** would have swallowed RSF's house rules (heading + "fix the underlying issue" sit between the Phase line and the seams paragraph). Rewritten: only the Phase paragraph plus compatibility/seams paragraphs are the block; headings and other paragraphs stay; show line ranges.
3. **Instrument count**: ten, not nine — `soul-prompt` shipped 2026-08-12 and every hand count missed it. README, spec Task 5, soul-help list fixed.
4. **Step 2b bypass**: the "import already present" branch routed to steps 3–3c; now 2b–3c.
5. **Pre-assigned id**: the changelog no longer names SOUL-181; "the next witness entry after SOUL-180".
6. **`4 == 2` misdescribed** as a rename; it was a paired change made as if single-repo. Skill + spec.
7. **Baseline counts** now carry their regex and are stated as line hits, not entries.
8. **Trigger (i) in prototype**: the block's proposal line now names "adding a deprecation path, alias or shim" outright.
9. **Witness format deviation** (TYPE, three-sentence WHAT) now stated with its reason.
10. **Wrong anchor** in the name-scan note — fixed earlier on the replayed branch (registry is gitignored).
11. "≤15-line" → "about fifteen lines".
12. **Missing fallbacks**: absent `CLAUDE.md` / no anchor line / nested case — step 4 now says what to do.
13. `**Stage:**` literal → "a line starting `**Stage:`" in init, resume, next.
14. Screen text no longer says "block" before the owner has seen one.
15. Contract paragraph now offers `/soul-stage` to record the rule-7 answer (trigger iv explicit).
16. Lifecycle page's question order matches init's (register → stage → git).

---

## Verification ledger (rule 4 — what runs, what is handed forward)

| Claim | Verified by | Where |
|---|---|---|
| The skill text is what Claude Code loads | `/soul-help` lists `soul-stage` from disk (sentinel: 2.1.1 cannot) | Task 9 step 2 |
| The block lands in the right place and the legacy Phase block is replaced in place | `grep` on RSF's `CLAUDE.md` after the run | Task 9 step 4 |
| The transition entry is written with the project's own code | `grep "^ID: *SENSA-065"` | Task 9 step 4 |
| The hook still scopes under the changed contract | `python3 hooks/test_scope.py` exit 0 | Task 6 step 3 |
| The contract gained no numbered rule and the resume sentinel still works | `grep -c` of numbered rules = 10 | Task 2 step 3 |
| Every enumerating surface names the new skill; no stale count | the consistency sweep | Task 5 step 6 |
| Prose defects the author cannot see | `diff-reviewer`, fresh context, claims listed as "verify, do not trust" | Task 7 |
| The behavioural claim (churn falls) | **NOT verifiable at release** — locked prediction with miss direction, checked at the next distill | SOUL-180 (override stated); run result at SOUL-181 |
| `/soul-init` step 2b, `/soul-resume` step 3, `/soul-next` line | **UNRUN at release** — handed forward: the next `/soul-init` on dvs-nav (already the cursor's open gate) and the next resume in RSF exercise them | cursor |

---

## Self-review (done while writing; fix-in-place)

- Spec coverage: Q1–Q24 and every carried assumption map to a task (Q1/Q3/Q11/Q18/Q19-iv → Task 2; Q2/Q4/Q7/Q8/Q10/Q12–Q17/Q19-i–iii/Q20/Q21 → Task 1; Q5/Q21 → Task 1 step 5 + Task 4; Q6 → Task 6 step 3 (regression only); Q9 → Task 3; Q22 → Task 9; Q23 → Task 8 step 2; Q24 → Tasks 0/8; resume echo → Task 4; docs → Task 5).
- Placeholders: the only bracketed text is in SOUL-180 and is explicitly "fill from what happened" — it cannot be pre-written without inventing history (rule 2).
- Name consistency: the block's terminating line is identical in the skill template, step 1 of the skill, and Task 9 step 4's grep; the id `SOUL-I061`/`SOUL-180`/`SENSA-065` are each checked free before use; `2.2.0` appears in plugin.json, SYSTEM-VERSION, the tag, and the cache directory check.
- Deliberately not done: no change to `philosophy/the-soul.md` (the human book; a stage paragraph is a follow-up if the Body wants one); no `frozen` preset; no per-entry witness field; no hook change; no migration of the other five projects.
