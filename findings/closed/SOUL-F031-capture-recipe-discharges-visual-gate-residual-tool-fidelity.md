```
FINDING ID:      SOUL-F031
DATE:            2026-05-22
WITNESS IDS:     REF-01 reference/dogfood project (Modelica/Dymola ANO-1 balance-of-
                 plant), branch devel_greenwood_new, commits 979486a..181a4e8; repeated
                 F012 completion-hook firings across the session (~12 turns).
WHAT:            Closing Finding for the REF-01 reference project, and the first
                 POSITIVE-activation counterpart to SOUL-F030. F030 named that the visual
                 gate (completion check #4) gets DEFERRED when no capture recipe exists.
                 This session supplies the converse evidence: when a low-friction capture
                 recipe DID exist, the gate was DISCHARGED, and it changed the artifact.
                 Modelica component icons cannot render headless (only in the Dymola/OMEdit
                 GUI). Rather than ship "look deferred to the GUI / the Body's eye," the
                 agent rendered the EXACT polygon coordinates of each planned Icon
                 annotation in matplotlib and Read the PNGs back BEFORE writing the
                 Modelica. The capture caught a real defect from inspection — a turbine
                 polygon whose point order self-intersected into a bowtie — and it was
                 fixed before it ever reached the model. So F030's recommended recipe
                 ("rasterize via the project's own image lib / a preview and Read it")
                 works in practice and is worth promoting from candidate to default.
                 RESIDUAL: matplotlib only APPROXIMATES the Dymola renderer, so a thin
                 deferral remained ("exact paint confirmable only in the GUI"). The recipe
                 discharges "is the DESIGN right"; a separate, smaller check covers "does
                 the TARGET TOOL paint it right." Those are two checks, not one, and only
                 the first is headless-dischargeable.

                 Other Soul applications that WORKED here (closing what-worked, beyond the
                 artifact):
                 (1) COUNCIL-ON-DEMAND de-conflated a binary direction question. The Body
                 asked "add a richer-events example OR the primary side?"; the frame gate +
                 Skeptic surfaced that the two sit on different AXES (exercise-what-exists
                 vs add-a-subsystem) and reframed — A is a close-out, B is a new phase that
                 crosses the project charter and stacks numerical risk. The reframe
                 materially improved the decision and the resulting deliverable.
                 (2) EMISSARY + ANCHOR OBLIGATION caught a Coherent Falsehood mid-stream.
                 An up-ramp sim crash was diagnosed as "OTSG transient-robustness," then as
                 "FWH level overflow" — BOTH falsified by external anchors (an OTSG-free
                 model failing identically at the same time; bounded trajectory levels) —
                 and the correction was PROPAGATED: the false "OTSG limit" claim had been
                 written into a model docstring, and it was fixed when the real cause
                 (solver/check-valve state-event handling) was found. The "anchored claims"
                 gate + Emissary lens did exactly their job.
                 (3) GLOBAL-INVARIANT discipline on shared-file edits: each change to a
                 shared control class (pump-RPM gating in ICS_Unlumped; the schedule input
                 on RunbackSupervisor) was re-validated against an existing model and came
                 back BIT-IDENTICAL — backward-compatibility verified, not assumed.
WHY NOT YET AMENDMENT:  Not a doctrine change — A007 already mandates capture+inspect and
                 F030 already proposed the recipe. This is activation EVIDENCE (the recipe
                 works → promote to default) plus one refinement: SPLIT gate check #4 into
                 (a) "design captured + inspected" (headless-dischargeable via the F030
                 recipe) and (b) "target-tool render confirmed" (may legitimately require
                 the Body / the tool), so the residual is NAMED rather than silently folded
                 into a prose "GAP → not eyeballed." Pair this with F030's candidate fix in
                 soul-verify.md / completion-gate.md: state the default capture recipe AND
                 distinguish the two sub-checks.
FILED BY:        Witness / Emissary (REF-01 reference-project close-out)
RELATED:         [[SOUL-F030]] (visual gate deferred without capture recipe — F031 is its
                 positive-activation converse; both harvested from greenwoodms06 projects),
                 [[SOUL-A007]] (capture + inspect), [[SOUL-F008]] (visual / non-automatable
                 Witness category), [[SOUL-F012]] (completion-gate activation — fired ~12x
                 this session with no false "complete" claim; mild over-fire on
                 progress-report turns that were not completion claims), [[SOUL-F015]]
                 (Coherent-Falsehood vocabulary — caught + corrected here), [[SOUL-F007]]
                 (Universe / global invariant — shared-file changes re-validated).
STATUS:          Closed [2026-05-26, via SOUL-066]. Operational fix landed together with
                 SOUL-F030: hook check #4 + soul-verify.md check #4 now embed the recipe
                 (rasterize via project's own lib + Read it; or screenshot via run/verify)
                 AND the split (design-capture headless vs target-tool render — residual
                 named, not folded into "not eyeballed"). Closes the negative/positive pair
                 from greenwoodms06's blog + REF-01 reference projects.
```
