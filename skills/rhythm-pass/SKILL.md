---
name: rhythm-pass
description: Tune spacing, alignment and hierarchy across a project without redesigning it, by grouping what reads as one thing and then spacing groups apart at every scale, and bind every value to a token. Use when the designer asks for a tuning pass, a spacing pass, a rhythm pass, or says things look squished, cramped, tight or loose.
---

# Rhythm pass

This is one real brief, made permanent. He wrote it and pasted it by hand; it
does not need retyping again:

> You are an expert product designer with a strong eye for spacing, rhythm,
> alignment, and visual hierarchy. You are doing a tuning pass on this project.
> This is not a redesign. The layouts, hierarchy, component choices, and overall
> composition are already decided. Your job is to tighten what's loose, loosen
> what's cramped, line up what's off, and make sure every spacing, color, and
> type value is bound to a Figma variable or style and a matching code token.
>
> The order of operations is fixed: read the Figma file, make the corrections in
> Figma, then reflect those exact corrections in the prototype code. Figma is the
> source of truth. Code follows it. Never make a change in code that isn't
> already in Figma, and never leave a Figma change unreflected in code.

**"This is not a redesign" is the binding constraint.** Do not improve the
composition, change a component choice, or restructure a screen. If you think
something needs that, note it and keep tuning.

Run this in a subagent when it spans more than a few screens, and return the
change list rather than the per-node output.

## The ladder is a ratio, not a set of numbers

Read the values from the project contract (see below). What transfers between projects is
the **spread**, roughly 3x between "inside a thought" and "between thoughts".
In one real system that is 8 inside a group against 24 between groups. The
numbers 8/12/16/24/32 are incidental and happen to be the common ones.

The rhythm that reads as rhythm is hierarchical, never uniform: tight inside a
thought, generous between thoughts. A flat gap everywhere is the failure mode,
even when the flat value is on the scale.

## Group first, then stack

This is the rule that does the real work, and it is the one most often missed.

Before applying the block value to a stack, ask of each adjacent pair: does the
second thing *read* the first? A legend reads its chart. A caption reads its
image. A rail reads the section head above it. A sub-line reads the value above
it.

If yes, they are one thing. Group them at the group value, and let the **group**
enter the block stack. Applying the block value between a head and its own
content pushes them apart and destroys the relationship the spacing is supposed
to encode.

Worked example, from the Wantlist screen: the section held Top, Line Chart,
Legend, Stats, Section Head, Carousel at a flat 12. The correct result is not
"set them all to 24". It is: group Chart with Legend at 8, group Section Head
with Carousel at 12, then stack the four resulting blocks at 24.

## Group, then space apart, at every scale

His own words, and the rule that governs the two sections above: **"We group
and then we space apart from the next group. And that goes for big clusters all
the way down to small ones."** (2026-10-03.)

It is recursive. Ask "what reads as one thing" at every level of the tree: the
screen's sections, a module's label against its content, the blocks inside the
content, a chart against its legend, a figure against its caption. Every level
gets the same treatment: tight inside, clearly apart outside.

**The "space apart" half is the one that gets skipped.** Grouping pulls things
together and removing doubled padding takes space out, so a pass that only does
the first half leaves the screen tighter than it found it. That is the failure
he reports as "crammed" or "squished".

**And the opposite failure is real too.** On 2026-10-06 he compared a passed
screen with his untouched source and said: "I think you have ruined a lot of
spacing." The pass had pushed sections to 40 and list rows to 16 while pulling a
section title to 16 from its own content, so nothing read as belonging to its
label. Rules that follow from it:

- **His existing spacing is the baseline, not raw material.** Before changing a
  screen, render the source and keep its proportions unless a Detect check
  fails on it. Match the source's head-to-content and section values rather
  than importing a ladder from another project.
- **A label is never looser to its own content than the gap that separates
  sections is tight.** If head-to-content is 16, sections at 40 make the head
  read as floating; the source had 24 and 24 with the head's own padding.
- **List rows keep the source's density.** Do not raise row padding to a floor
  the source does not use.
- Do not "take the larger step" by default. Take the source's step.

## Detect: measurable, not a sentiment

A rule that produces a sentiment does not fire. Run these on every screen you
touch, before and after, and do not call the pass done with an unexplained
violation.

1. **Flat stack.** A vertical frame with 4 or more children of different kinds
   (not a list of repeated rows) and no auto-layout group among them. That is
   a flat gap across unrelated things.
