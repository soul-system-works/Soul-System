# The skill-routing probe — does knowing *which* skill to deploy beat the model picking?

The agentic-roles probe ([`04`](04-agentic-roles.md)) found that roles-as-agents
add nothing over a generic decomposition — but it held *tools at zero*. The Body
then sharpened the real hypothesis: a Council role isn't just a perspective, it's a
purpose backed by a *curated bundle of skills/hooks*, and the Soul System is the
layer that knows **which bundle to deploy and when** — a meta-layer over skill
ecosystems (BMAD and the like), not a replacement. The interesting, Soul-specific
claim (Claim B) is **routing/expertise**: does Soul's *what+when* knowledge beat the
realistic default — the model selecting skills for itself from a catalog? ("Equipping
a role with tools helps at all" is Claim A, a trivial floor.)

## Design

A diagnosis task with a **counter-default** correct answer: a Python service whose
RSS climbs for days. The obvious read is "memory leak — go hunt it with a heap
profiler." The correct read is often **allocator fragmentation** — RSS grows while
the Python heap stays flat; the fix is `MALLOC_ARENA_MAX` / jemalloc, and a leak
profiler finds *nothing*. A 24-skill catalog, engineered for selection difficulty:

- **non-obvious-correct:** `allocator-tuning-guide` (right content; its name doesn't
  shout "memory grows over days" unless you already know fragmentation is the cause).
- **anti-relevance trap:** `memory-leak-hunt` (looks perfect; leads to heap-snapshot
  leak-hunting that dead-ends on a no-leak case).
- near-misses (`gc-tuning`, `heap-dump`, `oom-killer`) + ~19 distractors.

Arms: **floor** (task only) · **all-on** (all 24 contents — the degradation regime)
· **catalog-pick** (model names what to load → inject → solve) · **soul-oracle** (the
correct bundle injected — perfect what/when routing). Decisive contrast:
**oracle vs catalog-pick** — same ecosystem, differ only on whether Soul-curation
beats the model's own selection. Sonnet + Haiku, n=5.

## The validation forced a redesign — and that's a finding

With *no budget*, catalog-pick **over-selects**: the model loads 6–9 skills, grabbing
the trap **and** the correct skill **and** everything plausible (Sonnet picked the
correct skill 5/5, Haiku 4/5). The trap never bites — it's taken *alongside* the
right skill, not *instead*. **When loading is free, curation adds nothing: a wide net
catches the non-obvious skill for you.** Routing can only matter under a **selection
budget** — which is the real constraint (always-on tool sets degrade selection past
~10; the Soul's own "never always-on past budget" rule). So the faithful control is
**pick2: "load at most 2."** Floor also showed Sonnet *already knows* the
counter-default answer (5/5) — a ceiling — while Haiku gets it ~1/5. Haiku carries
the outcome signal; Sonnet is a ceiling reference.

## Results — surfaced the counter-default correct path, /5

| arm | Sonnet | Haiku |
|---|---|---|
| floor | 5/5 *(ceiling)* | ~1/5 |
| all-on | 5/5 | 5/5 |
| **oracle** (correct skill given) | 5/5 | **5/5** |
| **pick2** (model self-picks ≤2) | 5/5 | **1/5** |

Selection accuracy under budget≤2 (loaded `allocator-tuning-guide`): Sonnet 5/5,
**Haiku 1/5.**

## The decisive contrast: oracle 5/5 vs pick2 1/5 at Haiku

This is the first win on the **what/when-*deployment* face** — recall ([`02`](02-instrument-results.md))
already showed that *having* the right knowledge beats a generic equivalent
(record → 10/10 vs irrelevant-record 2/5); this shows *deploying the right piece*
does too. Both are Soul-shaped capabilities beating the generic alternative under
control. Forced to pick two, the
weak model spends them on the obvious `memory-leak-hunt` trap (5/5) plus a
distractor, and misses the non-obvious-correct skill (4/5). Handed the right skill
(oracle), it solves 5/5. Curated *what/when* routing beats the model's own budgeted
self-selection.

The mechanism, read-confirmed, is sharper than expected: the wrong pick *steers the
diagnosis wrong*. haiku-4 noticed the RSS-vs-heap divergence (the right clue!) but
attributed it to the **fd-leak** skill it had loaded; haiku-5 blamed **GC** (its
other pick). Loading the wrong bundle produced the wrong root cause. The one Haiku
run that loaded the allocator skill solved it. Usage is not the bottleneck (oracle
5/5, all-on 5/5) — **selection is.**

## The bounds are the finding — same shape as anchoring and recall/distill

Routing-curation has substance in exactly one cell: **weak model × tight budget ×
counter-default-correct skill.** It dissolves elsewhere:

1. **Frontier dissolves it.** Sonnet already knows the answer; oracle = pick2 = floor
   = 5/5. Routing is form at the frontier.
2. **No budget dissolves it.** Free selection over-selects and catches the skill
   anyway. The *budget* is what creates the routing problem.
3. **Obviousness dissolves it.** The win needs a tempting trap + a non-obvious-correct
   skill; where the right tool is obvious, the model self-selects fine. Value scales
   with how *counter-default* the right skill is — the same axis as recall and distill
   (knowledge a generic path gets wrong).

## Verdict and what it means for the fork

Together with `04`: the **elaborate agentic** direction (role-as-subagent) is not
supported, but the **routing/curation layer over a catalog has measured substance** —
bounded, and as an **upper bound** (oracle = *perfect* routing; a real router is
imperfect). This supports a **tested, selective skills catalog** as a lean-Soul
keeper, with value concentrated where weaker models meet budget pressure — precisely
the "layer that holds the expertise on what and when to deploy" the Body described.
The synthesis future is a lean record/convention substrate + a tested catalog +
budget-aware routing, *not* an elaborate role-execution engine.

Bounds: oracle is the value ceiling — the open question is whether a *built* router
can approach it better than the model's own pick (now worth asking; previously
unsettled). Procedure-knowledge text proxy (not real tool-skills); one task; n=5; one
budget point (≤2); Haiku-only outcome signal; multi-task/longitudinal what+when still
untested. Raw arms: `.soul/experiments/2026-05-29-skill-routing/`.
