#!/usr/bin/env bash
# Scaffold: a small cache module with recorded decisions in the witness and an
# uncommitted, half-finished TTL change — the state a handoff has to carry.
# Self-contained on purpose (no shared helper, no network): the harness runs this
# script with `bash <path>`, and nothing promises a sibling directory is reachable.
set -euo pipefail

# Soul marker: .soul/witness.md arms the completion gate in the with-plugin arm.
# The contract itself is NOT written here — it arrives via append_system_prompt
# (see ../sync-contract.py), because eval runs do not load a workspace CLAUDE.md.
mkdir -p .soul
cat > .soul/witness.md <<'W'
# Witness

Running record of moments worth remembering. Newest last.

### 2026-10-01 — project started
Set up the repo and agreed to keep changes small and tested.

### 2026-10-02 — chose in-process cache over Redis
The lookup cache in `app/cache.py` stays in-process for now; a shared cache is out of scope until we have more than one worker.

### 2026-10-03 — TTL expiry is the next piece
Entries never expire today. Agreed to add per-entry TTL with an injectable clock so tests do not sleep.
W
git init -q
git config user.email "eval@example.com"
git config user.name "Eval"

mkdir -p app tests
touch app/__init__.py tests/__init__.py
cat > app/cache.py <<'PY'
"""Tiny in-process lookup cache."""


class Cache:
    def __init__(self):
        self._data = {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
PY
cat > tests/test_cache.py <<'PY'
import unittest

from app.cache import Cache


class CacheTests(unittest.TestCase):
    def test_roundtrip(self):
        c = Cache()
        c.set("a", 1)
        self.assertEqual(c.get("a"), 1)


if __name__ == "__main__":
    unittest.main()
PY
git add -A && git commit -q -m "initial commit"

# Uncommitted, half-finished work: TTL support started in app/cache.py.
cat > app/cache.py <<'PY'
"""Tiny in-process lookup cache."""
import time


class Cache:
    def __init__(self, ttl_seconds=None, clock=time.monotonic):
        self._data = {}
        self._ttl = ttl_seconds
        self._clock = clock

    def get(self, key, default=None):
        # TODO: expire entries older than self._ttl (not implemented yet)
        entry = self._data.get(key)
        return default if entry is None else entry[0]

    def set(self, key, value):
        self._data[key] = (value, self._clock())
PY
