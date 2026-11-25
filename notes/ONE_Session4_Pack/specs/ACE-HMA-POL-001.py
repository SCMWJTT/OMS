# ACE-HMA-POL-001 Hydrocarbon Measurement, Product Quality and Commercial Policy (Revision A).
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "4.2, 9.5"),
    ("p", "This policy sets ACE's commitments for measuring and allocating the oil and gas it produces, for the quality of the sales gas "
          "and crude it delivers, and for meeting its nominations to customers. Accurate measurement is the basis of revenue, royalty, "
          "partner statements and trust with the Gas Buyer and partners."),
    ("p", "It applies to custody-transfer and allocation metering at the offshore installations, the CPF, the land leases and the export "
          "jetty, to gas deliveries to the Gas Buyer, to crude export cargoes, and to the people and systems that calculate allocation. "
          "Its parent is ACE-LDR-POL-001."),

    ("h1", "Our commitments", "4.2, 9.5"),
    values_note(),
    ("h2", "Meters are calibrated and verified", "9.5, 6.5", "COM_METERS"),
    ("p", "In line with our value Integrity in everything, custody-transfer and allocation meters are calibrated, verified and proved at the "
          "intervals in section 4.3, by competent people, and the records are kept so that any figure can be traced to the meter and the "
          "calibration behind it."),
    ("h2", "Allocation is approved, documented and auditable", "2.5, 9.5", "COM_ALLOCATION"),
    ("p", "In line with our values Integrity in everything and One team, one way, ACE allocates production to wells, fields and partners by "
          "one approved, documented method. Partners can see the method and the data behind their statements, and any change to the method "
          "is agreed with partners and made through Management of Change."),
    ("h2", "Mismeasurement is corrected and disclosed", "4.2, 9.5", "COM_MISMEASUREMENT"),
    ("p", "In line with our value Integrity in everything, a measurement error is never hidden or absorbed. Above the threshold in section "
          "4.1, the Gas Buyer and partners are told within the stated time, the volumes are corrected, and the correction is shown in the "
          "next statement."),
    ("req", "A mismeasurement above the threshold in section 4.1 shall be notified to the Gas Buyer and affected partners within 24 hours of discovery."),
    ("h2", "Product meets contract quality", "4.2, 4.1", "COM_QUALITY"),
    ("p", "In line with our values Integrity in everything and Care for people and places, sales gas and crude meet the quality set in the "
          "sales contracts. Off-specification product is not delivered without the buyer's written agreement; otherwise delivery is "
          "stopped or the product is diverted until it is back in specification."),
    ("h2", "Nominations are honoured", "4.2, 4.4", "COM_NOMINATIONS"),
    ("p", "In line with our value Integrity in everything, ACE delivers what it nominates. When a shortfall is expected, the Gas Buyer or the "
          "crude lifter is told in advance, at the threshold and time set in section 4.2, so that they can plan around it."),

    ("h1", "Accountabilities", "3.1, 4.2"),
    ("t", [("Role", "Named person", "Accountability"),
           ("VP Business Development & Markets (policy owner)", "Karen Jack", "Owns this policy, the sales contracts and partner relationships."),
           ("Metering & Measurement Lead", "Navin Sookdeo", "Technical Authority for metering; owner of the Allocation and Custody Transfer Process (ACE-HMA-PRS-001)."),
           ("Marketing Manager (Gas & Crude) (custodian)", "Anjali Boodoo", "Maintains this policy; proposed owner of gas nomination and crude lifting processes."),
           ("Partner Relations Lead", "Anushka Seepersad", "Partner communication, including disclosures of mismeasurement."),
           ("Hydrocarbon Accountant", "Michael Fernandes", "Daily allocation and the monthly allocation close."),
           ("Crude Loading & Custody Transfer Coordinator", "Vidya Rajkumar", "Custody transfer at crude export liftings."),
           ("Plant Manager - Central Processing Facility", "Rohan Ali", "Sales gas and crude quality at the CPF; stops off-specification delivery.")],
     [3.2, 2.2, 4.6]),

    ("h1", "Decision rights and thresholds", "4.2, 9.5"),
    ("h2", "Mismeasurement notification", "4.2, 9.5", "DR_MISMEASUREMENT"),
    ("t", [("Condition", "Action", "Who decides"),
           ("Error of more than ±0.5% of the daily volume at a custody-transfer or allocation meter", "Notify the Gas Buyer and affected partners within 24 hours; correct in the monthly close", "Metering & Measurement Lead confirms; Partner Relations Lead notifies"),
           ("Any failure of a custody-transfer meter", "Notify within 24 hours; apply the contract backup method until the meter is restored", "Metering & Measurement Lead"),
           ("Error at or below ±0.5% of daily volume", "Correct in the monthly close and record the cause", "Hydrocarbon Accountant")],
     [3.6, 4, 2.4]),
    ("h2", "Nomination shortfall notice", "4.2, 4.4", "DR_SHORTFALL"),
    ("p", "A planned shortfall of more than 5% of the nominated daily quantity is notified to the Gas Buyer at least 24 hours before the gas "
          "day. An unplanned shortfall is notified as soon as it is known, and in any case within two hours."),
    ("h2", "Meter verification intervals", "9.5, 6.5", "DR_METER_INTERVALS"),
    ("t", [("Meter or instrument", "Interval"),
           ("Gas chromatograph at a custody-transfer point", "Daily calibration check"),
           ("Custody-transfer gas meter secondary instruments (pressure, temperature)", "Monthly verification"),
           ("Crude custody-transfer meters", "Proved at each export lifting and at least monthly"),
           ("Allocation meters", "Verified at least quarterly"),
           ("Full calibration of custody-transfer meters", "At least annually, or as the sales contract requires if shorter")],
     [6, 4]),
    ("p", "The detailed methods are in the Hydrocarbon Measurement and Allocation Practice (ACE-HMA-PRA-001)."),
    ("h2", "Allocation method changes", "2.5, 5.3", "DR_ALLOCATION_CHANGE"),
    ("appr", "A change to the allocation method shall be approved by the VP Business Development & Markets after Technical Authority "
             "endorsement by the Metering & Measurement Lead and agreement with the affected partners."),

    ("h1", "How we will know", "9.4, 9.5"),
    ("h2", "Headline indicators", "9.4, 9.5", "KNOW_KPIS"),
    ("kpi", "Gas allocation imbalance and unaccounted-for gas (ALLOC-IMB). Target: under 0.5% (objective OBJ-26-05)."),
    ("kpi", "Monthly allocation closed and partner statements issued on time. Target: 100%."),
    ("kpi", "Gas Buyer contract quantity delivered (GAS-DCQ). Target: at least 98% (objective OBJ-26-05)."),
    ("kpi", "Off-specification deliveries without buyer agreement. Target: zero."),
    ("h2", "Review cycles", "9.5, 2.5", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency"),
           ("Production allocation", "Daily"),
           ("Allocation close and partner statement", "Monthly, by the tenth working day of the following month"),
           ("Meter verification and proving", "As in section 4.3"),
           ("Independent audit of the allocation system", "Annually")],
     [5, 5]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 4.2", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("ACE-HMA-PRS-001", "Allocation and Custody Transfer Process", "5.2", "Planned"),
           ("—", "Gas nomination and delivery to the Gas Buyer", "5.3", "Planned"),
           ("—", "Crude export cargo lifting", "5.4", "Planned")],
     [2.2, 4.6, 1, 1.2]),
    ("p", "Also applies to: revenue invoicing, which is governed by ACE-FIN-POL-001 and invoices only from approved allocation."),
    ("h2", "Standards and practices that implement this policy", "2.1, 9.5", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-HMA-PRA-001", "Hydrocarbon Measurement and Allocation Practice (parent of ACE-HMA-PRS-001)", "Planned"),
           ("ACE-STK-STD-002", "Customer and Product Quality Standard", "Planned"),
           ("ACE-OMS-STD-004", "Joint Venture and Partner Interface Standard", "Planned")],
     [2.2, 6, 1.2]),
]

ROLES = ["VP Business Development & Markets", "Metering & Measurement Lead", "Marketing Manager (Gas & Crude)", "Partner Relations Lead",
         "Hydrocarbon Accountant", "Crude Loading & Custody Transfer Coordinator", "Plant Manager - Central Processing Facility",
         "Technical Authority", "Process Owner"]

SPEC = new_policy("ACE-HMA-POL-001", "Hydrocarbon Measurement, Product Quality and Commercial Policy",
                  "How ACE measures and allocates what it produces, delivers product to contract quality and honours its nominations.",
                  owner="Karen Jack", author="Navin Sookdeo",
                  reviewers=["Rohan Ali", "Vidya Rajkumar", "Michael Fernandes", "Melissa Mitchell", "Anushka Seepersad", "Dev Jaggernauth"],
                  custodian="Anjali Boodoo", function="Business Development & Markets", tags="4.2, 9.5, 2.3", roles=ROLES, body=body)
