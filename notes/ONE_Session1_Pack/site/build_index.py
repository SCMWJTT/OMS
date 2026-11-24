"""ONE build step: read every Word file in the repository and produce one library index (JSON).
This is the same job a GitHub Action would run on every upload."""
import zipfile, re, html, glob, os, json, csv, sys
sys.path.insert(0, "/home/claude/oms/src")
from elements import ELEMENTS
from register import DOCS as REG, SYSTEMS
from doclist import DOCS as PRI

REPO = "/home/claude/site/stage"
FILES = sorted(glob.glob(f"{REPO}/manuals/*.docx")) + sorted(glob.glob(f"{REPO}/finals/ACE-*.docx"))
EXP = {e[0]: e[1] for el in ELEMENTS for e in el["exps"]}
ELN = {el["n"]: el["title"] for el in ELEMENTS}
PEOPLE = {r["Full Name"]: r["Job Title"] for r in csv.DictReader(open("/home/claude/ace/out/ACE_People.csv", encoding="utf-8-sig"))}
KNOWN_TITLES = {("ACE-" + k): v[0] for k, v in REG.items()}
KNOWN_TITLES.update({d["number"]: d["title"] for d in PRI})
SYSNAME = {s[0]: s[1] for s in SYSTEMS}
ROLES = ["Area Authority", "Technical Authority", "Technical Leadership Council", "Permit Issuer", "Performing Authority", "Isolating Authority",
         "OMS Manager", "Information Management Lead", "Document Controller", "Document owner", "System owner", "Element owner", "Line manager",
         "Supervisor", "Contract owner", "Process Safety Lead", "Maintenance & Integrity Manager", "Inspection Lead", "Offshore Installation Manager",
         "Plant Manager", "Investigation lead", "Lead auditor", "Head of Internal Audit", "HSE Adviser", "Approver", "Custodian", "Author", "Reviewer",
         "Executive Leadership Team", "Contractor"]
OK_SHALL = {"Requirement", "Responsibility", "ApprovalRequirement", "RecordRequirement", "RiskControl"}
REQUIRED = ["DocumentId","Title","DocumentType","Revision","IssueDate","EffectiveDate","Status","Author","Reviewer","Approver","DocumentOwner",
            "ProcessOwner","PrimaryFunction","Framework","TitleOMSTags","Classification","Applicability","RoleRegister"]

def T(x): return html.unescape(re.sub(r"<[^>]+>", "", x))

def runs_of(p):
    """text runs with bold/italic, skipping content controls that carry tags."""
    out = []
    p = re.sub(r"<w:sdt>(?:(?!</w:sdt>).)*?ODS\.OMSTags@.*?</w:sdt>", "", p, flags=re.S)
    p = re.sub(r"<w:instrText[^>]*>.*?</w:instrText>", "", p, flags=re.S)
    for r in re.findall(r"<w:r[ >].*?</w:r>", p, re.S):
        rp = re.search(r"<w:rPr>.*?</w:rPr>", r, re.S); rp = rp.group(0) if rp else ""
        b = bool(re.search(r"<w:b/>|<w:b w:val=\"(1|true)\"/>", rp)); i = "<w:i/>" in rp
        for t in re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>|<w:(tab)/>|<w:(br)/>", r):
            txt = html.unescape(t[0]) if t[0] else (" " if t[1] else ("\n" if t[2] else ""))
            if txt:
                if out and out[-1][1] == b and out[-1][2] == i: out[-1][0] += txt
                else: out.append([txt, b, i])
    return out

