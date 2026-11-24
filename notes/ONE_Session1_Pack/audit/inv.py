import zipfile, re, sys, json, glob, os, csv
from collections import Counter
from xml.dom import minidom

ROOT = "/home/claude/scmwjtt/oms"
PEOPLE = {r["Full Name"]: r["Job Title"] for r in csv.DictReader(open("/home/claude/ace/out/ACE_People.csv", encoding="utf-8-sig"))}
sys.path.insert(0, "/home/claude/oms/src")
from elements import ELEMENTS
EXP = {e[0] for el in ELEMENTS for e in el["exps"]}

def X(z, p):
    try: return z.read(p).decode("utf8")
    except KeyError: return None
def text(xml): return re.sub(r"<[^>]+>", "", xml)

def inspect(path):
    z = zipfile.ZipFile(path); names = z.namelist(); R = {"file": os.path.basename(path), "parts": names}
    core = X(z, "docProps/core.xml") or ""
    R["core"] = {k: v for k, v in re.findall(r"<(?:dc|cp|dcterms):(\w+)[^>]*>([^<]*)<", core)}
    app = X(z, "docProps/app.xml") or ""
    R["app"] = {k: v for k, v in re.findall(r"<(Template|Company|Manager|Application|AppVersion|Pages|Words)>([^<]*)<", app)}
    cu = X(z, "docProps/custom.xml")
    R["custom"] = dict(re.findall(r'name="([^"]+)"[^>]*><vt:\w+>([^<]*)<', cu)) if cu else {}
    st = X(z, "word/settings.xml") or ""
    R["attachedTemplate"] = re.findall(r'<w:attachedTemplate r:id="([^"]+)"', st)
    srel = X(z, "word/_rels/settings.xml.rels") or ""
    R["templateTarget"] = re.findall(r'Target="([^"]+)"', srel)
    R["docVars"] = re.findall(r'<w:docVar w:name="([^"]+)" w:val="([^"]*)"', st)
    R["customXml"] = [n for n in names if n.startswith("customXml/") and n.endswith(".xml") and "itemProps" not in n]
    R["customXmlContent"] = {n: text(X(z, n))[:300] for n in R["customXml"]}
    d = X(z, "word/document.xml")
    stx = X(z, "word/styles.xml"); sid2name = dict(re.findall(r'w:styleId="([^"]+)"[^>]*>\s*<w:name w:val="([^"]+)"', stx))
    # paragraphs
    paras = re.findall(r"<w:p[ >].*?</w:p>", d, re.S)
    P = []
    for p in paras:
        s = re.search(r'<w:pStyle w:val="([^"]+)"', p); s = sid2name.get(s.group(1), s.group(1)) if s else "Normal"
        bms = [b for b in re.findall(r'<w:bookmarkStart [^>]*w:name="([^"]+)"', p) if not b.startswith("_")]
        tags = re.findall(r'<w:tag w:val="([^"]+)"', p)
        P.append(dict(style=s, text=text(p).strip(), bms=bms, tags=tags, raw=p))
    R["styles"] = Counter(p["style"] for p in P)
    heads = [p for p in P if re.match(r"(?i)^(title|heading \d)$", p["style"])]
    R["title_para"] = next((p["text"] for p in P if p["style"].lower() == "title"), None)
    R["n_heads"] = len(heads)
    # tags & bookmarks
    alltags = re.findall(r'<w:sdt>.*?</w:sdt>', d, re.S)
    sdts = []
    for s in alltags:
        tg = re.search(r'<w:tag w:val="([^"]+)"', s); al = re.search(r'<w:alias w:val="([^"]+)"', s)
        sdts.append((al.group(1) if al else None, tg.group(1) if tg else None, text(s.split("<w:sdtContent>")[-1]).strip()))
    R["sdt_kinds"] = Counter(f"{a}|{(t or '').split('@')[0]}" for a, t, _ in sdts)
    omst = [(t.split("@")[1], v) for a, t, v in sdts if t and t.startswith("ODS.OMSTags@")]
    headbm = {b: p for p in heads for b in p["bms"]}
    allbm = re.findall(r'<w:bookmarkStart [^>]*w:name="([^"]+)"', d)
    R["bm_dupes"] = [b for b, c in Counter(allbm).items() if c > 1]
    R["tag_orphans"] = [bm for bm, v in omst if bm not in headbm]
    R["tag_bad"] = [(bm, v) for bm, v in omst if v.strip() and (not re.fullmatch(r"\s*\d{1,2}\.\d{1,2}(\s*,\s*\d{1,2}\.\d{1,2})*\s*", v) or any(t.strip() not in EXP for t in v.split(",")) or len(set(t.strip() for t in v.split(","))) != len(v.split(",")))]
    R["n_tags"] = len(omst)
    R["heads_untagged"] = [p["text"][:60] for p in heads if not any(b in dict(omst) for b in p["bms"])]
    title_bm = [bm for bm, v in omst if bm == "doc_title"]
    R["title_tag_value"] = dict(omst).get("doc_title")
    tp = next((p for p in P if p["style"].lower() == "title"), None)
    R["title_has_doc_title_bm"] = bool(tp and "doc_title" in tp["bms"])
    # shall checks
    R["shall_unstyled"] = [(p["style"], p["text"][:120]) for p in P if re.search(r"\bshall\b", p["text"], re.I) and not p["style"].startswith("ODS.Requirement") and p["style"] not in ("ODS.ApprovalRequirement", "ODS.RecordRequirement") and not re.match(r"(?i)heading|title", p["style"])]
    # control table key/values (2-col tables)
    kv = {}
    for t in re.findall(r"<w:tbl>.*?</w:tbl>", d, re.S)[:6]:
        for row in re.findall(r"<w:tr[ >].*?</w:tr>", t, re.S):
            cells = [text(c).strip() for c in re.findall(r"<w:tc>.*?</w:tc>", row, re.S)]
            if len(cells) == 2 and 2 < len(cells[0]) < 40 and cells[0] not in kv: kv[cells[0]] = cells[1]
    R["control_table"] = kv
    # cover text
    R["cover_text"] = " | ".join(p["text"] for p in P[:14] if p["text"])[:600]
    # headers / footers
    R["headers"] = {n: text(X(z, n)).strip()[:200] for n in names if re.match(r"word/(header|footer)\d+\.xml", n)}
    # references
    full = text(d)
    R["doc_refs"] = sorted(set(re.findall(r"\bAC(?:ME|E)-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?\b", full)))
    R["acme_mentions"] = len(re.findall(r"\bACME\b", full))
    R["names_in_doc"] = sorted({n for n in PEOPLE if n in full})
    R["name_title_pairs"] = sorted(set(re.findall(r"([A-Z][a-z]+(?:[ -][A-Z][a-zA-Z.'-]+){1,3}) — ([A-Z][^;|\n]{3,70}?)(?=;|$|\s{2}|\|)", full)))
    # misc hidden
    R["hidden_text"] = len(re.findall(r"<w:vanish/>", d))
    R["comments"] = "word/comments.xml" in names
    R["tracked"] = len(re.findall(r"<w:(ins|del) ", d))
    R["fields"] = Counter(re.sub(r"\s+.*", "", f.strip()) for f in re.findall(r"<w:instrText[^>]*>([^<]*)<", d))
    R["placeholders"] = re.findall(r"(?i)\[(?:insert|tbd|todo|xx+)[^\]]*\]|lorem ipsum|TBD\b", full)[:5]
    R["images"] = [n for n in names if "media/" in n]
    R["alt_text"] = re.findall(r'<wp:docPr [^>]*descr="([^"]*)"', d)[:4]
    R["words"] = len(full.split())
    return R

out = []
for f in sorted(glob.glob(f"{ROOT}/finals/*.docx")) + sorted(glob.glob(f"{ROOT}/templates/*")):
    if os.path.basename(f).startswith("~$"): continue
    try: out.append(inspect(f))
    except Exception as e: out.append({"file": os.path.basename(f), "error": str(e)})
json.dump(out, open("/home/claude/audit/inventory.json", "w"), indent=1, default=str)
print(len(out))
