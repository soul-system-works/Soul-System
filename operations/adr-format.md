# Architecture Decision Records (ADRs)

The Architect's record of structural decisions.

When the Architect commits a structural choice — module boundaries, interface
contracts, file layout, dependency selection — the choice is recorded as an ADR.
The record is immutable: it captures what was decided, why, and what follows.
Later ADRs can supersede earlier ones; the earlier record remains.

ADRs live in `docs/adr/` in the user's project, not in the Soul System repo.

---

## When to Write an ADR

Write an ADR when the Architect commits a structural decision that:
- a future Craftsman or Architect would need to understand to work with the system,
- cannot be derived by reading the code alone,
- has consequences that survive the present session.

Do not write an ADR for:
- tactical choices visible in the code — use a `NOTE` marker (see `code-markers.md`),
- decisions about the Soul itself — use the Council's AMENDMENT format (see `council-synthesis.md`).

### The Three Scales

The Soul System records decisions at three scales. Each has its own artifact:

| Scale | Artifact | Where it lives | Who writes it |
|---|---|---|---|
| Tactical | `NOTE` / `TODO` / `FIXME` / `DEBT` / `HACK` marker | in the code | Craftsman |
| Structural | ADR | `docs/adr/` in the project | Architect |
| Philosophical | AMENDMENT | the Soul itself | Council (Judge accepts) |

A marker may point to an ADR. An ADR may point to an AMENDMENT. They compose, they do not overlap.

---

## Template

```
# ADR-NNNN: [short title in present tense]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-NNNN]

## Context

[The forces at play — technical, organizational, philosophical. What is true
at the time of this decision that requires a choice.]

## Decision

[What was decided. State it clearly enough that someone reading only this
section can act on it.]

## Consequences

[What becomes easier, harder, or different after this decision. Include
consequences that are not strictly positive — the Architect commits to honesty.]
```

---

## Naming

Files: `docs/adr/NNNN-short-title.md`
Sequential numbering, never reset. The number is permanent.
Cross-references use the full ID: `[supersedes ADR-0007]`.

---

## Status Lifecycle

- **Proposed** — drafted, not yet committed.
- **Accepted** — committed; the structure is built on this.
- **Deprecated** — no longer in force, but the record remains.
- **Superseded by ADR-NNNN** — replaced by a later decision.

ADRs are never deleted. The history of what was decided and why it changed
is part of the record the next Architect needs.

---

## Execution Topology and Delegation

Execution topology is a structural decision and belongs in the ADR: whether the
work runs as a single agent, an orchestrator with independent workers, or a
communicating team. Single-agent is the default; record a multi-agent choice
only when genuine subproblem independence justifies it (judged at the
abstraction-layer gate against independence, cross-talk need, context-window
pressure, verification needs, and cost — multi-agent runs roughly an order of
magnitude more expensive and underperform on tightly-coupled work).

When work is delegated across an agent boundary — a subagent, a parallel
session, another tool's agent — the handoff package is self-contained *for
correctness*: it carries the goal, the context, and the success criteria the
fresh-context worker needs to produce a correct result, because the worker
inherits none of the delegator's history. Self-contained for correctness does
not mean hermetic — a worker may still read the surrounding repo for consistency
cues; what the packet must guarantee is that the result is correct from the
packet alone. A vague handoff is the named cause of duplicated work and gaps.
Provide context and goals, not instructions.

---

**Source:** Michael Nygard, "Documenting Architecture Decisions" (2011), https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
**Reinforced by:** Martin Fowler, https://martinfowler.com/bliki/ArchitectureDecisionRecord.html; MADR template (https://adr.github.io/madr/); ThoughtWorks Technology Radar, Adopt ring; AWS Prescriptive Guidance on ADRs
**Adopted:** 2026-05-19
**Status:** active
