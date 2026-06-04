# Longitudinal, part 2: does the carry hold for a *preference*, or only a fact?

The fact probe ([`07`](07-longitudinal.md)) left one question explicitly open, and wrote
it into its own bounds: the win was for a record carrying a counter-default *fact* the
model can't derive. *"A record carrying a pure reasoning-preference would likely dissolve
at the frontier like the rest of the study — that is not claimed here and would need its
own probe."*

This is that probe. The conjecture was wrong.

## Why the conjecture looked safe — and why it wasn't

The study's confident half is that **reasoning-lift dissolves at the frontier**: anchoring
and skill-routing helped the weak model but vanished at Sonnet, because Sonnet could
*reason its way* to the answer the record supplied. A preference — "we return Result types,
not exceptions" — feels like it belongs on the reasoning side: the model clearly *can*
reason about error-handling style, so surely the strong model just does the sensible thing
and the record adds nothing.

But run the study's own logic carefully. The record persists exactly when it carries
something the model **cannot regenerate on its own**. An arbitrary team convention is
*unguessable a priori* — the model can generate *a* valid choice, but not *this team's*
choice. By that logic a preference should **persist**, not dissolve. The real question was
never "does it dissolve" — it was **deference vs. override**: when the record states a
convention the model didn't pick and its own reasoning offers an equally-valid alternative,
does the frontier model *defer* to the record, or *override* it with its own idiom?

## The method: same harness, a preference D

The harness is identical to [`07`](07-longitudinal.md)'s — a manufactured session chain,
S1 (establish D as an ADR) → S2 (bury D under an unrelated ADR) → S3 (a new related task,
original context absent), with the decisive **with-record vs control** contrast (a
length-matched filler holding the same project framing and token volume but no D). Only D
changed.

Picking D carried the v1→v2 lesson — **floor-check counter-default-ness first** — plus a
new gate the fact probe didn't need. Three candidate conventions were floor-checked fresh
(no record) at both models:

| Candidate convention | Fresh-model default | Verdict |
|---|---|---|
| validate at construction, not in business logic | already validates at construction | not counter-default — out |
| all DB access through a repository | inlines SQL, **but a repo for one function is arguably YAGNI** | counter-default but override-prone — muddy |
| **return a Result type, don't raise for expected failures** | **raises exceptions (6/6, both models)** | **cleanest counter-default — picked** |

**D = expected business failures are signalled by returning a `Result` (`Ok`/`Err`), not by
raising exceptions; exceptions are reserved for genuine programmer errors.** It is a pure
*preference* — both styles are correct, neither is over-engineering — and it runs *against*
Python's strong exception idiom, so deferring to it is not a free choice. S1 establishes it
as ADR-001 (rationale: uncaught exceptions had leaked to customers as HTTP 500s); S3 asks
for a new `transfer_funds` function with two expected-failure cases that naturally pull
toward `raise`.

**The new gate — an install-check.** A fact either loads or doesn't; a *preference* might
be too arbitrary to install even at the weak model, which would leave no win whose
frontier-persistence we could measure. So before the full matrix: confirm with-record
moves Haiku from raise→Result. It did, 5/5. The floor-check (counter-default) and the
install-check (it carries at all) together gate the spend.

## The result

Scored HOLD (returns a `Result`, no `raise` for the expected failures) vs DRIFT (raises),
read-confirmed in the actual code across all 30 outputs. n=5 per cell.

| Arm | Haiku | Sonnet |
|---|---|---|
| floor (no record) | **5/5 DRIFT** | **5/5 DRIFT** |
| **with-record** (ADR-001 buried under ADR-002) | **5/5 HOLD** — cite ADR-001 | **5/5 HOLD** — cite ADR-001 |
| control (length-matched filler) | **5/5 DRIFT** | **5/5 DRIFT** |

The same three things as the fact probe, each load-bearing:

1. **The record moved the decision** — drift→hold 5/5 at both models, citing ADR-001 and
   reproducing its reasoning two sessions later with the context gone.

2. **Equal compute is controlled** — the length-matched filler drifts identically to the
   bare floor at both models. The control engages its record honestly: it cites the
   *filler's own* (logging) ADR — and never confabulates a Result convention that isn't
   there. The gain is the record's content, not its volume.

3. **It persists at the frontier — and the frontier model *defers*.** Sonnet's floor drifts
   5/5 (its own default is exceptions). With the record, it switches to Result 5/5 — *not
   reluctantly*. None of the five hedged or argued for the more-idiomatic exception; they
   adopted the convention and reproduced its reasoning. One reproduced the ADR's *boundary*
   unprompted: it kept an `amount > 0` check as an `assert` because *"a zero or negative
   amount is a programmer mistake, not a business condition — per ADR-001, programmer
   errors stay as exceptions."* The model didn't just match a keyword; it reconstructed the
   exact line the ADR drew between business failures (Result) and programmer errors
   (exceptions), two sessions after that line was written.

## The reframe: derivable vs. unguessable

The fact/preference distinction is **not** the frontier line. Both a fact and a preference
persisted at Sonnet, identically, 5/5. The line that actually separates the study's wins is
**derivable vs. unguessable**:

| | Derivable (model can re-reason it) | Unguessable (model can't regenerate it) |
|---|---|---|
| **examples** | anchoring, skill-routing | an external fact (`07`); an arbitrary convention (this) |
| **at the frontier** | **dissolves** — strong model reaches it alone | **persists** — strong model needs the record as much as the weak one |

An arbitrary convention is unguessable for the same reason an external fact is: the model
cannot derive *which* choice this team made, however well it can reason about the options.
So the record carries something the frontier model genuinely lacks — and the frontier model
**defers** to it rather than substituting its own equally-valid idiom. The accumulating
record governs not only facts the model can't know, but arbitrary conventions the model
can't guess — at any capability.

This sharpens, rather than contradicts, the study's central split. **What dissolves at the
frontier is the *derivable*; what persists is the *unguessable*.** A meta-doctrine system's
durable value is precisely the unguessable it carries forward.

## Bounds (what is and isn't claimed)

- **One preference, well-formed.** The convention was clearly stated and defensibly
  reasoned. A terse, weakly-justified, or actively-bad convention might not install even at
  the weak model, or might get overridden at the frontier — "the frontier model defers" is
  bounded to well-formed conventions until tested otherwise.
- **The reframe is inductive.** Derivable-vs-unguessable rests on ~4 points (two persist,
  two dissolve), not a proof. More dissolve/persist pairs would harden it.
- **Single dilution step, n=5, two models, establishment-assisted S1** — the same first-rung
  bounds as `07`. The *depth* of that single step has since been stretched: a follow-on
  (SOUL-125, see [`07` §depth-decay](07-longitudinal.md)) found **no decay cliff through
  N=20** burial at both capabilities for the fact D. What remains unmeasured for both probes:
  an *eroding/compressed* record and *interacting* (reinforcing or contradicting) entries.
- **A method honesty note:** under headless `claude -p`, 4 of the 15 Haiku floor/control
  runs tried to *write a file* (blocked, no tools) and returned a prose description instead
  of inline code; these were scored by the described approach (all explicitly named
  exceptions → DRIFT), and no verdict turned on the ambiguity. Every with-record run and
  every Sonnet run produced full inline code.

**Raw arms:** `.soul/experiments/2026-06-04-longitudinal-preference/` (floorcheck/ + s1/s2/s3
+ filler + arms + manifest). Shares the harness and design of
[`07`](07-longitudinal.md) / [`docs/specs/2026-05-29-longitudinal-harness-design.md`](../specs/2026-05-29-longitudinal-harness-design.md).
