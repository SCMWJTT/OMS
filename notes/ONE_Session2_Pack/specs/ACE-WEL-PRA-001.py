from specutil import *
exec(open("/home/claude/specs/x_ACE-WEL-PRA-001.py").read())
body = [b for b in BODY if not (b[0] == "rc" and b[1].startswith("Well barrier envelopes, elements"))]
rename(body, "Roles and technical authority", "Roles and technical authority", kind="h1")
replace(body, "This Practice defines ACE’s technical method", "p",
        "This Practice defines ACE’s technical method for establishing, verifying, monitoring and handing over well barriers in drilling, completion, "
        "production, suspension, intervention and abandonment states. It applies to wells at Pommerac A (PAP), Chenet B (CHB), Sapodilla C (SAP), and land "
        "leases Tamarind, Pawpaw and Soursop (LND). It serves ACE-WEL-STD-001 Well Integrity Management Standard. Well-specific barrier schematics, status "
        "records and acceptance evidence are mandatory parts of the well file.")
for i, b in enumerate(body):
    if b[0] == "t" and b[1][0] == ["Role", "Accountability"]:
        rows = [r for r in b[1] if not r[0].startswith(("Operations /", "Wellsite"))]
        rows.append([who("Arjun Gittens"), "Accepts operational well status, surveillance and response for offshore wells."])
        body[i] = ("t", rows)
    if b[0] == "t" and b[1][0][0] == "Reference":
        body[i] = ("t", [r if r[0] != "ACE-WEL-STD-001" else ["ACE-WEL-STD-001", "Parent Well Integrity Management Standard."] for r in b[1]])
add(body, "Roles and technical authority", [
    ("resp", "The Well Integrity Lead shall maintain the well integrity register, the barrier methodology and the integrity category of every ACE well."),
    ("resp", "The wellsite or intervention supervisor shall keep the barrier status current during operations and record every barrier test."),
])
add(body, "Barrier philosophy", [
    ("rc", "Every well shall have a current well-specific barrier schematic for its present state that identifies the primary and secondary barrier envelopes (C-WEL-001)."),
    ("rc", "The independence of the two barrier envelopes shall be assessed for common failure modes and recorded on the schematic (C-WEL-002)."),
])
replace(body, "Barrier elements are accepted against", "p",
        "Barrier elements are accepted against a defined function, design envelope and verification method.")
add(body, "Barrier element acceptance", [
    ("rec", "The well file shall identify each barrier element’s type, location, exposure, test criteria, test medium, duration, result and instrument calibration status."),
    ("rc", "Acceptance criteria shall be drawn from the approved well design and well-specific engineering basis, and an element whose test is invalid shall not be credited as a barrier (C-WEL-003)."),
], at_start=False)
add(body, "Well integrity categories", [
    ("rc", "The Well Integrity Lead shall assign each well a category with recorded rationale, and every category change shall be communicated to Operations within 24 hours (C-WEL-004)."),
    ("rc", "A well in Red category shall have the affected operation stopped and the well secured before any further work, with escalation to the VP Wells (C-WEL-005)."),
])
add(body, "Annulus pressure", [
    ("rc", "Each annulus shall have an approved MAASP calculated from the weakest exposed element of that well, and MAASP values shall not be copied between wells (C-WEL-006)."),
    ("rc", "Annulus bleed-down shall only be carried out under an approved plan and shall not be used to reset a pressure alarm (C-WEL-007)."),
    ("rc", "Unexplained annulus pressure, a threshold exceedance or an adverse trend shall be notified to the Well Integrity Lead and Operations within 24 hours (C-WEL-008)."),
])
add(body, "Well handover", [
    ("rc", "A well shall only be handed over to Operations when the handover pack is complete and the receiving Operations role has recorded acceptance (C-WEL-009)."),
    ("rc", "After intervention, the schematic, test evidence, category and register shall be updated before the well is returned to Operations (C-WEL-010)."),
])
replace(body, "Chenet B and Sapodilla C are normally unmanned", "p",
        "Chenet B and Sapodilla C are normally unmanned and accessed by boat. Land wells at Tamarind, Pawpaw and Soursop require site access coordination, "
        "local hazards, test equipment logistics and records suitable for dispersed locations.")
