#!/usr/bin/env bash
# Build a carryable archive of this toolkit.
#
#   ./package.sh            -> dist/design-toolkit.tar.gz  (with the personal judgment)
#   ./package.sh --template -> dist/design-toolkit-template.tar.gz  (judgment/ template only)
#
# Use it to move the toolkit to a machine that cannot clone this repo.
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-full}"
mkdir -p "$SRC/dist"
STAGE="$(mktemp -d)/design-toolkit"
mkdir -p "$STAGE"
rsync -a --exclude='.git' --exclude='dist' "$SRC/" "$STAGE/"
if [ "$MODE" = "--template" ]; then
  find "$STAGE/judgment" -type f ! -name 'TEMPLATE.md' -delete
  OUT="$SRC/dist/design-toolkit-template.tar.gz"
else
  OUT="$SRC/dist/design-toolkit.tar.gz"
fi
tar -czf "$OUT" -C "$(dirname "$STAGE")" design-toolkit
rm -rf "$(dirname "$STAGE")"
echo "$OUT  $(du -h "$OUT" | cut -f1)"
echo
echo "On the far machine:"
echo "  tar -xzf $(basename "$OUT") -C ~ && ~/design-toolkit/install.sh"
