"""Document register (DOC-REG-001) and MOC register (MOC-REG-001) for the ACE data spine. Called from gen_registers.py."""
import datetime as dt, math, re, zipfile, glob, os, collections

def _poisson(rnd, lam):
    Lx, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rnd.random()
        if p <= Lx: return k
        k += 1

# ---------------- MOC register -------------------------------------------------------------
MOC_TEMPL = {
 "PAP": [("Replace export pump P-1300A mechanical seal with different design", "Plant", "OPS"), ("Change separator V-1100 level alarm setpoint", "Process", "OPS"),
         ("Temporary bypass of test separator during repair", "Plant", "OPS"), ("Add vent line on chemical injection skid X-1500", "Plant", "AIM"),
         ("Revise crane lift procedure for supply vessel", "Document", "COW"), ("Change corrosion inhibitor supplier and chemistry", "Process", "AIM")],
 "CHB": [("Replace wellhead control panel solenoids with new model", "Plant", "WEL"), ("Change visit frequency for Chenet B", "Organisation", "OPS")],
 "SAP": [("Install solar panels for Sapodilla C telemetry", "Plant", "OPS"), ("Change Sapodilla C flowline pigging frequency", "Process", "AIM")],
 "CPF": [("Replace pressure transmitter on SIF with different span", "Plant", "ENG"), ("Upgrade DCS operator graphics", "Software", "OPS"),
         ("Change glycol circulation rate limits", "Process", "OPS"), ("Tie-in new compressor recycle valve", "Plant", "PSM"),
         ("Re-rate crude tank T-2602 after inspection", "Plant", "AIM"), ("Change jetty loading rate limit", "Process", "OPS"),
         ("Flow computer software update at the Gas Buyer meter", "Software", "HMA")],
 "LND": [("Combine supervisor coverage across Tamarind and Pawpaw", "Organisation", "OPS"), ("Replace flowline section with HDPE", "Plant", "AIM"),
         ("Convert TAM-27 to gas lift", "Plant", "WEL"), ("Change tank battery inspection interval", "Process", "AIM"), ("Install remote level monitoring on tank batteries", "Plant", "OPS")],
 "PLB": [("Change supply vessel contract and vessel type", "Organisation", "LOG"), ("New laydown area for pipe storage", "Plant", "LOG")],
 "HOF": [("Reorganise Maintenance & Integrity reporting lines", "Organisation", "MNT"), ("New CMMS work order priorities", "Software", "MNT"),
         ("Move document control to ONE repository", "Software", "DOC")],
}
SYS_RISK = {"OPS": {"PAP": "R-PAP-02", "CPF": "R-CPF-03", "LND": "R-LND-02", "CHB": "R-CHB-02", "SAP": "R-SAP-02"}, "AIM": {"PAP": "R-PAP-01", "CPF": "R-CPF-02", "LND": "R-LND-02", "SAP": "R-SAP-01"},
            "WEL": {"CHB": "R-CHB-02", "LND": "R-LND-01"}, "ENG": {"CPF": "R-CPF-04"}, "PSM": {"CPF": "R-CPF-01"}, "HMA": {"CPF": "R-CPF-05"},
            "COW": {"PAP": "R-PAP-07"}, "LOG": {"PLB": "R-PLB-02"}, "MNT": {"HOF": "R-HOF-14"}, "DOC": {"HOF": "R-HOF-08"}}
SYS_DOC = {"OPS": "ACE-OPS-STD-001", "AIM": "ACE-AIM-STD-001", "WEL": "ACE-WEL-STD-001", "ENG": "ACE-ENG-SPC-410", "PSM": "ACE-PSM-STD-001",
           "HMA": "ACE-OPS-STD-001", "COW": "ACE-COW-PRC-001", "LOG": "ACE-CON-STD-001", "MNT": "ACE-MNT-STD-001", "DOC": "ACE-DOC-PRC-001"}
