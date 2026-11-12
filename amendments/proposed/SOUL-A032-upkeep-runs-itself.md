AMENDMENT ID:    SOUL-A032 (PROPOSED — not accepted; drafted 2026-11-12 for the Body)
DATE:            2026-11-12
WITNESS IDS:     SOUL-235 (mining pass 4: MODEL-LIB's upstream note 2026-11-11, the
                 problem and the Body's words there); SOUL-118 (the one recorded case
                 where the Body's review of a Mind change caught a wrong cut). Source
                 idea: SOUL-I089, DISCUSSED round 1 (2026-11-12), which holds the
                 Body's answers in full.

## In one paragraph

Today the handoff cursor and the Mind are refreshed only when the Body asks
(`/soul-handoff`, `/soul-distill`), and `/soul-next` only reminds. The Body: "i get
reminders buti have to continueal stop and do it or we have long running sessions
that may need update througout … i rarlely if ever do anything but accept the
mind/handoffs as created". This amendment lets both run on their own and tell the
Body afterwards, with a no that undoes them, as A031 did for captures. The Mind keeps
one brake, at the Body's request ("there could be some severity on the mind changes
that could help avoid major oopsies"): a change is graded by how much it could
break, and only the low grade applies on its own.

## WHAT CHANGES

### (b) The handoff cursor refreshes itself

1. **When.** The session runs `/soul-handoff` itself — not the Body — when the
   cursor is stale: (i) at the first turn after a context summary, and (ii) at the
   end of a turn when K or more commits have landed in the project since the cursor
   was last written, or a decision the cursor names as open was closed this session
   (the measure is open question 2: commit counts vary too much between agents). Counted in events, never wall-clock time (the WSL clock can
   pause; the Body's global rule).
2. **How it is triggered.** Soul's existing Stop hook gains a staleness test; when
   it is true it returns `decision: "block"` with a reason ("the cursor is N commits
   stale — refresh it with /soul-handoff, then stop"), once per staleness (the hook's
   `stop_hook_active` flag prevents a loop). A SessionStart hook with the `compact`
   matcher adds one line of context: "a summary just happened — refresh the cursor
   first" (rule 6's re-read stays). Behaviour documented in code.claude.com/docs/en/
   hooks, fetched 2026-11-12; not yet run here.
3. **What the Body sees.** One line: "cursor refreshed (N commits since the last)".
   A vault-linked cursor is committed with `vault.py sync` as now.
4. **Unchanged.** The cursor's format and the flush step; the run-before-a-long-
   unattended-run step (hooks may not fire under `claude -p`); the Body can still run
   `/soul-handoff` with a focus argument at any time.

### (a) The Mind refreshes itself, graded by severity

1. **When.** At the growth signal `/soul-distill` already uses (about 15+ new witness
   entries since the Last-distilled stamp, or a finding closed or an amendment
   accepted), checked when the cursor refreshes. Not more than once per session.
2. **Grading.** Every change in the draft is graded:
   - **Minor — applied on its own:** a new item; new evidence or a new incident added
     to an item; a citation fixed; a rewording that keeps the item's rule, numbers and
     incident; wrapping and spacing.
   - **Major — held for the Body:** cutting an item or part of one; changing what an
     item tells a session to do (a rule reversed or loosened, a number changed);
     dropping an incident or record id from an item (an item without its incident gets
     reinterpreted — F053/A020); merging two items; any change to an item the Body
     wrote or marked as theirs; the Mind growing past its line cap.
3. **A mechanical brake, not only the model's grade.** A script compares old and new
   `mind.md` before anything is applied: the item count must not fall, and every
   record id (`SOUL-118`, `F063`, `A022` …) cited in the old Mind must still be cited
   in the new one. If either check fails, the whole change is treated as major,
   whatever the model graded it. (The model's grade can be wrong in the flattering
   direction — mind item 2; the script cannot be talked round.)
4. **Applying.** Minor changes are committed on their own ("mind: auto-distill
   (minor) — …"), and the Body gets one line: "Mind refreshed: <what changed> — say no
   to undo (`git revert <sha>`)". Major changes are drafted into `.ai/distill/` and the
   Body gets one line naming them; nothing major is applied until the Body says yes.
   With both present, the minor ones apply and the major ones wait.
5. **Unchanged.** The Body can run `/soul-distill` at any time; the slim-Mind rules
   (A021) and the anchor rule (every item cites its record) still decide what a draft
   may contain.

## WHERE IN SOUL

- Contract `operations/CLAUDE.md`, the **Stores** paragraph. Now: "Upkeep:
  `/soul-distill`, proposed when the record has grown; the owner confirms."
  Proposed: "Upkeep: `/soul-distill` runs itself when the record has grown; it
  applies minor changes and tells the owner, and holds a cut or a changed rule for the
  owner's yes." The Body saw this exact sentence and answered "accept" (2026-11-12).
- Contract rule 6: unchanged in substance ("write the cursor with /soul-handoff, not
  by hand" still holds; the session now runs it unasked when stale).
- `skills/soul-distill/SKILL.md`: the "Do not run without the Body's yes … Never
  schedule or hook this" and "Do not auto-commit" rules are replaced by the grading
  above; the description changes to match.
- `skills/soul-handoff/SKILL.md`: a "when it runs itself" paragraph.
- `skills/soul-next/SKILL.md`: the "consider re-distilling" item becomes a report of
  what ran, or of major changes waiting.
- `hooks/pre-completion-verify.py` (the Stop hook) or a new hook; `hooks/hooks.json`
  (a SessionStart `compact` entry); a new `tools/mind-guard.py` (the mechanical
  brake) with tests.
- `operations/contract-reasons.md`, `docs/using-the-soul.md`, `operations/codex.md`
  (Codex hooks differ — to be read before building).

## QUESTION ONE — Evidence

MODEL-LIB (SOUL-235's note): `/soul-next` said "distill due" two days running and
nothing ran; meanwhile one Mind item stopped holding and a duplicate idea went
unnoticed; the cursor stayed a day stale through a full day of work and a compaction.
The Body, there: "make that more autonomous like we did with witnesses … things to
investigate"; and here (SOUL-I089 DISCUSSED) that the cost is the stop itself and
that drafts are accepted as written. This repo: every distill since 2026-10-19 was
accepted as drafted (git log of mind.md). Against: SOUL-118, where the Body's
insistence on a test reversed a cut — the reason cuts stay held.

## QUESTION TWO — Necessity

A022 made distill model-proposable but Body-triggered, and A031 made captures
opt-out; nothing covers the upkeep step between them. The reminder exists and fails
in exactly the case it was built for (MODEL-LIB). Nothing refreshes a cursor during a
long session.

## QUESTION THREE — Coherence

- **Reverses A022 for distill** (the trigger is no longer human for minor changes);
  A022's own reason — an unchecked rewrite can drop a curated item — is kept by
  holding every major change and by the mechanical brake.
- **F063 / mind item 5** (a Stop hook that fired on every turn): the staleness test
  fires only when the cursor is stale, once, and a refresh resets it. A test must
  show it silent on a fresh cursor.
- **Rule 4** (a fix gets checked): the brake is a script, checked by its own tests.
- **What would make this wrong:** a change graded minor that in fact bends an item's
  meaning — a rewording the brake cannot see. Mitigated by the one-line notice, the
  one-command undo, and the first-trial plan below; not eliminated. No such incident
  is known; none is claimed.

## Open questions for the Body (before acceptance)

1. The contract sentence — the Body, 2026-11-12: "accept".
2. When the cursor counts as stale — the Body: "hard to say someagents/processes
   commit a lot and others not so much. is there something more robust to base off
   of?" Proposed instead of a commit count: the amount of new conversation since the
   cursor was last written, read from the session's own transcript (each turn records
   how large the working context is), with a fixed step (about 50,000 tokens) — plus
   always after a summary. It measures what a lost context would lose, the same for a
   session that commits often and one that never does. (Whether every host records
   the context size per turn is to be confirmed while building.) Awaiting the Body.
3. The opt-out — the Body: "ok, in soul-init? or elsewhere?" Proposed: one key in
   `.soul/init.md` (where `/soul-init` already keeps the owner's answers, one dated
   line per key, and the hooks can read it), asked once by `/soul-init`; a project
   with no answer gets the default (on), and the first notice says how to turn it
   off. Awaiting the Body.
4. First trial — the Body: "into release".

STATUS:          Proposed 2026-11-12. Not accepted; nothing built.
