from specutil import *
exec(open("/home/claude/specs/x_ACE-AIM-PRA-001.py").read())
body = list(BODY)
controls = take_controls(body, "Controls established")
rename(body, "Purpose and scope", "Purpose, scope and parent Standard")
rename(body, "Performance, assurance", "Performance and verification", "9.5, 6.5, 10.4")

add(body, "Purpose, scope", [
    ("p", "Parent Standard: ACE-AIM-STD-001 Asset Integrity Management Standard sets what must be true for asset integrity. This Practice "
          "sets how ACE inspects, monitors and dispositions degradation so that those requirements are met. It applies at PAP, CHB, SAP, CPF, "
          "LND and PLB."),
    ("ext", "Recognised practice applied: API RP 580 Risk-Based Inspection; API RP 581 Risk-Based Inspection Methodology; API RP 584 Integrity "
            "Operating Windows; API 579-1/ASME FFS-1 Fitness-For-Service; API RP 1160 Managing System Integrity for Hazardous Liquid Pipelines; "
            "NACE SP0169 Control of External Corrosion on Underground or Submerged Metallic Piping Systems."),
])
add(body, "Roles and technical authority", [
    ("t", [["Role", "Named person", "Accountability in this Practice"],
           ["Practice owner and approver", who("Dev Jaggernauth"), "Approves the method and its revisions; resolves conflicts between production and integrity priorities."],
           ["Practice custodian", who("Wayne Rajkumar"), "Maintains the method, the inspection programme quality and the deferral register."],
           ["TA — materials and corrosion", who("Sophia de Souza"), "Damage mechanism screening, inhibitor objectives, corrosion rate methods."],
           ["TA — pipelines", who("Allison Mitchell"), "Pipeline threat assessment, ILI and CP strategy, pipeline anomaly disposition."],
           ["TA — static mechanical", who("Marlon Gonzales"), "Pressure equipment, fitness-for-service and repair acceptance."],
           ["Inspection engineering", who("Rochelle Mark"), "RBI inputs, inspection scopes, results evaluation and anomaly records."]],
     [2, 3, 4]),
    ("resp", "The Inspection Lead shall maintain the site inspection programmes, the RBI register and the deferral register, and shall report their status to the Technical Leadership Council each quarter."),
    ("resp", "The Materials & Corrosion Lead shall approve the damage mechanism screening for every corrosion loop and every change to a corrosion inhibitor objective."),
    ("rc", "A technical decision on interval extension, deferral, fitness-for-service or return to service shall be approved by the Technical Authority named for that equipment class, and the decision record shall name the approver (C-AIM-010)."),
])
add(body, "Damage mechanisms", [
    ("rc", "Each corrosion loop shall have a documented damage mechanism screening that is reviewed at least every five years and after any change in fluid composition, operating conditions or materials (C-AIM-002)."),
])
add(body, "Risk-based inspection method", [
    ("rc", "Every integrity-managed item shall hold a current RBI assessment, no older than five years, traceable to its data sources, assumptions and approver (C-AIM-001)."),
    ("note", "Example: on the Pommerac A crude export line, the dominant PoF contributor is internal CO₂ corrosion at low points, and the CoF is driven by environmental release to the Gulf of Paria. Both contributors, and the confidence in the corrosion rate, are stated in the RBI record."),
])
add(body, "Inspection intervals", [
    ("rc", "Every inspection interval shall record its limiting basis (risk, remaining life, statutory or code limit) and the calculation used, and shall not exceed half the calculated remaining life (C-AIM-003)."),
    ("t", [["Risk category (ACE Risk Matrix)", "Default maximum interval", "Interval extension allowed"],
           ["Very high", "1 year or 0.25 × remaining life, whichever is less", "No"],
           ["High", "3 years or 0.5 × remaining life", "Only with TA approval and validated monitoring data"],
           ["Medium", "5 years or 0.5 × remaining life", "Yes, by RBI review"],
           ["Low", "10 years or 0.5 × remaining life", "Yes, by RBI review"]], [2, 3, 3]),
])
add(body, "Corrosion monitoring", [
    ("rc", "Corrosion inhibitor delivery shall be verified against its integrity operating window in ACE-OPS-PRA-001 at least weekly, and any sustained under-delivery shall be raised to the Materials & Corrosion Lead within 24 hours (C-AIM-005)."),
])
add(body, "Pipeline integrity", [
    ("rc", "Each pipeline shall have an integrity plan that sets ILI, CP survey and patrol frequencies from its threat assessment, reviewed annually by the Pipelines Lead (C-AIM-006)."),
    ("t", [["Pipeline activity", "Minimum frequency", "Owner"],
           ["Intelligent pigging (ILI)", "Per threat assessment; not more than 5 years for export lines", "Pipelines Lead"],
           ["CP potential survey", "Annual; close-interval survey every 5 years", "Pipelines Lead"],
           ["Offshore boat patrol (Gulf of Paria)", "Monthly, arranged through ACE-LOG-PRA-001", "Offshore Operations Manager (Gulf of Paria)"],
           ["Land right-of-way patrol", "Weekly", "Land Operations Manager"]], [3, 3, 2]),
])
add(body, "Deferral, anomalies", [
    ("rc", "An inspection of a Safety Critical Element shall only be deferred with a documented risk assessment, TA approval, interim safeguards and an expiry date, and the deferral shall be visible in ONE until closed (C-AIM-004)."),
    ("rc", "Every anomaly shall have a risk ranking, a named owner, a due date and closure evidence recorded in the anomaly register (C-AIM-007)."),
    ("warn", "Do not reset the due date of a deferred inspection. The original due date stays on the record so that overdue time remains visible."),
])
add(body, "Data, records", [
    ("rc", "Inspection and monitoring data shall be validated by the Inspection Engineer before it is used in an RBI, interval or fitness-for-service decision (C-AIM-008)."),
    ("rec", "Inspection results, corrosion rates, deferrals and anomaly dispositions shall be recorded in the CMMS against the equipment ID and retained for the life of the asset."),
])
add(body, "Performance and verification", [
    ("rc", "The Inspection Lead shall review programme completion, overdue inspections, deferrals and repeat damage every quarter and record the actions raised (C-AIM-009)."),
    ("kpi", "Leading: SCE inspections completed on time (target ≥ 95%); deferrals open past expiry (target 0); inhibitor availability within IOW (target ≥ 95%). Lagging: loss of containment from internal corrosion (target 0); repeat anomalies on the same loop."),
])
SPEC = dict(
    meta=dict(DocumentId="ACE-AIM-PRA-001", Title="Risk-Based Inspection and Corrosion Management Practice", DocumentType="Practice",
              Level="2", Revision="01", Status="Approved", IssueDate="15 May 2026", EffectiveDate="1 June 2026",
              Author=who("Rochelle Mark"),
              Reviewer="; ".join(who(n) for n in ["Wayne Rajkumar", "Sophia de Souza", "Allison Mitchell", "Marlon Gonzales"]),
              Endorser="Technical Leadership Council", Approver=who("Dev Jaggernauth"), DocumentOwner=who("Dev Jaggernauth"),
              ProcessOwner="Not applicable", Custodian=who("Wayne Rajkumar"), PrimaryFunction="Engineering & Projects",
              TitleOMSTags="6.5, 6.4, 5.4", Classification="Internal", Applicability="PAP, CHB, SAP, CPF, LND, PLB",
              ReviewInterval="Three years; earlier if triggered",
              RoleRegister="Practice owner; Technical Authority; Inspection Lead; Inspection Engineer; Materials & Corrosion Lead; Pipelines Lead; Area Authority",
              Parent="ACE-AIM-STD-001"),
    label="ACE  /  LEVEL 2 PRACTICE  /  APPROVED CONTROLLED DOCUMENT",
    subtitle="Method for assessing degradation, planning inspection, managing corrosion and dispositioning anomalies.",
    history=[("A", "—", "Draft for review."), ("01", "1 June 2026", "Initial approved issue. Adds named roles, binding statements and Control IDs C-AIM-001 to C-AIM-010.")],
    processes=None, body=body, controls=controls)
