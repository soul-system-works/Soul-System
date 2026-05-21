```
FINDING ID:      SOUL-F019
DATE:            2026-05-21
WITNESS IDS:     REF-09 docs/proposals/2026-05-21-feedback-on-published-
                 event-standard.md (item 1); its ADR-0006 (the conformance that
                 dropped parentagentid); parent FANOUT (orchestrator-worker validation)
WHAT:            The event standard (SOUL-F018) defines correlation attributes for
                 agent (genaiagentid) and session (genaisessionid) but NO parent/
                 lineage slot. A consumer can group events by agent and by session but
                 cannot place a subagent under the agent that spawned it — required for
                 any multi-agent lane / fan-out view. Conforming the reference adapter
                 forced it to DROP its prior parentagentid (ADR-0006), so the gap is
                 concrete, not hypothetical; the same threshold appears on the parent
                 side (FANOUT).
DECISION:        ADOPT — reserved + optional. Add genaiparentagentid as an optional
                 envelope correlation attribute (mirrors genaiagentid; CE-legal,
                 scalar, omitted when no parent; prior art OpenInference
                 graph.node.parent_id) AND document the PROV delegation relation
                 (subagent prov:actedOnBehalfOf parent agent). Emission is OPTIONAL:
                 single-agent runs omit it; emit on first real multi-agent use.
WHY:             Standards are anticipatory coordination devices (SOUL-F018). An
                 optional, additive attribute is cheap to add later, so the real risk
                 of deferral is not breakage but DIVERGENCE — a second party inventing
                 its own parent field (exactly what REF-09 had to do, then
                 drop). Reserving the agreed name now removes that risk at near-zero
                 cost; requiring emission only on real use honors YAGNI.
GRADUATED TO:    operations/event-standard.md (correlation table + PROV note),
                 2026-05-21. The Council governs the standard's version.
FILED BY:        Archivist (harvest of the REF-09 feedback)
RELATED:         [[SOUL-F018]] (the standard), [[SOUL-F011]] (execution topology /
                 multi-agent), [[SOUL-F020]] (reference-adapter sync — this change
                 re-triggers it: the REF-09 adapter must add the slot)
STATUS:          Graduated → operations/event-standard.md (2026-05-21). Closed.
```
