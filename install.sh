#!/usr/bin/env bash
# Install the design toolkit.
#
#   ./install.sh              install into ~/.claude (every project on this machine)
#   ./install.sh --repo PATH  also symlink into one repo, ignored locally, never committed
#   ./install.sh --copy --repo PATH   independent per-project copies instead of symlinks
#   ./install.sh --dry-run    show what would happen, change nothing
#
# Safe to re-run. Existing files are backed up before being replaced, and the
# CLAUDE.md section is appended only if it is not already there.

set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HOME/.claude"
MODE="link"; REPO=""; DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="${2:?--repo needs a path}"; shift 2 ;;
    --copy) MODE="copy"; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
done

say() { [ "$DRY" = 1 ] && echo "  would $*" || echo "  $*"; }
run() { [ "$DRY" = 1 ] || eval "$@"; }

echo "Installing from $SRC"

# ── skills and agents ──────────────────────────────────────────────────────
run "mkdir -p '$DEST/skills' '$DEST/agents'"
for d in "$SRC"/skills/*/; do
  n="$(basename "$d")"
  if [ -e "$DEST/skills/$n/SKILL.md" ] && ! diff -q "$d/SKILL.md" "$DEST/skills/$n/SKILL.md" >/dev/null 2>&1; then
    say "back up existing skill $n"
    run "cp '$DEST/skills/$n/SKILL.md' '$DEST/skills/$n/SKILL.md.bak'"
  fi
  say "install skill $n"
  run "mkdir -p '$DEST/skills/$n' && cp '$d/SKILL.md' '$DEST/skills/$n/'"
done
for f in "$SRC"/agents/*.md; do
  n="$(basename "$f")"
  if [ -e "$DEST/agents/$n" ] && ! diff -q "$f" "$DEST/agents/$n" >/dev/null 2>&1; then
    say "back up existing agent $n"; run "cp '$DEST/agents/$n' '$DEST/agents/$n.bak'"
  fi
  say "install agent ${n%.md}"; run "cp '$f' '$DEST/agents/'"
done

# ── the judgment record: never overwrite, it accumulates ───────────────────
if [ -e "$DEST/design-judgment.md" ]; then
  echo "  keeping existing design-judgment.md (it accumulates; not overwritten)"
else
  say "install design-judgment.md"; run "cp '$SRC/design-judgment.md' '$DEST/'"
fi

# ── the enforcement section, appended once ─────────────────────────────────
MARK="## Design workflow"
if [ -e "$DEST/CLAUDE.md" ] && grep -qF "$MARK" "$DEST/CLAUDE.md" 2>/dev/null; then
  echo "  CLAUDE.md already carries the Design workflow section, leaving it alone"
else
  say "append Design workflow and Context discipline to CLAUDE.md"
  run "cat '$SRC/claude-md-section.md' >> '$DEST/CLAUDE.md'"
fi

# ── optional: into one repo, local only ────────────────────────────────────
if [ -n "$REPO" ]; then
  [ -d "$REPO/.git" ] || { echo "Not a git repo: $REPO" >&2; exit 1; }
  echo
  echo "Into $REPO"
  run "mkdir -p '$REPO/.claude/skills'"
  for d in "$SRC"/skills/*/; do
    n="$(basename "$d")"
    if [ "$MODE" = copy ]; then say "copy $n";  run "rm -rf '$REPO/.claude/skills/$n' && cp -R '$d' '$REPO/.claude/skills/$n'"
    else                        say "link $n";  run "ln -sfn '$DEST/skills/$n' '$REPO/.claude/skills/$n'"; fi
  done
  EX="$REPO/.git/info/exclude"
  if ! grep -qxF '.claude/skills/' "$EX" 2>/dev/null; then
    say "add .claude/skills/ to .git/info/exclude (local only, never committed)"
    run "printf '\n# personal design toolkit, local only\n.claude/skills/\n' >> '$EX'"
  fi
fi

echo
[ "$DRY" = 1 ] && { echo "Dry run. Nothing changed."; exit 0; }
cat <<'DONE'
Installed.

Skills and agents register when a session starts, so open a new session before
using them.

On a new project, first session:
  1. /design-contract   writes the contract, or adopts the file already there
  2. /session-state     writes STATUS.md
Then /token-audit, /design-parity, /rhythm-pass and /ship-check as the work needs.
DONE
