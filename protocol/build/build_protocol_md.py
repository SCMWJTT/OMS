"""Writes protocol/ONE_Protocol_v1.md (the human version) from one-protocol.json, so the two never disagree.
Run from the repo root:  python3 protocol/build/build_protocol_md.py"""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = json.load(open(os.path.join(ROOT, "protocol", "one-protocol.json"), encoding="utf-8"))
L = []
w = L.append
def table(head, rows):
    w("| " + " | ".join(head) + " |"); w("|" + "---|" * len(head))
    for r in rows: w("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")
    w("")

w(f"# ONE Protocol v{P['version']}")
w(f"\n**The single rule set for ACE documents in ONE.** Issued {P['issued']}. Governed by {P['governed_by']}; this file becomes its Rev 02 content.")
w("The machine version is `one-protocol.json`. Every ONE tool — Studio (Auditor + Editor), Portal gateway and Word ribbon — reads that file and runs the same checker (`engine/one-audit.js`). This page is generated from it.\n")

w("## 1. The idea in one paragraph\n")
w("An author writes in Word. If the document follows this protocol, ONE can read it without anyone re-keying anything: it knows the document's identity, its place in the hierarchy, which OMS expectations each section serves, which sentences are binding, which controls it establishes and who is accountable. The protocol was written **from** the existing documents: everything already in `finals/` passes, or passes after the automatic Fix.\n")

w("## 2. Two formats: STRICT and LITE\n")
table(["Format", "What it is"], [[k, v] for k, v in P["formats"].items()])
w("ONE publishes STRICT only. The ONE Editor **Fix** button converts LITE to STRICT without touching the text.\n")
w("**Outcome of a check:**\n")
table(["Outcome", "Meaning"], [[k.replace("_", " "), v] for k, v in P["outcomes"].items()])
w(f"**Legacy documents.** {P['framework']['legacy_rule']}\n")

w("## 3. Identity\n")
w(f"- **Number:** `ACE-SSS-TTT-NNN[-LLL]` (SSS system, TTT type, NNN sequence, LLL site). {P['numbering']['eng_blocks']}.")
w("- **File name:** `<number>_Title_Words_Rev01.docx` (or `_RevA`).")
w(f"- **Revision:** letters for drafts (status {', '.join(P['revision']['draft_status'])}); two digits for issues (status {', '.join(P['revision']['approved_status'])}).")
w(f"- **Framework text (fixed):** `{P['framework']['current']}`\n")
w("### 3.1 Document types\n")
table(["Code", "Type", "Level", "Layer"], [[k, v["name"], v["level"] or "n/a", v["layer"]] for k, v in P["types"].items()])
w("### 3.2 System codes\n")
table(["Code", "System", "Owner", "Elements"], [[k, v["name"], v["owner"], ", ".join(map(str, v["elements"]))] for k, v in P["systems"].items()])
w("### 3.3 Site codes\n")
table(["Code", "Site"], list(P["sites"].items()))
w("### 3.4 Functions\n")
w(", ".join(P["functions"]) + ".\n")

w("## 4. Metadata — five places, one master\n")
w("The **document control table** (`ODS.Meta.*` content controls) is the master. The cover, header/footer, the 23 custom properties and Word's built-in properties must agree with it. Fix copies the table to the other four.\n")
w("### 4.1 The 23 custom properties\n")
table(["Property", "Control table tag(s)", "Format", "Required", "Since"],
      [[p["name"], ", ".join("ODS.Meta." + t for t in p["meta"]), p["format"], p["required"], p["since"]] for p in P["properties"]])
w("### 4.2 Word built-in properties (File › Info)\n")
table(["Field", "Value"], [[k, v] for k, v in {**P["builtin_properties"]["core"], **P["builtin_properties"]["app"]}.items()])
w(f"### 4.3 People\nWritten `{P['people']['format']}` exactly as in `{P['people']['source']}`, several separated by `{P['people']['separator']}`. Allowed non-person values: {', '.join(P['people']['allowed_values'])}. A role in brackets after an exact title (e.g. '(Technical Authority)') is accepted with a warning.\n")

