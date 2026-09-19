---
name: design-parity
description: Check a built screen against its Figma frame by putting them side by side at the same width and looking. Use when Marc asks whether the build matches Figma, says a screen is "still off" or "out of alignment", or before opening a PR that touches design. Reports defects, never a score.
---

# Design parity

Run this in a subagent whenever the sweep covers more than two screens. The
per-screen tool output is large and Marc does not need it in the main thread.
Return the defect list only.

## The rule this exists to enforce

**Never report a percentage as an answer to a visual question.** Marc was handed
a parity sweep reporting per-tier percentages and asked instead: *"Does
everything look exactly like Figma?"* He was right, and it was measurable: a
sweep across 14 properties and 1141 units reported the sportscard components
clean while their thumbnails rendered landscape where Figma authored portrait.
The sweep had never measured the property that was wrong. Four real defects were
found only by putting the two renders side by side, and none of them moved the
score.

A score answers "do the properties I sampled agree". It does not answer "does
this look right". The measured pass is for catching regression in what it
already measures. It never certifies fidelity.

So: **look first, measure second, and report defects rather than a number.**

## Finding the contract

Every project keeps its rules in one file at the repo root. **Do not assume a
filename.** Look, in order, for: `DESIGN_SYSTEM.md`, `DESIGN_CONTRACT.md`,
`DESIGN.md`, a design section in `CLAUDE.md` or `AGENTS.md`, or a `docs/`
equivalent. Pick the one that names the source of truth and the spacing rules.
Use what is there rather than creating a second file beside it, which would give
the project two contracts that can disagree.

If nothing exists, load the `design-contract` skill and write one.

## Method

**1. Match the width before you compare anything.**

Marc's own correction: *"Can you just make the Playground 393? Why so you get a
one-to-one comparison?"* A comparison at two different widths is not a
comparison. Render the build at the Figma frame's exact width. If the frame is
393, the viewport is 393.

**2. Get both images.**

- Figma: `get_screenshot` on the frame node.
- Build: run it and screenshot at the frame width. If it will not run locally
  (a backend dependency, no offline mode), serve the template statically and
  drive the client state directly to reach the screen. A static serve makes
  every API call fail, which is exactly right for checking empty and loading
  states, and is a genuine test of rendering, CSS and state logic. Say plainly
  in your report that the API paths were not exercised.

**3. Look at them side by side, and name what is wrong.**

Work down in this order, because this is the order Marc notices things:

- **Vertical rhythm.** He reads tight spacing as a defect before anything else.
  Check the gaps against the contract's ladder. A pair that should be grouped
  and sitting at the group value, but is sitting at the block value, is a
  defect even though both numbers are on the ladder.
- **Proportion inside components.** Two things that should scale together but
  are not: an icon that stepped down 0.5 while its label stepped 0.75 reads as
  broken even when both values are on scale.
- **Alignment and edges.** Gutters, left edges down a column, optical centering.
- **Type.** Size, weight, line height, case. He notices weight before size.
- **Missing or fabricated data.** A blank where a value should be, a zero
  standing in for an absent number, a dash doing a word's job.
- **State coverage.** Does the screen have a loading, empty and sparse
  treatment, or only the populated one?

**4. Only now, measure.**

Use computed styles or node properties to confirm what you saw and to catch
regression in the same properties next time. Measurement supports the finding.
It does not generate it.

## Reporting

One line per defect. Each line says where, what is wrong, and what it should be.

```
Card Detail / Market  Empty tab renders nothing. Needs the Empty State
                      component; it exists in Figma (85:693) and had no code
                      equivalent at all.
Wantlist / Wants      Chart legend sits 24 from its chart. It reads the chart,
                      so it belongs to it at 8. Group it, then stack.
```

No score. No percentage. If you found nothing, say you found nothing and name
what you looked at, so Marc knows the coverage of the claim.

## What counts as done

A defect is fixed when it is fixed **in both places**: corrected in Figma first,
then mirrored in code, per the contract's direction. A fix that exists only in
code is a new drift, not a repair.
