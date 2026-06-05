# I gave an AI a philosophy, then tried to prove it was useless

*I built a doctrine layer for AI coding agents — roles, gates, an accumulating record —
and ran a controlled study to find out whether it changes what the model does or just
how the work reads. Most of it is theatre. One part isn't, and it's the unglamorous
one: memory of the things the model can't guess.*

I spent a while building something I half-suspected was theatre.

It's called the Soul System: a body of doctrine — roles, gates, a first principle —
that loads into every AI coding session, plus a record (a witness log, findings,
amendments) that accumulates across sessions. The pitch, the one I'd been telling
myself, was that all this *makes the work better*. The model reasons more carefully.
It catches more. It stays coherent across a long project.

The trouble with a pitch like that is it's almost impossible to feel wrong. Load a
page of thoughtful doctrine into a model's context and its output gets longer, more
structured, more self-aware-sounding. It *reads* better. But "reads better" is
exactly what a system like this would produce whether or not it changed a single
decision. So I did the thing the system itself keeps telling me to do — I went and
checked it against reality, and I designed the check to try to make the answer "no."

## The one trick that makes the question answerable

Here is the whole method in one move. Whenever loading the doctrine seemed to help,
I re-ran the task with the doctrine **replaced by an equal amount of unrelated
filler** — the same token budget of warehouse-logistics prose where the philosophy
used to be, or a generic "double-check your work" where the named checklist used to
be. Same compute, no substance.

If the filler reproduces the gain, the gain was never the doctrine. It was just
*more context*, which any long prompt supplies. A "this improves the work" claim that
evaporates the moment you match it for length isn't substance. It's the model being
more thorough because you gave it more to chew on.

This sounds obvious written down. It is not what most evaluations of "prompt the model
to think step by step / adopt these roles / follow this framework" actually do, and it
is brutal. It caught four separate wins of mine red-handed.

## What turned out to be theatre

The control killed most of the parts I was proudest of.

**Roles.** The system has a whole council — an Archaeologist, a Skeptic, an Advocate,
a dozen more — meant to force the model through different perspectives. Against a
careful frontier model, invoking them changed the *form* of the work (it got named,
legible, auditable) and not its substance. When I rebuilt the roles as the obvious
steelman — *real, separate sub-agents*, one per role, instead of just prose — they
still only matched a generic "break this into perspectives" decomposition at equal
compute. The multi-agent version didn't even beat a single agent told to consider the
same angles; sometimes the step that merged the agents' findings quietly threw good
ones away.

**Trajectory-reading. Compliance-resistance. The handoff format. The verify
checklist.** One by one: looked like wins, dissolved under the filler. A generic
"double-check carefully" caught the planted bug in a draft exactly as well as my
carefully-named verification gate (both 5 out of 5). My structured handoff cursor was
tied by a plain, equally-long prose summary. The trajectory "insight" was reproduced
by unrelated long context. At one point a keyword count told me my verify gate was
winning 5.8 to 2.6 — until I read the actual outputs and saw both versions caught the
same defects; my number was measuring *how verbosely it flagged things*, not whether
it caught more. That one stung, because measuring verbosity and calling it
catch-rate is precisely the kind of self-flattering mistake the whole project is
supposed to guard against.

So: most of the ceremony is legibility. That's not nothing — legible, auditable work
has real value to the human reading it later — but it is not the model thinking
better. I had been quietly believing it was both.

## The one thing that's actually real

Strip all that away and something genuine remains, and it's narrow and specific:

**The system is valuable exactly when it carries knowledge the model cannot regenerate
on its own — and a plausible generic substitute gets wrong.**

Two clean measurements. In the first, the deciding piece of knowledge was a real,
non-obvious finding from my own project — that a certain import mechanism fails
silently in a certain mode and the model confabulates around it. With that finding in
the record, the model avoided the trap 10 times out of 10. With an unrelated record of
the same length, 2 out of 5. The *specific recorded content* did the work — not
"having a record," not the extra tokens.

In the second, my project has a convention that runs against the grain of what models
default to ("keep docs next to the code," where the trained-in default is a separate
docs tree). Load the project's actual rule and the model flips its recommendation to
the project's answer, 10 out of 10. Give it an equal-length set of *generic best
principles* instead and it gives the opposite, default answer, 10 out of 10.

I'll be honest about this second one, because it's a good lesson in its own right. When
I later re-ran it with a stricter control — adding an arm of pure meaningless padding and
an arm of *coherent but unrelated* text — the convention example mostly fell apart. "Keep
docs near the code" is a *defensible generic call*; a strong model already makes it, and
even a weak model, primed by any disciplined-sounding context, re-derives it. The recorded
rule made the model *cite the specific reason*, but it didn't change the decision the way I
thought, because the decision was re-derivable without it. The first example — the silent
import failure — held up perfectly under the same stricter control, precisely because no
amount of generic reasoning gets you to a specific, non-obvious fact about *your* tooling.
So the real keeper isn't "counter-default conventions." It's *un-guessable* facts. The
convention was a flattering example; the obscure failure was the honest one.

