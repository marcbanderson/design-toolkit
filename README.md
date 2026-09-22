# Design toolkit

A toolkit for running design work with Claude Code, between Figma and a
codebase. One repo, pulled into any project.

It exists because a designer's standards get hand-carried into every session as
pasted prompts, and a pasted prompt is a literal. This makes them tokens:
written once, applied everywhere, improved in one place.

## Install

First time on a machine:

```bash
git clone https://github.com/marcbanderson/design-toolkit.git ~/design-toolkit
~/design-toolkit/install.sh
```

That is usually all you need. `~/.claude` is personal scope, so the skills are
live in every repo on the machine. Install into a specific repo only when you
want repo-local copies, or when a session runs somewhere that cannot see your
home directory:

```bash
./install.sh --repo /path/to/repo          # symlinks, local only, never committed
./install.sh --copy --repo /path/to/repo   # independent copies you can diverge
./install.sh --judgment TEMPLATE           # install without the personal judgment file
./install.sh --dry-run                     # show what would happen, change nothing
```

Repo installs register the path in `.git/info/exclude`, which is per-clone and
never pushed. Your team sees nothing.

## Pulling updates

The toolkit changes as it learns. To take the latest:

```bash
git -C ~/design-toolkit pull
~/design-toolkit/install.sh
```

Then **open a new session**. Skills and agents register when a session starts,
so a running session will not see the update.

Three things worth knowing about how updates propagate:

- **A default install copies.** `~/.claude/skills/` holds copies, so pulling
  alone changes nothing until you re-run `install.sh`.
- **A repo install symlinks.** A repo installed with `--repo` points at
  `~/.claude/skills/`, so once you re-run the installer, every linked repo sees
  the edit at the same time. `--copy` installs do not; they are deliberately
  frozen until you re-run with `--copy` again.
- **New skills need the installer re-run per repo.** Repo installs link each
  skill directory individually, so a repo set up earlier will not see a skill
  added later until you re-run with the same `--repo`. Edits to existing skills
  propagate on their own; only new ones need this.

Re-running is always safe. It backs up anything it would replace and never
overwrites `design-judgment.md`, because that file accumulates and is the one
part worth more than everything around it.

## Contributing back

The judgment file and the skills both sharpen through use. When a session
records a new criterion or fixes a method, commit it here and push, so the next
project starts from what the last one learned:

```bash
cd ~/design-toolkit && git add -A && git commit -m "..." && git push
```

## Layout

```
tools/         executables the skills call, so a check is run rather than rewritten
overlay/       the on-screen editor: overlay.js, a demo screen, and its README
docs/          the web view (index.html) and the overlay demo (demo/), one
               self-contained page each, served by GitHub Pages
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

## The web view

`docs/index.html` is one self-contained page: every skill, agent and executable
with what it does and its full source, plus the judgment file rendered as prose.
Open it in a browser, or through GitHub Pages. Rebuild after a change with
`python3 docs/build.py`; add `--vision` to include the vision
record section, which is left out of the committed copy because that file is
not in this repo.

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

## The tools

Skills are instructions; tools are executables. The difference matters because a
rewritten check is a check that can be wrong differently each time.

| Tool | Does | Exists because |
| --- | --- | --- |
| `measure` | Rendered geometry at a fixed width, as JSON, with `--compare` to diff two runs | Three measurement errors in one day, all from hand-rolling the harness |
| `guard` | Proves a file survived a bulk edit: braces, comment pairs, stray placeholders, byte delta, selector collapse | A whole-file regex destroyed a stylesheet and was nearly committed |
| `tokens-manifest` | Reads the contract's ladder, ramp and weights and emits the manifest the overlay picks from | The overlay must offer the contract's tokens, not a copy of them |
| `overlay-server` | Serves the overlay to a dev build from one include line and writes its exports to `.toolkit/inbox/` | The paste step between "I changed it on screen" and "the session applies it" |
| `cssdiff` | Proves a stylesheet edit changes nothing that renders: same DOM, swap the `<link>`, diff every computed property of every element. `--tokens` resolves custom properties per palette and theme | Three refactors passed a careful static safety check and still changed rendering |

They install to `~/.claude/tools/` and the skills call them by that path.
`measure` drives headless Chrome over the DevTools protocol with no npm
dependencies. Both exit non-zero on failure, so either can gate a commit.

Their coverage is deliberately complementary. Revert a spacing rule and `guard`
says the file is fine, because it is; `measure --compare` reports the three gaps
that went from 24 to 12; `cssdiff` answers the different question of whether a
refactor that *should* be inert actually is.

Three rules `cssdiff` enforces that a hand-rolled harness will not:

- **It self-tests.** Run it with `--before` and `--after` identical first. It
  must report zero. An uncached first swap once reported 883 phantom differences
  on whichever screen was measured first.
- **It checks the served file against the file on disk** (`--verify PATH`) and
  aborts on a mismatch. A stale server on a familiar port silently serves a
  different checkout that looks identical, and every reading off it is a false
  pass. That cost two separate sessions.
- **It separates custom properties from rendered ones.** Deleting a variable
  shows up on every element that inherits it and says nothing about pixels.

`--tokens` exists because **a token system cannot be checked in the mode you
designed in.** Six semantic aliases once resolved correctly in Light and Dark
while both brand palettes silently rendered the default palette's colours.

## The overlay

A panel that sits on top of the running build. Click an element, see its gap,
padding, margin and text as tokens, change them only to other tokens, and watch
the render move. Changes reduce to net decisions (a change you reverse drops
out) and export as a prompt that asks the session to apply them to the source
rule, verify by measurement, mirror to Figma and record the decisions.

In the project:

```bash
~/.claude/tools/overlay-server          # reads the contract, serves the script, receives exports
```

In the dev build, and only the dev build:

```html
<script src="http://localhost:8766/overlay.js"></script>
```

Send to session writes `.toolkit/inbox/<stamp>-overlay.md`, which is local
only. The standing rule in `claude-md-section.md` says what a session does with
it. `overlay/demo.html` is a sample screen with seeded defects to try it on, and
`docs/demo/` is the same page for anyone viewing the repo: preview and export
work there, apply needs the server.

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
