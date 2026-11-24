/* ONE Portal — everything on screen is derived from window.ONE_DATA, which the build reads from the repository. */
"use strict";
const D = window.ONE_DATA;
const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const toDate = (s) => { if (!s) return null; if (/^\d{4}-\d{2}/.test(s)) return new Date(s.slice(0, 10) + "T00:00:00"); const m = s.match(/^(\d{1,2}) (\w+) (\d{4})$/); return m ? new Date(+m[3], MON.indexOf(m[2]), +m[1]) : null; };
const fmt = (d) => d ? `${d.getDate()} ${MON[d.getMonth()].slice(0, 3)} ${d.getFullYear()}` : "";
const fmtM = (d) => `${MON[d.getMonth()]} ${d.getFullYear()}`;
const nameOf = (p) => (p || "").split(" — ")[0].trim();
const TODAY = new Date(2026, 10, 24);
const REG = D.registers;
const EL = Object.fromEntries(D.protocol.elements.map((e) => [e.id, e]));
const EXP = D.protocol.expectations;
const EXPBY = Object.fromEntries(EXP.map((e) => [e.id, e]));
const ECOL = { 1: "#0B4F5E", 2: "#0F6B7A", 3: "#1E8796", 4: "#3AA3AE", 5: "#D9480F", 6: "#F26B21", 7: "#F5923E", 8: "#F8B26A", 9: "#3D5A80", 10: "#5C7BA6" };
const GROUP = (n) => (n <= 4 ? "Lead" : n <= 8 ? "Control" : "Learn");
const BIND = new Set(["req", "resp", "appr", "rec", "ctl"]);
const KNAME = { req: "Requirement", resp: "Responsibility", appr: "Approval", rec: "Record", ctl: "Control", warn: "Warning", note: "Note", kpi: "KPI", step: "Step", ref: "Reference", ext: "External standard", def: "Definition" };
const LAYER = (t) => ({ Manual: "Policy", Policy: "Policy", Standard: "Standard", Specification: "Standard", Practice: "Practice", Process: "Process", Procedure: "Procedure", Plan: "Procedure",
  "Work Instruction": "Task & record", Form: "Task & record", Register: "Task & record" }[t] || "Other");
const LAYERS = ["Policy", "Standard", "Practice", "Process", "Procedure", "Task & record"];
const TYPE_LAYER = { MAN: "Policy", POL: "Policy", STD: "Standard", SPC: "Standard", PRA: "Practice", PRS: "Process", PRC: "Procedure", PLN: "Procedure", WIN: "Task & record", FRM: "Task & record", REG: "Task & record" };

// ---------- indexes ----------
const DOCS = D.docs.map((d) => ({ ...d, eff: toDate(d.effective), layer: LAYER(d.type) }));
const DOC = Object.fromEntries(DOCS.map((d) => [d.id, d]));
const STMTS = []; const SEC = {};
for (const d of DOCS) for (const s of d.sections) {
  SEC[`${d.id}#${s.bm}`] = { d, s };
  for (const b of s.blocks) if (BIND.has(b.k)) STMTS.push({ d, s, b, tags: s.tags });
}
const PEOPLE = D.people; const PBY = Object.fromEntries(PEOPLE.map((p) => [p.n, p])); const PID = Object.fromEntries(PEOPLE.map((p) => [p.id, p]));
const CTL = Object.fromEntries(REG["RSK-REG-002"].map((c) => [c.control_id, c]));
const RISK = Object.fromEntries(REG["RSK-REG-001"].map((r) => [r.risk_id, r]));
const EVENTS = REG["INC-REG-001_events"];
const docLink = (id, bm, label) => DOC[id] ? `<a href="#/doc/${id}${bm ? "/" + bm : ""}">${esc(label || id)}</a>` : `<span class="muted" title="Not yet issued">${esc(label || id)}</span>`;
const ctlChip = (c) => { const x = CTL[c]; return `<a class="chip" href="#/control/${c}">${x ? `<span class="dot h-${(x.health || "").replace(" ", "")}"></span>` : ""}${esc(c)}</a>`; };
const tagChips = (tags, link = true) => (tags || []).map((t, i) => link ? `<a class="tag${i === 0 ? " primary" : ""}" href="#/exp/${t}" data-tip="${esc(t + " " + (EXPBY[t]?.title || ""))}">${esc(t)}</a>` : `<span class="tag">${esc(t)}</span>`).join("");
const kindChip = (k) => `<span class="kind k-${k}">${KNAME[k] || k}</span>`;
const rateChip = (r) => `<span class="rate r-${(r || "").replace(" ", "")}">${esc(r)}</span>`;
const gateChip = (id) => { const g = D.gate[id]; return g ? `<span class="gate g-${g.outcome}">${g.outcome === "PASS_AFTER_FIX" ? "Pass after fix" : g.outcome === "PASS" ? "Pass" : "Fail"}</span>` : ""; };

function coverage(at) {
  const m = new Map(EXP.map((e) => [e.id, { n: 0, docs: new Set(), primary: 0 }]));
  for (const x of STMTS) {
    if (at && (!x.d.eff || x.d.eff > at)) continue;
    if (x.d.typeCode === "MAN") continue;   // the Manual states expectations; coverage counts documents that deliver them
    x.tags.forEach((t, i) => { const c = m.get(t); if (c) { c.n++; c.docs.add(x.d.id); if (i === 0) c.primary++; } });
  }
  return m;
}

// ---------- navigation ----------
const NAV = [
  ["#/", "OMS wheel"], ["#/explore", "Requirements", STMTS.length], ["#/gaps", "Gaps"], ["#/risk", "Risks", REG["RSK-REG-001"].length],
  ["#/controls", "Controls", REG["RSK-REG-002"].length], ["#/authority", "Technical authority"], ["#/library", "Library", DOCS.length],
  ["#/process", "Processes"], ["#/performance", "Performance"],
];
$("#nav").innerHTML = NAV.map(([h, l, c]) => `<li><a href="${h}">${l}${c ? `<span class="count">${c}</span>` : ""}</a></li>`).join("");
$("#built").textContent = `Built ${fmt(new Date(D.built))} from ${DOCS.length} documents and ${Object.keys(REG).length} registers in the repository.`;

const ROUTES = [];
const route = (re, fn) => ROUTES.push([re, fn]);
function go() {
  const h = decodeURIComponent(location.hash.slice(1) || "/");
  for (const a of $("#nav").querySelectorAll("a")) a.toggleAttribute("aria-current", a.getAttribute("href") === "#" + (h === "/" ? "/" : "/" + h.split("/")[1]));
  for (const a of $("#nav").querySelectorAll("a[aria-current]")) a.setAttribute("aria-current", "page");
  for (const [re, fn] of ROUTES) { const m = h.match(re); if (m) { stopAll(); $("#main").innerHTML = ""; fn(...m.slice(1)); $("#main").focus({ preventScroll: true }); if (!/^\/doc\/[^/]+\/./.test(h)) window.scrollTo(0, 0); return; } }
  $("#main").innerHTML = `<div class="panel"><h2>Page not found</h2><p><a href="#/">Go to the OMS wheel</a></p></div>`;
}
window.addEventListener("hashchange", go);
const timers = []; const stopAll = () => { while (timers.length) clearInterval(timers.pop()); };
const head = (title, sub, crumb, right = "") => `<div class="page-head"><div>${crumb ? `<div class="crumb">${crumb}</div>` : ""}<h1>${title}</h1>${sub ? `<p>${sub}</p>` : ""}</div>${right}</div>`;

// tooltip
const tip = $("#tip");
document.addEventListener("mousemove", (e) => {
  const t = e.target.closest("[data-tip]");
  if (!t) { tip.hidden = true; return; }
  tip.innerHTML = t.getAttribute("data-tip"); tip.hidden = false;
  const x = Math.min(e.clientX + 14, innerWidth - 310); tip.style.left = x + "px"; tip.style.top = (e.clientY + 16) + "px";
});

