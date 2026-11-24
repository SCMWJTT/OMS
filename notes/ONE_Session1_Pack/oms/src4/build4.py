import re, copy, zipfile, shutil, os, datetime as dt
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from parts4 import WELCOME, GLANCE, WHY, HOWTO, PART_A, WORK, PART_B_INTRO, PART_C, PART_D, appendix_blocks
from elements import ELEMENTS
from register import ref, DOCS

IMG = "/home/claude/oms/img"; OUT = "/home/claude/oms/out"; os.makedirs(OUT, exist_ok=True)
INK, TEAL, FLARE, SAND, SKY, MUTE = "12232E", "0E5A6B", "F26B21", "F6F1E8", "A7D8E3", "5B6B73"
ELC = {1:"0B4F5E",2:"0F6B7A",3:"1E8796",4:"3AA3AE",5:"D9480F",6:"F26B21",7:"F5923E",8:"F8B26A",9:"3D5A80",10:"5C7BA6"}
GROUP = {1:"LEAD",2:"LEAD",3:"LEAD",4:"LEAD",5:"CONTROL",6:"CONTROL",7:"CONTROL",8:"CONTROL",9:"LEARN",10:"LEARN"}
HFONT, BFONT = "Segoe UI Semibold", "Calibri"
META = {
 "ODS.DocumentId": "ACE-OMS-MAN-001", "ODS.Title": "One Management System (OMS) Manual", "ODS.DocumentType": "Manual", "ODS.Level": "1",
 "ODS.Revision": "04", "ODS.Status": "Approved", "ODS.IssueDate": "16 March 2026", "ODS.EffectiveDate": "1 April 2026",
 "ODS.Author": "Marissa Bobb — OMS Manager",
 "ODS.Reviewer": "George Habib — VP HSE & Compliance; Gary Ho Sing — Manager, Strategy & Planning; Sanjay Jagessar — Information Management Lead",
 "ODS.Endorser": "Executive Leadership Team", "ODS.Approver": "Satesh Sankar — Chief Executive Officer",
 "ODS.DocumentOwner": "Satesh Sankar — Chief Executive Officer", "ODS.ProcessOwner": "Not applicable",
 "ODS.Custodian": "Marissa Bobb — OMS Manager", "ODS.PrimaryFunction": "HSE & Compliance",
 "ODS.Framework": "IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 04", "ODS.TitleOMSTags": "1.1, 2.1, 7.1", "ODS.Classification": "Internal",
 "ODS.Applicability": "All ACE activities, sites, staff and contractors", "ODS.ReviewInterval": "Three years; earlier if triggered",
 "ODS.RoleRegister": "Chief Executive Officer; Element owner; System owner; Document owner; Process owner; OMS Manager; Area Authority; Technical Authority; Technical Leadership Council; Information Management Lead; Line manager; Supervisor; Contractor",
 "ODS.Parent": "Not applicable (top-level document)",
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


# ================= Rev 04 additions =================
from docx.shared import Twips
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH
pstyle("ONEPullQuote", 15, TEAL, italic=True, before=10, after=4, left=0.3, font="Segoe UI")
st["ONEPullQuote"].name = "ONE Pull Quote"
pstyle("ONEQuoteBy", 9.5, FLARE, bold=True, before=0, after=12, left=0.3, font="Segoe UI Semibold")
st["ONEQuoteBy"].name = "ONE Quote By"
pstyle("ONECoverCaption", 11, MUTE, italic=True, before=2, after=8, font="Segoe UI")
st["ONECoverCaption"].name = "ONE Cover Caption"
# quote style: left flare bar
qp = st["ONE Pull Quote"].element.get_or_add_pPr()
bdr = OxmlElement("w:pBdr"); l = OxmlElement("w:left")
for k, v in (("w:val", "single"), ("w:sz", "36"), ("w:space", "12"), ("w:color", FLARE)): l.set(qn(k), v)
bdr.append(l); insert_before(qp, bdr, ["w:shd", "w:tabs", "w:suppressAutoHyphens", "w:spacing", "w:ind", "w:jc", "w:outlineLvl", "w:rPr"])

def no_borders(t):
    tblPr = t._tbl.tblPr; b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "nil"); b.append(e)
    insert_before(tblPr, b, ["w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook", "w:tblCaption", "w:tblDescription"])

