# ACE-OMS-POL-001 Governance, Assurance and Continuous Improvement Policy (Revision A). The policy for the CI dimension.
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "10.4, 2.1"),
    ("p", "This policy sets how ACE steers and improves its management system: how work is organised into processes, how objectives "
          "are set, how assurance tests that ONE works, and how every improvement is raised, decided, proven and made permanent. It is "
          "the governing policy of the Continuous Improvement (CI) dimension in ONE."),
    ("p", "It applies to every function and site (HOF, PLB, PAP, CHB, SAP, CPF and LND), to every L3 process in the Process Register "
          "(ACE-BPM-REG-001), and to contractors whose work forms part of an ACE process. Its parent is ACE-LDR-POL-001."),

    ("h1", "Our commitments", "10.4, 2.4"),
    values_note(),
    ("h2", "Work is organised as processes", "7.1, 3.1", "COM_PROCESS_APPROACH"),
    ("p", "In line with our value One team, one way, all ACE work is organised as L3 processes, each with exactly one owner, one primary "
          "function and one governing policy. Every corporate objective is carried by at least one process, so that no objective is left "
          "without a way of delivering it (ACE-BPM-PRA-001)."),
    ("h2", "Objectives we can measure", "2.4, 10.2", "COM_OBJECTIVES"),
    ("p", "In line with our values One team, one way and Learn and improve, ACE sets its OMS objectives every year in an annual OMS plan. "
          "Each objective is measurable, has one owner, and is linked to the processes that deliver it and the risks it addresses."),
    ("req", "Each annual objective shall be recorded in the Objectives and Opportunities register (OMS-REG-001) with a target, an owner, "
            "the linked processes and the linked risks before the start of the plan year."),
    ("h2", "Three lines of assurance", "10.1, 9.1", "COM_ASSURANCE"),
    ("p", "In line with our values Integrity in everything and Safety above all, ACE tests whether its controls and processes work in the "
          "field through three lines: checks by the line, conformance assessments by the OMS team, and independent audit by Internal "
          "Audit. The annual assurance plan is risk-based and every one of the ten OMS elements is independently audited at least once "
          "in every three-year period (ACE-PRF-STD-002)."),
    ("h2", "Continuous improvement is a duty", "10.4, 1.8", "COM_CI_DUTY"),
    ("p", "In line with our value Learn and improve, improving how we work is part of every job, not an extra. Every improvement is tied to "
          "the process it improves and, where possible, to the step in that process, so that ONE can show where improvement is happening "
          "and where it is not."),
    ("req", "Every improvement item shall be recorded in the CI register against one L3 process and, where it can be identified, one process step."),
    ("h2", "Sources of improvement", "10.3, 9.3", "COM_CI_SOURCES"),
    ("p", "In line with our values Learn and improve and One team, one way, ACE takes improvements from five sources, and anyone may raise one:"),
    ("bul", "Incident and near-miss actions, from investigations under ACE-INC-STD-001."),
    ("bul", "Audit and assurance findings, from all three lines of assurance."),
    ("bul", "Process reviews: the annual review and trigger reviews of each process."),
    ("bul", "KPI breaches: a process KPI outside its target for two consecutive periods."),
    ("bul", "Staff ideas, which any employee or contractor may raise at any time."),
    ("p", "These five sources are the values of the source field in the CI register."),
    ("h2", "A proportionate method", "10.4, 5.3", "COM_CI_METHOD"),
    ("p", "In line with our value Learn and improve, the effort spent on an improvement matches its size and risk. ACE uses four routes, "
          "which are the values of the method field in the CI register:"),
    ("bul", "Just do it: within one function, low risk, and no change to roles, controls or systems."),
    ("bul", "PDCA (Plan, Do, Check, Act): an improvement led by the process owner within the process."),
    ("bul", "DMAIC (Define, Measure, Analyse, Improve, Control): a data-driven study for a cross-functional problem or a KPI breach."),
    ("bul", "Project: an improvement that needs capital, or a change classed C3 under ACE-MOC-PRC-001."),
    ("p", "The process owner chooses the route and escalates to the BPM system owner when the right route is unclear or the improvement "
          "crosses process boundaries. Section 4 sets who approves each route."),
    ("h2", "Benefit must be shown", "10.4, 9.4", "COM_CI_BENEFIT"),
    ("p", "In line with our values Integrity in everything and Learn and improve, an improvement is judged by evidence, not by opinion. An "
          "item reaches the Verified stage only when a measured KPI has moved against its recorded baseline, or a control has been shown to "
          "work by a test or an assurance check."),
    ("req", "An improvement item shall not be closed until its benefit has been verified against a recorded baseline KPI or a "
            "demonstrated control test."),
    ("h2", "Standardise through control", "5.3, 1.7", "COM_CI_STANDARDISE"),
    ("p", "In line with our value One team, one way, a verified improvement becomes the normal way of working. Changes to wording and step "
          "detail are made by document revision; changes to roles, controls or systems are made through Management of Change (C-BPM-044 "
          "in ACE-BPM-PRA-003). An item reaches the Standardised stage when the revised document or the MOC is approved and the people in "
          "each affected lane have been briefed."),
    ("h2", "Recognition", "8.5, 3.5", "COM_CI_RECOGNITION"),
    ("p", "In line with our values Learn and improve and One team, one way, ACE recognises improvements and the people behind them, "
          "including staff and contractors who raise ideas. Recognition is visible on the ONE improvement board and in leadership "
          "communication, and it is fair and consistent across functions and sites."),
    ("h2", "Process maturity", "10.5, 10.4", "COM_MATURITY"),
    ("p", "In line with our value Learn and improve, ACE processes become more mature over time. Our target is that every Current process "
          "reaches maturity Level 3 (Managed) or above on the scale in ACE-BPM-PRA-003 by the end of 2028."),
    ("h2", "Leadership review of the whole system", "10.5, 1.1", "COM_MANAGEMENT_REVIEW"),
    ("p", "In line with our values One team, one way and Learn and improve, the Executive Leadership Team steps back once a year to ask "
          "whether ONE still works, still suits ACE and is becoming more mature, and sets the improvement priorities for the next annual plan."),

    ("h1", "Accountabilities", "3.1, 10.4"),
    ("t", [("Role", "Named person", "Accountability"),
           ("Chief Executive Officer (policy owner)", "Satesh Sankar", "Owns this policy; chairs the annual management review; approves the annual OMS plan."),
           ("Manager, Strategy & Planning (BPM system owner, custodian)", "Gary Ho Sing", "Owns the process architecture and the CI register; decides escalated CI routes; owner of the BPM processes and of the Improvement Management Process."),
           ("Head of Internal Audit & Risk Assurance", "Nicole Lange", "Owns the independent assurance plan and the three-year element coverage."),
           ("OMS Manager", "Marissa Bobb", "Runs conformance assessments and the annual OMS maturity assessment; prepares the management review."),
           ("Compliance & Assurance Manager", "Dillon Haddad", "Owner of the Audit Planning and Follow-up Process (ACE-PRF-PRS-001); samples process conformance and maturity."),
           ("Learning & Competence Manager", "Andrea Farfan", "Ensures process owners are trained and lane roles are briefed after a change."),
           ("Process owners", "As recorded in ACE-BPM-REG-001", "Own the improvement of their processes; choose the CI route; decide on ideas raised against their process."),
           ("Function Vice Presidents", "Executive Leadership Team members", "Receive quarterly process KPI reports; approve DMAIC studies in their function.")],
     [3.2, 2.3, 4.5]),
    ("resp", "The BPM system owner shall maintain the CI register and report its status to the Executive Leadership Team twice a year."),

    ("h1", "Decision rights and thresholds", "10.4, 2.2"),
    ("h2", "Who approves an improvement", "10.4, 2.2", "DR_CI_APPROVAL"),
    ("t", [("Route", "Who decides to proceed", "Who confirms Verified and Standardised"),
           ("Just do it", "The line manager of the team doing the work, recording it in the CI register", "Process owner"),
           ("PDCA", "Process owner", "Process owner"),
           ("DMAIC", "Process owner, with approval from the Vice President of the primary function for the resources", "Process owner; BPM system owner where more than one function is affected"),
           ("Project", "Approver set by the MOC class (ACE-MOC-PRC-001) and the financial limit (ACE-FIN-POL-001)", "Project sponsor and process owner")],
     [1.6, 4.4, 4]),
    ("p", "If the process owner and the originator disagree about the route, or an item affects more than one process, the BPM system "
          "owner decides."),
    ("h2", "Ideas that are rejected or parked", "3.5, 10.4", "DR_CI_REJECT"),
    ("req", "Only the process owner shall reject or park an improvement item, with the reason recorded in the CI register."),
    ("req", "The originator of an improvement item shall be told the decision and the reason within 30 days of the item being raised."),
    ("p", "A parked item is reviewed again at the next annual review of its process."),

    ("h1", "How we will know", "9.4, 10.2"),
    ("h2", "Headline indicators", "9.4, 10.4", "KNOW_KPIS"),
    ("kpi", "Improvement items closed with verified benefit, as a share of items closed. Target: 100%."),
    ("kpi", "Idea-to-decision time: days from an item being raised to the route or rejection decision. Target: 30 days or fewer for 90% of items."),
    ("kpi", "Share of Current processes at maturity Level 3 or above. Target: 100% by the end of 2028."),
    ("kpi", "Annual process reviews held on time. Target: 100%."),
    ("p", "Linked objective: OBJ-26-08 (launch ONE with the priority documents issued). From 2027 the annual OMS plan carries an objective "
          "for process maturity and CI under this policy."),
    ("h2", "Review cycles", "10.5, 10.1", "KNOW_CYCLES"),
    ("p", "The cycles below are commitments of this policy. The process maps in ONE read them as the cycle view."),
    ("t", [("Cycle", "Frequency", "Who"),
           ("Process review (each L3 process)", "Annually, and within 30 days of a trigger", "Process owner"),
           ("Process KPI report to the Vice President of the primary function", "Quarterly", "Process owner"),
           ("Report on process health and the CI register to the Executive Leadership Team", "Twice a year", "BPM system owner"),
           ("Management review of ONE", "Annually", "Executive Leadership Team, chaired by the Chief Executive Officer"),
           ("OMS maturity self-assessment", "Annually", "OMS Manager; process owners for their processes"),
           ("Annual OMS plan and objectives", "Annually, before the plan year", "Manager, Strategy & Planning"),
           ("Independent audit of all ten OMS elements", "At least once in every three-year period", "Head of Internal Audit & Risk Assurance")],
     [4.5, 3, 2.5]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 10.4", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Objectives and annual OMS plan", "12.1", "Planned"),
           ("—", "Management review", "12.2", "Planned"),
           ("—", "OMS maturity assessment", "12.2", "Planned"),
           ("ACE-PRF-PRS-001", "Audit Planning and Follow-up Process", "12.3", "Planned"),
           ("ACE-BPM-PRS-001", "Process Register Maintenance Process", "12.4", "Planned"),
           ("ACE-BPM-PRS-002", "Process Review and Improvement Process", "12.4", "Planned"),
           ("ACE-BPM-PRS-003", "Improvement Management Process (new)", "12.4", "Planned")],
     [2.2, 4.6, 1, 1.2]),
    ("p", "Also applies to: every L3 process, for its annual review, its KPIs and its improvement items."),
    ("h2", "Standards and practices that implement this policy", "2.1, 10.1", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-BPM-PRA-001", "Business Process Management Practice", "Current"),
           ("ACE-BPM-PRA-002", "Process Modelling and Process File Practice", "Current"),
           ("ACE-BPM-PRA-003", "Process Ownership and Continuous Improvement Practice", "Current"),
           ("ACE-PRF-STD-002", "Assurance and Audit Standard", "Current"),
           ("ACE-PRF-STD-001", "Performance Measurement and KPI Standard", "Planned"),
           ("ACE-PRF-STD-003", "Management Review Standard", "Planned"),
           ("ACE-PRF-STD-004", "OMS Maturity Assessment Standard", "Planned"),
           ("ACE-OMS-STD-001", "OMS Governance Standard", "Planned"),
           ("ACE-OMS-STD-003", "Objectives and Annual OMS Plan Standard", "Planned")],
     [2.2, 6, 1.2]),
]

ROLES = ["Chief Executive Officer", "Executive Leadership Team", "Manager, Strategy & Planning", "BPM system owner",
         "Head of Internal Audit & Risk Assurance", "OMS Manager", "Compliance & Assurance Manager", "Learning & Competence Manager",
         "Process Owner", "Line manager", "Vice President"]

SPEC = new_policy("ACE-OMS-POL-001", "Governance, Assurance and Continuous Improvement Policy",
                  "How ACE organises its work into processes, sets objectives, tests that ONE works and turns every improvement into proven, lasting change.",
                  owner="Satesh Sankar", author="Kwame Henry",
                  reviewers=["Gary Ho Sing", "Marissa Bobb", "Nicole Lange", "Dillon Haddad", "George Habib", "Andrea Farfan"],
                  custodian="Gary Ho Sing", function="CEO Office", tags="10.4, 10.5, 2.4", roles=ROLES, body=body)
