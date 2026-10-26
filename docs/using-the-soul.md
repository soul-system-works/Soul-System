# Using the Soul System — what it actually looks like

You work the way you already work. The system is one page of rules the AI reads,
plus a notebook your project keeps. This page is the whole lifecycle; every link
goes deeper.

The walkthrough below describes Claude Code. For the experimental Codex path,
see [the Codex preview](../README.md#codex-preview-experimental) and
[host integration](../operations/codex.md); use `$soul-system:soul-*` invocation there, and
verify hook trust and operation before relying on automatic completion reminders.

## Day one

Run `/soul-init` in your project. The first time, it asks where the record lives
(in git is the default), how settled the project is (prototype, pre-release,
released, or *Not now*, which means "treat it as released") and whether any names
must stay out of the repo, then offers a few safety checks in one list. It writes
one import line into your `CLAUDE.md`, creates two empty record files,
`.soul/ideas.md` and `.soul/witness.md`, and keeps your answers in `.soul/init.md`.
Running it again asks only what is new; `/soul-init revisit` asks everything
again. If your project already keeps its record at its root, it stays there; both
layouts work.

Findings and amendments are NOT created locally. Those are records of changes to
the Soul System itself and live upstream; anything your project learns about the
system is appended to an `upstream.md` file beside your other records. That file is
created the first time there is something to put in it — if your project never has
one, you will never see it, and nothing will ask you about it.

**Upgrading from before v2.3.0?** Earlier versions kept these notes in an `OWED
UPSTREAM` field inside `.soul/handoff.md`. The first `/soul-handoff` after the upgrade
moves that field's contents into `upstream.md` before replacing the cursor. If you want
to check it by hand first, the field is in your current `.soul/handoff.md`.

That's the install. There is no new workflow to learn — start working.

## Every session

**What happens by itself** (you'll see these; you don't trigger them):

- The contract loads — about ten rules: verify before claiming done, never invent
  history, record decisions where they'll be tested.
- When the AI hits something a later session couldn't figure out on its own — a
  decision with a non-obvious reason, a gotcha, an arbitrary convention — it
  **proposes** recording it: "worth capturing?" You say yes or no. Nothing is
  written without your yes.
- When a session tries to finish, the **completion gate** fires: work that nothing
  verified can't be called done; the session must name exactly what is unrun.

**What you do:**

- Answer the proposals (a yes or a no is the whole job).
- Start a session with `/soul-resume` (picks up where the last one left off) and
  end one with `/soul-handoff` (leaves the cursor for the next). Ask "what's
  next?" with `/soul-next`.
- Explore an idea before building it: `/soul-discuss` — the AI sets rivals beside
  it, gives the strongest objection first, scans a few sources, and, on your
  yes, keeps the result in the idea's entry. `/soul-next` reminds you when an idea is still
  undiscussed.
- Capture directly when you want to: `/soul-capture idea` (a forward thought,
  near-zero ceremony) · `/soul-capture witness` (something that happened) ·
  `/soul-capture finding` (a pattern your project has earned — this one is
  **yours alone**; the AI never promotes a finding by itself).
- Overrule anything. When urgency beats a rule, the rule is set aside out loud —
  and that's your call to make.

## Over time

The notebook grows. When it has grown enough (roughly 15+ entries, or a finding
closes), the AI proposes `/soul-distill`: it compresses what the project has
learned into `mind.md` — **the Mind**, a short always-on page carrying only what
an AI couldn't re-derive on its own. You review the draft; nothing is committed
without you. Many projects never need one; the proposal arriving is how you find
out yours does.

**Declaring a stage.** When the project's situation changes — the first outside
user, a v1.0, or the day you decide the prototype is now the real thing — run
`/soul-stage` and pick a stage (or `/soul-stage <stage>` directly). Then one short
prompt: name anything outside the project that relies on part of it, and say what
would move it to the next stage. It writes a short block into your `CLAUDE.md` saying what may be
broken and what must be kept, and records the change as one entry. Undeclared
projects are treated as released: nothing is broken without asking you.

**Where AI working files go.** Plans, drafts, review output, eval results and
scratch go in `.ai/` at the project root — created when first needed and safe to
delete or archive at a milestone. `.soul/` holds the small permanent record; your
code, tests and docs stay where they are. Moving a working file into your docs is
your decision. If an older project has plans or review dumps scattered in the root
or `docs/`, re-running `/soul-init` lists them and offers to move each group —
declining changes nothing and it won't ask again.

**Alongside other plugins.** Soul runs alongside skill plugins such as superpowers.
Where the two disagree on a path — superpowers saves plans to
`docs/superpowers/plans/` — Soul's `.ai/` rule wins, and the AI says it is
overriding the other skill's default rather than doing it silently. Measured once,
on Sonnet, with three sessions per setup: a plan saved with superpowers alone went
to `docs/superpowers/plans/` every time; with Soul added, every plan went to `.ai/plans/`
and named the override (witness SOUL-211). Not yet run: other models, other
plugins, or a path conflict other than plans.

**Handing work to other models (optional).** When a plan has routine steps that a
command can check — tests, a build — type `/soul-delegate`. Each step then carries
`Tier:` (who does it) and `Done when:` (the command that proves it). The AI can hand
routine steps to a local model, Codex or a smaller Claude, and it **runs every check
itself** and records the result, so a step is never marked done on the other model's
word. `/soul-delegate off` stops it; `/soul-delegate tiers` changes who does what.
Skip it for design work or anything you can only judge by reading.

**Moving to another computer.** In each project, run `/soul-init` (it tidies the
layout), then `/soul-migrate`. One round of questions and one summary box later you
have a zip holding what git does not carry — gitignored records, `.ai/`, untracked
files, unpushed branches, uncommitted work, the project's Claude memory. On the new
computer, run `/soul-migrate receive <zip>`: it checks every file, restores the
project without overwriting anything, rebuilds, and runs one check. Settings that
belong to no project (`~/.claude`, `~/.codex`) move by hand.

**Line endings.** When a Windows git (or Sourcetree) and WSL git share one checkout,
Windows writes files with Windows line endings and WSL then sees every file as
changed. `/soul-init` checks for this and offers a one-time fix as its own commit:
a `.gitattributes` rule so the repo decides, not each machine
(`python3 <soul-system>/tools/eol.py check .` to look yourself).

**Keeping every record in one private place.** A Soul vault is one private git repo
that holds the record of every project, each in its own folder; the project keeps a
`.soul` link into it, so the commands work as before (the next session asks once
to load files from outside the project — approve it). Make the repo (private) and clone it
— on WSL, onto a Windows drive — then run
`python3 <soul-system>/tools/vault.py init <clone> --register` once per machine.
From then on `/soul-init` offers "in the vault" beside "in git" and "local". A
`restricted` project never goes in. A new computer: clone the vault to the same
place, then `/soul-init` in each project re-links its record. Why and how:
[ADR 0001](adr/0001-soul-vault.md).

## Going deeper

| Want | Read |
|---|---|
| Any command in full | `skills/<name>/SKILL.md` (e.g. [`soul-capture`](../skills/soul-capture/SKILL.md), [`soul-stage`](../skills/soul-stage/SKILL.md), [`soul-distill`](../skills/soul-distill/SKILL.md), [`soul-init`](../skills/soul-init/SKILL.md)) |
| The page the AI actually reads | [`operations/CLAUDE.md`](../operations/CLAUDE.md) |
| Why the system is shaped this way | [`philosophy/the-soul.md`](../philosophy/the-soul.md) |
| What it will and won't do (measured) | [`docs/study/blog-release.md`](study/blog-release.md) |
| In a session | `/soul-help` |

---

**Source:** Built at the Body's ask after the 2.0 ship (witness SOUL-168 session) —
the lifecycle view the README and the book don't carry: who does what, and when.
**Status:** active; the README links here after Quick Start.
