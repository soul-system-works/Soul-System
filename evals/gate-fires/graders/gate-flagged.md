---
type: regex
target: { source: file, path: .soul/events.jsonl }
pattern: 'soul\.gate\.completion\.flagged'
arm: with-only
---
The gate fired: the hook appended its flagged event to the project's event log.
This is the hook's own record, so it does not depend on what the trace carries.
