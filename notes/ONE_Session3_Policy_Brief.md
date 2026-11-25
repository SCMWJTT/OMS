# ONE Session 3: Policy completion brief

**Purpose.** Close the policy gap before the Process dimension is built. This file lists every policy ACE needs, and for each one the details the policies must contain so processes can trace to them, branch on their thresholds, run their cycles and feed Continuous Improvement (CI).

**Status.** Written 25 November 2026 at the end of the Session 3 design discussion. Wilmark is writing the policies outside this session. When they are in `finals/`, return to Session 3 and pick up from Part G.

**Read with.** `notes/ONE_Session3_Process_Handover.md`, `protocol/ONE_Document_Standard.md`, ACE-BPM-PRA-001 (§3 golden thread, §5 one-owner rule), ACE-LDR-POL-001 and ACE-DOC-POL-001 (the two issued policies).

---

## Part A. What the documents showed

1. **Only two policies are issued**: LDR-POL-001 (OMS Policy) and DOC-POL-001. RSK-POL-001 is listed in the Manual as "In development".
2. **19 of the 20 processes in BPM-REG-001 name LDR-POL-001 as their governing policy**, because nothing else exists. BPM-PRA-001 §5 requires one governing Policy per process (C-BPM-003), so in practice the register has no real policy layer.
3. **Mission, vision and values are not written anywhere.** BPM-PRA-001 §3 says the top layer of the golden thread is "Mission, vision, values — ACE-LDR-POL-001", but LDR-POL-001 has no such section, and the company profile doesn't have one either. The golden thread has no top.
4. **The Wave 1 Standards and Procedures have no parent document.** The ODS.Parent property is empty in AIM-STD-001/002, CON, COW, DOC-STD-001/002, EMR, ENG-SPC-410, ENG-STD-901, INC, MNT-STD-001, MOC-PRC-001, OMS-STD-002, OPS-STD-001, PPL-STD-003, PRF-STD-002, PSM, RSK-STD-001 and WEL-STD-001. BPM-PRA-001 §3 requires exactly one parent. The new policies become those parents (Part F).
5. **The system codes have no Finance code.** Appendix B of the Document Standard has no `FIN`, so a Finance policy needs the code added first.
6. **The architecture has no L2 home** for environment, stakeholders/grievances, security, or legal obligations. Policies in those areas will have processes with nowhere to sit (Part F).

---

## Part B. Rules every policy must meet (so processes can use it)

These apply to all new policies, and to LDR-POL-001 Rev 02.

### B1. Common skeleton

The Document Standard (§5.2) gives section patterns for Standards and Procedures but none for Policies, and the two issued policies are laid out differently. Use one skeleton for every policy so ONE can find the commitments in the same place:

| Section | Content | Why processes need it |
|---|---|---|
| Front matter | From the v5 template, as usual | |
| 1 Purpose, scope and applicability | Sites, functions, contractors | Sets the policy's process scope |
| 2 Our commitments | **One Heading 2 per commitment** (2.1, 2.2…), each 1–4 sentences, with a tag line | **Each commitment is a link target.** Processes cite `ACE-XXX-POL-001#<bookmark>` |
| 3 Accountabilities | Table: Role, Named person, Accountability. Policy owner, plus the process owners of the governed processes | Puts process owners on the golden thread |
| 4 Decision rights and thresholds | Only where the policy sets them (risk acceptance, financial limits, notification levels) | **These become the labelled branches on process gateways** |
| 5 How we will know | 2–4 headline KPIs, the linked objectives (OMS-REG-001 IDs) and the review frequency | Process KPIs roll up to these |
| 6 Governed processes and implementing documents | Two tables: (a) L3 processes governed (ID, title, Current/Planned); (b) Standards and Practices that implement the policy | Same pattern as the "implementing processes" table in Practices (C-BPM-004) |
| Appendix A | Controls established by this document, if any (most policies have none) | |

### B2. Writing rules

