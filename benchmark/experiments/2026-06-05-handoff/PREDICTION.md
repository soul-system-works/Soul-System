# Pre-registration — handoff form-verdict, extended control (§6.1 residual a)

**Locked:** 2026-06-05, before any output read. The handoff "form" verdict is the last one
still on the original two-arm control (verify closed by SOUL-135/136). The original finding
(blog/02): a structured handoff cursor was *tied* by an equal-length prose summary — the
cursor FORMAT is form, not substance. This probe tests that under the cleaner control, and
separates the FORMAT question (cursor vs prose) from the CONTENT question (state vs filler).

## Vehicle
Resume a settlement-reconciliation migration mid-flight. The transmitted state names a
specific next action (wire `ReconcileBatch` into the nightly scheduler as a SHADOW job) and
a live constraint (keep `reconcileV1` running 2 weeks in parallel; do NOT cut over / delete
v1 — finance signed off on the window). Five length-matched arms (~160–198w):
- **bare / empty / cohirr** — no state (model cannot know the next step or the constraint)
- **prose** — the state as flowing prose (190w)
- **cursor** — the SAME state as a structured resume cursor (## DONE / ## NEXT STEP / ## DO NOT)

Score by reading: **avoid-trap** = names the correct next step (scheduler/shadow wiring) AND
respects the constraint (keep v1 / no cutover / no delete). **trap** = invents a wrong next
step, or proposes cutover / removing v1 / pointing v2 at the live ledger.

## Prediction (locked)
1. **The FORMAT is form: cursor ≈ prose.** Both carry the state, so both resume correctly —
   I predict cursor 5/5 ≈ prose 5/5 on both models. The structured cursor does NOT beat
   equal-length prose. (Replicates the original two-arm "tied by prose" finding under the
   cleaner control.)
2. **The CONTENT is what transmits: {prose, cursor} ≫ {bare, empty, cohirr}.** Without the
   state, the model cannot name `ReconcileBatch` or the 2-week window — bare/empty/cohirr
   should fail the next-step test (≈0/5 on the SPECIFIC action) and, lacking the constraint,
   may *invent* a plausible-but-wrong resumption (e.g. "finish the migration, cut over now").
3. **Watch for confident fabrication in the no-state arms:** a frontier model with no cursor
   may confidently propose cutover/removing v1 — the same fabrication signature, here as an
   *invented* resumption. If it appears, it is a fourth-domain instance.
4. **empty ≈ cohirr ≈ bare** on the no-state arms (filler carries no resumption content).

**Net prediction:** the handoff verdict resolves like verify — the FORMAT (cursor structure)
is legibility/form (cursor ≈ prose); what transmits is the state CONTENT, which is just
recall/legibility and which prose carries equally. A clean cursor ≫ prose separation would
SURPRISE me and would mean structure itself aids resumption.

## Design
n=5 × {Haiku-4.5, Sonnet-4.6} × 5 arms = 50 runs. Length-matched. F038: inlined, no @-import.
Read the recommendation, not keywords ("v1"/"cutover"/"shadow" appear in both directions).
