---
description: Force Universe-consultation checks before calling non-trivial work complete. The pre-completion gate that addresses SOUL-F012's auto-fire limit — global invariant, valid external anchor, outward reach, visual inspection, unfinished business. Run before claiming completion. Doctrine's checks made explicit because they do not reliably auto-fire.
---

# /soul-verify — the pre-completion gate, made to fire

You are about to call work complete (or just did). Before that stands, run these
checks explicitly and answer each **in writing, concretely** — not "yes."

This command exists because the doctrine's completion obligations *describe* these
checks but do not reliably fire on their own. Across four-plus autonomous runs the
outward and verification passes fired only when the Body insisted; one project
even loaded the doctrine and re-derived its content from scratch without
recognizing it. Loaded text is not live behavior (SOUL-F012). This gate converts
the obligation into an invokable step.

For the work just completed, answer each:

1. **Global invariant — verification ≠ validation (SOUL-A005).** What invariant
   must the WHOLE satisfy (a conservation law, an end-to-end balance, the behavior
   the whole is meant to exhibit)? Is it verified — not just local unit tests? If
   there is no global invariant, say why.

2. **A valid external anchor for absolute claims (SOUL-F013, SOUL-F028).** Does the
   work make any ABSOLUTE claim — a number, "this is correct / complete / conformant"?
   If so, name the EXTERNAL anchor that grounds it (a benchmark, a published value, a
   standard, a domain expert, a spec) **and its validity basis** — why that anchor is
   trusted, and how it could be wrong. A named-but-flawed anchor (a mis-taken
   measurement, a collapsed assumption) still passes if you only check that it EXISTS:
   that is **Coherent Falsehood** wearing the anchor's uniform (SOUL-F028) — and it
   needs a Skeptic's eye on the load-bearing assumption, not just on the claim. Internal
   consistency over an absolute claim is a Coherent Falsehood — self-consistent and
   wrong. No anchor, or no validity basis → not yet verified. Say so. (The gate
   guarantees sourcing, not measurement validity.)

3. **Outward reach — Universe Collapse (SOUL-A003).** Did the work reach outward
   (what already exists in the field, the standard others use, the real user's
   need, a larger frame), or did it treat the local task as the whole Universe?

4. **Visual / non-automatable Witness (SOUL-A007, SOUL-F030/F031).** Is there a visual
   or other non-test-checkable artifact? If so, was it CAPTURED and INSPECTED — not
   deferred to "the human will look"? **Default recipe (F030/F031):** rasterize via the
   project's own image lib (e.g. `sharp` for SVG, `matplotlib` for polygon coords) and
   Read the resulting PNG back; or screenshot the page via the project's run/verify
   skill. A prose "GAP → not eyeballed" on a visual change is **NON-PASS**, not a clean
   line — it is an admission the obligation was skipped. **Split the check** when the
   capture is approximate: (a) DESIGN captured + inspected (headless-dischargeable via
   the recipe — catches geometry/encoding defects, e.g. self-intersecting polygons) vs
   (b) TARGET-TOOL render confirmed (the artifact paints right in its actual renderer;
   may legitimately require the Body or the tool itself). Name the residual rather than
   folding it into "not eyeballed."

5. **Honest markers (SOUL-F016).** Is unfinished business flagged with a marker
   (`TODO`/`FIXME`/`DEBT`/`HACK`) where it lives, and standing limitations noted
   in docstrings? Or is something compromised and silent?

If any check fails, the work is **not** complete. Name the gap; fix it or record
it honestly (Witness entry / marker); do not claim completion until the checks
pass or their failure is explicitly accepted by the Body.

---

**Source:** Built by the Artificer in response to SOUL-F012 (amendments describe
but do not fire). The portable, Body-invoked form of the pre-completion gate. The
auto-firing form is a harness Stop hook (Claude Code), deferred. **Adopted:**
2026-05-20. **Status:** active — partial fix; F012 stays open until the gate
auto-fires without Body invocation.
