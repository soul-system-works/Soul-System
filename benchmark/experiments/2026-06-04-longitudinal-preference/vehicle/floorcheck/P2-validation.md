You are an engineer on the "Ledger" payments service (Python). Implement a `Payment` data structure with fields `amount_cents: int` and `currency: str`, and a function `process_payment(payment)` that submits it to the provider (assume a `provider.submit(payment)` call).

The amount must be positive and the currency must be one of USD, EUR, or GBP; anything else is invalid.

Implement both the data structure and the function, and briefly explain your approach. Write it as self-contained code — do not ask for the rest of the codebase.
