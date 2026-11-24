"""Generates the ACE data-spine registers (fictional, seeded) into registers/.
Run from the repo root:  python3 notes/ONE_Session2_Pack/tools/gen_registers.py
Everything links by ID to the documents in finals/ and to company/ACE_People.csv."""
import csv, glob, os, re, random, zipfile, datetime as dt, math, collections
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regdata import ASSETS, RISKS, OBJECTIVES, OPPORTUNITIES, PROCESSES, PLANNED_CONTROLS, ADJUST

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.join(ROOT, "registers")
rnd = random.Random(20261124)
TODAY = dt.date(2026, 11, 24)
D = lambda s: dt.date.fromisoformat(s)
PEOPLE = {r["Full Name"]: r for r in csv.DictReader(open(os.path.join(ROOT, "company/ACE_People.csv"), encoding="utf-8-sig"))}
who = lambda n: f"{n} — {PEOPLE[n]['Job Title']}"
MONTHS = "January February March April May June July August September October November December".split()

def write(name, rows, cols):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in rows: w.writerow({c: r.get(c, "") for c in cols})
    print(f"  {name}: {len(rows)} rows")

# ---------------- ACE Risk Matrix (ACE-RSK-STD-001 §3.1)
MATRIX = {"E": "MHHVV", "D": "MMHHV", "C": "LMMHH", "B": "LLMMH", "A": "LLLMM"}
BAND = {"L": "Low", "M": "Medium", "H": "High", "V": "Very High"}
rating = lambda L, C: BAND[MATRIX[L][C - 1]]
AUTH = {"Low": "Accountable Supervisor or L4 Lead", "Medium": "Function Manager / Area Authority (L3)",
        "High": "Relevant Vice President (L2)", "Very High": "Chief Executive Officer (L1)"}
REVIEW = {"Low": "Annually", "Medium": "Quarterly", "High": "Quarterly or more often", "Very High": "Daily while exposure remains"}
SYS_VP = {"AIM": "Dev Jaggernauth", "PSM": "George Habib", "WEL": "Joanne Ho Sing", "OPS": "Sophia Hosany", "MNT": "Sophia Hosany",
          "COW": "Sophia Hosany", "LOG": "Sasha George", "ENG": "Dev Jaggernauth", "HMA": "Karen Jack", "ENV": "George Habib",
          "SEC": "George Habib", "STK": "Rodney Garcia", "EMR": "George Habib", "LEG": "Sharda Bissoon", "PPL": "Adrian Achong",
          "PRF": "Teresa Daniel", "CON": "Sasha George", "OMS": "George Habib", "MOC": "Dev Jaggernauth", "OHH": "George Habib"}
LEGACY_DOCS = {"PSM": "ACE-PSM-STD-001", "OPS": "ACE-OPS-STD-001", "AIM": "ACE-AIM-STD-001", "WEL": "ACE-WEL-STD-001",
               "MNT": "ACE-MNT-STD-001", "COW": "ACE-COW-STD-001", "EMR": "ACE-EMR-STD-001", "CON": "ACE-CON-STD-001",
               "MOC": "ACE-MOC-PRC-001", "PRF": "ACE-PRF-STD-002", "OMS": "ACE-OMS-STD-002", "ENG": "ACE-ENG-STD-901", "PPL": "ACE-PPL-STD-003"}

# ---------------- read controls and dates from the documents
def read_docs():
    docs, ctrls = {}, {}
    for f in sorted(glob.glob(os.path.join(ROOT, "finals/*.docx")) + glob.glob(os.path.join(ROOT, "manuals/*.docx"))):
        z = zipfile.ZipFile(f); d = z.read("word/document.xml").decode()
        props = dict(re.findall(r'name="ODS\.([^"]+)"[^>]*>\s*<vt:\w+>([^<]*)<', z.read("docProps/custom.xml").decode()))
        did = props["DocumentId"]; eff = dt.datetime.strptime(props["EffectiveDate"], "%d %B %Y").date()
        docs[did] = dict(title=props["Title"], effective=eff, revision=props["Revision"], type=props["DocumentType"])
        sect = ""
        for p in re.findall(r"<w:p[ >].*?</w:p>", d, re.S):
            if re.search(r'pStyle w:val="Heading[12]"', p):
                m = re.search(r'w:name="([^"]+)"', p); sect = m.group(1) if m else sect
            for cid in re.findall(r'<w:tag w:val="ODS\.Control@(C-[A-Z]{3}-\d{3})"', p):
                ctrls.setdefault(cid, dict(doc=did, bookmark=sect, effective=eff))
        for tbl in re.findall(r"<w:tbl>.*?</w:tbl>", d, re.S):
            rows = [[re.sub(r"\s+", " ", "".join(re.findall(r"<w:t[^>]*>([^<]*)", c))).strip().replace("&amp;", "&")
                     for c in re.findall(r"<w:tc>.*?</w:tc>", r, re.S)] for r in re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S)]
            if rows and rows[0] and rows[0][0] == "Control ID":
                for r in rows[1:]:
                    if r[0] in ctrls: ctrls[r[0]].update(statement=r[1], threat=r[2], step=r[4], evidence=r[5])
    return docs, ctrls

DOCS, CTRL = read_docs()
print(f"read {len(DOCS)} documents, {len(CTRL)} Control IDs")

# ---------------- assets and SCEs
assets, aid = [], {}
cnt = collections.Counter()
for site, tag, title, cls, crit, sce, parent in ASSETS:
    cnt[site] += 1; a = f"A-{site}-{cnt[site]:03d}"; aid[tag] = a
    assets.append(dict(asset_id=a, tag=tag, title=title, site=site, parent_id=parent, iso14224_class=cls, criticality=crit,
                       sce="Yes" if sce else "No", in_service=f"{rnd.choice([1978, 1985, 1992, 1998, 2004, 2009, 2013, 2017])}-01-01"))
for a in assets: a["parent_id"] = aid.get(a["parent_id"], "") if a["parent_id"] else ""
sces, sid = [], {}
scnt = collections.Counter()
INTERVAL = {"ESD": "6 months", "F&G": "6 months", "PSV": "24 months", "SIS": "12 months", "Pipeline": "12 months", "Firewater": "1 month",
            "Lifesaving": "3 months", "Well barrier": "6 months", "Structural": "48 months", "Helideck": "12 months", "Navigation aid": "1 month",
            "Containment": "12 months", "Spill response": "1 month"}
for site, tag, title, cls, crit, sce, parent in ASSETS:
    if not sce: continue
    scnt[site] += 1; s = f"SCE-{site}-{scnt[site]:03d}"; sid[tag] = s
    iv = int(INTERVAL[sce].split()[0]); last = TODAY - dt.timedelta(days=rnd.randint(5, iv * 28))
    nxt = last + dt.timedelta(days=iv * 30)
    sces.append(dict(sce_id=s, title=title, group=sce, site=site, asset_ids=aid[tag], performance_standard=f"PS-{sce.upper().replace(' ', '')[:6]}-{scnt[site]:02d}",
                     test_interval=INTERVAL[sce], last_test=last.isoformat(), next_due=nxt.isoformat(),
                     status="Available" if nxt >= TODAY else "Deviation", controls=""))