2. **Weak spread.** At every nesting level, the gap between groups must be at
   least **1.5x** the gap inside them, target 2x to 3x. A 12 stack holding 8
   groups fails. (A ladder like 8/16/24/40 cannot give 2x at every step: 24 in
   40 is 1.67x and passes.)
3. **Under the floor.** A row with less than the contract's row padding (16
   unless the contract says otherwise), a block gap inside a module below 24,
   a section gap below the contract's section value.
4. **Doubled space.** A bottom padding that adds to the parent's gap, or a
   control's own space stacked on a section gap. Remove one, then re-check 2
   and 3 so the removal did not leave the stack tight.

5. **Two thoughts in one section.** A section that holds two headlines, or two
   separate calls to action, is two sections squeezed together. Split it and
   stack the halves at the section step. (Collection / Insights held the market
   read and "Your top three cards are still the book" at 24; they read as one
   run-on block until split to 40.)
6. **Label too close to what it labels.** A label, kicker or question over a
   block (chips, cards, stats, rows) sits at the head step (16), not 8. Only a
   field label over its single input stays at 8.
7. **Questions stacked as if they were fields.** Separate questions in a form
   or profile (Bio, Category, Athletes, Card Types) are sections: they stack at
   the section step, not the block step.
8. **An action floating off what it acts on.** A button or pill row that acts
   on the block above it groups with that block at 16; a 24 gap makes it read as
   a new block.
9. **A fixed-height empty container.** An empty chip area or list that keeps a
   fixed height leaves a hole that reads as broken. It hugs, or hides when empty.

Checks 5 to 9 are judgment on top of the script: render the screen and look
for them. They are the ones the designer reports as "still too compact" after
every number is on the ladder.

