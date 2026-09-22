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
ramp from the server and the panel header says "connected". Each change you
make then lands one of three ways, and the Changes list says which:

| Tier | When | What happens |
| --- | --- | --- |
| 1 | The winning declaration is in a stylesheet the server can find on disk | `Apply to source` rewrites that line to the token binding (or adds a longhand after a shorthand), reloads the sheet, drops the preview override and checks the rendered value against the target. Guard runs on the file. A backup goes to `.toolkit/backup/`. No model involved. |
| 2 | Same, but the rule is shared by other elements | One question, `Apply to all N`, then tier 1. |
| 3 | Inline style, cross-origin sheet, CSS-in-JS, text styles, or the rule cannot be found | The change goes into the prompt for the session. |

Export writes the prompt: what was applied (for the Figma mirror and the
decision log), what is still to apply, and the decisions all of it codifies.
Send to session lands it in `.toolkit/inbox/` as a markdown file; the session
applies what is left, verifies with measure, mirrors to Figma, records the
decisions and moves the file to `.toolkit/applied/`. The server adds
`.toolkit/` to the repo's local git exclude so none of it is committed.

Plain CSS and custom properties are nearly all tier 1. Utility classes such as
Tailwind and CSS-in-JS are tier 3 today; the class-swap path is the next thing
to build.

Each property is a field: label on the left, value on the right. Drag across
the label to step through the ladder; click the value for the list. Only
tokens are offered, and an off-ladder value is marked until it is changed.

`Alt+Shift+D` hides and shows the panel. `Escape` closes a list, then clears
the selection.

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

- Swap utility classes or edit CSS-in-JS. Those changes go to the session with
  the component name, a short selector path and the text.
- Know the Figma frame. The prompt asks for the mirror and says not to skip it
  silently.
