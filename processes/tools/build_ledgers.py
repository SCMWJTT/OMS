"""Build the process ledgers (event logs) and the CI register for the ONE demo.

    python processes/tools/build_ledgers.py

Writes
  registers/BPM-LOG-ACE-MOC-PRS-001_cases.csv / _events.csv   from the MOC register (MOC-REG-001 and its step dates)
  registers/BPM-LOG-ACE-AIM-PRS-001_cases.csv / _events.csv   simulated inspections 2024 to Nov 2026 from AIM-REG-002
  registers/CI-REG-001.csv and CI-REG-001_history.csv          improvement items, with baselines measured from the ledgers
and prints a short report of what it wrote. Deterministic: the same inputs always give the same files.
"""
import csv, os, random, statistics as st
from datetime import datetime, date, timedelta
from collections import defaultdict, Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REG = os.path.join(ROOT, "registers")
TODAY = datetime(2026, 11, 24, 17, 0)
R = random.Random(510)


def rd(name):
    with open(os.path.join(REG, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def wr(name, rows, cols):
    with open(os.path.join(REG, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def tri(a, m, b):
    return R.triangular(a, b, m)


def ts(d):
    return d.strftime("%Y-%m-%d %H:%M") if d else ""


def d0(s):
    return datetime.strptime(s, "%Y-%m-%d")


EVCOLS = ["case_id", "step_id", "lane", "arrived", "started", "finished", "branch", "rework", "trip"]

# ------------------------------------------------------------------ MOC: convert the register into a ledger
MOC_LANE = {"S01": "L1", "S02": "L1", "S03": "L2", "S04": "L3", "S05": "L2", "S06": "L4", "S07": "L5", "S08": "L6", "S09": "L4",
            "S10": "L2", "S11": "L2", "S12": "L1"}
MOC_WORK = {"S02": (0.5, 1, 3), "S03": (0.5, 1, 2), "S04": (4, 8, 24), "S05": (0.5, 1, 2), "S06": (1, 2, 6), "S07": (0.5, 1, 2),
            "S08": (8, 40, 200), "S09": (2, 4, 8), "S10": (2, 8, 24), "S11": (0, 0, 0), "S12": (0, 0, 0)}
REV2_MOC = datetime(2025, 4, 1)


def rework_p(t):
    if t < datetime(2025, 1, 1): return 0.17
    if t < REV2_MOC: return 0.15
    if t < datetime(2026, 1, 1): return 0.10
    return 0.07


def build_moc():
    regs = {r["moc_id"]: r for r in rd("MOC-REG-001.csv")}
    steps = defaultdict(list)
    for s in rd("MOC-REG-001_steps.csv"):
        steps[s["moc_id"]].append(s)
    cases, events = [], []
    for mid, r in regs.items():
        rows = steps.get(mid, [])
        if not rows: continue
        opened = d0(r["raised"]) + timedelta(hours=8, minutes=R.randint(0, 90))
        rev = "01" if opened < REV2_MOC else "02"
        ids = [x["step"] for x in rows]
        outcome = "Rejected" if "S12" in ids else "Closed" if r["status"] == "Closed" else "Cancelled" if r["status"].startswith("Cancelled") else "Open"
        prev_end = opened
        evs = []
        for i, x in enumerate(rows):
            sid = x["step"]
            arrived = prev_end
            a, m, b = MOC_WORK[sid]
            work = timedelta(hours=tri(a, m, b)) if b else timedelta(0)
            if x["left"]:
                fin = d0(x["left"]) + timedelta(hours=15, minutes=R.randint(0, 120))
                if fin < arrived + work: fin = arrived + work
            else:
                fin = None
            start = (max(arrived, fin - work) if fin else (arrived + timedelta(days=R.uniform(0.5, 3)) if arrived + timedelta(days=3) < TODAY else None))
            nxt = rows[i + 1]["step"] if i + 1 < len(rows) else ""
            br = ""
            if sid == "S03": br = "C2 or C3" if nxt == "S04" else "C1" if nxt == "S05" else ""
            if sid == "S07": br = "Rejected" if nxt == "S12" else "Approved" if nxt else ""
            ev = dict(case_id=mid, step_id=sid, lane=MOC_LANE[sid], arrived=arrived, started=start, finished=fin, branch=br, rework=0, trip="")
            # an approval that was returned once for rework: split the approval window
            if sid == "S07" and br == "Approved" and fin and (fin - arrived) >= timedelta(hours=20) and R.random() < rework_p(arrived):
                span = fin - arrived
                t1 = arrived + span * 0.25; t2 = arrived + span * 0.55; t3 = arrived + span * 0.8
                evs.append(dict(ev, started=arrived + span * 0.15, finished=t1, branch="Returned for rework", rework=1))
                evs.append(dict(ev, step_id="S02", lane="L1", arrived=t1, started=t1 + span * 0.1, finished=t2, branch="", rework=1))
                evs.append(dict(ev, step_id="S06", lane="L4", arrived=t2, started=t2 + span * 0.1, finished=t3, branch="", rework=1))
                ev = dict(ev, arrived=t3, started=t3 + (fin - t3) * 0.5)
            evs.append(ev)
            if fin is None: break
            prev_end = fin
        closed = evs[-1]["finished"] if outcome in ("Closed", "Rejected", "Cancelled") else None
        if outcome == "Cancelled" and closed is None: closed = d0(r["closed"]) if r["closed"] else None
        cases.append(dict(case_id=mid, process_id="ACE-MOC-PRS-001", revision=rev, site=r["site"], cls=r["class_"], title=r["title"], ref=mid,
                          opened=ts(opened), closed=ts(closed), outcome=outcome, due=r["target_close"], deferred_to="", asset_id="", technique="",
                          category=r["category"], value_key=f"MOC_BENEFIT_{r['class_']}"))
        for e in evs:
            events.append({k: (ts(v) if isinstance(v, datetime) else v) for k, v in e.items()})
    n1 = wr("BPM-LOG-ACE-MOC-PRS-001_cases.csv", cases, ["case_id", "process_id", "revision", "site", "cls", "category", "title", "ref", "opened", "closed", "outcome", "due", "value_key"])
    n2 = wr("BPM-LOG-ACE-MOC-PRS-001_events.csv", events, EVCOLS)
    return cases, events, n1, n2


# ------------------------------------------------------------------ Inspection: simulate from the asset register
POINTS = {  # class -> list of (technique, interval months, count of circuits or points)
    "Pressure vessel": [("UT thickness survey", 24, 2), ("External visual", 12, 1)],
    "Pipeline": [("UT and CP survey", 12, 2), ("External visual and patrol", 6, 1)],
    "Storage tank": [("External visual", 12, 1), ("Shell UT survey", 24, 1)],
    "Structure": [("Topsides structural survey", 12, 1), ("Splash zone and CP survey", 24, 2)],
    "Process unit": [("Piping circuit UT", 12, 4), ("CUI screening", 24, 2)],
    "Flare": [("Flare tip and structure visual", 24, 1)],
    "Chemical injection": [("Piping circuit UT", 12, 1)],
    "Compressor": [("Piping circuit UT", 12, 2)],
    "Pump": [("Piping circuit UT", 24, 1)],
    "Valve": [("External visual", 24, 1)],
    "Loading arm": [("NDT of swivels and structure", 12, 1)],
    "Crane": [("Thorough examination", 6, 1)],
    "Firewater": [("Piping circuit UT", 24, 2)],
}
OFFSHORE = {"PAP", "CHB", "SAP"}
REV2_INS = datetime(2025, 6, 1)
CAMPAIGN_EVERY = {"PAP": 21, "CHB": 42, "SAP": 42}
CAMPAIGN_START = {"PAP": datetime(2025, 6, 9), "CHB": datetime(2025, 6, 16), "SAP": datetime(2025, 6, 23)}


def next_campaign(site, t):
    d = CAMPAIGN_START[site]
    while d < t: d += timedelta(days=CAMPAIGN_EVERY[site])
    return d + timedelta(hours=7)


def deferral_p(site, t):
    if site not in OFFSHORE: return 0.04
    if t < REV2_INS: return 0.10
    if t < datetime(2026, 1, 1): return 0.15
    return 0.21


def build_inspections():
    assets = rd("AIM-REG-002.csv")
    tasks = []
    for a in assets:
        for tech, months, n in POINTS.get(a["iso14224_class"], []):
            for k in range(n * (2 if a["site"] in OFFSHORE else 1)):
                tasks.append(dict(asset=a, tech=tech, months=months, k=k))
    cases, events, seq, trips = [], [], Counter(), Counter()
    special = []
    for t in tasks:
        a = t["asset"]; site = a["site"]
        due = datetime(2024, 1, 15) + timedelta(days=R.randint(0, int(t["months"] * 30.4) - 1))
        while due < TODAY + timedelta(days=45):
            if a["asset_id"] == "A-PAP-026" and t["tech"].startswith("UT and CP") and t["k"] == 0 and datetime(2025, 9, 1) <= due < datetime(2026, 3, 1):
                special.append((t, due)); due += timedelta(days=int(t["months"] * 30.4)); continue
            case = simulate(t, due, seq, trips)
            if case: cases.append(case[0]); events.extend(case[1])
            due += timedelta(days=int(t["months"] * 30.4))
    # the PL-101 story: deferred, extended, near miss in July 2026, intelligent pigging in September found metal loss
    for t, due in special[:1]:
        c, e = pl101_case(t, due, seq)
        cases.append(c); events.extend(e)
    cases.sort(key=lambda c: c["opened"])
    events.sort(key=lambda e: (e["case_id"], e["arrived"]))
    n1 = wr("BPM-LOG-ACE-AIM-PRS-001_cases.csv", cases, ["case_id", "process_id", "revision", "site", "asset_id", "tag", "technique", "title", "ref", "opened", "closed", "outcome", "due", "deferred_to", "trips"])
    n2 = wr("BPM-LOG-ACE-AIM-PRS-001_events.csv", [{k: (ts(v) if isinstance(v, datetime) else v) for k, v in e.items()} for e in events], EVCOLS)
    return cases, events, n1, n2


def simulate(t, due, seq, trips):
    a = t["asset"]; site = a["site"]; off = site in OFFSHORE
    opened = due - timedelta(days=(30 if due < REV2_INS else 40) if off else 30) + timedelta(hours=8, minutes=R.randint(0, 60))
    if opened > TODAY: return None
    yr = opened.year; seq[yr] += 1
    cid = f"INS-{yr}-{seq[yr]:03d}"
    rev = "01" if opened < REV2_INS else "02"
    ev = []

    def add(sid, lane, arrived, wait_d, work_h, branch="", rework=0, trip=""):
        start = arrived + timedelta(days=wait_d)
        fin = start + timedelta(hours=work_h)
        ev.append(dict(case_id=cid, step_id=sid, lane=lane, arrived=arrived, started=start, finished=fin, branch=branch, rework=rework, trip=trip))
        return fin

    t1 = add("S02", "L2", opened, tri(1, 3, 7), tri(4, 8, 16))
    # projected trip date decides whether a deferral is needed
    ready_guess = t1 + timedelta(days=4)
    if off:
        proj = next_campaign(site, ready_guess + timedelta(days=2)) if opened >= REV2_INS else ready_guess + timedelta(days=tri(7, 16, 35))
    else:
        proj = ready_guess + timedelta(days=2)
    defer = (proj > due and R.random() < (0.95 if opened >= REV2_INS else 0.45)) or R.random() < deferral_p(site, opened) * 0.3
    t2 = add("S03", "L1", t1, tri(0, 0.5, 2), tri(0.5, 1, 2), "Needs deferral" if defer else "On time")
    deferred_to = None
    if defer:
        t2 = add("S04", "L3", t2, tri(2, 4, 10), tri(1, 2, 4))
        deferred_to = due + timedelta(days=R.choice([90, 90, 90, 180, 30]))
    t3 = add("S05", "L4", t2, tri(1, 2.5, 6), tri(1, 2, 4))
    ntrip = 0; rw = 0
    while True:
        if off:
            trip_at = next_campaign(site, t3 + timedelta(days=2)) if opened >= REV2_INS else t3 + timedelta(days=tri(7, 16, 35))
            trips[(site, trip_at.date())] += 1
            tid = f"TRIP-{site}-{trip_at.strftime('%Y%m%d')}" if opened >= REV2_INS else f"TRIP-{site}-{trip_at.strftime('%Y%m%d')}-{cid[-3:]}"
        else:
            trip_at = t3 + timedelta(days=tri(1, 2, 4)); tid = ""
        wait = max(0.0, (trip_at - t3).total_seconds() / 86400 - 0.2)
        t4 = add("S06", "L5", t3, wait, tri(0.5, 1, 2), rework=rw, trip=tid)
        ntrip += 1 if off else 0
        t5 = add("S07", "L6", t4, 0.05, tri(1, 2, 4), rework=rw)
        abort_p = (0.14 if opened < REV2_INS else 0.05) if off else 0.03
        if R.random() < abort_p and rw < 2:
            add("S08", "L6", t5, 0, 0.5, "Weather or permit not ready", rework=rw)
            rw += 1; t3 = t5
            continue
        t5 = add("S08", "L6", t5, 0, 0.2, "Ready", rework=rw)
        break
    t6 = add("S09", "L7", t5, 0.02, tri(4, 8, 24))
    t7 = add("S10", "L7", t6, tri(2, 4, 8), tri(2, 4, 8))
    anomaly = R.random() < 0.14
    t8 = add("S11", "L2", t7, tri(1, 2.5, 7), tri(2, 4, 12), "Anomaly found" if anomaly else "Acceptable")
    if anomaly:
        t8 = add("S12", "L3", t8, tri(0.5, 1.5, 4), tri(2, 4, 8))
    t9 = add("S13", "L1", t8, tri(1, 2.5, 6), tri(1, 2, 4))
    ev.append(dict(case_id=cid, step_id="S14", lane="L1", arrived=t9, started=t9, finished=t9, branch="", rework=0, trip=""))
    ev = [e for e in ev if e["arrived"] <= TODAY]
    for e in ev:
        if e["finished"] and e["finished"] > TODAY: e["finished"] = None
        if e["started"] and e["started"] > TODAY: e["started"] = None
    closed = ev[-1]["finished"] if ev[-1]["step_id"] == "S14" else None
    insp = next((e["finished"] for e in ev if e["step_id"] == "S09" and e["finished"]), None)
    outcome = ("Anomaly" if anomaly else "Acceptable") if closed else "Open"
    case = dict(case_id=cid, process_id="ACE-AIM-PRS-001", revision=rev, site=site, asset_id=a["asset_id"], tag=a["tag"], technique=t["tech"],
                title=f"{t['tech']} — {a['tag']} {a['title']}", ref=a["asset_id"], opened=ts(opened), closed=ts(closed), outcome=outcome,
                due=due.strftime("%Y-%m-%d"), deferred_to=deferred_to.strftime("%Y-%m-%d") if deferred_to else "", trips=ntrip)
    return case, ev


def pl101_case(t, due, seq):
    a = t["asset"]; site = "PAP"
    opened = due - timedelta(days=45) + timedelta(hours=8)
    yr = opened.year; seq[yr] += 1; cid = f"INS-{yr}-{seq[yr]:03d}"
    E = []

    def add(sid, lane, arr, start, fin, branch="", rework=0, trip=""):
        E.append(dict(case_id=cid, step_id=sid, lane=lane, arrived=arr, started=start, finished=fin, branch=branch, rework=rework, trip=trip))
        return fin
    h = lambda d, hh=9: datetime(d.year, d.month, d.day, hh)
    x = add("S02", "L2", opened, opened + timedelta(days=3), opened + timedelta(days=3, hours=8))
    x = add("S03", "L1", x, x + timedelta(hours=20), x + timedelta(hours=21), "Needs deferral")
    x = add("S04", "L3", x, x + timedelta(days=6), x + timedelta(days=6, hours=2))           # deferred 90 days to Feb 2026
    x = add("S04", "L3", h(datetime(2026, 2, 2)), h(datetime(2026, 2, 9)), h(datetime(2026, 2, 9), 11), "Extension", 1)   # extended to Aug 2026
    x = add("S05", "L4", x, h(datetime(2026, 6, 15)), h(datetime(2026, 6, 15), 12))
    x = add("S06", "L5", x, h(datetime(2026, 7, 20)), h(datetime(2026, 7, 20), 10), trip="TRIP-PAP-20260721-PIG")
    x = add("S07", "L6", x, h(datetime(2026, 9, 7), 7), h(datetime(2026, 9, 7), 9), trip="")
    x = add("S08", "L6", x, x, x + timedelta(minutes=12), "Ready")
    x = add("S09", "L7", x, x + timedelta(hours=1), h(datetime(2026, 9, 12), 16))
    x = add("S10", "L7", x, h(datetime(2026, 9, 21)), h(datetime(2026, 9, 21), 15))
    x = add("S11", "L2", x, h(datetime(2026, 9, 24)), h(datetime(2026, 9, 24), 17), "Anomaly found")
    x = add("S12", "L3", x, h(datetime(2026, 9, 28)), h(datetime(2026, 9, 28), 15))
    add("S13", "L1", x, None, None)
    case = dict(case_id=cid, process_id="ACE-AIM-PRS-001", revision="02", site=site, asset_id=a["asset_id"], tag=a["tag"], technique="Intelligent pigging (ILI) and CP survey",
                title=f"Intelligent pigging (ILI) and CP survey — PL-101 {a['title']}", ref="EV-2026-161; EV-2026-210; MOC-2026-061",
                opened=ts(opened), closed="", outcome="Open", due=due.strftime("%Y-%m-%d"), deferred_to="2026-08-31", trips=1)
    return case, E


# ------------------------------------------------------------------ measures used for CI baselines
def P(e, k):
    v = e.get(k)
    if isinstance(v, datetime) or v is None: return v
    return datetime.strptime(v, "%Y-%m-%d %H:%M") if v else None


def med_wait(events, step, y, only=None):
    v = [(P(e, "started") - P(e, "arrived")).total_seconds() / 86400 for e in events if e["step_id"] == step and P(e, "started") and P(e, "arrived").year == y and (only is None or e["case_id"] in only)]
    return round(st.median(v), 1) if v else None


def med_span(events, step, y):
    v = [(P(e, "finished") - P(e, "arrived")).total_seconds() / 86400 for e in events if e["step_id"] == step and P(e, "finished") and P(e, "arrived").year == y]
    return round(st.median(v), 1) if v else None


def rft(events, y):
    by = defaultdict(list)
    for e in events: by[e["case_id"]].append(e)
    ok = [not any(int(x["rework"]) for x in v) for v in by.values() if any(x["step_id"] == "S07" and x["branch"] == "Approved" for x in v) and P(v[0], "arrived").year == y]
    return round(100 * sum(ok) / len(ok)) if ok else None


def on_time(cases, events, y):
    insp = {e["case_id"]: P(e, "finished") for e in events if e["step_id"] == "S09" and P(e, "finished")}
    v = [insp[c["case_id"]] <= datetime.strptime(c["due"], "%Y-%m-%d") + timedelta(hours=23) for c in cases if c["case_id"] in insp and c["due"][:4] == str(y) and c["site"] in OFFSHORE]
    return round(100 * sum(v) / len(v)) if v else None


def defer_rate(cases, y):
    v = [bool(c["deferred_to"]) for c in cases if c["due"][:4] == str(y) and c["site"] in OFFSHORE]
    return round(100 * sum(v) / len(v)) if v else None


def aborts(events, y):
    v = [e["branch"] == "Weather or permit not ready" for e in events if e["step_id"] == "S08" and P(e, "arrived").year == y]
    return round(100 * sum(v) / len(v), 1) if v else None


def trips_per_year(events, y):
    return len({e["trip"] for e in events if e["trip"] and P(e, "arrived").year == y and e["step_id"] == "S06"})


# ------------------------------------------------------------------ CI register
def build_ci(mc, me, ic, ie):
    off = {c["case_id"] for c in ic if c["site"] in OFFSHORE}
    b_wait24, b_wait26 = med_wait(ie, "S06", 2024, off), med_wait(ie, "S06", 2026, off)
    ot24, ot25, ot26 = on_time(ic, ie, 2024), on_time(ic, ie, 2025), on_time(ic, ie, 2026)
    df24, df25, df26 = defer_rate(ic, 2024), defer_rate(ic, 2025), defer_rate(ic, 2026)
    ab24, ab26 = aborts(ie, 2024), aborts(ie, 2026)
    tr24, tr26 = trips_per_year(ie, 2024), trips_per_year(ie, 2026)
    s08_24, s08_26 = med_span(me, "S08", 2024), med_span(me, "S08", 2026)
    s04_26 = med_span(me, "S04", 2026)
    rft24, rft26 = rft(me, 2024), rft(me, 2026)
    trip_cost = 6500 * 1.2 + 14000 * 0.5
    saving = round((tr24 - tr26 * 12 / 10.8) * trip_cost, -3)
    C = []

    def item(**k):
        base = dict(ci_id="", title="", process_id="", step_id="", source="", source_ref="", method="", stage="", owner="", originator="",
                    raised="", decided="", verified="", closed="", kpi="", baseline="", target="", actual="", benefit_usd="", moc_id="",
                    from_rev="", to_rev="", element="10", notes="")
        base.update(k); C.append(base)

    item(ci_id="CI-2024-001", title="Bundle offshore inspections into platform campaigns", process_id="ACE-AIM-PRS-001", step_id="S06",
         source="KPI breaches", source_ref="Inspections done by the original due date below 90% for Q2 and Q3 2024", method="PDCA", stage="Standardised",
         owner="Wayne Rajkumar — Inspection Lead", originator="Wayne Rajkumar — Inspection Lead", raised="2024-10-07", decided="2024-10-21",
         verified="2026-01-15", closed="2026-02-02", kpi="Offshore inspections done by the original due date, %", baseline=ot24, target="≥ 90", actual=ot26,
         benefit_usd=saving, moc_id="MOC-2025-046", from_rev="01", to_rev="02", element="10",
         notes=f"Median offshore wait for transport went from {b_wait24} to {b_wait26} days and inspections done after the due date without an approved deferral almost disappeared. Offshore trips fell from {tr24} in 2024 to {tr26} in Jan–Nov 2026; logistics saving about USD {saving:,.0f} a year at public helicopter and boat rates. "
               f"Side effect seen later: offshore deferrals rose from {df24}% (2024) to {df25}% (2025) as items were pushed to the next campaign — see CI-2026-007.")
    item(ci_id="CI-2024-002", title="Confirm site readiness 48 hours before travel", process_id="ACE-AIM-PRS-001", step_id="S08",
         source="Staff ideas", source_ref="Idea from the OIM after three wasted trips in August 2024", method="Just do it", stage="Closed",
         owner="Wayne Rajkumar — Inspection Lead", originator="Winston Granger — Offshore Installation Manager", raised="2024-09-02", decided="2024-09-05",
         verified="2025-12-10", closed="2025-12-15", kpi="Trips aborted on arrival, %", baseline=ab24, target="≤ 5", actual=ab26, from_rev="01", to_rev="02",
         notes="Folded into Rev 02 of the process with the campaign change.")
    item(ci_id="CI-2025-003", title="Standard deferral safeguards template with expiry tracking", process_id="ACE-AIM-PRS-001", step_id="S04",
         source="Audit and assurance findings", source_ref="Line 2 conformance check: C-AIM-004 rated Degraded (deferral safeguards not recorded on 3 of 8 samples)",
         method="PDCA", stage="In progress", owner="Wayne Rajkumar — Inspection Lead", originator="Dillon Haddad — Compliance & Assurance Manager",
         raised="2025-11-18", decided="2025-12-02", kpi="Deferrals with safeguards and expiry recorded, %", baseline="62", target="100", actual="",
         notes="Do stage: template trialled at Pommerac A; extension rule awaiting MOC-2026-061.")
    item(ci_id="CI-2026-007", title="Stop campaign bundling from driving deferrals of critical lines", process_id="ACE-AIM-PRS-001", step_id="S03",
         source="Incident and near-miss actions", source_ref="EV-2026-161 pinhole leak on PL-101 (deferral extended; C-AIM-004 failed)",
         method="DMAIC", stage="In progress", owner="Wayne Rajkumar — Inspection Lead", originator="Christina Bain — HSE Manager",
         raised="2026-07-20", decided="2026-07-28", kpi="Offshore inspections needing a deferral, %", baseline=df25, target="≤ 10", actual="", moc_id="MOC-2026-061",
         notes=f"Analyse stage. Data: deferral rate {df24}% (2024), {df25}% (2025), {df26}% (2026). Proposal: criticality-A items get a dedicated trip if the next campaign is past the due date.")
    item(ci_id="CI-2024-004", title="Join MOC implementation to the weekly maintenance schedule", process_id="ACE-MOC-PRS-001", step_id="S08",
         source="KPI breaches", source_ref="MOCs open at month end above 20 for two quarters (MOC-OPEN)", method="PDCA", stage="Standardised",
         owner="Elena Farfan — Manager, Technical Excellence", originator="Haresh Ramcharan — Process Engineer", raised="2024-11-04", decided="2024-11-18",
         verified="2026-03-31", closed="2026-04-06", kpi="Median days in implementation (S08)", baseline=s08_24, target="≤ 21", actual=s08_26,
         from_rev="01", to_rev="02", notes="Step detail and lane changed within the process (PRS pair revision, no MOC needed under ACE-BPM-PRA-003 §6).")
    item(ci_id="CI-2025-005", title="Complete change packages before approval", process_id="ACE-MOC-PRS-001", step_id="S07",
         source="Process reviews", source_ref="Annual process review 2025: 15% of changes returned at approval", method="PDCA", stage="Verified",
         owner="Elena Farfan — Manager, Technical Excellence", originator="Elena Farfan — Manager, Technical Excellence", raised="2025-02-17", decided="2025-03-03",
         verified="2026-10-30", kpi="Changes approved without return, %", baseline=rft24, target="≥ 90", actual=rft26, from_rev="01", to_rev="02",
         notes="Checklist added to the MOC module; awaiting standardisation in ACE-MOC-PRC-001 Rev 02.")
    item(ci_id="CI-2026-006", title="Shorten the Technical Authority review queue", process_id="ACE-MOC-PRS-001", step_id="S04",
         source="KPI breaches", source_ref="MOC cycle time median above 30 days for C2 and C3 changes", method="DMAIC", stage="In progress",
         owner="Elena Farfan — Manager, Technical Excellence", originator="Elena Farfan — Manager, Technical Excellence", raised="2026-05-11", decided="2026-05-25",
         kpi="Median days at Technical Authority review (S04)", baseline=s04_26, target="≤ 10", actual="",
         notes="Measure stage: 90% of S04 time is waiting; three discipline leads hold 70% of reviews.")
    item(ci_id="CI-2026-008", title="Raise MOC requests from a phone on site", process_id="ACE-MOC-PRS-001", step_id="S02", source="Staff ideas",
         source_ref="Idea from an offshore operations engineer", method="Just do it", stage="Assessed", owner="Elena Farfan — Manager, Technical Excellence",
         originator="Teresa Thomas — Operations Engineer (Offshore)", raised="2026-10-06", decided="2026-10-20", kpi="Days from change identified to MOC raised",
         notes="Route chosen: just do it within the ONE MOC module.")
    item(ci_id="CI-2026-009", title="Drone visual inspection of flare tips", process_id="ACE-AIM-PRS-001", step_id="S09", source="Staff ideas",
         source_ref="Idea from the inspection contractor", method="Project", stage="Parked", owner="Wayne Rajkumar — Inspection Lead",
         originator="Contractor — NDT supervisor", raised="2026-08-14", decided="2026-09-03",
         notes="Parked: needs C2 MOC and aviation approval; review at the next annual process review.")
    item(ci_id="CI-2025-010", title="Pre-printed permits for routine inspection tasks", process_id="ACE-COW-PRS-001", step_id="", source="Staff ideas",
         source_ref="Idea from an Area Authority", method="Just do it", stage="Closed", owner="Arjun Gittens — Offshore Operations Manager (Gulf of Paria)",
         originator="Roger Ramkissoon — Offshore Installation Manager", raised="2025-03-10", decided="2025-03-14", verified="2025-08-29", closed="2025-09-05",
         kpi="Permit preparation time, hours", baseline="2.5", target="≤ 1", actual="0.8")
    item(ci_id="CI-2026-011", title="Automatic reminders for incident actions near due date", process_id="ACE-INC-PRS-001", step_id="", source="KPI breaches",
         source_ref="Overdue actions (ACT-OVERDUE) out of target for two months", method="PDCA", stage="Idea", owner="Christina Bain — HSE Manager",
         originator="Christina Bain — HSE Manager", raised="2026-11-10", kpi="Overdue incident actions")
    item(ci_id="CI-2026-012", title="Audit findings feed the process owner dashboard", process_id="ACE-PRF-PRS-001", step_id="", source="Process reviews",
         source_ref="Annual review of the audit process", method="PDCA", stage="Assessed", owner="Dillon Haddad — Compliance & Assurance Manager",
         originator="Marissa Bobb — OMS Manager", raised="2026-09-15", decided="2026-10-01", kpi="Days from finding to process owner notified")
    cols = list(C[0].keys())
    n = wr("CI-REG-001.csv", C, cols)
    H = []
    STAGES = ["Idea", "Assessed", "In progress", "Verified", "Standardised", "Closed"]
    for c in C:
        H.append(dict(ci_id=c["ci_id"], date=c["raised"], stage="Idea", note="Raised"))
        if c["decided"]:
            H.append(dict(ci_id=c["ci_id"], date=c["decided"], stage="Assessed" if c["stage"] != "Parked" else "Parked", note=f"Route: {c['method']}" if c["stage"] != "Parked" else "Parked by the process owner"))
        if c["stage"] in STAGES[2:]:
            d = (datetime.strptime(c["decided"], "%Y-%m-%d") + timedelta(days=21)).strftime("%Y-%m-%d")
            H.append(dict(ci_id=c["ci_id"], date=d, stage="In progress", note="Plan agreed"))
        if c["verified"]: H.append(dict(ci_id=c["ci_id"], date=c["verified"], stage="Verified", note=f"KPI {c['baseline']} → {c['actual']}"))
        if c["stage"] in ("Standardised", "Closed") and c["to_rev"]:
            H.append(dict(ci_id=c["ci_id"], date=c["closed"] or c["verified"], stage="Standardised", note=f"Process Rev {c['to_rev']}"))
        if c["closed"]: H.append(dict(ci_id=c["ci_id"], date=c["closed"], stage="Closed", note="Closed"))
    wr("CI-REG-001_history.csv", H, ["ci_id", "date", "stage", "note"])
    return C, dict(on_time=(ot24, ot25, ot26), defer=(df24, df25, df26), wait=(b_wait24, b_wait26), aborts=(ab24, ab26), trips=(tr24, tr26),
                   s08=(s08_24, s08_26), rft=(rft24, rft26), saving=saving)


if __name__ == "__main__":
    mc, me, a, b = build_moc()
    print(f"MOC ledger: {a} cases, {b} events (rework events: {sum(int(e['rework']) for e in me)})")
    ic, ie, a, b = build_inspections()
    print(f"Inspection ledger: {a} cases, {b} events; per year opened: {dict(Counter(c['opened'][:4] for c in ic))}")
    C, m = build_ci(mc, me, ic, ie)
    print(f"CI register: {len(C)} items; measures used: {m}")
    import importlib.util, sys
    _p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "enrich_ledgers.py")
    _s = importlib.util.spec_from_file_location("enrich_ledgers", _p); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m); _m.main()
