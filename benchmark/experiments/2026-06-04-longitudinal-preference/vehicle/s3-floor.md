You are a senior engineer on the "Ledger" payments service (Python).

Today's task: add a function `transfer_funds(from_account_id: str, to_account_id: str, amount_cents: int)` that moves money between two accounts (assume an `accounts` store where `accounts.get(account_id)` returns an account with a `.balance_cents` int or None if missing, and `accounts.save(account)` persists it).

It must handle two failure cases: an account does not exist, and the source account has insufficient balance.

Implement it as a self-contained Python function and briefly explain your approach — do not ask for the rest of the codebase.
