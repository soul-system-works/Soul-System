#!/usr/bin/env python3
"""Wire a verified live contract into a project's Codex instruction file.

Only this managed block is replaced. Record scaffolding and tracking preferences
remain in soul-init's owner-facing workflow; this helper never chooses them.
"""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- soul-system:codex:start -->"
END = "<!-- soul-system:codex:end -->"


def instruction_file(project):
    override = project / "AGENTS.override.md"
    # An empty override is skipped by Codex. Filling it would unexpectedly hide
    # all existing AGENTS.md rules, so keep wiring in the file already active.
    return override if override.is_file() and override.read_text(encoding="utf-8").strip() else project / "AGENTS.md"


def contract_reference(text):
    for line in text.splitlines():
        if line.startswith("Soul contract: `") and line.endswith("`."):
            return Path(line[len("Soul contract: `"):-2]).expanduser()
    return None


def wire(project):
    contract = ROOT / "operations" / "CLAUDE.md"
    contract.read_text(encoding="utf-8")
    if project == ROOT:
        raise ValueError("This source repo already has AGENTS.md; initialize an adopting project.")
    target = instruction_file(project)
    if target.is_symlink():
        raise ValueError("Instruction file is a symlink; review its target before changing it.")
    # Preserve surrounding CRLF and arbitrary spacing: only the managed block
    # belongs to this helper, even on Windows checkouts.
    text = target.read_bytes().decode("utf-8") if target.exists() else ""
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError("Malformed or duplicate Soul block; review it before retrying.")
    path = str(contract)
    try:
        path = "~/" + str(contract.relative_to(Path.home()))
    except ValueError:
        pass
    block = f"""{START}
## Soul System — Codex

Soul contract: `{path}`.
Before working, read that contract explicitly; Codex does not expand Claude @imports.
If it cannot be read, report the missing path and repair with $soul-system:soul-init before proceeding.
Read the existing mind.md (project root or .soul/), and the witness.md tail in its
existing layout. If both copies of a store exist, resolve the ambiguity first.
Read project CLAUDE.md, if present, for local Register and Stage declarations;
its @imports are not automatically loaded. Keep existing project instructions.
Use the same records and .soul/handoff.md as Claude. Invoke skills with $soul-system:soul-….
After plugin updates, run $soul-system:soul-resume to check wiring; rerun $soul-system:soul-init if stale.
The completion hook requires a supported local client and explicit hook trust;
project scoping alone does not prove the gate is armed.
{END}"""
    newline = "\r\n" if "\r\n" in text else "\n"
    block = block.replace("\n", newline)
    if START in text:
        start = text.index(START)
        end = text.index(END) + len(END)
        if end <= start:
            raise ValueError("Reversed Soul block markers; review before retrying.")
        updated = text[:start] + block + text[end:]
    else:
        updated = text + (newline * 2 if text and not text.endswith(newline * 2) else "") + block + newline
    target.write_bytes(updated.encode("utf-8"))
    return target


def status(project):
    target = instruction_file(project)
    text = target.read_text(encoding="utf-8") if target.exists() else ""
    block = text.split(START, 1)[-1].split(END, 1)[0] if START in text and END in text else ""
    reference = contract_reference(block)
    current = ROOT / "operations" / "CLAUDE.md"
    readable = reference is not None and reference.is_file()
    matches = readable and reference.read_bytes() == current.read_bytes()
    return {
        "instruction_file": str(target),
        "contract": str(reference) if reference else None,
        "contract_readable": readable,
        "contract_matches_installed": bool(matches),
        "instruction_file_bytes": target.stat().st_size if target.exists() else 0,
        "instruction_budget": "check host project_doc_max_bytes and the whole instruction chain",
        "installed_contract_sha256": hashlib.sha256(current.read_bytes()).hexdigest(),
        "gate": "unknown: verify this session's hook context and a live edit/Stop exercise",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("wire", "status"))
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()
    try:
        project = args.project.expanduser().resolve(strict=True)
        if not project.is_dir():
            parser.error("--project must name an existing directory")
        if args.action == "wire":
            print(wire(project))
        else:
            print(json.dumps(status(project), indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Soul Codex wiring: {exc}\n")


if __name__ == "__main__":
    main()
