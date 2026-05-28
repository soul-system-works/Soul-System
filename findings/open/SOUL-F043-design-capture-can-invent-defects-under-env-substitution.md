```
FINDING ID:      SOUL-F043
DATE:            2026-05-28
WITNESS IDS:     REF-02-OS reference/dogfood project (SNS operational-posture
                 inference from public data; imports the seed). VOY-002
                 (font-substitution false-defect near-miss); VOY-001 (capture
                 tool absent → Body-Input skipped). Cross-project harvest —
                 these are REF-02 witness codes, not Soul-System SOUL-NNN.
WHAT:            Closing Finding for the REF-02-OS reference project, and a
                 SHARPENING of the F030/F031 visual-gate family in a direction
                 those two did not cover. F030 named that the visual gate gets
                 DEFERRED when no capture recipe exists; F031 supplied the
                 positive converse (recipe exists → gate discharged → caught a
                 real self-intersecting "bowtie" polygon) and named its residual
                 as the target-tool render being only APPROXIMATED by the
                 headless capture — i.e. capture can UNDER-report. This project
                 surfaces the INVERSE, more dangerous failure mode:

                 (1) DESIGN-CAPTURE CAN ACTIVELY MISLEAD (VOY-002). Verifying a
                 sponsor .pptx after edits, the agent rasterized it via
                 libreoffice — the only headless renderer present. The deck
                 specifies Aptos (the MS Office default, not installed here);
                 libreoffice SUBSTITUTED the wider Noto Sans, inflating line-wrap
                 and vertical fill, producing FALSE layout defects — footer/text
                 collisions, a title-wrap accent overlap — that do not exist
                 under the real font. The agent nearly recommended "fixing" these
                 phantom defects, which would have optimised against the wrong
                 font and could have BROKEN the real (Aptos) layout. Caught by
                 checking declared vs installed fonts (`fc-match Aptos` → Noto
                 Sans). So the headless capture is not merely an under-
                 approximation of the target tool (F031's residual); under
                 environment substitution it can INVENT a defect the target tool
                 never shows. That is a Coherent Falsehood (F015/F028) generated
                 BY the verification instrument itself: internally real (the
                 render genuinely overflows) yet false against reality (the
                 target tool paints it fine). The discharge for "is the DESIGN
                 right" can become the SOURCE of the false claim. Discipline:
                 when the headless render's ENVIRONMENT diverges from the target
                 (substituted fonts / themes / DPI / locale), treat its layout
                 findings as SUSPECT, and prefer an ENVIRONMENT-INDEPENDENT
                 structural check — here the OOXML negative-dimension grep
                 (PowerPoint's own repair trigger), which is font-independent and
                 gave the true signal (clean) while the raster lied. (Confirmed
                 in the follow-up session: after more edits the raster still
                 showed slide-2 overflow; the Body reviewed and accepted the deck
                 — the overflow was the substitution artifact, not a real defect.)

                 (2) CAPTURE-TOOL ABSENT → BODY-INPUT, NOT SILENT DEGRADE
                 (VOY-001). F030's landed recipe ("rasterize via the project's
                 OWN lib and Read it") PRESUMES the lib is present. The first
                 deck-render turn had NO headless renderer installed at all; the
                 agent named the gap as a residual and pushed through to commit
                 on structural-only verification, rather than surfacing the
                 install decision (libreoffice / python-pptx) to the Body.
                 Whether to add a tool to close a verification gap is a Body-Input
                 dependency (F037): that path should fire — offer the install —
                 instead of degrading the gate silently. So the F030 recipe has a
                 precondition (tooling exists) and, when unmet, hands off to F037
                 rather than to acknowledge-and-ship.

                 WHAT WORKED (closing what-worked, beyond the artifact): the
                 ANCHOR OBLIGATION + an adversarial-honesty posture drove the
                 session's central win — an assumptions audit re-derived a
                 sponsor-deck headline ("66.7% transfers to schedule-less
                 facilities") from the data and found it MIS-ATTRIBUTED; the
                 genuinely-transferable number (no schedule, no direct feed) is
                 0.333, below chance. The audit then turned on ITSELF and caught
                 two of its own errors (a baseline 0.875→0.750 correction; an
                 overstatement walked back). Emissary + Anchor Obligation doing
                 exactly their job against the project's own claims.
WHY NOT YET AMENDMENT:  Not new doctrine — A007 mandates capture+inspect, and
                 the F030/F031 fix (SOUL-066) already embeds the recipe + the
                 design-capture-vs-target-tool split in the F012 hook and
                 soul-verify.md check #4. This REFINES that landed fix in two
                 places: (a) the target-tool-render residual is not only
                 "headless UNDER-approximates" but "headless can INVENT a defect
                 under environment substitution" — so the note should add: a
                 divergent-environment headless render is SUSPECT; prefer an
                 environment-independent structural check (e.g. an OOXML / lint /
                 schema grep) over trusting the raster's pixels; (b) the recipe's
                 precondition (capture tool present) should, when unmet, route to
                 the F037 Body-Input path (offer to install) rather than to a
                 prose "GAP → not eyeballed" ship. Candidate operational edit:
                 one line in soul-verify.md check #4 / the completion-gate
                 capture-recipe note.
FILED BY:        Witness / Emissary (REF-02-OS reference-project close-out)
RELATED:         [[SOUL-F031]] (target-tool render residual — F043 is its
                 inverse failure: the capture INVENTS rather than under-reports),
                 [[SOUL-F030]] (visual gate deferred without recipe — F043 adds
                 the tool-absent precondition that routes to F037),
                 [[SOUL-A007]] (capture + inspect),
                 [[SOUL-F037]] (Body-Input Obligation — the route when the
                 capture tool is absent),
                 [[SOUL-F028]] (anchor validity, not just existence — the raster
                 is an anchor that EXISTS but is invalid under font substitution),
                 [[SOUL-F015]] (Coherent-Falsehood vocabulary — the phantom
                 defect is one),
                 [[SOUL-F012]] (completion-gate activation — fired and held this
                 session, including catching this very visual-gate gap).
STATUS:          Open — confirm with a second environment-substitution instance
                 (a theme / DPI / locale divergence inventing a defect in a
                 headless render) before promoting the soul-verify.md edit.
```
