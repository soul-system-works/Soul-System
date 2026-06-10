# The Completion Gate

The "consult the Universe" gate, made runnable. It does not add an obligation — it makes
the existing one (*before calling work complete, verify against reality*) **enactable and
auditable**, because the Witness record shows it is the gate most often skipped. It fires
automatically as a **Stop hook** (`hooks/pre-completion-verify.py`) on non-trivial work.

The cause it addresses is **Universe Collapse** (*all brakes, no accelerator*) riding on
**Ad Hoc Methodology** (*the human reminding the AI of what should be automatic*): "consult
the Universe" treated as a posture rather than a step, so internal verification silently
stands in for external validation. A posture depends on memory; a gate that is run and shown
does not.

---

## The checks

Each must change what happens or be skipped honestly.

0. **Verify the verifier first.** Before asserting any execution-based check, confirm the
   executor exists and runs (a missing toolchain once produced eight asserted-but-never-run
   quality gates — SOUL-156). An exit code is not arm-/artifact-validity; judge from
   content (A019).
1. **Global invariant, not local tests.** What invariant must the WHOLE satisfy (a
   conservation law, an end-to-end balance, the behavior the whole must exhibit)? Verified —
   not just unit tests? Verification ≠ validation (A005).
2. **A valid external anchor for absolute claims (the load-bearing check).** Any number,
   "correct / complete / conformant," any absence or magnitude — anchored to an external
   source, *and* is the anchor itself valid (*trusted because… / wrong if…*)? An
   external-but-invalid anchor is Coherent Falsehood wearing the anchor's uniform (F028).
   For a "verified" claim from a prior record: **re-execute, don't re-read** (F047).
3. **Outward reach.** What already exists / what standard / what the real user needs that
   wasn't looked for? Name sources you cannot reach but the Body can — *"could not source"
   is a question for the Body*, not an endpoint.
4. **Visual artifact captured & inspected.** Rasterize via the project's own lib and Read
   it (or screenshot via run/verify). "Not eyeballed" is NON-PASS. Name the residual: design
   capture (headless) vs target-tool render (may need the Body) — F030/F031.
5. **Unfinished business marked** (`TODO`/`FIXME`/`DEBT`/`HACK`)?

---

## Run it open, but not as theatre

The reply leads with the ask or result; the gate lands **last, as one compact line** naming
its anchor or the specific gap, expanding to a failing check only when a gap is real:

`— Verify: clean (<anchor>)` or `— Verify: GAP → <specific>`

**A GAP on the primary artifact blocks.** If the gap sits on the thing the task exists to
produce (code never compiled or run, a document never rendered, a measurement never
executed), disclosure is NOT a permissible ending: obtain an executor, or stop and hand the
gap to the Body as a blocking question. GAP remains a legitimate close only for
secondary/residual surfaces. (A019 — six honest "Verify: GAP" lines once shipped alongside
code that did not compile; honesty about non-verification must change the outcome, not just
the report.)

A silent gate is an unrun gate — but a rote multi-line "no gaps" recitation is the theatre
the gate exists to prevent (F022) and it buries the ask (I018). **Visible means specific and
anchored, not verbose.** The gate is theatre the moment it stops finding gaps: a run of
reflexive "no gaps" answers is the signal to audit it, not to relax.

State the gate's reach honestly: it guarantees **sourcing discipline, not measurement
validity**. A green gate is not a truth certificate; the load-bearing assumption still needs
a Skeptic's eye.

---

**Source:** the Soul's failure vocabulary (Universe Collapse, Ad Hoc Methodology),
operationalized after both recurred in projects where every correction came from outside.
**Adopted:** 2026-05-20. **Status:** active (A010 names this file as "the mechanism").