- **Commitments are outcomes, not steps.** No role sequences: those belong in the PRS (BPM-PRA-001 §6).
- **Each commitment links upward to one or more values** (from LDR-POL-001 Rev 02, B3) by naming them in the text, for example "In line with our value *Integrity in everything*…". ONE will draw the line from value to commitment to process.
- **State cycle frequencies in the policy when they are a commitment** (for example "risks reviewed at least quarterly"). The cycle view in the process maps will read them.
- **Write thresholds as numbers or matrix cells**, not "significant". Gateway branches need a condition someone can test.
- Use exact job titles from `company/org/roles.csv`. Fictitious names only: "the Gas Buyer", "the environmental regulator", "the energy ministry", never real agencies.
- Level 1. Approver: Satesh Sankar, Chief Executive Officer. Review interval: three years. 1–3 title OMS tags.
- Effective date on or after 1 April 2026, so the BPM Practices (effective 1 April 2026) can point to policies that are in force. Suggest **1 January 2027** for the whole set.

### B3. One governing policy, several that "also apply"

A process has **one governing policy** (C-BPM-003). Cross-cutting policies (Code of Conduct, Financial Control, Environment, Security) still constrain many processes. In Session 3, ONE-PRS/2 will add a field `policies_also: []` alongside `policy`. In the policies, list these under 6(a) as "Also applies to".

---

## Part C. The set

| # | Number (proposed) | Title | Owner | Status | Action |
|---|---|---|---|---|---|
| 0 | ACE-LDR-POL-001 Rev 02 | OMS Policy (adds mission, vision and values) | Satesh Sankar — CEO | Issued Rev 01 | **Revise** |
| 1 | ACE-OMS-POL-001 | Governance, Assurance and Continuous Improvement Policy | Satesh Sankar — CEO | New | Write |
| 2 | ACE-RSK-POL-001 | Operational Risk Management Policy | George Habib — VP HSE & Compliance | Planned | Write |
| 3 | ACE-CON-POL-001 | Supply Chain, Logistics and Local Content Policy | Sasha George — VP Supply Chain Management | New | Write |
| 4 | ACE-PPL-POL-001 | People and Competence Policy | Adrian Achong — VP Human Resources | New | Write |
| 5 | ACE-HMA-POL-001 | Hydrocarbon Measurement, Product Quality and Commercial Policy | Karen Jack — VP Business Development & Markets | New | Write |
| 6 | ACE-FIN-POL-001 | Financial Control and Delegation of Authority Policy | Teresa Daniel — CFO | New (needs FIN code) | Write |
| 7 | ACE-LDR-POL-002 | Code of Conduct and Business Ethics Policy | Sharda Bissoon — VP Legal & Government Affairs | New | Write |
| 8 | ACE-ENV-POL-001 | Environment Policy | George Habib — VP HSE & Compliance | New | Write |
| 9 | ACE-SEC-POL-001 | Security Policy (physical and cyber) | George Habib — VP HSE & Compliance (see note) | New | Write |
| 10 | ACE-STK-POL-001 | Stakeholder, Community and Grievance Policy | Rodney Garcia — VP Communications & Corporate Services | New | Write |
| 11 | ACE-DOC-POL-001 | Document and Records Management Policy | as issued | Issued | **Minor correction**: add section 6 tables |

**Folded (not written):**
- Asset Integrity and Technical Authority goes into LDR-POL-001 Rev 02 §2.2.
- Emergency and Crisis goes into RSK-POL-001.
- Customer and product quality goes into HMA-POL-001.
- Reserves and Resources is deferred: the L1 1 processes are governed by LDR-POL-001 for now.

**Writing order for the demo:** 0, 1, 2, 3 first. These cover the three worked processes and the CI dimension:
- Management of Change is governed by RSK-POL-001.
- Offshore Trip Planning is governed by CON-POL-001.
- Inspection Planning is governed by LDR-POL-001.
- Continuous Improvement is governed by OMS-POL-001.

The rest can follow.

---

## Part D. Policy cards

Each card gives what the policy must contain for process treatment. Wording, tone and any other content are up to the writer.

---

### 0. ACE-LDR-POL-001 Rev 02 — OMS Policy (HSE and Operating Integrity)

