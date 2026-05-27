---
description: Body-invoked pre-delegation check — agent surveys its current state and surfaces pending Body-only inputs (heuristic hints, strategic intent, preference between technically-valid paths, private knowledge) before pushing past them. The knowledge-axis sibling of /soul-council (invocation) and /soul-roles (observability); pairs with SOUL-A012 §Body-Input Obligation (the recommendation-time doctrine). Use when Body is about to authorize autonomous work, before a Scope Manifest, or any moment where the agent might barrel past a dependency only the Body can resolve.
---

# /soul-ask-body — surface pending Body-only inputs

A Body-invoked check the agent runs against its current state to surface
questions only the Body can answer — heuristic hints, strategic intent,
preference between technically-valid paths, private knowledge. SOUL-F037
named these four kinds; the REF-02 M8 / M9 incidents are the empirical
precedent (AI declared infeasibility / sketched a too-narrow architecture;
Body's interjection changed the outcome materially).

The knowledge-axis half of the SOUL-F014 expansion-gap response: F014
established that auto-detection of activation moments is intrinsically
impossible. Same insight applies here — the AI cannot reliably auto-detect
when an input is Body-only. So this is **(β) Body-invoked pre-delegation
check**, paired with **(γ) SOUL-A012 §Body-Input Obligation** (the seed
doctrine that fires at recommendation-time). Together: pre-delegation
survey + recommendation-time discipline. Neither auto-fires.

## What this is NOT

- **Not auto-firing.** F014's PRE-MORTEM rules it out. Body invokes; that
  is the contract.
- **Not a substitute for (γ).** A012 §Body-Input Obligation is the
  recommendation-time discipline (the AI names the Body-only dependency
  whenever it's about to ship advice that depends on one). This command
  is the *pre-delegation* survey — different moment, same problem.
- **Not a finding scaffolder.** Output is witness-only. If a Body answer
  reveals a load-bearing pattern, the Body invokes `/soul-finding`
  separately. Same anti-inflation discipline as `/soul-council`.
- **Not a flooding interface.** Default cap is one question per F037 kind
  in scope. Surveys must be concrete-decisions-only; generic "do you have
  any thoughts?" is not allowed.
- **Not exhaustive.** The agent cannot prove survey completeness — Body-
  only inputs the agent has not noticed remain undetected by construction.
  The "may have missed X" caveat is mandatory, not politeness.

## What to do

1. **Parse scope** (optional argument):
   - Default: the current active work — live AL, in-flight task, named
     upcoming decision.
   - `for <finding-id>` — scope to a specific finding's resolution.
   - `for next <N> turns` — scope to immediately upcoming work.
   - `for session` — broader survey across the session's open threads.

2. **Survey honestly against F037's four kinds.** For each, ask whether
   the current work has a load-bearing dependency the Body is the only
   viable source for:
   - **Kind 1 — Heuristic:** "Am I about to declare something infeasible /
     not found / done based on a search the Body might know to extend?"
     (REF-02 M8 shape: 'Wayback' was the heuristic the Body had, the AI
     didn't.)
   - **Kind 2 — Strategic intent:** "Am I making design choices whose
     right answer depends on multi-step direction I haven't been told?"
     (REF-02 M9 shape: 'vast number of facilities' was the multi-step
     intent that reframed the ADR.)
   - **Kind 3 — Preference:** "Are there multiple technically-valid paths
     where my choice is actually the Body's call?" (This session's F038
     amendment shape choice — operations-level vs seed/Mind — was a Kind 3.)
   - **Kind 4 — Private knowledge:** "Am I assuming things about data,
     org, in-flight context, prior decisions, or external constraints I
     can't actually see?"

3. **Compose questions** — each tagged with its kind, each tied to a
   specific in-flight decision or work-step. Generic surveys are
   forbidden. If no concrete question surfaces for a kind, write nothing
   for that kind (and name the absence in step 5).

4. **Surface to Body via `AskUserQuestion`** when interactive (or plain
   prose questions otherwise). Cap: one question per kind by default —
   four total maximum. If the scope truly warrants more, name the
   over-cap explicitly and ask whether to proceed with all or batch.
   Present alternatives neutrally; no leading phrasing that elicits
   confirmation of the agent's preferred answer (Skeptic implicit at
   compose-time).

5. **OR report "no pending Body-only inputs at this scope"** with a
   one-line caveat naming what was surveyed and where the agent may
   have missed something. Survey-completeness cannot be proven by the
   surveyor; the caveat acknowledges that explicitly. Example:
   > *"No Kind 1–3 questions surfaced for the next 3 turns. Kind 4 not
   > surveyable from inside (I cannot enumerate what I don't see) —
   > Body may have private context the survey missed."*

6. **Record the invocation + answers in the witness — mandatory.** A
   short SOUL-XXX entry tagged TYPE: *Council Note — Advocate
   (knowledge-axis check fired)* or similar, naming:
   - the scope queried,
   - the questions surfaced (or "none"),
   - the Body answers,
   - the resulting course-change (if any).
   Without this step the answer evaporates — the witness lock is the
   anti-pollution guard (SOUL-F022 spirit).
   **I027 protocol — re-read-verify before write.** Scan
   `^ID: +SOUL-\d+` right before the append; if your assigned ID is
   taken, increment and retry; three collisions in a row → stop and
   tell the Body.

7. **Use the answers immediately for the work in scope.** The whole point
   is that the answer changes what the agent does next; it is not
   collected for later. If the answer changes scope materially, restate
   the new scope before continuing.

8. **No graduation.** This command produces no findings and no
   amendments. If the answers expose a finding-worthy pattern, the Body
   invokes `/soul-finding` as a separate, explicit step.

## Output sketch

```
/soul-ask-body for next 3 turns

Surveying current state for Body-only dependencies...

3 pending Body-only inputs detected (1 per kind, Kind 4 absent):

[Kind 1 — Heuristic]
  Context: about to declare a cross-validation source unavailable.
  Question: any external archive you'd extend the search to that I
            wouldn't have reached for? (e.g. a Wayback / private mirror
            / paper-only source).

[Kind 2 — Strategic intent]
  Context: about to draft an ADR scoped to one facility.
  Question: is "this facility" the intended scope, or is there a
            broader multi-facility intent I should reframe to?

[Kind 3 — Preference]
  Context: two technically-valid amendment landings (operations vs
           seed/Mind). Both work.
  Question: which footprint do you want — lighter (operations) or
            always-on (seed)?

(Kind 4 absent: nothing I can see suggests a private-knowledge
dependency in this scope. I cannot enumerate what I don't see —
flag if I'm missing something.)

Body answers each? Or skip?
```

## Failure-mode guards

| Failure | Guard |
|---|---|
| **Over-asking** — every micro-decision surfaced as a Body-only question | Concrete-decisions-only rule. Each question must name a SPECIFIC in-flight work item; generic survey questions are forbidden. Default cap: one per kind. |
| **Under-asking** — agent misses the Body-only nature of a question | Mandatory "may have missed X" caveat in step 5. Kind 4 (private knowledge) is structurally hardest to survey; name that explicitly. (γ) doctrine fires AGAIN at recommendation-time per A012, providing a second chance. |
| **Faux questions** — phrased to elicit confirmation of the agent's preferred answer | Questions must present alternatives neutrally; no leading phrasing. Skeptic implicit at compose-time; if you find yourself writing "should I X (which is clearly right)?", rewrite. |
| **Ceremony** — invoked routinely as theatre | Default scope is bounded (current work / next N turns / one finding); broader scopes earn-their-place. If invoked for trivial work, Steward flags it in the witness entry. |
| **Body-input pollution** — Body answers in passing, agent forgets to record | Step 6 witness entry is MANDATORY, not optional. Verifiable retrospectively; future Cartographer can trace what was asked vs what got recorded. |
| **Detection-problem creep** — temptation to make this auto-fire | NO. F014's structural insight applies: auto-detection of Body-only-input-needed is intrinsically unreliable. (γ) at recommendation-time is the second fire; (β) is this pre-delegation check; neither auto-detects, both rely on explicit invocation/discipline. |
| **Survey-completeness illusion** — agent claims a clean survey without caveat | The caveat in step 5 is non-optional. "No pending Body-only inputs" without the "what I may have missed" line is Coherent Falsehood (A010) on survey scope. |
| **Mishandling the four kinds as a checklist** — agent walks all four mechanically and surfaces nothing | The four kinds are FRAMING, not a quota. If none surface for the current scope, report none with the caveat — do not invent questions to fill all four slots. |

## What not to do

- Do not auto-fire. Body invokes; that is the contract.
- Do not skip step 6 (witness recording). The answer evaporates without it.
- Do not skip the I027 re-read-verify protocol on the witness write.
- Do not present leading questions. Alternatives must be neutral.
- Do not survey beyond the scope without naming the over-cap.
- Do not graduate the output to a finding. Separate Body decision via
  `/soul-finding`.
- Do not claim survey completeness. Name the limit explicitly.
- Do not mechanically populate all four kinds. The kinds are the framing;
  empty kinds are honest output.

---

**Source:** Built by the Artificer for SOUL-F037 (the failure pattern + the
instrument candidate it named) and the SOUL-F014 expansion-gap response
cluster on the knowledge axis; specced 2026-05-26 at
`docs/specs/2026-05-26-soul-ask-body-design.md` (Cluster 1 design beat,
third sibling); pairs with `/soul-council` (invocation), `/soul-roles`
(observability), and SOUL-A012 §Body-Input Obligation (the
recommendation-time doctrine line — the (γ) half this command's (β)
half completes). Empirical precedent: REF-02 M8 (Wayback heuristic Body
had, AI didn't); REF-02 M9 (multi-facility intent Body had, AI didn't).
This session's F038 amendment shape choice (operations vs seed) is the
in-project Kind 3 dogfood. **Adopted:** 2026-05-26. **Status:** active
— MVP. Tier 3 validation: (a) simulate the REF-02 M8/M9 scenarios —
would `/soul-ask-body` have surfaced Wayback / the multi-facility intent?
(b) pair with the next Scope Manifest — does it surface real
pre-delegation questions or return "none" trivially? (c) doctrine fire-
rate at recommendation-time — healthy band is some-but-not-all over 10
recommendation-shaped outputs.
