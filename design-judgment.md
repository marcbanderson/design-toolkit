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

---

## How he reads a screen

**Vertical spacing is the first thing he sees.** Before hierarchy, before
colour, before copy. If something is wrong and you do not know what, check the
gaps first. *Observed across 17 messages, every project.*

**Tight reads as broken, loose reads as unfinished.** "Squished" is his most
common word for a defect. He has never once asked for less space. *Observed.*

**He notices weight before size.** A wrong font weight gets flagged; a size one
step off often does not. *Observed.*

**A number that looks confident but is wrong is worse than a blank.** A
fabricated 0.0 score, a dash where a word belongs, a zero standing in for an
absent value. *Stated, repeatedly, and the whole missing-data pattern came from
it.*

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

---

## Maintenance

Append when a correction reveals a criterion, not when a task completes. The
test for an entry: **would knowing this have changed what I did?** If not, it
belongs in the project's decision log or nowhere.

Merge into an existing entry rather than adding a near-duplicate. This file
should get sharper, not longer.
