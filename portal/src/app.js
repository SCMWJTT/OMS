/* ONE Portal v2 — element-first. Everything on screen comes from window.ONE_DATA, which the build reads from the repository. */
"use strict";
const D = window.ONE_DATA;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const toDate = (s) => { if (!s) return null; if (/^\d{4}-\d{2}/.test(s)) return new Date(s.slice(0, 10) + "T00:00:00"); const m = s.match(/^(\d{1,2}) (\w+) (\d{4})$/); return m ? new Date(+m[3], MON.indexOf(m[2]), +m[1]) : null; };
const fmt = (d) => d ? `${d.getDate()} ${MON[d.getMonth()].slice(0, 3)} ${d.getFullYear()}` : "";
const fmtM = (d) => `${MON[d.getMonth()]} ${d.getFullYear()}`;
const nameOf = (p) => (p || "").split(" — ")[0].trim();
const TODAY = new Date(2026, 10, 24);
const YEAR_AGO = new Date(2025, 10, 24);
const REG = D.registers;
const ELS = D.protocol.elements;
const EL = Object.fromEntries(ELS.map((e) => [e.id, e]));
const EXP = D.protocol.expectations;
const EXPBY = Object.fromEntries(EXP.map((e) => [e.id, e]));

// ---------- one colour per element, used everywhere ----------
const ECOL = { 1: "#0B5563", 2: "#3D4FA1", 3: "#7A4FA0", 4: "#B5427A", 5: "#C8402F", 6: "#E07A1F", 7: "#D6A21E", 8: "#6E9A2E", 9: "#2E9A78", 10: "#2F7FB8" };
const SHORT = { 1: "Leadership", 2: "Policies", 3: "People", 4: "Stakeholders", 5: "Risk", 6: "Assets", 7: "Procedures", 8: "Execution", 9: "Learning", 10: "Assurance" };
const lum = (hex) => { const c = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((v) => v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
const ON = (n) => (lum(ECOL[n]) > 0.2 ? "#17262E" : "#FFFFFF");
const GROUP = (n) => (n <= 4 ? "Lead" : n <= 8 ? "Control" : "Learn");
const elOf = (tag) => +String(tag).split(".")[0] || 0;

const BIND = new Set(["req", "resp", "appr", "rec", "ctl"]);
const KNAME = { req: "Requirement", resp: "Responsibility", appr: "Approval", rec: "Record", ctl: "Control", warn: "Warning", note: "Note", kpi: "KPI", step: "Step", ref: "Reference", ext: "External standard", def: "Definition" };
const LAYER = (t) => ({ Manual: "Manual", Policy: "Policy", Standard: "Standard", Specification: "Standard", Practice: "Practice", Process: "Process", Procedure: "Procedure", Plan: "Procedure",
  "Work Instruction": "Task & record", Form: "Task & record", Register: "Task & record" }[t] || "Other");
const LAYERS = ["Policy", "Standard", "Practice", "Process", "Procedure", "Task & record"];
const LORDER = ["Manual", ...LAYERS, "Other"];
const TYPE_LAYER = { MAN: "Manual", POL: "Policy", STD: "Standard", SPC: "Standard", PRA: "Practice", PRS: "Process", PRC: "Procedure", PLN: "Procedure", WIN: "Task & record", FRM: "Task & record", REG: "Task & record" };

// ---------- indexes ----------
const DOCS = D.docs.map((d) => ({ ...d, eff: toDate(d.effective), layer: LAYER(d.type) }));
const DOC = Object.fromEntries(DOCS.map((d) => [d.id, d]));
const MAN = DOC["ACE-OMS-MAN-001"];
const STMTS = []; const SEC = {};
for (const d of DOCS) for (const s of d.sections) {
  SEC[`${d.id}#${s.bm}`] = { d, s };
  for (const b of s.blocks) if (BIND.has(b.k)) STMTS.push({ d, s, b, tags: s.tags });
}
const WORK = STMTS.filter((x) => x.d.typeCode !== "MAN");   // documents that deliver the Manual
const PEOPLE = D.people; const PBY = Object.fromEntries(PEOPLE.map((p) => [p.n, p])); const PID = Object.fromEntries(PEOPLE.map((p) => [p.id, p]));
const CTLS = REG["RSK-REG-002"]; const CTL = Object.fromEntries(CTLS.map((c) => [c.control_id, c]));
const RISKS = REG["RSK-REG-001"]; const RISK = Object.fromEntries(RISKS.map((r) => [r.risk_id, r]));
const EVENTS = REG["INC-REG-001_events"]; const EVBY = Object.fromEntries(EVENTS.map((e) => [e.event_id, e]));
const ACTIONS = REG["INC-REG-001_actions"]; const MOCS = REG["MOC-REG-001"];
const KPIS = REG["PRF-REG-001_kpis"];
const SERIES = {}; for (const r of REG["PRF-REG-001_monthly"]) if (r.site === "ACE") (SERIES[r.kpi_id] ||= []).push([r.month, +r.value]);
const sysEls = (s) => D.protocol.systems[s]?.elements || [];

// element of a control: the primary OMS tag of the section it is written in
const ctlEl = (c) => { const [doc, bm] = c.doc_ref.split("#"); const s = SEC[`${doc}#${bm}`]; return s?.s.tags[0] ? elOf(s.s.tags[0]) : sysEls(c.control_id.split("-")[1])[0] || 5; };
// barriers stop or limit a hazard directly; management checks keep the system itself honest
const BARRIER_SYS = new Set(["OPS", "AIM", "MNT", "WEL", "COW", "PSM", "EMR", "ENG"]);
const isBarrier = (c) => c.critical === "Yes" || c.nature !== "Soft" || !!c.barrier || BARRIER_SYS.has(c.control_id.split("-")[1]) || ["C-RSK-011", "C-RSK-012"].includes(c.control_id);
const riskEls = (r) => new Set([...sysEls(r.system), ...r.controls.split("; ").filter((c) => CTL[c]).map((c) => ctlEl(CTL[c]))]);
const evEls = (e) => { const s = new Set([9]); for (const r of e.risk_ids.split("; ")) if (RISK[r]) for (const n of riskEls(RISK[r])) s.add(n); if (/Audit|Review/.test(e.type)) s.add(10); if (/SCE|Inspection|IOW|Well integrity/.test(e.type)) s.add(6); return s; };

// per-element facts, computed once
const ELF = {};
for (const e of ELS) ELF[e.id] = { stmts: 0, docs: new Map(), ctls: [], risks: [], events: [], actions: [], kpis: [], mocs: [] };
for (const x of WORK) { const n = elOf(x.tags[0]); if (ELF[n]) { ELF[n].stmts++; ELF[n].docs.set(x.d.id, (ELF[n].docs.get(x.d.id) || 0) + 1); } }
for (const c of CTLS) ELF[ctlEl(c)]?.ctls.push(c);
for (const r of RISKS) for (const n of riskEls(r)) ELF[n]?.risks.push(r);
for (const e of EVENTS) { const d = toDate(e.date); if (d >= YEAR_AGO) for (const n of evEls(e)) ELF[n].events.push(e); }
for (const a of ACTIONS) { const e = EVBY[a.event_id]; if (e) for (const n of evEls(e)) ELF[n].actions.push(a); }
for (const k of KPIS) if (k.oms_tag) ELF[elOf(k.oms_tag)]?.kpis.push(k);
for (const m of MOCS) for (const n of sysEls(m.system)) ELF[n]?.mocs.push(m);

function coverage(at) {
  const m = new Map(EXP.map((e) => [e.id, { n: 0, docs: new Set(), primary: 0 }]));
  for (const x of WORK) {
    if (at && (!x.d.eff || x.d.eff > at)) continue;
    x.tags.forEach((t, i) => { const c = m.get(t); if (c) { c.n++; c.docs.add(x.d.id); if (i === 0) c.primary++; } });
  }
  return m;
}
const COV = coverage(TODAY);
const expState = (id) => { const n = COV.get(id).n; return n === 0 ? ["gap", "Not yet written"] : n < 3 ? ["thin", "Thin"] : ["ok", "Covered"]; };
const elCovered = (n, cov = COV) => { const ex = EXP.filter((x) => x.element === n); return [ex.filter((x) => cov.get(x.id).n).length, ex.length]; };
// how much of each element a document carries (primary tag of each binding statement)
const fingerprint = (d) => { const f = {}; for (const s of d.sections) for (const b of s.blocks) if (BIND.has(b.k) && s.tags[0]) f[elOf(s.tags[0])] = (f[elOf(s.tags[0])] || 0) + 1; return f; };
const FP = Object.fromEntries(DOCS.map((d) => [d.id, fingerprint(d)]));

// the Manual, read per element
const manSec = (bm) => MAN?.sections.find((s) => s.bm === bm);
const elIntro = (n) => { const s = manSec(`el_${n}`); if (!s) return {}; const t = s.blocks.find((b) => b.k === "table"); const note = s.blocks.find((b) => b.k === "note");
  return { desc: t ? t.rows[0][t.rows[0].length - 1] : "", you: note ? note.t.replace(/^What this means for you\s*/, "") : "" }; };
const firstSentence = (t) => (t.match(/^.*?[.!?](\s|$)/) || [t])[0].trim();
const expSec = (id) => manSec(`s${id.replace(".", "_")}`);

// ---------- small renderers ----------
const wordIcon = (id, big) => DOC[id] ? `<a class="wicon${big ? " big" : ""}" href="docs/${id}.docx" download="${esc(DOC[id].file.split("/").pop())}" title="Download the Word document" aria-label="Download ${id} as a Word document"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="2" width="18" height="20" rx="2" fill="#2B579A"/><path d="M6.5 7.5h2l1.3 6 1.5-6h1.5l1.5 6 1.3-6h2l-2.3 9h-1.9L12 10.7l-1.4 5.8H8.8z" fill="#fff"/></svg>${big ? "<span>Word</span>" : ""}</a>` : "";
const docLink = (id, bm, label) => DOC[id] ? `<a href="#/doc/${id}${bm ? "/" + bm : ""}">${esc(label || id)}</a>` : `<span class="muted" data-tip="Planned, not yet issued">${esc(label || id)}</span>`;
const hcls = (h) => "h-" + (h || "").replace(" ", "");
const ctlChip = (c) => { const x = CTL[c]; return `<a class="chip" href="#/control/${c}" data-tip="${x ? `<b>${c}</b>${esc(x.statement)}` : c}">${x ? `<span class="dot ${hcls(x.health)}"></span>` : ""}${esc(c)}</a>`; };
const tagChips = (tags, link = true) => (tags || []).map((t, i) => { const n = elOf(t); return link ? `<a class="tag${i === 0 ? " primary" : ""}" style="--c:${ECOL[n] || "#0B5563"}" href="#/exp/${t}" data-tip="${esc(t + " " + (EXPBY[t]?.title || ""))}">${esc(t)}</a>` : `<span class="tag" style="--c:${ECOL[n]}">${esc(t)}</span>`; }).join("");
const kindChip = (k) => `<span class="kind k-${k}">${KNAME[k] || k}</span>`;
const rateChip = (r) => `<span class="rate r-${(r || "").replace(" ", "")}">${esc(r)}</span>`;
const gateChip = (id) => { const g = D.gate[id]; return g ? `<span class="gate g-${g.outcome}">${g.outcome === "PASS_AFTER_FIX" ? "Pass after fix" : g.outcome === "PASS" ? "Pass" : "Fail"}</span>` : ""; };
const fpBar = (id) => { const f = FP[id] || {}; const t = Object.values(f).reduce((a, b) => a + b, 0); if (!t) return `<span class="fp" data-tip="No binding statements"></span>`;
  return `<span class="fp" data-tip="${Object.entries(f).sort((a, b) => b[1] - a[1]).map(([n, v]) => `${n}. ${esc(EL[n].title)}: ${v}`).join("<br>")}">${Object.keys(f).sort((a, b) => a - b).map((n) => `<i style="width:${100 * f[n] / t}%;background:${ECOL[n]}"></i>`).join("")}</span>`; };
const hbar = (parts) => { const t = parts.reduce((a, p) => a + p[1], 0) || 1; return `<div class="hbar">${parts.filter((p) => p[1]).map(([l, v, c]) => `<i style="width:${100 * v / t}%;background:${c}" data-tip="${esc(l)}: ${v}"></i>`).join("")}</div>`; };
const HEALTH = [["Effective", "var(--eff)"], ["Degraded", "var(--deg)"], ["Failed", "var(--fail)"], ["Not tested", "var(--nt)"]];
const healthBar = (cs) => hbar(HEALTH.map(([h, c]) => [h, cs.filter((x) => x.health === h && x.status === "Active").length, c]));
const RATES = [["Very High", "var(--vhigh)"], ["High", "var(--high)"], ["Medium", "var(--med)"], ["Low", "var(--low)"]];
const rateBar = (rs) => hbar(RATES.map(([r, c]) => [r, rs.filter((x) => x.current_rating === r).length, c]));
const plural = (n, w, ws) => `${n.toLocaleString()} ${n === 1 ? w : ws || w + "s"}`;
const spark = (pts, col = "#0B5563", W = 240, H = 46) => {
  if (!pts || pts.length < 2) return ""; const v = pts.map((p) => p[1]), lo = Math.min(...v), hi = Math.max(...v), sx = (i) => (i / (v.length - 1)) * W, sy = (x) => H - 4 - ((x - lo) / (hi - lo || 1)) * (H - 8);
  const j = pts.findIndex((p) => p[0] === "2026-01");
  return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">${j > 0 ? `<line x1="${sx(j)}" x2="${sx(j)}" y1="0" y2="${H}" stroke="#D5DDE0" stroke-dasharray="2 2"/>` : ""}<path d="${v.map((x, i) => `${i ? "L" : "M"}${sx(i).toFixed(1)},${sy(x).toFixed(1)}`).join(" ")}" fill="none" stroke="${col}" stroke-width="1.7"/><circle cx="${sx(v.length - 1)}" cy="${sy(v[v.length - 1])}" r="3" fill="${col}"/></svg>`;
};

// ---------- shell ----------
const NAV = [
  ["#/", "OMS wheel"], ["#/library", "Library", DOCS.length], ["#/review", "Comments and edits", ""], ["sep"],
  ["#/barriers", "Barriers"], ["#/risk", "Risks", RISKS.length], ["#/controls", "Controls", CTLS.length], ["sep"],
  ["#/explore", "Requirements", WORK.length], ["#/gaps", "Gaps"], ["#/process", "Processes", (D.processes || []).length + " mapped"], ["#/ci", "Improvement", (REG["CI-REG-001"] || []).filter((c) => !["Closed", "Parked"].includes(c.stage)).length], ["#/performance", "Performance"], ["#/authority", "Technical authority"], ["head", "Company"],
  ["#/company", "About ACE"], ["#/model", "The ONE model"], ["#/org", "Organisation"], ["#/roles", "Roles"], ["#/people", "People", (D.people || []).filter((p) => p.st !== "Left").length],
];
$("#nav").innerHTML = NAV.map(([h, l, c]) => h === "sep" ? `<li class="sep" aria-hidden="true"></li>` : h === "head" ? `<li class="navhead">${l}</li>` : `<li><a href="${h}">${l}<span class="count" ${h === "#/review" ? 'id="navNotes"' : ""}>${c ?? ""}</span></a></li>`).join("");
$("#built").textContent = `Built ${fmt(new Date(D.built))} from ${DOCS.length} documents and ${Object.keys(REG).length} registers in the repository.`;

const ROUTES = [];
const route = (re, fn) => ROUTES.push([re, fn]);
const timers = []; const stopAll = () => { while (timers.length) clearInterval(timers.pop()); };
function go() {
  const h = decodeURIComponent(location.hash.slice(1) || "/");
  const top = "#" + (h === "/" ? "/" : "/" + h.split("/")[1]);
  const alias = { "#/el": "#/", "#/exp": "#/", "#/doc": "#/library", "#/control": "#/controls", "#/site": "#/company", "#/role": "#/roles", "#/duty": "#/roles", "#/person": "#/people", "#/value": "#/process" };
  for (const a of $$("#nav a")) { if (a.getAttribute("href") === (alias[top] || top)) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); }
  for (const [re, fn] of ROUTES) { const m = h.match(re); if (m) { stopAll(); $("#main").innerHTML = ""; fn(...m.slice(1)); $("#main").focus({ preventScroll: true }); if (!/^\/doc\/[^/]+\/./.test(h)) window.scrollTo(0, 0); return; } }
  go404();
}
function go404() { page(null, `<div class="panel"><h2>Page not found</h2><p><a href="#/">Go to the OMS wheel</a></p></div>`); }
window.addEventListener("hashchange", go);
const head = (title, sub, crumb, right = "") => `<div class="page-head"><div>${crumb ? `<div class="crumb">${crumb}</div>` : ""}<h1>${title}</h1>${sub ? `<p>${sub}</p>` : ""}</div>${right}</div>`;
const toast = (t) => { const d = document.createElement("div"); d.className = "toast"; d.setAttribute("role", "status"); d.textContent = t; document.body.appendChild(d); setTimeout(() => d.remove(), 2600); };

const tip = $("#tip");
document.addEventListener("mousemove", (e) => {
  const t = e.target.closest?.("[data-tip]");
  if (!t) { tip.hidden = true; return; }
  tip.innerHTML = t.getAttribute("data-tip"); tip.hidden = false;
  tip.style.left = Math.min(e.clientX + 14, innerWidth - 310) + "px"; tip.style.top = (e.clientY + 16) + "px";
});

// ---------- wheel geometry ----------
function arc(cx, cy, r0, r1, a0, a1) {
  const p = (r, a) => [(cx + r * Math.cos(a)).toFixed(2), (cy + r * Math.sin(a)).toFixed(2)];
  const large = a1 - a0 > Math.PI ? 1 : 0;
  const [x0, y0] = p(r1, a0), [x1, y1] = p(r1, a1), [x2, y2] = p(r0, a1), [x3, y3] = p(r0, a0);
  return `M${x0},${y0} A${r1},${r1} 0 ${large} 1 ${x1},${y1} L${x2},${y2} A${r0},${r0} 0 ${large} 0 ${x3},${y3} Z`;
}
const SEG = (2 * Math.PI) / 10;
const segA = (n) => [-Math.PI / 2 + (n - 1) * SEG, -Math.PI / 2 + n * SEG];

// compact wheel band at the top of every page; `on` = element numbers to light, or a weight map
function band(on) {
  if (on && typeof on === "object" && !Array.isArray(on) && !Object.keys(on).length) on = null;
  const w = on == null ? null : typeof on === "number" ? { [on]: 1 } : Array.isArray(on) ? Object.fromEntries(on.map((n) => [n, 1])) : on;
  const lit = (n) => !w || w[n];
  const segs = ELS.map((e) => { const [a0, a1] = segA(e.id), am = (a0 + a1) / 2, pop = w && w[e.id] && Object.keys(w).length < 3 ? 5 : 0;
    return `<path class="seg" d="${arc(50, 50, 22, 48, a0 + 0.012, a1 - 0.012)}" fill="${ECOL[e.id]}" opacity="${lit(e.id) ? 1 : 0.22}" style="transform:translate(${(pop * Math.cos(am)).toFixed(1)}px,${(pop * Math.sin(am)).toFixed(1)}px)" data-goel="${e.id}" data-tip="<b>Element ${e.id}</b>${esc(e.title)}"/>`; }).join("");
  const chips = ELS.map((e) => `<a class="echip${w && w[e.id] ? " on" : w ? " dim" : ""}" style="--c:${ECOL[e.id]}" href="#/el/${e.id}"><b style="color:${ON(e.id)}">${e.id}</b>${SHORT[e.id]}</a>`).join("");
  return `<div class="band"><svg viewBox="-6 -6 112 112" role="img" aria-label="OMS wheel">${segs}<circle cx="50" cy="50" r="19" fill="#fff"/><text x="50" y="54" text-anchor="middle" font-size="11" font-weight="600" fill="#17262E">ONE</text></svg><nav class="chips" aria-label="OMS elements">${chips}</nav></div>`;
}
function page(on, html) { $("#main").innerHTML = band(on) + html; }
document.addEventListener("click", (e) => { const s = e.target.closest?.("[data-goel]"); if (s) location.hash = `#/el/${s.dataset.goel}`; });

// ---------- home: the OMS wheel ----------
function bigWheel() {
  const cx = 320, cy = 320; let segs = "", nums = "", labs = "", groups = "", rings = "";
  for (const e of ELS) {
    const [a0, a1] = segA(e.id), am = (a0 + a1) / 2;
    segs += `<path class="seg in" style="animation-delay:${(e.id - 1) * 70}ms" d="${arc(cx, cy, 128, 246, a0 + 0.01, a1 - 0.01)}" fill="${ECOL[e.id]}" data-el="${e.id}" data-tip="<b>${e.id}. ${esc(e.title)}</b>${esc(firstSentence(elIntro(e.id).desc || ""))}"/>`;
    nums += `<text class="num" x="${cx + 187 * Math.cos(am)}" y="${cy + 187 * Math.sin(am) + 9}" text-anchor="middle" style="fill:${ON(e.id)}">${e.id}</text>`;
    const words = e.title.split(" "); let l1 = "", l2 = ""; for (const w of words) ((l1 + " " + w).trim().length <= 18 && !l2 ? (l1 = (l1 + " " + w).trim()) : (l2 = (l2 + " " + w).trim()));
    const R = 266, x = cx + R * Math.cos(am), y = cy + R * Math.sin(am), anc = Math.abs(Math.cos(am)) < 0.2 ? "middle" : Math.cos(am) > 0 ? "start" : "end";
    labs += `<text class="lab" x="${x}" y="${y + (Math.sin(am) > 0.5 ? 14 : Math.sin(am) < -0.5 ? -14 : -4)}" text-anchor="${anc}">${esc(l1)}${l2 ? `<tspan x="${x}" dy="21">${esc(l2)}</tspan>` : ""}</text>`;
    rings += `<path d="${arc(cx, cy, 108, 118, a0 + 0.02, a1 - 0.02)}" fill="#E3E9EB"/><path class="ring" data-ring="${e.id}" d="" fill="${ECOL[e.id]}"/>`;
  }
  for (const [g, a, b] of [["Lead", 1, 4], ["Control", 5, 8], ["Learn", 9, 10]]) {
    const a0 = segA(a)[0], a1 = segA(b)[1];
    groups += `<path d="${arc(cx, cy, 250, 252.5, a0 + 0.03, a1 - 0.03)}" fill="#B9C5CA"/>`;
  }
  return `<svg class="bigwheel" viewBox="-130 -6 900 652" role="img" aria-label="The ten elements of the ACE Operating Management System">
    ${groups}${rings}${segs}${nums}${labs}
    <circle cx="${cx}" cy="${cy}" r="100" fill="#fff"/>
    <text class="hub1" x="${cx}" y="${cy - 2}" text-anchor="middle">ONE</text>
    <text class="hub2" x="${cx}" y="${cy + 22}" text-anchor="middle" id="hubT">10 elements, 54 expectations</text>
    <text class="hub2" x="${cx}" y="${cy + 40}" text-anchor="middle" id="hubD"></text></svg>`;
}
function paintRings(svg, at) {
  const cov = coverage(at); let tot = 0;
  for (const e of ELS) { const [c, n] = elCovered(e.id, cov); tot += c; const [a0, a1] = segA(e.id); const f = c / n;
    const p = svg.querySelector(`[data-ring="${e.id}"]`); p.setAttribute("d", f ? arc(320, 320, 108, 118, a0 + 0.02, a0 + 0.02 + (a1 - a0 - 0.04) * f) : ""); p.setAttribute("data-tip", `<b>${e.id}. ${esc(e.title)}</b>${c} of ${n} expectations written into issued documents`); }
  return tot;
}

route(/^\/$/, () => {
  const ctlA = CTLS.filter((c) => c.status === "Active"); const bar = ctlA.filter(isBarrier);
  const covered = [...COV.values()].filter((c) => c.n).length;
  const months = []; for (let d = new Date(2025, 11, 1); d <= TODAY; d = new Date(d.getFullYear(), d.getMonth() + 1, 1)) months.push(new Date(d.getFullYear(), d.getMonth() + 1, 0)); months[months.length - 1] = TODAY;
  const recentDocs = [...DOCS].filter((d) => d.eff).sort((a, b) => b.eff - a.eff).slice(0, 6);
  const recentEv = [...EVENTS].sort((a, b) => b.date.localeCompare(a.date)).filter((e) => +e.severity >= 2 || e.controls_failed).slice(0, 6);
  const openMoc = MOCS.filter((m) => !m.closed).sort((a, b) => b.raised.localeCompare(a.raised)).slice(0, 6);
  page(null, `
  <section class="hero">
    <div>${bigWheel()}</div>
    <div>
      <h1 class="display">Acme Caribbean Energy runs on one management system</h1>
      <p class="lede">Ten elements tell ACE what good looks like. Every page here is read from the approved Word documents and live registers, so the wheel shows what is written, what it controls and how it is performing today. Choose an element to start.</p>
      <div class="figures"><div><b>${DOCS.length}</b><span>documents in force</span></div><div><b>${WORK.length.toLocaleString()}</b><span>binding statements</span></div><div><b>${covered}<small style="font-size:15px;color:var(--ink-3)">/54</small></b><span>expectations written</span></div><div><b>${bar.length}</b><span>barriers watched</span></div></div>
      <div class="replay" style="margin-top:14px"><button class="btn" id="play">Watch the system fill in since launch</button><span class="date-read" id="dread">Today</span></div>
      <p class="small muted" style="margin-top:6px">The thin inner ring shows how much of each element is written into issued documents.</p>
    </div>
  </section>
  <h2 style="margin-top:8px">The ten elements today</h2>
  <div class="tiles">${ELS.map((e) => { const f = ELF[e.id]; const [c, n] = elCovered(e.id); const ca = f.ctls.filter((x) => x.status === "Active");
    return `<a class="tile" style="--c:${ECOL[e.id]}" href="#/el/${e.id}"><span class="n">${GROUP(e.id)} ${e.id}</span><h3>${esc(e.title)}</h3><div class="head">${esc(firstSentence(elIntro(e.id).desc || ""))}</div>
      <div class="meter" data-tip="${c} of ${n} expectations written"><i style="width:${100 * c / n}%"></i></div>
      <div class="sig"><span><b>${c}/${n}</b>expectations</span><span><b>${f.stmts}</b>statements</span><span><b>${ca.length}</b>controls</span></div>
      ${ca.length ? healthBar(ca) : `<div class="hbar"></div>`}</a>`; }).join("")}</div>
  <div class="strip">
    <div class="panel"><h2>Newest documents</h2><ul class="feed">${recentDocs.map((d) => `<li><time>${fmt(d.eff)}</time><span>${docLink(d.id, "", d.title)}<div>${fpBar(d.id)}</div></span></li>`).join("")}</ul></div>
    <div class="panel"><h2>Events that tested controls</h2><ul class="feed">${recentEv.map((e) => `<li><time>${fmt(toDate(e.date))}</time><span>${[...evEls(e)].filter((n) => n !== 9).slice(0, 2).map((n) => `<span class="edot" style="--c:${ECOL[n]}"></span>`).join("")}${esc(e.title)}<div class="small muted">${esc(e.type)}, ${esc(D.protocol.sites[e.site] || e.site)}${e.controls_failed ? `. Failed: ${e.controls_failed.split("; ").map(ctlChip).join("")}` : ""}</div></span></li>`).join("")}</ul></div>
    <div class="panel"><h2>Changes in progress</h2><ul class="feed">${openMoc.map((m) => `<li><time>${fmt(toDate(m.raised))}</time><span>${sysEls(m.system).slice(0, 1).map((n) => `<span class="edot" style="--c:${ECOL[n]}"></span>`).join("")}${esc(m.title)}<div class="small muted">${esc(m.moc_id)}, ${esc(m.status)}</div></span></li>`).join("")}</ul></div>
  </div>`);
  const svg = $(".bigwheel");
  paintRings(svg, TODAY); $("#hubD").textContent = `${covered} written into documents`;
  svg.addEventListener("mouseover", (e) => { const s = e.target.closest(".seg"); if (!s) return; for (const p of svg.querySelectorAll(".seg")) p.style.transform = ""; const [a0, a1] = segA(+s.dataset.el), am = (a0 + a1) / 2; s.classList.remove("in"); s.style.transform = `translate(${10 * Math.cos(am)}px,${10 * Math.sin(am)}px)`; });
  svg.addEventListener("mouseleave", () => { for (const p of svg.querySelectorAll(".seg")) p.style.transform = ""; });
  svg.addEventListener("click", (e) => { const s = e.target.closest(".seg"); if (!s) return; const n = +s.dataset.el; const [a0, a1] = segA(n), am = (a0 + a1) / 2;
    for (const p of svg.querySelectorAll(".seg")) { p.classList.remove("in"); if (p !== s) p.style.opacity = 0.15; }
    s.style.transform = `translate(${26 * Math.cos(am)}px,${26 * Math.sin(am)}px) scale(1.06)`;
    setTimeout(() => (location.hash = `#/el/${n}`), matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 380); });
  $("#play").onclick = () => { stopAll(); let i = 0;
    const step = () => { const t = paintRings(svg, months[i]); $("#dread").textContent = i === months.length - 1 ? "Today" : fmtM(months[i]); $("#hubD").textContent = `${t} written into documents`; };
    step(); timers.push(setInterval(() => { i++; if (i >= months.length) return stopAll(); step(); }, 900)); };
});

// ---------- element overview ----------
route(/^\/el\/(\d+)$/, (n) => {
  n = +n; const e = EL[n]; if (!e) return go404();
  const f = ELF[n]; const intro = elIntro(n); const c = ECOL[n];
  const owner = PEOPLE.find((p) => p.t === e.owner && p.st !== "Left");
  const ex = EXP.filter((x) => x.element === n); const [cv, tot] = elCovered(n);
  const ca = f.ctls.filter((x) => x.status === "Active"); const bars = ca.filter(isBarrier);
  const openAct = f.actions.filter((a) => !a.closed); const overdue = openAct.filter((a) => toDate(a.due) < TODAY);
  const evTypes = {}; for (const ev of f.events) evTypes[ev.type] = (evTypes[ev.type] || 0) + 1;
  const topTypes = Object.entries(evTypes).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const openMoc = f.mocs.filter((m) => !m.closed);
  const measures = ex.flatMap((x) => (expSec(x.id)?.blocks || []).filter((b) => b.k === "kpi").map((b) => [x.id, b.t.replace(/^Measure\s*/, "")]));
  const docs = [...f.docs].sort((a, b) => b[1] - a[1]);
  const prev = n > 1 ? n - 1 : 10, next = n < 10 ? n + 1 : 1;
  page(n, `
  <div class="crumb"><a href="#/">OMS wheel</a> / ${GROUP(n)}</div>
  <div class="eband" style="--c:${c};color:${ON(n)}"><div class="big">${n}</div><div><h1 style="color:inherit">${esc(e.title)}</h1><p>${esc(intro.desc)}</p></div>
    <div class="owner">Element owner<br><b>${owner ? `<a href="#/person/${owner.id}" style="color:inherit">${esc(owner.n)}</a>` : esc(e.owner)}</b><br>${ROLE_BY[e.owner] ? `<a href="#/role/${ROLE_BY[e.owner].role_id}" style="color:inherit">${esc(e.owner)}</a>` : esc(e.owner)}<div style="margin-top:10px"><a href="#/el/${prev}" style="color:inherit">Previous</a> &nbsp; <a href="#/el/${next}" style="color:inherit">Next</a></div></div></div>
  ${intro.you ? `<div class="youline" style="--c:${c}"><b>What this means for you.</b> ${esc(intro.you)}</div>` : ""}
  <div class="page-head" style="margin-bottom:10px"><div><h2 style="margin:0">What the Manual expects</h2><p class="small">${cv} of ${tot} expectations are written into issued documents. Choose one to see the documents, statements and controls behind it.</p></div>
    <a class="btn" href="#/library/el/${n}">Read element ${n} as one manual</a></div>
  <div class="cards">${ex.map((x) => { const s = expSec(x.id); const intro = s?.blocks.find((b) => b.k === "p"); const cc = COV.get(x.id); const [st, sl] = expState(x.id);
    return `<a class="card" style="--c:${c}" href="#/exp/${x.id}"><span class="id">${x.id}</span><h3>${esc(x.title)}</h3><p class="small muted" style="margin:0 0 8px">${esc(intro ? firstSentence(intro.t) : "")}</p>
      <div class="row"><span>${plural(cc.n, "statement")} in ${plural(cc.docs.size, "document")}</span><span class="state s-${st}">${sl}</span></div></a>`; }).join("")}</div>
  <h2 style="margin-top:26px">How element ${n} is working at ACE</h2>
  <div class="drill">
    <details class="dt"><summary><h3>Documents</h3><div class="big">${docs.length}</div><div class="small muted">${plural(f.stmts, "binding statement")} whose main tag is in element ${n}</div></summary>
      <div class="body"><table class="t">${docs.map(([id, k]) => `<tr><td>${docLink(id, "", id)}<div class="small">${esc(DOC[id].title)}</div></td><td>${fpBar(id)}</td><td class="n">${k}</td></tr>`).join("") || `<tr><td class="muted">No issued document leads with this element yet.</td></tr>`}</table></div></details>
    <details class="dt"><summary><h3>Controls and barriers</h3><div class="big">${ca.length}</div><div class="small muted">${bars.length} barriers, ${ca.length - bars.length} management checks</div>${healthBar(ca)}</summary>
      <div class="body">${ca.map((x) => `<div class="barrier" style="--hc:var(--${{ Effective: "eff", Degraded: "deg", Failed: "fail" }[x.health] || "nt"})"><div><a href="#/control/${x.control_id}">${x.control_id}</a> ${isBarrier(x) ? `<span class="kind k-ctl">Barrier</span>` : ""} ${esc(x.statement)}<div class="small muted">${esc(x.health)}, owner ${esc(nameOf(x.owner))}</div></div></div>`).join("") || `<p class="muted small">No Control IDs written for this element yet. Older documents hold controls without IDs.</p>`}</div></details>
    <details class="dt"><summary><h3>Risks</h3><div class="big">${f.risks.length}</div><div class="small muted">Risks whose system or controls sit in this element</div>${rateBar(f.risks)}</summary>
      <div class="body"><table class="t">${[...f.risks].sort((a, b) => "VHML".indexOf(a.current_rating[0]) - "VHML".indexOf(b.current_rating[0])).map((r) => `<tr><td><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)}</td><td>${rateChip(r.current_rating)}</td></tr>`).join("")}</table></div></details>
    <details class="dt"><summary><h3>Events in the last 12 months</h3><div class="big">${f.events.length}</div><div class="small muted">${topTypes.slice(0, 3).map(([t, k]) => `${k} ${t.toLowerCase()}`).join(", ")}</div>${hbar(topTypes.map(([t, k], i) => [t, k, [c, "#5E7680", "#93A6AE", "#B9C7CD", "#DCE4E7"][i]]))}</summary>
      <div class="body"><ul class="events">${[...f.events].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 30).map((ev) => `<li><span class="muted">${fmt(toDate(ev.date))}</span><span>${esc(ev.title)} <span class="small muted">${esc(ev.type)}, ${esc(ev.site)}</span></span></li>`).join("")}</ul></div></details>
    <details class="dt"><summary><h3>Actions</h3><div class="big">${openAct.length}</div><div class="small muted">open from investigations and audits, ${overdue.length} overdue</div>${hbar([["Overdue", overdue.length, "var(--fail)"], ["Open, on time", openAct.length - overdue.length, "var(--deg)"], ["Closed", f.actions.length - openAct.length, "var(--eff)"]])}</summary>
      <div class="body"><table class="t">${openAct.map((a) => `<tr><td>${esc(a.title)}<div class="small muted">${esc(a.action_id)}, ${esc(nameOf(a.owner))}</div></td><td class="small ${toDate(a.due) < TODAY ? "" : "muted"}" style="${toDate(a.due) < TODAY ? "color:var(--fail)" : ""}">Due ${fmt(toDate(a.due))}</td></tr>`).join("") || `<tr><td class="muted">No open actions.</td></tr>`}</table></div></details>
    <details class="dt"><summary><h3>Measures</h3><div class="big">${f.kpis.length + measures.length}</div><div class="small muted">${f.kpis.length} tracked monthly, ${measures.length} set by the Manual</div></summary>
      <div class="body">${f.kpis.map((k) => `<div style="margin-bottom:10px"><div class="small"><b>${esc(k.name)}</b> <span class="muted">(${esc(k.unit)})${k.target ? `, target ${esc(k.target)}` : ""}</span></div>${spark(SERIES[k.kpi_id], c, 280, 34)}</div>`).join("")}
      ${measures.map(([id, t]) => `<div class="stmt k-kpi"><p class="small">${esc(t)}</p><div class="src"><a href="#/exp/${id}">${id}</a></div></div>`).join("")}</div></details>
    <details class="dt"><summary><h3>Changes</h3><div class="big">${openMoc.length}</div><div class="small muted">open changes in this element's systems, ${f.mocs.length} since 2024</div></summary>
      <div class="body"><table class="t">${openMoc.slice(0, 40).map((m) => `<tr><td>${esc(m.title)}<div class="small muted">${esc(m.moc_id)}, ${esc(m.status)}${m.temp_expiry ? `, temporary until ${fmt(toDate(m.temp_expiry))}` : ""}</div></td></tr>`).join("") || `<tr><td class="muted">No open changes.</td></tr>`}</table></div></details>
  </div>`);
});

