---
description: Scaffold a graduated finding into findings/open/ — the formatting wrapper for a graduation the Body has decided. NOT a frictionless inbox; findings stay earned. Use when a witness pattern has matured enough that the Body says "this is a finding" — this command handles the mechanical work (ID, format, placement, upstream-route reminder).
---

# /soul-finding — scaffold a graduated finding

A finding is the system's named gap or pattern — earned from witness entries when
something is durable enough to demand a name. This command does the **mechanical**
part of that graduation: assign the next `SOUL-F###`, apply the standard format,
place in `findings/open/`, remind about upstream routing for reference projects.

It does NOT graduate witness entries on its own. The Body decides; this scaffolds.

## What this is NOT

- **Not a frictionless finding inbox.** That risks finding-inflation (SOUL-I024) —
  cheapening the witness→finding graduation that makes a finding *mean* something.
  The cheap-capture twin of `/soul-idea` is `/soul-witness` (deferred, not built);
  `/soul-finding` is a **scaffolder / router**, not an inbox.
- **Not for closed findings.** Closed findings live in `findings/closed/` and are
  moved there by the commit that resolves them.

## What to do

1. **Confirm the graduation is the Body's call.** If the Body has not explicitly
   said "make this a finding," stop and ask. A finding without explicit
   graduation is the inflation failure mode this command exists to prevent.

   **If this finding is being written from a reference project for upstreaming to
   the Soul System repo (the I014 obligation), also run the Soul-meta boundary
   check:** *if you removed this project's domain entirely, would the lesson still
   be a Soul System lesson?* If no, the finding belongs in the project's own
   record, not upstream. Project-paradigm content (which library, which physics
   model, which pattern fits this domain) stays at home; Soul-meta content (gates,
   instruments, roles, ceremony, doctrine) goes upstream. The seed §Reference
   Projects carries the rule; this step is its instrument-level enforcement.

2. **Gather the inputs** (Body-supplied or asked, one at a time only if missing):
   - **WHAT** — the pattern / observation / gap, in 2–6 sentences. State what is
     and what should be.
   - **WITNESS IDS** — the entries that anchor this (SOUL-NNN). Minimum one;
     more if the pattern recurs.
   - **WHY NOT YET AMENDMENT** — why this is a finding, not doctrine. What
     would have to be true (or how many data points) for it to graduate again?
   - **RELATED** — `[[SOUL-F###]]` / `[[SOUL-I###]]` linkbacks.
   - **FILED BY** — the Council role(s) that surfaced it (Archivist, Emissary,
     Skeptic, …).

3. **Determine the next ID** — scan **both** `findings/open/` AND `findings/closed/`
   for the highest `SOUL-F###`, increment by one.

4. **I027 protocol — re-read-verify before write.** Right before writing the file,
   **re-scan both directories** to confirm your assigned ID is still free. A
   concurrent session can claim an ID between step 3 and now (live evidence:
   SOUL-064 collision on F030). If your ID is taken, increment and try again. If
   you re-scan three times and keep colliding, **stop and tell the Body** — do not
   silently clobber. Scope: this is single-filesystem; cross-machine concurrency
   still needs git arbitration (out of scope here).

5. **Write `findings/open/SOUL-F###-<slug>.md`** with the standard format. Use a
   short `kebab-case-slug` derived from the WHAT.

   ```
   ```
   FINDING ID:      SOUL-F###
   DATE:            YYYY-MM-DD
   WITNESS IDS:     SOUL-NNN[, SOUL-MMM]
   WHAT:            <2–6 sentences>
   WHY NOT YET AMENDMENT:  <what's missing to graduate to an amendment>
   FILED BY:        <role(s)>
   RELATED:         [[SOUL-F###]], [[SOUL-I###]]
   STATUS:          Open
   ```
   ```

   Wrap the block in a fenced code block (` ``` `) so it renders as the existing
   findings do.

6. **Reference-project upstream reminder (SOUL-I014).** If the current working
   directory is a reference project (its `CLAUDE.md` imports the Soul seed) AND
   the finding is **Soul-meta** (about how the Soul System itself behaves, not
   about the project's own domain), remind the Body that the closing-Finding
   obligation may require harvesting this upstream into the Soul System repo's
   `findings/`. Don't auto-upstream — flag.

7. **Report** the file path, the assigned ID, and (if applicable) the upstream
   reminder. Do not commit.

## What not to do

- **Do not graduate witness entries unilaterally.** That's the Body's call.
- **Do not write to `findings/closed/`.** Closing is a separate, deliberate act
  (move + status-line edit + commit).
- **Do not skip the re-read-verify step (I027).** Silent ID-clobber is the
  failure mode this protocol exists to prevent.
- **Do not commit.** The Body owns the commit moment.
- **Do not re-format existing findings** when scanning. Read-only on the existing
  record.

---

**Source:** Built by the Artificer for SOUL-I024 (the scaffolder-not-inbox shape
the idea's NOTES converged on, after the /soul-skill grill surfaced the
project-vs-soul-meta routing question shared with SOUL-I023). Includes the
SOUL-I027 detect-only concurrency protocol from the same session. **Adopted:**
2026-05-26. **Status:** active — MVP. Cross-machine concurrency (option 2 of
I027, git-as-arbiter) deferred; `/soul-witness` cheap-capture twin deferred.
