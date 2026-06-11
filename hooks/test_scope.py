"""Negation test for the completion-gate's self-scoping (SOUL-160).

FENCE: _is_soul_project must NEVER match the bare English word "soul".
The incident: efficacy Chain J's signed-off comparator CLAUDE.md contained
"…spawn rates, hitbox sizes — are the soul of an action game…" and the gate
fired inside the control arm 7 times, voiding the false-done endpoint.
If this test fails, the gate is leaking into non-Soul projects again.

Run: python3 hooks/test_scope.py  (exit 0 = fence holds)
"""

import importlib.util
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "pre_completion_verify", os.path.join(_HERE, "pre-completion-verify.py")
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _project_with_claude_md(tmp, text):
    d = os.path.join(tmp, f"p{abs(hash(text)) % 10**8}")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "CLAUDE.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    return d


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        # 1. THE INCIDENT SENTENCE — ordinary English "soul" must NOT scope.
        chain_j = _project_with_claude_md(
            tmp,
            "# Game project\nTuning values — spawn rates, hitbox sizes — are "
            "the soul of an action game. Keep them in one file.\n",
        )
        if _mod._is_soul_project(chain_j):
            failures.append("LEAK: bare-word 'soul' in ordinary English scoped the gate (SOUL-160 regression)")

        # 2. More bare-word traps: capitalized, possessive, compound.
        for trap in ("Soul music playlist app.", "the team's soul", "soulful UX writing"):
            d = _project_with_claude_md(tmp, trap)
            if _mod._is_soul_project(d):
                failures.append(f"LEAK: {trap!r} scoped the gate")

        # 3. The real seed must scope (title marker).
        seed = _project_with_claude_md(tmp, "# CLAUDE.md — The Soul Seed (1.0)\n…")
        if not _mod._is_soul_project(seed):
            failures.append("MISS: the Soul Seed title no longer scopes the gate")

        # 4. Seed-import form must scope.
        imp = _project_with_claude_md(tmp, "@/mnt/d/Projects/Soul-System/operations/CLAUDE.md\n")
        if not _mod._is_soul_project(imp):
            failures.append("MISS: an operations/CLAUDE.md seed import no longer scopes the gate")

        # 5. witness.md presence must scope regardless of CLAUDE.md content.
        wd = os.path.join(tmp, "wproj")
        os.makedirs(wd)
        open(os.path.join(wd, "witness.md"), "w").close()
        if not _mod._is_soul_project(wd):
            failures.append("MISS: witness.md presence no longer scopes the gate")

        # 6. No CLAUDE.md, no witness.md — must not scope.
        bare = os.path.join(tmp, "bare")
        os.makedirs(bare)
        if _mod._is_soul_project(bare):
            failures.append("LEAK: empty project scoped the gate")

    if failures:
        for f in failures:
            print(f"FAIL  {f}")
        sys.exit(1)
    print("PASS  6/6 — the scope fence holds (no bare-word 'soul' matching)")


if __name__ == "__main__":
    main()
