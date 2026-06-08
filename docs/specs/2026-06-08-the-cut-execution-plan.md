# The Cut — execution plan (Soul System → 1.0)

Status: **EXECUTED 2026-06-08 → 1.0** (SOUL-146). Grilled with the Body (/grill-with-docs),
both pre-1.0 gates passed (Gate-1 orientation 6/6 across both models; Gate-2 hook firing), then
executed. **One mid-execution coherence catch:** the dangling-reference sweep found that cutting
`council-synthesis.md` also dropped the **amendment process** (load-bearing for the kept
`amendments/`/`findings/` records — a 4th hard requirement the SOUL-145 pass missed); extracted
to `operations/amendment-process.md`. Final surface: **8 commands, 6 operations files.**
Decision input: `docs/study/03-leandown.md` (the measured KEEP/CUT/MERGE matrix).
Hard constraints: witness **SOUL-145** (the coherence pass — three load-bearing carry-forwards).
Version: **1.0** (Body-set, from `0.3.0`).

## Resolved in grilling (2026-06-08, /grill-with-docs)

- **Capture merge = `soul-capture <mode>`.** `witness`/`idea`/`finding` merge into ONE
  command; the **mode token is the first arg** and selects friction + target store + format:
  `idea` → frictionless `ideas.md`; `witness` → light scaffold + I027 re-read-verify →
  `witness.md`; `finding` → the *earned* scaffolder → `findings/open/` (formats a decided
  graduation, never auto-promotes). The token IS the ratchet made visible (typing `finding`
  is the deliberate earning act). No-mode invocation asks rather than guesses. The
  friction differential (Mind contrast case; I024) is thus preserved inside one command.

- **Keep thin `soul-handoff` + `soul-resume`; drop the cursor-format ceremony.** Reversal of
  the matrix's "merge to convention." Basis: the *format* is inert (SOUL-139, measured), but
  the *activation* (handoff flushes volatile state to records first; resume forces
  load-restate-continue — used to open THIS session, worked) is the value. Kept on **Body
  lived-intuition + asymmetry** (cheap to keep, expensive to wrongly cut — re-derivation is
  the failure the system exists to prevent), explicitly **not measured**. Drop the elaborate
  `.soul/handoff.md` field structure → a rich plain summary. `resume-cost.py` is experiment
  instrumentation, not needed for resume to work → still cut. Flagged revisitable.

- **Read-only QoL cluster resolved.** `soul-help` → **KEEP, reframed** as a `--help`-style
  intro/onboarding to the Soul System (not a command-lister). `soul-explain` → **KEEP, thin**
  — a *present-state guardrail* (describe-don't-decide; stops the agent re-planning/inventing
  direction; Body lived-value). `soul-roles` → **CUT** (little to observe once the chamber is
  a one-liner). `soul-tasks` → **KEEP, RENAMED `soul-next`** — a *forward guardrail* (reconcile
  vs records + tiered now/next/later; stops invented direction; pairs with `soul-explain` as
  present↔next). Standard for all keeps: defended unique/activation value, not a target count
  (running tally ~8 commands, from 16 — each earned).

- **`soul-expand` + `soul-ask-body` → CUT the commands, KEEP as seed one-liners.**
  Evidence-backed (not reflex): both commands have **zero logged invocations**
  (`events.jsonl`, `role-queries.jsonl` empty), yet their disciplines (Counterweight F014,
  Body-Input F037) **fire repeatedly from the seed §Activation Disciplines text** (witness:
  "Counterweight Rule fired structurally," "Body-Input Obligation honored"). The command form
  is dead weight; the seed line is the live mechanism. Consistent F046/F047 sub-decision:
  the seed carries only the **two graduated** disciplines; F046/F047 stay open findings until
  earned (Rule 7) — no ungraduated disciplines in the always-on layer.

