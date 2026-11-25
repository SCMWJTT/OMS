/* ONE Auditor engine — the single implementation of the ONE Protocol rules.
 * Runs in Node (CLI, GitHub Action), in Electron (ONE Studio) and in the browser (Portal, Word add-in).
 * Needs JSZip. Rules and code lists come from one-protocol.json; nothing about ACE is hard-coded here.
 * auditDocx(bytes, ctx)  -> result for one document
 * auditSet(files, ctx)   -> results for a set, plus cross-document checks (uniqueness, parents, lock files)
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory(require("jszip"));
  else root.OneAudit = factory(root.JSZip);
})(typeof self !== "undefined" ? self : this, function (JSZip) {
  "use strict";
  const ENGINE_VERSION = "1.0.0";
  const MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December";
  const DATE_RE = new RegExp(`^\\d{1,2} (${MONTHS}) \\d{4}$`);
  const IGNORE_BM = /^(_GoBack|_Toc|_Ref|_Hlk)/;

  // ---------- small helpers ----------
  const dec = (s) => (s || "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, "&");
  const norm = (s) => dec(s).replace(/\s+/g, " ").trim();
  const textOf = (xml) => norm(xml.replace(/<w:tab\/>/g, " ").replace(/<w:br\/>/g, " ").match(/<w:t(?:\s[^>]*)?>[^<]*<\/w:t>/g)?.map((t) => t.replace(/<[^>]+>/g, "")).join("") || "");
  const attr = (xml, re) => { const m = xml.match(re); return m ? dec(m[1]) : null; };
  const nameOf = (person) => (person || "").split(" — ")[0].trim();

  function parseCsv(text) {
    const rows = []; let row = [], f = "", q = false;
    text = text.replace(/^﻿/, "");
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (q) { if (c === '"' && text[i + 1] === '"') { f += '"'; i++; } else if (c === '"') q = false; else f += c; }
      else if (c === '"') q = true; else if (c === ",") { row.push(f); f = ""; }
      else if (c === "\n") { row.push(f); rows.push(row); row = []; f = ""; } else if (c !== "\r") f += c;
    }
    if (f || row.length) { row.push(f); rows.push(row); }
    const h = rows.shift();
    return rows.filter((r) => r.length > 1).map((r) => Object.fromEntries(h.map((k, i) => [k, r[i]])));
  }
  function peopleFromCsv(text, proto) {
    const m = new Map(); m.left = new Map(); m.titles = new Set();
    for (const r of parseCsv(text)) {
      const n = r[proto.people.name_column], t = r[proto.people.title_column];
      if ((r.Status || "Active") === "Left") { m.left.set(n, r["Left Date"] || ""); if (!m.has(n)) m.set(n, t); continue; }
      m.set(n, t); m.titles.add(t);
    }
    return m;
  }

  // Minimal well-formedness check (G15)
  function wellFormed(xml) {
    const stack = []; const re = /<(\/?)([A-Za-z_][\w:.-]*)[^>]*?(\/?)>|<\?[\s\S]*?\?>|<!--[\s\S]*?-->|<!\[CDATA\[[\s\S]*?\]\]>/g; let m;
    while ((m = re.exec(xml))) {
      if (!m[2]) continue;
      if (m[3] === "/") continue;
      if (m[1] === "/") { if (stack.pop() !== m[2]) return `mismatched </${m[2]}> at ${m.index}`; }
      else stack.push(m[2]);
    }
    return stack.length ? `unclosed <${stack[stack.length - 1]}>` : null;
  }

  // ---------- document model ----------
  function styleMap(proto) {
    const m = new Map();
    for (const s of proto.styles) { m.set(s.id, s); for (const a of s.aliases || []) m.set(a, s); }
    return m;
  }

  function parseDocument(xml, smap) {
    const body = xml.replace(/<w:txbxContent>[\s\S]*?<\/w:txbxContent>/g, "");
    const re = /<w:tbl>|<\/w:tbl>|<w:p(?=[\s>])[^>]*>[\s\S]*?<\/w:p>/g;
    const paras = []; const tables = []; let depth = 0, m, cur = null;
    while ((m = re.exec(body))) {
      const t = m[0];
      if (t === "<w:tbl>") { depth++; if (depth === 1) { cur = { rows: [], start: paras.length }; } continue; }
      if (t === "</w:tbl>") { depth--; if (depth === 0 && cur) { tables.push(cur); cur = null; } continue; }
      const rawStyle = attr(t, /<w:pStyle w:val="([^"]+)"/) || "Normal";
      const st = smap.get(rawStyle);
      const sdts = [];
      for (const s of t.matchAll(/<w:sdt>([\s\S]*?)<\/w:sdt>/g)) {
        sdts.push({ tag: attr(s[1], /<w:tag w:val="([^"]*)"/), alias: attr(s[1], /<w:alias w:val="([^"]*)"/), text: textOf(s[1].replace(/<w:sdtPr>[\s\S]*?<\/w:sdtPr>/, "")) });
      }
      const p = {
        i: paras.length, rawStyle, style: st ? st.id : rawStyle, binding: !!(st && st.binding), known: !!st,
        text: textOf(t), inTable: depth > 0,
        bookmarks: [...t.matchAll(/<w:bookmarkStart[^>]*w:name="([^"]+)"/g)].map((x) => x[1]).filter((b) => !IGNORE_BM.test(b)),
        sdts, bmBeforePPr: /^<w:p[^>]*>\s*<w:bookmarkStart[^>]*\/>\s*<w:pPr>/.test(t),
        plainText: textOf(t.replace(/<w:sdt>[\s\S]*?<\/w:sdt>/g, "")),
      };
      paras.push(p);
    }
    // table rows (for control-table and appendix detection)
    for (const tb of tables) tb.paras = paras.slice(tb.start).filter((p) => p.inTable);
    const tblXml = [...body.matchAll(/<w:tbl>[\s\S]*?<\/w:tbl>/g)].map((x) => x[0]);
    const tablesRows = tblXml.map((tx) => [...tx.matchAll(/<w:tr[\s>][\s\S]*?<\/w:tr>/g)].map((r) => [...r[0].matchAll(/<w:tc>[\s\S]*?<\/w:tc>/g)].map((c) => textOf(c[0]))));
    return { paras, tablesRows };
  }

  function parseProps(xml) {
    const out = {};
    if (!xml) return out;
    for (const m of xml.matchAll(/<(?:\w+:)?property[^>]*name="([^"]+)"[^>]*>\s*<vt:\w+>([^<]*)<\/vt:\w+>|<(?:\w+:)?property[^>]*name="([^"]+)"[^>]*>\s*<vt:\w+\/>/g)) {
      if (m[1]) out[dec(m[1])] = norm(m[2]); else out[dec(m[3])] = "";
    }
    return out;
  }
  const coreVal = (xml, tag) => { const m = (xml || "").match(new RegExp(`<${tag}(?:\\s[^>]*)?>([^<]*)</${tag}>`)); return m ? norm(m[1]) : ""; };

  const LABELS = {
    "document number": "ODS.DocumentId", "title": "ODS.Title", "document type": "ODS.DocumentType", "document type and level": "ODS.DocumentType",
    "level": "ODS.Level", "revision": "ODS.Revision", "status": "ODS.Status", "document status": "ODS.Status", "issue date": "ODS.IssueDate",
    "effective date": "ODS.EffectiveDate", "parent": "ODS.Parent", "parent document": "ODS.Parent", "author": "ODS.Author",
    "reviewers": "ODS.Reviewer", "reviewer": "ODS.Reviewer", "endorser": "ODS.Endorser", "approver": "ODS.Approver",
    "approver / owner": "ODS.Approver", "document owner": "ODS.DocumentOwner", "process owner": "ODS.ProcessOwner", "custodian": "ODS.Custodian",
    "primary function": "ODS.PrimaryFunction", "framework": "ODS.Framework", "title oms tags": "ODS.TitleOMSTags",
    "classification": "ODS.Classification", "applies to": "ODS.Applicability", "applicability": "ODS.Applicability",
    "review interval": "ODS.ReviewInterval", "role register": "ODS.RoleRegister",
  };

  // ---------- the audit ----------
  async function auditDocx(bytes, ctx) {
    const P = ctx.protocol; const smap = ctx._smap || (ctx._smap = styleMap(P));
    const expSet = ctx._exp || (ctx._exp = new Set(P.expectations.map((e) => e.id)));
    const findings = []; const facts = {};
    const add = (rule, severity, fix, msg, where) => findings.push({ rule, severity, fix, msg, where: where || "" });
    const fileName = ctx.fileName || "";

    let zip;
    try { zip = await JSZip.loadAsync(bytes); } catch (e) { add("G15", "error", "manual", `Not a readable Word file: ${e.message}`); return finish(); }
    const read = async (n) => (zip.file(n) ? zip.file(n).async("string") : null);
    const docXml = await read("word/document.xml");
    if (!docXml) { add("G15", "error", "manual", "word/document.xml missing"); return finish(); }

    // G15 well-formed parts
    for (const n of Object.keys(zip.files)) {
      if (!/\.(xml|rels)$/.test(n)) continue;
      const err = wellFormed(await read(n));
      if (err) add("G15", "error", "manual", `XML not well-formed in ${n}: ${err}`);
    }

    const { paras, tablesRows } = parseDocument(docXml, smap);
    const props = parseProps(await read("docProps/custom.xml"));
    const core = await read("docProps/core.xml"); const app = await read("docProps/app.xml");

    // Meta controls
    const meta = {};
    for (const p of paras) for (const s of p.sdts) if (s.tag && s.tag.startsWith("ODS.Meta.")) (meta[s.tag.slice(9)] ||= []).push(s.text);
    // plain-text control table (LITE) — first 2-column table rows whose label is known
    const plain = {};
    for (const rows of tablesRows) for (const r of rows) {
      if (r.length < 2) continue;
      const k = LABELS[r[0].toLowerCase().replace(/\s+/g, " ").trim()];
      if (k && !(k in plain) && r[1]) plain[k] = r[1];
    }
    for (const rows of tablesRows) for (let i = 0; i + 1 < rows.length; i++) {
      const keys = rows[i].map((c) => LABELS[c.toLowerCase().replace(/\s+/g, " ").trim()]);
      if (keys.length > 1 && keys.every(Boolean) && rows[i + 1].length === keys.length)
        keys.forEach((k, j) => { if (!(k in plain) || Object.values(LABELS).includes(plain[k]) || LABELS[(plain[k] || "").toLowerCase()]) plain[k] = rows[i + 1][j]; });
    }
    for (const k of Object.keys(plain)) if (LABELS[plain[k].toLowerCase()]) delete plain[k];
    const propNames = P.properties.map((x) => x.name);
    const value = (name) => {
      const pd = P.properties.find((x) => x.name === name);
      for (const t of pd.meta) if (meta[t] && meta[t][0]) return metaToProp(name, meta[t][0]);
      if (props[name]) return props[name];
      if (plain[name]) return metaToProp(name, plain[name]);
      return derived[name] || "";
    };
    const derived = {}; // values Fix can work out from the document itself
    const isDerived = (name) => !!derived[name] && !props[name] && !pdMeta(name) && !plain[name];
    function pdMeta(name) { const pd = P.properties.find((x) => x.name === name); return pd.meta.some((t) => meta[t] && meta[t][0]); }
    function metaToProp(name, v) {
      v = norm(v);
      if (name === "ODS.Revision") return v.split(/\s+[—(-]/)[0].split(" ")[0];
      if (name === "ODS.DocumentType") return v.replace(/\s*[(/].*$/, "").trim();
      if (name === "ODS.Level") return v.replace(/^Level\s+/i, "");
      return v;
    }
    const metaLevel = (meta.DocumentType || [])[0]?.match(/Level\s+(\w+)/)?.[1];
    { const tp = paras.find((p) => p.style === "Title"); if (tp) { derived["ODS.Title"] = tp.text;
        const nx = paras[tp.i + 1]; if (nx && nx.style === "ODSTagLine") derived["ODS.TitleOMSTags"] = (nx.sdts[0]?.text || nx.text.replace(/^OMS\s*/, "")).trim(); }
      const fid = (props["ODS.DocumentId"] || (meta.DocumentID || [])[0] || plain["ODS.DocumentId"] || ctx.fileName || "").match(/ACE-[A-Z]{3}-([A-Z]{3})-\d{3}/);
      if (fid && P.types[fid[1]]) { derived["ODS.DocumentType"] = P.types[fid[1]].name; if (P.types[fid[1]].level) derived["ODS.Level"] = String(P.types[fid[1]].level); }
      for (const [k, v] of Object.entries(P.defaults || {})) derived[k] = v; }

    // --- identity
    const fnId = fileName.match(/^(ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?)/)?.[1];
    const docId = value("ODS.DocumentId") || fnId || "";
    facts.docId = docId; facts.title = value("ODS.Title"); facts.revision = value("ODS.Revision"); facts.status = value("ODS.Status");
    facts.framework = value("ODS.Framework");
    const legacy = P.framework.legacy.some((l) => facts.framework === l) || /Rev 03\b/.test(facts.framework);
    facts.legacy = legacy;
    const sev2 = (s) => (legacy ? "warning" : s); // rules introduced in protocol 2.0
    const nMeta = Object.keys(meta).length;
    const tagCCs = paras.flatMap((p) => p.sdts.filter((s) => s.tag && s.tag.startsWith("ODS.OMSTags@")));
    const plainTagLines = paras.filter((p) => p.style === "ODSTagLine" && !p.sdts.some((s) => s.tag?.startsWith("ODS.OMSTags@")) && /^OMS\b/.test(p.text));
    facts.format = nMeta >= 5 && tagCCs.length && !plainTagLines.length ? "STRICT" : plainTagLines.length && !tagCCs.length ? "LITE" : nMeta || tagCCs.length ? "MIXED" : "LITE";

    // --- G1 number and file name
    const idm = docId.match(new RegExp(P.numbering.docid));
    if (!docId) add("G1", "error", "manual", "No document number found (property, control table or file name)");
    else if (!idm) add("G1", "error", "manual", `Document number '${docId}' does not match ACE-SSS-TTT-NNN[-LLL]`);
    else {
      if (!P.systems[idm[1]]) add("G1", "error", "manual", `Unknown system code ${idm[1]}`);
      if (!P.types[idm[2]]) add("G1", "error", "manual", `Unknown type code ${idm[2]}`);
      if (idm[4] && !P.sites[idm[4]]) add("G1", "error", "manual", `Unknown site code ${idm[4]}`);
      facts.system = idm[1]; facts.type = idm[2];
    }
    if (fileName && docId) {
      const fm = fileName.match(new RegExp(P.numbering.file));
      if (!fm || fm[1] !== docId) add("G1", "warning", "auto", `File name does not follow ${docId}_Title_RevNN.docx`, fileName);
      else if (facts.revision && fm[2] !== facts.revision) add("G1", "warning", "auto", `File name revision Rev${fm[2]} differs from document revision ${facts.revision}`);
    }

    // --- G2 revision / status
    const rv = facts.revision, st = facts.status;
    if (rv && st) {
      const isDraftRev = new RegExp(P.revision.draft).test(rv), isAppRev = new RegExp(P.revision.approved).test(rv);
      if (!isDraftRev && !isAppRev) add("G2", "error", "manual", `Revision '${rv}' is neither a letter nor two digits`);
      else if (isDraftRev && !P.revision.draft_status.includes(st)) add("G2", "error", "manual", `Draft revision ${rv} with status ${st}`);
      else if (isAppRev && !P.revision.approved_status.includes(st)) add("G2", "error", "manual", `Approved revision ${rv} with status ${st}`);
      if (st === "Approved") for (const d of ["ODS.IssueDate", "ODS.EffectiveDate"]) if (!value(d)) add("G2", "error", "manual", `Approved issue without ${d.slice(4)}`);
    }
    if (ctx.folder === "finals" && st && st !== "Approved") add("G2", "warning", "manual", `finals/ holds a ${st} document; move it to drafts/`);

    // --- G3 properties
    const approved = P.revision.approved_status.includes(st);
    for (const pd of P.properties) {
      const present = pd.name in props;
      const v = value(pd.name);
      if (!present) {
        if (pd.since === "2.0") add("G3", sev2("error"), "auto", `Property ${pd.name} missing (added in template v5)`);
        else add("G3", "error", "auto", `Property ${pd.name} missing`);
      } else if (!props[pd.name] && v) add("G3", "error", "auto", isDerived(pd.name) ? `Property ${pd.name} empty; Fix will set '${v}'` : `Property ${pd.name} empty; value available in the document`);
      if (!approved && v && /^\[.*\]$/.test(v.trim())) { add("G3", "warning", "manual", `${pd.name} still holds the placeholder ${v.trim()}: to be completed before approval`); continue; }
      if (!v && !approved && (P.people.fields.includes(pd.name) || /Date$/.test(pd.name))) { add("G3", "warning", "manual", `${pd.name} left blank in this draft: to be completed before approval`); continue; }
      if (!v && (pd.required === "always" || (pd.required === "approved" && approved))) {
        if (pd.since === "2.0") { if (pd.name === "ODS.Parent") continue; add("G3", sev2("error"), "manual", `${pd.name} has no value`); }
        else add("G3", "error", "manual", `${pd.name} has no value anywhere in the document`);
      }
    }
    for (const n of Object.keys(props)) if (n.startsWith("ODS.") && !propNames.includes(n)) add("G3", "warning", "manual", `Unknown property ${n}`);
    const level = value("ODS.Level"), tname = value("ODS.DocumentType");
    if (level && !/^\d$/.test(level)) add("G3", "error", facts.type && P.types[facts.type] ? "auto" : "manual", `ODS.Level '${level}' is not a number 1–5`);
    else if (level && facts.type && P.types[facts.type]) {
      const T = P.types[facts.type]; const ok = [T.level, legacy ? T.legacy_level : null].filter((x) => x != null).map(String);
      if (T.level != null && !ok.includes(level)) add("G3", "error", "auto", `Level ${level} does not match type ${facts.type} (expected ${ok.join(" or ")})`);
    }
    if (metaLevel && level && metaLevel !== level && /^\d$/.test(metaLevel)) add("G4", "error", "auto", `Control table level ${metaLevel} ≠ property ${level}`);
    if (tname && facts.type && P.types[facts.type] && tname !== P.types[facts.type].name) add("G3", "error", "auto", `ODS.DocumentType '${tname}' should be '${P.types[facts.type].name}'`);
    if (st && !P.statuses.includes(st)) add("G3", "error", "manual", `Status '${st}' not allowed`);
    const cls = value("ODS.Classification"); if (cls && !P.classifications.includes(cls)) add("G3", "error", "auto", `Classification '${cls}' not one of ${P.classifications.join(", ")}`);
    const fw = facts.framework;
    if (fw && fw !== P.framework.current && !P.framework.legacy.includes(fw)) add("G3", "error", "auto", `Framework text '${fw}' is not the fixed wording`);
    const fn = value("ODS.PrimaryFunction"); if (fn && !P.functions.includes(fn)) add("G3", "warning", "manual", `Primary function '${fn}' is not one of the 13 ACE functions`);
    for (const d of ["ODS.IssueDate", "ODS.EffectiveDate"]) { const v = value(d); if (v && !DATE_RE.test(v)) add("G3", "error", "manual", `${d} '${v}' not in '1 January 2026' format`); }
    const ttags = value("ODS.TitleOMSTags");
    for (const t of ttags.split(",").map((x) => x.trim()).filter(Boolean)) if (!expSet.has(t)) add("G3", "error", "manual", `Title tag ${t} is not an OMS expectation`);

    // --- G4 agreement (control table is master)
    for (const pd of P.properties) for (const t of pd.meta) for (const mv of meta[t] || []) {
      const want = metaToProp(pd.name, mv), have = props[pd.name];
      if (have && want && want !== have && !(pd.name === "ODS.Revision" && t === "CoverRevision" && mv.startsWith(have)))
        add("G4", "error", "auto", `Control table ${t} '${want}' ≠ property ${pd.name} '${have}'`);
    }
    if (facts.format !== "LITE") {
      const missingMeta = P.properties.filter((pd) => !pd.meta.some((t) => meta[t])).map((pd) => pd.meta[0]);
      const old = missingMeta.filter((t) => !["Level", "Parent", "ProcessOwner", "RoleRegister"].includes(t));
      if (old.length) add("G4", legacy ? "warning" : "error", "auto", `Control table values not in Meta controls: ${old.join(", ")}`);
      const v2 = missingMeta.filter((t) => ["Level", "Parent", "ProcessOwner", "RoleRegister"].includes(t));
      if (v2.length) add("G4", sev2("error"), "auto", `Control table lacks v5 rows: ${v2.join(", ")}`);
    }
    const bi = P.builtin_properties.core;
    const expect = { "dc:title": value("ODS.Title"), "dc:subject": docId, "cp:keywords": ttags };
    for (const k of P.builtin_properties.checked_as_error) if (expect[k] && coreVal(core, k) !== expect[k])
      add("G4", sev2("error"), "auto", `Word built-in ${k.split(":")[1]} is '${coreVal(core, k)}', should be '${expect[k]}'`);
    void bi;
    const hf = (await Promise.all(Object.keys(zip.files).filter((n) => /^word\/(header|footer)\d*\.xml$/.test(n)).map(read))).map(textOf).join(" ");
    if (docId && !hf.includes(docId)) add("G4", "warning", "auto", "Header/footer does not show the document number");
    if (rv && !new RegExp(`(Rev|REV|Revision|DRAFT)\\s*${rv}\\b`).test(hf)) add("G4", "warning", "auto", `Header/footer does not show revision ${rv}`);

    // --- G5 title
    const titleP = paras.find((p) => p.style === "Title");
    if (!titleP) add("G5", "error", "manual", "No paragraph in the Title style");
    else {
      if (!titleP.bookmarks.includes("doc_title")) add("G5", "error", "auto", "Title paragraph has no doc_title bookmark");
      const tcc = paras.flatMap((p) => p.sdts).find((s) => s.tag === "ODS.OMSTags@doc_title");
      if (!tcc) add("G5", "error", "auto", "No title tag control ODS.OMSTags@doc_title");
      else if (ttags && tcc.text.replace(/\s/g, "") !== ttags.replace(/\s/g, "")) add("G5", "error", "auto", `Title tags '${tcc.text}' ≠ ODS.TitleOMSTags '${ttags}'`);
    }

    // --- G6 headings and tags
    const allBm = new Set(paras.flatMap((p) => p.bookmarks));
    const used = new Map(); let headings = 0, maxTagWarn = 0;
    const H = new Set(P.tags.headings_requiring_tags);
    for (let k = 0; k < paras.length; k++) {
      const p = paras[k];
      if (!H.has(p.style) || !p.text || p.inTable) continue;
      headings++;
      const nx = paras[k + 1];
      const tl = nx && nx.style === "ODSTagLine" ? nx : null;
      const cc = tl && tl.sdts.find((s) => s.tag?.startsWith("ODS.OMSTags@"));
      if (!tl) {
        const front = P.front_sections && P.front_sections[p.text];
        if (front) add("G6", "error", "auto", `Standard heading has no tag line; Fix adds OMS ${front}`, p.text);
        else add("G6", facts.type === "MAN" ? "warning" : "error", "manual", "Heading has no tag line", p.text.slice(0, 60));
        continue; }
      if (!cc) {
        if (/^OMS\b/.test(tl.text)) add("G6", "error", "auto", "Tag line is plain text (LITE)", p.text.slice(0, 60));
        else add("G6", "error", "manual", "Tag line has no tags", p.text.slice(0, 60));
      } else {
        const target = cc.tag.split("@")[1];
        if (!p.bookmarks.length) add("G6", "error", "auto", "Heading has no bookmark", p.text.slice(0, 60));
        else if (!p.bookmarks.includes(target)) add("G6", "error", "auto", `Tag control points to '${target}', heading bookmark is '${p.bookmarks[0]}'`, p.text.slice(0, 60));
        if (used.has(target)) add("G6", "error", "auto", `Duplicate tag control for ${target}`); used.set(target, 1);
      }
      const tags = (cc ? cc.text : tl.text.replace(/^OMS\s*/, "")).split(",").map((x) => x.trim()).filter(Boolean);
      for (const t of tags) if (!expSet.has(t)) add("G6", "error", "manual", `Tag '${t}' is not an OMS expectation`, p.text.slice(0, 60));
      if (!tags.length) add("G6", "error", "manual", "Empty tag line", p.text.slice(0, 60));
      if (tags.length > P.tags.max_per_section) maxTagWarn++;
    }
    if (maxTagWarn) add("G6", "warning", "manual", `${maxTagWarn} section(s) carry more than ${P.tags.max_per_section} tags`);
    for (const s of tagCCs) { const t = s.tag.split("@")[1]; if (t !== "doc_title" && !allBm.has(t)) add("G6", "error", "manual", `Orphan tag control: bookmark '${t}' does not exist`); }
    facts.headings = headings; facts.tagControls = tagCCs.length; facts.bookmarks = [...allBm];

    // --- G7 shall
    let shallBad = 0, shallCell = 0;
    for (const p of paras) {
      if (!/\bshall\b/i.test(p.text.replace(/[“"‘']shall(?: not)?[”"’']/gi, ""))) continue;
      if (p.inTable) { shallCell++; continue; }
      if (!p.binding) { shallBad++; if (shallBad <= 5) add("G7", "error", "manual", `'shall' in ${p.rawStyle} paragraph`, p.text.slice(0, 70)); }
    }
    if (shallBad > 5) add("G7", "error", "manual", `…and ${shallBad - 5} more 'shall' paragraphs in non-binding styles`);
    if (shallCell) add("G7", "error", "manual", `'shall' in ${shallCell} table cell(s)`);
    if (facts.type === "GDL" && paras.some((p) => p.binding)) add("G7", "error", "manual", "Guideline contains binding styles");
    facts.binding = paras.filter((p) => p.binding).length;
    const unknownStyles = [...new Set(paras.filter((p) => !p.known && /^(ODS|OMS|ONE)/.test(p.rawStyle)).map((p) => p.rawStyle))];
    if (unknownStyles.length) add("G7", "warning", "manual", `Styles not in the catalogue: ${unknownStyles.join(", ")}`);

    // --- G8 people
    for (const f of P.people.fields) {
      const v = value(f); if (!v) continue;
      for (const person of v.split(/;\s*/).map((x) => x.trim()).filter(Boolean)) {
        if (P.people.allowed_values.some((a) => person === a || person.startsWith(a))) continue;
        if (/^\[.*\]$/.test(person)) continue;   // draft placeholder, reported under G3
        const [nm, title] = person.split(" — ").map((x) => (x || "").trim());
        if (ctx.people.left && ctx.people.left.has(nm)) { add("G8", "warning", "manual", `${f.slice(4)}: ${nm} left ACE${ctx.people.left.get(nm) ? " on " + ctx.people.left.get(nm) : ""}; name the current ${title || "role holder"} at the next revision`); continue; }
        if (!ctx.people.has(nm)) add("G8", "error", "manual", `${f.slice(4)}: '${person}' not in the organisation register`);
        else if (ctx.people.get(nm) !== title && ctx.people.titles && ctx.people.titles.has(title) && !title.startsWith(ctx.people.get(nm) + " (")) add("G8", "warning", "manual", `${f.slice(4)}: ${nm} is now ${ctx.people.get(nm)}; name the current ${title} at the next revision`);
        else if (ctx.people.get(nm) !== title) {
          const reg = ctx.people.get(nm);
          if (title.startsWith(reg + " (")) add("G8", "warning", "auto", `${f.slice(4)}: role qualifier after the title in '${person}'`);
          else add("G8", "error", "auto", `${f.slice(4)}: '${person}' — register title is '${reg}'`);
        }
      }
    }

    // --- G9 controls
    const cre = new RegExp(P.control_id.pattern, "g");
    const ccIds = [], plainIds = [];
    for (const p of paras) {
      for (const s of p.sdts) if (s.tag?.startsWith("ODS.Control@")) ccIds.push(s.tag.split("@")[1]);
      if (p.style !== "ODS.RiskControl") continue;
      const inCC = p.sdts.filter((s) => s.tag?.startsWith("ODS.Control@"));
      const plainHere = [...p.plainText.matchAll(cre)].map((m) => m[0]);
      if (plainHere.length) { plainIds.push(...plainHere); add("G9", "error", "auto", `Control ID(s) ${plainHere.join(", ")} as plain text`, p.text.slice(0, 60)); }
      else if (!inCC.length) add("G9", sev2("error"), "manual", "RiskControl paragraph without a Control ID", p.text.slice(0, 60));
    }
    for (const id of [...ccIds, ...plainIds]) { const sys = id.split("-")[1]; if (!P.systems[sys]) add("G9", "error", "manual", `Control ID ${id}: unknown system ${sys}`); }
    const dupLocal = ccIds.filter((x, i) => ccIds.indexOf(x) !== i);
    if (dupLocal.length) add("G9", "warning", "manual", `Control ID used in more than one paragraph: ${[...new Set(dupLocal)].join(", ")}`);
    const rcTexts = paras.filter((p) => p.style === "ODS.RiskControl").map((p) => p.plainText.replace(cre, "").replace(/Control ID:?/gi, "").trim());
    const sameText = rcTexts.length - new Set(rcTexts).size;
    if (sameText > 1) add("G9", "error", "manual", `${sameText + 1} control paragraphs have identical text — placeholders, not real controls`);
    const appendix = tablesRows.find((r) => r[0] && /^control id$/i.test(r[0][0]));
    if (appendix) { const full = new RegExp("^" + P.control_id.pattern.replace("(?<![A-Za-z0-9-])", "") + "$");
      const bad = appendix.slice(1).map((r) => r[0]).filter((x) => x && !full.test(x));
      if (bad.length) add("G9", "error", "manual", `Malformed Control IDs in the controls table: ${bad.slice(0, 3).join(", ")}${bad.length > 3 ? "…" : ""}`); }
    if (appendix) {
      const tab = new Set(appendix.slice(1).map((r) => r[0]).filter(Boolean)), body = new Set([...ccIds, ...plainIds]);
      const onlyT = [...tab].filter((x) => !body.has(x)), onlyB = [...body].filter((x) => !tab.has(x));
      if (onlyT.length || onlyB.length) add("G9", "warning", "manual", `Controls appendix and body differ (appendix only: ${onlyT.join(", ") || "-"}; body only: ${onlyB.join(", ") || "-"})`);
    }
    facts.controls = [...new Set([...ccIds, ...plainIds])];

    // --- G10 parent (existence checked in auditSet)
    const parent = value("ODS.Parent");
    facts.parent = parent;
    const lvl1 = facts.type && P.types[facts.type] && P.types[facts.type].level === 1;
    if (!parent && !lvl1) add("G10", sev2("error"), "manual", "ODS.Parent not set");

    // --- G11 references (resolved in auditSet)
    const rre = new RegExp(P.numbering.reference, "g");
    const all = paras.map((p) => p.text).join(" \n ");
    facts.declaredPlanned = tablesRows.filter((r) => r[0] && r[0].some((c) => /^status$/i.test(c)))
      .flatMap((r) => r.slice(1).filter((row) => row.some((c) => /^planned/i.test(c))).map((row) => (row[0].match(/ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?/) || [])[0]).filter(Boolean));
    facts.references = [...new Set([...all.matchAll(rre)].map((m) => m[0].split(/\s*§/)[0]))].filter((x) => x !== docId);

    // --- G13 implementing processes table
    if (facts.type && P.types[facts.type]?.implementing_table) {
      const has = tablesRows.some((r) => r[0] && r[0].some((c) => /^(number|process|process \/ procedure)$/i.test(c)) && r[0].some((c) => /^status$/i.test(c)));
      if (!has) add("G13", "warning", "manual", "No implementing processes and procedures table");
    }

    // --- G14 media
    const rels = Object.keys(zip.files).filter((n) => n.endsWith(".rels"));
    const relTxt = (await Promise.all(rels.map(read))).join(" ");
    for (const n of Object.keys(zip.files).filter((n) => n.startsWith("word/media/"))) if (!relTxt.includes(n.replace("word/", ""))) add("G14", "warning", "auto", `Unused media ${n}`);
    if (/TargetMode="External"[^>]*image|image[^>]*TargetMode="External"/.test(relTxt)) add("G14", "warning", "manual", "Linked (external) image");
    const size = bytes.byteLength || bytes.length || 0; facts.sizeKB = Math.round(size / 1024);
    if (size > P.limits.max_file_mb * 1048576) add("G14", "warning", "manual", `File is ${(size / 1048576).toFixed(1)} MB`);

    const split = tablesRows.filter((r) => r[0] && r[0].length >= 4 && r[0].filter((c) => c.length === 1).length >= 4).length;
    if (split) add("G15", "error", "manual", `${split} table(s) with the header split one letter per column (damaged table)`);
    // --- G15 order
    const bmOrder = paras.filter((p) => p.bmBeforePPr).length;
    if (bmOrder) add("G15", "warning", "auto", `${bmOrder} paragraph(s) have a bookmark before paragraph properties`);

    // --- G12 PRS (pair check needs the folder; flagged here)
    if (facts.type === "PRS") facts.needsPair = true;
    return finish();

    function finish() {
      const errors = findings.filter((f) => f.severity === "error");
      const outcome = !errors.length ? "PASS" : errors.every((f) => f.fix === "auto") ? "PASS_AFTER_FIX" : "FAIL";
      return { file: fileName, folder: ctx.folder || "", engine: ENGINE_VERSION, protocol: P.version, outcome, facts, findings,
               counts: { errors: errors.length, warnings: findings.filter((f) => f.severity === "warning").length } };
    }
  }


  // ---------- G12: process model file (semantic checks; schema shape is checked by ONE-PRS/1) ----------
  function auditProcess(obj, ctx) {
    const P = ctx.protocol, F = [];
    const add = (severity, fix, msg, where) => F.push({ rule: "G12", severity, fix, msg, where: where || "" });
    if (obj.schema !== "ONE-PRS/1") add("error", "manual", `schema is '${obj.schema}', expected ONE-PRS/1`);
    const lanes = new Set((obj.lanes || []).map((l) => l.id)), ids = (obj.steps || []).map((s) => s.id), idset = new Set(ids);
    if (idset.size !== ids.length) add("error", "manual", "Duplicate step ids");
    const exp = new Set(P.expectations.map((e) => e.id));
    for (const t of obj.oms_tags || []) if (!exp.has(t)) add("error", "manual", `Tag ${t} is not an OMS expectation`);
    const [nm, title] = (obj.owner || "").split(" — ");
    if (ctx.people && ctx.people.get(nm) !== title) add("error", "auto", `Owner '${obj.owner}' does not match the organisation register`);
    if (!P.functions.includes(obj.function)) add("error", "manual", `Function '${obj.function}' is not an ACE function`);
    if (!(obj.steps || []).some((s) => s.type === "start")) add("error", "manual", "No start event");
    if (!(obj.steps || []).some((s) => s.type === "end")) add("error", "manual", "No end event");
    for (const s of obj.steps || []) {
      if (!lanes.has(s.lane)) add("error", "manual", `Lane ${s.lane} not defined`, s.id);
      for (const n of [...(s.next || []), ...(s.branches || []).map((b) => b.to)]) if (!idset.has(n)) add("error", "manual", `Next step ${n} does not exist`, s.id);
      if (s.branches && s.branches.every((b) => b.p != null)) { const sum = s.branches.reduce((a, b) => a + b.p, 0); if (Math.abs(sum - 1) > 0.001) add("error", "manual", `Branch probabilities add up to ${sum}`, s.id); }
      for (const r of s.doc_refs || []) {
        const [d, bm] = r.split("#"); const bms = ctx.bookmarks && ctx.bookmarks.get(d);
        if (!bms) add(ctx.knownDocs && ctx.knownDocs.has(d) ? "warning" : "error", "manual", `doc_ref ${d} is not a published document`, s.id);
        else if (!bms.has(bm)) add("error", "manual", `Bookmark ${bm} not found in ${d}`, s.id);
      }
      for (const c of s.controls || []) if (ctx.controls && !ctx.controls.has(c)) add("error", "manual", `Control ${c} is not established by any document`, s.id);
      if (s.type === "task" && !/^[A-Z][a-z]+\s\S/.test(s.name || "")) add("warning", "manual", `Step name '${s.name}' is not verb–object`, s.id);
    }
    // every step reachable from start
    const seen = new Set(), stack = (obj.steps || []).filter((s) => s.type === "start").map((s) => s.id), byId = Object.fromEntries((obj.steps || []).map((s) => [s.id, s]));
    while (stack.length) { const k = stack.pop(); if (seen.has(k) || !byId[k]) continue; seen.add(k); stack.push(...(byId[k].next || []), ...(byId[k].branches || []).map((b) => b.to)); }
    const orphan = ids.filter((k) => !seen.has(k)); if (orphan.length) add("error", "manual", `Steps not reachable from start: ${orphan.join(", ")}`);
    return F;
  }

  // ---------- set-level audit ----------
  async function auditSet(files, ctx) {
    // files: [{name, folder, bytes}]
    const results = [];
    for (const f of files) {
      if (/^~\$|\.tmp$/i.test(f.name)) { results.push({ file: f.name, folder: f.folder, outcome: "PASS_AFTER_FIX", facts: {}, findings: [{ rule: "G16", severity: "error", fix: "auto", msg: "Lock or temporary file: delete it" }], counts: { errors: 1, warnings: 0 } }); continue; }
      if (!/\.docx$/i.test(f.name)) continue;
      results.push(await auditDocx(f.bytes, { ...ctx, fileName: f.name, folder: f.folder }));
    }
    const known = new Set([...Object.keys(ctx.protocol.document_register.planned), ...results.flatMap((r) => [r.facts.docId, ...(r.facts.declaredPlanned || [])]).filter(Boolean)]);
    const issued = new Set(results.map((r) => r.facts.docId).filter(Boolean));
    const owner = new Map();
    for (const r of results) {
      const add = (rule, severity, fix, msg) => r.findings.push({ rule, severity, fix, msg, where: "" });
      for (const c of r.facts.controls || []) {
        if (owner.has(c) && owner.get(c) !== r.facts.docId) add("G9", "error", "manual", `Control ID ${c} also used in ${owner.get(c)}`);
        else owner.set(c, r.facts.docId);
      }
      const par = (r.facts.parent || "").match(/ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?/g) || [];
      if (r.facts.parent && !/^not applicable/i.test(r.facts.parent)) {
        if (!par.length) add("G10", "error", "manual", `Parent '${r.facts.parent}' is not a document number`);
        for (const p of par) if (!known.has(p)) add("G10", "error", "manual", `Parent ${p} is not in the document register`);
      }
      const unknown = (r.facts.references || []).filter((x) => !known.has(x));
      if (unknown.length) add("G11", "warning", "manual", `References to unknown documents: ${unknown.join(", ")}`);
      const planned = (r.facts.references || []).filter((x) => known.has(x) && !issued.has(x));
      r.facts.plannedRefs = planned;
      if (r.facts.needsPair && !files.some((f) => f.name === `${r.facts.docId}.json`)) add("G12", "error", "manual", "Process model file (JSON) missing");
      const errors = r.findings.filter((f) => f.severity === "error");
      r.outcome = !errors.length ? "PASS" : errors.every((f) => f.fix === "auto") ? "PASS_AFTER_FIX" : "FAIL";
      r.counts = { errors: errors.length, warnings: r.findings.filter((f) => f.severity === "warning").length };
    }
    return { protocol: ctx.protocol.version, engine: ENGINE_VERSION, date: new Date().toISOString(), results };
  }

  return { auditDocx, auditSet, auditProcess, peopleFromCsv, parseCsv, ENGINE_VERSION };
});
