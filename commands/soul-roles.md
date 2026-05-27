---
description: Read-only observability — surfaces which Council roles have actually fired in the project (witness TYPE + findings FILED BY + optional .soul/events.jsonl) and which have gone silent. Body-invoked only; never auto-fires; never changes state. Use when the Body wants a legible picture of role activity vs idleness, or wants to test whether a role assumed-active is actually firing.
---

# /soul-roles — observe which roles have fired

A Body-invoked, read-only instrument that aggregates role-firing evidence from
the existing record (witness.md TYPE fields, findings FILED BY, optional
`.soul/events.jsonl`) into a legible picture. A Steward silent for weeks looks
identical to a Steward satisfied with current state — until this command makes
the distinction visible.

The observability half of the SOUL-F014 expansion-gap response: contraction
roles fire by default; expansion roles need Body invocation. `/soul-council`
is the invocation half (the Body summons the chamber); `/soul-roles` is this
half (the Body sees who has actually been speaking). Sibling commands,
different jobs.

## What this is NOT

- **Not auto-firing.** Body-invoked, like `/soul-council`. No hook fires this.
- **Not a productivity dashboard.** Counts are descriptive, not prescriptive.
  "Researcher fired 0 times" is observational — it may be correct that no
  outward research was warranted. The Body reads the picture.
- **Not a write instrument.** Never modifies witness, findings, ideas, or
  amendments. Queries log to `.soul/role-queries.jsonl` only.
- **Not a substitute for the witness log.** TYPE fields in `witness.md` are
  the source of truth; this command READS them, it does not replace them.
- **Not a back-fill tool.** Entries without TYPE are invisible to the count.
  The instrument is as good as the data and says so explicitly.

## What to do

1. **Parse arguments** (all optional):
   - `<window>` — `all` (default), `recent` (last 20 witness entries),
     `since YYYY-MM-DD`, or `last <N>`.
   - `--role <name>` — focus tally on one canonical role; others omitted.
   - `--silent-threshold <N>` — count a role "silent" if no invocation in N
     entries (default **70**, ≈ 1 week at the measured 2026-05-26 rhythm of
     ~10 entries/day; tune from dogfood). Lower defaults flag normal
     between-session silence as silence — too coarse for this rhythm.
   - `--full` — include the unselected Magistrates explicitly even when
     count is zero (default output already lists all canonical roles; this
     flag is reserved for future extension and is currently a no-op).

2. **Read data sources, in order:**
   - `witness.md` — parse TYPE fields per entry. Roles within an entry may be
     `;`-separated or listed across lines; normalize both. One witness entry
     = one occurrence per distinct role named.
   - `findings/open/*.md` and `findings/closed/*.md` — parse FILED BY fields.
     Findings are deliberate role attributions; richer signal per entry.
   - `.soul/events.jsonl` if present (per SOUL-F018 event standard) — use
     role tags. If absent, skip silently; no build dependency.

3. **Canonicalize role names** against the canonical 13 from seed §The
   Council + Hands:
   - **Magistrates (8):** Archaeologist, Seer, Archivist, Prophet, Revelator,
     Researcher, Steward, Emissary.
   - **Tribunes (3):** Skeptic, Accountant, Advocate.
   - **Censors (2):** Guardian, Cartographer.
   - **Hands (3):** Architect, Craftsman, Artificer. *Tag separately* — they
     produce under the Body, answerable to the Council but not OF it.
   - Variants normalised at parse time. Unrecognised role names surfaced in
     a separate `Unrecognised:` line in output, never silently dropped.

4. **Tally per role within the window:**
   - Total invocations (sum across witness + findings + events).
   - Most recent invocation (witness ID + date if available).
   - Longest silent gap (max entries between consecutive invocations).
   - First invocation in the window.

5. **Classify roles:**
   - **Silent** — zero invocations in the window, OR no invocation in last
     `--silent-threshold` entries.
   - **Active** — invocations within threshold.
   - **Hot** — top 3 by invocation count. Output is neutral on whether hot
     is over-firing or load-bearing; that read is the Body's.

6. **Render output** — table + summary, neutral language:
   - **Council table** (Magistrates + Tribunes + Censors):
     `role | count | most-recent | longest-silent-gap | classification`.
   - **Hands table** (separate): `Architect | Craftsman | Artificer` with
     the same columns. Never conflated with Council.
   - **Summary lines:** `Silent: <roles>.` `Hot: <roles>.`
   - **Data quality line (mandatory):** `M of N entries missing TYPE field;
     results inferred from N-M.` Never omit this; silent-rate must always
     be qualified.
   - **Unrecognised line (if any):** `Unrecognised role names: X, Y.`