// ---------- the wheel ----------
function arc(cx, cy, r0, r1, a0, a1) {
  const p = (r, a) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  const large = a1 - a0 > Math.PI ? 1 : 0;
  const [x0, y0] = p(r1, a0), [x1, y1] = p(r1, a1), [x2, y2] = p(r0, a1), [x3, y3] = p(r0, a0);
  return `M${x0},${y0} A${r1},${r1} 0 ${large} 1 ${x1},${y1} L${x2},${y2} A${r0},${r0} 0 ${large} 0 ${x3},${y3} Z`;
}
function wheelSVG() {
  const cx = 300, cy = 300, step = (2 * Math.PI) / EXP.length; let a = -Math.PI / 2;
  let segs = "", cells = "", labels = "", groups = "";
  const gStart = {};
  for (const e of D.protocol.elements) {
    const ex = EXP.filter((x) => x.element === e.id), a0 = a, a1 = a + ex.length * step;
    if (!gStart[GROUP(e.id)]) gStart[GROUP(e.id)] = a0; gStart[GROUP(e.id) + "_end"] = a1;
    segs += `<path class="seg" d="${arc(cx, cy, 92, 168, a0 + 0.004, a1 - 0.004)}" fill="${ECOL[e.id]}" data-el="${e.id}" data-tip="<b>Element ${e.id}</b>${esc(e.title)}"/>`;
    const am = (a0 + a1) / 2; labels += `<text class="seg-label" x="${cx + 130 * Math.cos(am)}" y="${cy + 130 * Math.sin(am) + 5}" text-anchor="middle">${e.id}</text>`;
    ex.forEach((x, i) => {
      const b0 = a + i * step, b1 = b0 + step, bm = (b0 + b1) / 2, deg = bm * 180 / Math.PI, flip = Math.cos(bm) < 0;
      cells += `<path class="cell" d="${arc(cx, cy, 172, 262, b0, b1)}" fill="${ECOL[e.id]}" fill-opacity="0.1" data-exp="${x.id}"/>`;
      labels += `<text class="exp-label" data-lab="${x.id}" transform="translate(${cx + 217 * Math.cos(bm)},${cy + 217 * Math.sin(bm)}) rotate(${flip ? deg + 180 : deg})" text-anchor="middle" dy="3.5">${x.id}</text>`;
    });
    a = a1;
  }
  for (const [g, r] of [["Lead", 0], ["Control", 0], ["Learn", 0]]) {
    const a0 = gStart[g], a1 = gStart[g + "_end"], am = (a0 + a1) / 2;
    groups += `<path d="${arc(cx, cy, 268, 271, a0 + 0.01, a1 - 0.01)}" fill="#B9C5CA"/><text class="group" x="${cx + 286 * Math.cos(am)}" y="${cy + 286 * Math.sin(am) + 4}" text-anchor="middle">${g}</text>`;
  }
  return `<svg class="wheel" viewBox="-10 -10 620 620" role="img" aria-label="OMS wheel: 10 elements and 54 expectations, coloured by how many binding statements in issued documents serve each expectation">
    <g class="grow">${groups}${segs}${cells}${labels}
    <circle cx="300" cy="300" r="86" fill="#fff" stroke="#D5DDE0"/>
    <text class="hub-a num" x="300" y="300" text-anchor="middle" id="hubA">0</text>
    <text class="hub-b" x="300" y="322" text-anchor="middle">binding statements</text><text class="hub-b" x="300" y="339" text-anchor="middle">in force</text></g></svg>`;
}
function paintWheel(svg, at, prev) {
  const cov = coverage(at); const max = Math.max(...[...cov.values()].map((c) => c.n), 1);
  let total = 0;
  for (const p of svg.querySelectorAll(".cell")) {
    const c = cov.get(p.dataset.exp); const v = c.n; total += 0;
    const op = v ? 0.28 + 0.72 * Math.sqrt(v / max) : 0.08;
    p.setAttribute("fill-opacity", op.toFixed(2));
    p.setAttribute("data-tip", `<b>${p.dataset.exp} ${esc(EXPBY[p.dataset.exp].title)}</b>${v} binding statements in ${c.docs.size} document${c.docs.size === 1 ? "" : "s"}`);
    const lab = svg.querySelector(`[data-lab="${p.dataset.exp}"]`); lab.setAttribute("fill", op > 0.55 ? "#fff" : "#17262E");
    if (prev && prev.get(p.dataset.exp).n !== v) { p.classList.remove("pulse"); void p.getBBox(); p.classList.add("pulse"); }
  }
  const n = STMTS.filter((x) => x.d.typeCode !== "MAN" && x.d.eff && x.d.eff <= at).length;
  svg.querySelector("#hubA").textContent = n.toLocaleString();
  return cov;
}

route(/^\/$/, () => {
  const months = []; for (let d = new Date(2025, 11, 1); d <= TODAY; d = new Date(d.getFullYear(), d.getMonth() + 1, 1)) months.push(new Date(d.getFullYear(), d.getMonth() + 1, 0));
  months[months.length - 1] = TODAY;
  const covNow = coverage(TODAY); const covered = [...covNow.values()].filter((c) => c.n).length;
  const ctlCount = REG["RSK-REG-002"].filter((c) => c.status === "Active").length;
  $("#main").innerHTML = head("One Management System", "Every expectation of the OMS, shaded by how much of it is written into issued ACE documents. Drag the timeline or press play to watch the system come to life as documents take effect.") + `
  <div class="home">
    <div class="wheel-wrap">${wheelSVG()}
      <div class="timeline"><button class="btn primary" id="play">Play</button><input id="slider" type="range" min="0" max="${months.length - 1}" value="${months.length - 1}" aria-label="Date"><span class="date-read" id="dread"></span></div>
      <div class="legend"><span><i style="background:#0B4F5E"></i>Lead (elements 1–4)</span><span><i style="background:#D9480F"></i>Control (5–8)</span><span><i style="background:#3D5A80"></i>Learn (9–10)</span><span><i style="background:#E8ECEE"></i>Paler cell = fewer binding statements</span></div>
    </div>
    <div class="stack">
      <div class="figures"><div><b class="num" id="fDocs">${DOCS.length}</b><span>documents in force</span></div><div><b class="num">${covered}<small style="font-size:15px;color:var(--ink-3)">/54</small></b><span>expectations covered</span></div><div><b class="num">${ctlCount}</b><span>controls with IDs</span></div></div>
      <div class="panel"><h2>Issued so far</h2><ul class="issued" id="issued"></ul></div>
      <div class="panel" id="pick"><h2>Elements</h2>${D.protocol.elements.map((e) => {
        const ex = EXP.filter((x) => x.element === e.id); const c = ex.filter((x) => covNow.get(x.id).n).length;
        return `<div style="display:grid;grid-template-columns:14px 1fr 90px 40px;gap:10px;align-items:center;padding:4px 0"><i style="width:12px;height:12px;border-radius:2px;background:${ECOL[e.id]}"></i><a href="#/el/${e.id}">${e.id}. ${esc(e.title)}</a><span class="bar"><i style="width:${100 * c / ex.length}%;background:${ECOL[e.id]}"></i></span><span class="small muted num">${c}/${ex.length}</span></div>`; }).join("")}</div>
    </div>
  </div>`;
  const svg = $(".wheel"), slider = $("#slider"); let prev = null, shown = new Set();
  const show = (i, animate) => {
    const at = months[i]; $("#dread").textContent = i === months.length - 1 ? "Today" : fmtM(at);
    prev = paintWheel(svg, at, animate ? prev : null);
    const list = DOCS.filter((d) => d.eff && d.eff <= at).sort((a, b) => b.eff - a.eff || a.id.localeCompare(b.id));
    $("#fDocs").textContent = list.length;
    $("#issued").innerHTML = list.map((d) => `<li class="${animate && !shown.has(d.id) ? "new" : ""}"><time>${fmt(d.eff)}</time><span>${docLink(d.id, "", d.id)} ${esc(d.title)}</span></li>`).join("") || `<li><time></time><span class="muted">No ONE documents in force yet. The system launched on 1 January 2026.</span></li>`;
    shown = new Set(list.map((d) => d.id));
  };
  show(months.length - 1, false);
  slider.oninput = () => show(+slider.value, true);
  svg.addEventListener("click", (e) => { const c = e.target.closest("[data-exp]"); if (c) location.hash = `#/exp/${c.dataset.exp}`; const s = e.target.closest("[data-el]"); if (s) location.hash = `#/el/${s.dataset.el}`; });
  $("#play").onclick = () => {
    stopAll(); let i = 0; slider.value = 0; show(0, true);
    timers.push(setInterval(() => { i++; if (i >= months.length) { stopAll(); return; } slider.value = i; show(i, true); }, 950));
  };
});

