#!/usr/bin/env python3
"""Measure what a completion-gate firing costs in Body-facing output (SOUL-I054).

The gate blocks one stop and forces one extra full-context turn. That turn's
INFERENCE cost is unavoidable while the gate fires at all (SOUL-F063 retuned the
RATE). What is ours to cut is the turn's OUTPUT length: the post-gate turn has
been re-stating the session summary the Body already read, on top of running the
verification. SOUL-I054 asserts this "doubles" end-of-session output — an
unanchored magnitude. This script measures it.

Method: for each firing found in Claude Code transcripts, compare the visible
assistant text of the turn that TRIGGERED the gate (pre) against the turn that
ANSWERED it (post). Visible text only — thinking blocks and tool calls are
excluded, because the restatement this targets is Body-facing prose.

    pre  = assistant text from the last genuine user turn up to the fire
    post = assistant text from the fire up to the next genuine user turn
           (or the next fire, or end of transcript)

A ratio near 1.0 means the post-gate turn writes as much as the turn it was
answering — the restatement I054 describes. A ratio well under 1.0 means the
gate turn is already adding only the verify line.

Usage:
    python3 tools/gate-cost-measure.py                      # all projects
    python3 tools/gate-cost-measure.py --since 2026-07-16   # after the F063 retune
    python3 tools/gate-cost-measure.py --json out.json      # per-fire records

Kept in the repo deliberately: the SOUL-172 measurement was done with an ad-hoc
script that was not preserved, so this analysis had to be rebuilt from scratch.
An instrument used twice belongs in the record.
"""

import argparse
import json
import os
import statistics
import sys

DEFAULT_ROOT = os.path.expanduser("~/.claude/projects")

# The gate's own banner. Matches the checklist text emitted by
# hooks/pre-completion-verify.py::_checklist(); the middle dot is U+00B7.
FIRE_MARKER = "[Soul gate · SOUL-F012]"
HOOK_FEEDBACK_PREFIX = "Stop hook feedback:"


def load_records(path):
    recs = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            for ln in fh:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    recs.append(json.loads(ln))
                except Exception:
                    continue
    except Exception:
        return []
    return recs


def message_of(rec):
    msg = rec.get("message")
    return msg if isinstance(msg, dict) else {}


def content_blocks(rec):
    content = message_of(rec).get("content")
    if isinstance(content, list):
        return content
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return []


def raw_text(rec):
    """Flat text of a record's content, whatever its shape."""
    content = message_of(rec).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            b.get("text", "") for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def is_fire(rec):
    """A gate firing: the hook's stderr fed back into the session."""
    if message_of(rec).get("role") != "user":
        return False
    txt = raw_text(rec)
    return HOOK_FEEDBACK_PREFIX in txt and FIRE_MARKER in txt


def is_real_user_turn(rec):
    """A genuine Body message — not a tool result, not hook feedback, not meta.

    Mirrors _is_real_user_turn in hooks/pre-completion-verify.py so the turn
    boundaries this script measures are the same ones the gate scopes to.
    """
    if message_of(rec).get("role") != "user":
        return False
    if rec.get("isMeta"):
        return False
    if is_fire(rec):
        return False
    content = message_of(rec).get("content")
    if isinstance(content, str):
        return content.strip() != ""
    if isinstance(content, list):
        return any(
            isinstance(b, dict) and b.get("type") == "text" and b.get("text", "").strip()
            for b in content
        )
    return False


def visible_assistant_text(rec):
    """Body-facing prose only: text blocks of assistant messages.

    Thinking blocks and tool_use blocks are excluded — the restatement I054
    targets is what the Body reads, not what the model deliberates or calls.
    """
    if message_of(rec).get("role") != "assistant":
        return ""
    return "".join(
        b.get("text", "") for b in content_blocks(rec)
        if isinstance(b, dict) and b.get("type") == "text"
    )


