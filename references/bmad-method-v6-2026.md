---
id: bmad-method-v6-2026
csl: references.json#bmad-method-v6-2026
access: public
retrieved: 2026-05-27
file: none
grounds: [SOUL-098, SOUL-F041, SOUL-I035]
key-values:
  - value: "Always start a fresh chat for each workflow to avoid context limitations."
    defines: "BMAD's agent activation model — each agent is a skill invoked in a fresh chat, not a persona switch within one session"
    status: secondary-reading
    locus: "WebFetch summary of docs.bmad-method.org/llms-full.txt, 2026-05-27"
  - value: "For each story, repeat this cycle with fresh chats: | Step | Agent |"
    defines: "BMAD's sprint cycle is serial handoff between agents, not perspective switching within a worker"
    status: secondary-reading
    locus: "WebFetch summary of docs.bmad-method.org/llms-full.txt, 2026-05-27"
  - value: "12+ domain experts (PM, Architect, Developer, UX, and more)"
    defines: "BMAD's agent roster — phase-aligned specialists (Analyst, PM, Architect, SM, PO, Dev, QA, UX) rather than continuous-posture lenses"
    status: secondary-reading
    locus: "WebFetch summary of github.com/bmad-code-org/BMAD-METHOD README, 2026-05-27"
  - value: "Each workflow has a skill you invoke by name in your IDE (e.g., bmad-prd). Your AI tool will recognize the bmad-* name and run it."
    defines: "BMAD agents ship as Claude Code skills (or IDE equivalents) at .claude/skills/bmad-agent-{role}/SKILL.md"
    status: secondary-reading
    locus: "WebFetch summary of docs.bmad-method.org/llms-full.txt, 2026-05-27"
related: [[SOUL-I035]], [[SOUL-F041]], [[SOUL-087]]
---

BMAD-METHOD (Breakthrough Method for Agile AI-Driven Development) is an AI-agent
framework shipping a roster of phase-aligned named agents — Analyst, PM, Architect,
Scrum Master, Product Owner, Developer, QA, UX Designer (V6; V6 consolidated
Barry/Quinn/Bob into the Developer "Amelia"). Distributed as Claude Code skills
(and equivalents for other IDEs) under `.claude/skills/bmad-agent-{role}/SKILL.md`,
configured via `_bmad/config.toml` and per-skill `_bmad/custom/bmad-agent-{role}.toml`.

**Load-bearing for the Soul System** because the seed (§External Skills and Tools)
makes a *structural-composability claim* about BMAD: that Soul roles can layer over
BMAD agents "without restructuring." Testing that claim is exactly what SOUL-F041
discharges. The findings here ground F041 in BMAD's actual architecture rather than
in the seed's (untested) assumption about it.

**The decisive empirical points:**
1. BMAD agents are **skill-invocations in fresh chats**, not perspective switches.
   This makes them **process-shaped**, not perspective-shaped.
2. The sprint cycle is **serial handoff** between agents, with explicit "fresh chat"
   guidance to avoid context bleed.
3. Every named BMAD agent is **phase-aligned** (a discrete step in the SDLC); there
   are no continuous-posture agents (nothing that observes silently across all
   phases the way Soul's Witness does).
4. "Party Mode" exists as a non-default exception — multiple personas in one
   session — but is described as a special mode for collaborative discussion,
   not the standard invocation pattern.

**VALIDITY BASIS (F028):** Existence of BMAD-METHOD as a framework, its agent
roster, its skill-based activation model, and its phase-aligned topology are
**triply confirmed** across three independent sources (official docs, GitHub
README, third-party explainers — Benny Cheung, Vishal Mysore, Reenbit). The
verbatim quotes recorded in `key-values` above are **second-hand readings via
WebFetch's model summarization**, not primary-text reads — confirm against the
live docs before quoting as authoritative. The *structural* conclusion (phase-
based agents, serial handoff, no continuous-posture role) is well-supported by
the convergence of sources and is what F041 rests on; the *quotes* themselves
are pointers, not the ground.

**Open question:** whether CrewAI and AutoGen — the other two frameworks the
seed names — are similarly phase-shaped or include continuous-perspective roles
(supervisor / monitor / observer patterns). Untested in this beat per scope
guard ("BMAD only" per SOUL-I035 §NOTES). A follow-up Researcher beat could
test those two; if BOTH are also phase-shaped, the seed's claim collapses
broadly rather than just for BMAD.

---
**Source:** Field acquisition for SOUL-I035 (the BMAD Researcher beat).
**Adopted:** 2026-05-27
**Status:** active