- **Title tags:** 1.1, 2.1, 1.2
- **Governs:** L1 2 Deliver Wells, 3 Operate & Produce, 4 Maintain Assets; 12.2 TA appointment and legal tracking; L1 1 (interim)
- **Must add or contain:**
  1. **New section: Our purpose, vision and values** at the front. Mission (one sentence), vision (one sentence), and **4–6 values, each as its own Heading 2** so they can be linked to. Every other policy points to these values. They are the top of the golden thread and the top layer of the process landscape view.
  2. **§2.2 Asset integrity, expanded** to absorb the folded Asset Integrity and Technical Authority policy:
     - SCEs have performance standards and owners.
     - Technical Authorities are appointed and independent of line pressure (ENG-STD-901).
     - Overdue or impaired SCEs go through deviation, never silent deferral.
     - These are the commitments AIM-PRS-001, AIM-PRS-002, MNT-PRS-001/002 and ENG-PRS-410 trace to.
  3. **Keep these as separate Heading 2 commitments:**
     - stop work (8.4): a gateway in COW-PRS-001
     - work is planned, permitted, supervised and handed back (8.1–8.3)
     - operating within limits (6.3): OPS-PRS-001
  4. **§4.2:** move the detail on assurance and continual improvement out to OMS-POL-001, and leave one sentence pointing to it.
  5. Section 6 governed-processes table (Part E lists the processes).
- **Headline KPIs:** Tier 1+2 process safety events; SCE inspections and tests on time; overdue SCE deviations.
- **Cycles:** none of its own; points to OMS-POL-001.

---

### 1. ACE-OMS-POL-001 — Governance, Assurance and Continuous Improvement Policy

This is **the policy for the CI dimension**. It needs the most care.

- **Title tags:** 10.4, 10.5, 2.4
- **Owner:** CEO. Custodian: Gary Ho Sing — Manager, Strategy & Planning (BPM system owner).
- **Governs:** 12.1 Objectives and annual OMS plan; 12.2 Management review, OMS maturity assessment; 12.3 Audit planning and follow-up (PRF-PRS-001); 12.4 BPM-PRS-001, BPM-PRS-002 and **new BPM-PRS-003 Improvement Management Process** (the CI flow itself, modelled as a process).
- **Commitments it must contain:**
  1. **Process approach.** All work is organised as processes with one owner each. Every corporate objective is carried by at least one process (backs C-BPM-001).
  2. **Objectives.** Set every year, measurable, owned, and linked to processes and risks (2.4).
  3. **Three lines of assurance.** Risk-based audit plan with three-year element coverage (PRF-STD-002).
  4. **Continuous improvement as a duty.** Every improvement is tied to a process, and where possible to a step.
  5. **Sources of improvement.** Name all five, since the CI register's `source` field uses this list: incident and near-miss actions; audit and assurance findings; process reviews; KPI breaches (two periods out of target); **staff ideas**, which anyone may raise.
  6. **Proportionate method.** Name the ladder. The CI register's `method` field uses these four values:
     - *just do it*: one function, low risk, no change to roles or controls
     - *PDCA*: a process-owner improvement
     - *DMAIC*: data-driven, for a cross-functional problem or a KPI breach
     - *project*: needs capital or MOC Major
     State who decides the route: the process owner, escalating to the BPM system owner.
  7. **Benefit must be shown.** An improvement closes only when a measured KPI moves against its baseline, or a control is shown to work. Opinion is not enough. This gives the CI stages *Verified* and *Standardised*.
  8. **Standardise through control.** Improvements change documents by revision, and change roles, controls or systems through MOC (C-BPM-044).
  9. **Recognition.** Improvements and the people behind them are recognised (8.5). This feeds a CI board "recognition" view.
  10. **Maturity.** A company target, for example "all Current processes at maturity Level 3 by end 2028".
- **Decision rights:**
  - Who approves CI items by method.
  - Who may reject or park an idea. Proposal: the process owner, with a reason recorded and the originator told within 30 days.
