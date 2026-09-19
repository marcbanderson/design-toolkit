---
name: token-audit
description: Find every value that should be bound to a token but is not, in code, in Figma, or both, and check that the two sides agree. Use when the designer asks whether everything is tokenized, asks for a variable or styles audit, says values should be tokens, or before adopting a design system into a new codebase.
---

# Token audit

Three phases. Run all three by default. Run one when the designer names it.

1. **Code.** Raw values in a styling position.
2. **Figma.** Unbound fills, strokes, text, effects, spacing and radius.
3. **Reconcile.** Do the two token sets actually describe the same system?

Phase 3 is the point. The standard this phase serves:

> "Do you have a full understanding of the design system tokens as well as the
> design system as it is expressed and tokenized within Figma? The two of those
> things should be identical."

Run in a subagent. The scan output is large and only the findings matter.

---

## Two failures that make this skill worse than useless

Read these before writing any detector. Both were hit while validating this
skill, on a real project.

**1. A detector that silently finds nothing.** A first pass over his stylesheet
reported **0** raw values. The real number was **862**. The regex used `\b`,
which BSD grep accepts and silently does not honour. A clean result that is
wrong is worse than no result, because it manufactures the false confidence this
whole toolkit exists to prevent.

So: **every detector proves its own coverage.** Before reporting, plant a known
raw value, confirm the detector catches it, and report what you scanned
(files, declarations, nodes) alongside what you found. A report with no
denominator is not a report.

**2. An audit that cries wolf.** The first Figma pass returned 81 off-scale
spacing values. Every single one was inside a vendored Apple iOS tab bar
component. the authored components had **zero**. Had that shipped as "81
defects", the real signal would have been invisible and the audit would have
been ignored once and never run again.

So: **separate what was authored here from what was imported.** A vendored
component is not yours to tokenize. Report it as a separate, quieter line.

---

## Never regex the whole stylesheet

Three separate passes over one real stylesheet caused damage, each a
different bug, each nearly shipped: a brace scanner that destroyed every
selector inside a media query, a trim that chopped comments at their commas,
and a stash-and-restore that reinserted dead markers because nested
placeholders were restored in forward order.

**Work line by line.** Mark the token-definition blocks by line number and skip
them. Split each remaining line on its comments and only touch the code
segments. Change a value only when its property is one you are targeting.

Then prove the file survived, every time, before looking at anything else:

- braces balance
- `/*` count equals `*/` count
- a known class still exists
- no placeholder characters left behind
- byte count moved by roughly what you expected

A stylesheet that parses is not a stylesheet that is intact.

---

## The rhythm test, which the spacing test cannot see

If the project uses the `rhythm-model`, audit against **fractions of the body
line**, not only against the spacing scale. They are different questions:

- A value can be off the spacing scale and still be a clean fraction. It is not
  drift; the scale is short a step.
- A value can be on the spacing scale and not be a clean fraction. It was never
  justified, and no spacing audit will ever flag it.

Report both tests. On one real system the fraction test found 29 gaps at 4 and
19 at 6 doing a single job, which the spacing test could not see because both
values were legal.

---

## Phase 1: code

### Does this work across codebases? Only if you discover the dialect first.

The rule is universal: **a raw value in a styling position is a defect.** What
changes per project is three things, and a skill that hardcodes any of them
breaks on the next repo.

- **What a styling position looks like.** A CSS declaration, a Tailwind class, a
  key in a JS style object, a SwiftUI modifier argument.
- **What a bound value looks like.** `var(--x)`, `theme(...)`, `$x`, `@x`,
  `tokens.spacing.md`, a named Tailwind scale key, `Color("Ink")`.
- **What is legitimately exempt.** Differs by stack and by project.

**So the first run does discovery and writes the dialect into the project
contract.** Later runs read it and go straight to scanning.

Detect the family by what is in the repo, then confirm by reading real code
rather than trusting the file names:

| Family | Bound looks like | Scan |
|---|---|---|
| CSS custom properties | `var(--t-s-md)` | declarations, excluding the `:root` block that defines the tokens |
| Tailwind | `p-4`, `text-ink` | arbitrary values `p-[13px]`, `text-[#2D3459]`, plus `style=` escapes |
| Sass / Less | `$space-md` | declarations, excluding the variable file |
| CSS-in-JS | `theme.space.md`, `${space.md}` | template literals and style objects |
| Token JSON (Style Dictionary, DTCG) | a `{group.name}` alias | leaf values that are literals where a reference was intended |
| SwiftUI / Compose | `Spacing.md`, `Color("Ink")` | modifier arguments and literal `Color(...)` |
| React Native | `tokens.space.md` | `StyleSheet.create` objects and inline `style={{...}}` |

A repo may hold two layers at once, and one of one does: a generated layer
mirroring Figma one for one, and an alias layer that components consume. Both are legitimate, and the
rule differs by layer: the generated layer **holds** literals by design, the
alias layer must only ever alias, and components must consume the alias and
never the generated layer.
Write that structure into the contract; do not rediscover it each run.

### Exemptions

Not every literal is a defect. Do not report, unless the project says otherwise:

- `0`, and `100%` / `50%` used structurally
- hairlines: `1px` and `1.5px` borders and dividers
- a pill radius sentinel such as `999px`, if the project uses one
- `z-index`, `opacity`, `flex`, `line-height` given unitless
- values inside the token definitions themselves
- one-off values inside a vendored or third-party component
- geometry that is genuinely intrinsic: an icon's own viewBox, a mask size
  pinned to an asset's true dimensions

Everything else is reportable. **Component sizes are reportable.** A `height:
48px` repeated across the codebase is a size token waiting to be named, and the
"48 throughout" pass is exactly the work that happens when it is not.

### Near misses are the most valuable finding

A designer's instruction, worth generalising:

> "If something is a gap of 10, it should probably be the token for 12, and if
> it's a value of 9, it should be the token for 8."

For every raw value, snap to the nearest scale step and report both. A value one
or two off the scale is not a rounding error, it is a signal that someone
bypassed the system, and it is usually a real visual defect too.

**Four rules keep snapping honest.** A trial run on a real stylesheet broke
all four and produced nonsense like `-200px -> 0` and `100px -> 32`, which is
how a report loses a reader's trust in one line.

1. **Never snap a negative value.** Negatives are overlap, bleed and optical
   nudges. They are not spacing on a positive scale.
2. **Never snap against the wrong table.** Radius has its own scale. Letter
   spacing has its own, usually in ems or sub-pixel, and does not belong to the
   spacing ramp at all. Matching `-0.48px` letter-spacing against a spacing
   token is a category error.
3. **Cap the snap distance.** If the nearest token is more than a third of a
   step away, it is not a near miss. Report it as off-system and needing a
   human decision, with no suggestion attached.
4. **Positional offsets are mechanics, not rhythm.** `top`, `left`, `right`,
   `bottom` on an absolutely positioned element usually encode a relationship to
   another element's height, not a spacing choice. Report them in a separate,
   quieter section and never snap them by default.

Sizes are the opposite: report them loudly. A dimension repeated across the
codebase is a size token waiting to be named.

---

## Phase 2: Figma

Different failure modes entirely. A value here can be raw in seven ways.

Walk the page with `findAll`, and for each node check:

| What | Bound when | Raw when |
|---|---|---|
| Fill | `fillStyleId` set, or every paint has `boundVariables.color` | neither |
| Stroke | `strokeStyleId` set, or paints bound | neither |
| Text | `textStyleId` set | unset, or `figma.mixed` from local overrides |
| Effects | `effectStyleId` set | unset with effects present |
| Gap | `boundVariables.itemSpacing` | `itemSpacing > 0` unbound |
| Padding | `boundVariables.padding<Side>` | each side unbound |
| Radius | `boundVariables.topLeftRadius` | `cornerRadius > 0` unbound |

Watch `figma.mixed` on `textStyleId`: it means a text node carries local
overrides on part of its range, which is a detached style, not a bound one.

Three findings that only exist on this side:

- **A semantic variable holding a literal instead of an alias.** The variable
  exists, so a naive check passes, but the semantic layer is broken: `text/
  default` should alias a palette entry, not hold `#2D3459` directly. Resolve
  each variable's value per mode and check whether it is an alias.
