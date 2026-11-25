# ONE Document Standard

**Version 1.0, 25 November 2026.** How to write a controlled document for ONE, or convert an existing one, so that it passes the ONE gateway first time.

This standard is self-contained. Someone (or an AI tool) who has only this file, the ONE Word template and an old document should be able to produce a compliant draft. The rules here are the same ones the ONE checker applies; the full machine rules are in `one-protocol.json`.

Sections 1 to 10 apply to any company. Everything specific to Acme Caribbean Energy (codes, sites, functions, role titles) is in the appendices. To use this standard for another company, replace the appendices.

---

## 1. What you receive and what you hand back

**You receive:**

1. **The old document:** any format (Word, PDF, text). It may have no structure, no tags and mixed obligations.
2. **This standard.**
3. **The ONE template** (`ONE_ACE_Master_Template_v5.dotx`). It contains the cover, the document control table, the revision history, the approval table, the document map, the standard sections and all the styles. Its fields and tags are held in Word content controls that ONE reads.

**You hand back:**

1. **One Word document** (.docx) built from the template, at **Revision A, status Draft**.
2. **A conversion note** (section 11): what you changed, and what needs a decision from the document owner.

You do **not** fill in people or dates. Document Control completes those before approval (section 3).

---

## 2. Five principles

1. **Keep the meaning.** You are restructuring, not rewriting policy. Every obligation, limit, value, frequency and safety precaution in the old document survives with its full meaning. Never invent a requirement, and never drop one.
2. **Say what each paragraph is.** Every binding sentence goes in one of the five binding styles. Everything else is guidance, in a non-binding style. The word *shall* appears only in binding styles.
3. **Say what each section is for.** Every Heading 1 and Heading 2 is followed by a tag line naming the OMS expectations it serves (Appendix A).
4. **Name roles, not people.** Write "the Inspection Lead", never "Wayne Rajkumar". People change; roles stay. Use the exact job titles in Appendix C.
5. **Flag, don't guess.** If the old document is unclear (an obligation without an owner, a reference to a document that no longer exists, a missing value), keep what it says and list the question in the conversion note.

---

## 3. Start from the template

Open the template and save it as the new document. Keep every part of it. Do not delete content controls (the grey-bordered fields); type inside them.

### 3.1 Fields you fill in

| Field | What to enter |
|---|---|
| Document number | `ACE-SSS-TTT-NNN` (section 4). If the number is not known, keep `ACE-SSS-TTT-NNN` with the system and type filled in, e.g. `ACE-MNT-PRC-NNN`, and say so in the conversion note. |
| Title | Short and specific: what, not how. "Lifting Operations Procedure", not "Procedure for the safe conduct of all lifting operations". |
| Document type and Level | From section 4.1. |
| Revision | `A` |
| Status | `Draft` |
| Parent document | The document this one delivers. Usually the Standard above it. |
| Primary function | One function from Appendix B. |
| Framework | Leave the fixed text as it is. |
| Title OMS tags | One to three expectations for the document as a whole, primary first. |
| Classification | `Internal` unless the old document says otherwise. |
| Applies to | Sites and functions, using the site codes in Appendix B. |
| Review interval | Keep the template's text unless the old document sets a different one. |
| Role register | Every role named in the document, separated by `; `. |
| Cover summary line | One sentence saying what the document does. |

### 3.2 Fields you leave for Document Control

Leave these exactly as the template has them, with their square-bracket placeholders:

- Document owner, Process owner, Custodian, Author, Reviewers, Endorser, Approver
- Issue date and Effective date
- The *Named person* column of the roles table, and the people in the approval table

The checker reports these as **"to be completed before approval"**. In a draft that is expected and is not a failure.

### 3.3 Revision history

One row: Revision `A`, date left blank, description "Converted to the ONE document standard from <old title and number>."

---

## 4. Number, type and level

### 4.1 Choosing the type

Decide by what the document does, not by what the old one was called.

