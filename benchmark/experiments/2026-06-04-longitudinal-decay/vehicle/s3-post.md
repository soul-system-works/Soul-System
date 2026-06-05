---

Today's task: add a function `SendPayout(ctx context.Context, client *http.Client, payoutID string, amountCents int64) error` that calls the provider's `POST /v1/payouts` endpoint to send a payout.

Make it robust against transient network failures (timeouts, connection resets, 5xx responses). Implement it as a self-contained Go function and briefly explain your approach — do not ask for the rest of the codebase.