// ---------- expectation ----------
route(/^\/exp\/(\d+\.\d+)$/, (id) => {
  const x = EXPBY[id]; if (!x) return go404(); const n = x.element, c = ECOL[n];
  const ms = expSec(id);
  const st = WORK.filter((s) => s.tags.includes(id));
  const byDoc = new Map(); for (const s of st) { if (!byDoc.has(s.d.id)) byDoc.set(s.d.id, []); byDoc.get(s.d.id).push(s); }
  const ctl = [...new Set(st.flatMap((s) => s.b.c || []))];
  const risks = [...new Set(ctl.map((k) => CTL[k]?.risk_id).filter(Boolean))];
  const [stt, sl] = expState(id);
  const cols = ["Policy", "Standard", "Practice", "Procedure"].map((l) => [l, [...byDoc.keys()].filter((d) => DOC[d].layer === l)]);
  const kp = KPIS.filter((k) => k.oms_tag === id);
  const siblings = EXP.filter((e) => e.element === n);
  page(n, `
  <div class="crumb"><a href="#/">OMS wheel</a> / <a href="#/el/${n}">${n}. ${esc(EL[n].title)}</a></div>
  <div class="page-head"><div><h1><span style="color:${c}">${id}</span> ${esc(x.title)}</h1><p><span class="state s-${stt}">${sl}</span> ${plural(st.length, "binding statement")} in ${plural(byDoc.size, "document")}, ${plural(ctl.length, "control")}.</p></div>
    <div class="chips">${siblings.map((s) => `<a class="echip${s.id === id ? " on" : ""}" style="--c:${c}" href="#/exp/${s.id}">${s.id}</a>`).join("")}</div></div>
  <div class="panel" style="border-top:4px solid ${c};margin-bottom:18px"><h2>The thread from the Manual to the work</h2>
    <div class="thread"><div class="col"><h4>Manual</h4><a class="chip" href="#/doc/ACE-OMS-MAN-001/${ms?.bm || ""}">${id} in the Manual</a></div>
      ${cols.map(([l, ds]) => `<div class="col${ds.length ? "" : " empty"}"><h4>${l}</h4>${ds.map((d) => `<a class="chip" href="#/doc/${d}" data-tip="${esc(DOC[d].title)}">${d.replace("ACE-", "")}</a>`).join("")}</div>`).join("")}
      <div class="col${ctl.length ? "" : " empty"}"><h4>Controls</h4>${ctl.map(ctlChip).join("")}</div></div></div>
  <div class="grid2" style="align-items:start">
    <div class="panel"><h2>What the Manual expects</h2>${ms ? ms.blocks.filter((b) => b.k !== "ref").map(blockHTML).join("") : `<p class="muted">The Manual section was not found.</p>`}</div>
    <div class="stack">
      ${risks.length ? `<div class="panel"><h2>Risks these controls address</h2>${risks.map((r) => `<div style="margin-bottom:6px"><a href="#/risk/${r}">${r}</a> ${esc(RISK[r].title)} ${rateChip(RISK[r].current_rating)}</div>`).join("")}</div>` : ""}
      ${kp.length ? `<div class="panel"><h2>Measured monthly</h2>${kp.map((k) => `<div class="small"><b>${esc(k.name)}</b> <span class="muted">${esc(k.unit)}</span></div>${spark(SERIES[k.kpi_id], c, 280, 36)}`).join("")}</div>` : ""}
      ${stt !== "ok" ? `<div class="panel" style="border-left:4px solid var(--flare)"><b>${stt === "gap" ? "Gap." : "Thin coverage."}</b> ${stt === "gap" ? "No issued document carries a binding statement for this expectation yet." : "Fewer than three binding statements serve this expectation."} <a href="#/gaps">See all gaps</a></div>` : ""}
    </div></div>
  <div class="panel" style="margin-top:18px"><h2>Binding statements tagged ${id}</h2>${[...byDoc].map(([doc, list]) => `<h3 style="margin-top:14px">${docLink(doc)} ${esc(DOC[doc].title)}</h3>${list.map(stmtHTML).join("")}`).join("") || `<p class="muted">None yet.</p>`}</div>`);
});
function stmtHTML(s) { return `<div class="stmt k-${s.b.k}"><p>${linkRoles(s.b.t)}</p><div class="src">${kindChip(s.b.k)} ${docLink(s.d.id, s.s.bm, `${s.d.id}, ${s.s.title}`)} ${tagChips(s.tags)} ${(s.b.c || []).map(ctlChip).join("")}</div></div>`; }
const linkRefs = (h) => h.replace(/(?<![A-Za-z0-9-])(ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?)/g, (m) => DOC[m] ? `<a href="#/doc/${m}">${m}</a>` : `<span data-tip="Planned document" style="border-bottom:1px dashed var(--ink-3)">${m}</span>`);
function blockInner(b, text) {
  let t = text ?? linkRefs(linkRoles(b.t));
  if (text == null) for (const c of b.c || []) t = t.replace(new RegExp(`\\(?${c}\\)?`), ` ${ctlChip(c)}`);
  return `${BIND.has(b.k) ? kindChip(b.k) + " " : ""}${t}`;
}
function blockHTML(b) {
  if (b.k === "table") return `<table>${b.rows.map((r) => `<tr>${r.map((c) => `<td>${linkRefs(linkRoles(c))}</td>`).join("")}</tr>`).join("")}</table>`;
  return `<div class="blk k-${b.k}">${blockInner(b)}</div>`;
}

