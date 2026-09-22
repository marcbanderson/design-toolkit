#!/usr/bin/env bash
# Install the design toolkit.
#
#   ./install.sh              install into ~/.claude (every project on this machine)
#   ./install.sh --repo PATH  also symlink into one repo, ignored locally, never committed
#   ./install.sh --copy --repo PATH   independent per-project copies instead of symlinks
#   ./install.sh --dry-run    show what would happen, change nothing
#   ./install.sh --judgment NAME   which judgment/<NAME>.md to install (default: marc)
#
# Safe to re-run. Existing files are backed up before being replaced, and the
# CLAUDE.md section is appended only if it is not already there.

set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HOME/.claude"
MODE="link"; REPO=""; DRY=0; JUDGMENT="marc"

while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="${2:?--repo needs a path}"; shift 2 ;;
    --copy) MODE="copy"; shift ;;
    --dry-run) DRY=1; shift ;;
    --judgment) JUDGMENT="${2:?--judgment needs a name}"; shift 2 ;;
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

# ── tools: executables the skills call ─────────────────────────────────────
run "mkdir -p '$DEST/tools'"
for t in "$SRC"/tools/*; do
  [ -f "$t" ] || continue
  say "install tool $(basename "$t")"
  run "cp '$t' '$DEST/tools/' && chmod +x '$DEST/tools/$(basename "$t")'"
done

# the overlay is a browser script, not an executable, but it lives with the
# tools because overlay-server serves it from there
say "install overlay.js"
run "cp '$SRC/overlay/overlay.js' '$DEST/tools/overlay.js'"

# ── the judgment record: never overwrite, it accumulates ───────────────────
SRC_J="$SRC/judgment/$JUDGMENT.md"
[ -e "$SRC_J" ] || { echo "No judgment file: $SRC_J" >&2
  echo "Available: $(ls "$SRC/judgment" | sed 's/\.md$//' | tr '\n' ' ')" >&2; exit 1; }
if [ -e "$DEST/design-judgment.md" ]; then
  echo "  keeping existing design-judgment.md (it accumulates; not overwritten)"
else
  say "install judgment/$JUDGMENT.md as design-judgment.md"
  run "cp '$SRC_J' '$DEST/design-judgment.md'"
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

Re-run this after adding a skill. Repo installs link each skill directory
individually, so a repo installed earlier will not see a new one until you
re-run with the same --repo.

On a new project, first session:
  1. /design-contract   writes the contract, or adopts the file already there
  2. /session-state     writes STATUS.md
Then /token-audit, /design-parity, /rhythm-pass and /ship-check as the work needs.

Tools are at ~/.claude/tools/ and the skills call them by that path:
  measure          rendered geometry at a fixed width
  guard            prove a file survived a bulk edit
  tokens-manifest  the overlay's token manifest, read from the contract
  overlay-server   serves the overlay to a dev build and receives its exports

To edit a build on screen with tokens only, in the project:
  ~/.claude/tools/overlay-server
and put its one include line in the dev build.
DONE