| Type | Code | Level | Choose it when the document… |
|---|---|---|---|
| Manual | MAN | 1 | describes the whole management system |
| Policy | POL | 1 | states intent and commitments, signed by the top of the company |
| Standard | STD | 2 | sets what must be achieved in an area, and by whom, without saying step by step how |
| Practice | PRA | 2 | sets how a discipline does its technical work (methods, criteria, intervals) |
| Specification | SPC | 2 | sets technical requirements for equipment, materials or design |
| Process | PRS | 3 | describes a business process as a flow of steps between roles (needs a process model file as well) |
| Procedure | PRC | 4 | gives the steps for a task or activity that several people carry out |
| Plan | PLN | 4 | sets out arrangements for a specific situation (emergency, campaign, project) |
| Work Instruction | WIN | 5 | gives the steps for one task at the point of use |
| Form | FRM | 5 | is a form or checklist to be filled in |
| Register | REG | 5 | is a list kept up to date (a register or log) |
| Guideline | GDL | – | gives advice only. **A guideline may not contain binding styles.** |

If the old document mixes levels (for example, a "procedure" that is mostly requirements), choose the type that fits most of it and note the rest in the conversion note as a possible split.

### 4.2 The number

`ACE-SSS-TTT-NNN`, plus `-LLL` for a site-specific document.

- `SSS` is the system code (Appendix B), chosen by subject.
- `TTT` is the type code from 4.1.
- `NNN` is a sequence number given by Document Control.
- `LLL` is a site code (Appendix B), only when the document applies to one site.

File name: `<number>_Title_Words_RevA.docx`, e.g. `ACE-MNT-PRC-NNN_Lifting_Operations_Procedure_RevA.docx`.

---

## 5. Structure

### 5.1 Front matter (from the template, always)

Cover; Document control; Revision history; Approval and issue; Document map. Keep their headings and tag lines as they are.

### 5.2 Body sections by type

Use the template's numbered sections and adapt them. Map every part of the old document to one of them. Nothing is lost: if old content does not fit, it goes in the nearest section or an appendix.

| Section | Standard, Practice, Specification | Procedure, Plan, Work Instruction |
|---|---|---|
| 1 | Purpose, scope and parent document | Purpose, scope and parent document |
| 2 | Roles and technical authority (table: Role, Named person, Accountability) | Roles (same table) |
| 3 onwards | The requirements or the method, one section per topic | Before you start; the steps; completing the work |
| next | Records, data and systems | Records |
| next | Performance and verification | (optional) |
| next | Implementing processes and procedures (table, required for STD and PRA) | Related documents |
| Appendix A | Controls established by this document (table) | Controls established by this document, if any |
| further appendices | Definitions, worked examples, forms | Checklists, forms |

### 5.3 Headings

- **Heading 1** for numbered sections, **Heading 2** for sub-sections, **Heading 3** for minor headings.
- Number headings in the text: `3 Inspection planning`, `3.2 Setting intervals`.
- Do not use bold Normal text as a heading. ONE only sees real heading styles.

---

## 6. OMS tags

### 6.1 Where they go

Directly under every Heading 1 and Heading 2 there is one paragraph in the **ODS Tag Line** style. It holds the tags for that section: `OMS 6.5, 6.4`.

- In the template, the tag line under each existing heading already contains a content control. Type the tags inside it.
- To add a section, **copy an existing heading together with its tag line**, then change the text. The copy brings the tag control with it.
- If you cannot keep the controls (for example, the tool you use cannot copy them), type the tag line as plain text in the ODS Tag Line style: `OMS 6.5, 6.4`. The ONE Fix step turns it into a control. This is the **LITE** format and is acceptable for a draft.

### 6.2 How to choose tags

- **One to three tags** per section. The first is the **primary**: the expectation the section mainly serves.
- Tag what the section *does*, not every word it mentions. A section on inspection intervals is `6.5`; that it mentions records does not make it `1.7`.
- Tags are **not inherited**. Each Heading 1 and Heading 2 gets its own, even if they repeat the parent's.
- Only the 54 tags in Appendix A are valid. Write them as numbers, e.g. `5.3`, never as names.
- Standard front sections: Document control `1.7`; Revision history `1.7`; Approval and issue `2.2, 1.7`; Document map `7.1`.

---

## 7. Styles: what every paragraph is

### 7.1 The five binding styles

A paragraph is **binding** when it obliges someone to do something, or forbids something. Binding paragraphs use one of five styles. Each holds **one obligation**.

