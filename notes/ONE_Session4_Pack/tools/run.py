"""Build policy drafts: python run.py specs/ACE-XXX-POL-001.py ...  -> writes to <repo>/drafts/"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen import build
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "drafts")
os.makedirs(OUT, exist_ok=True)
for f in sys.argv[1:]:
    g = {"__file__": os.path.abspath(f)}
    exec(open(f, encoding="utf-8").read(), g)
    s = g["SPEC"]; m = s["meta"]
    name = s.get("file") or f'{m["DocumentId"]}_{re.sub(r"[^A-Za-z0-9-]+", "_", m["Title"]).strip("_")}_Rev{m["Revision"]}.docx'
    build(s, os.path.join(OUT, name))
    print("built", name)
