---
name: soul-stage
description: Declare or change the project's development stage — prototype, pre-release, or released — and write the short block of rules that follows from it into the project's CLAUDE.md, beside the Register line. Owner-invoked only; each change is one witness entry. Run with no argument to see the current stage; re-run with the current stage to refresh the block.
disable-model-invocation: true
---

# /soul-stage — say what may be broken and what must be kept

`/soul-stage` shows the current stage — a look, nothing more.
`/soul-stage <prototype|pre-release|released>` sets or changes it; the current stage refreshes it.

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

**Ask it through the harness's question prompt** (`AskUserQuestion`) whenever that
tool is available — one call, the items below as its questions: the stage as three
selectable options carrying the one-line descriptions, the chosen preset first and
marked recommended; question 1 as *Nothing* / *Let me list them* (the owner types the
list); question 2 as *First outside user* / *A v1.0 tag* / *Not sure yet* (or their own
line); the additions as *None* (or their own line). Skip question 1 for prototype; for
released, *Nothing* is not an answer — ask again. Fall back to the prose screen below
only when the prompt is unavailable (a `claude -p` run). Pre-fill from an existing
block only; never draft the owner's answers for them beyond the preset's defaults — the
first live run pre-filled question 1 with a paragraph of this repo's internals, the
opposite of approachable (the Body's test, 2026-08-26).

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
> **Anything to change or add?** *(optional — recorded as your additions)*

*Why only this much:* the stage the owner picks already answers who uses the code,
how settled the design is, and what a change ships with — the preset carries those.
Question 1 is the one fact no preset can know: a change on one side of a published
seam, made as if it were single-repo, doubled every sensor in the downstream viewer's
panel until that viewer's own suite failed `4 == 2` (an adopting project, 2026-08-24). Question 2 is the exit
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
  a release is cut, a rule above is about to be overridden, or you find yourself
  adding a deprecation path, alias or shim — one sentence, then wait; only the
  owner changes the stage.
The contract's rules and the completion gate apply unchanged.
```

For `prototype` the "Relied on from outside" line reads `nothing — nothing is
promised`. The last bullet is where the model's proposal triggers live: this skill
is invisible to the model by design, so the always-on block has to carry them.

## What to do

1. **Find the existing block.** Read `CLAUDE.md` in the directory the session
   started in (do not search upward). The block runs from a line starting `**Stage:` through the line
   `The contract's rules and the completion gate apply unchanged.` A line starting
   `**Phase:` from before this skill existed counts as the header of a hand-written
   block. What that block covers is only: the Phase paragraph itself, plus any later
   paragraph that states a compatibility rule or names the published seams. Every
   heading and every other paragraph — house rules, checklists — stays exactly where
   it is, even when it sits between those paragraphs. Show the owner the exact line
   ranges you intend to replace before doing it. If a block exists, show its stage, date, relied-on list, trigger and
   additions.
   - **No argument: look only.** Report the stage, date, relied-on list and trigger
     if a block exists — or "no stage declared; treated as released" — and one hint:
     `/soul-stage <prototype|pre-release|released>` to declare, `/soul-stage <the
     current stage>` to refresh. Then stop. Do not open the screen: a look is not a
     declaration, and the first live run answered a look with the full screen and a
     drafted proposal (2026-08-26). **Argument equal to the current stage:** refresh —
     rewrite from the current preset, keeping the owner's three answers.
2. **Ask the screen** (the prompt, or the prose fallback): preset from the argument,
   pre-selected; answers 1, 2 and the additions from the existing block if there is
   one, otherwise the preset's defaults and nothing more. Wait for the owner. Check:
   `released` needs a non-empty answer to question 1 — ask again rather than write
   an empty public contract.
3. **Compose the block** from the template and show it. Wait for go / edit / cancel.
4. **Write it:** replace the existing block in place, or insert it directly under
   the `**Register:**` line, or — with no Register line — directly under the last
   `@` import line. If `CLAUDE.md` is absent, or has neither (the import may live in
   `.claude/CLAUDE.md`), put the block at the top of `CLAUDE.md`, creating the file
   if needed, and say so. Touch nothing else in the file. A sub-deliverable's own
   block is written by a session started in that directory; this skill never
   searches upward or downward.
5. **Record the transition** — one witness entry, following `/soul-capture
   witness`'s rules (this project's code from the log header, next id, re-read
   before appending, never `SOUL-` outside the Soul System repo):
   - WHEN: today · WHERE: `CLAUDE.md`, the Stage block
   - WHAT: `Stage <previous stage, or "undeclared"> → <new stage> (owner, <date>).
     Why: <the owner's words>. Changed: <what differs from the previous block —
     the relied-on list, the trigger, the additions — or "first declaration">`
   - TYPE: `Decision — stage change` — not in the format's original list; the logs
     already carry free-form TYPEs ("Build record"), and this names what happened ·
     CONSEQUENCE: the preset's headline rule now applies (e.g. "no backwards
     compatibility beyond two named surfaces") · STATUS: `Resolved`. WHAT runs to
     three sentences on purpose: the why is the unguessable part.
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
(v2.2.0). **Amended:** 2026-08-26 (v2.2.1) — the screen is asked through the harness's
question prompt, and a bare `/soul-stage` only looks; both from the first live run, the
Body's test on this repo (SOUL-181). **Status:** active.
