#!/usr/bin/env python3
"""Soul System pre-completion Stop hook (scoped blocking).

The activation instrument for SOUL-F012: the completion-side doctrine (A003,
A005, A007, F013, F016) describes the right checks but does not fire on its own.
This hook makes them fire. When a Soul-governed session tries to end after
shipping artifacts AND signaling completion, it blocks once and injects the
verification checklist; the session must address gaps before ending.

Scoping (so it is not noise):
- Self-scopes to Soul-governed projects only (witness.md or a soul CLAUDE.md).
- Fires only when this turn both SHIPPED an artifact (a Write/Edit tool use)
  and CLAIMED completion (completion language in assistant text).
- Loop-safe: honors `stop_hook_active` so it blocks at most once per stop.
- Fail-open: any error or uncertainty allows the stop (exit 0).

Claude Code specific (Stop-hook contract). The OBLIGATION it enforces is
tool-agnostic; this is the reference implementation. Reference implementation
for SOUL-F012; see commands/soul-verify.md for the manual form.
"""

import json
import os
import re
import sys

_EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
_CLAIM_RE = re.compile(
    r"(complete|completed|\bdone\b|finished|all tests pass|tests pass|"
    r"tests passed|definition of done|shipped|✓)",
    re.IGNORECASE,
)
_SCAN_TAIL = 80  # records from the end to inspect


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # cannot parse input -> do nothing

    # Loop guard: never block twice in one stop cycle.
    if data.get("stop_hook_active"):
        sys.exit(0)

    cwd = data.get("cwd") or os.getcwd()
    if not _is_soul_project(cwd):
        sys.exit(0)

    transcript_path = data.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        sys.exit(0)

    shipped, claimed = _scan(transcript_path)
    if not (shipped and claimed):
        sys.exit(0)

    print(_checklist(), file=sys.stderr)
    sys.exit(2)  # block the stop; stderr is fed back to the session


def _is_soul_project(cwd: str) -> bool:
    if os.path.exists(os.path.join(cwd, "witness.md")):
        return True
    claude_md = os.path.join(cwd, "CLAUDE.md")
    if os.path.exists(claude_md):
        try:
            with open(claude_md, "r", encoding="utf-8", errors="ignore") as fh:
                txt = fh.read().lower()
            if "soul" in txt or "operations/claude.md" in txt:
                return True
        except Exception:
            pass
    return False


def _scan(transcript_path: str):
    """Return (shipped_artifact, claimed_completion) for the recent transcript tail."""
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except Exception:
        return (False, False)

    records = []
    for ln in lines[-_SCAN_TAIL:]:
        ln = ln.strip()
        if not ln:
            continue
        try:
            records.append(json.loads(ln))
        except Exception:
            continue

    shipped = False
    claim_text = []
    for rec in records:
        for block in _content(rec):
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") in _EDIT_TOOLS:
                shipped = True
            elif block.get("type") == "text":
                claim_text.append(block.get("text", ""))

    claimed = bool(_CLAIM_RE.search(" ".join(claim_text)))
    return (shipped, claimed)


def _content(record):
    msg = record.get("message", record)
    if not isinstance(msg, dict):
        return []
    content = msg.get("content")
    if isinstance(content, list):
        return content
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return []


def _checklist() -> str:
    return (
        "[Soul System pre-completion gate — SOUL-F012] This turn shipped "
        "artifacts and signaled completion in a Soul-governed project. Before "
        "ending, run these checks and address any gap (this fires once):\n"
        "1. Global invariant verified, not just local tests? (verification vs validation)\n"
        "2. Any ABSOLUTE claim grounded by an EXTERNAL anchor (benchmark / "
        "published value / standard / expert)? Internal consistency over an "
        "absolute claim is a Coherent Falsehood.\n"
        "3. Outward reach done (field / standards / real user), not Universe Collapse?\n"
        "4. Visual / non-automatable artifact CAPTURED and INSPECTED, not deferred "
        "to 'the human will look'?\n"
        "5. Unfinished business marked (TODO/FIXME/DEBT/HACK); standing limits in docstrings?\n"
        "Address gaps, then end. See commands/soul-verify.md."
    )


if __name__ == "__main__":
    main()
