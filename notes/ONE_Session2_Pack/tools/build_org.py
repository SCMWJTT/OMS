"""Build the ACE organisation files the portal reads (company/org/*.csv) from the staff list.

Run once from the repo root:  python notes/ONE_Session2_Pack/tools/build_org.py
After that, company/org/*.csv and company/ACE_People.csv are the files to edit by hand (or in Excel).
"""
import csv, collections, re, os

os.makedirs("company/org", exist_ok=True)
P = "company/ACE_People.csv"
rows = list(csv.DictReader(open(P, encoding="utf-8-sig")))
HDR = list(rows[0].keys())

SITE_OF = {"Head Office, Central Trinidad": "HOF", "Central Processing Facility": "CPF", "Pommerac A Platform (Gulf of Paria)": "PAP",
           "Land leases (Central & South Trinidad)": "LND", "Point Lisas Shore Base": "PLB", "Contracted rigs (land and offshore)": "RIG"}
GRADE_ORDER = lambda g: int(g[1]) if g and g[0] == "L" else 9
FUNC_ORDER = ["EXEC", "EXD", "WEL", "ENP", "OPS", "HSE", "FIN", "HR", "SCM", "IDK", "BDM", "CCS", "LGA"]

# ---------- staff changes (demonstration): one leaver replaced by a new hire, one internal move ----------
by_id = {r["Employee ID"]: r for r in rows}
for r in rows:
    r.setdefault("Status", "Active"); r.setdefault("Left Date", "")
