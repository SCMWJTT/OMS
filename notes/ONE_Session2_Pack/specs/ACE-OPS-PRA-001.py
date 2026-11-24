from specutil import *
exec(open("/home/claude/specs/x_ACE-OPS-PRA-001.py").read())
body = [b for b in BODY if not (b[0] == "rc" and b[1].startswith("Operating limits are technically based"))]
rename(body, "Roles and technical authority", "Roles and technical authority", kind="h1")
replace(body, "This Practice establishes the engineering", "p",
        "This Practice establishes the engineering and operating method used to define, classify, document, monitor and respond to operating limits and "
        "Integrity Operating Windows (IOWs). It provides the technical bridge between design intent, process safety analysis, materials and corrosion "
        "knowledge, operating discipline and integrity management. It applies to the Central Processing Facility (CPF), Pommerac A (PAP), land leases "
        "(LND), and interfaces with offshore unmanned facilities and supporting logistics. The Practice serves ACE-OPS-STD-001 Operating Envelopes and "
        "Operating Limits Standard and does not replace Control of Work, Risk Management, Management of Change or Asset Integrity requirements.")
add(body, "Purpose, scope", [
    ("ext", "Recognised practice applied: API RP 584 Integrity Operating Windows; IEC 62682 Management of alarm systems for the process industries; "
            "IEC 61511 Functional safety — safety instrumented systems for the process industry sector."),
])
# roles table: replace unnamed last row
for i, b in enumerate(body):
    if b[0] == "t" and b[1][0][0] == "Role":
        rows = [r for r in b[1] if not r[0].startswith("Area Authority")]
        rows.append([who("Roger Ramkissoon"), "Area Authority for Pommerac A: communicates active limits, checks response, escalates excursions and records actions."])
        body[i] = ("t", rows)
add(body, "Roles and technical authority", [
    ("resp", "The Process Engineering Lead shall maintain the Operating Limits Register and the technical basis dossier for every limit in it."),
    ("resp", "The Production Chemistry Lead shall set and review the chemistry IOWs, including corrosion inhibitor injection rates, with the Materials & Corrosion Lead."),
])
replace(body, "Limits are nested", "p",
        "Limits are nested; lower-level targets never override an upper-level safety or integrity boundary.")
add(body, "Limit hierarchy", [
    ("rc", "Every IOW shall be classified as critical, standard or informational using the hierarchy above, and the class shall be shown in the register and on the control room display (C-OPS-001)."),
])
add(body, "Establishing and validating", [
    ("rc", "Each limit shall have a technical basis dossier that records the evidence in the table above and is approved by the relevant Technical Authority before the limit is published (C-OPS-002)."),
    ("rc", "Where two constraints conflict, the more conservative boundary shall apply until the Technical Authority records a resolution (C-OPS-003)."),
])
replace(body, "Each limit shall be recorded in the Operating", "rec",
        "Each limit shall be recorded in the Operating Limits Register with a unique identifier, explicit units and enough context for ONE and the control room display to show the approved boundary and response.")
add(body, "Registers, control-system", [
    ("rc", "A limit shall not be published until it has an accountable owner, a technical approver, a monitoring method and a response instruction (C-OPS-004)."),
    ("rc", "Alarm and trip settings in the control system shall be reconciled with the Operating Limits Register every six months by the Instrumentation & Control Lead (C-OPS-005)."),
], at_start=False)
replace(body, "Excursions are assessed by limit class", "p",
        "Excursions are assessed by limit class, magnitude, duration, trend and consequence. Where uncertainty exists, treat the event as the more severe class pending assessment.")
add(body, "Excursion response", [
    ("rc", "Operators shall respond to a critical IOW excursion with the approved immediate action and notify the Area Authority and Technical Authority within one hour (C-OPS-006)."),
    ("rc", "A standard IOW excursion that lasts longer than its duration allowance, or recurs three times in 30 days, shall be reported in the incident system under ACE-INC-STD-001 (C-OPS-007)."),
    ("rc", "Repeated excursions shall not be normalised by resetting or acknowledging alarms; target values shall not be used in place of approved limits (C-OPS-008)."),
])
replace(body, "Operating limits may be changed only", "p",
        "Temporary limits have an expiry and a named accountable owner. Review follows incidents, process changes, equipment modification, chemistry change, "
        "inspection findings, study revisions or material trend shifts.")
