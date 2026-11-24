import zipfile,re,csv,html,sys,os
from lxml import etree
sys.path.insert(0,"/home/claude/oms/src")
from elements import ELEMENTS
EXP={e[0] for el in ELEMENTS for e in el["exps"]}
P={r["Full Name"]:r["Job Title"] for r in csv.DictReader(open("/home/claude/ace/out/ACE_People.csv",encoding="utf-8-sig"))}
T=lambda x: html.unescape(re.sub(r"<[^>]+>","",x)); W="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
OK={"Requirement","Responsibility","ApprovalRequirement","RecordRequirement","RiskControl"}
for f in sys.argv[1:]:
    z=zipfile.ZipFile(f); n=z.namelist(); d=z.read("word/document.xml").decode(); iss=[]
    cu=dict((k,html.unescape(v)) for k,v in re.findall(r'name="([^"]+)"[^>]*><vt:\w+>([^<]*)<',z.read("docProps/custom.xml").decode())) if "docProps/custom.xml" in n else {}
    core=dict(re.findall(r"<(?:dc|cp):(\w+)[^>]*>([^<]*)(?=<)",z.read("docProps/core.xml").decode()))
    meta={}
    for s in re.findall(r"<w:sdt>.*?</w:sdt>",d,re.S):
        m=re.search(r'<w:tag w:val="ODS\.Meta\.([^"]+)"',s)
        if m: meta.setdefault(m.group(1),T(s.split("<w:sdtContent>")[-1]).strip())
    did=meta.get("DocumentID","?")
    if cu.get("ODS.DocumentId")!=did: iss.append(f"hidden DocumentId {cu.get('ODS.DocumentId')} vs table {did}")
    if cu.get("ODS.Title","").split(" (")[0]!=meta.get("ControlTitle","").split(" (")[0]: iss.append("hidden title differs from table")
    for a,b in [("Author","ODS.Author"),("Approver","ODS.Approver"),("DocumentOwner","ODS.DocumentOwner")]:
        if meta.get(a) and meta[a]!=cu.get(b): iss.append(f"{a} differs: table '{meta[a][:40]}' vs hidden '{cu.get(b,'')[:40]}'")
    if core.get("identifier")!=did: iss.append(f"Word identifier '{core.get('identifier')}'")
    if not core.get("title"): iss.append("Word Title empty")
    if not cu.get("ODS.RoleRegister"): iss.append("RoleRegister empty")
    st=z.read("word/styles.xml").decode(); ids=dict(re.findall(r'w:styleId="([^"]+)"[^>]*>\s*<w:name w:val="([^"]+)"',st))
    paras=re.findall(r"<w:p[ >].*?</w:p>",d,re.S)
    tp=[p for p in paras if '<w:pStyle w:val="Title"/>' in p]
    if not (tp and "doc_title" in tp[0]): iss.append("doc_title bookmark not on Title")
    tags={k:T(v).strip() for k,v in re.findall(r'ODS\.OMSTags@([^"]+)"/>.*?<w:sdtContent>(.*?)</w:sdtContent>',d,re.S)}
    heads=set()
    for p in paras:
        s=re.search(r'<w:pStyle w:val="([^"]+)"',p); s=ids.get(s.group(1),s.group(1)) if s else "Normal"
        if re.match(r"(?i)heading|title",s): heads|=set(re.findall(r'w:name="([^"]+)"',p))
        elif re.search(r"\bshall\b",T(p),re.I) and s.replace("ODS.","") not in OK: iss.append(f"'shall' in {s}: {T(p)[:70]}")
    orph=[k for k in tags if k not in heads]; bad=[v for v in tags.values() if v and (any(t.strip() not in EXP for t in v.split(",")) or len(set(t.strip() for t in v.split(",")))!=len(v.split(",")))]
    if orph: iss.append(f"{len(orph)} orphan tag controls")
    if bad: iss.append(f"bad tags {bad[:3]}")
    if tags.get("doc_title","").replace(" ","")!=cu.get("ODS.TitleOMSTags","").replace(" ",""): iss.append("title tags differ from property")
    for k in ("Author","Reviewer","Approver","DocumentOwner","Custodian"):
        for part in meta.get(k,"").split(";"):
            m=re.match(r"\s*(.+?) — (.+?)\s*$",part)
            if m and (m.group(1) not in P or not P[m.group(1)].startswith(re.sub(r" \(.*","",m.group(2)))): iss.append(f"person? {part.strip()}")
    rels=z.read("word/_rels/document.xml.rels").decode(); used=set(re.findall(r'r:embed="([^"]+)"',d))
    for h in [x for x in n if re.match(r"word/(header|footer)\d+\.xml$",x)]: used|=set(re.findall(r'r:embed="([^"]+)"',z.read(h).decode()))
    unused=[t for r,t in re.findall(r'Id="([^"]+)"[^>]*Target="(media/[^"]+)"',rels) if r not in used]
    if unused: iss.append(f"{len(unused)} unused images")
    t=etree.fromstring(z.read("word/document.xml")); bp=sum(1 for p in t.iter(W+"p") if p.find(W+"pPr") is not None and p[0].tag!=W+"pPr")
    if bp: iss.append(f"{bp} paragraphs with bookmark before settings")
    if "INCLUDEPICTURE" in d: iss.append("linked logo")
    print(f"{os.path.basename(f)[:40]} | {len(tags)} tags | {os.path.getsize(f)//1024} KB |", "CLEAN" if not iss else "; ".join(iss))
