"""Adds the ONE Process Data Requirement fields to the demo ledgers and writes the supporting files.

Run after build_ledgers.py (it calls this at the end). Uses its own random seed so the ledgers themselves never change.

Writes
  registers/BPM-LOG-<process>_events.csv   + wait_reason and rework_reason columns (codes from the ONE Icon Standard, reason.*)
  registers/BPM-CAP-001.csv                capacity of each lane (role) available to each process, by period
  registers/BPM-SCN-001.csv                dated changes the demo history was built around (markers on the trends)
  processes/maps/<process>.map.json        which source system would feed each field in a real company
"""
import csv, json, os, random
from datetime import datetime
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REG = os.path.join(ROOT, "registers")
R2 = random.Random(1849)
P = lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M") if s else None
OFF = {"PAP", "CHB", "SAP"}

WAIT = {  # process -> step -> [(code, weight)]; a callable gets the event and its case
    "ACE-MOC-PRS-001": {"S02": [("information", 1)], "S03": [("resource", 70), ("batch", 30)], "S04": [("resource", 72), ("information", 18), ("batch", 10)],
                        "S05": [("resource", 1)], "S06": [("resource", 60), ("information", 40)], "S07": [("approval", 80), ("batch", 20)],
                        "S08": [("window", 48), ("parts", 31), ("permit", 21)], "S09": [("permit", 40), ("resource", 60)], "S10": [("resource", 55), ("window", 45)]},
    "ACE-AIM-PRS-001": {"S02": [("resource", 1)], "S03": [("resource", 1)], "S04": [("approval", 60), ("resource", 40)], "S05": [("resource", 70), ("information", 30)],
                        "S06": lambda e, c: ([("resource", 1)] if c["site"] not in OFF else [("transport", 75), ("weather", 25)] if c["revision"] == "01" else [("batch", 80), ("transport", 10), ("weather", 10)]),
                        "S07": [("permit", 1)], "S10": [("resource", 80), ("information", 20)], "S11": [("resource", 1)], "S12": [("resource", 1)], "S13": [("resource", 70), ("batch", 30)]},
}
REWORK = {"ACE-MOC-PRS-001": [("incomplete", 70), ("information", 30)], "ACE-AIM-PRS-001": [("weather", 60), ("permit", 30), ("parts", 10)]}


def pick(opts):
    t = sum(w for _, w in opts); r = R2.uniform(0, t); a = 0
    for k, w in opts:
        a += w
        if r <= a: return k
    return opts[-1][0]


