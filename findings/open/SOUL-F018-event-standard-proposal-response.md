```
FINDING ID:      SOUL-F018
DATE:            2026-05-20
WITNESS IDS:     REF-09 docs/proposals/2026-05-20-event-standard-to-parent-
                 soul-system.md (the proposal); SOUL-011 + VISUAL-F001 (the
                 continuous-activity question it escalates)
WHAT:            The Council's response to REF-09's proposal to formalize
                 the event standard into the parent methodology.
                 (1) ENDORSE the layering split — the event standard is methodology
                     (the neutral contract every adapter/consumer targets); the
                     Claude Code hook is one platform adapter that stays in the
                     tooling layer. Correct; honors tool-agnosticism.
                 (2) DEFER adoption into the parent. There is currently one consumer
                     (REF-09) and one adapter (its hook), in one project —
                     no coordination problem for the methodology to own. A
                     methodology-owned standard earns its place when MULTIPLE
                     independent parties must agree on it. Adopting now = governing
                     a standard with one user = Premature Sophistication (the
                     Accountant's call). Same deferral shape as F011 (knowledge
                     graphs): adopt at a need threshold, not on aspiration.
                 (3) §4 RESOLVED — continuous session activity is NOT a Soul event.
                     The doctrine already answers it: "the Witness is not a
                     transcript; it records moments of specific kinds." Soul events
                     are semantic (gates/roles/witness/amendments). Continuous
                     activity (every tool call) is optional, adapter-emitted
                     TELEMETRY — a separate stream, not a Soul event and not the
                     methodology's to own. This honors both the doctrine and the
                     demand for a continuous record (SOUL-011 / VISUAL-F001): the
                     activity stream may exist, just distinct from the semantic log.
WHY NOT YET AMENDMENT:  The endorsement and §4 resolution are clarifications of
                 existing doctrine, not new doctrine — no amendment needed. The
                 adoption is deferred, so there is nothing to amend yet.
TRIGGER TO ADOPT: a SECOND independent adapter (e.g. a Cursor/Aider emitter) OR a
                 second consumer appears — then the parent adopts the standard
                 (e.g. operations/event-standard.md) and the Council governs its
                 version. A platform-adapters/ area is created at the same trigger.
FILED BY:        Archivist
RELATED:         [[SOUL-F011]] (the deferral pattern), SOUL-011 + VISUAL-F001
                 (continuous-activity demand, now scoped to telemetry)
RESEARCH OUTCOME (2026-05-20): Two independent agents scanned the field and
                 converged from opposite directions. (a) The telemetry layer
                 (LLM-call mechanics) is consolidated on OpenTelemetry GenAI
                 semconv — settled; it records HOW work executed and its own spec
                 has "no provisions for decisions, approvals, verification gates,
                 or process methodology." (b) The SEMANTIC process/decision event
                 layer the Soul standard targets is WHITE SPACE: CloudEvents is
                 envelope-only (semantics explicitly out of scope); W3C PROV is a
                 generic model needing a binding; BPMN/DMN/XES are wrong-phase; the
                 only semantic-decision-provenance work (PROV-AGENT, AER) is
                 unadopted research preprints. External anchor: EU AI Act Art. 12
                 mandates lifecycle event logging by Aug 2026 with NO finalized
                 technical standard yet (prEN 18229-1, ISO/IEC DIS 24970 still
                 drafts). The two layers COMPLEMENT (one methodology event ↔ zero
                 or many LLM calls), they do not duplicate.
                 RECOMMENDATION FLIPS defer → ADOPT, with alignment: publish the
                 Soul methodology-event vocabulary as a CloudEvents v1.0 profile +
                 a W3C PROV binding, reusing OTel identity keys (gen_ai.agent.id,
                 gen_ai.conversation.id) for correlation. Claim the empty vocabulary
                 slot on settled primitives; do NOT reinvent the envelope. The
                 Claude Code hook stays in REF-09 as the reference adapter.
STATUS:          Open — Council now RECOMMENDS adopt-with-alignment (evidence-based,
                 flipping the provisional defer). Body to confirm the direction; on
                 confirmation, draft operations/event-standard.md (vocabulary +
                 CloudEvents profile + PROV binding + OTel identity reuse).
```

Note for the Body: this is the Judge's recommendation. You are invested in the
observability direction, so the adopt-now-vs-defer call is yours to confirm. The
§4 resolution and the layering endorsement stand regardless.
