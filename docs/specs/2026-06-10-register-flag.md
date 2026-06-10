# Spec — the Register flag (SOUL-I050)

**Status: DESIGN — implementation lands after the efficacy program's chains finish**
(nothing here may change mid-measurement; the chains use frozen doctrine copies, but
the hold keeps the system stable while it is being measured).

## Problem (SOUL-I050, Body)

Normal session responses drift verbose and jargon-dense enough that the Body invokes
/soul-explain on ordinary updates. Wanted: concise, plain-language responses by
default, with project vocabulary introduced gradually — switchable per project.

## Design (recommendation 1 + 3 from the session discussion)

### 1. The Register line (per-project, one line, zero seed cost)

`/soul-init` asks one new question ("Response register: plain or fluent?") and writes
ONE line into the project's CLAUDE.md, directly below the seed import:

> **Register: plain** — keep responses concise and in plain language; use a Soul or
> project term only when it earns its place, gloss it on first use in a session, and
> introduce vocabulary gradually. (Switch by editing this line; other value: `fluent`
> — full Soul vocabulary, current behavior.)

- Default for NEW inits: `plain` (the Body's stated preference).
- Existing projects: opt in by adding the line (a /soul-init re-run offers it).
- No seed or mind change: the project CLAUDE.md is already always-on for its own
  sessions, so the instruction carries itself. Rule-5 budget untouched.

### 2. Instrument cleanup (the named offenders)

- **skills/soul-resume** step 3: restate in plain language; under a `plain` register,
  say "the current design frame" instead of "the LIVE AL"; the 2–3-line cap stands.
- **hooks/pre-completion-verify.py** REPLY guidance: keep the one-line gate, allow the
  plain wording "— Verified: <what ran>" / "— Not verified: <what's missing>"; the
  structured `Verify: clean/GAP` form remains valid (records/telemetry parse it).
- **skills/soul-capture / soul-next** confirmations: one plain sentence + the ID;
  no field-name recitation.
- **NOT changed:** record FILE formats (witness/handoff/findings) — they are
  next-session artifacts, not Body-facing prose, and parsers/conventions depend on
  them. The handoff cursor stays structured.

### 3. What "plain" demands of narration (the register's meaning)

Lead with what happened in ordinary words; one idea per sentence; a project term only
when the plain phrase would be longer or lossier, glossed on first use ("the fence —
the warning comment at the code site"). Numbers and file paths stay precise. This is
a register, not a content cut: anchors, caveats, and asks survive; ceremony does not.

## Measurement (light, honest)

After 2–3 weeks of real use: count /soul-explain invocations per 10 sessions in
plain-register projects vs before (the .soul/events.jsonl + transcript record makes
this countable). If the rate does not drop, the register is the wrong fix — revisit
SOUL-I050 rather than adding more text.

## Rollout

1. Land this spec (now). 2. After the efficacy chains complete: edit soul-init,
soul-resume, soul-capture, soul-next, the hook REPLY text. 3. Add the Register line
to this repo's own CLAUDE.md (dogfood). 4. Offer the line to the three reference
projects at their next session.
