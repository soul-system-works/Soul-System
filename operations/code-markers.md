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

## Markers and Docstrings

Markers are not the only honesty channel in the artifact. Docstrings and comments carry a complementary kind of truth:

- **Markers** flag compromise and deferral (`TODO` / `FIXME` / `DEBT` / `HACK`) and non-obvious local context (`NOTE`). Short and scannable.
- **Docstrings** carry derivations, validity ranges, named approximations, sign conventions — the "how and why this is correct" a future reader needs. Longer, and they live with the definition.

Both are "honest in the artifact." A high-discipline codebase may carry most of its honesty in docstrings and few markers — that is not a failure of the marker doctrine, provided compromise and deferral are still flagged where they live. Use the marker when the truth is "this is incomplete or compromised"; use the docstring when the truth is "this is how and why this works."

**The test — unfinished business vs standing limitation.** The dividing line is *will it change?* A **standing limitation** — a deliberate, accepted property that is not going to change (a named approximation, a validity range, "calibrated, not production") — belongs in a docstring/`NOTE` and earns *no* marker; a `TODO` on something you will never do is noise. **Unfinished business** — work that *should* still happen — earns a **marker** even when a docstring also describes it, so it stays greppable. A docstring-heavy codebase is honest about what it *is*; without markers it is silent about what it still *owes*.

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
