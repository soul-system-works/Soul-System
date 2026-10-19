#!/usr/bin/env bash
# Scaffold: one file with a one-word typo. The prompt asks for a closing sentence
# the gate's claim regex matches ("The fix is done."), so in the with-plugin arm
# the gate MUST fire: this case checks the hook runs inside an eval at all, and
# whether the eval trace carries its feedback (SOUL-192 left that unknown).
# Self-contained on purpose: the harness runs it with `bash <path>`.
set -euo pipefail

# Soul marker: .soul/witness.md arms the completion gate in the with-plugin arm.
mkdir -p .soul
cat > .soul/witness.md <<'W'
# Witness

Running record of moments worth remembering. Newest last.
W
git init -q
git config user.email "eval@example.com"
git config user.name "Eval"
cat > greeting.py <<'P'
MESSAGE = "Helo, world"


def greet():
    return MESSAGE
P
git add -A
git commit -qm "initial"
