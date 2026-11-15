#!/usr/bin/env python3
"""Build the toolkit web view: docs/index.html, one self-contained page, and refresh docs/demo/overlay.js.

  python3 docs/build.py              rebuild from summary.json and the repo files
  python3 docs/build.py --vision     also include the vision record section, which
                                     quotes ~/.claude/ai-design-vision.md and is
                                     left out of the committed page by default

summary.json holds the per-skill, agent and tool summaries and the vision
themes; edit it when a skill changes, or regenerate it with a session.
"""
import json, os, re, sys, html, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRATCH = HERE
WITH_VISION = "--vision" in sys.argv
S = json.load(open(os.path.join(HERE, "summary.json")))
e = html.escape

def raw(rel):
    p = os.path.join(ROOT, rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True).stdout.strip()

def word(n):
    w = "zero one two three four five six seven eight nine ten eleven twelve".split()
    return w[n] if n < len(w) else str(n)

last_commit = git("log", "-1", "--format=%h  %s")
last_date = git("log", "-1", "--format=%ad", "--date=format:%Y-%m-%d")
n_commits = git("rev-list", "--count", "HEAD")

SKILL_ORDER = ["design-contract","session-state","decision-log","taste-extract","rhythm-model","token-audit","design-parity","rhythm-pass","ship-check"]
skills = sorted(S["skills"], key=lambda s: SKILL_ORDER.index(s["name"]) if s["name"] in SKILL_ORDER else 99)

def chips(items):
    if not items: return ""
    return '<ul class="chips">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"

def kv(pairs):
    out = '<dl class="kv">'
    for k, v in pairs:
        if not v: continue
        out += f"<div><dt>{e(k)}</dt><dd>{v}</dd></div>"
    return out + "</dl>"

def details(label, text, lang=""):
    if not text: return ""
    return (f'<details class="src"><summary>{e(label)}<span class="len">{len(text.splitlines())} lines</span></summary>'
            f'<pre><code>{e(text)}</code></pre></details>')

# ---------- Skills ----------
skills_html = ""
for s in skills:
    name = s["name"]
    skills_html += f'''
<article class="entry" id="skill-{e(name)}">
  <header class="entry-head">
    <h3><span class="slash">/</span>{e(name)}</h3>
    <p class="tagline">{e(s.get("tagline",""))}</p>
  </header>
  <p class="does">{e(s.get("does",""))}</p>
  {kv([("When", e(s.get("when",""))), ("Produces", e(s.get("produces",""))), ("Holds", f'<q>{e(s["rule"])}</q>' if s.get("rule") else "")])}
  {('<p class="calls"><span class="lbl">Calls</span>' + chips(s.get("calls", [])) + '</p>') if s.get("calls") else ""}
  {details(f"Read skills/{name}/SKILL.md", raw(f"skills/{name}/SKILL.md"))}
</article>'''

# ---------- Agents ----------
agents_html = ""
for a in S["agents"]:
    name = a["name"]
    agents_html += f'''
<article class="entry" id="agent-{e(name)}">
  <header class="entry-head">
    <h3>{e(name)}<span class="badge">agent</span></h3>
    <p class="tagline">{e(a.get("tagline",""))}</p>
  </header>
  <p class="does">{e(a.get("does",""))}</p>
  {kv([("Runs", f'<a href="#skill-{e(a.get("runs",""))}">/{e(a.get("runs",""))}</a>' if a.get("runs") else ""), ("Why an agent", e(a.get("why",""))), ("Model", e(a.get("model",""))), ("Has", chips(a.get("tools", [])))])}
  {details(f"Read agents/{name}.md", raw(f"agents/{name}.md"))}
</article>'''

# ---------- Tools ----------
tools_html = ""
for t in S["tools"]:
    name = t["name"]
    usage = "\n".join(t.get("usage", []))
    checks = "".join(f"<li>{e(c)}</li>" for c in t.get("checks", []))
    tools_html += f'''
<article class="entry" id="tool-{e(name)}">
  <header class="entry-head">
    <h3>{e(name)}<span class="badge">executable</span></h3>
    <p class="tagline">{e(t.get("tagline",""))}</p>
  </header>
  <p class="does">{e(t.get("does",""))}</p>
  <pre class="usage"><code>{e(usage)}</code></pre>
  {kv([("Exists because", e(t.get("because",""))), ("Reports" if name=="measure" else "Checks", f"<ul class='plain'>{checks}</ul>" if checks else "")])}
  {details(f"Read tools/{name}", raw(f"tools/{name}"))}
</article>'''

