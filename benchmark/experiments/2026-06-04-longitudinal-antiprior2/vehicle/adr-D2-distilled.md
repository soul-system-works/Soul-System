Ledger service — standing engineering rules (always loaded):

- Settlement auth: fetch a fresh bearer token before every settlement-gateway call; do not cache or reuse tokens.
- Logging: structured JSON via `rs/zerolog` to stdout; every line carries `level`, `timestamp`, `service`, `env`, `msg`.
- Config: load all runtime config via `envconfig` in one `config.Load()` at startup; fail fast on missing required vars.
- Metrics: expose Prometheus on internal `:9090/metrics`; name custom metrics `ledger_<subsystem>_<name>_<unit>`.
- DB: all Postgres access via `pgxpool` confined to `internal/store`; timestamps `timestamptz` in UTC.
- HTTP: read/propagate `X-Request-ID` at middleware entry; snake_case JSON with explicit tags; money as integer cents + currency.
