# Contributing

Contributions to the Soul System are welcome.
They are also held to a standard.

The standard is not high to discourage contribution.
It is high because the philosophy earns its evolution through honest evidence
from real use — not through good intentions, clever reasoning, or enthusiasm.

---

## What Qualifies as a Contribution

**Findings**
Something observed during a real run that matters but does not yet
warrant changing the Soul. Findings are the most common and most
valuable contribution. They are the raw material the Council works from.

**Proposed Amendments**
A change to a canonical document — the Soul, the Commons, an operational
document — supported by Witness log evidence and the amendment questions answered.

**Skills**
A compressed, reusable activation of a specific Council role.
Must have been tested in at least one real run.
Must produce the output the role is supposed to produce.

**Hooks**
An automatic trigger definition for Claude Code or compatible environments.
Must specify the condition, the action, and the expected output.
Must have been tested.

**Commons Entries**
Outside wisdom that illuminates something the Soul reaches for.
Must include source, date, and why it belongs here.
See `the-commons.md` for the entry format.

**Registry Entries**
A record of a project that used the system.
Domain, system version used, brief description of the run,
and any findings or amendments that came from it.

---

## What Does Not Qualify

- Proposed changes without Witness log evidence
- Amendments that cannot answer all three amendment questions
- Skills or hooks that have not been tested in a real run
- Commons entries without source and context
- Suggestions based on reasoning alone —
  however compelling the reasoning, it is not evidence

---

## How to Submit

**1. Open an issue first**
Describe what you found, what run it came from, and what you are proposing.
This starts the deliberation before the pull request.

**2. File your Witness log entries**
Anonymize project-specific details if needed.
The entries must be recognizable as genuine Witness log entries —
brief, factual, specific, no editorializing.
Use the format in `witness-log-format.md`.

**3. For proposed amendments — answer the amendment questions**

Include in your submission:

```
AMENDMENT QUESTIONS

Evidence:
  Which Witness log entries demand this change?
  [List entry IDs or paste anonymized entries]

Necessity:
  What in the current document does this extend, refine, or correct?
  Why is the current version insufficient on this point?

Coherence:
  Does this contradict anything else in the Soul System?
  If yes — which is more true and why?
```

**4. Submit a pull request**
Target the appropriate folder:
- `amendments/proposed/` for Soul or operational document changes
- `skills/` for new skills
- `hooks/` for new hooks
- `philosophy/the-commons.md` for Commons entries
- `registry/` for registry entries

**5. Participate in deliberation**
Maintainers will enact the Council synthesis process.
You may be asked to answer follow-up questions.
You may receive a Return — not a rejection.
A Return means the contribution needs more evidence or more thinking.
Respond to Returns honestly. Do not argue. Find more evidence.

---

## Amendment Naming Convention

```
amendments/proposed/[DOMAIN]-A[NNN]-[brief-description].md
amendments/accepted/[DOMAIN]-A[NNN]-[brief-description].md
amendments/returned/[DOMAIN]-A[NNN]-[brief-description].md
```

Example:
```
amendments/proposed/THERMAL-A001-partial-domain-coverage-discipline.md
```

---

## The Contributor's Obligation

You are not submitting a feature request.
You are submitting evidence to a deliberative process
that governs a living philosophy.

That means:
- Be accurate. Do not editorialize your Witness entries.
- Be honest about what your run actually produced.
- A messy run with a rich log is more valuable than a smooth run with none.
- Accept Returns gracefully. The Council is not rejecting you.
  It is asking for more evidence before changing something that matters.

The Skeptic will challenge your submission.
That is not hostility. It is the system working correctly.

---

## First Contribution Recommendation

If this is your first run, submit a registry entry and one or two Findings
before attempting a proposed amendment.

Registry entries and Findings have lower friction.
They help you learn the contribution process before
attempting to change the canonical documents.

They are also genuinely valuable — the Cartographer and Archaeologist
need the registry to map where the system has been used.

---

*Contributing version 1.0*
