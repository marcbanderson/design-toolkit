---
name: design-contract
description: Create or update the DESIGN_CONTRACT.md for a design project. Use at the start of a new project, or when Marc asks what the rules are, what the rhythm ladder is, or where the source of truth lives. Every other design skill reads this file.
---

# Design contract

Every design skill in this toolkit reads one file at the repo root. It holds the
values that change per project. The skills hold the rules, which do not.

**Use the file the project already has.** `DESIGN_SYSTEM.md`, `DESIGN.md`, a
design section in `CLAUDE.md`, whatever it is called. Only create
`DESIGN_CONTRACT.md` when there is genuinely nothing. Two contracts in one repo
is worse than none, because they will disagree and neither will be trusted.

That split is the whole point. A rule that names its own numbers is a house
style. A rule expressed as a relationship survives being moved to a different
scale, which is the test Marc applies: *"is it easily articulated in a prompt,
one that can be applied to a design system with different spacing tokens?"*

## Creating one

Read the project first, then write the file. Do not ask Marc to dictate values
you can read off the codebase and the Figma file yourself. Ask only about the
things that are genuinely a decision: which Figma file and page is canonical,
which direction the mirror runs, and what the deploy surface is.

Template:

```markdown
# Design contract

## Source of truth
- Figma file: <url> (key `<key>`)
- Default page: <name> (`<node id>`)
- Direction: Figma is authored first. Code follows. Never change code without
  the change existing in Figma, and never leave a Figma change unmirrored.

## Where the work runs
- Repo: <path>
- Local: <command, port, and whether it needs a database>
- Deployed: <url>, deploys from <branch> via <service>
- If it cannot run locally, say so here and name the fallback.

## Rhythm ladder
Values are this project's. The ratio is what carries across projects: roughly
3x between "inside a thought" and "between thoughts".
- <n> turn to turn, and header to content
- <n> between blocks and sections
- <n> list rows
- <n> under a control
- <n> inside a group
Rule: group first, then stack. A tight pair is grouped, and the group is what
enters the block stack. Never flatten a pair into the block gap.

## Type
- Ramp: <sizes>
- Weights: <the permitted set>. Anything lighter is retired, not discouraged.

## Tokens
- Figma variables: <collections>
- Code tokens: <file and naming layers>
- Rule: every spacing, radius, color and type value is bound. A literal is a
  defect, not a shortcut.

## Component inventory
| Component | Figma node | Code class |
|---|---|---|

## Copy rules
- No em dashes. Restructure the sentence.
- A value the system does not have says what is missing and what would fill it.
  Never a blank, never a zero, never a dash standing in for a number.
- Put the verdict next to the data, not only in chat.

## Open decisions
Things deliberately unresolved, with the date and who owns them.
```

## Maintaining it

When Marc states a rule, add it here in the same session, in his words where
the phrasing is his. When he corrects a value, change it here rather than only
in the file you were editing, or the next session will not know.

When a rule stops referring to this project's own values, it has graduated:
move it out of the contract and into the skill that enforces it, so every
project gets it.