// ---------- element and expectation ----------
route(/^\/el\/(\d+)$/, (n) => {
  const e = EL[n]; if (!e) return go404();
  const cov = coverage(TODAY); const ex = EXP.filter((x) => x.element === +n);
  const docs = new Map(); for (const x of STMTS) if (x.d.typeCode !== "MAN" && x.tags.some((t) => EXPBY[t]?.element === +n)) docs.set(x.d.id, (docs.get(x.d.id) || 0) + 1);
  const owner = PEOPLE.find((p) => p.t === e.owner || p.t.startsWith(e.owner));
  $("#main").innerHTML = head(`<span style="display:inline-block;width:16px;height:16px;border-radius:3px;background:${ECOL[n]};margin-right:10px"></span>Element ${n}. ${esc(e.title)}`,
    `${GROUP(+n)} group. Element owner: ${owner ? esc(owner.n + " — " + owner.t) : esc(e.owner)}.`, `<a href="#/">OMS wheel</a>`) + `
  <div class="grid2"><div class="panel"><h2>Expectations</h2><table class="t"><tr><th>Expectation</th><th class="n">Statements</th><th class="n">Documents</th><th>Coverage</th></tr>
    ${ex.map((x) => { const c = cov.get(x.id); return `<tr><td><a href="#/exp/${x.id}">${x.id} ${esc(x.title)}</a></td><td class="n">${c.n}</td><td class="n">${c.docs.size}</td><td><span class="bar"><i style="width:${Math.min(100, c.n * 4)}%;background:${ECOL[n]}"></i></span></td></tr>`; }).join("")}</table></div>
  <div class="panel"><h2>Documents that serve this element</h2><table class="t"><tr><th>Document</th><th class="n">Statements</th></tr>
    ${[...docs].sort((a, b) => b[1] - a[1]).map(([id, c]) => `<tr><td>${docLink(id)} ${esc(DOC[id].title)}</td><td class="n">${c}</td></tr>`).join("") || `<tr><td colspan="2" class="muted">No issued document carries this element's tags yet.</td></tr>`}</table></div></div>`;
});
function go404() { $("#main").innerHTML = `<div class="panel"><h2>Not found</h2><p><a href="#/">Go to the OMS wheel</a></p></div>`; }

route(/^\/exp\/(\d+\.\d+)$/, (id) => {
  const x = EXPBY[id]; if (!x) return go404();
  const man = DOC["ACE-OMS-MAN-001"]; const ms = man?.sections.find((s) => s.title.replace(/\s+/g, " ").startsWith(id + " "));
  const st = STMTS.filter((s) => s.d.typeCode !== "MAN" && s.tags.includes(id));
  const byDoc = new Map(); for (const s of st) { if (!byDoc.has(s.d.id)) byDoc.set(s.d.id, []); byDoc.get(s.d.id).push(s); }
  const ctl = [...new Set(st.flatMap((s) => s.b.c || []))];
  const risks = [...new Set(ctl.map((c) => CTL[c]?.risk_id).filter(Boolean))];
  const layers = new Set(st.map((s) => s.d.layer));
  const gap = !st.length ? "No issued document carries a binding statement for this expectation yet." : st.length < 3 ? "Thin coverage: fewer than three binding statements." : "";
  $("#main").innerHTML = head(`${id} ${esc(x.title)}`, "", `<a href="#/">OMS wheel</a> / <a href="#/el/${x.element}">Element ${x.element}. ${esc(EL[x.element].title)}</a>`) + `
  ${gap ? `<div class="panel" style="border-left:4px solid var(--flare);margin-bottom:18px"><b>Gap.</b> ${gap} <a href="#/gaps">See all gaps</a></div>` : ""}
  <div class="grid2" style="align-items:start">
    <div class="panel"><h2>What the OMS Manual expects</h2>${ms ? ms.blocks.slice(0, 8).map(blockHTML).join("") + `<p class="small">${docLink("ACE-OMS-MAN-001", ms.bm, "Read in the Manual")}</p>` : `<p class="muted">The Manual section was not found.</p>`}</div>
    <div class="stack"><div class="figures"><div><b>${st.length}</b><span>binding statements</span></div><div><b>${byDoc.size}</b><span>documents</span></div><div><b>${ctl.length}</b><span>controls</span></div></div>
      <div class="panel"><h3>Layers that deliver it</h3><div class="pill-row">${LAYERS.map((l) => `<span class="chip" style="${layers.has(l) ? "border-color:var(--teal);color:var(--teal)" : "border-style:dashed;color:var(--ink-3)"}">${l}</span>`).join("")}</div>
      ${ctl.length ? `<h3 style="margin-top:14px">Controls</h3>${ctl.map(ctlChip).join("")}` : ""}
      ${risks.length ? `<h3 style="margin-top:14px">Risks these controls address</h3>${risks.map((r) => `<a class="chip" href="#/risk/${r}">${r} ${esc(RISK[r].title.slice(0, 48))}</a>`).join("")}` : ""}</div></div>
  </div>
  <div class="panel" style="margin-top:18px"><h2>Binding statements tagged ${id}</h2>${[...byDoc].map(([doc, list]) => `<h3 style="margin-top:14px">${docLink(doc)} ${esc(DOC[doc].title)}</h3>${list.map(stmtHTML).join("")}`).join("") || `<p class="muted">None yet.</p>`}</div>`;
});
function stmtHTML(s) {
  return `<div class="stmt k-${s.b.k}"><p>${esc(s.b.t)}</p><div class="src">${kindChip(s.b.k)} ${docLink(s.d.id, s.s.bm, `${s.d.id} · ${s.s.title}`)} ${tagChips(s.tags)} ${(s.b.c || []).map(ctlChip).join("")}</div></div>`;
}
function blockHTML(b) {
  if (b.k === "table") return `<table>${b.rows.map((r) => `<tr>${r.map((c) => `<td>${linkRefs(esc(c))}</td>`).join("")}</tr>`).join("")}</table>`;
  let t = linkRefs(esc(b.t));
  for (const c of b.c || []) t = t.replace(new RegExp(`\\(?${c}\\)?`), ` ${ctlChip(c)}`);
  return `<div class="blk k-${b.k}">${BIND.has(b.k) ? kindChip(b.k) + " " : ""}${t}</div>`;
}
const linkRefs = (h) => h.replace(/(?<![A-Za-z0-9-])(ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?)/g, (m) => DOC[m] ? `<a href="#/doc/${m}">${m}</a>` : `<span title="Planned document" style="border-bottom:1px dashed var(--ink-3)">${m}</span>`);

// ---------- explorer ----------
route(/^\/explore(?:\/(.*))?$/, (q) => {
  const opt = (v, l) => `<option value="${esc(v)}">${esc(l)}</option>`;
  const fns = [...new Set(DOCS.map((d) => d.func).filter(Boolean))].sort();
  $("#main").innerHTML = head("Requirements explorer", "Every binding statement in every issued document. Filter by OMS element, system, function, document layer or kind of statement.") + `
  <div class="filters">
    <label>Element<select id="fe">${opt("", "All")}${D.protocol.elements.map((e) => opt(e.id, `${e.id}. ${e.title}`)).join("")}</select></label>
    <label>System<select id="fs">${opt("", "All")}${[...new Set(DOCS.map((d) => d.system))].sort().map((s) => opt(s, `${s} ${D.protocol.systems[s]?.name || ""}`)).join("")}</select></label>
    <label>Function<select id="ff">${opt("", "All")}${fns.map((f) => opt(f, f)).join("")}</select></label>
    <label>Layer<select id="fl">${opt("", "All")}${LAYERS.map((l) => opt(l, l)).join("")}</select></label>
    <label>Kind<select id="fk">${opt("", "All")}${[...BIND].map((k) => opt(k, KNAME[k])).join("")}</select></label>
    <label>Contains<input id="ft" type="search" placeholder="e.g. Area Authority"></label>
  </div><p class="muted small" id="cnt"></p><div id="res"></div>`;
  const run = () => {
    const e = $("#fe").value, s = $("#fs").value, f = $("#ff").value, l = $("#fl").value, k = $("#fk").value, t = $("#ft").value.toLowerCase();
    const r = STMTS.filter((x) => x.d.typeCode !== "MAN" && (!e || x.tags.some((g) => EXPBY[g]?.element === +e)) && (!s || x.d.system === s) && (!f || x.d.func === f) && (!l || x.d.layer === l) && (!k || x.b.k === k) && (!t || x.b.t.toLowerCase().includes(t)));
    $("#cnt").textContent = `${r.length} statements${r.length > 200 ? " (showing the first 200)" : ""}`;
    $("#res").innerHTML = r.slice(0, 200).map(stmtHTML).join("");
  };
  for (const id of ["fe", "fs", "ff", "fl", "fk", "ft"]) $("#" + id).oninput = run;
  if (q) $("#ft").value = q;
  run();
});

