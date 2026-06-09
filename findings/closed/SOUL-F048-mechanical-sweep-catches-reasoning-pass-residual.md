```
FINDING ID:      SOUL-F048
DATE:            2026-06-08
WITNESS IDS:     SOUL-146 (THE CUT executed → 1.0; the load-bearing coherence catch DURING
                 execution: cutting `council-synthesis.md` ALSO dropped the AMENDMENT PROCESS —
                 the three acceptance questions Evidence/Necessity/Coherence + accept/return/
                 file-finding — which is process doctrine for the KEPT `amendments/` + `findings/`
                 records, NOT council convening ceremony. Extracted to `operations/amendment-
                 process.md`; only the convening ceremony was cut. Ops ended at 6 files, not the
                 planned 4);
                 SOUL-145 (the pre-execution coherence pass that NAMED three hard requirements —
                 upstream-obligation, the F038 fact, the witness invariants — and verified them
                 present in the leaned seed, but MISSED this fourth load-bearing dependency).

WHAT:            **A reasoning-based coherence pass and a mechanical dangling-reference sweep
                 catch DIFFERENT classes of defect, and the sweep catches the reasoning pass's
                 residual. Run the mechanical sweep AFTER any deletion — it is not redundant with
                 having "thought carefully" first.**

                 The pre-execution coherence pass (SOUL-145) reasoned about what the cut must
                 preserve and produced a list of three hard requirements — all real, all verified.
                 But a coherence pass can only check what it thinks to ask about; it operates over
                 the reasoner's model of the system. The amendment-process dependency was NOT in
                 that model: `council-synthesis.md` was mentally filed as "council ceremony"
                 (cuttable), and the fact that it also HOUSED the acceptance process for the kept
                 records was exactly the kind of cross-cutting coupling a reasoning pass glosses.

                 What surfaced it was not more thinking. It was the mechanical post-deletion sweep
                 for dangling references: a KEPT file still POINTED at the cut one, and that
                 pointer — not any re-reasoning — exposed the dropped doctrine. The two checks are
                 complementary because they fail on opposite things:
                 • the **reasoning pass** catches defects of MEANING (does the leaned system still
                   say what it must?) but is blind to couplings outside the reasoner's model;
                 • the **mechanical sweep** catches defects of REFERENCE (does anything kept still
                   point at something gone?) with zero model of meaning — it cannot miss a
                   coupling for "not thinking of it," because it doesn't think.

                 This is the same shape as the Anchor four-faces (existence → validity → scope →
                 timing): each check catches the prior's residual, not a duplicate of it. A
                 coherence pass that returns clean is necessary but NOT sufficient before an
                 irreversible deletion; the sweep is the cheap mechanical backstop that catches
                 what reasoning structurally cannot.

OPERATIONAL RULE (the practice this earns):
                 **After any deletion/retirement of an instrument or doc, run a mechanical
                 dangling-reference sweep over the kept set** (e.g. `grep -rl <removed-path>` /
                 a link check) — BEFORE calling the change complete, regardless of how careful
                 the pre-flight reasoning was. The reasoning pass plans the cut; the sweep
                 verifies the cut didn't sever a load-bearing pointer. Belongs at the retirement
                 moment (Rule 4: generation couples with retirement — the retire handle should
                 include the sweep).

WHY THIS FILING (not an amendment):
                 Operational/methodological, not a new philosophy primitive. It sharpens an
                 existing discipline (the completion gate's "verify against reality, not internal
                 coherence" — A005/A010) by naming a concrete, cheap mechanical check that catches
                 a class the coherence pass misses. Folded into `mind.md` as a method note /
                 contrast-case neighbour (the F031-vs-F030 "recipe IS the activation" family: a
                 mechanical instrument discharges what posture alone defers). No seed change.

FILED BY:        Steward (the cut retired an instrument; this is the retirement's earned lesson);
                 Skeptic (named that a clean coherence pass is necessary-not-sufficient before
                 irreversible deletion);
                 Emissary (the sweep is the outward/mechanical check against reality — it found
                 what the internal-coherence model could not).

RELATED:         [[SOUL-146]] (the cut + the in-vivo catch that earned this);
                 [[SOUL-145]] (the coherence pass that named 3 and missed the 4th);
                 [[SOUL-F045]] (sibling four-faces shape — each check catches the prior's
                 residual; there for anchoring force, here for deletion safety);
                 [[SOUL-F031]] (the recipe IS the activation — a mechanical instrument discharges
                 what reasoning/posture defers; same family);
                 [[mind-rule-4]] (generation couples with retirement — the retire handle should
                 carry the post-deletion sweep);
                 [[mind-rule-6]] (the gate fires where the failure mode happens — the sweep fires
                 at the deletion moment, not at the planning moment).

STATUS:          GRADUATED (Body's call, 2026-06-08). Recorded as an operational practice; the
                 method note is carried in the 1.0 handoff and folds into `mind.md` on the next
                 `/soul-distill` run (contrast-case neighbour to F031). Closed: the lesson is
                 complete and the practice is stated; no further evidence pending.

                 UPSTREAM: this repo IS the Soul System (the upstream). Soul-meta (about how a
                 cut/retirement is verified), so it belongs in this `findings/` stream.
```
