```
FINDING ID:      SOUL-F029
DATE:            2026-05-22
WITNESS IDS:     SOUL-058 (the distribution-mechanism investigation). Anchors:
                 commands/soul-verify.md DIFFERS from ~/.claude/commands/soul-verify.md
                 (drift created THIS session by editing only the repo copy); install.sh
                 pinned to v0.3.0 (current 0.4.2) and copying only operations/ (no
                 commands, no hooks, no settings wiring); soul-init.md absent from the
                 repo's commands/ (the SOUL-057 side-note that opened this).
WHAT:            The Soul System distributes its artifacts under TWO unreconciled regimes,
                 and the copy regime has no update path:
                 - REFERENCE (live, never stale): operations/ doctrine via `@import` in an
                   adopting project's CLAUDE.md; the completion-gate HOOK via an absolute
                   path in settings.json. All five dogfood projects use `@import` — which
                   is WHY doctrine edits (the I014 seed obligation, the F028 completion-gate
                   change) reached them retroactively and none can get "stuck."
                 - COPY (frozen, drifts): the `/soul-*` COMMANDS as physical copies in
                   ~/.claude/commands/; and install.sh SNAPSHOT installs (`cp -r
                   operations/` + a pinned .soul-version). There is NO mechanism syncing
                   repo → ~/.claude/commands/ (done manually once), so editing a repo
                   command does not reach the command a user actually invokes — proven live
                   by soul-verify going stale this session. install.sh compounds it:
                   version-pinned (0.3.0) and it never installs commands or hooks at all.
                 One root: copies without a sync. soul-init's repo-absence, the stale
                 soul-verify, and the stale install.sh are three faces of it.
WHY NOT YET AMENDMENT:  Infrastructure, not philosophy — an Artificer fix, not a Soul
                 amendment. The model choice is open (Body/Council):
                 (a) make commands LIVE too (symlink or a thin shim) so they leave the copy
                     regime entirely — fewest moving parts, no update step needed;
                 (b) a soul-update / extended install.sh that syncs the copy artifacts
                     (commands, hooks, settings, .soul-version) repo → install, bumped each
                     release;
                 (c) accept copies but make drift VISIBLE — a freshness check that warns
                     when an installed command lags the repo.
                 Decide at the AL gate: which artifacts MUST be live vs may be copied, and
                 what propagates the copies. This is the cheap moment — one machine, all
                 `@import`, near-zero blast radius. Relates to the soul-init machine-local
                 path wrinkle and SOUL-I017 (tool/skill growth).
FILED BY:        Archaeologist (surfaced the existing mechanism) + Emissary (the live drift
                 evidence) + Cartographer (named the two-regime map)
RELATED:         [[SOUL-F020]] (reference-adapter sync governance — same family: keeping a
                 derived copy in step with its source), SYSTEM-VERSION.md (the version the
                 copy artifacts should track), the SOUL-057 soul-init side-note
STATUS:          Open — distribution model undecided; copy artifacts (commands, snapshot
                 installs) have no sync, reference artifacts (doctrine `@import`, hook path)
                 are fine. Decide before commands change often or a second machine/install
                 exists. Practical residual carried here: soul-verify is stale in
                 ~/.claude/commands/ right now.
```
