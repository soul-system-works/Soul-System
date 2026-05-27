# Council Convening — Cluster 1 review arc (2026-05-26)

**Witness ID:** SOUL-080
**Topic:** Body resumed mid-Cluster-1; asked "what would the Council's recommendations be?" on next thread.
**Type:** Informal `/soul-council` dogfood (third in the project, per /soul-council spec §Dogfood).
**Body decisions:** Accepted synthesis → continued with recommendation → proceeded with full sweep.
**Outcome:** A012 ratified; 3 specs cleaned via review pass; Cluster 1 design beat formally closed.

This is the inaugural file in `councils/` — created by Body authorization of the new
pointer+detail shape (decision D4, codified in `/soul-council` spec Q2 same session).
Witness entry SOUL-080 holds the pointer; this file holds the detail.

---

## The chamber (8 roles)

Picked for topic-relevance — thread selection across 8 visible options on resume.

| Role | Rationale | Position |
|---|---|---|
| **Archaeologist** | Recovers what's already in the queue and its value | Drafts came from weeks of evidence (F014, F037); deferring rots context |
| **Prophet** | Reads where each thread leads | Dependency funnel: (a) ⊃ (b) ⊃ (c) ⊃ (h); (a) is the keystone |
| **Cartographer** | Holds the map of done/in-flight/unknown | (a) gates 4 threads; (e) independent; (f)(g) watch-only — (a) is highest leverage |
| **Steward** | Judges what still serves; what is review-debt | Cheapest review context is right after authoring; deferral compounds cost |
| **Skeptic** | Adversarial logic; the unexamined assumption | *Is recommending review just F014-contraction in disguise?* Answer: no — review of expansion artifacts is loop-closing, not contraction-by-default |
| **Accountant** | Real costs in time/effort | (a)+(b)+(d) ≈ 1–1.5h closes 4 artifacts; (c) is 1–3h for ONE artifact; leverage favors (a) |
| **Advocate** | Speaks for the Body | Body's question is review-shaped; reading authored work is lighter than starting build cold on resume |
| **Guardian** | Watches Council integrity; skipped obligations | Flagged A008 duplicate (named in prior cursor, still unresolved); recommend fold into same sweep |

## Tensions named

- **Skeptic ↔ Advocate** — addressed; review here is loop-closing, not contraction-by-default.
- **Prophet ↔ Accountant** — (e) F038 amendment is also cheap (~30–45min); Accountant says do both, Prophet says different headspace, sequence them.
- **Guardian** — A008 merge-residue small but unaddressed across two cursors. Fold into the sweep.

## Synthesis

**Thread (a) — Review the four Cluster 1 drafts**, ordered A012 → /soul-council → /soul-roles → /soul-ask-body. A012 first because it anchors the doctrine the three specs reference; if A012 wording shifts under review, the specs inherit cleanly. /soul-council second because it is the lead instrument the other two reference observationally.

## Body decisions

1. **Accepted synthesis** — proceeded with recommendation order.
2. **Proceed on all default options** after review surfaced D1–D8 + verify-gate re-anchoring.
3. **A008 duplicate** — within scope of "proceed"; deleted via `git rm`.

## Review findings per artifact

### A012 (Activation Disciplines amendment)
- **Defect (must-fix):** line 113 carried "F014 has been open for 6+ months" — the exact F028-axis-3 failure mode SOUL-079 named. F014 was filed 2026-05-20 (six days ago). The amendment ratifying the discipline-against-this-error contained the error. Patched: now anchors date (2026-05-20) + duration (six days) + source (dense re-confirmation) separately.
- **Smaller concerns:** Body-Input Obligation cited `/soul-ask-body` which isn't built yet — softened to "inline question, or `/soul-ask-body` once shipped."
- **Strengths:** Bundling rationale (shared shape) is correct; placement (after Naming Roles, before Capturing Ideas) reads as extension not gate-doctrine.

### /soul-council spec
- **D3 cleanup:** Rubber-stamp flagger changed from Skeptic to Guardian (Tribune flagging its own convening is self-reference loop; Guardian watches chamber integrity per seed).
- **D4 resolved:** Output shape locked to pointer (witness) + detail (`councils/SOUL-CCC-<topic>.md`). Driven by measurement: 31 lines/entry average; 7–10 role convening would balloon witness by 3–5x.
- **Strengths:** Sharp scope separation from /soul-expand; failure-mode guards comprehensive; dogfood reference honest.

