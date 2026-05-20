# Soul System

A living philosophy and operational framework for human-AI collaborative work
in research, science, engineering, and coding.

Not a prompt collection. Not a workflow template. A craft tradition — principles
forged from real failure patterns, designed to make AI-assisted work more
principled and self-correcting.

<p align="center">
  <img src="architecture.svg" alt="Soul System architecture: the Universe wraps the Body, which wraps the Soul, Witness, Council, and Judge. The Council is a chamber of twelve symbolic voices in tiers. The Hands sit beneath the Judge; the Panel of Experts sits parallel to the Witness, summoned when needed." width="100%">
</p>

*The Soul governs. The Witness and the Panel inform; the Council synthesises; the Judge decides; the Hands produce.*
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

That is the entire install. Edits to the philosophy propagate immediately to every project that imports it.

---

## Alternative: Snapshot Install

If you prefer a self-contained snapshot copied into the project (no upstream dependency, no auto-updates):

```bash
./install.sh /path/to/your/project
```

This copies `operations/` into the project and records the system version.

---

## Other Agent Tools

`AGENTS.md` at the repo root is a cross-vendor convention (Cursor, Aider, OpenAI Codex, Gemini CLI, Jules, Zed, others) that points any agent tool at the right entry points. Soul-following projects are legible to any tool that reads `AGENTS.md`.

---

## Start

1. Read `philosophy/the-soul.md` — once, slowly, before anything else.
2. Open a session in your project.
3. State the problem at two levels (the Frame gate). The session continues from there.

---

## After Your Run

Read the Witness log. Not the output — the log.
If you found something worth sharing, see `CONTRIBUTING.md`.

---

## Structure

```
philosophy/     The Soul, the Commons (outside wisdom that earned its place)
operations/     The operational seed — imported by @ or copied by install.sh
commands/       Slash commands (/soul-init, /soul-verify, /soul-expand, /soul-idea)
hooks/          Activation instruments (e.g. the pre-completion Stop hook)
amendments/     Council Amendments to the Soul, by lifecycle state (accepted/proposed/returned)
findings/       Council Findings, open/ and closed/
witness.md      The repo's own Witness log (what happened, backward)
ideas.md        The idea inbox (what might, forward) — graduates into findings/
docs/           Design specs and proposals
skills/         Role activations — built through use
registry/       Where the system has been used
logs/           Contributed Witness logs
AGENTS.md       Cross-vendor entry point for any agent tool
install.sh      Snapshot installer (alternative path)
```

---

## Governance · Contributing · License

See `GOVERNANCE.md`, `CONTRIBUTING.md`, and `LICENSE` (MIT).

*The philosophy evolves. That is the point.*
