"""Extract a LITE ONE document body into a spec .py file (text preserved)."""
import zipfile, re, sys, pprint

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
FRONT = {"document control", "revision history", "document map", "approval and issue"}
KIND = {"ODS.Requirement": "req", "ODSRequirement": "req", "ODS.Responsibility": "resp", "ODS.ApprovalRequirement": "appr",
        "ODS.RecordRequirement": "rec", "ODS.RiskControl": "rc", "ODS.Warning": "warn", "ODS.PerformanceIndicator": "kpi",
        "ODS.Note": "note", "ODS.DocumentReference": "ref", "ODS.ExternalStandard": "ext", "ODS.ProcedureStep": "step",
        "ODS.Definition": "def", "ListParagraph": "bul", "ListBullet": "bul"}
CID = re.compile(r"(?<![A-Za-z0-9-])C-[A-Z]{3}-\d{3}")
import xml.etree.ElementTree as ET


def ptext(p):
    return "".join(x.text or "" for x in p.iter(W + "t")).strip()


def pstyle(p):
    s = p.find(f"{W}pPr/{W}pStyle")
    v = s.get(W + "val") if s is not None else "Normal"
    if v.startswith("ODS") and not v.startswith("ODS.") and v != "ODSTagLine":
        v = "ODS." + v[3:]
    return v


def classify(t):
    if CID.search(t):
        return "rc"
    lt = t.lower()
    if re.search(r"\bapprov", lt):
        return "appr"
    if re.search(r"\b(record|retain|register|logged|documented in)\b", lt):
        return "rec"
    if re.search(r"\b(responsib|accountab)", lt):
        return "resp"
    return "req"


def extract(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find(W + "body")
    els = list(body)
    blocks, started, pending_tag = [], False, False
    for el in els:
        if el.tag == W + "p":
            st, tx = pstyle(el), ptext(el)
            if not tx:
                continue
            if st.startswith("Heading"):
                lvl = int(re.sub(r"\D", "", st) or 1)
                clean = re.sub(r"^(\d+(\.\d+)*\.?)\s+", "", tx)
                if clean.lower() in FRONT:
                    started = False if not started else started
                    if not started:
                        continue
                started = True
                if clean.lower().startswith("appendix"):
                    clean = re.sub(r"^appendix\s+[a-z0-9]+\s*[—–:-]\s*", "", clean, flags=re.I)
                    blocks.append(["app", clean, ""])
                else:
                    blocks.append(["h1" if lvl == 1 else "h2", clean, ""])
                pending_tag = True
                continue
            if not started:
                continue
            if st == "ODSTagLine":
                if pending_tag and blocks:
                    blocks[-1][2] = re.sub(r"^OMS\s*", "", tx).strip()
                pending_tag = False
                continue
            pending_tag = False
            k = KIND.get(st, "p")
            if k not in ("req", "resp", "appr", "rec", "rc") and re.search(r"\bshall\b", tx, re.I):
                k = classify(tx)
            blocks.append([k, tx])
        elif el.tag == W + "tbl" and started:
            rows = []
            for tr in el.findall(W + "tr"):
                r = []
                for tc in tr.findall(W + "tc"):
                    ps = [ptext(p) for p in tc.findall(W + "p")]
                    ps = [p for p in ps if p]
                    r.append("".join(ps) if ps and all(len(p) == 1 for p in ps) else "\n".join(ps))
                rows.append(r)
            if rows:
                blocks.append(["t", rows])
    return blocks


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    b = extract(src)
    with open(out, "w") as f:
        f.write("# extracted from " + src.split("/")[-1] + "\nBODY = " + pprint.pformat([tuple(x) for x in b], width=150) + "\n")
    print(out, len(b), "blocks")