// ---------- gaps ----------
route(/^\/gaps$/, () => {
  const cov = coverage(TODAY);
  const docReg = REG["DOC-REG-001"]; const planned = docReg.filter((d) => d.status === "Planned");
  const sysRows = Object.keys(D.protocol.systems);
  const cell = (sys, layer) => {
    const iss = DOCS.filter((d) => d.system === sys && d.layer === layer).length;
    const pl = planned.filter((d) => d.system === sys && TYPE_LAYER[d.doc_id.split("-")[2]] === layer).length;
    if (iss) return `<td class="m${Math.min(3, iss)}" data-tip="${iss} issued${pl ? `, ${pl} planned` : ""}">${iss}${pl ? `<small> +${pl}</small>` : ""}</td>`;
    if (pl) return `<td class="mp" data-tip="${pl} planned, none issued">${pl}</td>`;
    return `<td class="m0" data-tip="Nothing issued or planned">–</td>`;
  };
  const noCtl = REG["RSK-REG-001"].filter((r) => !r.controls.split("; ").some((c) => CTL[c]?.status === "Active"));
  const plannedCtl = REG["RSK-REG-002"].filter((c) => c.status === "Planned");
  const noStep = REG["RSK-REG-002"].filter((c) => c.status === "Active" && !c.process_step);
  const refs = new Map(); for (const d of DOCS) for (const s of d.sections) for (const b of s.blocks) for (const r of b.r || []) if (!DOC[r]) refs.set(r, (refs.get(r) || new Set()).add(d.id));
  const pend = docReg.filter((d) => d.pending_revision);
  const thin = EXP.filter((x) => cov.get(x.id).n < 3);
  $("#main").innerHTML = head("Gaps", "Where the written system does not yet reach. Everything here is worked out from the documents and registers, so it shrinks as documents are issued.") + `
  <div class="figures" style="margin-bottom:18px"><div><b>${thin.length}</b><span>expectations with fewer than 3 binding statements</span></div><div><b>${planned.length}</b><span>planned documents not yet issued</span></div><div><b>${noCtl.length}</b><span>risks with no documented control</span></div><div><b>${noStep.length}</b><span>controls not yet tied to a process step</span></div></div>
  <div class="panel" style="margin-bottom:18px"><h2>Systems against document layers</h2><p class="muted small">Number of issued documents (with planned in small type). Hatched cells: planned only. Dashed: nothing yet.</p>
    <div style="overflow:auto"><table class="matrix"><tr><th></th>${LAYERS.map((l) => `<th>${l}</th>`).join("")}</tr>
    ${sysRows.map((s) => `<tr><th data-tip="${esc(D.protocol.systems[s].name)}">${s} <span class="muted" style="font-weight:400">${esc(D.protocol.systems[s].name)}</span></th>${LAYERS.map((l) => cell(s, l)).join("")}</tr>`).join("")}</table></div></div>
  <div class="grid2">
    <div class="panel"><h2>Thinly covered expectations</h2><div class="scroll"><table class="t"><tr><th>Expectation</th><th class="n">Statements</th><th class="n">Docs</th></tr>
      ${thin.sort((a, b) => cov.get(a.id).n - cov.get(b.id).n).map((x) => `<tr><td><a href="#/exp/${x.id}">${x.id} ${esc(x.title)}</a></td><td class="n">${cov.get(x.id).n}</td><td class="n">${cov.get(x.id).docs.size}</td></tr>`).join("")}</table></div></div>
    <div class="panel"><h2>Risks with no documented control</h2><p class="muted small">The risk relies on documents that have no Control IDs yet, or on a document not yet written.</p><div class="scroll"><table class="t"><tr><th>Risk</th><th>Rating</th><th>Relies on</th></tr>
      ${noCtl.map((r) => `<tr><td><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)}</td><td>${rateChip(r.current_rating)}</td><td class="small">${r.legacy_control_docs ? docLink(r.legacy_control_docs) : r.controls ? r.controls.split("; ").map((c) => esc(CTL[c]?.doc_ref || c)).join("<br>") : "<span class='muted'>Nothing written</span>"}</td></tr>`).join("")}</table></div></div>
    <div class="panel"><h2>Planned controls</h2><table class="t"><tr><th>Control</th><th>Waiting for</th></tr>${plannedCtl.map((c) => `<tr><td>${ctlChip(c.control_id)} ${esc(c.statement)}</td><td class="small">${esc(c.doc_ref)}</td></tr>`).join("")}</table></div>
    <div class="panel"><h2>Revisions in progress</h2><table class="t"><tr><th>Document</th><th>Revision</th><th>Change</th><th>Target</th></tr>${pend.map((d) => `<tr><td>${docLink(d.doc_id)} ${esc(d.title)}</td><td>${esc(d.pending_revision)}</td><td><a href="#/process">${esc(d.pending_moc)}</a></td><td>${fmt(toDate(d.target_issue))}</td></tr>`).join("")}</table></div>
    <div class="panel"><h2>References to documents not yet issued</h2><div class="scroll"><table class="t"><tr><th>Referenced</th><th>Status</th><th>Referenced by</th></tr>
      ${[...refs].sort().map(([r, by]) => { const p = docReg.find((d) => d.doc_id === r); return `<tr><td>${esc(r)}<div class="small muted">${esc(p?.title || "")}</div></td><td class="small">${p ? "Planned " + fmt(toDate(p.target_issue)) : "<b>Not in any register</b>"}</td><td class="small">${[...by].map((d) => docLink(d)).join(", ")}</td></tr>`; }).join("")}</table></div></div>
    <div class="panel"><h2>Documents waiting for automatic fix</h2><p class="muted small">They pass the protocol after the ONE Fix tool runs. Older Rev 01 documents also carry warnings until their next revision.</p><table class="t"><tr><th>Document</th><th>What Fix will correct</th></tr>
      ${Object.entries(D.gate).filter(([, g]) => g.outcome === "PASS_AFTER_FIX").map(([id, g]) => `<tr><td>${docLink(id)}</td><td class="small">${g.findings.filter((f) => f.sev === "error").map((f) => esc(f.msg)).join("<br>")}</td></tr>`).join("")}</table></div>
  </div>`;
});

// ---------- risks ----------
const LS = "EDCBA";
route(/^\/risk$/, () => {
  const risks = REG["RSK-REG-001"]; const H = REG["RSK-REG-001_history"];
  const dates = [...new Set(H.map((h) => h.date))].sort(); const COLOR = { L: "var(--low)", M: "var(--med)", H: "var(--high)", V: "var(--vhigh)" };
  const MAT = { E: "MHHVV", D: "MMHHV", C: "LMMHH", B: "LLMMH", A: "LLLMM" };
  const state = (d) => { const s = {}; for (const h of H) if (h.date <= d) s[h.risk_id] = h; return s; };
  $("#main").innerHTML = head("Risks", "The ACE Risk Matrix from the Risk Management Standard, with every risk in the register. Press play to see risks move as events happen and controls are restored.") + `
  <div class="grid2" style="grid-template-columns:minmax(0,1.1fr) minmax(0,1fr)">
    <div class="panel"><div class="heat" id="heat">${LS.split("").map((l, i) => `<div class="ax">${({ E: "E Expected", D: "D Likely", C: "C Possible", B: "B Unlikely", A: "A Rare" })[l]}</div>${[1, 2, 3, 4, 5].map((c) => `<div class="c" style="background:${COLOR[MAT[l][c - 1]]};opacity:.55"></div>`).join("")}`).join("")}
      <div></div>${["1 Minor", "2 Moderate", "3 Serious", "4 Major", "5 Catastrophic"].map((c) => `<div class="ax x">${c}</div>`).join("")}<div class="rdots" id="rdots"></div></div>
      <div class="timeline"><button class="btn primary" id="play">Play</button><input id="slider" type="range" min="0" max="${dates.length}" value="${dates.length}" aria-label="Date"><span class="date-read" id="dread">Today</span></div>
      <p class="small muted" style="margin-top:8px">Likelihood up the side, consequence along the bottom. Each circle is a risk; select one to see its controls.</p></div>
    <div class="panel"><h2>Register</h2><div class="scroll"><table class="t"><tr><th>Risk</th><th>Site</th><th>Now</th><th>After actions</th></tr>
      ${[...risks].sort((a, b) => "VHML".indexOf(a.current_rating[0]) - "VHML".indexOf(b.current_rating[0]) || a.risk_id.localeCompare(b.risk_id)).map((r) => `<tr data-r="${r.risk_id}"><td><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)}</td><td>${r.site}</td><td>${rateChip(r.current_rating)}</td><td>${rateChip(r.residual_rating)}</td></tr>`).join("")}</table></div></div>
  </div>`;
  const box = $("#rdots"), heat = $("#heat");
  box.innerHTML = risks.map((r) => `<a class="rdot" href="#/risk/${r.risk_id}" id="d-${r.risk_id}" data-tip="<b>${r.risk_id}</b>${esc(r.title)}">${r.risk_id.split("-")[2]}</a>`).join("");
  const place = (st) => {
    const W = heat.clientWidth, x0 = 113, cw = (W - x0) / 5, ch = 77;
    const pos = risks.map((r) => { const s = st[r.risk_id] || { likelihood: r.current_l, consequence: r.current_c }; return { r, k: s.likelihood + s.consequence, col: +s.consequence - 1, row: LS.indexOf(s.likelihood) }; });
    const n = {}; for (const p of pos) n[p.k] = (n[p.k] || 0) + 1; const seen = {};
    for (const p of pos) {
      const cnt = n[p.k], cols = Math.max(1, Math.ceil(Math.sqrt(cnt * (cw / ch)))), rows = Math.ceil(cnt / cols);
      const size = Math.min(24, (cw - 8) / cols, (ch - 8) / rows); const i = (seen[p.k] = (seen[p.k] || 0) + 1) - 1;
      const el = $("#d-" + p.r.risk_id); const d = Math.max(14, size - 3);
      el.style.width = el.style.height = d + "px"; el.style.margin = `${-d / 2}px 0 0 ${-d / 2}px`; el.style.fontSize = (d < 18 ? 8 : 9.5) + "px";
      el.style.left = (x0 + p.col * cw + 4 + size / 2 + (i % cols) * size) + "px"; el.style.top = (p.row * ch + 4 + size / 2 + Math.floor(i / cols) * size) + "px";
      el.classList.toggle("focus", p.r.risk_id === "R-PAP-01");
    }
  };
  const slider = $("#slider");
  const show = (i) => { const d = i >= dates.length ? "9999" : dates[i]; $("#dread").textContent = i >= dates.length ? "Today" : fmt(toDate(d)); place(state(d)); };
  show(dates.length); slider.oninput = () => show(+slider.value);
  window.addEventListener("resize", () => show(+slider.value), { once: true });
  $("#play").onclick = () => { stopAll(); let i = 0; slider.value = 0; show(0); timers.push(setInterval(() => { i++; if (i > dates.length) return stopAll(); slider.value = i; show(i); }, 1100)); };
});

