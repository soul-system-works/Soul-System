```
AMENDMENT ID:    SOUL-A019
DATE:            2026-06-10
WITNESS IDS:     SOUL-155 (the v1.0 evaluation study — the in-vivo Soul arm shipped
                 non-compiling code behind SIX honest "Verify: GAP" disclosures; the
                 stream soul-on arm shipped a failing test it could not run);
                 SOUL-156 (the three harness incidents: the missing executor asserted
                 8 quality checks that never ran; exit codes reported clean through a
                 limit storm that stubbed 33 outputs; hook-scope verification).

WHAT CHANGES:    The completion gate's treatment of verification gaps, plus three
                 experiment-harness rules. Extends F047 (asserted ≠ executed) and A013
                 (harness discipline) with the lesson all three incidents share:
                 VERIFICATION REQUIRES AN EXECUTOR THAT EXISTS, AND A GAP ON THE PRIMARY
                 ARTIFACT IS A BLOCKER, NOT A FOOTNOTE.

                 1. operations/completion-gate.md — "Verify: GAP" on the PRIMARY artifact
                    (the thing the task exists to produce — code never compiled/run, a
                    document never rendered, a measurement never executed) is NOT a
                    permissible way to end the work. The agent must obtain an executor,
                    or stop and hand the gap to the Body as a blocking question. GAP
                    remains permissible only for secondary/residual surfaces.
                 2. operations/completion-gate.md — verify-the-verifier preflight: before
                    asserting any execution-based check, confirm the executor exists and
                    runs (a missing toolchain produced 8 asserted-but-never-run quality
                    gates before being caught).
                 3. operations/experiment-harness.md — (a) arm validity is judged from
                    artifact CONTENT (is_error fields, size, sentinel), never from sweep
                    exit codes; (b) sentinel checks go MID-output, not output-first
                    (frontier models override format-first instructions with
                    sandbox-honesty disclosures); (c) executor-existence is asserted
                    before any quality gate runs.
                 4. hooks/pre-completion-verify.py — checklist item and REPLY guidance
                    updated to carry the primary-artifact blocking rule.

WHY:             The in-vivo result is the proof the disclosure form is insufficient:
                 the gate fired 6/6 times, the sessions honestly named the gap each
                 time, and the broken artifact shipped anyway. Honesty about
                 non-verification is necessary but not sufficient; the gate must change
                 the OUTCOME, not just the report. (The control arm, blind in exactly
                 the same way, happened to ship working code — discipline without an
                 executor is luck, in both directions.)

BOUNDS:          "Primary artifact" requires judgment; the gate names the test (the
                 thing the task exists to produce), not an enumeration. Headless
                 environments where no executor can exist (pure-text tasks) are out of
                 scope — the rule binds where execution is possible or obtainable.
```
