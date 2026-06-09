# Soul System

A living philosophy and operational framework for human-AI collaborative work
in research, science, engineering, and coding.

Not a prompt collection. Not a workflow template. A craft tradition — principles
forged from real failure patterns, designed to make AI-assisted work more
principled and self-correcting.

<p align="center">
  <img src="architecture.svg" alt="Soul System role model (the full philosophy, consulted on demand): the Universe wraps the Body, which inhabits the Soul, Witness, Council, Judge, and Hands. The Council is a chamber of symbolic voices in tiers; the Hands sit beneath the Judge; the Panel of Experts sits parallel to the Witness, summoned when needed." width="100%">
</p>

*The Soul governs. The Witness and the Panel inform; the Council synthesises; the Judge decides; the Hands produce — the full role model, consulted on demand. 1.0 keeps the always-on surface lean: a one-paragraph roster in the seed, with this depth in `philosophy/`.*
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

That installs the always-on **doctrine**. Edits to the philosophy propagate immediately to every project that imports it. For the `/soul-*` commands and the verification hook, add the plugin (below).

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
philosophy/     The Soul — the full philosophy, consulted on demand
operations/     The operational seed — imported by @ into your project's CLAUDE.md
commands/       Slash commands — eight /soul-* instruments (see commands/)
hooks/          Activation instruments — the pre-completion Stop hook + plugin hooks.json
amendments/     Amendments to the Soul, by lifecycle state (accepted/proposed/returned)
findings/       Findings, open/ and closed/
witness.md      The repo's own Witness log (what happened, backward)
ideas.md        The idea inbox (what might, forward) — graduates into findings/
mind.md         Optional project layer — compressed rule-set distilled from the record
docs/           Live design specs + study/ (the measurement behind 1.0); historical provenance under docs/archive/
skills/         Upstream skills — project-proven, submitted for cross-project reuse
.claude-plugin/ Plugin + marketplace manifests (install the /soul-* commands + hook)
AGENTS.md       Cross-vendor entry point for any agent tool
```

---

## Governance · Contributing · License

See `GOVERNANCE.md`, `CONTRIBUTING.md`, and `LICENSE` (MIT).

*The philosophy evolves. That is the point.*