def cell_pad(t, top=120, side=200):
    tblPr = t._tbl.tblPr; m = OxmlElement("w:tblCellMar")
    for s, v in (("top", top), ("left", side), ("bottom", top), ("right", side)):
        e = OxmlElement(f"w:{s}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); m.append(e)
    insert_before(tblPr, m, ["w:tblLook", "w:tblCaption", "w:tblDescription"])

def tight(p, after=0, before=0):
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before); p.paragraph_format.line_spacing = 1.05

def band(kicker, text, fill):
    t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    no_borders(t); cell_pad(t, 200, 260)
    c = t.rows[0].cells[0]; c.width = Inches(6.5); cell_fill(c, fill)
    p = c.paragraphs[0]; r = p.add_run(kicker); r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = rgb("FFD3B8" if fill != FLARE else "FFFFFF")
    r.font.name = "Segoe UI Semibold"; tight(p, 3)
    p2 = c.add_paragraph(); r = p2.add_run(text); r.font.size = Pt(16); r.font.color.rgb = rgb("FFFFFF"); r.font.name = "Segoe UI Semibold"; tight(p2)
    sp = doc.add_paragraph(); tight(sp, 4)

def tiles(items):
    t = doc.add_table(rows=1, cols=len(items)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    no_borders(t); cell_pad(t, 140, 120)
    w = 6.5 / len(items)
    for i, (big, label, fill) in enumerate(items):
        c = t.rows[0].cells[i]; c.width = Inches(w); cell_fill(c, fill)
        tcPr = c._tc.get_or_add_tcPr(); b = OxmlElement("w:tcBorders")
        for side in ("left", "right"):
            e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "24"); e.set(qn("w:color"), "FFFFFF"); b.append(e)
        insert_before(tcPr, b, ["w:shd", "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark"])
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p.add_run(big); r.font.size = Pt(30); r.font.name = "Segoe UI Semibold"
        r.font.color.rgb = rgb("FFFFFF"); tight(p)
        p2 = c.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p2.add_run(label.upper()); r.font.size = Pt(8); r.bold = True
        r.font.color.rgb = rgb("FFFFFF"); tight(p2)
    sp = doc.add_paragraph(); tight(sp, 6)

PLACEHOLDERS = []
def placeholder(iid, brief, h):
    PLACEHOLDERS.append((iid, brief))
    t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    tblPr = t._tbl.tblPr; b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "dashed"); e.set(qn("w:sz"), "8"); e.set(qn("w:color"), "A7B8BF"); b.append(e)
    insert_before(tblPr, b, ["w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook", "w:tblCaption", "w:tblDescription"])
    row = t.rows[0]; row.height = Inches(h); row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    c = row.cells[0]; c.width = Inches(6.5); cell_fill(c, "EEF3F4")
    tcPr = c._tc.get_or_add_tcPr(); va = OxmlElement("w:vAlign"); va.set(qn("w:val"), "center"); tcPr.append(va)
    p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p.add_run(f"IMAGE {iid}"); r.bold = True; r.font.size = Pt(10)
    r.font.color.rgb = rgb(TEAL); tight(p, 3)
    p2 = c.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p2.add_run(brief); r.italic = True; r.font.size = Pt(8.5)
    r.font.color.rgb = rgb(MUTE); tight(p2)
    sp = doc.add_paragraph(); tight(sp, 4)

def quote(text, who):
    p = doc.add_paragraph(style="ONE Pull Quote"); p.add_run("“" + text + "”")
    doc.add_paragraph(who, style="ONE Quote By")