# ---------------- risks
rcnt = collections.Counter(); risks = []
for (site, level, sys_, title, hazard, top, threats, cons, owner, cdom, L, (resC, resL), atag, obj, proc) in RISKS:
    rcnt[site] += 1; rid = f"R-{site}-{rcnt[site]:02d}"
    if rid in ADJUST:
        a_c, a_l, a_r = ADJUST[rid]; cdom = a_c or cdom; L = a_l or L
        if a_r: resC, resL = a_r
    C = max(cdom); cur = rating(L, C); res = rating(resL, resC); vp = SYS_VP[sys_]
    r = dict(risk_id=rid, level=level, title=title, site=site, system=sys_, asset_id=aid.get(atag, ""), process=proc or "",
             hazard=hazard, top_event=top, threats=threats, consequences=cons, owner=who(owner), escalation_vp=who(vp),
             c_people=cdom[0], c_environment=cdom[1], c_asset=cdom[2], c_reputation=cdom[3], current_c=C, current_l=L, current_rating=cur,
             alarp_status="ALARP demonstrated" if cur in ("Low", "Medium") else "ALARP case in progress",
             residual_c=resC, residual_l=resL, residual_rating=res,
             acceptance_authority=(who(vp) if cur == "High" else AUTH[cur]), review_frequency=REVIEW[cur],
             objective_id=obj, controls="", legacy_control_docs="", version="1")
    risks.append(r)
RID = {r["title"]: r["risk_id"] for r in risks}
def rid_of(prefix): return next(r["risk_id"] for r in risks if r["risk_id"] == prefix)

# control → risk mapping (by ID)
MAP = {}
def m(ids, risk):
    for i in ids: MAP[i] = risk
m(["C-AIM-001", "C-AIM-003", "C-AIM-004", "C-AIM-005", "C-AIM-006"], "R-PAP-01"); m(["C-AIM-002", "C-AIM-008"], "R-SAP-01")
m(["C-AIM-007"], "R-LND-02"); m(["C-AIM-009", "C-AIM-010"], "R-PAP-05")
m(["C-MNT-001", "C-MNT-002"], "R-HOF-14"); m(["C-MNT-003", "C-MNT-006", "C-MNT-007"], "R-PAP-06")
m(["C-MNT-004", "C-MNT-005", "C-MNT-010"], "R-CPF-01"); m(["C-MNT-008", "C-MNT-009"], "R-CPF-04")
m(["C-OPS-001", "C-OPS-004", "C-OPS-007", "C-OPS-008"], "R-CPF-03"); m(["C-OPS-002", "C-OPS-003"], "R-CPF-01")
m(["C-OPS-005"], "R-CPF-04"); m(["C-OPS-006"], "R-PAP-02"); m(["C-OPS-009"], "R-HOF-09"); m(["C-OPS-010", "C-OPS-011", "C-OPS-012"], "R-PAP-01")
m(["C-WEL-001", "C-WEL-002", "C-WEL-003", "C-WEL-005", "C-WEL-009", "C-WEL-010"], "R-PAP-03"); m(["C-WEL-004", "C-WEL-011", "C-WEL-012"], "R-CHB-02")
m(["C-WEL-006", "C-WEL-007", "C-WEL-008"], "R-LND-01")
m(["C-COW-001", "C-COW-002", "C-COW-005"], "R-PAP-07"); m(["C-COW-009"], "R-HOF-07"); m(["C-COW-018"], "R-HOF-09")
m([f"C-COW-{i:03d}" for i in (3, 4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19)], "R-PAP-08")
m([c for c in CTRL if c.startswith("C-BPM")], "R-HOF-08"); MAP["C-BPM-044"] = "R-HOF-09"
m(["C-RSK-001", "C-RSK-002", "C-RSK-003", "C-RSK-007", "C-RSK-008", "C-RSK-009"], "R-HOF-14"); m(["C-RSK-004", "C-RSK-005", "C-RSK-006"], "R-HOF-08")
m(["C-RSK-010"], "R-HOF-10"); m(["C-RSK-011"], "R-PAP-01"); m(["C-RSK-012"], "R-PLB-04")
PMAP = {"C-LOG-001": "R-CHB-01", "C-LOG-002": "R-PAP-01", "C-LOG-003": "R-PLB-01", "C-LOG-004": "R-PAP-04", "C-HMA-001": "R-CPF-05",
        "C-HMA-002": "R-CPF-05", "C-HMA-003": "R-CPF-05", "C-SEC-001": "R-HOF-01", "C-SEC-002": "R-LND-03", "C-EMR-001": "R-PLB-04",
        "C-ENV-001": "R-CPF-06", "C-OHH-001": "R-HOF-13"}
missing = [c for c in CTRL if c not in MAP]
assert not missing, missing

POS = lambda st: "Mitigating" if re.search(r"spill|response|shutdown|ESD|notif|escalat|secured|patrol|leak", st, re.I) else "Preventive"
NAT = lambda st: "Hard" if re.search(r"ESD|valve|alarm|trip|lock|SIF|bypass|display", st, re.I) else ("People" if re.search(r"brief|train|competen|crew|patrol", st, re.I) else "Soft")
CRIT_RISK = {r["risk_id"] for r in risks if r["current_c"] >= 4}
OWN = {"AIM": "Wayne Rajkumar", "MNT": "Nadira Ramsaran", "OPS": "Michelle de Verteuil", "WEL": "Shalini Jaggernauth", "COW": "Adrian Rodriguez",
       "BPM": "Kwame Henry", "RSK": "Stephanie Boissiere", "LOG": "Sarita Sookram", "HMA": "Navin Sookdeo", "SEC": "Kevin Mohammed",
       "EMR": "Jenelle Paul", "ENV": "Kevin Lutchman", "OHH": "Karishma Ramcharan"}
SPEC_OWN = {"C-OPS-012": "Rajesh Ramsaran", "C-AIM-005": "Sophia de Souza", "C-AIM-006": "Allison Mitchell", "C-RSK-011": "Akilah Noel",
            "C-RSK-012": "Jenelle Paul", "C-COW-019": "Sunita Seepersad", "C-OPS-005": "Vijay Ramcharan", "C-AIM-004": "Wayne Rajkumar"}
STEP_PRS = {"AIM": "ACE-AIM-PRS-001", "OPS": "ACE-OPS-PRS-001", "WEL": "ACE-WEL-PRS-001", "MNT": "ACE-MNT-PRS-001", "COW": "ACE-COW-PRS-001",
            "BPM": "ACE-BPM-PRS-001", "RSK": "ACE-RSK-PRS-001"}
LINKED_STEPS = {"C-OPS-009": "ACE-MOC-PRS-001#S02", "C-BPM-044": "ACE-MOC-PRS-001#S02", "C-BPM-045": "ACE-MOC-PRS-001#S10"}
SCE_FOR = {"C-RSK-011": "SDV-1001", "C-MNT-008": "SIS-CPF", "C-MNT-009": "SIS-CPF", "C-OPS-005": "SIS-CPF", "C-MNT-003": "P-1700A",
           "C-MNT-006": "P-1700A", "C-MNT-007": "P-1700A", "C-RSK-012": "OSR-KIT", "C-AIM-006": "PL-101", "C-WEL-006": "SOU-W15",
           "C-WEL-001": "PAP-W03", "C-WEL-011": "CHB-W02"}
ASSET_FOR = {"C-OPS-012": "X-1500", "C-AIM-005": "X-1500", "C-AIM-004": "PL-101", "C-AIM-001": "PL-101", "C-OPS-001": "DCS-CPF"}