route(/^\/risk\/(R-[A-Z]{3}-\d+)$/, (id) => {
  const r = RISK[id]; if (!r) return go404();
  const ctl = r.controls.split("; ").filter(Boolean).map((c) => CTL[c]).filter(Boolean);
  const pre = ctl.filter((c) => c.position === "Preventive"), mit = ctl.filter((c) => c.position !== "Preventive");
  const bar = (c) => `<div class="barrier ${c.status === "Planned" ? "planned" : ""}"><span class="dot h-${c.health.replace(" ", "")}" style="margin-top:6px"></span><div><a href="#/control/${c.control_id}">${c.control_id}</a> ${esc(c.statement)}<div class="small muted">${c.status === "Planned" ? "Planned — " + esc(c.doc_ref) : esc(c.health) + " · " + esc(nameOf(c.owner))}</div></div></div>`;
  const ev = EVENTS.filter((e) => e.risk_ids.split("; ").includes(id)).sort((a, b) => b.date.localeCompare(a.date));
  const hist = REG["RSK-REG-001_history"].filter((h) => h.risk_id === id);
  $("#main").innerHTML = head(`${id} ${esc(r.title)}`, `${esc(r.level)} risk at ${esc(D.protocol.sites[r.site] || r.site)}. Owner ${esc(r.owner)}. ${r.restrictions ? "Restriction: " + esc(r.restrictions) + "." : ""}`, `<a href="#/risk">Risks</a>`,
    `<div style="text-align:right"><div>Now ${rateChip(r.current_rating)} <span class="small muted">${r.current_l}${r.current_c}</span></div><div style="margin-top:4px">After actions ${rateChip(r.residual_rating)} <span class="small muted">${r.residual_l}${r.residual_c}</span></div></div>`) + `
  <div class="panel" style="margin-bottom:18px"><div class="bowtie">
    <div class="side"><h3>Threats</h3>${r.threats.split(";").map((t) => `<div class="small" style="margin-bottom:4px">${esc(t.trim())}</div>`).join("")}<h3 style="margin-top:12px">Preventive controls</h3>${pre.map(bar).join("") || `<p class="muted small">None with Control IDs.</p>`}</div>
    <div class="knot">${esc(r.top_event)}<div class="small muted" style="font-weight:400;margin-top:6px">${esc(r.hazard)}</div></div>
    <div class="side"><h3>Consequences</h3>${r.consequences.split(";").map((t) => `<div class="small" style="margin-bottom:4px">${esc(t.trim())}</div>`).join("")}<h3 style="margin-top:12px">Mitigating controls</h3>${mit.map(bar).join("") || `<p class="muted small">None with Control IDs.</p>`}</div>
  </div>${r.legacy_control_docs ? `<p class="small" style="margin-top:12px">Controls are also written in ${docLink(r.legacy_control_docs)}, which has no Control IDs yet.</p>` : ""}</div>
  <div class="grid2"><div class="panel"><h2>Consequence by domain</h2><table class="t"><tr><th>People</th><th>Environment</th><th>Asset and production</th><th>Reputation</th></tr><tr><td class="n">${r.c_people}</td><td class="n">${r.c_environment}</td><td class="n">${r.c_asset}</td><td class="n">${r.c_reputation}</td></tr></table>
    <h3 style="margin-top:14px">Rating history</h3><ul class="events">${hist.map((h) => `<li><span class="muted">${fmt(toDate(h.date))}</span><span>${rateChip(h.rating)} ${h.likelihood}${h.consequence} ${esc(h.reason)}</span></li>`).join("")}</ul>
    <p class="small muted" style="margin-top:10px">Accepted by ${esc(r.acceptance_authority)}${r.expiry ? `, expires ${fmt(toDate(r.expiry))}` : ""}. Reviewed ${esc(r.review_frequency.toLowerCase())}; last ${fmt(toDate(r.last_review))}. Objective ${esc(r.objective_id)}.</p></div>
    <div class="panel"><h2>Events</h2><ul class="events">${ev.slice(0, 25).map((e) => `<li><span class="muted">${fmt(toDate(e.date))}</span><span>${esc(e.title)} <span class="small muted">${esc(e.type)}</span>${e.controls_failed ? `<div class="small">Failed: ${e.controls_failed.split("; ").map(ctlChip).join("")}</div>` : ""}${e.controls_tested ? `<div class="small">Worked: ${e.controls_tested.split("; ").map(ctlChip).join("")}</div>` : ""}</span></li>`).join("") || `<li><span></span><span class="muted">No events recorded against this risk.</span></li>`}</ul></div></div>`;
});

// ---------- controls ----------
route(/^\/controls$/, () => {
  const all = REG["RSK-REG-002"];
  const cnt = (h) => all.filter((c) => c.health === h).length;
  $("#main").innerHTML = head("Controls", "Each control is written in a document as a RiskControl statement with a Control ID. Health comes from tests, samples and events.") + `
  <div class="figures" style="margin-bottom:18px">${["Effective", "Degraded", "Failed", "Not tested"].map((h) => `<div><b><span class="dot h-${h.replace(" ", "")}"></span>${cnt(h)}</b><span>${h}</span></div>`).join("")}</div>
  <div class="filters"><label>Health<select id="fh"><option value="">All</option>${["Effective", "Degraded", "Failed", "Not tested"].map((h) => `<option>${h}</option>`).join("")}</select></label>
    <label>System<select id="fs"><option value="">All</option>${[...new Set(all.map((c) => c.control_id.split("-")[1]))].sort().map((s) => `<option>${s}</option>`).join("")}</select></label>
    <label>Status<select id="fst"><option value="">All</option><option>Active</option><option>Planned</option></select></label></div>
  <div class="panel"><table class="t" id="ct"></table></div>`;
  const run = () => { const h = $("#fh").value, s = $("#fs").value, st = $("#fst").value;
    $("#ct").innerHTML = `<tr><th>Control</th><th>Statement</th><th>Risk</th><th>Written in</th><th>Owner</th></tr>` + all.filter((c) => (!h || c.health === h) && (!s || c.control_id.split("-")[1] === s) && (!st || c.status === st)).map((c) => {
      const [doc, bm] = c.doc_ref.split("#"); return `<tr><td>${ctlChip(c.control_id)}</td><td>${esc(c.statement)}</td><td><a href="#/risk/${c.risk_id}">${c.risk_id}</a></td><td class="small">${c.status === "Planned" ? esc(c.doc_ref) : docLink(doc, bm)}</td><td class="small">${esc(nameOf(c.owner))}</td></tr>`; }).join(""); };
  for (const id of ["fh", "fs", "fst"]) $("#" + id).oninput = run; run();
});
route(/^\/control\/(C-[A-Z]{3}-\d{3})$/, (id) => {
  const c = CTL[id]; if (!c) return go404();
  const [doc, bm] = c.doc_ref.split("#"); const sec = SEC[`${doc}#${bm}`];
  const para = sec?.s.blocks.find((b) => (b.c || []).includes(id));
  const hist = REG["RSK-REG-002_health"].filter((h) => h.control_id === id);
  const ev = EVENTS.filter((e) => (e.controls_failed + "; " + e.controls_tested).split("; ").includes(id));
  $("#main").innerHTML = head(`<span class="dot h-${c.health.replace(" ", "")}" style="width:14px;height:14px"></span>${id}`, esc(c.statement), `<a href="#/controls">Controls</a>`) + `
  <div class="grid2"><div class="panel"><h2>Where it is written</h2>${para ? `<div class="blk k-ctl">${esc(para.t)}</div><p class="small">${docLink(doc, bm, `${doc} · ${sec.s.title}`)}</p>` : `<p class="muted">${esc(c.doc_ref)}</p>`}
    <table class="t" style="margin-top:10px"><tr><td>Risk</td><td><a href="#/risk/${c.risk_id}">${c.risk_id}</a> ${esc(RISK[c.risk_id]?.title || "")}</td></tr><tr><td>Type</td><td>${esc(c.position)}, ${esc(c.nature.toLowerCase())}${c.critical === "Yes" ? ", critical" : ""}</td></tr>
    <tr><td>Owner</td><td>${esc(c.owner)}</td></tr><tr><td>Evidence</td><td>${esc(c.evidence)}</td></tr><tr><td>Process step</td><td>${c.process_step ? `<a href="#/process">${esc(c.process_step)}</a>` : `<span class="muted">Not yet modelled${c.process_planned ? " (expected in " + esc(c.process_planned) + ")" : ""}</span>`}</td></tr>
    ${c.barrier ? `<tr><td>Barrier</td><td>${esc(c.barrier)}</td></tr>` : ""}${c.sce_id ? `<tr><td>Safety-critical element</td><td>${esc(c.sce_id)}</td></tr>` : ""}</table></div>
  <div class="panel"><h2>Health over time</h2><ul class="events">${hist.map((h) => `<li><span class="muted">${fmt(toDate(h.date))}</span><span><span class="dot h-${h.health.replace(" ", "")}"></span>${esc(h.health)} <span class="small muted">${esc(h.note)}</span></span></li>`).join("") || `<li><span></span><span class="muted">Not yet in force.</span></li>`}</ul>
    ${ev.length ? `<h3 style="margin-top:14px">Events</h3><ul class="events">${ev.map((e) => `<li><span class="muted">${fmt(toDate(e.date))}</span><span>${esc(e.title)}</span></li>`).join("")}</ul>` : ""}</div></div>`;
});

