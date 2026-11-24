
# ================= document assembly (Rev 04) =================
REF_ADD = {"2.1": ["BPM-PRA-001"], "3.1": ["BPM-PRA-003"], "4.2": ["HMA-PRA-001"], "5.1": ["RSK-PRA-001"], "5.2": ["RSK-REG-002"],
           "5.3": ["MOC-PRS-001"], "6.2": ["ENG-SPC-410"], "6.3": ["OPS-PRA-001"], "6.4": ["MNT-PRA-001", "WEL-PRA-001"],
           "6.5": ["AIM-PRA-001"], "7.1": ["BPM-PRA-002"], "8.2": ["LOG-PRA-001", "COW-PRS-001"], "9.5": ["HMA-PRA-001"], "10.4": ["BPM-PRA-003"]}
REQ_ADD = {
 "3.1": "Every process in the Process Register shall have one named process owner, appointed in writing.",
 "5.1": "Every control that prevents or limits a significant risk shall carry a unique control ID and be recorded in the Controls Register, linked to its risk, the document section that requires it, the process step that performs it and the evidence that it works.",
 "7.1": "Every Standard and Standard Practice shall list the processes and procedures that put it into effect.",
 "10.4": "Each process owner shall review the performance of their process at least once a year and record the improvements agreed."}
for el in ELEMENTS:
    new = []
    for e in el["exps"]:
        e = list(e)
        e[5] = e[5] + [d for d in REF_ADD.get(e[0], []) if d not in e[5]]
        if e[0] in REQ_ADD: e[3] = e[3] + [REQ_ADD[e[0]]]
        new.append(tuple(e))
    el["exps"] = new

def dref(code):
    from register import ISSUED
    return ref(code)

# ---------------- cover ----------------
ct = doc.add_table(rows=1, cols=2); ct.autofit = False; no_borders(ct)
lc, rc = ct.rows[0].cells; lc.width, rc.width = Inches(4.5), Inches(2.0)
lp = lc.paragraphs[0]; lp.add_run().add_picture(f"{IMG}/one_mark.png", width=Inches(0.75)); r = lp.add_run("  ONE"); r.font.size = Pt(30)
r.font.name = "Segoe UI Semibold"; r.font.color.rgb = rgb(INK); tight(lp)
lp2 = lc.add_paragraph(); r = lp2.add_run("ONE MANAGEMENT SYSTEM"); r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = rgb(TEAL); tight(lp2)
rp = rc.paragraphs[0]; rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT; rp.add_run().add_picture(f"{IMG}/ace_logo.png", width=Inches(0.62)); tight(rp)
rp2 = rc.add_paragraph(); rp2.alignment = WD_ALIGN_PARAGRAPH.RIGHT; r = rp2.add_run("ACME CARIBBEAN ENERGY"); r.bold = True; r.font.size = Pt(7.5); r.font.color.rgb = rgb(FLARE); tight(rp2)
sp = doc.add_paragraph(); tight(sp, 6)
para("Document Kicker", "ACE  /  LEVEL 1 MANUAL  /  APPROVED CONTROLLED DOCUMENT")
p = doc.add_paragraph(style="Title"); p.add_run("OMS Manual"); bookmark(p, "doc_title"); tagline("doc_title", META["ODS.TitleOMSTags"])
para("Document SubTitle", "**One Management System** — how ACE works, every site, every day")
image("cover_wheel.png", 3.4)
band("ONE FRAMEWORK  ·  ONE SOURCE  ·  ONE WAY OF WORKING", "Safe, reliable and responsible operations — from the Gulf of Paria to the Central Processing Facility.", TEAL)
cm = doc.add_table(rows=2, cols=2); cm.autofit = False; borders(cm, "FFFFFF"); cell_margins(cm)
for (ri, ci), (lab, tag, val) in zip([(0, 0), (0, 1), (1, 0), (1, 1)], [("DOCUMENT NUMBER", "DocumentID", META["ODS.DocumentId"]), ("REVISION", "CoverRevision", "04 — Approved"),
                                                                    ("DOCUMENT STATUS", "CoverStatus", "Approved"), ("EFFECTIVE DATE", "CoverEffectiveDate", META["ODS.EffectiveDate"])]):
    c = cm.rows[ri].cells[ci]; c.width = Inches(3.25); cell_fill(c, "EAF2F3"); p = c.paragraphs[0]
    r = p.add_run(lab); r.bold = True; r.font.size = Pt(7.5); r.font.color.rgb = rgb(TEAL); tight(p)
    p2 = c.add_paragraph(); tight(p2); sdt_value(p2, f"ODS.Meta.{tag}", lab.title(), val, size=10, color=INK)
