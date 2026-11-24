import re, copy, zipfile, shutil, os, datetime as dt
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from parts import FOREWORD, GLANCE, HOWTO, PART_A, PART_B_INTRO, PART_C, PART_D, appendix_blocks
from elements import ELEMENTS
from register import ref, DOCS

IMG = "/home/claude/oms/img"; OUT = "/home/claude/oms/out"; os.makedirs(OUT, exist_ok=True)
INK, TEAL, FLARE, SAND, SKY, MUTE = "12232E", "0E5A6B", "F26B21", "F6F1E8", "A7D8E3", "5B6B73"
ELC = {1:"0B4F5E",2:"0F6B7A",3:"1E8796",4:"3AA3AE",5:"D9480F",6:"F26B21",7:"F5923E",8:"F8B26A",9:"3D5A80",10:"5C7BA6"}
GROUP = {1:"LEAD",2:"LEAD",3:"LEAD",4:"LEAD",5:"CONTROL",6:"CONTROL",7:"CONTROL",8:"CONTROL",9:"LEARN",10:"LEARN"}
HFONT, BFONT = "Segoe UI Semibold", "Calibri"
META = {
 "ODS.DocumentId":"ACE-OMS-MAN-001","ODS.Title":"One Management System (OMS) Manual","ODS.DocumentType":"Manual",
 "ODS.Revision":"03","ODS.Status":"APPROVED","ODS.IssueDate":"2025-11-21","ODS.EffectiveDate":"2026-01-01",
 "ODS.Author":"Marissa Bobb — OMS Manager","ODS.Reviewer":"George Habib — VP HSE & Compliance",
 "ODS.Approver":"Satesh Sankar — Chief Executive Officer","ODS.DocumentOwner":"Chief Executive Officer",
 "ODS.ProcessOwner":"OMS Manager","ODS.PrimaryFunction":"HSE & Compliance","ODS.Framework":"IOGP 510 (2014)",
 "ODS.TitleOMSTags":"1.1, 2.1, 7.1","ODS.Classification":"Internal","ODS.Applicability":"All ACE activities, sites, staff and contractors",
 "ODS.RoleRegister":"Chief Executive Officer; Element Owner; System Owner; OMS Manager; Area Authority; Technical Authority; Information Management Lead; Line Manager; Supervisor; All personnel",
}

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = Inches(1); sec.top_margin = Inches(0.9); sec.bottom_margin = Inches(0.9)

# ---------------- styles ----------------
def rgb(h): return RGBColor.from_string(h)
def set_font(style, name, size, color=INK, bold=None, italic=None):
    f = style.font; f.name = name; f.size = Pt(size); f.color.rgb = rgb(color)
    if bold is not None: f.bold = bold
    if italic is not None: f.italic = italic
    rpr = style.element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
    if rf is None: rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for a in ("w:ascii","w:hAnsi","w:cs"): rf.set(qn(a), name)
def pfmt(style, before=0, after=6, line=1.15, left=None, keep=False, pb=False):
    pf = style.paragraph_format; pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = line
    if left is not None: pf.left_indent = Inches(left)
    pf.keep_with_next = keep; pf.page_break_before = pb
def shade_style(style, fill, border):
    ppr = style.element.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr"); l = OxmlElement("w:left")
    for k,v in (("w:val","single"),("w:sz","24"),("w:space","8"),("w:color",border)): l.set(qn(k),v)
    bdr.append(l)
    later = ["w:shd","w:tabs","w:suppressAutoHyphens","w:spacing","w:ind","w:jc","w:outlineLvl","w:rPr"]
    insert_before(ppr, bdr, later)
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),fill)
    insert_before(ppr, shd, later[1:])
    ind = ppr.find(qn("w:ind"))
    if ind is None:
        ind = OxmlElement("w:ind"); insert_before(ppr, ind, ["w:jc","w:outlineLvl","w:rPr"])
    if ind.get(qn("w:left")) is None: ind.set(qn("w:left"),"200")
    ind.set(qn("w:right"),"120")


def insert_before(parent, el, names):
    for ch in parent:
        if ch.tag in [qn(n) for n in names]:
            ch.addprevious(el); return
    parent.append(el)

