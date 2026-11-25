# ACE-CON-POL-001 Supply Chain, Logistics and Local Content Policy (Revision A).
# Governs the worked process ACE-LOG-PRS-001 Offshore Trip Planning and Manifesting.
from polspec import new_policy, values_note

body = [
    ("h1", "Purpose, scope and applicability", "3.6, 8.1"),
    ("p", "This policy sets ACE's commitments for moving people and materials safely to and from its sites, and for buying goods and "
          "services from capable contractors and suppliers, with a preference for Trinidad and Tobago companies and nationals."),
    ("p", "It applies to marine and aviation movements between the Point Lisas Shore Base (PLB) and the offshore installations (PAP, CHB, "
          "SAP), to road movements to the CPF and the land leases (LND), to the shore base warehouse, and to every contract and purchase "
          "made by any ACE function. Its parent is ACE-LDR-POL-001. Tender and contract award value limits are set by ACE-FIN-POL-001, "
          "which also applies to the processes listed here."),

    ("h1", "Our commitments", "3.6, 8.1"),
    values_note(),
    ("h2", "Safe movement of people", "8.1, 3.3", "COM_PEOPLE_MOVEMENT"),
    ("p", "In line with our value Safety above all, every person who travels offshore is on the manifest, has completed the required "
          "induction and offshore survival training, holds the competence their role needs and is fit for work. Personnel on board (POB) "
          "at every installation and on every vessel and helicopter is known at all times."),
    ("req", "No person shall board a helicopter or vessel for an ACE offshore installation unless they are on the approved manifest and "
            "have passed the pre-boarding checks of induction, competence and fitness for work."),
    ("rec", "Personnel on board shall be recorded and reconciled for each installation, vessel and flight at every departure and arrival."),
    ("h2", "Safe movement of materials", "8.1, 5.1", "COM_MATERIAL_MOVEMENT"),
    ("p", "In line with our value Safety above all, all cargo is declared on the manifest, dangerous goods are identified, packed, marked "
          "and documented to the applicable dangerous goods rules, and lifting equipment and cargo carrying units are within their "
          "certification. Undeclared or uncertified cargo does not travel."),
    ("h2", "Transport decisions belong to the competent person", "8.4, 3.1", "COM_TRANSPORT_AUTHORITY"),
    ("p", "In line with our values Safety above all and Integrity in everything, the weather and sea-state limits for vessel and helicopter "
          "movements are set by the Marine Lead and by the helicopter operator, and the master or pilot decides whether a movement goes "
          "ahead. These limits are never overridden to keep a schedule, and anyone may stop a movement under the stop work commitment of "
          "ACE-LDR-POL-001."),
    ("h2", "Priority when capacity is short", "8.1, 3.4", "COM_PRIORITY"),
    ("p", "In line with our values Safety above all and One team, one way, when a flight or a vessel is oversubscribed, seats and deck "
          "space are allocated in a fixed order, the same at every site. The order is set in section 4.2 and is the decision point in the "
          "trip planning process when demand exceeds capacity."),
    ("h2", "Contractors selected and managed by risk", "3.6, 8.3", "COM_CONTRACTORS"),
    ("p", "In line with our values Safety above all and One team, one way, the risk of the work, not its value, sets how much assurance a "
          "contract receives. Contractors are risk-rated before procurement, pre-qualified where the rating requires, bridged into ACE "
          "arrangements before mobilisation and monitored through the contract (ACE-CON-STD-001). ACE stays accountable for work it "
          "delegates."),
    ("h2", "Local content", "3.4, 4.1", "COM_LOCAL_CONTENT"),
    ("p", "In line with our value Care for people and places, ACE prefers Trinidad and Tobago suppliers, contractors and nationals wherever "
          "they are capable of meeting our safety, technical and quality requirements, and helps local suppliers become capable. Local "
          "content is a scored criterion in every tender evaluation; the targets are set in section 4.4."),
    ("h2", "Supplier quality", "3.6, 6.4", "COM_SUPPLIER_QUALITY"),
    ("p", "In line with our values Safety above all and Integrity in everything, critical items are inspected and traceable to their "
          "manufacture, test and certification before they are accepted. Nonconforming supply is identified, segregated and kept out of "
          "use until it has a recorded disposition."),

    ("h1", "Accountabilities", "3.1, 3.6"),
    ("t", [("Role", "Named person", "Accountability"),
           ("VP Supply Chain Management (policy owner)", "Sasha George", "Owns this policy and the supply chain and logistics system."),
           ("Logistics & Materials Manager", "Lisa Williams", "Owner of the Offshore Trip Planning and Manifesting Process (ACE-LOG-PRS-001); marine scheduling and the shore base."),
           ("Contracts Manager (custodian)", "Rhea Sookram", "Maintains this policy; owner of the Contractor Pre-qualification Process (ACE-CON-PRS-001)."),
           ("Procurement Manager", "Gillian Modeste", "Tendering and award; applies the local content criterion."),
           ("Marine Lead", "Sarita Sookram", "Sets vessel weather and sea-state limits; marine operations assurance."),
           ("Quality Lead", "Terrence Henry", "Supplier quality, receiving inspection and nonconforming supply."),
           ("Local Content Specialist", "Celeste Bailey", "Measures and reports local content against the targets."),
           ("Offshore Installation Managers", "Roger Ramkissoon; Winston Granger", "Approve late additions to a manifest for their installation; account for POB on board."),
           ("Contract owners", "Named for each contract", "Risk screen, performance reviews and close-out for their contract.")],
     [3, 2.4, 4.6]),

    ("h1", "Decision rights and thresholds", "3.6, 8.1"),
    ("h2", "Contract risk rating", "3.6, 5.1", "DR_CONTRACT_RISK"),
    ("p", "The contract class is set by the highest credible exposure on the ACE Risk Matrix (ACE-CON-STD-001 §2). It decides the "
          "pre-qualification path and the frequency of performance reviews."),
    ("t", [("Contract class", "Pre-qualification path", "Performance review"),
           ("Low", "Basic eligibility and specification checks", "At completion, or as set by the contract owner"),
           ("Medium", "HSE pre-qualification before award", "At least quarterly"),
           ("High", "HSE and technical pre-qualification; formal bridging document", "At least monthly"),
           ("Very High", "As High, plus a multidisciplinary assurance plan and leadership oversight", "At least monthly, with independent verification")],
     [1.6, 4.6, 3.8]),
    ("h2", "Priority order for seats and deck space", "8.1, 3.4", "DR_PRIORITY_ORDER"),
    ("t", [("Priority", "Category", "Examples"),
           ("1", "Emergency", "Medical evacuation, emergency response personnel and equipment"),
           ("2", "Safety-critical work", "Work on safety-critical elements, overdue SCE tasks, well control"),
           ("3", "Production-critical", "Work to restore or protect production; critical spares"),
           ("4", "Routine", "Planned maintenance, projects, visits and general cargo")],
     [1, 2.6, 6.4]),
    ("p", "Within a category, the Logistics & Materials Manager decides with the Offshore Installation Manager. A person or item moved to a "
          "later trip is recorded as bumped, with the reason."),
    ("h2", "Manifest cut-off", "8.1, 3.1", "DR_MANIFEST_CUTOFF"),
    ("p", "The manifest for each flight and vessel closes 24 hours before departure. A later addition needs the approval of the Offshore "
          "Installation Manager of the receiving installation and still passes every pre-boarding check."),
    ("appr", "A person or item added to a manifest less than 24 hours before departure shall be approved by the Offshore Installation "
             "Manager of the receiving installation."),
    ("h2", "Local content targets", "3.4, 2.4", "DR_LOCAL_CONTENT"),
    ("t", [("Measure", "Target"),
           ("Share of annual contract and procurement spend with Trinidad and Tobago registered suppliers", "At least 60%"),
           ("Share of the ACE and contractor workforce at ACE sites who are Trinidad and Tobago nationals", "At least 90%"),
           ("Weight of local content in tender evaluation scoring", "At least 10% of the total score")],
     [7, 3]),

    ("h1", "How we will know", "9.4, 3.6"),
    ("h2", "Headline indicators", "9.4, 8.1", "KNOW_KPIS"),
    ("kpi", "Manifest accuracy: POB reconciled with the manifest at every departure and arrival. Target: 100%."),
    ("kpi", "Seat and deck-space utilisation on scheduled flights and vessels. Target: at least 85%."),
    ("kpi", "Trips cancelled or people and cargo bumped for reasons other than weather. Target: under 5% of seats and deck space booked."),
    ("kpi", "Local content share of spend and workforce. Target: as in section 4.4."),
    ("kpi", "Contractor recordable injuries, as part of TRIR. Target: TRIR below 0.5 (objective OBJ-26-01)."),
    ("p", "Linked objectives: OBJ-26-01 (injuries) and OBJ-26-09 (lifting cost)."),
    ("h2", "Review cycles", "3.6, 8.1", "KNOW_CYCLES"),
    ("t", [("Cycle", "Frequency"),
           ("Marine and aviation schedule", "Weekly"),
           ("Contract performance reviews", "By contract class, as in section 4.1"),
           ("Supplier re-qualification", "At least every three years, and after a major incident or a repeated defect"),
           ("Local content report to the VP Supply Chain Management", "Quarterly")],
     [5, 5]),

    ("h1", "Governed processes and implementing documents", "2.1, 7.1"),
    ("h2", "Processes governed by this policy", "7.1, 8.1", "GOVERNED_PROCESSES"),
    ("t", [("Number", "Process", "L2", "Status"),
           ("—", "Marine vessel scheduling", "6.1", "Planned"),
           ("—", "Shore base receipt, storage and dispatch", "6.2", "Planned"),
           ("ACE-LOG-PRS-001", "Offshore Trip Planning and Manifesting Process", "6.3", "Planned"),
           ("—", "Tendering and award", "9.1", "Planned"),
           ("ACE-CON-PRS-001", "Contractor Pre-qualification Process", "9.2", "Planned"),
           ("—", "Contractor mobilisation", "9.2", "Planned"),
           ("—", "Contract performance and close-out", "9.2", "Planned"),
           ("—", "Supplier quality", "9.3", "Planned")],
     [2.2, 4.6, 1, 1.2]),
    ("p", "Also applies: ACE-FIN-POL-001 (value limits for tender and award), ACE-LDR-POL-002 (conflicts of interest in tendering) and "
          "ACE-SEC-POL-001 (site and port access at the Point Lisas Shore Base)."),
    ("h2", "Standards and practices that implement this policy", "2.1, 3.6", "IMPLEMENTING_DOCUMENTS"),
    ("t", [("Number", "Title", "Status"),
           ("ACE-CON-STD-001", "Contractor and Supplier Management Standard", "Current"),
           ("ACE-CON-STD-002", "Local Content Standard", "Planned"),
           ("ACE-LOG-PRA-001", "Marine and Aviation Logistics Practice (parent of ACE-LOG-PRS-001)", "Planned")],
     [2.2, 6, 1.2]),
]

ROLES = ["VP Supply Chain Management", "Logistics & Materials Manager", "Contracts Manager", "Procurement Manager", "Marine Lead",
         "Quality Lead", "Local Content Specialist", "Offshore Installation Manager", "Contract owner", "Process Owner"]

SPEC = new_policy("ACE-CON-POL-001", "Supply Chain, Logistics and Local Content Policy",
                  "How ACE moves people and materials safely, chooses and manages contractors and suppliers, and builds local content.",
                  owner="Sasha George", author="Lisa Williams",
                  reviewers=["Gillian Modeste", "Sarita Sookram", "Terrence Henry", "Celeste Bailey", "Roger Ramkissoon", "Christina Bain"],
                  custodian="Rhea Sookram", function="Supply Chain Management", tags="3.6, 8.1, 2.3", roles=ROLES, body=body)
