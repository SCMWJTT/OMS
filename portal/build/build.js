#!/usr/bin/env node
/* ONE Portal build: reads the repository (Word documents, registers, people, protocol) and writes
 *   portal/dist/one-data.json   the data the portal draws from
 *   portal/dist/index.html      the portal, self-contained (data, styles and script inlined) — opens by double-click or on any web server
 * Usage: node portal/build/build.js [repo-root]
 * Nothing in the portal is typed in by hand: change a document or register, rebuild, and every view follows. */
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(process.argv[2] || path.join(__dirname, "..", ".."));
const A = require(path.join(ROOT, "protocol/engine/one-audit.js"));
const JSZip = require("jszip");

const P = JSON.parse(fs.readFileSync(path.join(ROOT, "protocol/one-protocol.json"), "utf8"));
const dec = (s) => (s || "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, "&");
const txt = (x) => dec(((x.replace(/<w:tab\/>/g, " ").match(/<w:t(?:\s[^>]*)?>[^<]*<\/w:t>/g)) || []).map((t) => t.replace(/<[^>]+>/g, "")).join("")).replace(/\s+/g, " ").trim();
const SMAP = new Map(); for (const s of P.styles) { SMAP.set(s.id, s); for (const a of s.aliases || []) SMAP.set(a, s); }
const KIND = { "ODS.Requirement": "req", "ODS.Responsibility": "resp", "ODS.ApprovalRequirement": "appr", "ODS.RecordRequirement": "rec",
  "ODS.RiskControl": "ctl", "ODS.Warning": "warn", "ODS.Note": "note", "ODS.PerformanceIndicator": "kpi", "ODS.DocumentReference": "ref",
  "ODS.ExternalStandard": "ext", "ODS.ProcedureStep": "step", "ODS.Definition": "def", "ODS.Example": "note", "ListBullet": "li", "Caption": "cap" };
const SKIP = /^(ONEBrand|ONESectionLabel|ONECoverCaption|ONEMetadata|DocumentKicker|ONEPullQuote|ONEQuoteBy)$/;
const FRONT = new Set(["Document control", "Revision history", "Approval and issue", "Document map"]);
const CID = new RegExp(P.control_id.pattern, "g"), REF = new RegExp(P.numbering.reference, "g");
const csv = (f) => { const p = path.join(ROOT, f); return fs.existsSync(p) ? A.parseCsv(fs.readFileSync(p, "utf8")) : []; };

async function readDoc(file, folder) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const xml = (await zip.file("word/document.xml").async("string")).replace(/<w:txbxContent>[\s\S]*?<\/w:txbxContent>/g, "");
  const cp = (await zip.file("docProps/custom.xml")?.async("string")) || "";
  const props = {}; for (const m of cp.matchAll(/name="ODS\.([^"]+)"[^>]*>\s*<vt:\w+>([^<]*)</g)) props[m[1]] = dec(m[2]).trim();
  const meta = {}; for (const m of xml.matchAll(/<w:tag w:val="ODS\.Meta\.([^"]+)"\/>[\s\S]*?<w:sdtContent>([\s\S]*?)<\/w:sdtContent>/g)) if (!meta[m[1]]) meta[m[1]] = txt(m[2]);
  const doc = { id: props.DocumentId || meta.DocumentID, title: props.Title || meta.Title, type: props.DocumentType, level: (props.Level || "").replace(/\D/g, ""),
    revision: props.Revision, status: props.Status, issued: props.IssueDate, effective: props.EffectiveDate, owner: props.DocumentOwner, author: props.Author,
    approver: props.Approver, custodian: props.Custodian, reviewers: props.Reviewer, endorser: props.Endorser, func: props.PrimaryFunction,
    tags: (props.TitleOMSTags || "").split(",").map((s) => s.trim()).filter(Boolean), parent: props.Parent || "", applies: props.Applicability,
    framework: props.Framework, folder, file: `${folder}/${path.basename(file)}`, subtitle: "", sections: [], revisions: [] };
  doc.system = (doc.id || "").split("-")[1]; doc.typeCode = (doc.id || "").split("-")[2];
  // walk paragraphs and top-level tables in order
  const re = /<w:tbl>[\s\S]*?<\/w:tbl>|<w:p(?=[\s>])[^>]*>[\s\S]*?<\/w:p>/g; let m, sec = null, pendingTag = false, inFront = false, seenTitle = false;
  const newSec = (title, level, bm) => { sec = { bm, title, level, tags: [], blocks: [] }; doc.sections.push(sec); pendingTag = true; };
  // nested tables: collapse inner tables first by matching outermost with a counter
  const tokens = []; { const t = /<w:tbl>|<\/w:tbl>/g; let depth = 0, start = 0, last = 0, mm;
    while ((mm = t.exec(xml))) { if (mm[0] === "<w:tbl>") { if (depth === 0) { tokens.push(["x", xml.slice(last, mm.index)]); start = mm.index; } depth++; }
      else { depth--; if (depth === 0) { tokens.push(["t", xml.slice(start, mm.index + 8)]); last = mm.index + 8; } } }
    tokens.push(["x", xml.slice(last)]); }
  for (const [kind, chunk] of tokens) {
    if (kind === "t") {
      const rows = [...chunk.matchAll(/<w:tr[\s>][\s\S]*?<\/w:tr>/g)].map((r) => [...r[0].matchAll(/<w:tc>[\s\S]*?<\/w:tc>/g)].map((c) => txt(c[0])));
      if (rows.length && rows[0][0] === "Revision" && rows[0][1] === "Date") doc.revisions = rows.slice(1).map((r) => ({ rev: r[0], date: r[1], text: r[2] }));
      if (sec && !inFront && rows.length) sec.blocks.push({ k: "table", rows });
      continue;
    }
    for (const pm of chunk.matchAll(/<w:p(?=[\s>])[^>]*>[\s\S]*?<\/w:p>/g)) {
      const p = pm[0], raw = (p.match(/<w:pStyle w:val="([^"]+)"/) || [])[1] || "Normal", st = SMAP.get(raw), sid = st ? st.id : raw, t = txt(p);
      if (!t) continue;
      if (SKIP.test(raw)) continue;
      if (sid === "Title") { seenTitle = true; continue; }
      if (sid === "DocumentSubTitle") { doc.subtitle = t; continue; }
      if (/^Heading[123]$/.test(sid)) {
        const bm = (p.match(/<w:bookmarkStart[^>]*w:name="([^"_][^"]*)"/) || [])[1] || "";
        inFront = FRONT.has(t); newSec(t, +sid.slice(-1), bm); continue;
      }
      if (sid === "ODSTagLine") {
        const cc = (p.match(/<w:tag w:val="ODS\.OMSTags@[^"]*"\/>[\s\S]*?<w:sdtContent>([\s\S]*?)<\/w:sdtContent>/) || [])[1];
        const tags = (cc ? txt(cc) : t.replace(/^OMS\s*/, "")).split(",").map((s) => s.trim()).filter(Boolean);
        if (pendingTag && sec) sec.tags = tags; pendingTag = false; continue;
      }
      pendingTag = false;
      if (!sec || inFront || !seenTitle) continue;
      const b = { k: KIND[sid] || "p", t };
      const ids = [...new Set([...p.matchAll(/<w:tag w:val="ODS\.Control@([^"]+)"/g)].map((x) => x[1]))]; if (ids.length) b.c = ids;
      const refs = [...new Set([...t.matchAll(REF)].map((x) => x[0].split(/\s*§/)[0]))].filter((x) => x !== doc.id); if (refs.length) b.r = refs;
      sec.blocks.push(b);
    }
  }
  doc.sections = doc.sections.filter((s) => !FRONT.has(s.title));
  return doc;
}

(async () => {
  const docs = [];
  for (const folder of ["finals", "manuals"]) {
    const dir = path.join(ROOT, folder); if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir).sort()) if (/\.docx$/i.test(f) && !f.startsWith("~$")) docs.push(await readDoc(path.join(dir, f), folder));
  }
  // gateway results from the shared checker
  const people = A.peopleFromCsv(fs.readFileSync(path.join(ROOT, P.people.source), "utf8"), P);
  const files = []; for (const folder of ["finals", "manuals"]) for (const f of fs.readdirSync(path.join(ROOT, folder))) if (/\.docx$/i.test(f)) files.push({ name: f, folder, bytes: fs.readFileSync(path.join(ROOT, folder, f)) });
  const audit = await A.auditSet(files, { protocol: P, people });
  const gate = {}; for (const r of audit.results) gate[r.facts.docId] = { outcome: r.outcome, errors: r.counts.errors, warnings: r.counts.warnings, format: r.facts.format, legacy: r.facts.legacy,
    findings: r.findings.map((f) => ({ rule: f.rule, sev: f.severity, fix: f.fix, msg: f.msg })) };
  // people (compact)
  const ppl = csv(P.people.source).map((r) => ({ id: r["Employee ID"], n: r["Full Name"], t: r["Job Title"], f: r["Function"], d: r["Department"], g: r["Grade"].slice(0, 2),
    to: r["Reports To (ID)"], dl: r["Dotted Line To (ID)"], dlp: r["Dotted Line Purpose"], disc: r["Discipline"], role: r["OMS Role"], loc: r["Work Location"],
    r: r["Role ID"] || "", s: r["Site"] || "", st: r["Status"] || "Active", left: r["Left Date"] || "", hire: r["Hire Date"], em: r["Email"], fc: r["Function Code"],
    q: [r["Base Degree"], r["Institution"], r["Postgraduate / Professional"]].filter(Boolean).join("; ") }));
  // the organisational dimension: editable CSV files in company/org
  const company = { roles: csv("company/org/roles.csv"), omsRoles: csv("company/org/oms_roles.csv"), sites: csv("company/org/sites.csv"), functions: csv("company/org/functions.csv"),
    links: csv("company/org/function_links.csv"), changes: csv("company/org/staff_changes.csv"),
    profile: fs.existsSync(path.join(ROOT, "company/ACE_Company_Profile.md")) ? fs.readFileSync(path.join(ROOT, "company/ACE_Company_Profile.md"), "utf8") : "" };
  const reg = {}; for (const f of fs.readdirSync(path.join(ROOT, "registers"))) if (f.endsWith(".csv")) reg[f.replace(".csv", "")] = csv(`registers/${f}`);
  // process models (processes/*.json, ONE-PRS/1 or /2)
  const processes = [];
  for (const dir of ["processes"]) { const d = path.join(ROOT, dir); if (fs.existsSync(d)) for (const f of fs.readdirSync(d)) if (f.endsWith(".json")) processes.push(JSON.parse(fs.readFileSync(path.join(d, f), "utf8"))); }
  const data = { built: new Date().toISOString(), protocol: { version: P.version, elements: P.elements, expectations: P.expectations, systems: P.systems, types: P.types,
    sites: P.sites, functions: P.functions, planned: P.document_register.planned }, docs, gate, people: ppl, company, registers: reg, processes,
    icons: fs.existsSync(path.join(ROOT, "standards/icons/one-icons.json")) ? JSON.parse(fs.readFileSync(path.join(ROOT, "standards/icons/one-icons.json"), "utf8")) : null,
    api: process.env.ONE_API || "https://oms-api.cynmark.app" };
  const out = path.join(ROOT, "portal/dist"); fs.mkdirSync(out, { recursive: true });
  // the original Word files, so the owner's "Download for Word" can write tracked changes into the real document
  fs.mkdirSync(path.join(out, "docs"), { recursive: true });
  const brand = path.join(ROOT, "company/branding"); if (fs.existsSync(brand)) { fs.mkdirSync(path.join(out, "brand"), { recursive: true }); for (const f of fs.readdirSync(brand)) fs.copyFileSync(path.join(brand, f), path.join(out, "brand", f)); }
  for (const d of docs) fs.copyFileSync(path.join(ROOT, d.file), path.join(out, "docs", `${d.id}.docx`));
  const json = JSON.stringify(data);
  fs.writeFileSync(path.join(out, "one-data.json"), json);
  // inline into the page
  const src = path.join(ROOT, "portal/src");
  if (fs.existsSync(path.join(src, "index.html"))) {
    let html = fs.readFileSync(path.join(src, "index.html"), "utf8");
    const css = fs.readFileSync(path.join(src, "style.css"), "utf8") + (fs.existsSync(path.join(src, "process.css")) ? "\n" + fs.readFileSync(path.join(src, "process.css"), "utf8") : "");
    // process.js (Process and Improvement dimensions) runs inside the same script as app.js, before the first route is drawn
    let js = fs.readFileSync(path.join(src, "app.js"), "utf8"); const pjs = path.join(src, "process.js");
    if (fs.existsSync(pjs)) { const extra = fs.readFileSync(pjs, "utf8"); const at = js.lastIndexOf("\ngo();"); js = at >= 0 ? js.slice(0, at) + "\n" + extra + js.slice(at) : js + "\n" + extra; }
    html = html.replace("<!--STYLE-->", () => `<style>\n${css}\n</style>`).replace("<!--DATA-->", () => `<script>window.ONE_DATA=${json.replace(/<\//g, "<\\/")};</script>`)
               .replace("<!--SCRIPT-->", () => `<script>\n${js}\n</script>`);
    fs.writeFileSync(path.join(out, "index.html"), html);
  }
  const nb = docs.reduce((a, d) => a + d.sections.reduce((b, s) => b + s.blocks.filter((x) => ["req", "resp", "appr", "rec", "ctl"].includes(x.k)).length, 0), 0);
  console.log(`ONE portal data: ${docs.length} documents, ${docs.reduce((a, d) => a + d.sections.length, 0)} sections, ${nb} binding statements, ${Object.keys(reg).length} registers, ${ppl.length} people, ${(json.length / 1048576).toFixed(1)} MB`);
})();
