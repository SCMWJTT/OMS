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

