import sys, os, re
sys.path.insert(0, "/home/claude/tools"); sys.path.insert(0, "/home/claude/specs")
from gen import build
os.makedirs("/home/claude/build/out", exist_ok=True)
for f in sys.argv[1:]:
    g = {}; exec(open(f).read(), g)
    s = g["SPEC"]; m = s["meta"]
    name = f'{m["DocumentId"]}_{re.sub(r"[^A-Za-z0-9-]+", "_", m["Title"]).strip("_")}_Rev{m["Revision"]}.docx'
    p = build(s, "/home/claude/build/out/" + name)
    print("built", name)
