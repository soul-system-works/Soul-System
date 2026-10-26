# Soul System

A project memory and a "done" check for AI coding sessions, in Claude Code
(and Codex, as a preview).

Every new AI session starts without the decisions made before it, the reasons
behind them, or what was half-finished, and a session will say "done" without
having run anything. The Soul keeps a short record in your project and checks a
"done" claim before it reaches you.

<p align="center">
  <img src="docs/media/handoff-resume.gif" alt="Animation: a session ends before the work does; /soul-handoff writes .soul/handoff.md (where we are, next step, pointers); the next session runs /soul-resume and continues with nothing re-derived." width="100%">
</p>

## Install

In Claude Code:

```
/plugin marketplace add soul-system-works/Soul-System
/plugin install soul-system@soul-system
```

Then, in your project:

```
/soul-init
```

The first run asks a few questions (where the record lives, how settled the
project is) and remembers the answers in `.soul/init.md`. Run it again any time:
it says what is set, repairs what broke, and asks only what is new.

## What you get

- **One page of rules the AI reads**: ten rules, such as "nothing is done until
  it is verified by running it" and "never invent history". `/soul-init` links the page into your
  project, so it updates with the plugin.
- **A record in your project**: `.soul/witness.md` (what happened, and why),
  `.soul/ideas.md` (what might), and later `mind.md` (the few facts a new session
  cannot work out for itself).
- **A completion gate**: a hook that stops a session from ending on an unverified
  "done".
- **A secret guard** (experimental): checks the AI's commits for credentials
  (with gitleaks installed) and for names you list as private.

| Command | When |
|---|---|
| `/soul-init` | Once per project; again any time to check and repair |
| `/soul-resume` | Starting a session: pick up where the last one stopped |
| `/soul-handoff` | Ending a session: leave the next one a note |
| `/soul-capture` | Keep an idea, or a record of what happened |
| `/soul-next` | What to do next, from the record |
| `/soul-discuss` | Test an idea against rivals and objections before building it |
| `/soul-explain` | Explain where things stand, without deciding anything |
| `/soul-distill` | Compress a grown record into `mind.md` |
| `/soul-stage` | Declare prototype, pre-release or released |
| `/soul-prompt` | Turn a rough prompt into a clear one |
| `/soul-delegate` | Send routine plan steps to another model; checks still run here |
| `/soul-migrate` | Move a project to another computer |
| `/soul-help` | A short tour |

In Claude Code the commands carry the plugin's name: `/soul-system:soul-capture`.
Keeping every project's record in one private repo: the
[Soul vault](docs/adr/0001-soul-vault.md). Day to day, who does what:
[`docs/using-the-soul.md`](docs/using-the-soul.md).

## Does it help?

We measured it. On current models it does not make the work itself better:
quality tied whether a session had the Soul, a careful `CLAUDE.md`, or a
five-minute one. What changes is what carries between sessions.
A decision written in the record stopped a later session from undoing it (5 of 5
sessions without the record drifted, 0 of 5 with it), and the strongest model
drifted too when the record was missing. Method, results and what is still open:
[`docs/study/`](docs/study/06-bounds-and-open-questions.md).

## Codex (preview)

From a clone of this repo:

```bash
codex plugin marketplace add /absolute/path/to/Soul-System
codex plugin add soul-system@soul-system-codex
```

Restart Codex, open your project and run `$soul-system:soul-init`. It adds a
managed block to `AGENTS.md` and uses the same record as Claude Code. Trust the
plugin's hooks in Codex before relying on the gate; installing alone does not
turn them on. Tested on the Codex CLI only. Details and limits:
[`operations/codex.md`](operations/codex.md).

## The philosophy

The rules came out of a longer book for people, `philosophy/the-soul.md`, with
names for the perspectives careful work takes (the Witness, the Council, the
Judge). The AI never reads it; it is there when you want the why.

<p align="center">
  <img src="architecture.svg" alt="The Soul System role model: the Universe wraps the Body (the human), who inhabits the Soul, Witness, Council, Judge and Hands." width="80%">
</p>

## Contributing

Clone the repo to a stable place and point your skills at the clone (a symlinked
skills folder); `/soul-init` then writes each project's import against the clone,
so your edits to the rules reach every project at once.

```
operations/   The page of rules the AI reads (operations/CLAUDE.md)
skills/       The /soul-* commands
hooks/        The completion gate, the secret guard, plugin hooks
tools/        Scripts the commands run (vault, line endings, layout, migrate)
philosophy/   The book for people
docs/         Specs, decisions (adr/), the study
witness.md, ideas.md, mind.md   This repo's own record
amendments/, findings/          Changes to the Soul and the evidence for them
```

`AGENTS.md` points other agent tools (Cursor, Aider, Gemini CLI, Zed) at the
same entry points. See `CONTRIBUTING.md`, `GOVERNANCE.md` and `LICENSE` (MIT).