| Style | Use for | Write it as |
|---|---|---|
| ODS.Requirement | something that must be done or must be true | "Each pressure vessel **shall** have a written scheme of examination." |
| ODS.Responsibility | a duty given to a role | "The Inspection Lead **shall** approve inspection intervals." |
| ODS.ApprovalRequirement | something that needs someone's approval before it happens | "Interval extensions **shall** be approved by the Technical Authority before the due date." |
| ODS.RecordRequirement | a record that must be kept | "Inspection results **shall** be recorded in the CMMS within 10 working days and kept for the life of the equipment." |
| ODS.RiskControl | a control: an action that prevents or limits a hazard (section 8) | "The Control Room Operator **shall** test the high-level trip every six months (C-OPS-901)." |

**Binding words.** Convert "must", "is required to", "will" (when it means an obligation), "is to" and "are responsible for" into **shall** in a binding style. Use **shall not** for prohibitions.

**One obligation per paragraph.** Split sentences that hold two duties for two roles, or two different actions.

**The subject is a role or a thing.** "The Area Authority shall…" or "Each permit shall…". Not "We shall…", not "Staff shall…" (say which staff).

### 7.2 Non-binding styles

| Style | Use for |
|---|---|
| Normal | explanation, background, context |
| ODS.Note | a note that helps the reader but obliges no one |
| ODS.Warning | a hazard warning, written as a plain instruction: "Do not open the valve while the line is pressurised." No *shall*. |
| ODS.ProcedureStep | a numbered step in a procedure. Steps are instructions ("Close valve V-101."), not *shall* statements. |
| ODS.Definition | a defined term: "**Area Authority:** the person accountable for…" |
| ODS.DocumentReference | a reference to another company document, by number |
| ODS.ExternalStandard | a reference to an external standard, by number and title. Do not quote it. |
| ODS.PerformanceIndicator | a measure, with its target |
| List Bullet | list items that are not obligations |

### 7.3 Rules that the checker enforces

- **"Shall" only in the five binding styles.** Not in Normal, notes, warnings, steps or **table cells**. If a table in the old document contains obligations, either move each obligation into a binding paragraph after the table, or reword the cell as a description ("Approves interval extensions").
- **"Should" and "may" are not binding.** Leave them in Normal or a note. If the old document clearly meant an obligation, make it a *shall* and list it in the conversion note.
- **No manual formatting** to imitate a style (bold, colour, indents). ONE reads styles, not appearance.

---

## 8. Controls

A **control** is a specific action, check or physical safeguard that prevents a hazardous event or limits its consequences, with an owner and evidence that it was done. "Test the trip every six months" is a control. "Comply with all procedures" is not.

1. Write each control as one **ODS.RiskControl** paragraph in the section where it belongs.
2. End it with its Control ID in brackets: `(C-SSS-NNN)`, where SSS is the system code.
3. **In a draft, number new controls from 901 upwards** (`C-MNT-901`, `C-MNT-902`…). The OMS Manager gives final numbers at approval.
4. List every control in **Appendix A — Controls established by this document**: Control ID, short statement, risk or threat addressed, section, process step, evidence or record.
5. In the template, each Control ID sits in a content control. If you copy the template's sample control paragraph, the control comes with it. Plain-text IDs are acceptable in a draft (LITE); Fix converts them.

Only mark something as a control if the old document makes it an obligation. Do not create controls the old document does not have; suggest them in the conversion note instead.

---

## 9. Roles, people and references

- **Roles in the text:** use the exact job titles in Appendix C, or the OMS duties (Area Authority, Technical Authority, Performing Authority, Isolating Authority…). If the old document names a person, replace the name with their role and note it.
- **Roles table (section 2):** one row per role used in the document: Role, Named person (left as a placeholder), Accountability (one line).
- **Other company documents:** cite by number, e.g. `ACE-COW-STD-001`, with a section if useful: `ACE-COW-STD-001 §4.2`. Keep references to documents that are not yet issued; list them in the conversion note.
- **External standards:** number and title only, e.g. "API 510 Pressure Vessel Inspection Code". Do not reproduce their text.

---

## 10. Things that must not happen

