#!/usr/bin/env node
/* ONE Auditor command line (used by the GitHub Action and for testing).
 * node cli.js <repo-root> [folders...]   -> writes <repo-root>/protocol/reports/audit.json and audit.md */
const fs = require("fs"), path = require("path");
const A = require("./one-audit.js");
(async () => {
  const root = path.resolve(process.argv[2] || ".");
  const folders = process.argv.slice(3).length ? process.argv.slice(3) : ["finals", "manuals", "drafts", "samples/lite", "protocol/samples"];
  const protocol = JSON.parse(fs.readFileSync(path.join(root, "protocol/one-protocol.json"), "utf8"));
  const people = A.peopleFromCsv(fs.readFileSync(path.join(root, protocol.people.source), "utf8"), protocol);
  const files = [];
  for (const fo of folders) {
    const dir = path.join(root, fo); if (!fs.existsSync(dir)) continue;
    for (const n of fs.readdirSync(dir).sort()) if (/\.(docx|dotx|json)$/i.test(n) || /^~\$/.test(n))
      files.push({ name: n, folder: fo, bytes: fs.readFileSync(path.join(dir, n)) });
  }
  const rep = await A.auditSet(files.map((f) => (f.name.endsWith(".dotx") ? { ...f, name: f.name } : f)), { protocol, people });
  // .dotx templates are audited too (same rules, reported separately)
  for (const f of files.filter((f) => /\.dotx$/i.test(f.name))) rep.results.push(await A.auditDocx(f.bytes, { protocol, people, fileName: f.name, folder: f.folder }));
  const out = path.join(root, "protocol/reports"); fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, "audit.json"), JSON.stringify(rep, null, 1));
  const L = [`# ONE Auditor report`, ``, `Protocol ${rep.protocol} · engine ${rep.engine} · ${rep.date.slice(0, 10)}`, ``];
  const tally = {}; for (const r of rep.results) tally[r.outcome] = (tally[r.outcome] || 0) + 1;
  L.push(`**${rep.results.length} files:** ` + Object.entries(tally).map(([k, v]) => `${k.replace(/_/g, " ")} ${v}`).join(" · "), ``);
  L.push(`| Folder | File | Format | Legacy | Outcome | Errors (auto/manual) | Warnings |`, `|---|---|---|---|---|---|---|`);
  for (const r of rep.results) {
    const e = r.findings.filter((f) => f.severity === "error");
    L.push(`| ${r.folder} | ${r.facts.docId || r.file} | ${r.facts.format || ""} | ${r.facts.legacy ? "yes" : ""} | ${r.outcome.replace(/_/g, " ")} | ${e.filter((f) => f.fix === "auto").length} / ${e.filter((f) => f.fix === "manual").length} | ${r.counts.warnings} |`);
  }
  L.push(``, `## Findings`);
  for (const r of rep.results) {
    if (!r.findings.length) continue;
    L.push(``, `### ${r.folder}/${r.file} — ${r.outcome.replace(/_/g, " ")}`);
    for (const f of r.findings) L.push(`- **${f.rule}** ${f.severity}${f.fix === "auto" ? " (auto-fix)" : ""}: ${f.msg}${f.where ? ` — _${f.where}_` : ""}`);
  }
  fs.writeFileSync(path.join(out, "audit.md"), L.join("\n"));
  console.log(Object.entries(tally).map(([k, v]) => `${k} ${v}`).join("  "));
})();
