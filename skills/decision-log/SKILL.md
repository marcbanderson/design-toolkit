---
name: decision-log
description: Record and read design decisions, open gaps and to-dos for a project, and capture what those decisions reveal about how Marc judges design. Use when a decision gets made or reversed, when Marc asks what is still open or what we decided, at the end of a working session, or when picking up a project after time away.
---

# Decision log

Two layers, because Marc asked for two things: the state of the work, and the
judgment behind it.

| Layer | Lives in | Scope | Answers |
|---|---|---|---|
| **State** | the project's contract file | one repo | What did we decide, what is still open, what is owed |
| **Judgment** | `~/.claude/design-judgment.md` | every project | How Marc decides, so the next proposal is right first time |

Keep them apart. State goes stale and gets closed out. Judgment accumulates and
gets sharper. Mixing them buries the durable thing inside the perishable one.

---

## Layer 1: state, in the project

Extend the contract file's existing decisions section. **Do not create a second
file.** If it only has "Open decisions", widen it to three parts.

```markdown
## Decisions

### Settled
| Date | Decision | Why | What it rejected |
|---|---|---|---|
| 2026-09-18 | Chips carry no fixed height | Figma hugs; the height is line-height plus padding | Adding a chip height token |

### Open
| Raised | Question | Blocked on | Owner |
|---|---|---|---|
| 2026-09-10 | Spotlight at 1, 3, 6, 12+ cards | Marc picking one of four proposals | Marc |

### Owed
| Since | What | Why it is not done |
|---|---|---|
| 2026-09-17 | Exercise the cardRemove DELETE path | Needs a real backend |
```

Three rules that keep it honest:

- **"Why" is mandatory, and it is not a restatement.** "Because it looks better"
  is not a reason. "Because Figma hugs and the pin restated a token" is.
- **Record what a decision rejected.** The alternative not taken is what makes
  the log worth reading in six weeks. It is also what stops the same debate
  reopening.
- **A decision that reversed stays in the table**, with the reversal as its own
  row. Deleting it hides the most instructive thing in the file.

Settled rows are not permanent. When a settled decision has held long enough to
be a rule, move it out of the table and into the contract's rules as a rule,
then delete the row. The log records the change; the contract records the state.

---

### Whose decision is it

A project has more than one decider. The two layers treat that differently, and
getting it wrong corrupts the more valuable one.

**The state layer records every decision that binds the project, whoever made
it, with the name attached.** A colleague's call on a build pipeline belongs in
the log; leaving it out makes the log wrong. Add a "Decided by" column when a
project has more than one decider, and never quietly reattribute.

**The judgment layer takes only Marc's criteria.** It is a model of how *he*
decides, used to pre-empt what he will want. Absorbing someone else's reasoning
into it poisons exactly the thing it exists for: you would start proposing work
shaped by a criterion he does not hold, and the file would confirm it.

Four cases, because the middle two are easy to get wrong:

| What happened | State log | Judgment |
|---|---|---|
| Marc decides | yes, his name | **yes** |
| A colleague decides, Marc is not involved | yes, their name | no |
| Marc relays a colleague's constraint and accepts it | yes, attributed to them, noted that Marc endorsed it | **no**, this is a constraint he accepted, not a criterion he holds |
| Marc overrides a colleague | yes, both positions | **yes**, an override is his criterion in its clearest form |

The third row is the trap. "Base every branch on current main, from Michael"
reads like a rule Marc holds. It is a rule Marc agreed to. If it enters the
judgment layer you will later defend it as though it were his, when he might
drop it the day the constraint does.

The fourth row is the most valuable entry type in the whole file. When he
overrides someone, the reason he gives is a criterion stated under pressure,
which is the least ambiguous form it ever takes.

**When you cannot tell whose it was, ask, or leave it out of the judgment
layer.** A missing entry costs nothing. A wrong one is believed.

---

## Layer 2: judgment, portable

`~/.claude/design-judgment.md` records how Marc decides, so the next proposal
lands right rather than getting corrected.

**The test for an entry: would knowing this have changed what I did?** If the
answer is no, it belongs in the project's log or nowhere. A completed task is
not a judgment. A criterion revealed by a correction is.

Capture from three moments:

1. **He corrected you.** The correction names a criterion you did not have.
   This is the richest source by far.
2. **He chose between options you offered.** What he picked, and more usefully
   what he passed over, is a criterion in action.
3. **He accepted something without comment that he has previously flagged.**
   That is a rule now held, and worth noting as resolved rather than repeating.

Mark every entry **Stated** (his words, quoted) or **Observed** (inferred from
repeated choices). Never promote an Observed to a Stated. If he has said it once
and you have seen it twice, quote the once and note the twice.

Merge into an existing entry rather than adding a near-duplicate.

### Where the philosophy goes instead

`~/.claude/ai-design-vision.md` is for writing: thought pieces, talks,
positioning. A thesis about design systems goes there. An executable rule about
what Marc will want next goes in `design-judgment.md`. When something is both,
put the argument there and the rule here, and do not paste it into both.

---

## Reading the log

When picking up a project after time away, or when Marc asks what is open, read
the state layer and report:

- What moved since the last entry
- What is open and who it is waiting on
- What is owed and why it is still owed

Lead with anything **blocked on Marc**, because that is the only part he can
clear.

## When to write

At the end of a working session, and whenever a decision is made or reversed
mid-session. Do not ask permission for either layer; both are append-only notes
and the cost of a wrong entry is a line to delete.

Mention it in one clause when you have added something substantial to the
judgment layer, because that file shapes how future work is proposed and he
should know what it now believes about him.
