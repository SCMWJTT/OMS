# ACE-LDR-POL-001 OMS Policy, draft of Rev 02 (Revision A).
# Every sentence of the approved Rev 01 is kept (lines marked R01) and moved into the B1 policy skeleton.
# Changes to approved wording: "We shall" -> "ACE shall" (2.3); stop work restyled from RiskControl to Requirement and
# split into its two sentences (2.4); Manual reference updated from Rev 03 to Rev 04 (6.4); effective-date note (6.4).
from specutil import who

DOC = "ACE-LDR-POL-001"
NEW_POLICIES = [
    ("ACE-OMS-POL-001", "Governance, Assurance and Continuous Improvement Policy", "Satesh Sankar"),
    ("ACE-RSK-POL-001", "Operational Risk Management Policy", "George Habib"),
    ("ACE-CON-POL-001", "Supply Chain, Logistics and Local Content Policy", "Sasha George"),
    ("ACE-PPL-POL-001", "People and Competence Policy", "Adrian Achong"),
    ("ACE-HMA-POL-001", "Hydrocarbon Measurement, Product Quality and Commercial Policy", "Karen Jack"),
    ("ACE-FIN-POL-001", "Financial Control and Delegation of Authority Policy", "Teresa Daniel"),
    ("ACE-LDR-POL-002", "Code of Conduct and Business Ethics Policy", "Sharda Bissoon"),
    ("ACE-ENV-POL-001", "Environment Policy", "George Habib"),
    ("ACE-SEC-POL-001", "Security Policy", "George Habib"),
    ("ACE-STK-POL-001", "Stakeholder, Community and Grievance Policy", "Rodney Garcia"),
]

