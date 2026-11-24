from specutil import *
exec(open("/home/claude/specs/x_ACE-MNT-PRA-001.py").read())
body = list(BODY)
controls = take_controls(body, "Controls established")
procs = take_controls(body, "Processes and procedures implementing")
rename(body, "Purpose and scope", "Purpose, scope and parent Standard")
rename(body, "Roles and authority", "Roles and technical authority")
rename(body, "Performance, verification", "Performance and verification", "9.5, 6.4, 10.4")
add(body, "Implementing processes", [("t", [["Number", "Title", "Status", "Steps relied on"]] + [list(p) for p in procs], [2, 3, 1.4, 3.4])])

add(body, "Purpose, scope", [
    ("p", "Parent Standard: ACE-MNT-STD-001 Maintenance Management Standard. This Practice turns its requirements into the method ACE uses to rank "
          "equipment, select strategies and assure Safety-Critical Elements. It applies at PAP, CHB, SAP, CPF, LND and PLB."),
    ("ext", "Recognised practice applied: ISO 14224 Collection and exchange of reliability and maintenance data for equipment; IEC 60300-3-11 "
            "Reliability centred maintenance; ISO 55001 Asset management systems; Energy Institute guidance on the management of SCEs."),
])
add(body, "Roles and technical authority", [
    ("t", [["Role", "Named person", "Accountability in this Practice"],
           ["Practice owner and approver", who("Sophia Hosany"), "Approves the method; accountable for SCE maintenance performance across operated sites."],
           ["Practice custodian", who("Nadira Ramsaran"), "Owns the criticality method, strategy library and reliability reviews."],
           ["Maintenance & integrity assurance", who("Marc Gomes"), "Assures alignment between maintenance, inspection and SCE performance standards."],
           ["Execution and backlog", who("Sunita Seepersad"), "Plans and schedules work; manages backlog and overdue SCE reporting."],
           ["TA — rotating equipment", who("Sharon Alexander"), "Failure modes and strategies for pumps, compressors and turbines."],
           ["TA — safety systems", who("Akilah Noel"), "Performance standards and test methods for fire and gas, ESD and SIS elements."]],
     [2, 3, 4]),
    ("resp", "The Reliability & Maintenance Lead shall maintain the criticality method and the strategy library, and shall present the criticality coverage report to the Technical Leadership Council every six months."),
    ("resp", "The Maintenance Superintendent shall report overdue SCE work to the Area Authority and the Maintenance & Integrity Manager every week."),
])
add(body, "Equipment hierarchy", [
    ("rc", "Every maintainable item shall have a unique equipment ID in the ISO 14224-aligned hierarchy, and the same ID shall be used in the CMMS, the SCE register and ONE (C-MNT-001)."),
])
add(body, "Criticality method", [
    ("rc", "Every equipment item shall carry an A, B or C criticality ranking assessed against the ACE Risk Matrix, with the rationale recorded and reviewed after each trigger listed above (C-MNT-002)."),
])
add(body, "Safety-Critical Elements", [
    ("rc", "Every SCE shall be listed in the SCE register (ACE-AIM-REG-001) with a current performance standard that defines its function, required performance and verification test (C-MNT-003)."),
])
add(body, "Maintenance strategy", [
    ("rc", "The maintenance strategy for each A and B item shall be selected from its credible failure modes and recorded, and a run-to-failure strategy shall only be applied to C items with documented justification (C-MNT-004)."),
])
add(body, "Work order priority", [
    ("rc", "Preventive and test work on A-critical equipment shall be scheduled in the CMMS with a planned date, and completion against plan shall be monitored every month (C-MNT-005)."),
    ("rc", "The Maintenance Superintendent shall review the risk-weighted backlog every week and escalate any A-critical or SCE item older than its backlog limit (C-MNT-006)."),
    ("t", [["Priority", "Typical condition", "Start within", "Backlog limit"],
           ["P1 Emergency", "SCE failed or loss of containment", "Immediately", "Not applicable"],
           ["P2 Urgent", "A-critical degraded or SCE impaired", "24 hours", "7 days"],
           ["P3 Planned high", "B-critical defect; preventive work on A items", "7 days", "30 days"],
           ["P4 Planned", "Routine preventive and C-critical work", "30 days", "90 days"]], [2, 3, 1.5, 1.5]),
])
add(body, "SCE overdue", [
    ("rc", "An overdue SCE maintenance or test task shall be raised as a deviation under ACE-OMS-STD-002 before its due date passes, with interim measures and an expiry date (C-MNT-007)."),
    ("rc", "Any defeat, bypass or inhibit of an SCE shall be authorised under ACE-COW-STD-001 and entered in the override log with its duration and compensating measures (C-MNT-008)."),
    ("rc", "SCE work orders shall only be closed when the function test result and the restoration to service are recorded against the performance standard (C-MNT-009)."),
])
add(body, "Failure data", [
    ("rc", "The Reliability & Maintenance Lead shall review failure data every quarter and update the criticality ranking or strategy where repeat failures show the current task is not effective (C-MNT-010)."),
    ("rec", "Failure records shall capture the ISO 14224 failure mode, cause and downtime against the equipment ID in the CMMS."),
])
add(body, "Performance and verification", [
    ("kpi", "Leading: SCE preventive and test work completed on time (target ≥ 98%); A-critical backlog older than limit (target 0); open SCE deviations past expiry (target 0). Lagging: SCE test failures on demand; repeat failures on bad-actor equipment."),
])
SPEC = dict(
    meta=dict(DocumentId="ACE-MNT-PRA-001", Title="Equipment Criticality and SCE Maintenance Practice", DocumentType="Practice",
              Level="2", Revision="01", Status="Approved", IssueDate="15 May 2026", EffectiveDate="1 June 2026",
              Author=who("Nadira Ramsaran"),
              Reviewer="; ".join(who(n) for n in ["Marc Gomes", "Sunita Seepersad", "Sharon Alexander", "Akilah Noel"]),
              Endorser="Technical Leadership Council", Approver=who("Sophia Hosany"), DocumentOwner=who("Sophia Hosany"),
              ProcessOwner="Not applicable", Custodian=who("Nadira Ramsaran"), PrimaryFunction="Operations",
              TitleOMSTags="6.4, 6.5, 8.2", Classification="Internal", Applicability="PAP, CHB, SAP, CPF, LND, PLB",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Practice owner; Technical Authority; Reliability & Maintenance Lead; Maintenance Superintendent; Area Authority; Planner",
              Parent="ACE-MNT-STD-001"),
    label="ACE  /  LEVEL 2 PRACTICE  /  APPROVED CONTROLLED DOCUMENT",
    subtitle="Ranking equipment by risk, selecting maintenance strategies and assuring Safety-Critical Elements.",
    history=[("A", "—", "Draft for review."), ("01", "1 June 2026", "Initial approved issue. Adds named roles, priority table, binding statements and Control IDs C-MNT-001 to C-MNT-010.")],
    processes=None, body=body, controls=controls)