- A requirement, limit, value, interval or safety precaution is changed or dropped.
- *Shall* appears in a non-binding style or a table cell.
- A heading has no tag line, or a tag is not one of the 54.
- A person's name appears in body text.
- Content controls from the template are deleted.
- Tracked changes or comments are left in the file.
- Images are linked from outside the file instead of embedded.

---

## 11. The conversion note

Hand back a short note with the document. Use these headings:

1. **Source:** old title, number, revision and date.
2. **Type and number chosen,** and why.
3. **What changed:** sections merged, split or moved; obligations reworded to *shall*; names replaced by roles.
4. **Decisions needed from the owner:** obligations without a clear owner; *should* statements made binding; values that look out of date; references to documents that do not exist; suggested controls; content that may belong in another document.
5. **Self-check:** confirm each item in section 12.

---

## 12. Self-check before handing back

- [ ] Built from the template; front matter complete; Revision A, status Draft.
- [ ] Fields in 3.1 filled; fields in 3.2 left as placeholders.
- [ ] Every Heading 1 and Heading 2 has a tag line with one to three valid tags, primary first.
- [ ] Every obligation is in a binding style, one per paragraph, using *shall*.
- [ ] *Shall* appears nowhere else, including tables.
- [ ] Every control is an ODS.RiskControl paragraph with a Control ID, and listed in Appendix A.
- [ ] Roles use the exact titles in Appendix C; no names of people in the text.
- [ ] Every requirement, value and precaution from the old document is still there.
- [ ] Conversion note written.

---

## 13. How the draft is checked

The ONE checker reads the Word file and gives one of three results:

| Result | Meaning |
|---|---|
| PASS | Ready for review and approval. Draft placeholders are listed as "to be completed". |
| PASS AFTER FIX | Everything that is wrong can be corrected automatically (for example plain-text tags in the LITE format). |
| FAIL | Something needs a person: usually *shall* in the wrong place, an invalid tag, or a missing section. |

The checker does not judge whether the tags are well chosen or whether the meaning is kept. That is the owner's review.

---

## Appendix A — The 54 OMS expectations (valid tags)

The ten elements and their expectations, based on IOGP Report 510, *Operating Management System Framework* (2014), © IOGP and IPIECA, as worded in the ACE OMS Manual (ACE-OMS-MAN-001).

**1 Commitment and accountability**

| Tag | Expectation | What it covers |
|---|---|---|
| 1.1 | Leading OMS across ACE | OMS is how ACE runs its business, not a project beside it. |
| 1.2 | A culture of safe, reliable and accountable work | Leaders set the tone by what they pay attention to. |
| 1.3 | Everyone committed to OMS and the law | Every employee and contractor commits to working within OMS and within the laws that apply to ACE's licences and sites. |
| 1.4 | Our Code of Conduct | The ACE Code of Conduct sets out how we behave: honestly, safely, fairly and within the law, including on gifts, conflicts of interest and speaking up. |
| 1.5 | OMS duties built into every role | OMS accountabilities are written into role profiles, delegated authorities and performance goals, so that OMS is part of the job and not extra to it. |
| 1.6 | Keeping OMS visible | We keep OMS in front of people through regular, consistent communication: shift briefings, toolbox talks, the OMS web portal, newsletters and leadership messages. |
| 1.7 | Controlled documents and records | OMS documents are controlled so that only the current approved version is in use, and records are kept, retained and archived in a planned way. |
| 1.8 | Learning to reduce risk | We actively look for lessons inside ACE and from the wider industry, and use them to reduce risk and improve how we work. |

**2 Policies, standards and objectives**

| Tag | Expectation | What it covers |
|---|---|---|
| 2.1 | Setting and sharing policies, standards and objectives | ACE's expectations are written down in one hierarchy of policies, standards and procedures, and shared with everyone who needs them through the OMS web portal. |
| 2.2 | Approval at the right level | Policies are approved by the CEO, standards by system owners and procedures by managers. |
| 2.3 | Risk-based standards that meet the law | ACE standards are based on our risks and meet or exceed the legal and other requirements that apply to us, including licence conditions and permits for the Gulf of Paria and land operations. |
| 2.4 | Objectives we can measure | Every year ACE sets OMS objectives with clear targets: improvements to the system, performance targets and compliance goals. |
| 2.5 | Working with partners | Where ACE shares licences or facilities with partners, we agree how policies and standards apply so that people on site get one consistent message. |
| 2.6 | Deviations and exemptions | Sometimes a standard cannot be met. |

