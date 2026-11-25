# ACE-FIN-POL-001 Financial Control and Delegation of Authority Policy (Revision A). Needs the FIN system code (added Session 4).
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "3.1, 2.2"),
    ("p", "This policy sets how ACE controls money: who may commit it, within which limits, how duties are separated, and how partner "
          "costs and revenues are accounted. The Delegation of Authority schedule in section 4 is the condition on every approval step that "
          "commits or changes money in an ACE process."),
    ("p", "It applies to every function, site and employee, to every commitment of ACE funds or of joint-venture funds that ACE manages as "
          "operator, and to revenue from gas and crude sales. Its parent is ACE-LDR-POL-001."),

    ("h1", "Our commitments", "3.1, 2.2"),
    values_note(),
    ("h2", "No commitment without budget and authority", "3.1, 3.4", "COM_BUDGET_AUTHORITY"),
    ("p", "In line with our value Integrity in everything, ACE commits money only when there is an approved budget for it and the person "
          "approving holds the authority for that value under section 4.1. Spending outside the budget needs the higher approval set in "
          "section 4.2."),
    ("req", "No purchase order, contract, variation or other financial commitment shall be issued until it has been approved by a person "
            "holding the delegated authority for its value."),
    ("h2", "Segregation of duties", "3.1, 1.4", "COM_SEGREGATION"),
    ("p", "In line with our value Integrity in everything, the person who requests a commitment is never the person who approves it, and no "
          "one person controls a transaction from start to finish. In ONE this is checked on the process maps: an approval step is never in "
          "the same lane as the step that raised the request."),
    ("req", "The approver of a financial commitment shall be a different person from the requester, and shall hold a position above the requester."),
    ("h2", "Partner costs and revenues are accounted as agreed", "2.5, 9.5", "COM_JV_ACCOUNTING"),
    ("p", "In line with our values Integrity in everything and One team, one way, ACE accounts for and reports joint-venture costs and "
          "revenues exactly as the joint operating agreements require, bills partners on time and answers their audit requests openly."),
    ("h2", "Revenue comes from approved allocation", "9.5, 4.2", "COM_REVENUE"),
    ("p", "In line with our value Integrity in everything, ACE invoices gas and crude sales only from allocation volumes approved under "
          "ACE-HMA-POL-001, and corrects invoices when measurement is corrected."),
    ("h2", "Reliable financial records", "9.5, 1.7", "COM_RECORDS"),
    ("p", "In line with our value Integrity in everything, financial records are complete, accurate and kept in the approved systems, so that "
          "every figure can be traced to its approval and its source document."),

    ("h1", "Accountabilities", "3.1, 2.2"),
    ("t", [("Role", "Named person", "Accountability"),
           ("Chief Financial Officer (policy owner)", "Teresa Daniel", "Owns this policy and the Delegation of Authority schedule; reports financial control to the Board Audit Committee."),
           ("Financial Controller (custodian)", "Krishna Jagessar", "Maintains this policy and the register of individual delegations; proposed owner of revenue invoicing."),
           ("Planning & Budgeting Manager", "Sherma Isaac", "Proposed owner of the annual plan and budget process and the quarterly forecast."),
           ("JV & Partner Accounting Lead", "Melissa Mitchell", "Proposed owner of joint-venture partner billing."),
           ("Head of Internal Audit & Risk Assurance", "Nicole Lange", "Independently tests financial controls and segregation of duties."),
           ("Budget holders", "Function Vice Presidents and managers", "Commit money only within their budget and delegated authority.")],
     [3.2, 2.2, 4.6]),

    ("h1", "Decision rights and thresholds", "3.1, 2.2"),
    ("h2", "Delegation of Authority schedule", "3.1, 2.2", "DR_DOA"),
    ("p", "Values are in United States dollars, for the whole commitment including all its phases and options. A commitment may not be "
          "split to bring it under a lower limit. These bands are the branch conditions on approval steps in every process: Management of "
          "Change cost approval, contract award, budget changes and write-offs."),
    ("t", [("Transaction", "Manager (L3)", "Vice President (L2)", "Chief Executive Officer", "Board"),
           ("Commitment within approved budget (purchase order, contract award, MOC cost)", "Up to 25,000", "Up to 250,000", "Up to 2,000,000", "Above 2,000,000"),
           ("Contract variation", "Up to 25,000 cumulative", "Up to 250,000 cumulative", "Up to 2,000,000 cumulative", "Above 2,000,000"),
           ("Budget transfer between cost centres", "Not delegated", "Up to 250,000 within own function", "Up to 2,000,000", "Above 2,000,000"),
           ("Write-off of an asset, debt or inventory", "Not delegated", "Up to 25,000", "Up to 250,000", "Above 250,000")],
     [3.4, 1.6, 1.8, 1.8, 1.4]),
    ("h2", "Spending outside the budget", "3.1, 3.4", "DR_UNBUDGETED"),
    ("p", "An unbudgeted commitment needs approval one level higher than the same value within budget, and the Chief Financial Officer is "
          "told. Any unbudgeted commitment above 250,000 needs the Chief Executive Officer."),
    ("h2", "Individual delegations", "3.1, 1.5", "DR_INDIVIDUAL"),
    ("appr", "Each delegation of financial authority to an individual shall be approved in writing by the Chief Financial Officer and "
             "recorded in the register of delegations before it is used."),

    ("h1", "How we will know", "9.4, 10.2"),
    ("h2", "Headline indicators", "9.4, 10.2", "KNOW_KPIS"),
    ("kpi", "Budget variance by function at year end. Target: within ±5% of the approved budget."),
    ("kpi", "Monthly close completed on time. Target: 100%, by the seventh working day of the following month."),
    ("kpi", "Partner billing disputes. Target: fewer than two a year, each resolved within 60 days."),
    ("p", "Linked objective: OBJ-26-09 (lifting cost)."),
    ("h2", "Review cycles", "10.2, 2.4", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency"),
           ("Annual plan and budget, approved by the Board before the plan year", "Annually"),
           ("Financial close", "Monthly"),
           ("Joint-venture partner billing statements", "Quarterly, or more often where an agreement requires"),
           ("Forecast of the year-end outturn", "Quarterly"),
           ("Review of the Delegation of Authority schedule", "Annually")],
     [6, 4]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 3.1", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Annual plan and budget", "10.1", "Planned"),
           ("—", "Joint-venture partner billing", "10.2", "Planned"),
           ("—", "Revenue invoicing", "10.3", "Planned")],
     [2.2, 4.6, 1, 1.2]),
    ("p", "Also applies to: every approval step in every ACE process that commits or changes money, including the Management of Change "
          "Process (ACE-MOC-PRS-001) and contract award under ACE-CON-POL-001."),
    ("h2", "Standards and practices that implement this policy", "2.1, 3.1", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-PPL-STD-001", "Roles, Accountabilities and Delegated Authority Standard", "Planned"),
           ("ACE-OMS-STD-004", "Joint Venture and Partner Interface Standard", "Planned")],
     [2.2, 6, 1.2]),
    ("p", "Finance standards for budgeting, close and treasury are to be added to the document register."),
]

ROLES = ["Chief Financial Officer", "Financial Controller", "Planning & Budgeting Manager", "JV & Partner Accounting Lead",
         "Head of Internal Audit & Risk Assurance", "Chief Executive Officer", "Vice President", "Manager", "Budget holder", "Process Owner"]

SPEC = new_policy("ACE-FIN-POL-001", "Financial Control and Delegation of Authority Policy",
                  "Who may commit ACE's money and within which limits, how duties are separated, and how partner costs and revenues are accounted.",
                  owner="Teresa Daniel", author="Sherma Isaac",
                  reviewers=["Krishna Jagessar", "Nicole Lange", "Melissa Mitchell", "Sasha George", "Sharda Bissoon", "Karen Jack"],
                  custodian="Krishna Jagessar", function="Finance", tags="3.1, 2.2, 2.5", roles=ROLES, body=body)
