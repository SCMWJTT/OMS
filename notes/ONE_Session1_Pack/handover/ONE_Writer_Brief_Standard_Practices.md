# ONE / ACE — Writer Brief: Standard Practices

**For:** ACE document writers
**From:** OMS documentation team (Cynmark Systems)
**Date:** 23 November 2026
**Covers:** 10 new Standard Practices:
- **Part 1:** the Business Process Framework (4 Practices);
- **Part 2:** the core discipline Practices (6 Practices).

**Write to:** ACE-DOC-STD-002 Rev 02 (Operational Document Publishing Standard, rewritten), template **v5** (v4 plus the changes listed in Section 0.3).

---

## 0. Read this first

### 0.1 What a Standard Practice is

ACE documents sit in five layers:

| Level | Layer | Answers | Example |
|---|---|---|---|
| 1 | **Policy** (POL) | Why, and what we commit to | OMS Policy |
| 2 | **Standard** (STD) | What must be true (minimum requirements) | Asset Integrity Management Standard |
| 2 | **Standard Practice** (PRA) | How ACE does it: the methods, criteria and technical rules of a discipline | Risk-Based Inspection & Corrosion Management Practice |
| 3 | **Process** (PRS) | Who does what, in what order, across functions | Inspection Planning and Execution Process |
| 4 | **Procedure / Plan** (PRC, PLN) | Step-by-step for one activity | Isolation and Reinstatement Procedure |
| 5 | **Work Instruction / Form / Register** (WIN, FRM, REG) | One task at one site, the record, the list | Pommerac A ESD Valve Function Test |

A Practice sits **beside** its Standard, at the same level. It **does not repeat** the Standard. It turns "what" into a professional method, and it **names the Processes and Procedures that carry the method out** (ENG-STD-901, Section 2.2).

**Test:** if a sentence describes *a sequence of steps by named roles*, it belongs in a Process or Procedure. Move it there and reference it.

### 0.2 Rules every Practice must follow

1. **Start from template v5.** Never copy an existing document (Errors to Avoid, item 1).
2. **The document control table is the master.** Fill it in once. The cover, header and footer must match it. The check script rebuilds the hidden properties from the table.
3. **People** are written as **Name — Job title**, exactly as in `ACE_People.csv`. Committees may appear only as endorsers.
4. **Framework field (fixed wording):** `IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 04`.
5. **"Shall" only in:** ODS.Requirement, ODS.Responsibility, ODS.ApprovalRequirement, ODS.RecordRequirement and ODS.RiskControl. **Never** in Warning, Note, Example, Normal, lists or table cells.
6. **OMS tags:** every heading gets a tag line (OMS Tags content control) with the primary tag first. Use the expectation numbers in the OMS Manual (1.1 to 10.5). Tag sparingly: 1 to 3 per section.
7. **Control IDs (new in Rev 02).** Every ODS.RiskControl paragraph carries a Control ID content control (alias "Control ID", tag `ODS.Control@C-<SYS>-<NNN>`), for example `C-AIM-014`. Each Practice is given its own control number range below, so writers can't collide.
8. **Process references (new).** When the Practice relies on a process, name it by its PRS number, for example `ACE-AIM-PRS-001 Inspection Planning and Execution Process`. Planned processes are fine; the gateway lists them as planned.
9. **Parent document (new property `ODS.Parent`).** This is the Standard (or Policy) the Practice serves.
10. **Status for this batch:** Draft, **Rev A**, with dates blank. Approval dates are set when the batch is issued (see the story calendar in the handover).
11. **Length:** 12 to 30 pages. Practical and specific to ACE. No generic textbook material.
12. **External standards:** cite by number and title (API 580/581, API 584, IEC 61511, ISO 14224, NORSOK D-010, API MPMS, ISO 5167, ISA-18.2/IEC 62682 and so on). Do not quote their text.
13. **IOGP:** don't quote it. Write to the spirit of the expectation and tag it.
14. Before uploading, run the check (`quick.py`) and make sure there are no `~$` files.