**3 Organisation, resources and capability**

| Tag | Expectation | What it covers |
|---|---|---|
| 3.1 | Clear roles, accountabilities and authorities | ACE's organisation is designed so that every OMS accountability has an owner, including the Area Authorities who control our locations and the Technical Authorities who set our technical standards. |
| 3.2 | Planning our workforce | We plan ahead for the people we need: recruitment, graduate and apprentice intake, career development, retention and succession for critical roles. |
| 3.3 | Competence assurance | Competence means having the skills, knowledge, behaviours and fitness to do a job safely. |
| 3.4 | The right resources | We match people, equipment and budget to our objectives and risks, using in-country suppliers and services wherever practicable. |
| 3.5 | Consulting our workforce | People who do the work know where the risks are. |
| 3.6 | Contractors and suppliers | Much of ACE's work is done by contractors: rigs, well services, supply boats, maintenance and construction. |

**4 Stakeholders and customers**

| Tag | Expectation | What it covers |
|---|---|---|
| 4.1 | Knowing and engaging our stakeholders | We identify the people affected by our activities across the life of each asset: communities near the land leases and the CPF, fishers in the Gulf of Paria, landowners, regulators and customers. |
| 4.2 | Managing stakeholder and customer risks | We manage the risks our activities create for stakeholders and customers, from noise and traffic near well pads to gas quality at the Gas Buyer delivery point. |
| 4.3 | Listening and responding | Feedback, including complaints, is logged, assessed and answered. |
| 4.4 | Two-way relationships | We build trust before we need it, including by preparing communities and authorities for how we would respond together in an emergency. |

**5 Risk assessment and control**

| Tag | Expectation | What it covers |
|---|---|---|
| 5.1 | Assessing risk and putting barriers in place | ACE uses one risk management process for every kind of risk: understand the context, identify hazards, assess risk with the ACE Risk Matrix, and put prevention and recovery barriers in place until the risk is as low as reasonably practicable. |
| 5.2 | Recording and reviewing significant risks | Significant risks are recorded in asset and corporate risk registers, with the level of management that must accept them set by their position on the Risk Matrix. |
| 5.3 | Managing change | Any change to plant, process, people, procedures or organisation that could affect risk goes through Management of Change. |
| 5.4 | Staying alert to rising risk | Serious accidents are usually preceded by weak signals: small deviations, repeated alarms, workarounds and backlogs. |

**6 Asset design and integrity**

| Tag | Expectation | What it covers |
|---|---|---|
| 6.1 | Designing with the right information | Site selection, design and equipment choices are based on sound baseline data and the findings of hazard studies, from the shallow waters of the Gulf of Paria to the land leases. |
| 6.2 | Engineering standards through the asset life | ACE engineering standards cover design, construction, commissioning, modification and decommissioning. |
| 6.3 | Staying inside operating limits | Every system has an operating envelope. |
| 6.4 | Safety-critical elements | Safety-critical elements are the equipment and systems that prevent or limit a major accident: emergency shutdown, fire and gas detection, relief valves, well barriers and more. |
| 6.5 | Maintenance, inspection and testing | Maintenance, inspection, testing and calibration are planned at risk-based intervals and done on time. |
| 6.6 | Buying and selling assets | Before ACE buys or sells an asset, lease or interest, we check its integrity, liabilities and risks so that there are no surprises. |

**7 Plans and procedures**

| Tag | Expectation | What it covers |
|---|---|---|
| 7.1 | Writing plans and procedures | Procedures and plans are written for the people who use them, in ACE templates, at a level of detail that matches the risk of the task and the legal requirements. |
| 7.2 | Approving plans and procedures | Every plan and procedure, and every revision, is approved by someone with the authority to do so. |
| 7.3 | Training people to use procedures | People are trained in the procedures they use, and supported by guidance, coaching and competence checks. |
| 7.4 | The current version wherever work is done | The current approved version of every plan and procedure is available where the work is done: on Pommerac A, at the CPF, on the land leases and at Point Lisas, through the OMS web portal and controlled copies. |
| 7.5 | Emergency and continuity plans | ACE has emergency response plans for each site, an oil spill contingency plan for the Gulf of Paria and a business continuity plan. |

