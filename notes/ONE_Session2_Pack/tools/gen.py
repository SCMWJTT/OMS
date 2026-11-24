"""ONE house-format document builder.
build(spec, out_path) writes a STRICT ONE Word document from a spec dict,
using shell.docx (a gateway-passed Rev 01 final) for styles, cover graphics,
header/footer and page setup. Body, control table, properties are regenerated."""
import zipfile, re, os, sys
from xml.sax.saxutils import escape

SHELL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shell.docx")
FRAMEWORK = "IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 04"
TOTAL_W = 9532
CID_RE = re.compile(r"(?<![A-Za-z0-9-])C-[A-Z]{3}-\d{3}")
STY = {"p": None, "req": "ODS.Requirement", "resp": "ODS.Responsibility", "appr": "ODS.ApprovalRequirement",
       "rec": "ODS.RecordRequirement", "rc": "ODS.RiskControl", "warn": "ODS.Warning", "kpi": "ODS.PerformanceIndicator",
       "note": "ODS.Note", "ref": "ODS.DocumentReference", "ext": "ODS.ExternalStandard", "step": "ODS.ProcedureStep",
       "def": "ODS.Definition", "bul": "ListBullet"}
BINDING = {"req", "resp", "appr", "rec", "rc"}
PROP_ORDER = ["DocumentId", "Title", "DocumentType", "Level", "Revision", "Status", "IssueDate", "EffectiveDate", "Author",
              "Reviewer", "Endorser", "Approver", "DocumentOwner", "ProcessOwner", "Custodian", "PrimaryFunction", "Framework",
              "TitleOMSTags", "Classification", "Applicability", "ReviewInterval", "RoleRegister", "Parent"]


class B:
    def __init__(self, docid):
        self.sid = 3000
        self.bid = 100
        self.hn = 0
        self.bmprefix = docid.replace("-", "_")
        self.out = []

    def nid(self):
        self.sid += 1
        return self.sid


def t(s):
    return f'<w:t xml:space="preserve">{escape(s)}</w:t>'


def run(s, rpr=""):
    return f"<w:r>{('<w:rPr>' + rpr + '</w:rPr>') if rpr else ''}{t(s)}</w:r>"


def sdt(b, tag, alias, value, rpr=""):
    return (f'<w:sdt><w:sdtPr><w:alias w:val="{escape(alias)}"/><w:tag w:val="{escape(tag)}"/><w:id w:val="{b.nid()}"/>'
            f'<w:text/></w:sdtPr><w:sdtContent>{run(value, rpr)}</w:sdtContent></w:sdt>')


def para(inner, style=None, extra_ppr="", bm=None, b=None):
    ppr = ""
    if style or extra_ppr:
        ppr = "<w:pPr>" + (f'<w:pStyle w:val="{style}"/>' if style else "") + extra_ppr + "</w:pPr>"
    if bm:
        b.bid += 1
        inner = f'<w:bookmarkStart w:id="{b.bid}" w:name="{bm}"/>{inner}<w:bookmarkEnd w:id="{b.bid}"/>'
    return f"<w:p>{ppr}{inner}</w:p>"


def text_with_cids(b, s, wrap):
    """Plain runs; Control IDs wrapped in Control ID content controls when wrap=True."""
    if not wrap:
        return run(s)
    out, pos = [], 0
    for m in CID_RE.finditer(s):
        if m.start() > pos:
            out.append(run(s[pos:m.start()]))
        out.append(sdt(b, f"ODS.Control@{m.group(0)}", "Control ID", m.group(0), '<w:b/>'))
        pos = m.end()
    if pos < len(s):
        out.append(run(s[pos:]))
    return "".join(out)


def tagline(b, bm, tags):
    return para(run("OMS  ") + sdt(b, f"ODS.OMSTags@{bm}", "OMS Tags", tags), "ODSTagLine", "<w:keepNext/>")


