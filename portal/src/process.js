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

const FLOWSTYLE = { information: { c: "#2F7FB8" }, material: { c: "#8E6A2E" }, people: { c: "#7A4FA0" } };
const wrap = (t, n = 17, max = 3) => { const w = String(t).split(" "); const L = [""]; for (const x of w) { if ((L[L.length - 1] + " " + x).trim().length > n && L[L.length - 1]) L.push(x); else L[L.length - 1] = (L[L.length - 1] + " " + x).trim(); } return L.slice(0, max); };
// ---------------------------------------------------------------- icons (standards/icons/one-icons.json)
const ICONS = D.icons?.icons || {}; const IPRE = D.icons?.base_set?.prefix || "fa-solid fa-";
function ico(key, size = 30, o = {}) {
  const k = ICONS[key] || ICONS[`${(key || "").split(".")[0]}.generic`] || { glyph: "circle-question", colour: "#7D8D95", shape: "circle", name: key };
  const col = o.colour || k.colour, sh = o.shape || k.shape || "circle";
  const badge = o.badge === false ? "" : o.badgeText ? `<b class="oib">${esc(o.badgeText)}</b>` : k.badge ? `<b class="oib">${esc(k.badge)}</b>` : k.badge_glyph ? `<b class="oib"><i class="${IPRE}${k.badge_glyph}"></i></b>` : "";
  return `<span class="oi" style="--c:${col};--s:${size}px"${o.tip === false ? "" : ` data-tip="${esc(o.tip || k.name || key)}"`}><span class="ois ois-${sh}"><i class="${IPRE}${k.glyph}"></i></span>${badge}</span>`;
}
const fo = (x, y, w, h, html) => `<foreignObject x="${x}" y="${y}" width="${w}" height="${h}"><div xmlns="http://www.w3.org/1999/xhtml" class="fo">${html}</div></foreignObject>`;
const REASON = { resource: "Person or team busy", information: "Waiting for information", approval: "Waiting for approval", transport: "Waiting for transport", weather: "Weather",
  batch: "Held for a batch or campaign", parts: "Waiting for parts", window: "Waiting for a work window", permit: "Waiting for a permit", incomplete: "Incomplete or wrong input" };
const RCOL = { resource: "#C8402F", information: "#2F7FB8", approval: "#3D4FA1", transport: "#8E6A2E", weather: "#57656C", batch: "#E07A1F", parts: "#B07A1F", window: "#7A5C9E", permit: "#B5427A", incomplete: "#A32D2D" };
const CAP = REG["BPM-CAP-001"] || []; const SCN = REG["BPM-SCN-001"] || [];

// ---------------------------------------------------------------- extra measures for the map: reasons, stages, capacity, confidence
function period(f) { const y = +f.year; if (y) return [new Date(y, 0, 1), new Date(Math.min(+TODAY, +new Date(y + 1, 0, 1)))]; return [new Date(2024, 0, 1), TODAY]; }
function stepMore(m, cases, f) {
  const R = {}, RW = {}, Q = {}, [p0, p1] = period(f), days = Math.max(1, (p1 - p0) / DAY);
  for (const s of m.steps) { R[s.id] = {}; RW[s.id] = {}; Q[s.id] = 0; }
  const stageOf = {}; for (const g of m.stages || []) for (const id of g.steps) stageOf[id] = g.id;
  const SG = {}; for (const g of m.stages || []) SG[g.id] = { tot: [], wait: 0, work: 0, q: 0 };
  for (const c of cases) {
    const per = {};
    for (const e of c.ev) {
      if (!R[e.step_id]) continue;
      if (e.s && e.a) { const w = (e.s - e.a) / DAY; if (e.wait_reason) R[e.step_id][e.wait_reason] = (R[e.step_id][e.wait_reason] || 0) + w;
        const a = Math.max(+e.a, +p0), b = Math.min(+e.s, +p1); if (b > a) Q[e.step_id] += (b - a) / DAY; }
      if (e.rework_reason) RW[e.step_id][e.rework_reason] = (RW[e.step_id][e.rework_reason] || 0) + 1;
      const g = stageOf[e.step_id]; if (g && e.f) { per[g] = (per[g] || 0) + (e.f - e.a) / DAY; if (e.s) { SG[g].wait += (e.s - e.a) / DAY; SG[g].work += (e.f - e.s) / DAY; } }
    }
    for (const g in per) SG[g].tot.push(per[g]);
  }
  for (const id in Q) Q[id] = Q[id] / days;
  for (const g of m.stages || []) SG[g.id].q = g.steps.reduce((a, id) => a + (Q[id] || 0), 0);
  return { R, RW, Q, SG };
}
function utilisation(m, f) {
  const [p0, p1] = period(f), out = {};
  for (const l of m.lanes) {
    let cap = 0; for (const r of CAP.filter((x) => x.process_id === m.id && x.lane === l.id)) { const a = Math.max(+p0, +PT(r.start)), b = Math.min(+p1, r.end ? +PT(r.end) + DAY : +p1); if (b > a) cap += ((b - a) / DAY / 7) * +r.hours_per_week; }
    let work = 0; for (const c of ledger(m).cases) for (const e of c.ev) if (e.lane === l.id && e.s && e.f && e.s >= p0 && e.s < p1) work += (e.f - e.s) / HR;
    out[l.id] = cap ? (100 * work) / cap : null;
  }
  return out;
}
function confidence(m) {
  let n = 0, full = 0, lw = 0, lr = 0, last = 0;
  for (const c of ledger(m).cases) for (const e of c.ev) { const s = m.steps.find((x) => x.id === e.step_id); if (!isWork(s)) continue; if (+e.a > last) last = +e.a;
    if (e.f) { n++; if (e.a && e.s && e.f) full++; } if (e.s && (e.s - e.a) / DAY > 1) { lw++; if (e.wait_reason) lr++; } }
  const comp = n ? (100 * full) / n : 0, rs = lw ? (100 * lr) / lw : 0, age = (TODAY - last) / DAY;
  const level = comp >= 95 && rs >= 90 && age <= 7 ? "High" : comp >= 80 && rs >= 50 && age <= 31 ? "Medium" : "Low";
  return { level, comp, rs, age };
}
let GCOL = {};
function gcol(m) {
  if (GCOL[m.id]) return GCOL[m.id];
  const S = Object.fromEntries(m.steps.map((s) => [s.id, s])), col = {}; const q = m.steps.filter((s) => s.type === "start").map((s) => [s.id, 0]); let g = 0;
  while (q.length && g++ < 4000) { const [k, c] = q.shift(); if (col[k] !== undefined && col[k] >= c) continue; col[k] = c; for (const n of fwd(S[k])) if (S[n]) q.push([n, c + 1]); }
  return (GCOL[m.id] = col);
}

