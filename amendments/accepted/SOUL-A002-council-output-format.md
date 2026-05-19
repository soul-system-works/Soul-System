```
AMENDMENT ID:    SOUL-A002
DATE:            2026-05-19
WITNESS IDS:     SOUL-005 (captured idea: caveman digests),
                 SOUL-009 (gap observed: system failed to operationalize SOUL-005
                 during the SOUL-A001 convening)
WHAT CHANGES:    Add `## Output Format` section to operations/council-synthesis.md.
                 Council output is two-track: a full artifact (Amendment / Finding /
                 Return file) plus a conversation digest of 3-7 lines naming the
                 tension, resolution, mechanism, and artifact ID.
WHERE IN SOUL:   operations/council-synthesis.md — new section inserted between
                 "What the Council Produces" and "The Order of Voices"
QUESTION ONE:    Evidence — SOUL-005 explicitly requested caveman-style digests
                 alongside artifact-level detail. SOUL-009 surfaced when the system
                 produced a full Council deliberation in conversation instead of
                 a digest, despite SOUL-005 being open. The Body explicitly named
                 the gap and approved formalization.
QUESTION TWO:    Necessity — without this, Council output defaults to full
                 deliberation in conversation. The Body's attention is the primary
                 constraint Council output must serve. A Council that floods the
                 Body with full deliberation has skipped the Body.
QUESTION THREE:  Coherence — extends, does not contradict. Existing doctrine on
                 Amendment / Finding / Return artifacts is preserved unchanged.
                 This adds a user-facing layer alongside, not in place of, the
                 artifact. The relationship is two views of the same convening.
ACCEPTED BY:     Judge
FILED BY:        Archivist
```

---

## Council Convening Summary

**Convened:** 2026-05-19, immediately following SOUL-A001.

**Trigger:** Body observed that the SOUL-A001 Council pass produced a full
deliberation in conversation, not the digest SOUL-005 had captured. Asked
whether the system had forgotten the captured practice.

**Resolution:** Caveman-style digest in conversation is now the default Council
output form. Full deliberation goes to the artifact (amendments/, findings/,
etc.). Two views of one convening.

**Significance:** Operationalizes a previously-captured Finding (SOUL-005) and
closes the immediate gap surfaced by SOUL-009. The Finding-promotion pathway
itself remains undefined and is captured as the open Finding SOUL-009;
SOUL-A002 does not address that meta-question.

---

## The Specific Change

Added the following section to `operations/council-synthesis.md`, placed after
`## What the Council Produces` and before `## The Order of Voices`:

```markdown
## Output Format

The Council produces two views of the same convening.

**The artifact** — full record. Lives in `amendments/accepted/`, `findings/open/`,
or wherever the convening's output goes. Contains the Witness IDs consulted,
the voice-by-voice synthesis, the Three Questions if an Amendment, the Judge's
reasoning. This is the permanent record.

**The conversation digest** — 3 to 7 lines. The user-facing distillation that
appears in real-time conversation. Names the tension, the resolution, the
mechanism, and the artifact ID. Designed to be skimmable; the artifact carries
the depth.

Template for the digest:

    COUNCIL → AMENDMENT (or FINDING, RETURN)
    Tension: <what the conflict was, one line>
    Resolution: <the synthesis, one or two lines>
    Mechanism: <what changes operationally, one line>
    Filed as <ID> → <path/to/artifact>

The digest is not a summary of the artifact. It is the Council speaking to the
Body in the moment. The artifact speaks to future readers — including future
Council convenings.

A Council that produces only an artifact has skipped the Body. A Council that
produces only a digest has skipped the record. Both views are obligations.
```
