```
AMENDMENT ID:    SOUL-A017
DATE:            2026-05-28
WITNESS IDS:     SOUL-107, SOUL-108, SOUL-109; graduates finding SOUL-F042.
WHAT CHANGES:    Add a `### What the Roles Are For` subsection to
                 philosophy/the-soul.md (under `## The Council and Its Roles`,
                 after the tier descriptions, before `## Magistrates`). It
                 records the measured value-locus of the Council roles/gates:
                 against a capable baseline they change the FORM of the work
                 (legibility / auditability / communicability) far more than its
                 SUBSTANCE (behaviour-lifting) or RELIABILITY (stabilisation).
                 The roles are justified primarily by legibility, not by
                 changing the answer — with an explicit bound: the evidence is
                 against a frontier baseline on moderate-to-tracer-hard tasks; a
                 genuinely baseline-breaking regime remains untested and could
                 shift the value-locus back toward substance.
WHERE IN SOUL:   philosophy/the-soul.md only (the on-demand depth layer). NOT
                 the always-on seed (operations/CLAUDE.md) — Rule 5 / SOUL-033:
                 auto-loaded doctrine has a token budget; this framing is depth,
                 not a gate that must fire every session. NOT mind.md by hand —
                 the Distiller folds it on the next /soul-distill (candidate: a
                 sharpened "roles' value is legibility, bounded to the careful-
                 baseline regime" rule/tension, replacing the implicit "each role
                 does heavy lifting" assumption already softened in the residual).
QUESTION ONE:    Evidence — the I040 self-ablation experiment, two runs. Run 1
                 (moderate tasks, A0–A10 + consistency, n=7 + 5×2) converged on
                 form-not-substance and graduated SOUL-F042. Run 2 (this gate:
                 the hard regime) ran three engineered fragility axes — HR1 pure
                 logic (bare 3/3 caught), HR2 false-premise under deference (bare
                 3/3 caught), HR3 ten-constraint long-horizon (completion-gate
                 ablated with/without, n=3 each: NULL — gate ≈ bare). Detail:
                 docs/experiments/2026-05-28-self-ablation-hard-regime.md; raw
                 arms in .soul/experiments/2026-05-28-hard-regime/. Field
                 corroboration: personas don't reliably help accuracy (arXiv
                 2311.10054); single≈multi-agent under equal compute (2604.02460,
                 2505.18286); orchestration aids interpretability not raw accuracy
                 (TRiSM 2506.04133). The "each role does heavy behavioural
                 lifting" assumption was never anchored; this anchors its
                 correction.
QUESTION TWO:    Necessity — without this, doctrine implicitly promises that each
                 role lifts behaviour, which the evidence contradicts and which
                 mis-sells the system (and would mislead a reference project about
                 *why* the roles earn their keep). Recording the measured value-
                 locus (legibility) keeps the role chamber honestly justified and
                 explains why roles stay lensed/on-demand rather than heavy.
