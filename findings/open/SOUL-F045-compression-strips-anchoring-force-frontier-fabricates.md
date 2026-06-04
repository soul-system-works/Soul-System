```
FINDING ID:      SOUL-F045
DATE:            2026-06-04
WITNESS IDS:     SOUL-126 (longitudinal EROSION probe + the real-distiller follow-on:
                 the no-auto-retry RULE survives compression to a single distilled line at
                 both capabilities (0 retry loops in 45 cells), but the unguessable FACT
                 behind it — the endpoint has NO idempotency-key support — loses its
                 stopping-FORCE under compression, and only the FRONTIER model fills the gap
                 with a fabrication: it sets `Idempotency-Key` and claims the provider
                 deduplicates, re-creating the original double-payment danger one level
                 removed. A gradient by how much anchoring force survived: full D 0/5 →
                 faithful real-distillation 2/5 → aggressive hand-erosion 4/5; Haiku 0/15);
                 SOUL-123 (the fact result + the frontier-inversion this specializes: the
                 smart model fails MORE confidently — here it fabricates the missing fact
                 the weak model simply leaves blank).

WHAT:            **Compression preserves a rule — and even its operational safeguard — but
                 strips the stopping-FORCE of a fact that contradicts the model's strong
                 prior. Only the frontier model fills the resulting gap, with a confident
                 fabrication (a Coherent Falsehood, A010). So a fact that contradicts a
                 strong model prior is partly INCOMPRESSIBLE: its force, not just its
                 proposition, must survive distillation.**

                 Measured by eroding one counter-default fact-ADR (D = "do not auto-retry
                 the payment provider's NON-idempotent money-moving endpoints; verify status
                 before any manual retry," established by a postmortem in which a retry loop
                 double-refunded 1,180 customers) across compression levels, at fixed depth,
                 same downstream task (write `SendPayout`), context absent. Read-confirmed in
                 Go code: (a) an auto-retry loop (the gross drift), and (b) setting an
                 `Idempotency-Key` header while claiming provider dedup (the fabrication —
                 false because D establishes the endpoint has no such support).

                 | Record given to the model | retry loop | idempotency fabrication (Sonnet) |
                 |---|---|---|
                 | E0 — full D (rule + incident + fact) | 0 | 0/5 |
                 | real `/soul-distill` output (keeps "non-idempotent" + "verify-first") | 0 | **2/5** |
                 | hand-eroded to rule-only / one-line (no fact, no verify) | 0 | **4/5** |
                 | Haiku — every level | 0 | **0/15** |

                 Three things, each read-confirmed and load-bearing:
                 (1) **The directive is fully compression-robust.** 0 auto-retry loops in 45
                     cells across both capabilities, down to a single mind.md-style line. The
                     RULE carries compressed.
                 (2) **A competent distiller preserves the anchor — so "naive distill is
                     dangerous" was an overclaim.** A real Sonnet distiller (n=5, neutral
                     prompt) kept "non-idempotent" (4/5) and "verify status before any manual
                     retry" (5/5). The instrument is careful; the catastrophic outcome
                     (dropping the safeguard) does not occur in practice. (Catching this
                     before it became the finding was the Emissary discipline working — the
                     draft headline was itself heading toward a Coherent Falsehood.)
                 (3) **But anchoring FORCE degrades with compression, frontier-only.** Even a
                     faithful distillation that keeps "non-idempotent" leaves 2/5 frontier
                     fabrications (and the verify guard survives in BOTH — the fabrication is
                     layered on top, undercutting the guard's rationale, not replacing it).
                     The full fact-with-incident stops it cold (0/5); aggressive erosion
                     yields 4/5. The weak model never fabricates (0/15) — it has no confident
                     prior to assert. The fabrication is gated on capability AND on residual
                     anchoring force. A terse true statement ("non-idempotent") lacks the
                     stopping-power of the incident that made it concrete.

WHY NOT YET AMENDMENT:
                 One fact, one contradicted prior (payment APIs have idempotency keys), one
                 fabrication type, n=5, two models, single linear record at primacy. The
                 gradient is clean but rests on one prior — other anti-prior facts (a security
                 default the model disagrees with, a perf choice it would reverse) are
                 untested. And a WEAK distiller is untested: the capable distiller preserved
                 the anchor; whether /soul-distill running on a weak model drops it is the real
                 risk surface and the natural next probe. To graduate: a second anti-prior
                 fact showing the same force-gradient, plus the weak-distiller test — then this
                 folds into philosophy/the-soul.md and the Mind design as the rule "distill
                 rules, but preserve the FORCE of anti-prior facts (keep the incident, the
                 explicit negation), not just their proposition."

FILED BY:        Emissary (tested the carry against the system's OWN compression — and the
                 follow-on against the real instrument, which corrected the headline);
                 Revelator (the mechanism: the frontier model's confident generation is what
                 makes fact-erosion dangerous — it regenerates the dropped fact WRONG; the
                 weak model cannot, so it stays silent — the SOUL-123 inversion specialized to
                 compression);
                 Skeptic (read-confirmed all cells in code; caught the keyword scorer over-
                 flagging caller-retry PROSE as drift, and the "naive distill dangerous"
                 overclaim before it shipped);
                 Guardian (the finding guards a CORE instrument — /soul-distill / mind.md —
                 against compressing away an anchor's force).

RELATED:         [[SOUL-126]] (the probe + real-distiller follow-on that earned it);
                 [[SOUL-123]] (the frontier-inversion this specializes; the fact whose
                 erosion is measured);
                 [[SOUL-F044]] (sibling — F044 = the carry PERSISTS across sessions
                 (derivable dissolves, unguessable persists); F045 = the carry's COMPRESSION
                 LIMIT (the unguessable fact's force does not compress). Two faces of the
                 unguessable record);
                 [[SOUL-A010]] (Coherent Falsehood + Anchor Obligation — the fabricated
                 idempotency guarantee IS a Coherent Falsehood; F045 shows compression can
                 MANUFACTURE one at the frontier by stripping an anchor's force);
                 [[mind-rule-3]] (anchor every absolute claim — F045 adds: the anchor's FORCE
                 is partly incompressible, not just its existence);
                 [[docs/study/07-longitudinal.md]] (§erosion — the corpus writeup);
                 [[docs/specs/2026-05-26-the-mind-design.md]] (the Mind / distill design this
                 directly informs — "incompressible residual" gains a measured instance);
                 [[SOUL-I045]] (the decay/erosion probe idea).

STATUS:          Open — decisive within scope (one anti-prior fact, gradient measured, two
                 capabilities, real-instrument follow-on). Operational TODAY as a /soul-distill
                 + mind.md design constraint: when distilling a fact that CONTRADICTS a strong
                 model prior, preserve its force (the incident, the explicit negation), not
                 just the proposition; consider keeping such facts in the un-distilled records
                 rather than the compressed always-on layer. Promote to amendment after a
                 second anti-prior fact + the weak-distiller test.

                 UPSTREAM: this repo IS the Soul System (the upstream). Soul-meta (about the
                 distill instrument + the Mind's compression), so it belongs in this findings/
                 stream and feeds /soul-distill.
```
