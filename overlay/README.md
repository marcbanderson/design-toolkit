# Overlay

A panel that sits on top of a rendered design. Click an element, see its gap,
padding, margin and text as tokens, change them only to other tokens, and send
the net decisions to the session as a prompt. It never writes source itself.

## In a project

```bash
cd the-project
~/.claude/tools/overlay-server
```

It reads the project's contract through `tokens-manifest`, serves the script,
and prints the include line. Put that line in the dev build only:

```html
<script src="http://localhost:8766/overlay.js"></script>
```

That is the whole integration. The script fetches the contract's ladder and
ramp from the server, the panel header says "session connected", and Export
gains a Send to session button. Each send lands in `.toolkit/inbox/` as a
markdown file; the session applies it, verifies with measure, mirrors to Figma,
records the decisions and moves the file to `.toolkit/applied/`. The server
adds `.toolkit/` to the repo's local git exclude so none of it is committed.

`Alt+Shift+D` hides and shows the panel. `Escape` clears the selection.

## Without the server

The script alone still works: it reads a `window.__designTokens` manifest if
the page sets one, otherwise it infers spacing tokens from custom properties on
`:root` and the ramp from the text styles already on the page, and says so in
the header. Export then offers Copy prompt. For a page you do not control, the
demo's copy button produces a bookmarklet with the script inlined.

## The demo

```bash
cd ~/design-toolkit/overlay && python3 -m http.server 8765
open http://localhost:8765/demo.html
```

The sample screen seeds an off-ladder grid gap, an off-ladder padding, a
button a third of a unit from its text, a middle rung in the reading flow and
a paragraph off the ramp, so every judgment lint fires.

## What it does not do yet

- Map an element to its source rule. The prompt carries the component name, a
  short selector path and the text, and the session does the mapping.
- Know the Figma frame. The prompt asks for the mirror and says not to skip it
  silently.
