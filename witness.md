# The Soul System Witness Log

The Witness records what happens during the Soul System's own development.

This log follows `operations/witness-log-format.md`. Entries are factual,
terse, and never deleted — resolved entries are marked Resolved.

Project code: `SOUL`.

---

## Entries

```
ID:           SOUL-001
WHEN:         2026-05-19 / Dogfood pass on README update
WHERE:        Repo root — missing CLAUDE.md
WHAT:         Soul System repo had no root CLAUDE.md to load operations/CLAUDE.md
              via @-import. Sessions opened in the repo did not auto-load the philosophy.
TYPE:         Obligation Skipped — Soul System failed to apply its own @-import
              workflow to itself.
CONSEQUENCE:  Self-dogfood blocked until fix. One-line CLAUDE.md added.
STATUS:       Resolved
```

```
ID:           SOUL-002
WHEN:         2026-05-19 / Dogfood pass on README update
WHERE:        philosophy/the-soul.md > The Architect section
WHAT:         Architect description used code-shaped language (modules, interfaces, files)
              implying code-only scope. Documentation and repository structural decisions
              had no named home.
TYPE:         Felt Wrong — doctrine implied a narrower scope than actually held.
CONSEQUENCE:  Clarifying sentence added covering documentation organization and
              repository layout.
STATUS:       Resolved
```

```
ID:           SOUL-003
WHEN:         2026-05-19 / Dogfood pass on README update
WHERE:        Multiple files — per-file Version footers, SYSTEM-VERSION.md, install.sh
WHAT:         Version markers existed in three places (per-file Version 1.0/1.1,
              SYSTEM-VERSION.md, install.sh). They drifted — SYSTEM-VERSION.md at
              0.1.2 while today's session added significant changes.
TYPE:         Felt Wrong — duplication created drift risk.
CONSEQUENCE:  Per-file versions removed. SYSTEM-VERSION.md bumped to 0.2.0, established
              as single source. install.sh synced.
STATUS:       Resolved
```

```
ID:           SOUL-004
WHEN:         2026-05-19 / Dogfood workflow setup
WHERE:        ~/.claude/commands/soul-init.md
WHAT:         /soul-init slash command hardcodes Soul System path to
              /mnt/d/Projects/Soul-System. Other machines need manual edit.
TYPE:         Council Note — Steward (machine-portability of dogfood tooling)
CONSEQUENCE:  Not blocking. An env var ($SOUL_SYSTEM_ROOT) would resolve it; the
              pattern earns its place when a second machine actually adopts the workflow.
STATUS:       Open
```

```
ID:           SOUL-005
WHEN:         2026-05-19 / Decision 5 framing
WHERE:        Conversation — user-stated future possibility
WHAT:         Caveman-style Council summaries to the user. When the Council convenes,
              the user receives a 3-5 line dense digest; full deliberation lives in
              linked artifacts (findings/, amendments/, ADRs).
TYPE:         Council Note — Advocate (user experience of Council outputs)
CONSEQUENCE:  Captured. Depends on findings/ + witness.md existing as artifacts.
STATUS:       Open
```

```
ID:           SOUL-006
WHEN:         2026-05-19 / Decision 5 framing
WHERE:        Conversation — user-stated future possibility
WHAT:         Post-project analysis as a named Council convening mode — mining the
              accumulated record (Witness log + Findings + Amendments + ADRs + in-code
              markers) for project-level retrospective. Distinct from Pre-Mortem;
              this is Post-Mortem.
TYPE:         Council Note — Prophet, Cartographer (named convening mode candidate)
CONSEQUENCE:  Captured. Could become a third named Council mode after Pre-Mortem
              earns its place through use.
STATUS:       Open
```

```
ID:           SOUL-007
WHEN:         2026-05-19 / Decision 5 framing
WHERE:        Conversation — user-stated future possibility
WHAT:         Visual session map — dots-on-circle or Warcraft-style agent-activity
              view showing which role is active when and where user intervention is
              needed. UX layer for observing the Soul System operating in real time.
TYPE:         Council Note — Artificer (instrument), Advocate (user observation)
CONSEQUENCE:  Captured. Far downstream of current dogfood phase.
STATUS:       Open
```
