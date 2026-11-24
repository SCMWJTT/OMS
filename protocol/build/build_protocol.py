"""Builds protocol/one-protocol.json from canonical sources in the repository.
Run from the repo root:  python3 protocol/build/build_protocol.py"""
import json, csv, sys, os, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "notes/ONE_Session1_Pack/oms/src4"))
import elements, register  # noqa: E402

people = list(csv.DictReader(open(os.path.join(ROOT, "company/ACE_People.csv"), encoding="utf-8-sig")))
functions = sorted({p["Function"] for p in people})

EL = [dict(id=e["n"], title=e["title"], owner=e["owner"]) for e in elements.ELEMENTS]
EXP = [dict(id=x[0], element=e["n"], title=x[1]) for e in elements.ELEMENTS for x in e["exps"]]
assert len(EXP) == 54

SYS = {c: dict(name=n, owner=o, elements=[int(x) for x in el.split(", ")]) for c, n, o, el in register.SYSTEMS}
assert len(SYS) == 26

TYPES = {
    "MAN": dict(name="Manual", level=1, layer="Policy"),
    "POL": dict(name="Policy", level=1, layer="Policy"),
    "STD": dict(name="Standard", level=2, layer="Standard and Practice", implementing_table=True),
    "PRA": dict(name="Practice", level=2, layer="Standard and Practice", implementing_table=True),
    "SPC": dict(name="Specification", level=2, layer="Standard and Practice"),
    "PRS": dict(name="Process", level=3, layer="Process", paired_file=True),
    "PRC": dict(name="Procedure", level=4, layer="Procedure and Plan", legacy_level=3),
    "PLN": dict(name="Plan", level=4, layer="Procedure and Plan", legacy_level=3),
    "WIN": dict(name="Work Instruction", level=5, layer="Task and record", legacy_level=4),
    "FRM": dict(name="Form", level=5, layer="Task and record", legacy_level=4),
    "REG": dict(name="Register", level=5, layer="Task and record", legacy_level=4),
    "GDL": dict(name="Guideline", level=None, layer="Supporting", binding_allowed=False),
}
SITES = {"PAP": "Pommerac A", "CHB": "Chenet B", "SAP": "Sapodilla C", "CPF": "Central Processing Facility",
         "LND": "Land leases (Tamarind, Pawpaw, Soursop)", "PLB": "Point Lisas shore base", "HOF": "Head Office"}

# ---- styles: what ONE does with each paragraph style
def sty(id_, name, binding, meaning, aliases=None, kind="paragraph"):
    a = aliases if aliases is not None else ([id_.replace(".", "")] if "." in id_ else [])
    return dict(id=id_, name=name, aliases=a, binding=binding, one=meaning, kind=kind)
STYLES = [
    sty("Title", "Title", False, "document title (carries doc_title bookmark)"),
    sty("Heading1", "Heading 1", False, "section; must have bookmark + tag line"),
    sty("Heading2", "Heading 2", False, "sub-section; must have bookmark + tag line"),
    sty("Heading3", "Heading 3", False, "minor heading; tag line optional"),
    sty("ODSTagLine", "ODS Tag Line", False, "holds the OMS Tags content control for the heading above"),
    sty("DocumentSubTitle", "Document Sub Title", False, "cover subtitle; shown as summary"),
    sty("DocumentKicker", "Document Kicker", False, "cover label"),
    sty("ODS.Requirement", "ODS Requirement", True, "requirement"),
    sty("ODS.Responsibility", "ODS Responsibility", True, "responsibility (role register)"),
    sty("ODS.ApprovalRequirement", "ODS Approval Requirement", True, "approval requirement"),
    sty("ODS.RecordRequirement", "ODS Record Requirement", True, "record requirement (records view)"),
    sty("ODS.RiskControl", "ODS Risk Control", True, "control; must carry Control ID content control(s)"),
    sty("ODS.Warning", "ODS Warning", False, "warning"),
    sty("ODS.Note", "ODS Note", False, "note"),
    sty("ODS.PerformanceIndicator", "ODS Performance Indicator", False, "KPI"),
    sty("ODS.DocumentReference", "ODS Document Reference", False, "reference to an ACE document"),
    sty("ODS.ExternalStandard", "ODS External Standard", False, "reference to an external standard"),
    sty("ODS.ProcedureStep", "ODS Procedure Step", False, "procedure step"),
    sty("ODS.Definition", "ODS Definition", False, "glossary term"),
    sty("ODS.Example", "ODS Example", False, "example", aliases=["ODSExample"]),
    sty("OMS.ElementKicker", "OMS Element Kicker", False, "Manual element label"),
    sty("ListBullet", "List Bullet", False, "list item"),
    sty("ONEBrand", "ONE Brand", False, "cover branding (ignored)"),
    sty("ONESectionLabel", "ONE Section Label", False, "cover label (ignored)"),
    sty("ONECoverCaption", "ONE Cover Caption", False, "cover caption (ignored)"),
    sty("ONEMetadata", "ONE Metadata", False, "cover metadata (ignored)"),
    sty("ONEPullQuote", "ONE Pull Quote", False, "Manual quote (ignored)"),
    sty("ONEQuoteBy", "ONE Quote By", False, "Manual quote author (ignored)"),
    sty("Caption", "Caption", False, "figure or table caption"),
]