- **Cycles to state:**
  - annual process review (each process)
  - quarterly process KPI report to the VP
  - twice-yearly report to the ELT (C-BPM-048)
  - annual management review (10.5)
  - annual maturity self-assessment
  - three-year audit coverage
- **Headline KPIs:**
  - CI items closed with verified benefit
  - idea-to-decision time
  - share of processes at maturity 3 or above
  - annual reviews on time
- **Implementing documents:** BPM-PRA-001/002/003, PRF-STD-002, planned PRF-STD-001/003/004 and OMS-STD-001/003.
- **Re-parent after issue:** BPM-PRA-001, PRF-STD-002.

---

### 2. ACE-RSK-POL-001 — Operational Risk Management Policy

- **Title tags:** 5.1, 5.2, 5.3
- **Governs:** L1 7 entire.
  - 7.1: RSK-PRS-001, Risk assessment and acceptance
  - 7.2: **MOC-PRS-001 (worked process)**, Deviation and exemption (absorbs SCE deviation as a branch)
  - 7.3: Hazard studies
  - 7.4: INC-PRS-001, Lessons learned and action tracking
  - 7.5: EMR-PRS-001, Emergency activation and response, Crisis management and continuity
- **Commitments it must contain:**
  1. Assess risk before acting, using the one ACE Risk Matrix (RSK-STD-001).
  2. Barriers identified, owned and verified (5.1).
  3. **Change is controlled.** No change to plant, process, people or organisation without MOC (5.3). MOC-PRS-001 traces here.
  4. **Departures are temporary.** Deviations have an expiry, compensating measures and named approval (2.6).
  5. Learn from every event: report, investigate in proportion, close actions, share lessons (9.2, 9.3). Name the hand-off to OMS-POL-001 CI.
  6. Rising risk is escalated early (5.4).
  7. Prepare for and respond to emergencies; manage crises; keep the business running (7.5). This absorbs the folded emergency policy.
- **Decision rights and thresholds (critical; these drive the gateway branches):**
  - **Risk appetite by consequence category** (people, environment, asset, reputation, financial), stated against the matrix bands in RSK-STD-001 §3.
  - **Risk acceptance authority by band**, for example Low: Area Authority; Medium: Function VP; High: CEO; Very High: not acceptable. This is the condition on the "Approve change" branch of MOC and on the deviation approval branch.
  - **MOC class rule in one line**, for example "Major if it affects an SCE, an operating limit or a lane role". This is the `Classify change` gateway, S03 in the MOC model.
  - **Deviation maximum duration** before re-approval, for example 90 days, or 30 days for SCEs. This drives the expiry and extension cycle.
  - **Emergency alert levels**: the trigger for each level.
- **Cycles to state:**
  - corporate risk register review (suggest quarterly)
  - asset risk review (suggest six-monthly)
  - bow-tie review on change or every three years
  - HAZOP revalidation every five years
  - drills to a stated programme
- **Headline KPIs:**
  - Tier 1/2 PSE
  - overdue risk and incident actions
  - MOC median cycle time (already in the MOC model)
  - deviations past expiry
- **Implementing documents:** RSK-STD-001, RSK-PRA-001, PSM-STD-001, INC-STD-001, EMR-STD-001, OMS-STD-002, MOC-PRC-001; planned MOC-STD-001, INC-STD-002, PSM-STD-002.
- **Re-parent after issue:** all of those (the issued ones currently have no parent).

---

### 3. ACE-CON-POL-001 — Supply Chain, Logistics and Local Content Policy

The worked process **Offshore Trip Planning and Manifesting** depends on this card.

- **Title tags:** 3.6, 8.1, 2.3
- **Governs:**
  - L1 6: LOG-PRS-001, Marine vessel scheduling, Shore base receipt, storage and dispatch
  - L1 9: Tendering and award, CON-PRS-001 Pre-qualification, Mobilisation, Contract performance and close-out, Supplier quality