body = [
    # ------------------------------------------------------------------ 1
    ("h1", "Purpose, vision, values and scope", "1.1, 2.1, 1.2"),
    ("p", "ACE operates one integrated management system for health, safety, environment, operating integrity and business performance. "
          "ONE sets the common expectations; accountable leaders provide the people, standards and resources necessary to meet them. "
          "We measure our performance through the health of our controls as well as our results."),  # R01
    ("p", "This policy states why ACE exists, what it aims to become and the values that guide how we work. It is the top of the ACE "
          "golden thread: every other ACE policy names the values below in its commitments, and every process traces to a policy."),
    ("h2", "Our mission and vision", "1.1, 1.2", "MISSION_VISION"),
    ("p", "Our mission: to produce oil and gas from Trinidad and Tobago's land and the Gulf of Paria safely, reliably and responsibly, "
          "creating lasting value for the country, our partners and our people."),
    ("p", "Our vision: to be the most trusted and best-run independent energy operator in the Caribbean."),
    ("h2", "Value: Safety above all", "1.2, 5.1", "VAL_SAFETY"),
    ("p", "No production, schedule or cost target justifies putting people or essential barriers at risk. In practice this means we stop "
          "work when a risk is not controlled, keep safety-critical equipment working and never knowingly exceed a safe operating limit."),
    ("h2", "Value: Integrity in everything", "1.4, 1.3", "VAL_INTEGRITY"),
    ("p", "We are honest, do what we say and follow the rules when no one is watching. In practice this means accurate reports and "
          "records, conflicts of interest declared, approvals given only within authority, and problems reported rather than hidden."),
    ("h2", "Value: Care for people and places", "4.1, 2.3", "VAL_CARE"),
    ("p", "We look after our workforce, our neighbours and the environment we share, on land and in the Gulf of Paria. In practice this "
          "means preventing pollution, minimising flaring, listening to communities and fishers, and answering their concerns."),
    ("h2", "Value: One team, one way", "1.1, 2.1", "VAL_ONE_TEAM"),
    ("p", "Staff, contractors and partners work to one management system and one set of rules at every site. In practice this means one "
          "risk matrix, one document hierarchy, one way of controlling work, clear roles, and processes that each have a single owner."),
    ("h2", "Value: Learn and improve", "1.8, 10.4", "VAL_LEARN"),
    ("p", "We learn from every incident, audit, idea and result, and turn lessons into lasting change. In practice this means reporting "
          "openly, closing actions with evidence that they worked, and improving processes and standards by revision and Management of Change."),
    ("h2", "Scope and applicability", "1.1, 1.3", "SCOPE"),
    ("p", "This policy applies to every ACE activity: offshore production in the Gulf of Paria, the Central Processing Facility, land leases, "
          "wells, pipelines, marine and shore-base services, and work delivered by contractors on our behalf. No production, schedule or "
          "commercial objective takes priority over protecting people or maintaining essential barriers."),  # R01
    ("p", "It covers all sites (HOF, PLB, PAP, CHB, SAP, CPF and LND), all functions, and every employee and contractor. The other ACE "
          "policies listed in section 6.3 sit under this policy and apply its values to their own subjects."),

    # ------------------------------------------------------------------ 2
    ("h1", "Our commitments", "2.1, 1.1"),
    ("p", "Each commitment below is an outcome ACE commits to, and names the values it serves. The steps that deliver it are in the "
          "governed processes and the implementing documents in section 6."),
    ("h2", "Leadership ownership", "1.1, 1.5", "COM_LEADERSHIP"),
    ("p", "In line with our values One team, one way and Integrity in everything, our leaders own ONE and are seen to lead it."),
    ("req", "The Chief Executive Officer shall own ONE, set the company direction and require each Executive Leadership Team member to "
            "demonstrate accountability for the controls in their area."),  # R01
    ("req", "Every system and OMS element shall have an accountable owner, an approved set of requirements and a means of verifying "
            "implementation."),  # R01
    ("resp", "Vice Presidents and managers provide visible leadership, evaluate risk and act on concerns raised by employees, contractors "
             "and neighbours."),  # R01
    ("p", "We lead by visiting the work, listening to the people who do it, checking the condition of critical barriers and correcting what "
          "is not working. Silence or an absence of reported problems is not evidence that risk is controlled."),  # R01
    ("h2", "One consistent system", "1.1, 2.1", "COM_ONE_SYSTEM"),
    ("p", "In line with our value One team, one way, ACE runs its business through one system, not through separate programmes."),
    ("req", "ACE activities shall be governed through ONE rather than disconnected HSE, integrity, maintenance or quality programmes."),  # R01
    ("req", "System owners shall use the common ACE Risk Matrix, the approved document hierarchy and the ONE reporting and assurance "
            "arrangements."),  # R01
    ("note", "A policy sets direction; standards describe requirements; procedures and work instructions describe how a job is performed. "
             "The current approved source is the ONE document repository."),  # R01
    ("h2", "Protect people and prevent serious harm", "5.1, 1.2", "COM_PROTECT_PEOPLE"),
    ("p", "In line with our value Safety above all, hazards are understood and controlled before work starts."),
    ("req", "ACE shall identify hazards before work, assess credible consequences, select effective prevention and recovery barriers, and "
            "verify that those barriers are available."),  # R01 ("We shall" -> "ACE shall")
    ("req", "Work involving major accident hazards shall be supported by appropriate hazard studies, competent personnel, operating limits "
            "and effective emergency arrangements."),  # R01
    ("h2", "Stop work", "8.4, 1.2", "COM_STOP_WORK"),
    ("p", "In line with our values Safety above all and Integrity in everything, anyone at ACE can stop work that is not safe, and is "
          "supported for doing so. The control that delivers this is in the Control of Work Standard (ACE-COW-STD-001)."),
    ("req", "Everyone has authority and a duty to stop or suspend work when conditions cannot be made safe."),  # R01 (was RiskControl)
    ("req", "Stopped work restarts only after the hazards are controlled and the responsible Area Authority releases it."),  # R01
    ("req", "Anyone who identifies an uncontrolled hazard or a failed critical barrier shall stop the affected work, make the situation "
            "safe where competent to do so, and inform the supervisor or Area Authority."),  # R01 (from 3.1)
    ("p", "We encourage reporting and professional challenge. No one is expected to continue a job solely because a schedule, budget or "
          "superior demands it."),  # R01 (from 2.4)
    ("h2", "Plan, permit, supervise and hand back work", "8.2, 8.1, 8.3", "COM_CONTROL_OF_WORK"),
    ("p", "In line with our values Safety above all and One team, one way, work is done the same controlled way by staff and contractors "
          "at every site."),
    ("req", "ACE shall assign critical tasks to competent people, communicate current procedures and ensure that work is planned, "
            "permitted, supervised and handed back safely."),  # R01
    ("req", "All employees and contractors shall follow the current approved requirements relevant to their role, attend required "
            "inductions, and act within their competence and authorization."),  # R01 (from 3.1)
    ("warn", "Do not bypass a safeguard or improvise around a mandatory procedure. Escalate the conflict and obtain an approved solution "
             "before proceeding."),  # R01 (from 3.1)
    ("h2", "Operate within limits", "6.3, 5.4", "COM_OPERATING_LIMITS"),
    ("p", "In line with our value Safety above all, every ACE system is operated within its approved operating envelope. Operating limits "
          "are set, known by the people who run the plant, and changed only through Management of Change."),
    ("p", "Excursions beyond operating limits are reported, assessed for their effect on safety-critical equipment and major accident "
          "barriers, and corrected. A safe operating limit is never knowingly exceeded to meet a production or sales target "
          "(ACE-OPS-STD-001)."),
    ("h2", "Maintain the integrity and reliability of assets", "6.4, 6.5", "COM_ASSET_INTEGRITY"),
    ("p", "In line with our values Safety above all and One team, one way, our assets are kept fit for purpose for their whole life, and "
          "the equipment that prevents or limits a major accident is known, owned and proven to work."),
    ("req", "Safety-critical elements shall have defined performance standards, ownership and planned inspection, maintenance and "
            "testing."),  # R01
    ("req", "Known impairments, overdue safety-critical tasks and changes affecting technical integrity shall be risk-assessed, escalated "
            "and managed using the approved deviation and management-of-change arrangements."),  # R01
    ("p", "An overdue or impaired safety-critical element is never deferred silently: it is either restored on time or held under an "
          "approved, time-limited deviation with compensating measures (ACE-OMS-STD-002)."),
    ("p", "ACE manages wells, platforms, subsea and land pipelines, the CPF, tank farm and jetty on a life-cycle basis; reliability and "
          "safe operation are treated as connected outcomes."),  # R01
    ("h2", "Independent technical authority", "3.1, 6.2", "COM_TECHNICAL_AUTHORITY"),
    ("p", "In line with our values Safety above all and Integrity in everything, each engineering discipline has an appointed Technical "
          "Authority who owns its technical standards and endorses designs, changes and deviations."),
    ("p", "Technical Authorities are appointed in writing, are competent for their discipline, and give their technical judgement "
          "independently of production, schedule or cost pressure. Their endorsement cannot be replaced by a line manager's approval "
          "(ACE-ENG-STD-901)."),
    ("h2", "Meet legal, environmental and stakeholder obligations", "2.3, 4.2", "COM_OBLIGATIONS"),
    ("p", "In line with our values Integrity in everything and Care for people and places, ACE knows its obligations and meets them."),
    ("req", "ACE shall identify and comply with applicable laws, licence conditions, permits, contractual obligations and adopted "
            "engineering and industry standards."),  # R01
    ("req", "Operations shall prevent pollution where practicable, control emissions, discharges, spills and waste, and respond promptly "
            "to events that affect communities or the environment."),  # R01
    ("resp", "Legal & Government Affairs supports interpretation and monitoring of obligations; operational owners remain accountable for "
             "their implementation."),  # R01
    ("p", "We will engage respectfully with communities and customers, respond to material concerns, and protect the quality of our sales "
          "gas and crude."),  # R01
    ("h2", "Report and learn", "9.2, 9.3", "COM_REPORT_LEARN"),
    ("p", "In line with our value Learn and improve, events and concerns are reported openly and used to make our barriers and methods "
          "better. How improvement is managed is set by ACE-OMS-POL-001."),
    ("req", "Incidents, near misses, equipment anomalies, deviations and concerns shall be reported accurately and used to improve barriers "
            "and methods."),  # R01
    ("req", "People shall promptly report incidents and near misses, cooperate with investigations and raise concerns about procedures "
            "that cannot be followed as written."),  # R01 (from 3.1)

    # ------------------------------------------------------------------ 3
    ("h1", "Accountabilities", "3.1, 1.5"),
    ("p", "The table names the policy owner and the owners of the processes this policy governs. Process owners are as recorded in the "
          "Process Register (ACE-BPM-REG-001)."),
    ("t", [("Role", "Named person", "Accountability"),
           ("Chief Executive Officer (policy owner)", "Satesh Sankar", "Owns this policy and ONE; approves Level 1 policies; leads the Executive Leadership Team in acting on OMS performance."),
           ("OMS Manager (custodian)", "Marissa Bobb", "Maintains this policy and coordinates conformance evidence against it."),
           ("VP Operations", "Sophia Hosany", "Accountable for safe operation within limits, control of work and maintenance delivery at all producing sites."),
           ("VP Engineering & Projects", "Dev Jaggernauth", "Sponsors the Technical Authority framework and confirms Technical Authority appointments."),
           ("VP Wells", "Joanne Ho Sing", "Accountable for well integrity from design to abandonment."),
           ("VP Legal & Government Affairs (General Counsel)", "Sharda Bissoon", "Interprets legal and licence obligations and owns legal and regulatory obligation tracking."),
           ("Process owner, ACE-COW-PRS-001", "Arjun Gittens", "Permit to Work Process: design, performance and improvement."),
           ("Process owner, ACE-OPS-PRS-001", "Michelle de Verteuil", "Operating Limit Management Process."),
           ("Process owner, ACE-AIM-PRS-001 and ACE-AIM-PRS-002", "Wayne Rajkumar", "Inspection Planning and Execution Process; Anomaly Management Process."),
           ("Process owner, ACE-MNT-PRS-001", "Sunita Seepersad", "Maintenance Planning and Scheduling Process."),
           ("Process owner, ACE-ENG-PRS-410", "Vijay Ramcharan", "SIS Safety Lifecycle Process."),
           ("Process owner, ACE-WEL-PRS-001 and ACE-WEL-PRS-002", "Shalini Jaggernauth", "Well Handover Process; Annulus Pressure Management Process.")],
     [3, 2, 5]),
    ("resp", "Line managers provide competent teams, time for proper planning, supervision, training and feedback."),  # R01
    ("resp", "Area Authorities control activity at their locations, coordinate simultaneous work and confirm the condition of plant before "
             "release or restart."),  # R01
    ("resp", "Technical Authorities define and assure technical requirements, assess proposed changes and deviations, and challenge "
             "decisions that could weaken critical barriers."),  # R01

    # ------------------------------------------------------------------ 4
    ("h1", "Decision rights and thresholds", "2.6, 3.1"),
    ("p", "This policy sets no financial or risk-band thresholds of its own. Risk acceptance, deviation periods and change classes are set "
          "by ACE-RSK-POL-001; financial limits are set by ACE-FIN-POL-001. The decision rights below are fixed by this policy."),
    ("t", [("Decision", "Who decides", "Condition"),
           ("Restart of stopped work", "Area Authority for the location", "Hazards controlled; actual conditions and any compensating measures recorded."),
           ("Technical acceptability of a design, change or deviation", "Technical Authority for the discipline", "Independent of line management; cannot be replaced by a line approval."),
           ("Operating with an impaired or overdue safety-critical element", "Approver set by ACE-OMS-STD-002 for the risk band", "Only under an approved, time-limited deviation; never by silent deferral.")],
     [3, 3, 4]),
    ("appr", "An approval to operate with a deviation shall never replace a legal permit or authorize action outside an absolute safety "
             "limit."),  # R01

    # ------------------------------------------------------------------ 5
    ("h1", "How we will know", "9.4, 10.5"),
    ("h2", "Objectives and transparent performance", "9.4, 2.4", "KNOW_OBJECTIVES"),
    ("req", "Every OMS objective shall have a measurable target, an accountable owner, a review date and an evidence source."),  # R01
    ("req", "Performance reporting shall include leading indicators for barrier health, overdue corrective actions, competence and "
            "control-of-work verification, alongside incidents, losses and environmental outcomes."),  # R01
    ("kpi", "Tier 1 and Tier 2 process safety events. Target: zero Tier 1 and no more than two Tier 2 per year (objective OBJ-26-02)."),
    ("kpi", "Safety-critical element inspections and tests completed on time. Target: 100% (objectives OBJ-26-03 and OBJ-26-06)."),
    ("kpi", "Safety-critical element deviations past their expiry date. Target: zero at any time."),
    ("kpi", "Measures include safety-critical maintenance compliance; impairments overdue; high-risk actions overdue; incident "
            "investigation closure and effectiveness; legal compliance status; and corrective actions verified effective."),  # R01
    ("p", "Objective IDs are those in the Objectives and Opportunities register (OMS-REG-001). They are renewed each year in the annual OMS "
          "plan under ACE-OMS-POL-001; the headline indicators above stay the same."),
    ("h2", "Assurance, review and continual improvement", "10.1, 10.5", "KNOW_REVIEW"),
    ("p", "This policy has no review cycles of its own beyond those below. The arrangements for assurance, management review, process "
          "review and continuous improvement, and their frequencies, are set by ACE-OMS-POL-001."),
    ("req", "ACE shall conduct planned self-checks, independent assurance and management review to test whether ONE requirements work in "
            "the field."),  # R01
    ("req", "The Executive Leadership Team shall review management-system performance at least annually and commission improvements where "
            "results or evidence indicate weaknesses."),  # R01
    ("req", "The Chief Executive Officer shall review and re-approve this policy at least every three years, or sooner following a "
            "material change to ACE's operations, risk profile or obligations."),  # R01
    ("resp", "The OMS Manager maintains the policy and coordinates conformance evidence; the CEO and ELT act on review outcomes."),  # R01

    # ------------------------------------------------------------------ 6
    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 2.1", "GOVERNED_PROCESSES"),
    ("p", "This policy is the governing policy of the L3 processes below. Numbers are given where the process is in the Process Register; "
          "the others are candidates from the process inventory. The L1 1 Explore & Develop processes are governed here for now, until a "
          "reserves and resources policy is written. As the OMS Policy, this policy also applies to every other ACE process."),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Reserves estimation (interim)", "1.2", "Planned"),
           ("—", "Field development planning (interim)", "1.3", "Planned"),
           ("—", "Well construction verification", "2.2", "Planned"),
           ("—", "Well intervention and abandonment", "2.3, 2.5", "Planned"),
           ("ACE-WEL-PRS-001", "Well Handover Process", "2.4", "Planned"),
           ("ACE-WEL-PRS-002", "Annulus Pressure Management Process", "2.4", "Planned"),
           ("—", "Well integrity anomaly management", "2.4", "Planned"),
           ("—", "Production planning", "3.1", "Planned"),
           ("ACE-OPS-PRS-001", "Operating Limit Management Process", "3.3", "Planned"),
           ("—", "Override and inhibit management", "3.3", "Planned"),
           ("ACE-COW-PRS-001", "Permit to Work Process", "3.4", "Planned"),
           ("—", "Isolation and reinstatement", "3.4", "Planned"),
           ("—", "Operational readiness and start-up", "3.5", "Planned"),
           ("—", "Maintenance strategy", "4.1", "Planned"),
           ("ACE-MNT-PRS-001", "Maintenance Planning and Scheduling Process", "4.1", "Planned"),
           ("ACE-AIM-PRS-001", "Inspection Planning and Execution Process", "4.2", "Planned"),
           ("—", "Corrosion monitoring", "4.2", "Planned"),
           ("—", "SCE performance verification", "4.3", "Planned"),
           ("ACE-ENG-PRS-410", "SIS Safety Lifecycle Process", "4.3", "Planned"),
           ("ACE-AIM-PRS-002", "Anomaly Management Process", "4.4", "Planned"),
           ("—", "Technical Authority appointment", "12.2", "Planned"),
           ("—", "Legal and regulatory obligation tracking", "12.2", "Planned")],
     [2.2, 4.6, 1, 1.2]),
    ("h2", "Standards and practices that implement this policy", "2.1, 6.2", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-AIM-STD-001", "Asset Integrity Management Standard", "Current"),
           ("ACE-AIM-STD-002", "Inspection Management Standard", "Current"),
           ("ACE-AIM-PRA-001", "Risk-Based Inspection and Corrosion Management Practice (under ACE-AIM-STD-001)", "Current"),
           ("ACE-COW-STD-001", "Control of Work Standard", "Current"),
           ("ACE-ENG-STD-901", "Engineering Standards Framework and Technical Authority Standard", "Current"),
           ("ACE-ENG-SPC-410", "Safety Instrumented Systems Specification", "Current"),
           ("ACE-MNT-STD-001", "Maintenance Management Standard", "Current"),
           ("ACE-MNT-PRA-001", "Equipment Criticality and SCE Maintenance Practice (under ACE-MNT-STD-001)", "Current"),
           ("ACE-OPS-STD-001", "Operating Envelopes and Operating Limits Standard", "Current"),
           ("ACE-OPS-PRA-001", "Operating Envelopes and Integrity Operating Windows Practice (under ACE-OPS-STD-001)", "Current"),
           ("ACE-WEL-STD-001", "Well Integrity Management Standard", "Current"),
           ("ACE-WEL-PRA-001", "Well Barriers and Well Handover Practice (under ACE-WEL-STD-001)", "Current"),
           ("ACE-LDR-STD-003", "Stop Work Authority Standard", "Planned"),
           ("ACE-LEG-STD-001", "Legal and Other Requirements Standard", "Planned"),
           ("ACE-OPS-STD-002", "Operating Procedures Standard", "Planned"),
           ("ACE-OPS-STD-003", "Operational Readiness, Start-up and Handover Standard", "Planned"),
           ("ACE-OPS-STD-004", "Supervision and Verification of Work Standard", "Planned"),
           ("ACE-AIM-REG-001", "Safety-Critical Element Register and Performance Standards", "Planned")],
     [2.2, 6, 1.2]),
    ("h2", "Policies under this policy", "2.1, 2.2", "CHILD_POLICIES"),
    ("p", "Each of these policies names this policy as its parent and links its commitments to the values in section 1."),
    ("t", [("Number", "Title", "Owner", "Status"),
           ("ACE-DOC-POL-001", "Document and Records Management Policy", "Marvin Williams", "Current")]
          + [(n, t, o, "Planned (draft)") for n, t, o in NEW_POLICIES],
     [2.2, 4.6, 2, 1.4]),
    ("h2", "Controlled references", "1.7, 7.4", "REFERENCES"),
    ("ref", "ACE-OMS-MAN-001 — One Management System Manual, Revision 04."),  # R01 (Revision 03 -> 04)
    ("ref", "ACE-DOC-STD-001 — Document and Records Management Standard."),  # R01
    ("ref", "ACE-DOC-STD-002 — Operational Document Publishing Standard."),  # R01
    ("ref", "ACE-RSK-STD-001 — Risk Management Standard."),  # R01
    ("ref", "ACE-AIM-STD-001 — Asset Integrity Management Standard."),  # R01
    ("ref", "ACE-MOC-PRC-001 — Management of Change Procedure."),  # R01
    ("ref", "ACE-COW-STD-001 — Control of Work Standard."),  # R01
    ("ref", "ACE-PRF-STD-002 — Assurance and Audit Standard."),  # R01
    ("note", "This policy takes effect on its effective date and remains in force until superseded or withdrawn by an approved revision. "
             "Revision 01 took effect on 1 January 2026."),  # R01 (date wording)
]

