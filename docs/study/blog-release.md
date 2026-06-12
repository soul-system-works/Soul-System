# Soul System 2.0: a conscience and a notebook for your AI coding sessions

Soul System 2.0 is out. It is one plain page of rules your AI coding agent
reads, four commands with teeth, and a book for humans — the shape left
standing after we spent a measurement program trying to kill the rest of it.

Install it in two commands from any Claude Code session:

```
/plugin marketplace add soul-system-works/Soul-System
/plugin install soul-system@soul-system
```

Then, in the project you want it on:

```
/soul-init
```

## The problem it solves

Your AI agent comes back to your project across dozens of sessions and
remembers nothing between them except what the project's files carry. Three
things go wrong, and they go wrong quietly:

- A decision you made for a hard-won reason gets reversed later, when the
  reason is no longer in view — and the reversal gets documented as if it were
  the plan all along.
- Work gets declared "done" that nothing ever ran.
- Something true and important gets discovered mid-session, and dies when the
  session ends.

We measured all three, on real multi-session builds, with every prediction
written down and locked before the experiments ran. The misses are published
alongside the hits.

## What you get

**A completion gate that blocks false "done" claims.** A Stop hook fires when
a session tries to finish; work nothing verified can't be called complete —
the session has to name exactly what is unrun and hand it forward. Before this
rule was made blocking, 6 of 6 gated work increments ended with
disclosed-but-shipped gaps on code that didn't build. After: 0 of 12, and the
build passed its first real execution. The gate has a useful side effect: as
the last reader before "done," it has caught a false provenance pointer in a
safety document, a citation over-claim, and a conflated incident in a paper
draft.

**A record that stays true.** The contract's load-bearing sentence is "never
invent history." That sentence exists because of the single starkest result in
the program: given rules with no backstory, an agent under an ordinary
CLAUDE.md *invented* the backstory — a reviewer who never existed, "mistakes
this project already paid for" that nobody paid — and wrote it into the
project's permanent handoff. Agents carrying this contract declined, and
marked their unknowns as unknown instead.

**A notebook that survives the session.** `/soul-capture` writes ideas,
observations, and findings into project files that the next session loads. In
every condition we tested — including under an excellent generic CLAUDE.md —
a finding born mid-session (a real release blocker, a real defect) was lost at
the session boundary unless an instrument captured it; one project's next
session then confidently taught the debunked conclusion onward. Since 2.0 the
agent proposes captures itself when it spots something a later session
couldn't re-derive; you just say yes or no.

**Decisions that hold as the record grows.** A counter-default fact recorded
early and buried under twenty unrelated entries (~14,000 characters) still
flipped the dangerous default 5 times out of 5, at two model tiers. An
equal-length record without the fact drifted 5 of 5. And the protection grows
with model strength rather than shrinking: without the recorded fact,
confident fabrication *rose* with capability in our cells — roughly 40%
(Haiku) → 85% (Sonnet) → 100% (Opus) — and with it, zero at every tier. A
stronger model doesn't abstain when it's missing your project's truth; it
invents a plausible substitute.

**A contract that stays small on purpose.** The always-on page is about ten
sentences because more text measurably obeys worse: over-loaded doctrine made
a model quote a rule and then violate it, and cutting the always-on text took
weak-model rule activation from 1/5 to 5/5 on identical content. Small is a
correctness rule here, not a style choice.

## What it won't do

Honest limits, each one measured:

- **It won't make your code better than a good five-minute CLAUDE.md.** A
  233-word ordinary contract matched every code-quality endpoint, at the
  lowest cost of any condition, across 9–11-increment builds. The 2026
  frontier model has absorbed the quality practices; if correct code at this
  scale is all you want, you don't need this system — and this system is the
  one telling you that.
- **It won't lower your token bill relative to a minimal contract.** The
  premium buys the notebook and the gate, not cheaper sessions. (It *was*
  13–48% cheaper than a long, excellent generic contract at equal verified
  quality — small contracts win on cost.)
- **It won't stop a model from reaching for a reinterpretation under
  pressure — it bounds the damage.** A pinned boundary converted a
  rule-replacement into an additive change; the reach still happened.
- **It won't write your record in fully automated pipelines.** Headless
  agents wrote record files 0 of 8 times even when instructed. In automation,
  the code-site comments and the handoff document *are* the record — if your
  pipeline discards the code, it discards the record.
- **Text alone won't change behavior — positioned instruments do.** Described
  temptations score 44/45 refusals with no rules at all; the differences only
  appear inside lived work, at the moment a hook or a fence fires. That's why
  2.0 ships instruments, not essays.

## What we actually tested

The full multi-session builds (twin chains, 9–12 increments each) ran on one
frontier model, Claude Opus 4.8. The record-carriage and fabrication probes
behind the numbers above ran at three model tiers — Haiku 4.5, Sonnet 4.6,
and Opus 4.8 — across roughly 390 scored sessions. The 2.0 contract itself
was verified at Haiku, deliberately the weakest tier: 5/5 retrieval-and-hold
on the planted operational fact, 3/3 refuse-and-cite on the invented-history
probe. Longer build horizons, other vendors' models, and a no-contract-at-all
condition remain unmeasured; the survival ties carry a disclosed meta-leak
asterisk. The harness, the frozen chains, and every locked prediction are in
the `soul-benchmark` repository — you're welcome to break it.

## The story in one paragraph

Soul System 1.0 was a philosophy: roles, doctrine, thousands of words of
always-on guidance. The measurement program found the model had quietly
learned most of it — every condition we ran, down to a five-minute CLAUDE.md,
now records decisions and verifies work unprompted. So the philosophy retired
into a book for humans, and what ships is the part no condition reproduced on
its own: a **conscience** (claims verified before "done," no invented
history) and a **notebook** (what this project learned, captured before the
session that learned it dies).

## What's next

Read the book — `philosophy/the-soul.md`, written for you, not the model. Read
the evidence — the formal papers and the research-narrative blog live beside
this file, and the raw corpus (locked predictions, results, scoring memos, arm
repositories) is in `soul-benchmark`. Found something? The contract's own rule
applies to us: open an issue, and we won't invent the history around it.
