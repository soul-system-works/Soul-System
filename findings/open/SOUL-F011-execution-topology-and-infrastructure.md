```
FINDING ID:      SOUL-F011
DATE:            2026-05-20
WITNESS IDS:     Body observation during Theme A convening. No prior witness
                 entry — all four test runs were single-agent, so this gap was
                 noticed by reasoning, not by failure.
WHAT:            The Soul System treats roles as perspectives, not agents, and has
                 no doctrine on TWO coupled execution concerns:
                 (a) Execution topology — when work should run as a single agent,
                     independent agents under an orchestrator, or a communicating
                     team. A properly working system would compose these for speed,
                     quality, and outcome (parallel independent subproblems →
                     orchestrated agents; tightly-coupled subproblems → team;
                     small bounded work → single agent). Roles could be embodied
                     as actual subagents, not only as perspectives in one mind.
                 (b) Infrastructure acquisition — when the Council/Artificer
                     acquires capabilities the runtime offers or that specific
                     roles need, within the constraints of the LLM/harness in use:
                     multi-agent frameworks (e.g. BMAD), and knowledge-graph
                     tooling (e.g. Graphiti and peers) which is bread-and-butter
                     for the memory-heavy roles — Archaeologist, Archivist,
                     Steward, Researcher. May require harness-level moves the
                     doctrine does not currently name (e.g. quit/restart a session
                     to switch into a multi-agent mode).
WHY NOT YET AMENDMENT:  No empirical evidence yet — all tests were single-agent.
                 This is a reasoned gap, not a witnessed failure, so it is a
                 strong candidate for a Pre-Mortem (forward) convening rather than
                 retrospective synthesis. Two decision points need defining without
                 becoming prescriptive about specific tools: an execution-topology
                 decision (who decides single vs orchestrated vs team, on what
                 basis) and an infrastructure-acquisition decision (when the
                 Artificer stands up a framework or a knowledge graph). Both must
                 stay tool-agnostic per the composability principle while still
                 telling the system WHERE the decision is made.
FILED BY:        Archivist
RELATED:         [[SOUL-F003]] (role-set by problem size — topology is the agent
                 analog of role-set), [[SOUL-F001]] (Researcher reaching outward —
                 knowledge graphs are the tool that enables it), [[SOUL-F002]]
                 (orchestration would make continuous-role activity observable),
                 [[SOUL-A008]]
PRE-MORTEM:      Convened 2026-05-20 with outward research (orchestration + memory
                 tooling). Outcome:
                 - TOPOLOGY half → SOUL-A008 (proposed): Architect names topology
                   at the AL gate; single-agent default; multi-agent earns its
                   place; self-contained handoff discipline. Production-proven win
                   is orchestrator-worker fan-out for INDEPENDENT subproblems
                   (Anthropic +90.2% on research, ~15x cost, bad for coupled work).
                 - KNOWLEDGE-GRAPH half → DEFER. Graphiti is the philosophical
                   twin (bi-temporal invalidate-don't-delete = supersede-with-care)
                   but adoption now is Premature Sophistication (~600k tokens/write,
                   3-4 person-months/yr upkeep; the record fits one context window).
                   TRIGGER to revisit: record no longer fits a single context
                   window, OR multi-project cross-hop queries become routine.
                   DECISION HOME: Artificer proposes/builds; Council ratifies vs
                   Accountant cost-reality + Steward "does it still serve."
STATUS:          Open — topology half addressed by SOUL-A008; knowledge-graph half
                 deferred with a defined trigger (above). Stays open until the
                 trigger is crossed.
```

This finding has the widest blast radius of the eleven: execution topology touches
how every role is embodied, and infrastructure acquisition (especially knowledge
graphs for the memory roles) could change how the Archaeologist/Archivist/Steward/
Researcher actually work rather than just how they are described. Likely its own
theme (Theme E) for a dedicated Pre-Mortem convening.