cv = doc.add_paragraph(style="ONE Cover Caption"); cv.add_run("The current approved revision is held in ONE. Printed copies are uncontrolled.")

# ---------------- document control ----------------
heading(1, "Document control", "front_control", "1.7")
meta_table([("Document number", "DocumentID", META["ODS.DocumentId"]), ("Title", "ControlTitle", META["ODS.Title"]),
            ("Document type and level", "DocumentType", "Manual (Level 1)"), ("Revision", "Revision", "04 (approved issue)"),
            ("Status", "Status", "Approved"), ("Issue date", "IssueDate", META["ODS.IssueDate"]), ("Effective date", "EffectiveDate", META["ODS.EffectiveDate"]),
            ("Document owner", "DocumentOwner", META["ODS.DocumentOwner"]), ("Custodian", "Custodian", META["ODS.Custodian"]),
            ("Author", "Author", META["ODS.Author"]), ("Reviewers", "Reviewer", META["ODS.Reviewer"]), ("Endorser", "Endorser", META["ODS.Endorser"]),
            ("Approver", "Approver", META["ODS.Approver"]), ("Parent document", "Parent", META["ODS.Parent"]),
            ("Primary function", "PrimaryFunction", META["ODS.PrimaryFunction"]), ("Framework", "Framework", META["ODS.Framework"]),
            ("Title OMS tags", "TitleOMSTags", META["ODS.TitleOMSTags"]), ("Classification", "Classification", META["ODS.Classification"]),
            ("Applies to", "Applicability", META["ODS.Applicability"]), ("Review interval", "ReviewInterval", META["ODS.ReviewInterval"])])
heading(2, "Revision history", "front_revhist", "1.7")
table(["Rev", "Date", "Description"], [
  ["01", "March 2019", "First issue. Brought the HSE, integrity and quality management systems under one framework based on IOGP 510."],
  ["02", "June 2023", "All ACE management systems moved inside OMS; one Risk Matrix and one document standard adopted."],
  ["03", "November 2025", "Renamed OMS — One Management System. Added the Part D documentation standard, OMS tags and the ONE portal; aligned with ISO/DIS 29501; expanded measures and maturity assessment."],
  ["04", "March 2026", "Added Standard Practices (Level 2) and Processes (Level 3) to a five-level hierarchy; the BPM, LOG and HMA systems; the process owner role; control IDs and the Controls Register; the data spine; the “OMS at work” section on core areas; process maturity; and the updated documentation standard and ONE gateway."]],
  [0.6, 1.3, 4.6], "plain")
heading(2, "Approval and issue", "front_approval", "2.2, 1.7")
table(["Role", "Person", "Recorded decision"], [["Author", META["ODS.Author"], "Prepared — 2 March 2026"],
  ["Reviewers", META["ODS.Reviewer"], "Reviewed — 9 March 2026"], ["Endorser", META["ODS.Endorser"], "Endorsed — 12 March 2026"],
  ["Approver", META["ODS.Approver"], "Approved — 16 March 2026"]], [1.2, 3.3, 2.0], "plain")
para("ODS.Note", "This approved issue is governed by the ACE controlled register. The signed or electronic approval record is retained with the authoritative Word source in ONE.", "Note", FLARE)

render(WELCOME); render(GLANCE); render(WHY); render(HOWTO); render(PART_A); render(WORK); render(PART_B_INTRO)

# ---------------- elements ----------------
for el in ELEMENTS:
    n = el["n"]; c = ELC[n]
    heading(1, f"Element {n} — {el['title']}", f"el_{n}", "", color=c)
    para("OMS.ElementKicker", f"{GROUP[n]}  ·  Element owner: {el['owner']}")
    t = doc.add_table(rows=1, cols=2); t.autofit = False; no_borders(t); cell_pad(t, 160, 200)
    left, right = t.rows[0].cells
    left.width, right.width = Inches(1.6), Inches(4.9); cell_fill(right, c); cell_fill(left, c)
    lp = left.paragraphs[0]; lp.add_run().add_picture(f"{IMG}/el{n}.png", width=Inches(1.35)); tight(lp)
    rp = right.paragraphs[0]; r = rp.add_run(el["purpose"]); r.font.size = Pt(11.5); r.font.color.rgb = rgb("FFFFFF"); r.font.name = "Segoe UI"; tight(rp)
    sp = doc.add_paragraph(); tight(sp, 6)
    para("ODS.Note", el["you"], "What this means for you", FLARE)
    for (num, title, intent, reqs, resp, docs, kpi, note, extra) in el["exps"]:
        tags = ", ".join([num] + extra)
        heading(2, f"{num}  {title}", "s" + num.replace(".", "_"), tags)
        para("Normal", intent)
        for rq in reqs: para("ODS.Requirement", rq)
        para("ODS.Responsibility", resp)
        for d in docs: para("ODS.DocumentReference", dref(d))
        para("ODS.PerformanceIndicator", kpi, "Measure", "3D5A80")
        if note: para("ODS.Note", note, "What this means for you", FLARE)