ROLES = ["Chief Executive Officer", "Executive Leadership Team", "OMS Manager", "VP Operations", "VP Engineering & Projects", "VP Wells",
         "VP Legal & Government Affairs (General Counsel)", "Offshore Operations Manager (Gulf of Paria)", "Process Engineering Lead",
         "Inspection Lead", "Maintenance Superintendent", "Instrumentation & Control Lead", "Well Integrity Lead", "Process Owner",
         "Line manager", "Area Authority", "Technical Authority", "System owner"]

SPEC = dict(
    meta=dict(DocumentId=DOC, Title="OMS Policy — Health, Safety, Environment and Operating Integrity", DocumentType="Policy", Level="1",
              Revision="A", Status="In Review", IssueDate="", EffectiveDate="",
              Author=who("Marissa Bobb"),
              Reviewer="; ".join(who(n) for n in ["George Habib", "Sharda Bissoon", "Sophia Hosany", "Dev Jaggernauth", "Nicole Lange"]),
              Endorser="Executive Leadership Team", Approver=who("Satesh Sankar"), DocumentOwner=who("Satesh Sankar"),
              ProcessOwner="Not applicable", Custodian=who("Marissa Bobb"), PrimaryFunction="CEO Office",
              TitleOMSTags="1.1, 2.1, 1.2", Classification="Internal",
              Applicability="All ACE activities, assets, sites, employees and contractors",
              ReviewInterval="Three years; earlier if triggered", RoleRegister="; ".join(ROLES), Parent="Not applicable"),
    label="ACE  /  LEVEL 1 POLICY  /  DRAFT FOR REVIEW",
    subtitle="ACE's mission, vision and values, and the leadership commitments for safe, responsible and reliable operations across ACE.",
    cover_note="Proposed effective date 1 January 2027",
    history=[("01", "1 January 2026", "First approved issue; establishes requirements for ONE and all ACE sites."),
             ("A", "", "Draft for Rev 02: adds mission, vision and values; restructures into the ACE policy skeleton; expands asset integrity "
                       "and Technical Authority commitments; adds stop work and operating limits as separate commitments; adds governed "
                       "processes and implementing documents. Proposed effective date 1 January 2027.")],
    file="ACE-LDR-POL-001_OMS_Policy_RevA.docx",
    processes=None, body=body, controls=None)