ORIG = {"PAP": ["Teresa Thomas", "Roger Ramkissoon", "Winston Granger"], "CHB": ["Teresa Thomas"], "SAP": ["Teresa Thomas"], "CPF": ["Rohan Ali", "Haresh Ramcharan", "Ian Laquis"],
        "LND": ["Navin Ramdass", "Luis de Verteuil"], "PLB": ["Lisa Williams"], "HOF": ["Marc Gomes", "Shalini Mungal", "Sanjay Jagessar"]}
APPROVER = {"C1": {"PAP": "Arjun Gittens", "CHB": "Arjun Gittens", "SAP": "Arjun Gittens", "CPF": "Rohan Ali", "LND": "Luis de Verteuil", "PLB": "Lisa Williams", "HOF": "Elena Farfan"},
            "C2": "Elena Farfan", "C3": "Dev Jaggernauth"}
COORD = "Haresh Ramcharan"   # holds the MOC Coordinator role (ACE-MOC-PRC-001)

def build_mocs(rnd, who, today, events, controls_by_id):
    D = dt.date.fromisoformat
    mocs = []
    def active(cid, d): c = controls_by_id.get(cid); return c and c["status"] == "Active" and c["effective"] and D(c["effective"]) <= d
    m = dt.date(2023, 9, 1)
    while m <= today:
        last = min((m.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1), today - dt.timedelta(days=1))
        for _ in range(_poisson(rnd, 10 * (last.day / 30))):
            site = rnd.choices(list(MOC_TEMPL), weights=[24, 4, 4, 30, 22, 6, 10])[0]
            title, cat, sys_ = rnd.choice(MOC_TEMPL[site])
            raised = m + dt.timedelta(days=rnd.randint(0, (last - m).days))
            cls = rnd.choices(["C1", "C2", "C3"], weights=[62, 33, 5])[0]
            typ = "Temporary" if "Temporary" in title or rnd.random() < 0.12 else "Permanent"
            mocs.append(dict(raised=raised, site=site, title=title, category=cat, system=sys_, cls=cls, type=typ))
        m = (m.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    # storyline MOCs (fixed)
    story = [dict(raised=D("2025-09-02"), site="CPF", title="Alarm rationalisation of CPF compressor and inlet sections", category="Software", system="OPS", cls="C2", type="Permanent",
                  story="CPF alarm flood"),
             dict(raised=D("2025-09-08"), site="CPF", title="Correct Gas Buyer meter flow computer configuration and add verification check", category="Software", system="HMA", cls="C2", type="Permanent",
                  story="Gas Buyer meter"),
             dict(raised=D("2026-07-15"), site="PAP", title="Temporary operating pressure limit on PL-101 (80% MAOP) pending repair", category="Process", system="AIM", cls="C2", type="Temporary",
                  story="Pommerac A"),
             dict(raised=D("2026-08-11"), site="PAP", title="Revise inhibitor IOW, pigging interval and deferral rule for PL-101; add low-flow alarm on X-1500", category="Process",
                  system="AIM", cls="C3", type="Permanent", story="Pommerac A")]
    mocs += story
    mocs.sort(key=lambda x: (x["raised"], 0 if x.get("story") else 1))
    seq = collections.Counter(); steps = []
    for x in mocs:
        y = x["raised"].year; seq[y] += 1; x["moc_id"] = f"MOC-{y}-{seq[y]:03d}"
        # lifecycle through ACE-MOC-PRS-001 steps
        t = x["raised"]; cls = x["cls"]; st = x.get("story")
        def step(sid, name, lane, days):
            nonlocal t
            start = t; t = t + dt.timedelta(days=days)
            steps.append(dict(moc_id=x["moc_id"], step=sid, name=name, role=lane, entered=start.isoformat(), left=t.isoformat() if t <= today else ""))
            return t <= today
        dur = {"C1": (1, 3, 0, 3, 2, (5, 30), 1, (3, 10)), "C2": (2, 5, (8, 25), (3, 7), (4, 10), (15, 70), (1, 3), (5, 20)), "C3": (3, 7, (20, 45), (5, 10), (7, 14), (30, 120), (2, 5), (10, 30))}[cls]
        r = lambda v: rnd.randint(*v) if isinstance(v, tuple) else v
        if st == "Pommerac A" and cls == "C3": dur = (1, 2, (10, 10), (3, 3), (4, 4), (24, 24), (2, 2), (60, 60))  # documents still being revised
        if st == "Pommerac A" and cls == "C2": dur = (0, 1, (2, 2), (1, 1), (1, 1), (1, 1), (1, 1), (200, 200))  # stays in force until repair
        ok = step("S02", "Raise MOC request", "Change Originator", r(dur[0]))
        ok = ok and step("S03", "Classify change", "MOC Coordinator", r(dur[1]))
        rejected = cls != "C3" and not st and rnd.random() < 0.08
        if ok and cls == "C1": ok = step("S05", "Screen minor change", "MOC Coordinator", rnd.randint(1, 4))
        elif ok: ok = step("S04", "Assess technical risk", "Technical Authority", r(dur[2]))
        ok = ok and step("S06", "Review operational impact", "Area Authority", r(dur[3]))
        ok = ok and step("S07", "Approve change", "MOC Approver", r(dur[4]))
        approved = t if ok else None
        if ok and rejected:
            steps.append(dict(moc_id=x["moc_id"], step="S12", name="Change rejected", role="Change Originator", entered=t.isoformat(), left=t.isoformat())); status = "Cancelled / superseded"; closed = t
        else:
            ok = ok and step("S08", "Implement change", "Change Originator", r(dur[5])); impl = t if ok else None
            ok = ok and step("S09", "Verify pre-start readiness", "Area Authority", r(dur[6]))
            ok = ok and step("S10", "Update documents and train", "MOC Coordinator", r(dur[7]))
            closed = t if ok else None
            if ok: steps.append(dict(moc_id=x["moc_id"], step="S11", name="Close MOC", role="MOC Coordinator", entered=t.isoformat(), left=t.isoformat()))
            last_open = [s for s in steps if s["moc_id"] == x["moc_id"] and not s["left"]]
            sname = last_open[0]["step"] if last_open else "S11"
            status = {"S02": "Registered", "S03": "Registered", "S04": "Under review", "S05": "Under review", "S06": "Under review", "S07": "Under review",
                      "S08": "Approved for implementation", "S09": "Ready for start-up", "S10": "Operating / verification", "S11": "Closed"}[sname]
        target = x["raised"] + dt.timedelta(days={"C1": 30, "C2": 75, "C3": 150}[cls])
        exp = (x["raised"] + dt.timedelta(days=90)).isoformat() if x["type"] == "Temporary" else ""
        if st == "Pommerac A" and cls == "C2": exp = "2026-12-31"
        risk = SYS_RISK.get(x["system"], {}).get(x["site"], "")
        ctrl = []
        if x["category"] == "Process" and active("C-OPS-009", x["raised"]): ctrl.append("C-OPS-009")
        if x["category"] == "Organisation" and active("C-BPM-044", x["raised"]): ctrl.append("C-BPM-044")
        docs = [SYS_DOC.get(x["system"], "")]
        if st == "Pommerac A" and cls == "C3": docs = ["ACE-OPS-PRA-001", "ACE-AIM-PRA-001", "ACE-AIM-STD-001"]
        if st == "Pommerac A" and cls == "C2": docs = ["ACE-OPS-STD-001"]
        ev = ""
        if st == "Pommerac A" and cls == "C3": ev = next((e["event_id"] for e in events if e["title"].startswith("MOC-2026-047")), "")  # title patched to the real ID in gen_registers
        x.update(dict(class_=cls, status=status, approved=approved.isoformat() if approved else "", closed=closed.isoformat() if closed else "",
                      target_close=target.isoformat(), temp_expiry=exp, originator=who(rnd.choice(ORIG[x["site"]]) if not st else {"Pommerac A": "Allison Mitchell", "CPF alarm flood": "Vijay Ramcharan", "Gas Buyer meter": "Navin Sookdeo"}[st]),
                      coordinator=who(COORD) + " (MOC Coordinator)",
                      approver=who(APPROVER[cls][x["site"]] if cls == "C1" else APPROVER[cls]), risk_ids=risk, controls=", ".join(ctrl).replace(", ", "; "),
                      documents="; ".join(d for d in docs if d), event_id=ev, storyline=st or ""))
        if st == "Pommerac A" and cls == "C3": x["originator"] = who("Michelle de Verteuil")
    return mocs, steps

MOC_COLS = ["moc_id", "title", "site", "system", "category", "class_", "type", "status", "raised", "approved", "closed", "target_close", "temp_expiry",
            "originator", "coordinator", "approver", "risk_ids", "controls", "documents", "event_id", "storyline"]

# ---------------- Document register -------------------------------------------------------
def build_docreg(rnd, root, who, people, protocol_planned, today):
    D = dt.date.fromisoformat
    title_to_person = {}
    for n, r in people.items(): title_to_person.setdefault(r["Job Title"], n)
    docs, revs = [], []
    found = set()
    for f in sorted(glob.glob(os.path.join(root, "finals/*.docx")) + glob.glob(os.path.join(root, "manuals/*.docx"))):
        z = zipfile.ZipFile(f); d = z.read("word/document.xml").decode()
        p = {k: v.replace("&amp;", "&") for k, v in re.findall(r'name="ODS\.([^"]+)"[^>]*>\s*<vt:\w+>([^<]*)<', z.read("docProps/custom.xml").decode())}
        did = p["DocumentId"]; found.add(did)
        eff = dt.datetime.strptime(p["EffectiveDate"], "%d %B %Y").date(); iss = dt.datetime.strptime(p["IssueDate"], "%d %B %Y").date()
        years = 3
        docs.append(dict(doc_id=did, title=p["Title"], type=p["DocumentType"], level=re.sub(r"\D", "", p.get("Level", "")) or "", system=did.split("-")[1],
                         status="Current", revision=p["Revision"], issue_date=iss.isoformat(), effective_date=eff.isoformat(),
                         next_review=eff.replace(year=eff.year + years).isoformat(), owner=p.get("DocumentOwner", ""), parent=p.get("Parent", ""),
                         file=os.path.relpath(f, root), pending_revision="", pending_moc="", target_issue="", predecessor="", predecessor_last_review="", predecessor_replaced=""))
        # revision history table
        for tbl in re.findall(r"<w:tbl>.*?</w:tbl>", d, re.S):
            rows = [[re.sub(r"\s+", " ", "".join(re.findall(r"<w:t[^>]*>([^<]*)", c))).strip() for c in re.findall(r"<w:tc>.*?</w:tc>", r, re.S)]
                    for r in re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S)]
            if rows and rows[0][:3] == ["Revision", "Date", "Description"]:
                for r in rows[1:]:
                    if len(r) >= 3: revs.append(dict(doc_id=did, revision=r[0], date=r[1], description=r[2].replace("&amp;", "&"), state="Issued" if r[0].isdigit() else "Draft"))
                break
    # pending Rev 02 (MOC-2026-047)
    for x in docs:
        if x["doc_id"] in ("ACE-OPS-PRA-001", "ACE-AIM-PRA-001", "ACE-AIM-STD-001"):
            x.update(pending_revision="02", pending_moc="MOC-2026-047", target_issue="2026-12-01")
            revs.append(dict(doc_id=x["doc_id"], revision="02", date="(target 1 December 2026)", description="Revision after the PL-101 near miss of 14 July 2026 (MOC-2026-047).", state="In preparation"))
    # predecessors (legacy pre-ONE documents)
    for x in docs:
        if x["type"] == "Manual" or rnd.random() < 0.15: continue
        last = dt.date(rnd.randint(2019, 2024), rnd.randint(1, 12), 1)
        x.update(predecessor=f"Legacy {x['type'].lower()} (PDF, pre-ONE)", predecessor_last_review=last.isoformat(), predecessor_replaced=x["effective_date"])
    # planned documents
    waves = [D("2027-02-01"), D("2027-04-01"), D("2027-06-01"), D("2027-09-01")]
    for did, v in sorted(protocol_planned.items()):
        if did in found: continue
        owner = title_to_person.get(v["owner_role"]) or next((n for t, n in title_to_person.items() if t.startswith(v["owner_role"])), "")
        typ = did.split("-")[2]
        x = dict(doc_id=did, title=v["title"], type={"STD": "Standard", "PRA": "Practice", "PRC": "Procedure", "PLN": "Plan", "REG": "Register", "PRS": "Process",
                 "POL": "Policy", "SPC": "Specification"}.get(typ, typ), level=str(v["level"]), system=did.split("-")[1], status="Planned", revision="", issue_date="",
                 effective_date="", next_review="", owner=who(owner) if owner else v["owner_role"], parent="", file="", pending_revision="", pending_moc="",
                 target_issue=rnd.choice(waves).isoformat(), predecessor="", predecessor_last_review="", predecessor_replaced="")
        if typ not in ("PRS", "PRA", "REG") and rnd.random() < 0.6:
            last = dt.date(rnd.randint(2018, 2024), rnd.randint(1, 12), 1)
            x.update(predecessor="Legacy document (PDF, pre-ONE)", predecessor_last_review=last.isoformat())
        docs.append(x)
    return docs, revs

