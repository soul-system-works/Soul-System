# Soul System

A living philosophy and operational framework for human-AI collaborative work
in research, science, engineering, and coding.

Not a prompt collection. Not a workflow template. A measured system: **one plain
page the AI reads** (about ten rules), **four instruments with teeth** (a capture
command, a completion gate, a handoff, a distiller), and **a book for humans**
(the philosophy that produced them). 2.0 is the shape the measurements left
standing — two days of pre-registered twin-chain experiments showed the frontier
model has absorbed this system's reasoning core; what it still cannot do is keep
its project history honest or carry what it learned across sessions. So that is
what the system does: a conscience and a notebook.

<p align="center">
  <img src="architecture.svg" alt="Soul System role model (the full philosophy, consulted on demand): the Universe wraps the Body, which inhabits the Soul, Witness, Council, Judge, and Hands. The Council is a chamber of symbolic voices in tiers; the Hands sit beneath the Judge; the Panel of Experts sits parallel to the Witness, summoned when needed." width="100%">
</p>

*The role model above is the **human-facing** layer since 2.0: names for perspectives
that arise naturally in careful work, kept as a reading lens and a record vocabulary.
The AI reads one page (`operations/CLAUDE.md`); people read `philosophy/the-soul.md`.*
*The Body — the human — inhabits all of it and bears responsibility for the whole.*

**Composes, does not replace.** The Soul System layers above how you already work — BMAD, TDD, Cursor Rules, your own conventions. Adopt what helps. Ignore what does not.

---

## Quick Start

Clone the Soul System repo to a stable path on your machine, once.

In any project you want to bring under the Soul, create a `CLAUDE.md` with one line:

```
@/path/to/Soul-System/operations/CLAUDE.md
```

Or run `/soul-init` from a Claude Code session in the project — the slash command writes that line for you.

That installs the always-on **contract** — one page. Edits propagate immediately to every project that imports it. `/soul-init` also asks one register question (plain or fluent language; plain is the default). For the `/soul-*` commands and the verification hook, add the plugin (below).

---

## Add the instruments (plugin)

The `@import` above brings the always-on **doctrine**. The **commands** (`/soul-*`) and the
**pre-completion verification hook** ship as a Claude Code plugin:

```
/plugin marketplace add soul-system-works/Soul-System
/plugin install soul-system@soul-system
```

Commands are namespaced under the plugin (e.g. `/soul-system:soul-capture`). The doctrine seed
and the instruments **compose**: the seed is the always-on lifetime layer, the plugin is the
tooling. Adopt the seed alone, the plugin alone, or both.

---

## Other Agent Tools

`AGENTS.md` at the repo root is a cross-vendor convention (Cursor, Aider, OpenAI Codex, Gemini CLI, Jules, Zed, others) that points any agent tool at the right entry points. Soul-following projects are legible to any tool that reads `AGENTS.md`.

---

## Start

1. Open a session in your project — the contract page is all the AI needs.
2. When you want to understand *why* the system is shaped this way, read
   `philosophy/the-soul.md` — it is written for you, not the model.
3. The honest claims ledger — what this will and will not do for you, each
   anchored to a measured result — is in `docs/study/blog-release.md`.

---

## After Your Run

Read the Witness log. Not the output — the log.
If you found something worth sharing, see `CONTRIBUTING.md`.

---

## Structure

```
philosophy/     The Soul — the human-facing book (the AI does not read this)
operations/     The contract page — imported by @ into your project's CLAUDE.md
skills/         The eight /soul-* instruments, as Claude Code skills (invoked /soul-capture, …)
hooks/          Activation instruments — the pre-completion Stop hook + plugin hooks.json
amendments/     Amendments to the Soul, by lifecycle state (accepted/proposed/returned)
findings/       Findings, open/ and closed/
witness.md      The repo's own Witness log (what happened, backward)
ideas.md        The idea inbox (what might, forward) — graduates into findings/
mind.md         Optional project layer — project notes distilled from the record (unguessables only)
docs/           Live design specs + study/ (the measurements behind 1.0 and 2.0); historical provenance under docs/archive/
.claude-plugin/ Plugin + marketplace manifests (install the /soul-* skills + hook)
AGENTS.md       Cross-vendor entry point for any agent tool
```

---

## Governance · Contributing · License

See `GOVERNANCE.md`, `CONTRIBUTING.md`, and `LICENSE` (MIT).

*The philosophy evolves. That is the point.*
