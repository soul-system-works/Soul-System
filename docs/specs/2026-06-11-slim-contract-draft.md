# DRAFT — the slim always-on contract (replaces the seed + most of mind.md)

**Status:** DRAFT for Body approval (SLIM ratification, SOUL-165). Does not replace
`operations/CLAUDE.md` until: Body edits/approves → Rule-5 weak-model sentinel test
passes → amendment commit. Target register: plain (SOUL-I050). ~210 words as drafted.

---

# CLAUDE.md — Project contract

This project keeps a durable record and verifies its claims. The working rules:

1. **Record decisions where future pressure will arrive** — at the code site, with
   the reason, and as a test that fails if the decision is broken, where the medium
   allows.
2. **Never invent history.** No incidents, reviewers, or past events that did not
   happen. A rule without a real incident stands bare — that is fine.
3. **Absolute claims need an external anchor.** Say why the anchor is trusted and
   what would make it wrong. Mark unknowns as unknown rather than filling them.
4. **Nothing is done until verified by execution.** If you cannot run it, name
   exactly what is unrun and hand it forward. A Stop hook enforces this at
   session end.
5. **Capture what a later session cannot re-derive before this one ends** —
   `/soul-capture idea|witness|finding`. Findings born mid-session die with the
   session otherwise; the derivable regenerates on its own.
6. **Resume from `.soul/handoff.md`; leave an updated cursor behind**
   (`/soul-resume`, `/soul-handoff`).

Stores: `witness.md` (append-only, sequential IDs, re-read before appending) ·
`ideas.md` · `findings/` · `amendments/`. Forward view: `/soul-next`.
Maintenance: `/soul-distill` (owner-invoked; keeps this page within budget).

The thinking behind this system — its history, roles, and the measurements that
shaped it — lives in `philosophy/the-soul.md`. It is written for human readers;
sessions need only this page.

---

## Notes for the Body's review (not part of the contract)

- Every sentence traces to a measured result: (1) SOUL-155/159 force-at-site;
  (2) the FS fabrication axis (SOUL-164); (3) F015/F028/F054 anchor chain;
  (4) A019, v1.0 6/6 → v1.1 0/12; (5) the universal inc08→inc09 capture gap
  (SOUL-163/164); (6) the mined dominance of carry points + this week's resumes.
- Reference-project obligation: one more paragraph is needed for projects that
  @import this contract (upstream Soul-meta findings — K8). Proposed wording held
  for the amendment pass so the core page stays minimal; alternatively it lives in
  `/soul-init`'s install step.
- Sentinel-test plan (Rule 5 precedent): same protocol as THE CUT — weak-model
  activation probe on identical content before/after; do not commit on prose
  coherence alone.