**8 Execution of activities**

| Tag | Expectation | What it covers |
|---|---|---|
| 8.1 | Ready before we start | Before start-up, handover or a new activity, we check that equipment, people, procedures and permits are ready, and that handovers between shifts and teams are clear. |
| 8.2 | Doing the work as planned | Work is carried out under Control of Work: permits to work, isolations, simultaneous operations controls and task risk assessments, applied the same way by staff and contractors at every site. |
| 8.3 | Supervision that checks the work | Supervisors are present, check that work follows the plan and the permit, and confirm that it achieved what was intended. |
| 8.4 | Stop work | Everyone at ACE, staff and contractors, can and must stop work when a risk is not adequately controlled. |
| 8.5 | Recognising good work and correcting poor work | We recognise people who work safely and speak up, and we deal fairly and consistently with behaviour that puts people or plant at risk. |

**9 Monitoring, reporting and learning**

| Tag | Expectation | What it covers |
|---|---|---|
| 9.1 | Monitoring and verification | We monitor operations, measure performance and verify that OMS requirements are being met, through routine checks, inspections and self-assessments. |
| 9.2 | Reporting and investigating incidents | Incidents, near misses and non-conformances are reported, classified and investigated to find the root causes, not just the people involved. |
| 9.3 | Learning and closing actions | Lessons from ACE incidents, audits and the wider industry lead to actions, and actions are tracked until their effectiveness is verified. |
| 9.4 | Leading and lagging indicators | ACE uses lagging indicators to see outcomes and leading indicators to see whether barriers and processes are working. |
| 9.5 | Reliable data | Decisions are only as good as the data behind them. |

**10 Assurance, review and improvement**

| Tag | Expectation | What it covers |
|---|---|---|
| 10.1 | A risk-based assurance programme | ACE runs a planned assurance programme across three lines: checks by the line, conformance assessments by the OMS team, and independent audits by Internal Audit. |
| 10.2 | Reviewing performance | Performance data is brought together and interpreted so that leaders can review it, compare ACE with industry peers and report to the Board, partners and regulators. |
| 10.3 | Finding weak controls | We analyse indicators, incidents and audit findings together to find weak controls and opportunities to improve. |
| 10.4 | Planned improvement | Findings, lessons and good practices feed a planned programme of OMS improvements, which is communicated to the people affected. |
| 10.5 | Leadership review of the whole system | Once a year the Executive Leadership Team steps back and asks whether OMS is still working, still suits ACE, and is getting more mature. |

## Appendix B — Company codes (Acme Caribbean Energy)

Replace this appendix to use the standard for another company.

**Document number prefix:** `ACE`. **Framework text (fixed):** `IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 04`. **Company name:** Acme Caribbean Energy Limited.

### B.1 System codes

| Code | System | Elements |
|---|---|---|
| LDR | Leadership and Conduct | 1 |
| OMS | OMS Governance and Deviations | 1, 2, 10 |
| LEG | Legal and Regulatory Compliance | 2 |
| PPL | People, Organisation and Competence | 3 |
| CON | Contractors and Supply Chain | 3, 8 |
| STK | Stakeholders, Community and Customers | 4 |
| RSK | Risk Management and the ACE Risk Matrix | 5 |
| PSM | Process Safety and Hazard Studies | 5, 6 |
| MOC | Management of Change | 5 |
| PRJ | Projects and Engineering Delivery | 6 |
| ENG | Engineering Standards and Technical Authority | 6 |
| AIM | Asset Integrity and Inspection | 6 |
| MNT | Maintenance Management | 6, 8 |
| WEL | Well Integrity | 6, 8 |
| OPS | Operations and Operating Limits | 6, 7, 8 |
| COW | Control of Work | 8 |
| EMR | Emergency, Crisis and Continuity | 7 |
| DOC | Information, Documents and Records | 1, 7, 9 |
| INC | Incidents and Learning | 9 |
| PRF | Performance, Assurance and Review | 9, 10 |
| ENV | Environment | 2, 5, 9 |
| OHH | Occupational Health | 3, 5 |
| SEC | Security | 5, 7 |
| BPM | Business Process Management | 1, 2, 3, 7, 10 |
| LOG | Marine and Aviation Logistics | 3, 7, 8 |
| HMA | Hydrocarbon Measurement and Allocation | 2, 4, 9 |
| FIN | Finance and Financial Control | 2, 3 |

