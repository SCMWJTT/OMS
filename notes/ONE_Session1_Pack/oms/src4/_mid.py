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

