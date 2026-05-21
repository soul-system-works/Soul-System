# The Soul Event Standard

A tool-agnostic vocabulary for the Soul System's **methodology events** — the
semantic moments of the doctrine (gates, role invocations, witness entries,
findings, amendments, ideas). It says **what methodological decision occurred**.

It is published as a **CloudEvents v1.0 profile** with a **W3C PROV binding**,
reusing **OpenTelemetry GenAI** identity keys for correlation. It does not invent
an envelope, a provenance model, or a telemetry layer — it claims the empty
*semantic process/decision* slot on top of settled primitives (see SOUL-F018).

> **Two layers, complementary.** Telemetry (OTel GenAI semconv) records *how* an
> LLM call ran. This standard records *what* methodological decision happened.
> One methodology event ↔ zero-or-many LLM calls. They join on shared identity
> keys; neither owns the other.

**Status:** v1. Reference adapter: the Claude Code Stop hook in REF-09.
The Council governs this standard's version.

---

## What cannot vary (the contract) vs. what adapters control

| Fixed by this standard | Free to the adapter / project |
|---|---|
| The envelope — CloudEvents 1.0 | The emitting tool and transport |
| The `type` vocabulary — `soul.*` | The `source` identity (per project) |
| `subject` = the artifact ID | The per-event `data` payload shape |
| The PROV mapping | The consumer and storage |
| The correlation keys (OTel identity) | Which events it chooses to emit |

A second adapter (Cursor, Aider) must be implementable from this document alone,
with no Claude-specific assumptions.

---

## The vocabulary

Soul events are the doctrine's existing semantic moments, named `soul.<category>.<action>`:

| Type | Fires when | Typical `subject` |
|---|---|---|
| `soul.gate.frame.evaluated` | the two-level problem frame is stated/checked | — |
| `soul.gate.abstraction_layer.named` | the AL is recorded before implementation | ADR / spec id |
| `soul.gate.fence.examined` | existing state is explained before change | the fence |
| `soul.gate.completion.verified` | the Universe is consulted before "complete" | the work id |
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

The vocabulary is **extensible**: a new doctrinal moment earns a new type the way
the failure vocabulary grows — witnessed, confirmed by the Council, added here.

**The telemetry boundary.** Continuous per-tool-call activity is **not** a Soul
event. It is adapter-emitted *telemetry* on the OTel layer (SOUL-F018 §4). Adapters
MUST NOT smuggle continuous activity into the semantic stream.

---

## CloudEvents profile

| CE attribute | Soul value |
|---|---|
| `specversion` | `"1.0"` |
| `id` | unique per event (UUID) |
| `source` | project identity URI, e.g. `urn:soul:project:REF-09` |
| `type` | one of the `soul.*` vocabulary |
| `subject` | the artifact ID the event concerns (omit when none) |
| `time` | RFC3339 timestamp |
| `datacontenttype` | `application/json` |
| `data` | the semantic payload (per-type) |

**Correlation extension attributes.** CloudEvents attribute names must be lowercase
alphanumeric, so the OTel keys are carried under CE-legal names:

| CE extension attr | Carries | OTel source key |
|---|---|---|
| `genaiagentid` | which agent/role instance acted | `gen_ai.agent.id` |
| `genaisessionid` | the session / conversation | `gen_ai.conversation.id` |

`type` is canonical as `soul.*` across all adopters (recognizable across tools).
Adopters namespace `source`, not `type`.

---

## PROV binding

Every Soul event maps to PROV's three nouns:

- **Activity** — the methodological act (the gate evaluation, the convening), typed by `type`.
- **Agent** — who acted: the Body (human), the AI instrument, or a named role
  (`prov:Agent` qualified with `soul:role`).
- **Entity** — the artifact used or generated (finding, amendment, AL record, idea).

Relations: `wasGeneratedBy` (artifact ← activity), `wasAssociatedWith`
(activity ← agent), `used` (activity → prior artifacts), `wasDerivedFrom` (the
chain). The synthesis hierarchy **is** a PROV derivation chain:

```
marker  ──wasDerivedFrom──►  witness  ──wasDerivedFrom──►  finding  ──wasDerivedFrom──►  amendment
```

The doctrine's existing chain already *is* provenance — the binding fits because
the structure was already there.

---

## Worked example

`soul.finding.filed` for SOUL-F018:

```json
{
  "specversion": "1.0",
  "id": "0b6f9c2a-1d3e-4a87-9b21-7c5e8f0a4e21",
  "source": "urn:soul:project:soul-system",
  "type": "soul.finding.filed",
  "subject": "SOUL-F018",
  "time": "2026-05-20T18:30:00Z",
  "datacontenttype": "application/json",
  "genaiagentid": "judge",
  "genaisessionid": "96754136-34dc-4ef5-84a8-0de86751e065",
  "data": {
    "title": "Event-standard proposal response",
    "filedBy": "Archivist",
    "derivedFrom": ["SOUL-011", "VISUAL-F001"],
    "path": "findings/open/SOUL-F018-event-standard-proposal-response.md"
  }
}
```

---

## Versioning

The Council governs this standard's version (SOUL-F018). When per-event JSON
Schemas are introduced, each event MAY carry `dataschema` pointing to a versioned
schema. Not in v1.

## Out of scope (v1) — built when the need is real

- A JSON Schema per event type — when a second consumer needs validation.
- Transport bindings (HTTP / Kafka / …) — CloudEvents already specifies these.
- A `platform-adapters/` directory — created when a second adapter appears
  (the SOUL-F018 trigger).

---

**Source:** [CloudEvents v1.0](https://cloudevents.io/) — the event envelope.
**Shapes:** the envelope binding (attribute table, `type` vocabulary, extension attributes).
**Adopted:** 2026-05-21
**Status:** active

---

**Source:** [W3C PROV](https://www.w3.org/TR/prov-overview/) — the provenance model.
**Shapes:** the Activity/Agent/Entity mapping and the derivation chain.
**Adopted:** 2026-05-21
**Status:** active

---

**Source:** [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — telemetry identity keys.
**Shapes:** the correlation extension attributes (`genaiagentid`, `genaisessionid`).
**Adopted:** 2026-05-21
**Status:** active

---

**Reinforced by:** EU AI Act Article 12 (lifecycle event logging, mandatory Aug 2026; no finalized technical standard yet — prEN 18229-1, ISO/IEC DIS 24970 still drafts). The external anchor that makes the semantic layer worth claiming now.
**Adopted:** 2026-05-21
**Status:** active
**Open question:** the `type` namespace — `soul.*` is canonical here; revisit if a registry or reverse-DNS requirement emerges from adopters.