# ---- 23 custom properties: name, Meta tags that hold the same value, format
P = lambda name, meta, fmt, req="approved", since="1.0", note="": dict(name=name, meta=meta, format=fmt, required=req, since=since, note=note)
PROPS = [
    P("ODS.DocumentId", ["DocumentID"], "docid", "always"),
    P("ODS.Title", ["Title", "ControlTitle"], "text", "always"),
    P("ODS.DocumentType", ["DocumentType"], "type_name", "always", note="Meta.DocumentType may read 'Standard (Level 2)' in legacy documents"),
    P("ODS.Level", ["Level"], "level", "always", note="digit only; 'Level 3' accepted and normalised by Fix"),
    P("ODS.Revision", ["Revision", "CoverRevision"], "revision", "always", note="Meta.CoverRevision reads '01 — Approved'; legacy Meta.Revision may read '01 (approved issue)'"),
    P("ODS.Status", ["Status", "CoverStatus"], "status", "always"),
    P("ODS.IssueDate", ["IssueDate"], "date", "approved"),
    P("ODS.EffectiveDate", ["EffectiveDate", "CoverEffectiveDate"], "date", "approved"),
    P("ODS.Author", ["Author"], "people", "always"),
    P("ODS.Reviewer", ["Reviewer"], "people", "approved"),
    P("ODS.Endorser", ["Endorser"], "people_or_body", "approved"),
    P("ODS.Approver", ["Approver"], "people", "approved"),
    P("ODS.DocumentOwner", ["DocumentOwner"], "people", "always"),
    P("ODS.ProcessOwner", ["ProcessOwner"], "people_or_na", "approved", since="2.0", note="required person for PRS; otherwise 'Not applicable' preferred"),
    P("ODS.Custodian", ["Custodian"], "people", "approved"),
    P("ODS.PrimaryFunction", ["PrimaryFunction"], "function", "always"),
    P("ODS.Framework", ["Framework"], "framework", "always"),
    P("ODS.TitleOMSTags", ["TitleOMSTags"], "tags", "always"),
    P("ODS.Classification", ["Classification"], "classification", "always"),
    P("ODS.Applicability", ["Applicability"], "text", "always"),
    P("ODS.ReviewInterval", ["ReviewInterval"], "text", "approved"),
    P("ODS.RoleRegister", ["RoleRegister"], "text", "approved", since="2.0"),
    P("ODS.Parent", ["Parent"], "parent", "approved", since="2.0", note="parent document number; Level 1 may use 'Not applicable'"),
]

BUILTIN = {
    "core": {"dc:title": "{Title}", "dc:subject": "{DocumentId}", "cp:keywords": "{TitleOMSTags}",
             "cp:category": "{DocumentType} (Level {Level})", "cp:contentStatus": "{Status}",
             "dc:description": "Rev {Revision} · Effective {EffectiveDate} · Owner: {DocumentOwner.name}",
             "dc:creator": "{Author.name}"},
    "app": {"Manager": "{DocumentOwner.name}", "Company": "Acme Caribbean Energy Limited", "HyperlinkBase": "https://oms.cynmark.app/"},
    "checked_as_error": ["dc:title", "dc:subject", "cp:keywords"],
}

