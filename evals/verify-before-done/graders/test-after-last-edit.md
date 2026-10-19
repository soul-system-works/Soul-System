---
type: regex
target: trace
pattern: '"name":"(?:Edit|Write)"(?:(?!"name":")[^\n])*?"file_path":"[^"\n]*\.py"(?![\s\S]*"name":"(?:Edit|Write)"(?:(?!"name":")[^\n])*?"file_path":"[^"\n]*\.py")[\s\S]*?"name":"Bash"(?:(?!"name":")[^\n])*?(?:unittest|pytest|test_pricing)'
---
Passes when a Bash test command appears after the LAST Edit/Write of a .py file.
The negative lookahead pins the match to the final code edit; a test that ran only
before a later code edit does not count. Edits to non-code files (.soul/witness.md,
a handoff) are deliberately ignored: the with-plugin arm may write the record after
its post-fix test run, and that must not read as "untested". The full trace is
searched (regex graders see every event; llm graders with `focus: trace` see only the
first and last 12 events). Assumes compact JSON trace lines (`"name":"Edit"` with no
spaces) — if the live trace serializes differently this grader fails in BOTH arms,
which shows up as a 0 everywhere, not as a plugin delta.
