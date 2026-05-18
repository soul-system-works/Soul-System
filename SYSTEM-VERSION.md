# System Version

Current system version: **0.1.2**

---

## Version History

| System Version | Date | What Changed |
|---|---|---|
| 0.1.0 | 2026-05-15 | Initial system — all founding documents |
| 0.1.1 | 2026-05-15 | Soul: Artificer role and pairing added |
| 0.1.2 | 2026-05-15 | Soul: Adversary, Critic, Craftsman added. The Hands section. Artificer moved to Hands. Versioned filenames removed. |

---

## Versioning Rules

Filenames are stable and never include version numbers.
The whole repository evolves together under a single version number.

**System version semantics** (MAJOR.MINOR.PATCH):
- PATCH (0.1.x) — skills, hooks, commons entries, registry entries added
- MINOR (0.x.0) — operational documents amended
- MAJOR (x.0.0) — the Soul itself amended

Prior versions of any amended document are retained in `amendments/accepted/`.
See `amendments/README.md`.

---

## Copying Into a Project

When copying `operations/` into a project, record the system version.
This allows findings to be traced back to the version that produced them.

```
Project:               [your project name]
System version copied: 0.1.2
Date:                  [date]
```