controls = []
for cid, c in sorted(CTRL.items()):
    sys_ = cid.split("-")[1]; st = c.get("statement", ""); risk = MAP[cid]
    controls.append(dict(control_id=cid, statement=st, position=POS(st), nature=NAT(st), critical="Yes" if risk in CRIT_RISK and NAT(st) != "Soft" or cid in SCE_FOR else "No",
                         risk_id=risk, threat=c.get("threat", ""), barrier="", doc_ref=f"{c['doc']}#{c['bookmark']}",
                         process_step=LINKED_STEPS.get(cid, ""), process_planned=STEP_PRS.get(sys_, ""), owner=who(SPEC_OWN.get(cid, OWN[sys_])),
                         asset_id=aid.get(ASSET_FOR.get(cid, SCE_FOR.get(cid, "")), ""), sce_id=sid.get(SCE_FOR.get(cid, ""), ""),
                         evidence=c.get("evidence", ""), test_interval=rnd.choice(["1 month", "3 months", "6 months", "12 months"]),
                         effective=c["effective"].isoformat(), status="Active"))
for cid, st, pos, nat, crit, threat, doc in PLANNED_CONTROLS:
    controls.append(dict(control_id=cid, statement=st, position=pos, nature=nat, critical=crit, risk_id=PMAP[cid], threat=threat, barrier="",
                         doc_ref=f"{doc} (planned)", process_step="", process_planned="", owner=who(OWN[cid.split('-')[1]]),
                         asset_id="", sce_id="", evidence="", test_interval="", effective="", status="Planned"))
CBY = {c["control_id"]: c for c in controls}
BARRIER = {"C-OPS-012": "Inhibitor injection within IOW", "C-AIM-005": "Inhibitor delivery verification", "C-AIM-001": "Corrosion monitoring and RBI",
           "C-AIM-004": "Intelligent pigging on interval", "C-AIM-006": "Pipeline patrol and leak detection", "C-LOG-002": "Pipeline patrol and leak detection",
           "C-RSK-011": "Emergency shutdown and isolation", "C-RSK-012": "Oil spill response", "C-OPS-010": "IOW review", "C-OPS-011": "IOW review"}
for k, v in BARRIER.items(): CBY[k]["barrier"] = v
for r in risks:
    r["controls"] = "; ".join(c["control_id"] for c in controls if c["risk_id"] == r["risk_id"])
    if not any(c["risk_id"] == r["risk_id"] and c["status"] == "Active" for c in controls):
        r["legacy_control_docs"] = LEGACY_DOCS.get(r["system"], "")
for s in sces:
    s["controls"] = "; ".join(c["control_id"] for c in controls if c["sce_id"] == s["sce_id"])

# ---------------- events 2024-01-01 .. 2026-11-23
SITES = ["PAP", "CHB", "SAP", "CPF", "LND", "PLB", "HOF"]
W = {"PAP": 26, "CHB": 5, "SAP": 4, "CPF": 25, "LND": 28, "PLB": 9, "HOF": 3}
RATE = {"Near miss": 15, "First aid": 2.0, "Medical treatment": 0.25, "Restricted work": 0.12, "Lost time injury": 0.07,
        "PSE Tier 3": 2.5, "PSE Tier 2": 0.18, "Spill": 0.7, "SCE test failure": 1.2, "Security": 0.6, "Environmental exceedance": 0.25,
        "Vehicle incident": 0.3, "Audit finding": 0}
TXT = {
 "Near miss": ["Dropped object from scaffold, exclusion zone held", "Unsecured load on forklift at laydown", "Worker entered barricaded area without permit",
               "Gas test missed before hot work; stopped by supervisor", "Wrong valve opened during line-up; corrected before flow",
               "Slip on wet deck near stairway", "Vehicle reversed without banksman", "Hose whip during pressure test, no one injured",
               "Isolation lock found missing during shift handover", "Crane lift close to process piping"],
 "First aid": ["Hand laceration during maintenance", "Insect sting during lease inspection", "Eye irritation from dust", "Minor burn from hot surface", "Bruised shin on stairway"],
 "Medical treatment": ["Finger injury requiring stitches", "Chemical splash to forearm treated at clinic", "Back strain requiring physiotherapy"],
 "Restricted work": ["Sprained ankle stepping off vessel", "Shoulder strain during valve operation"],
 "Lost time injury": ["Fractured wrist after fall from ladder", "Crush injury to hand during pipe handling"],
 "PSE Tier 3": ["Safety valve lifted during upset", "Trip on high level, plant secured", "Small gas release from instrument fitting", "ESD demand during compressor trip"],
 "PSE Tier 2": ["Gas release from compressor seal above Tier 2 threshold", "Crude release from flange during start-up"],
 "Spill": ["Crude spill from tank battery drain valve", "Oily water overflow at gathering station", "Hydraulic oil leak on deck, contained", "Diesel spill during refuelling"],
 "SCE test failure": ["Fire and gas detector failed function test", "ESD valve closure time out of specification", "PSV popped below set pressure on bench test",
                      "Firewater pump failed to start on test", "Lifeboat release hook defect found"],
 "Security": ["Hot-tap found on land trunkline", "Fence cut at gathering station", "Valve tampering at well pad"],
 "Environmental exceedance": ["Oil-in-water above discharge limit for one sample", "Flare smoke observed above permit duration"],
 "Vehicle incident": ["Minor collision on lease access road", "Vehicle rollover into drain, no injury"],
}
RISK_FOR = {
 ("Near miss", "PAP"): ["R-PAP-07", "R-PAP-08"], ("Near miss", "CPF"): ["R-CPF-01"], ("Near miss", "LND"): ["R-LND-04", "R-LND-06"],
 ("Near miss", "PLB"): ["R-PLB-03"], ("Near miss", "CHB"): ["R-CHB-01"], ("Near miss", "SAP"): ["R-CHB-01"],
 ("PSE Tier 3", "PAP"): ["R-PAP-02"], ("PSE Tier 3", "CPF"): ["R-CPF-01", "R-CPF-03"], ("PSE Tier 2", "CPF"): ["R-CPF-01"], ("PSE Tier 2", "PAP"): ["R-PAP-02"],
 ("Spill", "LND"): ["R-LND-02"], ("Spill", "CPF"): ["R-CPF-02"], ("Security", "LND"): ["R-LND-03"], ("Vehicle incident", "LND"): ["R-LND-04"],
 ("Environmental exceedance", "CPF"): ["R-CPF-06", "R-CPF-07"], ("SCE test failure", "PAP"): ["R-PAP-06"], ("SCE test failure", "CPF"): ["R-CPF-04"],
}
SEV = {"Near miss": 1, "First aid": 1, "Medical treatment": 2, "Restricted work": 2, "Lost time injury": 3, "PSE Tier 3": 1, "PSE Tier 2": 3,
       "Spill": 1, "SCE test failure": 2, "Security": 2, "Environmental exceedance": 2, "Vehicle incident": 1, "Audit finding": 2}
SITE_TYPES = {"Security": ["LND"], "Vehicle incident": ["LND", "CPF", "PLB"], "Environmental exceedance": ["CPF", "PAP"],
              "PSE Tier 2": ["CPF", "PAP"], "PSE Tier 3": ["CPF", "PAP", "LND"], "SCE test failure": ["PAP", "CPF", "CHB", "SAP"],
              "Spill": ["LND", "CPF", "PAP", "PLB"]}