// ---------- technical authority ----------
route(/^\/authority(?:\/(.+))?$/, (who) => {
  const vp = PEOPLE.find((p) => p.t === "VP Engineering & Projects");
  const leads = PEOPLE.filter((p) => p.dl === vp.id && p.disc);
  const fns = [...new Set(leads.map((p) => p.f))];
  const FC = ["#0E5A6B", "#D9480F", "#3D5A80", "#4E9F6A", "#8A5A9E", "#B07D18", "#5B6B73"];
  const cx = 360, cy = 330; let svg = "", i = 0;
  const N = leads.length; const sorted = fns.flatMap((f) => leads.filter((p) => p.f === f));
  sorted.forEach((p, k) => {
    const a = -Math.PI / 2 + (k / N) * 2 * Math.PI, R = 245, x = cx + R * Math.cos(a), y = cy + R * Math.sin(a), col = FC[fns.indexOf(p.f) % FC.length];
    const right = Math.cos(a) >= 0, lx = cx + (R + 16) * Math.cos(a), ly = cy + (R + 16) * Math.sin(a);
    svg += `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}"/><g class="node" data-n="${esc(p.n)}" data-tip="<b>${esc(p.n)}</b>${esc(p.t)}<br>${esc(p.f)}"><circle cx="${x}" cy="${y}" r="9" fill="${col}"/><text x="${lx}" y="${ly + 4}" text-anchor="${right ? "start" : "end"}">${esc(p.t.replace(/ Lead$/, ""))}</text></g>`;
  });
  svg += `<circle cx="${cx}" cy="${cy}" r="70" fill="#fff" stroke="#17262E" stroke-width="1.5"/><text class="fn" x="${cx}" y="${cy - 8}" text-anchor="middle">Technical Leadership</text><text class="fn" x="${cx}" y="${cy + 10}" text-anchor="middle">Council</text><text x="${cx}" y="${cy + 30}" text-anchor="middle">Chair: ${esc(vp.n)}</text>`;
  $("#main").innerHTML = head("Technical authority", `The ${N} discipline leads keep their line in their own function and hold a dotted line to the VP Engineering &amp; Projects through the Technical Leadership Council. Select a lead to see the documents, controls and risks they hold.`) + `
  <div class="grid2" style="grid-template-columns:minmax(0,1.15fr) minmax(0,1fr)"><div class="panel"><svg class="tlc" viewBox="-110 0 940 660">${svg}</svg>
    <div class="legend">${fns.map((f, k) => `<span><i style="background:${FC[k % FC.length]};border-radius:50%"></i>${esc(f)}</span>`).join("")}</div></div>
    <div class="panel" id="who"><h2>Select a discipline lead</h2><p class="muted">Each lead is the Technical Authority for their discipline: they own its standards, endorse changes and approve technical deviations.</p></div></div>`;
  const showP = (n) => {
    const p = PBY[n]; if (!p) return; for (const g of document.querySelectorAll(".tlc .node")) g.classList.toggle("on", g.dataset.n === n);
    const roles = []; for (const d of DOCS) for (const [k, l] of [["author", "Author"], ["owner", "Owner"], ["approver", "Approver"], ["custodian", "Custodian"], ["reviewers", "Reviewer"], ["endorser", "Endorser"]]) if ((d[k] || "").includes(n)) roles.push([d, l]);
    const ctls = REG["RSK-REG-002"].filter((c) => c.owner.startsWith(n)); const risks = REG["RSK-REG-001"].filter((r) => r.owner.startsWith(n));
    const title = p.t.replace(/ \(.*\)$/, "");
    const mentions = STMTS.filter((s) => s.b.t.includes(title) || s.b.t.includes(n)).slice(0, 12);
    const mgr = PID[p.to];
    $("#who").innerHTML = `<h2>${esc(p.n)}</h2><p>${esc(p.t)}<br><span class="muted small">${esc(p.f)}, reports to ${esc(mgr ? mgr.n + " — " + mgr.t : "")}</span></p>
      <h3 style="margin-top:12px">Documents</h3>${roles.length ? `<table class="t">${roles.map(([d, l]) => `<tr><td>${docLink(d.id)} ${esc(d.title)}</td><td class="small muted">${l}</td></tr>`).join("")}</table>` : `<p class="muted small">Not named on any issued document yet.</p>`}
      ${ctls.length ? `<h3 style="margin-top:12px">Controls owned</h3>${ctls.map((c) => ctlChip(c.control_id)).join("")}` : ""}
      ${risks.length ? `<h3 style="margin-top:12px">Risks owned</h3>${risks.map((r) => `<a class="chip" href="#/risk/${r.risk_id}">${r.risk_id}</a>`).join("")}` : ""}
      ${mentions.length ? `<h3 style="margin-top:12px">Named in binding statements</h3>${mentions.map(stmtHTML).join("")}` : ""}`;
  };
  $(".tlc").addEventListener("click", (e) => { const g = e.target.closest(".node"); if (g) showP(g.dataset.n); });
  if (who) showP(who);
});