- **Commitments it must contain:**
  1. **Safe movement of people.** Every person travelling offshore is manifested, inducted, competent for their role and fit for work. Personnel on board (POB) is known at all times. These are the people-flow tokens and the checks before boarding.
  2. **Safe movement of materials.** Cargo is declared, dangerous goods are identified and packed to rule, and lifting equipment is certified. These are the material-flow tokens.
  3. **Transport decisions belong to the competent person.** Weather and sea-state limits for helicopter and vessel moves are set by the Marine Lead and the aviation contractor, and are never overridden for schedule (ties to 8.4 stop work).
  4. **Priority when capacity is short.** A stated order for seats and deck space, for example: emergency, then SCE work, then production-critical, then routine. **This is the gateway when a flight or boat is oversubscribed.**
  5. Contractors are selected by risk rating, pre-qualified, bridged and monitored (CON-STD-001).
  6. **Local content.** Preference for Trinidad and Tobago suppliers and nationals where capable, with a stated target. This is a tendering evaluation criterion.
  7. Supplier quality: critical items are inspected and traceable; nonconforming supply is quarantined.
- **Decision rights and thresholds:**
  - Contract risk rating bands (from CON-STD-001 §2), which set the pre-qualification path.
  - Manifest cut-off time before departure, for example 24 hours, with late-addition approval by the Offshore Installation Manager.
  - Tender value limits come from FIN-POL-001 (state "also applies").
- **Cycles to state:**
  - contract performance reviews by risk rating (for example High quarterly, Medium six-monthly)
  - supplier re-qualification every three years
  - weekly marine and aviation schedule
- **Headline KPIs:**
  - manifest accuracy (POB reconciliation)
  - seat and deck-space utilisation
  - trips cancelled or bumped
  - local content share
  - contractor incidents
- **Implementing documents:** CON-STD-001; planned CON-STD-002, LOG-PRA-001 (**needed as the parent of LOG-PRS-001**).
- **Re-parent after issue:** CON-STD-001.

---

### 4. ACE-PPL-POL-001 — People and Competence Policy

- **Title tags:** 3.3, 3.1, 1.5
- **Governs:** 8.1 Recruitment, screening and induction; 8.2 Competence assessment and authorisation, Annual training needs; 8.3 Performance management.
- **Commitments it must contain:**
  1. **Role profiles carry OMS duties** (1.5). Lanes in process maps are roles, so a role's profile must show the process steps it performs. ONE will link role page, lanes and steps.
  2. **No one performs a safety-critical role until assessed and authorised** (3.3). This is a standard **pre-condition check** used inside PtW, isolation, offshore travel and other processes.
  3. Role authorities (Area Authority, Technical Authority, Performing Authority, process owner) are appointed in writing (3.1). *Financial* delegation sits in FIN-POL-001; *role* authority sits here (PPL-STD-001 implements it).
  4. **Process owners are trained** within 60 days of appointment (supports C-BPM-040), and lane roles are briefed before a revised process takes effect (C-BPM-045).
  5. Workforce consultation (3.5); fair recognition and consequence (8.5).
- **Cycles to state:**
  - annual training needs analysis
  - re-verification intervals per competence profile (set by profile, policy states the principle)
  - annual performance cycle
- **Headline KPIs:**
  - safety-critical roles with current authorisation
  - training plan completion
  - time to competence for new starters
- **Implementing documents:** PPL-STD-003; planned PPL-STD-001/002/004, LDR-STD-004, OHH-STD-001.
- **Re-parent after issue:** PPL-STD-003.

---

### 5. ACE-HMA-POL-001 — Hydrocarbon Measurement, Product Quality and Commercial Policy

- **Title tags:** 4.2, 9.5, 2.3
- **Governs:** L1 5: HMA-PRS-001 Allocation and custody transfer; Gas nomination and delivery to the Gas Buyer; Crude export cargo lifting.
- **Commitments it must contain:**
  1. Custody-transfer and allocation meters are calibrated and verified at stated intervals, with records kept.
  2. **The allocation method is approved, documented and auditable**, and partners can see it (2.5).
  3. **Mismeasurement is corrected and disclosed.** Above a stated threshold (for example ±0.5% of daily volume, or any custody meter failure) the Gas Buyer and partners are notified within a stated time. **This is a gateway with a notification branch.**
  4. Sales gas and crude meet contract quality; off-spec product is not delivered without the buyer's agreement. This absorbs customer and product quality.
  5. Nominations are honoured; shortfalls are notified in advance.
