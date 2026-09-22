
## Design workflow

A personal toolkit of skills lives in `~/.claude/skills/`: `design-contract`,
`design-parity`, `rhythm-pass`, `token-audit`, `ship-check`, with executables in
`~/.claude/tools/`: `measure`, `guard`, `tokens-manifest`, `overlay-server`. It is available in
every project. These are not optional suggestions, they are how design work runs.

**Find the project's contract first.** Every design repo keeps its rules in one
file (`DESIGN_SYSTEM.md`, `DESIGN_CONTRACT.md`, a design section in `CLAUDE.md`).
Read it before changing anything, and never create a second one beside it.

**Figma is authored first, code follows, in the same session.** Never change code
without the change existing in Figma, and never leave a Figma change unmirrored.
A fix that exists in only one place is new drift, not a repair.

**Never claim done, live, or shipped without running `ship-check`.** Name the
artifact the designer is looking at, confirm it contains the change, and say plainly what
was not exercised. This is the most repeated frustration in this working
relationship and it is a verification failure every time, not a design failure.

**Never answer a visual question with a number.** No parity score, no percentage
tokenized. A score says "the properties I sampled agree", which is not "this
looks right". Put the renders side by side at matched width and look.

**Measure the result before reporting it.** A change that reasons correctly can
still render wrong. Where a value has a target, check the rendered value against
the target rather than trusting the edit.

**A raw value in a styling position is a defect.** Not a shortcut. Bind it, or
say why it is exempt.

**A build served for review carries the overlay in dev mode.** One include line,
`<script src="http://localhost:8766/overlay.js"></script>`, with
`~/.claude/tools/overlay-server` running in the project. It lets the designer
change spacing and text on the render, to tokens only, and send the result to
the session. Never ship it in a production build.

**An overlay export in `.toolkit/inbox/` is a set of decisions, applied the
same session.** Read the file, apply each change to the rule that sets the
property rather than to instances, run `guard verify` on the files touched,
run `measure --compare` at the export's width against its targets, mirror the
token changes to Figma, record each decision with `decision-log`, then move the
file to `.toolkit/applied/`. Report any target that was not reached.

**Spacing is hierarchical, never uniform.** Group first, then stack: decide what
reads as one thing, set it tight, and let the group enter the block stack. A flat
gap between unrelated blocks is the failure mode even when the value is on scale.

## Context discipline

Tool output, not conversation, is what fills a context window. Measured on one
real session: 1,744 tool results totalling 29.5MB against 278KB of actual
discussion. Tool output was 99% of everything, and single results ran past half
a megabyte. None of it was the answer the designer wanted.

**Delegate the sweep, keep the judgment.** Send work to a subagent when it will
touch more than three files, more than two screens, or a whole Figma page.
`token-auditor` and `figma-parity` exist for exactly this and are read-only.
What comes back is the finding list, and that is what belongs in the thread.

Do not delegate the decision that follows. the designer wants the judgment in the main
conversation where he can argue with it.

**Read narrowly.** Never read a large file whole to find one rule: grep for the
selector, then read the lines around it. Never dump a Figma subtree when the
question is one property. Never screenshot a full page when the question is one
component.

**Return narrowly.** When a script produces findings, have it print the findings,
not the data it derived them from. A scan of 6,000 declarations should emit
twenty lines.

**Say the number, not the list.** "862 raw values, mostly gap and height" beats
862 lines. the designer asks for the list when he wants the list.
