---
name: rhythm-model
description: Derive a spacing system from the type rather than choosing it, and set its density. Use when starting a design system, when asked where spacing values should come from, when a spacing scale and a type ramp disagree, or when a system should be made looser or denser as a whole.
---

# Rhythm model

A spacing scale chosen independently of the type ramp is two systems that happen
to sit near each other. This derives one from the other, so there is a reason for
every value and the reason survives being moved to a different scale.

After Josef Müller-Brockmann, *Grid Systems in Graphic Design*. His grid is not a
set of measurements, it is a derivation: field depth is a count of text lines,
and the vertical distance between fields is one or more blank lines (p.11, p.57).
The unit is the line, not the millimetre.

---

## 1. The unit is the body line

**u = the line-height of body text.** Not the font size. Everything vertical is
counted in `u`.

This is the whole model. If you take nothing else, take this: spacing is measured
in lines of the text it separates.

## 2. Choose a leading that makes a composite unit

The relations below are fractions of `u`, so `u` must divide well. This is a real
constraint, not a nicety, and it is why some systems feel arbitrary: their unit
cannot be halved or thirded without producing decimals.

Score a candidate by how many of the ladder fractions give whole numbers:

| Unit | Whole-number fractions |
|---|---|
| 24, 36 | 8 of 8 |
| 18, 30 | 7 of 8 |
| 21 | 6 of 8 |
| 16, 20, 28, 32 | 4 of 8 |
| 22, 26 | 3 of 8 |

So pick the leading ratio that lands `u` on a composite number, rather than
picking a round ratio and accepting whatever unit falls out. Body 16 at 1.5 gives
24. Body 18 at 1.333 also gives 24. Body 14 at 1.286 gives 18.

Müller-Brockmann's own worked examples use 12pt (10pt type, 2pt lead), which
divides by 2, 3, 4 and 6.

## 3. The relations

One ladder of simple fractions, in order:

```
1/6   1/4   1/3   1/2   2/3   1   4/3   5/3   2
```

Six roles sit on it. At default density:

| Relationship | Fraction | On u=24 |
|---|---|---|
| Inside an atom: an icon and its label | 1/6 u | 4 |
| Inside a group that reads as one thing | 1/3 u | 8 |
| A control's own space beneath it | 1/2 u | 12 |
| A list row, top and bottom | 2/3 u | 16 |
| Between blocks and sections | 1 u | 24 |
| Header to first content, turn to turn | 4/3 u | 32 |

**Print and screen differ here, and the difference is principled.** The book puts
whole blank lines between fields, because print holds a baseline grid and text
must land on it. On screen, components are boxes with padding and page-wide
baseline alignment is rarely kept. So: **whole units between blocks, where the
book's rule holds exactly, and fractions of a unit inside a group, where screen
departs from print.** Note that the default table above does exactly this. One
unit between blocks, thirds and halves within.

## 4. Density is an index shift, not a multiplier

Density moves every role along the same ladder by one step. It does not scale the
values, which would produce decimals, and it does not change the unit, which
would break the derivation.

| Role | Dense | Default | Loose |
|---|---|---|---|
| Inside an atom | 1/6 u | 1/6 u | 1/4 u |
| Inside a group | 1/4 u | 1/3 u | 1/2 u |
| Under a control | 1/3 u | 1/2 u | 2/3 u |
| List row | 1/2 u | 2/3 u | 1 u |
| Between blocks | 2/3 u | 1 u | 4/3 u |
| Header to content | 1 u | 4/3 u | 5/3 u |

On `u = 24` that is:

```
dense     4   6   8  12  16  24
default   4   8  12  16  24  32
loose     6  12  16  24  32  40
```

Three densities, **one token scale**. Because the fractions overlap, a system
only needs 4, 6, 8, 12, 16, 24, 32, 40 to express all three. Changing density is a
remapping of roles onto tokens that already exist, not a new set of values.

Which is what makes it a semantic layer. `density: dense` is one declaration, and
every relationship follows.

**What density means.** The book ties it to content volume: denser when text and
data are heavy or statistics must be shown, looser when the content is simple
(p.57, p.62). In interface terms:

- **Dense** is enterprise, admin, data tables, anything where the user's job is
  comparison and the screen is a working surface. Also academic and reference
  setting, where volume is the point.
- **Default** is most product UI.
- **Loose** is marketing, editorial, onboarding, and anything read once rather
  than operated.

Density is a property of the *surface*, not the whole product. A dense data table
can live inside a default app. Set it per surface, and say which surface each
setting covers.

## 5. Align the rest of the ramp to the unit

Müller-Brockmann's sharpest rule, and the one most often missed (p.59): **a whole
number of small-type lines should equal a whole number of body lines.** His
example sets caption type so two of its lines equal one body line, and display
type so one headline line equals two body lines. Everything then lands on the
same grid.

So for each step of the type ramp, choose the line-height such that `N` of its
lines equals `M` body lines, with `N` and `M` small. On `u = 24`: a caption at
line-height 12 gives 2:1, at 16 gives 3:2, at 18 gives 4:3. The first two are
strong, the third is weak but legal. A heading at 36 gives 2:3, at 48 gives 2:1.

Prefer the smallest `N` and `M` you can get away with. A 4:3 relationship is
technically aligned and visually invisible.

## 6. Quantise last

Compute the ideal from the relation, then snap to the nearest token the project
actually has. The relation is the intent; the token scale is the output device.

If the snap moves a value more than a third of a step, the unit is wrong for that
scale. Do not scatter exceptions to cover it. Go back to step 2.

---

## Applying it

To a new system: pick body size, choose leading for a composite unit, pick
density per surface, generate, and write the resulting table into the project
contract with the fractions shown beside the values. The fractions are the part
that transfers; the values are local.

To an existing system: compute `u`, express each existing value as a fraction of
it, and see which ones are not simple fractions. Those are the drift. A value
that turns out to be a clean fraction is not off-system even if it is off the
spacing scale, and a value that is on the spacing scale but not a clean fraction
was never justified.

That second case is the one worth looking for. A caption-height chip is one line,
not a spacing value at all, and auditing it against a spacing scale will always
call it wrong.

**The commonest finding is two values doing one job.** On a real system, 29 gaps
at 4 and 19 at 6 were both the icon-to-label distance inside an atom. Neither was
wrong against the spacing scale, and the spacing audit had no way to see that
they were the same role. Expressed as fractions of the line, one is 1/6 and the
other 1/4, and the question becomes answerable: which role is this, and pick one.

Stop the ladder at 1/6. Below that you are inside a glyph's own optical spacing,
which is the typeface's business, not the system's.
