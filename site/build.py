#!/usr/bin/env python3
"""Build the toolkit web view: site/index.html, one self-contained page.

  python3 site/build.py              rebuild from summary.json and the repo files
  python3 site/build.py --vision     also include the vision record section, which
                                     quotes ~/.claude/ai-design-vision.md and is
                                     left out of the committed page by default

summary.json holds the per-skill, agent and tool summaries and the vision
themes; edit it when a skill changes, or regenerate it with a session.
"""
import json, os, sys, html, subprocess, datetime

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

# ---------- Judgment blurb (written in the main thread, from judgment/marc.md) ----------
judgment_html = '''
<p class="lede">The toolkit keeps one personal file, and this is what it says. Every line in it is marked <b>Stated</b>, his words, or <b>Observed</b>, a pattern inferred from repeated choices, and an Observed entry is never promoted to a Stated one. The file is meant to be predictive: when a situation comes up, this is what he will want, and why.</p>

<h3>How he reads a screen</h3>
<p><b>Vertical spacing is the first thing he sees.</b> Before hierarchy, before colour, before copy. If something is wrong and nobody knows what, the gaps are checked first. Tight reads as broken, loose reads as unfinished, and in seven weeks he has never once asked for less space. "Squished" is his most common word for a defect.</p>
<p>He notices weight before size. A wrong font weight gets flagged; a size one step off often does not. And a number that looks confident but is wrong is worse than a blank: a fabricated 0.0, a dash where a word belongs, a zero standing in for an absent value.</p>
<p>In a list, every row is one height and one grammar. The options of one control are one object. A field that a choice needs opens inside the chosen option, not below the control.</p>

<h3>Where spacing comes from</h3>
<p><b>Spacing is derived from the type, never chosen beside it.</b> This is the deepest rule he holds about systems, and he arrived at it twice: once by eye, once by argument. The unit is the line-height of body text, and every vertical distance is a count of it. The ladder he picked by eye over weeks of corrections turned out to be clean fractions of his 24px line, with no remainder. He had the relation before he had the words for it.</p>
<figure class="ladder" aria-label="The rhythm ladder as fractions of a 24px body line">
  <div class="rung"><span class="px">4</span><span class="fr">1/6 u</span><i style="--h:4px"></i></div>
  <div class="rung"><span class="px">8</span><span class="fr">1/3 u</span><i style="--h:8px"></i></div>
  <div class="rung"><span class="px">12</span><span class="fr">1/2 u</span><i style="--h:12px"></i></div>
  <div class="rung"><span class="px">16</span><span class="fr">2/3 u</span><i style="--h:16px"></i></div>
  <div class="rung on"><span class="px">24</span><span class="fr">1 u</span><i style="--h:24px"></i></div>
  <div class="rung"><span class="px">32</span><span class="fr">4/3 u</span><i style="--h:32px"></i></div>
  <div class="rung"><span class="px">48</span><span class="fr">2 u</span><i style="--h:48px"></i></div>
  <figcaption>u is the body line, 24px. This page is set on the same ladder.</figcaption>
</figure>
<p>Three consequences follow, and he expects them held. The type ramp is the primary decision and the spacing scale is derived from it; when the two disagree, the type wins and the spacing moves. The unit must be composite, so the fractions land on whole numbers, which turns the leading decision into "pick the ratio that lands the unit on a divisible number". And density is an index shift, not a multiplier: each role moves one step along the shared ladder, so one token scale serves dense, default and loose.</p>
<p>The same day he extended it to corners without being prompted: <q>why are our radiuses 6, 10 and 12? Shouldn't we do 8, 12, 16?</q> Expect any remaining eye-picked scale to get the same question.</p>

<h3>How he groups things</h3>
<p><b>To bind two things, move the next thing away. Never pull the pair tighter.</b> This is the sharpest correction he has given, because the rule was already written down and still got broken. When a relationship needs to read as closer, increase the distance to everything else.</p>
<p>In the reading flow he uses no middle rungs. On the frames he reworked by hand, the content stack runs at exactly two distances: bound, at 1/6 u, and separate, at 1 u, with 2 u between blocks. The middle rungs still exist, but only inside components. A flat 12 makes everything equally related, so nothing groups.</p>
<p>A button is an action, not a continuation of the text above it. It gets a full unit, never the tight inside-a-group rung. The air belongs to the component, as padding on the component, so it travels to every screen instead of being retyped per layout. And scale moves with content density while the ratio does not: a sparse screen runs 1 u inside and 2 u between, a dense one 1/3 u and 1 u, both roughly a 2 to 3x differential.</p>

<h3>How he decides</h3>
<p>Craft on principle, positioning on business need, and he does not confuse the two. A spacing question gets a rule. Whether a button says "Join the beta" or "Get in touch" gets reasoned from what the business wants from the visitor.</p>
<p><b>An aesthetic judgment is not finished until it is portable.</b> Three times in a month he moved from "I like this" to "state it as a rule that works on someone else's scale". When he approves something, the next question is "can that be a rule", so the rule is offered before he asks.</p>
<p>He looks for the structural cause, not the numeric fix. Given a list of off-scale heights he did not ask which token to snap them to; he asked whether the height should exist at all: <q>if it's a height, it might be a 'hug' in figma that is defined by top and bottom margins, or content within.</q> He was right, and the fix was to delete the value. Retirement over deprecation: when an option is wrong he removes it so it cannot be reached. A metric is never an answer to a visual question. He will take a concern seriously and then decide; push back once with evidence, then do what he says.</p>

<h3>How he wants to work</h3>
<p><q>I don't want you to make the prototype by yourself. I will guide you to make it, I just need you to have proper context.</q> Context first, direction after; no opening menu of options. Seeing beats describing: the dominant feedback mode is a screenshot with an annotation, and the loop that matters is intent to something he can look at. He tells a rule once and expects it held. Colleague reactions are design input, relayed without ceremony.</p>

<h3>What he counts as done</h3>
<p>Both places, same session: a fix in code that is not in Figma is new drift. Verified against the artifact he is looking at, not committed, not pushed, not merged. And gaps named rather than discovered: he would far rather be told the DELETE path is unexercised than find it himself in a screenshot.</p>

<h3>Colour</h3>
<p>Marc has a degree of colour vision deficiency. Two series in a chart must differ in lightness, not only in hue. This is a requirement, not a preference.</p>

<h3>Where the system stops</h3>
<p>Some entries have no detector and never will, and recognising them is the point. Composition: what goes on a screen, in what order, and what gets cut. When to break a rule, which he does deliberately and usually rightly. Whether a thing is beautiful. Positioning copy. For these the instruction is plain: <b>ask, do not assume.</b> A system that claims to have learned them has started guessing confidently.</p>

<h3>How an entry earns its place</h3>
<p><q>A rule that produces a number fires. A rule that produces a sentiment does not.</q> So each entry that can be made executable carries a Rule in his words, a Detect that can actually be run, and a Default so no judgment is needed to apply it. The loop: he corrects one case, the rule is extracted rather than the fix, a detector is written, the detector finds the whole class, he confirms on the cheapest second case, and the result is verified by measurement. One correction covered twelve screens that way.</p>
'''

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
    <p class="lede">A designer's standards, written once and pulled into every project. Nine skills hold the methods, two agents keep the sweeps out of the thread, two executables make the checks repeatable, and one judgment file holds what the system has learned about how Marc decides.</p>
    <ul class="facts">
      <li><b>{len(skills)}</b> skills</li>
      <li><b>{len(S["agents"])}</b> agents</li>
      <li><b>{len(S["tools"])}</b> executables</li>
      <li><b>{n_commits}</b> commits</li>
      <li>last commit <b>{e(last_date)}</b> {e(last_commit)}</li>
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
        <p>Drawn from <code>judgment/marc.md</code>, the toolkit's one personal layer. Last updated 2026-09-18.</p>
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
        <p>Files are organised by rate of change, not by topic. A fast-changing fact inside a slow-changing document makes the whole document look stale, and then none of it gets trusted.</p>
      </header>
      <div class="tbl"><table>
        <thead><tr><th>Changes</th><th>File</th><th>Holds</th></tr></thead>
        <tbody>
          <tr><td>never</td><td><code>~/.claude/CLAUDE.md</code></td><td>The rules that bind every session</td></tr>
          <tr><td>rarely</td><td><code>~/.claude/design-judgment.md</code></td><td>How this designer decides</td></tr>
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
page = "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n" + page.replace("<style>", "</head>\n<body>\n<style>", 1) + "\n</body>\n</html>\n"
# the title and links belong in head: move everything before <style> up
head_end = page.index("</head>")
pre = page[page.index("<title>"):page.index("</head>")]
page = page[:page.index("<title>")] + page[page.index("</head>"):]
page = page.replace("<head>\n<meta charset=\"utf-8\">", "<head>\n<meta charset=\"utf-8\">\n" + pre.strip(), 1)
out = os.path.join(HERE, "index.html")
open(out, "w", encoding="utf-8").write(page)
print(out, len(page), "bytes")
