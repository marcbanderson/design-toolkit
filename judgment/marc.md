# Marc's design judgments

_Last updated: 2026-11-15 (American spelling; Both places timing follows which side leads)_

One file for how Marc decides design, in two parts. Read it before proposing a
layout or a component in any project, and treat it as the starting position. A
project's own contract (`DESIGN_SYSTEM.md`, `DESIGN_CONTRACT.md`, `GUIDELINES.md`,
a design section in its `CLAUDE.md`) wins where it says something different;
record the departure there, not here.

- **Part 1, Rules.** What Marc has ruled, worded for any product, each with an id.
  Each rule says what to do. "Aim for" marks a preference with its allowed
  exception; everything else is a rule. Ids point back to where Marc ruled it, in
  the source project's guidelines file (section 13 for the
  2026-10-22 rulings, the preamble for the 2026-10-21 preferences). Rules here are
  principles; a project's own values (spacing, sizes, timings, tokens) live in
  that project's contract.
- **Part 2, How Marc judges.** Predictive criteria: when you hit a situation, what
  he will want, and why. Every entry is **Stated** (his words) or **Observed** (a
  pattern inferred from repeated choices). Never promote an Observed to a Stated.

Distinct from `~/.claude/ai-design-vision.md`, which exists so he can mine it for
writing. This file exists so work comes back right the first time. When something
belongs in both, put the philosophy there and the executable rule here. Individual
decisions go in `~/.claude/design-decisions.md`, not here.

---

# Part 1: Rules

## Preferences (ruled 2026-10-21)

- **P1. Aim for one filled button per surface.** Allowed: more than one when each marks an empty option side by side and none competes with another.
- **P2. Aim for no dark scrim behind a dialog; the page fades back.** Allowed: a scrim where what sits behind would compete with the decision, such as media playing.
- **P3. Minimize the navigation items that expand; start from the desire that nothing expands.** Allowed: one nested level under a section parent whose children are places people move between often.
- **P4. Aim for no dashed edges; an empty slot is a plain tinted tile with a plus.** Allowed: a drop target may be dashed, because it is where you put something.
- **P5. Aim for fade over travel in the product.** Allowed: marketing sections may rise as they fade. Where the product does travel, it is a short rise as the element fades in. (a creator platform, 2026-10-27)
- **P6. In a conversation, aim for suggestions at the end of the newest answer only.** Allowed: on an empty start, they sit with the input.
- **P7. Aim for buttons that hug their label on desktop and fill the width on a phone.** Allowed: a flow's single narrow column may let its primary fill at any width.
- **P8. Aim for choices as a soft stack of rows.** Allowed: a choice that needs a picture or a paragraph to be understood may be a card with a radio.
- **P9. Aim for no check mark in a pick-one list; the current row sits on the well.** Allowed: a pick-several list shows an empty box, then a fill and a check.

## Product principles

- **A1. Copy follows capability.** A page never advertises what does not run; a cut feature is hidden, not shown disabled.
- **A2. Each fact has one home.** A meaning is carried once; a second encoding (a meter beside a status word, a pill beside a switch) is cut even when it is accessible.
- **A3. Flatten the information architecture**: collect on one page, key detail one layer down.
- **A4. A layout never keeps space for something it no longer draws.**
- **A5. A reference supplies the gesture, never the look.** Borrow how something behaves; the product keeps its own appearance.
- **A6. Design only from data the user has**, and run the screen before drawing its empty state.
- **A7. Prefer a term people already know** over a more precise one the product must teach; plain words with an article.
- **A8. Different surfaces of one product (the app, the marketing site) may fork their controls but share the grammar underneath**; identity (marks, avatars, icons, the brand device) never forks.

## Page structure and flows

- **B1. The fastest path leads.** Several doors can exist; the one that saves the most effort is the visible one.
- **B2. A guided flow shows its whole length, lets steps be skipped, and can always be left** (Finish later; back on every step but the first).
- **B3. A guided flow stays inside the app's shell**: it is a page with the navigation, not a trap.
- **B4. Onboarding exists until anything is added, then it is gone**, by subtraction, and never comes back.
- **B5. A setup checklist retires once filled**; a nearly done one becomes a banner.
- **B6. Never draw a gate the code does not have.** Optional steps read optional; not started is muted, never an error color.
- **B7. Order belongs to the person**: setup steps are not numbered or gated; a dependency is told as a consequence.
- **B8. Order steps by cause, and put the payoff after what makes it feel like theirs.**
- **B9. As state advances, the primary becomes the next act**; skipping is never the loudest control.
- **B10. Alternative routes to one goal write the same state**, so done never depends on the door.
- **B11. A surface never demands setup before it shows the person's content.**
- **B12. A review step is a read-only summary**, never a second editor for the same object: one object, one editor.
- **B13. A transient review is a state, not a standing section.**
- **B14. A link from inside a context opens that context's slice first, then View all.**
- **B15. Hand the person the most specific thing they need now.**
- **B16. Information design uses the width**: content with structure takes a shape (side by side, a table), not a packed narrow column.
- **B17. The default view is where most items live** (a board over a calendar when most items have no date).

## Actions and controls

