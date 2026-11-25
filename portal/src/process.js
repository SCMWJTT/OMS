// =====================================================================================================================
// PROCESS AND IMPROVEMENT DIMENSIONS
// A process has three layers, all keyed by process and step ID:
//   Design  — the process model file (processes/*.json, ONE-PRS/2)
//   Run     — the ledger of real cases (registers/BPM-LOG-<process>_cases.csv and _events.csv)
//   Improve — the CI register (registers/CI-REG-001.csv) and the revision history in the model
// Value is worked out from Design + Run with the assumptions in registers/BPM-VAL-001.csv. Nothing here is typed in.
// =====================================================================================================================
const VAL = Object.fromEntries((REG["BPM-VAL-001"] || []).map((r) => [r.key, +r.value]));
const PRS = D.processes || []; const PRSBY = Object.fromEntries(PRS.map((p) => [p.id, p]));
const BPMREG = REG["BPM-REG-001"] || [];
const CIS = REG["CI-REG-001"] || []; const CIH = REG["CI-REG-001_history"] || [];
const DAY = 864e5, HR = 36e5;
const PT = (s) => (s ? new Date(s.length === 10 ? s + "T00:00" : s.replace(" ", "T")) : null);
const median = (a) => { if (!a || !a.length) return null; const b = [...a].sort((x, y) => x - y), m = b.length >> 1; return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2; };
const usd = (v) => (v == null || isNaN(v) ? "–" : Math.abs(v) >= 1e6 ? `$${(v / 1e6).toFixed(2)}M` : Math.abs(v) >= 1e3 ? `$${Math.round(v / 1e3).toLocaleString()}k` : `$${Math.round(v)}`);
const dfmt = (d) => (d == null || isNaN(d) ? "–" : d < 1 ? `${Math.max(1, Math.round(d * 24))} h` : `${d.toFixed(d < 10 ? 1 : 0)} d`);
const hfmt = (h) => (h == null || isNaN(h) ? "–" : h < 1 ? `${Math.round(h * 60)} min` : `${h.toFixed(h < 10 ? 1 : 0)} h`);
const pct = (v) => (v == null || isNaN(v) ? "–" : `${Math.round(v)}%`);
const OFFSHORE = new Set(["PAP", "CHB", "SAP"]);
const FCOL = { OPS: "#2F6F8F", ENP: "#7A5C9E", SCM: "#B07A1F", HSE: "#B5473A", EXEC: "#0B5563", HR: "#6E9A2E", ITD: "#3D4FA1", FIN: "#5B7F3A", WEL: "#8E5B3A", EXD: "#2E8A78", BDM: "#A0527A", LGA: "#57656C", CCS: "#6B7B83", CTR: "#7D8D95" };
const fname = (code) => (code === "CTR" ? "Contractors" : FUNC[code]?.name || code);
const fcol = (code) => FCOL[code] || "#5B6B73";
const fwd = (s) => [...(s.next || []), ...(s.branches || []).filter((b) => !b.loop).map((b) => b.to)];
const outs = (s) => [...(s.next || []), ...(s.branches || []).map((b) => b.to)];
const laneOf = (m, id) => m.lanes.find((l) => l.id === id) || {};
const laneFn = (m, id) => laneOf(m, id).function || "CTR";
const laneRate = (m, id) => { const l = laneOf(m, id); if (l.external) return VAL.RATE_CONTR || 85; const g = (ROLE[l.role_id]?.grade || "").slice(0, 2); return VAL["RATE_" + g] || VAL.RATE_L6 || 21; };
const TRIP_COST = () => (VAL.HELI_HOUR || 6500) * (VAL.HELI_TRIP_H || 1.2) + (VAL.BOAT_DAY || 14000) * 0.5;
const isWork = (s) => s && s.type !== "start" && s.type !== "end";
const ciFor = (pid, sid) => CIS.filter((c) => c.process_id === pid && (!sid || c.step_id === sid));
const STAGES = ["Idea", "Assessed", "In progress", "Verified", "Standardised", "Closed", "Parked"];
const STCOL = { Idea: "#A8B5BB", Assessed: "#7D9CB0", "In progress": "#E0AE2E", Verified: "#3E9A62", Standardised: "#0B5563", Closed: "#4E5F68", Parked: "#C9CFD2" };
const stageChip = (s) => `<span class="stage" style="--c:${STCOL[s] || "#999"}">${esc(s)}</span>`;
const polSec = (ref) => { const [d, bm] = (ref || "").split("#"); const doc = DOC[d]; const s = doc?.sections.find((x) => x.bm === bm); return { d, bm, doc, s }; };
const VALUES = (() => { const d = DOC["ACE-LDR-POL-001"]; return d ? d.sections.filter((s) => /^VAL_/.test(s.bm)).map((s) => ({ bm: s.bm, name: s.title.replace(/^[\d.]+\s*/, "").replace(/^Value:\s*/, "") })) : []; })();
const valuesIn = (s) => { const t = (s?.blocks || []).map((b) => b.t).join(" "); return VALUES.filter((v) => t.includes(v.name)); };
const valueChip = (v) => `<a class="valchip" href="#/doc/ACE-LDR-POL-001/${v.bm}">${esc(v.name)}</a>`;
const commitLink = (ref) => { const p = polSec(ref); return p.s ? `<a href="#/doc/${p.d}/${p.bm}">${esc(p.s.title.replace(/^\d+(\.\d+)*\s*/, ""))}</a> <span class="small muted">${p.d}</span>` : esc(ref); };

// site production for the risk-exposure value model (average of the last six months in the performance register)
const SITEPROD = (() => { const r = {}; const m = (REG["PRF-REG-001_monthly"] || []).filter((x) => x.kpi_id === "PROD-OIL"); const months = [...new Set(m.map((x) => x.month))].sort().slice(-6);
  for (const x of m) if (months.includes(x.month)) (r[x.site] ||= []).push(+x.value); const o = {}; for (const k in r) o[k] = r[k].reduce((a, b) => a + b, 0) / r[k].length; o.CPF = o.ACE || 0; return o; })();

// ---------------------------------------------------------------- ledger and measures
const LEDGER = {};
function ledger(m) {
  if (LEDGER[m.id]) return LEDGER[m.id];
  const byCase = {};
  for (const e of REG[m.ledger + "_events"] || []) (byCase[e.case_id] ||= []).push({ ...e, a: PT(e.arrived), s: PT(e.started), f: PT(e.finished), rw: e.rework === "1" });
  for (const k in byCase) byCase[k].sort((p, q) => p.a - q.a);
  const cases = (REG[m.ledger + "_cases"] || []).map((c) => ({ ...c, o: PT(c.opened), cl: PT(c.closed), dueD: PT(c.due), defD: PT(c.deferred_to), ev: byCase[c.case_id] || [] }));
  return (LEDGER[m.id] = { cases, byId: Object.fromEntries(cases.map((c) => [c.case_id, c])) });
}
const siteOk = (c, site) => !site || (site === "OFF" ? OFFSHORE.has(c.site) : site === "ON" ? !OFFSHORE.has(c.site) : c.site === site);
const pick = (m, f = {}) => ledger(m).cases.filter((c) => (!f.year || (c.o && c.o.getFullYear() === +f.year)) && siteOk(c, f.site) && (!f.rev || c.revision === f.rev));

function stats(m, cases) {
  const S = {}; for (const s of m.steps) S[s.id] = { n: 0, wait: [], work: [], span: [], rw: 0, waitSum: 0, workSum: 0, inQ: 0 };
  const allowed = new Set(); for (const s of m.steps) for (const n of outs(s)) allowed.add(`${s.id}>${n}`);
  const T = {}, FN = {}, HO = {}, trips = new Set(), cyc = [];
  let workH = 0, spanH = 0, labour = 0, conf = 0, confN = 0, rft = 0, rftN = 0, waitCost = 0, valueDel = 0, done = 0, onT = 0, onN = 0, defN = 0, lateN = 0;
  const fnRow = (fn) => (FN[fn] ||= { steps: 0, work: 0, wait: 0, cost: 0 });
  for (const c of cases) {
    let ok = true, prev = null, cw = 0, anyRw = false;
    for (const e of c.ev) {
      const st = S[e.step_id], sd = m.steps.find((x) => x.id === e.step_id); if (!st) continue; st.n++;
      const fn = laneFn(m, e.lane);
      if (e.s && isWork(sd)) { const w = (e.s - e.a) / DAY; st.wait.push(w); st.waitSum += w; cw += w; fnRow(fn).wait += w * 24; }
      if (e.s && e.f && isWork(sd)) { const h = (e.f - e.s) / HR, r = laneRate(m, e.lane); st.work.push(h); st.workSum += h; workH += h; labour += h * r; const x = fnRow(fn); x.steps++; x.work += h; x.cost += h * r; }
      if (e.f && isWork(sd)) { st.span.push((e.f - e.a) / DAY); spanH += (e.f - e.a) / HR; }
      if (!e.f && isWork(sd)) st.inQ++;
      if (e.rw) { st.rw++; anyRw = true; }
      if (e.trip) trips.add(e.trip);
      if (prev) { const k = `${prev.step_id}>${e.step_id}`; T[k] = (T[k] || 0) + 1; if (!allowed.has(k)) ok = false;
        const f1 = laneFn(m, prev.lane), f2 = fn; if (f1 !== f2) { const hk = `${f1}>${f2}`; (HO[hk] ||= { n: 0, wait: 0 }); HO[hk].n++; if (e.s) HO[hk].wait += (e.s - e.a) / DAY; } }
      prev = e;
    }
    if (c.ev.length) { confN++; if (ok) conf++; }
    if (c.cl) { done++; cyc.push((c.cl - c.o) / DAY); rftN++; if (!anyRw) rft++; }
    if (m.value?.model === "deferred-benefit") {
      const b = VAL[c.value_key] || 0;
      if (c.outcome === "Closed") valueDel += b;
      if (!["Rejected", "Cancelled"].includes(c.outcome)) waitCost += (cw * b) / 365;
    }
    if (m.value?.model === "risk-exposure") {
      const insp = c.ev.find((e) => e.step_id === "S09" && e.f)?.f; const cons = (VAL.INSP_SHUTDOWN_D || 14) * (SITEPROD[c.site] || 0) * (VAL.OIL_PRICE || 95);
      if (c.dueD) { const end = insp || (c.dueD < TODAY ? TODAY : null); if (end) { const late = Math.max(0, (end - c.dueD) / DAY); waitCost += (late * (VAL.INSP_POF_OVERDUE || 0.02) / 365) * cons; } }
      if (insp) valueDel += ((VAL.INSP_POF_OVERDUE || 0.02) - (VAL.INSP_POF_DONE || 0.002)) * cons;
      if (insp && c.dueD) { onN++; if (insp <= new Date(+c.dueD + DAY)) onT++; else if (!c.defD || insp > new Date(+c.defD + DAY)) lateN++; }
      if (c.defD) defN++;
    }
  }
  const ctls = [...new Set(m.steps.flatMap((s) => s.controls || []))].map((id) => CTL[id]).filter(Boolean);
  const logistics = trips.size * TRIP_COST();
  return { S, T, FN, HO, n: cases.length, done, cycle: median(cyc), rft: rftN ? (100 * rft) / rftN : null, conformance: confN ? (100 * conf) / confN : null,
    flowEff: spanH ? (100 * workH) / spanH : null, workH, labour, logistics, trips: trips.size, waitCost, valueDel,
    control_health: ctls.length ? (100 * ctls.filter((c) => c.health === "Effective").length) / ctls.length : null, ctls,
    on_time: onN ? (100 * onT) / onN : null, late: onN ? (100 * lateN) / onN : null, deferral_rate: cases.length && m.value?.model === "risk-exposure" ? (100 * defN) / cases.length : null };
}
const kpiVal = (k, st) => ({ cycle_median_days: st.cycle, right_first_time: st.rft, control_health: st.control_health, conformance: st.conformance, on_time: st.on_time, deferral_rate: st.deferral_rate }[k.measure]);
const kpiFmt = (k, v) => (v == null ? "–" : k.measure === "cycle_median_days" ? `${Math.round(v)} d` : pct(v));
const kpiOk = (k, v) => v == null || k.threshold == null ? null : k.better === "down" ? v <= k.threshold : v >= k.threshold;
const YEARS = ["2024", "2025", "2026"];

