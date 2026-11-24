from specutil import *
exec(open("/home/claude/specs/x_ACE-COW-PRC-002.py").read())
body = list(BODY)
take_controls(body, "Controls established")
drop(body, "Processes and procedures implementing")
heads = [["Step", "Application"], ["Item", "Minimum information"]]
k = 0
for i, b in enumerate(body):
    if b[0] == "t":
        body[i] = ("t", [heads[k]] + [r[:2] for r in b[1][1:]], [1, 3])
        k += 1
replace(body, "Positive isolation is used when required", "p",
        "Positive isolation is used when required by Standard, risk, intrusive scope or technical criteria. Consider valve reliability, leakage, "
        "differential pressure, hazardous contents, access and failure modes. Double block and bleed needs independently effective closures, a safe "
        "bleed route, a secured bleed and a monitored condition.")
add(body, "Purpose, scope", [
    ("p", "Parent: ACE-COW-STD-001 Control of Work Standard. This procedure is used with ACE-COW-PRC-001 Permit to Work Procedure; no permit for "
          "intrusive work is issued until the isolation in this procedure is verified."),
    ("warn", "Do not treat a closed valve, a control-system inhibit or a panel indication as proof of isolation. Verify the safe state."),
])
add(body, "Roles and responsibilities", [
    ("resp", "The Isolating Authority shall apply, secure, verify and record every isolation point on the certificate."),
    ("resp", "The Technical Authority for the discipline shall approve any complex or non-standard isolation before it is applied."),
])
add(body, "Planning and source identification", [
    ("rc", "Every energy source, including stored, induced and cross-connected energy, shall be identified on the isolation plan and the isolation points shall be verified in the field before approval (C-COW-010)."),
])
add(body, "Method selection", [
    ("rc", "The isolation method shall be selected from the hazard and the approved criteria in ACE-COW-STD-001, and positive isolation shall be used where those criteria require it (C-COW-011)."),
])
add(body, "Certificate, locks", [
    ("rc", "Every isolation point shall be locked, tagged and recorded with a unique identifier on the certificate and the isolation register (C-COW-012)."),
])
add(body, "Apply, secure and verify", [
    ("rc", "The safe state shall be verified by a suitable test, recorded with reading, instrument, time and verifier, before the permit is released for work (C-COW-013)."),
])
add(body, "Personal and group lock", [
    ("rc", "Each exposed worker shall apply a personal lock to the group lockbox, and an abandoned lock shall only be removed through the approved exceptional removal steps (C-COW-014)."),
])
add(body, "Maintain isolation", [
    ("rc", "Isolation status shall be revalidated at every shift handover, permit suspension, scope change or change in operating conditions (C-COW-015)."),
])
add(body, "Clearance and reinstatement", [
    ("rc", "Isolations shall only be removed after clearance is confirmed, personal locks are accounted for and the blind and spade register is reconciled (C-COW-016)."),
])
add(body, "Removal, restoration", [
    ("rc", "Operations shall verify configuration and readiness before equipment is energized or pressurized, and records shall only be closed when restoration evidence is complete (C-COW-017)."),
])
add(body, "Complex, emergency", [
    ("rc", "If the required isolation cannot be achieved, work shall stop, and any alternative safeguard shall be approved as a deviation under ACE-OMS-STD-002 (C-COW-018)."),
])
add(body, "Records, assurance", [
    ("rc", "The Maintenance Superintendent shall check field isolations against their certificates on a monthly sample at each site and record the result (C-COW-019)."),
    ("kpi", "Leading: isolations verified independently where required (target 100%); lock and tag discrepancies found in sampling. Lagging: isolation failures; unexpected energy releases."),
])
add(body, "Records, assurance", [("h1", "Related processes and documents", "7.1, 7.4"),
    ("t", [["Number", "Title", "Status", "Relationship"],
           ["ACE-COW-STD-001", "Control of Work Standard", "Current", "Parent Standard"],
           ["ACE-COW-PRC-001", "Permit to Work Procedure", "Current", "Permit issue depends on verified isolation"],
           ["ACE-COW-PRS-001", "Permit to Work Process", "Planned", "Isolation steps in the cross-functional process"],
           ["ACE-OMS-STD-002", "Deviation and Exemption Standard", "Current", "Alternative safeguards when isolation cannot be achieved"]],
     [2, 3, 1.2, 3.4])])
controls = [
    ("C-COW-010", "All energy sources identified and field verified", "Unexpected energy release", "3", "Isolation planning", "Isolation plan"),
    ("C-COW-011", "Method selected by hazard and approved criteria", "Inadequate isolation method", "4", "Method selection", "Certificate"),
    ("C-COW-012", "Points locked, tagged and uniquely recorded", "Inadvertent restoration", "5", "Apply isolation", "Isolation register"),
    ("C-COW-013", "Isolation effectiveness verified before work", "Exposure to live energy", "6", "Verify isolation", "Verification record"),
    ("C-COW-014", "Personal and group lock protection", "Worker unprotected", "7", "Apply isolation", "Lockbox record"),
    ("C-COW-015", "Status revalidated after change", "Isolation compromised", "8", "Maintain isolation", "Handover log"),
    ("C-COW-016", "Clearance complete before removal", "Re-energization with people exposed", "9", "Clearance", "Reinstatement checklist"),
    ("C-COW-017", "Restoration verified before return to service", "Unsafe start-up", "10", "Return to service", "Hand-back record"),
    ("C-COW-018", "Work stops when isolation cannot be achieved", "Unapproved compensating measures", "11", "Method selection", "Deviation record"),
    ("C-COW-019", "Monthly field sampling of isolations", "Weak assurance evidence", "12", "Assurance", "Sample record"),
]
SPEC = dict(
    meta=dict(DocumentId="ACE-COW-PRC-002", Title="Isolation and Reinstatement Procedure", DocumentType="Procedure",
              Level="4", Revision="01", Status="Approved", IssueDate="15 May 2026", EffectiveDate="1 June 2026",
              Author=who("Sunita Seepersad"),
              Reviewer="; ".join(who(n) for n in ["Rishi Seecharan", "Adrian Rodriguez", "Arjun Khan", "Christina Bain"]),
              Endorser="Not required", Approver=who("Marc Gomes"), DocumentOwner=who("Marc Gomes"),
              ProcessOwner="Not applicable", Custodian=who("Sunita Seepersad"), PrimaryFunction="Operations",
              TitleOMSTags="8.2, 6.5, 8.1", Classification="Internal", Applicability="PAP, CHB, SAP, CPF, LND, PLB",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Isolation Planner; Isolating Authority; Area Authority; Performing Authority; Technical Authority; Maintenance Superintendent",
              Parent="ACE-COW-STD-001"),
    label="ACE  /  LEVEL 4 PROCEDURE  /  APPROVED CONTROLLED DOCUMENT",
    subtitle="Planning, applying, verifying and removing isolations, and returning equipment to service.",
    history=[("A", "—", "Draft for review."), ("01", "1 June 2026", "Initial approved issue. Repairs tables, assigns Control IDs C-COW-010 to C-COW-019 and names the owner and reviewers.")],
    processes=None, body=body, controls=controls)
