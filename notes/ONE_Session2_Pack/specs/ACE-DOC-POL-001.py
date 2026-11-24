from specutil import *
exec(open("/home/claude/specs/x_ACE-DOC-POL-001.py").read())
body = [("note", b[1]) if b[0] == "rc" else b for b in BODY]
SPEC = dict(
    meta=dict(DocumentId="ACE-DOC-POL-001", Title="Document and Records Management Policy", DocumentType="Policy", Level="1",
              Revision="01", Status="Approved", IssueDate="16 March 2026", EffectiveDate="1 April 2026",
              Author=who("Marissa Bobb"),
              Reviewer="; ".join(who(n) for n in ["Marvin Williams", "Sharda Bissoon", "George Habib", "Sophia Hosany", "Dev Jaggernauth", "Nicole Lange"]),
              Endorser="Executive Leadership Team", Approver=who("Satesh Sankar"), DocumentOwner=who("Marvin Williams"),
              ProcessOwner="Not applicable", Custodian=who("Sanjay Jagessar"), PrimaryFunction="IT, Data & Knowledge",
              TitleOMSTags="1.7, 7.4, 9.5", Classification="Internal", Applicability="All ACE activities, sites, employees and contractors",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Chief Executive Officer; System owner; OMS Manager; Information Management Lead; Document Controller; Line manager; Technical Authority; Head of Internal Audit",
              Parent="ACE-LDR-POL-001"),
    label="ACE  /  LEVEL 1 POLICY  /  APPROVED CONTROLLED DOCUMENT",
    subtitle="The company commitment to one authoritative source, effective documents and trustworthy records.",
    history=[("A", "—", "Initial draft for review."), ("01", "1 April 2026", "Initial approved issue, released with ACE-OMS-MAN-001 Rev 04 and ACE-DOC-STD-002 Rev 02.")],
    processes=None, body=body, controls=None)
