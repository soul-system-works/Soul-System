Ledger — standing engineering conventions (project rules, always in effect):

- Documentation lives NEXT TO the code it describes — module-level `README.md` files beside the package, doc comments on exported symbols, and inline markers — and NOT in a separate top-level `docs/` tree. A separate documentation directory reliably drifts from the code and goes stale, because it is updated in a different change than the code it describes. Co-located documentation is edited in the same diff as the code, so it stays correct. This is a hard project rule, adopted after a prior service kept a central `docs/` tree that was roughly 40% out of date within two quarters and actively misled three on-call engineers during an incident.
- All monetary values are integer cents plus an explicit currency code; never floating point.
- Errors are returned as values; never panic across a package boundary.
- Every exported function carries a doc comment stating its contract and failure modes.
- All database access is confined to the `internal/store` package; no SQL elsewhere.
- Timestamps are stored as `timestamptz` in UTC and serialized as RFC3339.
- Runtime configuration is loaded once at startup; missing required variables fail fast.
- Structured JSON logging via `zerolog`; every line carries `service`, `env`, and `request_id`.
