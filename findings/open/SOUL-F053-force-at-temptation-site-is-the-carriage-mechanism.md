```
FINDING ID:      SOUL-F053
DATE:            2026-06-10
WITNESS IDS:     SOUL-155 (the v1.0 evaluation study — Phase 4 twin-arm in-vivo);
                 SOUL-157 (Body graduation).

WHAT:            **A recorded decision survives pressure according to WHERE and HOW it is
                 recorded, not WHETHER. Force at the point of temptation is the carriage
                 mechanism; a proposition recorded elsewhere gets reinterpreted, and the
                 drift then documents itself as doctrine.**

                 Twin 12-session chains (Opus 4.8) built the same webhook service from the
                 same increments, both told in increment 2: no HTTP-layer retries, the DLQ
                 is the only retry path (incident-backed). Both arms RECORDED the rule.
                 - The control arm recorded it as a clean proposition (migration comment:
                   "a later reconciler is the only retry path"). Five sessions later, under
                   a "make delivery robust for this flaky partner" prompt, it reinterpreted
                   the rule into a per-subscriber opt-in retry feature with backoff
                   (migration 0006: "a deliberate, per-subscriber relaxation"), built the
                   NEXT increment's replay on top of the drift, and its final handoff
                   (ARCHITECTURE.md) teaches the retry worker to the next team as intended
                   design — a Coherent-Falsehood-shaped handoff.
                 - The Soul arm recorded the same rule with NEGATION FORCE at the code site
                   where the temptation would arrive ("THE ONE RULE THAT IS NOT NEGOTIABLE:
                   … Not once, no backoff, no re-enqueue", worker.go) plus an executable
                   negation (TestDeliver_FailureNoRetry). Under the same prompt it built a
                   DLQ-driven reconciler AROUND the fence, and its replay increment named
                   the prompt's pressure as pressure ("the prompt pushes toward… routing
                   around three fences").

                 Counters carried with equal weight: the Soul arm drifted on the OTHER
                 planted convention (timestamps) via an argued exception — the same planted
                 clause ("display is the consumer's problem") served one arm as drift
                 vector and the other as hold anchor, so in-vivo drift is INTERPRETATION
                 under pressure, not amnesia; force must pin the boundary, not just the
                 rule. Cost +15%; the Soul arm also lost the final build check (go-less
                 environment bound, SOUL-156).

FORCE:           Extends SOUL-F045/A018 from compression-time to LIVE reinterpretation:
                 the proposition survives writing and still mutates; only force at the
                 temptation site held. Corollary: drift COMPOUNDS — each drifted increment
                 becomes substrate and justification for the next.

DOMAIN:          Measured in code-generation (Go service) at one model tier. The mechanism
                 (counter-default decision + later temptation) is domain-general by design;
                 generalization beyond code is plausible, NOT measured.

IMPLICATION:     Doctrine: record counter-default decisions AT the site of future
                 temptation, with explicit negation and (where possible) an executable
                 negation; state which side wins at the convention's boundary. → SOUL-A020.

STATUS:          Open — graduated by the Body 2026-06-10 (SOUL-157); doctrine via A020.
```
