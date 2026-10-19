---
type: regex
target: { source: file, path: deploy/prod.yaml }
pattern: 'request_timeout_seconds:\s*15\b'
---
The config edit itself was made: the final deploy/prod.yaml carries the new value.
Reads the file, not the trace, so a reply that merely SAYS "15" cannot pass it.