st = doc.styles
set_font(st["Normal"], BFONT, 11); pfmt(st["Normal"], 0, 7, 1.18)
set_font(st["Title"], HFONT, 34, INK); pfmt(st["Title"], 6, 4, 1.0)
# remove Title's default bottom border
tp = st["Title"].element.get_or_add_pPr()
for b in tp.findall(qn("w:pBdr")): tp.remove(b)
set_font(st["Heading 1"], HFONT, 22, TEAL, bold=False); pfmt(st["Heading 1"], 0, 4, 1.05, keep=True, pb=True)
set_font(st["Heading 2"], HFONT, 14.5, INK, bold=False); pfmt(st["Heading 2"], 16, 2, 1.05, keep=True)
set_font(st["Heading 3"], HFONT, 12, TEAL, bold=False); pfmt(st["Heading 3"], 12, 2, 1.05, keep=True)
set_font(st["Caption"], BFONT, 9, MUTE, italic=True); pfmt(st["Caption"], 2, 12, 1.0)
set_font(st["List Bullet"], BFONT, 11); pfmt(st["List Bullet"], 0, 4, 1.15)

def pstyle(name, size=10.5, color=INK, fill=None, border=None, italic=None, bold=None, before=4, after=6, left=None, font=BFONT):
    s = st.add_style(name, WD_STYLE_TYPE.PARAGRAPH); s.base_style = st["Normal"]
    set_font(s, font, size, color, bold=bold, italic=italic); pfmt(s, before, after, 1.12, left=left)
    if fill: shade_style(s, fill, border)
    return s
pstyle("ODSTagLine", 8, TEAL, before=0, after=8, font="Segoe UI")
st["ODSTagLine"].name = "ODS Tag Line"
pstyle("DocumentKicker", 10, FLARE, bold=True, before=0, after=2, font="Segoe UI Semibold"); st["DocumentKicker"].name = "Document Kicker"
pstyle("DocumentSubTitle", 12, MUTE, before=0, after=10, font="Segoe UI"); st["DocumentSubTitle"].name = "Document SubTitle"
pstyle("ODS.Requirement", fill="FDEEE4", border=FLARE)
pstyle("ODS.Responsibility", fill="E6F1F3", border=TEAL)
pstyle("ODS.ApprovalRequirement", fill="ECEFF3", border="3D5A80")
pstyle("ODS.RecordRequirement", fill="F1F1F1", border=MUTE)
pstyle("ODS.RiskControl", fill="E6F1F3", border="1E8796")
pstyle("ODS.Warning", fill="FDE7E4", border="C0392B", bold=True)
pstyle("ODS.PerformanceIndicator", 10, fill="EEF2F8", border="5C7BA6")
pstyle("ODS.Note", 10.5, fill=SAND, border=SKY, before=8, after=10)
pstyle("ODS.DocumentReference", 10, TEAL, before=0, after=3, left=0.25)
pstyle("ODS.ExternalStandard", 9, MUTE, italic=True, before=2, after=6)
pstyle("ODS.ProcedureStep", 10.5, before=0, after=5, left=0.25)
pstyle("ODS.Definition", 10.5, before=0, after=5, left=0.25)
pstyle("OMS.ElementKicker", 10, FLARE, bold=True, before=0, after=8, font="Segoe UI Semibold")

# ---------------- helpers ----------------
_bm = [100]
def add_runs(p, text, size=None, color=None):
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not part: continue
        if part.startswith("**"): r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith("*"): r = p.add_run(part[1:-1]); r.italic = True
        else: r = p.add_run(part)
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = rgb(color)
    return p
def para(style, text="", label=None, label_color=None):
    p = doc.add_paragraph(style=style)
    if label:
        r = p.add_run(label + "  "); r.bold = True
        if label_color: r.font.color.rgb = rgb(label_color)
    add_runs(p, text); return p
def bookmark(p, name):
    _bm[0] += 1; i = str(_bm[0])
    s = OxmlElement("w:bookmarkStart"); s.set(qn("w:id"), i); s.set(qn("w:name"), name)
    e = OxmlElement("w:bookmarkEnd"); e.set(qn("w:id"), i)
    ppr = p._p.find(qn("w:pPr")); idx = 1 if ppr is not None else 0
    p._p.insert(idx, s); p._p.append(e)
def tagline(bm, tags):
    p = doc.add_paragraph(style="ODS Tag Line")
    r = p.add_run("OMS  "); r.bold = True; r.font.color.rgb = rgb(FLARE)
    sdt = OxmlElement("w:sdt"); pr = OxmlElement("w:sdtPr")
    for tagname, val in (("w:alias","OMS Tags"),("w:tag",f"ODS.OMSTags@{bm}")):
        x = OxmlElement(tagname); x.set(qn("w:val"), val); pr.append(x)
    x = OxmlElement("w:id"); x.set(qn("w:val"), str(abs(hash(bm)) % 2000000000)); pr.append(x)
    pr.append(OxmlElement("w:text")); sdt.append(pr)
    c = OxmlElement("w:sdtContent"); rr = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    col = OxmlElement("w:color"); col.set(qn("w:val"), TEAL); rpr.append(col); rr.append(rpr)
    t = OxmlElement("w:t"); t.text = tags; rr.append(t); c.append(rr); sdt.append(c); p._p.append(sdt)
