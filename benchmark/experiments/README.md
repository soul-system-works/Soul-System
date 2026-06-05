# Experiments index

Eleven experiments, three families. All share the benchmark's backbone — pre-registration
before outputs, read-the-recommendation scoring (`../SCORING.md`), and inlined (never
`@`-imported) context under `claude -p`. They differ in the **control axis** they ablate.

The 2026-06-05 experiments were born with a genuine `**Locked:**` pre-registration. The
2026-06-04 experiments are normalized from the project's witness log and carry a
`**Reconstructed from:** SOUL-NNN` line instead — faithful to what was locked, never a faked
timestamp (`../SCORING.md` §provenance). The **lock** column below marks which is which.

## Family A — filler-control probes (the 4-arm ablation)

Does injected doctrine change the decision, separating **compute** / **distraction** /
**substance**? Four length-matched arms: `bare / empty / cohirr / substance`.

| experiment | probe class | headline | lock |
|---|---|---|---|
| `2026-06-04-docs-convention` | derivable convention | derivable → `cohirr` *primes* the answer 5/5; substance adds only a citation | reconstructed |
| `2026-06-04-recall` | unguessable fact | clean isolation: `substance` 10/10 vs `{bare,empty,cohirr}≈0`; frontier fabricates the wrong fact | reconstructed |
| `2026-06-05-verify-highstakes` | held disposition | ceiling 40/40 — verify is fully re-derived; substance is a legibility fingerprint, not behavior | locked |
| `2026-06-05-verify-lowstakes` | held disposition | binary caution still derived off-saturation; the one behavioral effect = `cohirr` *erodes* frontier caution (Sonnet 3/5) | locked |
| `2026-06-05-handoff` | form verdict | structured cursor **ties** equal-length prose 10/10 = 10/10; content transmits, format is legibility | locked |

The `cohirr` arm's sign is not fixed — it **primes** a derivable answer (docs), is **harmless**
on an unguessable fact (recall), and **erodes** a sustained caution (verify-lowstakes). That
sign-flip is the family's central result, and the reason the control has to be there.

## Family B — scale & position probes

Does the carry depend on *where* in the context the substance sits, or on model capability?

| experiment | knob | headline | lock |
|---|---|---|---|
| `2026-06-05-depth-position` | needle depth (8% / 50% / 92% in ~6.6k tok) | no positional decay 30/30 — no "lost in the middle" for a distinctive needle at this scale | locked |
| `2026-06-05-calibration` | model capability (Haiku→Sonnet→Opus) | the unguessable fact is never re-derived (44/45 flat); confident-false-assertion *rises* with capability | locked |

> `2026-06-05-calibration` is a capability gradient over the same fact; its procedure is
> described inline in its `PREDICTION.md`/`RESULT.md` (no standalone `run.sh` — it sweeps the
> recall vehicle across three models).

## Family C — longitudinal carry & erosion probes

Does a recorded decision survive across **sessions** (burial), across **compression**
(distillation), and against a model's **trained-in prior**? Arms are `withrecord / control
(length-matched, no D) / floor (no record)` for the carry probes, and erosion levels
`e0 / edir / edist / eloop` for the compression probes.

| experiment | knob | headline | lock |
|---|---|---|---|
| `2026-06-04-longitudinal-preference` | session + task boundary | an arbitrary team *convention* persists at the frontier 5/5 (withrecord) vs 0/5 (control/floor) — the line is derivable-vs-unguessable, not fact-vs-preference | reconstructed |
| `2026-06-04-longitudinal-decay` | record depth N (5 / 10 / 20) | no decay cliff through N=20 at both capabilities; the HOLD is D-being-findable, not context volume | reconstructed |
| `2026-06-04-longitudinal-erosion` | compression level | the *rule* survives compression 30/30; the unguessable *fact* does not — a gradient of anchoring **force** (0/5 → 2/5 → 5/5 → 4/5); Haiku never fabricates (0/15). Behind finding F045 | reconstructed |
| `2026-06-04-longitudinal-antiprior2` | second prior + directive form | force-gradient replicates on a 2nd prior; capability-direction inverts → two levers: directive-**form** gates the frontier, prior-strength + terseness gates the weak model | reconstructed |

These probes carry their original verdict detail in the project witness (SOUL-123→129) and
manifest files; the `RESULT.md` here is the normalized write-up.

---

**Source:** Soul System study `../../docs/study/`. Reconstructed experiments cite their
witness entry; see `../SCORING.md` for the provenance rule. **Status:** active.
