# How Marc judges design

Last updated: 2026-09-18

A working file, not a diary. Each entry is meant to be **predictive**: when you
hit the situation on the left, this is what he will want, and why. Use it to
pre-empt rather than propose and get corrected.

Distinct from `~/.claude/ai-design-vision.md`, which exists so he can mine it for
writing. This one exists so work comes back right the first time. When something
belongs in both, put the philosophy there and the executable rule here.

Every entry is **Stated** (his words) or **Observed** (a pattern inferred from
repeated choices). Never promote an Observed to a Stated.

## The shape of an entry

A principle in a file does not fire at the moment of decision. This file already
said "tight reads as broken, and he has never once asked for less space", and a
gap still got set to 8 the same day. **A rule that produces a number fires. A
rule that produces a sentiment does not.**

So an entry that can be made executable carries three parts:

- **Rule** in his words.
- **Detect** what violating it looks like, as something you can actually run.
- **Default** the answer when it fires, so no judgment is needed to apply it.

An entry that cannot produce a detector stays prose and is marked **Ask, do not
assume**. That boundary is the honest part: composition, when to break a rule,
and whether a thing is beautiful are his, and a system that claims to have
learned them has started guessing confidently.

The loop this enables, which is how the entries below were earned: he corrects
one case, you extract the rule rather than the fix, you write the detector, the
detector finds the whole class, he confirms on the cheapest second case, you
apply it and verify by measurement. One correction covered twelve screens that
way on 2026-09-18.

---

## How he reads a screen

**Vertical spacing is the first thing he sees.** Before hierarchy, before
colour, before copy. If something is wrong and you do not know what, check the
gaps first. *Observed across 17 messages, every project.*

> **Detect** any rendered gap that is not a simple fraction of the body line.
> **Default** snap to the nearest fraction, rounding up on a tie.

**Tight reads as broken, loose reads as unfinished.** "Squished" is his most
common word for a defect. He has never once asked for less space. *Observed.*

**He notices weight before size.** A wrong font weight gets flagged; a size one
step off often does not. *Observed.*

**A number that looks confident but is wrong is worse than a blank.** A
fabricated 0.0 score, a dash where a word belongs, a zero standing in for an
absent value. *Stated, repeatedly, and the whole missing-data pattern came from
it.*

