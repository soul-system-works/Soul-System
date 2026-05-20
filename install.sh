#!/bin/bash

# Soul System installer
# Usage: ./install.sh /path/to/your/project

set -e

SYSTEM_VERSION="0.3.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1}"

if [ -z "$TARGET" ]; then
  echo "Usage: ./install.sh /path/to/your/project"
  exit 1
fi

if [ ! -d "$TARGET" ]; then
  echo "Error: target directory does not exist: $TARGET"
  exit 1
fi

echo "Installing Soul System v${SYSTEM_VERSION} into ${TARGET}..."

# Copy operational documents
cp -r "$SCRIPT_DIR/operations/." "$TARGET/"

# Write version record
cat > "$TARGET/.soul-version" << EOF
system_version: ${SYSTEM_VERSION}
installed: $(date +%Y-%m-%d)
source: ${SCRIPT_DIR}
EOF

echo ""
echo "Done. Next steps:"
echo "  1. Read philosophy/the-soul.md in this repo — once, slowly"
echo "  2. Open autonomous-session-template.md in your project"
echo "  3. Fill in the problem slot and start your session"
echo ""
echo "Soul System version ${SYSTEM_VERSION} installed."
