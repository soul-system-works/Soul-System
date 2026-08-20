# Upstream note — thermal-plant modeling project (2026-08-18)

Instrument lessons owed upstream per the project contract ("Projects importing
this contract owe their Soul-System-level lessons upstream"). System-level
observations only; domain lessons stay home in that project's record. Project
identifiers deliberately omitted. This note also discharges the standing
"upstream note owed" item first flagged 2026-08-14 in that project's cursor —
the earlier session recorded the obligation but not the specific lesson, so
only lessons with durable records are carried here.

## Observations about the system itself

1. **A deliberately-strict standing decision has no re-evaluation trigger.**
   The project ran two content-fingerprint gates: a benchmark staleness anchor
   that ignores cosmetic churn, and a deliverable-provenance gate deliberately
   kept stricter ("any difference counts" — a recorded, Body-gated decision).
   Months later the Body locked a documentation-editing phase whose every edit
   would trip the strict gate, keeping the whole suite red for the phase's
   duration — training the eye to wave through a failing gate, the exact
   failure the project's own doctrine names. Nothing surfaced the conflict:
   not the gate, not the planning pass that locked the phase. It was caught
   incidentally, when the Body invoked an adversarial-questioning skill on an
   unrelated scope decision and one frontier question happened to intersect
   the gate. LESSON: a "deliberately strict, revisit-on-Body's-call" decision
   is a standing IOU with no maturity date; when a new plan is locked, some
   instrument should sweep the open Body-gated decisions for collisions with
   it. The grill caught it; the system was lucky, not covered.

2. **Layered verification caught the verifier's own error.** A read-only
   documentation-accuracy audit (six parallel agents, verify-every-claim-
   against-code-before-reporting) produced 86 findings. The corrections were
   then applied by separate implementer agents and reviewed by a fresh-context
   diff reviewer — which found exactly one factual defect: an error in the
   AUDIT itself (a "the only live consumers are X and Y" claim that omitted a
   third live consumer), copied faithfully into two files by the implementers.
   No single layer would have caught it: the audit believed itself, the
   implementers correctly trusted their brief. The independent-layer chain
   (audit → apply → adversarial re-review) is what converted a plausible
   falsehood into a caught one. LESSON: "verify the verifier" scales — the
   report of an instrument that itself verified things is still a claim, and
   the cheapest catch is a fresh-context reviewer of the APPLIED result, not a
   re-run of the same instrument.

3. **A terse directive reusing a loaded term needs one cheap disambiguation.**
   The Body deferred a large documentation pass ("the scrub") to project end,
   twice, explicitly — then hours later wrote "then do the scrub." Two
   readings led to materially different days of work (apply a small accuracy
   fix-list vs reverse the deferral and run the full pass). One structured
   question with a recommended default resolved it in seconds; the Body picked
   the narrow reading. LESSON: when a directive reuses a term the session has
   loaded with a specific big meaning, and the directive contradicts a
   decision the Body made the same day, a single clarifying question is not
   clarification-drift — assuming either reading would have been the error.

4. **A read-only audit is a good pressure-relief valve for a deferred pass.**
   Deferring the big cleanup created the risk that actively-wrong content
   stays live for months. Splitting "is it WRONG?" (cheap, read-only,
   agent-parallel, zero blast radius) from "is it STYLED right?" (the deferred
   pass) let the project fix the dangerous half the same day while honoring
   the deferral. The audit found one finding class the fixing pass could not
   legally touch (text living in constructs the staleness fingerprint treats
   as significant), and binning those explicitly — with their own named
   vehicle — kept the pass honest instead of silently partial.
