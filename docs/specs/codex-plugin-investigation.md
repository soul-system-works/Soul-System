# Codex plugin investigation and implementation preview

Date: 2026-10-16

Status: implementation preview awaiting Claude review; not a release

Working branch: `codex-plugin-investigation`

Intended reviewer: the owner and a Claude agent

## Recommendation

Review the initial Codex port on this branch, then exercise it in live sessions
before deciding whether to merge. The practical value is carrying the same project
knowledge and handoffs between tools. Packaging works in the installed CLI;
reliable model behavior and host hook execution still need live validation.

The initial investigation was source/documentation review. The implementation
below adds executed installation, discovery, wiring, and adapter checks. It does
not demonstrate model compliance, live host hook execution, or usefulness gains.
The owner subsequently authorized committing the report and implementation on
this branch for later Claude review. Review the branch against `main`; committing
the preview is not a release or merge authorization.

## Frame and abstraction

**Immediate problem:** make Soul System installable and usable in Codex without
breaking its Claude distribution.

**Larger system:** preserve one project record and one set of working principles
across agent tools, while adapting how each host loads instructions, invokes
skills, asks questions, and runs lifecycle hooks.

**Abstraction layer:** a shared methodology and durable record, with host-specific
integration adapters. Instruction-loading mechanisms, plugin metadata, tool
names, and event formats vary by host. Record ownership, stable record IDs,
truthful history, owner-controlled finding promotion, and existing Claude
behavior must remain coherent across hosts.

**Why the current integration exists:** Claude's manifest discovers the skills
and hook; `soul-init` establishes a persistent contract import; the completion
hook supplies a reminder at a moment prose instructions alone may miss. The
skills also preserve defenses against observed cache, import, and record-layout
failures. Preserve the reasons for these defenses when adapting their mechanisms.

**Counterweight:** a second host adds maintenance and may duplicate practices a
short `AGENTS.md` already supplies. Start with memory and handoff workflows and
measure whether they help. A full universal plugin architecture or an MCP server
is not justified by the inspected workflows.

## What the repository does

The current Claude manifest identifies version `2.3.2`
([manifest](../../.claude-plugin/plugin.json)). The practical system combines:

- A working contract: [operations/CLAUDE.md](../../operations/CLAUDE.md).
- Skills for project setup, capture, distillation, handoff/resume, next actions,
  stage declarations, explanations, help, and prompt rewriting.
- Project-local memory: witness and idea records, optional distilled `mind.md`,
  and `.soul/handoff.md`.
- A Python Stop hook that detects an artifact edit plus a completion claim,
  then interrupts once to request verification.
- A human-facing philosophy explaining the practices and their history.

The [usage guide](../using-the-soul.md) describes the intended lifecycle. The
root `AGENTS.md` already makes this source repository legible to other tools;
it does not by itself provide a Codex plugin installation or initialize adopting
projects for Codex.

## Usefulness and limits

The strongest plausible benefit is preserving unusual constraints, decisions,
and unfinished work across sessions and across tools. Small disposable tasks may
not justify the capture, approval, and record-maintenance overhead.

The repository's [study write-up](../study/blog-release.md) reports no code-quality
advantage over a short conventional contract in its tested builds, and identifies
other vendors as unmeasured. Those are the authors' reported results; the raw
experimental corpus was not independently audited in this investigation. They
should not be presented as demonstrated Codex benefits.

The [completion hook](../../hooks/pre-completion-verify.py) requests verification;
it does not prove that verification occurred. It uses completion-language
heuristics, a cooldown, and fail-open behavior. Its edit detection inspects Claude
transcript blocks and a fixed set of edit-tool names. File changes performed
through other tools can escape that detection. These limits matter in both the
product description and a future Codex implementation.

## Proposed changes

| Area | Proposed work | Reason |
|---|---|---|
| Packaging | Add `.codex-plugin/plugin.json` and a Codex-compatible marketplace catalog/install path. | Preserve the Claude manifests while exposing the shared skills to Codex. |
| Initialization | Add a Codex path to `soul-init` using `AGENTS.md` and an explicit, verified contract-loading strategy. | Claude `@import` and Claude cache paths are host-specific. |
| Shared skills | Audit host references, question tools, invocation controls, stage placement, and doctrine-path resolution. | Reusing Markdown does not establish equivalent execution behavior. |
| Resume and distillation | Recognize the selected host's instruction file and verify actual contract loading and hook readiness. | Project markers alone do not establish installed, enabled, trusted hooks. |
| Completion gate | Retain shared checklist/scoping logic and add a Codex event adapter. Prefer supported tool events and turn IDs for edit tracking. | Codex transcript format is explicitly unstable. |
| Documentation | Explain installation, updates, trust requirements, supported clients, and degraded behavior. | A skills-only install and a working completion gate offer different guarantees. |

Audit `soul-prompt` separately: its fresh-context requirement needs a Codex
equivalent that actually excludes the parent conversation. Audit `soul-stage`
and `soul-distill` because they currently write or maintain Claude instruction
files. Preserve owner-invoked versus model-proposable behavior explicitly;
do not assume Claude frontmatter controls have identical Codex semantics.

