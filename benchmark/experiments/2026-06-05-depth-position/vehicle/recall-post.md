---

Today's task: you are standing up a batch of automated, non-interactive evaluation runs for the Ledger service — each invoked as `claude -p "<task>" < /dev/null` in a fresh process. Every run needs the same shared 1,800-line engineering-doctrine file loaded into the model's context so the model follows the team's conventions.

To keep it DRY, the team lead proposes putting a single line — `@shared/ledger-doctrine.md` — in each run's `CLAUDE.md`, so the doctrine is imported by reference rather than duplicated into every run.

Recommend how to load the shared doctrine reliably across these `-p` runs. Be decisive and brief.
