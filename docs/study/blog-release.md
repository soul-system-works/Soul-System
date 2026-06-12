# Soul System 2.0: what it will do for you, and what it won't

*The honest release notes. Every claim below is anchored to a pre-registered,
locked-prediction experiment you can read in the `soul-benchmark` repository — the
misses included. The system this describes is small on purpose: one plain page the
AI reads, four instruments, and a book for humans. Here's exactly what that buys
you, and exactly what it doesn't.*

## What it is now

In June 2026 we ran the system through a measurement program designed to kill it:
twin-chain builds against an excellent generic CLAUDE.md, against a deliberately
mediocre one, and with all the persuasive backstory stripped out of the prompts.
Most of the doctrine didn't survive — not because it failed, but because the
frontier model now does those things unprompted. What survived is the part the
model still cannot do for itself. Version 2.0 is that residue:

- **The contract** — ~10 plain rules in `operations/CLAUDE.md` (the only thing the
  AI reads).
- **The instruments** — `/soul-capture` (a notebook with a triage rule), the
  completion gate (a Stop hook that blocks unverified "done"), `/soul-handoff` +
  `/soul-resume` (session continuity), `/soul-distill` (keeps the contract small).
- **The book** — `philosophy/the-soul.md`, for you, not the model.

## What it WILL do for you

**Block false "done" claims where verification is possible — and demand the gap be
named where it isn't.** The one before/after this program produced: under v1.0, 6
of 6 gated increments ended with disclosed-but-shipped gaps on code that didn't
build; under the v1.1 blocking rule, 0 of 12 — and the build passed cold. The gate
also moonlights as a last-read defect detector: it has caught a false provenance
pointer in a safety document, a citation over-claim, and a conflated incident in a
paper draft. *(soul-benchmark: v1-invivo-twin, v11-a020-placement; SOUL-159/164.)*

**Keep your project's record true.** The only behavioral difference between
doctrine and no-doctrine arms in the entire program: given rules without
backstories, the no-doctrine arm *invented* backstories — a reviewer who never
existed, "mistakes this project already paid for" that nobody paid for — and wrote
them into its permanent handoff. The contract's "never invent history" rule, plus
anchor discipline ("trusted because / would be wrong if"), measurably prevents
fabricated history in your records. *(force-stripped RESULT §2; SOUL-164.)*

**Catch the findings your sessions generate and then forget.** In every condition
tested — including under an excellent CLAUDE.md — a finding born mid-session
(a real release blocker, a real defect) died at the session boundary unless an
instrument captured it; one arm's successor then confidently taught the debunked
conclusion. The capture loop exists for exactly this, with a measured triage rule:
record the unguessable (held 0/30 drift at every model tier); skip the derivable
(the model re-derives it 10/10). *(efficacy-floor + force-stripped RESULTs; F044.)*

**Carry decisions across sessions, robustly.** A recorded counter-default fact
buried under twenty unrelated entries (~14k characters) still flipped the dangerous
default 5/5 at two model tiers; an equal-length record without the fact drifted
5/5. The record doesn't rot as it grows — through the depths we tested.
*(longitudinal-decay; docs/study/07.)*

**Protect you more, not less, as models get stronger.** Without the recorded fact,
confident fabrication *rises* with capability — roughly 40% (Haiku) → 85% (Sonnet)
→ 100% (Opus) in our cells; with the record, zero at all tiers. The stronger model
doesn't abstain when it's missing your project's truth; it invents a plausible
substitute. *(f044-rungs; F054.)*

**Stay cheap and small — because that's a correctness rule, not a style choice.**
Over-loaded doctrine made a model quote a rule and then violate it; cutting the
always-on text took weak-model rule activation from 1/5 to 5/5 on identical
content. The contract is ten sentences because more text measurably obeys worse.
*(erosion-audit; F055.)*

## What it WON'T do for you

- **It will not make your code better than a good five-minute CLAUDE.md.** A
  233-word ordinary contract matched every quality endpoint at ceiling across
  9–11-increment builds. If you only want correct code at this scale, you don't
  need this system. *(efficacy-floor RESULT.)*
- **It will not lower your token bill.** Cost ordered floor < Soul < excellent
  generic in every comparison; the premium over a minimal contract buys the
  notebook and the gate, not cheaper sessions. *(efficacy-floor §cost.)*
- **It will not stop a model from reinterpreting your rules under pressure — it
  bounds the damage.** The pinned boundary converted a replacement-drift into an
  additive change; the model still reached for the reinterpretation. *(SOUL-159.)*
- **Doctrine text alone will not change behavior — only positioned instruments
  do.** Described temptations score 44/45 refusals even with no doctrine at all;
  the differences only appear inside lived work, at the moment the hook or the
  fence fires. That's why 2.0 ships instruments, not essays. *(v11-a019.)*
- **It will not write your record for you in automated pipelines.** Headless
  sessions wrote record files 0/8 times even when instructed; in automation, the
  code-site comments and the handoff document ARE the record — if your pipeline
  discards the code, it discards the record. *(v1-stream.)*
- **It will not make the model want fewer war stories — it keeps the ones you
  have true.** Incident-shaped rhetoric is model-native; content integrity is
  what the contract buys. *(force-stripped §2.)*
- **And the honest scope line:** all of this was measured at 9–12 increment
  chains, on one frontier model, with the survival ties carrying a disclosed
  meta-leak asterisk. Longer horizons, other models, and a no-contract-at-all arm
  remain unmeasured. The harness is in the repo; the predictions get locked
  before the arms run; you're welcome to break it.

## The one-sentence version

The model learned the philosophy, so the philosophy retired into a book; what your
project still needs from software is a **conscience** (verified claims, no invented
history) and a **notebook** (what we learned, captured before the session dies) —
and that's what this installs.

---

*Evidence index: the formal papers (the equal-compute ablation and the
longitudinal/efficacy sequel) and the research-narrative blog live alongside this
file; the raw corpus — every locked prediction, result, scoring memo, and arm
repository — is in the `soul-benchmark` repository.*