// ---------------------------------------------------------------- map layout and drawing
const NW = 120, NH = 48, CW = 152, X0 = 176, SLOT = 64;
function layout(m, group) {
  const S = Object.fromEntries(m.steps.map((s) => [s.id, s])); const col = {};
  const q = m.steps.filter((s) => s.type === "start").map((s) => [s.id, 0]); let guard = 0;
  while (q.length && guard++ < 4000) { const [k, c] = q.shift(); if (col[k] !== undefined && col[k] >= c) continue; col[k] = c; for (const n of fwd(S[k])) if (S[n]) q.push([n, c + 1]); }
  const rows = group === "fn" ? [...new Set(m.lanes.map((l) => l.function || "CTR"))].map((f) => ({ key: f, label: fname(f), fn: f })) : m.lanes.map((l) => ({ key: l.id, label: l.role, fn: l.function || "CTR", lane: l }));
  const rowOf = (s) => rows.findIndex((r) => (group === "fn" ? r.key === laneFn(m, s.lane) : r.key === s.lane));
  const slot = {}, used = {};
  for (const s of [...m.steps].sort((a, b) => col[a.id] - col[b.id])) { const k = `${rowOf(s)}:${col[s.id]}`; slot[s.id] = used[k] || 0; used[k] = (used[k] || 0) + 1; }
  const rowH = rows.map((_, i) => Math.max(1, ...Object.entries(used).filter(([k]) => +k.split(":")[0] === i).map(([, v]) => v)) * SLOT + 30);
  const top = m.cycle ? 40 : 10; const rowY = []; let y = top; for (const h of rowH) { rowY.push(y); y += h; }
  const maxCol = Math.max(...Object.values(col));
  const P = {}; for (const s of m.steps) { const r = rowOf(s); P[s.id] = { x: X0 + col[s.id] * CW + 16, y: rowY[r] + 18 + slot[s.id] * SLOT, row: r }; }
  return { rows, rowY, rowH, P, S, W: X0 + (maxCol + 1) * CW + 190, H: y + 18, top, maxCol };
}
const heat = (d, max) => { if (d == null) return "#FFFFFF"; const t = Math.min(1, d / (max || 1)); const c = [[255, 255, 255], [250, 222, 160], [232, 140, 90], [201, 71, 63]]; const i = Math.min(2, Math.floor(t * 3)), f = t * 3 - i; const a = c[i], b = c[i + 1]; return `rgb(${a.map((v, k) => Math.round(v + (b[k] - v) * f)).join(",")})`; };
const wrap = (t, n = 17) => { const w = t.split(" "); const L = [""]; for (const x of w) { if ((L[L.length - 1] + " " + x).trim().length > n && L[L.length - 1]) L.push(x); else L[L.length - 1] = (L[L.length - 1] + " " + x).trim(); } return L.slice(0, 3); };
const FLOWSTYLE = { information: { c: "#2F7FB8", d: "6 4", w: 2 }, material: { c: "#B07A1F", d: "2 4", w: 3.2 }, people: { c: "#7A4FA0", d: "10 4 2 4", w: 2.4 } };