**In a list, every row is one height and one grammar.** *"all of these rows
should be the same height even if their description is 1 or two lines"*; a
sentence that would wrap clamps to one line and returns in full when the row
opens. And a row that expands in place gets no chevron (*"it's just
expanding"*), but it does get a verb: with only a trash beside it *"it looks
like clicking will delete"*, so a pencil sits beside the trash, both in
reserved slots so nothing shifts on hover. *Stated, 2026-09-17, on the
guardrails list; the same grammar he had already set on the conversation row.*

**The options of one control are one object.** Four choices 24 apart read as
"spaced too far apart"; at the object step they read as a control. A field a
choice needs opens inside the chosen option, not below the control. *Stated,
2026-09-17.*

---

## How he decides

**Craft on principle, positioning on business need, and he does not confuse the
two.** A spacing question gets a rule. A "should this button say Join the beta
or Get in touch" gets reasoned from what the business wants from the visitor.
Do not answer the second kind with a craft argument. *Observed.*

**An aesthetic judgment is not finished until it is portable.** Three times in a
month he moved from "I like this" to "state it as a rule that works on someone
else's scale": the token contract, the rhythm ladder, then his own process. When
he approves something, expect the next question to be "can that be a rule".
Offer the rule before he asks. *Observed, high confidence.*

**He looks for the structural cause, not the numeric fix.** Given a list of
off-scale heights he did not ask which token to snap them to. He asked whether
the height should exist at all: *"if it's a height, it might be a 'hug' in figma
that is defined by top and bottom margins, or content within."* He was right,
and the fix was to delete the value rather than tokenize it. **When you find an
off-system value, check whether the property belongs there before proposing a
token for it.** *Stated, 2026-09-18.*

**Spacing is derived from the type, never chosen beside it.** This is the
deepest rule he holds about systems, and he arrived at it twice: once by eye,
once by argument.

The unit is the line-height of body text, and every vertical distance is a count
of it. Not the font size, the line-height, because what separates two things is
measured in lines of the text it separates. From Muller-Brockmann, whose grid
defines field depth as a number of text lines and the gap between fields as one
or more blank lines. The unit is the line, not the millimetre.

The proof that he already believed it: the ladder he chose by eye over weeks of
corrections, 8 / 12 / 16 / 24 / 32, turns out to be exactly 1/3, 1/2, 2/3, 1 and
4/3 of his 24px body line. Five simple fractions, no remainder. His own "roughly
3x spread" is 1/3 u against 1 u. He had the relation before he had the words for
it, which is why the framework reads to him as a description rather than a
proposal.

Three consequences he will expect you to hold:

- **The type ramp is the primary decision and the spacing scale is derived from
  it.** This inverts how most systems including his own were built. When the two
  disagree, the type wins and the spacing moves.
- **The unit must be composite.** The relations are fractions, so a unit that
  will not divide produces decimals. 24 and 36 satisfy every fraction; 22 and 26
  satisfy three. This turns the leading decision from "pick a nice ratio" into
  "pick the ratio that lands the unit on a divisible number", which is not how
  anyone normally chooses leading.
- **Density is an index shift, not a multiplier.** Scaling the values produces
  decimals and a second token scale. Moving each role one step along the shared
  fraction ladder keeps every value whole and lets one token scale serve dense,
  default and loose. He asked for density as a semantic layer, and this is what
  makes it one: a single declaration from which everything follows.

**Why it matters for execution:** a value that is a clean fraction of the line is
not drift even when it is off the spacing scale, and a value that is on the
spacing scale but not a clean fraction was never justified. Auditing spacing
against a spacing scale cannot see either case. The first time this was run
against his codebase it found 29 gaps at 4 and 19 at 6 doing one job, which no
spacing audit could have flagged because both are legal values.

*Stated and built, 2026-09-18. Executable version in the `rhythm-model` skill.*

The same day he extended it to corners without being prompted: *"why are our
radiuses 6, 10 and 12? Shouldn't we do 8, 12, 16?"* Radii are fractions of the
line too, on the same ladder as the gaps, so a corner and a gap are one system.
Expect any remaining eye-picked scale (elevation steps, icon sizes) to get the
same question. *Stated, 2026-09-18.*

**To bind two things, move the next thing away. Never pull the pair tighter.**
This is the sharpest correction he has given, because he had already stated the
rule and it was still got wrong.

> **Detect** any change that reduces an existing gap in order to create a
> grouping. Compare before and after: if the inner gap shrank, it is wrong even
> when the resulting ratio is right.
> **Default** leave the inner gap and increase the outer one until the ratio is
> 2x or better.

On Wantlist / Insights he said the button read as evenly spaced between the
insight above it and the block below. The fix I made was to pull the button to
1/3 u from its text. The fix he made was to leave the button a full unit from
its text and push the next block to 2 u. Same ratio, opposite direction, and
his never takes space away.

> "Tight reads as broken, loose reads as unfinished. He has never once asked for
> less space."

That line was already in this file when I tightened a gap to create a grouping.
When a relationship needs to read as closer, **increase the distance to
everything else**. *Stated by demonstration, 2026-09-18.*

**A button is an action, not a continuation of the text above it.** It gets a
full unit, never the tight inside-a-group rung.

> **Detect** a vertical auto-layout whose children include a Button and whose
> gap is under 1 u. Run it across every frame, not the one in front of you.
> **Default** 1 u between the content and the button, and at least 2 u from the
> button to whatever follows.
> **Known exception, unresolved:** a submit button under form fields may want
> less, because it completes the field rather than acting on a paragraph. Ask
> before applying the default to a form. At 1/3 u it reads as the last
line of the paragraph; at 1 u it reads as a thing to do. An icon beside its
label is tight. A control that acts on content is not. *Observed from his
manual pass, and the ladder has been corrected.*

**The air belongs to the component, as padding on the component.**

> **Detect** a parent gap that exists only to space one specific child, or the
> same margin retyped at several call sites of one component.
> **Default** move it onto the component as padding and delete it from the
> parents.
 He sets a
Section Head's 12 beneath it as the head's own bottom padding, not as the
parent's gap. The space then travels with the component to every screen instead
of being retyped per layout, and a parent that forgets to set a gap still gets
the right result. *Observed, and it is the executable form of his stated "a
section title owns the space beneath it".*

**In the reading flow he uses no middle rungs.** This is the sharpest spacing
rule he has demonstrated, and it took two passes to see.

On both frames he reworked by hand, Wantlist / Insights and Collection /
Insights, the page's own content stack runs at exactly two distances: **bound**,
at 1/6 u, and **separate**, at 1 u, with 2 u between blocks. There is no 8, no
12 and no 16 anywhere in the reading flow. A label sits 4 above the paragraph it
introduces because they are one object; everything else is a full unit apart.

The middle rungs still exist, but **only inside components**: a Section Head's
own 12 of bottom padding, a stat row's 12 between tiles, a pill row's 8. They
never appear between things the reader is reading.

> **Detect** a page-level vertical stack whose gap is 8, 12 or 16. Distinguish
> it from a component's internal spacing, where those values are correct.
> **Default** 1 u between items in the reading flow, 2 u between blocks, and
> 1/6 u only where a label belongs to the text beneath it.

**Why it works, and worth saying because it is not obvious:** a flat 12 makes
everything equally related, so nothing groups. Using only two distances makes
every relationship unambiguous at a glance. The middle values are what create
the "everything is evenly spaced" reading he objects to.

*Observed across two hand passes, 2026-09-18.*

**Scale moves with content density, the ratio does not.** On a sparse screen he
runs 1 u inside a block and 2 u between. On a dense one, 1/3 u and 1 u. Both are
roughly a 2 to 3x differential. Do not carry a dense screen's numbers onto a
sparse one; carry the ratio and re-pick the scale. *Observed.*

**Retirement over deprecation.** When an option is wrong, he removes it so it
cannot be reached: the eight Medium text styles were deleted, not discouraged.
Offer deletion, not a lint warning. *Observed.*

**A metric is never an answer to a visual question.** Handed a parity score he
asked *"Does everything look exactly like Figma?"* and then fixed the measuring
apparatus rather than the number. *Stated.*

**He will take a concern seriously and then decide.** Push back once, with
evidence, then do what he says. Twice is arguing. *Observed.*

---

## How he wants to work

**Context first, direction after.** *"I don't want you to make the prototype by
yourself. I will guide you to make it, I just need you to have proper context."*
Do not open with a menu of options. Become informed, then wait. *Stated.*

**Seeing beats describing.** The dominant feedback mode is a screenshot with an
annotation. The loop that matters is intent to something-he-can-look-at. Shorten
that and most of the specification problem disappears. *Observed.*

**He will tell you the rule once and expect it held.** The repeated frustrations
are never new requirements. They are the same rule, unheld. *Observed.*

**Colleague reactions are design input, relayed without ceremony.** "My
colleague doesn't like the gold" is a real constraint, not a suggestion to
evaluate. *Observed.*

---

## What he counts as done

**Both places, same session.** A fix in code that is not in Figma is new drift.
*Stated, and it is the standing rule.*

**Verified against the artifact he is looking at.** Not committed, not pushed,
not merged. The thing on his screen. *Observed across seven weeks and it is the
single most repeated frustration.*

**Gaps named, not discovered.** He would far rather be told "the DELETE path is
unexercised" than find it himself in a screenshot. Naming it costs nothing;
having him find it costs the claim its credibility. *Observed.*

---

## Accessibility and colour

**Lightness and value separation, not hue separation.** Marc has a degree of
colour vision deficiency. In charts especially, two series must differ in
lightness, not only in hue. This is a requirement. *Stated.*

**Measure the pair, do not eyeball it.** Convert to relative luminance and
report the difference. Under about 10 points is separated by hue alone,
whatever it looks like on your screen. On this project every positive/negative
pair came in under 10, the worst at 2.5, and two of those pairs were defined in
Figma itself, so tokenising the code faithfully would have propagated the
problem rather than fixed it. **Where a hue-only pair lives upstream, the fix
is upstream.** *Observed 2026-09-21.*

**A colour change to satisfy a contrast rule is still a design change.** It
gets asked, not flagged afterwards. Raising a failing pair is right; changing
the swatch without asking is not. *Correction, 2026-09-21.*

---

## Ask, do not assume

These have no detector and never will. Recognising them is the point.

- **Composition.** What goes on a screen, in what order, and what gets cut.
- **When to break a rule.** He does it deliberately and the result is usually
  right. A system that flags it as a defect will be ignored.
- **Whether a thing is beautiful.** Not a measurement, and pretending otherwise
  is the parity-score mistake in a different costume.
- **Positioning copy.** Answered from what the business needs from the reader,
  not from craft.

---

## Maintenance

Append when a correction reveals a criterion, not when a task completes. The
test for an entry: **would knowing this have changed what I did?** If not, it
belongs in the project's decision log or nowhere.

Merge into an existing entry rather than adding a near-duplicate. This file
should get sharper, not longer.
