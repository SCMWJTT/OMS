import csv, sys
sys.path.insert(0, "/home/claude/oms/src")
from doclist import DOCS, W1, W2, W3
from elements import ELEMENTS
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

OUT = "/home/claude/oms/out"
EXP = {e[0]: e[1] for el in ELEMENTS for e in el["exps"]}
ELN = {el["n"]: el["title"] for el in ELEMENTS}
assert len(DOCS) == 30 and len({d["number"] for d in DOCS}) == 30
for d in DOCS:
    for t in d["tags"].split(","): assert t.strip() in EXP, (d["number"], t)
    for h in d["headings"]:
        for t in h[1].split(","): assert t.strip() in EXP, (d["number"], h[0], t)

cols = ["Priority","Wave","Document Number","Title","Type","Level","System","Primary OMS Tags","Elements","Est. Pages",
        "Author","Reviewers","Endorser (Technical Authority)","Approver","Why it is in the set","Built-in test faults","Status"]
def elements(tags): return ", ".join(sorted({t.split(".")[0] for t in tags.replace(" ","").split(",")}, key=int))
rows = [[d["pri"], d["wave"].split(" —")[0], d["number"], d["title"], d["type"], str(d["level"]), d["system"], d["tags"], elements(d["tags"]),
         d["pages"], d["author"], d["reviewers"], d["endorser"], d["approver"], d["why"], d["seed"] or "—", "To be written"] for d in DOCS]

with open(f"{OUT}/ACE_OMS_Document_Priority_List.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(rows)

wb = Workbook(); ws = wb.active; ws.title = "Priority List"
H = Font(name="Arial", bold=True, color="FFFFFF", size=10); F = Font(name="Arial", size=10)
ws.append(cols); [ws.append(r) for r in rows]
widths = [8,9,22,44,13,9,8,16,10,9,34,52,34,36,50,40,12]
for i, wdt in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = wdt
    c = ws.cell(1, i); c.font = H; c.fill = PatternFill("solid", fgColor="0E5A6B"); c.alignment = Alignment(wrap_text=True, vertical="center")
for row in ws.iter_rows(min_row=2):
    for c in row: c.font = F; c.alignment = Alignment(wrap_text=True, vertical="top")
ws.freeze_panes = "D2"; ws.row_dimensions[1].height = 32
t = Table(displayName="tblDocs", ref=f"A1:{get_column_letter(len(cols))}{len(rows)+1}"); t.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True); ws.add_table(t)

# headings sheet
hs = wb.create_sheet("Headings")
hc = ["Document Number","Title","Section No.","Heading","OMS Tags","What it covers"]
hs.append(hc)
for d in DOCS:
    for i, (h, tg, note) in enumerate(d["headings"], 1):
        hs.append([d["number"], d["title"], i, h, tg, note])
for i, wdt in enumerate([22,44,10,44,14,70], 1):
    hs.column_dimensions[get_column_letter(i)].width = wdt; c = hs.cell(1, i); c.font = H; c.fill = PatternFill("solid", fgColor="0E5A6B")
for row in hs.iter_rows(min_row=2):
    for c in row: c.font = F; c.alignment = Alignment(wrap_text=True, vertical="top")
hs.freeze_panes = "A2"
t2 = Table(displayName="tblHeadings", ref=f"A1:F{hs.max_row}"); t2.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True); hs.add_table(t2)

# summary with formulas
sm = wb.create_sheet("Summary")
sm.append(["Wave","Documents","Estimated pages"])
for i, wv in enumerate(["Wave 1","Wave 2","Wave 3"], 2):
    sm.append([wv, f'=COUNTIF(\'Priority List\'!$B$2:$B$31,A{i})', f'=SUMIF(\'Priority List\'!$B$2:$B$31,A{i},\'Priority List\'!$J$2:$J$31)'])
sm.append(["Total","=SUM(B2:B4)","=SUM(C2:C4)"])
sm.append([]); sm.append(["Element","Sections tagged (all 30 documents)","Expectations covered"])
start = sm.max_row + 1
for n in range(1, 11):
    allt = [t.strip() for d in DOCS for h in d["headings"] for t in h[1].split(",")]
    cov = sorted({t for t in allt if t.split(".")[0] == str(n)}, key=lambda x: int(x.split(".")[1]))
    total = len([k for k in EXP if k.split(".")[0] == str(n)])
    sm.append([f"{n} {ELN[n]}", f'=COUNTIF(Headings!$E$2:$E${hs.max_row},"*{n}.*")' if False else sum(1 for d in DOCS for h in d["headings"] if any(t.strip().split(".")[0]==str(n) for t in h[1].split(","))),
               f"{len(cov)} of {total}"])
