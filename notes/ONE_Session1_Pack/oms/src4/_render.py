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

