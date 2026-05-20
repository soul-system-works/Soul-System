```
AMENDMENT ID:    SOUL-A009
DATE:            2026-05-20
WITNESS IDS:     FANOUT-005, FANOUT-007 (fan-out dogfood: handoffs held with zero
                 drift, but a worker read sibling files for style despite a
                 hermetic-looking packet); SOUL-A008 (the discipline this refines)
WHAT CHANGES:    Clarify in operations/adr-format.md that the self-contained
                 handoff discipline is "self-contained for correctness" — the
                 packet must guarantee a correct result from the packet alone, but
                 does not need to be hermetic (a worker may still read the
                 surrounding repo for consistency cues).
WHERE IN SOUL:   operations/adr-format.md (Execution Topology and Delegation).
                 Operations-level; refines A008's wording, no philosophy change.
QUESTION ONE — EVIDENCE:
                 The FANOUT multi-agent dogfood ran five isolated workers with
                 self-contained handoffs and got zero integration drift (70 tests
                 green, first-try integration) — strong validation of A008. But
                 FANOUT-007 observed a worker reading sibling modules / the ADR for
                 docstring style despite a handoff that named neither. The original
                 A008 wording ("self-contained") could be read as "hermetic," which
                 the evidence shows is neither what happened nor what is needed.
QUESTION TWO — NECESSITY:
                 Without the refinement, "self-contained" overclaims. A future
                 reader might treat any outward reading by a worker as a discipline
                 violation, or might try to make handoffs hermetic (impossible and
                 unnecessary). The testable claim is correctness-from-the-packet.
QUESTION THREE — COHERENCE:
                 Extends, does not contradict A008 — sharpens its wording with
                 evidence from the test built to exercise it. No philosophy change.
ACCEPTED BY:     Judge (operations-level; Body authorized continuation 2026-05-20)
FILED BY:        Archivist
```

---

## Council Convening Summary

A short convening on the FANOUT dogfood result. The FANOUT test (an
orchestrator-worker build of a 5-transformer toolkit) was constructed to exercise
SOUL-A008. It validated A008 strongly — see SOUL-F010 (protective findings),
updated with the new evidence — and surfaced one wording refinement:

- **Skeptic:** "self-contained" risks being read as "hermetic," which the test
  disproved (a worker read siblings for style, harmlessly). Sharpen to
  "self-contained for correctness."
- **Judge:** ADOPT as SOUL-A009 (operations). The substantive discipline is
  unchanged; only its precision improves.

## The Specific Change

`operations/adr-format.md`, Execution Topology and Delegation: the handoff is
"self-contained *for correctness*" — guarantees a correct result from the packet
alone, but is not required to be hermetic.
