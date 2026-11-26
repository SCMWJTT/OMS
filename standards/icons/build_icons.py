"""Builds the ONE icon registry (one-icons.json) and the catalogue section of ONE_Icon_Standard.md.

    python standards/icons/build_icons.py

The registry is the single place that maps a ONE concept to its icon. Pages never hard-code a glyph: they ask for a
key (for example "doc.procedure" or "reason.transport") and draw what the registry says. To change an icon or colour,
edit the tables below and run this script; nothing else changes.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = {"name": "Font Awesome Free 6.5.1, solid style", "license": "Icons CC BY 4.0 (attribution kept in the files); fonts SIL OFL 1.1; code MIT",
        "css": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css", "prefix": "fa-solid fa-"}

COLOURS = {
    "elements": {"1": "#0B5563", "2": "#3D4FA1", "3": "#7A4FA0", "4": "#B5427A", "5": "#C8402F", "6": "#E07A1F", "7": "#D6A21E", "8": "#6E9A2E", "9": "#2E9A78", "10": "#2F7FB8"},
    "functions": {"EXEC": "#0B5563", "OPS": "#2F6F8F", "ENP": "#7A5C9E", "WEL": "#8E5B3A", "EXD": "#2E8A78", "SCM": "#B07A1F", "HSE": "#B5473A", "HR": "#6E9A2E",
                  "FIN": "#5B7F3A", "ITD": "#3D4FA1", "BDM": "#A0527A", "LGA": "#57656C", "CCS": "#6B7B83", "CTR": "#7D8D95"},
    "documents": {"POL": "#14275E", "MAN": "#0E4D6E", "STD": "#2648A6", "PRA": "#1D6FA3", "PRC": "#2E8BC9", "WIN": "#5468C4", "FRM": "#3A9AB8", "PLN": "#3F3A9C", "SPC": "#5B7FA6"},
    "families": {"records": "#3B6D11", "data": "#0F7C8C", "systems": "#3D4A55", "external": "#6B5B4E", "value": "#A87A12", "people": "#7A4FA0", "plant": "#D2691E",
                 "materials": "#8E6A2E", "transport": "#8E6A2E", "flow": "#444441"},
    "status": {"waiting": "#E0AE2E", "working": "#0F6E56", "rework": "#C8402F", "blocked": "#C8402F", "overdue": "#BA7517", "effective": "#3B6D11",
               "degraded": "#BA7517", "failed": "#A32D2D", "up": "#3B6D11", "down": "#C8402F"},
}

SHAPES = {
    "circle": "Organisation, external parties, resources and equipment: who and what does the work.",
    "tile": "OMS framework: elements and expectations. Square with small corner radius.",
    "hex": "Management objects: the things the business manages, measures and reports on.",
    "doc": "Artefacts: documents, records, data and systems. Rounded square.",
    "diamond": "Decisions.",
    "mark": "Status marks: small circles laid over another icon or a step. The only place red, amber and green are used.",
}

FAMILIES = [
    ("org", "Organisation", "circle", "function", "The company, its functions, roles, people and sites."),
    ("site", "Sites", "circle", "fixed:#0B5563", "Where the work happens."),
    ("ext", "External parties", "circle", "family:external", "Organisations outside ACE that work passes to or from."),
    ("oms", "OMS framework", "tile", "element", "The ten OMS elements and their expectations."),
    ("mo", "Management objects", "hex", "element", "Opportunities, objectives, processes, requirements, risks, controls, incidents, improvement, compliance and value."),
    ("doc", "Documents", "doc", "document", "Controlled documents. One base glyph; type shown by its blue and its letter badge."),
    ("rec", "Records", "doc", "family:records", "Evidence that work was done. One green; type shown by the badge glyph."),
    ("data", "Data and measurement", "doc", "family:data", "Measures, KPIs, registers and dashboards."),
    ("sys", "Systems", "doc", "family:systems", "Where records and data live."),
    ("res", "Resources", "circle", "own", "People, materials, money, transport and time."),
    ("eq", "Energy equipment", "circle", "family:plant", "Upstream and downstream plant. Most need custom drawing; a generic glyph stands in until then."),
    ("flow", "Flow and decisions", "circle", "family:flow", "Start, end, decision, approval, timer, cycle and what moves between steps."),
    ("reason", "Wait and rework reasons", "circle", "status:waiting", "Why work is waiting or coming back. Used in bottleneck views."),
    ("st", "Status marks", "mark", "status", "Waiting, working, rework, blocked, overdue, effective, degraded, failed, trend."),
]

# key: (name, glyph, colour or None to use the family rule, badge text, badge glyph, needs custom drawing)
I = {}
def add(key, name, glyph, colour=None, badge=None, bglyph=None, custom=False, element=None, shape=None):
    I[key] = {k: v for k, v in dict(name=name, glyph=glyph, colour=colour, badge=badge, badge_glyph=bglyph, custom=custom or None, element=element, shape=shape).items() if v is not None}

# organisation
add("org.company", "Company", "sitemap", "#0B5563")
FN = [("EXEC", "Executive", "user-tie"), ("OPS", "Operations", "industry"), ("ENP", "Engineering & Projects", "gears"), ("WEL", "Wells", "oil-well"),
      ("EXD", "Exploration & Development", "magnifying-glass-location"), ("SCM", "Supply Chain", "truck"), ("HSE", "HSE & Compliance", "helmet-safety"),
      ("HR", "Human Resources", "users"), ("FIN", "Finance", "coins"), ("ITD", "IT, Data & Knowledge", "laptop-code"), ("BDM", "Business Development & Markets", "handshake"),
      ("LGA", "Legal & Government Affairs", "scale-balanced"), ("CCS", "Communications & Corporate Services", "bullhorn"), ("CTR", "Contractors", "user-gear")]
for code, name, g in FN:
    add(f"org.function.{code}", name, "sitemap", COLOURS["functions"][code], bglyph=g)
add("org.role", "Role", "user")
add("org.person", "Person", "user")
add("org.team", "Team", "users")
add("org.contractor", "Contractor", "user-gear", COLOURS["functions"]["CTR"])
# sites
add("site.generic", "Site", "location-dot")
add("site.platform", "Offshore platform", "oil-well", custom=True)
add("site.plant", "Process plant", "industry")
add("site.shorebase", "Shore base / port", "anchor")
add("site.office", "Head office", "building")
add("site.terminal", "Terminal", "warehouse")
add("site.refinery", "Refinery", "industry", custom=True)
add("site.landlease", "Land lease", "map")
# external
add("ext.regulator", "Regulator", "landmark")
add("ext.customer", "Customer / buyer", "handshake")
add("ext.partner", "JV partner", "people-arrows")
add("ext.contractor", "Contractor company", "helmet-safety")
add("ext.community", "Community", "people-roof")
add("ext.supplier", "Supplier", "truck-ramp-box")
# OMS
# element names come from protocol/one-protocol.json so the registry never drifts from the OMS
_P = json.load(open(os.path.join(HERE, "..", "..", "protocol", "one-protocol.json"), encoding="utf-8"))
_G = {1: "flag", 2: "landmark", 3: "people-group", 4: "handshake", 5: "triangle-exclamation", 6: "oil-well", 7: "book", 8: "play", 9: "graduation-cap", 10: "magnifying-glass"}
EL = [(e["id"], e["title"], _G[e["id"]]) for e in _P["elements"]]
for n, name, g in EL:
    add(f"oms.element.{n}", name, g, COLOURS["elements"][str(n)], badge=str(n), element=n)
add("oms.expectation", "OMS expectation", "list-check", "#0B5563")
add("oms.manual", "OMS manual", "book-bookmark", "#0B5563")
# management objects (colour = home element)
for key, name, g, el in [("opportunity", "Business opportunity", "seedling", 2), ("objective", "Objective / target", "bullseye", 2), ("process", "Process", "diagram-project", 7),
                         ("requirement", "Requirement", "list-check", 2), ("hazard", "Hazard", "fire-flame-curved", 5), ("risk", "Risk", "triangle-exclamation", 5),
                         ("control", "Control / barrier", "shield-halved", 5), ("change", "Change (MOC)", "arrows-rotate", 5), ("deviation", "Deviation", "route", 5),
                         ("incident", "Incident / event", "burst", 9), ("action", "Action", "square-check", 9), ("finding", "Audit finding", "circle-exclamation", 10),
                         ("improvement", "Improvement", "arrow-trend-up", 9), ("efficiency", "Efficiency", "gauge-high", 10), ("compliance", "Compliance", "scale-balanced", 2),
                         ("regulation", "Rule / regulation", "gavel", 4), ("licence", "Licence / permit to operate", "certificate", 4), ("idea", "Idea", "lightbulb", 9),
                         ("recognition", "Recognition", "trophy", 3)]:
    add(f"mo.{key}", name, g, COLOURS["elements"][str(el)], element=el)
for key, name, g in [("value", "Value", "sack-dollar"), ("cost", "Cost", "money-bill-wave"), ("benefit", "Benefit", "hand-holding-dollar"), ("revenue", "Revenue", "file-invoice-dollar"),
                     ("profit", "Profit", "chart-line"), ("budget", "Budget", "coins")]:
    add(f"mo.{key}", name, g, COLOURS["families"]["value"])
# documents: one glyph, a blue per type, a letter badge
for code, name, b in [("POL", "Policy", "P"), ("MAN", "Manual", "M"), ("STD", "Standard", "S"), ("PRA", "Practice", "PA"), ("PRC", "Procedure", "PR"),
                      ("WIN", "Work instruction", "WI"), ("FRM", "Form", "F"), ("PLN", "Plan", "PL"), ("SPC", "Specification", "SP")]:
    add(f"doc.{code}", name, "file-lines", COLOURS["documents"][code], badge=b)
add("doc.generic", "Document", "file-lines", "#2648A6")
# records: one green, badge glyph = type
for key, name, bg in [("generic", "Record", None), ("work_order", "Work order", "wrench"), ("permit", "Permit to work", "fire"), ("moc", "MOC record", "arrows-rotate"),
                      ("inspection", "Inspection report", "magnifying-glass"), ("risk_assessment", "Risk assessment", "triangle-exclamation"), ("deferral", "Deferral record", "clock"),
                      ("manifest", "Manifest / booking", "helicopter"), ("training", "Training record", "graduation-cap"), ("certificate", "Certificate", "certificate"),
                      ("review", "Review record", "clipboard-check"), ("anomaly", "Anomaly record", "circle-exclamation")]:
    add(f"rec.{key}", name, "file-circle-check", bglyph=bg)
# data
for key, name, g in [("measure", "Measure / trend", "chart-line"), ("kpi", "KPI", "gauge-high"), ("register", "Register", "database"), ("dataset", "Dataset / table", "table"),
                     ("dashboard", "Dashboard", "chart-pie"), ("reading", "Field reading", "temperature-half"), ("meter", "Meter", "gauge")]:
    add(f"data.{key}", name, g)
# systems
for key, name, bg in [("generic", "System", None), ("cmms", "Maintenance system (CMMS)", "screwdriver-wrench"), ("erp", "ERP / finance system", "coins"),
                      ("docs", "Document system", "folder-open"), ("permit", "Permit system", "fire"), ("moc", "MOC system", "arrows-rotate"), ("rbi", "RBI / inspection software", "magnifying-glass"),
                      ("logistics", "Logistics booking", "helicopter"), ("training", "Training system", "graduation-cap")]:
    add(f"sys.{key}", name, "desktop", bglyph=bg)
# resources
add("res.people", "People", "user-group", COLOURS["families"]["people"])
add("res.competence", "Competence", "id-badge", COLOURS["families"]["people"])
add("res.materials", "Materials", "boxes-stacked", COLOURS["families"]["materials"])
add("res.spares", "Spares / parts", "box", COLOURS["families"]["materials"])
add("res.tools", "Tools and NDT equipment", "toolbox", COLOURS["families"]["materials"])
add("res.vehicle", "Vehicle", "truck", COLOURS["families"]["transport"])
add("res.helicopter", "Helicopter", "helicopter", COLOURS["families"]["transport"])
add("res.vessel", "Vessel", "ship", COLOURS["families"]["transport"])
add("res.money", "Money", "coins", COLOURS["families"]["value"])
add("res.time", "Time", "clock", "#444441")
# energy equipment (custom drawing wanted; generic stand-in shown until then)
for key, name, g, custom in [("well", "Well", "oil-well", False), ("borehole", "Borehole", "bore-hole", False), ("wellhead", "Wellhead / Christmas tree", "oil-well", True),
                             ("platform", "Platform", "tower-observation", True), ("fpso", "FPSO", "ship", True), ("separator", "Separator / vessel", "database", True),
                             ("compressor", "Compressor", "fan", True), ("pump", "Pump", "gears", True), ("pipeline", "Pipeline", "arrow-right-arrow-left", True),
                             ("pig_launcher", "Pig launcher / receiver", "arrow-right-arrow-left", True), ("relief_valve", "Relief valve", "gauge-high", True),
                             ("flare", "Flare", "fire-flame-curved", True), ("tank", "Storage tank", "database", True), ("tank_farm", "Tank farm", "cubes", True),
                             ("column", "Distillation column", "industry", True), ("jetty", "Jetty / tanker berth", "anchor", True), ("loading_rack", "Loading rack", "truck-droplet", True),
                             ("meter_skid", "Metering skid", "gauge", True), ("crane", "Crane", "gears", True), ("process_plant", "Process plant", "industry", False)]:
    add(f"eq.{key}", name, g, custom=custom)
# flow and decisions
add("flow.start", "Start", "play")
add("flow.end", "End", "stop")
add("flow.decision", "Decision", "code-branch", shape="diamond")
add("flow.approval", "Approval", "stamp")
add("flow.timer", "Timer", "clock")
add("flow.cycle", "Cycle", "rotate")
add("flow.handoff", "Hand-off", "people-arrows", "#E07A1F")
add("flow.information", "Information moves", "share-nodes", "#2F7FB8")
add("flow.material", "Material moves", "box", "#8E6A2E")
add("flow.people", "People move", "person-walking", "#7A4FA0")
# wait and rework reasons
for key, name, g in [("resource", "Person or team busy", "user-clock"), ("information", "Waiting for information", "circle-question"), ("approval", "Waiting for approval", "stamp"),
                     ("transport", "Waiting for transport", "helicopter"), ("weather", "Weather", "cloud-showers-heavy"), ("batch", "Held for a batch or campaign", "layer-group"),
                     ("parts", "Waiting for parts", "box-open"), ("window", "Waiting for a work window", "calendar-days"), ("permit", "Waiting for a permit", "file-circle-exclamation"),
                     ("incomplete", "Incomplete or wrong input (rework)", "rotate-left")]:
    add(f"reason.{key}", name, g)
# status marks
for key, name, g in [("waiting", "Waiting", "hourglass-half"), ("working", "Working", "gear"), ("rework", "Rework", "rotate-left"), ("blocked", "Blocked", "ban"),
                     ("overdue", "Overdue", "clock"), ("effective", "Effective", "check"), ("degraded", "Degraded", "minus"), ("failed", "Failed", "xmark"),
                     ("up", "Trend up", "arrow-up"), ("down", "Trend down", "arrow-down")]:
    add(f"st.{key}", name, g, COLOURS["status"][key])

# family rules fill in colour and shape
FAM = {f[0]: f for f in FAMILIES}
for k, v in I.items():
    fam = FAM[k.split(".")[0]]
    v["family"] = fam[0]
    v.setdefault("shape", fam[2])
    if "colour" not in v:
        rule = fam[3]
        if rule.startswith("fixed:"): v["colour"] = rule[6:]
        elif rule.startswith("family:"): v["colour"] = COLOURS["families"][rule[7:]]
        elif rule.startswith("status:"): v["colour"] = COLOURS["status"][rule[7:]]
        else: v["colour"] = "#444441"

reg = {"schema": "ONE-ICONS/1", "version": "1.0", "updated": "2026-11-26", "standard": "standards/icons/ONE_Icon_Standard.md", "base_set": BASE,
       "shapes": SHAPES, "colours": COLOURS, "families": [dict(id=a, name=b, shape=c, colour_rule=d, use=e) for a, b, c, d, e in FAMILIES], "icons": I}
json.dump(reg, open(os.path.join(HERE, "one-icons.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# catalogue section of the standard
rows = []
for fid, fname, shape, rule, use in FAMILIES:
    rows.append(f"\n### {fname} (`{fid}.*`) — {shape}\n\n{use}\n\n| Key | Meaning | Glyph | Colour | Badge |\n|---|---|---|---|---|")
    for k, v in I.items():
        if v["family"] != fid: continue
        b = v.get("badge") or (f"glyph `{v['badge_glyph']}`" if v.get("badge_glyph") else "")
        rows.append(f"| `{k}` | {v['name']}{' *(custom wanted)*' if v.get('custom') else ''} | `{v['glyph']}` | `{v['colour']}` | {b} |")
cat = "\n".join(rows)
md = os.path.join(HERE, "ONE_Icon_Standard.md")
text = open(md, encoding="utf-8").read()
text = re.sub(r"(<!-- CATALOGUE START -->).*(<!-- CATALOGUE END -->)", lambda m: m.group(1) + "\n" + cat + "\n\n" + m.group(2), text, flags=re.S)
open(md, "w", encoding="utf-8").write(text)
print(f"one-icons.json: {len(I)} icons in {len(FAMILIES)} families, {sum(1 for v in I.values() if v.get('custom'))} marked for custom drawing; catalogue written to ONE_Icon_Standard.md")