### /soul-roles spec
- **D5 resolved:** Query/decision split — `/soul-roles` queries log to `.soul/role-queries.jsonl`; only Body-acted-upon insights earn witness entries.
- **D6 REVISED via verify-gate re-anchoring:** Original threshold 10 was wrong direction. At measured ~10/day rhythm, 10 entries ≈ 1 day = normal silence. Revised default to **70** (~1 week) with session-marker alternative deferred to Tier 3.
- **Strengths:** Read-only contract; "silent is observational not pejorative" framing.

### /soul-ask-body spec
- **D7 added:** Structural-limit caveat — (β) does NOT solve the detection problem (α) was rejected for; it provides a Body-triggered moment for the survey, bounded by the same detection limit F014 names. The "may have missed X" caveat is honesty, not politeness.
- **D8 cross-spec coordination:** Removed alternative-wording for (γ); spec now references A012 as canonical owner. Q1 and Q2 resolved by A012 (placement + bundling).
- **Strengths:** (β)+(γ) two-shape decision correct; rejects (α) on same F014 grounds.

## Verify gate fire (mid-arc, post-review)

The pre-completion verify gate (SOUL-F012 hook) caught **two unanchored magnitudes in the AI's own review**:

1. *"average witness entry ~30 lines; convening 60–100 lines"* — informing D4.
2. *"current rhythm ~5 entries/day"* — informing D6.

Re-anchored by measurement:
- 79 entries / 2442 lines = **~31 lines/entry** (the first claim was lucky)
- 79 entries / 8 days = **~10/day** (the second was off by 2x; **D6 revised** from threshold 20 to 70)

**Significance:** SOUL-079's F028-axis-3 discipline (magnitude claims need re-anchoring, not propagation) fired AGAIN this session — caught unanchored magnitudes the same AI was about to embed in spec recommendations. Pattern is now confirmed across two consecutive sessions (SOUL-079 + this convening). The verify gate is doing the work the doctrine claims for it.

## Sixth I027 single-writer instance

The convening was logged via re-read-verify protocol (read tail → confirm SOUL-079 latest → write SOUL-080). No parallel-session interference. Six consecutive clean instances now (SOUL-064, 072, 075, 077, 079, 080). I027's "sixth instance may earn revisiting deferred options" trigger is now reached — open question for the Body whether advisory file-lock or git-arbitration earns a finding.

## Generalizable lesson (candidate for finding/amendment)

**A012 line 113 was not caught by SOUL-079's original cleanup pass.** SOUL-079 caught 3 file instances + 1 in-session statement, edited them, and considered the cleanup complete. But the AMENDMENT BEING DRAFTED contained a secondary mention in the §QUESTION TWO necessity argument that the verify pass missed — focused on headline magnitude claims, not secondary mentions in justification prose.

**Generalization:** Verify gates catch headline-level magnitude failures; secondary-mention propagation needs an independent re-read pass at a later moment (ideally before ratification, by a different "reader" mode than the drafter). This is potentially a new axis on F028 — or just F028 confirmed as needing both the verify gate AND independent re-read for full coverage. Worth a Body decision: finding-worthy or witness-only?

## Tier-3 dogfood notes

Third informal `/soul-council` dogfood. Pattern observations:

- **What held:** tight role statements, named tensions, synthesis, Body decision → action.
- **What's new:** (1) re-anchoring magnitudes mid-convening when verify gate fired — first instance of the doctrine-the-convening-was-discussing catching the convening's own claims. (2) Cross-spec coordination — 4 artifacts gesturing at the same doctrine got pointed at canonical owner. (3) Inaugural use of pointer+detail shape (this file).
- **What didn't hold:** the original review-pass missed A012 line 113 as a defect; needed verify gate + independent re-read for full coverage. The chamber's Skeptic role is in-conversation; needs SEPARATE re-read pass to catch what the drafter missed.

## Status

Resolved. Cluster 1 design beat closes with all four artifacts clean: A012 ratified + in seed; 3 specs draft-ready for build sessions. Next consequential ship: `/soul-council` (umbrella the others depend on observationally).
