
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
