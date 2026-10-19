#!/usr/bin/env bash
# Scaffold: a tiny pricing module with an off-by-one bulk-discount bug and a test
# file that already encodes the right behaviour. Runs inside the empty run dir.
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
W
git init -q
git config user.email "eval@example.com"
git config user.name "Eval"

mkdir -p shipcalc
touch shipcalc/__init__.py
cat > shipcalc/pricing.py <<'PY'
"""Order pricing helpers."""

BULK_THRESHOLD = 10
BULK_RATE = 0.10


def order_total(quantity, unit_price):
    """Total price for an order. Orders of BULK_THRESHOLD units or more get BULK_RATE off."""
    total = quantity * unit_price
    if quantity > BULK_THRESHOLD:
        total = total * (1 - BULK_RATE)
    return round(total, 2)
PY
cat > test_pricing.py <<'PY'
import unittest

from shipcalc.pricing import order_total


class OrderTotalTests(unittest.TestCase):
    def test_small_order_has_no_discount(self):
        self.assertEqual(order_total(3, 5.0), 15.0)

    def test_large_order_gets_discount(self):
        self.assertEqual(order_total(20, 5.0), 90.0)

    def test_exactly_threshold_gets_discount(self):
        self.assertEqual(order_total(10, 5.0), 45.0)


if __name__ == "__main__":
    unittest.main()
PY
git add -A && git commit -q -m "initial commit"