// ---------------------------------------------------------------- the stage swimlane
const LENSES = [["flow", "Who does what", "org.team"], ["fn", "Functions", "org.company"], ["info", "Information", "doc.generic"], ["time", "Time and cost", "res.time"],
  ["neck", "Bottlenecks", "st.waiting"], ["ci", "Improvement", "mo.improvement"], ["ctl", "Risk and controls", "mo.control"]];
function drawStage(m, g, o) {
  const S = Object.fromEntries(m.steps.map((s) => [s.id, s])), col = gcol(m), ids = g.steps.filter((id) => S[id]);
  const stageOf = {}; for (const x of m.stages) for (const id of x.steps) stageOf[id] = x;
  const cols = [...new Set(ids.map((id) => col[id]))].sort((a, b) => a - b), lc = (id) => cols.indexOf(col[id]);
  const byFn = o.lens === "fn";
  const rows = byFn ? [...new Set(ids.map((id) => laneFn(m, S[id].lane)))].map((f) => ({ key: f, fn: f, label: fname(f) }))
    : [...new Set(ids.map((id) => S[id].lane))].map((l) => { const L = laneOf(m, l); return { key: l, fn: L.function || "CTR", label: L.role, lane: L }; });
  rows.sort((a, b) => (byFn ? m.lanes.findIndex((l) => l.function === a.key) - m.lanes.findIndex((l) => l.function === b.key) : m.lanes.findIndex((l) => l.id === a.key) - m.lanes.findIndex((l) => l.id === b.key)));
  const rowOf = (id) => rows.findIndex((r) => r.key === (byFn ? laneFn(m, S[id].lane) : S[id].lane));
  const LW = 190, CWd = 236, BW = 154, BH = 58, RH = o.lens === "info" ? 182 : o.lens === "time" || o.lens === "neck" ? 172 : 140, TOP = 34;
  const OVH = o.lens === "info" ? 70 : o.lens === "time" || o.lens === "neck" ? 74 : 26;
  const slot = {}, used = {}; for (const id of ids) { const k = `${rowOf(id)}:${lc(id)}`; slot[id] = used[k] || 0; used[k] = (used[k] || 0) + 1; }
  const rh = rows.map((_, i) => RH + (Math.max(1, ...Object.entries(used).filter(([k]) => +k.split(":")[0] === i).map(([, v]) => v)) - 1) * (BH + 40));
  const ry = []; let y = TOP; for (const h of rh) { ry.push(y); y += h; }
  const X1 = 150, W = LW + X1 + cols.length * CWd + 200, H = y + 26;
  const P = {}; for (const id of ids) { const r = rowOf(id); P[id] = { x: LW + X1 + lc(id) * CWd, y: ry[r] + 30 + slot[id] * (BH + 40) }; }
  const st = o.st, more = o.more, cxr = (id) => P[id].x + BW, cy = (id) => P[id].y + BH / 2;
  let svg = `<defs><marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" orient="auto"><path d="M0,0L10,5L0,10z" fill="#3D4A55"/></marker>
    <marker id="a2r" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" orient="auto"><path d="M0,0L10,5L0,10z" fill="#C8402F"/></marker></defs>`;
  svg += `<rect x="0" y="0" width="${W}" height="24" class="sg-head"/><text x="12" y="16" class="sg-ht">${esc(g.name)} · ${esc(g.summary || "")}</text>`;
  rows.forEach((r, i) => {
    const fc = fcol(r.fn); svg += `<rect x="0" y="${ry[i]}" width="${W}" height="${rh[i]}" class="sg-lane" style="${byFn ? `fill:${fc};fill-opacity:.10` : ""}"/><rect x="0" y="${ry[i]}" width="7" height="${rh[i]}" fill="${fc}"/>`;
    svg += fo(14, ry[i] + 12, 44, 44, ico(byFn ? `org.function.${r.fn}` : r.lane?.external ? "ext.contractor" : `org.function.${r.fn}`, 32, { tip: byFn ? fname(r.fn) : `${r.label} — ${fname(r.fn)}` }));
    svg += wrap(r.label, 19, 4).map((t, k) => `<text x="62" y="${ry[i] + 26 + k * 15}" class="sg-ln">${esc(t)}</text>`).join("") + `<text x="62" y="${ry[i] + 26 + wrap(r.label, 19, 4).length * 15}" class="sg-lf" fill="${fc}">${byFn ? "" : esc(fname(r.fn))}</text>`;
    if (o.lens === "neck" && !byFn && o.util) { const u = o.util[r.key]; if (u != null) { const c = u > 85 ? "#C8402F" : u > 65 ? "#E0AE2E" : "#3B6D11";
      svg += `<g data-tip="${esc(r.label)} uses ${Math.round(u)}% of the hours it has for this process${u > 85 ? ". Above about 85%, queues grow sharply." : ""}"><rect x="16" y="${ry[i] + rh[i] - 34}" width="160" height="9" rx="2" class="sg-track"/><rect x="16" y="${ry[i] + rh[i] - 34}" width="${Math.min(160, 1.6 * u)}" height="9" rx="2" fill="${c}"/><text x="16" y="${ry[i] + rh[i] - 12}" class="sg-u" fill="${c}">${Math.round(u)}% of capacity</text></g>`; } }
  });
  // edges
  const exitR = [], exitL = [], entries = [];
  for (const id of ids) {
    const s = S[id]; const outsAll = [...(s.next || []).map((to) => ({ to })), ...(s.branches || [])];
    outsAll.forEach((b, bi) => {
      const n = st ? st.T[`${id}>${b.to}`] || 0 : 0, tot = st ? Object.entries(st.T).filter(([k]) => k.startsWith(id + ">")).reduce((a, [, v]) => a + v, 0) : 0;
      const share = st && tot && outsAll.length > 1 ? ` · ${Math.round((100 * n) / tot)}%` : "";
      const lab = b.label ? esc(b.label) + share : share ? share.slice(3) : "";
      if (P[b.to]) {
        const back = lc(b.to) <= lc(id) && b.to !== id;
        const ho = laneFn(m, s.lane) !== laneFn(m, S[b.to].lane);
        if (back) { const yb = Math.max(P[id].y, P[b.to].y) + BH + OVH; svg += `<path d="M${P[id].x + 14},${P[id].y + BH} L${P[id].x + 14},${yb} L${P[b.to].x + BW / 2},${yb} L${P[b.to].x + BW / 2},${P[b.to].y + BH + 2}" class="sg-e rw" marker-end="url(#a2r)"/><text x="${(P[id].x + P[b.to].x + BW) / 2}" y="${yb + 14}" class="sg-bl rw" text-anchor="middle">${lab}</text>`; }
        else { const xa = cxr(id), xb = P[b.to].x, ya = cy(id), yb2 = cy(b.to), mx = xa + 18 + bi * 8;
          svg += `<path d="M${xa},${ya} L${mx},${ya} L${mx},${yb2} L${xb - 2},${yb2}" class="sg-e${ho ? " ho" : ""}" marker-end="url(#a2)"/>`;
          if (lab) svg += `<text x="${xb - 6}" y="${yb2 - 7}" class="sg-bl" text-anchor="end">${lab}</text>`;
          if (byFn && ho) svg += fo(mx - 13, (ya + yb2) / 2 - 13, 30, 30, ico("flow.handoff", 24, { tip: `Hand-off ${fname(laneFn(m, s.lane))} → ${fname(laneFn(m, S[b.to].lane))}${n ? `: ${n} times` : ""}` })); }
      } else if (S[b.to]) {
        const tg = stageOf[b.to], back = m.stages.indexOf(tg) < m.stages.indexOf(g);
        (back ? exitL : exitR).push({ id, b, lab, tg });
      }
    });
  }
  for (const id of ids) for (const x of m.steps) if (!ids.includes(x.id)) for (const b of [...(x.next || []).map((to) => ({ to })), ...(x.branches || [])]) if (b.to === id) entries.push({ id, from: x, b, tg: stageOf[x.id] });
  exitR.forEach((x, i) => { const ya = cy(x.id) + (x.b.label ? 0 : 0), xa = cxr(x.id); const yy = ya + (exitR.filter((z) => z.id === x.id).indexOf(x)) * 20;
    svg += `<path d="M${xa},${ya} L${xa + 14},${ya} L${xa + 14},${yy} L${W - 10},${yy}" class="sg-e" marker-end="url(#a2)"/><text x="${xa + 30}" y="${yy - 6}" class="sg-bl">${x.lab ? x.lab + " → " : "→ "}${esc(x.tg?.name || "")}</text>`; });
  exitL.forEach((x) => { const yb = P[x.id].y + BH + OVH + 8; svg += `<path d="M${P[x.id].x + 14},${P[x.id].y + BH} L${P[x.id].x + 14},${yb} L${LW + 4},${yb}" class="sg-e rw" marker-end="url(#a2r)"/><text x="${LW + 10}" y="${yb + 14}" class="sg-bl rw">↺ ${x.lab ? x.lab + " · " : ""}back to ${esc(x.tg?.name || "")}</text>`; });
  const seenEntry = new Set();
  for (const e of entries) { if (seenEntry.has(e.id)) continue; seenEntry.add(e.id); const back = m.stages.indexOf(e.tg) > m.stages.indexOf(g);
    if (back) continue;
    svg += `<path d="M${LW + 2},${cy(e.id)} L${P[e.id].x - 2},${cy(e.id)}" class="sg-e" marker-end="url(#a2)"/><text x="${LW + 6}" y="${cy(e.id) - 7}" class="sg-bl">${esc(e.tg?.name || "")} →</text>`; }
  // the cycle: shown as a return stub where it leaves and an entry where it arrives
  if (m.cycle && P[m.cycle.from] && !P[m.cycle.to]) { const id = m.cycle.from; svg += `<path d="M${P[id].x + BW / 2},${P[id].y} L${P[id].x + BW / 2},${P[id].y - 40} L${W - 10},${P[id].y - 40}" class="sg-e cyc" marker-end="url(#a2)"/><text x="${P[id].x + BW / 2 + 8}" y="${P[id].y - 46}" class="sg-bl cy">↻ ${esc(m.cycle.label || "next cycle")} → ${esc(stageOf[m.cycle.to]?.name || "")}</text>`; }
  if (m.cycle && P[m.cycle.to] && !P[m.cycle.from]) { const id = m.cycle.to; svg += `<text x="${P[id].x}" y="${P[id].y + BH + 16}" class="sg-bl cy">↻ from ${esc(stageOf[m.cycle.from]?.name || "")}</text><text x="${P[id].x}" y="${P[id].y + BH + 30}" class="sg-bl cy">${esc(m.cycle.period || "")}</text>`; }
  // nodes
  const maxBar = Math.max(1, ...ids.map((id) => (median(st.S[id].wait) || 0) + (median(st.S[id].work) || 0) / 24), ...ids.map((id) => S[id].target_days || 0));
  for (const id of ids) {
    const s = S[id], p = P[id], ss = st.S[id], w = median(ss.wait), k = median(ss.work), tg = s.target_days;
    const sel = o.sel === id, dim = o.trace && !o.trace.ev.some((e) => e.step_id === id);
    let fill = "#FFFFFF";
    if (o.lens === "neck" && isWork(s) && w != null) fill = tg ? (w + (k || 0) / 24 > 2 * tg ? "#F7C1C1" : w + (k || 0) / 24 > tg ? "#FAE0A6" : "#FFFFFF") : w > 7 ? "#F7C1C1" : w > 2 ? "#FAE0A6" : "#FFFFFF";
    const icol = s.element ? ECOL[s.element] : null;
    let g2 = `<g class="sg-n${sel ? " sel" : ""}${dim ? " dim" : ""}" data-step="${id}" tabindex="0" role="button" aria-label="${id} ${esc(s.name)}">`;
    if (s.type === "start" || s.type === "end") {
      g2 += `<circle cx="${p.x + 24}" cy="${p.y + BH / 2}" r="22" fill="#fff" stroke="#17262E" stroke-width="${s.type === "end" ? 3.5 : 1.5}"/>` + fo(p.x + 9, p.y + BH / 2 - 15, 34, 34, ico(s.icon || (s.type === "start" ? "flow.start" : "flow.end"), 28, { tip: s.name }))
        + wrap(s.name, 18).map((t, i) => `<text x="${p.x + 54}" y="${p.y + BH / 2 - 2 + i * 13}" class="sg-nt2">${esc(t)}</text>`).join("");
    } else {
      g2 += s.type === "xor" ? `<path d="M${p.x + BW / 2},${p.y - 8} L${p.x + BW + 6},${p.y + BH / 2} L${p.x + BW / 2},${p.y + BH + 8} L${p.x - 6},${p.y + BH / 2} Z" fill="${fill}" class="sg-box"/>`
        : `<rect x="${p.x}" y="${p.y}" width="${BW}" height="${BH}" rx="9" fill="${fill}" class="sg-box"/>`;
      g2 += fo(p.x + (s.type === "xor" ? 14 : 8), p.y + BH / 2 - 17, 38, 38, ico(s.icon || "mo.process", 32, { colour: icol || undefined, tip: `${s.name}${s.element ? ` · element ${s.element} ${SHORT[s.element] || ""}` : ""}` }));
      g2 += wrap(s.name, s.type === "xor" ? 12 : 14).map((t, i, A) => `<text x="${p.x + (s.type === "xor" ? 92 : 96)}" y="${p.y + BH / 2 + 4 - (A.length - 1) * 7 + i * 14}" text-anchor="middle" class="sg-nt">${esc(t)}</text>`).join("");
      g2 += `<text x="${p.x}" y="${p.y - 9}" class="sg-id">${id}${s.value ? " · " + s.value : ""}</text>`;
    }
    // lens overlays
    if (isWork(s)) {
      if (o.lens === "flow") { const fl = (m.flows || []).filter((f) => f.from === id); fl.forEach((f, i) => { g2 += fo(p.x + BW - 22 - i * 26, p.y - 30, 28, 28, ico(`flow.${f.type}`, 22, { tip: `${f.type[0].toUpperCase() + f.type.slice(1)}: ${f.carries || ""}` })); }); }
      if (o.lens === "info") { const tc = s.touch || []; tc.slice(0, 5).forEach((t, i) => { const a = (m.artefacts || []).find((x) => x.id === t.a); if (!a) return;
        g2 += fo(p.x + i * 31, p.y + BH + 14, 32, 34, ico(a.icon, 24, { badgeText: t.op, tip: `${{ C: "Creates", R: "Reads", U: "Updates" }[t.op]} ${a.name}${a.system ? " · in " + (ICONS[a.system]?.name || "") : ""}${a.doc ? " · " + a.doc : ""}` })); });
        if (tc.length > 5) g2 += `<text x="${p.x + 5 * 31 + 4}" y="${p.y + BH + 34}" class="sg-bl">+${tc.length - 5}</text>`; }
      if (o.lens === "time" && w != null) { const sc = BW / maxBar, ww = w * sc, kk = ((k || 0) / 24) * sc;
        g2 += `<rect x="${p.x}" y="${p.y + BH + 14}" width="${Math.max(1.5, ww)}" height="10" fill="#E0AE2E"/><rect x="${p.x + ww}" y="${p.y + BH + 14}" width="${Math.max(1.5, kk)}" height="10" fill="#0F6E56"/>`;
        if (tg) g2 += `<line x1="${p.x + tg * sc}" x2="${p.x + tg * sc}" y1="${p.y + BH + 9}" y2="${p.y + BH + 29}" stroke="#17262E" stroke-width="1.5" stroke-dasharray="3 2"/>`;
        g2 += `<text x="${p.x}" y="${p.y + BH + 42}" class="sg-m">wait ${dfmt(w)} · work ${hfmt(k)}${tg ? ` · target ${tg} d` : ""}</text><text x="${p.x}" y="${p.y + BH + 57}" class="sg-m b">${usd((ss.workSum * laneRate(m, s.lane)) / Math.max(1, ss.n))} people cost per pass</text>`; }
      if (o.lens === "neck") { const q = Math.round(more.Q[id] || 0); for (let i = 0; i < Math.min(q, 12); i++) g2 += `<rect x="${p.x + BW - 10 - (i % 6) * 11}" y="${p.y - 18 - Math.floor(i / 6) * 10}" width="8" height="8" rx="1.5" fill="#C8402F"/>`;
        if (q > 12) g2 += `<text x="${p.x + BW - 78}" y="${p.y - 12}" class="sg-q" text-anchor="end">+${q - 12}</text>`;
        const R = Object.entries(more.R[id] || {}).sort((a, b) => b[1] - a[1]), tot = R.reduce((a, [, v]) => a + v, 0); let xx = p.x;
        if (tot) { for (const [r, v] of R) { const wd = (BW * v) / tot; g2 += `<rect x="${xx}" y="${p.y + BH + 14}" width="${wd}" height="10" fill="${RCOL[r] || "#999"}" data-tip="${esc(REASON[r] || r)}: ${Math.round((100 * v) / tot)}% of waiting"/>`; xx += wd; }
          g2 += fo(p.x - 2, p.y + BH + 28, 30, 30, ico(`reason.${R[0][0]}`, 22, { colour: RCOL[R[0][0]], tip: REASON[R[0][0]] })) + `<text x="${p.x + 28}" y="${p.y + BH + 44}" class="sg-m">${esc(REASON[R[0][0]] || "")}</text>`; }
        if (w != null) g2 += `<text x="${p.x + BW}" y="${p.y + BH + 62}" class="sg-q" text-anchor="end">wait ${dfmt(w)}${q ? ` · ${q} in queue on average` : ""}</text>`; }
      if (o.lens === "ci") { const items = ciFor(m.id, id); if (items.length) { const top = [...items].sort((a, b) => STAGES.indexOf(b.stage) - STAGES.indexOf(a.stage))[0];
        g2 += fo(p.x + BW - 18, p.y - 18, 34, 34, ico("mo.improvement", 28, { colour: STCOL[top.stage], badgeText: items.length > 1 ? String(items.length) : undefined, tip: items.map((c) => `${c.ci_id} ${c.title} (${c.stage})`).join(" · ") }));
        g2 += `<text x="${p.x}" y="${p.y + BH + 22}" class="sg-m">${esc(top.ci_id)} · ${esc(top.stage)}</text>`; } }
      if (o.lens === "ctl") { (s.controls || []).slice(0, 4).forEach((c, i) => { const h = CTL[c]?.health || ""; const hc = h === "Effective" ? "#3B6D11" : h === "Degraded" ? "#BA7517" : h === "Failed" ? "#A32D2D" : "#7D8D95";
        g2 += fo(p.x + i * 32, p.y + BH + 12, 32, 34, ico("mo.control", 26, { colour: hc, tip: `${c} ${CTL[c]?.statement || ""} — ${h}` })); });
        const rk = [...new Set((s.controls || []).map((c) => CTL[c]?.risk_id).filter(Boolean))]; if (rk.length) g2 += fo(p.x + BW - 30, p.y - 22, 34, 34, ico("mo.risk", 26, { badgeText: String(rk.length), tip: rk.map((r) => `${r} ${RISK[r]?.title || ""}`).join(" · ") })); }
    }
    svg += g2 + "</g>";
  }
  return `<svg class="sgmap" viewBox="0 0 ${W} ${H}" width="${W}" style="max-width:100%">${svg}</svg>`;
}