- **C1. Buttons take a modest corner radius, never a pill**: pills read consumer for a tool people must trust.
- **C2. Buttons in a row sit closer together than the groups around them, on one consistent gap; a text button beside a button with a plate gets one step more room, because its edge is invisible and the plate's is not.** The action first on the left, last on the right. The principal action goes last, at the inline end, in every row of buttons; an in-place confirm is the exception (C5). (a creator platform, 2026-10-27)
- **C3. A secondary button hovers into the primary's resting look.**
- **C4. Header controls take the small button size, and everything on that row matches.** A control filling a slot another vacates is the same size.
- **C5. Confirm only the direction that takes something away.** A confirm on the harmless direction teaches people to click through. An in-place confirm puts its confirming button where the arming press was not, so a double press cannot confirm by accident; this overrides principal-action-last for that one row. (a creator platform, 2026-10-29) Removing something from a row confirms in place by a second press; deleting a whole account or identity confirms in a destructive modal. (a creator platform, 2026-10-27)
- **C6. A state change with consequences beyond the row is a switch with its state word, confirmed by a modal**; a switch replaces a status pill plus a button.
- **C7. A status pill that has a way out is a control and shows it with a chevron.**
- **C8. Opting out is one visible tap at the point of action, never a setting.**
- **C9. Every affordance earns its permanent space.** Rare-but-always-available controls are quiet at rest, take a well on hover, and carry no label.
- **C10. A press on a suggestion sends it.**
- **C11. Never write the user's words or critique for them**: no canned correction chips, no invented turn; prefill the input instead of sending.
- **C12. A copy action confirms with a small "Copied" pill that rises and fades**; the icon does not swap.
- **C13. Close is one X glyph in every overlay, at the standard icon-control hit area, top right**; an open inline row closes with a quiet "Close". Every icon button, Close included, gets the full touch target while its glyph and plate keep their drawn size. (a creator platform, 2026-10-27)
- **C14. A button's label follows state** (Replace once something is uploaded).
- **C15. A disabled control always names what it waits for**; where nothing will ever enable it (including an act the person's role can never do), it is absent. A submit that waits for input is shown disabled with that line, never withheld until the input arrives. (a creator platform, 2026-10-27)
- **C16. Saving is automatic in editors and settings, and reported as a fact where it happened**; a choice saves on change. Exception: a sheet whose choices commit together under one named save holds them until saved, and closing it with unsaved choices asks first. (a creator platform, 2026-10-27)
- **C17. Autonomy scales with stakes**: a critical or high-stakes act asks before it happens (a modal or an in-place confirm) and shows confidence with an easy override; anything else acts, then says so in a toast or a status line.
- **C18. A row inside a raised surface hovers by sinking, not lifting**; it is already as high as it can go. The lifting hover is for rows on the page. (a creator platform, 2026-11-01)
- **C19. A segmented control holds a few options; beyond that it becomes a select or a filter menu.** (a creator platform, 2026-11-01)
- **C20. A pressable chip is a pill; a tag that only states a fact is not; a status tag is a pill.** (a creator platform, 2026-11-01)
- **C21. A selected choice is marked by a filled radio, never a tick.** (a creator platform, 2026-11-01)
- **C22. "+N more" belongs only where space is fixed (a calendar day), never on a profile card.** (a creator platform, 2026-11-01)
- **C23. An optional setup step says "Optional".** (a creator platform, 2026-10-27)
- **C24. A source photo is shaped differently from the avatar it produces**, so the two are never confused. (a creator platform, 2026-11-01)
- **C25. Generated tiles that sit side by side always differ.** (a creator platform, 2026-11-01)
- **C26. The person's own message aligns to the end; every other voice shares the start edge.** (a creator platform, 2026-11-01)
- **A control that toggles a region never moves between its two states.** (a market data product, 2026-11-10)

## Surfaces

- **D1. Sunken goes on a card, the well on the page**; a component that sits on either takes its ground from its host.
- **D2. Empty and loading tiles inside a card take the page surface**, not sunken: they are not inputs.
- **D3. A card never rules its title off with a hairline.**
- **D4. A group without a surface reads as floating**: a header and its contents share one panel.
- **D5. A notice in the content is a plain card with a subtle edge.**
- **D6. The main text input is a card** (card surface, subtle edge, lowest elevation); states inside it move to the well.
- **D7. Aim for a highlighted option marked by a ring, never by a different fill.** Allowed: an exception named case by case.
- **D8. Shadows are soft and tinted with the brand's dark, never a black smudge; a light surface on a tinted ground takes a hairline.**
- **D9. A ring around a stacked element uses its ground's surface.**
- **D10. A sticky header ends in a soft fade, and content at rest starts clear of it.**
- **D11. Media keeps a smaller radius than its chrome**, so it is never cropped wrongly.
- **D12. A motif belongs to its surface**: a motif made for one flow never decorates another.
- **D13. Behind a modal only the content area scales back; the navigation and the page width stay.**
- **D14. The tooltip matches the theme**: light in light mode, dark in dark mode.

## Lists and rows

- **E1. An accordion opens its first row on arrival only where that case is specifically defined**; it is not a default.
- **E2. A capped scrolling list shows a partial last row**, so it reads as scrollable.
- **E3. Browsable strips run past the edge rather than wrapping; a slot grid wraps at the same size.**
- **E4. Row actions end flush with the word they replace**, not at the hover plate's overhang.
- **E5. Rows center on the glyphs, not the line boxes** (fonts with tall ascenders sit high in their boxes).
- **E6. Rows keep the source's density**; a working queue may step denser than the house rhythm.
- **E7. Files, once added, look like files** (a type icon) on the same row spacing.
- **E8. Aim for a library's filter as left-aligned underline tabs above the content**, the line on the rule. Allowed: filters on the right where the layout calls for it.
- **A row in a work list has one shape: the name alone on the left; the update or action plus the date grouped on the right; no stacked second lines.** (a market data product, 2026-11-10)

## Spacing

- **F1. A title and its description sit tight as one unit, except in modals**, where the title is often smaller than the content.
- **F2. A label sits a tight step above its field, owned by one property.**
- **F3. A message and its action are a group apart**, not set tight as one unit.
- **F4. A content column and a side panel sit wider apart than any gap inside either**, so they read as two things.
- **F5. The page title clears the back control** with a smaller gap above it and a larger one under it, the same everywhere.
- **F6. Text beside an avatar is one unit**: a strong name line over a lighter line one size down, a tight gap from the avatar and centred on it.
- **F7. Two controls of different heights in one row center on each other**; one radio group's options are one height.
- **F8. A height that falls out of content hugs; an empty container hugs or hides.**
- **F9. Spacing derives from type: the unit is the body line**, and line heights are whole relations to it.
- **F10. Spacing comes from a fixed ladder derived from the body line, and nothing sits between its steps**; blocks take the steps one looser than tight.
- **F11. A control's height is the token; its padding is what is left over.**

## Type

- **G1. A size is set by role across the product**: all body copy one size, all metadata one size down.
- **G2. The label size is a label face; anything read as a sentence is body size; the smallest sizes never set running text.**
- **G3. Names, headings, labels and buttons take the strong weight; prose and the user's own words take the reading weight, one step lighter.**
- **G4. A distinction is made by structure (a tag, a label, position), never by a weight exception.**
- **G5. Large figures take the lighter weight**, not the heading weight.
- **G6. Phone to desktop, the statement steps up a level and controls step down; nothing is multiplied.**
- **G7. No separate marketing display scale**: marketing uses the product's type levels, and a view keeps to a few sizes. (provisional)
- **G8. A person's name never truncates**; the rest of the line gives way. Inside a fixed-width control it truncates with an ellipsis and the full name stays available. (a creator platform, 2026-11-01)
- **G9. No widows in two-line text**; balance the wrap.
- **G10. A line-count target is met by cutting copy, never by widening the column.**
- **G11. In a meta line a count is strong in the primary text color and its words stay muted.**
- **G12. Names in data tables are the primary text color at the reading weight, underlined on hover and focus, never colored.**
- **G13. The heaviest weight is for display only**: a landing headline, the one question a guided flow asks. Titles inside the product stay one step lighter.
- **G14. A name that is a row in a list takes the body weight of that list, not the heading weight**; heavier names are for names that head something.

## Color

- **H1. Every measurement binds to a token**: color, gap, padding, radius, blur, offset. A value with no token gets one added; binding straight to a raw palette step is a bypass. Named exemptions only (device chrome, content geometry).
- **H2. Components are drawn once and bound to mode-aware tokens**; dark keeps the same energy, it is not a recolouring.
- **H3. A screen counts as done only once checked in light and dark.**
- **H4. Each color has one job, fixed before styling starts.**
- **H5. Decoration carries no meaning and needs no contrast bar, but it reads as variation and is stable per object.**
- **H6. A link in running text is the link color plus an underline; a linked row name is plain, underlined on hover.**
- **H7. Text someone must read to decide is muted, never disabled.**
- **H8. A progression is one hue at stepped values, never the status family; normal is neutral, never a warning.**
- **H9. Two colors that a color-blind reader cannot tell apart are never the only difference between states; an accent color is never body text.**
- **H10. Contrast is measured against the worst ground, not the page.**
- **H11. A color change made for contrast is a design change: raise it, never swap silently.**
- **H12. An exception is scoped by the surface condition, never by a list of screens.**

## Motion

- **I1. Every duration is a motion token, zeroed by the setting or `prefers-reduced-motion`.**
- **I2. Motion is ambient, not fast; it carries the story, with mass, never bounce.** Marketing included; an arrival may use a soft spring that never overshoots. (a creator platform, 2026-10-27)
- **I3. Animation follows the person's act, a view refreshing, or a page loading; nothing else animates.** Travel in the product is short.
- **I4. Everything in an exchange arrives on one clock, in reading order.**
- **I5. Space is reserved inside a block that is arriving, so nothing reflows**; a container opens to full height, then its content fades in.
- **I6. Never fake latency**: no thinking state over a stored or prepared answer; in-flight indicators follow the request, never a timer.
- **I7. Nothing advances on a timer but transitions**; a filled affordance waits for the person, and a carousel never auto-cycles.
- **I8. A hover-revealed action fades in, never slides; a hover lift is slow and smooth.**
- **I9. Every screen has an entrance; nothing jumps.**
- **I10. Loading is a skeleton of the page's own layout with a left-to-right sweep.**
- **I11. If motion exists only to hide a layout change, change the structure instead.**
- **I12. Under reduced motion a live value still updates, and auto-cycling stops.**
- **I13. Motion is its own later pass; silence about it during layout is not a preference.**
- **I14. A change of state moves what persists: an element keeps its identity and travels between its two states (position, size, color); crossfading whole screens is not motion.** Showcase motion also needs a camera that moves with intent. (marcbanderson-site, 2026-10-25: "The elements didn't animate from one position to another")
- **I15. Clicking through never flickers**: one screen in the DOM at a time, no overlapping exit crossfade, and only content that arrives after a screen is up fades in; what is there on arrival appears at once. (a market data product, 2026-11-09)
- **I16. Interpretation of what the user is typing waits until they have finished**: nothing is shown mid-sentence; the product reconciles the whole request first, states the goal, then adds the details. (a market data product, 2026-11-09)
- **I17. What the user has already read never moves because an input below it changed size**; reserve the space for the largest state of a sequence, and re-anchor only when new content arrives. (a market data product, 2026-11-10)
- **I18. A turn reads in order: answer posts, the system responds, then any new structured input opens from the standard composer**; never swap one structured input straight into the next. (a market data product, 2026-11-10)

## States and copy

- **J1. A label claims no more than the record proves**; a sentence that states a fact fires only once the fact is true.
- **J2. One state, one string**, live and reloaded alike.
- **J3. A refusal, a gap and a failure are three states with three wordings; a fault never dresses as a decline.**
- **J4. When processing input fails, keep the input**; nobody enters it twice.
- **J5. A failed load never reads as empty.**
- **J6. Partial output is kept and labeled; actions that need a finished result are withheld.**
- **J7. A no-results state carries no warning glyph.**
- **J8. An off state says how to turn it on.**
- **J9. When a sequence ends, the next step is said as an instruction.**
- **J10. Teaching ends on what the person gets, not what happened.**
- **J11. A reassurance answers only a worry someone could have.**
- **J12. Name things plainly; never a metaphor.**
- **J13. No corny reveal copy, no invented counts, no date on a draft.**
- **J14. No pronoun the system does not store.**
- **J15. Words shown to an author are the author's meaning, not the system's state**; never organize by an internal taxonomy.
- **J16. One act, one word, everywhere.**
- **J17. Times and dates use the reader's locale and language form. When something will happen (more becomes available, an item is removed, a grace period ends) is a date or a clock time, never a countdown** ("Permanently deleted on 28 October", not "7 days"). English writes the month first with an ordinal ("November 3rd"); other languages take their own form. (a creator platform, 2026-11-01)
- **J18. Optional content with nothing to show is absent, not filled.**
- **J19. An absent image is drawn as an absence (a monogram), never a gray box.**

## AI shown honestly

- **K1. An AI disclosure is one sentence, defined once, printed word for word everywhere; a badge is a marker, not the disclosure.**
- **K2. The disclosure comes at an AI persona's first introduction, before anything is asked, and travels to every card.**
- **K28. A platform host never answers the subject matter**; it helps with setup and answers a fixed FAQ, matched by meaning. (a creator platform, 2026-11-01)
- **K29. The logging notice is never personalized; the line that tells a member the creator will see a declined question is a separate sentence and names the creator.** (a creator platform, 2026-11-01)
- **K30. Reading aloud by an AI voice is disclosed the first time it is turned on.** (a creator platform, 2026-11-01)
- **K3. Never spend prose on "I am an AI"**: the disclosure lives with the face.
- **K4. Every voice gets an avatar and a name before it speaks; the speaker row returns only when the speaker changes.**
- **K5. An AI face always carries its AI badge; a plain avatar always means a real person.**
- **K6. A host introduces; a persona's first words are an answer, never a pitch for itself.**
- **K7. One voice hosts and the others speak**; handoffs and upsells are the host's lines.
- **K8. A plain model never wears a persona's identity.**
- **K9. Wherever a user acts, say what the other party will see.**
- **K10. The AI's working steps sit on the background, one line; only what the user keeps earns a container.**
- **K11. AI work in motion collapses to a past-tense line that stays true.**
- **K12. An answer beyond the source material is marked as reasoning, not a stated position.**
- **K13. An inference lives inside the element it is about**, never in a new card, banner or bubble.
- **K14. A figure carries its source and date; which agent fetched it is never prominent.**
- **K15. Generated text stays visibly separate until accepted, then merges unmarked**; a drafted value says it was drafted.
- **K16. AI never overwrites what a person wrote; imports and drafts add.**
- **K17. What represents someone to others is approved by them first**, and shown from storage.
- **K18. What becomes public is shown, and changeable, before it goes public**; a later change says what breaks.
- **K19. A statement about data handling says only what is true of every provider.**
- **K20. A control presented as a setting must be enforced.**
- **K21. Uncertainty is admitted**: a spoken turn shows what was heard; no evidence returns "cannot vouch".
- **K31. When an answer draws on what the product remembers about the user, their past work or their organization, the answer itself says so**, naming each remembered value with its scope, and each can be changed or left out for that answer. Shown only when memory shaped the result; never applied silently. (a market data product, 2026-11-09) Any question that offers to remember something (where it applies, for me, my firm) always includes declining it ("Don't save"), and a declined item is never shown as remembered. (a market data product, 2026-11-10)
- **K32. What an agent does on its own is split by risk and said plainly**: reading and reporting is stated as harmless and needs no setting; anything that changes the user's work or reaches other people is opt-in per action, visible wherever the agent appears, and revocable in one tap from each place it shows, with every self-made change carrying Undo. (a market data product, 2026-11-09)
- **K33. Containers (conversations, projects) are places the user goes into, never inputs to new work; a container never nests inside another. Reuse happens with the things made inside them (artifacts).** (a market data product, 2026-11-09)
- **K34. A conversation turn is a response followed by one to five numbered options**; actions, scope choices, approvals and next steps are all options in one pattern, never buttons, menus or chips scattered through the reply. (a market data product, 2026-11-09)
- **K35. Anything that asks for the user names the action and its object** ("Approve brief and deck"), never a generic "Needs you" or "Action required". (a market data product, 2026-11-10)
- **K36. An agent is named by its activity and makes sense on its own** ("Monitor and report", never a project, topic or persona name). It can be consulted directly or brought into a project; what is specific to a project lives in that project as tasks and outputs, never in the agent. A conversation is the same thing without continuity. (a market data product, 2026-11-10) Its autonomy is set per project, where the work and its consequences live, never on the agent. (a market data product, 2026-11-10)
- **K37. A note given when confirming an agent's work is taken into account and starts the work**; the agent acknowledges it and never asks to confirm again. (a market data product, 2026-11-13)
- **K38. An optional checkpoint in an agent's run is chosen by the user when they confirm, never a silent default.** When they choose it, the line telling them they must come back is its own paragraph, in bold, and the line saying the run will not stop is bold too. (a market data product, 2026-11-13)
- **K39. A human check reviews the full set the agent will work from, not the summary it will produce**, and the user refines it by describing the change, after which the revised set is shown again. (a market data product, 2026-11-13)
- **K22. Progress in building something is shown by the thing filling out, never a percentage.** A meter reads as a count or a fraction, never a percentage. (a creator platform, 2026-11-01)

## Limits and money

- **L1. A usage limit is shown as a share of one allowance, never a cap, dollars, tokens or a split.**
- **L2. A meter shows what is left, labeled as left.**
- **L3. Cost differences are stated as direction, never magnitude.**
- **L4. A cost note appears only where cost is not already visible.**
- **L5. At a hard limit the input is replaced by the explanation, routed to whoever can lift it.**
- **L6. A price is meta, stated beside its control before the click, never the loudest thing on a card**, and never inside a button's label except where that button charges (BL2).

## Conversation

- **M1. An empty conversation is never blank**: a few starters inside the input, more on request, gone once a question is asked.
- **M2. Once asked, the screen is the answer**: suggestions clear, the view stays on the newest line.
- **M3. New activity goes where the reader is looking**: a reply to an earlier turn arrives at the bottom, quoting it.
- **M4. Every voice in a feed starts at the same left edge.**
- **M4c. A conversation has two left edges only**: the composer's (where message icons, the composer, options cards and the Goal Card start) and one message-content indent after the icon (text, cards, lines); user messages align to the composer's right edge. (a market data product, 2026-11-10)
- **M4b. Inside a card, every label and line starts on the title's left edge**; a state highlight may bleed past the text edge, never move it. (a market data product, 2026-11-09)
- **M5. One speaker's consecutive output is one message with hierarchy; finished steps stay as a record without their actions.**
- **M6. A refusal is labeled in words, with no warning color and a way forward. A turn nobody spoke has no avatar; a platform turn (a crisis line) is a card.**
- **M7. An answer reads: speaker, answer, qualifiers, support, onward, housekeeping.**
- **M8. Disagreement is reported with names.**
- **M9. A note or offer shows once, when relevant, then is remembered.**
- **M10. A layout that grows with content does not flip back until the content is cleared.**

## Voice and audio

- **N1. Typing is the floor, dictation the accelerant**; dictation writes into a field that stays editable.
- **N2. Read aloud, dictate and send are three controls, the microphone nearest send.**
- **N3. Read aloud is off by default; a synthetic voice is disclosed the first time it turns on.**
- **N4. A level meter is real, never decorative; the word carries the state.**
- **N5. The system never decides to interrupt; nothing that plays competes with the voice.**

## Mobile

- **O1. A phone carries the full experience; the constraint changes layout, never contents.**
- **O2. One component, two layouts, never two shells; a mobile-only treatment is a bug.**
- **O3. Below the phone breakpoint a settings row stacks**: text full width, the control beneath it, a tight step apart.
- **O4.** See AD11.
- **O5. Below the breakpoint hover insets go, and overflow actions go into a menu.**
- **O6. A page that breaks at phone width is rebuilt to the phone frame, not patched.**
- **O7. Touch targets are larger in navigation than inline, and no inline target falls under the floor; icon-only controls use the standard icon-control sizes.** (See C13: icon buttons all take the full target.)

## Navigation

- **P1. One back control, naming its destination.**
- **P2. A flow keeps one navigation on every page reached from it.**
- **P3. The navigation groups by whitespace; a collapsed navigation drops the nesting, the parent standing in.**
- **P4. The navigation is the product's shape, not the user's progress.**
- **P5. An end user has one account marker, in the top bar.**

## Forms

- **Q1. Add an item through an open field confirmed with Enter, never a dashed button.**
- **Q2. A field's action sits inside the field; the focus ring wraps the whole control.**
- **Q3. Never disable the field that has focus; guard the send.**
- **Q4. Ask only what cannot be derived.**
- **Q5. A control with future consequences states them live under the choice.**
- **Q6. A single-choice step moves on when picked, with no Next button**; the pick shows as chosen for a beat, and only the last step submits. (a market data product, 2026-11-13)
- **Q7. When a request is typed, the agent asks only what the message did not say, then reads back its interpretation** for a yes or a clarification in an open field; it never shows the structured inputs prefilled for re-confirmation, and a clarification revises the read-back and asks again. (a market data product, 2026-11-13)
- **Q8. A search field with text shows a clear control beside the search icon; clearing keeps focus in the field.** Each list or tab has its own search, scoped to it. (a market data product, 2026-11-13)

## Accessibility

- **R1. Every link and action takes the pointer cursor** (in a native desktop window, see DT5).
- **R2. Every button variant, quiet included, has one focus ring at one consistent offset.** The focus ring is the text color in both themes, never the accent. (a creator platform, 2026-11-01)
- **R3.** See KB8.
- **R4. When a small size cannot carry a color signal, words do.**
- **R5. A gesture is never the only way; a glyph keeps one meaning per screen.**
- **R6.** See KB11.
- **R7.** See KB14.

## Charts

- **S1. A chart earns its place from the data the user has**; one category becomes a sentence.
- **S2. Several lines are named at their ends and keyed; a lone point gets a dot; a time series has no wash; a change shows arrow, sign and color, and a flat one says "No change"; empty and loading tiles take the page surface.**
- **S3. A ranked scale uses a convention people know (gold, silver, bronze), with lightness between neighbors.**

## Building (design files and components)

- **T1. A component holds its full state space, or it is only a picture.**
- **T2. Repeated use earns a component; some things are containers.**
- **T3. A component taken from production keeps the job and takes the look from the system.**
- **T4. A new screen extends what passed review; a rebuild that drops a reviewed behavior is a regression.**
- **T5. A proposal is shown drawn, today against the proposal, in both themes, at the frame width; a visual question is never answered with a number.**
- **T6. A build is reviewed at the design frame's width; an overlay pins to its frame.**
- **T7. Design file structure**: auto layout where it encodes a relationship, spacing bound, instance never redraw, scroll set by what the screen is, wrappers carry no fill and do not clip, frames bare in flow-order bands, superseded frames to an archive.
- **T8. An interim that ships short of the design stays open against it.**


## Uncovered areas (ruled 2026-10-22, section 14)

### Notifications and toasts

- **NT1.** Choose the surface by where the outcome belongs. A problem with one field goes on that field. The outcome of a submitted form is a form message. Site or session state is a banner. An event the person caused, whose result is out of view, is a toast. A change visible where they are looking gets nothing.
- **NT2.** Aim for no toast on a save; an automatic save reports where it happened, as a fact (C16). Allowed: a save whose effect lands somewhere off the page.
- **NT3.** A failure is never a toast. It stays in place until it is resolved: a form message, an inline error state, a turn notice, or the item's own row.
- **NT4.** A toast carries at most one action, Undo. The same undo stays available somewhere that does not expire. A toast offers it only for acts that are not confirmed in place (C5): archive, move, a bulk act.
- **NT5.** A toast sits at the bottom center of the content area, clear of the navigation, and above the composer or dock where there is one. On a phone it runs full width inside the page gutter, above the dock.
- **NT6.** One toast at a time; a new one replaces the old, and they never stack.
- **NT7.** A toast leaves on its own after a short time, held while the pointer or focus is on it; one carrying Undo stays until the person's next act on the page.
- **NT8.** A toast is a polite status, announced once. Focus never moves to it, and it carries the one Close X (C13).
- **NT9.** A toast is one past-tense sentence naming the object and the count: "Moved 3 documents to Trash." No "Success", no exclamation mark, no icon in place of words.
- **NT10.** A toast wears the floating-card dress (the card surface, the subtle edge, the floating shadow, the card radius) and no status color.
- **NT11.** Aim for no notification inbox. What waits on a person lives on its object (the row, the gap), and anything that must reach them away from the product goes by email (EM8).
- **NT12.** Aim for no count badges in the navigation. Allowed: one plain number after the label of the navigation item whose page holds decisions waiting on this person, hidden at zero, never a colored dot.
- **NT13.** See C17.

### Permissions and consent

- **PC1.** See C15.
- **PC2.** An act someone could do once something changes (a plan, a seat, an admin's switch) shows with one sentence naming who or what enables it ("Ask your admin to turn this on."), or is replaced by that sentence.
- **PC3.** "Contact your admin" appears only when the person has an admin. Otherwise it reads Contact support, and the copy never mentions an admin they do not have.
- **PC4.** Someone who can view but not edit sees values as text, never as a grayed form.
- **PC5.** A role is a neutral tag in words on the person's row; roles are never color-coded against each other.
- **PC6.** Consent comes before the act it covers, in the same view as the button that agrees to it, as plain sentences of what the act may and may not do.
- **PC7.** The button is the agreement: no "I agree" checkbox where the confirming button can carry the consent.
- **PC8.** Wherever a user's words will reach a named person, the line saying so sits with the control that sends them, never only in Settings.
- **PC9.** Taking consent back is as easy as giving it: one secondary button, where the consent was given and in Settings, confirmed in place, saying what stops. Giving consent is never confirmed (C5).
- **PC10.** A scheduled account deletion is a state on its Settings row: the date it becomes permanent and a Cancel deletion action. It is not only a link in the email.
- **PC11.** See J17.

### Billing and plans

- **BL5.** A gated page shows its head and one sentence on what is behind it and which plan includes it, with one action to see plans, rather than redirecting away. Plans compared side by side are equal height, their actions aligned.
- **BL1.** Money displays in the locale's format with its symbol, in whole units when the amount is whole ("$20 a month") and with cents only when they are not zero. A label never carries the currency code.
- **BL2.** The button that charges says the amount ("Confirm and pay $96"); every other price follows L6.
- **BL3.** Aim for plans compared as columns of one table: price in its own row, the current plan marked by a ring and the words "Current plan", never by a different fill (D7). Allowed: with only two plans, two cards side by side.
- **BL4.** An upgrade is offered only where the user meets what their plan lacks (a gated page, a reached limit), as a secondary or quiet action, once per place and then remembered. It is never a modal on arrival.
- **BL6.** Paid content is marked in words in its meta line ("for subscribers"), never by a lock or a color alone, and the marker hides for a user who already has access.
- **BL7.** Seats read as one figure, "6 of 10 seats in use". A pending invitee is a user row reading "Invited, not yet signed in", and going over capacity is an error naming how many seats are left, shown before sending.
- **BL8.** A failed payment is an attention banner on every page until it is fixed, with "Update payment method". It also shows on the billing row.
- **BL9.** Canceling is one visible press and a destructive modal that says the date access ends. No retention offer or extra step sits between them, and afterwards the row reads "Ends on {date}" with Resume.
- **BL10.** A plan switch that charges shows, in its confirm, the exact amount due today and the recurring amount after it.
- **BL11.** Subscription state is a sentence-case tag (Active, Free trial, Cancellation scheduled, Payment past due), with a dated line under it ("Renews on November 3rd"). Dates in a status line read in the reader's language's own form: an ordinal day in English ("November 3rd") and each other language's own form.
- **BL12.** Aim for invoices and receipts to stay in the payment provider's portal, behind one quiet "Manage billing". Allowed: an in-product invoice table once users ask for one.

### Emails

- **EM1.** One email shell for every email the product sends, in light and dark.
- **EM2.** Emails flip with the mail app: light by default (the primary text color on white), with a dark version the client uses when it is in dark mode, declared with color-scheme.
- **EM3.** The email button is the primary button for the mode the email shows in, at the product's button radius, built as a padded inline-styled link. It is never an accent color.
- **EM4.** One action per email, with its URL repeated as plain text under the button.
- **EM5.** Every email has a plain-text part with the same words in the same order and the URL on its own line.
- **EM7.** Email type requests the product's typeface and falls back to the system stack, never to another named face. Heading, body and footnote follow the product's levels with the footnote muted, spacing stays on the scale, and the layout is one column at a width mail clients render reliably.
- **EM8.** Mail is sent only for three things: what the person asked for (sign-in link, code, reset, verify, export ready); changes to their account or money they must know about while away (invitation, deletion scheduled, trial ending, payment failed, plan changed, access ending); and security. No activity email until a notification contract is ruled.
- **EM9.** Every email ends with one muted line saying why it was sent ("You are getting this because you asked to sign in."). Mail not triggered by an act of the recipient also carries an unsubscribe link and a List-Unsubscribe header; transactional mail carries neither.
- **EM10.** The subject names the thing and the date ("Your trial ends on 3 November"), the heading repeats it, the body is one or two sentences, and any expiry is a date or a duration.

### Languages

- **IN1.** Aim for every button, tab, nav item and chip to hug its label, so the longest language fits on one line with no truncation. Allowed: a fixed-width slot, such as a segmented control or a table column. There, the translation is shortened in that locale; the slot does not widen and the type does not shrink.
- **IN2.** Equal line counts hold in every locale. A line-count limit (G10) is met in the longest locale by editing that locale's copy, never by widening the column or clamping.
- **IN3.** A screen counts as done once seen in the default language, the longest-running language and a non-Latin script, beside the light and dark check (H3).
- **IN5.** A script with tall stacked marks (Devanagari) gets a more generous line height than Latin at the same level, still on the grid. A single-line label keeps the Latin line box.
- **IN6.** The smallest levels never set CJK or Devanagari; in those scripts those roles render at the smallest level that stays legible.
- **IN7.** A role that all caps or italic tells apart also differs by container, label or position. Letter-spacing is zero in CJK and Devanagari.
- **IN8.** Never translated: the product's name, brand and product names, people's and personas' names, the language picker's autonyms, keyboard keys, addresses and code. Brand names enter strings as parameters, never inside a translation.
- **IN9.** Money, dates, times and numbers are formatted by the locale from a value, never typed into a translation.
- **IN12.** Right-to-left is out of scope until an RTL locale is scheduled. Code keeps logical properties (start and end) and nothing is drawn mirrored.

### Desktop apps

- **DT8.** A floating overlay carries its own surface and never trusts the backdrop: a translucent plate with a hairline that follows the mode. It sits in a corner, never takes focus, never covers the field it writes into, and its readouts yield to an open panel.
- **DT2.** Aim for every desktop app to follow the OS appearance in light and dark. Allowed: a surface whose job is judging color in media (an authoring app's viewer and timeline) is dark only.
- **DT3.** The page draws the title bar at the height the OS measures: window buttons at the start, then the app's name and view switcher, the avatar at the end opening Settings, and an empty draggable bar on front-door screens. The brand line sits under it as the line between chrome and content.
- **DT4.** Every action is in the native menu bar with its standard accelerator, and in the command box. Single-letter keys and Space belong to the page and carry no menu accelerator. Undo names the step.
- **DT5.** Inside a native desktop window, buttons and controls keep the arrow cursor, as the OS does. A link that leaves the app shows the hand.
- **DT6.** Each window has a minimum size at which nothing overlaps, set per app; panels scroll inside themselves, the window never scrolls, and a window reopens where it was left.
- **DT7.** An app that keeps running with its window closed shows a monochrome template icon in the menu bar, with Quit in its menu. It never posts a system notification the user did not ask for; finished work waits in the app.
- **DT11.** Status in the desktop apps has a word or a shape, never hue alone. A task that could not start leaves a mark, and "In progress" is not the primary's color.
- **DT12.** Every desktop app ships every locale the product supports, and all of them follow the one language setting the person chose.

### Marketing pages

- **MK1.** Aim for one content width per page, with prose at a reading measure and color grounds running full bleed behind it. Allowed: proof cards may run wider than the content column.
- **MK2.** A section is a lockup, then its content. Heading and body sit tight as one unit, and the lockup sits a full block apart from the content; the hero lockup takes larger steps of the same relationship.
- **MK3.** Fewer sections, no headline-only sections, and below the fold is a tour, not a website. Show rather than tell. Media takes the large radius and the soft tinted shadow (D8).
- **MK4.** The marquee fills at least the first screen. It says what this is at its head and where to go at its foot, and it sits side by side so the conversation has room. When the hero carries the mark, the nav does not.
- **MK5.** See G7.
- **MK7.** One filled primary per section (P1 applies per section). A price sits beside its CTA as meta, not inside the label (L6).
- **MK8.** The eyebrow is one device per page: a round filled pill naming the section's job, uppercase. It is never the same device as a tag or label elsewhere on the page.
- **MK9.** See P5 and I7. A carousel comes to rest against the column's start edge.
- **MK10.** The header holds the wordmark, nav, the language select, theme and one CTA. The footer of any page that collects anything links Privacy and Terms.
- **MK11.** Light is the default; dark follows the device. Both are drawn.

### Legal pages

- **LG1.** Privacy and Terms each have one canonical URL, shared by every app. The other paths redirect to it.
- **LG2.** A legal page is a prose page: a plain page at a reading measure, body at the reading size, section headings and subsections on the product's levels with a clear step between them. No hero, no color ground, no eyebrow.
- **LG3.** Under the title, one level down, sits "Last updated {date}" in the locale's date format (J17), with the version beside it.
- **LG4.** A long document opens with a contents list of in-page links, and every heading can be linked to.
- **LG5.** Legal text shows in its governing language in every locale, with one line in the interface language saying that language governs. The chrome around it is translated.
- **LG6.** A placeholder legal page is never public or linked. "Coming Soon" never ships.
- **LG7.** The agreement is the one modal with no close. Its only exits are the agree primary and a Sign out secondary.
- **LG8.** The agree button stays enabled. Pressing it with something missing names what is missing, under that field.
- **LG9.** The agreement follows the system: the checkbox fills with the primary color, the link is the link color underlined, and labels are sentence case ("I agree", not "I Agree").
- **LG10.** Changed terms open with a short summary of what changed, above the full text, and the gate asks again.
- **LG11.** The version and date someone accepted can be found in Settings.
- **LG12.** A legal link inside a form opens without losing the form.

### Admin and data tables

- **AD1.** A list compared down the page is a table; a list read one item at a time is a list row. Three or more facts that line up from row to row make a table.
- **AD2.** Aim for the whole row as the hit target, with the name as its link to the detail page, styled per G12. Allowed: a record read beside the list opens in a side drawer.
- **AD3.** Every admin list is paged on the server at one fixed page size. The filter bar sits a block apart above it and the pager is start-aligned under it. Filters, sort and page all live in the URL.
- **AD4.** A table opens in a default order, newest first. Only columns with a meaningful order sort. A sortable header is a button with aria-sort. Direction shows by chevron and weight, never color.
- **AD5.** Numbers align to the end of their column in tabular figures, and the header aligns with them. A unit goes in the header ("Spend, USD"), not in every cell.
- **AD6.** Aim for absolute dates in table cells, in the locale's format, in a `<time datetime>`. The exact date and time show on hover and focus. One time zone per page, said once beside the count ("All times in UTC"). Allowed: an activity feed uses relative time ("3 hours ago") for recent items.
- **AD7.** An ID in a table is a copyable line cut to a short prefix. The full ID is its accessible name. It is set in the interface typeface and is never the row's name.
- **AD8.** A status is a tag at the compact size in table rows, in sentence case, in words. Status tones appear only where there is a status; a role or category is neutral.
- **AD9.** Aim for one admin row density, one step denser than the main app: tighter row padding and a smaller value size. Allowed: an admin detail page in the settings register keeps the house rhythm.
- **AD10.** The name column never wraps, and every other cell is one line, truncated. The full text shows on open and on focus. A table wider than its column scrolls inside its own frame, with the name column pinned.
- **AD11.** On a phone a table keeps its key columns (name, status, one figure), and everything else opens inside the row, including the label of any status dot.
- **AD12.** Aim for no row selection; act on one row at a time. Allowed: where an operator routinely acts on many rows:
  - a checkbox column that always stays in the layout;
  - after page select-all, an offer of "Select all {n} matching";
  - a bar naming the count, the action and Clear;
  - a modal confirm that states the count.
- **AD14.** Each table state has one form, and the header row stays in every one of them.
  - An empty table is one start-aligned empty state in the body's place, saying what would fill it.
  - A missing cell reads "None" or "Not set" in the muted text color, never a dash.
  - Loading is skeleton rows in the table's own columns.
  - A failed load says so and never reads as empty (J5).

### Content pipelines and libraries

- **SP1.** The board is the pipeline's default view; month and week are secondary. The board is process and holds every piece. The calendar is a view of dated pieces only.
- **SP4.** A date is never required to make, move or finish a piece. Undated pieces in progress sit in a strip beside the month, and ideas are only counted there. A cadence marks the days its rule names as a ring, where a piece is a dot, and creates no empty slot.
- **SP6.** Every drag has a keyboard path and a menu path (R5).
  - The card is a button: Space picks it up, arrows move it, Space drops it, Escape cancels.
  - Each step is announced politely.
  - The card menu offers "Move to" and "Schedule".
- **SP7.** An idea shows its age, not its capture date ("Captured nine days ago"), at every stage.
- **SP9.** Aim for media as a grid of one tile size.
  - The image is its own edge, and the name and facts sit under it in the elevated card on hover.
  - Duration and size are file metadata at the metadata size.
  - The select checkbox stays in the layout: shown on hover and focus, at rest on touch.
  - Allowed: a list view, by a grid and list toggle at every width.
- **SP10.** A file in progress says its state in words on its tile (Uploading, Processing, Ready, Failed), with a bar while it moves. A failed upload keeps the file and offers Try again.
- **SP11.** Deleting from the library moves the item to Trash and confirms after the fact, in place: "Moved to Trash." with Undo, and no arming. Allowed: an item used in a scheduled or published post arms in place first and names the posts.
- **SP12.** A trashed item says when it goes as a date (J17). Restore is its row action and returns it where it was. Trash has no permanent delete.
- **SP14.** The post editor saves on change and reports it in its head (C16). Status is a menu in the head. Reorder anywhere (lessons, workflow steps) is a drag with SP6's keyboard path, plus Move up and Move down in the row menu.

### Keyboard and screen readers

- **KB1.** Every app's first focusable element is "Skip to content". It shows on focus and lands on the page's h1.
- **KB2.** One h1 per page, the page title. Section titles are h2 and row group heads h3. The level follows the visible hierarchy, never the size wanted.
- **KB3.** Landmarks are fixed per shell:
  - the navigation is a labeled nav;
  - content is main;
  - a filter bar is search or a labeled group;
  - a pager is a labeled nav;
  - a stat or metric card is a labeled section.
- **KB4.** On a route change, focus moves to the new page's h1 and the title is announced.
- **KB5.** Focus has one rule per surface:
  - a plate focuses its first field;
  - a modal traps focus and returns it to its opener;
  - a row opening in place keeps focus on the row;
  - after a delete, focus goes to the next row, or to the section title when the list is empty;
  - a drawer does not trap.
- **KB6.** Escape closes the topmost layer only, and cancels without saving. In a field with a query it clears the query first.
- **KB8.** A hover-revealed action stays in the layout and in the tab order, shows on focus within, and shows at rest on touch.
- **KB9.** A composite control takes one Tab stop, and arrows move inside it:
  - menus;
  - listboxes;
  - segmented controls;
  - tabs;
  - the date grid;
  - a board column. Tabs that switch pages are links with aria-current, not role=tab.
- **KB10.** Aim for no global keyboard shortcuts in the web apps; everything is reachable by Tab. Allowed: a shortcut with a modifier for a frequent act, named in its control's tooltip (Cmd or Ctrl plus Enter to send).
- **KB11.** A change is announced once, politely, when it settles, never every partial. Examples are "48 of 230", "Moved to Ready", "Copied" and "Saved". Assertive is kept for a failure of the act the person asked for.
- **KB12.** Every icon-only control is named by verb and object ("Delete {title}"), and its tooltip shows the same words. A placeholder is never a name. A link to a new tab says so in its name.
- **KB13.** A control disabled for now (C15) stays in the tab order with aria-disabled and describes what it waits for. A control that is unavailable by position leaves the tab order and keeps its name, as a pager's missing direction does.
- **KB14.** Accessibility is a build gate, like tokens:
  - an automated accessibility check runs in the test suite and fails on new violations;
  - a suppressed accessibility warning carries a reason;
  - every target meets the minimum target size (O7).

---

# Part 2: How Marc judges design

### The shape of an entry

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

### How he reads a screen

**Vertical spacing is the first thing he sees.** Before hierarchy, before
color, before copy. If something is wrong and you do not know what, check the
gaps first. *Observed across 17 messages, every project.*

> **Detect** any rendered gap that is not a simple fraction of the body line.
> **Default** snap to the nearest fraction, rounding up on a tie.

**Tight reads as broken, loose reads as unfinished, and a floating label reads
as ruined.** "Squished" is his most common word for a defect, but more space is
not the safe default. On 2026-10-06 a pass that pushed sections to 40 and list
rows to 16, while pulling a section title to 16 from its own content, drew "I
think you have ruined a lot of spacing." What he objects to in both directions
is the same thing: the gaps stop saying what belongs to what. *Stated.*

**His existing spacing is the contract.** A screen he has already laid out is
not raw material for a ladder. Read its values, keep its proportions, and change
only what a stated rule or a measured defect requires. When a pass and his
source disagree, the source wins. *Stated, 2026-10-06, after the pass above was
restored node by node from his file.*

**Spacing rules he has stated, in force:**
- Group, then space apart, at every scale, from screen sections down to an icon
  and its label. *"That goes for big clusters all the way down to small ones."*
- A label is never looser to its own content than sections are to each other.
  In his Q4 source a section title sits 24 from its content and sections are 24
  apart; the title's own padding carries part of that.
- A field or composer and the pills under it are two controls: 16 apart, never
  8. *"the pills under the prompt input are way too close"*, *"the pills are too
  close to the search. Apply that fix everywhere."*
- A list of actions in a sheet is one set: tiles 8 apart, a destructive action
  24 below the set, no dividers. Far-apart rows *"don't really look clickable."*
- List rows keep the source density (8 top and bottom in his Q4 lists). Do not
  raise rows to a floor the source does not use.
- Repeated items line up: card names and descriptions cap at two lines and the
  description keeps a fixed two-line height, so the grade or tag below sits in
  the same place on every card.
- A component change can move things on screens you did not touch. After any
  change that makes a component taller, render the screens that use it and look
  for collisions (*"look at the t-score collision"*).

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

**Component grammar he has set (a mobile app, October 2026), in force:**
- **One function, one look.** Chips are for choosing; read-only values are
  quiet neutral tags; navy only means "selected" while editing. A summary of
  picks in navy chips "feels a little bit crazy".
- **A suggested prompt has one treatment everywhere:** the gray chip with the
  AI sparkle, living with the composer (under it, or above it when it is
  pinned to the bottom). Never a prompt chip inside a content module next to a
  full-size button. Once a conversation has started, follow-ups stay inside
  the answer, never parked above the input.
- **Editing text is a field you tap into,** not an "Edit" button. A repeated
  edit action is a pencil icon button; add is the same button with a plus. A
  one-off AI action with no clear icon (Regenerate) keeps its word, as the
  action on the section title.
- **Stats are tiles with one anatomy:** a value over a one-line caption, equal
  widths, green or red only for market moves. Never a mix of price-with-chip,
  change-as-value and count-with-chip in one row.
- **Repeated items align regardless of content.** Card names cap at two lines
  and the box always holds two lines, so the grade, tag or value below lands
  in the same place on every card or row. Ungraded shows "Raw", never blank.
- **Show the thing you name, in the same shape every time.** Card art is
  card-shaped with a small radius; player avatars are rounded squares; a
  repeatable insight visual is one card-shaped tile (card, player, or headline
  figure), never a custom chart per insight.
- **Empty states stay inside the app:** real header and tab bar, no tab pills
  before there is anything to switch between, one primary action plus a
  "why" link, no chat to distract from the one thing to do.
- **Scrolling pill rows run off the right screen edge;** the screen edge cuts
  the last pill, never the margin.
- **Where an X goes:** in the header corner it closes a screen; beside a
  docked field it only dismisses the keyboard.
- **Link rows that lead to another page** sit 24 off the content above, with a
  rule after them at equal space each side; they never share a form's field
  rhythm.
- **Leaving a flow is always possible.** "Finish Later" in the header, back on
  every step but the first, progress resumes from Home. One bottom button that
  follows state ("Skip" outlined when nothing is picked, "Next" navy when
  something is); where there are two real outcomes the primary sits in the
  bottom slot where Next always was.
- **Copy uses the product's own name, not metaphors.** "The desk" confused him; insider
  jargon is flagged before it ships.

---

### What "livelier", "more approachable" and "fun" mean

For him, at the layout stage, energy comes from the content and from
confidence, never from decoration: he did not reach for gradients, illustration,
more hues or playful copy. Every entry below was earned by a correction on the
A mobile app's Q4 refresh, 2026-10-03. One project so far: treat the Defaults as strong
priors and confirm on the next.

**Silence about a dimension is not a preference.** *"I do consider things like
animation and whatnot, but not when I'm doing initial layout, so don't take my
lack of description of animation to mean that I don't want it."* *Stated,
2026-10-04.* He works in phases: layout, hierarchy and content first, motion
later. Motion is a lever for liveliness he will pull in its own pass (see the
motion-as-pacing entries in `ai-design-vision.md`). Never record "he didn't ask
for X" as "he doesn't want X"; record it as "not yet in scope", and raise motion
when a layout is settled rather than leaving it out of the system.

**The object is the personality.** *"If you're talking about cards, you should
probably have little images of the cards there. That's a way to make these
components interesting and the design interesting."* And: *"actual pictures in
the screens, not just placeholders."* *Stated.*

> **Detect** a card, player or set named in text with no thumbnail or headshot
> in the same row or group; an initials avatar where a real photo exists (the
> project's repo has 63 in `static/headshots`).
> **Default** card art at its own small radius (4), never the UI's large radius;
> player headshot as a rounded square (about 18% of its size), never a circle.
> Never show a near-match card: the wrong parallel is a fabricated fact.

**Movement and magnitude are drawn, not written.** *"Using icons from our library
or little up arrows and down arrows as well to indicate movement is a good way
to make it interesting."* *Stated.* The infographic set that followed (diverging
bars, progress segments, a dot grid) was accepted. *Observed.*

> **Detect** a change, a count against a total, or a comparison of two values
> expressed only as text.
> **Default** library Rise/Fall icon in the direction color (after the number in
> a right-aligned column, leading it in running text); comparison as bars from
> zero; part of a whole as segments; a count against a prior as a dot grid. Only
> from data that exists.

**Confident type, not airy type.** *"The typefaces all seem too thin."* *"The
fewer the sizes the better, can everything be 17?"* *Stated.* Muse-style
Regular and Medium read as weak to him in DM Sans.

> **Detect** running text below 500; more than five sizes on a screen; two sizes
> within 3px of each other.
> **Default** 500 floor, 600 for content, one size per job.

**Approachable means it reads at a glance.** *"I look at these screens and don't
know what information is important."* *"The metadata gets lost as it's the same
color, weight, and size as the description."* A number pulled into its own
column beside its sentence was *"hard to read"*. *Stated.*

> **Detect** an explanation set at the same role as the fact it explains;
> metadata sharing a run or a style with a sentence; secondary and tertiary text
> less than about 15 L* apart; a number separated from its sentence.
> **Default** four levels, each meaning one thing: answer, takeaway, fact,
> context. Metadata on its own line in tertiary, or as structured stats (number
> primary, label tertiary). Two parallel items that each hold a figure and a name
> stack full width rather than splitting into halves.

**Lead with judgment, not inventory.** *"This app is not about managing a
collection, but about being the true resource for building a collection and
understanding where the user should invest."* The hero of an AI product is the
desk's insight with its evidence, not a balance. And the way in stays in reach:
the prompt input *"needs to be fully visible on the phone when the user lands."*
*Stated.* Which insight leads is composition: **Ask, do not assume.**

> **Detect** a screen whose largest element is a total or a list rather than a
> read; an input whose bottom edge sits below the fold or under a floating bar.
> **Default** insight sentence plus the two figures that prove it; measure the
> input against the fold before calling it done.

**One function, one look.** *"I don't like that in dark mode the prompt input is
the same color as the cards on some of the screens. Same look different
function."* *Stated.* Color gets energy by having a job: navy came to mean "ask
the desk", green and red mean market direction and nothing else.

> **Detect** an input or primary action sharing a fill token with a content
> card; a hue doing two jobs on one screen.
> **Default** a dedicated token for the input surface; when two things look
> alike, change the one whose function is rarer.

**Platform chrome is a reference, not a design surface.** *"Tab bar should be
native iOS, so in the designs it's just a reference, no tokens (but my icons)."*
*Stated, 2026-10-06.* System components (tab bar, keyboard, sheets' grabber,
status bar) stay native; only what the app owns inside them, its icons, is
designed. Do not tokenize or restyle native chrome.

**Judge a direction on the real job.** Generic rows got *"more realistic in terms
of content, and the fact that the ui is based on users asking questions"*.
*Stated.* A style direction shown on placeholder content has not been tested.

> **Detect** an exploration built on generic or invented content.
> **Default** build it on the product's core flow with real content from the
> existing frames.

The spacing half of "approachable" is already above and in the rhythm rule:
*"we group and then we space apart from the next group... from big clusters all
the way down to small ones."* Three separate "crammed" corrections in one session
were all the same failure: a frame whose children shared one gap.

### How he decides

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
or more blank lines. The unit is the line, not the millimeter.

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

**Rhythm on a read surface: added context, not a replacement.** The rules
above stand. This records what the portfolio rebuild (marcbanderson-site,
2026-10-23 and 24) showed about rhythm on a surface that is read rather than
operated.

- **System limits are not his spacing.** *"The current spacing was defined by
  system limitations."* (About his Webflow site.) Then the source's proportions
  are evidence, not the contract: keep what reads right, derive the rest from
  the body line. *Stated.*
- **Grouping lives in the structure.** *"You might have to look at the data
  structure of how text is clustered and redo it to achieve the look we want
  while still making sure that we are SEO-friendly."* What reads as one thing
  shares one container and the container owns the gap; headings that group
  content are also the outline a crawler reads. A flat Markdown stream cannot be
  spaced well until it is grouped. *Stated.*
- **Restore text roles before spacing.** On two pages the migration had flattened
  leads, statements and display headings into body and title sizes; spacing them
  as found would have spaced the wrong hierarchy. Compare roles against the
  source render first. *Observed.*
- **The table he accepted on the home page** ("This looks good"), loose density,
  u = the body line: 1/4 u a title to its tags or one line; 2/3 u paragraphs, an
  image to its caption; 4/3 u list items and lead paragraphs; 2 u a heading to its
  content, tiers inside a section; 3 u peers in a grid, text to media; 4.5 u
  between sections. Each step at least 1.5x the one inside it. The values are
  that project's; the ratios are what transfer. *Accepted 2026-10-23.*
- **A reference he points to:** Instrument's editorial article, *"Good rhythm"*
  (instrument.com/latest/building-without-a-brief). Measured 2026-10-24: a
  doubling ladder on 24 (12, 24, 48, 96, 144), the same px at every width, body
  18/28. Worth carrying: media binds forward (144 before a figure, 12 figure to
  caption, 48 after the caption, so the figure opens what follows and there is no
  separate section gap); a subhead has twice the space above it as below (48 over
  24); a quote and its attribution sit 24 apart with 96 around the pair; pairs
  bind 4:1. Against the portfolio table it uses a much smaller section gap
  (1.7 u against 4.5 u), more room before media (5.1 u against 3 u), a looser
  subhead (0.86 u against 1/4 u) and a tighter caption (0.43 u against 2/3 u).
  *Measured; whether to move toward it is his call.*
- **Open: middle rungs on a read surface.** The rule above (no middle rungs in
  the reading flow, observed on two product screens) and the portfolio table he
  accepted (2/3 u between paragraphs, 4/3 u between list items) do not agree.
  They may both be right for their surfaces. Ask before applying either to a new
  read surface. *Observation, not a ruling.*

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

**A borrowed pattern is judged by what it accomplishes here, not by how good it looked there.** Shown a live goal card copied from a drink-ordering demo, every option as chips with the chosen one lit, he asked: *"These pill views are way too complicated. What is this accomplishing?"* The demo's chips worked because its choices were tiny physical sets; his answers were already given, so the alternatives were noise. **When adapting a reference, keep the job it does (here: show what was understood, what is unknown, and let it be corrected) and drop the parts that only made sense in the source domain.** Before proposing a borrowed pattern, say in one line what it accomplishes for this user. *Stated, 2026-11-09.*

**When he hands over a reference frame, the build matches it, not an interpretation of it.** Twice in one session a page was rebuilt "in the spirit of" his pattern (filter chips instead of his tabs, a boxed list instead of his ruled table) and he sent it back: *"It needs to have thicker rows, and they're not boxed in. It's just a rule across. You need to match the Figma frame I gave you."* **Measure the reference (row height, dividers, paddings, type) and reproduce it, in Figma and in code.** *Stated, 2026-11-09.*

### How he wants to work

**Which side leads depends on the project.** *"Whether I work in Figma first or
code first is dependent on the particular project I'm working on. Maybe it's
just something to confirm with me."* On prototypes explored in code he held
Figma until the code settled, then had it documented in one batch. Ask at the
start and record the answer in the contract. *Stated, 2026-11-14.*

**Context first, direction after.** *"I don't want you to make the prototype by
yourself. I will guide you to make it, I just need you to have proper context."*
Do not open with a menu of options. Become informed, then wait. *Stated.*

**Seeing beats describing.** The dominant feedback mode is a screenshot with an
annotation. The loop that matters is intent to something-he-can-look-at. Shorten
that and most of the specification problem disappears. *Observed.*

**He will tell you the rule once and expect it held.** The repeated frustrations
are never new requirements. They are the same rule, unheld. *Observed.*

**When rebuilding something he made, his existing layout is the brief.** Asked to
"take my current website to generate the look and feel" and do "slight cleanup",
a new layout was rejected: *"I wanted you to bring over the layout from my
existing site to use as the basis of this website."* Carry over the structure,
navigation and signature moves (here, the reel front and center, the name across
the page), then improve what is underneath: code, content model, accessibility.
Read "cleanup" as cleanup, not redesign. *Stated* (marcbanderson-site, 2026-10-23).

**Colleague reactions are design input, relayed without ceremony.** "My
colleague doesn't like the gold" is a real constraint, not a suggestion to
evaluate. *Observed.*

**A tool that cannot read a value says so. Nothing defaults silently.** When
the manifest could not find the unit in the contract it fell back to 24 and
said nothing, and the wrong ladder was offered with confidence. *"DESIGN_SYSTEM.md
should state the unit and the ladder in a table the tool can read, so nothing
gets defaulted silently."* The fix was in two places: the contract now has a
shape the tool reads, and the tool reports what it could not read. *Stated,
2026-09-23.*

> **Detect** any value a tool uses that it did not read from the contract or
> the code.
> **Default** show it as inferred, in the interface, and name where it should
> have come from.

**The vocabulary is the layer components consume.** A picker offers the alias,
never the primitive it points at: `--t-s-xl`, not `--fig-spacing-xl`. Both
resolve to 24, but only one is what a component should be bound to. *Stated,
2026-09-23.*

> **Detect** a token list that contains two names for one value.
> **Default** keep the one furthest from the literal, and let the project name
> a layer prefix to force it.

**Feedback on the render stays out of the way.** The hover highlight was a
filled, animated box and he called it *"a little bit crazy"*; a thin dashed
outline that only redraws when the element changes was right. A panel beside
the item is welcome only if it never covers the frame, because every spacing
judgment is about the neighbor, and covering the neighbor removes the
thing being judged. *Observed, 2026-09-23.*

---

### What he counts as done

**Both places.** A fix in code that is not in Figma, or the reverse, is new
drift. When the mirror happens depends on which side leads (see How he wants
to work): the same session, or a batch he schedules. *Stated; timing revised
2026-11-14.*

**Verified against the artifact he is looking at.** Not committed, not pushed,
not merged. The thing on his screen. *Observed across seven weeks and it is the
single most repeated frustration.*

**Gaps named, not discovered.** He would far rather be told "the DELETE path is
unexercised" than find it himself in a screenshot. Naming it costs nothing;
having him find it costs the claim its credibility. *Observed.*

---

### Accessibility and color

**Lightness and value separation, not hue separation.** Marc has a degree of
color vision deficiency. In charts especially, two series must differ in
lightness, not only in hue. This is a requirement. *Stated.*

**Measure the pair, do not eyeball it.** Convert to relative luminance and
report the difference. Under about 10 points is separated by hue alone,
whatever it looks like on your screen. On this project every positive/negative
pair came in under 10, the worst at 2.5, and two of those pairs were defined in
Figma itself, so tokenizing the code faithfully would have propagated the
problem rather than fixed it. **Where a hue-only pair lives upstream, the fix
is upstream.** *Observed 2026-09-21.*

**A color change to satisfy a contrast rule is still a design change.** It
gets asked, not flagged afterwards. Raising a failing pair is right; changing
the swatch without asking is not. *Correction, 2026-09-21.*

---

### Ask, do not assume

These have no detector and never will. Recognizing them is the point.

- **Composition.** What goes on a screen, in what order, and what gets cut.
- **When to break a rule.** He does it deliberately and the result is usually
  right. A system that flags it as a defect will be ignored.
- **Whether a thing is beautiful.** Not a measurement, and pretending otherwise
  is the parity-score mistake in a different costume.
- **Positioning copy.** Answered from what the business needs from the reader,
  not from craft.

---

# Keeping this file

- **A ruled rule goes in Part 1**, worded for any product, with its id and the
  project it came from. When Marc changes a rule, change it there and note the
  date; do not keep both.
- **A criterion revealed by a correction goes in Part 2.** Append when a
  correction reveals a criterion, not when a task completes. The test: **would
  knowing this have changed what I did?** If not, it belongs in the project's
  decision log or nowhere.
- When a Part 2 criterion gets ruled as a rule, move it to Part 1 and leave a
  one-line pointer by its id rather than keeping both texts.
- Merge into an existing entry rather than adding a near-duplicate. This file
  should get sharper, not longer.
- Part 1 holds principles only. Never copy a project's measurements, timings,
  type levels or token names here; state the relationship they encode.
- Update the "Last updated" line. No em dashes.