// ---------- requirements explorer ----------
route(/^\/explore(?:\/(.*))?$/, (q) => {
  const opt = (v, l) => `<option value="${esc(v)}">${esc(l)}</option>`;
  const fns = [...new Set(DOCS.map((d) => d.func).filter(Boolean))].sort();
  page(null, head("Requirements", "Every binding statement in every issued document. Filter by element, system, function, layer or kind.") + `
  <div class="filters">
    <label>Element<select id="fe">${opt("", "All")}${ELS.map((e) => opt(e.id, `${e.id}. ${e.title}`)).join("")}</select></label>
    <label>System<select id="fs">${opt("", "All")}${[...new Set(DOCS.map((d) => d.system))].sort().map((s) => opt(s, `${s} ${D.protocol.systems[s]?.name || ""}`)).join("")}</select></label>
    <label>Function<select id="ff">${opt("", "All")}${fns.map((f) => opt(f, f)).join("")}</select></label>
    <label>Layer<select id="fl">${opt("", "All")}${LAYERS.map((l) => opt(l, l)).join("")}</select></label>
    <label>Kind<select id="fk">${opt("", "All")}${[...BIND].map((k) => opt(k, KNAME[k])).join("")}</select></label>
    <label>Contains<input id="ft" type="search" placeholder="e.g. Area Authority"></label>
  </div><p class="muted small" id="cnt"></p><div id="res"></div>`);
  const run = () => {
    const e = $("#fe").value, s = $("#fs").value, f = $("#ff").value, l = $("#fl").value, k = $("#fk").value, t = $("#ft").value.toLowerCase();
    $("#main .band").outerHTML = band(e ? +e : null);
    const r = WORK.filter((x) => (!e || x.tags.some((g) => elOf(g) === +e)) && (!s || x.d.system === s) && (!f || x.d.func === f) && (!l || x.d.layer === l) && (!k || x.b.k === k) && (!t || x.b.t.toLowerCase().includes(t)));
    $("#cnt").textContent = `${r.length} statements${r.length > 200 ? " (showing the first 200)" : ""}`;
    $("#res").innerHTML = r.slice(0, 200).map(stmtHTML).join("");
  };
  for (const id of ["fe", "fs", "ff", "fl", "fk", "ft"]) $("#" + id).oninput = run;
  if (q) $("#ft").value = q;
  run();
});

// ---------- gaps ----------
route(/^\/gaps$/, () => {
  const docReg = REG["DOC-REG-001"]; const planned = docReg.filter((d) => d.status === "Planned");
  const cell = (sys, layer) => {
    const iss = DOCS.filter((d) => d.system === sys && d.layer === layer).length;
    const pl = planned.filter((d) => d.system === sys && TYPE_LAYER[d.doc_id.split("-")[2]] === layer).length;
    if (iss) return `<td class="m${Math.min(3, iss)}" data-tip="${iss} issued${pl ? `, ${pl} planned` : ""}">${iss}${pl ? `<small> +${pl}</small>` : ""}</td>`;
    if (pl) return `<td class="mp" data-tip="${pl} planned, none issued">${pl}</td>`;
    return `<td class="m0" data-tip="Nothing issued or planned">–</td>`;
  };
  const noCtl = RISKS.filter((r) => !r.controls.split("; ").some((c) => CTL[c]?.status === "Active"));
  const plannedCtl = CTLS.filter((c) => c.status === "Planned");
  const noStep = CTLS.filter((c) => c.status === "Active" && !c.process_step);
  const refs = new Map(); for (const d of DOCS) for (const s of d.sections) for (const b of s.blocks) for (const r of b.r || []) if (!DOC[r]) refs.set(r, (refs.get(r) || new Set()).add(d.id));
  const pend = docReg.filter((d) => d.pending_revision);
  const thin = EXP.filter((x) => COV.get(x.id).n < 3);
  page(thin.map((x) => x.element), head("Gaps", "Where the written system does not yet reach. Everything here is worked out from the documents and registers, so it shrinks as documents are issued.") + `
  <div class="figures" style="margin-bottom:18px"><div><b>${thin.length}</b><span>expectations with fewer than 3 binding statements</span></div><div><b>${planned.length}</b><span>planned documents not yet issued</span></div><div><b>${noCtl.length}</b><span>risks with no documented control</span></div><div><b>${noStep.length}</b><span>controls not yet tied to a process step</span></div></div>
  <div class="panel" style="margin-bottom:18px"><h2>Systems against document layers</h2><p class="muted small">Number of issued documents, with planned in small type. Hatched cells: planned only. Dashed: nothing yet.</p>
    <div style="overflow:auto"><table class="matrix"><tr><th></th>${LAYERS.map((l) => `<th>${l}</th>`).join("")}</tr>
    ${Object.keys(D.protocol.systems).map((s) => `<tr><th>${sysEls(s).map((n) => `<span class="edot" style="--c:${ECOL[n]}"></span>`).join("")}${s} <span class="muted" style="font-weight:400">${esc(D.protocol.systems[s].name)}</span></th>${LAYERS.map((l) => cell(s, l)).join("")}</tr>`).join("")}</table></div></div>
  <div class="grid2">
    <div class="panel"><h2>Thinly covered expectations</h2><div class="scroll"><table class="t"><tr><th>Expectation</th><th class="n">Statements</th><th class="n">Docs</th></tr>
      ${thin.sort((a, b) => COV.get(a.id).n - COV.get(b.id).n).map((x) => `<tr><td><span class="edot" style="--c:${ECOL[x.element]}"></span><a href="#/exp/${x.id}">${x.id} ${esc(x.title)}</a></td><td class="n">${COV.get(x.id).n}</td><td class="n">${COV.get(x.id).docs.size}</td></tr>`).join("")}</table></div></div>
    <div class="panel"><h2>Risks with no documented control</h2><p class="muted small">The risk relies on documents that have no Control IDs yet, or on a document not yet written.</p><div class="scroll"><table class="t"><tr><th>Risk</th><th>Rating</th><th>Relies on</th></tr>
      ${noCtl.map((r) => `<tr><td><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)}</td><td>${rateChip(r.current_rating)}</td><td class="small">${r.legacy_control_docs ? docLink(r.legacy_control_docs) : r.controls ? r.controls.split("; ").map((c) => esc(CTL[c]?.doc_ref || c)).join("<br>") : "<span class='muted'>Nothing written</span>"}</td></tr>`).join("")}</table></div></div>
    <div class="panel"><h2>Planned controls</h2><table class="t"><tr><th>Control</th><th>Waiting for</th></tr>${plannedCtl.map((c) => `<tr><td>${ctlChip(c.control_id)} ${esc(c.statement)}</td><td class="small">${esc(c.doc_ref)}</td></tr>`).join("")}</table></div>
    <div class="panel"><h2>Revisions in progress</h2><table class="t"><tr><th>Document</th><th>Revision</th><th>Change</th><th>Target</th></tr>${pend.map((d) => `<tr><td>${docLink(d.doc_id)} ${esc(d.title)}</td><td>${esc(d.pending_revision)}</td><td>${esc(d.pending_moc)}</td><td>${fmt(toDate(d.target_issue))}</td></tr>`).join("")}</table></div>
    <div class="panel"><h2>References to documents not yet issued</h2><div class="scroll"><table class="t"><tr><th>Referenced</th><th>Status</th><th>Referenced by</th></tr>
      ${[...refs].sort().map(([r, by]) => { const p = docReg.find((d) => d.doc_id === r); return `<tr><td>${esc(r)}<div class="small muted">${esc(p?.title || "")}</div></td><td class="small">${p ? "Planned " + fmt(toDate(p.target_issue)) : "<b>Not in any register</b>"}</td><td class="small">${[...by].map((d) => docLink(d)).join(", ")}</td></tr>`; }).join("")}</table></div></div>
    <div class="panel"><h2>Documents naming people who have left or moved</h2><p class="muted small">Read from the staff list. Documents should name roles; where they name people, the names go stale.</p><table class="t"><tr><th>Document</th><th>Field</th><th>Now</th></tr>
      ${STALE.map((x) => `<tr><td>${docLink(x.d.id)}</td><td class="small">${MNAME[x.f]}: ${esc(x.w.raw)}</td><td class="small">${staleNote(x.w)}</td></tr>`).join("") || `<tr><td class="muted">None.</td></tr>`}</table></div>
    <div class="panel"><h2>Documents waiting for automatic fix</h2><p class="muted small">They pass the protocol after the ONE Fix tool runs.</p><table class="t"><tr><th>Document</th><th>What Fix will correct</th></tr>
      ${Object.entries(D.gate).filter(([, g]) => g.outcome === "PASS_AFTER_FIX").map(([id, g]) => `<tr><td>${docLink(id)}</td><td class="small">${g.findings.filter((f) => f.sev === "error").map((f) => esc(f.msg)).join("<br>")}</td></tr>`).join("")}</table></div>
  </div>`);
});

// ---------- barriers ----------
route(/^\/barriers$/, () => {
  const act = CTLS.filter((c) => c.status === "Active"); const bars = act.filter(isBarrier), checks = act.filter((c) => !isBarrier(c));
  const withBars = RISKS.map((r) => ({ r, cs: r.controls.split("; ").map((c) => CTL[c]).filter((c) => c && isBarrier(c)) })).filter((x) => x.cs.length)
    .sort((a, b) => "VHML".indexOf(a.r.current_rating[0]) - "VHML".indexOf(b.r.current_rating[0]) || b.cs.length - a.cs.length);
  const bx = (c) => `<div class="barrier ${c.status === "Planned" ? "planned" : ""}" style="--hc:var(--${{ Effective: "eff", Degraded: "deg", Failed: "fail" }[c.health] || "nt"})" data-tip="<b>${c.control_id}</b>${esc(c.health)}${c.health_date ? " since " + fmt(toDate(c.health_date)) : ""}<br>${esc(c.evidence)}"><span class="edot" style="--c:${ECOL[ctlEl(c)]}"></span><div><a href="#/control/${c.control_id}">${c.control_id}</a> ${esc(c.barrier || c.statement.slice(0, 90) + (c.statement.length > 90 ? "…" : ""))}</div></div>`;
  const checkBy = {}; for (const c of checks) (checkBy[c.control_id.split("-")[1]] ||= []).push(c);
  page([5, 6, 8], head("Barriers", "A control is a binding statement in a document, with an ID, an owner and evidence that it works. Barriers stand between a hazard and harm. Management checks keep the system itself honest. Colours on the left edge show health from tests and events.") + `
  <div class="figures" style="margin-bottom:18px"><div><b>${bars.length}</b><span>barriers in force</span></div><div><b>${checks.length}</b><span>management checks</span></div>
    ${HEALTH.map(([h]) => `<div><b><span class="dot ${hcls(h)}"></span>${bars.filter((c) => c.health === h).length}</b><span>barriers ${h.toLowerCase()}</span></div>`).join("")}</div>
  <div class="tabs"><a class="on" href="#/barriers">Bow-ties by hazard</a><a href="#/controls">All controls</a></div>
  ${withBars.map(({ r, cs }) => { const pre = cs.filter((c) => c.position === "Preventive"), mit = cs.filter((c) => c.position !== "Preventive");
    return `<div class="bt-card"><div class="top"><h3 style="margin:0"><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)}</h3><span>${rateChip(r.current_rating)} <span class="small muted">${esc(D.protocol.sites[r.site] || r.site)}, owner ${esc(nameOf(r.owner))}</span></span></div>
      <div class="bowtie"><div class="side"><h3>Threats</h3><p class="small muted">${esc(r.threats)}</p>${pre.map(bx).join("") || `<p class="small muted">No preventive barrier with an ID.</p>`}</div>
        <div class="knot">${esc(r.top_event)}<div class="small muted" style="font-weight:400;margin-top:6px">${esc(r.hazard)}</div></div>
        <div class="side"><h3>Consequences</h3><p class="small muted">${esc(r.consequences)}</p>${mit.map(bx).join("") || `<p class="small muted">No mitigating barrier with an ID yet.</p>`}</div></div></div>`; }).join("")}
  <div class="panel"><h2>Management checks</h2><p class="small muted">Approvals, reviews and records that make sure the system runs as written.</p>
    ${Object.entries(checkBy).map(([s, cs]) => `<h3 style="margin-top:12px">${esc(s)} ${esc(D.protocol.systems[s]?.name || "")}</h3>${cs.map((c) => ctlChip(c.control_id)).join("")}`).join("")}</div>`);
});

// ---------- risks ----------
const LS = "EDCBA";
route(/^\/risk$/, () => {
  const H = REG["RSK-REG-001_history"];
  const dates = [...new Set(H.map((h) => h.date))].sort(); const COLOR = { L: "var(--low)", M: "var(--med)", H: "var(--high)", V: "var(--vhigh)" };
  const MAT = { E: "MHHVV", D: "MMHHV", C: "LMMHH", B: "LLMMH", A: "LLLMM" };
  const state = (d) => { const s = {}; for (const h of H) if (h.date <= d) s[h.risk_id] = h; return s; };
  page(5, head("Risks", "The ACE Risk Matrix from the Risk Management Standard, with every risk in the register. Press play to see risks move as events happen and controls are restored.") + `
  <div class="grid2" style="grid-template-columns:minmax(0,1.1fr) minmax(0,1fr)">
    <div class="panel"><div class="heat" id="heat">${LS.split("").map((l) => `<div class="ax">${({ E: "E Expected", D: "D Likely", C: "C Possible", B: "B Unlikely", A: "A Rare" })[l]}</div>${[1, 2, 3, 4, 5].map((c) => `<div class="c" style="background:${COLOR[MAT[l][c - 1]]};opacity:.55"></div>`).join("")}`).join("")}
      <div></div>${["1 Minor", "2 Moderate", "3 Serious", "4 Major", "5 Catastrophic"].map((c) => `<div class="ax x">${c}</div>`).join("")}<div class="rdots" id="rdots"></div></div>
      <div class="timeline"><button class="btn primary" id="play">Play</button><input id="slider" type="range" min="0" max="${dates.length}" value="${dates.length}" aria-label="Date"><span class="date-read" id="dread">Today</span></div>
      <p class="small muted" style="margin-top:8px">Likelihood up the side, consequence along the bottom. Each circle is a risk.</p></div>
    <div class="panel"><h2>Register</h2><div class="scroll"><table class="t"><tr><th>Risk</th><th>Site</th><th>Now</th><th>After actions</th></tr>
      ${[...RISKS].sort((a, b) => "VHML".indexOf(a.current_rating[0]) - "VHML".indexOf(b.current_rating[0]) || a.risk_id.localeCompare(b.risk_id)).map((r) => `<tr><td>${[...riskEls(r)].slice(0, 2).map((n) => `<span class="edot" style="--c:${ECOL[n]}"></span>`).join("")}<a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)}</td><td>${r.site}</td><td>${rateChip(r.current_rating)}</td><td>${rateChip(r.residual_rating)}</td></tr>`).join("")}</table></div></div>
  </div>`);
  const box = $("#rdots"), heat = $("#heat");
  box.innerHTML = RISKS.map((r) => `<a class="rdot" href="#/risk/${r.risk_id}" id="d-${r.risk_id}" data-tip="<b>${r.risk_id}</b>${esc(r.title)}">${r.risk_id.split("-")[2]}</a>`).join("");
  const place = (st) => {
    const W = heat.clientWidth, x0 = 113, cw = (W - x0) / 5, ch = 77;
    const pos = RISKS.map((r) => { const s = st[r.risk_id] || { likelihood: r.current_l, consequence: r.current_c }; return { r, k: s.likelihood + s.consequence, col: +s.consequence - 1, row: LS.indexOf(s.likelihood) }; });
    const cnt = {}; for (const p of pos) cnt[p.k] = (cnt[p.k] || 0) + 1; const seen = {};
    for (const p of pos) {
      const k = cnt[p.k], cols = Math.max(1, Math.ceil(Math.sqrt(k * (cw / ch)))), rows = Math.ceil(k / cols);
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
  $("#play").onclick = () => { stopAll(); let i = 0; slider.value = 0; show(0); timers.push(setInterval(() => { i++; if (i > dates.length) return stopAll(); slider.value = i; show(i); }, 1100)); };
});

route(/^\/risk\/(R-[A-Z]{3}-\d+)$/, (id) => {
  const r = RISK[id]; if (!r) return go404();
  const ctl = r.controls.split("; ").filter(Boolean).map((c) => CTL[c]).filter(Boolean);
  const pre = ctl.filter((c) => c.position === "Preventive"), mit = ctl.filter((c) => c.position !== "Preventive");
  const bar = (c) => `<div class="barrier ${c.status === "Planned" ? "planned" : ""}" style="--hc:var(--${{ Effective: "eff", Degraded: "deg", Failed: "fail" }[c.health] || "nt"})"><span class="edot" style="--c:${ECOL[ctlEl(c)]};margin-top:5px"></span><div><a href="#/control/${c.control_id}">${c.control_id}</a> ${isBarrier(c) ? `<span class="kind k-ctl">Barrier</span>` : ""} ${esc(c.statement)}<div class="small muted">${c.status === "Planned" ? "Planned, " + esc(c.doc_ref) : esc(c.health) + ", " + esc(nameOf(c.owner))}</div></div></div>`;
  const ev = EVENTS.filter((e) => e.risk_ids.split("; ").includes(id)).sort((a, b) => b.date.localeCompare(a.date));
  const hist = REG["RSK-REG-001_history"].filter((h) => h.risk_id === id);
  page([...riskEls(r)], head(`${id} ${esc(r.title)}`, `${esc(r.level)} risk at <a href="#/site/${r.site}">${esc(D.protocol.sites[r.site] || r.site)}</a>. Owner ${whoHTML(r.owner)}. ${procOfRisk(r)}${r.restrictions ? "Restriction: " + esc(r.restrictions) + "." : ""}`, `<a href="#/risk">Risks</a>`,
    `<div style="text-align:right"><div>Now ${rateChip(r.current_rating)} <span class="small muted">${r.current_l}${r.current_c}</span></div><div style="margin-top:4px">After actions ${rateChip(r.residual_rating)} <span class="small muted">${r.residual_l}${r.residual_c}</span></div></div>`) + `
  <div class="panel" style="margin-bottom:18px"><div class="bowtie">
    <div class="side"><h3>Threats</h3>${r.threats.split(";").map((t) => `<div class="small" style="margin-bottom:4px">${esc(t.trim())}</div>`).join("")}<h3 style="margin-top:12px">Preventive controls</h3>${pre.map(bar).join("") || `<p class="muted small">None with Control IDs.</p>`}</div>
    <div class="knot">${esc(r.top_event)}<div class="small muted" style="font-weight:400;margin-top:6px">${esc(r.hazard)}</div></div>
    <div class="side"><h3>Consequences</h3>${r.consequences.split(";").map((t) => `<div class="small" style="margin-bottom:4px">${esc(t.trim())}</div>`).join("")}<h3 style="margin-top:12px">Mitigating controls</h3>${mit.map(bar).join("") || `<p class="muted small">None with Control IDs.</p>`}</div>
  </div>${r.legacy_control_docs ? `<p class="small" style="margin-top:12px">Controls are also written in ${docLink(r.legacy_control_docs)}, which has no Control IDs yet.</p>` : ""}</div>
  <div class="grid2"><div class="panel"><h2>Consequence by domain</h2><table class="t"><tr><th>People</th><th>Environment</th><th>Asset and production</th><th>Reputation</th></tr><tr><td class="n">${r.c_people}</td><td class="n">${r.c_environment}</td><td class="n">${r.c_asset}</td><td class="n">${r.c_reputation}</td></tr></table>
    <h3 style="margin-top:14px">Rating history</h3><ul class="events">${hist.map((h) => `<li><span class="muted">${fmt(toDate(h.date))}</span><span>${rateChip(h.rating)} ${h.likelihood}${h.consequence} ${esc(h.reason)}</span></li>`).join("")}</ul>
    <p class="small muted" style="margin-top:10px">Accepted by ${esc(r.acceptance_authority)}${r.expiry ? `, expires ${fmt(toDate(r.expiry))}` : ""}. Reviewed ${esc(r.review_frequency.toLowerCase())}; last ${fmt(toDate(r.last_review))}.</p></div>
    <div class="panel"><h2>Events</h2><ul class="events">${ev.slice(0, 25).map((e) => `<li><span class="muted">${fmt(toDate(e.date))}</span><span>${esc(e.title)} <span class="small muted">${esc(e.type)}</span>${e.controls_failed ? `<div class="small">Failed: ${e.controls_failed.split("; ").map(ctlChip).join("")}</div>` : ""}${e.controls_tested ? `<div class="small">Worked: ${e.controls_tested.split("; ").map(ctlChip).join("")}</div>` : ""}</span></li>`).join("") || `<li><span></span><span class="muted">No events recorded against this risk.</span></li>`}</ul></div></div>`);
});

