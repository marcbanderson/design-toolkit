---
name: rhythm-pass
description: Tighten spacing, alignment and hierarchy across a project without redesigning it, and bind every value to a token. Use when the designer asks for a tuning pass, a spacing pass, a rhythm pass, or says things look squished, cramped, tight or loose.
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