And the word that keeps recurring — *confidently* — is the hinge of the whole study.

## The line that predicts what survives

Everything that survived the control sits on one side of a single line:

> **What the model can re-derive dissolves. What it cannot regenerate persists.**

A generic check-nudge re-derives "challenge the unverified premise," so my anchoring
doctrine only beats the filler at *weak* baselines — a strong model already does it.
But a fact about *my* API, a convention specific to *my* project, an incident that
happened on *my* watch — the model can't reason its way back to those from first
principles, and no amount of generic, equal-length prose substitutes for them. That's
the durable core. Memory of the unguessable.

## The part that actually moved my mind

The single-shot tests above all share a weakness: they're one session. The system's
real promise was always *longitudinal* — a record that builds up over a whole project
and keeps later sessions from drifting. You can't fake that with one prompt, so for a
long time I just honestly marked it "unmeasured."

Then I built a synthetic session chain to reach it: an early session records a
counter-default decision (say, "this payment endpoint is not safe to auto-retry,
here's the incident that proved it"); later sessions bury it under unrelated work;
a fresh session, with the original context gone, gets a task that tempts the dangerous
shortcut. Without the record, the model drifts into the dangerous default 5 times out
of 5. With the record carried forward, 0 out of 5. With an equal-length filler record,
it drifts exactly as if it had no record at all.

And here's the result that changed how I think about all of this: **this is the first
win that does not dissolve at the frontier.** The strong model drifts *too* — and it
drifts more dangerously, because when it lacks the recorded fact it doesn't just make
a default choice, it *invents* a reassuring justification that doesn't exist (it
confidently adds an idempotency key the API doesn't support, and explains why that
makes the retry safe). It fabricates instead of abstaining — which is exactly what the
calibration research says post-trained models do when they're missing a fact: be
confidently wrong rather than flag the gap. (I want to be careful here: I don't think
this proves "smarter always means more confidently wrong" as a clean law — when I pushed
on it, *which* model fabricated depended on how the rule was phrased, not just on
capability. But in this case, the only thing that stopped the strong model was having
the actual fact on record.) The carry held under burial twenty sessions deep, and it
held for arbitrary conventions, not just facts.

One limit I found while pushing on it inverts the obvious intuition. You can compress
the *rule* to a single line and it survives the trip across sessions intact. But you
cannot compress the *force* of the fact behind it. Strip the incident and the explicit
"no, this isn't supported," leave just the terse rule — and the strong model starts
fabricating its way around it again, walking through whatever loophole the compression
left open. The weak model, with no confident prior to assert, doesn't. So memory of the
unguessable works, but only if you keep *why* it was true, not just *that* it was — a
sharp little constraint on anyone planning to summarize their project's hard-won rules
into something tidy.

## What I think the honest version of this system is

Put it together and the lean system writes itself. Keep the parts that carry the
unguessable: the record, a small always-on rule-set of the project's counter-default
conventions, a tested index of which specialized skill to reach for when. Keep the
scaffolding that makes a good practice reliably *happen* rather than just be described
— the capture command that lowers the friction of writing things down, the completion
check that actually fires (it caught a real overclaim of mine in the session that
produced this very study). Cut the rest to a one-line reminder: the role chamber, the
forced perspectives, the elaborate formats. Not because ceremony is worthless, but
because a generic equivalent does the same job for free.

That's the version the evidence points to: keep the memory, keep the activation, cut the
ceremony to a line.

## What I can't claim

The method has a deliberate blind spot, and pretending otherwise would undo the point.
It's single-shot and single-resume. The numbers are small (five to seven runs a cell).
The longitudinal results come from a *synthetic* session chain, not a year of real
project history. And the one value I keep asserting but never actually measured — what
all this legibility is worth to a *human* coming back to the project months later — is
exactly the kind of human, over-time claim the harness can't reach. I marked it on the
map rather than coloring it in.

But the confident half I'll stand behind: most of what makes a methodology system
*feel* like it's helping is the system making the work legible and the model more
verbose. The part that genuinely changes what the model decides is narrower and less
glamorous than the pitch — it's memory. Specifically, memory of the things the model
can't guess and would otherwise get confidently, plausibly wrong.

That turned out to be worth keeping. The rest, I'm fairly sure now, I was admiring in
the mirror.

---

*A formal write-up — method, every probe's design and data, the controls, and the
threats to validity — is in the [companion paper](paper.md). The consolidated result
tables are in [`data/`](data/results-tables.md).*
