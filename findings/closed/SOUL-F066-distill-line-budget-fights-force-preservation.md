# SOUL-F066 — The Mind's line budget and the keep-the-incident rule pull opposite ways, and the obvious compromise is the one measured to fail

```
FINDING ID:      SOUL-F066
DATE:            2026-08-28
KIND:            Doctrine conflict with a measured wrong answer — two rules in the
                 same skill, no precedence stated, and the intuitive resolution is
                 the exact move a prior finding measured as destroying the rules.
REFERENCE PROJECT: Three independent projects:
                 (1) SENSOR-FORGE — "the 80-line TARGET pulls against F045 for a project
                     whose Mind is mostly anti-prior traps; the honest landing was
                     105 lines, every entry anchored. The skill could say which
                     wins on conflict instead of 'cut, do not request an exception'."
                 (2) NAV-TOOL — the same conflict, reported on its fourth cursor.
                 (3) A third project — reported it new, AND supplied the remedy
                     (below) after hitting it in a live distill.
WITNESS IDS:     SOUL-183.
STATUS:          Closed 2026-10-19 — ruled by the Body (SOUL-202); amendment
                 SOUL-A028 accepted and applied in v2.8.0.
RELATED:         SOUL-F045 (carry the incident's force), SOUL-F055 (folding
                 measured at 5/5 -> 1/5 activation), SOUL-A021 (the slim Mind).
```

## The conflict

`/soul-distill` carries a line budget (80 target / 120 cap) and, from F045, the rule
that a fence handed forward without its incident gets reinterpreted under pressure —
carry the **force**, not just the sentence.

For a Mind that is mostly anti-prior traps, every entry needs its incident to work at
all. The budget and the force requirement then pull directly against each other, and
the skill says only "cut, do not request an exception." It never says which rule wins.

## What the third project found — the part worth keeping

Told to hold the line count, the obvious move is to **merge related entries into one
bullet**. That project's first draft did exactly that, grew to 99 lines anyway, and
had to be un-merged.

Merging is precisely the folding F055 measured: rules that fired **5 times out of 5**
before being folded together fired **1 out of 5** after. So the intuitive way to
satisfy the budget is the one move already known to switch the Mind off — and nothing
in the skill says so at the moment the session is looking for lines to save.

Their resolution, which held: **cut whole entries; never merge them.** A Mind with
fewer, intact entries keeps working. A Mind with the same coverage compressed into
combined bullets does not.

## What needs deciding

1. **Precedence.** When force and budget conflict, which governs? SENSOR-FORGE's honest
   landing was 105 lines with every entry anchored — is that a pass or a fail?
2. **The anti-merge rule.** "Shrink" reads as "combine" unless told otherwise. One
   sentence in `/soul-distill` — *cut whole entries, never merge them, because
   merging is the folding F055 measured* — closes the trap for every future distill.
3. Whether the budget itself is right for a trap-heavy Mind, or whether the cap
   should scale with how many entries genuinely need an incident attached.

## A second budget, found while reviewing this finding

`/soul-distill` states the budget **twice and inconsistently**: "Target ≤80 lines;
hard cap 120" in its instructions, and "Do not silently exceed the line budget. ≤200
target, ≤300 cap" in its *What not to do* list. The 200/300 pair is the retired
pre-2.0 anchor that v2.1.1 re-anchored to 80/120 — in one place only.

A session obeying the Do-not list passes a 200-line Mind: the exact artifact the slim
switch (A021) was made to prevent. This finding analysed the 80/120 budget without
noticing the file still offers a second one (fresh-context review, 2026-08-28). Fixing
it is a one-line deletion and does not need this finding resolved first.

## Why it matters beyond one skill

The Mind is always-on text. A budget that is met by the one method that disables the
content is worse than no budget: it produces a Mind that passes its own size check and
stops changing behaviour, with nothing reporting the loss.

## Ruled 2026-10-19 (SOUL-202)

**Ruling (the Body).** The line budget is a **target, not a gate**. 80 lines is a
review trigger — reaching it means re-justifying every entry — but no line-shaving below the 120 cap.
Above 120 the cap is the Body's call, raised out loud. When the budget and an entry's
force conflict, **force wins**. Cut whole entries and never merge them (the F055
folding measurement). Show the weakest cuts to the Body as its call, and let the Body
keep one by raising the cap. This answers question 1 above.

**New instances (mining pass 2):** PLANT-BOP (2026-09-02): "cut, do not request an
exception", and the owner relaxed it on seeing the cut list, which is the ruling
above in practice. GAME-THERMAL (2026-09-02): distill's growth check names no unit;
lines shrank while items grew. The fix that ships with the ruling: always report both
units (`lines a→b · items c→d`). Growth in lines or items needs no sign-off when every
new entry passes the anchor and unguessability tests; above the 120 cap the Body
decides (confirmed by the Body, 2026-10-19).

**Where the fix lands:** `skills/soul-distill/SKILL.md` (step 4's budget and growth
check, step 8's status line), made separately from this record.
