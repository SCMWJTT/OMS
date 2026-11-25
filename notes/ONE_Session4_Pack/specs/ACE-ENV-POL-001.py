# ACE-ENV-POL-001 Environment Policy (Revision A).
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "2.3, 5.1"),
    ("p", "This policy sets ACE's commitments for protecting the environment it works in: complying with its permits, cutting flaring and "
          "venting, preventing spills, managing waste and discharges, and reporting its environmental performance openly."),
    ("p", "It applies to all ACE sites and activities, on land and in the Gulf of Paria, including drilling, production, the CPF, the "
          "export jetty, marine and road transport, and contractors working for ACE. Its parent is ACE-LDR-POL-001."),

    ("h1", "Our commitments", "2.3, 5.1"),
    values_note(),
    ("h2", "Comply with permits and licence conditions", "2.3, 1.3", "COM_PERMITS"),
    ("p", "In line with our values Integrity in everything and Care for people and places, ACE meets every condition of the permits and "
          "licences issued by the environmental regulator and the energy ministry. Each permit condition has an owner and is monitored, "
          "and an exceedance is reported to the regulator as the permit requires."),
    ("h2", "Minimise flaring and venting", "2.3, 6.3", "COM_FLARING"),
    ("p", "In line with our value Care for people and places, ACE will end routine flaring by the end of 2030. Until then, routine flared "
          "volume falls by at least 15% a year against the 2025 baseline. Gas is not vented except where needed for safety. Flaring limits "
          "are part of the operating envelope (ACE-OPS-STD-001)."),
    ("h2", "Prevent spills and respond by tier", "5.1, 7.5", "COM_SPILLS"),
    ("p", "In line with our values Safety above all and Care for people and places, ACE prevents loss of containment through its integrity "
          "and operating commitments, and when a spill happens responds at the tier in section 4.1, using the capability tiers of the "
          "oil spill plans (ACE-EMR-STD-001 §5)."),
    ("h2", "Manage waste and discharges", "2.3, 5.1", "COM_WASTE"),
    ("p", "In line with our value Care for people and places, waste is managed by the hierarchy of avoid, reduce, reuse, recycle, then safe "
          "disposal through licensed contractors, and every discharge to air, water or land stays within its permitted limits."),
    ("h2", "Report environmental performance", "9.1, 9.4", "COM_REPORTING"),
    ("p", "In line with our values Integrity in everything and Learn and improve, ACE measures its emissions, discharges, spills and waste, "
          "reports them at the frequencies in section 5.2, and uses the results to set its environmental objectives."),

    ("h1", "Accountabilities", "3.1, 2.3"),
    ("t", [("Role", "Named person", "Accountability"),
           ("VP HSE & Compliance (policy owner)", "George Habib", "Owns this policy and the environmental management system."),
           ("Environmental Lead (custodian)", "Kevin Lutchman", "Maintains this policy and the permit register; proposed owner of the emissions, discharges and waste monitoring and reporting process."),
           ("Plant Manager - Central Processing Facility", "Rohan Ali", "Flaring performance and discharges at the CPF."),
           ("Offshore Operations Manager (Gulf of Paria)", "Arjun Gittens", "Flaring, venting and discharges offshore."),
           ("Emergency Response & Security Manager", "Jenelle Paul", "Oil spill contingency plans and spill response readiness."),
           ("Counsel, Regulatory & Licensing", "Rawle Sandy", "Interprets permit and licence conditions with the environmental regulator.")],
     [3.2, 2.2, 4.6]),

    ("h1", "Decision rights and thresholds", "5.1, 7.5"),
    ("h2", "Spill tiers", "7.5, 5.1", "DR_SPILL_TIERS"),
    ("p", "The tier sets the response branch in the emergency process and is set by the volume, where the oil goes and the resources "
          "needed. Where a spill meets more than one row, the higher tier applies."),
    ("t", [("Tier", "Trigger", "Response (ACE-EMR-STD-001 §5)"),
           ("Tier 1", "Up to 10 bbl, contained within the site or its immediate surroundings by on-site resources", "Initial / on-site: site commander directs containment and clean-up"),
           ("Tier 2", "More than 10 bbl and up to 100 bbl, or any spill reaching the sea, a watercourse or land outside a site", "ACE reinforced: Incident Management Team brings resources from other ACE locations"),
           ("Tier 3", "More than 100 bbl, or any spill beyond ACE's capability or reaching a sensitive coastline or fishing ground", "External / mutual aid: Crisis Management Team activates external agreements")],
     [1, 5, 4]),
    ("req", "Any spill of Tier 2 or Tier 3 shall be reported to the environmental regulator within 24 hours, or sooner if a permit requires."),
    ("h2", "Permit exceedances", "2.3, 9.2", "DR_EXCEEDANCE"),
    ("p", "Any exceedance of a permit limit is reported to the VP HSE & Compliance within 24 hours and recorded as an incident under "
          "ACE-INC-STD-001, and the regulator is notified in the time the permit sets."),

    ("h1", "How we will know", "9.4, 9.1"),
    ("h2", "Headline indicators", "9.4, 9.1", "KNOW_KPIS"),
    ("kpi", "Routine flared volume, MMscf. Target: at least 15% a year below the 2025 baseline (objective OBJ-26-07); zero routine flaring by the end of 2030."),
    ("kpi", "Hydrocarbon spills, count and volume (SPILL-N, SPILL-BBL, from the spill_bbl field of INC-REG-001). Target: no Tier 2 or Tier 3 spills; total under 10 bbl a year."),
    ("kpi", "Permit exceedances. Target: zero."),
    ("h2", "Review cycles", "9.1, 2.3", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency"),
           ("Emissions and flaring report", "Monthly"),
           ("Environmental performance report to the Executive Leadership Team", "Quarterly"),
           ("Permit compliance review for every permit", "Annually"),
           ("Oil spill exercise", "Annually (with ACE-RSK-POL-001)")],
     [6, 4]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 9.1", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Emissions, discharges and waste monitoring and reporting (new)", "7.6 (proposed)", "Planned")],
     [2.2, 4.6, 1.4, 1.2]),
    ("p", "Also applies to: the Operating Limit Management Process (ACE-OPS-PRS-001) for flaring limits, emergency activation and response "
          "for spills, and crude export cargo lifting."),
    ("h2", "Standards and practices that implement this policy", "2.1, 2.3", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-EMR-STD-001", "Emergency, Crisis and Business Continuity Standard (oil spill preparedness, section 5)", "Current"),
           ("ACE-ENV-STD-001", "Environmental Management Standard", "Planned"),
           ("ACE-EMR-PLN-003", "Oil Spill Contingency Plan", "Planned")],
     [2.2, 6, 1.2]),
]

ROLES = ["VP HSE & Compliance", "Environmental Lead", "Plant Manager - Central Processing Facility",
         "Offshore Operations Manager (Gulf of Paria)", "Emergency Response & Security Manager", "Counsel, Regulatory & Licensing",
         "Process Owner"]

SPEC = new_policy("ACE-ENV-POL-001", "Environment Policy",
                  "How ACE complies with its permits, cuts flaring, prevents and responds to spills, manages waste and reports its performance.",
                  owner="George Habib", author="Nadine Cooper",
                  reviewers=["Rohan Ali", "Christina Bain", "Jenelle Paul", "Rawle Sandy", "Sophia Hosany"],
                  custodian="Kevin Lutchman", function="HSE & Compliance", tags="2.3, 5.1, 9.1", roles=ROLES, body=body)
