```
FINDING ID:      SOUL-F040
DATE:            2026-05-27
WITNESS IDS:     SOUL-088 (Soul-Console v1 structural audit: 3 operations/
                 files flagged DEFER-WITH-CRITERIA on surface-level Steward
                 intuition — `autonomous-session-template.md`,
                 `completion-gate.md`, `reference-repository.md`);
                 SOUL-090 (beta investigation: per-item grep + content analysis
                 REVERSED 2/3 to KEEP-IN-PLACE — completion-gate.md is A010-
                 named load-bearing doctrine; reference-repository.md is the
                 references/ format spec; only autonomous-session-template.md
                 remained RETIRE-NOW after evidence);
                 SOUL-091 (the one true retire-with-preservation: deleted
                 autonomous-session-template.md, lifted the Problem Slot
                 framing into operations/problem-slot-template.md);
                 SOUL-092 (completion-gate catch: SOUL-090's `.md`-only grep
                 had missed `install.sh:37` referencing the retired template;
                 the three-layer completion stack — doctrine + /soul-verify
                 + pre-completion-verify.py hook — fired and forced re-check.
                 Re-grep across all file types surfaced the live reference;
                 fix landed at install.sh 36–38).

WHAT:            **Retire-intuitions need a uniqueness-investigation step
                 AND the investigation itself needs scope-discipline.**
                 Surface-level Steward intuition ("this file looks unused /
                 superseded") is an unreliable basis for retirement action.
                 The discipline that catches the gap:

                 (1) **Per-item grep across the project** before any retire
                     decision — "is this actually referenced anywhere?"
                 (2) **Grep-scope check** — the grep itself has scope (file
                     types, subdirectories, exclusions). If scope is too
                     narrow, the anchor is INVALID per A010 §Anchor Obligation
                     and F028 §anchor-validity — passes existence, fails
                     validity. Default scope must be all-file-types unless
                     an exclusion is justified.
                 (3) **Content analysis** on each match — descriptive citation
                     (in audit / witness / council records) vs. load-bearing
                     citation (in doctrine / amendments / changelog). Only
                     the latter blocks retirement.
                 (4) **For doctrinal files specifically** — check
                     `amendments/accepted/`, the seed pointer, and
                     `SYSTEM-VERSION.md`. A file named as "the mechanism" by
                     an accepted amendment is STRUCTURALLY load-bearing
                     regardless of raw citation count.

                 Empirical rate from this single arc (N=3 surface intuitions
                 → discipline):
                 - **2/3 false-retire rate on surface intuition alone**
                   (completion-gate.md and reference-repository.md would have
                   been wrongly retired had SOUL-090's investigation not
                   fired).
                 - **0/3 actual false retirements after the discipline**
                   (SOUL-091 retired only the one true survivor;
                   SOUL-092 caught the residual grep-scope miss BEFORE it
                   could ship as a broken `install.sh:37` reference).

                 The pattern recurs across zoom-levels of the same surface
                 ("structural cleanup of the Soul-System repo"):
                 - Zoom 1 — chamber-level intuition (SOUL-087/088): wrong
                   on 2/3.
                 - Zoom 2 — grep-+-content investigation (SOUL-090): right
                   on the verdict, wrong on the grep's own scope.
                 - Zoom 3 — completion-gate re-check (SOUL-092): caught
                   zoom-2's residual error.

                 Each tighter zoom catches the prior zoom's failure mode.
                 The structural lesson: *no single check is sufficient for
                 retire decisions*; layered checks at successively finer
                 zoom-levels are.

WHY NOT YET AMENDMENT:
                 Single audit context (N=3 from one structural sweep within
                 one project). F035's three-instances-from-same-surface
                 heuristic is met WITHIN this audit at successively finer
                 zoom-levels — but the audit is itself one surface (the
                 Soul-System repo's own structural cleanup). Wait for a
                 SECOND retirement-context instance — either a different
                 project's cleanup beat, or a different kind of cleanup in
                 this project (e.g., command retirement, doctrine-file
                 supersession) — before generalizing the discipline to a
                 Soul-level amendment.

                 If the next retire-beat hits the same trap, A### "Retire-
                 intuition uniqueness-investigation" becomes amendment-ready
                 and could fold into seed §Mandatory Gates "Before changing
                 existing state" with a measurement-style recipe.

                 The Coherent Falsehood the gate caught at SOUL-092 also
                 vindicates A010 §Anchor Obligation — F040 is a **domain
                 specialization of A010** for the retirement-action class
                 of claim: "this file is not referenced" is an absolute
                 claim about reality that needs a valid external anchor,
                 and a grep with too-narrow scope is an INVALID anchor.
                 A010 names the obligation; F040 names the specific failure
                 mode in the retirement context and the four-step recipe
                 that discharges it.

FILED BY:        Steward (the role whose intuition was repeatedly wrong AND
                 right depending on whether the investigation step fired —
                 the audit-process lesson is most directly the Steward's);
                 Archaeologist (per-item-grep + content-analysis IS the
                 Archaeologist's job — what is this for, who refers to it,
                 what orphans if it goes);
                 Skeptic (forced the grep-anchor re-check at the completion
                 gate at SOUL-092);
                 Emissary (the re-grep across file types was the field test
                 of SOUL-090's original anchor);
                 Cartographer (per-boundary reshape from SOUL-087 Thread 2
                 — boundaries between record-kinds are where the
                 investigation discipline matters most);
                 Guardian (the completion-gate stack itself caught zoom-2's
                 residual at zoom-3 — F012-family operational health).

RELATED:         [[SOUL-F035]] (three-instances-from-same-surface heuristic
                 — F040's three instances span one surface at successively
                 finer zoom-levels, matching F035's pattern at a finer
                 grain);
                 [[SOUL-A010]] (Coherent Falsehood + Anchor Obligation —
                 F040 specializes A010 for retirement claims; the SOUL-092
                 gate-catch IS the A010 §Anchor Obligation discharge for
                 this arc);
                 [[SOUL-F028]] (anchor-validity third axis — F040's
                 grep-scope check is a direct instance: a grep that exists
                 but with invalid scope is the same failure-shape as a
                 mis-measured anchor wearing the uniform);
                 [[SOUL-A012]] (Activation Disciplines — F040's
                 uniqueness-investigation is a Counterweight Rule check at
                 the retire-decision moment: *what does this miss? where
                 else could it be referenced?*);
                 [[SOUL-088]] [[SOUL-090]] [[SOUL-091]] [[SOUL-092]] (the
                 audit → investigation → retire-with-preservation → gate-
                 catch arc that earned the finding);
                 [[docs/audits/2026-05-27-soul-console-v1-structure.md]]
                 §Section 4 + §Audit-process lesson (the candidate flagged
                 in the audit itself);
                 [[mind-rule-4]] (generation couples with retirement —
                 F040 adds the SAFETY-MECHANISM layer to the retirement
                 half).

STATUS:          Open — confirm with a second retirement-context instance
                 (different project OR different kind of cleanup beat in
                 this project) before promoting to a Soul amendment.

                 The discipline is operational TODAY for any retire-decision
                 in the Soul-System repo: surface intuition → per-item grep
                 (all-file-types) → content analysis → doctrinal-citation
                 check → only then retire.
```
