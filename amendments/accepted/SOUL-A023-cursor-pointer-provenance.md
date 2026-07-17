AMENDMENT ID:    SOUL-A023
DATE:            2026-07-16
WITNESS IDS:     RSENS-012 (the anchoring instance, RealisticSensors project
                 log — a session-7 cursor claimed an ADR "lives in the SEPARATE
                 dains repo, not on disk"; false, cost to check one `ls`, and
                 the claim rode into a Body decision before the completion gate
                 caught it. RSENS-009 is a prior unrecognized instance of the
                 same shape.) Finding SOUL-F061 carries the full analysis. A
                 third live instance, same day as acceptance: the 2026-07-16
                 Soul-System resume found the cursor two sessions stale, caught
                 only by cross-checking git status against the cursor's claims.
WHAT CHANGES:    Two edits closing the hole F061 names — nothing in a handoff
                 cursor distinguishes a pointer the writing session verified
                 from one it merely remembered, and the resume silently skips
                 pointers that fail to resolve.
                 (1) /soul-handoff: every POINTERS entry carries a provenance
                 mark — `[read]` (this session opened it) or `[inherited]`
                 (carried from a prior cursor or memory, unverified). Never
                 upgrade to `[read]` without opening it. Where a cross-repo
                 pointer is load-bearing, prefer removing the seam (move the
                 artifact in; add a red/green check) over annotating it —
                 F053's force-at-the-temptation-site applied to a repo
                 boundary.
                 (2) /soul-resume: step 2 becomes RESOLVE, not load — every
                 named path is resolved; a pointer that cannot be found is
                 reported explicitly ("cursor names X; X not found"), never
                 silently skipped. `[inherited]` and pre-A023 unmarked pointers
                 are claims to verify before repeating them to the Body.
WHERE IN SOUL:   skills/soul-handoff/SKILL.md (POINTERS template + new step 3
                 + Source footer); skills/soul-resume/SKILL.md (step 2 rewrite
                 + Source footer); findings/open/SOUL-F061 → closed.
QUESTION ONE:    Evidence — the anchoring instance is real and recorded
                 (RSENS-012): a false cursor claim was repeated to the Body
                 inside a next-step recommendation and shaped a deferral. The
                 failure is asymmetric — verifying a named path costs a
                 directory listing; propagating a false one costs a decision.
                 F047 (asserted vs executed) and F039 (secondary-mention
                 propagation) predict exactly this shape; the cursor is where
                 both meet: a store of secondary mentions with the typographic
                 authority of a durable record (F057's tier confusion).
QUESTION TWO:    Necessity — /soul-handoff §3 ("self-contained for
                 correctness") and /soul-resume §2 ("actually read them") were
                 both already right and neither closed the hole: reading what
                 exists silently succeeds past what doesn't, and nothing marked
                 which pointers were ever checked. The instrument that caught
                 the incident was the completion gate, NOT the resume — the
                 resume needed its own teeth. Two instances in one project
                 (RSENS-009/012) plus a same-day staleness catch here make the
                 shape systemic, not incidental.
QUESTION THREE:  Coherence — the cursor stays thin (A009 unchanged): a
                 two-token mark per pointer adds no duplication. Fail-open is
                 preserved: a missing cursor is still not an error, and a
                 reported miss degrades to exactly the fallback path that
                 already existed. The Body remains the authority — the resume
                 reports misses, it does not invent recoveries. Rule 3 is the
                 deeper alignment: a cursor pointer is an absolute claim about
                 reality, and this amendment gives it the anchor discipline the
                 contract already demands everywhere else.