### 0.3 Template v5 changes (from v4)

- Adds the custom property **`ODS.Parent`**, making 23 properties.
- Adds a **Control ID** content control inside the ODS.RiskControl example paragraph.
- Adds a **"Processes and procedures that implement this document"** table in the document map section, with columns: Number | Title | Status (Current/Planned) | Steps relied on.
- Adds a **"Controls established by this document"** appendix table, with columns: Control ID | Control statement (short) | Risk/threat addressed | Section | Process step | Evidence/record.
- Sets the Word built-in panel mapping in the template: Subject = document number; Tags = title OMS tags; Categories = "Practice (Level 2)"; Company = Acme Caribbean Energy Limited; Hyperlink base = https://oms.cynmark.app/.

### 0.4 Required anatomy of a Practice

Use these numbered sections, in this order. Sub-sections are free.

1. **Purpose, scope and parent Standard.** What the Practice turns into method, and where it applies (sites: PAP, CHB, SAP, CPF, LND, PLB, HOF).
2. **Roles and technical authority.** Who owns the method, who is Technical Authority (TA) and who applies it. Use ODS.Responsibility.
3. **Method:** the core of the document (two to five sections). Criteria, decision rules, calculations, acceptance limits and worked ACE examples.
4. **Records, data and systems.** What the method produces, where it lives (CMMS, ONE, registers) and the data quality rules.
5. **Performance and verification.** KPIs (leading and lagging), and how the TA checks the method is applied.
6. **Implementing processes and procedures.** This is the table from 0.3.
7. **Appendices:** controls table (mandatory); forms, matrices and examples.

### 0.5 ACE context to use (stay consistent)

- **Sites:**
  - Head Office (HOF), Central Trinidad;
  - Point Lisas shore base (PLB): supply boats and the helicopter route;
  - **Pommerac A** (PAP): manned platform with the Offshore Installation Manager (OIM);
  - **Chenet B** (CHB) and **Sapodilla C** (SAP): unmanned, normally visited by boat;
  - land leases **Tamarind, Pawpaw, Soursop** (LND);
  - the **Central Processing Facility** (CPF): gas sales to NGC, crude export.
- **The running storyline (use it in examples).** The Pommerac A crude export pipeline shows internal corrosion pinholes. Corrosion inhibitor injection had been running below its operating window for months. An intelligent pigging run was deferred. A small leak is found during a boat patrol (a near miss). An MOC follows, then the inspection interval and operating window are revised. The storyline crosses OPS, AIM, MNT, LOG (boat patrol), HMA (lost and unaccounted volumes) and every BPM Practice.
- **Org facts:** the 32 discipline leads report to their VP and have a dotted line to the VP Engineering & Projects through the **Technical Leadership Council (TLC)**.

---

## Part 1: Business Process Framework (BPM)

**New system code: BPM, Business Process Management.**
- **System owner (proposed):** Gary Ho Sing, Manager, Strategy & Planning.
- **Executive sponsor:** Satesh Sankar, Chief Executive Officer.
- **Elements:** 1, 2, 3, 7 and 10.

Why Strategy & Planning: processes cross functions, and the process architecture hangs from strategy, mission, vision and values. The system owner is confirmed in the OMS Manual Rev 04.

### P1. ACE-BPM-PRA-001: Business Process Management Practice

| Field | Value |
|---|---|
| Parent | ACE-LDR-POL-001 OMS Policy |
| Title OMS tags | 7.1, 2.1, 3.1 |
| Author | Kwame Henry — Strategy & Planning Analyst |
| Reviewers | Marissa Bobb — OMS Manager; Elena Farfan — Manager, Technical Excellence; Sanjay Jagessar — Information Management Lead |
| Endorser | Not required |
| Approver / Owner | Gary Ho Sing — Manager, Strategy & Planning |
| Control range | C-BPM-001 to C-BPM-019 |
| Pages | 20 to 26 |

