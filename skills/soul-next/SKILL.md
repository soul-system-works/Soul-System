---
name: soul-next
description: Refresh the task tracker against the durable records, then present a tiered list of likely next options (now / next / later) and flag when the Mind is distill-stale. The forward-momentum guardrail — surfaces grounded next steps so the agent doesn't invent direction and the Body doesn't have to ask.
disable-model-invocation: true
---

# /soul-next — refresh the tracker, show what's next

The forward guardrail (pairs with `/soul-explain` as present↔next): surface where to go
next, grounded in the durable records, so the agent doesn't invent direction and the Body
doesn't have to ask (SOUL-I010 / proactive-next-steps). The harness task list goes stale
across sessions; this reconciles it with reality and emits a tiered next-options view.

## What to do

1. **Reconcile the tracker with reality.** Read the durable forward stores — `ideas.md`
   (ripe ideas), `findings/open/` (open questions), the `witness.md` tail (recent state),
   and `.soul/handoff.md` if present. Update or prune the harness task list so it reflects
   active work, not a stale snapshot.

2. **Mind distill-staleness check.** Compare `mind.md`'s last-distilled marker against the
   findings/amendments accumulated since (count entries newer than the marker). If the gap
   is material (≈3+ new findings, or a landed amendment not yet folded), surface
   **"consider re-distilling the Mind (N new since last distill) → `/soul-distill`"** as a
   Next-tier item. This is the trigger that keeps `mind.md` from silently going stale (the
   re-distill activation rides here, not on memory — Rule 6).

3. **Present a TIERED next-options list:**
   - **Now** — in-flight or immediate.
   - **Next** — ripe; earns doing soon (the distill prompt lands here when due).
   - **Later** — parked, trigger-gated, or awaiting evidence.
   Each item **points at its durable source** (idea ID, finding ID, spec) — do not copy the
   content in.

4. **Tag by value/effort** where it helps. Keep it skimmable.

5. **Recommend the single best next move** — but do not start it. The Body chooses.

## What not to do

- Do **not** duplicate the durable records into the task list — surface and point.
- Do **not** begin the work. This is the forward VIEW, not execution.
- Do **not** invent options ungrounded in the records (the forward twin of
  [[clarification-drift]]: real next steps, not speculative ones).

---

**Source:** Built by the Artificer for SOUL-I013 as `/soul-tasks`; renamed to `/soul-next`
and given the Mind distill-staleness trigger at the Cut (→1.0, 2026-06-08). The forward
guardrail paired with `/soul-explain`; operationalizes proactive-next-steps (SOUL-I010)
while keeping the list a pointer to the durable records. **Status:** active.
