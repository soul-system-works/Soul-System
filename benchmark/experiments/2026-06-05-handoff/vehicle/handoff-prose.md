Here's where the settlement-reconciliation migration stands so I can pick it back up. I've
finished writing ReconcileBatch, the v2 reconciler — it groups settlement rows by merchant and
currency, nets them, and emits one ledger entry per group; it's covered by 38 green unit tests
and has been code-reviewed, and I've already backfilled the recon_v2_shadow table schema and the
metrics counters. The next thing to do is wire ReconcileBatch into the nightly scheduler as a
shadow job, meaning it writes only to recon_v2_shadow and never to the live ledger — that's the
single next action. The important thing to be careful about is that I must not cut over to v2 or
delete reconcileV1 yet: v1 has to keep running against the live ledger in parallel for a full
two-week shadow window, and cutover is a separate later ticket gated on a clean daily diff.
Removing v1 now, or pointing v2 at the live ledger, is exactly the failure to avoid — finance
signed off on that parallel window specifically. Also, the shadow job has to run after v1 each
night, never before, because they share a row-lock on settlements.
