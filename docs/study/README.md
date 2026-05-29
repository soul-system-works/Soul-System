# Does a meta-doctrine system change model behaviour, or just make it legible?

A self-ablation study of the Soul System — its always-on doctrine, its Council
roles, and its `/soul-*` instruments — measured against length-matched controls
under equal compute.

This directory is the **format-agnostic artifact corpus**: the method, every
probe's design + data + verdict, the consolidated result maps, and the resulting
lean-down decision. It is written so it can be rendered as either a long-form essay
(the journey + the verdict) or a formal preprint (method → results → bounds) —
the data is the same; only audience and language differ.

## The question

The Soul System loads a philosophy (roles, gates, doctrine) into every session and
accumulates a record (witness / findings / amendments / ideas) across sessions. The
implicit promise is that this *changes the work for the better*. Does it — or does
it change the **form** of the work (legibility, auditability) without changing its
**substance** (the decisions and answers) or **reliability**?

## The method in one line

Run the same task with the system loaded and without it — **and** with a
length-matched semantically-empty filler of the same token budget. If the filler
reproduces the gain, the "improvement" was compute (more context), not the doctrine.
A "substance" verdict that vanishes under equal compute is not substance. See
[`00-method.md`](00-method.md).

## The headline result (as of 2026-05-28)

The split is **what the content is *for*,** not "system vs no system." Two things
survive the equal-compute / generic-alternative control:

1. **Carrying project-specific knowledge & conventions** the model can't derive and
   a *generic equivalent gets wrong*. Measured twice: recall (a recorded finding,
   F038, → 10/10 trap-avoidance vs 2/5 for a length-matched irrelevant record) and
   distill (the project's counter-default "docs-near-code" convention flips a decision
   that generic principles get backwards). This is the record + a small always-on
   rule-set. **The clearest win.**
2. **The anchoring discipline at weak baselines** — when a weaker model is about to
   build on an unverified premise, the doctrine's content makes it stop. Survives the
   control (replicated); does **not** persist to the frontier (there a generic
   check-nudge suffices).

Everything that tries to make the model **reason better generically** — forcing
roles/perspectives, trajectory-reading, compliance-resistance at any stakes, the
handoff *format*, the verify *checklist format* — **dissolved under the control:** a
generic equivalent matched it. **The control caught four false positives**
(trajectory, compliance-flag, compliance-withhold, a keyword-illusion verify "win").
Largest un-measured value: **longitudinal** accumulation across many sessions; the
recall probe is the first single-shot reach at it.

**Roles-as-agents (added 2026-05-29).** A follow-up probe tested the obvious
objection to "roles = form": maybe roles only look like form because they were
measured as *prose*, never as *dedicated subagents*. Built as agents (one subagent
per Council role + synthesis), Soul roles still matched a generic decomposition
(A2 ≈ C1, equal compute) — and the multi-agent topology did **not** beat one agent
told to work through the same perspectives in a single context (it tied at best and
lost where the synthesis step pruned valid findings). The substance is
*decomposition into explicit perspectives* — cheap, generic, single-context — not
the Soul framing and not the agentic orchestration. The "form" verdict **extends
from prose to agents.** Bounds: one breadth-coverage task; depth-bottleneck tasks
(where one agent's context is the limit) remain untested. See
[`04-agentic-roles.md`](04-agentic-roles.md).

## Index

| File | Contents |
|---|---|
| [`00-method.md`](00-method.md) | Self-ablation under equal compute; controls C1/C2/C3; scoring discipline |
| [`01-doctrine-results.md`](01-doctrine-results.md) | I040/I041 — the regime × task-structure map for the always-on doctrine |
| [`02-instrument-results.md`](02-instrument-results.md) | The `/soul-*` instruments: handoff, recall/traceability, verify, distill |
| [`03-leandown.md`](03-leandown.md) | The ruthless keep/cut decision → a lean Soul-System |
| [`04-agentic-roles.md`](04-agentic-roles.md) | Roles-as-*agents* vs roles-as-prose — the maturity confound; "form" extends to agents |
| [`data/`](data/) | Consolidated result tables |

## Reproducibility note

Raw arm outputs live under `.soul/experiments/<date>-<probe>/` (gitignored — bulky
and local). The distilled designs, scores, and verdicts are lifted into this tracked
corpus and into the durable record (`witness.md`, `amendments/`, `ideas.md`). Each
probe section cites its raw-arm directory.

**Status:** corpus complete (`README` + `00`–`03` written). Doctrine arc (I040/I041)
closed; all four instrument probes measured (handoff, recall, verify, distill); the
lean-down recommendation is drafted ([`03-leandown.md`](03-leandown.md)). The cut
itself awaits Body approval (held). Optional polish remaining: a consolidated
`data/` table set, and rendering into a chosen publication format (blog / preprint).