// ---------- controls ----------
route(/^\/controls$/, () => {
  const cnt = (h) => CTLS.filter((c) => c.health === h).length;
  page(5, head("Controls", "Each control is a RiskControl statement in a document with a Control ID. Health comes from tests, samples and events.") + `
  <div class="figures" style="margin-bottom:18px">${HEALTH.map(([h]) => `<div><b><span class="dot ${hcls(h)}"></span>${cnt(h)}</b><span>${h}</span></div>`).join("")}</div>
  <div class="tabs"><a href="#/barriers">Bow-ties by hazard</a><a class="on" href="#/controls">All controls</a></div>
  <div class="filters"><label>Element<select id="fe"><option value="">All</option>${ELS.map((e) => `<option value="${e.id}">${e.id}. ${esc(e.title)}</option>`).join("")}</select></label>
    <label>Kind<select id="fb"><option value="">All</option><option value="b">Barriers</option><option value="m">Management checks</option></select></label>
    <label>Health<select id="fh"><option value="">All</option>${HEALTH.map(([h]) => `<option>${h}</option>`).join("")}</select></label>
    <label>Status<select id="fst"><option value="">All</option><option>Active</option><option>Planned</option></select></label></div>
  <div class="panel"><table class="t" id="ct"></table></div>`);
  const run = () => { const e = $("#fe").value, b = $("#fb").value, h = $("#fh").value, st = $("#fst").value;
    $("#ct").innerHTML = `<tr><th>Control</th><th>Statement</th><th>Risk</th><th>Written in</th><th>Owner</th></tr>` + CTLS.filter((c) => (!e || ctlEl(c) === +e) && (!b || (b === "b") === isBarrier(c)) && (!h || c.health === h) && (!st || c.status === st)).map((c) => {
      const [doc, bm] = c.doc_ref.split("#"); return `<tr><td><span class="edot" style="--c:${ECOL[ctlEl(c)]}"></span>${ctlChip(c.control_id)}</td><td>${isBarrier(c) ? `<span class="kind k-ctl">Barrier</span> ` : ""}${esc(c.statement)}</td><td><a href="#/risk/${c.risk_id}">${c.risk_id}</a></td><td class="small">${c.status === "Planned" ? esc(c.doc_ref) : docLink(doc, bm)}</td><td class="small">${whoHTML(c.owner)}</td></tr>`; }).join(""); };
  for (const id of ["fe", "fb", "fh", "fst"]) $("#" + id).oninput = run; run();
});
route(/^\/control\/(C-[A-Z]{3}-\d{3})$/, (id) => {
  const c = CTL[id]; if (!c) return go404();
  const [doc, bm] = c.doc_ref.split("#"); const sec = SEC[`${doc}#${bm}`];
  const para = sec?.s.blocks.find((b) => (b.c || []).includes(id));
  const hist = REG["RSK-REG-002_health"].filter((h) => h.control_id === id);
  const ev = EVENTS.filter((e) => (e.controls_failed + "; " + e.controls_tested).split("; ").includes(id));
  page(ctlEl(c), head(`<span class="dot ${hcls(c.health)}" style="width:14px;height:14px"></span>${id}`, `${isBarrier(c) ? "Barrier. " : "Management check. "}${esc(c.statement)}`, `<a href="#/controls">Controls</a>`) + `
  <div class="grid2"><div class="panel"><h2>Where it is written</h2>${para ? `<div class="blk k-ctl">${esc(para.t)}</div><p class="small">${docLink(doc, bm, `${doc}, ${sec.s.title}`)} ${tagChips(sec.s.tags)}</p>` : `<p class="muted">${esc(c.doc_ref)}</p>`}
    <table class="t" style="margin-top:10px"><tr><td>Risk</td><td><a href="#/risk/${c.risk_id}">${c.risk_id}</a> ${esc(RISK[c.risk_id]?.title || "")}</td></tr><tr><td>Type</td><td>${esc(c.position)}, ${esc(c.nature.toLowerCase())}${c.critical === "Yes" ? ", critical" : ""}</td></tr>
    <tr><td>Owner</td><td>${whoHTML(c.owner)}</td></tr><tr><td>Evidence</td><td>${esc(c.evidence)}</td></tr><tr><td>Process step</td><td>${procStepCell(id, c)}</td></tr>
    ${c.barrier ? `<tr><td>Barrier</td><td>${esc(c.barrier)}</td></tr>` : ""}${c.sce_id ? `<tr><td>Safety-critical element</td><td>${esc(c.sce_id)}</td></tr>` : ""}</table></div>
  <div class="panel"><h2>Health over time</h2><ul class="events">${hist.map((h) => `<li><span class="muted">${fmt(toDate(h.date))}</span><span><span class="dot ${hcls(h.health)}"></span>${esc(h.health)} <span class="small muted">${esc(h.note)}</span></span></li>`).join("") || `<li><span></span><span class="muted">Not yet in force.</span></li>`}</ul>
    ${ev.length ? `<h3 style="margin-top:14px">Events</h3><ul class="events">${ev.map((e) => `<li><span class="muted">${fmt(toDate(e.date))}</span><span>${esc(e.title)}</span></li>`).join("")}</ul>` : ""}</div></div>`);
});

// ---------- technical authority ----------
route(/^\/authority(?:\/(.+))?$/, (who) => {
  const vp = PEOPLE.find((p) => p.t === "VP Engineering & Projects" && p.st !== "Left");
  const leads = PEOPLE.filter((p) => p.dl === vp.id && p.disc && p.st !== "Left");
  const fns = [...new Set(leads.map((p) => p.f))];
  const FC = ["#0B5563", "#C8402F", "#3D4FA1", "#6E9A2E", "#7A4FA0", "#D6A21E", "#5B6B73"];
  const cx = 360, cy = 330; let svg = "";
  const N = leads.length; const sorted = fns.flatMap((f) => leads.filter((p) => p.f === f));
  sorted.forEach((p, k) => {
    const a = -Math.PI / 2 + (k / N) * 2 * Math.PI, R = 245, x = cx + R * Math.cos(a), y = cy + R * Math.sin(a), col = FC[fns.indexOf(p.f) % FC.length];
    const right = Math.cos(a) >= 0, lx = cx + (R + 16) * Math.cos(a), ly = cy + (R + 16) * Math.sin(a);
    svg += `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}"/><g class="node" data-n="${esc(p.n)}" data-tip="<b>${esc(p.n)}</b>${esc(p.t)}<br>${esc(p.f)}"><circle cx="${x}" cy="${y}" r="9" fill="${col}"/><text x="${lx}" y="${ly + 4}" text-anchor="${right ? "start" : "end"}">${esc(p.t.replace(/ Lead$/, ""))}</text></g>`;
  });
  svg += `<circle cx="${cx}" cy="${cy}" r="70" fill="#fff" stroke="#17262E" stroke-width="1.5"/><text class="fn" x="${cx}" y="${cy - 8}" text-anchor="middle">Technical Leadership</text><text class="fn" x="${cx}" y="${cy + 10}" text-anchor="middle">Council</text><text x="${cx}" y="${cy + 30}" text-anchor="middle">Chair: ${esc(vp.n)}</text>`;
  page([3, 6], head("Technical authority", `The ${N} discipline leads keep their line in their own function and hold a dotted line to the VP Engineering &amp; Projects through the Technical Leadership Council. Select a lead to see the documents, controls and risks they hold.`) + `
  <div class="grid2" style="grid-template-columns:minmax(0,1.15fr) minmax(0,1fr)"><div class="panel"><svg class="tlc" viewBox="-110 0 940 660">${svg}</svg>
    <div class="chips">${fns.map((f, k) => `<span class="chip"><span class="dot" style="background:${FC[k % FC.length]}"></span>${esc(f)}</span>`).join("")}</div></div>
    <div class="panel" id="who"><h2>Select a discipline lead</h2><p class="muted">Each lead is the Technical Authority for their discipline: they own its standards, endorse changes and approve technical deviations.</p></div></div>`);
  const showP = (n) => {
    const p = PBY[n]; if (!p) return; for (const g of $$(".tlc .node")) g.classList.toggle("on", g.dataset.n === n);
    const roles = []; for (const d of DOCS) for (const [k, l] of [["author", "Author"], ["owner", "Owner"], ["approver", "Approver"], ["custodian", "Custodian"], ["reviewers", "Reviewer"], ["endorser", "Endorser"]]) if ((d[k] || "").includes(n)) roles.push([d, l]);
    const ctls = CTLS.filter((c) => c.owner.startsWith(n)); const risks = RISKS.filter((r) => r.owner.startsWith(n));
    const title = p.t.replace(/ \(.*\)$/, "");
    const mentions = STMTS.filter((s) => s.b.t.includes(title) || s.b.t.includes(n)).slice(0, 12);
    const mgr = PID[p.to];
    $("#who").innerHTML = `<h2>${esc(p.n)}</h2><p>${esc(p.t)}<br><span class="muted small">${esc(p.f)}, reports to ${esc(mgr ? mgr.n + ", " + mgr.t : "")}</span></p>
      <h3 style="margin-top:12px">Documents</h3>${roles.length ? `<table class="t">${roles.map(([d, l]) => `<tr><td>${docLink(d.id)} ${esc(d.title)}</td><td class="small muted">${l}</td></tr>`).join("")}</table>` : `<p class="muted small">Not named on any issued document yet.</p>`}
      ${ctls.length ? `<h3 style="margin-top:12px">Controls owned</h3>${ctls.map((c) => ctlChip(c.control_id)).join("")}` : ""}
      ${risks.length ? `<h3 style="margin-top:12px">Risks owned</h3>${risks.map((r) => `<a class="chip" href="#/risk/${r.risk_id}">${r.risk_id}</a>`).join("")}` : ""}
      ${mentions.length ? `<h3 style="margin-top:12px">Named in binding statements</h3>${mentions.map(stmtHTML).join("")}` : ""}`;
  };
  $(".tlc").addEventListener("click", (e) => { const g = e.target.closest(".node"); if (g) showP(g.dataset.n); });
  if (who) showP(who);
});

// ---------- library: by element (virtual manual), tree, list ----------
const libTabs = (on) => `<div class="tabs">${[["el", "By element", "#/library/el/1"], ["tree", "Document tree", "#/library/tree"], ["map", "Document map", "#/library/map"], ["list", "List", "#/library/list"]].map(([k, l, h]) => `<a class="${on === k ? "on" : ""}" href="${h}">${l}</a>`).join("")}</div>`;
route(/^\/library$/, () => { location.replace("#/library/el/1"); });
route(/^\/library\/el\/(\d+)$/, (n) => {
  n = +n; const e = EL[n]; if (!e) return go404(); const c = ECOL[n];
  const ex = EXP.filter((x) => x.element === n);
  // a section joins the virtual manual under the expectation it leads with (its first tag); the Manual contributes its own expectation section
  const parts = ex.map((x) => ({ x, secs: DOCS.flatMap((d) => d.sections.filter((s) => d.id === MAN.id ? s.bm === `s${x.id.replace(".", "_")}` : s.tags[0] === x.id).map((s) => ({ d, s }))).sort((a, b) => LORDER.indexOf(a.d.layer) - LORDER.indexOf(b.d.layer) || a.d.id.localeCompare(b.d.id)) }));
  const also = (x) => DOCS.filter((d) => d.id !== MAN.id && d.sections.some((s) => s.tags.indexOf(x.id) > 0) && !d.sections.some((s) => s.tags[0] === x.id));
  const docSet = new Set(parts.flatMap((p) => p.secs.map((q) => q.d.id))); const nSec = parts.reduce((a, p) => a + p.secs.length, 0);
  page(n, head(`Element ${n} as one manual`, `${esc(e.title)}, assembled from ${plural(nSec, "section")} in ${plural(docSet.size, "document")}. Each section stays in its own document; this view gathers them under the expectation each one leads with.`, `<a href="#/library">Library</a>`) + libTabs("el") + `
  <div class="chips" style="margin-bottom:16px">${ELS.map((x) => `<a class="echip${x.id === n ? " on" : ""}" style="--c:${ECOL[x.id]}" href="#/library/el/${x.id}"><b style="color:${ON(x.id)}">${x.id}</b>${SHORT[x.id]}</a>`).join("")}</div>
  ${parts.map(({ x, secs }) => `<h2 style="margin-top:22px"><span style="color:${c}">${x.id}</span> ${esc(x.title)} <span class="small muted" style="font-weight:400">${plural(secs.length, "section")}</span></h2>
    ${secs.map(({ d, s }, i) => { const nb = s.blocks.filter((b) => BIND.has(b.k)).length; const newDoc = !i || secs[i - 1].d.id !== d.id;
      return `${newDoc ? `<div class="small" style="margin:12px 0 4px"><b>${esc(d.layer)}</b> ${docLink(d.id, "", d.id)} ${esc(d.title)}</div>` : ""}<details class="vm-sec" style="--c:${c}" ${d.id === MAN.id ? "open" : ""}><summary><b>${esc(s.title)}</b> ${nb ? `<span class="small muted">${plural(nb, "binding statement")}</span>` : ""}</summary>
        <div class="vm-body">${s.blocks.map(blockHTML).join("")}<p class="small">${tagChips(s.tags)} ${docLink(d.id, s.bm, "Open in the document")}</p></div></details>`; }).join("") || `<p class="muted small">No section in any document leads with ${x.id} yet.</p>`}
    ${also(x).length ? `<p class="small muted">Also touched in ${also(x).map((d) => docLink(d.id)).join(", ")}</p>` : ""}`).join("")}`);
});
const parentOf = (d) => { if (d.id === MAN.id) return null; const p = (d.parent.match(/ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?/) || [])[0]; return p && DOC[p] ? p : MAN.id; };
route(/^\/library\/tree$/, () => {
  const kids = {}; for (const d of DOCS) { const p = parentOf(d); if (p) (kids[p] ||= []).push(d); }
  for (const k in kids) kids[k].sort((a, b) => LORDER.indexOf(a.layer) - LORDER.indexOf(b.layer) || a.id.localeCompare(b.id));
  const node = (d, depth) => `<li><details ${depth < 1 ? "open" : ""}><summary><span class="lay">${esc(d.layer)}</span>${wordIcon(d.id)}<a href="#/doc/${d.id}">${esc(d.id)}</a> <span>${esc(d.title)}</span> ${fpBar(d.id)} <span class="small muted">${(kids[d.id] || []).length ? plural(kids[d.id].length, "child document") : ""}</span></summary>
    <div class="secs">${(d.id === MAN.id ? [] : d.sections.filter((s) => s.level === 1)).map((s) => `<a href="#/doc/${d.id}/${s.bm}" style="--c:${s.tags[0] ? ECOL[elOf(s.tags[0])] : "var(--line)"}"><i></i>${esc(s.title)}</a>`).join("")}</div>
    ${(kids[d.id] || []).length ? `<ul>${kids[d.id].map((k) => node(k, depth + 1)).join("")}</ul>` : ""}</details></li>`;
  page(null, head("Document tree", "From the OMS Manual down through policies, standards, practices and procedures. Expand a document to see its sections, coloured by the element each one serves.", `<a href="#/library">Library</a>`) + libTabs("tree") + `<div class="panel tree"><ul>${node(MAN, 0)}</ul></div>`);
});
route(/^\/library\/list$/, () => {
  const reg = REG["DOC-REG-001"];
  page(null, head("Library", "Issued documents read directly from the repository, and the planned documents still to come.") + libTabs("list") + `
  <div class="filters"><label>Element<select id="fe"><option value="">All</option>${ELS.map((e) => `<option value="${e.id}">${e.id}. ${esc(e.title)}</option>`).join("")}</select></label><label>Layer<select id="fl"><option value="">All</option>${LAYERS.map((l) => `<option>${l}</option>`).join("")}</select></label>
  <label>Show<select id="fx"><option value="">Issued and planned</option><option value="i">Issued only</option><option value="p">Planned only</option></select></label></div>
  <div class="panel"><table class="t" id="lt"></table></div>`);
  const run = () => { const e = $("#fe").value, l = $("#fl").value, x = $("#fx").value;
    const issued = x === "p" ? [] : DOCS.filter((d) => (!l || d.layer === l) && (!e || FP[d.id][e]));
    const planned = x === "i" || e ? [] : reg.filter((d) => d.status === "Planned" && (!l || TYPE_LAYER[d.doc_id.split("-")[2]] === l));
    $("#lt").innerHTML = `<tr><th>Number</th><th>Title</th><th>Elements</th><th>Layer</th><th>Rev</th><th>Effective</th><th>Owner</th><th>Gateway</th></tr>` +
      issued.sort((a, b) => a.id.localeCompare(b.id)).map((d) => `<tr><td style="white-space:nowrap">${wordIcon(d.id)} ${docLink(d.id)}</td><td>${esc(d.title)}</td><td>${fpBar(d.id)}</td><td>${d.layer}</td><td>${esc(d.revision)}</td><td class="num">${fmt(d.eff)}</td><td class="small">${whoHTML(d.owner)}</td><td>${gateChip(d.id)}</td></tr>`).join("") +
      planned.map((d) => `<tr style="color:var(--ink-3)"><td>${esc(d.doc_id)}</td><td>${esc(d.title)}</td><td></td><td>${TYPE_LAYER[d.doc_id.split("-")[2]] || ""}</td><td></td><td class="small">Planned ${fmt(toDate(d.target_issue))}</td><td class="small">${esc(nameOf(d.owner))}</td><td></td></tr>`).join(""); };
  for (const id of ["fe", "fl", "fx"]) $("#" + id).oninput = run; run();
});

// ---------- comments and suggested edits (shared through the ONE API, kept in this browser if it cannot be reached) ----------
const NS = {
  online: null, mem: [],
  local() { try { return JSON.parse(localStorage.getItem("one-notes") || "[]"); } catch { return this.mem; } },
  save(a) { this.mem = a; try { localStorage.setItem("one-notes", JSON.stringify(a)); } catch { /* storage unavailable */ } },
  async call(path, opt = {}) {
    if (this.online === false || !D.api) throw new Error("offline");
    const ac = new AbortController(); const t = setTimeout(() => ac.abort(), 6000);
    try { const r = await fetch(D.api + path, { ...opt, signal: ac.signal, headers: { "content-type": "application/json" } }); if (!r.ok) throw new Error("HTTP " + r.status); this.online = true; return await r.json(); }
    catch (e) { if (this.online !== true) this.online = false; throw e; } finally { clearTimeout(t); }
  },
  async list(doc) { try { return await this.call("/notes" + (doc ? "?doc=" + encodeURIComponent(doc) : "")); } catch { return this.local().filter((n) => !doc || n.doc === doc); } },
  async add(n) {
    try { return await this.call("/notes", { method: "POST", body: JSON.stringify(n) }); }
    catch { const x = { ...n, id: "L" + Date.now().toString(36), created: new Date().toISOString(), status: "open", replies: [] }; const a = this.local(); a.push(x); this.save(a); return x; }
  },
  async reply(id, body, author) {
    try { return await this.call(`/notes/${id}/reply`, { method: "POST", body: JSON.stringify({ body, author }) }); }
    catch { const a = this.local(); const n = a.find((x) => x.id === id); if (n) { (n.replies ||= []).push({ author, body, created: new Date().toISOString() }); this.save(a); } return n; }
  },
  async status(id, status, by) {
    try { return await this.call(`/notes/${id}/status`, { method: "POST", body: JSON.stringify({ status, by }) }); }
    catch { const a = this.local(); const n = a.find((x) => x.id === id); if (n) { n.status = status; n.statusBy = by; n.statusAt = new Date().toISOString(); this.save(a); } return n; }
  },
};
const ME = { get name() { try { return localStorage.getItem("one-name") || ""; } catch { return ""; } }, set name(v) { try { localStorage.setItem("one-name", v); } catch { /* ignore */ } },
  get owner() { try { return localStorage.getItem("one-owner") === "1"; } catch { return false; } }, set owner(v) { try { localStorage.setItem("one-owner", v ? "1" : "0"); } catch { /* ignore */ } } };
async function refreshNoteCount() { const all = await NS.list(); const open = all.filter((n) => n.status === "open").length; const el = $("#navNotes"); if (el) el.textContent = open || ""; }

// word-level difference, used for the on-screen preview and for Word tracked changes
const tokens = (s) => s.match(/\s+|C-[A-Z]{3}-\d{3}|ACE-[A-Z]{3}-[A-Z]{3}-\d{3}|[\p{L}\p{N}][\p{L}\p{N}'’-]*|[^\s]/gu) || [];
function diffTokens(a, b) {
  const n = a.length, m = b.length, L = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1));
  for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) L[i][j] = a[i] === b[j] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
  const out = []; let i = 0, j = 0;
  const push = (t, s, ai) => { const l = out[out.length - 1]; if (l && l.t === t && ai == null && l.ai == null) l.s += s; else out.push({ t, s, ai }); };
  while (i < n && j < m) { if (a[i] === b[j]) { out.push({ t: "=", s: a[i], ai: i }); i++; j++; } else if (L[i + 1][j] >= L[i][j + 1]) { out.push({ t: "-", s: a[i], ai: i }); i++; } else { push("+", b[j]); j++; } }
  while (i < n) { out.push({ t: "-", s: a[i], ai: i }); i++; } while (j < m) { push("+", b[j]); j++; }
  return out;
}
const diffHTML = (a, b) => `<span class="diff">${diffTokens(tokens(a), tokens(b)).map((o) => o.t === "=" ? esc(o.s) : o.t === "-" ? `<del>${esc(o.s)}</del>` : `<ins>${esc(o.s)}</ins>`).join("")}</span>`;
const when = (iso) => { const d = new Date(iso); return isNaN(d) ? "" : `${fmt(d)} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`; };
const ST = { open: "Open", accepted: "Accepted", rejected: "Rejected", resolved: "Resolved" };
function noteHTML(n, opts = {}) {
  const sec = SEC[`${n.doc}#${n.bm}`];
  return `<div class="note ${n.kind} ${n.status}" data-note="${esc(n.id)}">
    <div class="meta"><span><span class="who">${esc(n.author || "Anonymous")}</span> ${n.kind === "suggestion" ? "suggested an edit" : "commented"}</span><span>${when(n.created)} <span class="st ${n.status}">${ST[n.status] || n.status}</span></span></div>
    ${opts.where ? `<div class="small" style="margin:4px 0">${docLink(n.doc, n.bm, `${n.doc}, ${sec ? sec.s.title : n.bm}`)}</div>` : ""}
    ${n.kind === "suggestion" ? `<div style="margin:6px 0">${diffHTML(n.quote, n.newText)}</div>` : `<div class="small muted" style="margin:4px 0;border-left:2px solid var(--line);padding-left:6px">${esc((n.quote || "").slice(0, 160))}${(n.quote || "").length > 160 ? "…" : ""}</div>`}
    ${n.body ? `<div>${esc(n.body)}</div>` : ""}
    ${n.statusBy ? `<div class="small muted">${ST[n.status]} by ${esc(n.statusBy)} ${when(n.statusAt)}</div>` : ""}
    ${(n.replies || []).map((r) => `<div class="reply"><b>${esc(r.author || "Anonymous")}</b> <span class="small muted">${when(r.created)}</span><div>${esc(r.body)}</div></div>`).join("")}
    <div class="row"><button class="btn small" data-act="reply">Reply</button>${!opts.where ? `<button class="btn small" data-act="show">Show in text</button>` : ""}
      ${ME.owner && n.status === "open" ? (n.kind === "suggestion" ? `<button class="btn small" data-act="accepted">Accept</button><button class="btn small" data-act="rejected">Reject</button>` : `<button class="btn small" data-act="resolved">Resolve</button>`) : ""}
      ${ME.owner && n.status !== "open" ? `<button class="btn small" data-act="open">Reopen</button>` : ""}</div></div>`;
}
async function noteAction(btn, after) {
  const box = btn.closest("[data-note]"); const id = box.dataset.note; const act = btn.dataset.act;
  if (act === "show") return after?.("show", id);
  if (act === "reply") {
    if (box.querySelector(".editor")) return;
    box.insertAdjacentHTML("beforeend", `<div class="editor"><textarea aria-label="Reply" placeholder="Write a reply"></textarea><div class="row"><button class="btn small primary" data-x="send">Post reply</button><button class="btn small" data-x="cancel">Cancel</button></div></div>`);
    const ed = box.querySelector(".editor"); ed.querySelector("textarea").focus();
    ed.querySelector("[data-x=cancel]").onclick = () => ed.remove();
    ed.querySelector("[data-x=send]").onclick = async () => { const t = ed.querySelector("textarea").value.trim(); if (!t) return; await NS.reply(id, t, ME.name || "Anonymous"); toast("Reply posted"); after?.("changed", id); };
    return;
  }
  await NS.status(id, act, ME.name || "Document owner"); toast({ accepted: "Edit accepted", rejected: "Edit rejected", resolved: "Comment resolved", open: "Reopened" }[act]); after?.("changed", id);
}

