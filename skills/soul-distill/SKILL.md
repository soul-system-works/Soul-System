---
name: soul-distill
description: Refresh the project's Mind — compress the accumulated record (witness + findings + ideas + amendments) into mind.md as the slim form (A021) — this project's unguessables only, the things a later session cannot re-derive. The Distiller's instrument. Use when the Body asks, OR run it unasked at the growth signal (~15+ new witness entries since the Last-distilled stamp, or a finding closed or an amendment accepted), checked when the handoff cursor refreshes, at most once a day. Grades every change — minor ones (a new item, new evidence, a fixed citation, a rewording that keeps the rule) are committed alone with a one-line notice and the undo; major ones (a cut, a changed rule, a dropped incident, a merge) wait in .ai/distill/ for the Body's yes, and tools/mind-guard.py is the brake (A032). With upkeep off in .soul/init.md, propose it and wait instead.
---

# /soul-distill — refresh the Mind

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

The project's accumulated record (witness, findings, ideas, amendments) has been
growing. This command compresses it into `mind.md` — a project-scoped, always-on
artifact holding this project's **unguessables** — the facts, traps and
conventions a later session cannot re-derive — distinct from the records that
store what happened and the contract that carries doctrine.

**The verdict this is built on (SOUL-I026 Tier 2):** the Mind is a *lens layer*,
not a replacement. It holds this PROJECT's generators — rules that produce its
recurring decisions — while **obligations** (specific commitments at specific
times) stay in the records. It does NOT hold *system* doctrine: rules that apply
to any Soul project live in the contract and arrive by import, and restating them
here pays the always-on cost twice (A021; step 3). The word "doctrine" used to
appear here unqualified, which read as a licence to carry exactly what A021
moved out.
Tier 2 evidence: Mind-only reasoning was ~41% cheaper than full-record on
doctrinal questions; arms disagreed on obligation-shaped questions exactly where
the residual lives.

**Runs itself, graded by severity (A032, 2026-11-12).** A022 let the model notice
the growth signal and propose; the Body's yes was the trigger. In MODEL-LIB
`/soul-next` said "distill due" two days running and nothing ran, and the Body
accepts drafts as written: "i rarlely if ever do anything but accept the
mind/handoffs as created". So it now runs at the growth signal and grades each
change (step 8): minor ones apply on their own and the Body is told in one line,
with the undo; major ones wait for the Body's yes. A022's own reason stays — an
unchecked rewrite can drop a curated item — so every cut and every changed rule
still waits, and a script (`tools/mind-guard.py`) checks what the model's grade
cannot. SOUL-118, where the Body's insistence on a test reversed a cut, is why cuts
stay held.

**The growth signal:** material record activity since the `Last distilled` stamp
in `mind.md` — as a guideline, ~15+ new witness entries, or any finding closure
or accepted amendment. Event-anchored, not calendar-anchored. No `mind.md` yet?
Then the signal is the first accumulation that would fill one (see /soul-init's
"the Mind is earned" note).

## What to do

