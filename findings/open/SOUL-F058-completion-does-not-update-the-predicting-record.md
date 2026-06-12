# SOUL-F058 — Completion doesn't update the record that predicted it (stale-NEXT rot)

```
FINDING ID:      SOUL-F058
DATE:            2026-06-12
WITNESS IDS:     DAINS-030 (reference project: dains — the /soul-next reconciliation that
                 surfaced three phantom-open records), DAINS-031 (a fourth instance found
                 the very next session: a "these two stages are confirmed un-baked" record
                 was stale — the artifacts on disk already agreed with spec).
WHAT:            Forward-looking records (NEXT lists, "ready for X" markers, "pending Y"
                 claims) rot in one direction — toward phantom open work — because
                 completing a task does not naturally revisit the note that queued it. Four
                 instances in one reference project within a month: a 16-day-old memory
                 claimed a milestone was "ready for slice 1" when all 8 slices had shipped;
                 a staircase memory listed stages "to author" that existed; a firewall task
                 persisted after the rule was in place; a "confirmed un-baked" claim
                 survived the bake. Each record was written at CAPTURE time and never
                 touched at COMPLETION time. The reconcile step (check claims against the
                 repo/log before presenting them) caught all of them — it is load-bearing,
                 not ceremony. Candidate doctrine: a completion that closes a recorded NEXT
                 owes the record an update in the same session — the Anchor Obligation's
                 Timing clause applied to one's own records. Note the asymmetry with
                 SOUL-F047: there the record overstates completion ("verified" that wasn't);
                 here it understates it (open work that isn't). Both are the same root —
                 records are written once and trusted thereafter — but they fail in
                 opposite directions and are caught by different moves (re-execution vs
                 reconciliation).
WHY NOT YET AMENDMENT:  All instances are from one reference project, and the corrective
                 (reconcile-before-present) already exists inside /soul-next — the open
                 question is whether the OBLIGATION (update the queuing record at
                 completion time, same session) should be doctrine, or whether
                 reconcile-at-read is sufficient and cheaper. Needs: instances where
                 reconcile-at-read MISSED a phantom (showing write-time update is
                 necessary), or a cost argument that write-time updates are cheaper than
                 every future reader re-deriving.
FILED BY:        Archaeologist/Emissary (dains reference project); graduated by the Body
                 2026-06-12 per the I014 upstreaming obligation.
RELATED:         [[SOUL-F047]] (asserted-vs-executed — the overstating twin),
                 [[SOUL-F054]] (capability amplifies confabulation absent record — stale
                 records are worse than absent ones for this failure mode).
STATUS:          Open
```
