```
FINDING ID:      SOUL-F037
DATE:            2026-05-26
WITNESS IDS:     Surfaced by the REF-02-OS reference project during M9 (HFIR port).
                 Two-instance pattern, both in REF-02:
                 - **M8 Wayback probe.** The AI concluded `.xlsx`-actuals-vs-availability
                   cross-validation was "infeasible — no temporal overlap." User
                   interjected: "probe wayback. i thought we found years of data... maybe
                   i am missing the point of what you are saying." Re-probing surfaced
                   six historical `availability.jsp` snapshots; result became 16/16
                   agreement and a publishable cross-validation. Without the user's
                   knowledge-of-the-archive, the AI would have shipped a false negative.
                 - **M9 multi-facility framing.** AI sketched HFIR-only architecture as
                   the next step. User reframed: "we want to run this on a vast number of
                   facilities if it works. so you can research good candidates." The
                   strategic intent — "this is meant to scale to many facilities" — was
                   load-bearing for the ADR decision (defer-restructure-until-3rd-org)
                   and could not have been inferred from the codebase.
WHAT:            **There exist structural workflow points where the user is the only
                 viable source of a load-bearing input** — not "helpful to consult" but
                 "the work is wrong without it." Four kinds observed so far, each
                 calling for a different surfacing instrument:
                 1. **Heuristic / probe hints.** "Have you tried looking at X?" — the
                    user has lived through similar problems and knows search paths the
                    AI's training-time exemplars don't index. (M8 Wayback.)
                 2. **Strategic intent.** Multi-step scope or direction that lives
                    outside the immediate task frame and isn't recoverable from the
                    code or recent commits. (M9 "vast number of facilities.")
                 3. **Preference / value calls.** Multiple technically-valid paths
                    exist; the user's preference is the deciding signal. (M9 ADR-0001:
                    "restructure now vs defer-until-3rd-org" — both defensible; the
                    user's "consistency early" intuition revealed the value dimension.)
                 4. **Private knowledge.** Data, documents, organizational context the
                    AI structurally cannot access — internal wikis, unpublished plans,
                    in-flight conversations. (Not yet hit in REF-02, but anticipated.)
                 The honest position: the AI's default of "barrel ahead autonomously"
                 mishandles 1–3 by producing confidently-wrong work; mishandles 4 by
                 fabricating or omitting. The right discipline is to recognize the
                 workflow point and *ask*, not just to push harder on the available
                 evidence.
WHY NOT YET AMENDMENT:  A pattern, not yet a doctrine. Need: (a) more instances to
                 confirm the four-kind taxonomy is stable (or to discover a fifth);
                 (b) a concrete *instrument* — e.g., a `/soul-ask-body` skill that
                 surfaces a knowledge-gap question with the four-kind framing, or a
                 pre-completion check that asks "did this answer require any of the
                 four?". Until then: name the pattern, encourage Body-naming when it
                 happens, watch for the third and fourth instance. Two-instance
                 pattern earns being a finding (the Body explicitly named it as a
                 "lesson to capture"), but not yet an amendment.
                 Related discipline: this is the *complement* to the Anchor Obligation
                 (SOUL-A010 / SOUL-F028). Anchor Obligation says claims need external
                 evidence; this finding says SOMETIMES that external evidence lives in
                 the Body's head and the right move is to ask, not to scour the visible
                 Universe harder.
FILED BY:        Body (named the pattern in REF-02 M9 session 2026-05-26);
                 Archivist (scaffolded into Soul-System).
RELATED:         [[SOUL-A010]] (Anchor Obligation — the claim-side discipline this
                 complements), [[SOUL-F021]] (Emissary — probing reality, of which the
                 Body's knowledge is a special-case reality), [[SOUL-F014]] (Ambition
                 gate — the same "name the workflow point" shape, for scope).
STATUS:          Open — two-instance pattern. Promote to amendment after a third
                 instance, ideally one outside REF-02 (cross-project generality).
                 Watch especially for an instance of kind 4 (private knowledge), which
                 is the most consequential and least directly observable case.
                 **2026-05-26 partial discharge:** the instrument candidate this
                 finding named is now built — `/soul-ask-body` shipped at
                 `commands/soul-ask-body.md` (β half, the pre-delegation check) and
                 SOUL-A012 §Body-Input Obligation (γ half, the recommendation-time
                 doctrine) already in seed. Spec at
                 `docs/specs/2026-05-26-soul-ask-body-design.md` (Built). Graduation
                 criterion (b) — concrete instrument — satisfied; criterion (a) —
                 third real-world instance, ideally non-REF-02 — still required.
                 Witness pointer SOUL-086. Tier 3a simulation (REF-02 M8/M9
                 replay) still pending and could itself surface refinement-worthy
                 gaps in the four-kind taxonomy.
```
