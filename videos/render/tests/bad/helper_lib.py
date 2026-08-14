"""Negative fixture: the sibling a custom module must not reach for.

Neither denylist-scanned nor hashed into the manifest — which is exactly why
lint refuses the import that would pull it in.
"""

GREETING = "invisible to every gate"