for c in ("A","B","C"): sm.column_dimensions[c].width = 42 if c=="A" else 30
for r in (1, start-1):
    for c in sm[r]: c.font = H; c.fill = PatternFill("solid", fgColor="0E5A6B")
sm.cell(start+11, 1, "Element counts are computed from the Headings tab when the list was built; wave totals are live formulas.").font = Font(name="Arial", italic=True, size=9)
wb.save(f"{OUT}/ACE_OMS_Document_Priority_List.xlsx")

# ---------------- markdown ----------------
md = ["# ACE OMS — Priority Documents and Section Headings", "",
      "*Acme Caribbean Energy (fictional). Documentation programme for the OMS demonstration. Prepared 21 November 2026.*", "",
      "This file lists the **30 priority documents** that illustrate OMS at ACE, with the main (top-level) sections each will contain. "
      "Framing sections (purpose, scope, abbreviations, definitions, references, document control) are left out; every document will still carry them from the ACE template.",
      "", "Each heading shows the **OMS tags** it will carry (expectation numbers, most relevant first). Names come from the ACE organisation workbook. "
      "Numbers follow the ACE scheme in Part D of the OMS Manual (ACE-AAA-TTT-NNN-SSS).", "",
      "| Wave | Documents | Purpose |", "|---|---|---|",
      "| **Wave 1** | 1–10 | Drive the document management system and the web interface: the documentation rules, the Risk Matrix, the core integrity and control systems, incidents and audit |",
      "| **Wave 2** | 11–20 | Complete the wheel: policy, deviations, competence, contractors, emergency, wells, operating limits, inspection, KPIs, stakeholders |",
      "| **Wave 3** | 21–30 | Show the lower levels and site documents: procedures, a site emergency plan, a register, engineering documents, a work instruction and a form |", ""]
# coverage
def cov(ds):
    s = {t.strip() for d in ds for h in d["headings"] for t in h[1].split(",")} | {t.strip() for d in ds for t in d["tags"].split(",")}
    return s
c1, c12, c123 = cov(DOCS[:10]), cov(DOCS[:20]), cov(DOCS)
md += [f"**Expectation coverage:** Wave 1 addresses {len(c1)} of 54 expectations; Waves 1–2 address {len(c12)}; all 30 documents address {len(c123)}. "
       f"Not yet addressed by any of the 30: {', '.join('E'+k for k in EXP if k not in c123) or 'none'} (these are covered by the OMS Manual and later documents).", "",
       "**Built-in test faults:** two Wave 1 documents carry deliberate errors so the gateway check has something to catch in the demonstration (see documents 7 and 9).", "",
       "---", ""]
md += ["## Priority list", "", "| # | Number | Title | Pages | Author | Approver |", "|---|---|---|---:|---|---|"]
for d in DOCS:
    md.append(f"| {d['pri']} | {d['number']} | {d['title']} | {d['pages']} | {d['author'].split(' — ')[0]} | {d['approver'].split(' — ')[0]} |")
md += ["", "---", ""]
cur = None
for d in DOCS:
    if d["wave"] != cur:
        cur = d["wave"]; md += [f"## {cur}", ""]
    md += [f"### {d['pri']}. {d['title']}", "",
           f"**{d['number']}** · {d['type']} (Level {d['level']}) · System {d['system']} · Title tags **{d['tags']}** · about {d['pages']} pages", "",
           f"- **Author:** {d['author']}", f"- **Reviewers:** {d['reviewers']}", f"- **Endorser:** {d['endorser']}", f"- **Approver:** {d['approver']}",
           f"- **Why it is in the set:** {d['why']}"]
    if d["seed"]: md.append(f"- **Built-in test faults:** {d['seed']}")
    md += ["", "| No. | Heading | OMS tags | What it covers |", "|---|---|---|---|"]
    for i, (h, tg, note) in enumerate(d["headings"], 1):
        md.append(f"| {i} | {h} | {tg} | {note} |")
    md.append("")
md += ["---", "", "*Element titles and expectation numbering from IOGP Report 510 (2014), © IOGP and IPIECA, used with acknowledgement.*"]
open(f"{OUT}/ACE_OMS_Priority_Documents.md", "w").write("\n".join(md))
print("ok", len(c1), len(c12), len(c123))