PROC_FOR = {"PSE Tier 2": "ACE-INC-PRS-001", "PSE Tier 3": "ACE-INC-PRS-001", "SCE test failure": "ACE-MNT-PRS-002"}

def poisson(lam):
    Lx, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rnd.random()
        if p <= Lx: return k
        k += 1

events = []
def ev(date, site, typ, title, sev, risks_=(), tested=(), failed=(), procs=(), spill_bbl="", pse="", note=""):
    events.append(dict(date=date if isinstance(date, str) else date.isoformat(), site=site, type=typ, title=title, severity=sev,
                       risk_ids="; ".join(risks_), controls_tested="; ".join(tested), controls_failed="; ".join(failed),
                       processes="; ".join(procs), spill_bbl=spill_bbl, pse_tier=pse, notes=note))

def active(cid, date): c = CBY.get(cid); return c and c["status"] == "Active" and c["effective"] and D(c["effective"]) <= date
month = dt.date(2024, 1, 1)
while month <= dt.date(2026, 11, 1):
    last = (month.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    if month.year == 2026 and month.month == 11: last = dt.date(2026, 11, 23)
    for typ, lam in RATE.items():
        n = poisson(lam * (last.day / 30))
        for _ in range(n):
            site = rnd.choice(SITE_TYPES.get(typ, rnd.choices(SITES, weights=[W[s] for s in SITES], k=1)))
            day = month + dt.timedelta(days=rnd.randint(0, (last - month).days))
            risks_ = RISK_FOR.get((typ, site), [])[:1] if rnd.random() < 0.8 else []
            tested, failed = [], []
            if typ == "SCE test failure" and active("C-MNT-009", day) and site == "CPF": failed = ["C-MNT-009"]
            if typ == "Near miss" and site == "PAP" and active("C-COW-013", day) and rnd.random() < 0.15: tested = ["C-COW-013"]
            if typ == "Near miss" and active("C-COW-006", day) and rnd.random() < 0.1: tested = ["C-COW-006"]
            ev(day, site, typ, rnd.choice(TXT[typ]), SEV[typ], risks_, tested, failed, [PROC_FOR[typ]] if typ in PROC_FOR else [],
               spill_bbl=round(rnd.uniform(0.1, 4.5), 1) if typ == "Spill" else "", pse={"PSE Tier 3": "3", "PSE Tier 2": "2"}.get(typ, ""))
    month = (month.replace(day=28) + dt.timedelta(days=4)).replace(day=1)

# audits: findings clustered in audit months
AUDITS = [("2024-05-15", "CPF", "Process safety audit"), ("2024-10-09", "PAP", "Offshore HSE audit"), ("2025-03-19", "LND", "Land operations audit"),
          ("2025-06-11", "HOF", "Document control audit"), ("2025-10-22", "CPF", "Alarm management audit"), ("2026-02-25", "PAP", "Integrity management audit"),
          ("2026-05-20", "HOF", "OMS conformance assessment (ONE launch)"), ("2026-09-16", "PAP", "Post-incident integrity audit")]
FIND = ["Procedure past review date in use at site", "Permit sample missing gas test record", "SCE test record incomplete", "Training record expired for operator",
        "Inspection deferral without expiry date", "Bypass log not reconciled", "MOC closed without document updates", "Emergency drill not held at planned frequency"]
for d_, site, name in AUDITS:
    for i in range(rnd.randint(4, 8)):
        f = rnd.choice(FIND)
        ev(D(d_) + dt.timedelta(days=i % 3), site, "Audit finding", f"{name}: {f}", 2, ["R-HOF-10"], procs=["ACE-PRF-PRS-001"])

# ---- storylines (fixed)
ev("2024-03-12", "CHB", "Near miss", "Technician slipped on Chenet B boat landing ladder during transfer; held by fall arrest", 3, ["R-CHB-01"], note="Storyline: boat transfer")
ev("2024-07-01", "PAP", "Weather shut-in", "Tropical storm warning: precautionary shut-in of Gulf of Paria platforms for 2 days", 2, ["R-HOF-12"])
ev("2024-09-17", "CPF", "PSE Tier 2", "Gas release from K-2301 compressor dry gas seal; unit tripped and blown down", 3, ["R-CPF-01"], pse="2", procs=["ACE-INC-PRS-001"])
for d_, n in [("2025-02-11", 340), ("2025-03-27", 410), ("2025-05-06", 290)]:
    ev(d_, "CPF", "PSE Tier 3", f"Alarm flood: {n} alarms in 10 minutes during compressor trip; operator missed low-level alarm on V-2100", 2, ["R-CPF-03"], pse="3", note="Storyline: CPF alarm flood")
ev("2025-08-20", "CPF", "Measurement error", "NGC sales gas meter found reading 1.3% low after flow computer update in May", 3, ["R-CPF-05", "R-HOF-02"], note="Storyline: NGC meter mismeasurement")
ev("2025-11-05", "LND", "Well integrity", "SOU-15 A-annulus pressure above MAASP; well shut in and placed in Orange category", 3, ["R-LND-01"], note="Storyline: land annulus pressure")
for d_ in ["2026-03-09", "2026-04-06", "2026-05-11"]:
    ev(d_, "PAP", "IOW excursion", "Corrosion inhibitor injection on X-1500 below operating window for more than 72 hours", 2, ["R-PAP-01"], note="Storyline: Pommerac A corrosion")
ev("2026-04-15", "PAP", "Deviation", "Intelligent pigging of PL-101 deferred (vessel unavailable); deferral approved without expiry or interim safeguards", 2, ["R-PAP-01"], note="Storyline: Pommerac A corrosion")
ev("2026-06-24", "PAP", "Review finding", "First quarterly IOW review: sustained inhibitor under-delivery March–May on X-1500", 2, ["R-PAP-01"], tested=["C-OPS-010"], failed=["C-OPS-012", "C-AIM-005"], procs=["ACE-OPS-PRS-001"], note="Storyline")
ev("2026-07-14", "PAP", "Near miss", "Pinhole leak found on PL-101 during monthly boat patrol; 0.3 bbl sheen; line shut in and clamped", 4, ["R-PAP-01"],
   tested=["C-AIM-006", "C-RSK-011"], failed=["C-AIM-005", "C-OPS-012", "C-AIM-004"], procs=["ACE-AIM-PRS-001", "ACE-INC-PRS-001"], spill_bbl=0.3, pse="3", note="Storyline: Pommerac A near miss")
ev("2026-08-11", "PAP", "MOC", "MOC-2026-047 raised: revise inhibitor IOW, pigging interval and deferral rule for PL-101", 1, ["R-PAP-01"], tested=["C-OPS-009"], procs=["ACE-MOC-PRS-001"], note="Storyline")
ev("2026-09-12", "PAP", "Inspection", "Intelligent pigging of PL-101 completed; 14 internal metal-loss features, two above 40% wall", 2, ["R-PAP-01"], tested=["C-AIM-004"], procs=["ACE-AIM-PRS-001"], note="Storyline")
ev("2026-09-03", "SAP", "Missed visit", "Sapodilla C barrier test overdue after two cancelled boat trips (weather)", 2, ["R-CHB-02"], failed=["C-WEL-011"], note="Unmanned platform access")
ev("2026-10-08", "PAP", "SCE test failure", "Firewater pump P-1700B failed to start on weekly test; deviation raised late", 3, ["R-PAP-06"], failed=["C-MNT-007"], procs=["ACE-MNT-PRS-002"])

events.sort(key=lambda e: e["date"])
ycnt = collections.Counter()
for e in events:
    y = e["date"][:4]; ycnt[y] += 1; e["event_id"] = f"EV-{y}-{ycnt[y]:03d}"

# ---------------- actions
OWNERS_SITE = {"PAP": ["Roger Ramkissoon", "Winston Granger"], "CHB": ["Arjun Gittens"], "SAP": ["Arjun Gittens"], "CPF": ["Rohan Ali"],
               "LND": ["Luis de Verteuil"], "PLB": ["Lisa Williams"], "HOF": ["Dillon Haddad", "Marissa Bobb", "Sanjay Jagessar"]}
actions = []; acnt = collections.Counter()
def act(e, title, owner, due, closed, result=""):
    y = e["date"][:4]; acnt[y] += 1
    actions.append(dict(action_id=f"ACT-{y}-{acnt[y]:03d}", event_id=e["event_id"], title=title, owner=who(owner), due=due.isoformat(),
                        closed=closed.isoformat() if closed else "", result=result))
GENERIC = ["Brief crews on the lesson learned", "Update task risk assessment", "Repair and re-test the equipment", "Revise the local work instruction",
           "Verify barrier restored and record evidence", "Close gap in training records"]
for e in events:
    if e["notes"].startswith("Storyline") or e["type"] in ("MOC", "Inspection"): continue
    if e["severity"] >= 2 or e["type"] in ("Audit finding", "SCE test failure"):
        d0 = D(e["date"])
        for _ in range(1 if e["severity"] < 3 else 2):
            due = d0 + dt.timedelta(days=rnd.choice([30, 45, 60, 90]))
            age = (TODAY - d0).days
            pclose = 0.97 if age > 365 else 0.85 if age > 150 else 0.55
            closed = None
            if rnd.random() < pclose:
                closed = min(due + dt.timedelta(days=rnd.randint(-20, 35)), TODAY - dt.timedelta(days=1))
                closed = max(closed, d0 + dt.timedelta(days=3))
            act(e, rnd.choice(GENERIC), rnd.choice(OWNERS_SITE[e["site"]]), due, closed)
E = {e["title"][:40]: e for e in events}
def evt(prefix): return next(e for e in events if e["title"].startswith(prefix))
leak = evt("Pinhole leak found on PL-101")
act(leak, "Investigate the PL-101 near miss (root cause analysis)", "Christina Bain", D("2026-08-14"), D("2026-08-21"), "Investigation report INV-2026-011")
act(leak, "Run intelligent pigging on PL-101", "Allison Mitchell", D("2026-09-30"), D("2026-09-12"), "ILI report")
act(leak, "Install low-flow alarm on X-1500 inhibitor injection", "Vijay Ramcharan", D("2026-10-15"), D("2026-10-09"), "MOC-2026-047")
act(leak, "Revise ACE-OPS-PRA-001: inhibitor IOW and daily verification", "Michelle de Verteuil", D("2026-12-01"), None, "ACE-OPS-PRA-001 Rev 02 (drafting)")
act(leak, "Revise ACE-AIM-PRA-001: deferral rule and ILI interval", "Rochelle Mark", D("2026-12-01"), None, "ACE-AIM-PRA-001 Rev 02 (drafting)")
act(leak, "Revise ACE-AIM-STD-001 to require deferral expiry dates", "Wayne Rajkumar", D("2026-12-01"), None, "ACE-AIM-STD-001 Rev 02 (drafting)")
act(leak, "Repair the two PL-101 features above 40% wall loss", "Allison Mitchell", D("2026-12-15"), None, "Repair work orders")
act(evt("Alarm flood: 410"), "Alarm rationalisation of CPF compressor and inlet sections", "Vijay Ramcharan", D("2025-09-30"), D("2025-11-28"), "Alarm rationalisation report")
act(evt("NGC sales gas meter found"), "Correct flow computer and agree volume adjustment with NGC", "Navin Sookdeo", D("2025-09-30"), D("2025-10-17"), "Adjustment agreed with NGC")
act(evt("SOU-15 A-annulus"), "Rig workover to replace SOU-15 tubing", "Nazim Bailey", D("2026-03-31"), D("2026-04-22"), "Workover report")
act(evt("Firewater pump P-1700B"), "Repair P-1700B starter and re-test", "Marc Gomes", D("2026-10-22"), D("2026-10-19"), "Work order closed")
act(evt("Sapodilla C barrier test overdue"), "Complete overdue barrier tests at Sapodilla C", "Shalini Jaggernauth", D("2026-09-30"), D("2026-09-26"), "Barrier test record")

# ---------------- control health history and current health
health = []
def h(cid, date, val, eid="", note=""): health.append(dict(control_id=cid, date=date, health=val, event_id=eid, note=note))
for c in controls:
    if c["status"] != "Active": continue
    e0 = D(c["effective"])
    h(c["control_id"], e0.isoformat(), "Not tested", note="Document effective")
    t = e0 + dt.timedelta(days=rnd.randint(20, 75))
    if t < TODAY: h(c["control_id"], t.isoformat(), "Effective" if rnd.random() > 0.08 else "Degraded", note="First test or sample")
for e in events:
    for cid in filter(None, e["controls_failed"].split("; ")):
        if cid in CBY and CBY[cid]["status"] == "Active": h(cid, e["date"], "Failed" if e["severity"] >= 3 else "Degraded", e["event_id"], e["title"][:60])
    for cid in filter(None, e["controls_tested"].split("; ")):
        if cid in CBY and CBY[cid]["status"] == "Active": h(cid, e["date"], "Effective", e["event_id"], "Worked when tested")
h("C-OPS-012", "2026-10-01", "Effective", note="Low-flow alarm installed; daily verification in place")
h("C-AIM-005", "2026-10-01", "Effective", note="Weekly verification restored")
h("C-AIM-004", "2026-10-01", "Degraded", note="ILI done; deferral rule revision pending (Rev 02)")
h("C-MNT-007", "2026-10-19", "Degraded", note="Pump repaired; late deviation raising under review")
h("C-WEL-011", "2026-09-26", "Effective", note="Overdue tests completed")
health.sort(key=lambda x: (x["control_id"], x["date"]))
cur = {}
for x in health: cur[x["control_id"]] = x
for c in controls:
    x = cur.get(c["control_id"]); c["health"] = x["health"] if x else "Not tested"; c["health_date"] = x["date"] if x else ""

# ---------------- risk history (quarterly + storyline changes)
rhist = []
qdates = [dt.date(y, m_, 28) for y in (2024, 2025, 2026) for m_ in (3, 6, 9, 12) if dt.date(y, m_, 28) < TODAY]
STORY = {"R-PAP-01": [("2024-01-01", "B"), ("2026-07-15", "D"), ("2026-10-01", "C")],
         "R-CPF-03": [("2024-01-01", "C"), ("2025-02-12", "D"), ("2025-12-01", "C"), ("2026-06-01", "B")],
         "R-CPF-05": [("2024-01-01", "B"), ("2025-08-21", "D"), ("2025-11-01", "B")],
         "R-LND-01": [("2024-01-01", "B"), ("2025-11-06", "D"), ("2026-04-23", "B")]}
for r in risks:
    C = r["current_c"]
    if r["risk_id"] in STORY:
        for d_, L in STORY[r["risk_id"]]:
            rhist.append(dict(risk_id=r["risk_id"], date=d_, likelihood=L, consequence=C, rating=rating(L, C), reason="Event or review" if d_ != "2024-01-01" else "Baseline"))
        continue
    L = r["current_l"]; Ls = "ABCDE"
    start = Ls[max(0, min(4, Ls.index(L) + rnd.choice([0, 0, 1, -1])))]
    rhist.append(dict(risk_id=r["risk_id"], date="2024-01-01", likelihood=start, consequence=C, rating=rating(start, C), reason="Baseline"))
    if start != L:
        d_ = rnd.choice(qdates)
        rhist.append(dict(risk_id=r["risk_id"], date=d_.isoformat(), likelihood=L, consequence=C, rating=rating(L, C), reason="Quarterly review"))
rhist.sort(key=lambda x: (x["risk_id"], x["date"]))
for r in risks:
    last = [x for x in rhist if x["risk_id"] == r["risk_id"]][-1]
    r["last_review"] = max(last["date"], (TODAY - dt.timedelta(days=rnd.randint(10, 80))).isoformat())
    if r["current_rating"] == "High":
        r["accepted_date"] = r["last_review"]; r["expiry"] = (D(r["last_review"]) + dt.timedelta(days=182)).isoformat()
        r["restrictions"] = "Interim restrictions per ALARP case"
    else:
        r["accepted_date"] = r["last_review"]; r["expiry"] = ""; r["restrictions"] = ""
r_pap = next(r for r in risks if r["risk_id"] == "R-PAP-01")
r_pap.update(version="3", restrictions="PL-101 operating pressure limited to 80% MAOP until features repaired", change_reason="Near miss EV of 14 July 2026; ILI results")

# ---------------- KPIs (monthly 2024-01 .. 2026-10)
KPIS = [
 ("PROD-OIL", "Crude oil production", "bbl/d", "Production", "lagging", "", "Sophia Hosany", "≥ 6,600 (2026)", "up", "site"),
 ("PROD-GAS", "Sales gas to NGC", "MMscf/d", "Production", "lagging", "4.2", "Karen Jack", "≥ 44", "up", "ACE"),
 ("NGC-DCQ", "NGC contract quantity delivered", "%", "Production", "lagging", "4.2", "Karen Jack", "≥ 98", "up", "ACE"),
 ("PROD-EFF", "Production efficiency", "%", "Production", "lagging", "6.3", "Sophia Hosany", "≥ 92", "up", "ACE"),
 ("DEFER-OIL", "Deferred crude production", "bbl/d", "Production", "lagging", "6.3", "Sophia Hosany", "< 300", "down", "ACE"),
 ("ALLOC-IMB", "Gas allocation imbalance", "%", "Measurement", "leading", "9.1", "Navin Sookdeo", "< 0.5", "down", "ACE"),
 ("HRS-EMP", "Employee hours worked", "hours", "Exposure", "", "", "Adrian Achong", "", "", "ACE"),
 ("HRS-CON", "Contractor hours worked", "hours", "Exposure", "", "", "Rhea Sookram", "", "", "ACE"),
 ("NEAR-MISS", "Near misses reported", "count", "Personal safety", "leading", "9.2", "Christina Bain", "≥ 12 per month", "up", "site"),
 ("FAC", "First aid cases", "count", "Personal safety", "lagging", "9.2", "Christina Bain", "", "down", "site"),
 ("MTC", "Medical treatment cases", "count", "Personal safety", "lagging", "9.2", "Christina Bain", "0", "down", "site"),
 ("RWC", "Restricted work cases", "count", "Personal safety", "lagging", "9.2", "Christina Bain", "0", "down", "site"),
 ("LTI", "Lost time injuries", "count", "Personal safety", "lagging", "9.2", "George Habib", "0", "down", "site"),
 ("TRIR", "Total recordable injury rate (12-month rolling, per 200,000 h)", "rate", "Personal safety", "lagging", "9.2", "George Habib", "< 0.5", "down", "ACE"),
 ("PSE-T1", "Tier 1 process safety events", "count", "Process safety", "lagging", "9.2", "Damian Daniel", "0", "down", "site"),
 ("PSE-T2", "Tier 2 process safety events", "count", "Process safety", "lagging", "9.2", "Damian Daniel", "≤ 2 per year", "down", "site"),
 ("PSE-T3", "Tier 3 challenges to safety systems", "count", "Process safety", "leading", "9.2", "Damian Daniel", "", "down", "site"),
 ("SPILL-N", "Hydrocarbon spills", "count", "Environment", "lagging", "9.2", "Kevin Lutchman", "0", "down", "site"),
 ("SPILL-BBL", "Volume spilled", "bbl", "Environment", "lagging", "9.2", "Kevin Lutchman", "0", "down", "site"),
 ("IOW-EXC", "IOW excursions recorded", "count", "Process safety", "leading", "6.3", "Michelle de Verteuil", "", "down", "ACE"),
 ("ALARM-RATE", "CPF alarms per operator-hour", "rate", "Process safety", "leading", "6.3", "Vijay Ramcharan", "< 6", "down", "ACE"),
 ("SCE-PLAN", "SCE maintenance and tests planned", "count", "Asset integrity", "leading", "6.5", "Marc Gomes", "", "", "ACE"),
 ("SCE-DONE", "SCE maintenance and tests completed on time", "%", "Asset integrity", "leading", "6.5", "Marc Gomes", "≥ 98", "up", "ACE"),
 ("SCE-OVERDUE", "Overdue SCE items at month end", "count", "Asset integrity", "leading", "6.5", "Marc Gomes", "0", "down", "ACE"),
 ("SCE-FAIL", "SCE test failures", "count", "Asset integrity", "leading", "6.5", "Marc Gomes", "", "down", "ACE"),
 ("PM-COMP", "Preventive maintenance compliance", "%", "Maintenance", "leading", "6.4", "Sunita Seepersad", "≥ 90", "up", "ACE"),
 ("BACKLOG-WK", "Corrective maintenance backlog", "weeks", "Maintenance", "leading", "6.4", "Sunita Seepersad", "< 4", "down", "ACE"),
 ("INSP-DONE", "Inspections completed against plan", "%", "Asset integrity", "leading", "6.5", "Wayne Rajkumar", "≥ 95", "up", "ACE"),
 ("DEFERRALS", "Open inspection deferrals", "count", "Asset integrity", "leading", "6.5", "Wayne Rajkumar", "", "down", "ACE"),
 ("PTW-ISSUED", "Permits to work issued", "count", "Control of work", "", "8.2", "Adrian Rodriguez", "", "", "ACE"),
 ("PTW-NC", "Permit non-conformances found in sampling", "count", "Control of work", "leading", "8.2", "Adrian Rodriguez", "", "down", "ACE"),
 ("MOC-RAISED", "MOCs raised", "count", "Change", "", "5.3", "Elena Farfan", "", "", "ACE"),
 ("MOC-OPEN", "MOCs open at month end", "count", "Change", "leading", "5.3", "Elena Farfan", "", "down", "ACE"),
 ("MOC-OVERDUE", "MOCs overdue", "count", "Change", "leading", "5.3", "Elena Farfan", "0", "down", "ACE"),
 ("DEV-OPEN", "Open deviations", "count", "Change", "leading", "2.6", "Marissa Bobb", "", "down", "ACE"),
 ("ACT-OPEN", "Open actions (events and audits)", "count", "Assurance", "leading", "9.4", "Dillon Haddad", "", "down", "ACE"),
 ("ACT-OVERDUE", "Overdue actions", "count", "Assurance", "leading", "9.4", "Dillon Haddad", "0", "down", "ACE"),
 ("AUDIT-FIND", "Audit findings raised", "count", "Assurance", "", "10.1", "Dillon Haddad", "", "", "ACE"),
 ("TRAIN-COMP", "Mandatory training compliance", "%", "People", "leading", "3.3", "Andrea Farfan", "≥ 95", "up", "ACE"),
 ("FLARE", "Gas flared", "MMscf", "Environment", "lagging", "9.1", "Rohan Ali", "-15% vs 2025", "down", "ACE"),
 ("GHG", "Greenhouse gas emissions", "tCO2e", "Environment", "lagging", "9.1", "Kevin Lutchman", "", "down", "ACE"),
 ("OIW", "Produced water oil-in-water (monthly average)", "mg/l", "Environment", "lagging", "9.1", "Kevin Lutchman", "< 40", "down", "ACE"),
 ("BOAT-TRIPS", "Supply and crew boat trips", "count", "Logistics", "", "8.1", "Lisa Williams", "", "", "ACE"),
 ("HELI", "Helicopter flights", "count", "Logistics", "", "8.1", "Lisa Williams", "", "", "ACE"),
 ("OPEX", "Operating cost", "TT$ million", "Finance", "lagging", "", "Teresa Daniel", "", "down", "ACE"),
 ("LIFT-COST", "Lifting cost", "US$/boe", "Finance", "lagging", "", "Teresa Daniel", "< 24", "down", "ACE"),
 ("DOCS-ONE", "Controlled documents published in ONE (cumulative)", "count", "Documents", "leading", "1.7", "Sanjay Jagessar", "30", "up", "ACE"),
 ("DOCS-OVERDUE", "Controlled documents past review date", "%", "Documents", "leading", "1.7", "Sanjay Jagessar", "< 5", "down", "ACE"),
]
kdata = []
months = []
m0 = dt.date(2024, 1, 1)
while m0 <= dt.date(2026, 10, 1): months.append(m0); m0 = (m0.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
def put(m_, site, k, v): kdata.append(dict(month=m_.strftime("%Y-%m"), site=site, kpi_id=k, value=v))
ev_by = collections.defaultdict(list)
for e in events: ev_by[(e["date"][:7], e["site"])].append(e)
BASE = {"PAP": 3050, "CHB": 620, "SAP": 360, "LND": 2950}
DECL = {"PAP": 0.055, "CHB": 0.08, "SAP": 0.09, "LND": 0.035}
SHUT = {("2024-07", "PAP"): 0.12, ("2024-07", "CHB"): 0.12, ("2024-07", "SAP"): 0.12, ("2026-07", "PAP"): 0.38, ("2026-08", "PAP"): 0.25,
        ("2026-09", "PAP"): 0.12, ("2025-11", "LND"): 0.03, ("2026-09", "SAP"): 0.08}
rec12 = collections.deque(maxlen=12); hrs12 = collections.deque(maxlen=12)
docs_by_eff = sorted(DOCS.values(), key=lambda x: x["effective"])
for i, m_ in enumerate(months):
    ym = m_.strftime("%Y-%m"); t = i / 12
    tot = 0
    for s, b in BASE.items():
        v = b * (1 - DECL[s]) ** t * rnd.uniform(0.97, 1.03)
        if s == "LND" and m_ >= dt.date(2025, 6, 1): v += 140  # gas lift optimisation (OPP-08)
        if s == "LND" and m_ >= dt.date(2026, 5, 1): v += 60   # SOU-15 back after workover
        v *= 1 - SHUT.get((ym, s), 0); v = round(v); tot += v; put(m_, s, "PROD-OIL", v)
    put(m_, "ACE", "PROD-OIL", tot)
    gas = 46.5 * (1 - 0.04) ** t * rnd.uniform(0.97, 1.02)
    if ym == "2024-09": gas *= 0.9
    if ym in ("2026-07", "2026-08"): gas *= 0.93
    put(m_, "ACE", "PROD-GAS", round(gas, 1)); put(m_, "ACE", "NGC-DCQ", round(min(100, gas / 45.5 * 100 * rnd.uniform(0.99, 1.01)), 1))
    lost = {"2024-07": 380, "2026-07": 1250, "2026-08": 820, "2026-09": 420, "2024-09": 120}.get(ym, rnd.randint(120, 260))
    put(m_, "ACE", "DEFER-OIL", lost); put(m_, "ACE", "PROD-EFF", round(100 * tot / (tot + lost), 1))
    put(m_, "ACE", "ALLOC-IMB", round({"2025-06": 1.1, "2025-07": 1.3, "2025-08": 1.4}.get(ym, rnd.uniform(0.15, 0.45)), 2))
    he = round(300 * rnd.uniform(168, 176)); hc = round(rnd.uniform(58000, 74000) + (12000 if ym in ("2025-04", "2025-05", "2026-04") else 0))
    put(m_, "ACE", "HRS-EMP", he); put(m_, "ACE", "HRS-CON", hc)
    rec = 0
    for s in SITES:
        es = ev_by[(ym, s)]
        c = collections.Counter(e["type"] for e in es)
        put(m_, s, "NEAR-MISS", c["Near miss"]); put(m_, s, "FAC", c["First aid"]); put(m_, s, "MTC", c["Medical treatment"])
        put(m_, s, "RWC", c["Restricted work"]); put(m_, s, "LTI", c["Lost time injury"]); put(m_, s, "PSE-T1", 0)
        put(m_, s, "PSE-T2", sum(1 for e in es if e["pse_tier"] == "2")); put(m_, s, "PSE-T3", sum(1 for e in es if e["pse_tier"] == "3"))
        sp = [e for e in es if e["spill_bbl"] != ""]; put(m_, s, "SPILL-N", len(sp)); put(m_, s, "SPILL-BBL", round(sum(float(e["spill_bbl"]) for e in sp), 1))
        rec += c["Medical treatment"] + c["Restricted work"] + c["Lost time injury"]
    rec12.append(rec); hrs12.append(he + hc)
    put(m_, "ACE", "TRIR", round(sum(rec12) * 200000 / sum(hrs12), 2))
    allm = [e for (k, s), es in ev_by.items() if k == ym for e in es]
    put(m_, "ACE", "IOW-EXC", sum(1 for e in allm if e["type"] == "IOW excursion") + (rnd.randint(1, 4) if m_ >= dt.date(2026, 6, 1) else 0))
    ar = {"2025-01": 8.9, "2025-02": 11.4, "2025-03": 12.1, "2025-04": 10.2, "2025-05": 10.8, "2025-06": 9.5, "2025-07": 8.8, "2025-08": 8.1,
          "2025-09": 7.6, "2025-10": 7.0, "2025-11": 6.2, "2025-12": 5.8}.get(ym, rnd.uniform(7.2, 8.6) if m_ < dt.date(2025, 1, 1) else rnd.uniform(4.6, 5.7))
    put(m_, "ACE", "ALARM-RATE", round(ar, 1))
    plan = rnd.randint(55, 70); put(m_, "ACE", "SCE-PLAN", plan)
    od = {"2026-06": 4, "2026-07": 9, "2026-08": 7, "2026-09": 5, "2026-10": 3}.get(ym, rnd.choice([0, 0, 1, 1, 2]))
    put(m_, "ACE", "SCE-DONE", round(100 * (plan - od) / plan, 1)); put(m_, "ACE", "SCE-OVERDUE", od)
    put(m_, "ACE", "SCE-FAIL", sum(1 for e in allm if e["type"] == "SCE test failure"))
    pm = rnd.uniform(86, 93) - (6 if ym in ("2026-07", "2026-08") else 0); put(m_, "ACE", "PM-COMP", round(pm, 1))
    put(m_, "ACE", "BACKLOG-WK", round(rnd.uniform(3.0, 4.6) + (1.2 if ym in ("2026-07", "2026-08", "2026-09") else 0), 1))
    put(m_, "ACE", "INSP-DONE", round(rnd.uniform(88, 98) - (8 if ym in ("2026-04", "2026-05", "2026-06") else 0), 1))
    put(m_, "ACE", "DEFERRALS", {"2026-04": 6, "2026-05": 7, "2026-06": 7, "2026-07": 8, "2026-08": 5, "2026-09": 2, "2026-10": 2}.get(ym, rnd.randint(1, 4)))
    put(m_, "ACE", "PTW-ISSUED", rnd.randint(470, 560)); put(m_, "ACE", "PTW-NC", rnd.randint(2, 9))
    mr = rnd.randint(7, 13); put(m_, "ACE", "MOC-RAISED", mr); put(m_, "ACE", "MOC-OPEN", rnd.randint(28, 42)); put(m_, "ACE", "MOC-OVERDUE", rnd.randint(2, 8))
    put(m_, "ACE", "DEV-OPEN", rnd.randint(9, 16) + (3 if ym >= "2026-04" and ym <= "2026-08" else 0))
    end = (m_.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    put(m_, "ACE", "AUDIT-FIND", sum(1 for e in allm if e["type"] == "Audit finding"))
    put(m_, "ACE", "TRAIN-COMP", round(rnd.uniform(89, 96), 1))
    fl = rnd.uniform(38, 52) * (0.85 if m_.year == 2026 else 1) + (14 if ym in ("2024-09", "2026-07") else 0)
    put(m_, "ACE", "FLARE", round(fl, 1)); put(m_, "ACE", "GHG", round(9800 + fl * 62 + rnd.uniform(-300, 300)))
    put(m_, "ACE", "OIW", round(rnd.uniform(18, 34) + (22 if ym in ("2025-04", "2026-02") else 0), 1))
    put(m_, "ACE", "BOAT-TRIPS", rnd.randint(52, 66) + (10 if ym in ("2026-07", "2026-08", "2026-09") else 0)); put(m_, "ACE", "HELI", rnd.randint(16, 22))
    opex = rnd.uniform(64, 72) + (6 if ym in ("2026-07", "2026-08", "2026-09") else 0); put(m_, "ACE", "OPEX", round(opex, 1))
    boe = (tot + gas * 1000 / 6) * 30.4; put(m_, "ACE", "LIFT-COST", round(opex * 1e6 / 6.78 / boe, 2))
    put(m_, "ACE", "DOCS-ONE", sum(1 for d_ in docs_by_eff if d_["effective"] <= end))
    put(m_, "ACE", "DOCS-OVERDUE", round(rnd.uniform(22, 30) if m_ < dt.date(2026, 1, 1) else max(3.0, 18 - (m_.month * 1.6)) + rnd.uniform(-1, 1), 1))
# open / overdue actions at each month end (from the actions register)
EVD = {e["event_id"]: D(e["date"]) for e in events}
for m_ in months:
    end = (m_.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    live = [a for a in actions if EVD[a["event_id"]] <= end and (not a["closed"] or D(a["closed"]) > end)]
    put(m_, "ACE", "ACT-OPEN", len(live)); put(m_, "ACE", "ACT-OVERDUE", sum(1 for a in live if D(a["due"]) < end))

# ---------------- write
print("writing registers/")
write("AIM-REG-002.csv", assets, ["asset_id", "tag", "title", "site", "parent_id", "iso14224_class", "criticality", "sce", "in_service"])
write("AIM-REG-001.csv", sces, ["sce_id", "title", "group", "site", "asset_ids", "performance_standard", "test_interval", "last_test", "next_due", "status", "controls"])
RCOLS = ["risk_id", "level", "title", "site", "system", "asset_id", "process", "hazard", "top_event", "threats", "consequences", "owner", "escalation_vp",
         "c_people", "c_environment", "c_asset", "c_reputation", "current_c", "current_l", "current_rating", "controls", "legacy_control_docs",
         "alarp_status", "residual_c", "residual_l", "residual_rating", "acceptance_authority", "accepted_date", "expiry", "restrictions",
         "review_frequency", "last_review", "objective_id", "version", "change_reason"]
write("RSK-REG-001.csv", risks, RCOLS)
write("RSK-REG-001_history.csv", rhist, ["risk_id", "date", "likelihood", "consequence", "rating", "reason"])
write("RSK-REG-002.csv", controls, ["control_id", "statement", "position", "nature", "critical", "risk_id", "threat", "barrier", "doc_ref", "process_step",
                                     "process_planned", "owner", "asset_id", "sce_id", "evidence", "test_interval", "effective", "health", "health_date", "status"])
write("RSK-REG-002_health.csv", health, ["control_id", "date", "health", "event_id", "note"])
write("INC-REG-001_events.csv", events, ["event_id", "date", "site", "type", "title", "severity", "pse_tier", "spill_bbl", "risk_ids", "controls_tested",
                                          "controls_failed", "processes", "notes"])
write("INC-REG-001_actions.csv", actions, ["action_id", "event_id", "title", "owner", "due", "closed", "result"])
write("OMS-REG-001_objectives.csv", [dict(objective_id=o[0], title=o[1], owner=who(o[2]), kpi=o[3], target=o[4], year=o[5],
      risks="; ".join(r["risk_id"] for r in risks if r["objective_id"] == o[0])) for o in OBJECTIVES],
      ["objective_id", "title", "owner", "kpi", "target", "year", "risks"])
write("OMS-REG-001_opportunities.csv", [dict(opportunity_id=o[0], title=o[1], objective_id=o[2], owner=who(o[3]), value=o[4], likelihood=o[5], benefit=o[6], status=o[7])
      for o in OPPORTUNITIES], ["opportunity_id", "title", "objective_id", "owner", "value", "likelihood", "benefit", "status"])
write("BPM-REG-001.csv", [dict(process_id=p[0], title=p[1], l1=p[2], l2=p[3], owner=who(p[4]), function=p[5], policy=p[6], parent=p[7], status=p[8],
      revision=p[9], oms_tags=p[10], last_review="", maturity="2" if p[8] == "Draft" else "1",
      controls="; ".join(c["control_id"] for c in controls if c["process_planned"] == p[0] or c["process_step"].startswith(p[0] + "#"))) for p in PROCESSES],
      ["process_id", "title", "l1", "l2", "owner", "function", "policy", "parent", "status", "revision", "oms_tags", "last_review", "maturity", "controls"])
write("PRF-REG-001_kpis.csv", [dict(kpi_id=k[0], name=k[1], unit=k[2], category=k[3], family=k[4], oms_tag=k[5], owner=who(k[6]), target=k[7], better=k[8], scope=k[9]) for k in KPIS],
      ["kpi_id", "name", "unit", "category", "family", "oms_tag", "owner", "target", "better", "scope"])
write("PRF-REG-001_monthly.csv", kdata, ["month", "site", "kpi_id", "value"])
