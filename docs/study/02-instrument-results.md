# Instrument results — the `/soul-*` commands and the record

Three buckets (see [`00-method.md`](00-method.md)): **measured** (A/B + C1),
**reasoned** (cost vs plausible value), **inspected** (one-time/structural). This
file holds the measured ones; the reasoned/inspected verdicts live in
[`03-leandown.md`](03-leandown.md).

A method note that shaped this section: an early recall run was **contaminated** —
`claude -p` arms have tool access and read the working directory, so arms launched
from a directory containing the answer file (`records-relevant.md`) simply *grepped
it* ("I found the key constraint, SOUL-F038…") even in the no-record condition. Fix:
run every arm from an **isolated empty working directory**. This is itself a method
finding (it generalises the F038/harness-discipline lesson) and the contaminated run
is retained under `.soul/experiments/…/out-contaminated/` as evidence.

---

## Measured 1 — `/soul-handoff` → `/soul-resume` (cross-session state transfer)

**Claim:** the Soul cursor lets a fresh session resume better than alternatives.
**Design:** fresh session given the same curated records snapshot + one of {Soul
cursor · length-matched generic prose summary · terse compact summary · nothing};
state WHERE/NEXT/CONSTRAINT. Sonnet+Haiku, n=5, 40 arms. Raw:
`.soul/experiments/2026-05-28-handoff-resume-value/`.

**Result** (constraints surfaced, avg /5; re-derivation errors):

| | cold | cursor | generic (C1) | compact |
|---|---|---|---|---|
| Sonnet | 3.0 (0 err) | 4.6 (0) | 4.8 (0) | 3.2 (0) |
| Haiku | 2.4 (1 err) | 4.6 (0) | 4.6 (0) | 3.4 (0) |

**Verdict:** a rich written handoff beats cold re-derivation (≈+2 constraints; 0 vs
1 scope-invention error). **But the Soul format is form** — a length-matched generic
summary ties it (Sonnet generic 4.8 ≥ cursor 4.6; Haiku equal). Richness matters,
structure doesn't (terse compact ≈ cold). **Bounds:** retrieval (finding the right
records in a big repo) and scaffolding-completeness (does the command make you
*write* a more complete note) were held constant by design — untested, and the two
places the *command* (vs a plain summary) could still earn its keep.

**Three-arm confirmation (added 2026-06-05, SOUL-139).** Re-run under the cleaner control
(bare / empty / cohirr / prose / cursor) on a resumption vehicle with a buried live
constraint: the structured cursor **tied equal-length prose exactly** (cursor 10/10 = prose
10/10; no-state arms 0/30). Confirms "the Soul format is form" at the stricter bar — the
state *content* transmits (and prose carries it equally); the cursor structure is legibility.
Side-result: the no-state arms **abstained** (asked for the missing state), they did not
*fabricate* a resumption — confident fabrication needs a plausible prior to draw from, not a
salient gap (the opposite of the recall/@-import case). With verify (SOUL-135/136) this closes
both "form" verdicts as legibility, not behavior.

---

## Measured 2 — record-recall / traceability (the steelman)

**Claim:** the accumulated record lets a session avoid a non-obvious,
project-specific mistake it could not re-derive.
**Design:** a trap task (set up a `claude -p` harness; the DRY-tempting path is an
@-import) where a **real, non-obvious finding — SOUL-F038** (@-imports fail silently
under `-p`, confabulate ~43%) — is the deciding knowledge. Arms: {relevant record
(F038 + 2 decoys) · no record · length-matched **irrelevant** record (C1)}. Sonnet+
Haiku, n=5, isolated dirs. Raw: `.soul/experiments/2026-05-28-handoff-resume-value/`
sibling `recall-test`.

**Result** (avoided the trap = inlined / used `--append-file`, did not rely on
@-import; read-classified, not keyword):

| | record (F038) | no-record | irrelevant (C1) |
|---|---|---|---|
| Haiku | **5/5** | 3/5 | 2/5 |
| Sonnet | **5/5** | ~2/5 | 2/5 |

