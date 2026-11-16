# /soul-handoff — history

**Source:** Built by the Artificer for the handoff design
(docs/specs/2026-05-21-soul-handoff-design.md); grows only the Soul delta, leaning on
`/compact` + the durable records (SOUL-I007). Pocock's handoff skill informed the
"reference, don't duplicate" principle. **Amended:** SOUL-A023 (2026-07-16) — pointer
provenance marks, from F061 (a cursor pointer propagated a false claim into a Body
decision). **Amended:** 2026-08-28 (v2.3.0) — `OWED UPSTREAM` leaves the cursor for a
durable `upstream.md`; the carry-forward clause, the three-cursor escalation and all
other nagging go with it (SOUL-I062;
`docs/specs/2026-08-28-upstream-store.md`). **Amended:** 2026-08-28 (v2.3.1) — the
name-the-file test and the routing for what fails it, from the first mining pass
(26% misfiled), and its routing for what fails it. **Amended:** 2026-10-19 (mining
pass 2, SOUL-202) — F065 ruled (append marked unconfirmed; step 1 collects every
marked entry into the new `UNCONFIRMED` field; cursor first, then show); F067's fix
(an inherited OPEN GATES / NEXT STEP obligation is checked or dropped, pending the
Body's confirmation; commands, not counts, in WHERE WE ARE); flush before a long unattended run;
`git check-ignore` instead of asserting the cursor is ignored; 1b's surface gains
`operations/*.md` and `tools/*`. **Amended:** 2026-10-21 (v2.10.1, SOUL-208) — 1b
first checks for the Soul System repo itself, where there is no upstream (SOUL-187).
**Amended:** 2026-11-05 (v3.9.0, SOUL-A031) — model-initiated captures are appended
accepted with an opt-out; the unconfirmed mark and the ratify step are retired, and
the cursor's `UNCONFIRMED` field becomes `NEW ENTRIES` (SOUL-I085).
**Amended:** 2026-11-05 (v3.10.0, SOUL-I086) — a long unattended run keeps a
decisions log for `/soul-debrief`; POINTERS gains the newest debrief.
**Amended:** 2026-11-06 (v3.11.0, mining pass 3, SOUL-234) — a vault-linked cursor is
checked in the vault and committed with `vault.py sync`.
**Amended:** 2026-11-12 (v3.12.0, SOUL-A032) — runs itself when the cursor is stale
(about 100,000 tokens, or a summary, since the last write; `hooks/upkeep.py`), and checks
whether the Mind is due (step 1c).
**Adopted:** 2026-05-21. **Status:** active.
**Amended:** 2026-11-13 (v3.13.0, SOUL-239) — the step is about 100,000 tokens; `☀  ` starts every line about something the Soul did on its own.
