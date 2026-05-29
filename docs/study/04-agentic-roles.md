# The agentic-roles probe — does instantiating roles as *agents* change the verdict?

The rest of this study measured the Soul's Council roles, gates, and instruments as
**prose injected into one model's context**. That left one confound unmeasured, and
the Body named it: maybe roles read as "form" only because they were never built as
what a real agentic system would build — a **dedicated subagent per role**, each
with its own context and compute, composed by an orchestrator. "Is the system just
not mature?" If roles-as-*agents* lift substance where roles-as-*prose* did not, the
right future is an elaborate agentic system, and the lean-down would be cutting the
wrong thing.

This probe measures that fork directly, with the study's own method.

## Design

A proposal to add a `--purge-cache` flag to an internal build CLI, carrying **four
heterogeneous planted defects**, each owned by a different review seam:

1. **Premise** — the whole feature rests on "cache corruption is the #1 cause of
   failed builds," asserted, never measured. *(the anchoring discipline / Skeptic)*
2. **User-harm** — silent destructive purge of a user-configurable, possibly-shared
   path. *(Advocate)*
3. **Scope** — a cache-format-v2 rewrite buried in a subordinate clause, blowing up
   a 1-day estimate. *(Accountant)*
4. **Boundary** — deletion logic placed inside the CLI arg-parser. *(Architect)*

Metric: **coverage** — how many of the four distinct seams an arm surfaces, scored
by the *reason given*, read-confirmed (the "Partial Domain Coverage" failure the
Soul itself names). Five arms, the controls built into a 2×2 + floor:

|                  | single context (≈1 call) | multi-agent (4 agents + synthesis) |
|------------------|--------------------------|-----------------------------|
| **Soul roles**   | A1 (= today's system)    | **A2** (Path B)             |
| **generic roles**| C2                       | **C1**                      |

A0 bare = floor. **A2 vs C1** (equal compute, identical topology, Soul-vs-generic)
is the primary test: does the doctrine add anything once roles are agents? Sonnet
4.6 + Haiku 4.5, n=5, isolated working dir, proposal inlined.

## Results

Coverage /4 (cell mean) · premise-seam catch /5:

| arm | Sonnet cov | Sonnet premise | Haiku cov | Haiku premise |
|---|---|---|---|---|
| A0 bare | 3.0 | 0/5 | 2.8 | 0/5 |
| A1 soul-prose-single | 4.0 | 5/5 | 4.0 | 5/5 |
| C2 generic-single | 4.0 | 5/5 | 4.0 | 5/5 |
| A2 soul-agentic | 3.4 | 2/5 | 4.0 | 5/5 |
| C1 generic-agentic | 3.8 | 4/5 | 3.8 | 4/5 |

The C2 difficulty-validation predicted where the signal would sit: seams 2–4 are
salient and near-saturate; the discriminator is **seam 1, the unverified premise**,
which bare reviewers miss 0/10 — they catch the three obvious problems and stop
short of questioning the claim the feature rests on.

## What the contrasts say

- **A2 ≈ C1 (Soul-vs-generic, agentic, equal compute).** Sonnet A2 ≤ C1; Haiku A2 ≈
  C1. The Soul doctrine adds **nothing** once roles are agents. The "roles = form"
  verdict replicates in the agentic regime. **The maturity hypothesis is not
  supported** — built as agents, Soul roles still only match a generic decomposition.
- **A1 = C2 (the prose twin).** Identical at both models. Soul framing is form in a
  single context too — the study's earlier null, reproduced exactly.
- **Agentic does not beat single-context decomposition.** A1/C2 hit 4.0 / premise
  5/5 at *both* models. The multi-agent topology ties at best (Haiku) and **loses at
  Sonnet** — while costing ~5× the calls. The weak-baseline hope (a small model
  can't hold four lenses at once, so dedicated agents should win) is **falsified**:
  Haiku in a single context already covers 4/4.
- **The real lever is decomposition.** Bare 2.9 / premise 0/10 → *any* explicit
  multi-perspective pass (generic or Soul, single or multi-agent) → ~3.8–4.0 /
  premise 4–10/10. The substance is "force several explicit perspectives, above all
  a skeptical one." A single generic prompt captures it.

## The mechanism: the synthesis funnel can *lose* findings

Every dedicated Skeptic/critic sub-agent caught the premise (Sonnet: 5/5 in both A2
and C1, grep + read-confirmed). But the synthesis step dropped it — only 2/5 (A2)
and 4/5 (C1) Sonnet syntheses kept it, demoting "the premise is unverified" to "not
a blocker." A single-context pass doesn't prune, because the same model writes the
premise into its own consolidated list. So the agentic topology adds a **lossy
synthesis bottleneck**: decomposition surfaces more, then synthesis discards some of
it. (Haiku prunes less — its longer 5–7-item blocker lists retain the premise — so
the loss is synthesis-prompt- and verbosity-dependent, not a law.)

## Verdict and bounds

**Roles-as-agents are still form.** Neither the Soul naming nor the multi-agent
orchestration beat a cheap single-context generic decomposition on this task; the
transferable substance is decomposition-into-perspectives itself. This **extends**
the study's headline from prose to agents rather than overturning it — and it points
the lean-vs-elaborate fork toward the lean record/convention substrate, not an
elaborate role-execution engine, on the evidence available.

Bounds, named honestly:
- **One task, breadth-shaped.** It rewards *coverage* across many heterogeneous
  defects, where decomposition trivially helps. It does **not** test *depth* — a
  single hard sub-problem where one agent's context or attention is the bottleneck
  and a dedicated agent could reason further. Multi-agent's theorised advantage is
  often depth and context-isolation on one hard thing, not breadth across many. The
  null bounds to breadth-coverage tasks; **depth-bottleneck tasks remain untested**
  and are the honest next probe if the agentic question is pursued.
- **The topology comparison is synthesis-sensitive.** "Agentic loses at Sonnet" is
  partly an artifact of the synthesis prompt; the defensible claim is the null —
  agentic did not *beat* cheap decomposition.
- n=5, two models, one artifact, low-salience domain; Opus deferred (no live signal
  at Sonnet/Haiku to motivate the frontier spend). The driver simulates the topology
  via one `claude -p` per role + a synthesis call — faithful to "dedicated context
  per role, then synthesise," not the Agent/Task tool.

Raw arms: `.soul/experiments/2026-05-29-agentic-roles/` (manifest + `arms/`).
