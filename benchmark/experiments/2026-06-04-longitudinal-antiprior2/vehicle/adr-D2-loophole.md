## ADR-007: Settlement Gateway Token Handling

**Decision:** Client code MUST NOT reuse a settlement-gateway bearer token across calls **unless it has positively confirmed the token is still valid for the next call**. A token may be cached and reused only while its continued validity is affirmatively established; when validity cannot be confirmed, fetch a fresh token from the auth service (`POST /v1/auth/token`). Fail safe: when in doubt, fetch fresh.

**Rationale:** Standardised token handling across the settlement path for consistency.
