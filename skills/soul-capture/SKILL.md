---
name: soul-capture
description: Capture to the record in one of three modes — idea (frictionless, forward), witness (light scaffold, backward), finding (earned scaffolder). The mode token is the first arg and selects friction + target store + format. Use when the Body asks to capture, OR proactively when you spot an UNGUESSABLE mid-session — a fact, decision, or convention a later session could not re-derive (F044 triage) — in idea/witness mode only: draft the entry and hold for the Body's confirmation before appending. Never self-invoke finding mode; graduation is the Body's explicit call (A022).
---

# /soul-capture — capture to the record

`/soul-capture <mode> [text]` where **mode** is `idea`, `witness`, or `finding`.
The mode selects three things at once: **friction**, **target store**, and **format**.
The token *is* the capture ratchet made visible — typing `finding` is the deliberate
earning act. If no mode is given, **ask** ("idea / witness / finding?") — do not guess
the store.

**What earns capture (the measured triage rule, F044):** record the UNGUESSABLE — a
fact or arbitrary convention a later session cannot re-derive (those carried 0/30
drift at every model tier). The derivable regenerates on its own (the frontier
re-derives it 10/10) and only inflates the store. When in doubt: "could a fresh
session reason its way back to this?" No → capture. Yes → skip. And per contract
rule 2: capture what HAPPENED — never dramatize, never invent the incident a rule
"deserves" (SOUL-164).

## Who fires this (A022 — model-proposable, Body-confirmed)

The Body can invoke this at any time. The MODEL may also invoke it **proactively**
— the capture gap is the program's most universal failure (in every condition
tested, a mid-session finding died at the session boundary unless an instrument
caught it, SOUL-163/164) — under these limits:

- **Modes `idea` and `witness` only.** Never self-invoke `finding` — graduation
  is the Body's explicit, earned act (Rule 7 / I024).
- **The F044 triage rule is the trigger.** Propose only for the unguessable; do
  not propose for what a fresh session would re-derive.
- **Always hold for confirmation.** Model-initiated captures draft the entry and
  show it; nothing is appended until the Body says go. (Body-initiated `idea`
  keeps its near-zero ceremony; model-initiated `idea` shows the one-liner first.)
- The Body's "no" is final and costs nothing — proposals are cheap, vetoes cheaper.

## Where it writes (target — read this first)

The record is **this project's**, in the directory the session started in (do not
search upward). Two layouts are valid and you must detect, never assume:

1. **`.soul/witness.md` / `.soul/ideas.md`** — what `/soul-init` creates now.
2. **`witness.md` / `ideas.md` at the project root** — the older layout, still
   first-class. If these exist, they ARE the record: append there, and never
   create a second copy under `.soul/`.

If neither exists, create the `.soul/` form — a freshly `soul-init`'d or
hand-wired project may have no store yet, and its absence never means "write
elsewhere." **Never write the record into the Soul System source repo** (where the
imported contract and skills physically live) — that is the bug this rule
prevents. *Exception:* when the current project **is** the Soul System repo, that
repo's own record is the target.

---

## Mode `idea` — frictionless, forward (→ `ideas.md`)

Near-zero ceremony. Append the Body's forward-looking possibility to `ideas.md`
with a fresh id. Minimal at capture; enrich later. Jot it, confirm the ID, done.
No interview, no scaffolding beyond the ID + a one-line title. Ideas are cheap by
design (Rule 7).

**The id rule — three lines, and they are the whole format:**

- Form is `<PROJECTCODE>-I###`, where `<PROJECTCODE>` is the same code the
  project's witness log uses (`SENSA-001` → `SENSA-I001`). If the project has no
  code yet, ask for one — do not default to `SOUL-I`, which belongs to the Soul
  System's own ideas and collides the moment a project cites an upstream idea by
  number.
- Assigned **at capture**, never retrofitted. Scan for the highest existing id and
  increment.
- **Permanent handle**: a closed, resolved or struck-through entry keeps its id
  forever, ids are never reused, and nothing is ever renumbered.

Nothing else is specified. Heading-per-entry and bold-bullet-per-entry are both
fine — match whatever the file already does.

*Why only this much:* six adopting projects produced four id schemes and two
layouts. The layout variation cost nothing measurable; the id variation cost one
project a retrofit of 61 entries two months in, and left another reusing `SOUL-I`
because this skill used to name that prefix literally (2026-08-20 retrospective).
So the id gets a rule and the layout does not. Existing stores are grandfathered —
renaming ids across six projects would break permanent handles for no gain.

## Mode `witness` — light scaffold, backward (→ `witness.md`)

Hybrid capture: the Body types the observation; the command fills the standard fields and
shows the draft before appending.

