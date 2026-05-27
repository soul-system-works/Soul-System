# /soul-roles — Design Spec

**Date:** 2026-05-26
**Status:** Draft — Cluster 1 design beat, sibling of /soul-council; spec content is
draft pending Body review.
**Topic:** A read-only observability instrument that surfaces which Council roles have
actually fired in the project vs sat idle.

## Problem (two levels)

- **Immediate:** The Body has no view into role activity. A Steward silent for weeks
  looks identical to a Steward who is satisfied with the current state. A Researcher
  who never fires looks the same as one who decided no outward reach was needed. Roles
  exist in doctrine; their activation is invisible. The witness log records TYPE fields
  (which roles were invoked per entry), but no instrument aggregates that data into a
  legible picture.
- **Larger system:** [[SOUL-F014]]'s evidence on role economics — "contraction roles win
  by default because expansion roles cost more and risk being wrong" — was discovered
  by manual counting across one project. That manual analysis is the empirical method
  this instrument would automate. F002's "continuous-role invisibility" is the same
  concern from a different angle. The Council exists; whether it actually convenes is
  an open empirical question per project.

## Decision (settled with the Body, 2026-05-26 beat)

1. **Read-only.** Never invokes a role, never changes state. Pure observation.
2. **Body-invoked.** Like `/soul-council`, no auto-fire. The Body asks; the instrument
   reports.
3. **Existing data only.** No new substrate. Reads witness.md TYPE fields, findings'
   FILED BY fields, and (if present) `.soul/events.jsonl` per the SOUL-F018 event
   standard.
4. **Honest about data quality.** Entries without TYPE = invisible to the count; output
   must name this caveat. The instrument is as good as the data; it does not assume.
5. **Sibling of `/soul-council`** — not a sub-feature. Council = invocation; roles =
   observability. Different jobs.

## The abstraction layer

- **What varies:** the window (whole project / recent N / date range), the role focus
  (all / subset), the output format (table / summary).
- **What decides whether it varies:** the Body's arguments to the command; sensible
  defaults otherwise.
- **What cannot vary:** read-only behaviour; data source is the existing record (no
  back-fill, no inference); honesty about missing data; no auto-fire.

## The command: `/soul-roles [window]`

Steps the agent runs:

1. **Parse arguments** (all optional):
   - `<window>` — `all` (default), `recent` (last 20 witness entries),
     `since YYYY-MM-DD`, or `last <N>`.
   - `--role <name>` — focus on one role.
   - `--silent-threshold <N>` — count "silent" if no invocation in N entries
     (default **70**, ≈ 1 week at the measured 2026-05-26 rhythm of ~10
     entries/day; tune from dogfood). Lower defaults (10, 20) flag normal
     between-session silence as silence — too coarse for this rhythm.
2. **Read data sources** (in order):
   - `witness.md` TYPE fields, parsed per entry. Per-witness role-list.
   - `findings/open/*.md` and `findings/closed/*.md` FILED BY fields.
   - `.soul/events.jsonl` if present (per SOUL-F018 event standard); use role tags.
3. **Tally per role:**
   - Total invocations in the window.
   - Most recent invocation (witness ID + date).
   - Longest silent gap (entries between consecutive invocations).
   - First invocation in the window.
4. **Classify roles:**
   - **Silent** — zero invocations in the window, OR no invocation in last
     `--silent-threshold` entries.
   - **Active** — invocations within threshold.
   - **Hot** — top 3 by invocation count (could be over-firing or genuinely
     load-bearing; output is neutral on which).
5. **Render output** (default: table + summary):
   - **Table:** role | count | most-recent | longest-silent-gap | classification.
   - **Summary:** "Silent roles: X, Y, Z (no fire in last N entries)." "Hot roles:
     A, B, C (top by count)." "Data quality: M of N entries missing TYPE field;
     results inferred from N - M."
   - Neutral language. "Silent" is observational, not pejorative. A silent role
     may be correctly silent for this project.
6. **Logging — split by purpose** (resolved 2026-05-26 review pass).
   - **Queries log to `.soul/role-queries.jsonl`** — one JSONL line per invocation
     (timestamp, scope, headline result). Cheap, append-only, doesn't pollute
     witness.md scannability at the ~10 entries/day project rhythm.
   - **Witness entry ONLY for acted-upon insights** — e.g., "Body ran /soul-roles,
     observed Researcher zero-fire across 30 entries, decided to invoke /soul-council
     on outward reach." The DECISION is record-worthy; the bare query is not.

### Output example (sketch — final format settled at build)

```
/soul-roles last 30

ROLE-FIRING SUMMARY (last 30 witness entries, 2026-04-26 to 2026-05-26)

Role              Count  Last seen  Longest gap  Status
Skeptic              18  SOUL-076   2            Hot
Architect            14  SOUL-077   1            Hot
Emissary             12  SOUL-076   3            Active
Steward               7  SOUL-068   8            Silent (>5)
Prophet               2  SOUL-064   18           Silent
Revelator             1  SOUL-053   29           Silent
Researcher            0     —       30           Silent (zero)

Silent: Researcher, Revelator, Prophet, Steward.
Hot: Skeptic, Architect, Emissary.

Data quality: 4 of 30 entries missing TYPE field; results from N=26.
```

## Failure-mode guards

