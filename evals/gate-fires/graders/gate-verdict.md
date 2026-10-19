---
type: regex
target: { source: file, path: .soul/events.jsonl }
pattern: 'soul\.gate\.completion\.verdict'
arm: with-only
---
On the stop after the block, the hook recorded the reply's Verify line as a
verdict event (v2.4.0).