def parse(path):
    z = zipfile.ZipFile(path); d = z.read("word/document.xml").decode("utf8")
    st = z.read("word/styles.xml").decode("utf8")
    sname = dict(re.findall(r'w:styleId="([^"]+)"[^>]*>\s*<w:name w:val="([^"]+)"', st))
    cu = dict((k.replace("ODS.", ""), html.unescape(v)) for k, v in re.findall(r'name="([^"]+)"[^>]*><vt:\w+>([^<]*)<', z.read("docProps/custom.xml").decode())) if "docProps/custom.xml" in z.namelist() else {}
    meta_cc = {}
    for s in re.findall(r"<w:sdt>.*?</w:sdt>", d, re.S):
        m = re.search(r'<w:tag w:val="ODS\.Meta\.([^"]+)"', s)
        if m: meta_cc.setdefault(m.group(1), T(s.split("<w:sdtContent>")[-1]).strip())
    tags = {m.group(1): T(m.group(2)).strip() for m in re.finditer(r'<w:tag w:val="ODS\.OMSTags@([^"]+)"/>.*?<w:sdtContent>(.*?)</w:sdtContent>', d, re.S)}
    body = d[d.find("<w:body>") + 8:]
    blocks = []; started = False; title_bm = None; title_text = None
    for m in re.finditer(r"<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>", body, re.S):
        x = m.group(0)
        if x.startswith("<w:tbl>"):
            if not started: continue
            rows = []
            for tr in re.findall(r"<w:tr[ >].*?</w:tr>", x, re.S):
                rows.append([" ".join(T(p).strip() for p in re.findall(r"<w:p[ >].*?</w:p>", tc, re.S)).strip()
                             for tc in re.findall(r"<w:tc>.*?</w:tc>", tr, re.S)])
            if rows: blocks.append({"k": "tbl", "rows": rows})
            continue
        sid = re.search(r'<w:pStyle w:val="([^"]+)"', x); style = sname.get(sid.group(1), sid.group(1)) if sid else "Normal"
        bms = [b for b in re.findall(r'<w:bookmarkStart [^>]*w:name="([^"]+)"', x) if not b.startswith("_")]
        if style.lower() == "title":
            title_text = T(x).strip(); title_bm = bms[0] if bms else None; continue
        lvl = re.match(r"(?i)heading (\d)", style)
        if lvl and int(lvl.group(1)) == 1: started = True
        if not started or style == "ODS Tag Line": continue
        rs = runs_of(x); txt = "".join(r[0] for r in rs).strip()
        if lvl:
            bm = bms[0] if bms else None
            blocks.append({"k": "h", "l": int(lvl.group(1)), "t": txt, "bm": bm, "tags": tags.get(bm, "") if bm else ""})
        elif txt:
            kind = style.replace("ODS.", "") if style.startswith("ODS.") else ("li" if style.lower().startswith("list") else "p")
            blocks.append({"k": kind, "r": rs})
    meta = {k: cu.get(k, "") for k in set(REQUIRED) | {"Level", "Custodian", "Endorser", "ReviewInterval"}}
    if not meta["DocumentId"]: meta["DocumentId"] = meta_cc.get("DocumentID", "")
    return dict(file=os.path.basename(path), meta=meta, meta_cc=meta_cc, tags=tags, title=title_text or meta["Title"], title_bm=title_bm,
                title_tags=tags.get(title_bm, "") if title_bm else "", blocks=blocks)

def gateway(doc, all_ids):
    R = []; m = doc["meta"]; cc = doc["meta_cc"]
    heads = {b["bm"] for b in doc["blocks"] if b["k"] == "h" and b["bm"]} | ({doc["title_bm"]} if doc["title_bm"] else set())
    for bm, v in doc["tags"].items():
        if bm not in heads: R.append(["err", f"OMS tag control “{bm}” is not attached to a heading"])
        if not v.strip(): continue
        lst = [t.strip() for t in v.split(",")]
        if not re.fullmatch(r"\s*\d{1,2}\.\d{1,2}(\s*,\s*\d{1,2}\.\d{1,2})*\s*", v): R.append(["err", f"Tags “{v}” are not numbers separated by commas"]); continue
        bad = [t for t in lst if t not in EXP]
        if bad: R.append(["err", f"{', '.join('E'+t for t in bad)} not in the OMS register"])
        if len(set(lst)) != len(lst): R.append(["err", f"Duplicate tags “{v}”"])
    miss = [k for k in REQUIRED if not m.get(k)]
    draft = m.get("Status", "").lower().startswith("draft")
    if draft: miss = [k for k in miss if k not in ("IssueDate", "EffectiveDate")]
    if miss: R.append(["wrn", "Document properties missing: " + ", ".join(miss)])
    # visible control table must agree with hidden properties
    pairs = [("DocumentID", "DocumentId"), ("ControlTitle", "Title"), ("Approver", "Approver"), ("Author", "Author"), ("DocumentOwner", "DocumentOwner")]
    for a, b in pairs:
        if cc.get(a) and m.get(b) and cc[a].split(" (")[0] != m[b].split(" (")[0]: R.append(["err", f"Control table {a} “{cc[a][:40]}” differs from hidden property “{m[b][:40]}”"])
    if m["DocumentId"] and not re.fullmatch(r"ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(-[A-Z]{3})?", m["DocumentId"]): R.append(["wrn", f"Document number {m['DocumentId']} does not follow ACE-AAA-TTT-NNN"])
    rev = m.get("Revision", "")
    if rev and not re.fullmatch(r"\d{2}|[A-Z]", rev): R.append(["wrn", f"Revision “{rev}” is not A, B … or 01, 02 …"])
    if re.fullmatch(r"[A-Z]", rev or "") and not draft: R.append(["err", f"Revision {rev} is a draft letter but status is {m.get('Status')}"])
    if doc["title_tags"].replace(" ", "") != m.get("TitleOMSTags", "").replace(" ", ""): R.append(["wrn", "Title tags differ from the Title OMS Tags property"])
    for b in doc["blocks"]:
        if b["k"] not in OK_SHALL and b["k"] not in ("h", "tbl") and re.search(r"\bshall\b", "".join(r[0] for r in b["r"]), re.I):
            R.append(["wrn", f"“shall” in {b['k']} style: “{''.join(r[0] for r in b['r'])[:90]}…”"])
    for k in ("Author", "Approver", "DocumentOwner"):
        for part in m.get(k, "").split(";"):
            mm = re.match(r"\s*(.+?) — (.+?)\s*$", part)
            if mm and mm.group(1) not in PEOPLE: R.append(["wrn", f"{k} “{mm.group(1)}” is not in the ACE organisation chart"])
    untagged = sum(1 for b in doc["blocks"] if b["k"] == "h" and not b["tags"])
    if untagged: R.append(["inf", f"{untagged} headings without OMS tags (allowed)"])
    refs = sorted(set(re.findall(r"\bACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?\b", " ".join("".join(r[0] for r in b.get("r", [])) for b in doc["blocks"] if b["k"] != "tbl"))))
    missing = [r for r in refs if r not in all_ids and r != m["DocumentId"]]
    if missing: R.append(["inf", f"{len(missing)} referenced documents not yet in the library: {', '.join(missing[:6])}{'…' if len(missing) > 6 else ''}"])
    e = sum(1 for r in R if r[0] == "err"); w = sum(1 for r in R if r[0] == "wrn")
    return {"verdict": "fail" if e else "warn" if w else "pass", "errors": e, "warnings": w, "items": R}