function drawMap(m, o) {
  const L = layout(m, o.group), { P, S } = L, st = o.st, st2 = o.st2;
  const maxWait = st ? Math.max(1, ...m.steps.map((s) => median(st.S[s.id].wait) || 0)) : 1;
  const maxT = st ? Math.max(1, ...Object.values(st.T)) : 1;
  const traced = o.trace ? new Set(o.trace.ev.map((e) => e.step_id)) : null;
  const cx = (id) => P[id].x + NW / 2, cy = (id) => P[id].y + NH / 2;
  let g = `<defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#4E5F68"/></marker>
    <marker id="pr" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#C9473F"/></marker>
    <marker id="pc" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0B5563"/></marker></defs>`;
  L.rows.forEach((r, i) => { g += `<rect class="lane-bg" x="0" y="${L.rowY[i]}" width="${L.W}" height="${L.rowH[i]}"/><rect x="0" y="${L.rowY[i]}" width="6" height="${L.rowH[i]}" fill="${fcol(r.fn)}"/>
    ${wrap(r.label, 22).map((t, k) => `<text class="lane-name" x="16" y="${L.rowY[i] + 22 + k * 15}">${esc(t)}</text>`).join("")}<text class="lane-fn" x="16" y="${L.rowY[i] + 22 + Math.min(3, wrap(r.label, 22).length) * 15}" fill="${fcol(r.fn)}">${o.group === "fn" ? "" : esc(fname(r.fn))}${r.lane?.external ? " (external)" : ""}</text>`; });
  // cycle arc over the top
  if (m.cycle && P[m.cycle.from] && P[m.cycle.to]) { const a = m.cycle.from, b = m.cycle.to;
    g += `<path class="cyc" d="M${cx(a)},${P[a].y} C${cx(a)},${8} ${cx(b)},${8} ${cx(b)},${P[b].y - 2}" marker-end="url(#pc)"/><text class="cyc-t" x="${(cx(a) + cx(b)) / 2}" y="20" text-anchor="middle">↻ ${esc(m.cycle.label || m.cycle.name)}</text>`; }
  // sequence flows
  for (const s of m.steps) {
    const all = [...(s.next || []).map((to) => ({ to })), ...(s.branches || [])];
    for (const b of all) { if (!P[b.to]) continue;
      const a = P[s.id], t = P[b.to], back = t.x <= a.x, laneChange = o.group === "fn" ? laneFn(m, s.lane) !== laneFn(m, S[b.to].lane) : s.lane !== S[b.to].lane;
      const n = st ? st.T[`${s.id}>${b.to}`] || 0 : 0; const w = st ? (n ? 1 + 6 * Math.sqrt(n / maxT) : 0.8) : laneChange ? 2.2 : 1.3;
      const cls = `flow${laneChange ? " handoff" : ""}${b.loop ? " rework" : ""}${st && !n ? " unused" : ""}${traced && traced.has(s.id) && traced.has(b.to) ? " traced" : ""}`;
      let d; if (back) { const yb = Math.max(a.y, t.y) + NH + 26; d = `M${cx(s.id)},${a.y + NH} C${cx(s.id)},${yb} ${cx(b.to)},${yb} ${cx(b.to)},${t.y + NH + 2}`; }
      else d = `M${a.x + NW},${cy(s.id)} C${a.x + NW + 30},${cy(s.id)} ${t.x - 30},${cy(b.to)} ${t.x - 2},${cy(b.to)}`;
      g += `<path class="${cls}" d="${d}" style="stroke-width:${w.toFixed(1)}" marker-end="url(#${b.loop ? "pr" : "pa"})"${st ? ` data-tip="${esc(s.name)} → ${esc(S[b.to].name)}<br>${n.toLocaleString()} times"` : ""}/>`;
      if (b.label) { const lx = back ? (cx(s.id) + cx(b.to)) / 2 : t.x - 8, ly = back ? Math.max(a.y, t.y) + NH + 22 : cy(b.to) - 7;
        g += `<text class="blabel${b.loop ? " rework" : ""}" x="${lx}" y="${ly}" text-anchor="${back ? "middle" : "end"}">${esc(b.label)}${b.p != null && !st ? ` · ${Math.round(b.p * 100)}%` : ""}</text>`; } }
  }
  // typed flows: information, material, people (with moving markers)
  const ext = {}; let ei = 0;
  for (const f of m.flows || []) { if (!o.ov[f.type] || !P[f.from]) continue; const sty = FLOWSTYLE[f.type];
    let x2, y2; if (P[f.to]) { x2 = cx(f.to); y2 = cy(f.to); } else { if (!ext[f.to]) ext[f.to] = { y: P[f.from].y, i: ei++ }; x2 = L.W - 150; y2 = ext[f.to].y + NH / 2; }
    const x1 = cx(f.from), y1 = cy(f.from), mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - 40 - (f.type === "people" ? 24 : f.type === "material" ? 12 : 0);
    const d = `M${x1},${y1} Q${mx},${my} ${x2},${y2}`;
    g += `<path class="tflow" d="${d}" stroke="${sty.c}" stroke-dasharray="${sty.d}" stroke-width="${sty.w}" data-tip="<b>${esc(f.type[0].toUpperCase() + f.type.slice(1))}</b> ${esc(f.carries || "")}"/>`;
    if (o.animate) g += `<circle r="${f.type === "material" ? 4.5 : 3.6}" fill="${sty.c}">${f.type === "material" ? "" : ""}<animateMotion dur="${f.type === "people" ? 3.6 : f.type === "material" ? 5 : 2.6}s" repeatCount="indefinite" path="${d}"/></circle>`;
  }
  for (const [pid, e] of Object.entries(ext)) { const t = PRSBY[pid] ? pid : pid; const reg = BPMREG.find((r) => r.process_id === pid);
    g += `<a href="${PRSBY[pid] ? `#/process/${pid}` : DOC[pid] ? `#/doc/${pid}` : "#/process"}"><rect class="extbox" x="${L.W - 150}" y="${e.y}" width="140" height="${NH}" rx="6"/><text class="ext-t" x="${L.W - 80}" y="${e.y + 19}" text-anchor="middle">${esc(t)}</text><text class="ext-s" x="${L.W - 80}" y="${e.y + 34}" text-anchor="middle">${esc((reg?.title || "Another process").replace(/ Process$/, "").slice(0, 24))}</text></a>`; }
  // nodes
  for (const s of m.steps) {
    const p = P[s.id], x = p.x, y = p.y, ss = st?.S[s.id];
    let fill = "#fff", sub = "";
    if (o.mode === "actual" && ss && isWork(s)) { const w = median(ss.wait); fill = heat(w, maxWait); sub = ss.n ? `wait ${dfmt(w)} · work ${hfmt(median(ss.work))}` : "not used"; }
    if (o.mode === "compare" && st2 && isWork(s)) { const a = median(st.S[s.id].span), b = median(st2.S[s.id].span); if (a != null && b != null) { const r = (b - a) / (a || 1); fill = r < -0.1 ? "#CFEBD8" : r > 0.1 ? "#F6D2CC" : "#F1F4F5"; sub = `${dfmt(a)} → ${dfmt(b)}`; } }
    const cis = ciFor(m.id, s.id).filter((c) => !["Closed", "Parked"].includes(c.stage)).length;
    const cls = `pnode${o.sel === s.id ? " sel" : ""}${traced ? (traced.has(s.id) ? " on" : " dim") : ""}${(m.history || []).some((h) => (h.changed_steps || []).includes(s.id)) && o.mode === "compare" ? " changed" : ""}`;
    let shape;
    if (s.type === "start" || s.type === "end") shape = `<circle cx="${x + NW / 2}" cy="${y + NH / 2}" r="17" fill="#fff" stroke="#17262E" stroke-width="${s.type === "end" ? 3.4 : 1.4}"/>` + wrap(s.name, 20).map((t, k) => `<text class="nl" x="${x + NW / 2}" y="${y + NH + 6 + k * 12}" text-anchor="middle">${esc(t)}</text>`).join("");
    else if (s.type === "xor") shape = `<path d="M${x + NW / 2},${y - 4} L${x + NW + 2},${y + NH / 2} L${x + NW / 2},${y + NH + 4} L${x - 2},${y + NH / 2} Z" fill="${fill}" stroke="#17262E" stroke-width="1.4"/>` + wrap(s.name, 16).map((t, k, A) => `<text class="nt" x="${x + NW / 2}" y="${y + NH / 2 + 4 - (A.length - 1) * 6 + k * 12}" text-anchor="middle">${esc(t)}</text>`).join("");
    else shape = `<rect x="${x}" y="${y}" width="${NW}" height="${NH}" rx="7" fill="${fill}" stroke="#17262E" stroke-width="1.3"/>` + wrap(s.name, 17).map((t, k, A) => `<text class="nt" x="${x + NW / 2}" y="${y + NH / 2 + 4 - (A.length - 1) * 6.5 + k * 13}" text-anchor="middle">${esc(t)}</text>`).join("");
    const marks = (s.type === "start" || s.type === "end" ? "" : `<text class="sid" x="${x + 2}" y="${y - 6}">${s.id}${s.value ? ` · ${s.value}` : ""}</text>`)
      + (o.ov.ctl && (s.controls || []).length ? `<g data-tip="${(s.controls || []).map((c) => `<b>${c}</b> ${esc(CTL[c]?.statement || "")} (${esc(CTL[c]?.health || "")})`).join("<br>")}"><circle cx="${x + NW - 4}" cy="${y + 2}" r="8" fill="${(s.controls || []).some((c) => CTL[c]?.health === "Degraded" || CTL[c]?.health === "Failed") ? "#E0AE2E" : "#B33A3A"}"/><text class="mk" x="${x + NW - 4}" y="${y + 6}" text-anchor="middle">${s.controls.length}</text></g>` : "")
      + (o.ov.doc && (s.doc_refs || []).length ? `<g data-tip="${(s.doc_refs || []).map((r) => { const [d, bm] = r.split("#"); return `${d} ${esc(DOC[d]?.sections.find((x) => x.bm === bm)?.title || "")}`; }).join("<br>")}"><path d="M${x + 4},${y + NH - 14} h9 l4,4 v12 h-13 z" fill="#fff" stroke="#4E5F68"/><text class="mk2" x="${x + 21}" y="${y + NH - 2}">${s.doc_refs.length}</text></g>` : "")
      + (cis ? `<g data-tip="${cis} open improvement item${cis > 1 ? "s" : ""}"><circle cx="${x + 2}" cy="${y + 2}" r="8" fill="#E07A1F"/><text class="mk" x="${x + 2}" y="${y + 6}" text-anchor="middle">${cis}</text></g>` : "")
      + (o.mode === "actual" && ss?.inQ && isWork(s) ? `<text class="inq" x="${x + NW}" y="${y + NH + 26}" text-anchor="end">${ss.inQ} open now</text>` : "")
      + (sub ? `<text class="nsub" x="${x + NW / 2}" y="${y + NH + 14}" text-anchor="middle">${esc(sub)}</text>` : "")
      + `<text class="qcount" id="q-${s.id}" x="${x + NW / 2}" y="${y - 6}" text-anchor="middle"></text>`;
    g += `<g class="${cls}" data-step="${s.id}" tabindex="0" role="button" aria-label="${s.id} ${esc(s.name)}">${shape}${marks}</g>`;
  }
  g += `<g id="tok"></g>`;
  return { svg: `<svg class="pmap" viewBox="0 0 ${L.W} ${L.H}" style="min-width:${L.W}px">${g}</svg>`, L };
}

// ---------------------------------------------------------------- process page
const PSTATE = { mode: "design", group: "role", year: "", site: "", ov: { information: true, material: true, people: true, ctl: true, doc: false }, trace: "" };
route(/^\/process\/(ACE-[A-Z]{3}-PRS-\d{3})(?:\/(S\d\d))?$/, (pid, sel) => {
  const m = PRSBY[pid]; if (!m) { const r = BPMREG.find((x) => x.process_id === pid); return r ? plannedPage(r) : go404(); }
  const els = [...new Set((m.oms_tags || []).map(elOf))];
  const owner = parseWho(m.owner)[0]; const reg = BPMREG.find((r) => r.process_id === pid) || {};
  const risks = RISKS.filter((r) => r.process === pid);
  const commits = (m.commitments || []).map((c) => ({ ref: c, ...polSec(c) }));
  const vals = [...new Map(commits.flatMap((c) => valuesIn(c.s)).map((v) => [v.bm, v])).values()];
  const objs = (m.objectives || []).map((id) => (REG["OMS-REG-001_objectives"] || []).find((o) => o.objective_id === id)).filter(Boolean);
  const isInsp = m.value?.model === "risk-exposure";
  page(els, head(esc(m.title), esc(m.summary || ""), `<a href="#/process">Processes</a> / ${esc(m.apqc?.l1 || "")} / ${esc(m.apqc?.l2 || "")}`,
    `<div class="ownerbox"><div class="small muted">Process owner</div><div>${owner ? personLink(owner.person, owner.name) : esc(m.owner)}</div><div class="small">${owner?.role ? roleLink(owner.role, owner.title) : ""}</div>
     <div class="small muted" style="margin-top:6px">${esc(m.function)} · ${esc(m.id)} Rev ${esc(m.revision)} ${esc(m.status)} · maturity ${esc(reg.maturity || "–")}</div><div class="chips" style="margin-top:6px">${tagChips(m.oms_tags)}</div></div>`) + `
  <div class="thread panel">
    <div class="tcol"><h4>Values</h4>${vals.map(valueChip).join("") || `<span class="muted small">–</span>`}</div><div class="tarrow">→</div>
    <div class="tcol"><h4>Policy commitments</h4>${commits.map((c) => `<div class="small">${commitLink(c.ref)}</div>`).join("")}<div class="small muted">Governing policy ${docLink(m.policy)}${(m.policies_also || []).length ? `; also ${m.policies_also.map((x) => docLink(x)).join(", ")}` : ""}</div></div><div class="tarrow">→</div>
    <div class="tcol here"><h4>This process</h4><div class="small"><b>${esc(m.title)}</b></div><div class="small muted">Parent ${docLink(m.parent)} · ${esc((m.character || "").replace(/^./, (c) => c.toUpperCase()))}</div></div><div class="tarrow">→</div>
    <div class="tcol"><h4>Objectives</h4>${objs.map((o) => `<div class="small"><b>${esc(o.objective_id)}</b> ${esc(o.title)}</div>`).join("") || `<span class="muted small">–</span>`}</div><div class="tarrow">·</div>
    <div class="tcol"><h4>Risks it controls</h4>${risks.map((r) => `<div class="small"><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)} ${rateChip(r.current_rating)}</div>`).join("") || `<span class="muted small">None linked yet</span>`}</div>
  </div>
  <div class="panel pmap-panel">
    <div class="ptool">
      <div class="seg" id="mode">${[["design", "Design"], ["actual", "Actual"], ["compare", "Before / after"]].map(([k, l]) => `<button data-v="${k}" class="${PSTATE.mode === k ? "on" : ""}">${l}</button>`).join("")}</div>
      <div class="seg" id="grp">${[["role", "Lanes by role"], ["fn", "Lanes by function"]].map(([k, l]) => `<button data-v="${k}" class="${PSTATE.group === k ? "on" : ""}">${l}</button>`).join("")}</div>
      <label class="tsel">Year <select id="fy"><option value="">All years</option>${YEARS.map((y) => `<option ${PSTATE.year === y ? "selected" : ""}>${y}</option>`).join("")}</select></label>
      <label class="tsel">Site <select id="fs"><option value="">All sites</option>${isInsp ? `<option value="OFF">Offshore platforms</option><option value="ON">Onshore sites</option>` : ""}${[...new Set(ledger(m).cases.map((c) => c.site))].sort().map((s) => `<option value="${s}">${esc(SITE[s]?.name || s)}</option>`).join("")}</select></label>
      <span class="ovs">${[["information", "Information"], ["material", "Material"], ["people", "People"], ["ctl", "Controls"], ["doc", "Documents"]].map(([k, l]) => `<label class="ov ov-${k}"><input type="checkbox" data-ov="${k}" ${PSTATE.ov[k] ? "checked" : ""}> ${l}</label>`).join("")}</span>
      <button class="btn primary" id="play"></button>
    </div>
    <div class="pnote small muted" id="pnote"></div>
    <div class="pmap-wrap" id="mapwrap"></div>
    <div class="plegend small" id="legend"></div>
  </div>
  <div class="panel" id="detail" hidden></div>
  <div class="grid2 pgrid"><div class="panel" id="kpis"></div><div class="panel" id="value"></div></div>
  <div class="grid2 pgrid"><div class="panel" id="time"></div><div class="panel" id="funcs"></div></div>
  <div class="grid2 pgrid"><div class="panel" id="improve"></div><div class="panel" id="cases"></div></div>
  <div class="panel"><h2>SIPOC</h2><div class="sipoc">${["suppliers", "inputs", "process", "outputs", "customers"].map((k) => `<div><h4>${k[0].toUpperCase() + k.slice(1)}</h4>${(m.sipoc?.[k] || []).map((x) => `<div class="small">${esc(x)}</div>`).join("")}</div>`).join("")}</div>
    <p class="small muted" style="margin-top:10px">Drawn from <code>processes/${esc(m.id)}.json</code> (${esc(m.schema)}) and measured from <code>registers/${esc(m.ledger)}_cases.csv</code> and <code>_events.csv</code>. Value assumptions are on the <a href="#/value">value assumptions</a> page.</p></div>`);

  let selStep = sel || "";
  const render = () => {
    stopAll();
    const f = { year: PSTATE.year, site: PSTATE.site };
    const cases = pick(m, f); const st = stats(m, cases);
    const rev = (m.history || []).slice(-1)[0];
    const st1 = PSTATE.mode === "compare" ? stats(m, pick(m, { site: PSTATE.site, rev: (m.history || []).slice(-2)[0]?.revision })) : null;
    const st2 = PSTATE.mode === "compare" ? stats(m, pick(m, { site: PSTATE.site, rev: rev?.revision })) : null;
    const trace = PSTATE.trace ? ledger(m).byId[PSTATE.trace] : null;
    const { svg, L } = drawMap(m, { group: PSTATE.group, mode: PSTATE.mode, st: PSTATE.mode === "actual" ? st : PSTATE.mode === "compare" ? st1 : null, st2, ov: PSTATE.ov, sel: selStep, trace, animate: PSTATE.mode === "design" });
    $("#mapwrap").innerHTML = svg;
    $("#play").textContent = PSTATE.mode === "design" ? "Play the stages" : PSTATE.mode === "actual" ? "Replay real cases" : "Show what changed";
    $("#pnote").innerHTML = PSTATE.mode === "design" ? `The process as written: ${m.steps.filter(isWork).length} steps across ${m.lanes.length} roles in ${new Set(m.lanes.map((l) => l.function)).size} functions. Bold arrows are hand-offs between ${PSTATE.group === "fn" ? "functions" : "roles"}; red dashed arrows are rework loops${m.cycle ? "; the arc over the top is the cycle" : ""}. Coloured lines show what moves: information, material and people.`
      : PSTATE.mode === "actual" ? `${plural(cases.length, m.case_label || "case")} from the ledger${PSTATE.year ? " opened in " + PSTATE.year : ""}${PSTATE.site ? " at " + esc(PSTATE.site === "OFF" ? "the offshore platforms" : PSTATE.site === "ON" ? "onshore sites" : SITE[PSTATE.site]?.name || PSTATE.site) : ""}. Step colour shows the median wait before work starts (white none, red longest); arrow thickness shows how many cases took that path.`
      : `Rev ${esc((m.history || []).slice(-2)[0]?.revision || "")} cases against Rev ${esc(rev?.revision || "")} cases (from ${fmt(toDate(rev?.date))}). Green steps got faster, red slower; outlined steps changed in the revision. ${esc(rev?.summary || "")}`;
    $("#legend").innerHTML = PSTATE.mode === "actual" ? `<span class="lg"><i style="background:${heat(0.2, 1)}"></i>short wait</span><span class="lg"><i style="background:${heat(0.6, 1)}"></i></span><span class="lg"><i style="background:${heat(1, 1)}"></i>long wait</span> <span class="lg"><i class="dot" style="background:#E0AE2E"></i>waiting</span><span class="lg"><i class="dot" style="background:#0B5563"></i>being worked</span>`
      : `<span class="lg"><b style="color:#2F7FB8">- - -</b> information</span><span class="lg"><b style="color:#B07A1F">· · ·</b> material</span><span class="lg"><b style="color:#7A4FA0">— · —</b> people</span><span class="lg"><i class="dot" style="background:#B33A3A"></i>controls (amber if one is degraded)</span><span class="lg"><i class="dot" style="background:#E07A1F"></i>open improvement items</span><span class="lg">VA value-added · BVA needed by the business · NVA waste</span>`;
    for (const n of $$(".pnode", $("#mapwrap"))) { n.onclick = () => { selStep = n.dataset.step; history.replaceState(null, "", `#/process/${pid}/${selStep}`); render(); $("#detail").scrollIntoView({ behavior: "smooth", block: "nearest" }); }; n.onkeydown = (e) => { if (e.key === "Enter") n.onclick(); }; }
    $("#play").onclick = () => (PSTATE.mode === "design" ? playStages(m, L) : PSTATE.mode === "actual" ? replay(m, L, cases) : null);
    $("#play").hidden = PSTATE.mode === "compare";
    drawDetail(m, selStep, st, cases);
    drawKpis(m, st);
    drawValue(m);
    drawTime(m, st, st1, st2);
    drawFuncs(m, st);
    drawImprove(m);
    drawCases(m, cases, trace);
  };
  $("#mode").onclick = (e) => { const b = e.target.closest("button"); if (!b) return; PSTATE.mode = b.dataset.v; for (const x of $$("#mode button")) x.classList.toggle("on", x === b); render(); };
  $("#grp").onclick = (e) => { const b = e.target.closest("button"); if (!b) return; PSTATE.group = b.dataset.v; for (const x of $$("#grp button")) x.classList.toggle("on", x === b); render(); };
  $("#fy").oninput = (e) => { PSTATE.year = e.target.value; render(); };
  $("#fs").value = PSTATE.site; if ($("#fs").value !== PSTATE.site) PSTATE.site = "";
  $("#fs").oninput = (e) => { PSTATE.site = e.target.value; render(); };
  for (const c of $$("[data-ov]")) c.onchange = () => { PSTATE.ov[c.dataset.ov] = c.checked; render(); };
  PSTATE.trace = PSTATE.trace && ledger(m).byId[PSTATE.trace] ? PSTATE.trace : "";
  render();
  if (sel) setTimeout(() => $("#detail")?.scrollIntoView({ block: "nearest" }), 50);
  window.__render = render;
});