10. **Pills crowding a field.** A search or text field, or a prompt composer,
    and the pill row under it (sort, scope, picked chips, suggested prompts)
    are two controls, not one: 16 between them, never 8. Grouping them at the
    "inside a group" value is the mistake; they are related controls, not one
    thought. (Stated, 2026-10-06, on Player Detail / Catalog: "the pills are
    too close to the search. Apply that fix everywhere.")

Two placements that are easy to get wrong:

- **A tab row controls the content under it.** Group tabs with their content
  (tabs, then the content at the module step, 24 in the 8/16/24/40 ladder),
  and let that group enter the screen stack. A tab row 40 off its own content
  reads as a separate section.
- **A divider is part of the gap, not an addition to it.** Where a line
  separates sections, use the module step on each side (24 + line + 24), not
  the section step (40 + line + 40 reads as a hole).

The check, for a `use_figma` call (pass the screen frame as `root`). It does
not descend into instances (component internals and native chrome are not the
screen's spacing), skips the screen shell (header, body, bars stacked at 0),
and accepts a 0 gap where every child owns its own space (padding of 16 or
more, or a Section Head that owns the space beneath it):

```js
const issues=[]; const al=n=>n.type==='FRAME'&&n.layoutMode==='VERTICAL';
const walk=(n,acc=[])=>{ if(al(n)) acc.push(n); if('children' in n && n.type!=='INSTANCE') for(const c of n.children) walk(c,acc); return acc; };
const owns=k=>/Divider/.test(k.name)||(('paddingTop' in k)&&(k.paddingTop>=16||k.paddingBottom>=16))||/Section Head|Row|Item/.test(k.name); // dividers are neutral
for (const f of walk(root)) { const kids=f.children.filter(c=>c.visible!==false&&c.layoutPositioning!=='ABSOLUTE');
  if (kids.some(k=>/Page Header|Tab Bar|Action Bar/.test(k.name)) && kids.some(k=>k.name==='Body')) continue; // screen shell
  const names=new Set(kids.map(k=>k.name.replace(/\s*\d+$/,'')));
  if (kids.length>=4 && names.size>=3 && !kids.some(k=>al(k)&&k.children.length>=2)) issues.push(`flat: ${f.name} gap ${f.itemSpacing}`);
  if (f.itemSpacing===0 && kids.length>1 && !(kids.slice(0,-1).every(owns)||kids.slice(1).every(owns))) issues.push(`zero gap without owned space: ${f.name}`);
  const controlGroup = kids.length===2 && /Pill Row|Tabs|Search|Segment|Section Head/.test(kids[0].name); // a control and the content it controls
  if (!controlGroup) for (const k of kids) if (al(k) && k.children.length>=2 && k.itemSpacing>0 && f.itemSpacing>0 && f.itemSpacing < 1.5*k.itemSpacing) issues.push(`spread: ${f.name} ${f.itemSpacing} vs ${k.name} ${k.itemSpacing}`);
  if (/Row/.test(f.name) && f.paddingTop>0 && f.paddingTop<16) issues.push(`row floor: ${f.name} ${f.paddingTop}`); }
return issues;
```

More checks, from his corrections on 2026-10-06:

11. **Label floats.** For every section title (or kicker, or field label) that
    heads content, measure title-bottom to content-top and compare it with the
    gap between that section and the next. If the label's gap is the smaller of
    the two by less than half, fine; if sections are more than about 1.5x the
    label gap *and* the label gap is below the source's value, the label reads as
    floating. Restore the source's label gap before touching section gaps.
12. **Rows loosened.** Any list row whose vertical padding is larger than the
    source's for that list. Rows are density, not air.
13. **Actions that do not read as a set.** Sheet or menu actions separated by
    more than the group step, or by dividers, read as unrelated and unclickable.
    Group at 8, destructive 24 below.
14. **Collision after a component change.** After editing a component that
    changes its height, render each parent row that holds it and compare
    `node.height` with the tallest child. A parent that kept its old height
    (stale auto-layout or a clipping frame) hides or overlaps content. Fix by
    re-hugging; turn off clipping on rows that do not need it.

## Process: the source is the baseline

These are the process failures behind the 2026-10-06 regression. They are rules.

1. **Render the source first.** Before any pass on a screen he has laid out,
   screenshot it and read its gaps. If an untouched original exists (a
   duplicated file keeps node IDs), compare against it per node.
2. **Never hand an agent a ladder.** Twice, agents given a number ladder applied
   it uniformly: once too tight, once too loose. Give them the source values,
   the spread rule and the Detect checks, and have them report deviations from
   the source, not conformance to a ladder.
3. **No new wrapper frames to fake grouping.** Group with the containers the
   design already has. A pass that adds "Tab content", "Content", "Head group"
   wrappers changes structure the designer did not draw, and every later
   restore has to dissolve them.
4. **Judge on a side-by-side render at matched width** (source next to result),
   not on a property list. The final report names which screens were looked at
   and which were checked by property only.
5. **Restore beats re-tune.** If he says spacing was ruined and the source
   exists, restore it node by node and keep only the changes he asked for by
   name; do not try to tune toward it by eye.

## The air belongs to the component

the designer's fix for tight spacing is structural, not visual. A section title owns the
space beneath it. A row owns its 16 above and below. Do not solve a gap by
typing a margin onto one instance; solve it in the component, so every instance
inherits it and the next screen is right before anyone looks at it.

And the amount is always a token, never a number typed on a screen.

## Order of work

1. Read the contract and the Figma page.
2. **Figma first.** Fix the spacing on the components, then on the screens that
   use them. Fix the component before the instance, every time.
3. **Then code.** Mirror the exact same values. Same session, not later.
4. Report what changed, in both places, as a list of what and where.

## Checks before you call it done

- Every value you touched resolves to a variable in Figma and a token in code.
- No literal was introduced. A literal is a defect, not a shortcut.
- No composition changed. If you think one should, it is a note, not an edit.
- The Detect checks report zero violations, or each remaining one is listed
  with the reason it stays.
- Every deviation from his source is listed with the rule or the measured
  defect that required it. A change list that only tightens skipped the "space
  apart" half; one that loosens labels, sections and rows together imported a
  ladder. Both are failures.
- Source and result were rendered side by side at matched width, and the report
  says which screens were looked at.
- Both places agree. A Figma fix left unmirrored is the drift this skill exists
  to remove.

---

## Finding the contract

Every project keeps its rules in one file at the repo root. **Do not assume a
filename.** Look, in order, for: `DESIGN_SYSTEM.md`, `DESIGN_CONTRACT.md`,
`DESIGN.md`, a design section in `CLAUDE.md` or `AGENTS.md`, or a `docs/`
equivalent. Pick the one that names the source of truth and the spacing rules.
Use what is there rather than creating a second file beside it, which would give
the project two contracts that can disagree.

If nothing exists, load the `design-contract` skill and write one.