| Failure | Guard |
|---|---|
| **Pejorative reading** — "Researcher is broken" | Output language is neutral. "Silent" means observed-not-firing in the window, NOT judgement that the role is failing. Body reads the picture. |
| **Data-quality blindness** — TYPE field missing on some entries | Every output names data quality: "M of N entries missing TYPE; results from N-M." Silent rate must always be qualified. |
| **Role-name canonicalisation drift** — entries spell roles differently | Maintain canonical list (the 13 from seed §The Council + Hands). Variants normalised at parse time; unrecognised role names surfaced in a separate "unrecognised" line. |
| **Misuse as a productivity dashboard** — "we need more Researcher invocations" | Output explicitly disclaims: counts are descriptive, not prescriptive. The right number of Researcher invocations depends on whether outward research was warranted, not on hitting a target. |
| **Scope creep into auto-fire** — temptation to add "alert if Steward silent for 30 days" | NO. Read-only is the contract. Auto-firing observability is a /soul-council moment, not this instrument. |
| **Witness entry pollution** — every /soul-roles invocation creates a witness entry, dilutes signal | Witness entries from /soul-roles are short and explicitly tagged; future Cartographer pass can filter them. Alternative: log to .soul/role-queries.jsonl instead. Decision deferred to build session. |

## Dogfood reference

- **F014's ROLE ECONOMICS finding (2026-05-21)** did this analysis manually across one
  project: counted invocations, found "contraction roles dominated; expansion roles
  fire only on demand." That manual count is the empirical pattern this command
  automates. `/soul-roles` running on the same data should reproduce F014's headline.
- **The Cartographer cluster pass in this session** is an adjacent pattern — read the
  open pile, surface what's there. `/soul-roles` is the same shape pointed at roles
  instead of findings.

## Open questions

- **Q1. Parse FILED BY in findings, not just TYPE in witness?** Probably yes — findings
  are deliberate role attributions; richer signal per entry. Add at MVP.
- **Q2. Honor `.soul/events.jsonl` per SOUL-F018?** Yes if present. If absent (most
  projects today), fall back to witness/findings only. No build dependency.
- **Q3. Silent-threshold default — RESOLVED 2026-05-26.** Default 70 (~1 week at
  measured rhythm 79 entries / 8 days ≈ 10/day). Earlier draft said 10, but at the
  current rhythm 10 entries ≈ 1 day, which flags routine between-session silence.
  Alternative: session-marker-based ("silent since last `/soul-handoff`") — cleaner
  structurally but requires session-boundary parsing; defer to Tier 3.
- **Q4. Hands roles included?** Architect, Craftsman, Artificer are in the seed but
  are NOT Council. Include in tally (they're the build side), but tag separately:
  "Hands (build): Architect 14, Artificer 4, Craftsman 0." Body sees the full role-firing
  picture without conflating Council and Hands.
- **Q5. Should witness-entry-per-query be replaced with a /tmp log or .soul/queries
  file?** Resolve at build — deferring to keep MVP simple.

## Tier 3 — validation plan

After build:

- **Tier 3a — reproduce F014's manual finding.** Run `/soul-roles all` on the current
  Soul-System repo. If output reports Skeptic / Accountant / Steward as Hot and
  Researcher / Revelator / Prophet as Silent (matching F014's empirical claim), method
  is validated. If not, data quality is the gap; refine TYPE-field discipline.
- **Tier 3b — cross-project.** Run on a reference project (REF-05 is the
  freshest). Does the role profile differ meaningfully? Same instrument, different
  project, different role economics — that's the empirical test the F014 question wants.
- **Tier 3c — does it earn its place?** Track invocation count over first month. If
  Body uses `/soul-roles` <2× per month, it's ceremony; consider retirement or scope
  reduction.

## Build dependencies

- Existing infrastructure: `witness.md`, `findings/`, optional `.soul/events.jsonl`.
- No new substrate required. Pure read + render.
- Parsing TYPE fields needs awareness of the multi-line / multi-role format used in
  this repo's witness (roles separated by `;` or listed across lines). Concrete grammar
  settled at build.

## Discharges (when shipped)

- [[SOUL-I031]] — directly (the instrument it captures).
- [[SOUL-F002]] — partial (continuous-role invisibility; this makes it visible without
  forcing the roles to be continuous).
- [[SOUL-F014]] — partial (observability half of expansion-activation gap; pairs with
  `/soul-council` which is the invocation half).

## Open residuals (named, not promised)

- `/soul-ask-body` spec — separate (F037).
- Counterweight discipline doctrine line — owned by [[SOUL-A012]] §Activation Disciplines.
- F018 event-standard adoption per project — not blocking; this instrument works on
  witness alone.
- Whether the F014 expansion-role-economics finding STILL holds today, after recent
  doctrine (the Mind, /soul-distill) — empirical test via Tier 3a above.

---

**Designed:** 2026-05-26 (Cluster 1 design beat).
**Adopted:** pending Body review.
**Built:** TBD.

**Source:** Designed alongside /soul-council in the Cluster 1 design beat (Cartographer
cluster pass surfaced the family; Body authorized the suite, /soul-council first, then
this). Anchored in [[SOUL-I031]] (raw idea); [[SOUL-F014]]'s ROLE ECONOMICS section (the
manual-count precedent); seed §The Council (canonical role list); SOUL-F018 (event
standard, optional data source).