add(body, "Change, review and assurance", [
    ("rc", "Operating limits shall only be changed through ACE-MOC-PRC-001, and the MOC shall identify the technical basis, affected modes, alarms and trips, procedures, training and registers (C-OPS-009)."),
    ("appr", "A change to a critical IOW shall be endorsed by the relevant Technical Authority and approved by the VP Operations."),
    ("rc", "The Process Engineering Lead and Materials & Corrosion Lead shall hold a quarterly IOW review of excursion trends and record decisions and actions (C-OPS-010)."),
    ("kpi", "Leading: critical IOW excursions acknowledged within one hour (target 100%); IOW reviews held on schedule (target 100%); register-to-DCS mismatches (target 0). Lagging: integrity damage attributed to an IOW excursion."),
], at_start=False)
add(body, "Records and data quality", [
    ("rc", "The excursion log shall record every IOW excursion with time, value, duration, response and closure, and shall be retained for the life of the asset (C-OPS-011)."),
])
for i, b in enumerate(body):
    if b[0] == "t" and b[1][0][0] == "Process / procedure":
        body[i] = ("t", [["Number", "Title", "Status", "Steps relied on"],
                         ["ACE-OPS-PRS-001", "Operating Limit Management Process", "Planned", "Limit proposal, technical review, register update, monitoring and excursion review"],
                         ["ACE-MOC-PRC-001", "Management of Change Procedure", "Current", "Change screening, assessment, approval, implementation and close-out"],
                         ["ACE-INC-STD-001", "Incident Reporting and Investigation Standard", "Current", "Event classification, notification, investigation and learning"],
                         ["ACE-AIM-PRA-001", "Risk-Based Inspection and Corrosion Management Practice", "Current", "Inhibitor delivery verification and corrosion monitoring"]],
                       [2, 3, 1.2, 3.4])
add(body, "Example limits", [
    ("rc", "The Pommerac A export line corrosion inhibitor injection rate shall be a monitored IOW, verified daily from pump status, rate and tank level (C-OPS-012)."),
])
controls = [
    ("C-OPS-001", "IOWs are classified and displayed by class", "Excursion response mismatched to consequence", "3", "Limit proposal", "Operating Limits Register"),
    ("C-OPS-002", "Limit has an approved technical basis", "Unsafe or arbitrary limit", "4", "Technical review", "Technical basis dossier"),
    ("C-OPS-003", "Conservative boundary applies to conflicts", "Wrong limit applied", "4", "Technical review", "TA resolution record"),
    ("C-OPS-004", "Limit published only with owner, approver, monitoring and response", "Unowned limit", "5", "Register update", "Register entry"),
    ("C-OPS-005", "Control system settings reconciled with register", "Display or trip differs from approved limit", "5", "Monitoring", "Reconciliation report"),
    ("C-OPS-006", "Critical IOW excursion has immediate response and notification", "Integrity damage escalates", "6", "Excursion review", "Excursion log"),
    ("C-OPS-007", "Sustained or repeat excursion reported as incident", "Process drift unrecognised", "6", "Excursion review", "Incident record"),
    ("C-OPS-008", "No normalisation of excursions", "Informal tolerance develops", "6", "Monitoring", "Alarm and shift logs"),
    ("C-OPS-009", "Limit changes go through MOC", "Uncontrolled change", "7", "Register update", "MOC record"),
    ("C-OPS-010", "Quarterly IOW review", "Slow degradation missed", "7", "Excursion review", "IOW review record"),
    ("C-OPS-011", "Excursion log complete and retained", "Lost evidence for integrity decisions", "8", "Monitoring", "Excursion log"),
    ("C-OPS-012", "Pommerac A inhibitor injection verified daily", "Internal corrosion of export line", "A", "Monitoring", "Daily injection record"),
]
SPEC = dict(
    meta=dict(DocumentId="ACE-OPS-PRA-001", Title="Operating Envelopes and Integrity Operating Windows Practice", DocumentType="Practice",
              Level="2", Revision="01", Status="Approved", IssueDate="15 May 2026", EffectiveDate="1 June 2026",
              Author=who("Michelle de Verteuil"),
              Reviewer="; ".join(who(n) for n in ["Rohan Ali", "Arjun Gittens", "Rajesh Ramsaran", "Sophia de Souza"]),
              Endorser="Technical Leadership Council", Approver=who("Sophia Hosany"), DocumentOwner=who("Sophia Hosany"),
              ProcessOwner="Not applicable", Custodian=who("Michelle de Verteuil"), PrimaryFunction="Operations",
              TitleOMSTags="6.3, 5.4, 9.1", Classification="Internal", Applicability="PAP, CHB, SAP, CPF, LND",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Practice owner; Technical Authority; Process Engineering Lead; Area Authority; Shift Supervisor; Production Chemistry Lead",
              Parent="ACE-OPS-STD-001"),
    label="ACE  /  LEVEL 2 PRACTICE  /  APPROVED CONTROLLED DOCUMENT",
    subtitle="Methods for defining, approving, monitoring and responding to operating limits and integrity operating windows across ACE facilities.",
    history=[("A", "—", "Initial draft for review."), ("01", "1 June 2026", "Initial approved issue. Replaces placeholder control statements with controls C-OPS-001 to C-OPS-012; names the Area Authority.")],
    processes=None, body=body, controls=controls)
