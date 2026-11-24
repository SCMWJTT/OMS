import json, csv, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

d = json.load(open("/home/claude/ace/ace.json"))
P = d["people"]; byid = {p["id"]: p for p in P}
FN = {f[0]: f for f in d["functions"]}
first = lambda key: byid[d["holders"][key][0]]

F = "Arial"
H = Font(name=F, bold=True, color="FFFFFF", size=10)
HF = PatternFill("solid", fgColor="1F3A5F")
B = Font(name=F, size=10); BB = Font(name=F, size=10, bold=True)
T = Font(name=F, size=16, bold=True, color="1F3A5F")
WR = Alignment(wrap_text=True, vertical="top")

wb = Workbook()

def sheet(title, headers, rows, widths, table=True, wrap_cols=()):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for r in rows: ws.append(r)
    for c in range(1, len(headers)+1):
        cell = ws.cell(1, c); cell.font = H; cell.fill = HF
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(c)].width = widths[c-1]
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = B
            cell.alignment = WR if cell.column in wrap_cols else Alignment(vertical="top")
    ws.freeze_panes = "B2" if title == "People" else "A2"
    ws.row_dimensions[1].height = 30
    if table:
        ref = f"A1:{get_column_letter(len(headers))}{len(rows)+1}"
        t = Table(displayName="tbl" + title.replace(" ", "").replace("&", ""), ref=ref)
        t.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
        ws.add_table(t)
    return ws

# ---------------- People ----------------
PH = ["Employee ID","First Name","Last Name","Full Name","Gender","Age","Date of Birth","Hire Date",
      "Job Title","Function Code","Function","Department","Grade","Reports To (ID)","Reports To",
      "Dotted Line To (ID)","Dotted Line To","Dotted Line Purpose","Discipline","OMS Role",
      "Work Location","Work Pattern","Base Degree","Institution","Postgraduate / Professional","Email","Job Description"]
rows = []
for p in P:
    rows.append([p["id"],p["first"],p["last"],p["name"],p["gender"],p["age"],p["birth"],p["hire"],
                 p["title"],p["fn"],FN[p["fn"]][1],p["dept"],p["level"],p["reports_to"],p["reports_to_name"],
                 p["dotted_to"],p["dotted_to_name"],p["dotted_purpose"],p["disc"],p["oms"],
                 p["location"],p["pattern"],p["degree"],p["institution"],p["postgrad"],p["email"],p["jd"]])
W = [11,12,14,22,8,6,11,11,36,9,26,28,26,12,40,12,40,40,22,40,34,20,38,40,30,38,80]
ws = sheet("People", PH, rows, W, wrap_cols=(27,))
import datetime as dt
for r in range(2, len(rows)+2):
    for c in (7, 8):
        cell = ws.cell(r, c); cell.value = dt.date.fromisoformat(cell.value); cell.number_format = "yyyy-mm-dd"

