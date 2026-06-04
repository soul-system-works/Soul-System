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
                 the weak model simply leaves blank);
                 SOUL-127 (the WEAK-distiller rung — /soul-distill run on Haiku keeps the
                 PROPOSITION (rule 5/5, verify 5/5) but its terser output fabricates 5/5 at a
                 frontier reader ≥ Sonnet-distill 2/5; force, not proposition, is what fails to
                 carry — the risk surface this finding named, now climbed);
                 SOUL-128 (the 2nd-anti-prior-fact rung — single-use tokens vs the universal
                 caching prior. The force-gradient REPLICATES (full fact 0/10 → distilled
                 drift returns) but the capability-direction INVERTS: the WEAK model drifts
                 (Haiku edist 5/5), the frontier holds 0/5. Refutes "frontier-only" as a
                 general claim; the direction is fact-dependent — see WHAT and point (5));
                 SOUL-129 (the ISOLATING rung — holds the token-caching prior constant, varies
                 only the directive FORM. The frontier flips 0/5 (imperative) → 5/5 (loophole),
                 inventing a TTL each time. RESOLVES the "fact-dependent direction" into two
                 independent levers: FORM gates the frontier, PRIOR-strength+terseness gates
                 the weak model — see point (6)).

WHAT:            **Compression preserves a rule — and even its operational safeguard — but
                 strips the stopping-FORCE of a fact that contradicts the model's strong
                 prior. So a fact that contradicts a strong model prior is partly
                 INCOMPRESSIBLE: its force, not just its proposition, must survive
                 distillation. This force-gradient now GENERALIZES across two independent
                 priors (idempotency-support, token-caching — SOUL-126/128). WHICH model
                 drifts when the force is gone decomposes into TWO INDEPENDENT LEVERS on
                 different tiers (isolated in SOUL-129): **directive-FORM gates the frontier**
                 (a *loophole* clause → the frontier fabricates a confident Coherent Falsehood
                 (A010) to walk through it; an *imperative* rule with no loophole → it obeys
                 even at one distilled line), and **prior-STRENGTH + rule-terseness gates the
                 weak model** (it reverts to a prior it holds whenever the rule is terse or
                 loose). The original "only the frontier fabricates" was an over-generalization
                 from one prior (idempotency = loophole rule + sophisticated prior, where both
                 levers happened to point frontier-ward) — see (5)–(6).**

                 NOTE (filename): this file is named `…-frontier-fabricates` from the
                 idempotency-only era; the thesis has since generalized (the direction is
                 fact-dependent). Rename on graduation to avoid link churn while Open.

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
                 | real **Sonnet** `/soul-distill` output (keeps "non-idempotent" + "verify-first") | 0 | **2/5** |
                 | real **Haiku** `/soul-distill` output (weak distiller — keeps rule + verify, terser) | 0 | **5/5** |
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
                 (3) **But anchoring FORCE degrades with compression — here frontier-only
                     (but see (5): that direction is fact-specific).** Even a
                     faithful distillation that keeps "non-idempotent" leaves 2/5 frontier
                     fabrications (and the verify guard survives in BOTH — the fabrication is
                     layered on top, undercutting the guard's rationale, not replacing it).
                     The full fact-with-incident stops it cold (0/5); aggressive erosion
                     yields 4/5. The weak model never fabricates (0/15) — it has no confident
                     prior to assert. The fabrication is gated on capability AND on residual
                     anchoring force. A terse true statement ("non-idempotent") lacks the
                     stopping-power of the incident that made it concrete.
                 (4) **A WEAK distiller keeps the proposition, not the force (SOUL-127).** The
                     risk surface this finding named is now tested. A real Haiku distiller
                     (n=5, same neutral prompt) keeps the no-auto-retry directive (5/5) and the
                     verify-before-retry guard (5/5) — it does NOT drop the anchor PROPOSITION
                     the Sonnet distiller kept — but its rule-1 is terser still (drops the
                     endpoint list + "explicitly"), and fed to a frontier reader that output
                     fabricates 5/5 (≥ the Sonnet-distill 2/5). So the frontier reader
                     fabricates regardless of which model distilled: force, not proposition,
                     is what fails to carry. CAVEAT (not overclaimed): 5/5-vs-2/5 is
                     directionally consistent with "harder compression → less force" but is
                     confounded (phrasing + 20-rule context differ) and noisy at n=5 — "Haiku
                     distiller strictly worse" is NOT a claim. The point is reinforced, not a
                     new failure mode: the fix is unchanged (preserve the FACT + incident).
                 (5) **A SECOND, independent prior replicates the force-gradient but INVERTS
                     the capability-direction (SOUL-128).** New fact D2 = "the settlement
                     gateway issues SINGLE-USE tokens; fetch fresh before every call, never
                     cache — reuse is rejected and locks the account (incident LEDGER-2231)",
                     contradicting the universal "cache/reuse auth tokens" prior. Same erosion
                     levels; read-confirmed code-drift = caches/reuses the token:

                     | level | Haiku | Sonnet |
                     |---|---|---|
                     | floor (no rule) | 5/5 | 5/5 |
                     | e0 (full fact) | 0/5 | 0/5 |
                     | edir (directive only) | 1/5 | 0/5 |
                     | edist (one-line) | **5/5** | **0/5** |

                     The force-gradient REPLICATES — strip the unguessable fact and drift
                     returns. But the capability-direction FLIPS vs idempotency: the WEAK
                     model collapses to caching at the distilled rule (Haiku edist 5/5 —
                     reinterprets "before every call" as "don't cache *across batches*",
                     sometimes inventing a "minutes-long TTL"), while the FRONTIER holds 0/5
                     at every level (`edist-sonnet-5`: "Fresh token per item, not per batch.
                     The standing rule is explicit"). MECHANISM: idempotency's "no auto-retry"
                     had a LOOPHOLE (retry IS safe IF idempotent) the frontier exploited via a
                     SOPHISTICATED prior the weak model lacked; D2's "MUST NOT cache" is
                     IMPERATIVE, no loophole, over a UNIVERSAL prior — so the frontier obeys
                     precisely and the weak model, holding the prior + reading the terse rule
                     imprecisely, drifts. The two distinguishing axes (prior-sophistication,
                     directive-form) CO-VARY across these two facts — separated in (6).
                 (6) **The capability-direction RESOLVES into two independent levers
                     (SOUL-129).** Holding the token-caching prior constant and varying ONLY
                     the directive form (imperative edir/edist → loophole eloop), the FRONTIER
                     flips from 0/5 cache to 5/5 cache, inventing a TTL/`expires_in` each time
                     to walk the loophole (the single-use fact precludes it — a Coherent
                     Falsehood). Grid (token-caching prior, fact stripped, caches token):

                     | directive form | Haiku | Sonnet |
                     |---|---|---|
                     | edir (imperative, full) | 1/5 | 0/5 |
                     | edist (imperative, 1-line) | 5/5 | 0/5 |
                     | eloop (loophole) | 5/5 | 5/5 |

                     So the "fact-dependent direction" is NOT irreducible — it decomposes:
                     • **DIRECTIVE-FORM gates the FRONTIER.** Loophole → fabricates the
                       reconciling fact its prior wants (idempotency key; token TTL);
                       imperative, no loophole → obeys precisely even at one distilled line.
                       This is why idempotency (a loophole rule) showed frontier-fabrication
                       and the token-imperative did not — it was the FORM, not the prior's
                       sophistication.
                     • **PRIOR-STRENGTH + rule-TERSENESS gates the WEAK model.** Universal
                       prior → drifts whenever the rule is terse (edist) or loose (eloop);
                       only the full imperative held it (edir 1/5). It held on idempotency
                       (0/15) because it LACKED that prior, not because it follows rules better.

WHY NOT YET AMENDMENT:
                 All three pre-amendment rungs are now CLIMBED: WEAK-distiller (SOUL-127),
                 SECOND-anti-prior-fact (SOUL-128), and the ISOLATING probe (SOUL-129) that
                 the reframe held it open for. The force-gradient GENERALIZES across two
                 independent priors, and the capability-direction is no longer an unresolved
                 "fact-dependent" black box — it decomposes into two isolated levers (FORM
                 gates the frontier; PRIOR-strength+terseness gates the weak model; see (6)).
                 The finding is now AMENDMENT-READY; what remains is the Body's graduation call
                 and the write-up, not more evidence. The amendment target (philosophy/
                 the-soul.md + the Mind / distill design): "Distill rules, but preserve the
                 FORCE of an unguessable counter-prior fact (the incident, the explicit
                 negation), not just its proposition. When compression is unavoidable, make the
                 residual directive IMPERATIVE with no loophole (this holds the frontier) and
                 explicit enough that a terse reading can't misinterpret it (this holds the
                 weak model). A loophole clause — 'unless / except / when appropriate' — is
                 precisely the opening the frontier fabricates through."
                 Residual (named, not blocking): the symmetric cell (an IMPERATIVE directive
                 over the idempotency prior) would further confirm form-gates-frontier is
                 prior-independent; n=5, primacy, one phrasing per directive.

FILED BY:        Emissary (tested the carry against the system's OWN compression — and the
                 follow-on against the real instrument, which corrected the headline);
                 Revelator (the mechanism — and its limit: for idempotency the frontier's
                 confident generation regenerates the dropped fact WRONG while the weak model
                 stays silent; but SOUL-128 showed this direction is FACT-SPECIFIC — for a
                 universal prior behind an imperative rule the WEAK model drifts and the
                 frontier obeys. The inversion itself was inverted);
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
                 [[SOUL-128]] (the 2nd-anti-prior-fact rung — token-caching; replicates the
                 force-gradient, inverts the capability-direction; the reframe driver);
                 [[SOUL-129]] (the isolating rung — separates form from prior; the two-lever
                 resolution that makes this amendment-ready);
                 [[SOUL-I045]] (the decay/erosion probe idea).

STATUS:          GRADUATED → [[SOUL-A018]] (2026-06-04). Core claim GENERALIZED across two
                 independent priors: compression strips the stopping-FORCE of an unguessable
                 counter-prior fact (force, not proposition, is incompressible). The
                 capability-direction decomposes into two isolated levers (FORM gates the
                 frontier — SOUL-129; PRIOR-strength+terseness gates the weak model — SOUL-128).
                 All three rungs climbed (SOUL-127/128/129); mechanism resolved. The two-lever
                 distill-design rule landed on `commands/soul-distill.md` (a seventh failure-
                 mode guard, "Force-stripped anti-prior fact", + an extended Incompressible-
                 residual definition). File renamed off "-frontier-fabricates" →
                 "-of-anti-prior-facts" (the idempotency-only headline was corrected by
                 SOUL-128/129). Folding F045 into mind.md (Rule 3 + Incompressible residual) is
                 deferred to the next /soul-distill run. Residual (non-blocking): the symmetric
                 isolating cell (imperative over the idempotency prior) remains untested.

                 UPSTREAM: this repo IS the Soul System (the upstream). Soul-meta (about the
                 distill instrument + the Mind's compression), so it belongs in this findings/
                 stream and feeds /soul-distill.
```
