# Design toolkit

A toolkit for running design work with Claude Code, between Figma and a
codebase. One repo, pulled into any project.

It exists because a designer's standards get hand-carried into every session as
pasted prompts, and a pasted prompt is a literal. This makes them tokens:
written once, applied everywhere, improved in one place.

## Use it in a project

```bash
git -C ~/design-toolkit pull        # get the latest
~/design-toolkit/install.sh         # into ~/.claude, every project on this machine
```

That is usually all you need: `~/.claude` is personal scope, so the skills are
live in every repo. Install into a specific repo only when you want repo-local
copies or a machine that cannot see your home directory:

```bash
./install.sh --repo /path/to/repo          # symlinks, local only, never committed
./install.sh --copy --repo /path/to/repo   # independent copies you can diverge
./install.sh --dry-run                     # show what would happen
```

Repo installs register the path in `.git/info/exclude`, which is per-clone and
never pushed. Your team sees nothing.

**Re-run after adding a skill.** Repo installs link each skill directory
individually, so a repo installed earlier will not see a new one until you
re-run with the same `--repo`.

Skills and agents register when a session **starts**, so open a new session
after installing.

## Layout

```
skills/        nine skills, the methods. Written neutrally.
agents/        two read-only agents, so a sweep's output stays out of the thread
judgment/      the only personal layer
  marc.md        one designer's criteria, accumulated
  TEMPLATE.md    empty, with instructions for building your own
templates/     a contract and a STATUS file for a project that has nothing
claude-md-section.md   the enforcement rules, appended to ~/.claude/CLAUDE.md
```

Everything except `judgment/` is impersonal. That is the point: the methods are
the same for anyone, the criteria are not.

## The skills

| Skill | Does |
| --- | --- |
| `design-contract` | Writes the project's contract, or adopts the file already there |
| `session-state` | Reads and writes `STATUS.md`, so a restart loses nothing |
| `decision-log` | Records decisions and gaps, and what they reveal about how the designer judges |
| `taste-extract` | Recovers a designer's grammar for spacing, type and colour from work they hand-tuned |
| `rhythm-model` | Derives spacing from the type rather than choosing it, and sets density |
| `token-audit` | Finds unbound values in code, in Figma, and checks the two agree |
| `design-parity` | Puts the build beside its Figma frame at matched width and looks |
| `rhythm-pass` | Tightens spacing and hierarchy without redesigning anything |
| `ship-check` | Verifies the thing on screen actually contains the work |

## The architecture

Files are organised by **rate of change**, not by topic. A fast-changing fact
inside a slow-changing document makes the whole document look stale, and then
none of it gets trusted.

| Changes | File | Scope |
| --- | --- | --- |
| Never | `~/.claude/CLAUDE.md` | The rules that bind every session |
| Rarely | `~/.claude/design-judgment.md` | How this designer decides |
| Occasionally | the project's contract | What is true in this project |
| Every session | the project's `STATUS.md` | Where the work is right now |

**Grammar travels, vocabulary does not.** A design system copied between
projects hands over the values, which belong to the project they came from.
What transfers is how many distinct values are allowed, the ratios between them,
and which relationship gets which. `taste-extract` recovers that from work the
designer has already done, so a new project is informed by their taste without
inheriting another project's numbers.

## Starting on a new project

1. `/design-contract` reads the repo and writes the contract, or adopts the file
   already there rather than creating a rival.
2. `/token-audit` on its first run discovers that codebase's token dialect and
   writes it into the contract, so later runs go straight to scanning.
3. `/session-state` writes `STATUS.md`.
4. When three to five screens have been hand-tuned, `/taste-extract` recovers
   the grammar and writes it into the contract.

After that the skills fire on their own descriptions, and `/ship-check` runs
before any claim that something is done.

## Three rules the whole thing rests on

**Never answer a visual question with a number.** A parity score says "the
properties I sampled agree", not "this looks right". A sweep once reported
components clean while their thumbnails rendered landscape against portrait,
because it never measured that property.

**Prove the detector before trusting a clean result.** A scan that silently
finds nothing is worse than no scan. One pass reported 0 raw values where the
real number was 862, because BSD grep accepted a `\b` it does not honour.

**Measure the result, do not trust the reasoning.** Four chip heights were
reasoned correctly and two still rendered wrong. The reasoning is the
hypothesis. The measurement is the result.

## Maintaining it

When a correction reveals a criterion, it goes in the judgment file. When a
method fails, the fix goes in the skill that failed, not in a note. When a rule
stops referring to one project's values, it graduates out of the contract and
into the skill, so every project gets it.

The toolkit is meant to be edited. The skills are opinionated because vague
instructions produce vague work, but the opinions are a starting position. Where
one is wrong for how you work, change it rather than working around it.
