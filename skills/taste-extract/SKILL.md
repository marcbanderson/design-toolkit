---
name: taste-extract
description: Infer a designer's grammar for spacing, type and colour from screens they have hand-tuned, and write it into the project contract. Use at the start of a project after a calibration set exists, when asked how to apply someone's taste to a new codebase, or when a design system needs rules rather than a copied palette.
---

# Taste extract

A design system copied between projects gives you someone's **vocabulary**, which
is the wrong half. The values belong to the project they came from. What
transfers is the **grammar**: how many distinct values are allowed, the ratios
between them, and which relationship gets which.

This skill recovers the grammar from work the designer has already done, so a new
project is informed by their taste without inheriting another project's numbers.

---

## The calibration set

Ask for **three to five screens they have hand-tuned** and consider right. Not
screens they approved, screens they actively adjusted. A correction carries more
signal than an acceptance, because an acceptance might just be tolerance.

Choose for variety, not volume: a dense screen, a sparse one, a form, and
something with data in it. Three frames were enough to recover a full spacing
grammar on a real project.

This inverts the usual cost. Instead of one correction per screen for weeks,
they spend concentrated effort once on screens they pick, and everything else is
derivation.

---

## The unit of analysis is the relationship, not the value

Do not histogram every gap in the file. That returns a list of numbers, which is
vocabulary. Record **what each distance separates**, then ask what distance each
kind of relationship reliably gets.

On a real extraction that meant classifying every adjacency as: text to text,
head to content, content to action, or block to block. The answer came out as
"content to action is always one unit, nine times out of nine, no variation",
which is a rule. "24 appears 47 times" is not.

---

## Three filters, and they encode judgment

The first run of this on a real file returned three distinct distances. One was
noise. Get these wrong and you will produce a confident, wrong grammar.

1. **Drop gaps that render nothing.** A container with one child has a gap that
   separates nothing. It will still show up in a naive scan.
2. **Drop runs of identical items.** A row of three stat tiles or a list of
   bullets has a list rhythm, not a reading rhythm. Detect by whether every
   child shares a name or a main component.
3. **Separate component internals from the reading flow.** This is the important
   one. On the project this skill was built from, the designer used only two
   distances between things a reader reads, while components internally used
   three more. Mixing them makes the grammar look twice as loose as it is.
   Detect by whether the node is an instance or sits inside one.

Say which filters you applied when you report. A grammar is only as trustworthy
as the definition of what counted.

---

## Spacing

Derive the unit first, per the `rhythm-model` skill: it is the body text's
line-height. Then express every measured distance as a fraction of it, and
report:

- **How many distinct distances** appear in the reading flow. This is the single
  most characteristic number. Two is a strong, opinionated grammar. Five is a
  weak one, and usually reads as "everything is evenly spaced".
- **The ratio between them.** A 6x spread between bound and separate reads very
  differently from a 1.5x spread, at any scale.
- **The block boundary**, usually a multiple of the separate value.
- **Which relationship gets which distance**, as a table.

The output is portable. A grammar of "two distances, 6x apart, blocks at 2x"
applied to a project whose unit is 32 gives roughly 5, 32 and 64. Same taste,
different numbers.

---

## Type

Measure usage, not the style sheet. A defined ramp tells you what is available;
usage tells you what is believed.

- **Weights actually used.** A retired weight that still appears is a rule not
  holding. A ramp with three weights in use is a decision; six is a default.
- **Sizes actually used**, and the **step ratio** between adjacent ones. Steps
  under about 1.2x are hard to read as hierarchy: a 14 against a 16 is a 14%
  difference and registers as noise rather than rank.
- **Distinct sizes per screen**, as a median. This is the type equivalent of
  "how many distinct distances", and it is worth comparing the two. A system
  with two spacing distances and five type sizes per screen is using opposite
  philosophies in the two axes, and the type is usually the half that is wrong.
- **Line-height against the spacing unit.** Per Müller-Brockmann, a whole number
  of small-type lines should equal a whole number of body lines. Flag any
  heavily used size whose line-height has no small common multiple with the
  unit, because that is the one quietly breaking the grid.

---

## Colour

Convert every value to relative luminance and hue before comparing anything.
Hex strings and names tell you nothing about whether a hierarchy works.

For each family (text, surface, icon, border, status, chart) report:

- **The lightness ladder**, sorted. A hierarchy that steps cleanly in lightness
  is robust; one that does not is relying on hue.
- **How many hues** the family spans.
- **Whether the family separates by lightness or by hue.** This is the grammar
  question, and different families legitimately answer differently.

**Then run the contrast check, and treat it as a first-class finding.** For any
pair that carries opposite meaning, positive against negative most of all,
report the lightness difference. A pair separated by under about 10 points of
luminance is distinguished almost entirely by hue.

That matters generally and it matters more for a designer with colour vision
deficiency, where hue separation alone is not separation. On the project this
was built from, the chart palette was seven colours in a single hue band
separated purely by lightness, which is exactly right, while the positive and
negative text colours sat 2.5 luminance points apart and differed only in red
against green. The same file contained both the rule and its violation, and only
measuring found it.

---

## What does not extract

Say so plainly rather than inferring it.

- **Composition.** What goes on a screen, in what order, what gets cut. A single
  observation is a hypothesis, not a rule, and encoding it produces confident
  nonsense.
- **When to break a rule.** Deliberate exceptions look identical to defects in
  any measurement.
- **Whether a thing is beautiful.**

If a pattern appears once, record it as a hypothesis to test against the next
hand pass, and label it as one.

---

## Output

Write the grammar into the project contract, not into a separate file, and state
it as relationships rather than values so it survives being moved:

```markdown
## Grammar, extracted <date> from <the calibration frames>

Spacing   two distances in the reading flow, 1/6 u and 1 u, roughly 6x apart.
          Blocks at 2 u. Middle values only inside components.
          Content to action is always the separate value, never the bound one.
Type      three weights. Steps of at least 1.2x. Aim for three distinct sizes
          per screen. Line-heights share a small multiple with the unit.
Colour    text and icon hierarchies separate by lightness in one hue family.
          Charts separate by lightness, never hue alone. Opposed pairs need
          10+ points of luminance difference.
```

Re-run it after the next few hand passes. A grammar that changes is a grammar
that was read from too small a sample; a grammar that holds across three passes
is one you can apply without asking.