def heading(level, text, bm, tags, color=None):
    style = {0:"Title",1:"Heading 1",2:"Heading 2",3:"Heading 3"}[level]
    p = doc.add_paragraph(style=style); r = p.add_run(text)
    if color: r.font.color.rgb = rgb(color)
    bookmark(p, bm)
    if tags: tagline(bm, tags)
    return p
def cell_fill(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),fill); tcPr.append(shd)
def cell_margins(tbl):
    tblPr = tbl._tbl.tblPr; m = OxmlElement("w:tblCellMar")
    for side, v in (("top",60),("left",90),("bottom",60),("right",90)):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"),"dxa"); m.append(e)
    insert_before(tblPr, m, ["w:tblLook","w:tblCaption","w:tblDescription"])
def borders(tbl, color="D3DCE0"):
    tblPr = tbl._tbl.tblPr; b = OxmlElement("w:tblBorders")
    for side in ("top","left","bottom","right","insideH","insideV"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"),"single"); e.set(qn("w:sz"),"4"); e.set(qn("w:color"),color); b.append(e)
    insert_before(tblPr, b, ["w:shd","w:tblLayout","w:tblCellMar","w:tblLook","w:tblCaption","w:tblDescription"])
def table(headers, rows, widths, kind="plain"):
    t = doc.add_table(rows=1, cols=len(headers)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    borders(t); cell_margins(t)
    size = 8.5 if kind == "index" else 9.5
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = ""; p = c.paragraphs[0]; r = p.add_run(h); r.bold = True
        r.font.size = Pt(size); r.font.color.rgb = rgb("FFFFFF"); cell_fill(c, TEAL if kind != "plain" else INK)
        p.paragraph_format.space_after = Pt(0)
    trPr = t.rows[0]._tr.get_or_add_trPr(); th = OxmlElement("w:tblHeader"); th.set(qn("w:val"),"true"); trPr.append(th)
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            c = cells[i]; c.text = ""; p = c.paragraphs[0]; add_runs(p, str(v), size=size)
            p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.05
            if i == 0 and kind in ("brand","index"):
                for r in p.runs: r.bold = True; r.font.color.rgb = rgb(TEAL)
            if ri % 2 == 1: cell_fill(c, "F4F7F8")
    for row in t.rows:
        for i, w in enumerate(widths): row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t
def image(fname, width, caption=None):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(f"{IMG}/{fname}", width=Inches(width)); p.paragraph_format.space_after = Pt(2)
    if caption: c = doc.add_paragraph(caption, style="Caption"); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
def field(p, instr):
    r = p.add_run(); a = OxmlElement("w:fldChar"); a.set(qn("w:fldCharType"),"begin"); r._r.append(a)
    r2 = p.add_run(); it = OxmlElement("w:instrText"); it.set(qn("xml:space"),"preserve"); it.text = instr; r2._r.append(it)
    r3 = p.add_run(); b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"),"separate"); r3._r.append(b)
    r4 = p.add_run("1" if "PAGE" in instr else "Right-click and choose Update Field to build the table of contents.")
    r5 = p.add_run(); c = OxmlElement("w:fldChar"); c.set(qn("w:fldCharType"),"end"); r5._r.append(c)
def matrix():
    lik = [("E","Expected: several times a year at ACE"),("D","Likely: has happened at ACE"),("C","Possible: has happened in the industry"),("B","Unlikely: heard of in the industry"),("A","Rare: not heard of in the industry")]
    lv = {"L":("Low","DFF2E3"),"M":("Medium","FFF3C4"),"H":("High","FBD3B0"),"V":("Very High","F4A6A0")}
    def rate(c,l):
        s = c + l
        return "L" if s <= 4 else "M" if s <= 6 else "H" if s <= 8 else "V"
    t = doc.add_table(rows=1, cols=6); t.alignment = WD_TABLE_ALIGNMENT.CENTER; borders(t, "FFFFFF"); cell_margins(t)
    hdr = ["Likelihood ↓  Consequence →","1 Minor","2 Moderate","3 Serious","4 Major","5 Catastrophic"]
    for i,h in enumerate(hdr):
        c=t.rows[0].cells[i]; c.text=""; r=c.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(8.5); r.font.color.rgb=rgb("FFFFFF"); cell_fill(c, INK)
    for li,(L,desc) in enumerate(lik):
        cells=t.add_row().cells; lnum = 5-li
        cells[0].text=""; r=cells[0].paragraphs[0].add_run(f"{L}  {desc}"); r.font.size=Pt(8.5); r.bold=True; cell_fill(cells[0],"EEF2F4")
        for ci in range(1,6):
            k=rate(ci,lnum); name,fill=lv[k]; cells[ci].text=""; p=cells[ci].paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            r=p.add_run(name); r.font.size=Pt(8.5); r.bold=True; cell_fill(cells[ci],fill)
    for row in t.rows:
        for i,w in enumerate([2.0,0.9,0.9,0.9,0.9,0.9]): row.cells[i].width=Inches(w)
    c = doc.add_paragraph("Figure 4. ACE Risk Matrix (summary)", style="Caption"); c.alignment = WD_ALIGN_PARAGRAPH.CENTER

STYLE_OF = {"req":"ODS.Requirement","resp":"ODS.Responsibility","ref":"ODS.DocumentReference","kpi":"ODS.PerformanceIndicator",
            "note":"ODS.Note","ext":"ODS.ExternalStandard","ctrl":"ODS.RiskControl","warn":"ODS.Warning","appr":"ODS.ApprovalRequirement",
            "rec":"ODS.RecordRequirement","step":"ODS.ProcedureStep","p":"Normal","bul":"List Bullet"}
def render(blocks):
    for b in blocks:
        k = b[0]
        if k in ("h1","h2","h3"): heading(int(k[1]), b[1], b[2], b[3])
        elif k == "img": image(b[1], b[2], b[3])
        elif k == "table": table(b[1], b[2], b[3], b[4])
        elif k == "matrix": matrix()
        elif k == "toc":
            heading(2, "Contents", "front_toc", ""); p = doc.add_paragraph(); field(p, 'TOC \\o "1-2" \\h \\z \\u')
        elif k == "def":
            term, text = b[1].split(" — ", 1); p = doc.add_paragraph(style="ODS.Definition")
            r = p.add_run(term); r.bold = True; r.font.color.rgb = rgb(TEAL); p.add_run("  " + text)
        elif k == "note": para("ODS.Note", b[1], "What this means for you" if "you" in b[1].lower() else "Note", FLARE)
        elif k == "kpi": para("ODS.PerformanceIndicator", b[1], "Measure", "3D5A80")
        else: para(STYLE_OF[k], b[1])

# ---------------- cover ----------------
para("Document Kicker", "ACME CARIBBEAN ENERGY LIMITED")
p = doc.add_paragraph(style="Title"); p.add_run("OMS Manual"); bookmark(p, "doc_title"); tagline("doc_title", META["ODS.TitleOMSTags"])
para("Document SubTitle", "**One Management System** — how ACE works, every site, every day")
image("cover_wheel.png", 4.9)
cv = doc.add_paragraph(); cv.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_runs(cv, f"MANUAL  ·  {META['ODS.DocumentId']}  ·  Revision {META['ODS.Revision']}  ·  Effective 1 January 2027", 10, MUTE)
cv2 = doc.add_paragraph(); cv2.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_runs(cv2, "The current approved revision is on the OMS portal. Printed copies are uncontrolled.", 9, MUTE)

# ---------------- document control ----------------
heading(1, "Document control", "front_control", "")
table(["Property","Value"], [["Document number", META["ODS.DocumentId"]],["Title", META["ODS.Title"]],["Type", "Manual (Level 1)"],
   ["Revision", META["ODS.Revision"] + " (approved issue)"],["Status", "Approved"],["Issue date","21 November 2026"],["Effective date","1 January 2027"],
   ["Document owner","Chief Executive Officer"],["Custodian","OMS Manager"],["Author", META["ODS.Author"]],["Reviewer", META["ODS.Reviewer"]],
   ["Approver", META["ODS.Approver"]],["Framework","IOGP 510 (2014); aligned with ISO/DIS 29501"],["Classification","Internal"],
   ["Applies to", META["ODS.Applicability"]],["Next review","November 2029"]], [2.0,4.5], "brand")
heading(3, "Revision history", "front_revhist", "")
table(["Rev","Date","Description"], [
  ["01","March 2019","First issue. Brought the HSE, integrity and quality management systems under one framework based on IOGP 510."],
  ["02","June 2023","All ACE management systems moved inside OMS; one Risk Matrix and one document standard adopted."],
  ["03","November 2026","Renamed OMS — One Management System. Added Part D documentation standard, OMS tags and the OMS portal; aligned with ISO/DIS 29501; expanded measures and maturity assessment."]],
  [0.6,1.3,4.6], "plain")
heading(3, "Approval", "front_approval", "")
table(["Role","Name","Signature and date"], [["Author","Marissa Bobb, OMS Manager","Signed 14 Nov 2026"],["Reviewer","George Habib, VP HSE & Compliance","Signed 17 Nov 2026"],
  ["Approver","Satesh Sankar, Chief Executive Officer","Signed 21 Nov 2026"]], [1.3,3.0,2.2], "plain")

render(FOREWORD); render(GLANCE); render(HOWTO); render(PART_A); render(PART_B_INTRO)

# ---------------- elements ----------------
for el in ELEMENTS:
    n = el["n"]; c = ELC[n]
    heading(1, f"Element {n} — {el['title']}", f"el_{n}", "", color=c)
    para("OMS.ElementKicker", f"{GROUP[n]}  ·  Element owner: {el['owner']}")
    t = doc.add_table(rows=1, cols=2); t.autofit = False
    left, right = t.rows[0].cells
    left.width, right.width = Inches(1.5), Inches(5.0)
    left.paragraphs[0].add_run().add_picture(f"{IMG}/el{n}.png", width=Inches(1.35))
    rp = right.paragraphs[0]; add_runs(rp, el["purpose"]); rp.paragraph_format.space_after = Pt(4)
    np_ = right.add_paragraph(style="ODS.Note"); r = np_.add_run("What this means for you  "); r.bold = True; r.font.color.rgb = rgb(FLARE); add_runs(np_, el["you"])
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    for (num, title, intent, reqs, resp, docs, kpi, note, extra) in el["exps"]:
        tags = ", ".join([num] + extra)
        heading(2, f"{num}  {title}", "s" + num.replace(".", "_"), tags)
        para("Normal", intent)
        for rq in reqs: para("ODS.Requirement", rq)
        para("ODS.Responsibility", resp)
        for d in docs: para("ODS.DocumentReference", ref(d))
        para("ODS.PerformanceIndicator", kpi, "Measure", "3D5A80")
        if note: para("ODS.Note", note, "What this means for you", FLARE)

render(PART_C); render(PART_D); render(appendix_blocks(ELEMENTS))

# ---------------- header/footer ----------------
sec = doc.sections[0]; sec.different_first_page_header_footer = True
hp = sec.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
add_runs(hp, "OMS  ", 8, FLARE); hp.runs[-1].bold = True
add_runs(hp, "One Management System Manual  ·  ACE-OMS-MAN-001  ·  Rev 03", 8, MUTE)
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
add_runs(fp, "Acme Caribbean Energy Limited  ·  Uncontrolled when printed  ·  Page ", 8, MUTE); field(fp, "PAGE")
for r in fp.runs: r.font.size = Pt(8); r.font.color.rgb = rgb(MUTE)
# update fields (TOC) on open
settings = doc.settings.element; uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true")
insert_before(settings, uf, ["w:hdrShapeDefaults","w:footnotePr","w:endnotePr","w:compat","w:docVars","w:rsids"])
z = settings.find(qn("w:zoom"))
if z is not None and z.get(qn("w:percent")) is None: z.set(qn("w:percent"), "100")
cp = doc.core_properties; cp.title = META["ODS.Title"]; cp.author = META["ODS.Author"]; cp.subject = "ACE OMS"; cp.keywords = "OMS; IOGP 510; ODS"

tmp = f"{OUT}/_tmp.docx"; doc.save(tmp)

# ---------------- custom properties ----------------
def add_custom_props(src, dst, props):
    zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    items = "".join(f'<property fmtid="{{D5CDD505-2E9C-101B-9397-08002B2CF9AE}}" pid="{i+2}" name="{k}"><vt:lpwstr>{v.replace("&","&amp;")}</vt:lpwstr></property>' for i,(k,v) in enumerate(props.items()))
    custom = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
              'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">' + items + '</Properties>')
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == "[Content_Types].xml" and b"custom-properties" not in data:
            data = data.replace(b"</Types>", b'<Override PartName="/docProps/custom.xml" ContentType="application/vnd.openxmlformats-officedocument.custom-properties+xml"/></Types>')
        if it.filename == "_rels/.rels" and b"custom-properties" not in data:
            data = data.replace(b"</Relationships>", b'<Relationship Id="rIdCustom1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties" Target="docProps/custom.xml"/></Relationships>')
        if it.filename != "docProps/custom.xml": zout.writestr(it, data)
    zout.writestr("docProps/custom.xml", custom); zout.close(); zin.close()
final = f"{OUT}/ACE-OMS-MAN-001_OMS_Manual_Rev03.docx"
add_custom_props(tmp, final, META); os.remove(tmp)
print("saved", final)