RULES = [
    dict(id="G1", title="Document number, codes and file name", severity="error", fix="manual",
         checks=["DocumentId matches the number pattern", "system, type and site codes are valid", "file name starts with the number (auto-fix: rename)"]),
    dict(id="G2", title="Revision and status agree", severity="error", fix="manual",
         checks=["letters ↔ Draft/In Review; digits ↔ Approved/Superseded/Withdrawn", "approved issues have issue and effective dates", "finals/ holds Approved only (warning)"]),
    dict(id="G3", title="Custom properties", severity="error", fix="auto",
         checks=["all 23 present with standard names (ODS.Parent missing → warning for legacy)", "required values filled", "values in valid format", "no unknown ODS.* properties (warning)"]),
    dict(id="G4", title="Metadata agrees in the five places", severity="error", fix="auto",
         checks=["control table (ODS.Meta.*) = custom properties (control table is master)", "built-in Title/Subject/Tags (warning for legacy)", "header/footer shows number and revision (warning)"]),
    dict(id="G5", title="Title bookmark and title tags", severity="error", fix="auto",
         checks=["doc_title bookmark on the Title paragraph", "title tag control ODS.OMSTags@doc_title = ODS.TitleOMSTags"]),
    dict(id="G6", title="Headings, bookmarks and OMS tags", severity="error", fix="auto",
         checks=["every Heading 1/2 has a bookmark and is followed by a tag line", "tag line holds ODS.OMSTags@<that bookmark> (plain-text tag line = LITE, auto-fix)", "every tag is one of the 54 expectations", "no orphan or duplicate tag controls", "1 to 3 tags per section (warning)"]),
    dict(id="G7", title="'Shall' only in binding styles", severity="error", fix="manual",
         checks=["no 'shall' in non-binding paragraphs or table cells", "Guidelines contain no binding styles"]),
    dict(id="G8", title="People match the organisation register", severity="error", fix="auto",
         checks=["each person is 'Name — Job title' exactly as in ACE_People.csv", "known name with wrong title → auto-fix", "unknown name → manual"]),
    dict(id="G9", title="Control IDs", severity="error", fix="auto",
         checks=["C-SSS-NNN with a valid system code", "unique across the repository", "every ODS.RiskControl paragraph carries a Control ID content control (legacy → warning)", "plain-text IDs in RiskControl paragraphs → auto-fix", "controls appendix matches body (warning)"]),
    dict(id="G10", title="Parent document", severity="error", fix="manual",
         checks=["ODS.Parent set below Level 1 (legacy → warning)", "parent exists in the document register"]),
    dict(id="G11", title="References to ACE documents", severity="warning", fix="manual",
         checks=["referenced numbers exist (issued or planned)", "unknown number → warning"]),
    dict(id="G12", title="Process (PRS) pair", severity="error", fix="manual",
         checks=["JSON file present with same number and revision", "validates against ONE-PRS/1", "every step has a bookmarked narrative heading", "doc_refs and controls resolve"]),
    dict(id="G13", title="Implementing processes table (STD, PRA)", severity="warning", fix="manual",
         checks=["table listing implementing processes and procedures present"]),
    dict(id="G14", title="Media and size", severity="warning", fix="auto",
         checks=["no linked (external) images", "no unused media", "file under 2 MB"]),
    dict(id="G15", title="Valid Word XML", severity="error", fix="manual",
         checks=["all parts well-formed", "bookmarkStart not before pPr (warning, auto-fix)"]),
    dict(id="G16", title="No lock or temporary files", severity="error", fix="auto",
         checks=["no ~$ or .tmp files in the submission"]),
]


