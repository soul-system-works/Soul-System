```
FINDING ID:      SOUL-F044
DATE:            2026-06-04
WITNESS IDS:     SOUL-123 (longitudinal-drift v2 — the FACT result: a self-accumulated
                 record prevents drift 5/5 HOLD vs 5/5 DRIFT at BOTH Haiku and Sonnet,
                 citing the buried ADR-001; the length-matched filler control drifts
                 identically to the bare floor → it is the record's CONTENT, not context
                 volume; the frontier model fails MORE dangerously without it, inventing
                 an idempotency key the provider does not support);
                 SOUL-124 (longitudinal-PREFERENCE probe — the PREFERENCE result: the same
                 harness with a counter-default reasoning-PREFERENCE D (return a Result
                 type, do NOT raise for expected failures) ALSO holds 5/5 vs 5/5 at both
                 models. The frontier model DEFERS to the recorded convention — reproduces
                 its reasoning and its boundary (keeps a programmer-error `assert` as an
                 exception per the ADR) — even though Result is counter to Python's
                 exception idiom and its own floor default is 5/5 the opposite. This
                 broke the conjecture SOUL-123 carried that a preference would dissolve);
                 SOUL-122 (longitudinal-drift v1 — mechanism-validation + the C2 lesson:
                 floor-check counter-default-ness BEFORE building the chain);
                 SOUL-125 (DEPTH-decay — the carry survives burial under N=20 intervening
                 ADRs with NO cliff at either capability; the frontier control still invents
                 an idempotency key to drift at depth 20. Climbs the depth/burial rung).

WHAT:            **A self-accumulated record carries UNGUESSABLE knowledge — content the
                 model cannot regenerate on its own — across a session boundary AND a task
                 boundary, and prevents drift at BOTH capabilities. This holds whether the
                 unguessable content is an external FACT or an arbitrary team CONVENTION,
                 and it does NOT dissolve at the frontier.**

                 The frontier line is **derivable vs. unguessable**, not fact vs.
                 preference:
                 - **Derivable** — content the model can re-reason its way to (anchoring,
                   skill-routing): the record's value DISSOLVES at the frontier, because
                   the strong model reaches the answer without it.
                 - **Unguessable** — content the model cannot regenerate: the record's
                   value PERSISTS at the frontier. Two kinds measured:
                   - an external FACT (SOUL-123: the payment endpoint has no idempotency
                     support — the frontier model can't derive this and fails MORE
                     dangerously without it, inventing a key that doesn't exist);
                   - an arbitrary CONVENTION (SOUL-124: the team signals expected failures
                     with Result types, not exceptions — unguessable a priori; the frontier
                     model DEFERS to the record rather than overriding with its own idiom).

                 Both results use the same manufactured session chain (the counterfactual
                 the real project history can't supply):
                 - **S1 (establish)** records a counter-default decision D as an ADR.
                 - **S2 (dilute)** buries D under a later, unrelated ADR.
                 - **S3 (the fork)** runs a NEW related task with the original context C
                   ABSENT, three ways differing ONLY in carried record: with-record (real
                   log, D buried) / control (length-matched filler, same volume, NO D) /
                   floor (no record). n=5 per cell, read-confirmed in actual code.

                 | Probe | Arm | Haiku | Sonnet |
                 |---|---|---|---|
                 | FACT (123) | floor | 5/5 DRIFT | 5/5 DRIFT |
                 | FACT (123) | with-record | 5/5 HOLD | 5/5 HOLD |
                 | FACT (123) | control | 5/5 DRIFT | 5/5 DRIFT |
                 | PREFERENCE (124) | floor | 5/5 DRIFT | 5/5 DRIFT |
                 | PREFERENCE (124) | with-record | 5/5 HOLD | 5/5 HOLD |
                 | PREFERENCE (124) | control | 5/5 DRIFT | 5/5 DRIFT |

                 Three load-bearing facts, identical across both probes:
                 (1) The record MOVED the decision — drift→hold 5/5 at both models,
                     citing the ADR by name and reproducing its reasoning, two sessions
                     later, with the triggering context absent.
                 (2) Equal compute is controlled — the length-matched filler drifts
                     identically to the bare floor at both models; the gain is the
                     record's CONTENT, not volume. (Neither control confabulated the
                     decision; the preference control cited only the filler's own
                     unrelated ADR.)
                 (3) It PERSISTS at the frontier — the key differentiator from the
                     reasoning-lift wins (anchoring, skill-routing), which dissolved at
                     Sonnet. The substance is unguessable, so the frontier model needs
                     the record exactly as much as the weak one.

WHY NOT YET AMENDMENT:
                 The reframe is decisive within scope but the scope is the first rung, not
                 the ladder. The fact/preference axis is now CLOSED (both persist; SOUL-124
                 tested the conjecture SOUL-123 left open and falsified it). What remains
                 before this graduates to doctrine:
                 - **Decay — depth now measured, erosion and interaction not.** A depth probe
                   (SOUL-125) stretched the single dilution step to N=20 burial and found
                   **no cliff at either capability** — the fact D fires 5/5 buried under 20
                   intervening ADRs, and the frontier control still invents an idempotency
                   key to drift. So depth/burial accumulation is addressed. What remains: an
                   *eroding/compressed* record (D summarized by a later consolidation —
                   directly tests /soul-distill), *interacting* entries (a later ADR that
                   reinforces or CONTRADICTS D), and D in a *middle* (non-primacy) position.
                 - **The deference bound.** SOUL-124's convention was clearly-stated and
                   defensible. A terse, weakly-rationalized, or absurd convention might not
                   install (even at the weak model) or might get overridden at the frontier.
                   "The frontier model defers to recorded conventions" is bounded to
                   well-formed ones until tested otherwise.
                 - **The reframe is inductive.** Derivable-vs-unguessable is supported by
                   ~4 points (two persist, two dissolve), not proven. More dissolve/persist
                   pairs would harden it.
                 - **Establishment-assisted S1, one drift type per probe, n=5, two models.**

                 To graduate: the depth/burial rung is now climbed (SOUL-125, N=20 both
                 capabilities); what would close the case is an *erosion* rung (does D
                 survive being compressed by /soul-distill?) and an *interaction* rung (does
                 it survive a later contradicting entry?), so the claim generalizes from "a
                 record carries one step, and survives depth" to "the accumulating record's
                 value is durable across the conditions doctrine assumes." That generalized
                 claim folds into philosophy/the-soul.md as the measured backing for the
                 system's strongest premise — that an accumulating record keeps work
                 coherent with decisions whose justifying context is gone — with the
                 frontier line stated as derivable-vs-unguessable.

FILED BY:        Emissary (tested the record's strongest claim against reality — and then
                 tested its stated BOUND and broke it: SOUL-124 falsified the preference-
                 dissolves conjecture);
                 Skeptic (read-confirmed all 60 outputs across both probes in actual code;
                 verified the equal-compute controls + causal attribution; tightened
                 overclaims at each step — "first frontier-persistent win" → "first
                 directly measured", and "fact-carrying" → "unguessable" once the
                 preference also persisted);
                 Revelator (the reframe — the frontier line is derivable-vs-unguessable,
                 not fact-vs-preference; an arbitrary convention is unguessable so it
                 persists exactly like a fact, and the frontier model defers rather than
                 overrides);
                 Accountant (floor-check-first + the new install-check gated each 30-call
                 spend — the v1→v2→preference method discipline).

RELATED:         [[SOUL-122]] [[SOUL-123]] [[SOUL-124]] [[SOUL-125]] (the v1 mechanism +
                 C2 lesson → v2 fact result → preference result → depth-decay arc that
                 earned, broadened, then depth-hardened the finding);
                 [[SOUL-I042]] (the frontier-persistence axis this result sits on);
                 [[SOUL-I045]] (the decay probe — depth done, erosion + interaction open);
                 [[SOUL-F026]] (savings-from-targeted-retrieval-not-carried-record — F044
                 is the COMPLEMENT: F026 found the carried record loses on token-COST vs
                 targeted retrieval; F044 finds it wins on DECISION-CORRECTNESS where the
                 content is unguessable. Cost vs value, two faces of the same record);
                 [[docs/study/07-longitudinal.md]] (the FACT writeup) +
                 [[docs/study/08-longitudinal-preference.md]] (the PREFERENCE writeup +
                 the reframe);
                 [[docs/study/06-bounds-and-open-questions.md]] (row 1 — the open ends
                 these results moved);
                 [[docs/specs/2026-05-29-longitudinal-harness-design.md]] (the harness);
                 [[mind-rule-3]] (anchor every absolute claim — the read-confirm-in-code
                 scoring IS the anchor discipline at writing time).

ADDENDUM:        2026-06-10 (SOUL-155, the v1.0 evaluation study, Phase 2 — 180 arms,
                 THREE capabilities incl. Opus 4.8): the remaining rungs are CLIMBED.
                 - INTERACTION: D survives a later generically-contradicting ADR 15/15
                   (Sonnet/Opus reconcile explicitly 10/10 via the conflicting ADR's own
                   exception clause).
                 - MIDDLE-POSITION: D in the middle of 21 entries fires 15/15.
                 - MULTI-FACT: three planted decisions hold simultaneously 45/45 per-fact,
                   all cited.
                 - DEPTH: no cliff through N=100 (5× the prior bound), all tiers.
                 - WITHIN-CELL DISSOCIATION (the thesis, within-subject): the same control
                   arms that drift 0/30 on unguessable facts hold the DERIVABLE fact
                   (integer money) along a capability gradient — Opus 10/10 unaided,
                   Sonnet 1/10, Haiku 0/10. Derivable improves with capability; unguessable
                   requires the record at EVERY capability.
                 - Fabrication asymmetry spun off as its own finding ([[SOUL-F054]]).
                 In-vivo corroboration + the placement mechanism: [[SOUL-F053]].

STATUS:          Open — promotion conditions MET 2026-06-10: the erosion rung closed via
                 F045/A018, the interaction rung (and middle/multi/N=100) closed via
                 SOUL-155 Phase 2. Doctrine carriage already exists (Rule 13, A018, and now
                 A020); the Body may close this finding at its discretion. The result is
                 operational as the measured backing for the accumulating record's value
                 wherever it carries something the model cannot regenerate on its own.

                 UPSTREAM: this repo IS the Soul System (the upstream) — no cross-project
                 harvest needed. The finding is Soul-meta (about the value of the
                 accumulating record itself, a core Soul premise), so it belongs in this
                 findings/ stream and feeds /soul-distill.
```
