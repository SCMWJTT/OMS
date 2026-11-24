import base64, json, sys
sys.path.insert(0, "/home/claude/oms/src")
from elements import ELEMENTS
reg = {"exp": {}, "el": {}}
for el in ELEMENTS:
    reg["el"][el["n"]] = el["title"]
    for e in el["exps"]:
        reg["exp"][e[0]] = e[1]
docx = "/home/claude/audit/manual/ACE-OMS-MAN-001_OMS_Manual_Rev03.docx"
t = open("/home/claude/oms/src/viewer.tpl").read()
jszip = open("/opt/node-tools/node_modules/jszip/dist/jszip.min.js").read().replace("</script", "<\\/script")
t = t.replace("__JSZIP__", jszip).replace("__REGISTRY__", json.dumps(reg)).replace("__DOCX_B64__", base64.b64encode(open(docx, "rb").read()).decode())
open("/home/claude/oms/out/ACE_OMS_Manual_Web.html", "w").write(t)
print(len(t))
