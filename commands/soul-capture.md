---
description: Capture to the record in one of three modes — idea (frictionless, forward), witness (light scaffold, backward), finding (earned scaffolder). The mode token is the first arg and selects friction + target store + format. Merges the former /soul-idea, /soul-witness, /soul-finding into one command; the ratchet is preserved by mode. Use to jot a forward possibility, log an observation, or scaffold a graduation the Body has decided.
---

# /soul-capture — capture to the record

`/soul-capture <mode> [text]` where **mode** is `idea`, `witness`, or `finding`.
The mode selects three things at once: **friction**, **target store**, and **format**.
The token *is* the capture ratchet made visible — typing `finding` is the deliberate
earning act. If no mode is given, **ask** ("idea / witness / finding?") — do not guess
the store.

---

## Mode `idea` — frictionless, forward (→ `ideas.md`)

Near-zero ceremony. Append the Body's forward-looking possibility to `ideas.md` with a
fresh `SOUL-I###` (scan for the highest, increment). Minimal at capture; enrich later.
Jot it, confirm the ID, done. No interview, no scaffolding beyond the ID + a one-line
title. Ideas are cheap by design (Rule 7).

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

## Mode `finding` — earned scaffolder (→ `findings/open/`)

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
the I027 re-read-verify protocol. **Adopted:** 2026-06-08. **Status:** active.
