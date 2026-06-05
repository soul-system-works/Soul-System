Project engineering record — selected doctrine (read before declaring any work complete):

D012 — COMPLETION GATE. Before calling anything complete, consult reality. Local tests passing is NOT global correctness: a green unit suite verifies the parts in isolation; it does not validate the invariant the WHOLE system must satisfy. Verification (did I build the thing right?) is not validation (did I build the right thing, and does it hold against reality?). Therefore: before declaring done, name the single global invariant the change must preserve, and check it against the real system — production-shaped data, the actual downstream consumer, an external anchor — not against the test fixtures. Internal coherence is not enough; a change can pass every local check and still violate the invariant the moment it meets the real world.

D013 — ANCHOR OBLIGATION. Any claim that the work is finished is a claim about reality and needs an external anchor proportionate to its weight (a real run, real data, the real consumer), never just self-consistent reasoning.

D004 — when something feels unfinished before you can articulate why, record it and do not declare done; that signal is usually a real uncovered case.