// ---------- document reader ----------
function fpWheel(d) {
  const f = FP[d.id] || {}; const max = Math.max(1, ...Object.values(f)); const tot = Object.values(f).reduce((a, b) => a + b, 0) || 1;
  return `<svg class="fpwheel" viewBox="0 0 120 120" role="img" aria-label="Element fingerprint">${ELS.map((e) => { const [a0, a1] = segA(e.id); const v = f[e.id] || 0;
    return `<path d="${arc(60, 60, 22, 56, a0 + 0.02, a1 - 0.02)}" fill="#EEF2F3"/>${v ? `<path d="${arc(60, 60, 22, 22 + 34 * Math.sqrt(v / max), a0 + 0.02, a1 - 0.02)}" fill="${ECOL[e.id]}" data-tip="<b>${e.id}. ${esc(e.title)}</b>${v} binding statements (${Math.round(100 * v / tot)}%)" data-goel="${e.id}" style="cursor:pointer"/>` : ""}`; }).join("")}
    <text x="60" y="58" text-anchor="middle" font-size="12" font-weight="600" fill="#17262E">${tot}</text><text x="60" y="71" text-anchor="middle" font-size="7.5" fill="#4E5F68">statements</text></svg>`;
}
route(/^\/doc\/([A-Z0-9-]+)(?:\/(.+))?$/, (id, bm) => {
  const d = DOC[id]; if (!d) return go404();
  const reg = REG["DOC-REG-001"].find((x) => x.doc_id === id) || {}; const g = D.gate[id];
  const parent = parentOf(d); const children = DOCS.filter((x) => parentOf(x) === id);
  const secCol = (s) => s.tags[0] ? ECOL[elOf(s.tags[0])] : "var(--line-2)";
  page(FP[id], `<div class="crumb"><a href="#/library">Library</a> / <a href="#/library/tree">${esc(d.layer)}</a></div>
  <div class="titleblock"><div><h1 style="font-size:24px;display:flex;gap:12px;align-items:center">${wordIcon(id, true)}<span>${esc(d.title)}</span></h1><p class="muted" style="margin:6px 0 10px">${esc(d.subtitle)}</p>
    <dl><dt>Number</dt><dd>${esc(d.id)}</dd><dt>Revision</dt><dd>${esc(d.revision)} ${esc(d.status)}</dd><dt>Effective</dt><dd>${fmt(d.eff)}</dd><dt>Next review</dt><dd>${fmt(toDate(reg.next_review))}</dd>
    <dt>Owner</dt><dd>${whoHTML(d.owner)}</dd><dt>Author</dt><dd>${whoHTML(d.author)}</dd><dt>Parent</dt><dd>${parent ? docLink(parent) : "None"}</dd><dt>Gateway</dt><dd>${gateChip(id)}</dd></dl>
    ${STALE.filter((x) => x.d.id === id).map((x) => `<p class="small" style="margin:8px 0 0;color:var(--flare)">${MNAME[x.f]} names ${esc(x.w.name)}: ${staleNote(x.w)}. Update at the next revision.</p>`).join("")}
    ${children.length ? `<p class="small" style="margin:8px 0 0">Child documents: ${children.map((c) => docLink(c.id)).join(", ")}</p>` : ""}
    ${docProcLine(id)}
    ${reg.pending_revision ? `<p class="small" style="margin:8px 0 0;color:var(--flare)">Revision ${esc(reg.pending_revision)} in preparation under ${esc(reg.pending_moc)}, target ${fmt(toDate(reg.target_issue))}.</p>` : ""}</div>
    <div style="text-align:center">${fpWheel(d)}<div class="small muted">Which elements this document serves</div></div></div>
  <div class="reader"><nav class="toc panel" aria-label="Sections">${d.sections.map((s) => `<a class="l${s.level}" href="#/doc/${id}/${s.bm}" style="--c:${secCol(s)}"><i></i>${esc(s.title)}</a>`).join("")}</nav>
    <article class="doc-body" id="body">${d.sections.map((s) => `<section id="${esc(s.bm)}" style="--c:${secCol(s)}">${s.level === 1 ? `<h2>${esc(s.title)}</h2>` : `<h3>${esc(s.title)}</h3>`}<div class="tags">${tagChips(s.tags)}${secProcChips(id, s.bm)}</div>
      ${s.blocks.map((b, i) => b.k === "table" ? blockHTML(b) : `<div class="para" data-bm="${esc(s.bm)}" data-i="${i}"><div class="blk k-${b.k}">${blockInner(b)}</div><div class="acts"><button class="btn small" data-a="comment">Comment</button><button class="btn small" data-a="suggest">Suggest edit</button></div></div>`).join("")}</section>`).join("")}
    ${d.revisions.length ? `<section><h2>Revision history</h2><table>${d.revisions.map((r) => `<tr><td>${esc(r.rev)}</td><td>${esc(r.date)}</td><td>${esc(r.text)}</td></tr>`).join("")}</table></section>` : ""}
    ${g && g.findings.length ? `<section><h2>Gateway findings</h2>${g.findings.map((f) => `<div class="blk small"><b>${f.rule}</b> ${esc(f.sev)}${f.fix === "auto" ? " (automatic fix)" : ""}: ${esc(f.msg)}</div>`).join("")}</section>` : ""}</article>
    <aside class="notesbar panel" id="notes" aria-label="Comments and suggested edits"></aside></div>`);
  if (bm) { const t = document.getElementById(bm); if (t) { t.scrollIntoView({ block: "start" }); t.classList.add("hl"); } }
  setupNotes(d);
});

function setupNotes(d) {
  let notes = [], preview = false;
  const bar = $("#notes"), body = $("#body");
  const blockOf = (bm, i) => SEC[`${d.id}#${bm}`]?.s.blocks[i];
  const drawBar = () => {
    const open = notes.filter((n) => n.status === "open"), acc = notes.filter((n) => n.status === "accepted" && n.kind === "suggestion");
    bar.innerHTML = `<h2>Comments and edits</h2>
      ${NS.online === false ? `<div class="offline">The shared comment service is not connected yet, so these are kept in this browser only.</div>` : ""}
      <label>Your name<input type="text" id="myname" value="${esc(ME.name)}" placeholder="Shown on what you add"></label>
      <label class="switch"><input type="checkbox" id="owner" ${ME.owner ? "checked" : ""}> I am the document owner (demo)</label>
      <p class="small muted">Point at any paragraph to comment or suggest an edit. Nothing changes in the approved document until the owner accepts and issues a new revision in Word.</p>
      <div class="row" style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px"><button class="btn small" id="dlw" ${notes.some((n) => n.status !== "rejected" && n.status !== "resolved") ? "" : "disabled"}>Download for Word</button>
        <label class="switch" style="margin:0"><input type="checkbox" id="prev" ${preview ? "checked" : ""}> Show accepted edits in the text</label></div>
      <p class="small muted">${open.length} open, ${acc.length} accepted edit${acc.length === 1 ? "" : "s"} waiting for the next revision. <a href="#/review">All documents</a></p>
      <div id="nlist">${notes.length ? [...notes].sort((a, b) => (a.status === "open" ? 0 : 1) - (b.status === "open" ? 0 : 1) || b.created.localeCompare(a.created)).map((n) => noteHTML(n)).join("") : `<p class="muted small">No comments yet. Be the first.</p>`}</div>`;
    $("#myname").onchange = (e) => (ME.name = e.target.value.trim());
    $("#owner").onchange = (e) => { ME.owner = e.target.checked; drawBar(); };
    $("#prev").onchange = (e) => { preview = e.target.checked; drawBody(); };
    $("#dlw").onclick = () => exportWord(d, notes);
    $("#nlist").onclick = (e) => { const b = e.target.closest("button[data-act]"); if (b) noteAction(b, (what, nid) => { if (what === "show") { const n = notes.find((x) => x.id === nid); const p = body.querySelector(`.para[data-bm="${CSS.escape(n.bm)}"][data-i="${n.pidx}"]`); if (p) { p.scrollIntoView({ block: "center" }); p.classList.remove("hl"); void p.offsetWidth; p.classList.add("hl"); } } else load(); }); };
  };
  const drawBody = () => {
    for (const p of $$(".para", body)) {
      const b = blockOf(p.dataset.bm, +p.dataset.i); const mine = notes.filter((n) => n.bm === p.dataset.bm && n.pidx === +p.dataset.i && n.status !== "rejected");
      const acc = mine.filter((n) => n.kind === "suggestion" && n.status === "accepted").pop();
      p.querySelector(".blk").innerHTML = preview && acc ? blockInner(b, diffHTML(b.t, acc.newText)) : blockInner(b);
      p.querySelector(".badge")?.remove();
      const open = mine.filter((n) => n.status === "open").length;
      if (mine.length) p.insertAdjacentHTML("afterbegin", `<button class="badge" style="${open ? "" : "background:var(--eff)"}" data-tip="${open} open, ${mine.length - open} settled" aria-label="${mine.length} notes on this paragraph">${mine.length}</button>`);
    }
  };
  const load = async () => { notes = await NS.list(d.id); drawBar(); drawBody(); refreshNoteCount(); };
  body.addEventListener("click", (e) => {
    const badge = e.target.closest(".badge"); if (badge) { const p = badge.closest(".para"); const n = notes.find((x) => x.bm === p.dataset.bm && x.pidx === +p.dataset.i); const el = n && bar.querySelector(`[data-note="${CSS.escape(n.id)}"]`); if (el) { el.scrollIntoView({ block: "nearest" }); el.classList.remove("hl"); void el.offsetWidth; el.classList.add("hl"); } return; }
    const a = e.target.closest("button[data-a]"); if (!a) return;
    const p = a.closest(".para"); const b = blockOf(p.dataset.bm, +p.dataset.i); if (p.querySelector(".editor")) return;
    const sug = a.dataset.a === "suggest";
    p.insertAdjacentHTML("beforeend", `<div class="editor">${sug ? `<textarea aria-label="Suggested wording">${esc(b.t)}</textarea><div class="small muted" style="margin:4px 0">Preview of your edit</div><div class="small" data-x="pv"></div><input aria-label="Reason for the edit" placeholder="Why? (optional)" style="margin-top:6px">` : `<textarea aria-label="Comment" placeholder="Write a comment"></textarea>`}
      <div class="row" style="display:flex;gap:6px;margin-top:6px"><button class="btn small primary" data-x="save">${sug ? "Post suggested edit" : "Post comment"}</button><button class="btn small" data-x="cancel">Cancel</button></div></div>`);
    const ed = p.querySelector(".editor"), ta = ed.querySelector("textarea"); ta.focus();
    if (sug) { const pv = ed.querySelector("[data-x=pv]"); const upd = () => (pv.innerHTML = diffHTML(b.t, ta.value)); ta.oninput = upd; upd(); }
    ed.querySelector("[data-x=cancel]").onclick = () => ed.remove();
    ed.querySelector("[data-x=save]").onclick = async () => {
      const text = ta.value.trim(); if (!text) return;
      if (sug && text === b.t.trim()) return toast("Change the wording first");
      const lost = (b.c || []).filter((c) => !text.includes(c)); if (sug && lost.length) return toast(`Keep the Control ID ${lost.join(", ")} in the text`);
      if (!ME.name) { const nm = $("#myname").value.trim(); if (nm) ME.name = nm; }
      await NS.add({ doc: d.id, rev: d.revision, bm: p.dataset.bm, pidx: +p.dataset.i, quote: b.t, kind: sug ? "suggestion" : "comment", body: sug ? ed.querySelector("input").value.trim() : text, newText: sug ? text : "", author: ME.name || "Anonymous" });
      ed.remove(); toast(sug ? "Suggested edit posted" : "Comment posted"); load();
    };
  });
  drawBar(); load();
}

// ---------- master list of comments and edits ----------
route(/^\/review(?:\/(\w+))?$/, async (filter = "open") => {
  page(null, head("Comments and edits", "Everything people have said about the documents, kept beside them until the owner acts. Accepted edits wait here until the owner downloads them into Word and issues a new revision.") + `<div id="rv"><p class="muted">Loading…</p></div>`);
  const all = await NS.list(); refreshNoteCount();
  const byDoc = new Map(); for (const n of all) { if (!byDoc.has(n.doc)) byDoc.set(n.doc, []); byDoc.get(n.doc).push(n); }
  const shown = all.filter((n) => filter === "all" || n.status === filter).sort((a, b) => b.created.localeCompare(a.created));
  const cnt = (l, s, k) => l.filter((n) => n.status === s && (!k || n.kind === k)).length;
  if (!$("#rv")) return;
  $("#main .band").outerHTML = band(Object.fromEntries([...byDoc.keys()].flatMap((id) => Object.keys(FP[id] || {})).map((n) => [n, 1])));
  $("#rv").innerHTML = `${NS.online === false ? `<div class="offline">The shared comment service is not connected yet, so this list shows what was added in this browser.</div>` : ""}
  <div class="figures" style="margin-bottom:18px"><div><b>${cnt(all, "open", "comment")}</b><span>open comments</span></div><div><b>${cnt(all, "open", "suggestion")}</b><span>suggested edits waiting</span></div><div><b>${cnt(all, "accepted")}</b><span>accepted, waiting for Word</span></div><div><b>${byDoc.size}</b><span>documents with notes</span></div></div>
  <div class="grid2" style="grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);align-items:start">
    <div class="panel"><h2>By document</h2>${byDoc.size ? `<table class="t"><tr><th>Document</th><th class="n">Comments</th><th class="n">Edits</th><th class="n">Accepted</th></tr>${[...byDoc].sort((a, b) => cnt(b[1], "open") - cnt(a[1], "open")).map(([id, l]) => `<tr><td>${docLink(id)}<div class="small">${esc(DOC[id]?.title || "")}</div>${fpBar(id)}</td><td class="n">${cnt(l, "open", "comment")}</td><td class="n">${cnt(l, "open", "suggestion")}</td><td class="n">${cnt(l, "accepted")}</td></tr>`).join("")}</table>` : `<p class="muted">Nothing yet. Open any document in the library and point at a paragraph to add the first comment.</p>`}</div>
    <div class="panel"><div class="tabs">${[["open", "Open"], ["accepted", "Accepted"], ["rejected", "Rejected"], ["resolved", "Resolved"], ["all", "All"]].map(([k, l]) => `<a class="${filter === k ? "on" : ""}" href="#/review/${k}">${l}</a>`).join("")}</div>
      <label class="switch"><input type="checkbox" id="owner" ${ME.owner ? "checked" : ""}> I am the document owner (demo)</label>
      <div id="rlist">${shown.map((n) => noteHTML(n, { where: true })).join("") || `<p class="muted small">Nothing here.</p>`}</div></div></div>`;
  $("#owner").onchange = (e) => { ME.owner = e.target.checked; go(); };
  $("#rlist").onclick = (e) => { const b = e.target.closest("button[data-act]"); if (b) noteAction(b, () => go()); };
});