1. **When it runs.**
   - **The Body asks:** run it now. Step 8's grading still applies; the Body is
     there, so show the held changes at once.
   - **By itself:** at the growth signal, checked when the handoff cursor refreshes
     (`/soul-handoff`, step 1c), at most once a calendar day — a session cannot see
     the one before it, so the date is the test. It already ran today if the `Last
     distilled` stamp is today, or `.ai/distill/` holds a `mind-held-<today>.md` or a
     `mind-declined-<today>.md`: skip it then. No question first; the notice comes
     after (step 8).
   - **A declined change is not proposed again** unless record entries written after
     the `mind-declined-<date>.md` that holds it bear on it. Read the declined files
     before drafting, and leave out what the Body already said no to — otherwise the
     next refresh re-proposes the same change every day.
   - **Upkeep off** — `.soul/init.md` holds `upkeep: off` (the owner's opt-out,
     asked once by `/soul-init`): never run it by itself. Propose instead — state the
     signal ("N witness entries and M finding closures since the last distill — want
     me to refresh the Mind?") and wait for the yes, as before A032.

2. **Read the project's record AND the existing Mind.** Pull from the project root:
   - `witness.md` (tail at minimum; full if recent distill is stale)
   - `ideas.md` (full)
   - `findings/open/` + `findings/closed/` and `amendments/accepted/` — **Soul
     System repo only.** Domain projects have neither (they are upstream stores);
     there, the record is witness + ideas. `upstream.md`, if the project has one,
     holds lessons about the Soul System — not this project's unguessables. Read it
     only to check nothing domain-specific was misfiled there; it is not distill input.
   - `mind.md` (the previous distill, if present — used for the growth check)
   - The seed (`operations/CLAUDE.md`) — to apply the renamed-seed guard

3. **Distill into the slim form: the unguessables only.** One numbered list of
   the things a later session *cannot re-derive* from the code, the record, or
   its own reasoning. No fixed section headings — the shape follows the content.

   **The bar for an entry (F044 triage):** ask "could a fresh session reason its
   way back to this?" No → carry it. Yes → leave it out; the derivable
   regenerates on its own and only inflates the always-on cost. Each entry cites
   at least one anchor (witness ID, finding, amendment, commit).

   What that usually leaves — as guidance, never as headings to fill:

   - **Generators.** Rules that *produce* decisions, not describe them.
     Phrase-test: "do Y when Z" / "prefer Y over Z because…" = keep; "X is
     true" = description, prune.
   - **The trap and its direction.** A calibration lean, a measurement that
     returns a plausible wrong number, a tool that fails silently on this
     platform. These are the highest-value entries in the form.
   - **Path-dependent facts that contradict a strong model prior** — "this
     endpoint has NO idempotency support"; "these tokens are SINGLE-USE".
     Carry the FORCE (the incident, the explicit negation), not just the
     proposition: the incident is the load-bearing part (SOUL-A018 / F045).
   - **Conventions that live nowhere else** — a branch discipline, a name that
     must stay redacted, a directory that must never be touched with a given
     tool.

   **Doctrine does NOT go here.** Rules that apply to any Soul project live in
   the contract (`operations/CLAUDE.md`) and arrive by import; restating them in
   `mind.md` pays the always-on cost twice. This is the A021 line: the always-on
   layer is one plain contract plus this project's unguessables, and nothing else.

   > **Why slim, and why this changed (2026-08-20).** A021 (2026-06-11) shrank
   > the Soul System's own Mind to this form on measured evidence: doctrine prose
   > above the core bought no quality difference across 62+20+27 scored
   > increments while costing ~6k always-on tokens per session, and F055 makes
   > unnecessary always-on text a *correctness* risk, not merely a cost. This
   > skill kept prescribing the older four-bucket schema (Rules / Tensions /
   > Invariants / Contrast cases / Residual), so five of five consumer projects
   > distilled into a form the source repo had abandoned — one of them to 239
   > lines and 20 KB of always-on text. The Body's call, 2026-08-20: slim is the
   > path everywhere; no test arm required. **Existing four-bucket Minds are not
   > migrated** — they convert naturally at their next distill, since a distill
   > rewrites `mind.md` whole.

4. **Run the four shrinkage-invariant checks.** Before producing the draft:

   - **Line budget — a target, not a gate** (SOUL-F066). Three bands, proposed by
     the session and accepted by the Body (SOUL-202, 2026-10-19):
     - **≈80 lines is the target, and reaching it is a review trigger:** re-justify
       every entry against the anchor and unguessability tests below — throw out
       or correct old rules, keep the most important.
     - **80–120 is acceptable.** Do not shave lines and do not merge entries; cut
       only whole entries that fail the tests, and report the count.
     - **Over 120:** present the weakest whole-entry cuts to the Body, who takes
       them or raises the cap out loud. When force and budget conflict, force
       wins; the cap is the Body's to move, not the session's.

     Why a target at all: the contract is ~75 lines and this repo's own Mind is
     ~69 (re-anchored 2026-08-20); the old pre-2.0 200/300 cap let a 239-line,
     20 KB project Mind pass unflagged; and unnecessary always-on text is a
     *correctness* cost, not merely a token cost (F055, step 5b). Why not a gate:
     the old "cut, do not request an exception" left the precedence unstated, and
     in PLANT-BOP the Body relaxed it on seeing the cut list. The Body's view, in
     paraphrase: the target is worth keeping because it forces a review — throw out
     or correct old rules, keep the most important — but the Body should not have to
     babysit it or talk a session out of saving three lines, and a hard limit the
     Body manages belongs only well past 80–100 lines.
   - **Anchor requirement.** Every entry cites at least one anchor. Anchorless
     = description = prune. An anchor that exists is not enough (mining pass 2,
     SOUL-202):
     - **Executable facts are re-checked.** An entry that names a command, a
       path, a flag or a selector is checked against the repo at distill time —
       one grep or one run. False → fix it or cut it (MODEL-TEST).
     - **A prohibition carries its falsifier.** An entry that FORBIDS re-trying
       something ("dead end", "never X") states what would overturn it: what was
       tried, and whether the cause was shown or inferred. Missing → flag it for
       the Body or prune it; in PLANT-BOP a distilled prohibition outlived its
       evidence. This is contract rule 3 applied to the Mind. The falsifier is
       evidence for the next distill, not an "unless" clause in the directive —
       the force-stripped guard (step 5) still applies.
   - **Unguessability test.** Every entry fails "could a fresh session reason
     its way back to this?" Anything that passes is derivable — cut it.
   - **Growth check — in both units.** If `mind.md` already exists, always report
     `lines a→b · items c→d`: in GAME-THERMAL lines shrank while items grew, so
     one unit hides the other. Growth in lines or items needs no sign-off when
     every new entry passes the anchor and unguessability tests; say what each new
     entry earns. Above the 120 cap the Body decides (the budget, above). This
     replaced default-deny growth (SOUL-202): with the budget a target, the tests
     decide, not the count.

5. **Run the seven failure-mode guards.** Refuse to produce a draft that fails any:

   - **Drift into summary.** Caught in step 4: the growth check makes growth
     visible in both units, and the unguessability test cuts the summary entries.
   - **Force-fit entry.** An entry that reads like a heading being filled
     rather than a trap being recorded. The slim form has no sections to fill;
     if an entry exists to round out a shape, cut it.
   - **Renamed contract.** Per-distill check: "what's in `mind.md` that's NOT
     in `operations/CLAUDE.md`?" If trivial → Mind is redundant → **Steward
     retires** (recommend deletion, do not deploy). Under the slim form this
     guard bites harder than it used to: doctrine restated locally is the
     single most common way a Mind grows.
   - **Renamed CLAUDE.md.** Boundary: CLAUDE.md is *authored* (what the project
     is, how agents work). Mind is *distilled* (rules the project discovered
     from its own record). Different sources. If the draft overlaps heavily
     with the project's CLAUDE.md, refine to focus on the distilled-from-record
     rules.
   - **Doctrine–obligation collapse.** Per candidate entry, ask "generator
     (produces decisions across contexts) or obligation (a specific commitment at
     a specific time)?" Only generators go in the Mind; obligations stay in the
     records. And per step 3, a generator that applies to ANY Soul project is
     contract doctrine, not a Mind entry — cut it.
   - **Force-stripped anti-prior fact** (SOUL-A018 / F045). When a candidate
     rule rests on an unguessable fact that CONTRADICTS a strong model prior,
     do not compress away the fact's FORCE. Keep the incident and the explicit
     negation in the distilled entry, or leave the fact in the un-distilled
     records — never reduce it to the bare directive. The residual directive
     must be **imperative and loophole-free**: a clause like "unless / except /
     when appropriate" is exactly the opening a frontier model fabricates a
     false reconciling fact through (an invented idempotency key; an invented
     token TTL — each a Coherent Falsehood, A010). It must also be explicit
     enough to survive a terse reading, because a weak reader reverts to the
     prior whenever the rule is loose. Two levers, two tiers: directive-FORM
     gates the frontier (SOUL-129); prior-strength + terseness gates the weak
     model (SOUL-128).
   - **Stale.** Project-internal clock — staleness is event-anchored, not
     calendar-anchored. If material activity has accumulated since the `Last
     distilled` stamp (dozens of new witness entries, multiple finding closures,
     accepted amendments, doctrine edits), the refresh is overdue but legitimate
     — proceed. If the project has been quiet by event-count regardless of
     calendar time, surface the Steward question: is the Mind still load-bearing
     or should it retire?

5b. **Apply the measured compression rules (2.0 — these are results, not style):**

   - **Dedicated-bullet salience beats coverage** (F055): a rule a weak model must
     act on gets its OWN bullet; folding it into a paragraph took activation
     5/5 → 1/5 on identical content. Bloat also splits quoting from obeying —
     a model can cite a rule it then violates; the budget is a correctness rule.
   - **Negation + executable fence is the surviving form** (SOUL-164,
     erosion-audit): "never X" at the site plus a test that fails if broken
     survives compression 30/30; prose rationale erodes. When a distilled entry
     can point at an executable fence, point at it.
   - **Imperative, loophole-free residuals** (SOUL-128/129): "unless / except /
     when appropriate" is the gap a frontier model walks through with an invented
     reconciling fact; terseness is the gap a weak model reverts through.
   - **Anti-prior facts are partly incompressible** (F045/A018): keep the
     incident and the explicit negation, or leave the fact un-distilled — and
     NEVER fabricate an incident to give a bare rule force (the fabrication
     axis, SOUL-164: that is the model's own failure mode, not a technique).

6. **Run the three diagnostic self-test questions** on the draft:

   1. **Load-bearing or renamed-contract?** Does this Mind generate decisions
      the contract alone wouldn't?
   2. **Unguessable-coherent?** A fresh agent reading the contract PLUS this
      Mind (no witness, no findings) — is it kept off the traps this project
      has already paid for? Ask about the traps, not about next-work: the slim
      form deliberately leaves doctrine in the contract and obligations in the
      records, so a Mind that could predict next-work on its own would be
      carrying material A021 moved out. Judged against the contract+Mind pair,
      never the Mind alone (SOUL-I055, closed 2026-08-20).
   3. **Anything carried that a fresh session would re-derive?** Every entry
      must fail the "could they reason back to this?" test. One that passes it
      is inflation — cut it.

   Record honest answers in the draft's commit message or the witness entry
   that follows. A failed self-test is not a draft failure; it is a flag for
   the Body to weigh during curation.

7. **Format the deployed `mind.md`.** Use this shape:

   ```
   # Project notes — <Project Name>

   [Header — two or three lines: the slim form (A021), only this project's
   unguessables; doctrine lives in the contract, obligations in the records.]

   ## Carry these (project-specific, not re-derivable)

   1. **<Short name for the trap or convention.>** The fact, its force, and
      the anchor that earned it.
   2. …

   ---
   **Last distilled:** YYYY-MM-DD against <witness tail / commit SHA>
   [+ one line naming what was compressed away to pay for anything new]
   ```

   Numbered items, not headings. If a project's Mind genuinely needs grouping,
   group it — but do not restore fixed section names, because empty sections
   invite force-fill, which is the failure the four-bucket form kept producing.

   **Keep the numbers stable.** The Mind's items are cited by number from
   outside it — code, registry docs, other records. On 2026-10-19 this repo's
   distill added two items (2 and 5) and cut one — 6 → 7 items, 69 → 76 lines
   (commit 9d1aa6d) — and a live registry doc's "mind 5(c)" silently pointed at
   the wrong item (SOUL-202); PLANT-BOP and NAV-TOOL reported the same defect.
   Prefer appending new items and keeping existing numbers over renumbering — a
   renumbering is a major change, because `tools/mind-guard.py` checks each item by
   its number (step 8). If a
   cut or reorder does renumber, search for citations of the old numbers ("mind
   N", "Mind #N", "item N", "rule N") with a plain `grep -rn` over the working
   tree — not `git grep`, which skips gitignored files, and the motivating hit was
   in a gitignored registry file. List each hit, with what it should now point at,
   in the draft's notes for the Body — never in the Mind text itself.

8. **Grade every change; apply the minor ones, hold the major ones (A032).**
   **Write the draft to `.ai/`, never in place** — e.g.
   `.ai/distill/mind-draft-<date>.md`. `mind.md` is imported, so a draft written
   into it is live next session whether or not anyone commits (NAV-TOOL,
   SOUL-202); only the minor changes reach `mind.md`, as below. **`.ai/` ignored first:**
   run `git check-ignore -q .ai/x`; if it is not ignored, add `.ai/` to
   `.git/info/exclude` (as `tools/dispatch.py` does) and say so in one line. In a
   public repo, write nothing there until it is ignored (mining pass 3, SOUL-234).

   - **Grade each change** against the prior `mind.md`. When unsure, it is major.
     - **Minor — applied on its own:** a new item; new evidence or a new incident
       added to an item; a citation fixed; a rewording that keeps the item's rule,
       numbers and incident; wrapping and spacing.
     - **Major — held for the Body:** cutting an item or part of one; changing what
       an item tells a session to do (a rule reversed or loosened, a number
       changed); dropping an incident or record id from an item (an item without
       its incident gets reinterpreted — F053/A020); merging two items; any change
       to an item the Body wrote or marked as theirs; the Mind growing past its line
       cap (step 4's 120, or the cap the Body set). A first Mind is major too: it
       adds an always-on file and an import line in the Body's `CLAUDE.md` (below).
   - **Run the brake before applying anything.** Write the minor-only version (the
     prior Mind plus the minor changes alone) to `.ai/distill/mind-minor-<date>.md`
     and run `python3 <root>/tools/mind-guard.py <mind path> .ai/distill/mind-minor-<date>.md`
     (`<root>` is two levels above this skill's base directory; `<mind path>` is the
     Mind's real path — `mind.md` or `.soul/mind.md`, wherever it lives). **Any exit
     but 0 makes every change major**, whatever the grade: apply nothing. Exit 1 is a
     failed check; exit 2 means it could not read a file — usually the wrong Mind
     path; fix the path and run it again. The script checks, item by item, that every
     old item number still exists and still cites every record id it cited (the
     `**Last distilled:**` stamp is not checked). It cannot see a rewording that
     bends a meaning, so the grade still matters.
   - **Apply the minor changes as their own commit.** Copy the prior Mind to
     `.ai/distill/mind-before-<date>.md`, copy the minor-only version over the Mind,
     then by where the Mind lives:
     - **Tracked in this repo:** `git commit -m "mind: auto-distill (minor) — <what
       changed>" -- <mind path>` — that path only, nothing else in the commit. Undo:
       `git revert <sha>`.
     - **In a vault** (`.soul` is a link): `python3 <root>/tools/vault.py sync . -m
       "mind: auto-distill (minor) — <what changed>"`. Sync commits this project's
       whole vault folder, so a revert could take other files with it; the undo is
       `cp .ai/distill/mind-before-<date>.md .soul/mind.md` and `vault.py sync .` again.
     - **Not in git** (an ignored record): nothing to commit; the undo is the same `cp`.

     Then one line to the Body: *"☀ Mind refreshed: <what changed> — say no to undo
     (`git revert <sha>`)"*, with the vault or untracked undo in its place (`☀ ` marks
     a line about something the Soul did on its own: `/soul-handoff` step 5; a distill
     the Body asked for carries no mark). The first
     such line in a project that has no `upkeep:` answer adds "to turn this off:
     /soul-init revisit upkeep".
   - **Hold the major changes.** Save the full draft as
     `.ai/distill/mind-held-<date>.md` — the name `/soul-next` looks for — and say one
     line to the Body: *"☀ Mind: N changes wait for your yes — <short names>, in
     .ai/distill/mind-held-<date>.md"*. Nothing major is applied until the Body says
     yes; on the yes, apply and commit it the same way, then delete the held file. On
     a no, leave the Mind as it is and rename the held file to
     `.ai/distill/mind-declined-<date>.md`, with one line at its top naming what was
     declined: step 1 reads it, so the same change is not proposed again. With both
     present, the minor ones apply and the major ones wait.

   **When the Body reviews the held changes** — at once when the Body ran this, or
   later on request — the review surface must make the *load-bearing question per
   entry* cheap to judge — the Body cannot weigh a draft buried in passing-check prose (the
   I037 pain). Apply the compact, gap-only discipline the completion gate
   already adopted (SOUL-055: "expand to the failing check only on a real gap;
   do not recite passing checks"):

   - **Show the delta, not the whole Mind.** Diff the draft against the prior
     `mind.md`. Present only **new (+)** and **changed (~)** entries;
     collapse unchanged ones to a count (`N unchanged items — expand on
     request`). First distill (no prior Mind) = everything is new;
     present in full.
   - **One load-bearing verdict per delta entry.** For each new/changed item:
     `what it prevents or generates · anchor · UNGUESSABLE? Y/N — could a fresh
     session reason its way back to this?` A "Y, they could" is a prune
     candidate — surface it for the Body to cut, do not hide it.
   - **Checks: run all, recite none.** Steps 4–6 (4 shrinkage checks, the guards,
     3 diagnostics) still run in full — that honesty is non-negotiable. But
     present them as **one status line each, expanded only on a flag**, e.g.
     `Shrinkage: clean (lines 69→76 · items 6→7) · Guards: clean · Diagnostics: 1 flag →
     <flagged question + honest answer>`. A passing check is not recited.
   - This governs the *review* only; the deployed `mind.md` format (step 7) is
     unchanged. The minor changes need no review; their one-line notice is enough.

   **A Mind nothing imports is not live.** Ask `init-status.py`, do not search for
   the line yourself: run `python3 <root>/tools/init-status.py status . --json` and
   read its `mind` item. It reads the `@` lines of `CLAUDE.md`, `.claude/CLAUDE.md`,
   `AGENTS.md` and `CLAUDE.local.md` (not imports nested inside them), resolves each
   relative to the file it sits in, and reports a `mind.md` nothing loads as a
   `repair` whose detail names the line and the file. It reads only a `mind.md` that
   exists, so for a first Mind run it again right after the file is written. When it
   reports that repair — for a first Mind, expect it; a first Mind is always held —
   the Body's yes covers two writes: `mind.md` and that import line, placed by `/soul-init`'s `mind` rule (right
   after the contract import, relative to the file it goes into, in `CLAUDE.local.md`
   when the wiring is there). Say so in the draft's one-line summary ("first Mind: the
   yes also adds `@.soul/mind.md` to CLAUDE.md"). Step 8 used to stop at the draft and
   the yes; CAPTURE-RIG's note was that a first Mind is not live until imported
   (upstream mining, 2026-11-12).

## Retirement (Steward / never-always-on)

- The Mind carries `Last distilled` so decay is visible.
- Review on **project-internal cadence** — whenever material activity has
  accumulated (significant new witness entries, finding closures, doctrine
  amendments). Event-anchored, not calendar-anchored: still load-bearing?
  still distinct from the seed + CLAUDE.md? reproduction-coherent on recent
  decisions? (Skills review on a different — Anthropic-driven — clock; the
  two cadences are decoupled.)
- A project that stabilizes its rules and stops needing redistills has *won*;
  its Mind goes static-and-good. A project where the Mind keeps drifting toward
  obligation-collapse retires the Mind cleanly (delete `mind.md`; remove
  the Mind's import line from CLAUDE.md — `@mind.md` or `@.soul/mind.md`,
  whichever the project uses; witness entry naming the retirement reason).

## What not to do

- **Do not apply a major change without the Body's yes.** Cuts, changed rules,
  dropped incidents, merges, the Body's own items and a first Mind wait as a draft
  (step 8). A failing `mind-guard.py` makes the whole change major. With
  `upkeep: off`, do not run by itself at all — propose and wait (step 1).
- **Do not put anything else in the Mind's commit.** In a repo, the minor commit
  holds the Mind only, so `git revert` touches nothing else. A vault-linked Mind is
  the exception: `vault.py sync` commits the project's whole vault folder, so its
  undo is the copy back from `mind-before-<date>.md` (step 8), never a revert.
- **Do not let the Mind grow unexamined.** Growth is allowed when every new entry
  passes the tests; report it in lines and items (the growth check, step 4).
- **Do not manufacture entries to fill a shape.** The slim form has no buckets to
  fill, so there is nothing to force-fit; honesty about what doesn't compress
  is part of the discipline (SOUL-I026 failure mode #2).
- **Do not duplicate the seed or CLAUDE.md.** If the Mind reads as a rename of
  either, retire it.
- **Do not capture obligations as rules.** Doctrine vs obligation is the
  load-bearing boundary (Tier 2 evidence).
- **Do not chase lines, and do not silently pass the cap.** ≈80 target (a review
  trigger), 80–120 acceptable with whole-entry cuts only, over 120 the Body's call
  — the same numbers step 4 states. This line said ≤200/≤300 until 2026-08-28: v2.1.1
  re-anchored the budget away from the retired pre-2.0 seed in one place and missed
  this one, so the skill offered two budgets and a session obeying this list passed a
  200-line Mind, the exact artifact A021's slim switch exists to prevent (found by
  fresh-context review while reviewing SOUL-F066, which is about the same budget and
  did not notice the second copy).
- **Do not merge entries to make the budget.** Cut whole entries instead. Merging is
  the folding SOUL-F055 measured at 5-of-5 → 1-of-5 activation, so the intuitive way
  to save lines is the one move known to switch the Mind off. SOUL-F066's other half,
  accepted by the Body 2026-10-19 (SOUL-202): when force and budget conflict, force
  wins — cut whole entries that fail the tests, or the Body raises the cap out loud.
- **Do not recite passing checks or re-show unchanged entries.** Present the
  delta + a load-bearing verdict per changed entry; surface only flagged
  checks — the SOUL-055 gap-only discipline applied to the Mind's review
  (step 8). Reciting clean checks is the I037 ceremony cost.

---

**Source:** Built by the Artificer + Architect from the SOUL-I026 brainstorm
(spec: `docs/specs/2026-05-26-the-mind-design.md`, plan:
`docs/plans/2026-05-26-the-mind-implementation.md`). Necessity established
before instrument: Tier 1 (hand-crafted candidate, 218 lines) + Tier 2 (held-out
A/B on `/soul-witness?`; Mind-only arm ~41% cheaper, arms disagreed on
direction — the disagreement is the evidence for the lens-layer architecture).
**Reinforced by:** Kolmogorov complexity / MDL (rules > descriptions),
constitutional-AI's rules-over-examples, SOUL-033 description budget,
the system-level amendment process (this is its project-level analog).
**Shapes:** the slim unguessables-only form (A021), the doctrine-vs-obligation
boundary, the draft-for-curation discipline. **Adopted:** 2026-05-26.
**Amended:** 2026-08-20 — schema switched from four-buckets-plus-residual to the
slim form, closing SOUL-I055; the four-bucket prescription had outlived A021 by
ten weeks and five of five consumer projects had followed it.
**Amended:** 2026-10-19 (mining pass 2, SOUL-202) — the budget becomes a target with
a Body-owned cap (F066); growth reported in lines and items; executable anchors
re-checked; renumbering and draft location.
**Amended:** 2026-11-12 (unreleased, SOUL-A032) — runs itself at the growth signal,
checked when the cursor refreshes; each change graded, minor ones committed alone with
a one-line notice and the undo, major ones held; `tools/mind-guard.py` the brake; the
`upkeep: off` opt-out.
**Status:** active — MVP; model-proposed on the growth signal from SOUL-A022
(2026-06-12; the manual-fire-only deferral discharged by the Body's v2.0 review);
runs itself, graded, from SOUL-A032 (2026-11-12).
`/soul-mind` viewer, cross-project synthesis, and reproduction-fidelity
automation remain deferred.