// ---------- library and reader ----------
route(/^\/library$/, () => {
  const reg = REG["DOC-REG-001"];
  $("#main").innerHTML = head("Library", "Issued documents read directly from the repository, and the planned documents still to come.") + `
  <div class="filters"><label>Layer<select id="fl"><option value="">All</option>${LAYERS.map((l) => `<option>${l}</option>`).join("")}</select></label>
  <label>System<select id="fs"><option value="">All</option>${Object.keys(D.protocol.systems).map((s) => `<option value="${s}">${s} ${esc(D.protocol.systems[s].name)}</option>`).join("")}</select></label>
  <label>Show<select id="fx"><option value="">Issued and planned</option><option value="i">Issued only</option><option value="p">Planned only</option></select></label></div>
  <div class="panel"><table class="t" id="lt"></table></div>`;
  const run = () => { const l = $("#fl").value, s = $("#fs").value, x = $("#fx").value;
    const issued = x === "p" ? [] : DOCS.filter((d) => (!l || d.layer === l) && (!s || d.system === s));
    const planned = x === "i" ? [] : reg.filter((d) => d.status === "Planned" && (!l || TYPE_LAYER[d.doc_id.split("-")[2]] === l) && (!s || d.system === s));
    $("#lt").innerHTML = `<tr><th>Number</th><th>Title</th><th>Layer</th><th>Rev</th><th>Effective</th><th>Owner</th><th>Gateway</th></tr>` +
      issued.sort((a, b) => a.id.localeCompare(b.id)).map((d) => `<tr><td>${docLink(d.id)}</td><td>${esc(d.title)}</td><td>${d.layer}</td><td>${esc(d.revision)}</td><td class="num">${fmt(d.eff)}</td><td class="small">${esc(nameOf(d.owner))}</td><td>${gateChip(d.id)}</td></tr>`).join("") +
      planned.map((d) => `<tr style="color:var(--ink-3)"><td>${esc(d.doc_id)}</td><td>${esc(d.title)}</td><td>${TYPE_LAYER[d.doc_id.split("-")[2]] || ""}</td><td></td><td class="small">Planned ${fmt(toDate(d.target_issue))}</td><td class="small">${esc(nameOf(d.owner))}</td><td></td></tr>`).join(""); };
  for (const id of ["fl", "fs", "fx"]) $("#" + id).oninput = run; run();
});
route(/^\/doc\/([A-Z0-9-]+)(?:\/(.+))?$/, (id, bm) => {
  const d = DOC[id]; if (!d) return go404();
  const reg = REG["DOC-REG-001"].find((x) => x.doc_id === id) || {}; const g = D.gate[id];
  const parent = (d.parent.match(/ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?/) || [])[0];
  const children = DOCS.filter((x) => x.parent.includes(id));
  $("#main").innerHTML = `<div class="crumb"><a href="#/library">Library</a> / ${esc(d.layer)}</div>
  <div class="titleblock"><div><h1 style="font-size:24px">${esc(d.title)}</h1><p class="muted" style="margin:6px 0 10px">${esc(d.subtitle)}</p>
    <dl><dt>Number</dt><dd>${esc(d.id)}</dd><dt>Revision</dt><dd>${esc(d.revision)} ${esc(d.status)}</dd><dt>Effective</dt><dd>${fmt(d.eff)}</dd><dt>Next review</dt><dd>${fmt(toDate(reg.next_review))}</dd>
    <dt>Owner</dt><dd>${esc(nameOf(d.owner))}</dd><dt>Author</dt><dd>${esc(nameOf(d.author))}</dd><dt>Parent</dt><dd>${parent ? docLink(parent) : "—"}</dd><dt>Function</dt><dd>${esc(d.func)}</dd></dl>
    ${reg.pending_revision ? `<p class="small" style="margin:10px 0 0;color:var(--flare)">Revision ${esc(reg.pending_revision)} in preparation under ${esc(reg.pending_moc)}, target ${fmt(toDate(reg.target_issue))}.</p>` : ""}</div>
    <div style="text-align:right">${tagChips(d.tags)}<div style="margin-top:8px">${gateChip(id)}</div><div class="small muted" style="margin-top:6px">${g ? `${g.errors} errors, ${g.warnings} warnings` : ""}</div>${children.length ? `<div class="small" style="margin-top:8px">Child documents:<br>${children.map((c) => docLink(c.id)).join("<br>")}</div>` : ""}</div></div>
  <div class="reader"><nav class="toc panel" aria-label="Sections">${d.sections.map((s) => `<a class="l${s.level}" href="#/doc/${id}/${s.bm}">${esc(s.title)}</a>`).join("")}</nav>
    <article class="doc-body">${d.sections.map((s) => `<section id="${esc(s.bm)}">${s.level === 1 ? `<h2>${esc(s.title)}</h2>` : `<h3>${esc(s.title)}</h3>`}<div class="tags">${tagChips(s.tags)}</div>${s.blocks.map(blockHTML).join("")}</section>`).join("")}
    ${d.revisions.length ? `<section><h2>Revision history</h2><table>${d.revisions.map((r) => `<tr><td>${esc(r.rev)}</td><td>${esc(r.date)}</td><td>${esc(r.text)}</td></tr>`).join("")}</table></section>` : ""}
    ${g && g.findings.length ? `<section><h2>Gateway findings</h2>${g.findings.map((f) => `<div class="blk small"><b>${f.rule}</b> ${esc(f.sev)}${f.fix === "auto" ? " (automatic fix)" : ""}: ${esc(f.msg)}</div>`).join("")}</section>` : ""}</article></div>`;
  if (bm) { const t = document.getElementById(bm); if (t) { t.scrollIntoView({ block: "start" }); t.classList.add("hl"); } }
});

// ---------- processes ----------
route(/^\/process$/, () => {
  const reg = REG["BPM-REG-001"]; const model = D.processes[0]; const steps = REG["MOC-REG-001_steps"]; const mocs = REG["MOC-REG-001"];
  const med = {}; for (const s of steps) if (s.left) { (med[s.step] ||= []).push((toDate(s.left) - toDate(s.entered)) / 864e5); }
  const median = (a) => { if (!a || !a.length) return 0; a = [...a].sort((x, y) => x - y); return a[Math.floor(a.length / 2)]; };
  // layout: columns by longest path from start
  const S = Object.fromEntries(model.steps.map((s) => [s.id, s])); const col = {}; const q = model.steps.filter((s) => s.type === "start").map((s) => [s.id, 0]);
  while (q.length) { const [k, c] = q.shift(); if (col[k] >= c) continue; col[k] = c; for (const n of [...(S[k].next || []), ...(S[k].branches || []).map((b) => b.to)]) q.push([n, c + 1]); }
  for (const s of model.steps.sort((a, b) => col[a.id] - col[b.id])) while (model.steps.some((o) => o !== s && o.lane === s.lane && col[o.id] === col[s.id] && model.steps.indexOf(o) < model.steps.indexOf(s))) col[s.id]++;
  const lanes = model.lanes; const LH = 86, CW = 122, X0 = 140, W = X0 + (Math.max(...Object.values(col)) + 1) * CW + 20;
  const pos = (id) => ({ x: X0 + col[id] * CW + 8, y: lanes.findIndex((l) => l.id === S[id].lane) * LH + 20 });
  let g = `<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7D8D95"/></marker></defs>`;
  lanes.forEach((l, i) => { g += `<rect class="lane-bg" x="0" y="${i * LH}" width="${W}" height="${LH}"/><text class="lane-name" x="10" y="${i * LH + LH / 2 + 4}">${esc(l.role)}</text>`; });
  for (const s of model.steps) for (const n of [...(s.next || []), ...(s.branches || []).map((b) => b.to)]) {
    const a = pos(s.id), b = pos(n), hand = S[n].lane !== s.lane;
    g += `<path class="flow${hand ? " handoff" : ""}" d="M${a.x + 100},${a.y + 22} C${a.x + 112},${a.y + 22} ${b.x - 12},${b.y + 22} ${b.x},${b.y + 22}"/>`;
  }
  for (const s of model.steps) {
    const p = pos(s.id); const m = median(med[s.id]);
    const shape = s.type === "xor" ? `<path d="M${p.x + 50},${p.y} L${p.x + 100},${p.y + 22} L${p.x + 50},${p.y + 44} L${p.x},${p.y + 22} Z" fill="#fff" stroke="#17262E" stroke-width="1.4"/>`
      : s.type === "start" || s.type === "end" ? `<rect x="${p.x + 2}" y="${p.y + 2}" width="96" height="40" rx="20" fill="#fff" stroke="#17262E" stroke-width="${s.type === "end" ? 3 : 1.4}"/>`
      : `<rect x="${p.x}" y="${p.y}" width="100" height="44" rx="6"/>`;
    g += `<g class="task" data-tip="<b>${s.id} ${esc(s.name)}</b>${(s.doc_refs || []).map((r) => esc(r)).join("<br>")}${m ? `<br>Median ${m.toFixed(0)} days in the MOC register` : ""}">${shape}${(() => { const w = s.name.split(" "); let a = "", b = ""; for (const x of w) ((a + " " + x).trim().length <= 15 && !b ? (a = (a + " " + x).trim()) : (b = (b + " " + x).trim())); return s.type === "xor" ? `<text x="${p.x + 50}" y="${p.y + 26}" text-anchor="middle" font-size="10.5">${esc(s.name.length > 16 ? s.name.slice(0, 15) + "…" : s.name)}</text><text x="${p.x + 50}" y="${p.y - 4}" text-anchor="middle" font-size="10" fill="#7D8D95">${s.id}</text>` : `<text x="${p.x + 50}" y="${p.y + (b ? 19 : 26)}" text-anchor="middle">${esc(a)}</text>${b ? `<text x="${p.x + 50}" y="${p.y + 32}" text-anchor="middle">${esc(b.length > 16 ? b.slice(0, 15) + "…" : b)}</text>` : ""}<text x="${p.x + 4}" y="${p.y - 4}" font-size="10" fill="#7D8D95">${s.id}</text>`; })()}
      ${(s.controls || []).length ? `<circle class="ctrlmark" cx="${p.x + 96}" cy="${p.y + 4}" r="6"/>` : ""}</g>`;
  }
  g += `<g id="tokens"></g>`;
  const open = mocs.filter((m) => !m.closed);
  $("#main").innerHTML = head("Processes", "The process layer sits between Standards and Procedures. Most processes are still planned; the Management of Change model shows where this is going.") + `
  <div class="panel" style="margin-bottom:18px"><div class="page-head" style="margin-bottom:8px"><div><h2>${esc(model.title)} <span class="small muted">${esc(model.id)} Rev ${esc(model.revision)} ${esc(model.status)}</span></h2><p class="small">Owner ${esc(model.owner)}. Red marks show steps that perform a control. Bold arrows are hand-offs between roles.</p></div><button class="btn primary" id="flow">Run the last 30 changes</button></div>
    <div style="overflow:auto"><svg class="lanes" viewBox="0 0 ${W} ${lanes.length * LH}" style="min-width:${W}px">${g}</svg></div>
    <p class="small muted">Step timings come from ${mocs.length} changes in the MOC register. ${open.length} changes are open now.</p></div>
  <div class="panel"><h2>Process register</h2><table class="t"><tr><th>Process</th><th>Owner</th><th>Parent</th><th>Status</th><th>Controls</th></tr>
    ${reg.map((p) => `<tr><td>${esc(p.process_id)} ${esc(p.title)}</td><td class="small">${esc(nameOf(p.owner))}</td><td>${docLink(p.parent)}</td><td>${esc(p.status)}</td><td>${p.controls.split("; ").filter(Boolean).slice(0, 4).map(ctlChip).join("")}${p.controls.split("; ").filter(Boolean).length > 4 ? "…" : ""}</td></tr>`).join("")}</table></div>`;
  $("#flow").onclick = () => {
    stopAll(); const T = $("#tokens"); T.innerHTML = "";
    const recent = [...new Set(steps.map((s) => s.moc_id))].slice(-30);
    const path = (mid) => steps.filter((s) => s.moc_id === mid && S[s.step]);
    let t = 0; const tok = recent.map((mid, i) => ({ mid, p: path(mid), born: i * 3, el: null }));
    timers.push(setInterval(() => {
      t++;
      for (const k of tok) {
        const age = t - k.born; if (age < 0) continue;
        const idx = Math.floor(age / 4); if (idx >= k.p.length) { k.el?.remove(); k.el = null; continue; }
        const p = pos(k.p[idx].step);
        if (!k.el) { k.el = document.createElementNS("http://www.w3.org/2000/svg", "circle"); k.el.setAttribute("r", 5); k.el.setAttribute("class", "token"); k.el.style.transition = "cx .5s, cy .5s"; T.appendChild(k.el); }
        k.el.setAttribute("cx", p.x + 50 + ((k.born % 5) - 2) * 6); k.el.setAttribute("cy", p.y + 22 + ((k.born % 3) - 1) * 6);
      }
      if (t > recent.length * 3 + 60) stopAll();
    }, 160));
  };
});