- **Cycles to state:**
  - daily allocation
  - monthly allocation close and partner statement
  - meter verification and proving intervals
  - annual allocation audit
- **Headline KPIs:**
  - unaccounted-for gas
  - allocation closed on time
  - nomination performance
  - off-spec events
- **Implementing documents:** planned HMA-PRA-001 (**needed as the parent of HMA-PRS-001**), STK-STD-002.

---

### 6. ACE-FIN-POL-001 — Financial Control and Delegation of Authority Policy

- **First:** add `FIN | Finance and Financial Control | 2, 3` to Appendix B.1 of the Document Standard.
- **Title tags:** 3.1, 2.2, 2.5
- **Governs:** L1 10: Annual plan and budget; JV partner billing; Revenue invoicing. **Also applies to every approval step** in every process.
- **Commitments it must contain:**
  1. No commitment of money without an approved budget and the authority to spend.
  2. **Segregation of duties.** The person who requests is not the person who approves. ONE can check this mechanically: an approval step must not be in the same lane as the step that raised the request.
  3. Partner (JV) costs and revenues are accounted and reported as the agreements require (2.5).
  4. Revenue is invoiced from approved allocation (link to HMA-POL-001).
- **Decision rights and thresholds (critical):** a **Delegation of Authority schedule** in USD bands by role, for example up to 25k Manager; up to 250k VP; up to 2M CEO; above that the Board. These bands become branch conditions on approval steps: MOC cost approval, contract award, budget changes, write-offs. Keep the schedule in the policy as a table, or in a named register the policy points to.
- **Cycles to state:** annual budget; monthly close; quarterly partner billing; quarterly forecast.
- **Headline KPIs:** budget variance; monthly close on time; partner billing disputes.

---

### 7. ACE-LDR-POL-002 — Code of Conduct and Business Ethics Policy

- **Title tags:** 1.4, 1.3
- **Governs:** new candidate L3 **Speak-up and concern handling** (L2: 12.2, or a new L2, see Part F). **Also applies to** tendering and award, recruitment, and any approval step.
- **Commitments it must contain:**
  1. Integrity, anti-bribery and anti-corruption, fair dealing.
  2. **Conflicts of interest are declared before decisions.** This is a check step inside tendering, recruitment and award.
  3. Gifts and hospitality limits, with a stated value.
  4. **Speak up without retaliation.** Concerns are acknowledged and responded to within stated times. These become cycle-time KPIs, and the channel also feeds CI ideas.
- **Relationship:** the Manual lists LDR-STD-001 *Code of Conduct* (planned, Level 2). This policy is its parent. Keep the commitments here and the detailed rules in the Standard.
- **Headline KPIs:** concerns raised and closed in time; conflict declarations completed for awards.

---

### 8. ACE-ENV-POL-001 — Environment Policy

- **Title tags:** 2.3, 5.1, 9.1
- **Governs:** new candidate L3 **Emissions, discharges and waste monitoring and reporting**. **Also applies to** OPS-PRS-001 (flaring limits), Emergency response (spills) and Crude export.
- **Commitments it must contain:**
  1. Comply with permits and licence conditions from the environmental regulator.
  2. **Minimise flaring and venting**, with a stated no-routine-flaring commitment or target. This links to operating limits.
  3. Spill prevention, with **spill tiers** (Tier 1/2/3 by volume and location) that set the emergency branch. Align with EMR-STD-001 §5.
  4. Waste managed by hierarchy; discharges within limits.
  5. Report environmental performance at stated frequencies.
- **Cycles to state:** monthly emissions reporting; annual permit compliance review.
- **Headline KPIs:** flared volume; spills (bbl, from INC-REG-001 `spill_bbl`); permit exceedances.
- **Implementing documents:** planned ENV-STD-001, EMR-PLN-003.