def enrich(pid):
    cases = {c["case_id"]: c for c in csv.DictReader(open(os.path.join(REG, f"BPM-LOG-{pid}_cases.csv"), encoding="utf-8"))}
    f = os.path.join(REG, f"BPM-LOG-{pid}_events.csv")
    rows = list(csv.DictReader(open(f, encoding="utf-8")))
    n_w = n_r = 0
    for e in rows:
        e["wait_reason"] = e["rework_reason"] = ""
        a, s = P(e["arrived"]), P(e["started"])
        if a and s and (s - a).total_seconds() > 86400:
            o = WAIT[pid].get(e["step_id"])
            if callable(o): o = o(e, cases[e["case_id"]])
            if o: e["wait_reason"] = pick(o); n_w += 1
        if (pid == "ACE-MOC-PRS-001" and e["step_id"] == "S07" and e["branch"] == "Returned for rework") or (pid == "ACE-AIM-PRS-001" and e["step_id"] == "S08" and e["branch"].startswith("Weather")):
            e["rework_reason"] = pick(REWORK[pid]); n_r += 1
    cols = ["case_id", "step_id", "lane", "arrived", "started", "finished", "branch", "rework", "wait_reason", "rework_reason", "trip"]
    with open(f, "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=cols); w.writeheader(); w.writerows(rows)
    return rows, n_w, n_r


def work_by_lane(rows, m):
    W = defaultdict(float); skip = {s["id"] for s in m["steps"] if s["type"] in ("start", "end")}
    for e in rows:
        s, f = P(e["started"]), P(e["finished"])
        if s and f and e["step_id"] not in skip: W[(e["lane"], s.year)] += (f - s).total_seconds() / 3600
    return W


def capacity(models, ledgers):
    out = []
    UTIL = {"ACE-MOC-PRS-001": {"L1": .36, "L2": .70, "L3": .80, "L4": .45, "L5": .35, "L6": .86},
            "ACE-AIM-PRS-001": {"L1": .48, "L2": .74, "L3": .58, "L4": .44, "L5": .66, "L6": .30, "L7": .82}}
    for pid, m in models.items():
        W = work_by_lane(ledgers[pid], m)
        for l in m["lanes"]:
            yrs = [W.get((l["id"], y), 0) for y in (2024, 2025)]
            avg = sum(yrs) / 2 or 1
            hpw = round(avg / UTIL[pid][l["id"]] / 52.14, 1)
            ppl = 1 if hpw < 30 else round(hpw / 30)
            row = dict(process_id=pid, lane=l["id"], role=l["role"], role_id=l.get("role_id", ""), people=ppl, hours_per_week=hpw, start="2024-01-01", end="", note="")
            if pid == "ACE-MOC-PRS-001" and l["id"] == "L3":
                out.append(dict(row, end="2025-02-28", note="Four discipline leads share MOC technical reviews"))
                out.append(dict(row, hours_per_week=round(hpw * 0.82, 1), start="2025-03-01", note="Rotating equipment lead post vacant; reviews shared by the remaining three leads"))
                continue
            if pid == "ACE-AIM-PRS-001" and l["id"] == "L5":
                out.append(dict(row, end="2025-05-31", note="Logistics coordinator books each offshore inspection trip separately"))
                out.append(dict(row, start="2025-06-01", note="Campaign bundling: one booking per platform campaign"))
                continue
            out.append(row)
    cols = ["process_id", "lane", "role", "role_id", "people", "hours_per_week", "start", "end", "note"]
    with open(os.path.join(REG, "BPM-CAP-001.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=cols); w.writeheader(); w.writerows(out)
    return len(out)


SCN = [
    ("2024-01-01", "ACE-MOC-PRS-001", "revision", "Rev 01 modelled from ACE-MOC-PRC-001", "", ""),
    ("2024-01-01", "ACE-AIM-PRS-001", "revision", "Rev 01 modelled from ACE-AIM-PRA-001 and ACE-AIM-STD-002", "", ""),
    ("2024-09-02", "ACE-AIM-PRS-001", "improvement", "Idea raised after three wasted trips: confirm readiness before travel", "S08", "CI-2024-002"),
    ("2024-10-07", "ACE-AIM-PRS-001", "improvement", "Offshore on-time inspections below target two quarters running", "S06", "CI-2024-001"),
    ("2024-11-04", "ACE-MOC-PRS-001", "improvement", "MOCs open at month end above target", "S08", "CI-2024-004"),
    ("2025-03-01", "ACE-MOC-PRS-001", "capacity", "Rotating equipment lead post vacant; MOC technical reviews shared by three leads", "S04", ""),
    ("2025-04-01", "ACE-MOC-PRS-001", "revision", "Rev 02: implementation joined to the weekly maintenance schedule", "S08", "CI-2024-004"),
    ("2025-06-01", "ACE-AIM-PRS-001", "revision", "Rev 02: offshore inspections bundled into platform campaigns; readiness checked 48 hours before travel", "S06", "CI-2024-001"),
    ("2025-11-18", "ACE-AIM-PRS-001", "assurance", "Conformance check rates C-AIM-004 (deferral safeguards) Degraded", "S04", "CI-2025-003"),
    ("2026-02-09", "ACE-AIM-PRS-001", "deviation", "PL-101 inspection deferral extended to August 2026", "S04", ""),
    ("2026-05-11", "ACE-MOC-PRS-001", "improvement", "DMAIC study opened on the Technical Authority review queue", "S04", "CI-2026-006"),
    ("2026-07-14", "ACE-AIM-PRS-001", "incident", "Pinhole leak on PL-101 (near miss)", "S04", "EV-2026-161"),
    ("2026-07-20", "ACE-AIM-PRS-001", "improvement", "DMAIC study: stop campaign bundling driving deferrals of critical lines", "S03", "CI-2026-007"),
]


def maps(models):
    os.makedirs(os.path.join(ROOT, "processes", "maps"), exist_ok=True)
    SRC = {"ACE-MOC-PRS-001": ("ONE MOC module (in a client: the MOC tool)", "CMMS work orders for S08"), "ACE-AIM-PRS-001": ("RBI / inspection data system", "CMMS work orders, permit system, logistics booking")}
    for pid, m in models.items():
        a, b = SRC[pid]
        doc = {"process_id": pid, "owner": m["owner"], "data_champion": "OMS data champion (to be appointed)", "refresh": "daily extract",
               "demo_note": "ACE has no live systems: these files are curated by processes/tools/build_ledgers.py in this shape.",
               "cases": {"source": a, "fields": {"case_id": "record number", "opened": "date raised", "closed": "date closed", "outcome": "final status", "due": "target date", "site": "location"}},
               "events": {"source": f"{a}; {b}", "fields": {"arrived": "status changed to waiting at this step", "started": "assignee began work (first edit or acceptance)",
                          "finished": "status moved on", "branch": "decision recorded", "wait_reason": "reason drop-down (to be added to the form)", "rework_reason": "return reason drop-down"}},
               "capacity": {"source": "rosters and role assignments, monthly", "file": "registers/BPM-CAP-001.csv"},
               "costs": {"source": "ERP and logistics booking", "fields": {"trip": "booking or flight reference"}}}
        json.dump(doc, open(os.path.join(ROOT, "processes", "maps", f"{pid}.map.json"), "w", encoding="utf-8"), indent=2)


def main():
    models = {pid: json.load(open(os.path.join(ROOT, "processes", f"{pid}.json"), encoding="utf-8")) for pid in ("ACE-MOC-PRS-001", "ACE-AIM-PRS-001")}
    ledgers = {}
    for pid in models:
        rows, nw, nr = enrich(pid); ledgers[pid] = rows
        print(f"{pid}: wait reasons on {nw} events, rework reasons on {nr} events")
    print(f"BPM-CAP-001: {capacity(models, ledgers)} capacity rows")
    with open(os.path.join(REG, "BPM-SCN-001.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.writer(h); w.writerow(["date", "process_id", "kind", "description", "step_id", "ref"]); w.writerows(SCN)
    print(f"BPM-SCN-001: {len(SCN)} dated changes")
    maps(models); print("processes/maps: 2 mapping files")


if __name__ == "__main__":
    main()
