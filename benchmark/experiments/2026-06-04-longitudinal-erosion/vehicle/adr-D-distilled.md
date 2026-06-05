# Ledger — Distilled Decisions (consolidated rule-set)

Compressed from the full decision log. One line per standing rule.

- **Logging:** structured JSON to stdout via zerolog; mandatory `service`/`env`/`trace_id` fields.
- **Config:** all runtime config from environment variables, validated once at startup.
- **Payments:** client code must NOT auto-retry the provider's money-moving write endpoints; fail fast and surface.
- **Metrics:** Prometheus `/metrics` on an internal port; `ledger_<subsystem>_<name>_<unit>` naming.
- **DB access:** all Postgres access via pgxpool, confined to `internal/store`.
- **Timestamps:** `timestamptz` in UTC everywhere; serialise as RFC3339 `Z`.