def heading(b, level, txt, tags, bm=None):
    if bm is None:
        b.hn += 1
        bm = f"{b.bmprefix}_H{b.hn:03d}"
    return para(run(txt), f"Heading{level}", "<w:keepNext/>", bm, b) + tagline(b, bm, tags)


def cell(txt, w, fill=None, hdr=False, bold=False):
    rpr = ("<w:b/>" if (hdr or bold) else '<w:b w:val="0"/>') + f'<w:color w:val="{"FFFFFF" if hdr else "122A36"}"/><w:sz w:val="16"/>'
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ""
    paras = "".join(f'<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>{run(line, rpr)}</w:p>'
                    for line in (str(txt).split("\n") if str(txt) else [""]))
    return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}<w:vAlign w:val="center"/></w:tcPr>{paras}</w:tc>'


def table(rows, widths=None, label_col=False, header=True):
    n = len(rows[0])
    if widths is None:
        widths = [1] * n
    tot = sum(widths)
    ws = [int(TOTAL_W * w / tot) for w in widths]
    x = ('<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'
         '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
         '</w:tblPr><w:tblGrid>' + "".join(f'<w:gridCol w:w="{w}"/>' for w in ws) + "</w:tblGrid>")
    for i, r in enumerate(rows):
        hdr = header and i == 0
        fill = "102630" if hdr else ("F1F5F6" if i % 2 == 0 else None)
        x += ("<w:tr><w:trPr><w:tblHeader/></w:trPr>" if hdr else "<w:tr>")
        x += "".join(cell(c, ws[j], fill, hdr, label_col and j == 0) for j, c in enumerate(r)) + "</w:tr>"
    return x + "</w:tbl>" + para("", extra_ppr='<w:spacing w:before="0" w:after="60"/>')


def check_shall(kind, txt, where):
    if kind not in BINDING and re.search(r"\bshall\b", txt, re.I):
        raise ValueError(f"'shall' in non-binding {kind}: {where}: {txt[:80]}")


