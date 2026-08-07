AMENDMENT ID:    SOUL-A024
DATE:            2026-08-07
WITNESS IDS:     SOUL-173 (the anchoring measurement and the wrong-unit failure
                 that nearly buried it: per text block the corpus looked healthy,
                 per turn the median reply ran 2,537 chars with 72% of
                 sub-80-character questions drawing back over 1,500). SOUL-172
                 (the gate-cost measurement whose session captured SOUL-I054 as
                 a companion cost item). The Body's own repeated report is part
                 of the evidence and is recorded verbatim in SOUL-173: the
                 complaint was made, measured against, and upheld.
WHAT CHANGES:    A ninth contract rule — **Answer at the size of the ask.** A
                 one-line question gets a one-to-three-sentence answer; lead with
                 the answer and stop — no restating the question, no reasoning
                 that did not change it, no closing summary of what was just
                 said, no pre-empting follow-ups. Structure (headings, tables,
                 bold-label lists) is for genuinely multi-part content; on a
                 short answer it is length, not clarity. The rule carries its
                 measurement because the adjective alone had already failed.
                 Consequent edit: the per-project **Register line is reduced to
                 vocabulary only**. Length is no longer a register concern — it
                 holds under `plain` and `fluent` alike.
WHERE IN SOUL:   operations/CLAUDE.md (the contract) — new rule 9. CLAUDE.md
                 (this project's Register line) and skills/soul-init/SKILL.md
                 (the template written into new projects) — both reduced to the
                 vocabulary choice, pointing at rule 9 for length.
QUESTION ONE:    Evidence — SOUL-173. The measurement is on this machine's own
                 transcripts, 908 Body-facing turns across 14 project
                 directories, and it is unambiguous: median 2,537 chars per
                 turn, 76% over 1,500, and a question under 80 characters draws
                 a median 2,106-char reply. Verbosity is the central tendency,
                 not a tail — 51% of all turns exceed 2,500 chars. The evidence
                 also names what the rule must NOT be: the classic filler
                 patterns are already gone (preamble openers 4% overall, 0% in
                 the longest decile; request-restating, "Summary" sections and
                 hedging closers ≈0%), so guidance aimed at fluff cannot reach
                 this. What remains long is real content delivered at a size
                 nobody asked for.
QUESTION TWO:    Necessity — the current Soul says "keep responses concise" in
                 the Register line, adopted 2026-06-10 (SOUL-I050 / the
                 register-flag spec). It did not work, and this is measured
                 rather than argued: at baseline, Soul-governed projects ran
                 median 2,608 chars per turn against 2,350 in non-Soul control
                 projects — the governed arm was slightly LONGER. An adjective
                 with no target is unfalsifiable and unenforceable; the session
                 cannot tell whether it complied. Rule 9 replaces the adjective
                 with a target tied to the size of the ask, which a session can
                 check itself and a later session can measure. Placement is also
                 necessary, not cosmetic: the Register line is COPIED into each
                 project's CLAUDE.md, so an edit there reaches only the project
                 edited (at the time of this amendment, 3 of 8 Soul projects
                 carried the old line, 3 carried none, 1 had no CLAUDE.md). The
                 contract is @-imported by every project, so doctrine that must
                 reach all of them belongs here. General form: the imported
                 contract carries doctrine; the copied line carries only
                 per-project CHOICES.
QUESTION THREE:  Coherence — no contradiction found, and one tension worth
                 naming. Rule 9 could be read against rule 3 (absolute claims
                 need an external anchor, mark unknowns as unknown) and rule 8
                 (overrides happen out loud), both of which cost words. It does
                 not override them: rule 9 governs length relative to the ask,
                 never the disclosure of a gap or an unknown. An honest "I could
                 not verify X" is never the thing to cut — cutting it would
                 violate rule 4, which is the stronger rule. Where they meet, the
                 anchor stays and the surrounding explanation goes. Rule 9 also
                 REINFORCES the completion gate's existing reply convention
                 (operations/completion-gate.md: lead with the ask, gate last as
                 one compact line, "visible means specific and anchored, not
                 verbose") — that convention was already the right shape and
                 applied only at gate firings; rule 9 generalizes it to every
                 turn.
STATUS:          Accepted 2026-08-07 (Body's call, same session as the
                 measurement).

---

**Scope note — deliberately not machine-global.** The Body's call: the rule stays
inside the Soul System and is NOT added to the machine-global CLAUDE.md, so
non-Soul projects remain a control arm and the rule's effect stays observable.
Baseline for both arms is recorded in SOUL-I054; re-measure with the turn-level
method preserved in `tools/gate-cost-measure.py`.

**Known gap at acceptance.** One of the eight Soul-governed projects is governed by its
`witness.md` but has no CLAUDE.md, so it imports no contract and rule 9 does not
reach it. Every other Soul project @-imports `operations/CLAUDE.md` and picks the
rule up at next session start with no deploy step.

**What would make this wrong.** If replies get shorter but the Body starts having
to ask follow-up questions to get information that used to arrive unprompted, the
target is mis-set and rule 9 is trading their time for tokens — the wrong trade.
The check is not reply length alone; it is reply length against follow-up rate.
