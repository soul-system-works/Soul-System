# Governance

This document describes who governs the Soul System,
how decisions are made, and what authority different contributors hold.

---

## The Governing Principle

This system is governed by its own philosophy.

The amendment process described in `council-synthesis.md` is not just
for AI sessions. It governs changes to this repository.
Proposed changes must follow that process.
The Council's amendment questions must be answered.
Evidence from Witness logs must be cited.

No amendment to the philosophy is accepted without evidence from real use.
No amendment is accepted under pressure or urgency.
No amendment contradicts the Soul without explaining which is more true and why.

---

## Roles

**Maintainers**
Hold merge authority on the canonical repository.
Responsible for Council deliberation on proposed amendments.
Must have run the system seriously enough to have Witness log evidence.
Initially: the founder. Expanded by invitation based on demonstrated use.

**Contributors**
Anyone who has run the system and has findings or proposed amendments
supported by Witness log evidence. See `CONTRIBUTING.md`.

**Observers**
Anyone using the system in their own projects without contributing upstream.
No obligations. No restrictions. Welcome.

---

## What Maintainers Can Do

- Accept or return proposed amendments following the amendment process
- Merge accepted amendments into canonical documents
- Increment system version numbers
- Invite new maintainers
- Add entries to the registry

## What Maintainers Cannot Do

- Accept amendments without Witness log evidence
- Accept amendments that cannot answer all three amendment questions
- Amend the Soul under urgency or pressure
- Remove prior versions of any document from the amendment record
- Act unilaterally on amendments that affect the core philosophy —
  at least two maintainers must deliberate

---

## Decision Making

**For operational documents** (CLAUDE.md, log format, template, synthesis process)
One maintainer can accept amendments with documented deliberation.
These documents iterate faster and need less friction to evolve.

**For the Soul**
Minimum two maintainers must deliberate.
The Skeptic role must be explicitly enacted — recorded in the deliberation.
The amendment record must show the full order of voices.

**For Governance itself**
All active maintainers must deliberate.
Unanimous acceptance required.
This document changes rarely and deliberately.

---

## Versioning

Each document carries its own version number in its filename and header.
`SYSTEM-VERSION.md` records the current coherent set.

When any document is amended:
- Its version number increments
- The amendment is filed in `amendments/accepted/`
- `SYSTEM-VERSION.md` is updated
- The prior version is retained — never discarded

System versions follow the format `MAJOR.MINOR`
- MINOR increments when operational documents change
- MAJOR increments when the Soul itself changes

---

## Disputes

If maintainers disagree on an amendment the Skeptic role is invoked formally.
Both positions are stated. The Skeptic challenges both.
The amendment is returned if consensus cannot be reached.
Returned amendments remain open — not rejected.

If a dispute cannot be resolved the amendment is filed as a Finding
and revisited when more evidence arrives from real use.
Evidence resolves disputes. Argument rarely does.

---

## Forking

This system may be forked freely.
A fork that diverges significantly from the Soul
should rename itself to avoid confusion about lineage.
A fork that proposes improvements is encouraged to contribute
those improvements back through the amendment process.

---

*Governance version 1.0*
*Changes to this document require all active maintainers.*