changes = []
def find(title): return next(r for r in rows if r["Job Title"] == title and r.get("Status", "Active") == "Active")
if not any(r["Employee ID"] == "ACE-0301" for r in rows):
    old = find("Maintenance & Integrity Manager")
    new = dict(old); new.update({"Employee ID": "ACE-0301", "First Name": "Keisha", "Last Name": "Ramnarine", "Full Name": "Keisha Ramnarine", "Gender": "Female",
        "Age": "44", "Date of Birth": "1982-05-19", "Hire Date": "2026-09-14", "Base Degree": "BSc Mechanical Engineering", "Institution": "Saman University, Trinidad",
        "Postgraduate / Professional": "MSc Asset Management; Chartered Engineer", "Email": "keisha.ramnarine@ace-energy.example", "Status": "Active", "Left Date": ""})
    old["Status"] = "Left"; old["Left Date"] = "2026-08-31"
    for r in rows:   # the team now reports to the new manager
        if r["Reports To (ID)"] == old["Employee ID"]: r["Reports To (ID)"] = "ACE-0301"; r["Reports To"] = "Keisha Ramnarine (Maintenance & Integrity Manager)"
        if r["Dotted Line To (ID)"] == old["Employee ID"]: r["Dotted Line To (ID)"] = "ACE-0301"; r["Dotted Line To"] = "Keisha Ramnarine (Maintenance & Integrity Manager)"
    rows.append(new)
    changes += [["2026-08-31", old["Employee ID"], old["Full Name"], "Left", "Maintenance & Integrity Manager", "", "Left to join another operator"],
                ["2026-09-14", "ACE-0301", "Keisha Ramnarine", "Joined", "", "Maintenance & Integrity Manager", "Replaces Marc Gomes"]]
    # internal move: the offshore PTW coordinator becomes a production supervisor; a senior technician steps up
    ptw = find("Permit to Work Coordinator (Offshore)"); sup = find("Offshore Production Supervisor"); tech = find("Production Technician (Offshore)")
    for k in ["Job Title", "Grade", "Reports To (ID)", "Reports To", "Job Description", "OMS Role"]: pass
    tech_old = dict(tech)
    for k in ["Job Title", "Grade", "Reports To (ID)", "Reports To", "Job Description", "OMS Role", "Discipline", "Dotted Line To (ID)", "Dotted Line To", "Dotted Line Purpose"]:
        tech[k] = ptw[k]
    for k in ["Job Title", "Grade", "Reports To (ID)", "Reports To", "Job Description", "OMS Role", "Discipline", "Dotted Line To (ID)", "Dotted Line To", "Dotted Line Purpose"]:
        ptw[k] = sup[k]
    changes += [["2026-10-01", ptw["Employee ID"], ptw["Full Name"], "Moved", "Permit to Work Coordinator (Offshore)", "Offshore Production Supervisor", "Promotion"],
                ["2026-10-01", tech["Employee ID"], tech["Full Name"], "Moved", "Production Technician (Offshore)", "Permit to Work Coordinator (Offshore)", "Promotion"]]
    with open("company/org/staff_changes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["date", "employee_id", "name", "event", "from_role", "to_role", "note"]); w.writerows(changes)

# ---------- job roles ----------
active = [r for r in rows if r["Status"] == "Active"]
roles = collections.OrderedDict()
for r in sorted(active, key=lambda r: (FUNC_ORDER.index(r["Function Code"]), GRADE_ORDER(r["Grade"]), r["Job Title"])):
    roles.setdefault(r["Job Title"], []).append(r)
counter = collections.Counter(); rid = {}
for t, hs in roles.items():
    f = hs[0]["Function Code"]; counter[f] += 1; rid[t] = f"{f}-{counter[f]:02d}"
title_of = {r["Employee ID"]: r["Job Title"] for r in rows}
# short names used in documents, e.g. "Plant Manager" for "Plant Manager - Central Processing Facility"
short = collections.Counter(re.sub(r"\s*(\(.*\)|- .*)$", "", t) for t in roles)
def alias(t):
    s = re.sub(r"\s*(\(.*\)|- .*)$", "", t)
    extra = {"Offshore Installation Manager": "OIM", "Chief Executive Officer": "CEO", "Chief Financial Officer": "CFO"}.get(t, "")
    return "; ".join(x for x in [s if s != t and short[s] == 1 else "", extra] if x)

with open("company/org/roles.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["role_id", "title", "aliases", "function", "department", "grade", "reports_to", "dotted_to", "dotted_purpose", "discipline", "sites", "purpose", "oms_role_note"])
    for t, hs in roles.items():
        h = hs[0]
        mgr = title_of.get(h["Reports To (ID)"], ""); dot = title_of.get(h["Dotted Line To (ID)"], "")
        sites = sorted({SITE_OF.get(x["Work Location"], "HOF") for x in hs})
        w.writerow([rid[t], t, alias(t), h["Function Code"], h["Department"], h["Grade"], rid.get(mgr, ""), rid.get(dot, ""), h["Dotted Line Purpose"], h["Discipline"],
                    "; ".join(sites), h["Job Description"], h["OMS Role"]])

# ---------- people: add Role ID and Site, keep everything else ----------
for r in rows:
    r["Role ID"] = rid.get(r["Job Title"], "") if r["Status"] == "Active" else ""
    r["Site"] = SITE_OF.get(r["Work Location"], "HOF")
cols = HDR + [c for c in ["Role ID", "Site", "Status", "Left Date"] if c not in HDR]
with open(P, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

# ---------- OMS roles: duties that job roles carry ----------
R = lambda *ts: "; ".join(rid[t] for t in ts if t in rid)
leads = [t for t, hs in roles.items() if hs[0]["Discipline"] and t.endswith("Lead") and hs[0]["Dotted Line To (ID)"]]
OMS = [
    ["AA", "Area Authority", "Accountable for everything that happens at a location: plant status, permits, simultaneous operations and release of work.",
     R("Offshore Installation Manager", "Offshore Operations Manager (Gulf of Paria)", "Land Operations Manager", "Plant Manager - Central Processing Facility", "Logistics & Materials Manager", "Facilities & Administration Manager"), "", "ACE-OMS-MAN-001; ACE-COW-STD-001", "7; 8"],
    ["TA", "Technical Authority", "Discipline lead who owns the technical standards of a discipline and endorses designs, changes and deviations, independent of line management.",
     "; ".join(rid[t] for t in leads), "", "ACE-OMS-MAN-001; ACE-ENG-STD-901", "6; 5"],
    ["PA", "Performing Authority", "Leads a work party: accepts the permit, briefs the crew, monitors the work and hands the worksite back.",
     R("Offshore Production Supervisor", "Shift Supervisor (CPF)", "Field Supervisor (Land)", "Maintenance Superintendent", "Warehouse Supervisor", "Drilling Supervisor (Wellsite)"), "", "ACE-COW-STD-001", "8"],
    ["IA", "Isolating Authority", "Authorised to prepare, apply and verify energy isolations and to reinstate plant.",
     R("Control Room Operator (Offshore)", "Control Room Operator (CPF)", "Electrical & Instrument Technician", "Mechanical Technician"), "", "ACE-COW-STD-001; ACE-COW-PRC-001", "8"],
    ["PTWC", "Permit to Work Coordinator", "Runs the permit office at a site: checks permits, keeps the isolation register and plans simultaneous operations.",
     R("Permit to Work Coordinator (Offshore)", "Permit to Work Coordinator (CPF)"), "", "ACE-COW-PRC-001", "8"],
    ["WCA", "Well Control Authority", "ACE's representative at the wellsite, with authority over well control on the rig.", R("Drilling Supervisor (Wellsite)"), "", "ACE-WEL-STD-001", "8; 6"],
    ["EO", "Element Owner", "Executive who owns one of the ten OMS elements: its expectations, its performance and its improvement.", "", "elements", "ACE-OMS-MAN-001", "1; 10"],
    ["DO", "Document Owner", "Accountable for a controlled document: its content, its review on time and its revision.", "", "documents", "ACE-DOC-STD-001", "2; 7"],
    ["DC", "Document Controller", "Registers, checks, publishes and revises controlled documents.",
     R("Document Controller", "Engineering Document Controller", "Operations Document Controller", "Information Management Lead"), "", "ACE-DOC-STD-001; ACE-DOC-PRC-001", "2; 7"],
    ["RO", "Risk Owner", "Accountable for a risk in the register: its assessment, its controls and its actions.", "", "risks", "ACE-RSK-STD-001", "5"],
    ["CO", "Control Owner", "Accountable for one control: that it is in place, tested and working.", "", "controls", "ACE-RSK-STD-001", "5; 6"],
    ["PO", "Process Owner", "Accountable for a business process: its design, its performance and its improvement.", "", "processes", "ACE-BPM-PRA-001", "7; 10"],
    ["MOCC", "MOC Coordinator", "Screens and tracks changes through the Management of Change process.", R("Manager, Technical Excellence", "Operations Engineer (Offshore)", "Operations Engineer (CPF)", "Operations Engineer (Land)"), "", "ACE-MOC-PRC-001", "5"],
    ["ERC", "Emergency Response Coordinator", "Keeps emergency plans, drills and the response organisation ready.", R("Emergency Response & Security Manager", "Emergency Response Coordinator"), "", "ACE-EMR-STD-001", "5; 8"],
    ["AUD", "Auditor", "Independent check that the OMS works as written.", R("Head of Internal Audit & Risk Assurance", "Internal Auditor", "Compliance & Assurance Manager", "HSE Auditor"), "", "ACE-OMS-MAN-001", "10"],
    ["OMSM", "OMS Manager", "Custodian of the OMS framework and its mapping to the ten elements; runs conformance assessments.", R("OMS Manager"), "", "ACE-OMS-MAN-001", "2; 10"],
]
with open("company/org/oms_roles.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["oms_role_id", "name", "definition", "held_by", "derived_from", "defined_in", "elements"]); w.writerows(OMS)

# ---------- sites ----------
SITES = [
    ["HOF", "Head Office", "Corporate office", "Office", "Central Trinidad, close to the highway", "Executive, technical and support functions", "Facilities & Administration Manager", "", "", 64, 38],
    ["PLB", "Point Lisas Shore Base", "Marine base and warehouse", "Manned (day)", "Point Lisas", "Supply and crew boats to the Gulf of Paria; warehouse and laydown", "Logistics & Materials Manager", "", "", 42, 24],
    ["PAP", "Pommerac A", "Offshore production platform", "Manned, 14/14 rotation", "Gulf of Paria", "Separation, metering and export of crude and gas", "Offshore Installation Manager", "", "R-PAP", 13, 42],
    ["CHB", "Chenet B", "Wellhead platform", "Normally unmanned", "Gulf of Paria", "Wells tied back to Pommerac A", "Offshore Operations Manager (Gulf of Paria)", "PAP", "R-CHB", 8, 16],
    ["SAP", "Sapodilla C", "Wellhead platform", "Normally unmanned", "Gulf of Paria", "Wells tied back to Pommerac A", "Offshore Operations Manager (Gulf of Paria)", "PAP", "R-SAP", 10, 70],
    ["CPF", "Central Processing Facility", "Crude and gas processing plant", "Manned 24/7", "Central Trinidad, west coast", "Stabilises and stores crude, conditions and compresses gas, meters sales gas, loads crude", "Plant Manager - Central Processing Facility", "", "R-CPF", 38, 60],
    ["LND", "Land leases", "Tamarind, Pawpaw and Soursop leases", "Field-based", "Central and South Trinidad", "Oil and gas wells on pump jacks, tank batteries, gathering stations and flowlines", "Land Operations Manager", "", "R-LND", 68, 74],
    ["RIG", "Contracted rigs", "Drilling and workover rigs", "Mobile", "Land leases and Gulf of Paria", "Land rigs, workover units and a jack-up for offshore campaigns", "Drilling Supervisor (Wellsite)", "", "", 86, 90],
]
with open("company/org/sites.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["site_code", "name", "type", "manning", "location", "purpose", "area_authority", "parent", "risk_prefix", "map_x", "map_y"])
    for s in SITES: s[6] = rid.get(s[6], s[6]); w.writerow(s)

print(f"{len(roles)} job roles, {len(OMS)} OMS roles, {len(SITES)} sites, {len(rows)} people ({sum(r['Status']=='Active' for r in rows)} active), {len(changes)} staff changes")

# ---------- functions and cross-functional links (from the workbook, once) ----------
import openpyxl
wb = openpyxl.load_workbook("company/ACE_Organisation.xlsx")
heads = {r["Function Code"]: r for r in active if r["Grade"].startswith(("L1", "L2")) or r["Job Title"] in ("Chief Executive Officer",)}
with open("company/org/functions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["code", "name", "head_role", "purpose", "elements"])
    for row in wb["Functions"].iter_rows(min_row=2, values_only=True):
        if not row[0] or row[0] == "None": continue
        head = next((t for t, hs in roles.items() if hs[0]["Function Code"] == row[0] and hs[0]["Grade"][:2] in ("L1", "L2")), "")
        w.writerow([row[0], row[1], rid.get(head, ""), row[7], "; ".join(x.strip().lstrip("E") for x in str(row[8]).split(","))])
with open("company/org/function_links.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["from", "to", "strength", "nature"])
    for row in wb["Cross-Functional Links"].iter_rows(min_row=2, values_only=True):
        if row[0]: w.writerow([row[0], row[2], row[4], row[5]])
print("functions and links written")