def build(spec, out_path):
    m = dict(spec["meta"])
    m.setdefault("Framework", FRAMEWORK)
    missing = [k for k in PROP_ORDER if not m.get(k)]
    if missing:
        raise ValueError(f"{m.get('DocumentId')}: missing meta {missing}")
    b = B(m["DocumentId"])
    rev, status, eff, issue = m["Revision"], m["Status"], m["EffectiveDate"], m["IssueDate"]
    typelvl = f'{m["DocumentType"]} (Level {m["Level"]})'

    z = zipfile.ZipFile(SHELL)
    doc = z.read("word/document.xml").decode()
    head, body = doc.split("<w:body>")
    sect = body[body.rindex("<w:sectPr"):].replace("</w:body></w:document>", "")
    # cover top block (logo table + caption + rule) copied from shell up to section label
    cover_top = body[:body.index('<w:p><w:pPr><w:pStyle w:val="ONESectionLabel"/>')]
    o = [cover_top]
    o.append(para(run(spec["label"]), "ONESectionLabel", '<w:spacing w:after="200"/>'))
    b.bid += 1
    o.append(f'<w:p><w:pPr><w:pStyle w:val="Title"/><w:spacing w:after="80"/></w:pPr><w:bookmarkStart w:id="{b.bid}" w:name="doc_title"/>'
             f'{sdt(b, "ODS.Meta.Title", "Document title", m["Title"])}<w:bookmarkEnd w:id="{b.bid}"/></w:p>')
    o.append(para(run("OMS  ") + sdt(b, "ODS.OMSTags@doc_title", "OMS Tags", m["TitleOMSTags"]), "ODSTagLine",
                  '<w:keepNext/><w:spacing w:after="140"/>'))
    o.append(para(run(spec["subtitle"]), "DocumentSubTitle", '<w:spacing w:after="280"/>'))
    # cover box
    def box(lbl, tag, val):
        return (f'<w:tc><w:tcPr><w:tcW w:w="4766" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EAF2F3"/></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>{run(lbl, "<w:b/><w:color w:val=\"0E5A6B\"/><w:sz w:val=\"16\"/>")}</w:p>'
                f'<w:p><w:pPr><w:spacing w:after="60"/></w:pPr>{sdt(b, tag, lbl, val, "<w:b/><w:sz w:val=\"24\"/>")}</w:p></w:tc>')
    o.append('<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'
             '<w:tblLook w:val="04A0" w:firstRow="0" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
             '<w:tblGrid><w:gridCol w:w="4766"/><w:gridCol w:w="4766"/></w:tblGrid>'
             f'<w:tr>{box("DOCUMENT NUMBER", "ODS.Meta.DocumentID", m["DocumentId"])}{box("REVISION", "ODS.Meta.CoverRevision", f"{rev} — {status}")}</w:tr>'
             f'<w:tr>{box("DOCUMENT STATUS", "ODS.Meta.CoverStatus", status)}{box("EFFECTIVE DATE", "ODS.Meta.CoverEffectiveDate", eff)}</w:tr></w:tbl>')
    o.append(para(run("The current approved revision is held in the controlled ONE repository. Printed copies are uncontrolled."),
                  extra_ppr='<w:spacing w:before="440"/>'))
    o.append(para(run(f"APPROVED ISSUE {rev}   •   EFFECTIVE {eff.upper()}"), extra_ppr='<w:spacing w:before="160"/>'))
    o.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # ---- document control (all values are ODS.Meta content controls)
    o.append(heading(b, 1, "Document control", "1.7", "front_document_control"))
    rows = [("Document number", "DocumentID", m["DocumentId"]), ("Title", "ControlTitle", m["Title"]),
            ("Document type", "DocumentType", m["DocumentType"]), ("Level", "Level", m["Level"]),
            ("Revision", "Revision", rev), ("Status", "Status", status), ("Issue date", "IssueDate", issue),
            ("Effective date", "EffectiveDate", eff), ("Parent document", "Parent", m["Parent"]),
            ("Document owner", "DocumentOwner", m["DocumentOwner"]), ("Process owner", "ProcessOwner", m["ProcessOwner"]),
            ("Custodian", "Custodian", m["Custodian"]), ("Author", "Author", m["Author"]), ("Reviewers", "Reviewer", m["Reviewer"]),
            ("Endorser", "Endorser", m["Endorser"]), ("Approver", "Approver", m["Approver"]),
            ("Primary function", "PrimaryFunction", m["PrimaryFunction"]), ("Framework", "Framework", m["Framework"]),
            ("Title OMS tags", "TitleOMSTags", m["TitleOMSTags"]), ("Classification", "Classification", m["Classification"]),
            ("Applies to", "Applicability", m["Applicability"]), ("Review interval", "ReviewInterval", m["ReviewInterval"]),
            ("Role register", "RoleRegister", m["RoleRegister"])]
    x = ('<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'
         '<w:tblLook w:val="04A0" w:firstRow="0" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
         '<w:tblGrid><w:gridCol w:w="2700"/><w:gridCol w:w="6832"/></w:tblGrid>')
    for i, (lbl, tag, val) in enumerate(rows):
        fill = '<w:shd w:val="clear" w:color="auto" w:fill="F1F5F6"/>' if i % 2 == 0 else ""
        x += (f'<w:tr><w:tc><w:tcPr><w:tcW w:w="2700" w:type="dxa"/>{fill}</w:tcPr><w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>'
              f'{run(lbl, "<w:b/><w:color w:val=\"122A36\"/><w:sz w:val=\"16\"/>")}</w:p></w:tc>'
              f'<w:tc><w:tcPr><w:tcW w:w="6832" w:type="dxa"/>{fill}</w:tcPr><w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>'
              f'{sdt(b, "ODS.Meta." + tag, lbl, val, "<w:color w:val=\"122A36\"/><w:sz w:val=\"16\"/>")}</w:p></w:tc></w:tr>')
    o.append(x + "</w:tbl>" + para(""))

    o.append(heading(b, 2, "Revision history", "1.7", "front_revision_history"))
    o.append(table([("Revision", "Date", "Description")] + [tuple(h) for h in spec["history"]], [1, 1.6, 6]))
    o.append(heading(b, 2, "Approval and issue", "2.2, 1.7", "front_approval"))
    endorse = m["Endorser"]
    appr_rows = [("Role", "Person", "Recorded decision"), ("Author", m["Author"], f"Prepared — {issue}"),
                 ("Reviewers", m["Reviewer"], f"Reviewed — {issue}")]
    if endorse != "Not required":
        appr_rows.append(("Technical endorsement", endorse, f"Endorsed — {issue}"))
    appr_rows.append(("Approver", m["Approver"], f"Approved — {issue}"))
    o.append(table(appr_rows, [1.4, 4.6, 2]))
    o.append(para(run("This approved issue is governed by the ACE controlled register. The signed or electronic approval record is "
                      "retained by Document Control with the release package."), "ODS.Note"))

    # ---- document map + implementing processes
    o.append(heading(b, 1, "Document map", "7.1", "front_document_map"))
    o.append(para(run("The numbered sections below contain the binding statements and supporting guidance. Appendices are part of this document.")))
    blocks = spec["body"]
    num, app = 0, 0
    mrows = [("Section", "Subject")]
    for blk in blocks:
        if blk[0] == "h1":
            num += 1
            mrows.append((str(num), blk[1]))
        elif blk[0] == "app":
            app += 1
            mrows.append((chr(64 + app), blk[1]))
    if spec.get("controls"):
        mrows.append((chr(64 + app + 1), "Controls established by this document"))
    o.append(table(mrows, [1, 7]))
    if spec.get("processes"):
        o.append(para(run("Processes and procedures that implement this document"), "Heading3", "<w:keepNext/>"))
        o.append(table([("Number", "Title", "Status", "Steps relied on")] + [tuple(p) for p in spec["processes"]], [2, 3, 1.2, 3.4]))

    # ---- body
    num, app, sub = 0, 0, 0
    for i, blk in enumerate(blocks):
        k = blk[0]
        if k == "h1":
            num += 1; sub = 0
            o.append(heading(b, 1, f"{num} {blk[1]}", blk[2]))
        elif k == "app":
            app += 1; sub = 0
            o.append(heading(b, 1, f"Appendix {chr(64 + app)} — {blk[1]}", blk[2]))
        elif k == "h2":
            sub += 1
            lbl = f"{num}.{sub}" if app == 0 else f"{chr(64 + app)}.{sub}"
            o.append(heading(b, 2, f"{lbl} {blk[1]}", blk[2]))
        elif k == "t":
            o.append(table(blk[1], blk[2] if len(blk) > 2 else None))
        elif k in STY:
            check_shall(k, blk[1], m["DocumentId"])
            if k == "rc" and not CID_RE.search(blk[1]):
                raise ValueError(f"RiskControl without Control ID: {blk[1][:60]}")
            o.append(para(text_with_cids(b, blk[1], k == "rc"), STY[k]))
        else:
            raise ValueError(f"unknown block {k}")
    if spec.get("controls"):
        app += 1
        o.append(heading(b, 1, f"Appendix {chr(64 + app)} — Controls established by this document", "5.1, 7.1"))
        o.append(para(run("Each control below is written as an ODS.RiskControl statement in the section shown and is held in the "
                          "Controls Register (ACE-RSK-REG-002) under the same Control ID.")))
        o.append(table([("Control ID", "Control statement", "Risk / threat addressed", "Section", "Process step", "Evidence / record")]
                       + [tuple(c) for c in spec["controls"]], [1.3, 3, 2.2, 0.9, 1.8, 1.8]))
        # consistency: every control listed is in a RiskControl paragraph and vice versa
        body_ids = set()
        for blk in blocks:
            if blk[0] == "rc":
                body_ids |= set(CID_RE.findall(blk[1]))
        tab_ids = {c[0] for c in spec["controls"]}
        if body_ids != tab_ids:
            raise ValueError(f"{m['DocumentId']}: control mismatch body-only {sorted(body_ids - tab_ids)} table-only {sorted(tab_ids - body_ids)}")

    newdoc = head + "<w:body>" + "".join(o) + sect + "</w:body></w:document>"

    # ---- package
    zout = zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED)
    drop = {"word/media/image1.png", "word/media/image2.png", "docProps/thumbnail.jpeg"}
    for it in z.infolist():
        n = it.filename
        if n in drop:
            continue
        data = z.read(n)
        if n == "word/document.xml":
            data = newdoc.encode()
        elif n == "word/_rels/document.xml.rels":
            s = data.decode()
            s = re.sub(r'<Relationship Id="rId(9|10)"[^>]*/>', "", s)
            data = s.encode()
        elif n == "_rels/.rels":
            data = re.sub(r'<Relationship Id="rId2"[^>]*thumbnail[^>]*/>', "", data.decode()).encode()
        elif n.startswith("word/header") or n.startswith("word/footer"):
            s = data.decode().replace("ACE-OPS-STD-001", m["DocumentId"]).replace("Rev 01", f"Rev {rev}").replace("REV 01", f"REV {rev}")
            s = s.replace("APPROVED   •   1 January 2026", f"{status.upper()}   •   {eff}")
            data = s.encode()
        elif n == "docProps/custom.xml":
            data = custom_xml(m).encode()
        elif n == "docProps/core.xml":
            data = core_xml(m, typelvl).encode()
        elif n == "docProps/app.xml":
            data = app_xml(m).encode()
        zout.writestr(it, data)
    zout.close()
    return out_path


