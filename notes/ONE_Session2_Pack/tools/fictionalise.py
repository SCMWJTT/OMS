"""Replace names of real organisations with fictional ones across ACE data and Word documents.

Run from the repo root:  python notes/ONE_Session2_Pack/tools/fictionalise.py
Safe to run more than once. Word files keep their revision; only text inside w:t runs changes.
"""
import re, sys, zipfile, shutil, os, glob, csv, io

# The gas buyer: a role, not an invented company, so it cannot collide with a real one
def gas(text):
    text = re.sub(r"\s*\(The National Gas Company of Trinidad and Tobago\)", "", text)
    text = text.replace("NGC-DCQ", "GAS-DCQ")
    text = re.sub(r"\bNGC-interface\b", "Gas Buyer interface", text)
    text = re.sub(r"\b(to|with|by|from|of|and|at|for|on) NGC\b", r"\1 the Gas Buyer", text)
    text = re.sub(r"\bthe NGC\b", "the Gas Buyer", text)
    text = re.sub(r"\bNGC\b", "Gas Buyer", text)
    return text

# Training institutions: all fictional
INST = [
    ("The University of the West Indies, St. Augustine", "Saman University, Trinidad"),
    ("UWI Cave Hill (Barbados)", "Saman University, Barbados campus"),
    ("UWI Mona (Jamaica)", "Saman University, Jamaica campus"),
    ("Point Lisas Campus, UTT", "Lisas Institute of Technology"),
    ("The University of Trinidad and Tobago", "Lisas Institute of Technology"),
    ("COSTAATT", "Central Trinidad Community College"),
    ("NESC Technical Institute", "Southern Technical Institute"),
    ("MIC Institute of Technology", "Caroni Technical Institute"),
    ("ROYTEC", "Gulf Business School"),
    ("Arthur Lok Jack Global School of Business", "Gulf Business School (graduate)"),
    ("School of Business & Computer Science", "Gulf Business School"),
    ("Caribbean Maritime University (Jamaica)", "Windward Maritime Academy"),
]
FOREIGN = r"(University of [A-Z][\w ]+|Colorado School of Mines|Texas A&M University|Imperial College London|Robert Gordon University|Heriot-Watt University|Dalhousie University|London School of Economics) \((UK|USA|Canada)\)"

def inst(text):
    for a, b in INST: text = text.replace(a, b)
    text = re.sub(FOREIGN, lambda m: f"University ({m.group(2)})", text)
    text = re.sub(r"\bUWI St\. Augustine\b", "Saman University", text)
    text = re.sub(r"\bUWI\b", "Saman University", text)
    text = re.sub(r"\bUTT\b", "the Lisas Institute of Technology", text)
    text = re.sub(r"\bNESC\b", "Southern Technical Institute", text)
    text = re.sub(r"\bMIC\b", "Caroni Technical Institute", text)
    return text

def fix(text): return inst(gas(text))

def fix_text_file(p):
    s = open(p, encoding="utf-8-sig").read()
    if p.endswith(".csv"):   # cell by cell, so a new comma is quoted properly
        rows = list(csv.reader(io.StringIO(s))); new = [[fix(c) for c in r] for r in rows]
        if new == rows: return 0
        b = io.StringIO(); csv.writer(b, lineterminator="\n").writerows(new); open(p, "w", encoding="utf-8").write(b.getvalue()); return 1
    t = fix(s)
    if t != s: open(p, "w", encoding="utf-8").write(t); return 1
    return 0

def fix_docx(p):
    z = zipfile.ZipFile(p); changed = 0; out = {}
    for n in z.namelist():
        data = z.read(n)
        if n.startswith("word/") and n.endswith(".xml"):
            s = data.decode("utf-8")
            t = re.sub(r"(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)", lambda m: m.group(1) + gas(m.group(2)) + m.group(3), s)
            if t != s: changed += 1; data = t.encode("utf-8")
        out[n] = (z.getinfo(n), data)
    z.close()
    if changed:
        tmp = p + ".tmp"
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as w:
            for n, (info, data) in out.items(): w.writestr(info, data)
        shutil.move(tmp, p)
    return changed

def fix_xlsx(p):
    import openpyxl
    wb = openpyxl.load_workbook(p); n = 0
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and not c.value.startswith("="):
                    t = fix(c.value)
                    if t != c.value: c.value = t; n += 1
    wb.save(p); return n

if __name__ == "__main__":
    files = glob.glob("registers/*.csv") + glob.glob("company/*.csv") + glob.glob("company/*.md") + glob.glob("company/*.html") + glob.glob("company/org/*.csv") \
        + glob.glob("notes/ONE_Session2_Pack/tools/*.py") + glob.glob("notes/ONE_Session2_Pack/specs/*.py")
    files = [f for f in files if not f.endswith("fictionalise.py")]
    n = sum(fix_text_file(f) for f in files)
    d = 0
    for f in glob.glob("finals/*.docx") + glob.glob("manuals/*.docx"):
        c = fix_docx(f); d += bool(c)
        if c: print("Word file updated:", f)
    x = sum(fix_xlsx(f) for f in glob.glob("company/*.xlsx") + glob.glob("registers/*.xlsx"))
    print(f"{n} text files changed, {d} Word files changed, {x} spreadsheet cells changed")