function drawDetail(m, sid, st, cases) {
  const el = $("#detail"); const s = m.steps.find((x) => x.id === sid); if (!s) { el.hidden = true; return; } el.hidden = false;
  const l = laneOf(m, s.lane), role = ROLE[l.role_id], ss = st.S[sid];
  const hold = role ? (HOLD[role.role_id] || []) : [];
  const risks = [...new Set((s.controls || []).map((c) => CTL[c]?.risk_id).filter(Boolean))];
  const cis = ciFor(m.id, sid);
  const flows = (m.flows || []).filter((f) => f.from === sid || f.to === sid);
  const inbound = m.steps.filter((x) => outs(x).includes(sid)), outbound = outs(s).map((id) => m.steps.find((x) => x.id === id)).filter(Boolean);
  const cm = s.commitment ? polSec(s.commitment) : null;
  el.innerHTML = `<div class="page-head" style="margin-bottom:10px"><div><div class="crumb">Step ${s.id} · ${esc({ task: "Task", xor: "Decision", start: "Start", end: "End" }[s.type] || s.type)}${s.value ? ` · ${{ VA: "Value-added", BVA: "Needed by the business", NVA: "Non-value-added (waste)" }[s.value]}` : ""}</div><h2 style="margin:0">${esc(s.name)}</h2></div>
    <button class="btn small" id="dclose">Close</button></div>
  <div class="grid3">
    <div><h4>Who</h4><div>${role ? roleLink(role, l.role) : esc(l.role)}</div><div class="small" style="color:${fcol(l.function)}">${esc(fname(l.function))}${l.external ? " (contractor)" : ""}</div>${hold.length ? `<div class="small muted">Held by ${hold.slice(0, 4).map((p) => personLink(p)).join(", ")}${hold.length > 4 ? "…" : ""}</div>` : ""}${l.note ? `<div class="small muted">${esc(l.note)}</div>` : ""}
      <h4>Comes from</h4><div class="small">${inbound.map((x) => `<a href="#/process/${m.id}/${x.id}">${x.id} ${esc(x.name)}</a>`).join("<br>") || "–"}</div>
      <h4>Goes to</h4><div class="small">${(s.branches || []).length ? s.branches.map((b) => `<a href="#/process/${m.id}/${b.to}">${esc(b.label)} → ${b.to}</a>`).join("<br>") : outbound.map((x) => `<a href="#/process/${m.id}/${x.id}">${x.id} ${esc(x.name)}</a>`).join("<br>") || "–"}</div></div>
    <div><h4>Written in</h4>${(s.doc_refs || []).map((r) => { const [d, bm] = r.split("#"); const sec = DOC[d]?.sections.find((x) => x.bm === bm); return `<div class="small">${docLink(d, bm, `${d}`)} ${esc(sec?.title || "")} ${sec ? tagChips(sec.tags) : ""}</div>`; }).join("") || `<div class="small muted">No document section linked.</div>`}
      ${cm?.s ? `<h4>Policy commitment</h4><div class="small">${commitLink(s.commitment)}</div><div>${valuesIn(cm.s).map(valueChip).join("")}</div>` : ""}
      ${s.threshold ? `<h4>Decision threshold</h4><div class="small">${esc(s.threshold)}</div>` : ""}
      <h4>Inputs → outputs</h4><div class="small">${(s.inputs || []).map(esc).join(", ") || "–"} → ${(s.outputs || []).map(esc).join(", ") || "–"}</div>
      <h4>Records and systems</h4><div class="small">${[...(s.records || []), ...(s.systems || []).map((x) => `<i>${esc(x)}</i>`)].join(", ") || "–"}</div>
      ${flows.length ? `<h4>What moves</h4>${flows.map((f) => `<div class="small"><b style="color:${FLOWSTYLE[f.type].c}">${esc(f.type)}</b> ${esc(f.carries || "")} ${f.from === sid ? "→ " + esc(m.steps.find((x) => x.id === f.to)?.name || f.to) : "← " + esc(m.steps.find((x) => x.id === f.from)?.name || f.from)}</div>`).join("")}` : ""}</div>
    <div><h4>Controls performed</h4>${(s.controls || []).map((c) => `<div class="small"><span class="dot ${hcls(CTL[c]?.health)}"></span>${ctlChip(c)} ${esc(CTL[c]?.statement || "")}</div>`).join("") || `<div class="small muted">None.</div>`}
      ${risks.length ? `<h4>Risks these controls address</h4>${risks.map((r) => `<div class="small"><a href="#/risk/${r}">${r}</a> ${esc(RISK[r]?.title || "")} ${rateChip(RISK[r]?.current_rating)}</div>`).join("")}` : ""}
      <h4>In the ledger</h4>${ss?.n ? `<div class="small">${ss.n.toLocaleString()} passes · median wait ${dfmt(median(ss.wait))} · median work ${hfmt(median(ss.work))}${ss.rw ? ` · ${ss.rw} as rework` : ""}${ss.inQ ? ` · <b>${ss.inQ} open now</b>` : ""}</div>` : `<div class="small muted">No passes in this selection.</div>`}
      ${s.sim ? `<div class="small muted">Planning estimate: ${s.sim.dur_h ? `${s.sim.dur_h[0]}–${s.sim.dur_h[2]} h of work` : ""}${s.sim.wait_h ? `, ${s.sim.wait_h} h waiting` : ""}</div>` : ""}
      <h4>Improvement items</h4>${cis.map((c) => `<div class="small"><a href="#/ci/${c.ci_id}">${c.ci_id}</a> ${esc(c.title)} ${stageChip(c.stage)}</div>`).join("") || `<div class="small muted">None on this step.</div>`}</div>
  </div>`;
  $("#dclose").onclick = () => { history.replaceState(null, "", `#/process/${m.id}`); for (const n of $$(".pnode.sel")) n.classList.remove("sel"); el.hidden = true; };
}