### B.2 Site codes

| Code | Site |
|---|---|
| HOF | Head Office (corporate office) |
| PLB | Point Lisas Shore Base (marine base and warehouse) |
| PAP | Pommerac A (offshore production platform) |
| CHB | Chenet B (wellhead platform) |
| SAP | Sapodilla C (wellhead platform) |
| CPF | Central Processing Facility (crude and gas processing plant) |
| LND | Land leases (tamarind, pawpaw and soursop leases) |

### B.3 Functions

- CEO Office
- Exploration & Development
- Wells
- Engineering & Projects
- Operations
- HSE & Compliance
- Finance
- Human Resources
- Supply Chain Management
- IT, Data & Knowledge
- Business Development & Markets
- Communications & Corporate Services
- Legal & Government Affairs

## Appendix C — Roles (Acme Caribbean Energy)

Use these titles exactly. They come from the company role catalogue (`company/org/roles.csv`), which is the master list.

### C.1 OMS duties

These are carried by several job roles and may be used in text as they are.

| OMS duty | What it means |
|---|---|
| Area Authority | Accountable for everything that happens at a location: plant status, permits, simultaneous operations and release of work. |
| Technical Authority | Discipline lead who owns the technical standards of a discipline and endorses designs, changes and deviations, independent of line management. |
| Performing Authority | Leads a work party: accepts the permit, briefs the crew, monitors the work and hands the worksite back. |
| Isolating Authority | Authorised to prepare, apply and verify energy isolations and to reinstate plant. |
| Permit to Work Coordinator | Runs the permit office at a site: checks permits, keeps the isolation register and plans simultaneous operations. |
| Well Control Authority | ACE's representative at the wellsite, with authority over well control on the rig. |
| Element Owner | Executive who owns one of the ten OMS elements: its expectations, its performance and its improvement. |
| Document Owner | Accountable for a controlled document: its content, its review on time and its revision. |
| Document Controller | Registers, checks, publishes and revises controlled documents. |
| Risk Owner | Accountable for a risk in the register: its assessment, its controls and its actions. |
| Control Owner | Accountable for one control: that it is in place, tested and working. |
| Process Owner | Accountable for a business process: its design, its performance and its improvement. |
| MOC Coordinator | Screens and tracks changes through the Management of Change process. |
| Emergency Response Coordinator | Keeps emergency plans, drills and the response organisation ready. |
| Auditor | Independent check that the OMS works as written. |
| OMS Manager | Custodian of the OMS framework and its mapping to the ten elements; runs conformance assessments. |

### C.2 Job titles by function

