#!/usr/bin/env python3
"""Soul System pre-completion Stop hook (scoped blocking).

The activation instrument for SOUL-F012: the completion-side doctrine (A003,
A005, A007, F013, F016) describes the right checks but does not fire on its own.
This hook makes them fire. When a Soul-governed session tries to end after
shipping artifacts AND signaling completion, it blocks once and injects the
verification checklist; the session must address gaps before ending.

Scoping (so it is not noise):
- Self-scopes to Soul-governed projects only (witness.md or a soul CLAUDE.md).
- Fires only when the CURRENT turn (records after the last genuine user message)
  both SHIPPED an artifact (a Write/Edit tool use) and CLAIMED completion
  (completion language in assistant text). Turn-scoped, not a flat tail — see _scan.
- Loop-safe: honors `stop_hook_active` so it blocks at most once per stop.
- Cooldown: fires at most once per COOLDOWN_SECONDS per project, so a high-commit
  iterative session (where ship+claim matches every turn) is not flooded — the
  gate marks genuine completion moments, not every increment (real-world evidence:
  SOUL-026, fired on consecutive turns).
- Fail-open: any error or uncertainty allows the stop (exit 0).

Claude Code specific (Stop-hook contract). The OBLIGATION it enforces is
tool-agnostic; this is the reference implementation. Reference implementation
for SOUL-F012; see operations/completion-gate.md for the gate doctrine.
"""

import hashlib
import json
import os
import re
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone

COOLDOWN_SECONDS = 900  # 15 min — fire at most once per window per project

_EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
# NOTE: claim detection is a heuristic regex — it can false-positive (e.g. "done"
# in an unrelated sentence) or false-negative (completion phrased unusually). This
# is acceptable because the hook is fail-open and fires at most once per turn, so a
# spurious fire costs only one verification pass and a missed fire degrades to the
# pre-hook status quo. A precise "claim" signal would need model-level intent, not
# a regex; deliberately not attempted here.
_CLAIM_RE = re.compile(
    r"(complete|completed|\bdone\b|finished|all tests pass|tests pass|"
    r"tests passed|definition of done|shipped|✓)",
    re.IGNORECASE,
)
_SCAN_TAIL = 200  # records from the end to read; scan is then sliced to the CURRENT turn


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

    # Cooldown: in a high-commit session the scope (ship + claim) matches nearly
    # every turn. Fire at most once per COOLDOWN_SECONDS per project, so the gate
    # marks genuine completion moments rather than every increment. Real-world
    # evidence: the gate fired on consecutive turns in an iterative session
    # (SOUL-026). The cost of a missed fire is low (fail toward the pre-hook
    # status quo); the cost of firing every turn is friction that gets it disabled.
    cooldown = _cooldown_path(cwd)
    if _within_cooldown(cooldown):
        sys.exit(0)
    _mark_fire(cooldown)

    _emit_event(cwd, data)  # reference emitter for the Soul event standard
                            # (SOUL-F018); fail-safe — never affects the exit path.

    print(_checklist(), file=sys.stderr)
    sys.exit(2)  # block the stop; stderr is fed back to the session


def _cooldown_path(cwd: str) -> str:
    h = hashlib.sha1((cwd or "").encode("utf-8")).hexdigest()[:12]
    return os.path.join(tempfile.gettempdir(), f"soul-verify-cooldown-{h}")


def _within_cooldown(path: str) -> bool:
    try:
        return os.path.exists(path) and (time.time() - os.path.getmtime(path)) < COOLDOWN_SECONDS
    except Exception:
        return False


def _mark_fire(path: str) -> None:
    try:
        with open(path, "w") as fh:
            fh.write(str(time.time()))
    except Exception:
        pass


def _emit_event(cwd: str, data: dict) -> None:
    """Emit one Soul event-standard record for this gate firing (reference adapter).

    Writes a CloudEvents v1.0 line (the soul.gate.completion.flagged profile,
    SOUL-F018) to the project event sink (.soul/events.jsonl, or $SOUL_EVENT_LOG).
    Fully fail-safe: any error is swallowed so emission can never change whether the
    gate blocks. The hook FLAGS completion for verification — it cannot observe
    whether verification then happened — so the type is .flagged, not .verified.
    """
    try:
        sink = os.environ.get("SOUL_EVENT_LOG") or os.path.join(cwd, ".soul", "events.jsonl")
        event = {
            "specversion": "1.0",
            "id": str(uuid.uuid4()),
            "source": f"urn:soul:project:{os.path.basename(os.path.abspath(cwd)) or 'unknown'}",
            "type": "soul.gate.completion.flagged",
            "time": datetime.now(timezone.utc).isoformat(),
            "datacontenttype": "application/json",
            "data": {
                "gate": "completion",
                "finding": "SOUL-F012",
                "shipped": True,
                "claimed": True,
                "outcome": "checklist_injected",
            },
        }
        session_id = data.get("session_id")
        if session_id:
            event["genaisessionid"] = session_id
        os.makedirs(os.path.dirname(sink), exist_ok=True)
        with open(sink, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(event) + "\n")
    except Exception:
        pass  # fail-safe: emission never affects the gate


