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

*Version 1.0. Refines as evidence accumulates.*
