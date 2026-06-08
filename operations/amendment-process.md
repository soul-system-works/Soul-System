# The Amendment Process

How a change to the Soul (or a Finding) is evaluated and recorded. This is the
process doctrine for the `amendments/` and `findings/` records — preserved at the
Cut (→1.0) when the broader `council-synthesis.md` convening ceremony was retired.
The records it governs are kept; this is how they evolve.

A doctrine change is earned through honest evidence from real use, not through
reasoning, cleverness, or enthusiasm. The bar is the three Amendment Questions.

---

## The Amendment Questions

A Proposed Amendment must answer all three before it is accepted. An amendment that
cannot answer all three is a **Return**, not an acceptance.

**Question One — Evidence.** What specific entries in the Witness log demand this
change? Name them by ID. If no entries are named, the amendment has no foundation.

**Question Two — Necessity.** What in the current Soul does this amendment extend,
refine, or correct? Why is the current Soul insufficient on this point? If the
current Soul already covers it, the amendment is redundant, not necessary.

**Question Three — Coherence.** Does this amendment contradict anything else in the
Soul? If yes — which is more true, and why? An amendment that introduces
contradiction without resolving it weakens the Soul rather than strengthening it.

---

## Accepting an Amendment

When an amendment answers all three questions honestly, it is accepted and filed in
`amendments/accepted/` with the record:

```
AMENDMENT ID:    [project-code]-A[sequential number]   e.g. SOUL-A001
DATE:            [date]
WITNESS IDS:     [IDs of entries that demanded this change]
WHAT CHANGES:    [the specific addition, refinement, or correction]
WHERE IN SOUL:   [which section is affected]
QUESTION ONE:    [evidence summary]
QUESTION TWO:    [necessity summary]
QUESTION THREE:  [coherence summary — or: no contradiction found]
```

The amendment is then applied to the Soul document. The prior version is retained,
never discarded.

---

## Returning an Amendment

When an amendment cannot answer all three questions, it is returned with a specific
reason (a Return is not a rejection — it means more evidence or thinking is needed):

```
RETURN ID:       [project-code]-R[sequential number]
DATE:            [date]
AMENDMENT:       [what was proposed]
REASON:          [which question it failed and why]
WHAT IS NEEDED:  [what evidence or thinking would allow it to proceed]
STATUS:          Open — revisited when conditions are met
```

Returns live in `amendments/returned/`, revisited when related evidence surfaces.

---

## Filing a Finding

When an observation matters but does not yet warrant amending the Soul, it is filed
as a Finding (scaffold via `/soul-capture finding` — earned, the Body decides):

```
FINDING ID:      [project-code]-F[sequential number]
DATE:            [date]
WITNESS IDS:     [IDs that informed this finding]
WHAT:            [the observation, compressed]
WHY NOT YET AMENDMENT:  [what evidence is missing to graduate it]
FILED BY:        [role(s)]
RELATED:         [other findings / returns / open witness entries]
STATUS:          Open
```

A Finding lives in `findings/open/` and moves to `findings/closed/` when it resolves
— by escalation into an Amendment, by becoming moot, or by being absorbed into other
Findings. Findings are not failures; they are honest work at the edge of what is
currently understood.

---

**Source:** Extracted at the Cut (→1.0, 2026-06-08) from the retired
`council-synthesis.md` — the convening ceremony was cut, but the amendment-acceptance
process governs the kept `amendments/` + `findings/` records and is load-bearing
(coherence catch, this session). **Sub-class:** PROCEDURE. **Status:** active.
