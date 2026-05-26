---
description: Append a structured observation to witness.md with near-zero ceremony. Hybrid capture — Body types raw text, the command scaffolds the standard fields (ID/WHEN/WHERE/WHAT/TYPE/CONSEQUENCE/STATUS) and shows the draft before writing. The cheap-capture twin of /soul-idea, pointed at the BACKWARD record.
---

# /soul-witness — capture an observation

Append a new entry to `witness.md` at the project root. The Body provides the
observation in their own words; the command fills the structured fields
(format per `operations/witness-log-format.md`) and shows the draft before
appending. Frictionless input, scaffolded output.

The witness is the system's eyes — capture friction is exactly what discourages
in-the-moment observation, the moments most worth catching. This command
removes that friction without losing the structured fields that downstream
tooling (witness→finding graduation, role tagging, search) relies on.

## What this is NOT

- **Not a finding.** Findings graduate from witness entries when earned
  (`/soul-finding`). The witness is the raw record; the finding is the named
  pattern. Cheap capture here preserves the friction differential.
- **Not an idea.** Ideas are forward (`ideas.md`, `/soul-idea`); the witness is
  backward (what happened).
- **Not for opinion or recommendation.** Per `operations/witness-log-format.md`:
  *"If an entry contains the word 'should' the Witness has stopped witnessing."*
  The observation goes here; the response goes to the Council.

## What to do

1. **Take the observation as the Body types it.** If invoked with no argument,
   prompt for the observation in one short question — do not interview field-
   by-field (that's the `/soul-finding` shape, not this one).

2. **Determine the next witness ID** — scan `witness.md` for the highest
   `^ID: +[CODE]-\d+` entry and increment by one. Project code from the witness
   log header (default to the project's witness-log code, e.g. `SOUL`).

3. **I027 protocol — re-read-verify before write.** Right before appending,
   re-scan `witness.md` to confirm your assigned ID is still free. `witness.md`
   is the **highest-collision record** in the project (every session writes to
   it). If your ID is taken, increment and retry. If three re-scans keep
   colliding, stop and tell the Body — do not silently clobber. Scope: single-
   filesystem; cross-machine concurrency still needs git arbitration.

4. **Scaffold the entry from the observation.** Fill the standard fields:

   ```
   ID:           [CODE]-NNN
   WHEN:         [today's date, YYYY-MM-DD] / [brief phase if obvious from context]
   WHERE:        [the location in the work — infer from current conversation
                 context: file path, command, doc section, conversation phase.
                 If genuinely unclear, write "conversation context" and let the
                 Body correct.]
   WHAT:         [the Body's observation, lightly tightened to remove filler.
                 PRESERVE the Body's voice and phrasing. Do not add
                 interpretation. Do not insert "should." Two-to-five sentences
                 is the target; honor the format spec's terseness norm but do
                 not force-cut if the Body provided more.]
   TYPE:         [agent's best classification from the valid types below; mark
                 with `?` if uncertain so the Body can correct on review.
                 Valid types from operations/witness-log-format.md:
                   - Failure Mode        — name the specific mode if known
                   - Obligation Skipped  — name which obligation
                   - Felt Wrong          — unresolved, noticed but not named
                   - Unnamed Tension     — two forces in conflict
                   - Universe Contradiction — assumption met reality and lost
                   - Multiverse Signal   — evidence the assumed Universe is wrong
                   - Council Note        — observation for a specific Council role]
   CONSEQUENCE:  [one line if obvious from the observation; otherwise
                 "unresolved" — the Body can fill on review or in a later edit.
                 Do NOT speculate on cost.]
   STATUS:       Open
   ```

   Wrap the block in a fenced code block (` ``` `) so it renders like the
   existing witness entries.

5. **Show the draft to the Body BEFORE appending.** One compact display: the
   filled entry as it will be written. The Body says **go / edit / cancel**:
   - **go** → append to `witness.md` (with the I027 re-verify step 3) and
     report the assigned ID.
   - **edit `<field> = <value>`** → update the named field(s) and re-show, OR
     accept free-form edits if the Body rewrites the block directly.
   - **cancel** → discard; do not append.

6. **Append on go.** Add a blank line + the fenced block at the end of
   `witness.md`. Do not reorder or edit existing entries.

7. **Report the ID assigned and confirm capture.** One short line:
   `Captured as SOUL-NNN. <one-phrase recap>.`

## What not to do

- Do not interview field-by-field. Hybrid capture means the agent fills,
  Body confirms — not Body answers seven prompts.
- Do not insert interpretation, recommendation, or the word "should" into
  WHAT. Per the format spec, that has the Witness speaking for the Council.
- Do not create a finding from this. If the observation is graduation-worthy,
  the Body says so explicitly afterward and runs `/soul-finding`.
- Do not silently clobber on ID collision — the I027 protocol is mandatory
  here precisely because witness.md is the highest-collision record.
- Do not enforce a 5-line cap. The format spec names terseness as a norm;
  recent practice has carried richer entries. Capture what the Body provided.

---

**Source:** Built by the Artificer for SOUL-I029 — the cheap-capture twin of
`/soul-idea` for the backward record. Shape decided by Body: hybrid (frictionless
input + scaffolded output). Adopts the SOUL-I027 re-read-verify protocol from
day one (witness.md is the highest-collision record). Pattern mirrors
`/soul-finding` scaffolder but with lower ceremony — the Body's framing
"I am observing some XYZ" is the input, not a field-by-field interview.
**Adopted:** 2026-05-26. **Status:** active.