- **Detached instances.** A component instance that has been detached is a
  future divergence with no warning attached to it.
- **Dead styles and variables.** Defined and referenced nowhere. These make the
  system look bigger than it is, which fights the "very lightweight" goal.

Report per component, not per node. Ten unbound paddings inside one component is
one fix, not ten findings.

---

## Phase 3: reconcile

The audit that neither side can do alone. Pull the Figma variable collections
and the code token set, normalise the names, and compare:

- **In Figma, missing from code.** A designed value the build cannot express.
- **In code, missing from Figma.** A value invented in the build. This is the
  drift that produces "the app is out of alignment with the Figma".
- **Same name, different value.** The worst case, because both sides pass their
  own audit and the screens still disagree.
- **Same value, different name.** Two names for one decision, which will drift
  the moment one of them changes.

Report these as pairs with both values side by side. This is the section the designer
will read first.

### A number in code that Figma derives is not a missing token

The highest-value finding in this phase is a value the code **states** and Figma
**computes**. It never shows up as a missing token, because the number is
correct; it is the wrong kind of value.

Figma auto-layout frames that HUG have no chosen height. The height is content
plus padding. When the code pins that height instead, three things follow, and
all three were found on one real component set in one pass:

- The pin restates a token. `height: 18px` on a chip whose line-height token is
  already 18 is a literal copy of a token, and it will not follow if the token
  moves.
- The pin can disagree with Figma and nobody notices, because both sides look
  deliberate. Two chips were pinned to 18 where the component hugs to 22, so the
  text sat squeezed in its own box.
- A variant can override the pin and end up smaller than the component it
  varies.

So: **when a Figma component hugs, the code should carry padding and
line-height and no height.** Ask "does Figma choose this number, or fall out of
it?" before proposing a token for it.

**The one exception, and it is a real one.** A Figma stroke set to INSIDE does
not expand its frame, so a bordered component that hugs to 18 is 18 *including*
its border. A CSS border always adds to the box. The only way to express an
inside stroke in CSS is a pinned height with `box-sizing: border-box`. Unpinning
such a component makes it grow by twice the border width. Check `strokeAlign`
before removing any height from a component that has a stroke.

**Measure after changing.** Each of the above was reasoned correctly and two of
the four still rendered wrong. Render the component and compare its box to the
Figma frame's height. The reasoning is the hypothesis; the measurement is the
result.

---

## Reporting

Coverage first, then findings, then the noise you set aside:

```
Scanned: 6,410 declarations in app.css, 2,254 nodes on Components.
Detector self-test: passed (planted value caught).

Code
  gap            219 raw   most common 12px  ->  space/md
  height         214 raw   48px x 31         ->  needs a size token
  border-radius   65 raw   near miss: 10px   ->  radius/sm is 8

Figma
  Tag / TScore        radius 12 unbound        -> radius/md
  Empty State         effect unstyled          -> needs an elevation style

Reconcile
  radius/xxs = 2px    no Figma variable        -> invented in code
  surface/secondary   #F1F4FB / code #F1F4FA   -> same name, different value

Set aside
  81 off-scale values inside vendored Apple components. Not ours to tokenize.
```

Never report a percentage tokenized. It is the same pathology as a parity score:
it answers "of the things I checked, how many passed", and the value that is
wrong is usually one the detector never looked at.

## Fixing

Fix in Figma first, then mirror to code, per the contract. Bind the component
before the instance. After any batch, re-run phase 3, because a fix on one side
is a new mismatch until the other side follows.

---

## Finding the contract

Every project keeps its rules in one file at the repo root. **Do not assume a
filename.** Look, in order, for: `DESIGN_SYSTEM.md`, `DESIGN_CONTRACT.md`,
`DESIGN.md`, a design section in `CLAUDE.md` or `AGENTS.md`, or a `docs/`
equivalent. Pick the one that names the source of truth and the spacing rules.
Use what is there rather than creating a second file beside it, which would give
the project two contracts that can disagree.

If nothing exists, load the `design-contract` skill and write one.
