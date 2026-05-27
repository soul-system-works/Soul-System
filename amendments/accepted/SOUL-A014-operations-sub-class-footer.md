```
AMENDMENT ID:    SOUL-A014
DATE:            2026-05-27
WITNESS IDS:     SOUL-088 (Soul-Console v1 structural audit §1.5 named the
                 fuzzy boundary inside `operations/` — three sub-classes
                 living flat: DOCTRINE-ABOVE-INSTRUMENT, FORMAT-SPEC,
                 PROCEDURE — and proposed resolution-via-documented-
                 sub-classification rather than reorganization); SOUL-091
                 (dogfood instance — `operations/problem-slot-template.md`
                 carries `**Sub-class:** PROCEDURE (per the proposed A014
                 operations sub-classification convention).` in its
                 footer, before the convention was formalized).

WHAT CHANGES:    Extend seed §Source Footers with an optional `Sub-class:`
                 field for `operations/` files. Permitted values:

                 - **DOCTRINE-ABOVE-INSTRUMENT** — text the seed @-imports
                   or directly references (`CLAUDE.md`, `council-synthesis.md`,
                   `completion-gate.md`, `experiment-harness.md`).
                 - **FORMAT-SPEC** — defines record shapes used elsewhere
                   (`witness-log-format.md`, `adr-format.md`, `code-markers.md`,
                   `event-standard.md`).
                 - **PROCEDURE** — how-to docs for specific situations
                   (`problem-slot-template.md`, `reference-repository.md`).

                 Rule: `operations/` holds on-demand DOCTRINE-ABOVE-INSTRUMENT,
                 FORMAT-SPEC, and PROCEDURE docs in a flat structure; each
                 file's footer names its sub-class. The flat layout is
                 cheaper than subdirectories and avoids URL/import churn —
                 the rule does the work the directory tree would have.

                 The footer field is OPTIONAL but RECOMMENDED for any new
                 operations/ file going forward. Existing files without the
                 field stay valid; the audit's §1.5 table establishes the
                 sub-class for each current file (back-fill on touch, not
                 in bulk).

WHERE IN SOUL:   `operations/CLAUDE.md` §Source Footers — extend the footer
                 template with the optional `Sub-class:` line and add a
                 brief paragraph explaining the operations/-specific use
                 of the field.

                 No `philosophy/the-soul.md` edit. No `mind.md` edit (the
                 rule is operations-layer-specific; it does not generalize
                 to a doctrinal rule across contexts).

QUESTION ONE — EVIDENCE:
                 - SOUL-088 audit Section 1.5 enumerated the three
                   sub-classes from inspection of the actual operations/
                   directory; the table maps every current file to one.
                 - SOUL-090's beta investigation reinforced the rule —
                   `completion-gate.md` (DOCTRINE) and `reference-repository.md`
                   (FORMAT-SPEC, treating it as the spec for `references/`)
                   were KEEP-IN-PLACE for sub-class-specific reasons; the
                   sub-class made the load-bearing-ness LEGIBLE.
                 - SOUL-091 dogfooded the field in
                   `operations/problem-slot-template.md` before the
                   amendment landed; the file reads coherently with the
                   field in place.

QUESTION TWO — NECESSITY:
                 - Without the rule, `operations/` grows by accretion;
                   future audits will re-discover the same fuzzy boundary.
                 - The rule named at the footer-level catches sub-class
                   confusion at AUTHORING time (the writer must name the
                   sub-class before publishing) rather than at audit time
                   (years later, by reverse-engineering from content).
                 - The cost of the field is one optional footer line per
                   file. The cost of NOT having it is the audit's §1.5
                   ambiguity re-emerging at scale.
                 - SOUL-091's dogfood demonstrates the writer-time discipline
                   works: naming `PROCEDURE` while authoring made the file's
                   role explicit and tested the convention before it became
                   a rule.

QUESTION THREE — COHERENCE:
                 - Extends the existing §Source Footers convention with one
                   optional field. No new structure; no new lifecycle; no
                   new gate.
                 - Coheres with `mind-rule-11` (two parties reading must
                   arrive at the same meaning) — the explicit sub-class
                   label preserves coherence under independent reading.
                 - Coheres with `mind-rule-5` (never always-on past the
                   description budget) — the rule itself lives in the seed
                   (one new paragraph in §Source Footers), but the
                   sub-class taxonomy stays on-demand (the field is read
                   only when a reader is inspecting the file).
                 - Coheres with `mind-rule-2` (default simplicity) — flat
                   structure stays; only the naming gets formalized. No
                   reorganization, no moves, no churn.
                 - No contradictions with existing doctrine. Pairs naturally
                   with A011 (marker-vs-docstring) on the same principle:
                   structural meaning gets named at the point of use.

ACCEPTED BY:     Body, 2026-05-27 (within the b→c→a beat following the
                 Soul-Console v1 audit close — SOUL-088's audit explicitly
                 flagged A014 as a candidate amendment and the Body
                 authorized the batch).

FILED BY:        Architect (the boundary rule named at the seam — operations
                 sub-class is a structural boundary); Steward (the
                 sub-classification is what makes RETIRE / KEEP decisions
                 legible per SOUL-090's discharge); Archivist (the footer
                 is the indexing surface — `grep -B1 "^\*\*Sub-class:"
                 operations/` returns the index on demand); Cartographer
                 (the SOUL-087 per-boundary reshape — Architect per-boundary
                 rather than Steward per-item — applied directly here).
```

---

## On Acceptance

Operations-layer amendment. The audit (SOUL-088) named the boundary rule explicitly; SOUL-091 dogfooded the footer field before this amendment formalized it. The acceptance closes a fuzzy seam without reorganizing the directory.

The work landed in three places this beat:

1. `operations/CLAUDE.md` §Source Footers — extended template + paragraph naming the operations sub-class convention.
2. This amendment record.
3. (Already in place from SOUL-091) `operations/problem-slot-template.md` — first dogfood instance, retroactively conforms to the formalized rule.

No findings closed by this amendment — it codifies a rule named in an audit, not a finding's discharge. Future operations/ files use the field; the SOUL-088 audit's §1.5 table back-fills existing files in place.