def iso(d):
    import datetime
    return datetime.datetime.strptime(d, "%d %B %Y").strftime("%Y-%m-%dT09:00:00Z")


def custom_xml(m):
    x = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
         'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">')
    for i, k in enumerate(PROP_ORDER):
        x += (f'<property fmtid="{{D5CDD505-2E9C-101B-9397-08002B2CF9AE}}" pid="{i + 2}" name="ODS.{k}"><vt:lpwstr>{escape(m[k])}</vt:lpwstr></property>')
    return x + "</Properties>"


def name_only(p):
    return p.split(" — ")[0]


def core_xml(m, typelvl):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{escape(m["Title"])}</dc:title><dc:subject>{m["DocumentId"]}</dc:subject>'
            f'<dc:creator>{escape(name_only(m["Author"]))}</dc:creator><cp:keywords>{m["TitleOMSTags"]}</cp:keywords>'
            f'<dc:description>{escape("Rev " + m["Revision"] + " · Effective " + m["EffectiveDate"] + " · Owner: " + name_only(m["DocumentOwner"]))}</dc:description>'
            f'<cp:lastModifiedBy>{escape(name_only(m["Author"]))}</cp:lastModifiedBy><cp:revision>1</cp:revision>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{iso(m["IssueDate"])}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{iso(m["IssueDate"])}</dcterms:modified>'
            f'<cp:category>{escape(typelvl)}</cp:category><cp:contentStatus>{m["Status"]}</cp:contentStatus>'
            '</cp:coreProperties>')


def app_xml(m):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>ONE_ACE_Master_Template_v4.dotx</Template>'
            '<TotalTime>0</TotalTime><Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
            f'<Manager>{escape(name_only(m["DocumentOwner"]))}</Manager><Company>Acme Caribbean Energy Limited</Company>'
            '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinkBase>https://oms.cynmark.app/</HyperlinkBase>'
            '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')
