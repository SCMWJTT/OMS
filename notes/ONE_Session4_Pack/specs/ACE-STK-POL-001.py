# ACE-STK-POL-001 Stakeholder, Community and Grievance Policy (Revision A).
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "4.1, 4.3"),
    ("p", "This policy sets how ACE knows, engages and listens to the people affected by its work: neighbours of the Point Lisas Shore "
          "Base, the CPF and the land leases, fishing communities in the Gulf of Paria, landowners, local authorities and regulators. It "
          "sets clear times for answering grievances."),
    ("p", "It applies to all ACE sites and activities and to contractors working for ACE in the community. Its parent is "
          "ACE-LDR-POL-001. Customer relationships for gas and crude are covered by ACE-HMA-POL-001."),

    ("h1", "Our commitments", "4.1, 4.3"),
    values_note(),
    ("h2", "Know and engage our stakeholders", "4.1, 4.4", "COM_ENGAGE"),
    ("p", "In line with our value Care for people and places, ACE keeps a current map of the people and groups affected by each site (PLB, "
          "the CPF and the land leases) and by its marine activity, and meets them regularly so that relationships exist before they are "
          "needed."),
    ("h2", "Grievances are answered on time", "4.3, 4.2", "COM_GRIEVANCES"),
    ("p", "In line with our values Care for people and places and Integrity in everything, every grievance or complaint is logged, "
          "acknowledged and answered within the times in section 4.1, and escalated if it is not resolved. No one is disadvantaged for "
          "raising a grievance."),
    ("rec", "Every grievance shall be logged in the grievance register with the date received, the acknowledgement, the response and the outcome."),
    ("h2", "Fishing communities are consulted before marine activity", "4.1, 4.2", "COM_FISHERS"),
    ("p", "In line with our value Care for people and places, fishing communities in the Gulf of Paria are consulted before marine activity "
          "that affects them, such as rig moves, pipeline work, surveys and exclusion zones, with the notice set in section 4.2."),
    ("h2", "Prepared together for emergencies", "4.4, 7.5", "COM_EMERGENCY"),
    ("p", "In line with our values Safety above all and Care for people and places, ACE prepares nearby communities and local authorities "
          "for how we would respond together in an emergency, and keeps them informed during one (ACE-EMR-STD-001)."),
    ("h2", "Honest communication", "4.4, 1.4", "COM_COMMUNICATION"),
    ("p", "In line with our value Integrity in everything, what ACE says to communities is accurate and timely, including when the news is bad."),

    ("h1", "Accountabilities", "3.1, 4.1"),
    ("t", [("Role", "Named person", "Accountability"),
           ("VP Communications & Corporate Services (policy owner)", "Rodney Garcia", "Owns this policy; reviews escalated grievances."),
           ("Communications Manager (custodian)", "Ricardo Gittens", "Maintains this policy and the grievance register; proposed owner of the grievance and feedback handling process."),
           ("Community Relations Officers", "Reshma Seecharan; Dillon Lovelace", "Stakeholder maps, community meetings, logging and acknowledging grievances."),
           ("Government Affairs Manager", "Kevon Garcia", "Relationships with local authorities, the energy ministry and the environmental regulator."),
           ("Marine Lead", "Sarita Sookram", "Notice to fishing communities before marine activity."),
           ("Area Authorities", "Site Area Authorities", "Act on grievances about their sites.")],
     [3.2, 2.4, 4.4]),

    ("h1", "Decision rights and thresholds", "4.3, 4.2"),
    ("h2", "Grievance times and escalation", "4.3, 4.2", "DR_GRIEVANCE"),
    ("t", [("Stage", "Time", "Who"),
           ("Grievance acknowledged", "Within 5 working days of receipt", "Community Relations Officer"),
           ("Response with the proposed resolution", "Within 30 days of receipt", "Communications Manager, with the Area Authority"),
           ("Escalation if unresolved or the complainant is not satisfied", "Reviewed within a further 30 days", "VP Communications & Corporate Services"),
           ("Grievance alleging injury, damage to property or a breach of law", "Referred the same day", "VP Legal & Government Affairs (General Counsel)")],
     [4, 3, 3]),
    ("h2", "Notice to fishing communities", "4.1, 4.2", "DR_FISHERS_NOTICE"),
    ("p", "Planned marine activity that limits fishing access is notified to the affected fishing communities at least 30 days in advance. "
          "Short-notice activity is notified as soon as it is planned and at least 72 hours in advance, except in an emergency."),

    ("h1", "How we will know", "9.4, 4.3"),
    ("h2", "Headline indicators", "9.4, 4.3", "KNOW_KPIS"),
    ("kpi", "Grievances acknowledged within 5 working days and answered within 30 days. Target: at least 90%."),
    ("kpi", "Repeat grievances: the same issue raised again by the same party within 12 months. Target: zero."),
    ("h2", "Review cycles", "4.1, 4.4", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency"),
           ("Stakeholder map for each site and for marine activity", "Reviewed annually"),
           ("Community liaison meetings at PLB, the CPF and the land leases", "Quarterly"),
           ("Grievance report to the Executive Leadership Team", "Quarterly")],
     [6, 4]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 4.3", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Grievance and feedback handling (new)", "12.5 (proposed)", "Planned")],
     [2.2, 4.6, 1.4, 1.2]),
    ("h2", "Standards and practices that implement this policy", "2.1, 4.1", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-STK-STD-001", "Stakeholder and Community Engagement Standard", "Planned"),
           ("ACE-STK-PRC-001", "Grievance and Feedback Procedure", "Planned"),
           ("ACE-EMR-STD-001", "Emergency, Crisis and Business Continuity Standard (community interfaces, section 7)", "Current")],
     [2.2, 6, 1.2]),
]

ROLES = ["VP Communications & Corporate Services", "Communications Manager", "Community Relations Officer", "Government Affairs Manager",
         "Marine Lead", "VP Legal & Government Affairs (General Counsel)", "Area Authority", "Process Owner"]

SPEC = new_policy("ACE-STK-POL-001", "Stakeholder, Community and Grievance Policy",
                  "How ACE knows, engages and listens to the communities around its sites and in the Gulf of Paria, and answers their grievances on time.",
                  owner="Rodney Garcia", author="Reshma Seecharan",
                  reviewers=["Kevon Garcia", "Sophia Hosany", "Sarita Sookram", "George Habib", "Jenelle Paul"],
                  custodian="Ricardo Gittens", function="Communications & Corporate Services", tags="4.1, 4.3, 4.4", roles=ROLES, body=body)