---

### 9. ACE-SEC-POL-001 — Security Policy (physical and cyber)

- **Owner note:** physical security sits with the Emergency Response & Security Manager (HSE & Compliance). OT cyber sits with the Telecoms & OT Cyber Security Lead (IT, Data & Knowledge). One owner is required, so either the VP HSE & Compliance or the VP IT, Data & Knowledge. **Decide before writing.**
- **Title tags:** 5.1, 7.5
- **Governs:** 11.2 Access management; new candidate L3 **Site and port access control** (Point Lisas shore base, offshore). **Also applies to** ENG-PRS-410 SIS lifecycle (changes to control systems) and MOC.
- **Commitments it must contain:**
  1. Access to sites, systems and information is by need and authorised role.
  2. **Changes to control and safety systems (OT) go through MOC**, and remote access is controlled.
  3. Security incidents are reported through INC-STD-001.
  4. Port and marine security arrangements at Point Lisas, described generically.
- **Cycles to state:** quarterly access reviews; annual security risk assessment.
- **Headline KPIs:** access reviews on time; security incidents.

---

### 10. ACE-STK-POL-001 — Stakeholder, Community and Grievance Policy

- **Title tags:** 4.1, 4.3, 4.4
- **Governs:** new candidate L3 **Grievance and feedback handling** (STK-PRC-001 is planned).
- **Commitments it must contain:**
  1. Know and engage stakeholders around PLB, the CPF and the land leases.
  2. **Grievances are logged, acknowledged within a stated time** (for example 5 working days) **and answered within a stated time** (for example 30 days), with escalation if not resolved. This makes a strong, readable demo process with clear cycle-time KPIs.
  3. Fishing communities in the Gulf of Paria are consulted before marine activity that affects them.
- **Headline KPIs:** grievances closed in time; repeat grievances.

---

### 11. ACE-DOC-POL-001 — Document and Records Management Policy (minor correction)

- Add the **section 6 tables** (governed processes and implementing documents):
  - governed processes: DOC-PRS-001, Periodic document review, Records retention and disposal
  - implementing documents: DOC-STD-001/002, DOC-PRC-001; planned DOC-STD-003
- Make sure the review frequency for periodic document review is stated as a commitment (it drives the document currency timeline).
- **Re-parent after issue:** DOC-STD-001, DOC-STD-002.

---

## Part E. Which policy governs each candidate process

From the Session 3 inventory: the 62 candidates plus the new candidates the policies create (marked **new**).

| L2 | Process | Governing policy |
|---|---|---|
| 1.2, 1.3 | Reserves estimation; Field development planning | LDR-POL-001 (interim) |
| 2.2–2.5 | Well construction verification; WEL-PRS-001; WEL-PRS-002; Well integrity anomaly; Intervention/abandonment | LDR-POL-001 |
| 3.1–3.5 | Production planning; OPS-PRS-001; COW-PRS-001; Isolation; Override and inhibit; Operational readiness | LDR-POL-001 |
| 4.1–4.4 | Maintenance strategy; MNT-PRS-001; **AIM-PRS-001 (worked)**; SCE performance verification; Corrosion monitoring; ENG-PRS-410; AIM-PRS-002 | LDR-POL-001 |
| 4.3 | MNT-PRS-002 SCE deviation | RSK-POL-001 (if merged into Deviation and exemption) |
| 5.2–5.4 | HMA-PRS-001; Gas nomination; Crude lifting | HMA-POL-001 |
| 6.1–6.3 | **LOG-PRS-001 (worked)**; Marine scheduling; Shore base | CON-POL-001 |
| 7.1–7.5 | RSK-PRS-001; Risk assessment; **MOC-PRS-001 (worked)**; Deviation; Hazard studies; INC-PRS-001; Lessons; EMR-PRS-001; Emergency response; Crisis/BCP | RSK-POL-001 |
| 7.x | **new** Emissions, discharges and waste reporting | ENV-POL-001 |
| 8.1–8.3 | Recruitment; Competence authorisation; Training needs; Performance management | PPL-POL-001 |
| 9.1–9.3 | Tendering; CON-PRS-001; Mobilisation; Contract performance; Supplier quality | CON-POL-001 |
| 10.1–10.3 | Budget; JV billing; Revenue invoicing | FIN-POL-001 |
| 11.1, 11.3 | DOC-PRS-001; Periodic review; Records retention | DOC-POL-001 |
| 11.2 | Access management | SEC-POL-001 |
| 12.1–12.4 | Objectives and OMS plan; Management review; Maturity; PRF-PRS-001; BPM-PRS-001; BPM-PRS-002; **new BPM-PRS-003 Improvement Management** | OMS-POL-001 |
| 12.2 | TA appointment; Legal tracking | LDR-POL-001 |
| 12.x | **new** Speak-up and concern handling | LDR-POL-002 |
| 12.x | **new** Grievance and feedback | STK-POL-001 |
| 6.2 / 11.2 | **new** Site and port access control | SEC-POL-001 |

