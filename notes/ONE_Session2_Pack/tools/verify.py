"""Independent check of built documents (does not use gen.py)."""
import zipfile, re, sys, csv, glob
import xml.dom.minidom
P = {r["Full Name"]: r["Job Title"] for r in csv.DictReader(open("/home/claude/repo/company/ACE_People.csv", encoding="utf-8-sig"))}
SYS = "LDR OMS LEG PPL CON STK RSK PSM MOC PRJ ENG AIM MNT WEL OPS COW EMR DOC INC PRF ENV OHH SEC BPM LOG HMA".split()
BIND = {"ODS.Requirement", "ODS.Responsibility", "ODS.ApprovalRequirement", "ODS.RecordRequirement", "ODS.RiskControl"}
CID = re.compile(r"(?<![A-Za-z0-9-])C-([A-Z]{3})-\d{3}")
MAP = {"DocumentID": "DocumentId", "ControlTitle": "Title"}
allc = {}
bad_total = 0
for f in sorted(sys.argv[1:]):
    z = zipfile.ZipFile(f); errs = []
    for n in z.namelist():
        if n.endswith(".xml") or n.endswith(".rels"):
            try: xml.dom.minidom.parseString(z.read(n))
            except Exception as e: errs.append(f"XML invalid {n}: {e}")
    d = z.read("word/document.xml").decode()
    props = dict(re.findall(r'name="ODS\.([^"]+)"><vt:lpwstr>([^<]*)<', z.read("docProps/custom.xml").decode()))
    props = {k: v.replace("&amp;", "&") for k, v in props.items()}
    if len(props) != 23: errs.append(f"{len(props)} properties")
    empty = [k for k, v in props.items() if not v]
    if empty: errs.append(f"empty props {empty}")
    # meta controls agree with props
    for tag, val in re.findall(r'<w:tag w:val="ODS\.Meta\.([^"]+)"/>.*?<w:sdtContent>(.*?)</w:sdtContent>', d, re.S):
        v = "".join(re.findall(r"<w:t[^>]*>([^<]*)", val)).replace("&amp;", "&")
        k = MAP.get(tag, tag)
        if k in props and props[k] != v: errs.append(f"Meta.{tag} '{v}' != prop '{props[k]}'")
    if "CoverRevision" not in d: errs.append("no cover revision")
    # core
    core = z.read("docProps/core.xml").decode()
    if f"<dc:subject>{props['DocumentId']}</dc:subject>" not in core: errs.append("core subject")
    if f"<cp:keywords>{props['TitleOMSTags']}</cp:keywords>" not in core: errs.append("core keywords")
    hf = "".join(z.read(n).decode() for n in z.namelist() if re.match(r"word/(header|footer)\d", n))
    if props["DocumentId"] not in hf or f"Rev {props['Revision']}" not in hf: errs.append("header/footer mismatch")
    if "Rev 04" not in props["Framework"]: errs.append("framework")
    # people
    for k in ["Author", "Reviewer", "Approver", "DocumentOwner", "Custodian"]:
        for p in props[k].split("; "):
            nm, _, tt = p.partition(" — ")
            if P.get(nm) != tt: errs.append(f"person {k}: {p}")
    # headings: bookmark + tag CC
    paras = re.findall(r"<w:p>.*?</w:p>", d, re.S)
    for i, p in enumerate(paras):
        st = re.search(r'<w:pStyle w:val="([^"]+)"', p); st = st.group(1) if st else "Normal"
        txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)", p))
        if st in ("Heading1", "Heading2") and txt:
            bm = re.search(r'bookmarkStart w:id="\d+" w:name="([^"]+)"', p)
            nxt = paras[i + 1] if i + 1 < len(paras) else ""
            if not bm: errs.append(f"no bookmark: {txt}")
            elif f"ODS.OMSTags@{bm.group(1)}" not in nxt: errs.append(f"no tag CC: {txt}")
            else:
                tags = "".join(re.findall(r"<w:t[^>]*>([^<]*)", nxt)).replace("OMS", "").strip()
                for t in tags.split(","):
                    t = t.strip()
                    if not re.fullmatch(r"(10|[1-9])\.[1-9]", t): errs.append(f"bad tag {t} at {txt}")
        if re.search(r"\bshall\b", txt, re.I) and st not in BIND: errs.append(f"shall in {st}: {txt[:50]}")
        if st == "ODS.RiskControl" and "ODS.Control@C-" not in p: errs.append(f"RC without CC: {txt[:50]}")
    # shall in table cells
    for c in re.findall(r"<w:tc>.*?</w:tc>", d, re.S):
        if re.search(r"\bshall\b", "".join(re.findall(r"<w:t[^>]*>([^<]*)", c)), re.I): errs.append("shall in table cell")
    for c in re.findall(r'<w:tag w:val="ODS\.Control@(C-([A-Z]{3})-\d{3})"', d):
        if c[1] not in SYS: errs.append(f"bad system in {c[0]}")
        if c[0] in allc and allc[c[0]] != props["DocumentId"]: errs.append(f"duplicate {c[0]} also in {allc[c[0]]}")
        allc[c[0]] = props["DocumentId"]
    if 'doc_title' not in d or "ODS.OMSTags@doc_title" not in d: errs.append("doc_title")
    if any(n in ("word/media/image1.png", "word/media/image2.png") for n in z.namelist()): errs.append("unused media")
    print(f"{'PASS' if not errs else 'FAIL'}  {f.split('/')[-1]}")
    for e in errs[:12]: print("      -", e)
    bad_total += bool(errs)
print(f"\n{len(sys.argv) - 1 - bad_total} passed, {bad_total} failed; {len(allc)} Control IDs, all unique")