**Verdict — a real, C1-surviving record value.** The F038 record reliably produces
trap-avoidance (10/10); a **length-matched irrelevant record does not** (2/5), and
no-record only partially (capable arms reason toward "@-imports may not resolve in
isolated calls" and add a sentinel hedge, but mostly still recommend @-import). So
the *specific recorded content* — not "having a record" and not compute — is what
makes the model reliably do the right thing. **This is the strongest instrument-side
result in the study: the record carries project-specific empirical knowledge the
model can only partially derive and an unrelated record cannot supply.**

Nuance (honest): the trap is *partially* derivable (no-record 2–3/5), so the
record's value is "makes the right call reliable + explicit," not "supplies
otherwise-unreachable knowledge." Still real; still survives the C1 control.

---

## Measured 3 — `/soul-verify` / the completion gate (catch defects before shipping)

**Claim:** running the verify gate catches real errors that would otherwise ship.
**Design:** finalize a draft containing one planted defect. Arms: {bare · verify
(Soul checklist) · generic-vague ("double-check carefully") · **generic structured
checklist** (C1, length/structure-matched, generic checks)}. Two defects: an
**unanchored-claim** draft ("fastest available… ≥60%… low-risk", no basis) and a
**dropped-requirement** draft (asked for 3 things, delivers 2). Sonnet, n=5.

**Result** (binary: was the planted defect caught?):

| defect | bare | generic-vague | generic-checklist (C1) | verify (Soul) |
|---|---|---|---|---|
| unanchored claim | 2/5 | 5/5 | 4/5 | 5/5 |
| dropped requirement | 5/5 | 5/5 | 5/5 | 5/5 |

**Verdict — the gate *concept* works; the Soul-specific format is form.** Prompting
*any* check lifts catch-rate on the non-obvious defect (bare 2/5 → ~5/5), so a
completion gate earns its place. **But the Soul checklist does not beat a generic
"double-check carefully" on catch-rate** (both 5/5) — it adds *thoroughness and
legibility* (it itemises each unanchored claim under a named "Anchor" check), which
is form. The dropped-requirement defect was **too easy** (all arms 5/5 — a C2
ceiling, no signal; that task under-discriminated).

Caution worth recording: a keyword-count first pass *looked* like a decisive Soul
win (verify 5.8 ≫ generic 2.6), but that measured **verbosity of flagging, not
catch-rate**. The binary read corrected it. Keyword counts ≠ outcomes.

---

## The unified picture (with the doctrine results in 01)

> Note: this summary is **refined by Measured 4 (the distill probe) below** — item 1
> broadens from "the record" to "the record *and* a small always-on rule-set," both
> carrying project-specific knowledge/conventions. The fuller statement is in
> "The unified thesis, sharpened by this probe" at the end of this file.

Across doctrine (single-shot) and instruments (cross-session), the things that
survive the equal-compute / generic-alternative controls are:

1. **Project-specific knowledge & conventions** carried by the record *and* a small
   always-on rule-set (recall: F038 5/5 vs irrelevant 2/5; distill: the
   counter-default docs-near-code convention) — robust, content-specific, a generic
   equivalent gets it *wrong*. The clearest win.
2. **The anchoring discipline at weak baselines** (doctrine: HR2/G3b on Haiku,
   replicated) — narrow; at mid+ capability a generic check-nudge suffices (the
   verify probe: generic = Soul on catch-rate).

Everything else measured — Council roles / forcing perspectives, the handoff
*format*, the verify *format*, trajectory-reading, compliance-resistance at any
stakes — is **form (legibility), disposition (any long prompt), or compute**. The
equal-compute control caught **four** false positives across the study (trajectory,
compliance-flag, compliance-withhold, and the keyword-illusion verify win).

---

## Measured 4 — `/soul-distill` / the Mind (does compressed doctrine change decisions?)

**Claim:** the Mind — the accumulated record compressed into always-on rules —
helps a session make project-aligned decisions.
**Design:** a decision where the project's convention **contradicts the generic
default** — *"docs live near the code"* (most projects default to a separate `docs/`
tree). A contributor proposes a `docs/architecture/` tree; recommend. Project-aligned
= reject the separate tree for the *convention* (drift); generic = adopt it. Arms:
{Mind (`mind.md`) · nothing · generic-principles (C1) · raw-records excerpt (C1)},
length-matched (~1000–1150w context), Sonnet+Haiku, n=5, isolated dirs.

**Result** (read-classified by the *reason* given — keyword grep was unreliable, it
conflated "reject the tree concept" with "don't create docs *yet*"):

| arm | project-aligned (reject tree, cite convention) |
|---|---|
| **Mind** | ~10/10 — cite Rule 10 / "docs live near code", drift certainty |
| **raw-records (C1)** | ~10/10 — cite the recorded convention |
| **generic-principles (C1)** | ~0/10 — **adopt the tree** (the generic default) |
| **nothing** | mixed — some reject, but via "empty dir / premature", not the convention |

**Verdict — doctrine *content* has real, C1-surviving substance on
convention-transmission, and it corrects a too-hasty cut.** Loading the project's
rules (Mind *or* records) flips a counter-default decision to the project's answer;
a length-matched *generic* principles set gives the **opposite** (default) answer,
so the effect is the project's specific content, not generic wisdom or compute.
This is **not form** — it is the same axis as recall (carrying project-specific
knowledge a model can't derive and a generic equivalent gets wrong). The earlier
"Mind = compressed doctrine, doctrine = form → cut" reasoning was wrong: doctrine is
form on *generic-reasoning* tasks, but it has substance on *transmitting
counter-default conventions*.

**But `Mind ≈ raw-records`** — the compressed Mind transmits the convention no
better (and no worse) than a similar-size raw excerpt. So the *content* earns its
keep; the **Mind/`distill` machinery vs hand-curated seed rules vs the raw records**
is the open question this probe does not settle. **Bound:** the Mind's real
efficiency claim — compress the *whole* (un-loadable) record into a small always-on
budget (SOUL-033) — was not tested; both arms here were already budget-sized. The
probe tested transmission *quality* (compression preserves signal), not the
budget-efficiency that motivates the Mind.

**Moderation (added 2026-06-04, SOUL-133/134 — a three-arm filler control).** Re-run
with a cleaner control — bare / empty-padding (compute) / coherent-irrelevant (distraction)
/ substance — this *docs-near-code* probe proved a **weak** substance vehicle: the
"reject the tree" outcome is partly *derivable* (the frontier model gives it at baseline;
a coherent-irrelevant distractor primed the weak model to re-derive it 5/5), so the binary
does not isolate substance — only the *reasoning* does (the substance arm cites the
specific incident). The original `generic-principles → 0/10` was a **loaded** counter-
distractor (it argued *for* the default), which inflated the gap. The convention KEEP is
real but narrower than 10/10-vs-0/10 implied. Crucially, the **recall** probe above —
an unguessable *fact* a generic equivalent gets *confidently wrong* — was re-run under the
same three-arm control and isolated **cleanly** (record 10/10 vs bare ≈ empty ≈ coherent-
irrelevant 0/10; the coherent filler is harmless because no disposition re-derives a fact
the model lacks, and the frontier *confidently asserts the false negation*). So the KEEP
holds, sharpened: it is for **unguessable** content (a counter-default fact), and the
docs-convention instance was simply too *derivable* to be a clean demonstration.

**Verify form-verdict, three-arm (added 2026-06-05, SOUL-135).** Extending the control to
*Measured 3* (the completion gate above) confirms that section's "gate concept works, Soul
format is form" verdict at the stricter bar: a high-stakes vehicle (ship a payment-rounding
refactor on green unit tests?) ceilinged at **40/40 avoid-trap across all four arms, bare
included** — the gate is *fully derivable*, more so than the docs convention (whose bare sat
at 2/5). The substance arm's only isolable mark is a **citation** (6/10 cells name the
doctrine codes; 0/10 elsewhere); it does not change the decision. So verify sits at the
opposite pole from recall on the same axis: recall carries an *unguessable fact* (clean
isolation), verify records an *already-held disposition* (legibility only). The
domain-saturation bound was then tested (SOUL-136) with a low-stakes vehicle: bare still
withheld 10/10, so "legibility, not behavior" holds off-saturation — the only behavioral
residue is a thin frontier *stabilizer* effect (a coherent distractor eroded Sonnet's
caution 3/5; the doctrine resisted it 5/5). The **handoff** form-verdict was then closed
the same way (SOUL-139, Measured 1 above): the structured cursor ties equal-length prose
(10/10 = 10/10). Both form verdicts now resolve as legibility, not behavior.

### The unified thesis, sharpened by this probe

The split is not "doctrine vs no doctrine." It is **what the content is *for*:**

- **Carries project-specific knowledge / conventions** the model can't derive and a
  generic equivalent gets *wrong* → **real, C1-surviving substance.** Shown twice:
  recall (F038) and distill (docs-near-code). This is the record + always-on rules.
- **Tries to make the model reason better generically** (roles, council, the verify
  checklist's non-anchor parts, handoff format, trajectory, compliance-resist) →
  **form / disposition / compute.** A generic equivalent matches it.

The anchoring discipline sits in the first group at weak baselines. So the system's
durable value is **project-specific-knowledge transmission + the anchor discipline**;
the reasoning-ceremony is form.
