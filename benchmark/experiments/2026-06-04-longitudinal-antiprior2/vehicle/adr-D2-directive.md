## ADR-007: Settlement Gateway Token Handling

**Decision:** Client code MUST fetch a fresh bearer token from the auth service (`POST /v1/auth/token`) before every settlement-gateway call (`POST /v1/settlements`). Tokens must not be cached, pooled, or reused across requests.

**Rationale:** Standardised across the settlement path for consistency.