| Function | Job titles |
|---|---|
| CEO Office | Chief Executive Officer; Head of Internal Audit & Risk Assurance; Manager, Strategy & Planning; Internal Auditor; Strategy & Planning Analyst; Executive Assistant to the CEO |
| Exploration & Development | VP Exploration & Development; Development & Reservoir Manager; Exploration Manager; Geology Lead; Geophysics Lead; Petrophysics Lead; Production Technology Lead; Reservoir Engineering Lead; Reserves Coordinator; Senior Geomodeller; Geologist; Geophysicist; Petrophysicist; Production Technologist; Reservoir Engineer; Subsurface Data Coordinator |
| Wells | VP Wells; Completions & Well Intervention Manager; Drilling Manager; Completions Lead; Drilling Engineering Lead; Well Integrity Lead; Drilling Supervisor (Wellsite); Completions Engineer; Drilling Engineer; Fluids & Cementing Engineer; Well Integrity Engineer; Well Services Coordinator; Wells Planning & Cost Engineer; Wells Administrator |
| Engineering & Projects | VP Engineering & Projects; Manager, Technical Excellence; Projects Manager; Cost & Planning Lead; Electrical Lead; Fire & Gas and Safety Systems Lead; Instrumentation & Control Lead; Materials & Corrosion Lead; Metering & Measurement Lead; Pipelines Lead; Piping Lead; Process Engineering Lead; Static Mechanical Lead; Structural & Civil Lead; Subsea Lead; Project Manager; Electrical Engineer; Instrumentation & Control Engineer; Mechanical Engineer; Pipeline Engineer; Process Engineer; Project Controls Analyst; Project Engineer; Structural Engineer; CAD Designer; Engineering Document Controller |
| Operations | VP Operations; Land Operations Manager; Maintenance & Integrity Manager; Offshore Operations Manager (Gulf of Paria); Plant Manager - Central Processing Facility; Inspection Lead; Maintenance Superintendent; Offshore Installation Manager; Production Chemistry Lead; Reliability & Maintenance Lead; Rotating Equipment Lead; Field Supervisor (Land); Offshore Production Supervisor; Shift Supervisor (CPF); Crude Loading & Custody Transfer Coordinator; Inspection Engineer; Integrity Engineer; Laboratory Chemist; Maintenance Planner; Operations Engineer (CPF); Operations Engineer (Land); Operations Engineer (Offshore); Operations Training & Competence Coordinator; Permit to Work Coordinator (CPF); Permit to Work Coordinator (Offshore); Production Data Analyst; Reliability Engineer; CMMS Administrator; Control Room Operator (CPF); Control Room Operator (Offshore); Corrosion Technician; Deck & Crane Operator; Electrical & Instrument Technician; Field Operator (CPF); Lease Operator; Marine & Helideck Coordinator; Mechanical Technician; Offshore Medic; Operations Administrator; Operations Document Controller; Pipeline & Gathering Technician; Production Technician (Offshore) |
| HSE & Compliance | VP HSE & Compliance; Compliance & Assurance Manager; Emergency Response & Security Manager; HSE Manager; Environmental Lead; Human Factors Lead; OMS Manager; Occupational Health & Hygiene Lead; Process Safety Lead; Emergency Response Coordinator; Environmental Specialist; HSE Adviser; HSE Auditor; Industrial Hygienist; Occupational Health Nurse; Process Safety Engineer; Regulatory Compliance Specialist; Security Coordinator |
| Finance | Chief Financial Officer; Financial Controller; Planning & Budgeting Manager; JV & Partner Accounting Lead; Tax Manager; Accountant; Financial Analyst; Hydrocarbon Accountant; Royalty & Fiscal Reporting Analyst; Treasury Officer; Accounts Payable / Receivable Officer |
| Human Resources | VP Human Resources; Learning & Competence Manager; HR Business Partner; Industrial Relations Specialist; Competence Assurance Coordinator; Talent Acquisition Specialist; Training Coordinator; HR Assistant; Payroll & Benefits Officer |
| Supply Chain Management | VP Supply Chain Management; Contracts Manager; Logistics & Materials Manager; Procurement Manager; Marine Lead; Quality Lead; Warehouse Supervisor; Buyer; Contracts Engineer; Local Content Specialist; Logistics Coordinator (Marine & Aviation); Storekeeper |
| IT, Data & Knowledge | VP IT, Data & Knowledge; Data & Applications Manager; IT Infrastructure & Operations Manager; Information Management Lead; Telecoms & OT Cyber Security Lead; Data Engineer; Document Controller; GIS & Subsurface Data Administrator; Knowledge Management Specialist; Network Engineer; Technical Writer / Procedures Specialist; IT Support Analyst |
| Business Development & Markets | VP Business Development & Markets; Marketing Manager (Gas & Crude); New Ventures Manager; Partner Relations Lead; Petroleum Economist; Commercial Analyst; Market Analyst |
| Communications & Corporate Services | VP Communications & Corporate Services; Communications Manager; Facilities & Administration Manager; Community Relations Officer; Corporate Communications Specialist; Facilities Coordinator; Office Administrator; Travel & Accommodation Coordinator |
| Legal & Government Affairs | VP Legal & Government Affairs (General Counsel); Corporate Secretary; Government Affairs Manager; Senior Counsel, Contracts & Commercial; Counsel, Regulatory & Licensing; Licensing & Regulatory Specialist; Paralegal |