**Must establish:**
- **The golden thread.** Mission, vision and values → strategy and objectives → Policy → Standard/Practice → Process → Procedure → Record.
- **The ACE Process Architecture.** Use APQC PCF style levels:
  - L1 Category;
  - L2 Process Group;
  - L3 Process (one PRS document);
  - L4 Activity (a swimlane step);
  - L5 Task (the procedure or work instruction).

  Give the ACE L1 list, about 10 to 12 categories, in three groups:
  - **core:** Explore & Develop, Deliver Wells, Operate & Produce, Maintain Assets, Process & Sell, Move People & Materials;
  - **enabling:** Manage Risk & HSE, People, Supply Chain, Finance, Information;
  - **governing:** Strategy & OMS.

  Give the L2 groups under each.
- **The one-owner rule.** Each process has one process owner, one primary function and one governing Policy (and normally one parent Standard or Practice).
- **When to write which document.** A decision table: Standard vs Practice vs Process vs Procedure vs Work Instruction.
- **Traceability rules.**
  - Every L3 process traces up to a Standard or Practice and down to its procedures.
  - Every binding requirement in a Standard is either carried out by a process step or flagged as "direct", meaning no process is needed.
- **The Process Register** (ACE-BPM-REG-001), its fields, and how ONE displays it.
- **Adapting client tools.** ACE's architecture can map to tools the client already uses. Write this generically, with no product names.

### P2. ACE-BPM-PRA-002: Process Modelling and Process File Practice

| Field | Value |
|---|---|
| Parent | ACE-BPM-PRA-001 |
| Title OMS tags | 7.1, 7.4, 9.5 |
| Author | Karen Ahyew — Strategy & Planning Analyst |
| Reviewers | Shalini Mungal — Data & Applications Manager; Ryan Ramsaran — Technical Writer / Procedures Specialist; Trevor Chin — Human Factors Lead |
| Endorser | Not required |
| Approver / Owner | Gary Ho Sing — Manager, Strategy & Planning |
| Control range | C-BPM-020 to C-BPM-039 |
| Pages | 20 to 30 |

