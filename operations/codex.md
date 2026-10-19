# Codex host integration (experimental)

Read this file when running a Soul skill in Codex. Resolve the plugin root from
the loaded skill's path, two levels above its directory, resolving symlinks.
Keep the shared skill's substantive workflow and owner approval requirements.
The host-specific replacements below take precedence over Claude mechanics in
that workflow; they do not change the contract's obligations.

## Shared replacements

- Invoke skills as `$soul-system:soul-init`, `$soul-system:soul-capture witness`, etc. References to
  `/soul-*` in shared prose name those same skills. A loaded skill's directory is
  in the installed plugin; project records always belong to the working project.
- Read files with the available filesystem tools. Use the available question tool
  only if it supports the current mode; otherwise ask in conversation and wait.
  `AskUserQuestion` is a Claude tool name, not a requirement to call it in Codex.
- For **local Register and Stage policy**, read existing project `CLAUDE.md` if
  present. This keeps one policy when Claude and Codex share a project. Otherwise
  use root `AGENTS.override.md` if non-empty, else root `AGENTS.md`. This is the
  **project policy file** for the shared skill's read/write instructions. Never
  replace `operations/CLAUDE.md`: that remains the canonical shared contract.
- A non-empty root `AGENTS.override.md` takes precedence over root `AGENTS.md` in Codex.
  Report conflicting policy declarations in these files rather than silently
  selecting a different stage. Obtain the owner's resolution before editing.
- Codex does not expand Claude `@` imports. Read the contract and Mind explicitly.
  Keep the existing root or `.soul/` record layout; resolve duplicate stores before
  writing. The managed startup instructions discover an existing Mind in either
  layout, so distillation requires no new Claude import in a Codex-only project.
  When retiring a Mind, retain the conditional startup instruction; remove only
  an obsolete explicit reference to the retired file. Preserve Claude imports
  when its own Mind still exists.
- Existing `disable-model-invocation: true` skills have matching
  `agents/openai.yaml` policies. An explicit workflow handoff, such as init
  offering stage selection, can read the procedure; it is not authorization to
  choose or write a stage for the owner.
- Keep capture/finding and distillation approval boundaries. Installation is not
  consent to create project records or change project policy. Session hooks do
  not perform those workflow writes.

## soul-init: Codex procedure

This replaces the Claude initialization procedure, including its `@import`
instructions and its Claude-only prohibition on writing anything beyond an import.
It still references doctrine live; it never copies doctrine into the project.

1. Verify `<plugin-root>/operations/CLAUDE.md` exists and read it. Use the session's
   working directory as the adopting project, without searching upward. In the
   Soul System source repository itself, use its existing `AGENTS.md`; do not run
   the wiring helper on that repository.
2. Read the active project instruction file (`AGENTS.override.md` if non-empty,
   otherwise `AGENTS.md`) and the project policy file. Show the proposed managed
   block or its delta before adding it to an existing file; obtain consent as the
   Claude procedure does. Preserve all content outside the block. Reuse an
   existing Register; otherwise ask plain/fluent once, writing only a fluent
   override to the project policy file on the owner's choice.
3. Run `python3 <plugin-root>/tools/codex-project.py wire --project <project-root>`.
   Quote paths as shell arguments. It appends or refreshes a marked live-reference
   block; it does not scaffold or move records, edit ignores, or configure trust.
4. Follow shared init steps **3–3b** for the record-tracking choice, scaffolding,
   and ignore rules. Keep the record at its existing location and ignore only
   runtime state if tracking was chosen. Follow step **3d** for the optional stage,
   using the project policy file in place of the project's `CLAUDE.md`. Follow
   step **3e** (offer to move AI working files into `.ai/` with
   `tools/layout-cleanup.py`) on an already-initialized project — one whose
   instruction file already held the managed block, the Codex form of the shared
   "import already present" path; skip it for a fresh project.
5. Read an existing Mind explicitly and check that the managed block asks future
   sessions to read it. Do not add `@` imports to `AGENTS.md`.
6. Run the helper's `status --project <project-root>` command. Report a missing or
   different contract as a wiring gap. The helper compares referenced content
   with the currently installed contract; equality proves content, not model
   loading or hook readiness. Check the host's instruction size budget across the
   full instruction chain: an appended block can be truncated in a large file.
   Read the files now to start following the contract;
   restart to exercise startup delivery.
