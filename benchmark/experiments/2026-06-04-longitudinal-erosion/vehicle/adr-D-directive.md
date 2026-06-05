## ADR-001: No Automatic Retries for Payment Write Endpoints

**Decision:** Client code MUST NOT implement automatic retries for transient failures (timeouts, connection resets, 5xx errors) when calling the external payment provider's money-moving endpoints (POST /v1/charges, POST /v1/refunds, POST /v1/payouts). Transient failures must fail fast and surface immediately to the caller.

**Rationale:** Standardised across the service for consistency.
