"""Issue the Session 4 policy drafts as approved controlled documents (demo):
   python issue.py  -> writes approved files to <repo>/finals/ and moves the superseded copies to <repo>/superseded/"""
import sys, os, re, glob, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen import build
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SPECS = os.path.join(HERE, "..", "specs")
ISSUE, EFFECTIVE = "16 November 2026", "23 November 2026"
REV = {"ACE-LDR-POL-001": "02", "ACE-DOC-POL-001": "02"}
FIRST = {"ACE-LDR-POL-001": ("01", "1 January 2026", "First approved issue; establishes requirements for ONE and all ACE sites."),
         "ACE-DOC-POL-001": ("01", "1 April 2026", "Initial approved issue, released with ACE-OMS-MAN-001 Rev 04 and ACE-DOC-STD-002 Rev 02.")}
os.makedirs(os.path.join(ROOT, "superseded"), exist_ok=True)
done = 0
for f in sorted(glob.glob(os.path.join(SPECS, "*.py"))):
    g = {"__file__": os.path.abspath(f)}
    exec(open(f, encoding="utf-8").read(), g)
    s = g["SPEC"]; m = s["meta"]; doc = m["DocumentId"]
    rev = REV.get(doc, "01")
    m.update(Revision=rev, Status="Approved", IssueDate=ISSUE, EffectiveDate=EFFECTIVE)
    s["label"] = "ACE  /  LEVEL 1 POLICY  /  APPROVED CONTROLLED DOCUMENT"
    s.pop("cover_note", None)
    hist = [FIRST[doc]] if doc in FIRST else []
    what = [h[2] for h in s["history"] if h[0] not in ("01",)][-1]
    what = re.sub(r"^Draft for Rev 02: ", "", what).replace(" Proposed effective date 1 January 2027.", "").replace("Initial draft for review.", "Initial approved issue.")
    hist.append((rev, EFFECTIVE, what[0].upper() + what[1:]))
    s["history"] = hist
    name = re.sub(r"_Rev[A-Z]\.docx$", f"_Rev{rev}.docx", s["file"])
    for old in glob.glob(os.path.join(ROOT, "finals", f"{doc}_*.docx")):
        if os.path.basename(old) != name:
            shutil.move(old, os.path.join(ROOT, "superseded", os.path.basename(old)) if re.search(r"_Rev\d\d\.docx$", old) else old + ".del")
    build(s, os.path.join(ROOT, "finals", name))
    done += 1
    print("issued", name)
for x in glob.glob(os.path.join(ROOT, "finals", "*.del")): os.remove(x)
print(f"{done} policies issued as Approved, effective {EFFECTIVE}")