// ---------------------------------------------------------------- process page
const PSTATE = { lens: "flow", stage: "", year: "", site: "", trace: "", full: false, pid: "" };
route(/^\/process\/(ACE-[A-Z]{3}-PRS-\d{3})(?:\/(S\d\d))?$/, (pid, sel) => {
  const m = PRSBY[pid]; if (!m) { const r = BPMREG.find((x) => x.process_id === pid); return r ? plannedPage(r) : go404(); }
  if (!m.stages) m.stages = [{ id: "all", name: "All steps", steps: m.steps.map((s) => s.id) }];
  const els = [...new Set((m.oms_tags || []).map(elOf))];
  const owner = parseWho(m.owner)[0]; const reg = BPMREG.find((r) => r.process_id === pid) || {};
  const risks = RISKS.filter((r) => r.process === pid);
  const commits = (m.commitments || []).map((c) => ({ ref: c, ...polSec(c) }));
  const vals = [...new Map(commits.flatMap((c) => valuesIn(c.s)).map((v) => [v.bm, v])).values()];
  const objs = (m.objectives || []).map((id) => (REG["OMS-REG-001_objectives"] || []).find((o) => o.objective_id === id)).filter(Boolean);
  const isInsp = m.value?.model === "risk-exposure";
  if (PSTATE.pid !== pid) { PSTATE.pid = pid; PSTATE.stage = ""; PSTATE.trace = ""; PSTATE.site = ""; }
  if (!m.stages.some((g) => g.id === PSTATE.stage)) PSTATE.stage = "";
  if (sel) { const g = m.stages.find((x) => x.steps.includes(sel)); if (g) PSTATE.stage = g.id; }
  page(els, head(`${ico("mo.process", 34)} ${esc(m.title)}`, esc(m.summary || ""), `<a href="#/process">Processes</a> / ${esc(m.apqc?.l1 || "")} / ${esc(m.apqc?.l2 || "")}`,
    `<div class="ownerbox"><div class="small muted">Process owner</div><div>${owner ? personLink(owner.person, owner.name) : esc(m.owner)}</div><div class="small">${owner?.role ? roleLink(owner.role, owner.title) : ""}</div>
     <div class="small muted" style="margin-top:6px">${esc(m.function)} · ${esc(m.id)} Rev ${esc(m.revision)} · maturity ${esc(reg.maturity || "–")}</div><div class="chips" style="margin-top:6px">${(m.oms_tags || []).map((t) => elIconTag(t)).join("")}</div></div>`) + `
  <div class="thread panel">
    <div class="tcol"><h4>${ico("oms.element.1", 20, { tip: "Values" })} Values</h4>${vals.map(valueChip).join("") || `<span class="muted small">–</span>`}</div><div class="tarrow">→</div>
    <div class="tcol"><h4>${ico("doc.POL", 20)} Policy commitments</h4>${commits.map((c) => `<div class="small">${commitLink(c.ref)}</div>`).join("")}</div><div class="tarrow">→</div>
    <div class="tcol here"><h4>${ico("mo.process", 20)} This process</h4><div class="small"><b>${esc(m.title)}</b></div><div class="small muted">Governed by ${docLink(m.policy)} · parent ${docLink(m.parent)}</div></div><div class="tarrow">→</div>
    <div class="tcol"><h4>${ico("mo.objective", 20)} Objectives</h4>${objs.map((o) => `<div class="small"><b>${esc(o.objective_id)}</b> ${esc(o.title)}</div>`).join("") || `<span class="muted small">–</span>`}</div><div class="tarrow">·</div>
    <div class="tcol"><h4>${ico("mo.risk", 20)} Risks it controls</h4>${risks.map((r) => `<div class="small"><a href="#/risk/${r.risk_id}">${r.risk_id}</a> ${esc(r.title)} ${rateChip(r.current_rating)}</div>`).join("") || `<span class="muted small">None linked yet</span>`}</div>
  </div>
  <div class="ptiles" id="tiles"></div>
  <div class="panel pmap-panel">
    <div class="ptool">
      <div class="lensbar" id="lensbar">${LENSES.map(([k, l, ic]) => `<button data-v="${k}" class="${PSTATE.lens === k ? "on" : ""}">${ico(ic, 22, { tip: false })}<span>${l}</span></button>`).join("")}</div>
      <label class="tsel">Year <select id="fy"><option value="">All years</option>${YEARS.map((y) => `<option ${PSTATE.year === y ? "selected" : ""}>${y}</option>`).join("")}</select></label>
      <label class="tsel">Site <select id="fs"><option value="">All sites</option>${isInsp ? `<option value="OFF">Offshore platforms</option><option value="ON">Onshore sites</option>` : ""}${[...new Set(ledger(m).cases.map((c) => c.site))].sort().map((s) => `<option value="${s}">${esc(SITE[s]?.name || s)}</option>`).join("")}</select></label>
    </div>
    <div class="stagebar" id="stagebar"></div>
    <div class="insight" id="insight"></div>
    <div class="pmap-wrap" id="mapwrap"></div>
    <div class="plegend small" id="legend"></div>
  </div>
  <div class="panel scard" id="card"></div>
  <div class="panel" id="detail" hidden></div>
  <div class="grid2 pgrid"><div class="panel" id="kpis"></div><div class="panel" id="value"></div></div>
  <div class="grid2 pgrid"><div class="panel" id="time"></div><div class="panel" id="funcs"></div></div>
  <div class="grid2 pgrid"><div class="panel" id="improve"></div><div class="panel" id="cases"></div></div>
  <div class="panel"><h2>SIPOC</h2><div class="sipoc">${["suppliers", "inputs", "process", "outputs", "customers"].map((k) => `<div><h4>${k[0].toUpperCase() + k.slice(1)}</h4>${(m.sipoc?.[k] || []).map((x) => `<div class="small">${esc(x)}</div>`).join("")}</div>`).join("")}</div>
    <p class="small muted" style="margin-top:10px">Drawn from <code>processes/${esc(m.id)}.json</code> and measured from <code>registers/${esc(m.ledger)}_*.csv</code>, capacity in <code>registers/BPM-CAP-001.csv</code>, following the <a href="https://github.com/SCMWJTT/OMS/blob/main/standards/process-data/ONE_Process_Data_Requirement.md" target="_blank" rel="noopener">ONE Process Data Requirement</a>. Value assumptions are on the <a href="#/value">value assumptions</a> page.</p></div>`);

  let selStep = sel || "";
  const render = () => {
    const f = { year: PSTATE.year, site: PSTATE.site };
    const cases = pick(m, f), st = stats(m, cases), more = stepMore(m, cases, f), util = utilisation(m, f), conf = confidence(m);
    const hist = m.history || [];
    const st1 = hist.length > 1 ? stats(m, pick(m, { site: PSTATE.site, rev: hist.slice(-2)[0].revision })) : null, st2 = hist.length > 1 ? stats(m, pick(m, { site: PSTATE.site, rev: hist.slice(-1)[0].revision })) : null;
    // stage summaries and the bottleneck stage
    const SGs = m.stages.map((g) => { const x = more.SG[g.id] || { tot: [], wait: 0, work: 0, q: 0 }; const lt = median(x.tot); const tgt = g.steps.reduce((a, id) => a + (m.steps.find((s) => s.id === id)?.target_days || 0), 0);
      return { g, lt, wshare: x.wait + x.work ? (100 * x.wait) / (x.wait + x.work) : null, q: x.q, tgt }; });
    const hot = [...SGs].filter((x) => x.lt != null).sort((a, b) => b.lt * (b.wshare || 0) - a.lt * (a.wshare || 0))[0];
    if (!PSTATE.stage) PSTATE.stage = hot?.g.id || m.stages[0].id;
    const g = m.stages.find((x) => x.id === PSTATE.stage);
    if (!selStep || !g.steps.includes(selStep)) { const cand = g.steps.map((id) => m.steps.find((s) => s.id === id)).filter(isWork).sort((a, b) => (median(st.S[b.id].wait) || 0) - (median(st.S[a.id].wait) || 0)); selStep = cand[0]?.id || g.steps[0]; }
    // tiles
    const kc = (m.kpis || []).find((k) => k.measure === "cycle_median_days"), krt = (m.kpis || []).find((k) => k.measure === "right_first_time" || k.measure === "on_time");
    const tile = (v, l, ok, ic) => `<div class="ptile2 ${ok === false ? "bad" : ok ? "good" : ""}">${ico(ic, 34)}<div><b>${v}</b><span>${l}</span></div></div>`;
    $("#tiles").innerHTML = tile(`${st.cycle != null ? Math.round(st.cycle) : "–"} d`, `Lead time, median${kc ? ` (target ${esc(kc.target.replace(/[^\d]/g, ""))} d)` : ""}`, kc ? kpiOk(kc, st.cycle) : null, "res.time")
      + tile(pct(st.flowEff), "Of that time someone is working", st.flowEff != null ? st.flowEff >= 25 : null, "st.working")
      + tile(krt ? kpiFmt(krt, kpiVal(krt, st)) : "–", krt ? esc(krt.name) : "Right first time", krt ? kpiOk(krt, kpiVal(krt, st)) : null, krt?.measure === "on_time" ? "flow.timer" : "st.effective")
      + tile(usd((st.labour + st.logistics) / Math.max(1, st.n)), `Cost per ${esc(m.case_label || "case")}${isInsp ? " incl. trips" : ""}`, null, "mo.cost")
      + `<div class="ptile2 conf-${conf.level.toLowerCase()}" data-tip="Data confidence (ONE Process Data Requirement §6): ${Math.round(conf.comp)}% of events have all three times; ${Math.round(conf.rs)}% of long waits have a reason; newest event ${Math.round(conf.age)} days old">${ico("data.dataset", 34)}<div><b>${conf.level}</b><span>Data confidence</span></div></div>`;
    // stage bar
    $("#stagebar").innerHTML = SGs.map((x, i) => `<button class="stg2 ${x.g.id === PSTATE.stage ? "on" : ""}" data-stage="${x.g.id}" style="--z:${SGs.length - i}">
      ${x === hot ? `<span class="hot2">${ico("st.waiting", 18, { tip: false })} bottleneck</span>` : ""}${ico(x.g.icon || "mo.process", 30, { colour: x.g.element ? ECOL[x.g.element] : undefined, tip: false })}
      <span class="nm">${esc(x.g.name)}</span><span class="sm">${x.lt != null ? dfmt(x.lt) : "–"}${x.tgt ? ` · target ${x.tgt} d` : ""} · ${Math.round(x.q)} waiting</span>
      <span class="bar2"><i style="width:${x.wshare || 0}%;background:#E0AE2E"></i><i style="width:${100 - (x.wshare || 0)}%;background:#0F6E56"></i></span></button>`).join("");
    for (const b of $$(".stg2")) b.onclick = () => { PSTATE.stage = b.dataset.stage; selStep = ""; history.replaceState(null, "", `#/process/${pid}`); render(); };
    // map
    const trace = PSTATE.trace ? ledger(m).byId[PSTATE.trace] : null;
    $("#mapwrap").innerHTML = drawStage(m, g, { lens: PSTATE.lens, st, more, util, sel: selStep, trace });
    for (const n of $$(".sg-n", $("#mapwrap"))) { n.onclick = () => { selStep = n.dataset.step; history.replaceState(null, "", `#/process/${pid}/${selStep}`); render(); }; n.onkeydown = (e) => { if (e.key === "Enter") n.onclick(); }; }
    // insight line
    const work = g.steps.map((id) => m.steps.find((s) => s.id === id)).filter(isWork);
    const worst = [...work].sort((a, b) => (median(st.S[b.id].wait) || 0) - (median(st.S[a.id].wait) || 0))[0];
    let ins = "";
    if (worst) { const w = median(st.S[worst.id].wait), u = util[worst.lane], R = Object.entries(more.R[worst.id] || {}).sort((a, b) => b[1] - a[1]), tot = R.reduce((a, [, v]) => a + v, 0);
      const why = R.length ? `${Math.round((100 * R[0][1]) / tot)}% of the waiting is "${REASON[R[0][0]].toLowerCase()}"` : "";
      const capS = u == null ? "" : u > 85 ? ` ${esc(laneOf(m, worst.lane).role)} is at ${Math.round(u)}% of capacity, so more people or fewer reviews each would cut the wait.` : ` ${esc(laneOf(m, worst.lane).role)} is at ${Math.round(u)}% of capacity, so capacity is not the main cause.`;
      ins = PSTATE.lens === "neck" ? `${ico("st.waiting", 22, { tip: false })} <b>${esc(worst.name)}</b> is where work waits longest in this stage: median ${dfmt(w)}${worst.target_days ? ` against a target of ${worst.target_days} d` : ""}. ${why}.${capS}`
        : PSTATE.lens === "time" ? `${ico("res.time", 22, { tip: false })} Amber is waiting, green is working; the dashed mark is the step's target. This stage takes a median ${dfmt(SGs.find((x) => x.g === g)?.lt)} per ${esc(m.case_label)}.`
        : PSTATE.lens === "info" ? `${ico("doc.generic", 22, { tip: false })} Each step shows the documents, records and data it creates (C), reads (R) or updates (U). Hover an icon for the record and the system it lives in.`
        : PSTATE.lens === "fn" ? `${ico("org.company", 22, { tip: false })} Lanes grouped by function. ${ico("flow.handoff", 18, { tip: false })} marks a hand-off between functions; bold arrows cross a function boundary.`
        : PSTATE.lens === "ci" ? `${ico("mo.improvement", 22, { tip: false })} Improvement items pinned to the steps they target, coloured by how far they have got.`
        : PSTATE.lens === "ctl" ? `${ico("mo.control", 22, { tip: false })} Controls performed at each step, coloured by health, and the risks they address.`
        : `${ico("org.team", 22, { tip: false })} Who does each step. Small icons above a step show what moves on from it: information, material or people. Branch figures are the share of real ${esc(m.case_label)}s that took each path.`; }
    $("#insight").innerHTML = ins;
    // legend: element colours in this stage + lens keys
    const elsHere = [...new Set(work.map((s) => s.element).filter(Boolean))];
    $("#legend").innerHTML = `<span class="lg">Step icon colour = OMS element:</span>${elsHere.map((e) => `<span class="lg"><i class="dot" style="background:${ECOL[e]}"></i>${e} ${esc(SHORT[e] || "")}</span>`).join("")}`
      + (PSTATE.lens === "neck" ? `<span class="lg"><i style="background:#C8402F;width:9px;height:9px"></i>one ${esc(m.case_label)} waiting (average queue)</span>${[...new Set(work.flatMap((s) => Object.keys(more.R[s.id] || {})))].map((r) => `<span class="lg"><i style="background:${RCOL[r]}"></i>${esc(REASON[r])}</span>`).join("")}` : "")
      + (PSTATE.lens === "info" ? `<span class="lg"><b>C</b> creates · <b>R</b> reads · <b>U</b> updates</span><span class="lg">Document blues: ${["POL", "STD", "PRA", "PRC", "WIN", "SPC"].map((c) => ico(`doc.${c}`, 18)).join("")}</span><span class="lg">${ico("rec.generic", 18)} records</span><span class="lg">${ico("data.register", 18)} data</span>` : "")
      + (PSTATE.lens === "time" ? `<span class="lg"><i style="background:#E0AE2E"></i>waiting</span><span class="lg"><i style="background:#0F6E56"></i>working</span><span class="lg">┆ target</span>` : "")
      + (PSTATE.lens === "ci" ? STAGES.map((s) => `<span class="lg"><i class="dot" style="background:${STCOL[s]}"></i>${s}</span>`).join("") : "")
      + (PSTATE.lens === "ctl" ? `<span class="lg"><i class="dot" style="background:#3B6D11"></i>effective</span><span class="lg"><i class="dot" style="background:#BA7517"></i>degraded</span><span class="lg"><i class="dot" style="background:#A32D2D"></i>failed</span>` : "");
    drawCard(m, selStep, st, more, util);
    drawDetail(m, selStep, st, cases); $("#detail").hidden = !PSTATE.full;
    drawKpis(m, st); drawValue(m); drawTime(m, st, st1, st2); drawFuncs(m, st); drawImprove(m); drawCases(m, cases, trace);
  };
  $("#lensbar").onclick = (e) => { const b = e.target.closest("button"); if (!b) return; PSTATE.lens = b.dataset.v; for (const x of $$("#lensbar button")) x.classList.toggle("on", x === b); render(); };
  $("#fy").oninput = (e) => { PSTATE.year = e.target.value; render(); };
  $("#fs").value = PSTATE.site; if ($("#fs").value !== PSTATE.site) PSTATE.site = "";
  $("#fs").oninput = (e) => { PSTATE.site = e.target.value; render(); };
  PSTATE.trace = PSTATE.trace && ledger(m).byId[PSTATE.trace] ? PSTATE.trace : "";
  render();
  window.__render = render;
});
function elIconTag(t) { const e = elOf(t); return `<a href="#/exp/${t}" class="eltag">${ico(`oms.element.${e}`, 22)}<span>${esc(t)}</span></a>`; }

