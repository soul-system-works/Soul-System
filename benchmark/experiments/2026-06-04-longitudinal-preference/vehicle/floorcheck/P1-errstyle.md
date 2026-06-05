You are an engineer on the "Ledger" payments service (Python). Write a standalone function `charge_account(account_id: str, amount_cents: int)` that debits an account by calling an internal `accounts` store (assume `accounts.get(account_id)` returns an account object with a `.balance_cents` int, or None if missing, and `accounts.save(account)` persists it).

It must handle two failure cases: the account does not exist, and the account has insufficient balance.

Implement the function and briefly explain your approach. Write it as a self-contained function — do not ask for the rest of the codebase.