7. **Log the query — split by purpose** (per spec D4 / SOUL-F018 alignment):
   - **Append one JSONL line to `.soul/role-queries.jsonl`**:
     `{"ts": "<ISO>", "scope": "<window>", "silent": [...], "hot": [...],
     "data_quality": "M/N"}`. Cheap, append-only, doesn't pollute witness
     scannability.
   - **No witness entry by default.** The bare query is not record-worthy.
   - **Witness entry ONLY for acted-upon insights** — e.g., "Body ran
     `/soul-roles`, observed Researcher zero-fire across 30 entries,
     decided to invoke `/soul-council` on outward reach." The DECISION
     is record-worthy; if the Body acts on the observation, that goes in
     the witness via `/soul-witness` separately.

8. **Surface the picture, do not interpret it.** The output reports what the
   record shows; the Body reads what it means. If a role is silent, do not
   recommend invoking it — that is the Body's call (and possibly a
   `/soul-council` moment).

## Output example (illustrative, not contractual)

```
/soul-roles last 30

ROLE-FIRING SUMMARY (last 30 witness entries, 2026-04-26 to 2026-05-26)

Council (Magistrates + Tribunes + Censors)
Role              Count  Last seen  Longest gap  Status
Skeptic              18  SOUL-076   2            Hot
Architect*           —   —          —            (see Hands)
Emissary             12  SOUL-076   3            Active
Steward               7  SOUL-068   8            Active
Prophet               2  SOUL-064   18           Silent (>70 entries)
Revelator             1  SOUL-053   29           Silent
Researcher            0  —          30           Silent (zero)
Guardian              9  SOUL-080   2            Active
Cartographer          6  SOUL-078   4            Active
...

Hands (build-side; not OF the Council)
Role              Count  Last seen  Longest gap  Status
Architect            14  SOUL-077   1            Hot
Artificer             4  SOUL-083   5            Active
Craftsman             0  —          30           Silent (zero)

Silent: Researcher, Revelator, Prophet, Craftsman.
Hot: Skeptic, Architect, Emissary.
Data quality: 4 of 30 entries missing TYPE field; results from N=26.
```

## Failure-mode guards

| Failure | Guard |
|---|---|
| **Pejorative reading** — "Researcher is broken" | Output language is neutral. "Silent" means observed-not-firing in the window, NOT judgement that the role is failing. The Body reads the picture. |
| **Data-quality blindness** — TYPE field missing on some entries | Every output names data quality on a mandatory line: `M of N entries missing TYPE; results from N-M.` Silent rate is always qualified. |
| **Role-name canonicalisation drift** — entries spell roles differently | Canonical 13 from seed §The Council + Hands. Variants normalised at parse time; unrecognised names surfaced in a separate `Unrecognised:` line — never silently dropped. |
| **Misuse as a productivity dashboard** — "we need more Researcher invocations" | Output is descriptive, not prescriptive. The right number of Researcher invocations depends on whether outward research was warranted, not on hitting a target. |
| **Scope creep into auto-fire** — "alert if Steward silent for 30 days" | NO. Read-only is the contract. Auto-firing observability is a `/soul-council` moment, not this instrument. |
| **Witness entry pollution** — every invocation creates a witness entry | Queries log to `.soul/role-queries.jsonl`, NOT witness.md. Witness entries are reserved for acted-upon insights and written via `/soul-witness` separately. |
| **Conflating Council and Hands** — Architect counted as a Magistrate | Hands rendered in a separate table. They produce; they do not deliberate. |
| **Self-report inflation** — agent prose says "as Steward..." but no TYPE-tagged record | TYPE fields and FILED BY are the anchors. Prose role-naming without a structural record does not count. F028 anchor-validity applied to role attribution. |

## What not to do

- Do not auto-fire. Body invokes; that is the contract.
- Do not modify witness, findings, ideas, or amendments. Read-only.
- Do not recommend invoking silent roles. Surface the observation; the Body
  decides.
- Do not silently drop unrecognised role names. List them.
- Do not omit the data-quality line. Silent rate without qualification is
  Coherent Falsehood (A010) on role activity.
- Do not collapse Hands into the Council table.
- Do not infer role activity from prose alone. Anchor to TYPE / FILED BY /
  events.

---

**Source:** Built by the Artificer for SOUL-I031 (the raw idea, "Council role
observability"); specced 2026-05-26 at
`docs/specs/2026-05-26-soul-roles-design.md` (Cluster 1 design beat); pairs
with `/soul-council` (invocation sibling) and SOUL-A012 §Activation
Disciplines (the doctrine line for the same activation problem on both
scope and knowledge axes). Dogfood precedent: SOUL-F014's ROLE ECONOMICS
section did this analysis manually across one project; this command
automates that empirical method. **Adopted:** 2026-05-26. **Status:**
active — MVP. Tier 3 validation: (a) reproduce F014's manual finding on
this repo, (b) cross-project test on a reference project, (c) does it
earn its place — event-anchored on project-internal clock: invocation
count over first ~50 witness entries since adoption <2× ⇒ ceremony,
retire or reduce scope. (Adopted at SOUL-084 per witness; threshold
fires around SOUL-134.)