function drawCard(m, sid, st, more, util) {
  const s = m.steps.find((x) => x.id === sid), el = $("#card"); if (!s) { el.innerHTML = ""; return; }
  const l = laneOf(m, s.lane), ss = st.S[sid], w = median(ss.wait), k = median(ss.work), u = util[s.lane];
  const R = Object.entries(more.R[sid] || {}).sort((a, b) => b[1] - a[1]), tot = R.reduce((a, [, v]) => a + v, 0);
  const RW = Object.entries(more.RW[sid] || {}).sort((a, b) => b[1] - a[1]);
  let body = "";
  if (PSTATE.lens === "info") body = `<div class="cgrid">${(s.touch || []).map((t) => { const a = (m.artefacts || []).find((x) => x.id === t.a); return a ? `<div class="crow">${ico(a.icon, 26, { badgeText: t.op })}<div><b>${esc(a.name)}</b><div class="small muted">${{ C: "Created", R: "Read", U: "Updated" }[t.op]} here${a.system ? ` · ${esc(ICONS[a.system]?.name || "")}` : ""}${a.doc ? ` · ${docLink(a.doc)}` : ""}</div></div></div>` : ""; }).join("") || `<span class="muted small">No artefacts recorded.</span>`}</div>`;
  else if (PSTATE.lens === "neck") body = `${R.length ? R.map(([r, v]) => `<div class="rrow">${ico(`reason.${r}`, 22, { colour: RCOL[r] })}<span>${esc(REASON[r])}</span><div><i style="width:${(100 * v) / tot}%;background:${RCOL[r]}"></i></div><b>${Math.round((100 * v) / tot)}%</b></div>`).join("") : `<span class="muted small">No waiting recorded at this step.</span>`}
    ${u != null ? `<p class="small" style="margin-top:8px">${ico("org.role", 20)} ${esc(l.role)} uses <b>${Math.round(u)}%</b> of the hours it has for this process. ${u > 85 ? "Queues grow sharply above about 85%: capacity is a main cause here." : "Capacity is not the main cause here."}</p>` : ""}
    ${RW.length ? `<p class="small">${ico("st.rework", 18)} Rework reasons: ${RW.map(([r, n]) => `${esc(REASON[r])} (${n})`).join(", ")}</p>` : ""}`;
  else if (PSTATE.lens === "ci") { const items = ciFor(m.id, sid); body = items.map((c) => `<a class="crow ci" href="#/ci/${c.ci_id}">${ico("mo.improvement", 26, { colour: STCOL[c.stage] })}<div><b>${c.ci_id} ${esc(c.title)}</b><div class="small muted">${esc(c.stage)} · ${esc(c.method)} · ${esc(c.source)}${c.baseline ? ` · ${esc(c.baseline)} → ${esc(c.actual || "…")}` : ""}</div></div></a>`).join("") || `<span class="muted small">No improvement item on this step.</span>`; }
  else if (PSTATE.lens === "ctl") body = (s.controls || []).map((c) => { const h = CTL[c]?.health || ""; return `<div class="crow">${ico("mo.control", 26, { colour: h === "Effective" ? "#3B6D11" : h === "Degraded" ? "#BA7517" : "#A32D2D" })}<div><b>${ctlChip(c)}</b> ${esc(CTL[c]?.statement || "")}<div class="small muted">${esc(h)}${CTL[c]?.risk_id ? ` · protects <a href="#/risk/${CTL[c].risk_id}">${CTL[c].risk_id}</a> ${esc(RISK[CTL[c].risk_id]?.title || "")}` : ""}</div></div></div>`; }).join("") || `<span class="muted small">No control is performed at this step.</span>`;
  else if (PSTATE.lens === "time") { const tot = (w || 0) + (k || 0) / 24, sh = tot ? (100 * (w || 0)) / tot : 0;
    body = `<div class="small">${ico("st.waiting", 20)} Waiting is <b>${Math.round(sh)}%</b> of the time a ${esc(m.case_label)} spends at this step${s.target_days ? `; median ${dfmt(tot)} against a target of ${s.target_days} d (${tot > s.target_days ? "over" : "within"} target)` : ""}.</div>
      <div class="small" style="margin-top:6px">${ico("mo.cost", 20)} People cost per pass <b>${usd((ss.workSum * laneRate(m, s.lane)) / Math.max(1, ss.n))}</b> at ${usd(laneRate(m, s.lane))} an hour for ${esc(l.role)} (<a href="#/value">rates</a>).</div>`; }
  else if (PSTATE.lens === "fn") { const ins = m.steps.filter((x) => outs(x).includes(sid)), out = outs(s).map((id) => m.steps.find((x) => x.id === id)).filter(Boolean);
    body = `<div class="small">Receives from ${ins.map((x) => `<b style="color:${fcol(laneFn(m, x.lane))}">${esc(fname(laneFn(m, x.lane)))}</b> (${x.id})`).join(", ") || "–"}; passes to ${out.map((x) => `<b style="color:${fcol(laneFn(m, x.lane))}">${esc(fname(laneFn(m, x.lane)))}</b> (${x.id})`).join(", ") || "–"}.</div>`; }
  else body = `<div class="small">${(s.inputs || []).map(esc).join(", ") || "–"} → ${(s.outputs || []).map(esc).join(", ") || "–"}</div>${(m.flows || []).filter((f) => f.from === sid).map((f) => `<div class="crow">${ico(`flow.${f.type}`, 22)}<span class="small">${esc(f.carries || "")}</span></div>`).join("")}`;
  el.innerHTML = `<div class="chead">${ico(s.icon || "mo.process", 44, { colour: s.element ? ECOL[s.element] : undefined })}<div><div class="crumb">Step ${s.id}${s.element ? ` · element ${s.element} ${esc(SHORT[s.element] || "")}` : ""}${s.value ? ` · ${{ VA: "value-added", BVA: "needed by the business", NVA: "waste" }[s.value]}` : ""}</div><h2>${esc(s.name)}</h2>
    <div class="small">${ico(`org.function.${l.function || "CTR"}`, 20)} ${ROLE[l.role_id] ? roleLink(ROLE[l.role_id], l.role) : esc(l.role)} · <span style="color:${fcol(l.function)}">${esc(fname(l.function))}</span></div></div>
    <div class="cnums">${[["Passes", ss.n.toLocaleString()], ["Median wait", dfmt(w)], ["Median work", hfmt(k)], ["Target", s.target_days ? s.target_days + " d" : "–"], ["Queue", `${Math.round(more.Q[sid] || 0)}`], ["Open now", ss.inQ]].map(([a, b]) => `<div><b>${b}</b><span>${a}</span></div>`).join("")}</div></div>
    <div class="cbody">${body}</div><button class="btn small" id="cfull">${PSTATE.full ? "Hide" : "Show"} the full step record</button>`;
  $("#cfull").onclick = () => { PSTATE.full = !PSTATE.full; $("#detail").hidden = !PSTATE.full; $("#cfull").textContent = `${PSTATE.full ? "Hide" : "Show"} the full step record`; };
}

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
