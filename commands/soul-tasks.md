---
description: Refresh the task tracker against the durable records, then present a tiered list of likely next options (now / next / later). The forward-momentum view on demand.
---

# /soul-tasks — refresh the tracker, show what's next

The forward twin of the completion gate: surface where to go next so the Body
does not have to ask (SOUL-I010 / the proactive-next-steps discipline). The
harness task list goes stale across sessions; this command reconciles it with the
durable records and emits a tiered next-options view. Its twin is `/soul-explain`
(describe, don't decide); this one points forward.

## What to do

1. **Reconcile the tracker with reality.** Read the durable forward stores —
   `ideas.md` (ripe ideas), `findings/open/` (open questions), the `witness.md`
   tail (recent state), and `.soul/handoff.md` if present. Update or prune the
   harness task list so it reflects active work, not a stale snapshot.
2. **Present a TIERED next-options list:**
   - **Now** — in-flight or immediate.
   - **Next** — ripe; earns doing soon.
   - **Later** — parked, trigger-gated, or awaiting evidence.
   Each item **points at its durable source** (idea ID, finding ID, spec) — do not
   copy the content in. **Prophet / Cartographer:** read trajectory and map the
   tiers; **Archivist:** keep the ephemeral list pointing at the durable record.
3. **Tag by value/effort** where it helps. Keep it skimmable.
4. **Recommend the single best next move** — but do not start it. The Body chooses.

## What not to do

- Do **not** duplicate the durable records into the task list — surface and point,
  do not copy (forward state is scattered across three stores; this view unifies
  without re-storing — SOUL-I010).
- Do **not** begin the work. This is the forward VIEW, not execution.
- Do **not** invent options ungrounded in the records. The forward twin of
  [[clarification-drift]]: surface real next steps, not speculative ones.

---

**Source:** Built by the Artificer for SOUL-I013. The forward twin of
`/soul-explain`, and the forward complement of the completion gate. Operationalizes
SOUL-I010 / the proactive-next-steps discipline (don't make the Body ask), while
keeping the task list a pointer to the durable records, not a duplicate of them.
**Adopted:** 2026-05-21. **Status:** active.