Use the same record stores when both agents work in one project. Avoid creating
separate Claude and Codex notebooks or copying the full philosophy into startup
instructions. Avoid machine-specific, versioned installation paths in committed
project instructions. Decide how contract updates propagate before implementing
the initializer; silently stale copies and dead cache paths are existing hazards.

## Current official Codex constraints

The official documentation reviewed for this investigation establishes:

- Codex accepts plugin packages with shared `skills/` and a compatibility
  `.codex-plugin/plugin.json` manifest. A portable root manifest is also an
  option. [Packaging](https://developers.openai.com/plugins/build/plugins)
- Codex loads project instructions through `AGENTS.md`.
  [Project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- Codex has Stop and tool lifecycle hooks. Stop supports exit code `2` with a
  continuation reason on stderr, so the existing blocking convention is not
  itself the main incompatibility. The transcript parser is.
  [Hooks](https://learn.chatgpt.com/docs/hooks)
- Plugin hooks require user trust. Compatibility environment variables include
  `CLAUDE_PLUGIN_ROOT`; changing that variable name alone is not a port.
  [Hooks](https://learn.chatgpt.com/docs/hooks)
- Current public-directory submission guidance excludes lifecycle hooks and
  directs hook-dependent plugins to manual Codex desktop installation.
  A public skills-only distribution would have reduced functionality.
  [Claude plugin conversion](https://developers.openai.com/plugins/guides/submit-claude-plugin)

These sources are trusted as the vendor's specification, not as proof of behavior
in every installed client. Availability, schemas, trust handling, and installation
behavior can change. Recheck the target client's version and current documentation
before implementation; do not claim CLI, IDE, desktop, and cloud hook parity
without exercising each claimed surface.

## Suggested implementation sequence and acceptance checks

1. Package the shared skills for a specific Codex client and prove discovery and
   explicit invocation. Document the initial supported surface.
2. Adapt setup and instruction loading, then exercise capture, handoff, resume,
   and distillation in a disposable adopting project. Confirm both tools read
   the same records and preserve existing project instructions.
3. Implement the Codex completion adapter. Exercise edit plus completion,
   read-only turns, earlier-turn edits, repeated stops, cooldowns, untrusted
   hooks, missing inputs, and projects outside Soul scope. Include edits through
   `apply_patch` and explicitly define coverage for shell-based file writes.
4. Check restart and upgrade behavior, including stale installation paths.
   Exercise the existing Claude path to detect regressions before release.
5. Only after execution, document which behaviors actually work and which remain
   unsupported. Evaluate usefulness separately from installation success.

## Implemented preview

The user authorized an implementation attempt after the investigation. The work
is on `codex-plugin-investigation`, with owner authorization to commit it for
review. There is no release/version bump, merge, push, global installation, or
persisted hook-trust change. No subagent or independent agent review was run;
the implementing agent performed the checks below. Claude review is outstanding.

Review these entry points:

- [Codex manifest](../../.codex-plugin/plugin.json) and
  [marketplace catalog](../../.agents/plugins/marketplace.json): install the same
  shared `skills/` tree, selecting a separate Codex hook definition.
- [Codex host instructions](../../operations/codex.md): initialization and resume
  procedures, shared policy/record ownership, question-tool fallbacks, Stage and
  Mind handling, fresh-context prompt behavior, and detector boundaries. Each
  shared skill has a conditional pointer to this document.
- [Wiring helper](../../tools/codex-project.py): preserves existing instructions
  around one managed live-reference block. Uses the active non-empty override
  when present; leaves an empty override alone so it cannot hide existing base
  rules. Checks missing/stale contract content, preserves CRLF outside its block,
  refuses malformed markers and symlink targets, and never initializes this source
  repo or chooses record-tracking preferences.
- [Codex hook configuration](../../hooks/codex.json) and
  [event adapter](../../hooks/codex.py): SessionStart contract delivery, direct
  edit events, Git-visible Bash changes, and Stop continuation. Reuses the
  original checklist, claim heuristic, scoping, cooldown, and event emitter.
- [Shared hook change](../../hooks/pre-completion-verify.py): adds specific Soul
  marker detection in `AGENTS.md` and `AGENTS.override.md`; preserves the
  ordinary-English scoping fence and existing Claude hook configuration.
- `agents/openai.yaml` in the existing explicitly invoked skills: preserves
  their invocation policy in Codex while keeping Claude frontmatter intact.
  `soul-capture`'s existing description also needed YAML quoting around an
  embedded colon; its wording is unchanged. Init and Stage descriptions now
  describe host-neutral behavior.

**Do not copy the contract:** the implementation preserves the existing live
reference discipline. Its tradeoff is machine/cache-path dependence. Trusted
SessionStart delivery reads the current installed contract independently, while
resume detects a missing or different referenced copy. No automatic path repair
or global trust configuration is performed. This needs particular review because
cache/import silence is already a documented failure mode.

**One project policy:** if an adopting project has `CLAUDE.md`, both tools use its
local Register/Stage declarations. Codex-only projects use the active AGENTS file.
The host guide requires resolution of conflicting declarations. No separate
Codex notebook, findings promotion rule, or autonomous record-capture policy is
introduced. The source-repo handoff exception in the Codex guide names the existing
SOUL-187 gap rather than creating an upstream store aimed at this repository.

## Execution evidence (2026-10-16)

All checks used disposable projects/configurations, with the source checkout on
this branch. These commands are repeatable from the repository root:

```bash
python3 -B tools/check_codex_plugin.py
python3 -B -m unittest discover -s hooks -p 'test_codex.py' -v
python3 -B -m unittest discover -s tools -p 'test_codex_project.py' -v
python3 -B hooks/test_scope.py
git diff --check
```

| Check | Observed result | What it establishes |
|---|---|---|
| Installed `codex-cli 0.163.0`, temporary configuration | Local marketplace add, listing, and plugin installation succeeded. | The actual CLI accepts the catalog and package. |
| Actual app-server `skills/list` | All ten Soul skills enabled and discovered; no skill parse errors. | Actual loader acceptance, including retained Claude metadata. Names are qualified, e.g. `$soul-system:soul-init`. |
| Actual app-server `hooks/list` | SessionStart, PreToolUse, PostToolUse, and Stop discovered from `hooks/codex.json`; trust status `untrusted`. | Correct hook configuration selected; installation does not establish trust. |
| Adapter suite | 19 tests passed. | Contract output, scoping, turn/session/project isolation, loop/cooldown guards, shell read/write distinctions, already-dirty/untracked/deleted files, missing inputs, and documented coverage exclusions. |
| Wiring suite | 10 tests passed. | Existing instructions and Claude files preserved, idempotence, override/empty-override behavior, CRLF, missing/stale references, malformed blocks, symlinks, and source-repo guards. |
| Existing scope fence | Reported 11/11 passed. | Existing Claude scope regression checks still hold. |
| Diff whitespace check | Passed. | No tracked-diff whitespace errors; not a behavioral check. |

The generic skill-creator validator was also run. After the description quoting
fix it accepts the standard frontmatter portions, but rejects the retained
`disable-model-invocation` extension on the six Claude explicitly invoked skills.
That extension was intentionally preserved; the actual Codex loader accepted all
ten skills. The matching Codex invocation-policy files were checked in the
installed package. Discovery does not prove the model respects those policies.

The installation/discovery helper starts an app-server for local metadata queries
only; it does not run a model, trust hooks, or invoke skills. Its temporary Codex
configuration does not replace the user's normal configuration.

## Remaining review and live validation

- Run initialization, capture, handoff, resume, Stage, distillation, and prompt
  isolation through actual Codex conversations. Deterministic helper tests cannot
  demonstrate that the model follows the adapted skill instructions.
- In a supported local client, review/trust the hooks and verify actual startup
  context plus an edit/completion/Stop continuation cycle. The adapter suite calls
  the code and exercises process error handling; it does not prove host dispatch
  during a real conversation. Do not label the gate armed from the current tests.
- Exercise a Claude session after installing this branch to check the shared skill
  changes in use. Existing scope tests passed; Claude model behavior was not run.
- Exercise restart and upgrade with an existing installation. The package stays
  at `2.3.2` during review; edits in this checkout do not imply an installed cache
  was refreshed. Use a fresh temporary install for repeatable code checks, and
  inspect/reinstall the preview deliberately for live testing.
- Check instruction size limits and any custom fallback filenames/nested overrides
  in the adopting project. The helper targets the default files in the specified
  project directory, not every possible host configuration.
- Review shell coverage: ignored files, non-Git projects, nested Git working
  directories, submodule contents, external writes, oversized fingerprints, and
  timeouts need manual verification. Concurrent external edits can trigger a
  conservative reminder. This remains a reminder, not a security boundary.

After the authorized commit, review `git diff main...codex-plugin-investigation`
for the complete preview, including new manifests, adapter, helper, tests, host
guide, policies, and this report. Check `git status --short` separately for any
later working-tree edits. The branch remains local until explicitly pushed.

## Questions for Claude review

- Does this preserve the force of the existing cache/import and record-locality
  protections rather than merely replacing Claude vocabulary?
- What is the smallest explicit host adapter that avoids duplicating the skills?
- Should instruction loading use a stable local reference, a maintained project
  copy, or a supported startup hook, and how will updates be verified?
- Which Codex surface should be supported first, and is manual installation with
  a trusted hook acceptable to the owner?
- Are there existing release conventions or evidence that change this scope?

Owner decisions about target clients and distribution are **Body-Input**: they
depend on intended use. They need resolution before promising supported surfaces,
but do not prevent an isolated local prototype.

## Review disposition

Recommended next action: review this implementation preview and perform the live
checks above. Maintain Claude support and shared project records. Do not merge
until installation, instruction loading, record workflows, and the promised gate
behavior have been exercised in the target clients.
