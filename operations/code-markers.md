# Code Markers

The Craftsman's duty of in-code honesty.

The code is the document. Compromise and non-obvious context live where they live —
not in a separate file that will go stale. This file anchors the vocabulary.
The markers do the work.

---

## The Five Markers

**`TODO`** — work not yet done. The present state is intentional; the future state is known.

**`FIXME`** — a known defect in working code. Bug identified, not yet repaired.

**`DEBT`** — a corner knowingly cut. The code is correct; the structure was compromised to ship.

**`HACK`** — ugly-but-functional. Works for reasons that do not generalize.

**`NOTE`** — a non-obvious assumption a future reader would otherwise miss.
Not a flag of compromise — a flag of context.

---

## Rules

**A bare marker is a failure.** Every marker carries a description.
`// TODO` is not a marker. `// TODO: validate input against the schema` is.

**One marker per concern.** Do not stack intents into one comment.

**`DEBT` names what was cut and what would make it unsafe.**
`// DEBT: skipping validation here — the upstream check is sufficient. If that changes, this breaks.`

**`FIXME`, `DEBT`, and `HACK` each require a Witness entry.**
`TODO` and `NOTE` may stand alone — they record deferred work or context.
The other three are stop-and-surface obligations met by marking rather than stopping;
each must have a corresponding Witness entry with `WHERE` pointing to the file
and line where the marker lives.

---

## When Using Source Control

Commits follow Conventional Commits — the same spirit as in-code markers, applied to git history.

**Format:** `<type>(<scope>): <description>`

Types:
- **`feat`** — a new feature
- **`fix`** — a bug fix
- **`refactor`** — code change that neither fixes a bug nor adds a feature
- **`docs`** — documentation only
- **`test`** — adding or correcting tests
- **`style`** — formatting, whitespace
- **`perf`** — performance improvement
- **`build`** — build system or dependencies
- **`ci`** — CI configuration
- **`chore`** — maintenance, no production code change

A commit with `!` after the type or scope is a breaking change: `feat!:` or `feat(api)!:`.
Body and footer follow the standard Conventional Commits format.

This section applies when source control is in use. It is not required.

---

**Source:** TODO/FIXME marker tradition, originating in code commentary practices that predate modern source control. Documented in Steve Maguire, _Writing Solid Code_ (Microsoft Press, 1993), and reinforced by widespread industry use across decades.
**Shapes:** The Five Markers, Rules
**Adopted:** 2026-05-19
**Status:** active

**Source:** Conventional Commits 1.0.0, https://www.conventionalcommits.org/en/v1.0.0/
**Reinforced by:** ~94.5% adoption across popular NPM repos per ICSE 2025 study, https://conf.researchr.org/details/icse-2025/icse-2025-research-track/28/A-First-Look-at-Conventional-Commits-Classification
**Shapes:** When Using Source Control section
**Adopted:** 2026-05-19
**Status:** active

*Refines as evidence accumulates.*