def doc_overdue_pct(docs, month_end, years=3):
    live, over = 0, 0
    for x in docs:
        if x["status"] == "Current" and x["effective_date"] and dt.date.fromisoformat(x["effective_date"]) <= month_end:
            live += 1
            if x["next_review"] and dt.date.fromisoformat(x["next_review"]) < month_end: over += 1
        if x["predecessor_last_review"]:
            rep = x["predecessor_replaced"]
            if not rep or dt.date.fromisoformat(rep) > month_end:
                live += 1
                lr = dt.date.fromisoformat(x["predecessor_last_review"])
                if lr.replace(year=lr.year + years) < month_end: over += 1
    return round(100 * over / live, 1) if live else 0.0

DOC_COLS = ["doc_id", "title", "type", "level", "system", "status", "revision", "issue_date", "effective_date", "next_review", "owner", "parent", "file",
            "pending_revision", "pending_moc", "target_issue", "predecessor", "predecessor_last_review", "predecessor_replaced"]

def build_reads(rnd, docs, people, today):
    """Read-and-acknowledge status per current document and function."""
    staff = collections.Counter(r["Function"] for r in people.values())
    FN = {"OPS": "Operations", "AIM": "Engineering & Projects", "MNT": "Operations", "WEL": "Wells", "COW": "Operations", "ENG": "Engineering & Projects",
          "PSM": "HSE & Compliance", "RSK": "HSE & Compliance", "INC": "HSE & Compliance", "EMR": "HSE & Compliance", "PRF": "HSE & Compliance",
          "OMS": "HSE & Compliance", "DOC": "IT, Data & Knowledge", "CON": "Supply Chain Management", "PPL": "Human Resources", "BPM": "CEO Office", "LDR": None}
    out = []
    for x in docs:
        if x["status"] != "Current": continue
        fns = list(staff) if x["system"] in ("LDR", "OMS") or x["type"] in ("Policy", "Manual") else sorted({FN.get(x["system"]) or "Operations", "Operations"})
        age = (today - dt.date.fromisoformat(x["effective_date"])).days
        for fn in fns:
            req = staff[fn]; pct = min(1.0, 0.45 + age / 300) * rnd.uniform(0.85, 1.0)
            out.append(dict(doc_id=x["doc_id"], revision=x["revision"], function=fn, required=req, acknowledged=min(req, round(req * pct)), as_of=today.isoformat()))
    return out
