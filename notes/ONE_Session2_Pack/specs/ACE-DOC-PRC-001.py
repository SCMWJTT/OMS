from specutil import *
exec(open("/home/claude/specs/x_ACE-DOC-PRC-001.py").read())
body = [("note", b[1]) if b[0] == "rc" else b for b in BODY]
for i, b in enumerate(body):
    if b[0] == "t" and b[1][0] == ["Document class", "Who approves", "Technical endorsement"]:
        body[i] = ("t", [["Document class", "Who approves", "Technical endorsement"],
                         ["Manual or policy (Level 1)", "Chief Executive Officer", "Executive Leadership Team; Legal and element owners review."],
                         ["Standard or specification (Level 2)", "System owner (function VP)", "Technical Authority where technical."],
                         ["Practice (Level 2)", "Function VP", "Technical Authority review; Technical Leadership Council endorsement for technical Practices."],
                         ["Process (Level 3)", "VP of the process owner’s function", "Affected functions review; BPM system owner endorses cross-functional processes."],
                         ["Procedure, plan or guideline (Level 4)", "Function manager", "Technical Authority where technical."],
                         ["Work instruction, form or register (Level 5)", "Responsible supervisor or manager", "As required by governing technical content."]])
replace(body, "ACE-OMS-MAN-001, Rev 03", "ref", "ACE-OMS-MAN-001, Rev 04 — One Management System Manual, especially sections A.4, A.6, D.1–D.9 and Appendix 3.")
replace(body, "ACE-DOC-POL-001 — Document and Records", "ref", "ACE-DOC-POL-001 — Document and Records Management Policy.")
for k in ["ACE-DOC-STD-001 —", "ACE-DOC-STD-002 —", "ACE-MOC-PRC-001 —", "ACE-OMS-STD-002 —"]:
    for i, b in enumerate(body):
        if b[0] == "ref" and b[1].startswith(k):
            body[i] = ("ref", b[1].replace(" (programme priority; verify approved revision before operational use)", ""))
replace(body, "If a referenced supporting document has not yet", "p",
        "Where a referenced document is revised, the current approved revision in ONE applies. This Procedure is subject to the OMS Manual.")
SPEC = dict(
    meta=dict(DocumentId="ACE-DOC-PRC-001", Title="Controlled Document and Records Lifecycle Procedure", DocumentType="Procedure", Level="4",
              Revision="01", Status="Approved", IssueDate="16 March 2026", EffectiveDate="1 April 2026",
              Author=who("Sanjay Jagessar"),
              Reviewer="; ".join(who(n) for n in ["Ryan Ramsaran", "Allison St. Hill", "Paul Gomes", "Marissa Bobb", "Sharda Bissoon", "Sophia Hosany"]),
              Endorser="Not required", Approver=who("Shalini Mungal"), DocumentOwner=who("Marvin Williams"),
              ProcessOwner="Not applicable", Custodian=who("Sanjay Jagessar"), PrimaryFunction="IT, Data & Knowledge",
              TitleOMSTags="1.7, 7.2, 7.4", Classification="Internal", Applicability="All ACE activities, sites, employees and contractors",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Document owner; Author; Reviewer; Technical Authority; Approver; Document Controller; Information Management Lead; Custodian; Line manager",
              Parent="ACE-DOC-STD-001"),
    label="ACE  /  LEVEL 4 PROCEDURE  /  APPROVED CONTROLLED DOCUMENT",
    subtitle="Operating instructions for registration, authoring, verification, approval, publication, review, retention and withdrawal.",
    history=[("A", "—", "Initial draft for review."), ("01", "1 April 2026", "Initial approved issue under ACE-OMS-MAN-001 Rev 04. Approval matrix updated to the five-level hierarchy (adds Practice and Process).")],
    processes=None, body=body, controls=None)