function drawKpis(m, st) {
  const by = Object.fromEntries(YEARS.map((y) => [y, stats(m, pick(m, { year: y, site: PSTATE.site }))]));
  const open = ciFor(m.id).filter((c) => !["Closed", "Parked"].includes(c.stage));
  $("#kpis").innerHTML = `<h2>Performance</h2><p class="small muted">Worked out from the ledger, not typed in. Selection: ${PSTATE.year || "all years"}${PSTATE.site ? ", " + esc(PSTATE.site === "OFF" ? "offshore" : PSTATE.site === "ON" ? "onshore" : PSTATE.site) : ""}.</p>
  <div class="pkpis">${(m.kpis || []).map((k) => { const v = kpiVal(k, st); const ok = kpiOk(k, v); const ys = YEARS.map((y) => kpiVal(k, by[y]));
    const breach = YEARS.slice(-2).every((y) => kpiOk(k, kpiVal(k, by[y])) === false);
    const max = Math.max(...ys.filter((x) => x != null), k.threshold || 0, 1);
    return `<div class="pkpi ${ok === false ? "bad" : ok ? "good" : ""}"><div class="small muted">${esc(k.family)}</div><h3>${esc(k.name)}</h3><div class="v">${kpiFmt(k, v)} <span class="small muted">target ${esc(k.target)}</span></div>
      <div class="ybars">${YEARS.map((y, i) => `<div data-tip="${y}: ${kpiFmt(k, ys[i])}"><i style="height:${ys[i] == null ? 0 : Math.max(3, (40 * ys[i]) / max)}px;background:${kpiOk(k, ys[i]) === false ? "var(--fail)" : "var(--eff)"}"></i><span>${y.slice(2)}</span></div>`).join("")}${k.threshold != null ? `<b style="bottom:${14 + (40 * k.threshold) / max}px"></b>` : ""}</div>
      ${breach ? `<div class="small breach">Out of target in ${YEARS.slice(-2).join(" and ")}${open.some((c) => c.source === "KPI breaches") ? " — improvement item open" : " — suggests a CI item (ACE-OMS-POL-001 §2.5)"}</div>` : ""}</div>`; }).join("")}
    <div class="pkpi"><div class="small muted">efficiency</div><h3>Flow efficiency</h3><div class="v">${pct(st.flowEff)}</div><div class="small muted">Share of elapsed time when someone is working on the case. The rest is waiting.</div></div></div>`;
}

function drawValue(m) {
  const rows = YEARS.map((y) => [y, stats(m, pick(m, { year: y, site: PSTATE.site }))]);
  const isInsp = m.value?.model === "risk-exposure";
  $("#value").innerHTML = `<h2>Business value</h2><p class="small muted">${esc(m.value?.explain || "")} <a href="#/value">Assumptions and sources</a>.</p>
  <table class="t"><tr><th>Year</th><th class="n">${esc((m.case_label || "case").replace(/^./, (c) => c.toUpperCase()))}s</th><th class="n">People cost</th>${isInsp ? `<th class="n">Trips</th><th class="n">Logistics</th>` : ""}<th class="n">Cost of waiting</th><th class="n">${isInsp ? "Loss avoided" : "Value delivered"}</th></tr>
  ${rows.map(([y, s]) => `<tr><td>${y}${y === "2026" ? " <span class='small muted'>to Nov</span>" : ""}</td><td class="n">${s.n}</td><td class="n">${usd(s.labour)}</td>${isInsp ? `<td class="n">${s.trips}</td><td class="n">${usd(s.logistics)}</td>` : ""}<td class="n">${usd(s.waitCost)}</td><td class="n"><b>${usd(s.valueDel)}</b></td></tr>`).join("")}</table>
  <p class="small" style="margin-top:10px">${isInsp ? `Offshore trips fell from <b>${rows[0][1].trips}</b> in 2024 to <b>${rows[2][1].trips}</b> in 2026 after campaign bundling (Rev 02, <a href="#/ci/CI-2024-001">CI-2024-001</a>). Each trip is costed at ${usd(TRIP_COST())} (helicopter round trip plus half a boat day).`
    : `Each implemented change is valued at its yearly benefit by class; waiting days defer that benefit. People cost uses loaded hourly rates by grade.`}</p>`;
}

function drawTime(m, st, st1, st2) {
  const steps = m.steps.filter(isWork); const rows = steps.map((s) => ({ s, w: median(st.S[s.id].wait) || 0, k: (median(st.S[s.id].work) || 0) / 24, n: st.S[s.id].n }));
  const max = Math.max(0.01, ...rows.map((r) => r.w + r.k));
  $("#time").innerHTML = `<h2>Where the time goes</h2><p class="small muted">Median days per step: <span class="lg"><i style="background:#E0AE2E"></i>waiting</span> <span class="lg"><i style="background:#0B5563"></i>working</span>. Waiting is where improvement pays.</p>
  ${rows.map((r) => `<div class="tbar" data-tip="${r.s.id} ${esc(r.s.name)}<br>${r.n} passes · wait ${dfmt(r.w)} · work ${hfmt(r.k * 24)}"><span class="small">${r.s.id} ${esc(r.s.name)}</span><div><i style="width:${(100 * r.w) / max}%;background:#E0AE2E"></i><i style="width:${Math.max(0.5, (100 * r.k) / max)}%;background:#0B5563"></i></div><span class="small n">${dfmt(r.w + r.k)}</span></div>`).join("")}
  ${st1 && st2 ? `<h3 style="margin-top:14px">Before and after the last revision</h3><table class="t"><tr><th>Step</th><th class="n">Rev ${esc((m.history || []).slice(-2)[0]?.revision)}</th><th class="n">Rev ${esc((m.history || []).slice(-1)[0]?.revision)}</th><th class="n">Change</th></tr>${steps.map((s) => { const a = median(st1.S[s.id].span), b = median(st2.S[s.id].span); const r = a && b ? (b - a) / a : null; return `<tr><td class="small">${s.id} ${esc(s.name)}</td><td class="n">${dfmt(a)}</td><td class="n">${dfmt(b)}</td><td class="n" style="color:${r == null ? "" : r < -0.1 ? "var(--eff)" : r > 0.1 ? "var(--fail)" : ""}">${r == null ? "–" : (r > 0 ? "+" : "") + Math.round(100 * r) + "%"}</td></tr>`; }).join("")}</table>` : ""}`;
}

function drawFuncs(m, st) {
  const fns = [...new Set(m.lanes.map((l) => l.function || "CTR"))];
  const max = Math.max(1, ...Object.values(st.HO).map((h) => h.n));
  $("#funcs").innerHTML = `<h2>How the functions interact</h2><p class="small muted">Each cell counts hand-offs from the row function to the column function, with the median wait after the hand-off. Hand-offs are where work stalls between functions.</p>
  <table class="t hom"><tr><th>From \\ to</th>${fns.map((f) => `<th style="color:${fcol(f)}">${esc(fname(f).replace(/ & /g, " & "))}</th>`).join("")}</tr>
  ${fns.map((a) => `<tr><th style="color:${fcol(a)}">${esc(fname(a))}</th>${fns.map((b) => { const h = st.HO[`${a}>${b}`]; return a === b ? `<td class="n muted">·</td>` : `<td class="n" style="background:${h ? `rgba(224,174,46,${0.12 + (0.6 * h.n) / max})` : ""}" ${h ? `data-tip="${h.n} hand-offs, average wait after hand-off ${dfmt(h.wait / h.n)}"` : ""}>${h ? `${h.n}<div class="small muted">${dfmt(h.wait / h.n)}</div>` : ""}</td>`; }).join("")}</tr>`).join("")}</table>
  <h3 style="margin-top:14px">Effort and waiting by function</h3><table class="t"><tr><th>Function</th><th class="n">Steps worked</th><th class="n">Hours worked</th><th class="n">Hours cases waited</th><th class="n">People cost</th></tr>
  ${fns.map((f) => { const x = st.FN[f] || { steps: 0, work: 0, wait: 0, cost: 0 }; return `<tr><td>${f === "CTR" ? "Contractors" : `<a href="#/org/${f}" style="color:${fcol(f)}">${esc(fname(f))}</a>`}</td><td class="n">${x.steps.toLocaleString()}</td><td class="n">${Math.round(x.work).toLocaleString()}</td><td class="n">${Math.round(x.wait).toLocaleString()}</td><td class="n">${usd(x.cost)}</td></tr>`; }).join("")}</table>`;
}

