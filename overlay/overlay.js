/* Toolkit overlay.
 *
 * Sits on top of a rendered design. Click an element, see its spacing and text
 * as tokens, change them only to other tokens, and watch the render move. A
 * change is then applied one of three ways:
 *
 *   tier 1  the winning declaration is in a stylesheet the dev server can reach:
 *           overlay-server rewrites that line, the sheet reloads, the rendered
 *           value is checked against the target. No model involved.
 *   tier 2  the same, but the rule is shared by other elements: one question,
 *           change all of them or not, then tier 1.
 *   tier 3  the declaration cannot be located (inline style, cross-origin
 *           sheet, CSS-in-JS): the change goes into the prompt for the session.
 *
 * Every change, whichever tier, is a decision, and the export records it.
 *
 * Tokens come from window.__designTokens when the page provides it, from
 * overlay-server when the script is served by it, otherwise they are inferred
 * from :root custom properties and the text styles on the page.
 *
 * Toggle with Alt+Shift+D, or window.__toolkitOverlay.toggle().
 */
(function () {
  if (window.__toolkitOverlay) { window.__toolkitOverlay.toggle(); return; }
  const SCRIPT_SRC = (document.currentScript && document.currentScript.src) || "";
  // The endpoint is the script's own origin, but only once it answers as overlay-server.
  const CANDIDATE = (window.__designTokens && window.__designTokens.endpoint) || (/^https?:\/\//.test(SCRIPT_SRC) && /\/overlay\.js(\?|$)/.test(SCRIPT_SRC) ? new URL(SCRIPT_SRC).origin : "");
  let ENDPOINT = "";

  // ---------- tokens ----------
  const FRACTIONS = [[1,6],[1,4],[1,3],[1,2],[2,3],[1,1],[4,3],[3,2],[2,1],[3,1]];
  function discoverTokens() {
    const given = window.__designTokens || {};
    const bodyLH = parseFloat(getComputedStyle(document.body).lineHeight);
    const unit = given.unit || (isFinite(bodyLH) ? Math.round(bodyLH) : 24);
    const unitNote = given.unit ? "" : `unit ${unit} from the body line-height, not stated in the contract`;
    let space = given.space, spaceSource = given.source ? "contract" : "manifest";
    if (!space) {
      // custom properties on :root; var() chains are followed and the alias layer wins
      space = {}; spaceSource = "inferred from :root";
      const decls = {};
      for (const sheet of document.styleSheets) {
        let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
        for (const r of rules) {
          if (!r.selectorText || !/(^|,)\s*(:root|html)\s*(,|$)/.test(r.selectorText)) continue;
          for (const name of r.style) if (name.startsWith("--") && !(name in decls)) decls[name] = r.style.getPropertyValue(name).trim();
        }
      }
      const SPACEY = /space|spacing|gap|^--sp|^--s-\d|-s-/i;
      const resolve = (name, depth) => {
        const v = decls[name]; if (v == null || depth > 8) return null;
        const a = /^var\(\s*(--[\w-]+)/.exec(v); if (a) { const r = resolve(a[1], depth + 1); return r && { px: r.px, depth: r.depth, chain: [a[1]].concat(r.chain) }; }
        const m = /^(-?\d*\.?\d+)(px|rem)$/.exec(v); return m ? { px: m[2] === "rem" ? parseFloat(m[1]) * 16 : parseFloat(m[1]), depth, chain: [] } : null;
      };
      const byPx = new Map();
      for (const name in decls) {
        const r = resolve(name, 0); if (!r) continue;
        if (!SPACEY.test(name) && !r.chain.some(c => SPACEY.test(c))) continue;
        if (!byPx.has(r.px)) byPx.set(r.px, []); byPx.get(r.px).push({ name, depth: r.depth });
      }
      for (const [px, names] of byPx) { names.sort((a, b) => (b.depth - a.depth) || (a.name.length - b.name.length)); space[names[0].name.replace(/^--/, "")] = px; }
    }
    let text = given.text, textSource = given.source ? "contract" : "manifest";
    if (!text) {
      text = {}; textSource = "inferred from the page";
      const seen = new Map();
      for (const el of document.body.querySelectorAll("*")) {
        if (el.closest("[data-toolkit-overlay]") || !hasOwnText(el)) continue;
        const cs = getComputedStyle(el);
        const key = `${parseFloat(cs.fontSize)}/${parseFloat(cs.lineHeight)}/${cs.fontWeight}`;
        const s = seen.get(key) || { size: parseFloat(cs.fontSize), line: parseFloat(cs.lineHeight), weight: +cs.fontWeight, n: 0 };
        s.n++; seen.set(key, s);
      }
      [...seen.values()].sort((a, b) => b.n - a.n).slice(0, 8).forEach((s, i) => { text[`style-${i + 1} (${s.n} uses)`] = s; });
    }
    const bind = given.bind || "var(--{name})";
    const ladder = Object.entries(space).map(([name, px]) => ({ name, px })).sort((a, b) => a.px - b.px);
    return { unit, space, ladder, text, spaceSource, textSource, bind, unitNote, notes: given.notes || [] };
  }
  function hasOwnText(el) { for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) return true; return false; }
  function tokenFor(px) {
    const hit = T.ladder.find(t => Math.abs(t.px - px) < 0.5);
    if (hit) return { kind: "token", name: hit.name };
    if (px === 0) return { kind: "zero", name: "0" };
    const f = FRACTIONS.find(([a, b]) => Math.abs(px - T.unit * a / b) < 0.5);
    if (f) return { kind: "fraction", name: `${f[0]}/${f[1]} u, no token` };
    return { kind: "off", name: "off ladder" };
  }
  function nearestToken(px) {
    let best = T.ladder[0];
    for (const t of T.ladder) if (Math.abs(t.px - px) < Math.abs(best.px - px) || (Math.abs(t.px - px) === Math.abs(best.px - px) && t.px > best.px)) best = t;
    return best;
  }
  function bindingFor(tokenName) { return tokenName === "0" ? "0" : T.bind.replace("{name}", tokenName.replace(/^--/, "")); }
  function textStyleFor(cs) {
    const size = parseFloat(cs.fontSize), line = parseFloat(cs.lineHeight), weight = +cs.fontWeight;
    for (const [name, s] of Object.entries(T.text)) if (Math.abs(s.size - size) < 0.5 && Math.abs(s.line - line) < 0.5 && s.weight === weight) return name;
    return null;
  }

  // ---------- identity ----------
  function componentName(el) {
    let node = el;
    while (node) {
      if (node.dataset && (node.dataset.component || node.dataset.testid)) return node.dataset.component || node.dataset.testid;
      const fk = Object.keys(node).find(k => k.startsWith("__reactFiber$"));
      if (fk) { let f = node[fk]; while (f) { const t = f.type; if (typeof t === "function" && t.name && /^[A-Z]/.test(t.name)) return t.name; if (t && t.displayName) return t.displayName; f = f.return; } }
      if (node.__vueParentComponent && node.__vueParentComponent.type && node.__vueParentComponent.type.name) return node.__vueParentComponent.type.name;
      node = node.parentElement;
    }
    return null;
  }
  function shortSel(el) {
    const cls = [...el.classList].filter(c => !/^(is-|has-|hover|focus|active|js-)/.test(c)).slice(0, 2).map(c => "." + CSS.escape(c)).join("");
    return el.tagName.toLowerCase() + cls;
  }
  function pathOf(el) {
    const parts = []; let n = el, depth = 0;
    while (n && n !== document.body && depth < 4) {
      let s = shortSel(n);
      if (n.parentElement) { const same = [...n.parentElement.children].filter(c => c.tagName === n.tagName); if (same.length > 1 && n.classList.length === 0) s += `:nth-of-type(${same.indexOf(n) + 1})`; }
      parts.unshift(s); n = n.parentElement; depth++;
    }
    return parts.join(" > ");
  }
  function identity(el) {
    const t = (el.innerText || el.textContent || "").trim().replace(/\s+/g, " ");
    return { component: componentName(el), path: pathOf(el), text: t.length > 60 ? t.slice(0, 57).replace(/\s+\S*$/, "") + "..." : t, tag: el.tagName.toLowerCase() };
  }

  // ---------- cascade: which declaration wins for this property ----------
  const SHORTHAND = { "row-gap": "gap", "column-gap": "gap", "padding-top": "padding", "padding-right": "padding", "padding-bottom": "padding", "padding-left": "padding", "margin-top": "margin", "margin-bottom": "margin" };
  function specificity(sel) {
    const s = sel.replace(/::?[\w-]+(\([^)]*\))?/g, m => (/^::/.test(m) ? " E " : " C "));
    const ids = (s.match(/#[\w-]+/g) || []).length;
    const cls = (s.match(/\.[\w-]+|\[[^\]]+\]| C /g) || []).length;
    const els = (s.match(/(^|[\s>+~])[a-zA-Z][\w-]*| E /g) || []).length;
    return ids * 10000 + cls * 100 + els;
  }
  function resolveDecl(el, prop) {
    const cands = []; let order = 0;
    const walk = (rules, sheet) => {
      for (const r of rules) {
        if (r.cssRules && (r.media || r.conditionText !== undefined)) { if (!r.media || matchMedia(r.media.mediaText).matches) walk(r.cssRules, sheet); continue; }
        if (!r.selectorText || !r.style) continue;
        for (const sel of r.selectorText.split(/,(?![^(]*\))/)) {
          const s = sel.trim(); let ok = false; try { ok = el.matches(s); } catch (e) {}
          if (!ok) continue;
          for (const p of [prop, SHORTHAND[prop]]) {
            if (!p) continue;
            const v = r.style.getPropertyValue(p);
            if (!v) continue;
            cands.push({ sheet, rule: r, selector: s, fullSelector: r.selectorText, prop: p, value: v.trim(), important: r.style.getPropertyPriority(p) === "important", spec: specificity(s), order: order++, longhand: p === prop });
          }
        }
      }
    };
    for (const sheet of document.styleSheets) { let rules; try { rules = sheet.cssRules; } catch (e) { continue; } walk(rules, sheet); }
    if (!cands.length) return null;
    cands.sort((a, b) => (b.important - a.important) || (b.spec - a.spec) || (b.order - a.order) || (b.longhand - a.longhand));
    const w = cands[0];
    const sheetIndex = [...document.styleSheets].indexOf(w.sheet);
    let matches = 0; try { matches = [...document.querySelectorAll(w.fullSelector)].filter(x => !x.closest("[data-toolkit-overlay]")).length; } catch (e) { matches = 1; }
    return { href: w.sheet.href || location.href, inline: !w.sheet.href, sheetIndex, selector: w.fullSelector, prop: w.prop, value: w.value, shorthand: !w.longhand, matches };
  }

  // ---------- state ----------
  let T = discoverTokens();
  const records = [];
  const undoStack = [];
  let selected = null, hoverEl = null, picking = true; // picking false is Navigate: the page gets every click
  const STORE = "toolkit-overlay:" + location.pathname;
  try { const saved = JSON.parse(localStorage.getItem(STORE) || "[]"); saved.forEach(r => records.push(r)); } catch (e) {}
  function persist() { try { localStorage.setItem(STORE, JSON.stringify(records.map(r => Object.assign({}, r, { el: undefined, loc: undefined, busy: undefined })))); } catch (e) {} }
  const newId = () => Date.now().toString(36) + Math.random().toString(16).slice(2, 6);

  function applyChange(el, prop, toPx, toToken, fromPx) {
    const prev = el.style.getPropertyValue(prop);
    el.style.setProperty(prop, toPx + "px", "important");
    const rec = { id: newId(), at: new Date().toISOString(), width: innerWidth, identity: identity(el), prop, fromPx, fromToken: tokenFor(fromPx).name, toPx, toToken, el };
    records.push(rec); undoStack.push({ el, prop, prev }); persist(); render();
  }
  function applyText(el, name, from) {
    const s = T.text[name];
    const prev = { fs: el.style.fontSize, lh: el.style.lineHeight, fw: el.style.fontWeight };
    el.style.setProperty("font-size", s.size + "px", "important"); el.style.setProperty("line-height", s.line + "px", "important"); el.style.setProperty("font-weight", s.weight, "important");
    const rec = { id: newId(), at: new Date().toISOString(), width: innerWidth, identity: identity(el), prop: "text-style", fromPx: `${from.size}/${from.line} ${from.weight}`, fromToken: from.style || "off ramp", toPx: `${s.size}/${s.line} ${s.weight}`, toToken: name, el };
    records.push(rec); undoStack.push({ el, text: prev }); persist(); render();
  }
  function undo() {
    const u = undoStack.pop(); if (!u) return;
    if (u.text) { u.el.style.fontSize = u.text.fs; u.el.style.lineHeight = u.text.lh; u.el.style.fontWeight = u.text.fw; } else u.el.style.setProperty(u.prop, u.prev);
    records.pop(); persist(); render();
  }
  // Net change per element and property: first "from", latest "to". A change
  // that returns to where it started is not a decision and is dropped.
  function netRecords() {
    const net = new Map();
    for (const r of records) {
      const key = `${r.identity.path}|${r.prop}`;
      const cur = net.get(key);
      if (cur) { cur.toPx = r.toPx; cur.toToken = r.toToken; cur.at = r.at; cur.width = r.width; cur.el = r.el || cur.el; cur.applied = r.applied || cur.applied; cur.verified = r.verified !== undefined ? r.verified : cur.verified; cur.loc = r.loc || cur.loc; cur.busy = r.busy || cur.busy; cur.last = r; }
      else net.set(key, Object.assign({}, r, { last: r }));
    }
    return [...net.values()].filter(r => String(r.toPx) !== String(r.fromPx) || r.applied);
  }
  function groupRecords() {
    const g = new Map();
    for (const r of netRecords()) {
      const key = `${r.prop}|${r.fromToken}|${r.toToken}`;
      if (!g.has(key)) g.set(key, { prop: r.prop, fromToken: r.fromToken, fromPx: r.fromPx, toToken: r.toToken, toPx: r.toPx, items: [] });
      g.get(key).items.push(r);
    }
    return [...g.values()];
  }

  // ---------- tiers: locate, apply, verify ----------
  // The tier is a property of the net change, resolved against the live cascade.
  function refind(r) {
    if (r.el && r.el.isConnected) return r.el;
    try { const el = document.querySelector(r.identity.path); if (el) { r.el = el; if (r.last) r.last.el = el; return el; } } catch (e) {}
    return null;
  }
  function tierOf(r) {
    if (!r.el || !r.el.isConnected) refind(r);
    if (r.applied) return { tier: 0, label: `applied ${r.applied.file}:${r.applied.line}${r.verified === false ? ", renders differently" : r.verified ? ", verified" : ""}` };
    if (!ENDPOINT) return { tier: 3, label: "prompt, no session" };
    if (r.prop === "text-style") return { tier: 3, label: "prompt, text styles are a ramp change" };
    if (!r.el || !r.el.isConnected) return { tier: 3, label: "prompt, element gone" };
    const orig = undoStack.find(u => u.el === r.el && u.prop === r.prop);
    if (orig && orig.prev && !/px !important$/.test(orig.prev)) return { tier: 3, label: "prompt, set inline on the element" };
    const d = r.decl || (r.decl = resolveDecl(r.el, r.prop));
    if (!d) return { tier: 3, label: "prompt, no declaration found (browser default)" };
    if (r.loc && r.loc.error) return { tier: 3, label: "prompt, " + r.loc.error };
    if (!r.loc) return { tier: 1, label: "locating", pending: true };
    if (d.matches > 1) return { tier: 2, label: `${r.loc.file}:${r.loc.line}, shared by ${d.matches} elements` };
    return { tier: 1, label: `${r.loc.file}:${r.loc.line}` };
  }
  function locate(r) {
    if (r.busy || r.loc || !r.decl) return;
    r.busy = true;
    fetch(ENDPOINT + "/locate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ href: r.decl.href, selector: r.decl.selector, prop: r.decl.prop, value: r.decl.value }) })
      .then(x => x.json()).then(j => { r.loc = j; r.last.loc = j; r.busy = false; render(); })
      .catch(e => { r.loc = { error: "server unreachable" }; r.busy = false; render(); });
  }
  async function applyToSource(r) {
    const d = r.decl || (r.el && r.el.isConnected ? resolveDecl(r.el, r.prop) : null), binding = bindingFor(r.toToken);
    if (!d) { r.last.loc = { error: "no declaration found" }; render(); return; }
    r.busy = true; r.last.busy = true; render();
    let j;
    try {
      const res = await fetch(ENDPOINT + "/apply", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ href: d.href, selector: d.selector, prop: d.prop, value: d.value, longhand: r.prop, newValue: binding, shorthand: d.shorthand }) });
      j = await res.json();
    } catch (e) { j = { error: e instanceof TypeError && !/fetch/i.test(e.message) ? "overlay error: " + e.message : "server unreachable" }; }
    r.busy = false; r.last.busy = false;
    if (j.error) { r.loc = { error: j.error }; r.last.loc = r.loc; render(); return; }
    r.applied = { file: j.file, line: j.line, before: j.before, after: j.after, guard: j.guard }; r.last.applied = r.applied;
    // let the source drive: drop the preview override, reload the sheet, read the render
    await reloadSheet(d);
    r.el.style.removeProperty(r.prop);
    await new Promise(res => setTimeout(res, 350));
    const rendered = parseFloat(getComputedStyle(r.el).getPropertyValue(r.prop)) || 0;
    r.verified = Math.abs(rendered - r.toPx) < 0.5; r.last.verified = r.verified; r.rendered = rendered;
    if (!r.verified) r.el.style.setProperty(r.prop, r.toPx + "px", "important");
    r.decl = null; r.loc = null; persist(); render();
  }
  async function reloadSheet(d) {
    const sheet = document.styleSheets[d.sheetIndex]; const node = sheet && sheet.ownerNode; if (!node) return;
    if (node.tagName === "LINK") {
      const u = new URL(node.href); u.searchParams.set("toolkit", Date.now());
      await new Promise(res => { node.addEventListener("load", res, { once: true }); node.addEventListener("error", res, { once: true }); node.href = u.toString(); setTimeout(res, 1500); });
    } else if (node.tagName === "STYLE") {
      try {
        const html = await (await fetch(location.href, { cache: "no-store" })).text();
        const doc = new DOMParser().parseFromString(html, "text/html");
        const styles = [...doc.querySelectorAll("style")]; const live = [...document.querySelectorAll("style")].filter(s => !s.closest("[data-toolkit-overlay]"));
        const i = live.indexOf(node); if (styles[i]) node.textContent = styles[i].textContent;
      } catch (e) {}
    }
  }

  // ---------- prompt ----------
  function buildPrompt() {
    const net = netRecords(), applied = net.filter(r => r.applied), pending = net.filter(r => !r.applied);
    const lines = [];
    const id = r => `${r.identity.component ? `<${r.identity.component}> ` : ""}${r.identity.path}${r.identity.text ? ` "${r.identity.text}"` : ""}`;
    lines.push(`Spacing and text decisions from the overlay. Tokens: unit u = ${T.unit}px (${T.spaceSource}); ladder ${T.ladder.map(t => `${t.name}=${t.px}`).join(", ")}.`);
    lines.push(`Preview width: ${innerWidth}px. Page: ${location.href}`);
    if (applied.length) {
      lines.push(""); lines.push("## Already applied to source, deterministically");
      lines.push("These lines were rewritten by overlay-server and the render was checked. Do not redo them. Mirror them to Figma and record them.");
      applied.forEach(r => lines.push(`- ${r.applied.file}:${r.applied.line}  ${r.prop}: ${r.fromToken} (${r.fromPx}) to ${r.toToken}  ${r.verified === false ? "RENDERS " + r.rendered + "px, NOT the target; another rule wins, find it" : "verified"}  ${id(r)}`));
    }
    if (pending.length) {
      lines.push(""); lines.push("## To apply");
      lines.push("Rebind the rule that sets each property rather than editing instances one at a time. Where the same change repeats across a component, fix the component once.");
      const g = new Map();
      for (const r of pending) { const k = `${r.prop}|${r.fromToken}|${r.toToken}`; if (!g.has(k)) g.set(k, { r, items: [] }); g.get(k).items.push(r); }
      [...g.values()].forEach(({ r, items }, i) => {
        lines.push(`${i + 1}. ${r.prop}: ${r.fromToken} (${r.fromPx}) to ${r.toToken} (${r.toPx})${items.length > 1 ? `, ${items.length} elements, so this is a pattern: fix the shared rule` : ""}${r.loc && r.loc.error ? `  [not located: ${r.loc.error}]` : ""}`);
        items.forEach(x => lines.push(`   - ${id(x)}`));
      });
      lines.push("");
      lines.push("Verify before claiming done: the preview is the target. Measure at the same width and confirm each element renders it:");
      lines.push("```json"); lines.push(JSON.stringify(pending.map(r => ({ selector: r.identity.path, prop: r.prop, target: r.toPx })), null, 2)); lines.push("```");
      lines.push(`Run guard verify on every file you touched, and measure --width ${innerWidth} --compare against a snapshot taken before the edit.`);
    }
    lines.push(""); lines.push("## Decisions these codify");
    groupRecords().forEach(g => {
      const comps = [...new Set(g.items.map(r => r.identity.component).filter(Boolean))];
      const where = comps.length ? comps.map(c => `<${c}>`).join(", ") : g.items.map(r => r.identity.path.split(" > ").pop()).join(", ");
      lines.push(`- ${g.prop} on ${where} is ${g.toToken}${g.items.length > 1 ? ", as a rule, not per instance" : ""}. It was ${g.fromToken}${g.fromToken !== String(g.fromPx) ? ` (${g.fromPx})` : ""}.`);
    });
    lines.push("Record each as a settled decision in the project contract, with the why.");
    lines.push(""); lines.push("## Mirror");
    lines.push("Make the same token changes in the Figma frames for these screens in this session. If you cannot find the frame, say so; do not leave it unmirrored silently.");
    return lines.join("\n");
  }

  // ---------- UI ----------
  const host = document.createElement("div");
  host.setAttribute("data-toolkit-overlay", "");
  host.style.cssText = "all:initial;position:fixed;inset:0;pointer-events:none;z-index:2147483646";
  const root = host.attachShadow({ mode: "open" });
  const css = `
    :host { --u:24px; --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s6:24px; --ink:#E9EEEC; --ink2:#A7B3AF; --ink3:#748280; --ground:#151B1A; --sunk:#0E1312; --line:#2B3634; --accent:#5CC7AA; --warn:#F1D27B; --mono:"IBM Plex Mono",Menlo,Consolas,monospace; --sans:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif; }
    * { box-sizing:border-box; }
    .hl { position:fixed; pointer-events:none; }
    .hl.hover { outline:1px dashed rgba(140,160,155,.6); outline-offset:-1px; }
    .hl.sel { outline:2px solid var(--accent); outline-offset:-2px; }
    .hl .tag { position:absolute; left:-2px; top:-22px; background:var(--accent); color:#0B1512; font:500 12px/20px var(--mono); padding:0 6px; white-space:nowrap; }
    .pop { position:fixed; width:320px; max-height:calc(100vh - 16px); overflow:auto; background:var(--ground); color:var(--ink); font:400 14px/20px var(--sans); pointer-events:auto; border:1px solid var(--line); border-radius:8px; box-shadow:0 12px 32px rgba(0,0,0,.35); display:flex; flex-direction:column; }
    .pop .sec { padding:var(--s3) var(--s4); }
    .pop .sec:last-child { border-bottom:0; }
    .pop .id .name { font-size:13px; }
    .pop .field { height:28px; }
    .pop details { display:flex; flex-direction:column; gap:var(--s2); }
    .pop summary { cursor:pointer; list-style:none; font:500 11px/16px var(--sans); letter-spacing:.08em; text-transform:uppercase; color:var(--ink3); }
    .pop summary::-webkit-details-marker { display:none; } .pop summary::after { content:" +"; } .pop details[open] summary::after { content:" \\2212"; }
    .panel { position:fixed; top:0; right:0; bottom:0; width:344px; background:var(--ground); color:var(--ink); font:400 14px/20px var(--sans); pointer-events:auto; display:flex; flex-direction:column; border-left:1px solid var(--line); box-shadow:-8px 0 24px rgba(0,0,0,.25); }
    .head { padding:var(--s3) var(--s4); border-bottom:1px solid var(--line); display:flex; align-items:center; gap:var(--s2); flex-wrap:wrap; }
    .head b { font-weight:600; flex:1; white-space:nowrap; }
    .head small { color:var(--ink3); font:400 12px/16px var(--mono); flex-basis:100%; }
    .head small.warnnote { color:var(--warn); }
    .seg { display:inline-flex; } .seg .btn { border-radius:0; } .seg .btn:first-child { border-radius:6px 0 0 6px; } .seg .btn:last-child { border-radius:0 6px 6px 0; margin-left:-1px; }
    .btn { font:500 12px/20px var(--sans); color:var(--ink); background:transparent; border:1px solid var(--line); border-radius:6px; padding:2px 8px; cursor:pointer; white-space:nowrap; }
    .btn:hover { border-color:var(--ink3); } .btn.on { background:var(--accent); color:#0B1512; border-color:var(--accent); } .btn[disabled] { opacity:.5; cursor:default; }
    .btn:focus-visible, .tok:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }
    .body { overflow:auto; flex:1; display:flex; flex-direction:column; }
    .sec { padding:var(--s4); border-bottom:1px solid var(--line); display:flex; flex-direction:column; gap:var(--s3); }
    .sec h3 { margin:0; font:500 11px/16px var(--sans); letter-spacing:.08em; text-transform:uppercase; color:var(--ink3); }
    .id .name { font:500 14px/20px var(--sans); } .id .path { font:400 12px/16px var(--mono); color:var(--ink2); overflow-wrap:anywhere; } .id .txt { color:var(--ink3); font-size:12px; line-height:16px; }
    .empty { color:var(--ink3); }
    .row { display:flex; flex-direction:column; gap:var(--s1); }
    .row .lab { display:flex; justify-content:space-between; gap:var(--s2); font:400 12px/16px var(--mono); color:var(--ink2); }
    .row .cur { color:var(--ink); } .row .cur.off { color:var(--warn); } .row .cur.off::before { content:"\\25B2 "; } .row .cur.frac { color:var(--ink2); }
    .fields { display:flex; flex-direction:column; gap:var(--s2); }
    .field { position:relative; display:grid; grid-template-columns:1fr auto; align-items:center; height:32px; background:var(--sunk); border:1px solid var(--line); border-radius:6px; padding:0 var(--s2) 0 var(--s3); }
    .field:hover, .field.open { border-color:var(--ink3); }
    .flab { font:400 13px/20px var(--sans); color:var(--ink2); cursor:ew-resize; user-select:none; -webkit-user-select:none; align-self:stretch; display:flex; align-items:center; }
    .flab:active { color:var(--ink); }
    .fval { font:500 13px/20px var(--mono); color:var(--ink); background:transparent; border:0; padding:2px 4px; border-radius:4px; cursor:pointer; display:flex; gap:var(--s2); align-items:baseline; font-variant-numeric:tabular-nums; }
    .fval small { font:400 11px/16px var(--mono); color:var(--ink3); }
    .fval:hover { background:rgba(255,255,255,.05); } .fval.off { color:var(--warn); } .fval.off::before { content:"\\25B2"; font-size:9px; margin-right:2px; } .fval.frac small { color:var(--ink2); }
    .menu { position:absolute; right:0; top:34px; z-index:2; min-width:180px; background:var(--ground); border:1px solid var(--line); border-radius:6px; box-shadow:0 8px 24px rgba(0,0,0,.35); padding:var(--s1); display:flex; flex-direction:column; }
    .mi { display:flex; justify-content:space-between; gap:var(--s3); font:400 12px/20px var(--mono); color:var(--ink2); background:transparent; border:0; border-radius:4px; padding:2px var(--s2); cursor:pointer; text-align:left; font-variant-numeric:tabular-nums; }
    .mi span:first-child { color:var(--ink); } .mi:hover { background:rgba(255,255,255,.06); } .mi.cur { background:var(--accent); } .mi.cur span { color:#0B1512; }
    .toks { display:flex; flex-wrap:wrap; gap:var(--s1); }
    .tok { font:500 12px/20px var(--mono); padding:0 7px; border-radius:5px; border:1px solid var(--line); background:var(--sunk); color:var(--ink2); cursor:pointer; }
    .tok:hover { border-color:var(--ink3); color:var(--ink); } .tok.cur { background:var(--accent); color:#0B1512; border-color:var(--accent); }
    .lint { display:flex; flex-direction:column; gap:var(--s1); padding:var(--s2) var(--s3); border-radius:6px; background:var(--sunk); border-left:3px solid var(--ink3); font-size:12px; line-height:16px; color:var(--ink2); }
    .lint.defect { border-left-color:var(--warn); color:var(--ink); } .lint .fix { align-self:flex-start; }
    .note { font-size:12px; line-height:16px; color:var(--ink3); } .note b { color:var(--ink); font-weight:500; }
    .chg { display:flex; flex-direction:column; gap:var(--s1); padding:var(--s2) 0; border-top:1px solid var(--line); }
    .chg:first-of-type { border-top:0; padding-top:0; }
    .chg .what { display:flex; justify-content:space-between; gap:var(--s2); font:400 12px/16px var(--mono); color:var(--ink2); }
    .chg .what b { color:var(--ink); font-weight:500; }
    .chg .who { font:400 11px/16px var(--mono); color:var(--ink3); overflow-wrap:anywhere; }
    .chg .tier { display:flex; align-items:center; justify-content:space-between; gap:var(--s2); font:400 11px/16px var(--mono); color:var(--ink3); }
    .chg .tier.t0 { color:var(--accent); } .chg .tier.t0.bad { color:var(--warn); } .chg .tier.t2 { color:var(--warn); }
    .chg .diff { font:400 11px/16px var(--mono); background:var(--sunk); border-radius:4px; padding:var(--s1) var(--s2); white-space:pre-wrap; overflow-wrap:anywhere; }
    .chg .diff .m { color:var(--ink3); } .chg .diff .p { color:var(--accent); }
    .foot { padding:var(--s3) var(--s4); border-top:1px solid var(--line); display:flex; gap:var(--s2); align-items:center; }
    .foot .cnt { flex:1; color:var(--ink2); font:400 12px/16px var(--mono); }
    textarea { width:100%; height:260px; background:var(--sunk); color:var(--ink); border:1px solid var(--line); border-radius:6px; padding:var(--s2); font:400 12px/16px var(--mono); resize:vertical; }
  `;
  root.innerHTML = `<style>${css}</style><div class="hl hover" hidden></div><div class="hl sel" hidden><span class="tag"></span></div><div class="pop" hidden></div><div class="panel"></div>`;
  const hoverBox = root.querySelector(".hl.hover"), selBox = root.querySelector(".hl.sel"), panel = root.querySelector(".panel"), pop = root.querySelector(".pop");
  document.documentElement.appendChild(host);

  function place(box, el) {
    if (!el || !el.isConnected) { box.hidden = true; return; }
    const r = el.getBoundingClientRect();
    box.hidden = false; box.style.left = r.left + "px"; box.style.top = r.top + "px"; box.style.width = r.width + "px"; box.style.height = r.height + "px";
  }
  function frameRect(el) {
    const avail = innerWidth - DOCK_W; let frame = null, n = el;
    while (n && n !== document.body) { const r = n.getBoundingClientRect(); if (r.width > 0 && r.width <= avail - POP_W - 2 * GUT) frame = n; n = n.parentElement; }
    return (frame || el).getBoundingClientRect();
  }
  function placePop() {
    if (pop.hidden || !selected || !selected.isConnected) return false;
    const avail = innerWidth - DOCK_W, f = frameRect(selected), r = selected.getBoundingClientRect();
    let left = null;
    if (f.right + GUT + POP_W <= avail - 8) left = f.right + GUT;
    else if (f.left - GUT - POP_W >= 8) left = f.left - GUT - POP_W;
    else if (f.right + 8 + POP_W <= avail) left = f.right + 8;
    if (left === null) return false;
    const hgt = pop.offsetHeight || 300;
    pop.style.left = left + "px"; pop.style.top = Math.max(8, Math.min(r.top, innerHeight - hgt - 8)) + "px";
    return true;
  }
  function h(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

  // ---------- inspection ----------
  const PADS = ["padding-top", "padding-right", "padding-bottom", "padding-left"];
  const MARGS = ["margin-top", "margin-bottom"];
  function inspect(el) {
    const cs = getComputedStyle(el);
    const isFlex = /flex|grid/.test(cs.display);
    const out = { el, cs, isFlex, gaps: null, pads: {}, margs: {}, text: null, lints: [] };
    if (isFlex) out.gaps = { "row-gap": parseFloat(cs.rowGap) || 0, "column-gap": parseFloat(cs.columnGap) || 0 };
    PADS.forEach(p => out.pads[p] = parseFloat(cs.getPropertyValue(p)) || 0);
    MARGS.forEach(p => out.margs[p] = parseFloat(cs.getPropertyValue(p)) || 0);
    if (hasOwnText(el)) out.text = { size: parseFloat(cs.fontSize), line: parseFloat(cs.lineHeight), weight: +cs.fontWeight, style: textStyleFor(cs) };
    const vals = Object.assign({}, out.gaps || {}, out.pads);
    for (const [p, v] of Object.entries(vals)) {
      if (v === 0) continue;
      const t = tokenFor(v);
      if (t.kind === "off") out.lints.push({ prop: p, level: "defect", msg: `${p} is ${v}px, not a fraction of the body line (u = ${T.unit}). Nearest token ${nearestToken(v).name} at ${nearestToken(v).px}px.`, fix: { prop: p, token: nearestToken(v) } });
      else if (t.kind === "fraction") out.lints.push({ prop: p, level: "note", msg: `${p} is ${v}px, a clean fraction of u but no token carries it.` });
    }
    if (out.gaps) {
      const kids = [...el.children];
      const column = cs.display.includes("grid") || cs.flexDirection.startsWith("column");
      const g = column ? out.gaps["row-gap"] : out.gaps["column-gap"];
      const hasButton = kids.some(k => k.matches("button, a[role=button], [class*=btn], [class*=button]"));
      if (column && hasButton && g > 0 && g < T.unit) out.lints.push({ prop: "row-gap", level: "defect", msg: `A button is an action, not a continuation of the text above it. Gap to a button is ${g}px, under 1 u (${T.unit}px).`, fix: { prop: "row-gap", token: T.ladder.find(t => t.px === T.unit) } });
      const reading = kids.filter(k => k.matches("p, h1, h2, h3, h4, h5, h6")).length >= 2;
      if (column && reading && [8, 12, 16].some(v => Math.abs(g - v) < 0.5)) out.lints.push({ prop: "row-gap", level: "note", msg: `${g}px is a middle rung between reading-flow items. In the reading flow he uses 1/6 u (bound) and 1 u (separate) only; middle rungs live inside components.` });
    }
    return out;
  }
  // A field: label on the left, value on the right. Drag across the label to
  // step through the ladder; click the value for the list. Only tokens are offered.
  function steps() { return [{ px: 0, name: "0" }].concat(T.ladder); }
  function fieldRow(label, prop, px) {
    const t = tokenFor(px);
    const cls = t.kind === "off" ? "off" : t.kind === "fraction" ? "frac" : "";
    const open = menuFor === prop;
    const menu = open ? `<div class="menu">${steps().map(k => `<button class="mi ${Math.abs(k.px - px) < 0.5 ? "cur" : ""}" data-prop="${prop}" data-px="${k.px}" data-tok="${h(k.name)}"><span>${k.px}</span><span>${h(k.name)}</span></button>`).join("")}</div>` : "";
    return `<div class="field ${open ? "open" : ""}" data-field="${prop}"><span class="flab" data-drag="${prop}" title="Drag to step through the ladder">${h(label)}</span><button class="fval ${cls}" data-menu="${prop}" data-px="${px}" title="Choose a token">${px}px<small>${h(t.kind === "token" ? t.name : t.kind === "zero" ? "" : t.name)}</small></button>${menu}</div>`;
  }
  function textFieldRow(info) {
    const names = Object.keys(T.text); const open = menuFor === "text-style";
    const menu = open ? `<div class="menu">${names.map(n => { const st = T.text[n]; return `<button class="mi ${n === info.text.style ? "cur" : ""}" data-text="${h(n)}"><span>${st.size}/${st.line} ${st.weight}</span><span>${h(n)}</span></button>`; }).join("")}</div>` : "";
    return `<div class="field ${open ? "open" : ""}" data-field="text-style"><span class="flab" data-drag="text-style" title="Drag to step through the ramp">Style</span><button class="fval ${info.text.style ? "" : "off"}" data-menu="text-style">${info.text.size}/${info.text.line} ${info.text.weight}<small>${h(info.text.style || "off ramp")}</small></button>${menu}</div>`;
  }

  let exporting = false, sent = "", confirming = null, menuFor = null, drag = null;
  let mode = "dock"; try { mode = localStorage.getItem("toolkit-overlay:mode") || "dock"; } catch (e) {}
  const DOCK_W = 344, POP_W = 320, GUT = 16; let marginOpen = false;
  function render() {
    const prevBody = panel.querySelector(".body"); const scrollAt = prevBody ? prevBody.scrollTop : 0;
    const info = selected && selected.isConnected ? inspect(selected) : null;
    const prevPop = pop.scrollTop;
    let body = "", fields = "";
    body += `<div class="sec"><h3>Selected</h3>${info ? `<div class="id"><div class="name">${info.el === document.body ? "body" : h(identity(info.el).component || identity(info.el).tag)}</div><div class="path">${h(pathOf(info.el))}</div>${identity(info.el).text ? `<div class="txt">${h(identity(info.el).text)}</div>` : ""}</div>` : `<div class="empty">Click anything on the page. Escape clears the selection.</div>`}${info && !records.length ? `<div class="note">Drag a field's label to step through the ladder. Click its value to choose.</div>` : ""}</div>`;
    if (info) {
      if (info.lints.length) fields += `<div class="sec"><h3>Judgment</h3>${info.lints.map((l, i) => `<div class="lint ${l.level}"><span>${h(l.msg)}</span>${l.fix && l.fix.token ? `<button class="btn fix" data-lint="${i}">Set ${h(l.fix.prop)} to ${h(l.fix.token.name)}</button>` : ""}</div>`).join("")}</div>`;
      if (info.gaps) fields += `<div class="sec"><h3>Gap</h3><div class="fields">${fieldRow("Row", "row-gap", info.gaps["row-gap"])}${fieldRow("Column", "column-gap", info.gaps["column-gap"])}</div></div>`;
      fields += `<div class="sec"><h3>Padding</h3><div class="fields">${PADS.map(p => fieldRow(p.replace("padding-", "").replace(/^./, c => c.toUpperCase()), p, info.pads[p])).join("")}</div></div>`;
      const marginFields = `<div class="fields">${MARGS.map(p => fieldRow(p.replace("margin-", "").replace(/^./, c => c.toUpperCase()), p, info.margs[p])).join("")}</div><div class="note">The air belongs to the component, as padding. Reach for margin only when the space is not the component's own.</div>`;
      fields += mode === "beside" ? `<div class="sec"><details ${marginOpen ? "open" : ""}><summary>Margin</summary>${marginFields}</details></div>` : `<div class="sec"><h3>Margin</h3>${marginFields}</div>`;
      if (info.text) fields += `<div class="sec"><h3>Text</h3><div class="fields">${textFieldRow(info)}</div><div class="note">Ramp ${h(T.textSource)}.</div></div>`;
    }
    let beside = false;
    if (mode === "beside" && info) {
      pop.hidden = false;
      pop.innerHTML = `<div class="sec"><div class="id"><div class="name">${h(identity(info.el).component || identity(info.el).tag)}</div><div class="path">${h(pathOf(info.el).split(" > ").slice(-2).join(" > "))}</div></div></div>${fields}`;
      beside = placePop();
      if (!beside) pop.hidden = true; else pop.scrollTop = prevPop;
    } else pop.hidden = true;
    if (!beside) body += fields;
    // changes, each with its tier
    const net = netRecords();
    let applyable = 0;
    const chgs = net.map(r => {
      const t = tierOf(r); if (t.pending) locate(r);
      if (t.tier === 1) applyable++;
      const isConf = confirming === r.id;
      let action = "";
      if (r.busy) action = `<span>working</span>`;
      else if (t.tier === 1) action = `<button class="btn" data-apply="${r.id}">Apply to source</button>`;
      else if (t.tier === 2) action = isConf ? `<span><button class="btn on" data-apply="${r.id}" data-confirmed="1">Yes, all ${r.decl.matches}</button> <button class="btn" data-cancel="1">No, prompt</button></span>` : `<button class="btn" data-confirm="${r.id}">Apply to all ${r.decl.matches}</button>`;
      const diff = r.applied && r.applied.before ? `<div class="diff"><span class="m">- ${h(r.applied.before.trim())}</span>\n<span class="p">+ ${h(r.applied.after.trim())}</span></div>` : "";
      return `<div class="chg"><div class="what"><span><b>${h(r.prop)}</b> ${h(r.fromToken)} to ${h(r.toToken)}</span><span>${h(r.identity.component || r.identity.tag)}</span></div><div class="who">${h(r.identity.path)}</div><div class="tier t${t.tier}${r.verified === false ? " bad" : ""}"><span>${h(t.label)}</span>${action}</div>${diff}</div>`;
    }).join("");
    body += `<div class="sec"><h3>Changes</h3>${net.length ? chgs : `<div class="empty">${records.length ? "Everything is back where it started. Nothing to export." : "Nothing yet. A change you reverse drops out. Each change shows where in the source it lands, or that it needs the session."}</div>`}${sent ? `<div class="note">Sent to <b>${h(sent)}</b>. The session applies what is left, mirrors, and records.</div>` : ""}${exporting ? `<textarea readonly>${h(buildPrompt())}</textarea><div style="display:flex;gap:8px">${ENDPOINT ? `<button class="btn on" data-act="send">Send to session</button>` : ""}<button class="btn" data-act="copy">Copy prompt</button><button class="btn" data-act="closex">Close</button></div>` : ""}</div>`;
    panel.innerHTML = `<div class="head"><b>Overlay</b><span class="seg"><button class="btn ${picking ? "on" : ""}" data-act="pick" title="Alt+Shift+N switches">Select</button><button class="btn ${picking ? "" : "on"}" data-act="nav" title="Clicks reach the page, so you can move between screens">Navigate</button></span><button class="btn" data-act="mode" title="Where the fields appear">${mode === "beside" ? "Beside" : "Dock"}</button><button class="btn" data-act="hide">Hide</button><small>u = ${T.unit}px, ${T.ladder.length} tokens, ${h(T.spaceSource)}${ENDPOINT ? ", connected" : ""}</small>${T.unitNote ? `<small class="warnnote">${h(T.unitNote)}</small>` : ""}</div><div class="body">${body}</div>
      <div class="foot"><span class="cnt">${net.length} net change${net.length === 1 ? "" : "s"}${records.length !== net.length ? `, ${records.length} made` : ""}</span><button class="btn" data-act="undo" ${undoStack.length ? "" : "disabled"}>Undo</button><button class="btn" data-act="clear" ${records.length ? "" : "disabled"} title="Forget every change here. Applied edits stay in the source.">Clear</button>${applyable > 1 ? `<button class="btn" data-act="applyall">Apply ${applyable}</button>` : ""}<button class="btn on" data-act="export" ${net.length ? "" : "disabled"}>Export</button></div>`;
    panel.querySelector(".body").scrollTop = scrollAt;
    place(selBox, selected); if (selected) selBox.querySelector(".tag").textContent = identity(selected).component || pathOf(selected).split(" > ").pop();
  }

  // drag across a label: each 14px of travel is one rung; the record is written on release
  const onPointerDown = ev => {
    const lab = ev.target.closest("[data-drag]"); if (!lab || !selected || ev.button !== 0) return;
    const prop = lab.dataset.drag; menuFor = null;
    let list, idx, startPx;
    if (prop === "text-style") { list = Object.keys(T.text); const i = inspect(selected); if (!i.text) return; idx = Math.max(0, list.indexOf(i.text.style)); startPx = i.text; }
    else { list = steps(); startPx = parseFloat(getComputedStyle(selected).getPropertyValue(prop)) || 0; idx = list.findIndex(k => Math.abs(k.px - startPx) < 0.5); if (idx < 0) idx = list.findIndex(k => k.px > startPx); if (idx < 0) idx = list.length - 1; }
    drag = { prop, list, idx0: idx, idx, x0: ev.clientX, startPx, moved: false, el: selected, lab };
    lab.setPointerCapture(ev.pointerId); ev.preventDefault();
  };
  const onPointerMove = ev => {
    if (!drag) return;
    const dx = ev.clientX - drag.x0; if (Math.abs(dx) > 3) drag.moved = true;
    const idx = Math.max(0, Math.min(drag.list.length - 1, drag.idx0 + Math.round(dx / 14)));
    if (idx === drag.idx) return; drag.idx = idx;
    const val = root.querySelector(`.field[data-field="${drag.prop}"] .fval`);
    if (drag.prop === "text-style") { const st = T.text[drag.list[idx]]; drag.el.style.setProperty("font-size", st.size + "px", "important"); drag.el.style.setProperty("line-height", st.line + "px", "important"); drag.el.style.setProperty("font-weight", st.weight, "important"); if (val) val.innerHTML = `${st.size}/${st.line} ${st.weight}<small>${h(drag.list[idx])}</small>`; }
    else { const k = drag.list[idx]; drag.el.style.setProperty(drag.prop, k.px + "px", "important"); if (val) { val.className = "fval"; val.innerHTML = `${k.px}px<small>${h(k.px ? k.name : "")}</small>`; } }
    place(selBox, selected);
  };
  const endDrag = ev => {
    if (!drag) return; const d = drag; drag = null;
    if (!d.moved) { menuFor = d.prop; render(); return; }
    if (d.prop === "text-style") { const name = d.list[d.idx]; if (name !== d.startPx.style) { d.el.style.removeProperty("font-size"); d.el.style.removeProperty("line-height"); d.el.style.removeProperty("font-weight"); applyText(d.el, name, d.startPx); } else render(); return; }
    const k = d.list[d.idx];
    if (Math.abs(k.px - d.startPx) < 0.5) { d.el.style.removeProperty(d.prop); render(); return; }
    d.el.style.removeProperty(d.prop); applyChange(d.el, d.prop, k.px, k.name, d.startPx);
  };
  const onSurfaceClick = ev => {
    const b = ev.target.closest("button");
    if (menuFor && !(b && (b.dataset.menu || b.classList.contains("mi")))) { menuFor = null; render(); }
    if (!b) return;
    const act = b.dataset.act;
    if (b.dataset.menu) { menuFor = menuFor === b.dataset.menu ? null : b.dataset.menu; render(); return; }
    if (b.classList.contains("mi")) { menuFor = null; if (b.dataset.text) { const i = inspect(selected); if (i.text && i.text.style !== b.dataset.text) applyText(selected, b.dataset.text, i.text); else render(); return; } }
    if (act === "pick") { picking = true; render(); return; }
    if (act === "nav") { picking = false; hoverBox.hidden = true; render(); return; }
    if (act === "mode") { mode = mode === "beside" ? "dock" : "beside"; try { localStorage.setItem("toolkit-overlay:mode", mode); } catch (e) {} render(); return; }
    if (act === "hide") { api.toggle(); return; }
    if (act === "undo") { undo(); return; }
    if (act === "clear") { while (undoStack.length) undo(); records.length = 0; persist(); sent = ""; render(); return; }
    if (act === "export") { exporting = true; sent = ""; render(); return; }
    if (act === "closex") { exporting = false; render(); return; }
    if (act === "applyall") { netRecords().filter(r => tierOf(r).tier === 1).forEach(r => applyToSource(r)); return; }
    if (act === "copy") { navigator.clipboard.writeText(buildPrompt()).then(() => { b.textContent = "Copied"; setTimeout(() => (b.textContent = "Copy prompt"), 1200); }); return; }
    if (act === "send") {
      b.disabled = true; b.textContent = "Sending";
      const payload = { prompt: buildPrompt(), records: netRecords().map(r => Object.assign({}, r, { el: undefined, last: undefined, decl: undefined, loc: undefined })), page: location.href, width: innerWidth };
      fetch(ENDPOINT + "/export", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
        .then(r => r.json()).then(j => { sent = j.file || "sent"; exporting = false; render(); })
        .catch(() => { b.disabled = false; b.textContent = "Send failed, copy instead"; });
      return;
    }
    if (b.dataset.confirm) { confirming = b.dataset.confirm; render(); return; }
    if (b.dataset.cancel) { confirming = null; render(); return; }
    if (b.dataset.apply) { const r = netRecords().find(x => x.id === b.dataset.apply); confirming = null; if (r) applyToSource(r); return; }
    if (!selected) return;
    if (b.dataset.lint != null) { const l = inspect(selected).lints[+b.dataset.lint]; if (l && l.fix && l.fix.token) { const cur = parseFloat(getComputedStyle(selected).getPropertyValue(l.fix.prop)) || 0; applyChange(selected, l.fix.prop, l.fix.token.px, l.fix.token.name, cur); } return; }
    if (b.dataset.prop) { const cur = parseFloat(getComputedStyle(selected).getPropertyValue(b.dataset.prop)) || 0; if (Math.abs(cur - +b.dataset.px) < 0.5) return; applyChange(selected, b.dataset.prop, +b.dataset.px, b.dataset.tok, cur); return; }
    if (b.dataset.text) { const i = inspect(selected); if (i.text && i.text.style !== b.dataset.text) applyText(selected, b.dataset.text, i.text); }
  };
  pop.addEventListener("toggle", ev => { if (ev.target.tagName === "DETAILS") marginOpen = ev.target.open; }, true);
  for (const surface of [panel, pop]) {
    surface.addEventListener("pointerdown", onPointerDown); surface.addEventListener("pointermove", onPointerMove);
    surface.addEventListener("pointerup", endDrag); surface.addEventListener("pointercancel", endDrag);
    surface.addEventListener("click", onSurfaceClick);
  }

  function targetFrom(ev) { const t = ev.target; if (t === host || host.contains(t) || ev.composedPath().includes(host)) return null; const el = ev.composedPath()[0]; if (!(el instanceof Element)) return null; return el; }
  function onMove(ev) { if (!picking || !visible) return; const el = targetFrom(ev); if (!el) { hoverEl = null; hoverBox.hidden = true; return; } if (el === hoverEl || el === selected) { if (el === selected) hoverBox.hidden = true; return; } hoverEl = el; place(hoverBox, el); }
  function onClick(ev) { if (!picking || !visible) return; const el = targetFrom(ev); if (!el) return; ev.preventDefault(); ev.stopPropagation(); selected = el; exporting = false; render(); }
  function onKey(ev) { if (ev.altKey && ev.shiftKey && ev.code === "KeyD") { ev.preventDefault(); api.toggle(); } else if (ev.altKey && ev.shiftKey && ev.code === "KeyN") { ev.preventDefault(); picking = !picking; hoverBox.hidden = true; render(); } else if (ev.key === "Escape" && visible) { if (menuFor) menuFor = null; else selected = null; render(); } }
  function onScroll() { place(selBox, selected); if (hoverEl) place(hoverBox, hoverEl); if (!pop.hidden && !placePop()) render(); }
  document.addEventListener("mousemove", onMove, true);
  document.addEventListener("click", onClick, true);
  document.addEventListener("keydown", onKey, true);
  addEventListener("scroll", onScroll, true); addEventListener("resize", onScroll);

  let visible = true;
  const api = { toggle() { visible = !visible; host.style.display = visible ? "" : "none"; if (visible) render(); }, records, net: netRecords, tokens: () => T, prompt: buildPrompt, resolve: resolveDecl, apply: applyToSource };
  window.__toolkitOverlay = api;
  render();
  if (CANDIDATE) {
    fetch(CANDIDATE + "/tokens.json").then(r => { if (!r.headers.get("x-toolkit-overlay-server")) throw 0; return r.json(); }).then(m => {
      ENDPOINT = CANDIDATE;
      if (!window.__designTokens && m && m.space && Object.keys(m.space).length) { window.__designTokens = m; T = discoverTokens(); T.spaceSource = "contract"; T.textSource = "contract"; }
      render();
    }).catch(() => {});
  }
})();