7. Explain that the path is local to this installation. As with a Claude import,
   another machine or a removed cache version may need init again. Prefer a stable
   clone for portable development setups. After upgrades, resume checks for stale
   paths/content. A trusted SessionStart hook supplies the installed contract
   independently, but does not repair stale project instructions on its own.
8. Hook trust must be reviewed in the host. Without a demonstrated working gate,
   say the project has manual verification only. Do not enable hooks, modify global
   configuration, or claim they are trusted as a side effect of init.

## soul-resume: Codex wiring check

Replace shared resume step 0 with this check, then follow its steps 1 onward:

1. From context alone, perform the shared contract sentinel (rule count and rule
   3); do not read this report or the contract to manufacture a passing sentinel.
   If unknown, say startup loading is unconfirmed, then explicitly read the
   installed contract to repair this session. State that repair happened.
2. Run `python3 <plugin-root>/tools/codex-project.py status --project <project-root>`.
   A missing/unreadable/different reference requires `$soul-system:soul-init`. The source
   repository's hand-authored `AGENTS.md` is an intentional exception to managed
   wiring: verify its explicit pointers instead of adding a managed block.
3. Locate the shared stores. Report ambiguity or missing records.
4. Separate **scoped**, **startup observed**, and **Stop demonstrated**. A witness
   file or marker proves scope only. This session's `Soul Codex SessionStart hook
   ran` context proves startup delivery. Only a live exercise after an edit and
   completion claim demonstrates Stop. An old event log is not proof; absent
   evidence means unknown/manual, not armed. Check enabled/trusted state in the
   host when available; do not fabricate that state from project files.

Report actual gaps concisely, then read the cursor and its pointers. Preserve the
shared rule that an inherited pointer is a claim to verify.

## Other host-sensitive workflows

- **soul-stage / soul-next:** use the project policy file for Register, Stage,
  Phase, and placement. In an `AGENTS.md` policy file insert a new stage after the
  managed block or Register line; preserve the managed block itself. A stage is
  shared project policy, not a separate Codex-only stage.
- **soul-distill:** read the actual store layout rather than assuming root files;
  follow the shared curation procedure. Startup reads an existing Mind without
  an import. A dual-tool project's existing Claude Mind import still matters.
- **soul-prompt:** resolve contract paths from the managed block/helper or from
  the loaded skill's plugin root, not from Claude import syntax. Use a fresh agent
  with no inherited conversation if the host supports it, passing only the brief
  and file paths. If no such facility exists, report that context isolation is
  unavailable and leave a brief for a fresh session; do not imitate isolation by
  rewriting in the current conversation. A fork with inherited history fails this
  requirement.
- **soul-help:** describe Codex invocation and actual hook readiness; do not repeat
  the Claude guide's automatic-gate claim when hooks are untrusted or unexercised.
- **soul-handoff:** preserve the shared cursor and provenance. When running in the
  Soul System source repo, route system lessons to its existing witness/ideas
  stores, not to an `upstream.md` aimed back at itself (known SOUL-187 gap).

## Detector boundaries

Codex uses `hooks/codex.json`; Claude continues using `hooks/hooks.json`. Both use
the same scope predicate, completion-language heuristic, checklist, event emitter,
and project cooldown. Codex tracks direct edit-tool events per session/turn and
fingerprints Git-visible content around Bash calls. Read-only shell commands do
not count merely because they ran, and editing an already dirty file still counts.

The shell detector requires the session directory to be the Git root. It excludes
ignored files, writes outside that directory, submodule content, and projects
without Git. It abandons shell fingerprints over 64 MiB of dirty/untracked content
or when Git cannot finish within its timeout. Concurrent external edits can be
attributed to the running Bash call. Direct edit invocations count conservatively,
including unsuccessful attempts. Tool paths without lifecycle hooks are not
covered. Missing event IDs or runtime failures fail open with a diagnostic.

The gate remains a reminder, not a security boundary or proof of verification.
Apply the completion discipline manually wherever automatic detection is absent.

## Sources and status

Checked 2026-10-16 against the installed `codex-cli 0.163.0` help and official
[plugin packaging](https://developers.openai.com/plugins/build/plugins),
[hooks](https://learn.chatgpt.com/docs/hooks), and
[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) guidance.
Treat client availability and trust behavior as version-dependent; see
`docs/specs/codex-plugin-investigation.md` for execution evidence and remaining gaps.
