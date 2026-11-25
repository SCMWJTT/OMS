# ACE-RSK-POL-001 Operational Risk Management Policy (Revision A).
# Thresholds follow the issued standards (Wilmark, Session 4): acceptance ACE-RSK-STD-001 §5.1, deviation periods ACE-OMS-STD-002 §5.1,
# change classes ACE-MOC-PRC-001 §2.2, response levels ACE-EMR-STD-001 §3.2.
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "5.1, 2.1"),
    ("p", "This policy sets how ACE understands, accepts, changes and learns from operational risk, and how it prepares for and responds "
          "to emergencies. It brings together risk assessment, barriers, Management of Change, deviations, incident learning, emergency "
          "response, crisis management and business continuity under one set of commitments and decision rules."),
    ("p", "It applies to all ACE sites (HOF, PLB, PAP, CHB, SAP, CPF and LND), all functions, all phases of the asset life, and to "
          "contractors working on ACE activities. Its parent is ACE-LDR-POL-001. The detailed rules are in the implementing standards "
          "listed in section 6.2; where this policy states a band or a number, it is the one set in those standards."),

    ("h1", "Our commitments", "5.1, 5.2"),
    values_note(),
    ("h2", "Assess risk before acting", "5.1, 5.2", "COM_ASSESS"),
    ("p", "In line with our values Safety above all and One team, one way, ACE assesses risk before it acts, using one ACE Risk Matrix for "
          "every kind of risk: people, environment, asset and production, and reputation (ACE-RSK-STD-001). A risk is accepted only by the "
          "person with the authority for its band, and only once it is as low as reasonably practicable."),
    ("h2", "Barriers are identified, owned and verified", "5.1, 6.4", "COM_BARRIERS"),
    ("p", "In line with our value Safety above all, every significant risk has prevention and recovery barriers that are identified, have "
          "an owner and are tested to show they work. A barrier that has not been verified is not counted as available (ACE-RSK-PRA-001)."),
    ("h2", "Change is controlled", "5.3, 6.2", "COM_CHANGE"),
    ("p", "In line with our values Safety above all and One team, one way, no change to plant, process, people, procedures or organisation "
          "that could affect risk is made without Management of Change. Each change is classified by its most significant credible impact, "
          "assessed, approved at the right level, and verified before it is put into use (ACE-MOC-PRC-001)."),
    ("req", "A change to plant, process, people, procedures or organisation that could affect risk shall not be implemented until it has "
            "been approved under ACE-MOC-PRC-001."),
    ("h2", "Departures are temporary", "2.6, 5.2", "COM_DEVIATIONS"),
    ("p", "In line with our values Integrity in everything and Safety above all, a departure from an ACE requirement is a temporary, "
          "controlled condition and never a quiet new normal. Every deviation has an expiry date, compensating measures and a named approver; "
          "at expiry without a replacement approval, the affected work stops or the equipment goes to its safe state (ACE-OMS-STD-002)."),
    ("h2", "Learn from every event", "9.2, 9.3", "COM_LEARN"),
    ("p", "In line with our value Learn and improve, every incident, near miss and non-conformance is reported, investigated in proportion "
          "to its actual and potential consequence, and closed with actions whose effectiveness is verified. Lessons are shared across sites. "
          "Actions that change a process are handed to the improvement arrangements of ACE-OMS-POL-001 and recorded in the CI register with "
          "the source \"incident and near-miss actions\"."),
    ("h2", "Rising risk is escalated early", "5.4, 9.4", "COM_EARLY_WARNING"),
    ("p", "In line with our values Safety above all and Integrity in everything, weak signals are acted on before they become events: "
          "repeated alarms, overdue safety-critical work, growing action backlogs, repeated deviations and workarounds. A risk that moves to "
          "a higher band is escalated to the acceptance authority for the new band without waiting for the next scheduled review."),
    ("h2", "Prepare, respond and recover", "7.5, 4.4", "COM_EMERGENCY"),
    ("p", "In line with our values Safety above all and Care for people and places, every site has a tested emergency response plan, ACE "
          "has an oil spill contingency plan for the Gulf of Paria and its land operations, and critical business functions have tested "
          "continuity arrangements. When an emergency happens we protect people first, then the environment, then the asset, and we keep "
          "communities, regulators, partners and customers informed (ACE-EMR-STD-001)."),

    ("h1", "Accountabilities", "3.1, 5.2"),
    ("t", [("Role", "Named person", "Accountability"),
           ("VP HSE & Compliance (policy owner)", "George Habib", "Owns this policy, the ACE Risk Matrix and the emergency, crisis and continuity system; consolidates the quarterly significant-risk report."),
           ("Chief Executive Officer", "Satesh Sankar", "Decides on exceptional recovery plans for Very High risks; leads the Crisis Management Team."),
           ("Head of Internal Audit & Risk Assurance", "Nicole Lange", "Maintains the corporate risk register with function owners."),
           ("HSE Manager (custodian)", "Christina Bain", "Maintains this policy; owner of the Risk and Control Review Process and the Incident Reporting and Investigation Process."),
           ("Manager, Technical Excellence", "Elena Farfan", "Owner of the Management of Change Process (ACE-MOC-PRS-001)."),
           ("Emergency Response & Security Manager", "Jenelle Paul", "Owner of the Emergency Drill and Exercise Process; custodian of emergency, crisis and continuity requirements."),
           ("Process Safety Lead", "Damian Daniel", "Owns the hazard study programme and the Controls Register."),
           ("VP Operations (interim process owner)", "Sophia Hosany", "Interim owner of the SCE Deviation Process (ACE-MNT-PRS-002); the register still shows a former owner."),
           ("OMS Manager", "Marissa Bobb", "Reviews deviation requests outside the initial duration schedule with the relevant Vice President.")],
     [3, 2, 5]),
    ("resp", "Each Risk Owner shall keep their risk, its barriers and its actions current in the risk register and review them at the "
             "frequency set in section 5.2."),

    ("h1", "Decision rights and thresholds", "5.2, 2.6"),
    ("p", "These thresholds are the conditions on the decision points in the processes this policy governs. They are taken from the "
          "implementing standards named in each table, which hold the full rules."),
    ("h2", "Risk appetite", "5.2, 5.1", "DR_APPETITE"),
    ("p", "ACE states its appetite for residual risk against the four consequence domains of the ACE Risk Matrix (ACE-RSK-STD-001 §3.3). "
          "Financial consequence is assessed in the asset and production domain."),
    ("t", [("Consequence domain", "Appetite", "Position by residual band"),
           ("People", "None", "Low and Medium tolerated with verified controls. High only as a temporary, dated condition with an ALARP case. Very High never in routine operation."),
           ("Environment", "Very low", "As for people. No routine operation with a High residual risk of a spill reaching land or the Gulf of Paria."),
           ("Asset and production (including financial)", "Moderate", "Medium accepted as part of normal business. High accepted by the Vice President with a dated reduction plan."),
           ("Reputation", "Low", "Medium accepted with a communication plan. High accepted by the Vice President with the VP Communications & Corporate Services informed.")],
     [2.6, 1.2, 6.2]),
    ("h2", "Risk acceptance authority", "5.2, 3.1", "DR_ACCEPTANCE"),
    ("p", "The minimum authority to accept a current or residual risk is set by its band on the ACE Risk Matrix (ACE-RSK-STD-001 §5.1). "
          "This is the condition on the approval branch of Management of Change, deviation and risk review processes."),
    ("t", [("Residual band", "Minimum acceptance authority", "Condition"),
           ("Low", "Accountable Supervisor or L4 Lead", "Task controls verified and recorded."),
           ("Medium", "Function Manager or Area Authority (L3)", "Documented safeguards, control owner, action dates and review period."),
           ("High", "Relevant Vice President (L2)", "Technical Authority endorsement where technical barriers are affected; ALARP case; defined expiry or review."),
           ("Very High", "Not acceptable for routine activity", "Stop or prevent exposure. Only the Chief Executive Officer may approve an exceptional recovery plan, after VP and Technical Authority review.")],
     [1.6, 3.2, 5.2]),
    ("appr", "A High residual risk shall be accepted only by the relevant Vice President, with a written ALARP case endorsed by the "
             "Technical Authority where technical barriers are affected."),
    ("h2", "Management of Change classes", "5.3, 2.2", "DR_MOC_CLASS"),
    ("p", "Every change is classified by its most significant credible impact (ACE-MOC-PRC-001 §2.2). In one line: C3 if it could affect a "
          "major accident hazard, creates or materially alters a safety-critical element, ties in a major project or changes the shutdown or "
          "relief philosophy; C2 if it changes plant configuration, operating limits, procedures, interfaces, competence or roles; otherwise "
          "C1. This is the Classify change decision in the MOC process."),
    ("t", [("Class", "Description", "Minimum path"),
           ("C1 — Local controlled", "Small, bounded change within an established design envelope; no new SCE function or major accident scenario.", "Documented screening, focused risk review, Technical Authority agreement as applicable, manager and Area Authority approval."),
           ("C2 — Significant", "Changes plant configuration, operating limits, procedures, interfaces, competence or safety-critical support arrangements.", "Multi-discipline risk assessment, technical endorsement, pre-start-up review and management approval."),
           ("C3 — Major or complex", "Credible major accident hazard effect; new or materially altered SCE; major project tie-in; changed shutdown or relief philosophy.", "Formal hazard study, Process Safety Lead review, technical challenge and approval at the acceptance authority for the residual band.")],
     [2, 4, 4]),
    ("h2", "Deviation periods", "2.6, 5.2", "DR_DEVIATION"),
    ("p", "The maximum initial period of a deviation is set by its residual risk band (ACE-OMS-STD-002 §5.1). This drives the expiry and "
          "extension cycle."),
    ("t", [("Residual band", "Maximum initial period", "Review while open"),
           ("Low", "180 days", "At the controls check, when conditions change, and before expiry."),
           ("Medium", "90 days", "At least monthly."),
           ("High", "30 days", "At least weekly; more often for an impaired major accident barrier."),
           ("Very High", "No routine period", "Routine exposure is stopped or prevented.")],
     [1.6, 2.4, 6]),
    ("req", "A deviation shall be extended no more than once under its original identifier, by the same or a higher authority than the "
            "original acceptance, before it expires."),
    ("p", "A request for a longer initial period goes to the relevant Vice President and the OMS Manager for documented justification."),
    ("h2", "Emergency response levels", "7.5, 4.4", "DR_EMERGENCY_LEVELS"),
    ("p", "The response level is chosen by consequence and by the capacity needed to control the event (ACE-EMR-STD-001 §3.2)."),
    ("t", [("Level", "Trigger", "Who leads"),
           ("Level 1 — Site", "The site's own resources and its incident plan can control the event.", "Area Authority as site incident commander"),
           ("Level 2 — IMT supported", "Specialist resources, support from another site or external coordination are needed; or any imminent life threat, possible major accident escalation or material environmental release.", "Site command, supported by the Incident Management Team"),
           ("Level 3 — Crisis", "Strategic, reputational, community or prolonged business disruption; multi-site disruption; significant media or community impact.", "Chief Executive Officer and the Crisis Management Team, alongside the operational response")],
     [2.2, 5, 2.8]),

    ("h1", "How we will know", "9.4, 5.2"),
    ("h2", "Headline indicators", "9.4, 9.3", "KNOW_KPIS"),
    ("kpi", "Tier 1 and Tier 2 process safety events (PSE-T1, PSE-T2). Target: zero Tier 1 and no more than two Tier 2 per year (objective OBJ-26-02)."),
    ("kpi", "Overdue risk and incident actions (ACT-OVERDUE). Target: zero overdue actions on High and Very High risks; fewer than 5% of all actions overdue."),
    ("kpi", "Management of Change median cycle time, from raising to closure. Target: 30 days or fewer."),
    ("kpi", "Deviations past their expiry date. Target: zero at any time."),
    ("p", "Linked objectives: OBJ-26-01 and OBJ-26-02 (injuries and process safety events) and OBJ-26-03 (no loss of containment from integrity failure)."),
    ("h2", "Review cycles", "5.2, 7.5", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency", "Source"),
           ("Corporate significant-risk review and report", "Quarterly", "ACE-RSK-STD-001"),
           ("Asset and function risk registers", "At least six-monthly as a whole; High risks at least quarterly", "ACE-RSK-STD-001"),
           ("Critical control health review", "At least monthly", "ACE-RSK-PRA-001"),
           ("Bow-tie review for each major accident hazard", "On any change to the hazard or its barriers, and at least every three years", "This policy"),
           ("HAZOP revalidation of each operating facility", "At least every five years, and earlier on a trigger", "ACE-PSM-STD-001"),
           ("Drills and exercises", "To each site plan's programme, with at least one major emergency exercise per site each year and an annual oil spill exercise", "ACE-EMR-STD-001"),
           ("Plan updates after drills and real emergencies", "Within 90 days", "ACE-EMR-STD-001")],
     [3.8, 4, 2.2]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 5.1", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("ACE-RSK-PRS-001", "Risk and Control Review Process", "7.1", "Planned"),
           ("—", "Risk assessment and acceptance", "7.1", "Planned"),
           ("ACE-MOC-PRS-001", "Management of Change Process", "7.2", "Planned (draft in progress)"),
           ("—", "Deviation and exemption", "7.2", "Planned"),
           ("ACE-MNT-PRS-002", "SCE Deviation Process (proposed as a branch of Deviation and exemption)", "4.3", "Planned"),
           ("—", "Hazard studies", "7.3", "Planned"),
           ("ACE-INC-PRS-001", "Incident Reporting and Investigation Process", "7.4", "Planned"),
           ("—", "Lessons learned and action tracking", "7.4", "Planned"),
           ("ACE-EMR-PRS-001", "Emergency Drill and Exercise Process", "7.5", "Planned"),
           ("—", "Emergency activation and response", "7.5", "Planned"),
           ("—", "Crisis management and business continuity", "7.5", "Planned")],
     [2.2, 4.6, 1, 1.2]),
    ("p", "Also applies to: every process that contains a risk assessment, a change or a deviation, including the SIS Safety Lifecycle "
          "Process (ACE-ENG-PRS-410) and the Operating Limit Management Process (ACE-OPS-PRS-001)."),
    ("h2", "Standards and practices that implement this policy", "2.1, 5.1", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-RSK-STD-001", "Risk Management Standard", "Current"),
           ("ACE-RSK-PRA-001", "Controls and Barrier Linkage Practice (under ACE-RSK-STD-001)", "Current"),
           ("ACE-PSM-STD-001", "Process Safety and Hazard Study Standard", "Current"),
           ("ACE-INC-STD-001", "Incident Reporting and Investigation Standard", "Current"),
           ("ACE-EMR-STD-001", "Emergency, Crisis and Business Continuity Standard", "Current"),
           ("ACE-OMS-STD-002", "Deviation and Exemption Standard", "Current"),
           ("ACE-MOC-PRC-001", "Management of Change Procedure", "Current"),
           ("ACE-MOC-STD-001", "Management of Change Standard", "Planned"),
           ("ACE-INC-STD-002", "Lessons Learned and Action Tracking Standard", "Planned"),
           ("ACE-PSM-STD-002", "Process Safety Leadership and Early Warning Standard", "Planned"),
           ("ACE-RSK-REG-001", "Corporate and Asset Risk Registers", "Planned"),
           ("ACE-RSK-REG-002", "Controls Register", "Planned")],
     [2.2, 6, 1.2]),
]

ROLES = ["VP HSE & Compliance", "Chief Executive Officer", "Head of Internal Audit & Risk Assurance", "HSE Manager",
         "Manager, Technical Excellence", "Emergency Response & Security Manager", "Process Safety Lead", "VP Operations", "OMS Manager",
         "VP Communications & Corporate Services", "Vice President", "Function Manager", "Area Authority", "Technical Authority",
         "Risk Owner", "Accountable Supervisor", "Process Owner"]

SPEC = new_policy("ACE-RSK-POL-001", "Operational Risk Management Policy",
                  "How ACE assesses, accepts, changes and learns from operational risk, and prepares for and responds to emergencies.",
                  owner="George Habib", author="Damian Daniel",
                  reviewers=["Christina Bain", "Nicole Lange", "Elena Farfan", "Jenelle Paul", "Sophia Hosany", "Marissa Bobb"],
                  custodian="Christina Bain", function="HSE & Compliance", tags="5.1, 5.2, 5.3", roles=ROLES, body=body)
