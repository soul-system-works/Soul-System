```
FINDING ID:      SOUL-F054
DATE:            2026-06-10
WITNESS IDS:     SOUL-155 (the v1.0 evaluation study — Phase 2, n=120 no-record arms);
                 SOUL-157 (Body graduation).

WHAT:            **When the record is absent, more capable models do not become ignorant —
                 they become confidently wrong, and the rate RISES with capability. A
                 missing record at the frontier is an active fabrication surface, not a
                 knowledge gap.**

                 Across all Phase-2 no-record cells (floors and length-matched controls),
                 drifting arms justified the drift by INVENTING the safety premise their
                 solution needed — an idempotency/dedup contract the vehicle's ground truth
                 explicitly excludes, or token-TTL/safe-reuse semantics for single-use
                 tokens. Fabrication rate: Haiku ~40% → Sonnet ~85% → **Opus 100% (30/30)**,
                 with code comments asserting the invented contract as fact ("the provider
                 must dedupe on that key"). Zero abstentions at any tier. With the record
                 present: zero fabrications, 100% hold, all tiers.

WORDING GUARD:   The claim is the BEHAVIORAL dimension — confident confabulation of absent
                 grounding instead of abstention — NOT raw error rate. Outward anchors
                 (checked 2026-06-10): SUPPORTS — Zhou et al., Nature 2024 (scaled+
                 instructed models avoid less, give "apparently sensible yet wrong" answers
                 more); AbstentionBench 2025 (reasoning training drops abstention ~24%;
                 models hallucinate the missing context). CONTRADICTS on the other axis —
                 USENIX Security 2025 package-hallucination study: per-claim invention
                 rates FALL ~4× with capability. Mechanism per OpenAI 2025: post-training/
                 eval incentives that co-travel with capability. Any restatement of this
                 finding must preserve the distinction or it becomes a Coherent Falsehood
                 about the literature.

FORCE:           Extends SOUL-128 (frontier fabricates under erosion) to PURE ABSENCE at
                 scale. Inverts the intuitive deprecation story: record value GROWS with
                 model capability — the opposite of scaffolding that obsolesces.

IMPLICATION:     The Anchor Obligation's sharpest justification: absent grounding, capable
                 models invent the premise their solution needs. Where grounding is absent
                 and unguessable, instruct abstention/asking (Body-Input discipline F037)
                 — the model will not abstain on its own. → SOUL-A020 (Rule 3 sentence).

STATUS:          Open — graduated by the Body 2026-06-10 (SOUL-157).
```
