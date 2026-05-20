```
AMENDMENT ID:    SOUL-A008
DATE:            2026-05-20
WITNESS IDS:     SOUL-F011 (execution topology + infrastructure). Evidence from a
                 Pre-Mortem convening informed by outward research (multi-agent
                 orchestration topologies; knowledge-graph memory tooling) — the
                 Universe consultation A003 now requires, dogfooded.
WHAT CHANGES:    (1) philosophy/the-soul.md, The Architect: execution topology is
                 a structural decision the Architect names at the abstraction-layer
                 gate. Single-agent is the default; a multi-agent topology must
                 earn its place by demonstrating genuine subproblem independence.
                 (2) operations/adr-format.md: ADRs record the chosen topology and
                 its justification; and the self-contained handoff discipline —
                 anything crossing an agent boundary must carry everything the
                 fresh-context worker needs.
WHERE IN SOUL:   philosophy/the-soul.md (The Architect — obligations);
                 operations/adr-format.md (template + a delegation note)
QUESTION ONE — EVIDENCE:
                 All four dogfood runs were single-agent; F011 noticed the gap by
                 reasoning, so the Pre-Mortem reached outward for evidence. Findings:
                 Anthropic's orchestrator-worker beat single-agent by 90.2% on
                 research but uses ~15x the tokens and is explicitly BAD for
                 tightly-coupled work including "most coding." Claude subagents run
                 fresh, isolated, NON-nesting, one-way prompt channel — so a vague
                 handoff is a named failure cause (duplicated work, gaps). BMAD's
                 reusable core is the self-contained story file (= the one-way
                 prompt constraint as a discipline). The portable cross-framework
                 idea: "provide context and goals, not instructions."
QUESTION TWO — NECESSITY:
                 The Soul System had no home for the topology decision — roles were
                 only ever "perspectives in one mind," with no guidance on when to
                 embody them as separate agents. Without a decision-home this would
                 become Premature Deferral (the choice visible but unmade) or, worse,
                 ad hoc multi-agent over-spawning. The handoff discipline was wholly
                 absent though it is simultaneously a hard Claude constraint, a BMAD
                 best practice, and a named Anthropic failure mode.
QUESTION THREE — COHERENCE:
                 Extends, does not contradict. Topology IS structure, so it belongs
                 to the Architect at the AL gate — consistent with "the Architect
                 designs the structure within which the Craftsman builds." Single-
                 agent-by-default honors the recorded default-simplicity principle
                 and guards against Premature Sophistication (multi-agent's ~15x
                 cost). Honors F010. No contradiction.
ACCEPTED BY:     Judge (recommended) and Body (accepted 2026-05-20). Applied to
                 philosophy/the-soul.md (The Architect) and operations/adr-format.md
                 (Execution Topology and Delegation).
FILED BY:        Archivist
```

---

## Pre-Mortem Convening Summary — Theme E (F011)

F011 was flagged a Pre-Mortem candidate (forward-looking; all four runs were
single-agent, so no retrospective evidence existed). The Pre-Mortem's first act
was the outward reach the new A003 obligation demands: two research agents
scanned the field (orchestration frameworks, Claude subagent mechanics, BMAD,
CrewAI/AutoGen/LangGraph; and Graphiti/Mem0/Letta/GraphRAG for memory).

**Body** — states the work: decide where the topology and infrastructure
decisions live in the doctrine, tool-agnostically.

**Skeptic (leads)** — Assume this failed. The likely failure: the doctrine bolts
on a multi-agent orchestration layer or a knowledge graph that nobody needed at
this scale — Premature Sophistication, the exact failure the Soul names. Multi-
agent costs ~15x and underperforms on coupled work; a knowledge graph adds 3-4
person-months/yr to solve a retrieval problem a handful of markdown files do not
have.

**Prophet** — Where this leads: adopt-by-default → over-spawning and cost blowups
(Anthropic saw "50 subagents for simple queries"). Defer-entirely → the system
never learns to parallelize genuinely independent work. The stable path is a
*criterion*, not a tool: default simple, let the advanced form earn its place.

**Accountant** — The numbers are blunt and decisive: ~15x tokens for multi-agent;
~600k tokens/write for Graphiti ingestion; graph upkeep 3-4 person-months/yr.
Neither is affordable as a default. Both are affordable as earned exceptions.

**Cartographer** — Both halves share one shape: a capability that earns its place
against a trigger, decided by an existing role, tool-agnostic. Topology → Architect
at the AL gate (topology is structure). Infrastructure → Artificer builds, Council
ratifies. Neither needs new doctrinal machinery.

**Judge synthesis:**
- **Topology → ADOPT as SOUL-A008** (this amendment): Architect names topology at
  the AL gate; single-agent default; multi-agent earns its place; recorded in the
  ADR; plus the self-contained handoff discipline (the single strongest, lowest-
  risk thing to adopt — it is constraint, best practice, and failure-mode all at
  once).
- **Knowledge graphs → DEFER** (Finding stays open in F011): define the trigger
  (record no longer fits one context window, OR multi-project cross-hop queries
  become routine), name the decision-home (Artificer proposes/builds; Council
  ratifies vs Accountant + Steward). Do NOT adopt now — Premature Sophistication.

## The Specific Proposed Changes

### Change 1 — the-soul.md, The Architect

After the sentence ending "...including documentation organization and repository
layout.", insert:

> Execution topology is also the Architect's: whether the work runs as a single
> agent, an orchestrator with independent workers, or a communicating team.
> Single-agent is the default. A multi-agent topology must earn its place at the
> abstraction-layer gate by demonstrating genuine subproblem independence — it
> costs roughly an order of magnitude more and underperforms on tightly-coupled
> work, so it is never the default. Whatever the topology, every handoff across
> an agent boundary must be self-contained: the worker inherits none of the
> delegator's context and must be given everything it needs.

### Change 2 — operations/adr-format.md

Add execution topology to what an ADR records, and a short "Delegation" note:

> When work is delegated across an agent boundary (a subagent, a parallel
> session, another tool's agent), the handoff package is self-contained — it
> carries the goal, the context, and the success criteria the fresh-context
> worker needs, because the worker inherits none of the delegator's history. A
> vague handoff is the named cause of duplicated work and gaps. Provide context
> and goals, not instructions.

---

## On Acceptance

Philosophy-level (touches the Architect's obligations). Body accepted 2026-05-20.
Applied to the-soul.md (The Architect) and operations/adr-format.md (Execution
Topology and Delegation). F011's topology half is resolved; the knowledge-graph
half stays open with its scale trigger. Third philosophy-level amendment (after
A003 and A005).