# ---------- Templates + enforcement ----------
templates_html = ""
for t in S.get("templates", []):
    fname = t["name"] if t["name"].endswith(".md") else t["name"]
    rel = f"templates/{fname}" if os.path.exists(os.path.join(ROOT, "templates", fname)) else ""
    templates_html += f'''
<article class="entry compact">
  <header class="entry-head"><h3>{e(t["name"])}<span class="badge">template</span></h3></header>
  <p class="does">{e(t.get("does",""))}</p>
  {details(f"Read {rel}", raw(rel)) if rel else ""}
</article>'''

enforcement_html = "".join(f"<li>{e(r)}</li>" for r in S.get("enforcement", []))

# ---------- Vision ----------
V = S.get("vision", {})
themes_html = ""
for th in V.get("themes", []):
    q = f'<blockquote>{e(th["quote"])}</blockquote>' if th.get("quote") else ""
    themes_html += f'''<li><h4>{e(th["title"])}</h4><p>{e(th.get("thesis",""))}</p>{q}</li>'''
threads_html = "".join(f"<li>{e(t)}</li>" for t in V.get("open_threads", []))

J_TEXT = raw("judgment/marc.md")
_m = re.search(r"Last updated: ([0-9-]+)", J_TEXT)
J_UPDATED = _m.group(1) if _m else "unknown"
_p1 = J_TEXT.split("# Part 2")[0]
n_rules = len(re.findall(r"^- \*\*[A-Z]{1,2}[0-9]+[a-z]?\.", _p1, re.M))

# ---------- Judgment blurb (written in the main thread, from judgment/marc.md) ----------
judgment_html = '''
<p class="lede">The toolkit keeps one personal file, and this is what it says. It has two parts. <b>Part 1</b> holds the __N__ rules he has ruled, worded so they apply to any product. <b>Part 2</b> holds how he judges: predictive criteria, each marked <b>Stated</b> (his words) or <b>Observed</b> (a pattern inferred from repeated choices), and an Observed entry is never promoted to Stated. The point is that work comes back right the first time.</p>

<h3>The rules</h3>
<p>Part 1 covers actions and controls, surfaces, lists, spacing, type, color, motion, states and copy, conversation, forms, charts, navigation, accessibility and how design files are built. A few show its character. <b>Each fact has one home</b>: a second encoding of the same meaning is cut, even when it is accessible. <b>Copy follows capability</b>: a page never advertises what does not run. <b>Aim for one filled button per surface.</b> <b>A guided flow shows its whole length and can always be left.</b></p>
<p>A large share is about AI shown honestly. An inference lives inside the element it is about, never in a new card. AI never overwrites what a person wrote. What an agent does on its own is split by risk: reading and reporting needs no setting, while anything that changes the user's work or reaches other people is opt-in and can be undone. The newest rules come from agent workflows: a single-choice step moves on when picked; a typed request gets the agent's reading of it back rather than a form to re-confirm; a note given at confirmation starts the work instead of asking again; and a human check reviews the full set the agent works from, not the summary it will produce.</p>

<h3>How he reads a screen</h3>
<p><b>Vertical spacing is the first thing he sees,</b> before hierarchy, color or copy. Tight reads as broken and loose reads as unfinished, but more space is not a safe default: a pass that pushed everything apart drew <q>I think you have ruined a lot of spacing.</q> What he objects to in both directions is the same thing, gaps that stop saying what belongs together. A screen he has already laid out is the contract; change only what a rule or a measured defect requires.</p>
<p>He notices weight before size. A number that looks confident but is wrong is worse than a blank. And <b>one function, one look</b>: <q>Same look different function</q> is a defect, so a color earns its energy by having a single job.</p>

<h3>Where spacing comes from</h3>
<p><b>Spacing is derived from the type, never chosen beside it.</b> The unit is the body line height, and every vertical distance is a fraction of it. The ladder he picked by eye over weeks, 8, 12, 16, 24 and 32, turned out to be exact fractions of his 24px line, so the type ramp is the primary decision and the spacing follows. To bind two things, move the next thing away; never pull the pair tighter. In a product's reading flow he uses two distances and no middle rungs, which leave everything looking evenly related. Whether that holds on a long read surface is still open, and marked as a question rather than a rule.</p>

<h3>What “livelier” means</h3>
<p>Energy comes from content and confidence, never decoration. <b>The object is the personality</b>: show the thing you name, as a real image. Movement and magnitude are drawn with arrows, bars and segments, not written. Type is confident rather than airy, with as few sizes as possible. And silence about a dimension is not a preference: <q>don't take my lack of description of animation to mean that I don't want it.</q></p>

<h3>How he decides</h3>
<p>Craft questions get a principle; positioning questions get reasoned from what the business needs, and he does not confuse the two. <b>An aesthetic judgment is not finished until it is portable</b>, so when he approves something, the rule is offered before he asks. He looks for the structural cause rather than the numeric fix, and often the fix is deleting a value rather than tokenizing it. A borrowed pattern is judged by what it accomplishes here: <q>What is this accomplishing?</q> When he hands over a reference frame, the build matches it rather than interpreting it. Push back once, with evidence, then do what he says.</p>

<h3>How he works, and what counts as done</h3>
<p>Context first, direction after: become informed, then wait. Seeing beats describing. He states a rule once and expects it held; the repeated frustrations are never new requirements, they are the same rule unheld. Whether Figma or code leads depends on the project, so it is asked at the start. <b>Done means verified against the thing on his screen,</b> not committed or pushed, with every gap named before he finds it.</p>

<h3>Color</h3>
<p>Marc has a degree of color vision deficiency. Two series must differ in lightness, not only hue, and the pair is measured rather than eyeballed. A color change made to pass a contrast rule is still a design change, so it gets asked, not flagged afterward.</p>

<h3>Ask, do not assume</h3>
<p>Some judgments have no detector and never will: composition, when to break a rule, whether a thing is beautiful, and positioning copy. <q>A rule that produces a number fires. A rule that produces a sentiment does not.</q> Everything that can be made executable carries a rule, a way to detect it and a default. Everything else stays his, and a system that claims to have learned it has started guessing confidently.</p>
'''.replace("__N__", str(n_rules))

