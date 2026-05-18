# Hooks

Automatic trigger definitions for Claude Code and compatible environments.
Built by the Artificer through real use. Empty until the first run produces
evidence that a hook is needed.

---

## Entry Format

Each hook is a script or configuration file that fires on a specific condition.

```
hooks/
    pre-implementation.sh      ← fires before implementation begins
    post-iteration.sh          ← fires after each iteration to prompt Witness log
    pre-synthesis.sh           ← fires before Council convenes
    ...
```

---

## When to Add a Hook

When the Witness log shows an obligation being skipped consistently,
a hook is the Artificer's answer — make the obligation automatic rather
than remembered.
