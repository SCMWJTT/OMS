"""Pre-publication correction of the ACE Wave 1 files.
Single source of truth = the visible document-control content controls (ODS.Meta.*).
Everything hidden (custom and core properties) is rebuilt from them."""
import zipfile, re, glob, os, csv, html, datetime as dt
SRC = "/tmp/inc"; OUT = "/home/claude/audit/fixed_inc"; os.makedirs(OUT, exist_ok=True)
LOG = []
def log(f, area, before, after, why): LOG.append([f, area, before, after, why])
def T(x): return html.unescape(re.sub(r"<[^>]+>", "", x))
def esc(s): return html.escape(s, quote=False)

ROLES = ["Area Authority","Technical Authority","Technical Leadership Council","Permit Issuer","Performing Authority","Isolating Authority",
 "OMS Manager","Information Management Lead","Document Controller","Line Manager","Supervisor","System Owner","Element Owner","Contract Owner",
 "Process Safety Lead","Maintenance & Integrity Manager","Inspection Lead","Offshore Installation Manager","Plant Manager","Land Operations Manager",
 "Offshore Operations Manager","Manager, Technical Excellence","HSE Adviser","Incident Investigation Lead","Lead Auditor","Head of Internal Audit",
 "Emergency Response","Project Manager","Custodian","Approver","Reviewer","Author","Endorser"]
FIX_PEOPLE = {  # role-only or non-person control values -> named holders from the ACE org chart
 ("ACE-COW-STD-001","DocumentOwner"): "Sophia Hosany — VP Operations",
 ("ACE-COW-STD-001","Custodian"): "Adrian Rodriguez — Permit to Work Coordinator (Offshore)",
 ("ACE-MNT-STD-001","DocumentOwner"): "Sophia Hosany — VP Operations",
 ("ACE-MNT-STD-001","Custodian"): "Marc Gomes — Maintenance & Integrity Manager",
}
FRAMEWORK = "IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 03"

def sdt_blocks(d): return list(re.finditer(r"<w:sdt>.*?</w:sdt>", d, re.S))
def get_cc(d, tag):
    for m in sdt_blocks(d):
        if f'<w:tag w:val="ODS.Meta.{tag}"' in m.group(0): return T(m.group(0).split("<w:sdtContent>")[-1]).strip()
    return None
def set_cc(d, tag, value):
    out, n = d, 0
    for m in reversed(sdt_blocks(d)):
        s = m.group(0)
        if f'<w:tag w:val="ODS.Meta.{tag}"' not in s: continue
        head, content = s.split("<w:sdtContent>", 1)
        ts = list(re.finditer(r"<w:t(?: [^>]*)?>[^<]*</w:t>", content))
        if not ts: continue
        new = content
        for k, t in reversed(list(enumerate(ts))):
            rep = f'<w:t xml:space="preserve">{esc(value) if k == 0 else ""}</w:t>'
            new = new[:t.start()] + rep + new[t.end():]
        out = out[:m.start()] + head + "<w:sdtContent>" + new + out[m.end():]; n += 1
    return out, n
def replace_in_para(d, find, repl):
    """Replace text that may be split over several runs inside one paragraph."""
    count = 0
    for m in reversed(list(re.finditer(r"<w:p[ >].*?</w:p>", d, re.S))):
        p = m.group(0)
        if find not in T(p): continue
        ts = list(re.finditer(r"(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)", p))
        full = "".join(html.unescape(t.group(2)) for t in ts)
        if find not in full: continue
        newfull = full.replace(find, repl)
        # keep run boundaries: put whole new text in the run where the match starts, empty the runs it covered
        pos = full.find(find); acc = 0; start_i = end_i = None
        for i, t in enumerate(ts):
            L = len(html.unescape(t.group(2)))
            if start_i is None and acc + L > pos: start_i = i
            if acc + L >= pos + len(find): end_i = i; break
            acc += L
        pieces = [html.unescape(t.group(2)) for t in ts]
        a0 = sum(len(x) for x in pieces[:start_i]); a1 = sum(len(x) for x in pieces[:end_i + 1])
        merged = "".join(pieces[start_i:end_i + 1]).replace(find, repl, 1)
        pieces[start_i] = merged
        for j in range(start_i + 1, end_i + 1): pieces[j] = ""
        newp = p
        for i, t in reversed(list(enumerate(ts))):
            newp = newp[:t.start()] + f'<w:t xml:space="preserve">{esc(pieces[i])}</w:t>' + newp[t.end():]
        d = d[:m.start()] + newp + d[m.end():]; count += 1
    return d, count