VISION_SECTION = f'''<section id="vision">
      <header>
        <h2>The vision record</h2>
        <p>The other file, kept at <code>~/.claude/ai-design-vision.md</code> for mining into talks and writing. Philosophy lives there; the executable rule lives in the judgment file. One thesis per section, with the quote that anchors it. Last updated {e(V.get("last_updated",""))}.</p>
      </header>
      <ol class="themes">{themes_html}</ol>
      <h3>Open threads worth developing</h3>
      <ul class="threads">{threads_html}</ul>
    </section>''' if WITH_VISION else ''

page = f'''<title>Design Toolkit</title>
<meta name="description" content="What is in the design toolkit and what it has learned about how Marc judges design.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {{
  --u: 24px;
  --s-1: 4px; --s-2: 8px; --s-3: 12px; --s-4: 16px; --s-6: 24px; --s-8: 32px; --s-12: 48px; --s-16: 64px;
  --r-2: 8px; --r-3: 12px;
  --ground: #F5F7F5; --surface: #FFFFFF; --sunk: #ECF0EE;
  --ink: #18201E; --ink-2: #4E5A57; --ink-3: #7E8A87;
  --line: #D6DDDA; --line-strong: #B9C3BF;
  --accent: #0F6B5A; --accent-ink: #0B5446; --accent-tint: #DCEEE8;
  --code: #1E2826; --code-ink: #DCE5E1;
  --display: "Bricolage Grotesque", "Helvetica Neue", Arial, sans-serif;
  --body: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
  --mono: "IBM Plex Mono", "SFMono-Regular", Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground: #121817; --surface: #192120; --sunk: #0E1413;
    --ink: #E6ECEA; --ink-2: #A9B5B1; --ink-3: #7C8985;
    --line: #2A3431; --line-strong: #3B4743;
    --accent: #5CC7AA; --accent-ink: #8FDCC6; --accent-tint: #173129;
    --code: #0E1413; --code-ink: #C9D4D0;
  }}
}}
:root[data-theme="dark"] {{
  --ground: #121817; --surface: #192120; --sunk: #0E1413;
  --ink: #E6ECEA; --ink-2: #A9B5B1; --ink-3: #7C8985;
  --line: #2A3431; --line-strong: #3B4743;
  --accent: #5CC7AA; --accent-ink: #8FDCC6; --accent-tint: #173129;
  --code: #0E1413; --code-ink: #C9D4D0;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--ground); color: var(--ink); font: 400 16px/var(--u) var(--body); -webkit-font-smoothing: antialiased; }}
a {{ color: var(--accent-ink); text-decoration-thickness: 1px; text-underline-offset: 3px; }}
a:focus-visible, summary:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
h1, h2, h3, h4 {{ font-family: var(--display); font-weight: 500; margin: 0; text-wrap: balance; letter-spacing: -0.005em; }}
h1 {{ font-size: 40px; line-height: var(--s-12); font-weight: 600; }}
h2 {{ font-size: 28px; line-height: 36px; }}
h3 {{ font-size: 20px; line-height: var(--u); }}
h4 {{ font-size: 16px; line-height: var(--u); font-weight: 600; }}
p {{ margin: 0; }}
q {{ quotes: "\\201C" "\\201D"; font-style: italic; }}
b {{ font-weight: 600; }}
code {{ font-family: var(--mono); font-size: 14px; }}

.shell {{ max-width: 1120px; margin: 0 auto; padding: var(--s-12) var(--s-6) var(--s-16); display: grid; grid-template-columns: 1fr; gap: var(--s-12); }}
@media (min-width: 960px) {{ .shell {{ grid-template-columns: 200px minmax(0, 720px); column-gap: var(--s-16); }} }}

/* masthead */
.mast {{ grid-column: 1 / -1; display: flex; flex-direction: column; gap: var(--s-6); max-width: 720px; }}
.mast .eyebrow {{ font-family: var(--mono); font-size: 13px; line-height: 20px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-3); }}
.mast .lede {{ font-size: 18px; line-height: 28px; color: var(--ink-2); max-width: 62ch; }}
.facts {{ display: flex; flex-wrap: wrap; gap: var(--s-2) var(--s-6); margin: 0; padding: 0; list-style: none; font-family: var(--mono); font-size: 13px; line-height: 20px; color: var(--ink-3); }}
.facts b {{ color: var(--ink); font-weight: 500; }}

/* nav */
nav.toc {{ align-self: start; }}
@media (min-width: 960px) {{ nav.toc {{ position: sticky; top: var(--s-6); }} }}
nav.toc ol {{ list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: var(--s-1) var(--s-4); }}
@media (min-width: 960px) {{ nav.toc ol {{ flex-direction: column; gap: 0; border-left: 1px solid var(--line); }} }}
nav.toc a {{ display: block; padding: 2px 0; color: var(--ink-2); text-decoration: none; font-size: 14px; line-height: 20px; }}
@media (min-width: 960px) {{ nav.toc a {{ padding: 2px var(--s-3); margin-left: -1px; border-left: 1px solid transparent; }} }}
nav.toc a:hover {{ color: var(--ink); border-left-color: var(--line-strong); }}
nav.toc .count {{ color: var(--ink-3); font-family: var(--mono); font-size: 12px; margin-left: var(--s-2); }}

main {{ display: flex; flex-direction: column; gap: var(--s-16); min-width: 0; }}
section {{ display: flex; flex-direction: column; gap: var(--s-6); scroll-margin-top: var(--s-6); }}
section > header {{ display: flex; flex-direction: column; gap: var(--s-1); padding-bottom: var(--s-3); border-bottom: 1px solid var(--line-strong); }}
section > header p {{ color: var(--ink-2); max-width: 62ch; }}
.intro {{ max-width: 62ch; color: var(--ink-2); }}

/* judgment */
.judgment {{ display: flex; flex-direction: column; gap: var(--s-6); background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-3); padding: var(--s-8); max-width: none; }}
.judgment .lede {{ font-size: 18px; line-height: 28px; }}
.judgment h3 {{ padding-top: var(--s-6); border-top: 1px solid var(--line); margin-bottom: calc(var(--s-3) - var(--s-6)); }}
.judgment p {{ max-width: 66ch; }}
.judgment b {{ color: var(--accent-ink); }}
.ladder {{ margin: 0; display: flex; flex-direction: column; gap: var(--s-3); padding: var(--s-4) var(--s-4) var(--s-3); background: var(--sunk); border-radius: var(--r-2); }}
.ladder .rung {{ display: grid; grid-template-columns: 32px 56px 1fr; align-items: center; gap: var(--s-3); font-family: var(--mono); font-size: 13px; line-height: 20px; color: var(--ink-2); font-variant-numeric: tabular-nums; }}
.ladder .rung i {{ display: block; height: var(--h); width: 100%; max-width: 320px; background: var(--line-strong); border-radius: 2px; }}
.ladder .rung.on i {{ background: var(--accent); }}
.ladder .rung.on .px, .ladder .rung.on .fr {{ color: var(--ink); font-weight: 500; }}
.ladder figcaption {{ font-size: 13px; line-height: 20px; color: var(--ink-3); }}

/* vision */
.themes {{ list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; }}
.themes li {{ display: flex; flex-direction: column; gap: var(--s-1); padding: var(--s-4) 0; border-top: 1px solid var(--line); }}
.themes li:last-child {{ border-bottom: 1px solid var(--line); }}
.themes p {{ color: var(--ink-2); max-width: 66ch; }}
blockquote {{ margin: var(--s-2) 0 0; padding-left: var(--s-3); border-left: 2px solid var(--accent); font-style: italic; color: var(--ink); max-width: 62ch; }}
.threads {{ margin: 0; padding-left: 1.2em; color: var(--ink-2); display: flex; flex-direction: column; gap: var(--s-1); max-width: 66ch; }}

/* entries */
.list {{ display: flex; flex-direction: column; }}
.entry {{ display: flex; flex-direction: column; gap: var(--s-6); padding: var(--s-6) 0; border-top: 1px solid var(--line); scroll-margin-top: var(--s-6); }}
.entry:first-child {{ border-top: 0; padding-top: 0; }}
.entry.compact {{ gap: var(--s-3); }}
.entry-head {{ display: flex; flex-direction: column; gap: var(--s-1); }}
.entry-head h3 {{ font-family: var(--mono); font-weight: 500; font-size: 18px; display: flex; align-items: baseline; gap: var(--s-2); }}
.entry-head .slash {{ color: var(--ink-3); }}
.badge {{ font-family: var(--body); font-size: 12px; line-height: 16px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--accent-ink); background: var(--accent-tint); padding: 2px 8px; border-radius: 999px; font-weight: 500; }}
.tagline {{ font-family: var(--display); font-size: 20px; line-height: 28px; color: var(--ink); }}
.does {{ max-width: 66ch; }}
.kv {{ margin: 0; display: flex; flex-direction: column; gap: var(--s-3); }}
.kv > div {{ display: grid; grid-template-columns: 112px 1fr; gap: var(--s-3); }}
.kv dt {{ font-size: 13px; line-height: var(--u); letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-3); font-weight: 500; }}
.kv dd {{ margin: 0; color: var(--ink-2); max-width: 60ch; }}
.kv dd q {{ color: var(--ink); }}
.chips {{ list-style: none; margin: 0; padding: 0; display: inline-flex; flex-wrap: wrap; gap: var(--s-2); vertical-align: middle; }}
.chips li {{ font-family: var(--mono); font-size: 13px; line-height: 20px; padding: 2px 8px; border: 1px solid var(--line-strong); border-radius: 6px; color: var(--ink-2); }}
.calls {{ display: flex; align-items: center; gap: var(--s-3); flex-wrap: wrap; }}
.calls .lbl {{ font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-3); font-weight: 500; }}
ul.plain {{ margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: var(--s-1); }}
pre.usage {{ margin: 0; background: var(--code); color: var(--code-ink); border-radius: var(--r-2); padding: var(--s-4); overflow-x: auto; font-size: 13px; line-height: 20px; }}
pre.usage code {{ font-size: inherit; }}

details.src {{ border: 1px solid var(--line); border-radius: var(--r-2); background: var(--surface); }}
details.src summary {{ cursor: pointer; padding: var(--s-2) var(--s-4); font-family: var(--mono); font-size: 13px; line-height: var(--u); color: var(--accent-ink); display: flex; justify-content: space-between; gap: var(--s-4); list-style: none; }}
details.src summary::-webkit-details-marker {{ display: none; }}
details.src summary::before {{ content: "+"; margin-right: var(--s-2); color: var(--ink-3); }}
details.src[open] summary::before {{ content: "\\2212"; }}
details.src summary .len {{ color: var(--ink-3); }}
details.src pre {{ margin: 0; border-top: 1px solid var(--line); padding: var(--s-4); max-height: 560px; overflow: auto; font-size: 13px; line-height: 20px; white-space: pre-wrap; overflow-wrap: anywhere; color: var(--ink); background: var(--sunk); border-radius: 0 0 var(--r-2) var(--r-2); }}
details.src pre code {{ font-size: inherit; }}

/* enforcement, architecture */
ol.rules {{ margin: 0; padding-left: 1.4em; display: flex; flex-direction: column; gap: var(--s-3); max-width: 66ch; }}
ol.rules li::marker {{ font-family: var(--mono); color: var(--ink-3); font-size: 13px; }}
.tbl {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: 15px; line-height: var(--u); }}
th, td {{ text-align: left; padding: var(--s-2) var(--s-3); border-bottom: 1px solid var(--line); vertical-align: top; }}
th {{ font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-3); font-weight: 500; }}
td:first-child {{ font-family: var(--mono); font-size: 14px; white-space: nowrap; }}
td code {{ font-size: 14px; }}
@media (prefers-reduced-motion: no-preference) {{ html {{ scroll-behavior: smooth; }} }}
</style>

<div class="shell">
  <header class="mast">
    <p class="eyebrow">design-toolkit</p>
    <h1>Design Toolkit</h1>
    <p class="lede">A designer's standards, written once and pulled into every project. {word(len(skills)).capitalize()} skills hold the methods, {word(len(S["agents"]))} agents keep the heavy work out of the thread, {word(len(S["tools"]))} executables make the checks repeatable, and one judgment file holds what the system has learned about how Marc decides.</p>
    <ul class="facts">
      <li><b>{len(skills)}</b> skills</li>
      <li><b>{len(S["agents"])}</b> agents</li>
      <li><b>{len(S["tools"])}</b> executables</li>
      <li><b id="gh-count">{n_commits}</b> commits</li>
      <li>last commit <b id="gh-date">{e(last_date)}</b> <span id="gh-commit">{e(last_commit)}</span></li>
      <li>built {datetime.date.today().isoformat()}</li>
    </ul>
  </header>

  <nav class="toc" aria-label="Sections">
    <ol>
      <li><a href="#judgment">Judgment</a></li>
      {f'<li><a href="#vision">Vision record<span class="count">{len(V.get("themes", []))}</span></a></li>' if WITH_VISION else ""}
      <li><a href="#skills">Skills<span class="count">{len(skills)}</span></a></li>
      <li><a href="#agents">Agents<span class="count">{len(S["agents"])}</span></a></li>
      <li><a href="#tools">Executables<span class="count">{len(S["tools"])}</span></a></li>
      <li><a href="#rules">Standing rules<span class="count">{len(S.get("enforcement", []))}</span></a></li>
      <li><a href="#templates">Templates</a></li>
      <li><a href="#architecture">Architecture</a></li>
    </ol>
  </nav>

  <main>
    <section id="judgment">
      <header>
        <h2>What the system understands about how Marc judges design</h2>
        <p>Drawn from <code>judgment/marc.md</code>, the toolkit's one personal layer, published from <code>~/.claude/design-judgments.md</code> by <code>tools/publish-judgment</code> with client names replaced. {n_rules} ruled rules in Part 1. Last updated {e(J_UPDATED)}.</p>
      </header>
      <div class="judgment">{judgment_html}</div>
      {details("Read judgment/marc.md", raw("judgment/marc.md"))}
    </section>

    {VISION_SECTION}
    <section id="skills">
      <header>
        <h2>Skills</h2>
        <p>Instructions, invoked as <code>/name</code> in any project. Listed in the order a project meets them: the contract first, then the files that carry state, then the passes that do the work. Every skill reads the project's contract before it changes anything.</p>
      </header>
      <div class="list">{skills_html}</div>
    </section>

    <section id="agents">
      <header>
        <h2>Agents</h2>
        <p>Read-only. Each runs one skill in its own context so a sweep's screenshots and scan output never land in the main thread. What comes back is the finding list; the decision that follows stays in the conversation.</p>
      </header>
      <div class="list">{agents_html}</div>
    </section>

    <section id="tools">
      <header>
        <h2>Executables</h2>
        <p>Skills are instructions; these are programs. A rewritten check can be wrong differently each time. Both install to <code>~/.claude/tools/</code>, both exit non-zero on failure, and their coverage is deliberately complementary: revert a spacing rule and guard says the file is fine, because it is, while measure reports the gaps that changed.</p>
      </header>
      <div class="list">{tools_html}</div>
    </section>

    <section id="rules">
      <header>
        <h2>Standing rules</h2>
        <p>Appended to <code>~/.claude/CLAUDE.md</code> by the installer, so they bind every session on the machine whether or not a skill is invoked.</p>
      </header>
      <ol class="rules">{enforcement_html}</ol>
      {details("Read claude-md-section.md", raw("claude-md-section.md"))}
    </section>

    <section id="templates">
      <header>
        <h2>Templates</h2>
        <p>For a project that has nothing yet. The contract skill adopts an existing file before it ever creates one of these.</p>
      </header>
      <div class="list">{templates_html}</div>
    </section>

    <section id="architecture">
      <header>
        <h2>Architecture</h2>
        <p>Files are organized by rate of change, not by topic. A fast-changing fact inside a slow-changing document makes the whole document look stale, and then none of it gets trusted.</p>
      </header>
      <div class="tbl"><table>
        <thead><tr><th>Changes</th><th>File</th><th>Holds</th></tr></thead>
        <tbody>
          <tr><td>never</td><td><code>~/.claude/CLAUDE.md</code></td><td>The rules that bind every session</td></tr>
          <tr><td>rarely</td><td><code>~/.claude/design-judgments.md</code></td><td>How this designer decides</td></tr>
          <tr><td>occasionally</td><td>the project's contract</td><td>What is true in this project</td></tr>
          <tr><td>every session</td><td>the project's <code>STATUS.md</code></td><td>Where the work is right now</td></tr>
        </tbody>
      </table></div>
      <p class="intro"><b>Grammar travels, vocabulary does not.</b> A design system copied between projects hands over the values, which belong to the project they came from. What transfers is how many distinct values are allowed, the ratios between them, and which relationship gets which. That is what taste-extract recovers.</p>
      <h3>Pulling updates</h3>
      <pre class="usage"><code>git -C ~/design-toolkit pull
~/design-toolkit/install.sh
# then open a new session: skills register at start</code></pre>
      {details("Read README.md", raw("README.md"))}
    </section>
  </main>
</div>
'''
FOOTER_JS = '<script>\n/* The footer is written at build time, before the commit that carries it, so it\n   would always name the previous commit. Read the live values from GitHub and\n   keep the built ones if the request fails. */\n(function () {\n  var api = "https://api.github.com/repos/marcbanderson/design-toolkit/commits?sha=main&per_page=1";\n  fetch(api).then(function (r) {\n    if (!r.ok) throw 0;\n    var link = r.headers.get("Link") || "", m = link.match(/[?&]page=(\\d+)>; rel="last"/);\n    if (m) document.getElementById("gh-count").textContent = m[1];\n    return r.json();\n  }).then(function (c) {\n    if (!c || !c[0]) return;\n    var sha = c[0].sha.slice(0, 7), msg = c[0].commit.message.split("\\n")[0];\n    document.getElementById("gh-commit").textContent = sha + "  " + msg;\n    document.getElementById("gh-date").textContent = c[0].commit.committer.date.slice(0, 10);\n  }).catch(function () {});\n})();\n</script>'
page = "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n" + page.replace("<style>", "</head>\n<body>\n<style>", 1) + "\n" + FOOTER_JS + "\n</body>\n</html>\n"
# the title and links belong in head: move everything before <style> up
head_end = page.index("</head>")
pre = page[page.index("<title>"):page.index("</head>")]
page = page[:page.index("<title>")] + page[page.index("</head>"):]
page = page.replace("<head>\n<meta charset=\"utf-8\">", "<head>\n<meta charset=\"utf-8\">\n" + pre.strip(), 1)
import shutil
shutil.copy(os.path.join(ROOT, "overlay", "overlay.js"), os.path.join(HERE, "demo", "overlay.js"))
out = os.path.join(HERE, "index.html")
open(out, "w", encoding="utf-8").write(page)
print(out, len(page), "bytes")
