# ACE-DOC-POL-001 Document and Records Management Policy, draft of Rev 02 (Revision B): minor correction.
# Body is the issued Rev 01 body (Session 2 extraction, same transform as the Session 2 spec) with three additions only:
#   3.9 Periodic review (commitment that drives the document currency timeline)
#   7.1 Processes governed by this policy;  7.2 Standards and practices that implement this policy
import os
from specutil import add, who

HERE = os.path.dirname(os.path.abspath(__file__))
g = {}
exec(open(os.path.join(HERE, "..", "..", "ONE_Session2_Pack", "specs", "x_ACE-DOC-POL-001.py"), encoding="utf-8").read(), g)
body = [("note", b[1]) if b[0] == "rc" else b for b in g["BODY"]]

add(body, "Policy commitments", [
    ("h2", "Periodic review", "1.7, 7.4", "COM_PERIODIC_REVIEW"),
    ("p", "In line with our values Integrity in everything and One team, one way, every controlled document is reviewed on time so that "
          "people can trust that what they read is current. Policies, standards, practices, processes, procedures and plans are reviewed "
          "at least every three years, emergency plans every year, and work instructions, forms and registers at least every five years, "
          "and earlier after a relevant change or incident (ACE-DOC-STD-001 §7). The review dates drive the document currency timeline in ONE."),
])
add(body, "Implementation and supporting controlled documents", [
    ("h2", "Processes governed by this policy", "7.1, 1.7", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("ACE-DOC-PRS-001", "Controlled Document Publication Process", "11.3", "Planned"),
           ("—", "Periodic document review", "11.1", "Planned"),
           ("—", "Records retention and disposal", "11.1", "Planned")],
     [2.2, 4.6, 1, 1.2]),
    ("p", "Process owner of ACE-DOC-PRS-001: the Information Management Lead, as recorded in the Process Register (ACE-BPM-REG-001)."),
    ("h2", "Standards and practices that implement this policy", "7.1, 1.7", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-DOC-STD-001", "Document and Records Management Standard", "Current"),
           ("ACE-DOC-STD-002", "Operational Document Publishing Standard", "Current"),
           ("ACE-DOC-PRC-001", "Controlled Document and Records Lifecycle Procedure (under ACE-DOC-STD-001)", "Current"),
           ("ACE-DOC-STD-003", "Data Quality and Information Management Standard", "Planned")],
     [2.2, 6, 1.2]),
])

SPEC = dict(
    meta=dict(DocumentId="ACE-DOC-POL-001", Title="Document and Records Management Policy", DocumentType="Policy", Level="1",
              Revision="B", Status="In Review", IssueDate="", EffectiveDate="",
              Author=who("Marissa Bobb"),
              Reviewer="; ".join(who(n) for n in ["Marvin Williams", "Sharda Bissoon", "George Habib", "Sophia Hosany", "Dev Jaggernauth", "Nicole Lange"]),
              Endorser="Executive Leadership Team", Approver=who("Satesh Sankar"), DocumentOwner=who("Marvin Williams"),
              ProcessOwner="Not applicable", Custodian=who("Sanjay Jagessar"), PrimaryFunction="IT, Data & Knowledge",
              TitleOMSTags="1.7, 7.4, 9.5", Classification="Internal", Applicability="All ACE activities, sites, employees and contractors",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Chief Executive Officer; System owner; OMS Manager; Information Management Lead; Document Controller; Line manager; Technical Authority; Head of Internal Audit",
              Parent="ACE-LDR-POL-001"),
    label="ACE  /  LEVEL 1 POLICY  /  DRAFT FOR REVIEW",
    subtitle="The company commitment to one authoritative source, effective documents and trustworthy records.",
    cover_note="Proposed effective date 1 January 2027",
    history=[("A", "—", "Initial draft for review."),
             ("01", "1 April 2026", "Initial approved issue, released with ACE-OMS-MAN-001 Rev 04 and ACE-DOC-STD-002 Rev 02."),
             ("B", "", "Draft for Rev 02: adds the periodic review commitment (3.9) and the tables of governed processes and implementing "
                       "documents (7.1, 7.2). Proposed effective date 1 January 2027.")],
    file="ACE-DOC-POL-001_Document_and_Records_Management_Policy_RevB.docx",
    processes=None, body=body, controls=None)