function drawImprove(m) {
  const items = ciFor(m.id);
  $("#improve").innerHTML = `<h2>Improvement</h2><p class="small muted">Items in the CI register against this process (<a href="#/ci">all improvement</a>), and the revisions they produced.</p>
  ${items.map((c) => `<div class="ciline"><div><a href="#/ci/${c.ci_id}">${c.ci_id}</a> ${esc(c.title)}</div><div class="small">${stageChip(c.stage)} ${esc(c.method)} · ${esc(c.source)} · step ${c.step_id ? `<a href="#/process/${m.id}/${c.step_id}">${c.step_id}</a>` : "–"}${c.baseline ? ` · ${esc(c.kpi)}: ${esc(c.baseline)}${c.actual ? ` → <b>${esc(c.actual)}</b>` : ""} (target ${esc(c.target)})` : ""}</div></div>`).join("") || `<p class="muted small">No items yet.</p>`}
  <h3 style="margin-top:14px">Revisions</h3><ul class="events">${(m.history || []).map((h) => `<li><span class="muted">${fmt(toDate(h.date))}</span><span><b>Rev ${esc(h.revision)}</b> ${esc(h.summary)}${h.ci ? ` <a href="#/ci/${h.ci}">${h.ci}</a>` : ""}</span></li>`).join("")}</ul>`;
}

function drawCases(m, cases, trace) {
  const list = [...cases].sort((a, b) => b.o - a.o);
  const sel = trace || null;
  let gantt = "";
  if (sel) { const t0 = sel.o, t1 = Math.max(...sel.ev.map((e) => +(e.f || e.s || e.a)), +t0 + DAY); const span = t1 - t0 || 1;
    gantt = `<div class="gantt">${sel.ev.map((e) => { const s = m.steps.find((x) => x.id === e.step_id); const a = (100 * (e.a - t0)) / span, b = (100 * ((e.s || e.f || e.a) - t0)) / span, c = (100 * ((e.f || new Date(Math.min(+TODAY, t1))) - t0)) / span;
      return `<div class="grow"><span class="small">${e.step_id} ${esc(s?.name || "")}${e.rw ? " <b class='rework'>rework</b>" : ""}</span><div><i class="w" style="left:${a}%;width:${Math.max(0, b - a)}%"></i><i class="k" style="left:${b}%;width:${Math.max(0.4, c - b)}%"></i></div><span class="small muted">${e.branch ? esc(e.branch) : ""}</span></div>`; }).join("")}
      <div class="small muted">${fmt(sel.o)} → ${sel.cl ? fmt(sel.cl) : "open"} · ${Math.round(((sel.cl || TODAY) - sel.o) / DAY)} days${sel.due ? ` · due ${fmt(sel.dueD)}` : ""}${sel.deferred_to ? ` · deferred to ${fmt(sel.defD)}` : ""}${sel.ref && sel.ref !== sel.case_id ? ` · ${esc(sel.ref)}` : ""}</div></div>`; }
  $("#cases").innerHTML = `<h2>Trace a case</h2><p class="small muted">Pick a real ${esc(m.case_label || "case")} to light up its path on the map and see where its time went.</p>
  <div class="filters"><label>${esc((m.case_label || "case").replace(/^./, (c) => c.toUpperCase()))}<select id="tc"><option value="">None</option>${list.slice(0, 400).map((c) => `<option value="${c.case_id}" ${sel && sel.case_id === c.case_id ? "selected" : ""}>${c.case_id} · ${esc((c.title || "").slice(0, 60))} · ${esc(c.outcome)}</option>`).join("")}</select></label>${sel ? `<button class="btn small" id="tcx">Clear</button>` : ""}</div>
  ${sel ? `<h3>${esc(sel.title)}</h3><div class="small muted">${esc(SITE[sel.site]?.name || sel.site)}${sel.cls ? " · class " + esc(sel.cls) : ""} · Rev ${esc(sel.revision)} · ${esc(sel.outcome)}</div>${gantt}` : ""}`;
  $("#tc").oninput = (e) => { PSTATE.trace = e.target.value; window.__render(); };
  if ($("#tcx")) $("#tcx").onclick = () => { PSTATE.trace = ""; window.__render(); };
}

// ---------------------------------------------------------------- animation: stages (no clock) and real-case replay
function centre(L, id) { const p = L.P[id]; return { x: p.x + NW / 2, y: p.y + NH / 2 }; }
function playStages(m, L) {
  stopAll(); const T = $("#tok"); if (!T) return; T.innerHTML = "";
  const S = Object.fromEntries(m.steps.map((s) => [s.id, s])); const start = m.steps.find((s) => s.type === "start").id;
  const choose = (s) => { if (s.branches) { let r = Math.random(), acc = 0; for (const b of s.branches) { acc += b.p ?? 1 / s.branches.length; if (r <= acc) return b.to; } return s.branches[0].to; } return (s.next || [])[0]; };
  const toks = []; let hand = 0, tick = 0, finished = 0; const N = 8;
  const note = $("#pnote"); const base = note.innerHTML;
  timers.push(setInterval(() => {
    tick++;
    if (tick % 14 === 1 && toks.length < N) { const el = document.createElementNS("http://www.w3.org/2000/svg", "circle"); el.setAttribute("r", 7); el.setAttribute("class", "stok"); T.appendChild(el); toks.push({ at: start, to: null, t: 0, el, k: toks.length }); }
    for (const k of toks) { if (k.done) continue;
      if (!k.to) { const s = S[k.at]; if (s.type === "end") { k.done = true; finished++; k.el.remove(); continue; } k.to = choose(s); k.t = 0; for (const n of $$(".pnode")) if (n.dataset.step === k.at) { n.classList.add("lit"); setTimeout(() => n.classList.remove("lit"), 500); } }
      k.t += 0.12; const a = centre(L, k.at), b = centre(L, k.to); const t = Math.min(1, k.t);
      const back = L.P[k.to].x <= L.P[k.at].x; const yb = Math.max(L.P[k.at].y, L.P[k.to].y) + NH + 26;
      const x = back ? a.x + (b.x - a.x) * t : a.x + (b.x - a.x) * t, y = back ? (1 - t) * (1 - t) * a.y + 2 * t * (1 - t) * yb + t * t * b.y : a.y + (b.y - a.y) * t;
      k.el.setAttribute("cx", x + ((k.k % 3) - 1) * 5); k.el.setAttribute("cy", y);
      if (t >= 1) { if (S[k.at].lane !== S[k.to].lane) hand++; k.at = k.to; k.to = null; }
    }
    note.innerHTML = `${base}<br><b>Playing:</b> ${toks.filter((k) => !k.done).length} ${esc(m.case_label || "case")}s in flow · ${finished} finished · <b>${hand}</b> hand-offs between roles so far.`;
    if (finished >= N) { stopAll(); note.innerHTML = `${base}<br><b>${N} ${esc(m.case_label || "case")}s</b> took <b>${hand}</b> hand-offs between roles — about ${(hand / N).toFixed(1)} each. Every hand-off is a queue in the Actual view.`; }
  }, 70));
}
function replay(m, L, cases) {
  stopAll(); const T = $("#tok"); if (!T) return; T.innerHTML = "";
  const cs = cases.filter((c) => c.ev.length); if (!cs.length) return;
  let t = Math.min(...cs.map((c) => +c.o)); const end = Math.min(+TODAY, Math.max(...cs.map((c) => +(c.cl || TODAY))));
  const pool = {}; const note = $("#pnote");
  const step = Math.max(DAY / 2, (end - t) / 700);
  timers.push(setInterval(() => {
    t += step; const at = {};
    for (const c of cs) { if (+c.o > t || (c.cl && +c.cl < t)) { if (pool[c.case_id]) { pool[c.case_id].remove(); delete pool[c.case_id]; } continue; }
      const e = c.ev.find((x) => +x.a <= t && (!x.f || +x.f > t)); if (!e || !L.P[e.step_id]) continue;
      const k = (at[e.step_id] = (at[e.step_id] || 0) + 1) - 1; const p = L.P[e.step_id];
      let el = pool[c.case_id]; if (!el) { el = document.createElementNS("http://www.w3.org/2000/svg", "circle"); el.setAttribute("r", 4.2); T.appendChild(el); pool[c.case_id] = el; }
      el.setAttribute("cx", p.x + 8 + (k % 12) * 9); el.setAttribute("cy", p.y + NH + 10 + Math.floor(k / 12) * 9);
      el.setAttribute("class", `rtok ${e.s && +e.s <= t ? "work" : "wait"}`);
    }
    for (const s of m.steps) { const q = $(`#q-${s.id}`); if (q) q.textContent = at[s.id] ? `${at[s.id]} here` : ""; }
    const d = new Date(t); note.innerHTML = `<b>Replaying ${cs.length.toLocaleString()} real ${esc(m.case_label || "case")}s</b> — ${d.getDate()} ${MON[d.getMonth()]} ${d.getFullYear()} · ${Object.values(at).reduce((a, b) => a + b, 0)} in flow. Amber dots are waiting; dark dots are being worked.`;
    if (t >= end) stopAll();
  }, 60));
}

