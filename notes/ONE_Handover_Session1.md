# ONE / ACE — Handover Document (end of Session 1)

**Prepared:** 23 November 2026 · **For:** Wilmark (Cynmark Systems Limited) and the next working session
**Read with:**
- `ONE_Writer_Brief_Standard_Practices.md`: the 10 Practices for writers;
- `ACE-DOC-STD-002_Rev02_Draft_Publishing_Standard.md`: the rewritten rules for the new slate;
- `ONE_Session1_Pack.zip`: all scripts, data and outputs from this session.

**To restart next session:** upload this file, the two MD files above and the zip, and say "continue ONE from the handover". The repository is **SCMWJTT/OMS** (public). Unzip the pack into `/home/claude/`, because the scripts use fixed paths (Section 13).

---

## 1. What ONE is, in one paragraph

**ODS/ONE** turns approved Word documents into a navigable OMS web system. Authors write in Word using a template with:
- semantic styles;
- OMS tag content controls under every heading;
- controlled properties.

A **gateway** checks every file. ONE then builds web views automatically from the repository: the OMS wheel, library, reader, element pages, roles, document map and gateway report, and later processes, controls and an animated dashboard. Nothing is re-keyed: **the document archive drives everything**.

- **Target site:** oms.cynmark.app.
- **Branding:** "OMS – One Management System", possibly shortened to "ONE" (undecided).
- **The problem it solves:** big-company OMS repositories add OMS linkage after the fact and end up falling back to PDFs.

## 2. Where things stand

| Area | Status |
|---|---|
| Fictional company ACE | Done: 300 people, org chart, company profile |
| OMS Manual | Rev 03 done (Word + web viewer). **Rev 04 changes specified (Section 8)** |
| 30-document priority list | Done |
| Documents in repo | 16 in `finals/` + 3 in `manuals/`, all pass the gateway after the fixes |
| Template | v4 in repo. **v5 specified** (Writer Brief, Section 0.3) |
| Library web site (ONE_Library.html) | Working prototype, built here by hand; **not live** on GitHub/oms.cynmark.app |
| Publishing standard | Rev 01 issued. **Rev 02 drafted** (separate MD) |
| Process layer, Practices | Designed and briefed; not yet written |
| Data spine, dashboard, Word add-in, Inspector app | Designed or discussed only |

**Decision taken now: start the next session with a new slate.** Every document is reissued against DOC-STD-002 Rev 02 and template v5 (plan in Section 9).

## 3. Inventory: what exists and where

### 3.1 GitHub, SCMWJTT/OMS (the user's master copies)

| Path | Files |
|---|---|
| `finals/` | ACE-AIM-STD-001, CON-STD-001, COW-STD-001, DOC-POL-001 (Rev A), DOC-PRC-001 (Rev A), DOC-STD-001, DOC-STD-002, EMR-STD-001, INC-STD-001, LDR-POL-001, MNT-STD-001, MOC-PRC-001, OMS-STD-002, PRF-STD-002, PSM-STD-001, RSK-STD-001 (all Rev 01 unless stated, effective 1 Jan 2026) |
| `finals/images/` | logo.png, logo_lg.png |
| `manuals/` | ACE-OMS-MAN-001 Rev 03; ACE-ENG-STD-901 Rev 01; ACE-ENG-SPC-410 Rev 01 |
| `templates/` | ONE_ACE_Master_Template_v4.dotx; ONE_ACE_Master_Template_Preview.docx |

**Housekeeping still open in the repo:**
- Delete `finals/~$E-MOC-PRC-001…docx` (a Word lock file).
- Move ENG-STD-901 and ENG-SPC-410 from `manuals/` to `finals/`.
- Create the folders `drafts/`, `processes/`, `registers/` and `superseded/`.
- Confirm what DOC-POL-001 and DOC-PRC-001 are. Their file names are generic ("Policy", "Procedure").

