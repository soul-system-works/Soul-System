```
FINDING ID:      SOUL-F020
DATE:            2026-05-21
WITNESS IDS:     REF-09 docs/proposals/2026-05-21-feedback-on-published-
                 event-standard.md (item 2); parent commit 8f0a8aa (.flagged split);
                 REF-09 VISUAL-031 / VISUAL-033 (the two re-syncs)
WHAT:            When a standard NAMES a reference implementation, nothing obliges that
                 reference to be re-verified when the standard changes. Twice in one
                 week the parent changed operations/event-standard.md (SOUL-032 publish;
                 8f0a8aa .flagged split) and the named reference adapter
                 (REF-09) silently lagged until hand-resynced — a window in
                 which the canonical reference CONTRADICTED the canonical standard.
WHY:             A reference that contradicts its standard is the most expensive
                 Coherent Falsehood (SOUL-F015): the next adapter is told "copy the
                 reference" and copies the lie. This is the standard-scoped instance of
                 SOUL-F007 (verification != validation) and SOUL-F012 (the obligation
                 must fire, not be remembered). The completion gate covers a project's
                 own work; it does not cover a change's named-reference obligation,
                 which lives in another repo.
PROPOSED:        Add to the completion discipline for standards: a change to a standard
                 that designates a reference implementation is not "done" until the
                 reference is re-verified against it (or the lag is explicitly recorded
                 as owed). Dogfooded immediately — SOUL-F019's lineage change
                 re-triggers this: the REF-09 adapter must add
                 genaiparentagentid support. Recorded here as the first owed
                 re-verification rather than silently skipped.
WHY NOT YET AMENDMENT:  A process proposal awaiting Body/Council confirmation; may be
                 judged a refinement of the existing completion obligation rather than
                 new doctrine. Item 3 of the same proposal (vocabulary extension must
                 re-verify every consumer) is folded in as the consumer-side twin of
                 this producer-side gap — both likely subsumed by SOUL-F007.
FILED BY:        Archivist
RELATED:         [[SOUL-F007]], [[SOUL-F012]], [[SOUL-F015]], [[SOUL-F018]],
                 [[SOUL-F019]] (the change that re-triggers it)
STATUS:          ACCEPTED (Body, 2026-05-21) — adopted at the OPERATIONS level: encoded
                 as a Governance note in operations/event-standard.md (a change to the
                 standard is not complete until its named reference is re-verified, or
                 the lag recorded). Generalization into the philosophy-level completion
                 obligation is DEFERRED until a SECOND standard with a named reference
                 exists (default simplicity; threshold logic per F011/F018; no seed
                 bloat after C-lite). First owed instance already discharged (SOUL-040).
                 Closed.
```
