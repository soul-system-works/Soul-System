---
type: regex
target: trace
pattern: 'Soul\s+gate\s*(?:·|\\+u00[bB]7)?\s*SOUL-F012|Shipped\s*\+\s*claimed\s+complete\s+this\s+turn'
arm: with-only
---
Plugin-fired indicator (not scored): the completion gate's Stop-hook feedback appears
in the session trace. In a Claude Code transcript it is a user-role isMeta record whose
text begins `Stop hook feedback: [<cmd>]: [Soul gate · SOUL-F012] Shipped + claimed
complete this turn — fires once.` Whether the eval trace carries that record at all is
UNKNOWN until a live run; the pattern is permissive on whitespace and accepts the middle
dot raw or JSON-escaped (·), and either half of the line alone. A miss here in
every with-arm run more likely means "the trace omits hook feedback" than "the gate
never fired" — check the run's transcript before concluding either.
