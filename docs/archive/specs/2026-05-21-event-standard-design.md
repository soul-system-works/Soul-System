# Event Standard — Design Spec

**Date:** 2026-05-21
**Status:** Design pass — spec-first per Body confirmation of SOUL-F018 (adopt-with-alignment). Pending review, then `operations/event-standard.md`.
**Topic:** A methodology-event vocabulary for the Soul System, published as a CloudEvents v1.0 profile + W3C PROV binding, reusing OpenTelemetry GenAI identity keys for correlation.

## Problem (two levels)

- **Immediate:** REF-09 emits Soul events from a Claude Code Stop hook,
  but the format is ad hoc and bound to one tool. For a second adapter
  (Cursor/Aider) or a second consumer to interoperate, the *semantic* event
  contract must live at the methodology layer, not inside the hook.
- **Larger system:** the Soul System is tool-agnostic methodology. Its semantic
  moments — gates, role invocations, witness entries, findings, amendments, ideas
  — are exactly the *process/decision event layer* the field has left as white
  space (SOUL-F018 research): OpenTelemetry GenAI covers HOW an LLM call ran;
  nothing standard records WHAT methodological decision occurred. The standard
  claims that empty slot on settled primitives rather than inventing its own.

## What the research settled (SOUL-F018)

- **Adopt-with-alignment.** Do not reinvent the envelope.
- Build ON three settled primitives: **CloudEvents v1.0** (the envelope),
  **W3C PROV** (the provenance model), **OTel GenAI semconv identity keys**
  (correlation).
- The methodology layer **complements** telemetry — one methodology event ↔
  zero-or-many LLM calls. They join, they do not duplicate.
- External anchor: **EU AI Act Art. 12** mandates lifecycle event logging by
  Aug 2026 with no finalized technical standard yet (prEN 18229-1, ISO/IEC DIS
  24970 still drafts).

## The abstraction layer

- **What varies:** the tool/adapter that emits events; the transport; the
  consumer; the set of projects; the per-event payload.
- **What decides whether it varies:** the adapter (platform-specific concerns)
  and the project (its own `source` identity and artifact-ID scheme).
- **What cannot vary** (the contract every adapter and consumer targets):
  the envelope (**CloudEvents 1.0**), the type vocabulary (`soul.*`), `subject`
  = the artifact ID, the provenance mapping (**PROV**), and the correlation keys
  (**OTel identity**). These are doctrine; everything above is adapter freedom.

## The vocabulary (the design work)

Soul events are the semantic moments **already in the doctrine** — not a new
ontology. Grouped by category, `soul.<category>.<action>`:

| Type | Fires when | Typical `subject` |
|---|---|---|
| `soul.gate.frame.evaluated` | the two-level problem frame is stated/checked | — |
| `soul.gate.abstraction_layer.named` | the AL is recorded before implementation | ADR / spec id |
| `soul.gate.fence.examined` | existing state explained before change | the fence |
| `soul.gate.completion.verified` | Universe consulted before "complete" | the work id |
| `soul.witness.recorded` | a Witness entry is filed | `SOUL-029` |
| `soul.council.convened` | the Council meets | — |
| `soul.finding.filed` | a Finding is filed | `SOUL-F018` |
| `soul.amendment.proposed` | an amendment is proposed | `SOUL-A008` |
| `soul.amendment.accepted` | an amendment is accepted into the Soul | `SOUL-A008` |
| `soul.idea.captured` | an idea enters the inbox | `SOUL-I006` |
| `soul.idea.graduated` | an idea graduates to a Finding/work | `SOUL-I006` |
| `soul.role.invoked` | a role is named in the moment | role name |
| `soul.judge.override` | the Judge overrides a gate (with reason) | the gate |
| `soul.universe.shift.named` | a Multiverse-level shift is named | — |

Extensible: a new doctrinal moment earns a new type the same way the failure
vocabulary grows — witnessed, confirmed by the Council, added here.

**Explicitly NOT Soul events:** continuous per-tool-call activity. That is
adapter-emitted *telemetry* (SOUL-F018 §4) — a separate stream on the OTel layer,
not the methodology's to own.

## CloudEvents profile (the envelope binding)

How Soul fills the CloudEvents 1.0 attributes:

| CE attribute | Soul value |
|---|---|
| `specversion` | `"1.0"` |
| `id` | unique per event (UUID) |
| `source` | project identity URI, e.g. `urn:soul:project:REF-09` |
| `type` | one of the `soul.*` vocabulary above |
| `subject` | the artifact ID the event concerns (optional when none) |
| `time` | RFC3339 timestamp |
| `datacontenttype` | `application/json` |
| `data` | the semantic payload (per-type; e.g. the gate's answers, the finding ref) |

**Correlation extension attributes** (CE names must be lowercase alphanumeric, so
the OTel keys are carried under CE-legal names, mapping documented):

| CE extension attr | Carries | OTel source key |
|---|---|---|
| `genaiagentid` | which agent/role instance acted | `gen_ai.agent.id` |
| `genaisessionid` | the session/conversation | `gen_ai.conversation.id` |

## PROV binding

Every Soul event maps cleanly to PROV's three nouns:

- **Activity** — the methodological act (the gate evaluation, the convening),
  typed by the event `type`.
- **Agent** — who acted: the Body (human), the AI instrument, or a named role
  (a `prov:Agent` qualified with `soul:role`).
- **Entity** — the artifact used or generated (finding, amendment, AL record, idea).

Relations: `wasGeneratedBy` (artifact ← activity), `wasAssociatedWith`
(activity ← agent), `used` (activity → prior artifacts), `wasDerivedFrom`
(the chain). The synthesis hierarchy **is** a PROV derivation chain:

```
marker  ──wasDerivedFrom──►  witness  ──wasDerivedFrom──►  finding  ──wasDerivedFrom──►  amendment
```

That alignment is the strongest evidence the binding fits: the doctrine's
existing chain already *is* provenance.

## Correlation with telemetry

One Soul event ↔ zero-or-many OTel GenAI spans, joined on `genaiagentid` /
`genaisessionid`. The methodology layer says **what** decision; the telemetry
layer says **how** the LLM executed. A consumer can drill from a filed finding
down to the exact calls that produced it — without either layer owning the other.

## Example event

```json
{
  "specversion": "1.0",
  "id": "0b6f...e21",
  "source": "urn:soul:project:soul-system",
  "type": "soul.finding.filed",
  "subject": "SOUL-F018",
  "time": "2026-05-20T18:30:00Z",
  "datacontenttype": "application/json",
  "genaiagentid": "judge",
  "genaisessionid": "96754136-34dc-...",
  "data": {
    "title": "Event-standard proposal response",
    "filedBy": "Archivist",
    "derivedFrom": ["SOUL-011", "VISUAL-F001"],
    "path": "findings/open/SOUL-F018-event-standard-proposal-response.md"
  }
}
```

## What v1 publishes vs defers

**Publishes** (`operations/event-standard.md`): the vocabulary table, the
CloudEvents profile table, the PROV mapping, the correlation keys, one worked
example, and a Source footer (CloudEvents / PROV / OTel + EU AI Act anchor).

**Defers** (YAGNI; the activation-gap lesson):

- A JSON Schema per event type — build when a second consumer needs validation.
- Transport bindings (HTTP/Kafka/etc.) — CloudEvents already specifies these;
  adapter's choice.
- The `platform-adapters/` directory — created when a second adapter appears
  (the SOUL-F018 trigger).

The Claude Code hook in REF-09 stays as the **reference adapter** and
is updated to emit this profile.

## Doctrine touch (minimal — and deliberately not in the always-loaded seed)

- `operations/event-standard.md` (new) — the standard itself.
- `README.md` structure list — add it.
- `operations/CLAUDE.md` — at most a one-line *consult-on-demand* pointer, **not**
  an `@`-import. The standard is reference material, not always-on doctrine;
  loading it every session would repeat the SOUL-I006 mistake.
- `SOUL-F018` — mark `Graduated → operations/event-standard.md` once written.

## Success criteria

- A Soul event is a valid CloudEvents 1.0 event (no custom envelope).
- Every doctrinal semantic moment has a type; nothing semantic is unrepresentable.
- A finding's provenance chain (witness → finding → amendment) is expressible in PROV.
- A Soul event can be joined to its underlying LLM telemetry via shared identity keys.
- A second adapter (Cursor/Aider) could implement the profile from this spec
  alone, with no Claude-specific assumptions.

## Open questions

1. **Namespace.** Proposed: `soul.` is the canonical `type` prefix for all
   adopters (recognizable across tools); adopters namespace `source`, not `type`.
   Alternative: require reverse-DNS prefixes. Lean: keep `soul.` canonical.
2. **Profile versioning.** The Council governs the standard's version (SOUL-F018).
   Add a per-event `dataschema` pointing to a versioned schema later, when schemas
   are introduced — not in v1.
3. **The telemetry boundary** (SOUL-F018 §4) should be stated explicitly in the
   standard so adapters don't smuggle continuous activity into the semantic stream.

## Related

- **SOUL-F018** — the finding this graduates; carries the research that flipped
  defer → adopt-with-alignment.
- **SOUL-I006** — the always-loaded-seed cost concern; this spec deliberately
  keeps the standard out of the `@`-imported path.
- **SOUL-I005** — token economics; the standard is consult-on-demand, not session overhead.