render(PART_C); render(PART_D); render(appendix_blocks(ELEMENTS))
p = doc.add_paragraph(); tight(p, 0, 18); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run().add_picture(f"{IMG}/one_mark.png", width=Inches(0.5))
p = doc.add_paragraph(style="ONE Cover Caption"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run("One framework. One source. One way of working.")

# ---------------- header / footer ----------------
sec = doc.sections[0]; sec.different_first_page_header_footer = True
hp = sec.header.paragraphs[0]
hp.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), alignment=2)
add_runs(hp, "ONE", 8.5, TEAL); hp.runs[-1].bold = True
add_runs(hp, "  |  ACME CARIBBEAN ENERGY", 7.5, MUTE)
add_runs(hp, "\t\tOMS MANUAL  •  ACE-OMS-MAN-001  •  REV 04", 7.5, MUTE)
fp = sec.footer.paragraphs[0]
add_runs(fp, "ONE", 8, TEAL); fp.runs[-1].bold = True
add_runs(fp, "  |  ACME CARIBBEAN ENERGY   ", 7.5, FLARE); fp.runs[-1].bold = True
add_runs(fp, "Printed copies are uncontrolled   •   Page ", 7.5, MUTE); field(fp, "PAGE")
for r in fp.runs[-5:]: r.font.size = Pt(7.5); r.font.color.rgb = rgb(MUTE)
ffp = sec.first_page_footer.paragraphs[0]; ffp.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_runs(ffp, "ONE  •  ONE MANAGEMENT SYSTEM   |   ACME CARIBBEAN ENERGY LIMITED", 7.5, MUTE)

settings = doc.settings.element; uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true")
insert_before(settings, uf, ["w:hdrShapeDefaults", "w:footnotePr", "w:endnotePr", "w:compat", "w:docVars", "w:rsids"])
z = settings.find(qn("w:zoom"))
if z is not None and z.get(qn("w:percent")) is None: z.set(qn("w:percent"), "100")
cp = doc.core_properties
cp.title = META["ODS.Title"]; cp.author = "Marissa Bobb"; cp.subject = META["ODS.DocumentId"]; cp.keywords = META["ODS.TitleOMSTags"]
cp.category = "Manual (Level 1)"; cp.content_status = "Approved"; cp.identifier = META["ODS.DocumentId"]
cp.comments = f"Rev 04 · Effective {META['ODS.EffectiveDate']} · Owner: Satesh Sankar"; cp.last_modified_by = "Marissa Bobb"; cp.revision = 4
cp.created = dt.datetime(2026, 3, 2, 9, 0); cp.modified = dt.datetime(2026, 3, 16, 15, 0)
# fix table grids so every renderer uses the intended column widths
for t in doc.tables:
    tcs = t.rows[0]._tr.findall(qn("w:tc"))
    ws = []
    for tc in tcs:
        w = tc.find(qn("w:tcPr") + "/" + qn("w:tcW"))
        ws.append(int(w.get(qn("w:w"))) if w is not None and w.get(qn("w:type")) == "dxa" else None)
    if None in ws: continue
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), ws): gc.set(qn("w:w"), str(w))
    tblPr = t._tbl.tblPr; tw = tblPr.find(qn("w:tblW"))
    if tw is None: tw = OxmlElement("w:tblW"); insert_before(tblPr, tw, ["w:jc","w:tblCellSpacing","w:tblInd","w:tblBorders","w:shd","w:tblLayout","w:tblCellMar","w:tblLook","w:tblCaption","w:tblDescription"])
    tw.set(qn("w:w"), str(sum(ws))); tw.set(qn("w:type"), "dxa")
    lay = tblPr.find(qn("w:tblLayout"))
    if lay is None: lay = OxmlElement("w:tblLayout"); insert_before(tblPr, lay, ["w:tblCellMar","w:tblLook","w:tblCaption","w:tblDescription"])
    lay.set(qn("w:type"), "fixed")
tmp = f"{OUT}/_tmp4.docx"; doc.save(tmp)
