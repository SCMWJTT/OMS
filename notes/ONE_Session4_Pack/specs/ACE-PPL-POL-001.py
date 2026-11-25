# ACE-PPL-POL-001 People and Competence Policy (Revision A).
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "3.3, 3.1"),
    ("p", "This policy sets ACE's commitments for recruiting, developing, authorising and managing the people who do ACE's work, so that "
          "every role is clear, every safety-critical task is done by someone proven competent, and OMS duties are part of the job."),
    ("p", "It applies to all ACE employees and secondees at every site, and to contractors where they fill an ACE role or perform a "
          "safety-critical task at an ACE site. Its parent is ACE-LDR-POL-001. Financial delegation is set by ACE-FIN-POL-001; this "
          "policy covers role authority."),

    ("h1", "Our commitments", "3.3, 1.5"),
    values_note(),
    ("h2", "Role profiles carry OMS duties", "1.5, 3.1", "COM_ROLE_PROFILES"),
    ("p", "In line with our value One team, one way, every ACE role has a profile that states its OMS duties and the process steps the role "
          "performs. Because the lanes in ACE process maps are roles, a person can see from their role profile where they act in each "
          "process, and ONE links role pages, process lanes and steps."),
    ("h2", "Proven competent before working alone", "3.3, 8.1", "COM_COMPETENCE"),
    ("p", "In line with our value Safety above all, no one performs a safety-critical role or task unsupervised until they have been "
          "assessed against the role profile and authorised in writing (ACE-PPL-STD-003). This authorisation is a pre-condition check in "
          "permit to work, isolation, offshore travel and other processes."),
    ("req", "No person shall perform a safety-critical task unsupervised unless they hold a current, recorded authorisation for that task."),
    ("h2", "Role authorities are appointed in writing", "3.1, 1.5", "COM_APPOINTMENTS"),
    ("p", "In line with our values One team, one way and Integrity in everything, the OMS role authorities (Area Authority, Technical "
          "Authority, Performing Authority, Isolating Authority and Process Owner) are appointed in writing by the person named in section "
          "4.1, with a defined scope, and the appointment is recorded so that anyone can check who holds it."),
    ("h2", "Process owners trained and lanes briefed", "3.3, 7.3", "COM_PROCESS_TRAINING"),
    ("p", "In line with our value Learn and improve, a new process owner completes process owner training within 60 days of appointment "
          "(C-BPM-040 in ACE-BPM-PRA-003), and the people in each lane of a revised process are briefed before the revision takes effect "
          "(C-BPM-045)."),
    ("h2", "We consult the people who do the work", "3.5, 4.3", "COM_CONSULTATION"),
    ("p", "In line with our values Learn and improve and Care for people and places, ACE consults its workforce and their representatives "
          "on changes to work, procedures and organisation that affect them, and uses what they tell us."),
    ("h2", "Fair recognition and consequence", "8.5, 1.2", "COM_RECOGNITION"),
    ("p", "In line with our values Integrity in everything and Safety above all, ACE recognises people who work safely, speak up and improve "
          "the way we work, and deals fairly and consistently with behaviour that puts people or plant at risk. Honest mistakes reported "
          "openly are treated as chances to learn."),
    ("h2", "Fair recruitment", "3.2, 1.4", "COM_RECRUITMENT"),
    ("p", "In line with our value Integrity in everything, people are recruited and promoted on merit against the role profile, with "
          "credentials verified and conflicts of interest declared, and every new starter is inducted before starting work."),

    ("h1", "Accountabilities", "3.1, 3.3"),
    ("t", [("Role", "Named person", "Accountability"),
           ("VP Human Resources (policy owner)", "Adrian Achong", "Owns this policy and the people system; interim owner of the recruitment and performance management processes."),
           ("Learning & Competence Manager (custodian)", "Andrea Farfan", "Maintains this policy and the competence profile register; proposed owner of the competence assessment and training needs processes."),
           ("Competence Assurance Coordinators", "Damian St. Hill; Savitri Gomes", "Run competence assessments and keep authorisation records."),
           ("Industrial Relations Specialist", "Paul Fernandes", "Coordinates workforce consultation."),
           ("Line managers", "All", "Record authorisations for their teams; set and review performance goals that include OMS duties."),
           ("Function Vice Presidents", "Executive Leadership Team members", "Appoint the role authorities in their function as set in section 4.1.")],
     [3, 2.4, 4.6]),

    ("h1", "Decision rights and thresholds", "3.1, 3.3"),
    ("h2", "Who appoints the role authorities", "3.1, 1.5", "DR_APPOINTMENTS"),
    ("t", [("Role authority", "Appointed by", "Condition"),
           ("Area Authority", "Vice President of the function that controls the location", "Competence assessed for the location; scope and deputy named."),
           ("Technical Authority", "Discipline lead nominated; appointment confirmed by the VP Engineering & Projects", "As set in ACE-ENG-STD-901."),
           ("Performing Authority and Isolating Authority", "Area Authority for the site", "Current competence authorisation under ACE-PPL-STD-003."),
           ("Process Owner", "Vice President of the primary function, recorded in the Process Register by the BPM system owner", "Manager level or above (ACE-BPM-PRA-001 §5); training within 60 days.")],
     [2.6, 4, 3.4]),
    ("h2", "Re-verification of competence", "3.3, 9.1", "DR_REVERIFICATION"),
    ("p", "The re-verification interval for each safety-critical competence is set in its competence profile, according to the risk of the "
          "task and how often it is performed. No interval for a safety-critical competence is longer than three years, and any change to "
          "the equipment, procedure or hazard study for a task triggers reassessment of the people authorised for it."),

    ("h1", "How we will know", "9.4, 3.3"),
    ("h2", "Headline indicators", "9.4, 3.3", "KNOW_KPIS"),
    ("kpi", "People in safety-critical roles with a current authorisation. Target: at least 95% (objective OBJ-26-10), rising to 100%."),
    ("kpi", "Annual training plan completion (TRAIN-COMP). Target: at least 90%."),
    ("kpi", "Time to competence for new starters in safety-critical roles. Target: authorised within six months of starting."),
    ("p", "Linked objective: OBJ-26-10 (competence assurance for safety-critical roles)."),
    ("h2", "Review cycles", "3.3, 3.2", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency"),
           ("Training needs analysis for each function", "Annually, before the training budget is set"),
           ("Performance goals and review, including OMS duties", "Annually, with a mid-year check"),
           ("Re-verification of safety-critical competence", "As set in each competence profile; at least every three years"),
           ("Review of role profiles", "When the role, equipment, process or hazard study changes, and at least every three years")],
     [5.5, 4.5]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 3.3", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Recruitment, screening and induction", "8.1", "Planned"),
           ("—", "Competence assessment and authorisation", "8.2", "Planned"),
           ("—", "Annual training needs analysis", "8.2", "Planned"),
           ("—", "Performance management", "8.3", "Planned")],
     [2.2, 4.6, 1, 1.2]),
    ("p", "Also applies to: every process with a lane role that needs a competence authorisation, including the Permit to Work Process "
          "(ACE-COW-PRS-001) and the Offshore Trip Planning and Manifesting Process (ACE-LOG-PRS-001)."),
    ("h2", "Standards and practices that implement this policy", "2.1, 3.3", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-PPL-STD-003", "Competence Assurance Standard", "Current"),
           ("ACE-PPL-STD-001", "Roles, Accountabilities and Delegated Authority Standard", "Planned"),
           ("ACE-PPL-STD-002", "Workforce Planning and Succession Standard", "Planned"),
           ("ACE-PPL-STD-004", "Workforce Engagement and Consultation Standard", "Planned"),
           ("ACE-LDR-STD-004", "Recognition and Consequence Management Standard", "Planned"),
           ("ACE-OHH-STD-001", "Occupational Health and Fitness for Work Standard", "Planned")],
     [2.2, 6, 1.2]),
]

ROLES = ["VP Human Resources", "Learning & Competence Manager", "Competence Assurance Coordinator", "Industrial Relations Specialist",
         "Line manager", "Vice President", "VP Engineering & Projects", "BPM system owner", "Area Authority", "Technical Authority",
         "Performing Authority", "Isolating Authority", "Process Owner"]

SPEC = new_policy("ACE-PPL-POL-001", "People and Competence Policy",
                  "How ACE makes roles clear, proves competence before people work alone, and builds OMS duties into every job.",
                  owner="Adrian Achong", author="Damian St. Hill",
                  reviewers=["Sophia Hosany", "George Habib", "Gary Ho Sing", "Paul Fernandes", "Richard Ng Wai"],
                  custodian="Andrea Farfan", function="Human Resources", tags="3.3, 3.1, 1.5", roles=ROLES, body=body)