C = lambda name, rule, link=None: dict(name=name, rule=rule, **({"link": link} if link else {}))
REGISTERS = {
 "BPM-REG-001": dict(title="Process Register", file="registers/BPM-REG-001.csv", key="process_id", owner="Manager, Strategy & Planning", defined_in="ACE-BPM-PRA-001", columns=[
   C("process_id", "PRS number, unique"), C("title", "process title"), C("l1", "L1 code"), C("l2", "L2 code"),
   C("owner", "Name — Job title", "people"), C("function", "one of the 13 functions"), C("policy", "Policy number", "document"),
   C("parent", "parent Standard/Practice/Procedure", "document"), C("status", "Planned / Draft / Current / Retired"),
   C("revision", "current PRS revision"), C("oms_tags", "expectations, primary first"), C("last_review", "date"),
   C("maturity", "1 to 5"), C("requirements", "doc#bookmark list carried out (; separated)")]),
 "RSK-REG-001": dict(title="Risk Register", file="registers/RSK-REG-001.csv", key="risk_id", owner="Head of Internal Audit & Risk Assurance", defined_in="ACE-RSK-STD-001", columns=[
   C("risk_id", "R-<SITE>-nn"), C("title", "short risk title"), C("site", "site code"), C("hazard", "hazard"), C("top_event", "top event"),
   C("threats", "; separated"), C("consequences", "; separated"), C("owner", "Name — Job title", "people"), C("asset_id", "A-SITE-nnn", "asset"),
   C("inherent_l", "likelihood 1-5"), C("inherent_c", "consequence 1-5"), C("residual_l", "1-5"), C("residual_c", "1-5"),
   C("appetite", "within / outside"), C("objective_id", "OBJ-nn it threatens", "objective"), C("controls", "C-IDs (; separated)", "control"), C("review_date", "date")]),
 "RSK-REG-002": dict(title="Controls Register", file="registers/RSK-REG-002.csv", key="control_id", owner="Process Safety Lead", defined_in="ACE-RSK-PRA-001", columns=[
   C("control_id", "C-SSS-NNN"), C("statement", "short statement"), C("position", "Preventive / Mitigating"), C("nature", "Hard / Soft / People"),
   C("critical", "Yes / No"), C("risk_id", "R-SITE-nn", "risk"), C("threat", "threat addressed"), C("barrier", "bow-tie barrier name"),
   C("doc_ref", "document#bookmark", "document"), C("process_step", "PRS#Snn", "process"), C("owner", "Name — Job title", "people"),
   C("asset_id", "A-SITE-nnn", "asset"), C("sce_id", "SCE id", "sce"), C("evidence", "record type and system"), C("test_interval", "e.g. 6 months"),
   C("health", "Effective / Degraded / Failed / Not tested"), C("health_date", "date"), C("status", "Active / Planned / Retired")]),
 "AIM-REG-001": dict(title="SCE Register", file="registers/AIM-REG-001.csv", key="sce_id", owner="Manager, Technical Excellence", defined_in="ACE-MNT-PRA-001", columns=[
   C("sce_id", "SCE-<SITE>-nnn"), C("title", "element"), C("group", "SCE group, e.g. ESD, F&G, PSV"), C("site", "site code"),
   C("asset_ids", "A-SITE-nnn (; separated)", "asset"), C("performance_standard", "PS reference"), C("test_interval", "interval"),
   C("last_test", "date"), C("next_due", "date"), C("status", "Available / Impaired / Deviation"), C("controls", "C-IDs", "control")]),
 "AIM-REG-002": dict(title="Asset Register", file="registers/AIM-REG-002.csv", key="asset_id", owner="Maintenance & Integrity Manager", defined_in="ACE-MNT-PRA-001", columns=[
   C("asset_id", "A-<SITE>-nnn"), C("tag", "equipment tag"), C("title", "description"), C("site", "site code"), C("parent_id", "hierarchy parent", "asset"),
   C("iso14224_class", "equipment class"), C("criticality", "A / B / C"), C("sce", "Yes / No"), C("in_service", "date")]),
 "INC-REG-001-EV": dict(title="Events and Actions — events", file="registers/INC-REG-001_events.csv", key="event_id", owner="HSE Manager", defined_in="ACE-INC-STD-001", columns=[
   C("event_id", "EV-yyyy-nnn"), C("date", "date"), C("site", "site code"), C("type", "Incident / Near miss / Audit finding / Test failure / IOW excursion / Deviation"),
   C("title", "short description"), C("risk_ids", "R-IDs", "risk"), C("controls_tested", "C-IDs that worked", "control"),
   C("controls_failed", "C-IDs that failed", "control"), C("processes", "PRS numbers", "process"), C("severity", "ACE matrix 1-5")]),
 "INC-REG-001-ACT": dict(title="Events and Actions — actions", file="registers/INC-REG-001_actions.csv", key="action_id", owner="HSE Manager", defined_in="ACE-INC-STD-001", columns=[
   C("action_id", "ACT-yyyy-nnn"), C("event_id", "EV id", "event"), C("title", "action"), C("owner", "Name — Job title", "people"),
   C("due", "date"), C("closed", "date or blank"), C("result", "document revision or MOC raised", "document")]),
 "OMS-REG-001-OBJ": dict(title="Objectives and Opportunities — objectives", file="registers/OMS-REG-001_objectives.csv", key="objective_id", owner="Manager, Strategy & Planning", defined_in="ACE-BPM-PRA-001", columns=[
   C("objective_id", "OBJ-nn"), C("title", "objective"), C("owner", "Name — Job title", "people"), C("kpi", "measure"), C("target", "target"),
   C("year", "yyyy"), C("processes", "PRS numbers supporting it", "process"), C("risks", "R-IDs threatening it", "risk")]),
 "OMS-REG-001-OPP": dict(title="Objectives and Opportunities — opportunities", file="registers/OMS-REG-001_opportunities.csv", key="opportunity_id", owner="Manager, Strategy & Planning", defined_in="ACE-RSK-PRA-001", columns=[
   C("opportunity_id", "OPP-nn"), C("title", "opportunity"), C("objective_id", "OBJ-nn", "objective"), C("owner", "Name — Job title", "people"),
   C("value", "expected value"), C("likelihood", "1-5"), C("benefit", "1-5"), C("status", "Open / Pursued / Realised / Dropped")]),
}