// ---------------------------------------------------------------- landscape
route(/^\/process$/, () => {
  const bpm = DOC["ACE-BPM-PRA-001"];
  const tbl = (head0) => bpm?.sections.flatMap((s) => s.blocks).find((b) => b.k === "table" && b.rows[0][0] === head0)?.rows.slice(1) || [];
  const L1 = tbl("Group").map((r) => ({ group: r[0], code: r[1], name: r[2], fn: r[3] }));
  const L2 = Object.fromEntries(tbl("L1 category").map((r) => [r[0].split(" ")[0], r[1].split(/;\s*/).map((x) => ({ code: x.split(" ")[0], name: x.replace(/^\S+\s/, "") }))]));
  const pols = DOCS.filter((d) => d.typeCode === "POL");
  const open = CIS.filter((c) => !["Closed", "Parked"].includes(c.stage));
  page([7, 10], head("Processes", "The process layer sits between the Standards and Practices that say what must be true and the procedures that say how one task is done. Each mapped process is drawn from its model file and measured from its ledger of real cases.") + `
  <div class="figures" style="margin-bottom:18px"><div><b>${BPMREG.length}</b><span>processes in the register</span></div><div><b>${PRS.length}</b><span>mapped and measured</span></div><div><b>${pols.length}</b><span>governing policies</span></div><div><b>${open.length}</b><span>open improvement items</span></div><div><b>${PRS.reduce((a, m) => a + ledger(m).cases.length, 0).toLocaleString()}</b><span>real cases in the ledgers</span></div></div>
  <div class="pcards">${PRS.map((m) => { const st = stats(m, pick(m, { year: "2026" })); const ks = (m.kpis || []).slice(0, 2); return `<a class="pcard panel" href="#/process/${m.id}">
    <div class="small muted">${esc(m.apqc?.l2 || "")} · ${esc(m.character || "")}</div><h2>${esc(m.title)}</h2><p class="small">${esc((m.summary || "").split(". ")[0])}.</p>
    <div class="pc-figs"><div><b>${st.n}</b><span>${esc(m.case_label)}s in 2026</span></div>${ks.map((k) => { const v = kpiVal(k, st); return `<div class="${kpiOk(k, v) === false ? "bad" : ""}"><b>${kpiFmt(k, v)}</b><span>${esc(k.name)}</span></div>`; }).join("")}<div><b>${pct(st.flowEff)}</b><span>flow efficiency</span></div></div>
    <div class="small muted">Owner ${esc(nameOf(m.owner))} · ${m.lanes.length} roles · ${new Set(m.lanes.map((l) => l.function)).size} functions · governed by ${esc(m.policy)}</div></a>`; }).join("")}</div>
  <div class="panel" style="margin-top:18px"><h2>The ACE process architecture</h2><p class="small muted">Levels 1 and 2 from ACE-BPM-PRA-001 §4. Filled tiles are mapped and measured; outlined tiles are in the register; dashes mark groups with no process yet.</p>
    <div class="arch">${L1.map((c) => `<div class="l1 g-${esc(c.group.toLowerCase())}"><div class="l1h"><span class="small muted">${esc(c.group)}</span><b>${esc(c.code)} ${esc(c.name)}</b></div>${(L2[c.code] || []).map((g) => { const ps = BPMREG.filter((r) => r.l2 === g.code);
      return `<div class="l2"><span class="small">${esc(g.code)} ${esc(g.name)}</span><div>${ps.map((p) => `<a class="ptile ${PRSBY[p.process_id] ? "mapped" : "planned"}" href="#/process/${p.process_id}" data-tip="<b>${esc(p.process_id)}</b> ${esc(p.title)}<br>${esc(p.status)} · owner ${esc(nameOf(p.owner))}<br>Policy ${esc(p.policy)}">${esc(p.title.replace(/ Process$/, ""))}</a>`).join("") || `<span class="muted small">–</span>`}</div></div>`; }).join("")}</div>`).join("")}</div></div>
  <div class="panel" style="margin-top:18px"><h2>Policies and the processes they govern</h2><p class="small muted">Each L3 process has one governing policy (ACE-BPM-PRA-001 §5). The policy column of the Process Register is the link.</p>
    <table class="t"><tr><th>Policy</th><th>Owner</th><th class="n">Processes</th><th>Commitments</th></tr>${pols.map((d) => { const n = BPMREG.filter((r) => r.policy === d.id); return `<tr><td>${docLink(d.id)} ${esc(d.title)}</td><td class="small">${esc(nameOf(d.owner))}</td><td class="n">${n.length}</td><td class="small">${d.sections.filter((s) => /^COM_/.test(s.bm)).length}</td></tr>`; }).join("")}</table></div>
  <div class="panel" style="margin-top:18px"><h2>Process register</h2><table class="t"><tr><th>Process</th><th>Owner</th><th>Policy</th><th>Parent</th><th>Status</th><th class="n">Maturity</th></tr>
    ${BPMREG.map((p) => { const o = parseWho(p.owner)[0]; return `<tr><td><a href="#/process/${p.process_id}">${esc(p.process_id)}</a> ${esc(p.title)}</td><td class="small">${o?.person ? personLink(o.person, o.name) : esc(nameOf(p.owner))}</td><td class="small">${docLink(p.policy)}</td><td class="small">${docLink(p.parent)}</td><td>${esc(p.status)}</td><td class="n">${esc(p.maturity)}</td></tr>`; }).join("")}</table></div>`);
});

function plannedPage(r) {
  const o = parseWho(r.owner)[0];
  page([...new Set((r.oms_tags || "").split(", ").filter(Boolean).map(elOf))], head(esc(r.title), `${esc(r.process_id)} is in the Process Register as ${esc(r.status.toLowerCase())}. It has no model file or ledger yet, so it cannot be drawn or measured.`, `<a href="#/process">Processes</a>`) + `
  <div class="grid2"><div class="panel"><table class="t"><tr><td>Owner</td><td>${o?.person ? personLink(o.person, o.name) : esc(r.owner)}${o?.stale === "left" ? ` <span class="st rejected">left ACE</span>` : ""}</td></tr><tr><td>Function</td><td>${esc(r.function)}</td></tr><tr><td>Architecture</td><td>L1 ${esc(r.l1)}, L2 ${esc(r.l2)}</td></tr>
    <tr><td>Governing policy</td><td>${docLink(r.policy)}</td></tr><tr><td>Parent</td><td>${docLink(r.parent)}</td></tr><tr><td>Maturity</td><td>${esc(r.maturity)}</td></tr><tr><td>OMS tags</td><td>${tagChips((r.oms_tags || "").split(", ").filter(Boolean))}</td></tr></table></div>
  <div class="panel"><h2>Controls it will perform</h2>${r.controls ? r.controls.split("; ").map(ctlChip).join("") : `<p class="muted small">None listed.</p>`}
    <h2 style="margin-top:14px">Improvement items</h2>${ciFor(r.process_id).map((c) => `<div class="small"><a href="#/ci/${c.ci_id}">${c.ci_id}</a> ${esc(c.title)} ${stageChip(c.stage)}</div>`).join("") || `<p class="muted small">None.</p>`}</div></div>`);
}