**Must establish:**
- **The PRS document pair.** A Word **process description** (cover, control table, purpose, owner, SIPOC, KPIs, step narrative) plus a **process model file** (`ACE-XXX-PRS-NNN.json`) with the same number and revision. The Word file is the controlled source of the narrative; the JSON carries the swimlanes. The gateway checks that they agree.
- **Modelling conventions.** A small BPMN subset: start/end events, tasks, exclusive gateway, parallel gateway, handoff, wait/timer, document/record. One lane per **role** (not per person). Each step has a verb–object name ("Approve permit"). Steps are numbered `S01`, `S02` and so on.
- **The process file fields** (see the schema in the Handover, Section 11):
  - `id`, `owner`, `function`, `policy`, `parent`, `oms_tags`;
  - `lanes`;
  - `steps`, each with `id`, `lane`, `type`, `name`, `inputs`, `outputs`, `doc_refs` (doc#bookmark), `controls` (C-IDs), `records`, `systems` and `next`;
  - `kpis`.
- **Simulation-ready fields (optional now, required later):** step duration (min, likely, max), cost per hour by role, volume per year, rework probability per gateway branch, wait time. They are captured now so animation and simulation need no rework later.
- **Linking rules.** Step ↔ document section (bookmark), step ↔ control, step ↔ role in the role register, step ↔ OMS expectation.
- **Drawing and reading.** How the ONE process reader displays swimlanes, and the colour rules (controls in red, records in grey, handoffs as arrows across lanes).
- **Worked example.** A short version of the MOC process, ACE-MOC-PRS-001, with 8 to 12 steps.

### P3. ACE-BPM-PRA-003: Process Ownership and Continuous Improvement Practice

| Field | Value |
|---|---|
| Parent | ACE-BPM-PRA-001 |
| Title OMS tags | 10.4, 3.1, 9.4 |
| Author | Kwame Henry — Strategy & Planning Analyst |
| Reviewers | Marissa Bobb — OMS Manager; Dillon Haddad — Compliance & Assurance Manager; Andrea Farfan — Learning & Competence Manager |
| Endorser | Not required |
| Approver / Owner | Gary Ho Sing — Manager, Strategy & Planning |
| Control range | C-BPM-040 to C-BPM-059 |
| Pages | 16 to 22 |

**Must establish:**
- **Process owner duties.** The process owner is accountable for the design, performance and **continuous improvement** of the process. Contrast with:
  - the *document owner*, who controls the text;
  - the *Technical Authority*, who controls technical content;
  - the *line manager*, who controls the people doing the work.
- **Process KPIs.** At least one each for: cycle time, quality (right first time), control effectiveness, and conformance (sampled).
- **The review cycle.** An annual process review, plus triggers: an incident, an audit finding, an MOC, KPI drift or a regulatory change.
- **Improvement routes.** Small fixes go through document revision. Changes to roles, controls or systems go through **MOC** (ACE-MOC-PRC-001). Lessons come from INC.
- **Process maturity.** A five-level scale (1 ad hoc → 5 optimised), self-assessed annually and fed to the OMS maturity assessment (Manual C.4).
- **Process health on the ONE dashboard.** Owner, last review, KPIs, open actions, linked incidents.

### P4. ACE-RSK-PRA-001: Controls and Barrier Linkage Practice

| Field | Value |
|---|---|
| Parent | ACE-RSK-STD-001 Risk Management Standard |
| Title OMS tags | 5.1, 6.4, 10.3 |
| Author | Stephanie Boissiere — Process Safety Engineer |
| Reviewers | Damian Daniel — Process Safety Lead; Nicole Lange — Head of Internal Audit & Risk Assurance; Marc Gomes — Maintenance & Integrity Manager |
| Endorser | Technical Leadership Council |
| Approver / Owner | George Habib — VP HSE & Compliance |
| Control range | C-RSK-001 to C-RSK-029 |
| Pages | 20 to 28 |

**Must establish:**
- **The control as the hinge.** Every significant risk has controls. Every control links to:
  - the risk and threat it addresses;
  - the bow-tie barrier it forms (if any);
  - the **document section** that requires it;
  - the **process step** that performs it;
  - the **role** that owns it;
  - the **equipment or Safety Critical Element (SCE)** it depends on;
  - the **evidence record** that proves it works.
- **Control types:** preventive or mitigating; hard (engineered), soft (procedural) or people; critical or non-critical.
- **The Control ID scheme:** `C-<SYS>-<NNN>`, with an allocation rule per system and how IDs are written into documents (the content control).
- **The Controls Register** (ACE-RSK-REG-002): its fields, and how it links to the Risk Register (RSK-REG-001), the SCE register (AIM-REG-001) and the Process Register (BPM-REG-001).
- **Control health.** Effective / degraded / failed / not tested, and how events (incidents, test failures, overdue maintenance) change it.
- **Risk appetite and objectives.** Controls are sized against the ACE Risk Matrix and appetite. Over-control has a cost too. Opportunities sit on the same matrix, with objectives as the counterweight to risk.
- **Worked example:** the Pommerac A export pipeline bow-tie (threat: internal corrosion). Barriers: inhibitor injection within its operating window (OPS), corrosion monitoring and intelligent pigging (AIM), pipeline patrols (LOG), leak detection, emergency shutdown, and the spill response plan.

---

## Part 2: Core discipline Practices

One Practice for each of the six core areas. Two are in new systems: **LOG** and **HMA** (see the Handover for the Manual Rev 04 change).

### D1. ACE-OPS-PRA-001: Operating Envelopes and Integrity Operating Windows Practice

| Field | Value |
|---|---|
| Parent | ACE-OPS-STD-001 Operating Envelopes and Operating Limits Standard (planned) |
| Title OMS tags | 6.3, 5.4, 9.1 |
| Author | Michelle de Verteuil — Process Engineering Lead |
| Reviewers | Rohan Ali — Plant Manager - Central Processing Facility; Arjun Gittens — Offshore Operations Manager (Gulf of Paria); Rajesh Ramsaran — Production Chemistry Lead; Sophia de Souza — Materials & Corrosion Lead |
| Endorser | Technical Leadership Council |
| Approver / Owner | Sophia Hosany — VP Operations |
| Control range | C-OPS-001 to C-OPS-039 |
| Pages | 22 to 30 |

**Must establish:**
- **The limit hierarchy.** Design limits → safe operating limits (trip) → **integrity operating windows (IOWs): critical, standard and informational** → operating targets. Align with API RP 584.
- **How limits are set.** From design basis, HAZOP/LOPA, materials and corrosion studies, and chemistry. Who approves each type (the TA for critical limits).
- **The operating limits register** per site (CPF, PAP, LND), and how it is built into the control system (alarms, displays).
- **Exceedance response.** For each IOW class: required response time, who is notified, the investigation threshold, and when an excursion becomes an incident or a deviation (OMS-STD-002).
- **Changing a limit.** Always through MOC.
- **Examples:**
  - CPF separator pressure;
  - glycol dehydration water dew point;
  - **corrosion inhibitor injection rate on the Pommerac A export line**: the storyline. This IOW was breached for months without escalation.
- **Implementing processes:**
  - ACE-OPS-PRS-001 Operating Limit Management (planned);
  - ACE-MOC-PRS-001;
  - ACE-INC-PRS-001.

### D2. ACE-WEL-PRA-001: Well Barriers and Well Handover Practice

| Field | Value |
|---|---|
| Parent | ACE-WEL-STD-001 Well Integrity Management Standard (planned) |
| Title OMS tags | 6.4, 6.5, 8.1 |
| Author | Shalini Jaggernauth — Well Integrity Lead |
| Reviewers | Arjun Ramlal — Drilling Engineering Lead; Kathy-Ann Simmons — Completions Lead; Nazim Bailey — Completions & Well Intervention Manager; Luis de Verteuil — Land Operations Manager |
| Endorser | Technical Leadership Council |
| Approver / Owner | Joanne Ho Sing — VP Wells |
| Control range | C-WEL-001 to C-WEL-039 |
| Pages | 24 to 30 |

**Must establish:**
- **The two-barrier principle.** Primary and secondary well barrier envelopes. Well barrier elements and their acceptance criteria (align with NORSOK D-010, ISO 16530-1 and API RP 90/90-2).
- **Well barrier schematics.** Required for every well state: drilling, completion, production, suspended, abandoned.
- **Well integrity categories** (for example green, yellow, orange, red), their definitions and the response for each.
- **Annulus pressure management.** Maximum allowable annulus surface pressure (MAASP), monitoring frequency, and the bleed-down rules.
- **Well handover.** Wells → Operations → Wells (for intervention). The handover pack, sign-offs and the barrier status at handover.
- **Unmanned platforms and land.** How barrier testing is done on Chenet B and Sapodilla C (boat visits) and on Tamarind, Pawpaw and Soursop.
- **Implementing processes:**
  - ACE-WEL-PRS-001 Well Handover (planned);
  - ACE-WEL-PRS-002 Annulus Pressure Management (planned).

### D3. ACE-AIM-PRA-001: Risk-Based Inspection and Corrosion Management Practice

| Field | Value |
|---|---|
| Parent | ACE-AIM-STD-001 Asset Integrity Management Standard |
| Title OMS tags | 6.5, 6.4, 5.4 |
| Author | Rochelle Mark — Inspection Engineer |
| Reviewers | Wayne Rajkumar — Inspection Lead; Sophia de Souza — Materials & Corrosion Lead; Allison Mitchell — Pipelines Lead; Marlon Gonzales — Static Mechanical Lead |
| Endorser | Technical Leadership Council |
| Approver / Owner | Dev Jaggernauth — VP Engineering & Projects |
| Control range | C-AIM-001 to C-AIM-039 |
| Pages | 26 to 32 |

**Must establish:**
- **RBI method** (API RP 580/581 aligned):
  - corrosion loops and damage mechanisms (CO₂, H₂S, microbially influenced corrosion (MIC), erosion, corrosion under insulation (CUI));
  - probability of failure (PoF) and consequence of failure (CoF) on the ACE Risk Matrix;
  - the inspection interval rules.
- **Corrosion management:**
  - inhibitor programmes;
  - coupons and probes;
  - corrosion rate calculation and remaining life;
  - links to the IOWs in OPS-PRA-001.
- **Pipeline integrity:** intelligent pigging frequency, cathodic protection surveys and patrol frequency (with LOG).
- **Deferral rule.** An inspection on an SCE may be deferred only by risk assessment, with TA approval, a time limit and interim measures. Deferrals are visible in ONE. (This is the storyline's broken barrier.)
- **Anomaly management.** Classification, fitness-for-service (API 579), and the repair/replace decision.
- **Implementing processes:**
  - ACE-AIM-PRS-001 Inspection Planning and Execution (planned);
  - ACE-AIM-PRS-002 Anomaly Management (planned).

### D4. ACE-MNT-PRA-001: Equipment Criticality and Safety-Critical Element Maintenance Practice

| Field | Value |
|---|---|
| Parent | ACE-MNT-STD-001 Maintenance Management Standard |
| Title OMS tags | 6.4, 6.5, 8.2 |
| Author | Nadira Ramsaran — Reliability & Maintenance Lead |
| Reviewers | Marc Gomes — Maintenance & Integrity Manager; Sunita Seepersad — Maintenance Superintendent; Sharon Alexander — Rotating Equipment Lead; Akilah Noel — Fire & Gas and Safety Systems Lead |
| Endorser | Technical Leadership Council |
| Approver / Owner | Sophia Hosany — VP Operations |
| Control range | C-MNT-001 to C-MNT-039 |
| Pages | 22 to 28 |

**Must establish:**
- **The equipment hierarchy and criticality ranking** (ISO 14224 taxonomy): the A/B/C method using the ACE Risk Matrix.
- **SCE identification.** Linkage to the SCE register (AIM-REG-001) and the performance standards.
- **Maintenance strategy by criticality.** Preventive, predictive (condition-based), run-to-failure. Reliability-centred maintenance (RCM) light for A-critical equipment.
- **Work order priority** and backlog limits. **SCE overdue rules:** an overdue SCE maintenance item is a deviation, raised through OMS-STD-002.
- **Defeat/bypass of SCEs.** Linkage to Control of Work and the override log.
- **Feedback.** Failure data → criticality and strategy review.
- **Implementing processes:**
  - ACE-MNT-PRS-001 Maintenance Planning and Scheduling (planned);
  - ACE-MNT-PRS-002 SCE Deviation (planned);
  - ACE-MNT-WIN-001-PAP (existing in the priority list).

### D5. ACE-LOG-PRA-001: Marine and Aviation Logistics Practice

| Field | Value |
|---|---|
| Parent | ACE-CON-STD-001 Contractor and Supplier Management Standard (until a LOG Standard exists) |
| Title OMS tags | 8.2, 3.6, 7.5 |
| Author | Sarita Sookram — Marine Lead |
| Reviewers | Lisa Williams — Logistics & Materials Manager; Brian Felix — Logistics Coordinator (Marine & Aviation); Kerwin Daniel — Marine & Helideck Coordinator; Jenelle Paul — Emergency Response & Security Manager |
| Endorser | Not required |
| Approver / Owner | Sasha George — VP Supply Chain Management |
| Control range | C-LOG-001 to C-LOG-039 |
| Pages | 20 to 26 |

**Must establish:**
- **The logistics model.** Point Lisas shore base → supply vessels and fast crew boats → Pommerac A, Chenet B and Sapodilla C. The helicopter route to the Pommerac A helideck.
- **Vessel and aircraft assurance.** Contractor vetting (IMCA-style vessel audits, aviation operator audits). Minimum crew competence.
- **Marine operations:**
  - weather limits;
  - personnel transfer (basket, gangway);
  - lifting at platforms;
  - unmanned platform visits (boarding rules, two-person minimum);
  - pipeline and platform patrol duties (the storyline: the leak was found on patrol).
- **Aviation:** helideck operations, manifesting, passenger briefing, flight following.
- **Cargo:** dangerous goods, deck cargo load plans, backloading of waste.
- **Emergency interfaces.** Standby vessel and medevac, linked to the Pommerac A ERP.
- **Implementing processes:**
  - ACE-LOG-PRS-001 Offshore Trip Planning and Manifesting (planned);
  - ACE-LOG-PRS-002 Vessel and Aircraft Assurance (planned).

### D6. ACE-HMA-PRA-001: Hydrocarbon Measurement and Allocation Practice

| Field | Value |
|---|---|
| Parent | ACE-STK-STD-002 Customer and Product Quality Standard (until an HMA Standard exists) |
| Title OMS tags | 9.5, 4.2, 2.3 |
| Author | Navin Sookdeo — Metering & Measurement Lead |
| Reviewers | Anjali Boodoo — Marketing Manager (Gas & Crude); Melissa Mitchell — JV & Partner Accounting Lead; Rohan Ali — Plant Manager - Central Processing Facility; Kerry-Ann Persad — Production Technology Lead |
| Endorser | Technical Leadership Council |
| Approver / Owner | Karen Jack — VP Business Development & Markets |
| Control range | C-HMA-001 to C-HMA-039 |
| Pages | 22 to 30 |

**Must establish:**
- **The measurement hierarchy:**
  - **fiscal/custody transfer:** the CPF gas sales meter to NGC, and crude lifting measurement;
  - **allocation:** well tests and platform meters;
  - **operational.**
- **Meter types and standards:** ultrasonic or orifice gas meters (AGA 9 / ISO 5167), crude metering and proving (API MPMS), sampling and analysis (gas chromatograph, BS&W).
- **Calibration, proving and verification frequencies.** Witnessing by NGC, the regulator and partners.
- **The allocation method.** Back-allocation from fiscal meters to fields and wells: Pommerac A, Chenet B, Sapodilla C and the land leases. JV partner shares.
- **Mismeasurement.** Reporting, correction and commercial settlement. Lost and unaccounted-for volumes (the storyline: volume lost from the pinhole leak).
- **Data integrity.** Flow computer audit trails and the production reporting deadlines (monthly and regulatory).
- **Implementing processes:**
  - ACE-HMA-PRS-001 Monthly Production Allocation (planned);
  - ACE-HMA-PRS-002 Meter Proving and Calibration (planned).

---

## Delivery checklist (per document)

- [ ] Started from template v5; file name `ACE-XXX-PRA-NNN_Title_With_Underscores_RevA.docx`
- [ ] Control table complete; people match `ACE_People.csv`; Framework text exact
- [ ] Title OMS tags in the control table **and** File › Info › Tags
- [ ] Every heading has an OMS tag line; primary tag first
- [ ] "Shall" only in the five binding styles
- [ ] Every ODS.RiskControl paragraph has a Control ID from your range
- [ ] Section 6 table lists the processes and procedures (planned is fine)
- [ ] Controls appendix complete
- [ ] `quick.py` passes; no `~$` files; uploaded to `drafts/` (not `finals/`)
