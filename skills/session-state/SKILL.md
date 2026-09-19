---
name: session-state
description: Read or write the project's STATUS.md, the file that records where work stands right now. Use at the start of a session to pick up where things left off, when the designer asks where we are or to catch him up, and at the end of a working session or whenever position changes.
---

# Session state

The goal: **restart the session and lose nothing in terms of
context and understanding.**

That fails today because every file in a project records what is *true* and none
records where we *are*. The branch, the open PR, the half-done thing, the next
move, the trap that already cost a round trip. All of it lives only in the
conversation, and the conversation ends.

`STATUS.md` at the repo root is that file.

## The organising principle: rate of change, not topic

This is why it is a separate file rather than a section in the contract.

| Changes | File | Holds |
|---|---|---|
| Never | `~/.claude/CLAUDE.md` | the rules that bind every session |
| Rarely | `~/.claude/design-judgment.md` | how the designer decides |
| Occasionally | the project contract | what is true in this project |
| Every session | `STATUS.md` | where we are right now |

**A fast-changing fact inside a slow-changing document makes the whole document
look stale, and then none of it is trusted.** That is exactly what happened to
the "Open decisions" list in one real contract: it was written once, went out
of date, and stopped being read. Keep the clocks apart.

Corollary: if something in `STATUS.md` stops changing, it has graduated. Move it
into the contract as a rule and delete the line. If something in the contract
starts changing every session, it was never a rule. Move it here.

## Reading it

First action in a session on a project that has one, before any other file.
Then tell the designer, in three lines or fewer:

- Where we are, and anything that changed since it was written (check the branch
  and the PR state yourself; do not trust the file for facts a command can
  confirm)
- What is next
- Anything blocked on him, which leads, because it is the only part he can clear

If the file disagrees with reality, reality wins. Fix the file and say you did.

## Writing it

At the end of a working session, and whenever position changes mid-session. Do
not ask permission; it is a status note and the cost of a wrong line is a line.

Five sections, in this order. Keep the whole file under a screen, because a
status file nobody rewrites is worse than none.

- **Read next.** A short table pointing at the other documents. This is the
  entry point to everything else.
- **Position.** Branch, PR state, what is pushed and what is not, what is
  deployed. Verify with commands rather than memory.
- **In flight.** Anything half-done, with enough detail to resume. "Nothing
  half-edited, tree is clean" is a valid and useful entry.
- **Next.** The actual next actions, ordered. Not aspirations.
- **Traps.** Things that have already cost a round trip. This section only grows
  when something bites, which makes it the most valuable part of the file.

Plus, optionally, **Known broken, not ours to fix yet**, so a pre-existing defect
is never rediscovered as news.

## What does not go here

- Decisions and their reasoning. Those belong in the contract's decision log,
  via the `decision-log` skill. This file says where we are, not what we chose.
- How the designer judges design. That is `~/.claude/design-judgment.md`.
- Anything a command can answer more reliably. Do not write a commit SHA that
  `git log` will tell you. Write the ones that carry meaning, like a stack of
  local commits that need rebasing, and verify them on read.

## The test

Before ending a session, ask: **if the next session read only `STATUS.md` and the
contract, would it know what to do and what not to trust?** If not, the missing
part goes in one of them.
