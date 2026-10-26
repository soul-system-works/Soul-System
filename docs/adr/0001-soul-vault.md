# ADR 0001 — The Soul vault: records in one private repo, reached by a `.soul` link

**Status:** built in v3.4.0 on the Body's go-ahead (2026-10-22: "go ahead with
steps 1-4", then 5–7); the pilot on one project is pending. **Source:** SOUL-I079 —
its DISCUSSED, CLARIFIED, ROUND 2–5, LINK TEST and SIMPLIFIED fields hold the full
discussion; this file holds only the decision and what binds the code.

## Context

A Soul record (witness, ideas, Mind, handoff) has lived inside each project, either
tracked in git or kept local. The Body works across many projects of different
sensitivity. They wanted one private, consistent home for every record: kept safe
through machine changes, out of public repos, and in one place for cross-project
work. In the Body's words: "capture, protability, and management are all part of
the issue".

## Decision

1. **One vault per machine.** A vault is a private git repo of Obsidian folders:
   `projects/<key>/project.md` (label, contributes, remote) and
   `projects/<key>/soul/` (the record). A one-line machine file names it. The
   Body: "i don't want an overengineered system".
2. **The project keeps a `.soul` link into the vault**, so everything that finds
   `.soul/` today keeps working: the completion gate, the Mind import and every
   skill. The vault is a third answer in `/soul-init`; local and in-git stay.
3. **Labels:** public, private, confidential, restricted. The one rule enforced is
   that `restricted` never goes in a vault. The boundary is where the vault lives:
   a closed system's vault stays on that system, so no level or read-down code is
   needed.
4. **The key, not the path, names the vault folder.** A project is matched by its
   git remote; the folder name is used only when neither side has a remote.

## What cannot vary — each from the I079 link test, 2026-10-22, Claude Code 2.1.308, WSL2

- **On WSL with the project on a Windows drive, the link is a junction**
  (`mklink /J`). Windows tools could not follow a WSL-made symlink ("The file
  cannot be accessed by the system"); a junction worked from both sides. So the
  vault must be on a Windows drive too.
- **The vault must be listed in `.claude/settings.local.json`
  `permissions.additionalDirectories`.** Without it, Claude Code refused writes
  through the link ("outside the allowed working directories").
- **The Mind loads through the one-time outside-imports approval**, not a hook.
  A SessionStart hook's output reached the session only as a ~2KB preview, and the
  Mind is about 8KB. A declined approval is caught by `/soul-resume`'s Mind check.
- **A broken link is reported out loud** (`vault.py check`, the SessionStart line,
  `/soul-resume` step 0). The test confirmed that a broken link hides every store
  while git says nothing.
- **Copy, compare, link, compare again; only then delete** (from the ROUND 3 plan
  sketch, not the link test: "copy, verify, then link; never delete first").
  Nothing is removed before both hash compares pass.

## Rejected

- **A pure `$SOUL_VAULT` path, with no link** (the original brief's form). The gate
  and the Mind import assume the record is in the project. Moving it out meets the
  recorded failures: a gate silently off for three months (2026-08-20
  retrospective), and outside imports that fail silently and get confabulated
  (SOUL-F038).
- **Do nothing and hide `.soul/` with an exclude.** That answers clutter, but not
  the Body's main aim: one consistent home.
- **A backup-only copy.** It kept the record in the project, so it did not give
  the one home the Body asked for (CLARIFIED); it had been the fallback "if links
  fail", and the links passed.
- **Vault levels and read-down access (Bell–LaPadula).** Drafted in ROUND 5, cut
  by SIMPLIFIED. Revisit only if two vaults ever share one machine.

## Private-name lists

Each project's `private-names.txt` travels with its record and is committed to the
vault (the Body's call, 2026-10-22): it arms the secret guard on the next machine.
The guard does not flag those lists in a vault. A list can hold names no record
mentions, such as a work email; those enter the vault's history — the Body kept
the lists with that known (2026-10-22).

Private names in a vault commit still warn. The guard cannot confirm a GitLab
repo is private, and it never assumes a repo is private (the Body's call,
2026-10-22): the warnings are expected noise, never a block.

## Known hazard, kept and reported

While a moved record is still tracked in the project's git, a reset, stash,
restore or checkout can put the old committed copy back in place of the link.
`vault.py link` prints STILL TRACKED and recommends `git rm --cached`; `check`
reports TWO COPIES. Found by fresh-context review of the 3.4.0 diff and reproduced
there.

## What would make this wrong

- A Windows tool that cannot follow a junction either. Only cmd and PowerShell were
  tested; Codex was not.
- A Claude Code change that treats a junctioned folder as inside the project. The
  allowed-directory step would then be unneeded but harmless.
- The Body ends up wanting a second vault on one machine (decision 1).
- macOS was not tested. There the link is a plain symlink, and the allowed-folder
  and import-approval steps are assumed to carry over — that is unverified.

Cited from: `tools/vault.py`, `skills/soul-init/SKILL.md` (`vault-link` and the vault move).