1. Take the observation as typed (if none, ask one short question — do not interview
   field-by-field).
2. Next ID: scan `witness.md` for the highest `^ID: +[CODE]-\d+`, increment (project code
   from the log header, default `SOUL`).
3. **I027 protocol — re-read-verify before write.** Right before appending, re-scan to
   confirm the ID is still free (`witness.md` is the highest-collision record). If taken,
   increment and retry; if three re-scans keep colliding, **stop and tell the Body** — never
   silently clobber.
4. Scaffold the fenced entry (format per `operations/witness-log-format.md`):
   `ID / WHEN / WHERE / WHAT / TYPE / CONSEQUENCE / STATUS`. Preserve the Body's voice in
   WHAT; do not add interpretation or the word "should"; mark TYPE with `?` if uncertain.
5. **Show the draft before appending.** Body says go / edit / cancel. On go, append (with
   the I027 re-verify) and report the ID. Do not reorder existing entries.

## Mode `finding` — earned scaffolder (→ the Soul System's `findings/open/`)

**Findings are a Soul System store, not a project store.** `findings/` records
lessons about the *system* — its gates, instruments and doctrine — and is governed
by `operations/amendment-process.md` alongside `amendments/`, which `/soul-init`
has always (correctly) declined to scaffold locally. From 2026-08-20 init does not
scaffold `findings/` either. In a domain project, this mode's output goes to the
cursor's `OWED UPSTREAM` field, where a later mining pass collects it; it lands in
`findings/open/` only when the session is running in the Soul System repo itself.

*What made this explicit:* six adopting projects held zero findings between them
over three-plus months while the source repo accumulated 64, and three of them
carried permanently empty `findings/open/` + `findings/closed/` directories that
init had created. The store was never a project store; the scaffold said otherwise.

A finding is earned: the Body has decided this graduates. This mode does the **mechanical**
part (ID, format, placement, upstream reminder) — it does NOT graduate on its own.

1. **Confirm the graduation is the Body's call.** If the Body hasn't explicitly said "this
   is a finding," stop and ask. A finding without explicit graduation is the inflation
   failure mode this guards against (Rule 7 / I024).
2. **If writing from a reference project for upstreaming (the I014 obligation), run the
   Soul-meta boundary check:** *remove this project's domain entirely — is the lesson still a
   Soul System lesson?* If no, it stays home (project-paradigm content); only Soul-meta
   content (gates, instruments, roles, doctrine) goes upstream.
3. Gather: **WHAT** (2–6 sentences, what is / what should be), **WITNESS IDS** (≥1),
   **WHY NOT YET AMENDMENT**, **RELATED** (`[[SOUL-F###]]`/`[[SOUL-I###]]`), **FILED BY**
   (role(s)).
4. Next ID: scan **both** `findings/open/` AND `findings/closed/` for the highest
   `SOUL-F###`, increment.
5. **I027 re-read-verify before write** (live collision evidence: SOUL-064 on F030). Same
   stop-don't-clobber rule as witness mode.
6. Write `findings/open/SOUL-F###-<kebab-slug>.md` with the standard fenced format:
   `FINDING ID / DATE / WITNESS IDS / WHAT / WHY NOT YET AMENDMENT / FILED BY / RELATED /
   STATUS: Open`.
7. **Upstream reminder (I014):** if cwd is a reference project AND the finding is Soul-meta,
   remind the Body the closing-Finding obligation may require harvesting it upstream into the
   Soul System repo's `findings/`. Flag — don't auto-upstream.
8. Report the path + ID + (if applicable) the upstream reminder. **Do not commit.**

---

## What not to do

- Do not guess the mode — ask if it's omitted.
- Do not graduate witness entries to findings unilaterally — that's the Body's call.
- Do not skip the I027 re-read-verify in witness/finding modes — silent ID-clobber is
  forbidden (Invariant). Idea mode also takes a fresh ID but is lower-collision.
- Do not insert "should" or interpretation into a witness WHAT.
- Do not write to `findings/closed/` (closing is a separate deliberate act). Do not commit —
  the Body owns the commit moment.

---

**Source:** Merged at the Cut (→1.0) from `/soul-idea` (SOUL-I-inbox), `/soul-witness`
(SOUL-I029), `/soul-finding` (SOUL-I024) into one mode-dispatched command. The friction
differential (Mind contrast case; I024) is preserved by mode, not by command count. Carries
the I027 re-read-verify protocol. Model-proposable for idea/witness since
SOUL-A022 (2026-06-12; the Body's v2.0 review — "not clear WHEN").
**Adopted:** 2026-06-08. **Status:** active.