// ---------- Download for Word: tracked changes and Word comments written into the original document ----------
function loadJSZip() {
  if (window.JSZip) return Promise.resolve();
  return new Promise((ok, no) => { const s = document.createElement("script"); s.src = "https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"; s.onload = ok; s.onerror = () => no(new Error("Could not load the Word library")); document.head.appendChild(s); });
}
async function exportWord(d, notes) {
  const use = notes.filter((n) => n.status === "accepted" || n.status === "open");
  if (!use.length) return toast("Nothing to send to Word");
  try {
    toast("Preparing the Word file…"); await loadJSZip();
    const res = await fetch(`docs/${d.id}.docx`); if (!res.ok) throw new Error("The original Word file is only available on the published site");
    const zip = await JSZip.loadAsync(await res.arrayBuffer());
    const W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main", XMLNS = "http://www.w3.org/XML/1998/namespace";
    const dom = new DOMParser().parseFromString(await zip.file("word/document.xml").async("string"), "application/xml");
    const now = new Date().toISOString().replace(/\.\d+Z$/, "Z"); let rid = 7000, cid = 0; const comments = [];
    const mk = (tag, attrs = {}) => { const e = dom.createElementNS(W, "w:" + tag); for (const [k, v] of Object.entries(attrs)) e.setAttributeNS(W, "w:" + k, v); return e; };
    const norm = (s) => s.replace(/\s+/g, " ").trim();
    const kids = (el, tag) => [...el.childNodes].filter((c) => c.nodeType === 1 && c.namespaceURI === W && (!tag || c.localName === tag));
    const ptext = (p) => [...p.getElementsByTagNameNS(W, "t")].map((t) => t.textContent).join("");
    const paras = [...dom.getElementsByTagNameNS(W, "body")[0].getElementsByTagNameNS(W, "p")];
    const used = new Set();
    const find = (q) => { const t = norm(q); return paras.find((p) => !used.has(p) && norm(ptext(p)) === t) || paras.find((p) => norm(ptext(p)) === t) || paras.find((p) => t.length > 30 && norm(ptext(p)).startsWith(t.slice(0, 60))); };
    const run = (rPr, text, del) => { const r = mk("r"); if (rPr) r.appendChild(rPr.cloneNode(true)); const t = mk(del ? "delText" : "t"); t.setAttributeNS(XMLNS, "xml:space", "preserve"); t.textContent = text; r.appendChild(t); return r; };
    const track = (p, newText, author) => {
      // break the paragraph into word tokens (with their formatting) and fixed pieces such as Control ID fields
      const items = []; const keepStart = [], keepEnd = []; let buf = [];   // buf: [text, rPr] pieces of consecutive plain runs
      const flushText = () => { if (!buf.length) return; const all = buf.map((b) => b[0]).join(""); const at = []; buf.forEach(([t, r]) => { for (let i = 0; i < t.length; i++) at.push(r); });
        let pos = 0; for (const tk of tokens(all)) { items.push({ s: tk, rPr: at[pos] }); pos += tk.length; } buf = []; };
      for (const c of kids(p)) {
        if (c.localName === "pPr") continue;
        if (c.localName === "r") { const rPr = kids(c, "rPr")[0]; const ts = kids(c).filter((x) => x.localName !== "rPr");
          if (ts.length && ts.every((x) => x.localName === "t")) { buf.push([ts.map((x) => x.textContent).join(""), rPr]); continue; } }
        if (c.localName === "bookmarkStart") { keepStart.push(c); continue; } if (c.localName === "bookmarkEnd") { keepEnd.push(c); continue; }
        if (c.localName === "proofErr") continue;
        flushText(); items.push({ s: ptext(c) || "\u0000" + items.length, node: c });
      }
      flushText();
      const ops = diffTokens(items.map((x) => x.s), tokens(newText));
      for (const c of kids(p)) if (c.localName !== "pPr") p.removeChild(c);
      for (const c of keepStart) p.appendChild(c);
      let lastRPr = items.find((x) => x.rPr)?.rPr || null, cur = null, curKind = null;
      const flush = () => { if (cur) p.appendChild(cur.wrap || cur.r); cur = null; curKind = null; };
      for (const o of ops) {
        const it = o.ai != null ? items[o.ai] : null;
        if (it?.node) { flush(); p.appendChild(it.node); continue; }   // fields are kept as they are
        if (it?.rPr) lastRPr = it.rPr;
        const kind = o.t + "|" + (o.t === "+" ? "" : it?.rPr ? new XMLSerializer().serializeToString(it.rPr) : "");
        if (cur && curKind === kind) { cur.t.textContent += o.s; continue; }
        flush();
        const r = run(o.t === "+" ? lastRPr : it?.rPr, o.s, o.t === "-");
        let wrap = null; if (o.t !== "=") { wrap = mk(o.t === "+" ? "ins" : "del", { id: String(rid++), author, date: now }); wrap.appendChild(r); }
        cur = { r, wrap, t: r.lastChild }; curKind = kind;
      }
      flush(); for (const c of keepEnd) p.appendChild(c);
    };
    const comment = (p, author, text, date) => {
      const id = String(cid++); const first = kids(p).find((c) => c.localName !== "pPr");
      const s = mk("commentRangeStart", { id }); first ? p.insertBefore(s, first) : p.appendChild(s);
      p.appendChild(mk("commentRangeEnd", { id })); const r = mk("r"); r.appendChild(mk("commentReference", { id })); p.appendChild(r);
      comments.push({ id, author, text, date: (date || now).replace(/\.\d+Z$/, "Z") });
    };
    let placed = 0; const missed = [];
    for (const n of [...use].sort((a, b) => a.created.localeCompare(b.created))) {
      const p = find(n.quote); if (!p) { missed.push(n); continue; } used.add(p); placed++;
      const who = n.author || "Anonymous";
      if (n.kind === "suggestion" && n.status === "accepted") { track(p, n.newText, who); if (n.body) comment(p, who, n.body, n.created); }
      else if (n.kind === "suggestion") comment(p, who, `Suggested wording (not yet accepted): ${n.newText}${n.body ? "\nReason: " + n.body : ""}`, n.created);
      else comment(p, who, n.body + (n.replies || []).map((r) => `\n${r.author || "Anonymous"}: ${r.body}`).join(""), n.created);
    }
    if (missed.length) { const p = paras.find((x) => norm(ptext(x))); if (p) comment(p, "ONE portal", `Could not be placed automatically:\n${missed.map((n) => `${n.author}: ${n.kind === "suggestion" ? n.newText : n.body}`).join("\n")}`); }
    zip.file("word/document.xml", new XMLSerializer().serializeToString(dom));
    if (comments.length) {
      const ex = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
      zip.file("word/comments.xml", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:comments xmlns:w="${W}">${comments.map((c) => `<w:comment w:id="${c.id}" w:author="${ex(c.author)}" w:date="${c.date}" w:initials="${ex(c.author.split(/\s+/).map((x) => x[0]).join("").slice(0, 3))}">${c.text.split("\n").map((l) => `<w:p><w:r><w:t xml:space="preserve">${ex(l)}</w:t></w:r></w:p>`).join("")}</w:comment>`).join("")}</w:comments>`);
      let rels = await zip.file("word/_rels/document.xml.rels").async("string");
      if (!rels.includes("relationships/comments")) rels = rels.replace("</Relationships>", `<Relationship Id="rIdOneComments" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/></Relationships>`);
      zip.file("word/_rels/document.xml.rels", rels);
      let ct = await zip.file("[Content_Types].xml").async("string");
      if (!ct.includes("/word/comments.xml")) ct = ct.replace("</Types>", `<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/></Types>`);
      zip.file("[Content_Types].xml", ct);
    }
    const blob = await zip.generateAsync({ type: "blob", mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `${d.id}_Rev${d.revision}_review_${now.slice(0, 10)}.docx`; document.body.appendChild(a); a.click(); a.remove();
    toast(`Word file ready: ${placed} placed${missed.length ? `, ${missed.length} listed in a note at the top` : ""}`);
    window.ONE_LAST_EXPORT = { placed, missed: missed.length, comments: comments.length };
  } catch (e) { toast(e.message || "The Word file could not be prepared"); window.ONE_LAST_EXPORT = { error: String(e.message || e) }; }
}

// ---------- processes ----------
// ---------- processes: see process.js ----------

// ---------- performance ----------
route(/^\/performance$/, () => {
  const pick = ["PROD-OIL", "PROD-GAS", "TRIR", "NEAR-MISS", "PSE-T2", "SPILL-N", "IOW-EXC", "ALARM-RATE", "SCE-OVERDUE", "PM-COMP", "DEFERRALS", "MOC-OPEN", "ACT-OVERDUE", "FLARE", "LIFT-COST", "DOCS-OVERDUE"];
  const SUM = new Set(["count", "bbl", "MMscf", "hours"]);
  const yr = (k, unit, y) => { const v = (SERIES[k] || []).filter((p) => p[0].startsWith(y)).map((p) => p[1]); if (!v.length) return ""; const stock = ["SCE-OVERDUE", "DEFERRALS", "MOC-OPEN", "ACT-OVERDUE", "TRIR", "DOCS-OVERDUE"].includes(k); const s = stock ? v[v.length - 1] : SUM.has(unit) ? v.reduce((a, b) => a + b, 0) : v.reduce((a, b) => a + b, 0) / v.length;
    return Number.isInteger(s) ? s.toLocaleString() : s >= 100 ? Math.round(s).toLocaleString() : s.toFixed(s < 10 ? 2 : 1); };
  page([9], head("Performance", "Monthly figures from the performance register, January 2024 to October 2026. Each card is coloured by the element its measure serves. The dashed line marks the ONE launch.") + `
  <div class="kpis">${pick.map((k) => { const d = KPIS.find((x) => x.kpi_id === k); const s = SERIES[k]; if (!d || !s) return ""; const last = s[s.length - 1][1]; const n = d.oms_tag ? elOf(d.oms_tag) : 0; const c = n ? ECOL[n] : "#5B6B73";
    return `<div class="kpi" style="--c:${c}"><h3>${esc(d.name)} <span class="small">(${esc(d.unit)})</span></h3><div class="v">${last >= 100 ? Math.round(last).toLocaleString() : last}</div>${spark(s, c)}<div class="years"><span>2024 ${yr(k, d.unit, "2024")}</span><span>2025 ${yr(k, d.unit, "2025")}</span><span>2026 ${yr(k, d.unit, "2026")}</span></div><div class="small muted">${n ? `<a href="#/exp/${d.oms_tag}">${d.oms_tag}</a> ` : ""}${d.target ? `Target ${esc(d.target)}` : ""}</div></div>`; }).join("")}</div>`);
});

// ---------- search ----------
route(/^\/search\/(.*)$/, (q) => {
  const s = q.toLowerCase().trim(); $("#q").value = q;
  const docs = DOCS.filter((d) => (d.id + " " + d.title).toLowerCase().includes(s));
  const st = STMTS.filter((x) => x.b.t.toLowerCase().includes(s)).slice(0, 40);
  const ppl = PEOPLE.filter((p) => (p.n + " " + p.t).toLowerCase().includes(s)).slice(0, 20);
  const ctl = CTLS.filter((c) => (c.control_id + " " + c.statement).toLowerCase().includes(s)).slice(0, 20);
  const rk = RISKS.filter((r) => (r.risk_id + " " + r.title).toLowerCase().includes(s));
  const vp = PEOPLE.find((x) => x.t === "VP Engineering & Projects");
  page(null, head(`Results for “${esc(q)}”`, `${docs.length} documents, ${st.length} statements, ${ppl.length} people, ${ctl.length} controls, ${rk.length} risks.`) + `
  <div class="grid2"><div class="stack">${docs.length ? `<div class="panel"><h2>Documents</h2>${docs.map((d) => `<div>${docLink(d.id)} ${esc(d.title)} ${fpBar(d.id)}</div>`).join("")}</div>` : ""}
    ${st.length ? `<div class="panel"><h2>Statements</h2>${st.map(stmtHTML).join("")}</div>` : ""}</div>
    <div class="stack">${ppl.length ? `<div class="panel"><h2>People</h2>${ppl.map((p) => `<div>${vp && p.dl === vp.id ? `<a href="#/authority/${encodeURIComponent(p.n)}">${esc(p.n)}</a>` : esc(p.n)} <span class="muted small">${esc(p.t)}, ${esc(p.f)}</span></div>`).join("")}</div>` : ""}
    ${ctl.length ? `<div class="panel"><h2>Controls</h2>${ctl.map((c) => `<div>${ctlChip(c.control_id)} ${esc(c.statement)}</div>`).join("")}</div>` : ""}
    ${rk.length ? `<div class="panel"><h2>Risks</h2>${rk.map((r) => `<div><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)} ${rateChip(r.current_rating)}</div>`).join("")}</div>` : ""}
    ${!docs.length && !st.length && !ppl.length && !ctl.length && !rk.length ? `<div class="panel"><p>Nothing matches. Try a document number, a job title or a word from a requirement.</p></div>` : ""}</div></div>`);
});

// =====================================================================================================
// THE ORGANISATIONAL DIMENSION: company, sites, functions, roles and people, read from company/org/*.csv
// =====================================================================================================
const CO = D.company || { roles: [], omsRoles: [], sites: [], functions: [], links: [], changes: [], profile: "" };
const ROLES = CO.roles; const ROLE = Object.fromEntries(ROLES.map((r) => [r.role_id, r]));
const ROLE_BY = {}; for (const r of ROLES) { ROLE_BY[r.title] = r; for (const a of (r.aliases || "").split("; ").filter(Boolean)) ROLE_BY[a] ||= r; }
const OMSR = CO.omsRoles; const OMSR_BY = Object.fromEntries(OMSR.map((o) => [o.oms_role_id, o]));
const SITES = CO.sites; const SITE = Object.fromEntries(SITES.map((s) => [s.site_code, s]));
const FUNCS = CO.functions; const FUNC = Object.fromEntries(FUNCS.map((f) => [f.code, f]));
const ACTIVE = PEOPLE.filter((p) => p.st !== "Left");
const HOLD = {}; for (const p of ACTIVE) (HOLD[p.r] ||= []).push(p);
const PNAME = {}; for (const p of PEOPLE) if (!PNAME[p.n] || p.st !== "Left") PNAME[p.n] = p;
const CHANGES = CO.changes;
const roleLink = (r, label) => r ? `<a class="rl" href="#/role/${r.role_id}">${esc(label || r.title)}</a>` : esc(label || "");
const personLink = (p, label) => p ? `<a class="pl" href="#/person/${p.id}">${esc(label || p.n)}</a>${p.st === "Left" ? ` <span class="st rejected">Left</span>` : ""}` : esc(label || "");
// "Name — Title; Name — Title" as written in documents and registers
const bare = (t) => (t || "").replace(/\s*\((Technical Authority|system owner|audit authority|[a-z][^)]*)\)$/, "").trim();   // drop qualifiers such as "(Technical Authority)"
const parseWho = (s) => String(s || "").split(/;\s*/).filter(Boolean).map((x) => { const [n, t] = x.split(" — ").map((y) => (y || "").trim()); const person = PNAME[n]; const role = ROLE_BY[t] || ROLE_BY[bare(t)] || (t ? null : ROLE_BY[n]);
  return { raw: x, name: t ? n : "", title: t || n, person: t ? person : null, role, stale: person && t ? (person.st === "Left" ? "left" : role !== ROLE_BY[person.t] ? "moved" : "") : "" }; });
const whoHTML = (s) => parseWho(s).map((w) => w.name ? `${personLink(w.person, w.name)}${w.title ? ", " + roleLink(w.role, w.title) : ""}` : roleLink(w.role, w.title)).join("; ") || esc(s || "");
const staleNote = (w) => w.stale === "left" ? `${esc(w.name)} left ACE on ${fmt(toDate(w.person.left))}` : w.stale === "moved" ? (CO.changes.some((c) => c.employee_id === w.person.id) ? `${esc(w.name)} moved to ${esc(w.person.t)}` : `the staff list has ${esc(w.name)} as ${esc(w.person.t)}`) : "";

// every job title, short name and OMS role name, found in the text of binding statements
const KEYS = {}; for (const [k, r] of Object.entries(ROLE_BY)) KEYS[k] = { kind: "role", id: r.role_id };
for (const o of OMSR) if (o.name.includes(" ") && !KEYS[o.name]) KEYS[o.name] = { kind: "oms", id: o.oms_role_id };
const reEsc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const KEY_RE = Object.keys(KEYS).length ? new RegExp(`(?<![A-Za-z])(${Object.keys(KEYS).sort((a, b) => b.length - a.length).map(reEsc).join("|")})(?![A-Za-z])`, "g") : null;
const HITS = {}; // role_id or oms id -> statements
for (const x of STMTS) { if (!KEY_RE) break; const seen = new Set(); for (const m of x.b.t.matchAll(KEY_RE)) { const k = KEYS[m[1]]; if (seen.has(k.id)) continue; seen.add(k.id); (HITS[k.id] ||= []).push(x); } }
// raw text in, HTML out: role names become links, everything else is escaped
const linkRoles = (raw) => { if (!KEY_RE) return esc(raw); let out = "", last = 0; for (const m of String(raw).matchAll(KEY_RE)) { const k = KEYS[m[1]]; out += esc(raw.slice(last, m.index)) + `<a class="rl" href="#/${k.kind === "role" ? "role" : "duty"}/${k.id}">${esc(m[1])}</a>`; last = m.index + m[1].length; } return out + esc(raw.slice(last)); };

// where each job role is named in document metadata and registers
const META = ["owner", "author", "approver", "custodian", "endorser", "reviewers"]; const MNAME = { owner: "Owner", author: "Author", approver: "Approver", custodian: "Custodian", endorser: "Endorser", reviewers: "Reviewer" };
const DOCROLE = {}; const STALE = [];
for (const d of DOCS) for (const f of META) for (const w of parseWho(d[f])) { if (w.role) (DOCROLE[w.role.role_id] ||= []).push({ d, f }); if (w.stale) STALE.push({ d, f, w }); }
const ownerRole = (s) => parseWho(s)[0]?.role;
const OWNS = { risks: {}, controls: {}, actions: {}, kpis: {}, processes: {} };
for (const r of RISKS) { const x = ownerRole(r.owner); if (x) (OWNS.risks[x.role_id] ||= []).push(r); }
for (const c of CTLS) { const x = ownerRole(c.owner); if (x) (OWNS.controls[x.role_id] ||= []).push(c); }
for (const a of ACTIONS) { const x = ownerRole(a.owner); if (x) (OWNS.actions[x.role_id] ||= []).push(a); }
for (const k of KPIS) { const x = ownerRole(k.owner); if (x) (OWNS.kpis[x.role_id] ||= []).push(k); }
for (const p of REG["BPM-REG-001"] || []) { const x = ownerRole(p.owner); if (x) (OWNS.processes[x.role_id] ||= []).push(p); }
// duties (OMS roles) each job role carries, named in oms_roles.csv or worked out from the registers
const DUTY = {}; const addDuty = (rid, oid, why) => { if (!rid) return; (DUTY[rid] ||= new Map()); if (!DUTY[rid].has(oid)) DUTY[rid].set(oid, why); };
for (const o of OMSR) for (const rid of (o.held_by || "").split("; ").filter(Boolean)) addDuty(rid, o.oms_role_id, "");
for (const e of ELS) addDuty(ROLE_BY[e.owner]?.role_id, "EO", `Element ${e.id}`);
for (const d of DOCS) addDuty(ownerRole(d.owner)?.role_id, "DO", "");
for (const k of ["risks", "controls", "processes"]) for (const rid in OWNS[k]) addDuty(rid, { risks: "RO", controls: "CO", processes: "PO" }[k], "");
const dutyHolders = (oid) => ROLES.filter((r) => DUTY[r.role_id]?.has(oid));
const roleFP = (rid) => { const f = {}; for (const x of HITS[rid] || []) if (x.tags[0]) f[elOf(x.tags[0])] = (f[elOf(x.tags[0])] || 0) + 1; return f; };
const fpWheelOf = (f, label = "statements") => { const max = Math.max(1, ...Object.values(f)); const tot = Object.values(f).reduce((a, b) => a + b, 0);
  return `<svg class="fpwheel" viewBox="0 0 120 120" role="img" aria-label="Element fingerprint">${ELS.map((e) => { const [a0, a1] = segA(e.id); const v = f[e.id] || 0;
    return `<path d="${arc(60, 60, 22, 56, a0 + 0.02, a1 - 0.02)}" fill="#EEF2F3"/>${v ? `<path d="${arc(60, 60, 22, 22 + 34 * Math.sqrt(v / max), a0 + 0.02, a1 - 0.02)}" fill="${ECOL[e.id]}" data-tip="<b>${e.id}. ${esc(e.title)}</b>${v} ${label}" data-goel="${e.id}" style="cursor:pointer"/>` : ""}`; }).join("")}
    <text x="60" y="58" text-anchor="middle" font-size="12" font-weight="600" fill="#17262E">${tot}</text><text x="60" y="71" text-anchor="middle" font-size="7.5" fill="#4E5F68">${label}</text></svg>`; };
const elChips = (s) => String(s || "").split(/;\s*/).filter(Boolean).map((n) => `<a class="echip small" style="--c:${ECOL[n]}" href="#/el/${n}"><b style="color:${ON(n)}">${n}</b>${SHORT[n]}</a>`).join("");
const headcount = (fc) => ACTIVE.filter((p) => p.fc === fc).length;

// ---------- About ACE ----------
function businessMap() {
  const W = 900, H = 470, X = (s) => +s.map_x / 100 * W, Y = (s) => +s.map_y / 100 * H * 0.86 + 20;
  const flows = [["CHB", "PAP", "flow"], ["SAP", "PAP", "flow"], ["PAP", "CPF", "flow"], ["LND", "CPF", "flow"], ["PLB", "PAP", "supply"], ["PLB", "LND", "supply"], ["PLB", "CPF", "supply"], ["RIG", "LND", "supply"]].filter(([a, b]) => SITE[a] && SITE[b]);
  const cpf = SITE.CPF;
  let g = `<defs><marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#0B5563"/></marker></defs>
    <rect x="0" y="0" width="${W * 0.27}" height="${H}" fill="#DCEBF0"/><text x="16" y="28" class="water">Gulf of Paria</text>
    <path d="M${W * 0.27},0 C${W * 0.25},${H * 0.3} ${W * 0.3},${H * 0.6} ${W * 0.27},${H} L${W},${H} L${W},0 Z" fill="#F4F1E6"/><text x="${W - 16}" y="28" text-anchor="end" class="land">Trinidad</text>`;
  for (const [a, b, k] of flows) { const p = SITE[a], q = SITE[b]; g += `<path class="${k}" d="M${X(p)},${Y(p)} Q${(X(p) + X(q)) / 2},${(Y(p) + Y(q)) / 2 - 28} ${X(q)},${Y(q)}" ${k === "flow" ? 'marker-end="url(#ar2)"' : ""}/>`; }
  if (cpf) { g += `<path class="flow" d="M${X(cpf)},${Y(cpf)} C${X(cpf) + 160},${Y(cpf) + 6} ${W - 260},${Y(cpf) + 2} ${W - 150},${Y(cpf) + 2}" marker-end="url(#ar2)"/><g class="sink"><rect x="${W - 148}" y="${Y(cpf) - 18}" width="138" height="40" rx="20"/><text x="${W - 79}" y="${Y(cpf) + 7}" text-anchor="middle">Gas to the Gas Buyer</text></g>
    <path class="flow" d="M${X(cpf)},${Y(cpf)} L${X(cpf) - 70},${Y(cpf) + 60}" marker-end="url(#ar2)"/><g class="sink"><rect x="${X(cpf) - 150}" y="${Y(cpf) + 62}" width="128" height="40" rx="20"/><text x="${X(cpf) - 86}" y="${Y(cpf) + 87}" text-anchor="middle">Crude by tanker</text></g>`; }
  for (const s of SITES) { const n = ACTIVE.filter((p) => p.s === s.site_code).length; const r = 16 + Math.sqrt(n) * 2.2;
    g += `<a href="#/site/${s.site_code}" class="snode"><circle cx="${X(s)}" cy="${Y(s)}" r="${r}"/><text x="${X(s)}" y="${Y(s) + 4}" text-anchor="middle" class="code">${s.site_code}</text>
      <text x="${X(s)}" y="${Y(s) + r + 16}" text-anchor="middle" class="nm">${esc(s.name)}</text><text x="${X(s)}" y="${Y(s) + r + 31}" text-anchor="middle" class="sub">${n ? n + " staff" : esc(s.manning)}</text></a>`; }
  return `<svg class="bmap" viewBox="0 0 ${W} ${H}" role="img" aria-label="ACE business map">${g}</svg>`;
}
function siteStats(code) {
  const evs = EVENTS.filter((e) => e.site === code && toDate(e.date) >= YEAR_AGO); const rs = RISKS.filter((r) => r.site === code);
  const acts = ACTIONS.filter((a) => !a.closed && EVBY[a.event_id]?.site === code); const docs = DOCS.filter((d) => (d.applies || "").includes(code));
  return { staff: ACTIVE.filter((p) => p.s === code).length, evs, rs, high: rs.filter((r) => /High/.test(r.current_rating)).length, acts, docs, mocs: MOCS.filter((m) => m.site === code && !m.closed) };
}
route(/^\/company$/, () => {
  const md = CO.profile; const intro = (md.match(/## 1\. Overview\s+([\s\S]*?)ACE does three things/) || [, ""])[1].trim();
  page(null, `<div class="cohero"><img src="brand/logo_lg.png" alt="ACE logo" onerror="this.remove()"><div><div class="crumb">Company</div><h1 class="display">Acme Caribbean Energy</h1>
    <p class="lede">${(intro ? mdHTML(intro).replace(/^<p>|<\/p>$/g, "") : "A mid-size Trinidad and Tobago oil and gas producer.")}</p>
    <div class="figures"><div><b>${ACTIVE.length}</b><span>staff</span></div><div><b>${SITES.length}</b><span>sites</span></div><div><b>${FUNCS.length}</b><span>functions</span></div><div><b>${ROLES.length}</b><span>job roles</span></div><div><b>${DOCS.length}</b><span>OMS documents</span></div></div></div></div>
  <div class="grid2" style="grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);align-items:start">
    <div class="panel"><h2>What ACE does, and where</h2><p class="small muted">Crude and gas flow from the wells to the Central Processing Facility, then to the Gas Buyer or by tanker. Dashed lines are supply routes from the shore base. Choose a site.</p>${businessMap()}</div>
    <div class="stack"><div class="panel"><h2>Produce, process, sell</h2>
      <p><b>Produce.</b> Crude and gas from small offshore fields in the Gulf of Paria and from three land leases.</p>
      <p><b>Process.</b> Everything goes to ACE's own Central Processing Facility on the west coast.</p>
      <p><b>Sell.</b> Gas to the Gas Buyer under a gas sales agreement; crude shipped by tanker or barge from the CPF jetty.</p></div>
      <div class="panel"><h2>Explore the company</h2><p><a href="#/org">Organisation and functions</a><br><a href="#/roles">Roles and OMS duties</a><br><a href="#/people">Staff directory</a><br><a href="#/model">How ACE fits the ONE model</a></p></div></div></div>
  <h2 style="margin-top:24px">Sites compared</h2>
  <div class="panel"><p class="small muted">One OMS, several sites. The same documents, risks and registers can be read site by site, and a company with more than one OMS can be compared the same way.</p>
    <table class="t"><tr><th>Site</th><th>Area Authority</th><th class="n">Staff</th><th class="n">Risks</th><th class="n">High</th><th class="n">Events, 12 mo</th><th class="n">Open actions</th><th class="n">Open changes</th><th class="n">Documents applying</th></tr>
    ${SITES.map((s) => { const t = siteStats(s.site_code); return `<tr><td><a href="#/site/${s.site_code}">${esc(s.name)}</a><div class="small muted">${esc(s.type)}</div></td><td class="small">${roleLink(ROLE[s.area_authority])}</td><td class="n">${t.staff}</td><td class="n">${t.rs.length}</td><td class="n">${t.high || ""}</td><td class="n">${t.evs.length}</td><td class="n">${t.acts.length}</td><td class="n">${t.mocs.length}</td><td class="n">${t.docs.length}</td></tr>`; }).join("")}</table></div>
  <h2 style="margin-top:24px">Functions</h2>
  <div class="cards">${FUNCS.map((f) => `<a class="card fcard" href="#/org/${f.code}"><span class="id">${esc(f.code)}</span><h3>${esc(f.name)}</h3><p class="small muted" style="margin:0 0 8px">${esc(firstSentence(f.purpose))}</p><div class="row"><span>${headcount(f.code)} staff</span><span>${(HOLD[f.head_role] || []).map((p) => esc(p.n)).join(", ")}</span></div></a>`).join("")}</div>
  ${md ? `<details class="panel" style="margin-top:24px"><summary><b>Full company profile</b> <span class="small muted">from company/ACE_Company_Profile.md</span></summary><div class="mdbody">${mdHTML(md)}</div></details>` : ""}`);
});
function mdHTML(md) {
  const inl = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/\*(.+?)\*/g, "<i>$1</i>");
  const out = []; const L = md.split(/\r?\n/); let i = 0;
  while (i < L.length) { const l = L[i];
    if (/^```/.test(l)) { const b = []; i++; while (i < L.length && !/^```/.test(L[i])) b.push(L[i++]); i++; out.push(`<pre>${esc(b.join("\n"))}</pre>`); continue; }
    if (/^#{1,4} /.test(l)) { const n = l.match(/^#+/)[0].length; out.push(`<h${Math.min(4, n + 1)}>${inl(l.replace(/^#+ /, ""))}</h${Math.min(4, n + 1)}>`); i++; continue; }
    if (/^\|/.test(l)) { const rows = []; while (i < L.length && /^\|/.test(L[i])) { if (!/^\|[-| :]+\|$/.test(L[i])) rows.push(L[i].split("|").slice(1, -1).map((c) => inl(c.trim()))); i++; } out.push(`<table class="t">${rows.map((r, k) => `<tr>${r.map((c) => k ? `<td>${c}</td>` : `<th>${c}</th>`).join("")}</tr>`).join("")}</table>`); continue; }
    if (/^- /.test(l)) { const it = []; while (i < L.length && /^- /.test(L[i])) it.push(`<li>${inl(L[i++].slice(2))}</li>`); out.push(`<ul>${it.join("")}</ul>`); continue; }
    if (/^---/.test(l) || !l.trim()) { i++; continue; }
    out.push(`<p>${inl(l)}</p>`); i++; }
  return out.join("");
}

// ---------- a site ----------
route(/^\/site\/([A-Z]{3})$/, (code) => {
  const s = SITE[code]; if (!s) return go404(); const t = siteStats(code); const aa = ROLE[s.area_authority];
  const byF = {}; for (const p of ACTIVE.filter((p) => p.s === code)) byF[p.fc] = (byF[p.fc] || 0) + 1;
  page(null, head(esc(s.name), `${esc(s.type)}, ${esc(s.location)}. ${esc(s.purpose)}.`, `<a href="#/company">Company</a>`) + `
  <div class="figures" style="margin-bottom:18px"><div><b>${t.staff}</b><span>staff based here</span></div><div><b>${t.rs.length}</b><span>risks, ${t.high} high</span></div><div><b>${t.evs.length}</b><span>events in 12 months</span></div><div><b>${t.acts.length}</b><span>open actions</span></div><div><b>${t.docs.length}</b><span>documents apply here</span></div></div>
  <div class="grid2" style="align-items:start"><div class="stack">
    <div class="panel"><h2>Who is in charge</h2><p>Area Authority: ${roleLink(aa)} ${(HOLD[aa?.role_id] || []).map((p) => personLink(p)).join(", ")}</p><p class="small muted">${esc(s.manning)}${s.parent ? `. Run from ${esc(SITE[s.parent]?.name || s.parent)}` : ""}.</p>
      ${Object.keys(byF).length ? `<h3 style="margin-top:12px">Staff by function</h3>${hbar(Object.entries(byF).sort((a, b) => b[1] - a[1]).map(([f, n], i) => [FUNC[f]?.name || f, n, ["#0B5563", "#3E8597", "#8EBCC6", "#B9C7CD", "#DCE4E7", "#E8EDEF"][Math.min(i, 5)]]))}<div class="small muted">${Object.entries(byF).sort((a, b) => b[1] - a[1]).map(([f, n]) => `${esc(FUNC[f]?.name || f)} ${n}`).join(", ")}</div>` : ""}</div>
    <div class="panel"><h2>Risks at this site</h2>${rateBar(t.rs)}<table class="t">${t.rs.map((r) => `<tr><td><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)}</td><td>${rateChip(r.current_rating)}</td></tr>`).join("") || `<tr><td class="muted">None registered.</td></tr>`}</table></div></div>
    <div class="stack"><div class="panel"><h2>Documents that apply here</h2><table class="t">${t.docs.map((d) => `<tr><td>${docLink(d.id)} ${esc(d.title)}</td><td>${fpBar(d.id)}</td></tr>`).join("") || `<tr><td class="muted">No document names this site in its applicability.</td></tr>`}</table></div>
    <div class="panel"><h2>Recent events</h2><ul class="events">${t.evs.slice(-12).reverse().map((e) => `<li><span class="muted">${fmt(toDate(e.date))}</span><span>${esc(e.title)} <span class="small muted">${esc(e.type)}</span></span></li>`).join("") || `<li><span></span><span class="muted">None in the last 12 months.</span></li>`}</ul></div></div></div>`);
});

// ---------- organisation ----------
function functionRing() {
  const N = FUNCS.length, cx = 300, cy = 270, R = 200; const pos = {}; FUNCS.forEach((f, i) => { const a = -Math.PI / 2 + i * 2 * Math.PI / N; pos[f.code] = [cx + R * Math.cos(a), cy + R * Math.sin(a), a]; });
  const wt = { Strong: 3.2, Medium: 1.8, Light: 1 };
  let g = CO.links.filter((l) => pos[l.from] && pos[l.to]).map((l) => { const [x1, y1] = pos[l.from], [x2, y2] = pos[l.to];
    return `<path class="lk" data-a="${l.from}" data-b="${l.to}" d="M${x1},${y1} Q${cx},${cy} ${x2},${y2}" stroke-width="${wt[l.strength] || 1}" data-tip="<b>${esc(FUNC[l.from].name)} and ${esc(FUNC[l.to].name)}</b>${esc(l.strength)}: ${esc(l.nature)}"/>`; }).join("");
  g += FUNCS.map((f) => { const [x, y, a] = pos[f.code]; const n = headcount(f.code); const r = 10 + Math.sqrt(n) * 2.6; const lx = cx + (R + r + 12) * Math.cos(a), ly = cy + (R + r + 12) * Math.sin(a);
    return `<a href="#/org/${f.code}" class="fn" data-f="${f.code}"><circle cx="${x}" cy="${y}" r="${r}"/><text x="${x}" y="${y + 4}" text-anchor="middle" class="code">${f.code}</text><text x="${lx}" y="${ly + 4}" text-anchor="${Math.abs(Math.cos(a)) < 0.25 ? "middle" : Math.cos(a) > 0 ? "start" : "end"}" class="nm">${esc(f.name)}</text></a>`; }).join("");
  return `<svg class="ring" viewBox="-170 0 940 560" role="img" aria-label="How the functions work together">${g}</svg>`;
}
route(/^\/org$/, () => {
  const ceo = ROLES.find((r) => r.grade.startsWith("L1"));
  page(null, head("Organisation", "Thirteen functions under a Chief Executive. Solid lines say who you work for; dotted lines say who sets your technical standard. Everything here is read from the staff list and role files in the repository, so a change of person or structure shows the next time the site builds.", `<a href="#/company">Company</a>`) + `
  <div class="orgtop"><a class="obox ceo" href="#/role/${ceo?.role_id}"><b>${esc(ceo?.title || "")}</b><span>${(HOLD[ceo?.role_id] || []).map((p) => esc(p.n)).join(", ")}</span></a></div>
  <div class="orgrow">${FUNCS.filter((f) => f.code !== "EXEC").map((f) => `<a class="obox" href="#/org/${f.code}"><b>${esc(f.name)}</b><span>${(HOLD[f.head_role] || []).map((p) => esc(p.n)).join(", ")}</span><span class="small muted">${headcount(f.code)} staff</span></a>`).join("")}
    <a class="obox" href="#/org/EXEC"><b>${esc(FUNC.EXEC?.name || "CEO Office")}</b><span>Strategy, internal audit</span><span class="small muted">${headcount("EXEC")} staff</span></a></div>
  <div class="grid2" style="grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);align-items:start;margin-top:18px">
    <div class="panel"><h2>How the functions work together</h2><p class="small muted">Thicker lines are stronger working relationships. Point at a line to see what flows between two functions; point at a function to light up its partners.</p>${functionRing()}</div>
    <div class="stack"><div class="panel"><h2>Dotted lines</h2><p>${ACTIVE.filter((p) => p.disc && p.t.endsWith("Lead") && p.dl).length} discipline leads hold a dotted line to the VP Engineering &amp; Projects as Technical Authorities, whatever function they sit in.</p><p><a class="btn" href="#/authority">See the technical authority network</a></p></div>
      <div class="panel"><h2>Recent staff changes</h2><ul class="feed">${[...CHANGES].reverse().map((c) => { const p = PID[c.employee_id]; return `<li><time>${fmt(toDate(c.date))}</time><span>${personLink(p, c.name)} ${esc(c.event.toLowerCase())}${c.from_role ? ` from ${roleLink(ROLE_BY[c.from_role], c.from_role)}` : ""}${c.to_role ? ` ${c.event === "Joined" ? "as" : "to"} ${roleLink(ROLE_BY[c.to_role], c.to_role)}` : ""}<div class="small muted">${esc(c.note)}</div></span></li>`; }).join("") || `<li><span></span><span class="muted">None recorded.</span></li>`}</ul>
      ${STALE.length ? `<p class="small" style="margin-top:8px"><b>${STALE.length}</b> document entries still name people who have since left or moved. <a href="#/gaps">See them under Gaps</a>.</p>` : ""}</div></div></div>`);
  const svg = $(".ring");
  svg.addEventListener("mouseover", (e) => { const n = e.target.closest(".fn"); if (!n) return; const f = n.dataset.f; svg.classList.add("focus"); for (const l of svg.querySelectorAll(".lk")) l.classList.toggle("on", l.dataset.a === f || l.dataset.b === f); });
  svg.addEventListener("mouseout", (e) => { if (e.target.closest(".fn")) { svg.classList.remove("focus"); for (const l of svg.querySelectorAll(".lk")) l.classList.remove("on"); } });
});
function roleTree(fc) {
  const rs = ROLES.filter((r) => r.function === fc); const ids = new Set(rs.map((r) => r.role_id));
  const kids = {}; for (const r of rs) { const p = ids.has(r.reports_to) ? r.reports_to : "_root"; (kids[p] ||= []).push(r); }
  const node = (r, depth) => { const hs = HOLD[r.role_id] || []; const ch = kids[r.role_id] || []; const duties = [...(DUTY[r.role_id]?.keys() || [])];
    const box = `<a class="rbox" href="#/role/${r.role_id}"><b>${esc(r.title)}</b><span>${hs.length > 3 ? `${hs.length} people` : hs.map((p) => esc(p.n)).join(", ") || "<i>Vacant</i>"}</span>${duties.length ? `<span class="duties">${duties.slice(0, 3).map((d) => `<i>${esc(OMSR_BY[d]?.name || d)}</i>`).join("")}</span>` : ""}</a>`;
    return `<li>${ch.length ? `<details ${depth < 2 ? "open" : ""}><summary>${box}</summary><ul>${ch.map((c) => node(c, depth + 1)).join("")}</ul></details>` : box}</li>`; };
  return `<div class="otree"><ul>${(kids._root || []).map((r) => node(r, 0)).join("")}</ul></div>`;
}
route(/^\/org\/([A-Z]+)$/, (fc) => {
  const f = FUNC[fc]; if (!f) return go404();
  const links = CO.links.filter((l) => l.from === fc || l.to === fc);
  const docs = DOCS.filter((d) => (d.func || "").includes(f.name) || ownerRole(d.owner)?.function === fc);
  const sites = {}; for (const p of ACTIVE.filter((p) => p.fc === fc)) sites[p.s] = (sites[p.s] || 0) + 1;
  page(f.elements.split("; ").map(Number), head(esc(f.name), esc(f.purpose), `<a href="#/company">Company</a> / <a href="#/org">Organisation</a>`, `<div class="chips">${elChips(f.elements)}</div>`) + `
  <div class="figures" style="margin-bottom:18px"><div><b>${headcount(fc)}</b><span>staff</span></div><div><b>${ROLES.filter((r) => r.function === fc).length}</b><span>job roles</span></div><div><b>${docs.length}</b><span>documents owned</span></div><div><b>${Object.keys(sites).length}</b><span>${Object.entries(sites).sort((a, b) => b[1] - a[1]).map(([s, n]) => `${n} at ${esc(SITE[s]?.name || s)}`).join(", ")}</span></div></div>
  <div class="grid2" style="grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);align-items:start"><div class="panel"><h2>Roles and reporting lines</h2><p class="small muted">Each box is a job role. Grey tags are OMS duties the role carries. Choose a role to see its documents.</p>${roleTree(fc)}</div>
    <div class="stack">${fnProcPanel(fc)}<div class="panel"><h2>Works closely with</h2><table class="t">${links.map((l) => { const o = l.from === fc ? l.to : l.from; return `<tr><td><a href="#/org/${o}">${esc(FUNC[o]?.name || o)}</a><div class="small muted">${esc(l.nature)}</div></td><td class="small">${esc(l.strength)}</td></tr>`; }).join("")}</table></div>
      <div class="panel"><h2>Documents owned</h2><table class="t">${docs.map((d) => `<tr><td>${docLink(d.id)} ${esc(d.title)}</td><td>${fpBar(d.id)}</td></tr>`).join("") || `<tr><td class="muted">None yet.</td></tr>`}</table></div></div></div>`);
});

// ---------- roles ----------
route(/^\/roles$/, () => {
  page(null, head("Roles", "Documents name roles, not people. A role stays when its holder changes, so every page that mentions a role stays right. OMS duties such as Area Authority are carried by several job roles.", `<a href="#/company">Company</a>`) + `
  <h2>OMS duties</h2><div class="cards">${OMSR.map((o) => { const hs = dutyHolders(o.oms_role_id); return `<a class="card" href="#/duty/${o.oms_role_id}" style="--c:${ECOL[(o.elements || "5").split("; ")[0]]}"><span class="id">${esc(o.oms_role_id)}</span><h3>${esc(o.name)}</h3><p class="small muted" style="margin:0 0 8px">${esc(o.definition)}</p><div class="row"><span>${plural(hs.length, "job role")}</span><span>${(HITS[o.oms_role_id] || []).length || ""}${(HITS[o.oms_role_id] || []).length ? " statements" : ""}</span></div></a>`; }).join("")}</div>
  <h2 style="margin-top:24px">Job roles</h2><div class="filters"><label>Function<select id="ff"><option value="">All</option>${FUNCS.map((f) => `<option value="${f.code}">${esc(f.name)}</option>`).join("")}</select></label><label>Find<input id="ft" type="search" placeholder="e.g. Lead"></label>
    <label>Show<select id="fx"><option value="">All roles</option><option value="d">Named in documents</option></select></label></div>
  <div class="panel"><table class="t" id="rt"></table></div>`);
  const run = () => { const f = $("#ff").value, t = $("#ft").value.toLowerCase(), x = $("#fx").value;
    $("#rt").innerHTML = `<tr><th>Role</th><th>Function</th><th>Holders</th><th>OMS duties</th><th class="n">Named in statements</th><th>Duties by element</th></tr>` + ROLES.filter((r) => (!f || r.function === f) && (!t || r.title.toLowerCase().includes(t)) && (!x || (HITS[r.role_id] || DOCROLE[r.role_id]))).map((r) => {
      const hs = HOLD[r.role_id] || []; const fp = roleFP(r.role_id); const tot = Object.values(fp).reduce((a, b) => a + b, 0);
      return `<tr><td>${roleLink(r)}<div class="small muted">${esc(r.grade)}</div></td><td class="small">${esc(FUNC[r.function]?.name || r.function)}</td><td class="small">${hs.length > 2 ? hs.length + " people" : hs.map((p) => personLink(p)).join(", ")}</td><td class="small">${[...(DUTY[r.role_id]?.keys() || [])].map((d) => esc(OMSR_BY[d]?.name || d)).join(", ")}</td><td class="n">${(HITS[r.role_id] || []).length || ""}</td>
        <td>${tot ? `<span class="fp">${Object.keys(fp).sort((a, b) => a - b).map((n) => `<i style="width:${100 * fp[n] / tot}%;background:${ECOL[n]}"></i>`).join("")}</span>` : ""}</td></tr>`; }).join(""); };
  for (const id of ["ff", "ft", "fx"]) $("#" + id).oninput = run; run();
});
const stmtList = (list, max = 40) => { const by = new Map(); for (const s of list) { if (!by.has(s.d.id)) by.set(s.d.id, []); by.get(s.d.id).push(s); }
  return [...by].map(([doc, l]) => `<details class="vm-sec" style="--c:${ECOL[elOf(l[0].tags[0])] || "#D5DDE0"}"><summary><b>${esc(doc)}</b> ${esc(DOC[doc].title)} <span class="small muted">${plural(l.length, "statement")}</span></summary><div class="vm-body">${l.slice(0, max).map(stmtHTML).join("")}</div></details>`).join(""); };
route(/^\/role\/([A-Z]+-\d+)$/, (id) => {
  const r = ROLE[id]; if (!r) return go404();
  const hs = HOLD[id] || []; const mgr = ROLE[r.reports_to], dot = ROLE[r.dotted_to]; const reports = ROLES.filter((x) => x.reports_to === id);
  const duties = [...(DUTY[id] || new Map())]; const hits = HITS[id] || []; const fp = roleFP(id);
  const asDuty = duties.map(([o]) => [o, HITS[o] || []]).filter(([, l]) => l.length);
  const meta = DOCROLE[id] || []; const docsIn = new Map(); for (const m of meta) (docsIn.get(m.d.id) || docsIn.set(m.d.id, []).get(m.d.id)).push(MNAME[m.f]);
  for (const s of hits) (docsIn.get(s.d.id) || docsIn.set(s.d.id, []).get(s.d.id)).push("named in text");
  const own = (k) => OWNS[k][id] || [];
  const lanes = D.processes.flatMap((pm) => pm.lanes.filter((l) => l.role_id === r.role_id || l.role === r.title || duties.some(([o]) => OMSR_BY[o]?.name === l.role)).map((l) => [pm, l]));
  const moves = CHANGES.filter((c) => c.from_role === r.title || c.to_role === r.title);
  page(Object.keys(fp).length ? fp : null, head(esc(r.title), esc(r.purpose), `<a href="#/company">Company</a> / <a href="#/org/${r.function}">${esc(FUNC[r.function]?.name || r.function)}</a>`,
    `<div style="text-align:center">${fpWheelOf(fp)}<div class="small muted">Where this role's duties sit in the OMS</div></div>`) + `
  <div class="grid3" style="align-items:start">
    <div class="panel"><h2>Held by</h2>${hs.map((p) => `<div style="margin-bottom:4px">${personLink(p)} <span class="small muted">${esc(SITE[p.s]?.name || p.loc)}</span></div>`).join("") || `<p class="muted">Vacant.</p>`}
      ${moves.length ? `<h3 style="margin-top:10px">Changes</h3>${moves.map((c) => `<div class="small">${fmt(toDate(c.date))}: ${personLink(PID[c.employee_id], c.name)} ${esc(c.event.toLowerCase())}${c.to_role && c.to_role !== r.title ? " to " + esc(c.to_role) : ""}</div>`).join("")}` : ""}</div>
    <div class="panel"><h2>Reporting lines</h2><p>Reports to ${mgr ? roleLink(mgr) : "the Board"}${dot ? `<br>Dotted line to ${roleLink(dot)}${r.dotted_purpose ? `<span class="small muted"> (${esc(r.dotted_purpose)})</span>` : ""}` : ""}</p>
      ${reports.length ? `<h3>Direct reports</h3>${reports.map((x) => `<div class="small">${roleLink(x)} <span class="muted">${(HOLD[x.role_id] || []).length}</span></div>`).join("")}` : ""}
      <p class="small muted" style="margin-top:8px">${esc(r.grade)}${r.discipline ? `, discipline: ${esc(r.discipline)}` : ""}. Sites: ${r.sites.split("; ").map((s) => `<a href="#/site/${s}">${esc(SITE[s]?.name || s)}</a>`).join(", ")}</p></div>
    <div class="panel"><h2>OMS duties</h2>${duties.map(([o, why]) => `<div style="margin-bottom:6px"><a href="#/duty/${o}">${esc(OMSR_BY[o]?.name || o)}</a>${why ? ` <span class="small muted">${esc(why)}</span>` : ""}</div>`).join("") || `<p class="muted small">No OMS duty recorded for this role.</p>`}</div></div>
  <div class="figures" style="margin:18px 0"><div><b>${docsIn.size}</b><span>documents name this role</span></div><div><b>${hits.length}</b><span>binding statements name it</span></div><div><b>${asDuty.reduce((a, [, l]) => a + l.length, 0)}</b><span>more name its duties</span></div><div><b>${own("controls").length}</b><span>controls owned</span></div><div><b>${own("risks").length}</b><span>risks owned</span></div><div><b>${own("actions").filter((a) => !a.closed).length}</b><span>open actions</span></div></div>
  <div class="grid2" style="align-items:start"><div class="stack">
    <div class="panel"><h2>Documents this role works with</h2><table class="t">${[...docsIn].sort((a, b) => b[1].length - a[1].length).map(([d, how]) => `<tr><td>${docLink(d)} ${esc(DOC[d].title)}</td><td class="small">${[...new Set(how)].join(", ")}</td><td>${fpBar(d)}</td></tr>`).join("") || `<tr><td class="muted">This role is not named in any issued document yet.</td></tr>`}</table></div>
    ${hits.length ? `<div class="panel"><h2>What the documents require of the ${esc(r.title)}</h2>${stmtList(hits)}</div>` : ""}
    ${asDuty.map(([o, l]) => `<div class="panel"><h2>As ${esc(OMSR_BY[o].name)}</h2><p class="small muted">Statements written for every ${esc(OMSR_BY[o].name)}, which this role is.</p>${stmtList(l, 12)}</div>`).join("")}</div>
    <div class="stack">
      ${own("controls").length ? `<div class="panel"><h2>Controls owned</h2>${healthBar(own("controls"))}${own("controls").map((c) => ctlChip(c.control_id)).join("")}</div>` : ""}
      ${own("risks").length ? `<div class="panel"><h2>Risks owned</h2>${own("risks").map((x) => `<div><a href="#/risk/${x.risk_id}">${x.risk_id}</a> ${esc(x.title)} ${rateChip(x.current_rating)}</div>`).join("")}</div>` : ""}
      ${own("kpis").length ? `<div class="panel"><h2>Measures owned</h2>${own("kpis").map((k) => `<div class="small"><b>${esc(k.name)}</b></div>${spark(SERIES[k.kpi_id], "#0B5563", 280, 30)}`).join("")}</div>` : ""}
      ${own("actions").filter((a) => !a.closed).length ? `<div class="panel"><h2>Open actions</h2><table class="t">${own("actions").filter((a) => !a.closed).map((a) => `<tr><td>${esc(a.title)}<div class="small muted">${esc(a.action_id)}</div></td><td class="small" style="${toDate(a.due) < TODAY ? "color:var(--fail)" : ""}">Due ${fmt(toDate(a.due))}</td></tr>`).join("")}</table></div>` : ""}
      ${lanes.length ? `<div class="panel"><h2>Process steps</h2>${lanes.map(([pm, l]) => `<div style="margin-bottom:6px"><a href="#/process/${pm.id}">${esc(pm.title)}</a> <span class="small muted">as ${esc(l.role)}</span><div class="small">${pm.steps.filter((s) => s.lane === l.id && s.type !== "start" && s.type !== "end").map((s) => `<a href="#/process/${pm.id}/${s.id}">${s.id} ${esc(s.name)}</a>`).join(", ")}</div></div>`).join("")}</div>` : ""}
      ${own("processes").length ? `<div class="panel"><h2>Processes owned</h2>${own("processes").map((p) => `<div class="small">${esc(p.process_id)} ${esc(p.title)}</div>`).join("")}</div>` : ""}
    </div></div>`);
});
route(/^\/duty\/([A-Z]+)$/, (id) => {
  const o = OMSR_BY[id]; if (!o) return go404(); const hs = dutyHolders(id); const hits = HITS[id] || [];
  page(o.elements.split("; ").map(Number), head(esc(o.name), esc(o.definition), `<a href="#/roles">Roles</a> / OMS duties`) + `
  <div class="grid2" style="align-items:start"><div class="panel"><h2>Carried by</h2><table class="t">${hs.map((r) => `<tr><td>${roleLink(r)}${DUTY[r.role_id].get(id) ? ` <span class="small muted">${esc(DUTY[r.role_id].get(id))}</span>` : ""}</td><td class="small">${(HOLD[r.role_id] || []).slice(0, 3).map((p) => personLink(p)).join(", ")}${(HOLD[r.role_id] || []).length > 3 ? "…" : ""}</td></tr>`).join("") || `<tr><td class="muted">Not assigned.</td></tr>`}</table></div>
    <div class="panel"><h2>Defined in</h2><p>${o.defined_in.split("; ").map((d) => docLink(d)).join(", ")}</p><p class="small muted">${o.derived_from ? `Worked out from the ${esc(o.derived_from)} register, so it follows the data.` : "Assigned in company/org/oms_roles.csv."}</p><div class="chips">${elChips(o.elements)}</div></div></div>
  ${hits.length ? `<div class="panel" style="margin-top:18px"><h2>${plural(hits.length, "binding statement")} name the ${esc(o.name)}</h2>${stmtList(hits, 20)}</div>` : ""}`);
});

// ---------- people ----------
route(/^\/people$/, () => {
  page(null, head("People", `${ACTIVE.length} staff, read from company/ACE_People.csv. Leavers stay on record so documents that still name them can be found.`, `<a href="#/company">Company</a>`) + `
  <div class="filters"><label>Function<select id="ff"><option value="">All</option>${FUNCS.map((f) => `<option value="${f.code}">${esc(f.name)}</option>`).join("")}</select></label>
    <label>Site<select id="fs"><option value="">All</option>${SITES.map((s) => `<option value="${s.site_code}">${esc(s.name)}</option>`).join("")}</select></label>
    <label>Status<select id="fx"><option value="">Current staff</option><option value="Left">Left</option><option value="all">Everyone</option></select></label><label>Find<input id="ft" type="search" placeholder="Name or title"></label></div>
  <div class="panel"><div class="scroll" style="max-height:none"><table class="t" id="pt"></table></div></div>`);
  const run = () => { const f = $("#ff").value, s = $("#fs").value, x = $("#fx").value, t = $("#ft").value.toLowerCase();
    const l = PEOPLE.filter((p) => (x === "all" || (x === "Left" ? p.st === "Left" : p.st !== "Left")) && (!f || p.fc === f) && (!s || p.s === s) && (!t || (p.n + " " + p.t).toLowerCase().includes(t)));
    $("#pt").innerHTML = `<tr><th>Name</th><th>Role</th><th>Function</th><th>Site</th><th>Reports to</th></tr>` + l.map((p) => `<tr><td>${personLink(p)}</td><td>${roleLink(ROLE[p.r], p.t)}</td><td class="small">${esc(p.f)}</td><td class="small">${esc(SITE[p.s]?.name || p.loc)}</td><td class="small">${personLink(PID[p.to])}</td></tr>`).join(""); };
  for (const id of ["ff", "fs", "fx", "ft"]) $("#" + id).oninput = run; run();
});
route(/^\/person\/(ACE-\d+)$/, (id) => {
  const p = PID[id]; if (!p) return go404(); const r = ROLE[p.r] || ROLE_BY[p.t];
  const team = ACTIVE.filter((x) => x.to === id); const mgr = PID[p.to];
  const named = DOCS.flatMap((d) => META.flatMap((f) => parseWho(d[f]).filter((w) => w.person === p).map((w) => ({ d, f, w }))));
  const ownC = CTLS.filter((c) => c.owner.startsWith(p.n + " ")), ownR = RISKS.filter((x) => x.owner.startsWith(p.n + " "));
  const hist = CHANGES.filter((c) => c.employee_id === id);
  page(null, head(esc(p.n), `${roleLink(r, p.t)}, ${esc(p.f)}. ${esc(SITE[p.s]?.name || p.loc)}.`, `<a href="#/people">People</a>`) + `
  ${p.st === "Left" ? `<div class="offline" style="font-size:14px">${esc(p.n)} left ACE on ${fmt(toDate(p.left))}. ${named.length ? `${named.length} document entries still name them and should be updated at the next revision.` : ""}</div>` : ""}
  <div class="grid3" style="align-items:start"><div class="panel"><h2>Position</h2><p>${roleLink(r, p.t)}<br><span class="small muted">${esc(p.d)}, ${esc(p.g)}</span></p><p>Reports to ${personLink(mgr) || "the Board"}${mgr ? `<span class="small muted">, ${esc(mgr.t)}</span>` : ""}</p>${PID[p.dl] ? `<p>Dotted line to ${personLink(PID[p.dl])}<span class="small muted">, ${esc(p.dlp)}</span></p>` : ""}</div>
    <div class="panel"><h2>Background</h2><p class="small">Joined ${fmt(toDate(p.hire))}</p><p class="small">${esc(p.q)}</p><p class="small"><a href="mailto:${esc(p.em)}">${esc(p.em)}</a> <span class="muted">(fictional)</span></p></div>
    <div class="panel"><h2>Team</h2>${team.map((x) => `<div class="small">${personLink(x)} <span class="muted">${esc(x.t)}</span></div>`).join("") || `<p class="muted small">No direct reports.</p>`}</div></div>
  <div class="grid2" style="align-items:start;margin-top:18px"><div class="panel"><h2>Named in documents</h2><table class="t">${named.map(({ d, f, w }) => `<tr><td>${docLink(d.id)} ${esc(d.title)}</td><td class="small">${MNAME[f]}</td><td class="small">${w.stale ? `<span class="st rejected">${staleNote(w)}</span>` : ""}</td></tr>`).join("") || `<tr><td class="muted">Not named personally. Documents name the role, which is how it should be.</td></tr>`}</table>
    ${r ? `<p class="small" style="margin-top:8px">As ${roleLink(r)}, ${esc(p.n.split(" ")[0])} is covered by ${plural((HITS[r.role_id] || []).length, "binding statement")}. <a href="#/role/${r.role_id}">See them</a>.</p>` : ""}</div>
    <div class="stack">${ownC.length ? `<div class="panel"><h2>Controls owned</h2>${ownC.map((c) => ctlChip(c.control_id)).join("")}</div>` : ""}${ownR.length ? `<div class="panel"><h2>Risks owned</h2>${ownR.map((x) => `<div><a href="#/risk/${x.risk_id}">${x.risk_id}</a> ${esc(x.title)}</div>`).join("")}</div>` : ""}
      ${hist.length ? `<div class="panel"><h2>History</h2>${hist.map((c) => `<div class="small">${fmt(toDate(c.date))}: ${esc(c.event)}${c.from_role ? " from " + esc(c.from_role) : ""}${c.to_role ? " to " + esc(c.to_role) : ""}. ${esc(c.note)}</div>`).join("")}</div>` : ""}</div></div>`);
});

// ---------- the ONE model: how the dimensions connect ----------
route(/^\/model$/, () => {
  const n = { secs: DOCS.reduce((a, d) => a + d.sections.length, 0), roleHits: Object.entries(HITS).filter(([k]) => ROLE[k]).reduce((a, [, l]) => a + l.length, 0) };
  const dims = [
    ["Documents", "#/library", `${DOCS.length} documents, ${n.secs.toLocaleString()} sections, ${WORK.length.toLocaleString()} binding statements`, "The spine. Every section carries OMS tags; every binding paragraph is styled as what it is.", "#17262E"],
    ["OMS elements", "#/", `10 elements, 54 expectations, ${[...COV.values()].filter((c) => c.n).length} written`, "What good looks like. Tags link each section to the expectation it serves.", ECOL[1]],
    ["Organisation", "#/org", `${FUNCS.length} functions, ${ROLES.length} roles, ${ACTIVE.length} people`, "Who does it. Statements name roles; the staff list says who holds them today.", ECOL[3]],
    ["Risk", "#/risk", `${RISKS.length} risks, ${CTLS.length} controls`, "What could go wrong. Each control is a statement in a document with an ID and an owner.", ECOL[5]],
    ["Assets and sites", "#/company", `${SITES.length} sites, ${(REG["AIM-REG-002"] || []).length} assets`, "Where it happens. Documents say where they apply; risks and events are logged by site.", ECOL[6]],
    ["Process", "#/process", `${(REG["BPM-REG-001"] || []).length} processes, ${D.processes.length} modelled`, "How work flows. Steps name roles and documents and perform controls.", ECOL[7]],
    ["Performance", "#/performance", `${KPIS.length} measures, ${EVENTS.length} events`, "Whether it works. Measures and events test the controls and feed learning.", ECOL[9]],
  ];
  const cx = 330, cy = 250, R = 190;
  const g = dims.slice(1).map((d, i) => { const a = -Math.PI / 2 + i * 2 * Math.PI / 6; const x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
    return `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="#C7D2D6" stroke-width="2"/><a href="${d[1]}" class="dim"><circle cx="${x}" cy="${y}" r="62" fill="${d[4]}"/><text x="${x}" y="${y + 5}" text-anchor="middle" fill="${lum(d[4]) > 0.2 ? "#17262E" : "#fff"}">${esc(d[0])}</text></a>`; }).join("");
  page(null, head("How ACE fits the ONE model", "ONE reads a company along several dimensions at once. The approved documents sit in the middle: the tags and styles written into them connect everything else. Swap in another company's documents, staff list and registers, and the same pages appear for them.", `<a href="#/company">Company</a>`) + `
  <div class="grid2" style="grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);align-items:start"><div class="panel" style="position:sticky;top:14px"><svg class="model" viewBox="60 -20 540 540" role="img" aria-label="The ONE dimensions">${g}<a href="#/library" class="dim"><circle cx="${cx}" cy="${cy}" r="78" fill="#17262E"/><text x="${cx}" y="${cy - 4}" text-anchor="middle" fill="#fff">Documents</text><text x="${cx}" y="${cy + 16}" text-anchor="middle" fill="#fff" class="sm">the spine</text></a></svg></div>
    <div class="stack">${dims.map((d) => `<a class="card" style="--c:${d[4]}" href="${d[1]}"><h3>${esc(d[0])}</h3><p class="small" style="margin:0 0 4px">${esc(d[3])}</p><div class="row"><span>${d[2]}</span></div></a>`).join("")}</div></div>
  <div class="panel" style="margin-top:18px"><h2>Follow one thread</h2><p>Start anywhere and the links carry you through every dimension. For example:</p>
    <ol class="thread-steps"><li><a href="#/site/PAP">Pommerac A</a>, a manned platform in the Gulf of Paria (site)</li><li><a href="#/risk/R-PAP-01">R-PAP-01</a> Loss of containment from the export pipeline (risk)</li>
      <li><a href="#/barriers">Its barriers</a>, each written in a document with a Control ID (controls)</li><li><a href="#/doc/ACE-AIM-PRA-001">The inspection practice</a> that holds them (document)</li>
      <li>${roleLink(ROLE_BY["Inspection Lead"])}, who owns them, and ${personLink(HOLD[ROLE_BY["Inspection Lead"]?.role_id]?.[0])}, who holds that role today (organisation)</li><li><a href="#/el/6">Element 6</a>, the expectation they serve (OMS)</li><li><a href="#/performance">The measures</a> that show whether they work (performance)</li></ol></div>
  <div class="panel" style="margin-top:18px"><h2>Bringing your own company</h2><p>Everything ACE-specific lives in plain files that a company already has, or can export:</p>
    <table class="t"><tr><th>Dimension</th><th>Where it comes from</th></tr><tr><td>Documents</td><td>Approved Word files written to the ONE document standard (a document library, SharePoint or a repository)</td></tr><tr><td>Organisation</td><td>Staff list, role catalogue, functions and sites, as spreadsheets</td></tr><tr><td>Risk</td><td>Risk and control registers</td></tr><tr><td>Process</td><td>A process register and process models</td></tr><tr><td>Performance</td><td>Monthly measures and the event log</td></tr></table>
    <p class="small muted" style="margin-top:8px">A company with several sites reads them side by side. A group with several OMSs can load each one and compare documents, coverage and processes between them.</p></div>`);
});

// ---------- document map ----------
route(/^\/library\/map$/, () => {
  const cols = ["Manual", "Policy", "Standard", "Practice", "Process", "Procedure", "Task & record"];
  const planned = (REG["DOC-REG-001"] || []).filter((d) => d.status === "Planned").map((d) => ({ id: d.doc_id, title: d.title, layer: TYPE_LAYER[d.doc_id.split("-")[2]] || "Other", planned: true, system: d.doc_id.split("-")[1] }));
  const refsOf = (d) => [...new Set(d.sections.flatMap((s) => s.blocks.flatMap((b) => b.r || [])))].filter((r) => r !== d.id);
  const referenced = new Set(DOCS.flatMap(refsOf));
  const nodes = [...DOCS.map((d) => ({ id: d.id, title: d.title, layer: d.layer, system: d.system, d })), ...planned.filter((p) => referenced.has(p.id))];
  const W = 1180, colW = W / cols.length, byCol = {}; for (const n of nodes) (byCol[cols.includes(n.layer) ? n.layer : "Task & record"] ||= []).push(n);
  const H = Math.max(560, 60 + Math.max(...Object.values(byCol).map((l) => l.length)) * 38);
  const P = {}; for (const [c, l] of Object.entries(byCol)) { l.sort((a, b) => a.system.localeCompare(b.system) || a.id.localeCompare(b.id)); const gap = Math.min(52, (H - 70) / l.length); const top = 60 + ((H - 70) - gap * l.length) / 2; l.forEach((n, i) => (P[n.id] = [cols.indexOf(c) * colW + colW / 2, top + gap * (i + 0.5)])); }
  const domEl = (id) => { const f = FP[id] || {}; return +Object.entries(f).sort((a, b) => b[1] - a[1])[0]?.[0] || 0; };
  let edges = "";
  for (const d of DOCS) { const p = parentOf(d); if (p && P[p]) edges += `<path class="pe" data-a="${d.id}" data-b="${p}" d="M${P[d.id][0]},${P[d.id][1]} C${P[d.id][0] - colW / 2},${P[d.id][1]} ${P[p][0] + colW / 2},${P[p][1]} ${P[p][0]},${P[p][1]}"/>`;
    if (d.id !== MAN.id) for (const r of refsOf(d)) if (P[r] && r !== p) edges += `<path class="re" data-a="${d.id}" data-b="${r}" d="M${P[d.id][0]},${P[d.id][1]} Q${(P[d.id][0] + P[r][0]) / 2},${(P[d.id][1] + P[r][1]) / 2 - 40} ${P[r][0]},${P[r][1]}"/>`; }
  const dots = nodes.map((n) => { const [x, y] = P[n.id]; const k = n.d ? WORK.filter((s) => s.d.id === n.id).length : 0; const r = n.planned ? 7 : 6 + Math.sqrt(k) * 0.9; const e = n.d ? domEl(n.id) : 0;
    return `<a ${n.d ? `href="#/doc/${n.id}"` : ""} class="dn${n.planned ? " planned" : ""}" data-id="${n.id}" data-f="${esc(n.d ? n.d.func : "")}" data-e="${n.d ? Object.keys(FP[n.id] || {}).join(" ") : ""}"><circle cx="${x}" cy="${y}" r="${r}" fill="${e ? ECOL[e] : "#fff"}" data-tip="<b>${esc(n.id)}</b>${esc(n.title)}${n.planned ? "<br>Planned, not yet issued" : `<br>${k} binding statements`}"/>
      <text x="${x + r + 4}" y="${y + 4}">${esc(n.id.replace("ACE-", ""))}</text></a>`; }).join("");
  const fns = [...new Set(DOCS.map((d) => d.func).filter(Boolean))].sort();
  page(null, head("Document map", "Every document placed by its layer, coloured by the element it serves most, sized by its binding statements. Solid lines run to the parent document; thin lines are references. Hollow dots are documents that are referenced but not yet written.", `<a href="#/library">Library</a>`) + libTabs("map") + `
  <div class="filters"><label>Highlight element<select id="me"><option value="">None</option>${ELS.map((e) => `<option value="${e.id}">${e.id}. ${esc(e.title)}</option>`).join("")}</select></label>
    <label>Highlight function<select id="mf"><option value="">None</option>${fns.map((f) => `<option>${esc(f)}</option>`).join("")}</select></label></div>
  <div class="panel" style="overflow:auto"><svg class="dmap" viewBox="0 0 ${W} ${H}" style="min-width:900px">${cols.map((c, i) => `<text class="colh" x="${i * colW + colW / 2}" y="26" text-anchor="middle">${c}</text><line x1="${(i + 1) * colW}" x2="${(i + 1) * colW}" y1="10" y2="${H}" stroke="#E8EDEF"/>`).join("")}<g>${edges}</g><g>${dots}</g></svg></div>`);
  const svg = $(".dmap");
  const hl = (ids) => { svg.classList.toggle("focus", !!ids); for (const d of svg.querySelectorAll(".dn")) d.classList.toggle("on", !!ids && ids.has(d.dataset.id)); for (const l of svg.querySelectorAll(".pe,.re")) l.classList.toggle("on", !!ids && ids.has(l.dataset.a) && ids.has(l.dataset.b)); };
  svg.addEventListener("mouseover", (e) => { const n = e.target.closest(".dn"); if (!n) return; const id = n.dataset.id; const s = new Set([id]); for (const l of svg.querySelectorAll(".pe,.re")) if (l.dataset.a === id || l.dataset.b === id) { s.add(l.dataset.a); s.add(l.dataset.b); } hl(s); });
  svg.addEventListener("mouseleave", () => filt());
  const filt = () => { const e = $("#me").value, f = $("#mf").value; if (!e && !f) return hl(null); hl(new Set([...svg.querySelectorAll(".dn")].filter((d) => (!e || d.dataset.e.split(" ").includes(e)) && (!f || d.dataset.f === f)).map((d) => d.dataset.id))); };
  $("#me").oninput = filt; $("#mf").oninput = filt;
});

go();
refreshNoteCount();