def span_chars(records, start, end):
    """Visible assistant characters in records[start:end]."""
    return sum(len(visible_assistant_text(r)) for r in records[start:end])


def measure_file(path, since=None):
    """Return one record per gate firing in this transcript."""
    records = load_records(path)
    if not records:
        return []

    fire_idx = [i for i, r in enumerate(records) if is_fire(r)]
    if not fire_idx:
        return []

    real_user_idx = [i for i, r in enumerate(records) if is_real_user_turn(r)]
    fire_set = set(fire_idx)

    out = []
    for i in fire_idx:
        ts = records[i].get("timestamp", "") or ""
        if since and ts and ts[:10] < since:
            continue

        # Pre-gate turn: back to the last genuine user message before the fire.
        prev_user = max((u for u in real_user_idx if u < i), default=-1)
        pre_start = prev_user + 1
        pre = span_chars(records, pre_start, i)

        # Post-gate turn: forward to the next genuine user message or next fire.
        next_user = min((u for u in real_user_idx if u > i), default=len(records))
        next_fire = min((f for f in fire_set if f > i), default=len(records))
        post_end = min(next_user, next_fire)
        post = span_chars(records, i + 1, post_end)

        out.append({
            "project": os.path.basename(os.path.dirname(path)),
            "session": os.path.basename(path).replace(".jsonl", ""),
            "timestamp": ts,
            "pre_chars": pre,
            "post_chars": post,
            "ratio": (post / pre) if pre else None,
            # The gate is the last thing in the transcript: the session ended
            # on the post-gate turn, so this fire's cost is pure end-of-session.
            "ended_session": post_end >= len(records),
        })
    return out


def summarize(fires, label):
    if not fires:
        print(f"{label}: no firings found")
        return
    pre = [f["pre_chars"] for f in fires]
    post = [f["post_chars"] for f in fires]
    ratios = [f["ratio"] for f in fires if f["ratio"] is not None]

    print(f"\n{label}")
    print(f"  firings:            {len(fires)}")
    print(f"  sessions:           {len(set((f['project'], f['session']) for f in fires))}")
    print(f"  projects:           {len(set(f['project'] for f in fires))}")
    print(f"  pre-gate  chars:    median {statistics.median(pre):>8.0f}   mean {statistics.mean(pre):>8.0f}")
    print(f"  post-gate chars:    median {statistics.median(post):>8.0f}   mean {statistics.mean(post):>8.0f}")
    if ratios:
        print(f"  post/pre ratio:     median {statistics.median(ratios):>8.2f}   mean {statistics.mean(ratios):>8.2f}")
    print(f"  total post chars:   {sum(post):,}  (~{sum(post)//4:,} tokens of Body-facing output)")
    ended = [f for f in fires if f["ended_session"]]
    print(f"  ended the session:  {len(ended)} of {len(fires)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=DEFAULT_ROOT, help=f"transcript root (default {DEFAULT_ROOT})")
    ap.add_argument("--since", help="only firings on/after this date (YYYY-MM-DD)")
    ap.add_argument("--json", help="write per-firing records to this path")
    ap.add_argument("--by-project", action="store_true", help="break the summary down per project")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print(f"transcript root not found: {args.root}", file=sys.stderr)
        sys.exit(1)

    fires = []
    scanned = 0
    for dirpath, _dirnames, filenames in os.walk(args.root):
        for fn in filenames:
            if not fn.endswith(".jsonl"):
                continue
            scanned += 1
            fires.extend(measure_file(os.path.join(dirpath, fn), since=args.since))

    print(f"scanned {scanned} transcripts under {args.root}")
    if args.since:
        print(f"window: firings on/after {args.since}")
    summarize(fires, "ALL FIRINGS")

    if args.by_project:
        for proj in sorted(set(f["project"] for f in fires)):
            summarize([f for f in fires if f["project"] == proj], f"  · {proj}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(fires, fh, indent=2)
        print(f"\nper-firing records → {args.json}")


if __name__ == "__main__":
    main()