# ---- align register definitions with the generated register files (registers/*.csv headers are authoritative for column order)
RULES_EXTRA = {
 "level": "Enterprise / Asset / Site", "system": "system code", "process": "PRS number", "escalation_vp": "Name — Job title", "c_people": "1-5",
 "c_environment": "1-5", "c_reputation": "1-5", "current_c": "headline = most severe domain", "current_l": "A-E", "current_rating": "from ACE matrix",
 "legacy_control_docs": "document addressing the risk without Control IDs", "alarp_status": "ALARP demonstrated / in progress", "residual_rating": "from ACE matrix",
 "acceptance_authority": "per RSK-STD-001 §5.1", "accepted_date": "date", "expiry": "date (High risks)", "restrictions": "operating conditions",
 "review_frequency": "per RSK-STD-001 §8.2", "last_review": "date", "version": "integer", "change_reason": "text", "process_planned": "PRS expected to perform it",
 "effective": "date the establishing document took effect", "pse_tier": "1, 2, 3 or blank", "spill_bbl": "barrels", "notes": "text", "controls": "C-IDs",
}
REGISTERS["RSK-REG-001-HIST"] = dict(title="Risk Register — rating history", file="registers/RSK-REG-001_history.csv", key="risk_id+date", owner="Head of Internal Audit & Risk Assurance", defined_in="ACE-RSK-STD-001", columns=[])
REGISTERS["RSK-REG-002-HEALTH"] = dict(title="Controls Register — health history", file="registers/RSK-REG-002_health.csv", key="control_id+date", owner="Process Safety Lead", defined_in="ACE-RSK-PRA-001", columns=[])
REGISTERS["PRF-REG-001-KPI"] = dict(title="Performance data — KPI catalogue", file="registers/PRF-REG-001_kpis.csv", key="kpi_id", owner="Compliance & Assurance Manager", defined_in="ACE-PRF-STD-001 (planned)", columns=[])
REGISTERS["PRF-REG-001-M"] = dict(title="Performance data — monthly values", file="registers/PRF-REG-001_monthly.csv", key="month+site+kpi_id", owner="Compliance & Assurance Manager", defined_in="ACE-PRF-STD-001 (planned)", columns=[])
for k, r in REGISTERS.items():
    f = os.path.join(ROOT, r["file"])
    if os.path.exists(f):
        have = {c["name"]: c for c in r["columns"]}
        head = next(csv.reader(open(f, encoding="utf-8")))
        r["columns"] = [have.get(h, dict(name=h, rule=RULES_EXTRA.get(h, ""))) for h in head]

