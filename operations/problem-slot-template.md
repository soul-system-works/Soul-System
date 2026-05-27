# Problem Slot Template

A framing prompt for the start of a non-trivial session — fill these fields
*before* implementation begins. Names the problem at two levels, the
constraints, the abstraction layer (if known), and what success looks like as a
*process* not a *solution*. Pairs with the seed §Mandatory Gates (the AL gate)
and the `writing-plans` skill.

Use when the problem is fuzzy, the scope is unclear, or the AI is about to
start work without a recorded framing. Skip for trivial bounded work.

---

```
PROBLEM:        [Insert problem statement here.]

DOMAIN:         [e.g. Software Engineering / Thermal Systems / Research]

EPISTEMIC TYPE: [What kind of truth are we pursuing?]
                e.g. Engineering approximation / Scientific rigor /
                Working software / Conceptual clarity

KNOWN CONSTRAINTS: [What is already known about limits, resources, scope.]

KNOWN ABSTRACTIONS: [If any — what varies, what decides whether it varies,
                     what cannot vary. Leave blank if unknown — the alignment
                     phase will develop this.]

SUCCESS LOOKS LIKE: [How will a human evaluating this run know it went well?
                     Not the solution — the quality of the process.]
```

---

**Source:** Lifted from the now-retired `operations/autonomous-session-template.md` (Problem Slot section, lines 50–67) when that file was retired at SOUL-091 (the rest of the template's machinery had been decomposed into modern instruments — see audit `docs/audits/2026-05-27-soul-console-v1-structure.md` §Section 4). The framing prompt had no modern equivalent and the Body chose to preserve it as a standalone artifact.
**Sub-class:** PROCEDURE (per the proposed A014 operations sub-classification convention).
**Adopted:** 2026-05-27.
**Status:** active.
