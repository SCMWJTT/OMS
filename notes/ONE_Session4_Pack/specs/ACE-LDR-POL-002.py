# ACE-LDR-POL-002 Code of Conduct and Business Ethics Policy (Revision A). Parent of the planned ACE-LDR-STD-001 Code of Conduct.
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "1.4, 1.3"),
    ("p", "This policy sets the standards of conduct ACE expects of everyone who works for or with it: honesty, fair dealing, no bribery or "
          "corruption, conflicts declared, and the freedom to speak up without fear. The detailed rules are in the Code of Conduct "
          "(ACE-LDR-STD-001), which this policy governs."),
    ("p", "It applies to every ACE director, employee and secondee at every site, and to contractors, suppliers, agents and partners when "
          "they act for ACE. Its parent is ACE-LDR-POL-001."),

    ("h1", "Our commitments", "1.4, 1.3"),
    values_note(),
    ("h2", "Integrity and fair dealing", "1.4, 1.3", "COM_INTEGRITY"),
    ("p", "In line with our value Integrity in everything, ACE does business honestly and within the law. We do not offer, give, ask for "
          "or accept bribes or facilitation payments of any kind, directly or through others, and we deal fairly with customers, "
          "suppliers, partners, competitors and public officials."),
    ("req", "No person acting for ACE shall offer, give, request or accept a bribe, a facilitation payment or any other improper advantage."),
    ("h2", "Conflicts of interest are declared before decisions", "1.4, 3.6", "COM_CONFLICTS"),
    ("p", "In line with our value Integrity in everything, anyone with a personal interest that could affect, or appear to affect, a "
          "decision declares it before the decision is made and steps aside from it. This declaration is a check step in tendering and "
          "award, recruitment and promotion, and other approvals."),
    ("req", "Each person taking part in a tender evaluation, contract award, recruitment or approval decision shall declare any conflict of "
            "interest before the decision and shall take no further part in it if a conflict exists."),
    ("h2", "Gifts and hospitality within limits", "1.4, 1.3", "COM_GIFTS"),
    ("p", "In line with our value Integrity in everything, gifts and hospitality are modest, occasional and open, never cash, and never "
          "given or received when they could influence a decision. The limits are set in section 4.2."),
    ("h2", "Speak up without retaliation", "1.4, 3.5", "COM_SPEAK_UP"),
    ("p", "In line with our values Integrity in everything and Learn and improve, anyone may raise a concern about conduct, safety or the "
          "law, openly or anonymously, and ACE protects them from retaliation. Every concern is acknowledged and answered within the times "
          "in section 4.3. Concerns that point to a better way of working are passed, with the originator's consent, to the CI register "
          "as staff ideas under ACE-OMS-POL-001."),
    ("req", "No person shall retaliate against anyone who raises a concern in good faith."),
    ("h2", "Respect at work", "1.4, 3.5", "COM_RESPECT"),
    ("p", "In line with our values Care for people and places and One team, one way, everyone at ACE is treated with respect, free from "
          "harassment, bullying and unfair discrimination."),

    ("h1", "Accountabilities", "3.1, 1.4"),
    ("t", [("Role", "Named person", "Accountability"),
           ("VP Legal & Government Affairs (General Counsel) (policy owner)", "Sharda Bissoon", "Owns this policy and the Code of Conduct; receives and directs the handling of concerns."),
           ("Corporate Secretary (custodian)", "Kerry-Ann Mitchell", "Maintains this policy, the gifts and hospitality register and the conflicts of interest register."),
           ("Head of Internal Audit & Risk Assurance", "Nicole Lange", "Independent channel for concerns; investigates concerns about senior leaders; reports to the Board Audit Committee."),
           ("VP Human Resources", "Adrian Achong", "Applies conflict declarations in recruitment; handles conduct cases fairly and consistently."),
           ("Senior Counsel, Contracts & Commercial", "Winston Daniel", "Proposed owner of the speak-up and concern handling process."),
           ("Line managers", "All", "Make sure their teams know the Code; act on concerns raised with them.")],
     [3.4, 2.2, 4.4]),

    ("h1", "Decision rights and thresholds", "1.4, 2.2"),
    ("h2", "Conflicts of interest", "1.4, 3.1", "DR_CONFLICTS"),
    ("p", "Declarations are recorded in the conflicts of interest register. The declarer's line manager decides how a declared conflict is "
          "managed; for a Vice President the decision is made by the General Counsel, and for the Chief Executive Officer by the Board."),
    ("h2", "Gifts and hospitality limits", "1.4, 1.3", "DR_GIFTS"),
    ("t", [("Value per item or occasion", "Rule"),
           ("Up to TT$500", "May be given or accepted; recorded in the register"),
           ("Above TT$500 and up to TT$2,500", "Needs prior approval of the Vice President of the function; recorded"),
           ("Above TT$2,500, cash or cash equivalents, or anything from a party in an open tender with ACE", "Not permitted"),
           ("Anything to or from a public official beyond token items of the company's branding", "Not permitted without the General Counsel's prior written approval")],
     [5, 5]),
    ("h2", "Concern response times", "1.4, 4.3", "DR_CONCERNS"),
    ("t", [("Stage", "Time"),
           ("Concern acknowledged to the person who raised it", "Within 5 working days"),
           ("Initial assessment and decision on how it will be handled", "Within 30 days"),
           ("Investigation closed and outcome communicated as far as confidentiality allows", "Within 90 days, or with a stated reason and new date")],
     [6, 4]),

    ("h1", "How we will know", "9.4, 1.4"),
    ("h2", "Headline indicators", "9.4, 1.4", "KNOW_KPIS"),
    ("kpi", "Concerns acknowledged within 5 working days and closed within 90 days. Target: at least 90% of concerns."),
    ("kpi", "Conflict declarations completed for contract awards. Target: 100% of awards."),
    ("kpi", "Employees completing the annual Code of Conduct certification. Target: at least 98%."),
    ("h2", "Review cycles", "1.4, 10.2", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency"),
           ("Code of Conduct certification by every employee", "Annually"),
           ("Conflict of interest declaration by every manager and every person in procurement and HR", "Annually, and before each relevant decision"),
           ("Report on concerns, conflicts and gifts to the Executive Leadership Team and the Board Audit Committee", "Quarterly")],
     [6, 4]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 1.4", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Speak-up and concern handling (new)", "12.6 (proposed)", "Planned")],
     [2.2, 4.6, 1.4, 1.2]),
    ("p", "Also applies to: tendering and award (ACE-CON-POL-001), recruitment (ACE-PPL-POL-001) and every approval step in every ACE "
          "process, for the conflict of interest check."),
    ("h2", "Standards and practices that implement this policy", "2.1, 1.4", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-LDR-STD-001", "Code of Conduct", "Planned")],
     [2.2, 6, 1.2]),
]

ROLES = ["VP Legal & Government Affairs (General Counsel)", "Corporate Secretary", "Head of Internal Audit & Risk Assurance",
         "VP Human Resources", "Senior Counsel, Contracts & Commercial", "Line manager", "Vice President", "Chief Executive Officer",
         "Process Owner"]

SPEC = new_policy("ACE-LDR-POL-002", "Code of Conduct and Business Ethics Policy",
                  "The standards of honest, fair and lawful conduct ACE expects of everyone who works for or with it, and the freedom to speak up.",
                  owner="Sharda Bissoon", author="Winston Daniel",
                  reviewers=["Adrian Achong", "Nicole Lange", "Sasha George", "Teresa Daniel", "Rodney Garcia"],
                  custodian="Kerry-Ann Mitchell", function="Legal & Government Affairs", tags="1.4, 1.3", roles=ROLES, body=body)
