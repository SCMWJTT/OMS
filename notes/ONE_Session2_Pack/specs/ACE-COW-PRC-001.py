from specutil import *
exec(open("/home/claude/specs/x_ACE-COW-PRC-001.py").read())
body = list(BODY)
take_controls(body, "Controls established")
drop(body, "Processes and procedures implementing")
# repair the four corrupted tables (header split one letter per column)
heads = [["Work type", "Typical supplementary requirements"], ["Role", "Key duty / record"],
         ["Item", "Minimum confirmation"], ["Item", "Check"]]
k = 0
for i, b in enumerate(body):
    if b[0] == "t":
        body[i] = ("t", [heads[k]] + [r[:2] for r in b[1][1:]], [1, 3])
        k += 1
replace(body, "Permit type and supplemental certificates", "p",
        "Permit type and supplemental certificates are selected by hazard and task. Routine work may use a simplified authorization only where "
        "ACE-COW-STD-001 explicitly permits it and risk controls remain equivalent.")
add(body, "Purpose, scope", [
    ("p", "Parent: ACE-COW-STD-001 Control of Work Standard. Isolation is controlled by ACE-COW-PRC-002 Isolation and Reinstatement Procedure. "
          "The cross-functional flow is modelled in ACE-COW-PRS-001 Permit to Work Process (planned)."),
    ("warn", "Stop the job if the scope, the conditions or the work party change. Do not continue on the existing permit."),
])
add(body, "Permit applicability", [
    ("req", "Work shall not be subdivided or narrowly described to avoid the authorization level its hazards require."),
])
add(body, "Roles and authorization", [
    ("resp", "The Area Authority shall keep an overview of every active permit in the area and shall resolve conflicts before a permit is issued."),
    ("rc", "A permit shall only be issued by an authorized Permit Issuer and accepted by an authorized Performing Authority, and both names shall be recorded on the permit (C-COW-003)."),
])
add(body, "Request and work preparation", [
    ("rc", "The work scope and boundaries shall be specific to the equipment tag and confirmed against the current drawing and in the field before permit issue (C-COW-001)."),
    ("rc", "The hazards and controls in the risk assessment shall be reviewed with the work party in a recorded toolbox talk before work starts (C-COW-002)."),
])
add(body, "Field verification and issue", [
    ("rc", "The permit shall not be issued until the isolation certificate and any required gas test are valid and attached (C-COW-004)."),
])
add(body, "Execution and monitoring", [
    ("rc", "The Performing Authority shall monitor permit conditions at the frequency stated on the permit and stop work when any stop-work trigger occurs (C-COW-006)."),
])
add(body, "SIMOPS and coordination", [
    ("rc", "The Area Authority shall assess simultaneous operations before issuing a permit that shares a system, area or emergency route with other active work (C-COW-005)."),
])
add(body, "Suspension, shift handover", [
    ("rc", "Every permit suspension and shift handover shall be recorded and accepted by the incoming Performing Authority before work resumes (C-COW-007)."),
])
add(body, "Completion, hand-back", [
    ("rc", "A permit shall only be closed when the Permit Issuer and Area Authority have confirmed completion and hand-back, and equipment shall only return to service through ACE-COW-PRC-002 (C-COW-008)."),
])
add(body, "Records, assurance", [
    ("rec", "Permits, attachments, gas tests and hand-back records shall be retained for three years under ACE-DOC-STD-001."),
    ("rc", "The Permit to Work Coordinator shall sample at least ten closed permits per site each month for completeness and field compliance (C-COW-009)."),
    ("kpi", "Leading: permits passing field verification first time; monthly sample completed (target 100%). Lagging: permit non-conformances found in audit; incidents involving permitted work."),
])
add(body, "Records, assurance", [("h1", "Related processes and documents", "7.1, 7.4"),
    ("t", [["Number", "Title", "Status", "Relationship"],
           ["ACE-COW-STD-001", "Control of Work Standard", "Current", "Parent Standard"],
           ["ACE-COW-PRS-001", "Permit to Work Process", "Planned", "Cross-functional process model of this procedure"],
           ["ACE-COW-PRC-002", "Isolation and Reinstatement Procedure", "Current", "Isolation applied, verified and removed"],
           ["ACE-MNT-PRA-001", "Equipment Criticality and SCE Maintenance Practice", "Current", "SCE bypass and impairment authorization"]],
     [2, 3, 1.2, 3.4])])
controls = [
    ("C-COW-001", "Scope and boundaries are specific and field verified", "Wrong equipment or uncontrolled work", "4", "Permit verification", "Permit and field check"),
    ("C-COW-002", "Hazards and controls reviewed with the crew", "Uncontrolled task risk", "4", "Preparation / briefing", "Risk assessment and toolbox record"),
    ("C-COW-003", "Authorized roles issue and accept the permit", "Accountability gap", "3", "Issue authorization", "Permit record"),
    ("C-COW-004", "Isolation and atmosphere prerequisites valid", "Energy or atmosphere exposure", "5", "Issue gate", "Certificates and test record"),
    ("C-COW-005", "SIMOPS conflicts assessed", "Interaction or escalation hazards", "7", "Area coordination", "SIMOPS review"),
    ("C-COW-006", "Conditions monitored; work stops on change", "Conditions no longer safe", "6", "Field monitoring", "Field check and suspension record"),
    ("C-COW-007", "Handover and suspension explicit", "Unsafe shift transition", "8", "Handover", "Handover log"),
    ("C-COW-008", "Completion and hand-back confirmed", "Premature operation", "9", "Closeout", "Hand-back and release record"),
    ("C-COW-009", "Permit records sampled monthly", "Weak assurance evidence", "10", "Assurance", "Sample record and KPI"),
]
SPEC = dict(
    meta=dict(DocumentId="ACE-COW-PRC-001", Title="Permit to Work Procedure", DocumentType="Procedure",
              Level="4", Revision="01", Status="Approved", IssueDate="15 May 2026", EffectiveDate="1 June 2026",
              Author=who("Adrian Rodriguez"),
              Reviewer="; ".join(who(n) for n in ["Arjun Khan", "Arjun Gittens", "Rohan Ali", "Christina Bain"]),
              Endorser="Not required", Approver=who("Sophia Hosany"), DocumentOwner=who("Sophia Hosany"),
              ProcessOwner="Not applicable", Custodian=who("Adrian Rodriguez"), PrimaryFunction="Operations",
              TitleOMSTags="8.2, 8.1, 5.1", Classification="Internal", Applicability="PAP, CHB, SAP, CPF, LND, PLB",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Area Authority; Permit Issuer; Performing Authority; Isolating Authority; Gas Tester; HSE Adviser; Permit to Work Coordinator",
              Parent="ACE-COW-STD-001"),
    label="ACE  /  LEVEL 4 PROCEDURE  /  APPROVED CONTROLLED DOCUMENT",
    subtitle="Work authorization and coordination of hazardous activities at ACE facilities.",
    history=[("A", "—", "Draft for review."), ("01", "1 June 2026", "Initial approved issue. Repairs tables, assigns Control IDs C-COW-001 to C-COW-009 and names the owner and reviewers.")],
    processes=None, body=body, controls=controls)