add(body, "Unmanned platform", [
    ("req", "Barrier surveillance and test plans for unmanned platforms shall account for weather, boat availability, visit frequency, remote monitoring limits and contingency response while the site is unattended."),
    ("rc", "A missed visit or overdue barrier test on an unmanned platform shall be assessed against the well category within 72 hours and shall not be deferred to the next convenient boat trip without that assessment (C-WEL-011)."),
], at_start=False)
add(body, "Records, performance", [
    ("rc", "The Well Integrity Lead shall review the well integrity register every quarter, including overdue tests, open anomalies and category changes, and report to the VP Wells (C-WEL-012)."),
    ("kpi", "Leading: barrier tests completed on time (target ≥ 98%); wells with a current schematic (target 100%); handovers accepted first time. Lagging: wells in Orange or Red category; MAASP exceedances."),
])
for i, b in enumerate(body):
    if b[0] == "t" and b[1][0][0] == "Process / procedure":
        body[i] = ("t", [["Number", "Title", "Status", "Steps relied on"],
                         ["ACE-WEL-PRS-001", "Well Handover Process", "Planned", "Prepare pack, technical review, Operations acceptance, live transfer, closeout"],
                         ["ACE-WEL-PRS-002", "Annulus Pressure Management Process", "Planned", "Monitor, assess trend, diagnose, bleed-down if authorised, escalate, verify and close"],
                         ["ACE-MOC-PRC-001", "Management of Change Procedure", "Current", "Barrier design or state changes, review, authorisation, implementation and verification"]],
                       [2, 3, 1.2, 3.4])
controls = [
    ("C-WEL-001", "Current well-specific barrier schematic", "Unknown barrier status", "3", "Barrier review", "Barrier schematic"),
    ("C-WEL-002", "Barrier independence assessed", "Common-mode barrier failure", "3", "Barrier review", "Schematic annotation"),
    ("C-WEL-003", "Elements accepted against well-specific criteria", "Unverified element credited", "4", "Barrier testing", "Barrier test record"),
    ("C-WEL-004", "Integrity category assigned and communicated", "Degraded well operated normally", "5", "Category review", "Well integrity register"),
    ("C-WEL-005", "Red category well secured and escalated", "Loss of well control", "5", "Category review", "Incident record"),
    ("C-WEL-006", "Well-specific MAASP", "Annulus over-pressure", "6", "Annulus monitoring", "MAASP sheet"),
    ("C-WEL-007", "Bleed-down under approved plan only", "Masked annulus communication", "6", "Annulus monitoring", "Bleed-down log"),
    ("C-WEL-008", "Abnormal annulus pressure notified", "Escalating integrity threat", "6", "Annulus monitoring", "Notification record"),
    ("C-WEL-009", "Handover only with complete pack and acceptance", "Barrier status lost at handover", "7", "Well handover", "Handover acceptance"),
    ("C-WEL-010", "Records updated before return to Operations", "Outdated well file", "7", "Closeout", "Updated schematic and register"),
    ("C-WEL-011", "Missed visit or test assessed on unmanned sites", "Undetected barrier degradation", "8", "Surveillance planning", "Assessment record"),
    ("C-WEL-012", "Quarterly well integrity review", "Systemic barrier issues missed", "9", "Performance review", "Review minutes"),
]
SPEC = dict(
    meta=dict(DocumentId="ACE-WEL-PRA-001", Title="Well Barriers and Well Handover Practice", DocumentType="Practice",
              Level="2", Revision="01", Status="Approved", IssueDate="15 May 2026", EffectiveDate="1 June 2026",
              Author=who("Shalini Jaggernauth"),
              Reviewer="; ".join(who(n) for n in ["Arjun Ramlal", "Kathy-Ann Simmons", "Nazim Bailey"]),
              Endorser="Technical Leadership Council", Approver=who("Joanne Ho Sing"), DocumentOwner=who("Joanne Ho Sing"),
              ProcessOwner="Not applicable", Custodian=who("Shalini Jaggernauth"), PrimaryFunction="Wells",
              TitleOMSTags="6.4, 6.5, 8.1", Classification="Internal", Applicability="PAP, CHB, SAP, LND, PLB",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Practice owner; Technical Authority; Well Integrity Lead; Wellsite supervisor; Area Authority; Offshore Operations Manager",
              Parent="ACE-WEL-STD-001"),
    label="ACE  /  LEVEL 2 PRACTICE  /  APPROVED CONTROLLED DOCUMENT",
    subtitle="Establishing, verifying, monitoring and handing over well barriers through every well state.",
    history=[("A", "—", "Initial draft for review."), ("01", "1 June 2026", "Initial approved issue. Replaces placeholder control statements with controls C-WEL-001 to C-WEL-012; names all accountable roles.")],
    processes=None, body=body, controls=controls)