def cards(items, fill):
    rows = (len(items) + 1) // 2
    t = doc.add_table(rows=rows, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    tblPr = t._tbl.tblPr; b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "18"); e.set(qn("w:color"), "FFFFFF"); b.append(e)
    insert_before(tblPr, b, ["w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook", "w:tblCaption", "w:tblDescription"])
    cell_pad(t, 120, 160)
    for i, (title, text) in enumerate(items):
        c = t.rows[i // 2].cells[i % 2]; c.width = Inches(3.25); cell_fill(c, fill)
        p = c.paragraphs[0]; r = p.add_run(title); r.bold = True; r.font.size = Pt(10.5); r.font.color.rgb = rgb(TEAL); r.font.name = "Segoe UI Semibold"; tight(p, 3)
        p2 = c.add_paragraph(); add_runs(p2, text, size=9.5); tight(p2)
    sp = doc.add_paragraph(); tight(sp, 6)

def sdt_value(par, tag, alias, value, size=None, color=None, bold=False):
    sdt = OxmlElement("w:sdt"); pr = OxmlElement("w:sdtPr")
    for tn, val in (("w:alias", alias), ("w:tag", tag)):
        x = OxmlElement(tn); x.set(qn("w:val"), val); pr.append(x)
    x = OxmlElement("w:id"); x.set(qn("w:val"), str(abs(hash(tag)) % 2000000000)); pr.append(x)
    pr.append(OxmlElement("w:text")); sdt.append(pr)
    cont = OxmlElement("w:sdtContent"); rr = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    if bold: rpr.append(OxmlElement("w:b"))
    if color: col = OxmlElement("w:color"); col.set(qn("w:val"), color); rpr.append(col)
    if size: sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size * 2))); rpr.append(sz)
    rr.append(rpr); t = OxmlElement("w:t"); t.text = value; t.set(qn("xml:space"), "preserve"); rr.append(t)
    cont.append(rr); sdt.append(cont); par._p.append(sdt)

def meta_table(rows, widths=(2.0, 4.5)):
    t = doc.add_table(rows=0, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    borders(t, "CED8DC"); cell_margins(t)
    for label, tag, value in rows:
        cells = t.add_row().cells
        cells[0].text = ""; p = cells[0].paragraphs[0]; r = p.add_run(label); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = rgb(TEAL); tight(p)
        cell_fill(cells[0], "EAF2F3")
        cells[1].text = ""; p = cells[1].paragraphs[0]; tight(p)
        sdt_value(p, f"ODS.Meta.{tag}", label, value, size=9.5, color=INK)
    for row in t.rows:
        for i, w in enumerate(widths): row.cells[i].width = Inches(w)
    sp = doc.add_paragraph(); tight(sp, 4)

_render_old = render
def render(blocks):
    for b in blocks:
        k = b[0]
        if k == "band": band(b[1], b[2], b[3])
        elif k == "tiles": tiles(b[1])
        elif k == "ph": placeholder(b[1], b[2], b[3])
        elif k == "quote": quote(b[1], b[2])
        elif k == "cards": cards(b[1], b[2])
        elif k == "h2pb":
            hp_ = heading(2, b[1], b[2], b[3]); hp_.paragraph_format.page_break_before = True
        else: _render_old([b])
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
final = f"{OUT}/ACE-OMS-MAN-001_OMS_Manual_Rev04.docx"
add_custom_props(tmp, final + ".tmp", META); os.remove(tmp)
zin = zipfile.ZipFile(final + ".tmp"); zout = zipfile.ZipFile(final, "w", zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    data = zin.read(it.filename)
    if it.filename == "docProps/app.xml":
        s = data.decode()
        s = s.replace("<Manager/>", "<Manager>Satesh Sankar — Chief Executive Officer</Manager>").replace("<Company/>", "<Company>Acme Caribbean Energy Limited</Company>")
        s = s.replace("<HyperlinkBase/>", "<HyperlinkBase>https://oms.cynmark.app/</HyperlinkBase>")
        data = s.encode()
    zout.writestr(it, data)
zout.close(); zin.close(); os.remove(final + ".tmp")
open("/home/claude/oms/out/image_placeholders.txt", "w").write("\n".join(f"{i}\t{b}" for i, b in PLACEHOLDERS))
print("saved", final, len(PLACEHOLDERS), "image placeholders")