docs = [parse(f) for f in FILES]
ids = {d["meta"]["DocumentId"] for d in docs}
out_docs = []
for d in docs:
    m = d["meta"]; did = m["DocumentId"]; system = did.split("-")[1] if did.count("-") >= 3 else ""
    secs = []; refs = set(); roles = {}
    cur = None
    for i, b in enumerate(d["blocks"]):
        if b["k"] == "h": cur = i; secs.append({"i": i, "l": b["l"], "t": b["t"], "bm": b["bm"], "tags": b["tags"]})
        txt = " ".join(" ".join(c) for c in b["rows"]) if b["k"] == "tbl" else ("".join(r[0] for r in b.get("r", [])) if b["k"] != "h" else b["t"])
        refs |= set(re.findall(r"\bACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?\b", txt))
        if b["k"] in ("Requirement", "Responsibility", "ApprovalRequirement", "RecordRequirement", "RiskControl", "ProcedureStep", "Warning"):
            for r in ROLES:
                if re.search(r"\b" + re.escape(r) + r"s?\b", txt, re.I): roles.setdefault(r, []).append(i)
    refs.discard(did)
    gw = gateway(d, ids)
    out_docs.append({"id": did, "file": d["file"], "title": d["title"], "type": m["DocumentType"], "level": m["Level"] or ("1" if "Manual" in m["DocumentType"] else ""),
                     "rev": m["Revision"], "status": m["Status"], "eff": m["EffectiveDate"], "owner": m["DocumentOwner"], "author": m["Author"],
                     "approver": m["Approver"], "function": m["PrimaryFunction"], "system": system, "systemName": SYSNAME.get(system, system),
                     "titleTags": d["title_tags"], "blocks": d["blocks"], "secs": secs, "refs": sorted(refs), "roles": roles, "gateway": gw,
                     "words": sum(len("".join(r[0] for r in b.get("r", [])).split()) for b in d["blocks"])})
index = {"built": "21 November 2026", "source": "github.com/SCMWJTT/OMS @ main", "docs": out_docs, "exp": EXP, "el": ELN,
         "known": KNOWN_TITLES, "systems": SYSNAME}
json.dump(index, open("/home/claude/site/index.json", "w"), separators=(",", ":"))
for d in out_docs:
    print(f"{d['id']:<20} {d['status']:<9} rev {d['rev']:<3} secs {len(d['secs']):>3} refs {len(d['refs']):>2} roles {len(d['roles']):>2} gateway {d['gateway']['verdict']} {[i[1][:60] for i in d['gateway']['items'] if i[0]!='inf']}")
print(os.path.getsize("/home/claude/site/index.json") // 1024, "KB")
