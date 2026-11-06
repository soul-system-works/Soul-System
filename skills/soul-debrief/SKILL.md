---
name: soul-debrief
description: Catch the Body up after a long or unattended run — one page that leads with the conclusion, then explains each result (what was tried, what happened, what was learned, how sure, and what to look at), where the work stands, the best next move, what is worth trying, and what only the Body can decide. Numbers are re-read from the run's files, and the page gets one independent check before the Body is told it is ready. Owner-invoked.
disable-model-invocation: true
---

# /soul-debrief — catch the Body up on a run they did not watch

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

The session's bottom lines (rule 10) assume the reader watched the run. This skill
turns them into one page a returning Body can read, act on and keep. It explains
like `/soul-explain` and looks forward like `/soul-next`, from the run's evidence.

Arguments (optional): `<since>` (a date, commit, witness id, or "this session");
`<run>` (a short lowercase hyphenated slug, used in every file name below).

## Before writing: scope, sources, fact sheet

1. **Set the scope** — the first that exists: `<since>`; the last commit on the
   newest line of `.ai/debriefs/INDEX.md` (create it if missing); the commit before
   the Body's message that launched the run; the cursor's date (it may postdate the
   run's start if the run ended with `/soul-handoff`). None (a fresh clone): ask the
   Body for `<since>`; do not guess. State the scope as commit and time ranges. An
   empty scope from the first three gets one line and no page; from the cursor, ask.
2. **Gather the sources**, most trusted first: the files the run wrote (results,
   metrics, logs, images, the code at its commits); records added in scope (witness,
   ideas, plan changes, `git log <range>`); the decisions log at
   `.ai/runs/<date>-<run>-decisions.md` or the path the cursor names (only if
   neither exists, say the run kept none, and take its choices from records and
   commits, never from memory, rule 2); the `— Bottom line:` blocks still in
   context. Subagent reports are **leads, not sources**: re-read each number from
   its file. Never split one result; order by importance, not by time.
3. **Build a fact sheet before any prose.** One short script reads every number the
   page uses from its source file into `.ai/debriefs/<date>-<run>.facts.json`, each
   with its path; the page takes its numbers from there. A number only a summary or
   report gives appears labelled "reported, not re-checked" with who reported it, or
   not at all. Where the script differs from a bottom line or report, the page uses
   the script's value and says the earlier figure was wrong. If a durable record
   holds it too, correct it forward through `/soul-capture witness` (id scan,
   re-read, append), never by editing the old entry; step 13 names it. Output of
   helper scripts made for the page is a source too: read it, don't trust it.

## Writing the page

4. **Conclusion first:** the headline result, how sure, where it stands, the best
   next move, and your calls — the chat reply's content (step 13). Just under it,
   the scope line; then a contents list with links. About 1,500 words, plain
   register: gloss each project or Soul term on first use; no padding or stock AI
   phrasing (run the host's voice checker if it has one).
5. **If a debrief already exists**, a short section next says what changed since it:
   new results, the Body's decisions, corrections to its numbers. Apply the Body's
   feedback (the newest index line; any witness entry with a debrief preference) and
   say how in one line.
6. **Each item** opens with a one-line verdict; the method and full numbers go in a
   fold-out section. It says **what we tried, and why** (no recorded reason →
   "reason not recorded"; never reconstruct one, rule 2); **what happened** (from
   the fact sheet); **what we learned** (what it changes next time); **how sure** —
   checked by an instrument that did not make the claim (rule 4), reported, or
   unverified, said plainly in words, never by colour alone; **what to look at**.
7. **What to look at: the form that shows the result best.** Images are one form
   among several: a small table of key numbers; a chart of fact-sheet numbers; an
   image or before/after pair; a short clip; a diff or code excerpt; a log excerpt;
   an interactive view. Use an interactive view only when it answers what a static
   one cannot: many cases to browse (a filterable or sortable table), a step or
   parameter to scrub (a slider over saved frames or steps), or a toggle between two
   states. It reads saved outputs only. For every form:
   - **Pick by a stated rule, not by score** ("the middle test case of each group"),
     and put the rule in the caption. The best-looking example misleads.
   - **Look at (or run) every visual before captioning it**, at reduced size. Point
     out what looks wrong or surprising; it is often the most useful line.
   - **Cost cap:** reuse what the run wrote; at most one new visual per item. A
     read-only render or plot from saved outputs is fine; no re-runs or retraining.
8. **Standard viewing.** Each visual has a caption (what it shows, the selection
   rule), alt text if an image, and a click that opens it full size in a native
   `<dialog>` (no library), scrolling when larger than the screen, with the source
   file's path. Media ship as files, never inlined: on the artifact route as the
   artifact's own files, which the page loads by relative path; beside a local HTML
   page, in a folder. On the artifact route, never offer a plain link to a published
   file: in a new tab it reopens the page, not the file (first test, 2026-11-05).
   Show the original in the page's dialog instead. Follow the
   host's own design or data-visualisation guidance (Claude Code's artifact skills,
   for example) for layout, theme, charts and interaction.
9. **Where the work stands, and what next.**
   - **Where it stands** — point at the handoff cursor (`.soul/handoff.md`) and the
     `**Stage:` line in the project's CLAUDE.md, if any; don't rebuild them. Say
     what the run changed.
   - **Next steps** — grounded in the records as `/soul-next` does (not its tracker
     or distill steps); name the single best next move.
   - **Worth trying** — each names the result from this run that suggests it.
   - **Your call** (🙋) — if a read or read-only check would settle it, it is not the
     Body's call: say what you would check or do, let the Body pick the order, and
     do not run it here. Add each choice the run made on its own that the Body may
     want to reverse: an assumed value, a fix made after seeing results, a stop.

## Delivering

10. **Publish** privately where the host allows (an artifact starts private, so
    publishing before the check is fine); else write `.ai/debriefs/<date>-<run>.html`.
    Either way the page heading names project, date and run; the host's own title rule (a short name, for example) governs the tab title.
11. **One independent check, before the Body is told.** A fresh-context reviewer
    gets the page, the fact sheet and the source paths, not your conclusions. It
    checks for numbers that differ from the fact sheet or sources; claims with no
    source; claims stronger than their evidence; visuals that do not match their
    caption (it looks at, or runs, each itself); 🙋 items that are really yours. Fix
    real defects, re-check only those against the sources, publish once more, and
    stop (rule 4). Wording findings go on the index line's follow-up list.
12. **Record it.** Append to `.ai/debriefs/INDEX.md`: date, run, scope, last commit
    covered, page link, wording follow-ups; the Body's feedback is added later. A
    preference for every future debrief is also captured as a witness entry through
    `/soul-capture`, because `.ai/` does not survive a fresh clone.
13. **In chat:** three or four sentences (headline result, where it stands, best next
    move); the link (say if it needs sharing); if step 3 corrected a record, one
    line: *"Added <CODE>-NNN correcting <CODE>-MMM — say no to strike it."*; last,
    the bottom line (rule 10) with the 🙋 items. Nothing else (rule 9).

## What not to do

- Do **not** start the next step or re-run anything; the Body chooses.
- Do **not** retell the run in order, or repeat background the Body already knows.
- Do **not** put an unlabelled number from a summary on the page (step 3), or leave
  a visual for the Body to inspect when you can look at it yourself.
- Do **not** make a page for an empty scope; one line is enough (step 1).

## When to propose it

Owner-invoked. The session may suggest `/soul-debrief` once, in one line, and wait:
when the cursor says an unattended run was started and results exist since, or when
the Body returns in the same session after a run with more than one bottom-line
item. `/soul-handoff` asks a long unattended run to keep the decisions log.

---

**Source:** SOUL-I086 (discussed 2026-11-05): a slim version of a draft written in
CAPTURE-RIG and tried there once, after a long unattended run (2026-11-05). There
the fact sheet caught a wrong number that had also reached a ratified record, and
the trial notes record 15 findings from the independent check (a caption for
something the image did not show, overclaimed checks, questions not the owner's).
**Status:** experimental. The draft was tried once, on CAPTURE-RIG; this slim version
was first run on 2026-11-05, on the Sonnet half of SOUL-I083 round 2. The fact sheet
held every number; the independent check caught 6 real defects (one a misread
field, the rest overstated claims); links to published files failed and step 8 now
shows originals in the page.
