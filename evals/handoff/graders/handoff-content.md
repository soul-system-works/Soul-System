---
type: llm
focus: { source: file, path: .soul/handoff.md }
---
This file is a session handoff. PASS only if it (1) names the specific in-progress change (adding TTL expiry to the Cache in app/cache.py, currently uncommitted and unfinished) and (2) gives at least one concrete next step (e.g. implement the expiry check in Cache.get and add tests using an injectable clock). FAIL if it is generic, omits the in-progress change, or has no actionable next step. If the file is missing or empty, FAIL.