def custom_xml(props):
    items = "".join(f'<property fmtid="{{D5CDD505-2E9C-101B-9397-08002B2CF9AE}}" pid="{i+2}" name="{k}"><vt:lpwstr>{esc(v)}</vt:lpwstr></property>' for i, (k, v) in enumerate(props.items()))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">' + items + "</Properties>")

def set_core(core, tag, val, ns="dc"):
    val = esc(val)
    if re.search(fr"<{ns}:{tag}(?: [^>]*)?>.*?</{ns}:{tag}>", core, re.S):
        return re.sub(fr"(<{ns}:{tag}(?: [^>]*)?>).*?(</{ns}:{tag}>)", lambda m: m.group(1) + val + m.group(2), core, flags=re.S)
    if re.search(fr"<{ns}:{tag}\s*/>", core): return re.sub(fr"<{ns}:{tag}\s*/>", f"<{ns}:{tag}>{val}</{ns}:{tag}>", core)
    return core.replace("</cp:coreProperties>", f"<{ns}:{tag}>{val}</{ns}:{tag}></cp:coreProperties>")

for f in sorted(glob.glob(f"{SRC}/ACE-*.docx")):
    name = os.path.basename(f); zin = zipfile.ZipFile(f)
    d = zin.read("word/document.xml").decode("utf8")
    docid = get_cc(d, "DocumentID")
    # 1. role-only owners/custodians -> named holders
    for (did, tag), val in FIX_PEOPLE.items():
        if did == docid:
            old = get_cc(d, tag)
            if old != val: d, _ = set_cc(d, tag, val); log(name, f"Control field {tag}", old, val, "Field held a role or system name, not a named person from the org chart")
    # 2. job title harmonised with the org chart
    d, n = replace_in_para(d, "Plant Manager, CPF", "Plant Manager - Central Processing Facility")
    if n: log(name, "Job title", "Rohan Ali — Plant Manager, CPF", "Rohan Ali — Plant Manager - Central Processing Facility", f"Matches the ACE org chart ({n} places)")
    # 3. framework field made consistent
    old = get_cc(d, "Framework")
    if old and old != FRAMEWORK: d, _ = set_cc(d, "Framework", FRAMEWORK); log(name, "Control field Framework", old, FRAMEWORK, "Same wording in every document")
    # 4. PSM warning wording
    d, n = replace_in_para(d, "This example shall not be used as", "Do not use this example as")
    if n: log(name, "Warning wording (ODS.Warning)", "This example shall not be used as…", "Do not use this example as…", "Binding 'shall' belongs in a requirement style; warnings use plain instructions")
    # 5. title bookmark so the title OMS tags attach to the title
    tp = re.search(r'<w:p[ >](?:(?!</w:p>).)*?<w:pStyle w:val="Title"/>.*?</w:p>', d, re.S)
    if tp and "doc_title" not in tp.group(0):
        p = tp.group(0); ppr_end = p.find("</w:pPr>") + len("</w:pPr>")
        newp = p[:ppr_end] + '<w:bookmarkStart w:id="900001" w:name="doc_title"/>' + p[ppr_end:-len("</w:p>")] + '<w:bookmarkEnd w:id="900001"/></w:p>'
        d = d[:tp.start()] + newp + d[tp.end():]
        log(name, "Title bookmark", "Title paragraph had no doc_title bookmark", "doc_title bookmark added to the Title paragraph", "Title OMS tags now attach to the title (they were orphaned)")
    # ---- rebuild hidden properties from the visible control fields ----
    meta = {k: get_cc(d, k) or "" for k in ["DocumentID","ControlTitle","DocumentType","Revision","Status","IssueDate","EffectiveDate","Author","Reviewer",
            "Endorser","Approver","DocumentOwner","Custodian","PrimaryFunction","Framework","TitleOMSTags","Classification","Applicability","ReviewInterval","NextReview"]}
    dtype, level = (re.match(r"(.+?) \(Level (\w+)\)", meta["DocumentType"]) or re.match(r"(.+)()", meta["DocumentType"])).groups()
    rev = meta["Revision"].split(" ")[0]; status = meta["Status"].split(" /")[0]
    draft = status.lower().startswith("draft")
    body = T(d)
    roles = [r for r in ROLES if r.lower() in body.lower()]
    props = {
     "ODS.DocumentId": meta["DocumentID"], "ODS.Title": meta["ControlTitle"], "ODS.DocumentType": dtype, "ODS.Level": level,
     "ODS.Revision": rev, "ODS.Status": status, "ODS.IssueDate": "" if draft else meta["IssueDate"], "ODS.EffectiveDate": "" if draft else meta["EffectiveDate"],
     "ODS.Author": meta["Author"], "ODS.Reviewer": meta["Reviewer"], "ODS.Endorser": meta["Endorser"], "ODS.Approver": meta["Approver"],
     "ODS.DocumentOwner": meta["DocumentOwner"], "ODS.ProcessOwner": meta["Custodian"], "ODS.Custodian": meta["Custodian"],
     "ODS.PrimaryFunction": meta["PrimaryFunction"], "ODS.Framework": meta["Framework"], "ODS.TitleOMSTags": meta["TitleOMSTags"],
     "ODS.Classification": meta["Classification"], "ODS.Applicability": meta["Applicability"],
     "ODS.ReviewInterval": meta["ReviewInterval"] or meta["NextReview"], "ODS.RoleRegister": "; ".join(roles)}
    oldcu = zin.read("docProps/custom.xml").decode("utf8") if "docProps/custom.xml" in zin.namelist() else ""
    oldid = re.search(r'name="DocumentID"[^>]*><vt:\w+>([^<]*)<', oldcu)
    log(name, "Custom properties", f"{len(re.findall('<property', oldcu))} properties, non-standard names" + (f"; DocumentID was {oldid.group(1)}" if oldid else ""),
        "22 properties, ODS.* names from the ONE master template, values copied from the control table",
        "Hidden properties disagreed with the document" if oldid and oldid.group(1) != meta["DocumentID"] else "Standard property names")
    core = zin.read("docProps/core.xml").decode("utf8")
    if "xmlns:dc=" not in core: raise SystemExit("core ns")
    core2 = set_core(core, "title", meta["ControlTitle"])
    core2 = set_core(core2, "identifier", meta["DocumentID"])
    core2 = set_core(core2, "subject", f"ONE / ACE controlled document — {dtype} (Level {level})")
    core2 = set_core(core2, "category", f"{dtype} (Level {level})", ns="cp")
    core2 = set_core(core2, "keywords", meta["TitleOMSTags"], ns="cp")
    core2 = set_core(core2, "description", "Draft revision A. Document Control registration and formal approvals pending." if draft else f"Approved revision {rev}. Controlled source in the ONE repository.")
    if draft: core2 = re.sub(r"(<dcterms:created[^>]*>)[^<]*(<)", r"\g<1>2026-11-01T00:00:00Z\2", core2)
    log(name, "Core properties", "Title empty; no identifier; mixed subject/category/description" + ("; created 2013" if draft else ""),
        f"Title, identifier ({meta['DocumentID']}), subject, category, keywords and description set" + ("; created Nov 2026" if draft else ""), "Word's own fields agree with the document")
    zout = zipfile.ZipFile(f"{OUT}/{name}", "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        if it.filename.endswith("/"): continue
        data = zin.read(it.filename)
        if it.filename == "word/document.xml": data = d.encode("utf8")
        elif it.filename == "docProps/custom.xml": data = custom_xml(props).encode("utf8")
        elif it.filename == "docProps/core.xml": data = core2.encode("utf8")
        zout.writestr(it, data)
    zout.close()

with open("/home/claude/audit/change_log_inc.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh); w.writerow(["File","Area","Before","After","Why"]); w.writerows(LOG)
print(len(LOG), "changes")