### 3.2 Session workspace, all in `ONE_Session1_Pack.zip`

| Folder | Contents | Purpose |
|---|---|---|
| `ace/` | `roles.py`, `gen.py` (seed 20261121), `build_xlsx.py`, `ace.json`, `out/ACE_Organisation.xlsx`, `out/ACE_People.csv`, `out/ACE_Org_Chart.html`, `out/ACE_Company_Profile.md`, `site/` | The ACE company. **`ACE_People.csv` is the master list for names and titles** |
| `oms/src/` | `brand.py`, `register.py` (document register + 23 systems), `elements.py` (54 expectations), `parts.py`, `build_docx.py`, `viewer.tpl`, `build_viewer.py`, `doclist.py`, `build_list.py` | Builds the Manual (Word), the Manual web viewer and the priority list |
| `oms/out/` | Manual Rev 03 (.docx/.pdf, generated version), `ACE_OMS_Manual_Web.html`, priority list (.xlsx/.csv), `ACE_OMS_Priority_Documents.md` | Outputs |
| `oms/img/` | Cover wheel and element graphics | Manual graphics |
| `audit/` | `inv.py` (inventory), `cmp.py` (table vs properties vs people), `fix.py` (rebuilds properties from the control table, adds `doc_title`, fixes people and wording), `fix_inc.py`, `quick.py` (fast full check of any .docx), `ACE_Authoring_Errors_to_Avoid.md`, the findings report, change logs, `manual/` (the user's Manual Rev 03 with logo, re-dated), `template/` v3, `batch3/` (template v4 + 2 fixed docs) | The gateway checks and fixes |
| `site/` | `build_index.py` (reads the repo copy → `index.json`), `build_site.py`, `site.tpl`, `ONE_Library.html` | The ONE library prototype |

## 4. Decisions made (keep these)

1. **Word is the source.** Web views are derived. Only approved, gateway-passed revisions are published.
2. **Framework:** IOGP Report 510 (2014): 10 elements, 54 expectations ("E" = expectation). Credit IOGP/IPIECA, quote minimally, write to the spirit. Align with ISO/DIS 29501/29502 and ISO 29011.
3. **The ACE OMS Manual numbering follows IOGP:** sections 1.1 to 10.5 = the expectations. These are the OMS tags.
4. **Tags:**
   - a content control (alias "OMS Tags", tag `ODS.OMSTags@<bookmark>`) in a tag line under each heading;
   - scope runs to the next heading of the same or higher level;
   - not inherited;
   - primary tag first;
   - the title's tags are attached to the `doc_title` bookmark.
5. **Metadata:** the control table is the master. Custom property names are fixed (22, plus `ODS.Parent` from v5 = 23). The built-in Word panel mapping is fixed (DOC-STD-002 Rev 02, Section 5.3); the panel layout itself cannot be changed.
6. **"Shall"** only in ODS.Requirement, Responsibility, ApprovalRequirement, RecordRequirement and RiskControl.
7. **Numbering:** `ACE-SSS-TTT-NNN[-LLL]`. Revisions use letters for drafts and digits for approved issues. Engineering uses discipline blocks 100 to 900, and the framework standard is ENG-STD-**901** (renamed from 001).
8. **Effective date of the Wave 1 set:** 1 January 2026. The Manual was changed to match, rather than the documents.
9. **Process layer:**
   - processes sit between Standards/Practices and Procedures;
   - each has one **process owner (accountable for continuous improvement)**, one primary function and one governing Policy, traced up to strategy, mission, vision and values;
   - levels follow APQC PCF style (L1 Category to L5 Task);
   - each process is stored as a JSON model with an HTML reader;
   - simulation and animation are on the back burner, but the fields are captured now.
10. **New types and systems:** PRA (Practice) and PRS (Process); systems **BPM**, **LOG** and **HMA**.
11. **Controls are the hinge** of the data spine. Control IDs `C-SSS-NNN` are written into ODS.RiskControl paragraphs.
12. **App deliverables are installers** (for example a Windows Setup .exe), never npm or terminal. Keep explanations short and in plain language.

**Proposed: confirm next session.**
- **a.** BPM system owner: Manager, Strategy & Planning (Gary Ho Sing). The alternative is the VP Operations.
- **b.** The five-level hierarchy (Practice at Level 2, Process Level 3, Procedure/Plan Level 4, WIN/FRM/REG Level 5). The Manual Rev 03 used four levels.
- **c.** PRS = Word process description + JSON model as a pair.
- **d.** The story calendar (Section 10).
- **e.** "ONE" rebrand: undecided.

## 5. Specifications (summary; full text in DOC-STD-002 Rev 02 draft)

- **Custom properties (23):** ODS.DocumentId, Title, DocumentType, Level, Revision, Status, IssueDate, EffectiveDate, Author, Reviewer, Endorser, Approver, DocumentOwner, ProcessOwner, Custodian, PrimaryFunction, Framework, TitleOMSTags, Classification, Applicability, ReviewInterval, RoleRegister, **Parent**.
- **Metadata appears in five places:** the cover, the control table (`ODS.Meta.*`), custom properties, built-in properties, and header/footer. All must agree with the control table.
- **Type codes:** MAN, POL, STD, **PRA**, SPC, **PRS**, PRC, PLN, WIN, FRM, REG, GDL.
- **Site codes:** PAP, CHB, SAP, CPF, LND, PLB, HOF.
- **System codes (26):** LDR, OMS, LEG, PPL, CON, STK, RSK, PSM, MOC, PRJ, ENG, AIM, MNT, WEL, OPS, COW, EMR, DOC, INC, PRF, ENV, OHH, SEC, BPM, LOG, HMA.
- **Gateway checks G1 to G16:** number and codes, revision rule, properties, agreement between the five places, `doc_title`, tags, "shall", people, control IDs, parent, references, PRS agreement, implementing-processes table, media, XML validity, lock files.

## 6. ACE company facts (stay consistent)

- **Acme Caribbean Energy Limited (ACE):** about 300 staff (150 women, 150 men), Trinidadian names.
- **Sites and assets:**
  - head office in Central Trinidad near the highway (no exact place);
  - Point Lisas shore base, with supply boats and helicopters to the Gulf of Paria;
  - offshore: **Pommerac A** (manned, OIM), **Chenet B** and **Sapodilla C** (unmanned);
  - land leases **Tamarind, Pawpaw, Soursop**;
  - **Central Processing Facility (CPF):** sells gas to NGC and ships crude.
- **Structure:**
  - CEO plus VPs by function; 13 functions;
  - 32 discipline leads with a dotted line to the VP Engineering & Projects through the **Technical Leadership Council**.
- **Key people:**
  - Satesh Sankar (CEO); George Habib (VP HSE & Compliance);
  - Dev Jaggernauth (VP Engineering & Projects); Sophia Hosany (VP Operations);
  - Joanne Ho Sing (VP Wells); Teresa Daniel (CFO);
  - Adrian Achong (VP HR); Sasha George (VP Supply Chain Management);
  - Marvin Williams (VP IT, Data & Knowledge); Karen Jack (VP Business Development & Markets);
  - Rodney Garcia (VP Communications & Corporate Services); Sharda Bissoon (VP Legal & Government Affairs);
  - Nicole Lange (Head of Internal Audit & Risk Assurance); Gary Ho Sing (Manager, Strategy & Planning);
  - Marissa Bobb (OMS Manager); Sanjay Jagessar (Information Management Lead);
  - Ryan Ramsaran (Technical Writer); Elena Farfan (Manager, Technical Excellence);
  - Rohan Ali (Plant Manager - Central Processing Facility).

  The full list is in `ACE_People.csv`.

## 7. What we are trying to do (the roadmap)

1. **Manual Rev 04** (Section 8) and **DOC-STD-002 Rev 02** + **template v5**: the foundation.
2. **10 Practices:** 4 BPM (the process framework) + 6 discipline Practices (Writer Brief).
3. **Process files:** 3 PRS pairs (MOC, Control of Work, SIS lifecycle) and the **process reader**. A fourth candidate is AIM inspection planning, for the storyline.
4. **Data spine registers** with 2024 to 2026 history and storylines (Section 12).
5. **Rev 02 of the existing 16 documents** (the new slate, Section 9). This gives real dated revision histories.
6. **Automation:** a GitHub Action that runs the gateway and builds the site on every upload, plus a DNS record for oms.cynmark.app. Needs push access or the user adding the workflow.
7. **The dashboard with animations** (Section 14).
8. **Later:** the Word add-in ("ONE" ribbon tab, as an installer) and the ONE Inspector desktop app (as an installer).

## 8. OMS Manual Rev 04: required changes

Rev 04 is generated from `oms/src` (edit `register.py`, `parts.py`, `elements.py`, then run `build_docx.py`) and **merged into the user's logo version**. Alternatively, the user edits his Word copy using this table.

| Section | Change |
|---|---|
| Cover, control table, header/footer | Rev 04. Dates per the story calendar. Framework text "…ACE-OMS-MAN-001 Rev 04" across the set |
| Revision history | Add: "04: adds the Practice and Process layers, the BPM, LOG and HMA systems, the process owner role, control IDs, the 'shall' rule and the property mapping" |
| How to use this Manual | Mention the processes and controls views in ONE |
| **A.3 How OMS is built** | Replace the hierarchy figure with the 5-level model (Policy → Standard/Practice → Process → Procedure/Plan → WIN/Form/Register). Explain the "golden thread" from mission, vision and values to records |
| **A.4 Systems inside OMS** | Add **BPM** (Business Process Management: Manager, Strategy & Planning; elements 1, 2, 3, 7, 10), **LOG** (Marine & Aviation Logistics: VP Supply Chain Management; elements 3, 7, 8), **HMA** (Hydrocarbon Measurement & Allocation: VP Business Development & Markets, with Metering & Measurement Lead as TA; elements 2, 4, 9). Total 26 |
| **A.5 How the systems connect** | Add "controls are the hinge": risk ↔ control ↔ document section ↔ process step ↔ role ↔ asset ↔ evidence |
| **A.6 Who does what** | Add the **process owner** (accountable for process performance and continuous improvement). Distinguish document owner, process owner, Technical Authority and line manager. Add the Technical Leadership Council |
| 2.1 / 2.2 | Practices are approved by the function VP, with TA endorsement for technical practices |
| 3.1 | Process owners appointed in writing and listed in the Process Register |
| 5.1 / 5.2 | Controls Register (RSK-REG-002), control IDs, control health |
| 6.2 | Each engineering discipline maintains its Practices (ENG-STD-901). Reference the new discipline Practices |
| 6.3 | Reference OPS-PRA-001 (integrity operating windows) |
| 7.1 | Processes are a document layer. Every Standard/Practice lists its implementing processes |
| 10.4 | Process improvement through process owners (BPM-PRA-003) |
| C.4 OMS maturity | Process maturity (5 levels) feeds the OMS maturity assessment |
| **D.1 Document hierarchy** | 5 levels and the types table (DOC-STD-002 Rev 02, Section 2) |
| **D.2 Numbering** | Add PRA and PRS to the type codes. Add BPM, LOG and HMA to the system codes. Explain the ENG discipline blocks (901 = framework). Control ID format |
| D.3 Revisions | Unchanged. Restate letters for drafts and digits for approved issues |
| **D.4 Approval matrix** | Add rows: **Practice:** author → TA/discipline review → TLC endorsement (technical) → function VP approves. **Process:** process owner prepares → affected function reviewers → process owner's VP approves (cross-functional: the BPM system owner endorses) |
| **D.5 Templates, styles, tags** | Template v5. The "shall" style table. The ODS.Parent property. Control ID content control. The Word built-in property mapping |
| **D.6 Gateway** | Replace with the G1 to G16 summary |
| D.7 Records | Repository folders: finals, drafts, processes, registers, templates, superseded |
| **New D.8 Processes and the process file** | The PRS pair, APQC levels, the Process Register (BPM-REG-001) |
| **New D.9 Controls and the data spine** | The registers and how they link (Section 12) |
| Appendix 3 register | Add the 10 Practices, the PRS files, the registers BPM-REG-001 and RSK-REG-002, and LOG/HMA Standards (planned) |
| Appendix 4 glossary | Add: Practice, Process, Process owner, APQC PCF, swimlane, SIPOC, IOW, control ID, control health, data spine, Technical Leadership Council |
| Appendix 5 references | APQC PCF; BPMN 2.0 (ISO/IEC 19510); ISO 31000; API RP 580/581/584; API 579; ISO 14224; NORSOK D-010; ISO 16530-1; API MPMS; AGA 9; ISO 5167; IEC 62682 |

Keep the generated Manual's "shall" rule: no "shall" in ProcedureStep or other non-binding styles (fixed in D.6 during Rev 03).

## 9. The new slate: documents for next session

All documents use DOC-STD-002 Rev 02 and template v5.

**Tier 0: foundation** (do first)

| Number | Title | Action |
|---|---|---|
| ACE-OMS-MAN-001 | OMS Manual | Rev 04 (Section 8) |
| ACE-DOC-STD-002 | Operational Document Publishing Standard | Rev 02 (from the draft MD) |
| Template | ONE_ACE_Master_Template_v5.dotx | Build from v4 + Writer Brief, Section 0.3 |

**Tier 1: process framework (BPM)**
- ACE-BPM-PRA-001 Business Process Management Practice
- ACE-BPM-PRA-002 Process Modelling and Process File Practice
- ACE-BPM-PRA-003 Process Ownership and Continuous Improvement Practice
- ACE-RSK-PRA-001 Controls and Barrier Linkage Practice

**Tier 2: discipline Practices**
- OPS-PRA-001 Operating Envelopes and Integrity Operating Windows
- WEL-PRA-001 Well Barriers and Well Handover
- AIM-PRA-001 Risk-Based Inspection and Corrosion Management
- MNT-PRA-001 Equipment Criticality and Safety-Critical Element Maintenance
- LOG-PRA-001 Marine and Aviation Logistics
- HMA-PRA-001 Hydrocarbon Measurement and Allocation

**Tier 3: reissue the existing set as Rev 02**

Applies to: LDR-POL-001, DOC-STD-001, RSK-STD-001, PSM-STD-001, MOC-PRC-001, AIM-STD-001, MNT-STD-001, COW-STD-001, INC-STD-001, PRF-STD-002, OMS-STD-002, CON-STD-001, EMR-STD-001, ENG-STD-901, ENG-SPC-410. DOC-POL-001 and DOC-PRC-001 get confirmed or retired.

The same changes in each:
- Framework text → Rev 04; ODS.Parent set; built-in panel mapping.
- "Implementing processes and procedures" table.
- Control IDs on every ODS.RiskControl paragraph, plus the controls appendix.
- Cross-references to the new Practices.
- A revision history entry with a reason drawn from the storyline where it fits (for example AIM-STD-001 Rev 02 after the Pommerac A near miss).

**Tier 4: processes (PRS pairs)**
- ACE-MOC-PRS-001 Management of Change Process
- ACE-COW-PRS-001 Permit to Work Process
- ACE-ENG-PRS-410 SIS Safety Lifecycle Process
- *candidate:* ACE-AIM-PRS-001 Inspection Planning and Execution

**Tier 5: registers (data spine)**

| Register | Number |
|---|---|
| Process Register | BPM-REG-001 |
| Risk Registers | RSK-REG-001 |
| Controls Register | RSK-REG-002 |
| SCE Register | AIM-REG-001 |
| Events & Actions | INC-REG-001 (new) |
| Objectives & Opportunities | OMS-REG-001 (new) |
| Assets | AIM-REG-002 (new) |

**Then:** the remaining Wave 2 and 3 items on the 30-document list (PPL-STD-003, WEL-STD-001, OPS-STD-001, AIM-STD-002, PRF-STD-001, STK-STD-001, COW-PRC-001/002, EMR-PLN-001-CPF, LEG-STD-001, PRF-STD-003, MNT-WIN-001-PAP, COW-FRM-001).

## 10. Story calendar (proposed: dates drive the animations)

| Date | Event |
|---|---|
| 2024 to 2025 | Legacy period: events, audits and actions recorded in the registers (pre-ONE) |
| 1 Jan 2026 | ONE launch: Manual Rev 03 and Wave 1 Rev 01 effective |
| 1 Apr 2026 | Manual Rev 04, DOC-STD-002 Rev 02, BPM Practices Rev 01 |
| 1 Jun 2026 | Discipline Practices Rev 01; first PRS files |
| Mar to Jun 2026 | Pommerac A inhibitor injection below its IOW; intelligent pigging deferred |
| Jul 2026 | Pinhole leak found on a boat patrol (a near miss); investigation (INC) |
| Aug 2026 | MOC raised; operating window, pigging interval and deferral rule changed |
| 1 Oct 2026 | Rev 02 of AIM-STD-001, OPS-PRA-001, AIM-PRA-001; control health recovers |
| 1 Dec 2026 | Rev 02 of the rest of the Wave 1 set |

## 11. Process file: draft JSON schema (for BPM-PRA-002)

```json
{
  "id": "ACE-MOC-PRS-001", "revision": "01", "status": "Approved",
  "title": "Management of Change Process",
  "apqc": {"l1": "Manage Risk & HSE", "l2": "Manage change", "l3": "Management of Change"},
  "owner": "Elena Farfan — Manager, Technical Excellence",
  "function": "Engineering & Projects",
  "policy": "ACE-LDR-POL-001", "parent": "ACE-MOC-PRC-001",
  "oms_tags": ["5.3", "6.2", "7.1"],
  "lanes": [{"id": "L1", "role": "Change Originator"}, {"id": "L2", "role": "MOC Coordinator"}, {"id": "L3", "role": "Technical Authority"}],
  "steps": [
    {"id": "S01", "lane": "L1", "type": "start", "name": "Identify change", "next": ["S02"]},
    {"id": "S02", "lane": "L1", "type": "task", "name": "Raise MOC request",
     "inputs": ["Change description"], "outputs": ["MOC record"],
     "doc_refs": ["ACE-MOC-PRC-001#_s3_1"], "controls": ["C-MOC-003"],
     "records": ["MOC register entry"], "systems": ["ONE MOC module"],
     "sim": {"dur_h": [0.5, 1, 3], "cost_role": "L1"}, "next": ["S03"]},
    {"id": "S03", "lane": "L2", "type": "xor", "name": "Change classified?",
     "branches": [{"to": "S04", "label": "Major", "p": 0.3}, {"to": "S05", "label": "Minor", "p": 0.7}]}
  ],
  "kpis": [{"name": "MOC cycle time", "target": "≤ 30 days", "type": "leading"}],
  "sim_defaults": {"volume_per_year": 120, "rates_per_h": {"L1": 60, "L2": 75, "L3": 120}}
}
```

## 12. The data spine (registers)

Each register is a CSV or JSON file in `registers/`. Each row has a stable ID. The links are by ID.

| Entity | ID | Key links |
|---|---|---|
| Objective | OBJ-nn | owner, KPI, risks, opportunities |
| Opportunity | OPP-nn | objective, value, owner |
| Risk | R-SITE-nn | causes/threats, consequences, controls, asset, owner, rating (inherent and residual), appetite |
| Control | C-SSS-nnn | risk, barrier, document section (doc#bookmark), process step (PRS#Snn), role, asset/SCE, evidence, health |
| Asset / SCE | A-SITE-nnn | site, hierarchy, criticality, SCE flag, performance standard |
| Process | PRS number | owner, function, policy, steps, controls |
| Role / person | from `ACE_People.csv` | documents, steps, controls |
| Event | EV-yyyy-nnn | date, site, type (incident, near miss, audit finding, test failure, IOW excursion), controls tested or failed, risks |
| Action | ACT-yyyy-nnn | event, owner, due, closed, document/MOC raised |
| Document | number + revision | sections, tags, controls, processes, dates |
| OMS expectation | 1.1 to 10.5 | sections, controls, processes |

**What balances risk:** objectives and opportunities (ISO 31000), and risk appetite, on the same ACE matrix.

**Storylines** (2024 to 2026): Pommerac A pipeline corrosion (main). Others to write: a CPF alarm flood, a Chenet B boat-transfer near miss, a land lease well annulus pressure, and an NGC meter mismeasurement.

## 13. Tools: how to rebuild

The scripts use fixed paths under `/home/claude/`, so unzip the pack there. The repo is cloned at `/home/claude/scmwjtt/oms` (`git clone https://github.com/SCMWJTT/OMS scmwjtt/oms`).

| Task | Command |
|---|---|
| Check files | `python3 audit/quick.py <files.docx>` |
| Full inventory | `python3 audit/inv.py` → `inventory.json` |
| Rebuild properties from the control tables | `python3 audit/fix.py` (reads `scmwjtt/oms/finals`, writes `audit/fixed`) |
| Build the library site | copy the repo to `site/stage`, then `python3 site/build_index.py`, then `python3 site/build_site.py` → `ONE_Library.html` |
| Build the Manual web viewer | `python3 oms/src/build_viewer.py` (needs JSZip at `/opt/node-tools/node_modules/jszip`) |
| Build the Manual Word file | `python3 oms/src/build_docx.py` (graphics from `oms/img`) |
| Org data | `python3 ace/gen.py && python3 ace/build_xlsx.py` (fixed seed: same people every time) |

**Rev 02 changes needed in the scripts:**
- `quick.py` / `build_index.py`: add PRA and PRS; BPM, LOG and HMA; ODS.Parent; Control ID checks (G9); the PRS JSON pair (G12); `drafts/` and `processes/` folders.
- `register.py`: add the new documents and systems.

## 14. Dashboard and animations (driven only by the archive)

All of these come from dates in documents and registers:
- **OMS coming to life:** the wheel fills as documents are issued.
- **The library growing:** the document map builds node by node, with links forming as documents reference each other.
- **Work flowing through a process:** tokens move through the swimlanes. Later this becomes the simulation, using the `sim` fields.
- **Risk over time:** the risk dot moves on the heat map. On the bow-tie, barriers flash, fail and recover with events and revisions.
- **Change ripple:** an MOC or revision spreads to the processes, controls, roles and risks it touches.
- **The coverage matrix** (system × layer) filling in.

The Pommerac A storyline plays through all of them.

## 15. Known pitfalls (from the Errors to Avoid list)

1. Copying an old document carries its hidden properties along.
2. Non-standard property names.
3. A lost `doc_title` bookmark.
4. Empty built-in fields.
5. Roles written without names.
6. Shortened job titles.
7. Inconsistent Framework text.
8. "Shall" in a Warning or Note.
9. Uploading `~$` files.
10. Missing uploads.
11. The placeholder number ACE-AAA-STD-001 left in.
12. Unused images in the template, which make files bloated.
13. The generator writes XML in the wrong order (bookmark before `pPr`, `sdtPr` order, `shd` without `val`).

**Fix the generator before the new slate.**