QUESTION THREE:  Coherence — extends, does not contradict. It sharpens, not
                 reverses: the roles remain the rules' executors and the chamber
                 keeps its depth; what changes is the stated *reason* they earn
                 their place (legibility over behaviour-change). Consistent with
                 SOUL-033/034 (gates survive context reduction, expansion does
                 not) and with the seed opening ("two parties reading the same
                 record must arrive at the same meaning"). The explicit bound
                 prevents over-reading into a universal law.
ACCEPTED BY:     Judge (Body-decided graduation: "graduate → scoped amendment").
FILED BY:        Emissary (the system tested its own beliefs against reality);
                 Skeptic + Accountant (named the confounds and the surviving
                 bound).
```

---

## Why an Amendment and not a continued Finding

SOUL-F042 was held open precisely until its named graduation gate — the hard-
regime test — produced data. It has. The result (hard regime *also* form-not-
substance) is the data point F042's `WHY-NOT-YET-AMENDMENT` required, so the
finding is discharged into doctrine rather than left accumulating. The Body made
the graduation call (earned-graduation: the Body decides), choosing the **scoped**
amendment so the doctrine change banks the measured result while the surviving
open edge (no truly baseline-breaking regime was tested) is carried *in the
amendment text itself*, not dropped.

## The Scope (what this does NOT claim)

- It does **not** claim roles are valueless — legibility/auditability is a real,
  named value (the Body's "naming is the value" point, now well-supported).
- It does **not** claim the result holds where the baseline *breaks* — that
  regime was untested at acceptance and explicitly fenced as the place substance
  could return. See **Follow-up evidence (SOUL-I041)** below — it has since been
  probed once, and the bound is sharpened (substance returns, but narrowly), not
  removed.
- It does **not** restructure the Council, retire any role, or touch the always-on
  seed. One depth-layer subsection; the gates and roles are unchanged in operation.

## The Specific Change

Added to `philosophy/the-soul.md`, under `## The Council and Its Roles`, after the
tier descriptions and before `## Magistrates`, a `### What the Roles Are For`
subsection stating: the roles are justified primarily by legibility, auditability,
and communicability rather than behaviour-lifting; with the explicit bound that
the evidence is against a capable frontier baseline on moderate-to-tracer-hard
tasks and a genuinely baseline-breaking regime remains untested.

---

## Follow-up evidence (SOUL-I041, 2026-05-28) — the bound, sharpened not removed

A017's bound named a *baseline-breaking* regime as the place substance could
return. SOUL-I041 ran the first probe of it — a **weaker-model arm** (Haiku 4.5
vs the (b) Opus baseline), same tasks HR1–HR3, C1 compute-controlled. Detail:
.soul/experiments/2026-05-28-i041-weaker-model/manifest.md; witness SOUL-110.

- **The fragile regime exists.** The weaker baseline broke where Opus was robust:
  HR1 logic 2/3 (vs 3/3), HR2 false-premise 0/3 caught (vs 3/3 NO-GO), HR3
  constraints broken (vs ~3/3).
- **A single role/gate still adds only FORM, even when the baseline breaks.**
  Accountant lens on HR1: 2/3 → 2/3. Completion-gate on HR2: 0/3 → 0/3 flipped
  (added verification *language*, not a flipped decision). A017's core holds, now
  robust into the broken regime.
- **The INTEGRATED layer (seed + Mind) DOES add substance — narrowly.** On HR2
  (the anchoring axis) it lifted the weak baseline 0/3 → ~1.5/3 (one clean NO-GO
  that named non-linear cost scaling; one run that surfaced the unverified premise
  explicitly). It did NOT help HR1 (1/3, *worse* — big context distracted) or HR3
  (worse). The lift is **discipline-matched** (the anchoring/skepticism the Soul
  most encodes), **integration-dependent** (single lenses did not transmit it),
  and **partial**.
- **C1 control — the gain is doctrine, not compute.** A length-matched neutral
  26 KB filler left HR2 at 0/3 (= bare). The whole-layer gain is attributable to
  the Soul's anchoring discipline, not to added tokens/thinking.

### Generalisation attempt (G2, Prophet/trajectory) — FAILS the compute control

The "discipline-matched substance" reading above was tested on a SECOND
discipline: a Prophet/trajectory trap (a SaaS cost-cut whose buried second-order
harm is severing the conversion funnel — the arm must *read the trajectory*). On
the weak baseline: bare 1/3 caught → whole-layer 3/3. That looks like clean
generalisation — **until C1.** A length-matched NEUTRAL filler (26 KB of
warehouse-logistics nonsense) lifted the same baseline to **2/3** (catches
verified genuine). So most of the trajectory "gain" is a **generic long-context /
be-more-thorough effect, not the doctrine** — the doctrine's margin over filler
(2/3 → 3/3) is within n=3 noise. This is the OPPOSITE of HR2 (anchoring), where
filler stayed at 0/3 and the gain was doctrine-attributable.

**Why the two axes differ (the sharpened insight):** challenging a false premise
(anchoring) is **content-dependent** — it needs the specific "internal coherence
is not truth / do not assert the unverifiable" content; generic thoroughness can't
fake it. Flagging downstream consequences (trajectory) is **disposition-
elicitable** — any serious, long system prompt nudges the model into it. C1
separates the two.

**Net effect on A017 (tightened):** the core (single roles/gates = form, not
behaviour-lifting) is *reinforced* — now across two disciplines and into the
broken-baseline regime. The integrated layer's C1-SURVIVING substance is, so far,
**robust only for ANCHORING** — plausibly the single most-repeated discipline in
the seed+Mind, and content-dependent rather than disposition-elicitable. The
broader "discipline-matched substance" hope did NOT generalise to Prophet once
compute was controlled. Method rule this establishes: **run C1 on EVERY apparent
win** — the trajectory result was a false positive without it.

### Replication (G3b, 2nd anchor task) — the anchoring substance REPLICATES

The owed 2nd-anchor-task test ran (SOUL-I041 Step 6; witness SOUL-112). A first
attempt (G3, a medical vendor-study rollout) was C2-rejected — bare caught it 3/3,
because high-stakes-SAFETY salience triggers a caution reflex that substitutes for
the anchoring discipline (a useful side-finding). Recalibrated to a low-salience
business anchor (G3b: a $1.2M ad-budget reallocation on an agency-reported 4.2x
ROAS from a one-month pilot): bare ~0–1/3, **whole-layer 3/3, C1 filler 0/3.** So
the C1-surviving, doctrine-attributable anchoring substance now **replicates across
two anchor tasks** (HR2 + G3b), different domains. The cross-axis pattern is clean:
filler stays 0/3 on BOTH anchor tasks but jumps to 2/3 on the trajectory task —
confirming content-dependent vs disposition-elicitable. **A017's anchoring-specific
substance claim is now firm (n=2, replicated, C1-controlled).** Still owed for more
weight: higher n + a 2nd model (Sonnet 4.6 gradient) — carried in SOUL-I041. No
further doctrine change until then.

### Capability gradient (SOUL-I041 Step 7; witness SOUL-113) — the substance is also task-structure-dependent

A Sonnet-4.6 mid-capability probe (HR2 + G3b, n=5, bare/whole/filler) asked
whether the anchoring substance shrinks as the baseline strengthens. It does — but
not uniformly. The gate is **whether the baseline self-catches**, set by capability
AND task structure:

- **HR2 (a go/no-go JUDGMENT task):** Sonnet's bare baseline already recommends
  NO-GO 5/5 (like Opus 3/3, unlike Haiku 0/3). Ceiling reached → whole-layer gap
  gone. The analytical catch self-corrects by mid-capability.
- **G3b (a comply-and-DRAFT task):** the *flag* is cheap at Sonnet (all arms raise
  the 4.2x concern), but the *action* separates them — whole-layer **withholds /
  resists** (3/5) while bare flags-then-drafts (4/5 drafted) and the equal-length
  filler drafts 5/5 ("ready to send"). The doctrine's edge here is **resisting the
  compliance pull on a flawed premise** — and it survives to higher capability than
  the analytical catch does.

**Sharpening of "only when the baseline needs it":** the baseline needs the
doctrine when it won't self-catch — and analysis-inviting tasks get self-caught at
lower capability than compliance-inviting ones. So the integrated layer's durable
substance (the part that persists toward the frontier) is concentrated in
**resisting compliance with flawed premises on "just-do-it" tasks**; the
analytical catch is a weak-baseline-only rescue. BOUNDS: n=5, one mid model, two
tasks; the G3b whole>filler gap (3/5 vs 0/5) is the load-bearing claim. A 3rd
capability point + more compliance-tasks would firm the curve (SOUL-I041).