// ---------------------------------------------------------------- improvement (CI) dimension
route(/^\/ci$/, () => {
  const open = CIS.filter((c) => !["Closed", "Parked"].includes(c.stage));
  const benefit = CIS.filter((c) => ["Verified", "Standardised", "Closed"].includes(c.stage)).reduce((a, c) => a + (+c.benefit_usd || 0), 0);
  const cnt = (k) => { const o = {}; for (const c of CIS) o[c[k]] = (o[c[k]] || 0) + 1; return o; };
  const src = cnt("source"), met = cnt("method");
  const pol = DOC["ACE-OMS-POL-001"];
  const SRC = ["Incident and near-miss actions", "Audit and assurance findings", "Process reviews", "KPI breaches", "Staff ideas"], MET = ["Just do it", "PDCA", "DMAIC", "Project"];
  const PCOL = ["#C8402F", "#2F7FB8", "#0B5563", "#E0AE2E", "#6E9A2E"];
  const q = {}; for (const c of CIS) { const k = c.raised.slice(0, 4); q[k] ||= { raised: 0, closed: 0 }; q[k].raised++; } for (const c of CIS) if (c.closed) { const k = c.closed.slice(0, 4); q[k] ||= { raised: 0, closed: 0 }; q[k].closed++; }
  page([10, 9], head("Continuous improvement", `Every improvement points at a process and, where possible, a step. Items come from five sources and follow four routes, as set in ${docLink("ACE-OMS-POL-001")}. An item is only Verified when a measured KPI has moved against its baseline.`) + `
  <div class="figures" style="margin-bottom:18px"><div><b>${CIS.length}</b><span>items in the register</span></div><div><b>${open.length}</b><span>open</span></div><div><b>${CIS.filter((c) => ["Verified", "Standardised", "Closed"].includes(c.stage) && c.baseline).length}</b><span>with verified benefit</span></div><div><b>${usd(benefit)}</b><span>yearly benefit verified</span></div><div><b>${src["Staff ideas"] || 0}</b><span>from staff ideas</span></div></div>
  <div class="board">${STAGES.map((sname) => `<div class="bcol"><h3>${stageChip(sname)} <span class="small muted">${CIS.filter((c) => c.stage === sname).length}</span></h3>${CIS.filter((c) => c.stage === sname).map((c) => `<a class="bcard" href="#/ci/${c.ci_id}" style="--c:${STCOL[sname]}"><div class="small muted">${c.ci_id} · ${esc(c.method)}</div><div>${esc(c.title)}</div><div class="small muted">${esc(PRSBY[c.process_id]?.title || BPMREG.find((r) => r.process_id === c.process_id)?.title || c.process_id)}${c.step_id ? " · " + c.step_id : ""}</div>${c.baseline ? `<div class="small">${esc(c.baseline)}${c.actual ? ` → <b>${esc(c.actual)}</b>` : ""} <span class="muted">target ${esc(c.target)}</span></div>` : ""}</a>`).join("")}</div>`).join("")}</div>
  <div class="grid2 pgrid"><div class="panel"><h2>Where improvements come from</h2>${hbar(SRC.map((s, i) => [s, src[s] || 0, PCOL[i]]))}<table class="t" style="margin-top:8px">${SRC.map((s, i) => `<tr><td><span class="lg"><i style="background:${PCOL[i]}"></i></span>${esc(s)}</td><td class="n">${src[s] || 0}</td></tr>`).join("")}</table>
      <h2 style="margin-top:16px">Routes</h2><table class="t">${MET.map((s) => `<tr><td>${esc(s)}</td><td class="n">${met[s] || 0}</td></tr>`).join("")}</table>
      <p class="small muted" style="margin-top:8px">The sources and routes are the exact lists in ${pol ? `<a href="#/doc/ACE-OMS-POL-001/COM_CI_SOURCES">§2.5</a> and <a href="#/doc/ACE-OMS-POL-001/COM_CI_METHOD">§2.6</a>` : "ACE-OMS-POL-001"} of the policy.</p></div>
    <div class="panel"><h2>Benefit tracker</h2><p class="small muted">Baseline, target and measured result for items with a KPI.</p>${CIS.filter((c) => c.baseline && !isNaN(parseFloat(c.baseline))).map((c) => { const b = parseFloat(c.baseline), a = parseFloat(c.actual), t = parseFloat(String(c.target).replace(/[^\d.]/g, "")); const mx = Math.max(b, a || 0, t || 0) * 1.1 || 1;
      return `<div class="btrack"><div class="small"><a href="#/ci/${c.ci_id}">${c.ci_id}</a> ${esc(c.kpi)}</div><div class="bt"><i class="b" style="width:${(100 * b) / mx}%" data-tip="Baseline ${esc(c.baseline)}"></i>${!isNaN(a) ? `<i class="a" style="width:${(100 * a) / mx}%" data-tip="Measured ${esc(c.actual)}"></i>` : ""}${!isNaN(t) ? `<b style="left:${(100 * t) / mx}%" data-tip="Target ${esc(c.target)}"></b>` : ""}</div><div class="small muted">${esc(c.baseline)} → ${c.actual ? `<b>${esc(c.actual)}</b>` : "not yet measured"} · target ${esc(c.target)} ${stageChip(c.stage)}</div></div>`; }).join("")}
      <h2 style="margin-top:16px">Raised and closed by year</h2><table class="t"><tr><th>Year</th><th class="n">Raised</th><th class="n">Closed</th></tr>${Object.keys(q).sort().map((k) => `<tr><td>${k}</td><td class="n">${q[k].raised}</td><td class="n">${q[k].closed}</td></tr>`).join("")}</table></div></div>
  <div class="panel"><h2>Steps that attract improvement</h2><p class="small muted">Where improvement effort lands on the mapped processes. A step that keeps attracting items is a candidate for redesign.</p>
    ${PRS.map((m) => `<h3>${esc(m.title)}</h3><div class="heatrow">${m.steps.filter(isWork).map((s) => { const n = ciFor(m.id, s.id).length; return `<a href="#/process/${m.id}/${s.id}" class="hcell" style="background:${n ? `rgba(224,122,31,${0.2 + 0.25 * n})` : "#F1F4F5"}" data-tip="${s.id} ${esc(s.name)}: ${n} item${n === 1 ? "" : "s"}"><b>${s.id}</b><span>${esc(s.name)}</span><i>${n || ""}</i></a>`; }).join("")}</div>`).join("")}</div>`);
});
route(/^\/ci\/(CI-\d{4}-\d{3})$/, (id) => {
  const c = CIS.find((x) => x.ci_id === id); if (!c) return go404();
  const m = PRSBY[c.process_id]; const s = m?.steps.find((x) => x.id === c.step_id); const hist = CIH.filter((h) => h.ci_id === id);
  const evs = (c.source_ref.match(/EV-\d{4}-\d{3}/g) || []).map((e) => EVBY[e]).filter(Boolean);
  const moc = c.moc_id ? MOCS.find((x) => x.moc_id === c.moc_id) : null;
  const ow = parseWho(c.owner)[0], og = parseWho(c.originator)[0];
  page([10], head(`${esc(id)} ${esc(c.title)}`, `${stageChip(c.stage)} ${esc(c.method)} · source: ${esc(c.source)}`, `<a href="#/ci">Continuous improvement</a>`) + `
  <div class="grid2"><div class="panel"><table class="t">
    <tr><td>Process</td><td>${m ? `<a href="#/process/${m.id}">${esc(m.title)}</a>` : `<a href="#/process/${c.process_id}">${esc(c.process_id)}</a>`}</td></tr>
    <tr><td>Step</td><td>${s ? `<a href="#/process/${m.id}/${s.id}">${s.id} ${esc(s.name)}</a>` : "–"}</td></tr>
    <tr><td>Why it was raised</td><td>${esc(c.source_ref)}${evs.map((e) => `<div class="small"><b>${e.event_id}</b> ${esc(e.title)} (${fmt(toDate(e.date))})</div>`).join("")}</td></tr>
    <tr><td>Owner</td><td>${ow?.person ? personLink(ow.person, ow.name) : esc(c.owner)}</td></tr><tr><td>Raised by</td><td>${og?.person ? personLink(og.person, og.name) : esc(c.originator)}</td></tr>
    <tr><td>Measure</td><td>${esc(c.kpi || "–")}</td></tr><tr><td>Baseline → result</td><td>${esc(c.baseline || "–")} → <b>${esc(c.actual || "not yet measured")}</b> (target ${esc(c.target || "–")})</td></tr>
    ${c.benefit_usd ? `<tr><td>Yearly benefit</td><td><b>${usd(+c.benefit_usd)}</b> <span class="small muted">at the <a href="#/value">public rates</a></span></td></tr>` : ""}
    ${moc ? `<tr><td>Standardised through</td><td>${esc(moc.moc_id)} ${esc(moc.title)} <span class="small muted">${esc(moc.status)}</span></td></tr>` : ""}
    ${c.to_rev ? `<tr><td>Process revision</td><td>Rev ${esc(c.from_rev)} → Rev ${esc(c.to_rev)}</td></tr>` : ""}</table>
    ${c.notes ? `<p class="small" style="margin-top:10px">${esc(c.notes)}</p>` : ""}</div>
  <div class="panel"><h2>History</h2><ul class="events">${hist.map((h) => `<li><span class="muted">${fmt(toDate(h.date))}</span><span>${stageChip(h.stage)} ${esc(h.note)}</span></li>`).join("")}</ul>
    <p class="small muted" style="margin-top:10px">Policy: ${commitLink("ACE-OMS-POL-001#COM_CI_BENEFIT")} · ${commitLink("ACE-OMS-POL-001#COM_CI_STANDARDISE")}</p></div></div>`);
});

route(/^\/value$/, () => {
  const rows = REG["BPM-VAL-001"] || [];
  page([10], head("Value assumptions", "The figures ONE uses to put a money value on process time. Public figures are linked to their source; the rest are labelled as assumptions and can be changed in registers/BPM-VAL-001.csv.", `<a href="#/process">Processes</a>`) + `
  <div class="panel"><table class="t"><tr><th>Figure</th><th class="n">Value</th><th>Unit</th><th>Basis</th><th>Source</th></tr>${rows.map((r) => `<tr><td><b>${esc(r.name)}</b><div class="small muted">${esc(r.group)} · ${esc(r.key)}</div></td><td class="n">${(+r.value).toLocaleString()}</td><td class="small">${esc(r.unit)}</td><td class="small">${esc(r.basis)}</td><td class="small">${r.url ? `<a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.source)}</a>` : esc(r.source)}</td></tr>`).join("")}</table></div>`);
});

// ---------------------------------------------------------------- links back from the other dimensions
function stepsUsing(pred) { const out = []; for (const m of PRS) for (const s of m.steps) if (pred(s, m)) out.push([m, s]); return out; }
function procStepCell(id, c) {
  const hits = stepsUsing((s) => (s.controls || []).includes(id));
  if (hits.length) return hits.map(([m, s]) => `<a href="#/process/${m.id}/${s.id}">${esc(m.title)}, ${s.id} ${esc(s.name)}</a>`).join("<br>");
  return `<span class="muted">Not yet mapped${c.process_planned ? ` (expected in <a href="#/process/${esc(c.process_planned)}">${esc(c.process_planned)}</a>)` : ""}</span>`;
}
function procOfRisk(r) { if (!r.process) return ""; return PRSBY[r.process] ? `Controlled through the <a href="#/process/${r.process}">${esc(PRSBY[r.process].title)}</a>. ` : `Process ${esc(r.process)} (not yet mapped). `; }
function fnProcPanel(fc) {
  const rows = PRS.map((m) => { const lanes = m.lanes.filter((l) => l.function === fc); if (!lanes.length) return ""; const st = stats(m, pick(m, { year: "2026" })); const x = st.FN[fc] || { steps: 0, work: 0, wait: 0, cost: 0 };
    const hin = Object.entries(st.HO).filter(([k]) => k.endsWith(">" + fc)).reduce((a, [, v]) => a + v.n, 0), hout = Object.entries(st.HO).filter(([k]) => k.startsWith(fc + ">")).reduce((a, [, v]) => a + v.n, 0);
    return `<div style="margin-bottom:8px"><a href="#/process/${m.id}">${esc(m.title)}</a>${m.function === fname(fc) ? ` <span class="small muted">(owns it)</span>` : ""}<div class="small">${lanes.map((l) => esc(l.role)).join(", ")}: ${m.steps.filter((s) => lanes.some((l) => l.id === s.lane) && isWork(s)).map((s) => `<a href="#/process/${m.id}/${s.id}">${s.id}</a>`).join(" ")}</div><div class="small muted">2026: ${Math.round(x.work).toLocaleString()} hours worked, ${Math.round(x.wait).toLocaleString()} hours cases waited in its lanes, ${hin} hand-offs in, ${hout} out</div></div>`; }).join("");
  return rows ? `<div class="panel"><h2>Mapped process steps</h2>${rows}</div>` : "";
}
function docProcLine(id) {
  const steps = stepsUsing((s) => (s.doc_refs || []).some((r) => r.split("#")[0] === id) || (s.commitment || "").split("#")[0] === id);
  const gov = PRS.filter((m) => m.policy === id || m.parent === id || (m.commitments || []).some((c) => c.startsWith(id + "#")));
  if (!steps.length && !gov.length) return "";
  return `<p class="small" style="margin:8px 0 0">Processes: ${gov.map((m) => `<a href="#/process/${m.id}">${esc(m.title)}</a> (${m.policy === id ? "governing policy" : m.parent === id ? "parent" : "commitment"})`).join(", ")}${steps.length ? `${gov.length ? ". " : ""}Steps that rely on this document: ${steps.map(([m, s]) => `<a href="#/process/${m.id}/${s.id}">${s.id} ${esc(s.name)}</a>`).join(", ")}` : ""}.</p>`;
}
function secProcChips(id, bm) {
  const hits = stepsUsing((s) => (s.doc_refs || []).includes(`${id}#${bm}`) || s.commitment === `${id}#${bm}`);
  const gov = PRS.filter((m) => (m.commitments || []).includes(`${id}#${bm}`));
  return [...gov.map((m) => `<a class="pchip" href="#/process/${m.id}">${esc(m.title)}</a>`), ...hits.map(([m, s]) => `<a class="pchip" href="#/process/${m.id}/${s.id}" title="${esc(m.title)}">${s.id} ${esc(s.name)}</a>`)].join("");
}
