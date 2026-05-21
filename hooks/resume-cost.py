#!/usr/bin/env python3
"""resume-cost — Step 1 of the token-economics measurement (SOUL-I005).

Measures a PROXY for "re-derivation avoided": the context a /soul-resume loads to
re-establish state (the handoff cursor + the targeted record excerpts it points to)
versus the COLD alternative (re-reading the full durable record to reconstruct state).
The ratio is a lower-bound estimate of what the cursor saves at a session boundary.

Honest about its limits (per the spec's anti-vanity invariant): this is a static
byte/token proxy, not a measured-in-session token count, and not the full
Soul-vs-non-Soul comparison the claim ultimately needs. It is the cheapest credible
first cut. Token estimate = bytes / 4 (rough English-text heuristic).

Emits one `soul.resume.cost` event to .soul/events.jsonl (the SOUL-F018 standard).
"""
import glob
import json
import os
import sys
import uuid
from datetime import datetime, timezone


def b(path):
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def tail_bytes(path, lines=90):
    try:
        with open(path, encoding="utf-8") as f:
            return len("".join(f.readlines()[-lines:]).encode("utf-8"))
    except OSError:
        return 0


def main(root="."):
    root = os.path.abspath(root)
    j = lambda *p: os.path.join(root, *p)

    # What a /soul-resume actually loads: cursor + witness tail + ideas + open findings.
    resume = {
        "handoff": b(j(".soul", "handoff.md")),
        "witness_tail": tail_bytes(j("witness.md")),
        "ideas": b(j("ideas.md")),
        "findings_open": sum(b(p) for p in glob.glob(j("findings", "open", "*.md"))),
    }
    # The cold alternative: re-read the full record to reconstruct state.
    cold = {
        "witness_full": b(j("witness.md")),
        "ideas": b(j("ideas.md")),
        "findings_all": sum(b(p) for p in glob.glob(j("findings", "**", "*.md"), recursive=True)),
    }
    resume_bytes, cold_bytes = sum(resume.values()), sum(cold.values())
    est = lambda x: x // 4
    ratio = round(resume_bytes / cold_bytes, 3) if cold_bytes else None

    project = os.path.basename(root)
    event = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": f"urn:soul:project:{project}",
        "type": "soul.resume.cost",
        "time": datetime.now(timezone.utc).isoformat(),
        "datacontenttype": "application/json",
        "data": {
            "metric": "context_bytes_proxy",
            "resume_bytes": resume_bytes,
            "cold_bytes": cold_bytes,
            "resume_est_tokens": est(resume_bytes),
            "cold_est_tokens": est(cold_bytes),
            "ratio_resume_over_cold": ratio,
            "saved_est_tokens": est(cold_bytes - resume_bytes),
            "breakdown": {"resume": resume, "cold": cold},
            "note": "static byte/token proxy; lower bound on resume savings, not an in-session token count",
        },
    }
    os.makedirs(j(".soul"), exist_ok=True)
    with open(j(".soul", "events.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event["data"], indent=2))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