with open("/home/claude/ace/out/ACE_People.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(PH); w.writerows(rows)

# column letters in People for formulas
col = {h: get_column_letter(i+1) for i, h in enumerate(PH)}
def rng(h): return f"People!${col[h]}$2:${col[h]}${len(rows)+1}"

# ---------------- Functions ----------------
frows = []
for code, name, headkey, purpose, elems in d["functions"]:
    h = first(headkey)
    frows.append([code, name, h["name"], h["title"], None, None, None, purpose, elems])
ws = sheet("Functions", ["Code","Function","Head","Head Title","Headcount","Female","Male","Purpose","Main OMS Elements"],
           frows, [8,32,22,42,11,9,9,80,18], wrap_cols=(8,))
for i in range(2, len(frows)+2):
    ws[f"E{i}"] = f'=COUNTIF({rng("Function Code")},A{i})'
    ws[f"F{i}"] = f'=COUNTIFS({rng("Function Code")},A{i},{rng("Gender")},"Female")'
    ws[f"G{i}"] = f'=COUNTIFS({rng("Function Code")},A{i},{rng("Gender")},"Male")'
n = len(frows) + 2
ws[f"D{n}"] = "Total"; ws[f"D{n}"].font = BB
for c in "EFG":
    ws[f"{c}{n}"] = f"=SUM({c}2:{c}{n-1})"; ws[f"{c}{n}"].font = BB

# ---------------- Discipline Leads ----------------
leads = [p for p in P if p["oms"].startswith("Technical Authority")]
drows = []
for p in sorted(leads, key=lambda x: x["disc"]):
    drows.append([p["disc"], p["name"], p["id"], p["title"], FN[p["fn"]][1], p["dept"], p["reports_to_name"],
                  "VP Engineering & Projects (Technical Leadership Council)", None, p["jd"]])
ws = sheet("Discipline Leads", ["Discipline","Discipline Lead","Employee ID","Title","Home Function","Department",
           "Solid Line (Line Manager)","Dotted Line","People in Discipline (incl. lead)","Technical Authority Scope"],
           drows, [28,22,11,34,28,30,44,36,14,80], wrap_cols=(10,))
for i in range(2, len(drows)+2):
    ws[f"I{i}"] = f'=COUNTIF({rng("Discipline")},A{i})'

# ---------------- Cross-Functional Links ----------------
lrows = [[a, FN[a][1], b, FN[b][1], s, nat] for a, b, nat, s in d["links"]]
sheet("Cross-Functional Links", ["From Code","From Function","To Code","To Function","Strength","Nature of Relationship"],
      lrows, [10,30,10,30,10,80], wrap_cols=(6,))

# ---------------- OMS Element Owners ----------------
erows = []
for e, t, key, contrib in d["elements"]:
    h = first(key); erows.append([e, t, h["name"], h["title"], contrib])
sheet("OMS Element Owners", ["Element","IOGP 510 Element Title","Element Owner","Owner Title","Key Contributing Functions"],
      erows, [9,38,22,42,60], wrap_cols=(5,))

# ---------------- Assets & Locations ----------------
arows = [list(a) for a in d["assets"]]
sheet("Assets", ["Asset","Type","Manning","Location","Purpose","Area Authority / Responsible Role"],
      arows, [30,36,30,24,60,44], wrap_cols=(5,))
locs = sorted(set(p["location"] for p in P))
ws = sheet("Locations", ["Work Location","Headcount"], [[l, None] for l in locs], [44,12])
for i in range(2, len(locs)+2):
    ws[f"B{i}"] = f'=COUNTIF({rng("Work Location")},A{i})'

# ---------------- Grades ----------------
grades = sorted(set(p["level"] for p in P))
ws = sheet("Grades", ["Grade","Headcount","Female","Male","Average Age"], [[g,None,None,None,None] for g in grades], [36,12,10,10,13])
for i in range(2, len(grades)+2):
    ws[f"B{i}"] = f'=COUNTIF({rng("Grade")},A{i})'
    ws[f"C{i}"] = f'=COUNTIFS({rng("Grade")},A{i},{rng("Gender")},"Female")'
    ws[f"D{i}"] = f'=COUNTIFS({rng("Grade")},A{i},{rng("Gender")},"Male")'
    ws[f"E{i}"] = f'=AVERAGEIF({rng("Grade")},A{i},{rng("Age")})'; ws[f"E{i}"].number_format = "0.0"

# ---------------- README ----------------
ws = wb["Sheet"]; ws.title = "README"
lines = [
 ("Acme Caribbean Energy (ACE) - Fictional Organisation", T),
 ("Reference organisation for OMS, document control and other demonstration projects.", BB),
 ("", B),
 ("Everything in this workbook is fictional. Names were generated and any resemblance to real people is coincidental.", B),
 ("Ages are as at 21 November 2026. Emails use the reserved domain ace-energy.example.", B),
 ("ACE is a mid-size crude and gas producer with 300 staff. Head office in Central Trinidad, shore base at Point Lisas,", B),
 ("small offshore fields in the Gulf of Paria, land leases in Central and South Trinidad, and a Central Processing Facility", B),
 ("that sells gas to NGC and ships crude by tanker or barge. See ACE_Company_Profile.md for the full description.", B),
 ("", B),
 ("Tabs", BB),
 ("People - all 300 employees, reporting lines, dotted lines, OMS roles and job descriptions (also supplied as ACE_People.csv).", B),
 ("Functions - the 13 functions, their heads and live headcounts (formulas count from People).", B),
 ("Discipline Leads - 32 discipline leads. Each has a solid line in a home function and a dotted line to the VP Engineering & Projects", B),
 ("     through the Technical Leadership Council. Each is the Technical Authority for the discipline.", B),
 ("Cross-Functional Links - how functions depend on each other (used for the org chart network view).", B),
 ("OMS Element Owners - owner of each IOGP 510 element and the functions that contribute.", B),
 ("Assets, Locations, Grades - asset register, headcount by location and by grade.", B),
 ("", B),
 ("Editing", BB),
 ("Edit People freely; the counts on Functions, Discipline Leads, Locations and Grades update automatically.", B),
 ("Keep Employee IDs unique; Reports To (ID) and Dotted Line To (ID) refer to Employee IDs.", B),
 ("To update the org chart: save the People tab as CSV (UTF-8), open the org chart and use 'Load CSV'. Keep the column headers unchanged.", B),
 ("", B),
 ("IOGP 510 element titles: IOGP Report 510, Operating Management System Framework (2014), IOGP / IPIECA.", B),
 ("Created by Cynmark Systems Limited for demonstration use.", B),
]
for i, (txt, f) in enumerate(lines, 1):
    ws.cell(i, 1, txt).font = f
ws.column_dimensions["A"].width = 130

wb.save("/home/claude/ace/out/ACE_Organisation.xlsx")
print("saved")