w("## 5. Headings, bookmarks and OMS tags\n")
w(f"- The Title paragraph carries the bookmark `{P['bookmarks']['title']}`; its tag line holds `ODS.OMSTags@doc_title`.")
w(f"- Every Heading 1 and Heading 2 carries a bookmark and is followed by an **ODS Tag Line** holding the control `ODS.OMSTags@<that bookmark>`.")
w(f"- New headings use `{P['bookmarks']['recommended_heading']}`. {P['bookmarks']['rule']}")
w(f"- Tags: {P['tags']['min_per_section']} to {P['tags']['max_per_section']} per section, primary first, scope {P['tags']['scope']}.")
w("- Standard front headings and their tags: " + "; ".join(f"{k} → {v}" for k, v in P["front_sections"].items()) + ".\n")
w("### 5.1 The 54 OMS expectations (valid tags)\n")
for e in P["elements"]:
    w(f"**{e['id']} {e['title']}** — " + "; ".join(f"{x['id']} {x['title']}" for x in P["expectations"] if x["element"] == e["id"]) + "\n")

w("## 6. Styles — what ONE does with each paragraph\n")
w("Variants without the dot (e.g. `ODSRequirement`) are treated as the same style. **'Shall' is allowed only in the binding styles** (quoted mentions such as “shall” are ignored).\n")
table(["Style ID", "Accepted variants", "Binding", "ONE meaning"], [[s["id"], ", ".join(s["aliases"]) or "–", "yes" if s["binding"] else "", s["one"]] for s in P["styles"]])

w("## 7. Content controls\n")
table(["Tag", "Alias", "Use"], [[c["tag"], c["alias"], c["use"]] for c in P["content_controls"]])
w(f"**Control IDs:** `C-<SYS>-<NNN>`, unique across the repository, allocated in blocks by the OMS Manager and recorded in {P['control_id']['allocation_register']}. In a RiskControl paragraph each ID sits inside `ODS.Control@<ID>`.\n")
w(f"**References:** ACE documents are recognised in text by the pattern `ACE-SSS-TTT-NNN[-LLL] [§x.y]`.\n")

w("## 8. Gateway rules\n")
w("Errors block publication; warnings are listed. 'auto' means ONE Fix can correct it without a person.\n")
table(["Rule", "Check", "Severity", "Fix", "What is checked"], [[r["id"], r["title"], r["severity"], r["fix"], "; ".join(r["checks"])] for r in P["rules"]])

w("## 9. Process files (PRS)\n")
w(f"A Process is a Word description plus a model file `ACE-SSS-PRS-NNN.json` (schema ONE-PRS/1, `{P['process_schema']}`). Defined in ACE-BPM-PRA-002. Worked example: `schemas/example/ACE-MOC-PRS-001.json`.\n")

w("## 10. Data spine registers\n")
for k, r in P["registers"].items():
    w(f"**{r['title']}** (`{r['file']}`, key `{r['key']}`, owner {r['owner']}, defined in {r['defined_in']})  ")
    w(", ".join(f"`{c['name']}`" + (f" → {c['link']}" if c.get("link") else "") for c in r["columns"]) + "\n")

w("## 11. Pack contents\n")
table(["File", "Purpose"], [
    ["one-protocol.json", "the rule set every tool reads"], ["engine/one-audit.js", "the single checker (Node, Electron, browser)"],
    ["engine/cli.js", "runs the checker over the repository; writes reports/audit.md and audit.json"],
    ["schemas/one-prs-1.schema.json", "process file schema"], ["registers/*.csv", "empty register templates"],
    ["samples/ACE-DOC-PRA-999_…Golden_Sample…docx", "test document that passes every rule"],
    ["../templates/ONE_ACE_Master_Template_v5.dotx", "template v5"], ["build/", "scripts that regenerate the JSON and this page"]])
open(os.path.join(ROOT, "protocol", "ONE_Protocol_v1.md"), "w", encoding="utf-8").write("\n".join(L))
print("wrote ONE_Protocol_v1.md", len(L), "lines")