# Markers that appear ONLY in Soul-governed doctrine, never in ordinary English.
# NEVER scope by the bare word "soul" — not even word-bounded: a signed-off
# comparator CLAUDE.md containing the ordinary sentence "…are the soul of an
# action game…" pulled this gate into the control arm of a measurement 7 times
# and voided an endpoint (SOUL-160, efficacy Chain J, 2026-06-10).
_SOUL_MARKERS = (
    "the soul seed",            # seed title
    "philosophy/the-soul.md",   # philosophy pointer
    "operations/claude.md",     # seed import path
    "soul-capture",             # instrument commands
    "soul-handoff",
    "soul-resume",
    "witness.md",               # the record store, named by doctrine
)


def _is_soul_project(cwd: str) -> bool:
    if os.path.exists(os.path.join(cwd, "witness.md")):
        return True
    claude_md = os.path.join(cwd, "CLAUDE.md")
    if os.path.exists(claude_md):
        try:
            with open(claude_md, "r", encoding="utf-8", errors="ignore") as fh:
                txt = fh.read().lower()
            if any(marker in txt for marker in _SOUL_MARKERS):
                return True
        except Exception:
            pass
    return False


def _scan(transcript_path: str):
    """Return (shipped_artifact, claimed_completion) for the CURRENT turn only.

    The scan is sliced to records after the last genuine user turn — not a flat
    multi-record tail. Without this, an edit from an earlier turn plus a completion
    word in a later analysis turn cross-trigger the gate (false-positive evidence:
    SOUL-027, and a pure-recommendation turn in this session). Turn-scoping is the
    precision fix for SOUL-F012's blast radius.
    """
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

    # Slice to the current turn: everything after the last genuine user message.
    # Tool results also arrive as role "user", so a genuine turn is a user message
    # carrying actual text, not only tool_result blocks.
    start = 0
    for i in range(len(records) - 1, -1, -1):
        if _is_real_user_turn(records[i]):
            start = i + 1
            break
    turn = records[start:]

    shipped = False
    claim_text = []
    for rec in turn:
        for block in _content(rec):
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") in _EDIT_TOOLS:
                shipped = True
            elif block.get("type") == "text":
                claim_text.append(block.get("text", ""))

    claimed = bool(_CLAIM_RE.search(" ".join(claim_text)))
    return (shipped, claimed)


def _is_real_user_turn(record) -> bool:
    """A genuine user turn — a user message with actual text, not just tool_result."""
    msg = record.get("message", record)
    if not isinstance(msg, dict) or msg.get("role") != "user":
        return False
    content = msg.get("content")
    if isinstance(content, str):
        return content.strip() != ""
    if isinstance(content, list):
        return any(
            isinstance(b, dict) and b.get("type") == "text" and b.get("text", "").strip()
            for b in content
        )
    return False


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
    # Terse by design (SOUL-I008): the gate must reach the AGENT to be actionable,
    # but verbose prose on every fire is noise and tokens.
    # Two audiences (SOUL-I018): the agent RUNS all five checks (rigor: F012, F022);
    # the BODY-facing reply must LEAD with the ask, not a rote 5-line recitation that
    # buries it. So render the result as ONE compact, specific line — name the anchor
    # or the gap — and expand only when a gap is real. A reflexive "no gaps × 5"
    # recitation is itself the F022 theater; the doctrine wants specifics, not
    # checkmarks, and "run in the open" is satisfied by a compact, anchored line.
    return (
        "[Soul gate · SOUL-F012] Shipped + claimed complete this turn — fires once.\n"
        "Run ALL of these honestly before ending:\n"
        "0. Verify the verifier: does the executor for each execution-based check EXIST "
        "and RUN? (asserted-but-never-run gates — SOUL-156/A019)\n"
        "1. Global invariant, not just local tests?\n"
        "2. Absolute claims have a VALID external anchor — trusted why / wrong if?\n"
        "   (anchor that merely EXISTS but is flawed = Coherent Falsehood — F028)\n"
        "3. Outward reach done (field/standard/user)? (else Universe Collapse)\n"
        "4. Visual artifact captured & inspected — RASTERIZE via the project's own lib + Read it (or screenshot via run/verify); 'not eyeballed' is NON-PASS. Split: (a) design-capture (headless) vs (b) target-tool render (may need Body) — name the residual (SOUL-F030/F031).\n"
        "5. Unfinished business marked (TODO/FIXME/DEBT/HACK)?\n"
        "REPLY (Body-facing): lead with the ask / next step; place the gate LAST as ONE "
        "compact line — `— Verify: clean (<anchor>)` or `— Verify: GAP → <specific>`. "
        "A GAP on the PRIMARY artifact (the thing the task exists to produce — code never "
        "compiled/run, a doc never rendered, a measurement never executed) BLOCKS: obtain "
        "an executor or stop and hand the Body the gap as a blocking question (A019). "
        "Expand to the failing check(s) only when a gap is real; do not recite passing "
        "checks. Full form: operations/completion-gate.md."
    )


if __name__ == "__main__":
    main()
