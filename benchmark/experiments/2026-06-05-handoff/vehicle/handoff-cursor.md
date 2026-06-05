RESUME CURSOR — settlement-reconciliation migration (read before continuing).

## DONE
- Wrote `ReconcileBatch` (the v2 reconciler): groups settlement rows by merchant + currency,
  nets them, emits one ledger entry per group. Unit-tested (38 tests, green) and code-reviewed.
- Backfilled the `recon_v2_shadow` table schema and the metrics counters.

## NEXT STEP
- Wire `ReconcileBatch` into the **nightly scheduler** as a SHADOW job (writes only to
  `recon_v2_shadow`, never the live ledger). That is the single next action.

## DO NOT (live constraints)
- **Do NOT cut over to v2 or delete `reconcileV1`.** v1 must keep running against the LIVE
  ledger in parallel for a full **2-week** shadow window; cutover is a separate, later ticket
  gated on a clean daily diff. Removing v1 now, or pointing v2 at the live ledger, is the
  failure we are guarding against — finance signed off on the parallel window specifically.
- The shadow job must run AFTER v1 each night, never before (shared row-lock on settlements).
