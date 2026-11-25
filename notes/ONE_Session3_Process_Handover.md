# ONE Session 3: the Process dimension and Continuous Improvement

Handover for a fresh session. Repo: SCMWJTT/OMS (live site oms.cynmark.app, built by GitHub Actions from `main`). Read this file, then `protocol/ONE_Document_Standard.md`, then the three BPM Practices in `finals/`.

## 1. The user

Wilmark (Cynmark Systems Limited). Former OMS documentation consultant in Trinidad oil and gas. Not a programmer: short, plain-language answers; no npm or terminal for him; find-and-replace style instructions if he must edit; no long lists of alternatives during build work. He merges pull requests on the GitHub website. Branch, then pull request, for every change.

## 1a. Where everything is

Clone the repo and read in this order. All paths are from the repo root.

| What | Where |
|---|---|
| **This handover** | `notes/ONE_Session3_Process_Handover.md` |
| Project background, terminology, document hierarchy (from the writers' phase) | `notes/ONE_Project_Continuation_Brief(writers handover).md` |
| Session 1 handover (how ACE and the documents came about) | `notes/ONE_Handover_Session1.md` and `notes/ONE_Session1_Pack/` (company profile, OMS priority list, publishing standard draft, authoring errors to avoid) |
| Session 2 clean-up log (decisions about the documents) | `notes/ONE_Session2_Cleanup_Log.md` |
| Generators for documents, registers, organisation files and the name clean-up | `notes/ONE_Session2_Pack/tools/` (gen.py, gen_registers.py, regdata.py, regmoc.py, build_org.py, fictionalise.py) |
| How ONE will run on a company's SharePoint later | `notes/ONE_SharePoint_Transition.md` |
| **The document standard** (how a ONE document is written; tags, styles, controls; Appendix A lists the 54 expectations) | `protocol/ONE_Document_Standard.md` |
| Machine rules and the checker | `protocol/one-protocol.json`, `protocol/ONE_Protocol_v1.md`, `protocol/engine/one-audit.js` |
| Process file schema and the worked example | `protocol/schemas/one-prs-1.schema.json`, `protocol/schemas/example/ACE-MOC-PRS-001.json`, `processes/README.md` |
| Approved documents (33) | `finals/` and `manuals/ACE-OMS-MAN-001_OMS_Manual_Rev04.docx` |
| The three BPM Practices (read these first) | `finals/ACE-BPM-PRA-001…`, `-002…`, `-003…` |
| Word template | `templates/ONE_ACE_Master_Template_v5.dotx` |
| Registers (CSV) | `registers/` (process register BPM-REG-001; MOC register and steps; risks; controls; incidents and actions; KPIs; objectives and opportunities; documents) |
| Organisation | `company/ACE_People.csv`, `company/org/*.csv` and its README, `company/ACE_Company_Profile.md`, `company/branding/` |
| Portal code | `portal/src/app.js`, `style.css`, `index.html`; build `portal/build/build.js`; deploy `.github/workflows/portal.yml` |
| Comments service | `worker/` (Cloudflare Worker + D1), deploy `.github/workflows/worker.yml` |

Build locally with `node portal/build/build.js .` (needs the jszip package). The live site rebuilds itself when `main` changes.

## 2. Goal of this session

Build the **Process dimension** of ONE and a new **Continuous Improvement (CI) dimension** tied to it, for the fictional company Acme Caribbean Energy (ACE). This should become the most engaging part of the demo. Design first; build in stages after agreement.

He wants:
- a **process inventory** drawn from the existing documents;
- a list of the **policies** the system is missing (the document map shows policies are thin) and, later, the policies written;
- **process maps** on standard swimlanes that show the stages, how **information**, **materials** and **people** move, and the **cycles**;
- **animation** of the stages with no clock times;
- a **ledger** of actual cases, giving real times and efficiency;
- **CI** as its own dimension, linked to the processes.

## 3. What already exists (use it, don't rebuild it)

| Item | Where | Notes |
|---|---|---|
| Process architecture, 5 levels (L1 category to L5 task), APQC style | ACE-BPM-PRA-001 §4 | 12 L1 categories in Core / Enabling / Governing groups, each with L2 groups. L3 = one process, one owner, one PRS document pair. |
| Process modelling rules and file format | ACE-BPM-PRA-002 | PRS pair = Word description + JSON model. Simulation-ready fields. |
| Process ownership, KPIs, review cycle, improvement routes, maturity | ACE-BPM-PRA-003 | The seed of the CI dimension. |
| JSON schema ONE-PRS/1 | `protocol/schemas/one-prs-1.schema.json` | Fields: id, revision, apqc, owner, function, policy, parent, oms_tags, sipoc, lanes, steps (inputs, outputs, doc_refs, controls, records, systems, sim, next/branches), kpis, sim_defaults. |
| Worked model | `protocol/schemas/example/ACE-MOC-PRS-001.json` | Management of Change, 5 lanes. Drawn on the portal's Processes page with animated tokens. |
| Process register (20 L3 processes, 1 draft, 19 planned) | `registers/BPM-REG-001.csv` | Columns include l1, l2, owner, function, policy, parent, status, maturity, controls. |
| A real event log for one process | `registers/MOC-REG-001.csv` and `MOC-REG-001_steps.csv` | 366 changes with step entry and exit dates: already a ledger. |
| Opportunities and objectives | `registers/OMS-REG-001_*.csv` | Business opportunities, not yet CI items. |
| Incident actions | `registers/INC-REG-001_actions.csv` | Lessons and corrective actions: a CI input. |
| Organisation | `company/org/*.csv`, `company/ACE_People.csv` | Roles (lanes), OMS duties, sites, functions, function links. |
| Policies | finals/ | Only ACE-LDR-POL-001 (OMS / HSE and operating integrity) and ACE-DOC-POL-001 are issued; ACE-RSK-POL-001 is planned. |
| Checker | `protocol/engine/one-audit.js` (rule G12 checks PRS pairs) | |
| Portal | `portal/src/app.js` (single file), built by `portal/build/build.js` | Element-first design, one colour per element. Company/Org pages read `company/org`. |

## 4. Approach agreed in discussion (to confirm with him)

### 4.1 Standards to borrow from (not reinvent)

- **BPMN 2.0** notation, simplified: pools and swimlanes, tasks, start/end events, decision gateways, message flows, data objects. Store our own JSON, but be able to **export BPMN 2.0 XML** so clients with Visio, Signavio or bpmn.io can open it.
- **APQC Process Classification Framework** for the inventory levels and codes (BPM-PRA-001 already follows its style).
- **SIPOC** for each process card (suppliers, inputs, process, outputs, customers).
- **Value stream mapping** for material and information flow, and for the value-added vs waiting view.
- **Process mining** ideas (event log: case, step, start, end, role) for the ledger and for replaying real cases.
- **PDCA / DMAIC** for the CI cycle; ISO 9001 process approach; IOGP 510 element 10 (and 9.3 learning).

### 4.2 Order of work

1. **Inventory first, from the documents.** Mine the 33 documents for process evidence: ODS.ProcedureStep sequences, approval requirements (decision points), record requirements (data objects), roles named (lanes), controls (control points), references between documents (hand-offs). Map each finding into the existing L1/L2 architecture. Output: an extended process register (L1, L2, L3 candidates, owner role, policy, parent standard, source documents, evidence strength, gaps).
2. **Policy gap list from the inventory.** One policy per L1 category (or group of categories) sets intent and owner. Starting list to test against the inventory:
   - existing: OMS / HSE and Operating Integrity (LDR-POL-001), Document and Records (DOC-POL-001)
   - planned: Operational Risk Management (RSK-POL-001)
   - candidates: Code of Conduct and Business Ethics; People and Competence; Contractor and Procurement; Stakeholder and Community; Asset Integrity and Technical Authority; Environment (including flaring); Security (physical and cyber); Hydrocarbon Measurement and Commercial; Delegation of Authority; Emergency and Crisis Management; Assurance and Audit; Business Process and Continuous Improvement.
3. **Data model.** Extend ONE-PRS/1 to v2 (section 5). Agree it before drawing anything.
4. **Two or three worked processes** chosen for contrast:
   - one information-heavy: Management of Change (exists) or Allocation and Custody Transfer;
   - one material and people movement: Offshore Trip Planning and Manifesting (crew change, helicopter, supply boat, Point Lisas shore base);
   - one cyclical: Inspection Planning and Execution, or the Process Review and Improvement cycle.
5. **Visuals in the portal** (section 6).
6. **Ledger** with simulated event logs for the worked processes, then real-case replay and bottleneck views.
7. **CI dimension** (section 7).
8. **Write the missing policies and PRS documents** to the ONE Document Standard, once the inventory and the visuals prove the structure.

## 5. Storage (proposal)

| What | Format | File |
|---|---|---|
| Process inventory | CSV (editable in Excel) | `registers/BPM-REG-001.csv`, extended with L1/L2 codes, APQC code, policy, evidence and source documents |
| Process model (the map) | JSON, schema ONE-PRS/2 | `processes/ACE-SSS-PRS-NNN.json`, paired with the Word PRS description |
| Flows | inside the model: each flow typed `sequence`, `information`, `material` or `people`, with what moves (record, system, product, crew) | |
| Cycles | flag on the model and on loop flows (`cycle: true`, cycle name) | |
| Ledger (actual cases) | CSV event log: case_id, process_id, step_id, role, site, start, end, outcome, rework flag | `registers/BPM-LOG-<process>.csv` |
| CI items | CSV register: id, title, process_id, step_id, source (incident, audit, review, idea, KPI), method (just-do-it, PDCA, DMAIC, project), stage, owner role, baseline, target, benefit, dates, status | `registers/CI-REG-001.csv` |
| Process versions | the JSON's revision history, so before/after maps can be compared | |
| Export | BPMN 2.0 XML, generated | |

## 6. Visualisation ideas to explore

- **Value chain (L0):** the core categories as a flowing band (Explore → Wells → Produce → Process & Sell) with enabling and governing categories underneath; product moving through.
- **Process landscape (L1/L2):** a grid or tree of all processes, coloured by maturity or health, with policy and owner; planned processes shown hollow (like the document map).
- **Swimlane map (L3):** lanes = roles from the role catalogue; step boxes linked to documents and controls. Overlay toggles: control flow, information flow (records and systems), material flow, people movement, each with its own line style and moving token.
- **Stage animation without clock times:** steps light up in order; tokens show work passing between roles; the hand-off count is visible.
- **Cycle view:** circular layout for cyclical processes (inspection cycle, MOC review, PDCA).
- **SIPOC card** on each process.
- **Ledger views:** replay real cases on the map; cycle time per step; waiting vs working; rework loops; conformance with the model.
- **Hand-off matrix:** role-to-role hand-offs, which is where most waste hides.
- **Links back to every other dimension:** each step shows its documents, controls, risks, roles, site and element.

## 7. The CI dimension

CI gets its own menu section and register, always pointing at a process (and where possible a step):
- **Sources:** incident actions, audit findings, process reviews (BPM-PRA-003), KPI breaches, staff ideas.
- **Flow:** idea → assess → improve (PDCA or DMAIC stage) → verify benefit → standardise (document revision through MOC).
- **Views:** improvement funnel or board by stage; benefit tracker; before/after process maps; process maturity over time; heat map of the steps that attract the most improvement items.
- **Element tie:** mostly element 10 (assurance, review, improvement) and 9.3 (learning), shown in the element colours.

## 8. First steps for the new session

1. Read this file, BPM-PRA-001, -002 and -003, the ONE-PRS/1 schema and the MOC example.
2. Mine the documents and produce the draft process inventory and the policy gap list. Show both to Wilmark as tables before building anything.
3. Propose ONE-PRS/2 and the ledger and CI formats; agree them.
4. Then build, in stages, on a branch with a pull request each time.

## 9. Opening message for the new session

> We are continuing the ONE project (repo SCMWJTT/OMS, live at oms.cynmark.app). This session is about the Process dimension and a new Continuous Improvement dimension. Clone the repo and read `notes/ONE_Session3_Process_Handover.md` first; section 1a lists where everything else is. Then read the three BPM Practices in `finals/`, the ONE-PRS/1 schema and the MOC example. Don't build anything yet. Start by giving me (1) a draft process inventory mined from the documents and placed in the existing L1/L2 architecture, and (2) a list of the policies we are missing. Show both as tables, then propose the data formats for process maps, the ledger and CI.