- **`soul-council` → folded into a `council` lens-mode of `soul-explain`.** Cut the standalone
  command + `council-synthesis.md` doctrine. The surviving value (multi-angle *sense-making* —
  what the 4 `councils/` artifacts actually delivered: consolidation, framing) becomes
  `/soul-explain council`: **one agent, one pass, multiple lenses** (Skeptic/Advocate/
  Accountant angles), read-only. Dodges SOUL-119's measured failure (lossy synthesis was the
  multi-*agent* version; lenses-in-one-pass don't drop findings) and adds no new command
  surface. Does NOT cover multi-angle deliberation toward a hard decision — that's
  `brainstorming`/`grill` territory (no real loss). **Dependency surfaced:** the lens-mode
  needs a *lens roster* (which roles, 1 line each); source it from a kept slim role roster —
  ties to the `the-soul.md` decision below (keep a slim deep-reference vs delete).

- **`soul-distill` → KEEP thin (tool) + trigger on `soul-next`.** The matrix bundled the
  untested *auto-maintenance concept* with the *command*; the command is actually a
  Body-invoked, draft-only, schema-aware curation aid (it built the current `mind.md`). Since
  `mind.md` is kept, it needs maintenance — but a command you must *remember* doesn't solve
  "will anyone remember" (that's exactly why expand/ask-body had zero invocations). So the
  activation is a **trigger, not memory**: `soul-next` compares `mind.md`'s last-distilled
  marker vs findings-accumulated-since and surfaces "consider re-distilling (N new findings)"
  in its tiered view (same shape as the handoff cursor flagging un-upstreamed findings; Rule
  6 — gate fires where the failure happens). Keep `/soul-distill` as the tool that does the
  fold correctly (force-preservation is the hand-botched part). **This DISSOLVES Conscious
  Trade #1** (see revised below).

- **Skills catalog → DEFERRED to post-1.0 (#1 fast-follow); `soul-skill` → CUT entirely.**
  Investigation: `skills/` is EMPTY (just `.gitkeep`+README), `soul-skill` has produced
  nothing (unused, like expand/ask-body). The matrix's "cut wrapper, keep output" has no
  output to keep. A catalog's value is its content; shipping it empty = vapor, seeding it now
  = un-earned entries. So defer the catalog (SOUL-120's measured value is real → record as the
  top post-1.0 build, populate when a genuine verified success earns the first entry). Cut
  `soul-skill` outright: the **record already captures what happened**, and **generic
  skill-authoring (`write-a-skill`/`skill-creator`) writes a skill when truly needed**
  (Soul-composes-not-replaces). `skills/` keeps a short README marking the deferred intent.

- **Philosophy layer resolved.** `the-soul.md` → **KEEP** as the on-demand deep reference
  (it is ALREADY not auto-loaded → zero per-session cost; the matrix's "get the chamber out
  of always-on" is already satisfied). Slim/update it to the lean architecture (drop cut-
  command rationale, reframe council as the lens-mode, update §Mind/§Seeding), but keep the
  **role roster** (supplies `/soul-explain council`'s lenses — closes that dependency) + the
  failure vocabulary / tensions / obligations (the depth backstop). `the-commons.md` → **CUT**
  (Body call, default-simplicity — a slow quote-reference never reached for; not load-bearing).

- **`adr-format.md` → CUT (migrate A009 note); `code-markers.md` → FOLD to a seed line.**
  adr-format: the repo uses `amendments/`+`docs/specs/` for its own decisions (no `docs/adr/`;
  the only ADRs are experiment vehicles) → it documents a record type outside the lean core;
  cut it, but **migrate the A009 "self-contained = correctness, not hermetic" note** to the
  handoff doctrine. code-markers: the completion hook already hardcodes TODO/FIXME/DEBT/HACK
  and docs-near-code is already Mind Rule 10 → 93 lines duplicate a gate check + an existing
  rule; fold the marker list + docs-near-code into one seed line, cut the file.

- **Adopter migration → RESOLVED by checking (concern collapsed).** Verified: (1) **no adopter
  symlinks `commands/`** (only venv noise) and `install.sh` doesn't even distribute commands
  (`cp -r operations/.` only) → **hard-deleting cut commands breaks nothing; no tombstones.**
  (2) Adopters tie to the seed via **absolute-path `@import`** (`@/mnt/d/Projects/Soul-System/
  operations/CLAUDE.md`) → the lean-seed rewrite **propagates live** (the design), safe because
  the three hard requirements are mandated. (3) Adopters `@import` their *own* local `mind.md`,
  not this repo's. **Imposed rule: rewrite the seed IN PLACE at `operations/CLAUDE.md` (never
  move/rename)** or the absolute-path imports break. Gate-1 (orientation) doubles as the
  adopter-safety check.

- **`soul-verify` command → CUT; keep the hook.** Same shape as expand/ask-body: the
  command is a *manual* entry point (0 invocations) duplicating the **automatic Stop hook**
  (`pre-completion-verify.py`) that actually fires the gate (caught SOUL-140 + the SOUL-144
  over-claim this session). The gate stays where it fires — the hook + leaned
  `completion-gate.md`. Drops commands 9 → 8.

- **Always-on layer = TWO artifacts, not one.** The lean seed (orientation) **+ a slimmed
  `mind.md`** (kept for its structure). `mind.md` is **NOT** retired/absorbed. Slim it to the
  load-bearing **rules + the contrast cases**; drop the meta-structure prose, the
  incompressible-residual section, and the distillation log. Rationale: the contrast cases
  (e.g. F031-vs-F030, default-simplicity↔outward-reach) are the least-compressible,
  highest-transmission part (Rule 13 — preserve force; SOUL-124 convention-transmission);
  flattening them into seed bullets is the exact failure the coherence pass flagged. Cost:
  two always-on files, a real tension with the "single small core" the matrix imagined —
  accepted.

---

## Problem (two levels)

- **Immediate:** translate the `03-leandown` matrix — which is a *recommendation* — into
  an *executable, reviewable* sequence of file changes that shrinks ~16 commands + 3
  doctrine layers to a small validated core, **without dropping load-bearing doctrine** and
  **without surprise-breaking the 8 adopters**.
- **Larger system:** the study measured where the value actually is (records, anchor
  discipline, the completion gate's *activation*, a tested skills catalog) and where it is
  ceremony the frontier already matches. The Cut graduates the *validated* core to a stable
  **1.0** while keeping the evolution-fuel loop (reference-project upstreaming) intact — the
  loop that produced F046/F047/SOUL-144/145 *during this very arc*.

Coherence check (SOUL-145): these two levels are consistent — the Cut removes ceremony, not
the mechanism that lets the system keep learning. The risk is *silently* cutting a
load-bearing item that *looks* like ceremony. This plan exists to make that impossible.

---

## Post-grilling end state — the 1.0 surface

**Commands: 16 → 8** (each earned; see honesty note).
`soul-init` · `soul-capture <idea|witness|finding>` · `soul-handoff` · `soul-resume` ·
`soul-explain` (+ `council` lens-mode) · `soul-help` (reframed → system intro) · `soul-next`
(ex-`soul-tasks`; carries the distill-staleness trigger) · `soul-distill` (thin tool).
**Cut:** verify (→ hook), council, expand, ask-body, roles, skill (+ witness/idea/finding
merged away). The completion gate survives as the **hook** + leaned `completion-gate.md`.

**Always-on layer: lean seed (`operations/CLAUDE.md`, in place) + slimmed `mind.md`.**
Seed = First Principle/AL gate · Anchor Obligation · expansion + ask-Body one-liners · upstream
obligation · marker/docs-near-code one-line · record pointers · one-line "roles exist" → the
deep reference. `mind.md` = rules + contrast cases (slimmed).

**Records: unchanged** — witness/findings/ideas/amendments.

**Operations: 10 → 4** — KEEP `experiment-harness.md`, `witness-log-format.md`,
`reference-repository.md`, `completion-gate.md` (leaned). CUT `council-synthesis.md`,
`event-standard.md`, `problem-slot-template.md`, `adr-format.md` (migrate A009 note),
`code-markers.md` (fold to seed line).

**Philosophy: `the-soul.md` kept** (already on-demand; slimmed; supplies council lenses + depth)
· **`the-commons.md` cut.**

**Hooks: 2 → 1** — `pre-completion-verify.py` leaned (anchor check load-bearing); `resume-cost.py` cut.

**Deferred to post-1.0 (#1 fast-follow):** the tested skills catalog (SOUL-120 value, populate when earned).

**Honesty note (the central tension, named).** The matrix imagined ~5–6 commands; we landed at
**8**. The extra ~2–3 (`handoff`, `resume`, `explain`, `next`) are **activation/guardrail keeps
on Body lived-value, not measurement** — the "scaffolding that makes a good practice reliably
happen" counterweight the study itself allows. The default-simplicity alternative (cut them per
the matrix) was on the table; the Body chose activation-value. Defensible and conscious — but
this is the lean-toward-activation, not the maximal cut.

## Abstraction layer

- **What varies:** each instrument's *form* — KEEP / LEAN / MERGE / CUT.
- **What decides the variation:** the Cut's rule — *measured value (A/B+C1) or a
  clearly-argued unique value a generic equivalent does not provide*; PLUS SOUL-145's three
  hard requirements; PLUS Body input on the skills catalog and the keep-but-alter commands.
- **What cannot vary (invariants):**
  1. The **records** core (witness/findings/ideas) and its invariants — append-only,
     sequential IDs, the **I027** re-read-verify concurrent-writer protocol, the
     **earned-finding** gate (Rule 7).
  2. The **completion gate's activation** — it fires as a hook, not prose.
  3. The three **SOUL-145 carry-forwards** below.

---

## The three HARD REQUIREMENTS (SOUL-145 — non-negotiable carry-forwards)

These sit in the matrix's "everything else → cut or folded" bucket but are load-bearing,
unguessable doctrine — not ceremony. The lean seed **must** carry each, or the plan is rejected:

1. **The reference-project upstream obligation** (`seed §Reference Projects` +
   `operations/reference-repository.md`). The dogfood→findings→doctrine loop. Adopters
   reference it directly (registry). → Folded into the lean seed as a short rule + pointer.
2. **The F038 experiment-harness fact** (`operations/experiment-harness.md`): cross-project
   `@import` silently confabulates ~43%; inline content + sentinel-test loading is
   non-optional. An unguessable fact (Rule 13) that re-bites the next measurement session if
   lost. → **Kept as a file**, cited from the lean seed, preserved *with its force* (the
   incident + the explicit negation), not just the proposition.
3. **The witness invariants** (`operations/witness-log-format.md`): append-only + sequential
   IDs + I027 re-read-verify + earned-finding gate. → Kept; confirm I027 + earned-finding
   ride along in the leaned record doctrine.

## The two CONSCIOUS TRADES (SOUL-145 — named, not silent)

1. ~~**No re-distill mechanism after the cut.**~~ **DISSOLVED in grilling (2026-06-08).**
   The earlier framing assumed `/soul-distill` was cut and `mind.md` hand-edited. Resolved
   instead: keep `/soul-distill` thin as the curation tool + `soul-next` carries a staleness
   trigger. Re-distillation is tool-assisted and *prompted*, not manual-and-forgotten. No
   trade remains here.
2. **Shared-language thinning.** The role chamber → a one-liner. Behaviour is unaffected
   (A017: roles = legibility, not behaviour-lifting), but the named vocabulary you and the
   agent share gets thinner. This spends the *asserted-unmeasured* legibility residual
   knowingly.

---

## The file-level cut list

Verdict = the `03-leandown` matrix. Action = the concrete file operation. **[BODY]** marks a
decision point flagged for your input (skills + keep-but-alter).

### Commands (`commands/` — 16 today)

| Command | Verdict | Action |
|---|---|---|
| `soul-init` | KEEP | keep (trivial, needed for setup) |
| `soul-witness`, `soul-idea`, `soul-finding` | KEEP, MERGE→1 | merge into one `soul-capture` command; **preserve the earned-finding gate** as a sub-mode |
| `soul-verify` | ~~KEEP~~ **CUT (Resolved)** | command has 0 invocations; the **automatic Stop hook** already fires the gate. Cut the command; keep hook + leaned `completion-gate.md` (anchor check load-bearing) |
| `soul-handoff`, `soul-resume` | MERGE→convention | drop the cursor *ceremony*; keep the *habit* of a rich handoff note as a seed one-liner. **[BODY]** — or keep a thin resume command if you value it (study: retrieval untested) |
| `soul-expand` | MERGE→seed line | delete command; fold "what am I missing / what could this become?" into the seed |
| `soul-ask-body` | MERGE→seed line | delete command; fold the ask-the-Body nudge into the seed |
| `soul-council` | CUT | delete command + `operations/council-synthesis.md` |
| `soul-roles`, `soul-tasks`, `soul-help`, `soul-explain` | CUT from core | delete (optional QoL; not part of a lean core). **[BODY]** — keep any as personal convenience? |
| `soul-skill` | CUT wrapper, KEEP output | delete the wrapper command; its tested know-how feeds the catalog below |
| `soul-distill` | OPEN / lean | delete the *machinery*; fold its load-bearing rules into the seed by hand (Conscious Trade #1) |

### Tested skills catalog **[BODY — primary decision point]**

The matrix's one *new* KEEP: a lean, selective, tested skills catalog + what/when routing
(SOUL-120 — curated which-to-deploy beats self-pick at weak-model × tight-budget). This is
where you said you want input. **Open for your decision:**
- which skills enter the v1 catalog (each entry earned via a verified success);
- the catalog's *form* (a flat index file? per-skill SKILL.md? a routing table?);
- whether any *current* command survives *as* a catalog entry rather than being cut.

I will draft a *candidate* catalog for you to edit, not a final one.

### Operations doctrine (`operations/`)

| File | Action |
|---|---|
| `CLAUDE.md` (the seed) | **rewrite** as the lean seed (see next section) |
| `experiment-harness.md` | **KEEP** (Hard Req #2) |
| `witness-log-format.md` | **KEEP** (Hard Req #3 — records core) |
| `reference-repository.md` | **KEEP / fold** (Hard Req #1 — upstream loop) |
| `completion-gate.md` | **KEEP, LEAN** (the gate doctrine the hook cites) |
| `council-synthesis.md` | **CUT** (council cut) |
| `event-standard.md` | **CUT/fold** (tied to soul-roles observability, which is cut) |
| `code-markers.md` | **[BODY]** keep as a thin convention (Rule 10 docs-near-code) or fold to a seed line? |
| `adr-format.md` | **[BODY]** keep only if ADRs remain a record type (they were the longitudinal vehicle, not clearly a kept record) |
| `problem-slot-template.md` | **CUT/fold** (situational procedure; the AL gate covers the intent) |

### Philosophy (`philosophy/`)

| File | Action |
|---|---|
| `the-soul.md` (700-line chamber) | **LEAN to a one-liner in the seed** + **[BODY]** keep the full text as an on-demand historical/deep-reference artifact, or delete and rely on git history? |
| `the-commons.md` | **[BODY]** needs-review — not in the matrix; confirm intent before touching |

---

## The lean seed (target `operations/CLAUDE.md`)

Always-on, small. Contents:
1. **The First Principle / AL gate** — "understand the abstraction before the instantiation."
2. **The Anchor Obligation** — the one reasoning-substance (absolute claims need a valid
   external anchor; internal coherence is not truth).
3. **The load-bearing project conventions** — kept in the **slimmed `mind.md`** (rules +
   contrast cases), `@import`ed after the seed; not flattened into seed bullets (Resolved
   2026-06-08). The seed points to it.
4. **One-line expansion nudge** (ex-`soul-expand`) and **one-line ask-the-Body nudge**
   (ex-`soul-ask-body`).
5. **The reference-project upstream obligation** (Hard Req #1) — short rule + pointer.
6. **Pointers into the records** (witness/findings/ideas) and to the kept operations files
   (`experiment-harness.md`, `witness-log-format.md`, `completion-gate.md`).
7. A one-line acknowledgement that perspectives/roles exist (no chamber prose).

Durability test for the draft: **two parties reading the lean seed arrive at the same
meaning** (Rule 11). Verified empirically by the orientation gate below.

---

## Pre-1.0 GATES (must pass before graduation)

1. **Empirical fresh-agent orientation test** (SOUL-145 deferred item). Give a fresh `claude
   -p` agent *only* the drafted lean seed + a representative task; confirm it orients
   correctly (names the AL, anchors a claim, checks the record, asks the Body when needed).
   Run with-record inlined, never `@`-imported (F038). n≥3, read-scored. A drift here means
   the lean seed dropped something orienting — fix before cutting.
2. **Completion-hook firing test** (the one real-code change). After leaning
   `hooks/pre-completion-verify.py`, feed it a known over-claim and confirm it still fires
   and catches the anchor gap. A hook that silently stops firing is the worst regression —
   the study's activation result leans on it.

---

## 1.0 mechanics

- `install.sh`: `SYSTEM_VERSION="0.3.0"` → `"1.0.0"`; the `.soul-version` write follows.
- **Adopter migration (opt-in, no surprise-break):** adopters are version-pinned / symlink
  per Rule 9. **[BODY decision]** — deleting a *symlinked* command breaks any adopter that
  symlinks it. Options: (a) coordinate-migrate the 8 adopters, (b) leave thin "retired"
  tombstone files pointing at the convention, (c) confirm adopters copy (not symlink)
  commands so deletion is inert. Resolve before any command deletion.
- **A closing Finding** for the Cut itself (the reference-project obligation applies to the
  arc): what the lean-down changed and what it bet.

---

## Execution order (reversible-first; irreversible last)

1. Draft the lean seed + leaned `completion-gate.md` + the candidate skills catalog
   (**reversible** — new/edited files, nothing deleted).
2. **Body review** of the draft (the skills + keep-but-alter decisions land here).
3. Run **Gate 1** (orientation) and **Gate 2** (hook firing). Fix drift.
4. Lean `hooks/pre-completion-verify.py`; merge the capture commands; write seed one-liners.
5. Resolve the **adopter-migration** decision.
6. **Irreversible last:** delete the cut commands + cut operations files; lean
   `the-soul.md`; bump the version. (git history is the safety net, but treat as one-way.)
7. Write the closing Finding + handoff.

---

## Open questions / BODY decision points (consolidated)

- **Skills catalog** — contents, form, and which (if any) current commands survive *as*
  catalog entries. *(You flagged this; I'll draft a candidate.)*
- **Keep-but-alter commands** — `soul-resume` (thin command vs convention?), the read-only
  QoL set (`roles`/`tasks`/`help`/`explain` — delete all, or keep any?).
- **`adr-format.md` / `code-markers.md`** — keep as thin conventions or fold to seed lines?
- **`the-soul.md`** — keep full text as on-demand deep-reference, or delete (git history)?
- **`the-commons.md`** — confirm what it is and whether the Cut touches it.
- **Adopter migration** — coordinate, tombstone, or confirm-copy (above).

---

## What is NOT in this spec

- **Building a router** for the skills catalog — the catalog win is an oracle upper bound;
  a built router is a later, separately-justified step (study §3 risk (d)).
- **A replacement for auto-distill** — Conscious Trade #1 accepts hand-curation for now.
- **The actual lean-seed prose** — drafted in step 1, reviewed in step 2; this spec is the
  plan, not the artifact.

---
**Source:** Built by the Architect from `docs/study/03-leandown.md` (the measured matrix) +
witness SOUL-145 (the coherence pass). **Adopted:** draft 2026-06-08. **Status:** awaiting
Body approval. **Sub-class:** PROCEDURE.