proto = {
    "protocol": "ONE-PROTOCOL", "version": "1.0.0", "issued": "2026-11-24",
    "governed_by": "ACE-DOC-STD-002 Rev 02",
    "company": {"name": "Acme Caribbean Energy Limited", "short": "ACE", "site_url": "https://oms.cynmark.app/"},
    "framework": {"current": "IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 04",
                  "legacy": ["IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 03"],
                  "legacy_rule": "A document whose Framework names Rev 03 is LEGACY: rules introduced in protocol 2.0 give warnings, not errors, until its next revision."},
    "numbering": {"docid": r"^ACE-([A-Z]{3})-([A-Z]{3})-(\d{3})(?:-([A-Z]{3}))?$",
                  "file": r"^(ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?)_[A-Za-z0-9_\-]+_Rev([A-Z]|\d{2})\.docx$",
                  "reference": r"(?<![A-Za-z0-9-])ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?(?:\s*§\s*[0-9A-Z][0-9A-Z.]*)?",
                  "eng_blocks": "ENG uses discipline blocks 100 to 900; 901 is the framework standard"},
    "revision": {"draft": "^[A-Z]$", "approved": r"^\d{2}$", "draft_status": ["Draft", "In Review"],
                 "approved_status": ["Approved", "Superseded", "Withdrawn"]},
    "statuses": ["Draft", "In Review", "Approved", "Superseded", "Withdrawn"],
    "classifications": ["Public", "Internal", "Confidential"],
    "types": TYPES, "systems": SYS, "sites": SITES, "functions": functions,
    "elements": EL, "expectations": EXP,
    "people": {"source": "company/ACE_People.csv", "name_column": "Full Name", "title_column": "Job Title",
               "format": "Name — Job title", "separator": "; ",
               "allowed_values": ["Technical Leadership Council", "Executive Leadership Team", "Not required", "Not applicable",
                                  "Board of Directors"],
               "fields": ["ODS.Author", "ODS.Reviewer", "ODS.Endorser", "ODS.Approver", "ODS.DocumentOwner", "ODS.ProcessOwner", "ODS.Custodian"]},
    "styles": STYLES,
    "content_controls": [
        {"tag": "ODS.Meta.<Field>", "alias": "free text (label)", "kind": "plain text", "use": "control table and cover values; Field from properties[].meta"},
        {"tag": "ODS.OMSTags@<bookmark>", "alias": "OMS Tags (variants accepted)", "kind": "plain text", "use": "OMS expectation tags for the heading carrying <bookmark>; doc_title for the Title"},
        {"tag": "ODS.Control@<ControlID>", "alias": "Control ID", "kind": "plain text", "use": "inside ODS.RiskControl paragraphs", "since": "2.0"},
    ],
    "properties": PROPS, "builtin_properties": BUILTIN,
    "bookmarks": {"title": "doc_title",
                  "recommended_heading": "<DOCID with _>_H<nnn>  e.g. ACE_RSK_STD_001_H004",
                  "accepted_heading_patterns": [r"^ACE_[A-Z]{3}_[A-Z]{3}_\d{3}(_[A-Z]{3})?_H\d{3}$", r"^front_[a-z_]+$", r"^sec_[a-z0-9_]+$",
                                                r"^s\d+_\d+$", r"^(el|d|a|w|c|app)_\d+(_\d+)?$", r"^_S\d{2}$"],
                  "rule": "Any valid bookmark is accepted; the tag control must name the bookmark of its own heading. Fix adds <DOCID>_Hnnn where missing."},
    "tags": {"min_per_section": 1, "max_per_section": 3, "scope": "heading down to next heading of same or higher level; not inherited",
             "tag_line_prefix": "OMS", "headings_requiring_tags": ["Heading1", "Heading2"]},
    "control_id": {"pattern": r"(?<![A-Za-z0-9-])C-([A-Z]{3})-(\d{3})", "content_control": "ODS.Control@{id}",
                   "unique": "repository", "allocation_register": "ACE-RSK-REG-002"},
    "formats": {
        "STRICT": "Values in ODS.Meta content controls; tags in ODS.OMSTags@bookmark controls; heading bookmarks; 23 properties filled; Control ID controls. ONE publishes STRICT only.",
        "LITE": "What writers and AI tools produce: Title and headings in template styles; tags typed as plain text in ODS Tag Line paragraphs ('OMS 6.5, 6.4'); control table as plain text; Control IDs as plain text; properties may be empty. Fix converts LITE to STRICT without changing the text."},
    "outcomes": {"PASS": "no errors", "PASS_AFTER_FIX": "all errors can be fixed automatically by ONE Fix", "FAIL": "at least one error needs a person"},
    "document_register": {"planned": {f"ACE-{k}": dict(title=v[0], owner_role=v[1], level=v[2]) for k, v in register.DOCS.items()}},
    "rules": RULES,
    "registers": REGISTERS,
    "process_schema": "protocol/schemas/one-prs-1.schema.json",
    "limits": {"max_file_mb": 2},
    "front_sections": {"Document control": "1.7", "Revision history": "1.7", "Approval and issue": "2.2, 1.7", "Document map": "7.1"},
    "defaults": {"ODS.Classification": "Internal", "ODS.ReviewInterval": "Three years; earlier if triggered", "ODS.ProcessOwner": "Not applicable"},
}
out = os.path.join(ROOT, "protocol", "one-protocol.json")
json.dump(proto, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import csv as _csv
rdir = os.path.join(ROOT, "protocol", "registers"); os.makedirs(rdir, exist_ok=True)
for k, r in REGISTERS.items():
    with open(os.path.join(rdir, os.path.basename(r["file"])), "w", newline="", encoding="utf-8") as fh:
        _csv.writer(fh).writerow([c["name"] for c in r["columns"]])
print("wrote", out, os.path.getsize(out), "bytes;", len(EXP), "expectations;", len(SYS), "systems;", len(functions), "functions")