// ---------- performance ----------
route(/^\/performance$/, () => {
  const K = REG["PRF-REG-001_kpis"]; const M = REG["PRF-REG-001_monthly"].filter((r) => r.site === "ACE");
  const series = {}; for (const r of M) (series[r.kpi_id] ||= []).push([r.month, +r.value]);
  const pick = ["PROD-OIL", "PROD-GAS", "TRIR", "NEAR-MISS", "PSE-T2", "SPILL-N", "IOW-EXC", "ALARM-RATE", "SCE-OVERDUE", "PM-COMP", "DEFERRALS", "MOC-OPEN", "ACT-OVERDUE", "FLARE", "LIFT-COST", "DOCS-OVERDUE"];
  const spark = (pts, better) => {
    const v = pts.map((p) => p[1]), lo = Math.min(...v), hi = Math.max(...v), W = 240, Hh = 50, sx = (i) => (i / (v.length - 1)) * W, sy = (x) => Hh - 4 - ((x - lo) / (hi - lo || 1)) * (Hh - 8);
    const dlist = v.map((x, i) => `${i ? "L" : "M"}${sx(i).toFixed(1)},${sy(x).toFixed(1)}`).join(" ");
    const j = pts.findIndex((p) => p[0] === "2026-01");
    return `<svg viewBox="0 0 ${W} ${Hh}" preserveAspectRatio="none"><line x1="${sx(j)}" x2="${sx(j)}" y1="0" y2="${Hh}" stroke="#D5DDE0" stroke-dasharray="2 2"/><path d="${dlist}" fill="none" stroke="#0E5A6B" stroke-width="1.6"/><circle cx="${sx(v.length - 1)}" cy="${sy(v[v.length - 1])}" r="3" fill="#E3651D"/></svg>`;
  };
  const SUM = new Set(["count", "bbl", "MMscf", "hours"]);
  const yr = (k, unit, y) => { const v = (series[k] || []).filter((p) => p[0].startsWith(y)).map((p) => p[1]); if (!v.length) return ""; const stock = ["SCE-OVERDUE", "DEFERRALS", "MOC-OPEN", "ACT-OVERDUE", "TRIR", "DOCS-OVERDUE"].includes(k); const s = stock ? v[v.length - 1] : SUM.has(unit) ? v.reduce((a, b) => a + b, 0) : v.reduce((a, b) => a + b, 0) / v.length;
    return Number.isInteger(s) ? s.toLocaleString() : s >= 100 ? Math.round(s).toLocaleString() : s.toFixed(s < 10 ? 2 : 1); };
  $("#main").innerHTML = head("Performance", "Monthly figures from the performance register, January 2024 to October 2026. Incident and change numbers are counted from the events and MOC registers. The dashed line marks the ONE launch.") + `
  <div class="kpis">${pick.map((k) => { const d = K.find((x) => x.kpi_id === k); const s = series[k]; if (!d || !s) return ""; const last = s[s.length - 1][1];
    return `<div class="kpi"><h3>${esc(d.name)} <span class="small">(${esc(d.unit)})</span></h3><div class="v">${last >= 100 ? Math.round(last).toLocaleString() : last}</div>${spark(s, d.better)}<div class="years"><span>2024 ${yr(k, d.unit, "2024")}</span><span>2025 ${yr(k, d.unit, "2025")}</span><span>2026 ${yr(k, d.unit, "2026")}</span></div>${d.target ? `<div class="small muted">Target ${esc(d.target)}</div>` : ""}</div>`; }).join("")}</div>`;
});

// ---------- search ----------
route(/^\/search\/(.*)$/, (q) => {
  const s = q.toLowerCase().trim(); $("#q").value = q;
  const docs = DOCS.filter((d) => (d.id + " " + d.title).toLowerCase().includes(s));
  const st = STMTS.filter((x) => x.b.t.toLowerCase().includes(s)).slice(0, 40);
  const ppl = PEOPLE.filter((p) => (p.n + " " + p.t).toLowerCase().includes(s)).slice(0, 20);
  const ctl = REG["RSK-REG-002"].filter((c) => (c.control_id + " " + c.statement).toLowerCase().includes(s)).slice(0, 20);
  const rk = REG["RSK-REG-001"].filter((r) => (r.risk_id + " " + r.title).toLowerCase().includes(s));
  $("#main").innerHTML = head(`Results for “${esc(q)}”`, `${docs.length} documents, ${st.length} statements, ${ppl.length} people, ${ctl.length} controls, ${rk.length} risks.`) + `
  <div class="grid2"><div class="stack">${docs.length ? `<div class="panel"><h2>Documents</h2>${docs.map((d) => `<div>${docLink(d.id)} ${esc(d.title)}</div>`).join("")}</div>` : ""}
    ${st.length ? `<div class="panel"><h2>Statements</h2>${st.map(stmtHTML).join("")}</div>` : ""}</div>
    <div class="stack">${ppl.length ? `<div class="panel"><h2>People</h2>${ppl.map((p) => `<div>${PEOPLE.find((x) => x.t === "VP Engineering & Projects") && p.dl === PEOPLE.find((x) => x.t === "VP Engineering & Projects").id ? `<a href="#/authority/${encodeURIComponent(p.n)}">${esc(p.n)}</a>` : esc(p.n)} <span class="muted small">${esc(p.t)}, ${esc(p.f)}</span></div>`).join("")}</div>` : ""}
    ${ctl.length ? `<div class="panel"><h2>Controls</h2>${ctl.map((c) => `<div>${ctlChip(c.control_id)} ${esc(c.statement)}</div>`).join("")}</div>` : ""}
    ${rk.length ? `<div class="panel"><h2>Risks</h2>${rk.map((r) => `<div><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)} ${rateChip(r.current_rating)}</div>`).join("")}</div>` : ""}
    ${!docs.length && !st.length && !ppl.length && !ctl.length && !rk.length ? `<div class="panel"><p>Nothing matches. Try a document number, a job title or a word from a requirement.</p></div>` : ""}</div></div>`;
});

go();