---

## Part F. Knock-on changes (for when we return, not for the policy writer)

1. **Re-parent the Wave 1 documents** by setting their ODS.Parent property. Under the Document Standard's "minor necessary corrections" rule, this is a property change, not a rewrite:
   - LDR-POL-001: AIM-STD-001/002, COW-STD-001, MNT-STD-001, OPS-STD-001, WEL-STD-001, ENG-STD-901, ENG-SPC-410
   - RSK-POL-001: RSK-STD-001, PSM-STD-001, INC-STD-001, EMR-STD-001, OMS-STD-002, MOC-PRC-001
   - CON-POL-001: CON-STD-001
   - PPL-POL-001: PPL-STD-003
   - OMS-POL-001: PRF-STD-002, BPM-PRA-001
   - DOC-POL-001: DOC-STD-001, DOC-STD-002
2. **Update the `policy` column in BPM-REG-001** from Part E.
3. **Add the FIN system code** to Appendix B.1, and to `protocol/one-protocol.json` if the checker validates codes.
4. **Add L2 groups to BPM-PRA-001 §4.2.** This is a document change, approved by the BPM system owner:
   - 7.6 Manage environmental performance
   - 12.5 Engage stakeholders and handle grievances
   - 12.6 Uphold conduct and handle concerns
   - Security: suggest placing it under 11.2 and 6.2 rather than adding a new group
5. **Add a Policy column to the Document Standard §5.2 table** using the B1 skeleton, so the checker can test policies.
6. **Portal:** the document map and the process landscape show policies as the top band, with values above them.

---

## Part G. Open items from Session 3 (still to decide)

1. **Owner rule.** 8 of the 20 register owners are Leads, below the manager level BPM-PRA-001 §5 requires, and MNT-PRS-002's owner (Marc Gomes) left on 31 August 2026 with no replacement recorded. Fix the register, or keep it as a deliberate finding for the demo?
2. **Scope.** Do all candidates go into the register as Planned, with the C-grade ones (L1 1 and L1 10, no documents) shown hollow?
3. **Merge.** Does MNT-PRS-002 SCE deviation become a branch of Deviation and exemption?
4. **Worked processes.** MOC, Offshore Trip Planning and Inspection Planning, with Document Publication as the alternative. Plus BPM-PRS-003 Improvement Management as the showcase for the CI dimension?
5. **Formats.** ONE-PRS/2, the ledger (cases plus events with arrived/started/finished times) and the CI register, as proposed in the Session 3 chat. Agree these before building.

## Part H. Done when

- [ ] LDR-POL-001 Rev 02 issued, with mission, vision and values as linkable headings
- [ ] OMS-POL-001, RSK-POL-001, CON-POL-001 issued (the minimum to resume Session 3)
- [ ] PPL, HMA, FIN, LDR-002, ENV, SEC, STK policies issued, or deliberately deferred
- [ ] DOC-POL-001 corrected with its section 6 tables
- [ ] Every policy follows the B1 skeleton, with commitments as Heading 2s and thresholds as numbers
- [ ] All files in `finals/` and passing the checker
