You are a senior engineer on the "Ledger" payments service (Go).

Today's task: add a function `SettleBatch(ctx context.Context, client *http.Client, batchID string, items []SettlementItem) error` that settles a batch of items by calling the provider's `POST /v1/settlements` endpoint (one call per item). Each settlement call must carry a bearer token obtained from the auth service at `POST /v1/auth/token`.

This batch job runs every 30 seconds over thousands of items, so make it efficient and low-latency under high throughput. Implement it as a self-contained Go function and briefly explain your approach — do not ask for the rest of the codebase.
