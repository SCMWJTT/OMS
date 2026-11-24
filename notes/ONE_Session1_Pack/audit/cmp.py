import zipfile, re, glob, os, csv, json, sys
sys.path.insert(0,"/home/claude/oms/src")
from register import DOCS as REG
from doclist import DOCS as PRI
known=set("ACE-"+k for k in REG)|{d["number"] for d in PRI}
P={r["Full Name"]:r["Job Title"] for r in csv.DictReader(open("/home/claude/ace/out/ACE_People.csv",encoding="utf-8-sig"))}
def T(x): return re.sub(r"<[^>]+>","",x)
alltitles=set(P.values())
for f in sorted(glob.glob("/home/claude/scmwjtt/oms/finals/*.docx")):
    z=zipfile.ZipFile(f); d=z.read("word/document.xml").decode()
    meta={}
    for s in re.findall(r"<w:sdt>.*?</w:sdt>",d,re.S):
        tg=re.search(r'<w:tag w:val="ODS\.Meta\.([^"]+)"',s)
        if tg: meta.setdefault(tg.group(1),T(s.split("<w:sdtContent>")[-1]).strip())
    cu=dict(re.findall(r'name="([^"]+)"[^>]*><vt:\w+>([^<]*)<',z.read("docProps/custom.xml").decode()))
    core=dict(re.findall(r"<(?:dc|cp):(\w+)[^>]*>([^<]*)<",z.read("docProps/core.xml").decode()))
    print("=====",os.path.basename(f)[:30])
    mism=[]
    for mk,ck in [("DocumentID","DocumentID"),("ControlTitle","Title"),("Revision","Revision"),("Status","Status"),("IssueDate","IssueDate"),("EffectiveDate","EffectiveDate"),("Author","Author"),("Reviewer","Reviewer"),("Approver","Approver"),("DocumentOwner","Owner"),("Custodian","Custodian"),("Endorser","Endorser"),("TitleOMSTags","TitleOMSTags"),("PrimaryFunction","PrimaryFunction"),("Applicability","Applicability")]:
        a=meta.get(mk,"").replace("&amp;","&"); b=cu.get(ck,"").replace("&amp;","&")
        if a.split(" (")[0]!=b.split(" (")[0]: mism.append(f"{mk}: cc='{a[:45]}' prop='{b[:45]}'")
    print(" meta vs props mismatches:",len(mism)); [print("   ",m) for m in mism[:6]]
    print(" core title:",core.get("title"),"| cover title cc:",meta.get("Title"),"| type cc:",meta.get("DocumentType"))
    # people
    txt=T(d).replace("&amp;","&")
    bad=[]
    for name,title in set(re.findall(r"([A-Z][a-zA-Z.'-]+(?: [A-Za-z.'-]+){1,3}) — ([A-Z][A-Za-z&,()/ .'-]+?)(?=;|$| \(|Approved|Signed|\d|[A-Z]{3,}|  )",txt)):
        title=title.strip().rstrip(",")
        if name in P:
            if not (P[name].startswith(title) or title.startswith(P[name].split(" (")[0])): bad.append(f"{name}: doc says '{title}', org chart '{P[name]}'")
        elif title in alltitles or "Lead" in title or "VP" in title or "Manager" in title: bad.append(f"UNKNOWN PERSON {name} — {title}")
    print(" people issues:",bad[:8])
    refs=sorted(set(re.findall(r"\bACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?\b",txt)))
    print(" unknown refs:",[r for r in refs if r not in known])
    print(" role-only meta:",{k:v for k,v in meta.items() if k in("DocumentOwner","Custodian","Approver","Author") and " — " not in v})
