# CLAUDE.md — Project contract (Soul, 2.0)

This project keeps a durable record and verifies its claims. The working rules:

1. **Record decisions where future pressure will arrive** — at the code site, with
   the reason, and as a test that fails if the decision is broken, where the medium
   allows.
2. **Never invent history.** No incidents, reviewers, or past events that did not
   happen. A rule without a real incident stands bare — that is fine.
3. **Absolute claims need an external anchor.** Say why the anchor is trusted and
   what would make it wrong. Mark unknowns as unknown rather than filling them.
4. **Nothing is done until verified by execution.** If you cannot run it, name
   exactly what is unrun and hand it forward. A Stop hook enforces this at session
   end.
5. **Capture what a later session cannot re-derive before this one ends** —
   `/soul-capture idea|witness|finding`. The derivable regenerates on its own; the
   unguessable dies with the session. Where capture instruments are unavailable
   (automated/headless sessions write no record files), force-comments at the code
   site and the handoff document ARE the record.
6. **Resume from `.soul/handoff.md`; leave an updated cursor behind**
   (`/soul-resume`, `/soul-handoff`).
7. **When the right choice depends on knowledge only the owner has** — intent,
   preference, private context — **ask**; do not push harder on available evidence
   as a substitute.
8. **Overrides happen out loud.** When urgency wins over a rule, say so explicitly
   — never silently.

**Stores** (at THIS project's root, never the Soul System source repo):
`witness.md` (append-only, sequential IDs, re-read before appending) · `ideas.md` ·
`findings/` · `amendments/`. Forward view: `/soul-next`. Maintenance:
`/soul-distill` (propose it when the record has grown; the owner confirms —
it keeps this page within budget).

**Projects importing this contract** owe their Soul-System-level lessons upstream:
a closing note at milestones, and observations about how this system itself behaved
(gates, instruments) sent home to the Soul System repo's `findings/`. Domain
lessons stay home.

The thinking behind this system — its history, roles, and the measurements that
shaped it — lives in `philosophy/the-soul.md`. It is written for human readers;
sessions need only this page.
