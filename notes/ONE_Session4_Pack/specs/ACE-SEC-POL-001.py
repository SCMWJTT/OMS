# ACE-SEC-POL-001 Security Policy (physical and cyber) (Revision A).
# Owner decision (Wilmark, Session 4): VP HSE & Compliance; OT cyber with the Telecoms & OT Cyber Security Lead; IT with the VP IT, Data & Knowledge.
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "5.1, 7.5"),
    ("p", "This policy sets ACE's commitments for protecting its people, sites, control and safety systems, and information against "
          "deliberate harm: theft, intrusion, sabotage and cyber attack. It covers physical security, information technology (IT) "
          "security and operational technology (OT) security, the control and safety systems that run the plant."),
    ("p", "It applies to all ACE sites, with particular attention to the Point Lisas Shore Base (PLB) port facility and the offshore "
          "installations, to every ACE information and control system, and to every employee, contractor and visitor. Its parent is "
          "ACE-LDR-POL-001."),

    ("h1", "Our commitments", "5.1, 7.5"),
    values_note(),
    ("h2", "Access by need and authorised role", "5.1, 3.1", "COM_ACCESS"),
    ("p", "In line with our values Safety above all and Integrity in everything, access to ACE sites, systems and information is given only "
          "to people who need it for an authorised role, only for as long as they need it, and is removed promptly when they no longer do."),
    ("req", "Access to ACE sites, systems and information shall be granted only for an authorised role and shall be removed within one "
            "working day of the role ending."),
    ("h2", "Control and safety systems are protected", "5.3, 6.4", "COM_OT"),
    ("p", "In line with our value Safety above all, every change to a control or safety system, including software, configuration and "
          "network connections, goes through Management of Change. There is no standing remote access to OT: each remote session is "
          "approved, time-limited and logged."),
    ("req", "No change shall be made to a control or safety system, its software, its configuration or its network connections without an "
            "approved Management of Change."),
    ("h2", "Security incidents are reported", "9.2, 7.5", "COM_INCIDENTS"),
    ("p", "In line with our values Integrity in everything and Learn and improve, every security incident or suspected incident, physical or "
          "cyber, is reported straight away and handled through the incident system (ACE-INC-STD-001). One that affects a control or safety "
          "system is also treated as a process safety matter."),
    ("h2", "Port and marine security at Point Lisas", "7.5, 4.4", "COM_PORT"),
    ("p", "In line with our values Safety above all and One team, one way, the Point Lisas Shore Base meets the port facility security "
          "requirements that apply to it: controlled entry for people, vehicles and cargo, screening, a security plan agreed with the port "
          "authorities, and coordination with vessels calling at the base."),
    ("h2", "Security risk is assessed and planned for", "5.1, 7.5", "COM_RISK"),
    ("p", "In line with our value Safety above all, ACE assesses security threats to each site and system every year using the ACE Risk "
          "Matrix, and its emergency plans cover security events and cyber attacks on control systems."),

    ("h1", "Accountabilities", "3.1, 5.1"),
    ("t", [("Role", "Named person", "Accountability"),
           ("VP HSE & Compliance (policy owner)", "George Habib", "Owns this policy and the security system as a whole."),
           ("Telecoms & OT Cyber Security Lead", "Kevin Mohammed", "Accountable for OT cyber security: control and safety system networks, remote access to OT and OT security incidents."),
           ("VP IT, Data & Knowledge", "Marvin Williams", "Accountable for IT systems security: corporate networks, identities, applications and information."),
           ("Emergency Response & Security Manager (custodian)", "Jenelle Paul", "Maintains this policy; accountable for physical security and the PLB port facility security plan; proposed owner of site and port access control."),
           ("IT Infrastructure & Operations Manager", "Imran Singh", "Proposed owner of the access management process for IT systems."),
           ("Security Coordinator", "Dillon Granger", "Runs site security operations and access passes."),
           ("Area Authorities", "Site Area Authorities", "Control physical access to their locations.")],
     [3.2, 2.2, 4.6]),

    ("h1", "Decision rights and thresholds", "5.1, 3.1"),
    ("t", [("Decision", "Who decides", "Condition"),
           ("Remote access session to an OT system", "Telecoms & OT Cyber Security Lead, with the Area Authority's agreement", "Named person, defined task, time-limited to the task, logged; no standing access."),
           ("Privileged access to an IT system", "VP IT, Data & Knowledge or delegate", "Named person, reviewed quarterly."),
           ("Access to a site", "Area Authority for the location", "Authorised role, induction complete, visitor escorted."),
           ("Escalation of a security incident", "Person discovering it reports at once", "Any incident affecting a control or safety system goes to the Telecoms & OT Cyber Security Lead and the Area Authority at once, and to emergency response Level 2 if control of the plant is affected.")],
     [3, 3, 4]),

    ("h1", "How we will know", "9.4, 5.1"),
    ("h2", "Headline indicators", "9.4, 5.1", "KNOW_KPIS"),
    ("kpi", "Access reviews completed on time. Target: 100%."),
    ("kpi", "Leavers' access removed within one working day. Target: 100%."),
    ("kpi", "Security incidents, physical and cyber, by severity. Target: zero incidents affecting a control or safety system."),
    ("h2", "Review cycles", "5.1, 7.5", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency"),
           ("Review of access to sites, IT systems and OT systems", "Quarterly"),
           ("Security risk assessment for each site and system", "Annually"),
           ("Exercise of a security or cyber scenario within the emergency programme", "Annually")],
     [6, 4]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 5.1", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Access management", "11.2", "Planned"),
           ("—", "Site and port access control (new)", "6.2 / 11.2", "Planned")],
     [2.2, 4.6, 1.4, 1.2]),
    ("p", "Also applies to: the SIS Safety Lifecycle Process (ACE-ENG-PRS-410) and the Management of Change Process (ACE-MOC-PRS-001), "
          "for changes to control and safety systems."),
    ("h2", "Standards and practices that implement this policy", "2.1, 5.1", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-SEC-STD-001", "Security Management Standard", "Planned"),
           ("ACE-ENG-SPC-410", "Safety Instrumented Systems Specification (security of safety systems)", "Current")],
     [2.2, 6, 1.2]),
]

ROLES = ["VP HSE & Compliance", "Telecoms & OT Cyber Security Lead", "VP IT, Data & Knowledge", "Emergency Response & Security Manager",
         "IT Infrastructure & Operations Manager", "Security Coordinator", "Area Authority", "Process Owner"]

SPEC = new_policy("ACE-SEC-POL-001", "Security Policy",
                  "How ACE protects its people, sites, control and safety systems, and information against deliberate harm, physical and cyber.",
                  owner="George Habib", author="Dillon Granger",
                  reviewers=["Marvin Williams", "Kevin Mohammed", "Imran Singh", "Lisa Williams", "Sophia Hosany"],
                  custodian="Jenelle Paul", function="HSE & Compliance", tags="5.1, 7.5", roles=ROLES, body=body)
