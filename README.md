# Design toolkit

Marc Anderson's personal toolkit for running design work with Claude Code.
Private. Not for distribution.

It exists because the standards were being hand-carried into every session as
pasted prompts, and a pasted prompt is a literal. This is the token.

## Install

```bash
./install.sh                      # into ~/.claude, available in every project
./install.sh --dry-run            # show what would happen, change nothing
./install.sh --repo PATH          # also into one repo, local only, never committed
./install.sh --copy --repo PATH   # independent per-project copies
```

Safe to re-run. It backs up anything it would replace, never overwrites
`design-judgment.md` because that file accumulates, and appends the `CLAUDE.md`
section only once.

Skills and agents register when a session **starts**, so open a new session
before using them.

## What is in it

**Seven skills.** The method.

| Skill | Does |
| --- | --- |
| `design-contract` | Writes the project's contract, or adopts the file already there |
| `session-state` | Reads and writes `STATUS.md`, so a restart loses nothing |
| `decision-log` | Records decisions, gaps and to-dos, and what they reveal about how Marc judges |
| `token-audit` | Finds unbound values in code, in Figma, and checks the two agree |
| `design-parity` | Puts the build beside its Figma frame at matched width and looks |
| `rhythm-pass` | Tightens spacing and hierarchy without redesigning anything |
| `ship-check` | Verifies the thing Marc is looking at actually contains the work |

**Two agents.** The container. Read-only, and they exist so a sweep's output
never lands in the main conversation. On one measured session, tool results were
99% of all content.

**`design-judgment.md`.** How Marc decides, so a proposal lands right the first
time rather than getting corrected. It accumulates and is never overwritten by
the installer.

**Two templates**, for a project that has nothing yet.

## The architecture

Files are organised by **rate of change**, not by topic. A fast-changing fact
inside a slow-changing document makes the whole document look stale, and then
none of it gets trusted.

| Changes | File | Scope |
| --- | --- | --- |
| Never | `~/.claude/CLAUDE.md` | The rules that bind every session |
| Rarely | `~/.claude/design-judgment.md` | How Marc decides |
| Occasionally | the project's contract | What is true in this project |
| Every session | the project's `STATUS.md` | Where the work is right now |

The skills hold rules. The contract holds values. That split is what lets the
same rhythm rule work on someone else's spacing scale, which is Marc's own test
for whether a judgment has become a system.

## Starting on a new project

First session, in order:

1. `/design-contract` reads the repo and writes the contract. If the project
   already has a `DESIGN_SYSTEM.md` or similar, it adopts that file rather than
   creating a rival.
2. `/token-audit` on its first run discovers the codebase's token dialect and
   writes it into the contract, so later runs go straight to scanning.
3. `/session-state` writes `STATUS.md`.

After that the skills fire on their own descriptions, and `/ship-check` runs
before any claim that something is done.

## Three rules the whole thing rests on

**Never answer a visual question with a number.** A parity score says "the
properties I sampled agree", not "this looks right". A sweep once reported
components clean while their thumbnails rendered landscape against portrait,
because it never measured that property.

**Prove the detector before trusting a clean result.** A scan that silently
finds nothing is worse than no scan. One pass here reported 0 raw values where
the real number was 862, because BSD grep accepted a `\b` it does not honour.

**Measure the result, do not trust the reasoning.** Four chip heights were
reasoned correctly and two still rendered wrong. The reasoning is the
hypothesis. The measurement is the result.

## Maintaining it

When a correction reveals a criterion, it goes in `design-judgment.md`. When a
method fails, the fix goes in the skill that failed, not in a note. When a rule
stops referring to one project's values, it graduates out of the contract and
into the skill, so every project gets it.
