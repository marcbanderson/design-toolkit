# Design contract

The rules of this project. Slow-changing. What is **true** here.

Where the work stands right now lives in `STATUS.md`, deliberately separate,
because it changes every session and a fast-changing fact inside a slow-changing
document makes the whole document look stale.

**If this repo already has a file like this under another name, use that one.**
Two contracts in one repo is worse than none.

---

## Source of truth

- Figma file: `<url>` (key `<key>`)
- Default page: `<name>` (`<node id>`)
- Direction: Figma is authored first. Code follows. Never change code without
  the change existing in Figma, and never leave a Figma change unmirrored.

## Where the work runs

- Repo: `<path>` / `<remote>`
- Local: `<command, port, and whether it needs a database>`
- Deployed: `<url>`, from `<branch>` via `<service>`
- If it cannot run locally, say so here and name the fallback.
- Note any lookalike surface that is **not** this project. A neighbouring
  checkout serving the same-looking app on a nearby port will pass a check
  falsely, and someone will hit it.

## Rhythm ladder

Values are this project's. The ratio is what carries across projects: roughly
3x between "inside a thought" and "between thoughts".

| Relationship | Token | Value |
| --- | --- | --- |
| Turn to turn, header to content | | |
| Between blocks and sections | | |
| List rows | | |
| Under a control | | |
| Inside a group | | |

**Group first, then stack.** Decide what reads as one thing, set it tight, and
let the group enter the block stack. Never run a flat gap across unrelated
blocks.

## Type

- Ramp: `<sizes>`
- Weights: `<the permitted set>`. Anything lighter is retired, not discouraged.

## Tokens

- Figma variables: `<collections>`
- Code tokens: `<file, and the naming layers>`
- Dialect, so the audit does not rediscover it: `<what a bound value looks like
  here, and what is legitimately exempt>`
- Rule: every spacing, radius, colour and type value is bound. A literal is a
  defect, not a shortcut.

## Component inventory

| Component | Figma node | Code class |
| --- | --- | --- |

## Copy rules

- No em dashes. Restructure the sentence.
- A value the system does not have says what is missing and what would fill it.
  Never a blank, never a zero, never a dash standing in for a number.
- Put the verdict next to the data, not only in chat.

## Decisions

### Settled

| Date | Decision | Why | What it rejected |
| --- | --- | --- | --- |

### Open

| Raised | Question | Blocked on | Owner |
| --- | --- | --- | --- |

### Owed

| Since | What | Why it is not done |
| --- | --- | --- |
