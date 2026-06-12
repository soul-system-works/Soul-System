# Using the Soul System — what it actually looks like

You work the way you already work. The system is one page of rules the AI reads,
plus a notebook your project keeps. This page is the whole lifecycle; every link
goes deeper.

## Day one

Run `/soul-init` in your project. It asks one question (plain or fluent language —
plain is the default), writes one import line into your `CLAUDE.md`, and creates
empty record files (`ideas.md`, `witness.md`, `findings/`).

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

## Going deeper

| Want | Read |
|---|---|
| Any command in full | `skills/<name>/SKILL.md` (e.g. [`soul-capture`](../skills/soul-capture/SKILL.md), [`soul-distill`](../skills/soul-distill/SKILL.md), [`soul-init`](../skills/soul-init/SKILL.md)) |
| The page the AI actually reads | [`operations/CLAUDE.md`](../operations/CLAUDE.md) |
| Why the system is shaped this way | [`philosophy/the-soul.md`](../philosophy/the-soul.md) |
| What it will and won't do (measured) | [`docs/study/blog-release.md`](study/blog-release.md) |
| In a session | `/soul-help` |

---

**Source:** Built at the Body's ask after the 2.0 ship (witness SOUL-168 session) —
the lifecycle view the README and the book don't carry: who does what, and when.
**Status:** active; the README links here after Quick Start.
