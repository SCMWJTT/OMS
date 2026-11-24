# ONE Protocol v1.0.0

**The single rule set for ACE documents in ONE.** Issued 2026-11-24. Governed by ACE-DOC-STD-002 Rev 02; this file becomes its Rev 02 content.
The machine version is `one-protocol.json`. Every ONE tool — Studio (Auditor + Editor), Portal gateway and Word ribbon — reads that file and runs the same checker (`engine/one-audit.js`). This page is generated from it.

## 1. The idea in one paragraph

An author writes in Word. If the document follows this protocol, ONE can read it without anyone re-keying anything: it knows the document's identity, its place in the hierarchy, which OMS expectations each section serves, which sentences are binding, which controls it establishes and who is accountable. The protocol was written **from** the existing documents: everything already in `finals/` passes, or passes after the automatic Fix.

## 2. Two formats: STRICT and LITE

| Format | What it is |
|---|---|
| STRICT | Values in ODS.Meta content controls; tags in ODS.OMSTags@bookmark controls; heading bookmarks; 23 properties filled; Control ID controls. ONE publishes STRICT only. |
| LITE | What writers and AI tools produce: Title and headings in template styles; tags typed as plain text in ODS Tag Line paragraphs ('OMS 6.5, 6.4'); control table as plain text; Control IDs as plain text; properties may be empty. Fix converts LITE to STRICT without changing the text. |

ONE publishes STRICT only. The ONE Editor **Fix** button converts LITE to STRICT without touching the text.

**Outcome of a check:**

| Outcome | Meaning |
|---|---|
| PASS | no errors |
| PASS AFTER FIX | all errors can be fixed automatically by ONE Fix |
| FAIL | at least one error needs a person |

**Legacy documents.** A document whose Framework names Rev 03 is LEGACY: rules introduced in protocol 2.0 give warnings, not errors, until its next revision.

## 3. Identity

- **Number:** `ACE-SSS-TTT-NNN[-LLL]` (SSS system, TTT type, NNN sequence, LLL site). ENG uses discipline blocks 100 to 900; 901 is the framework standard.
- **File name:** `<number>_Title_Words_Rev01.docx` (or `_RevA`).
- **Revision:** letters for drafts (status Draft, In Review); two digits for issues (status Approved, Superseded, Withdrawn).
- **Framework text (fixed):** `IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 04`

### 3.1 Document types

| Code | Type | Level | Layer |
|---|---|---|---|
| MAN | Manual | 1 | Policy |
| POL | Policy | 1 | Policy |
| STD | Standard | 2 | Standard and Practice |
| PRA | Practice | 2 | Standard and Practice |
| SPC | Specification | 2 | Standard and Practice |
| PRS | Process | 3 | Process |
| PRC | Procedure | 4 | Procedure and Plan |
| PLN | Plan | 4 | Procedure and Plan |
| WIN | Work Instruction | 5 | Task and record |
| FRM | Form | 5 | Task and record |
| REG | Register | 5 | Task and record |
| GDL | Guideline | n/a | Supporting |

### 3.2 System codes

| Code | System | Owner | Elements |
|---|---|---|---|
| LDR | Leadership and Conduct | Chief Executive Officer | 1 |
| OMS | OMS Governance and Deviations | VP HSE & Compliance (custodian: OMS Manager) | 1, 2, 10 |
| LEG | Legal and Regulatory Compliance | VP Legal & Government Affairs | 2 |
| PPL | People, Organisation and Competence | VP Human Resources | 3 |
| CON | Contractors and Supply Chain | VP Supply Chain Management | 3, 8 |
| STK | Stakeholders, Community and Customers | VP Communications & Corporate Services | 4 |
| RSK | Risk Management and the ACE Risk Matrix | VP HSE & Compliance | 5 |
| PSM | Process Safety and Hazard Studies | VP HSE & Compliance (Technical Authority: Process Safety Lead) | 5, 6 |
| MOC | Management of Change | VP Engineering & Projects | 5 |
| PRJ | Projects and Engineering Delivery | VP Engineering & Projects | 6 |
| ENG | Engineering Standards and Technical Authority | VP Engineering & Projects (Technical Leadership Council) | 6 |
| AIM | Asset Integrity and Inspection | VP Engineering & Projects | 6 |
| MNT | Maintenance Management | VP Operations | 6, 8 |
| WEL | Well Integrity | VP Wells | 6, 8 |
| OPS | Operations and Operating Limits | VP Operations | 6, 7, 8 |
| COW | Control of Work | VP Operations | 8 |
| EMR | Emergency, Crisis and Continuity | VP HSE & Compliance | 7 |
| DOC | Information, Documents and Records | VP IT, Data & Knowledge | 1, 7, 9 |
| INC | Incidents and Learning | VP HSE & Compliance | 9 |
| PRF | Performance, Assurance and Review | VP HSE & Compliance (audit: Head of Internal Audit) | 9, 10 |
| ENV | Environment | VP HSE & Compliance | 2, 5, 9 |
| OHH | Occupational Health | VP HSE & Compliance | 3, 5 |
| SEC | Security | VP HSE & Compliance | 5, 7 |
| BPM | Business Process Management | Manager, Strategy & Planning (sponsor: Chief Executive Officer) | 1, 2, 3, 7, 10 |
| LOG | Marine and Aviation Logistics | VP Supply Chain Management | 3, 7, 8 |
| HMA | Hydrocarbon Measurement and Allocation | VP Business Development & Markets (Technical Authority: Metering & Measurement Lead) | 2, 4, 9 |

### 3.3 Site codes

| Code | Site |
|---|---|
| PAP | Pommerac A |
| CHB | Chenet B |
| SAP | Sapodilla C |
| CPF | Central Processing Facility |
| LND | Land leases (Tamarind, Pawpaw, Soursop) |
| PLB | Point Lisas shore base |
| HOF | Head Office |

### 3.4 Functions

Business Development & Markets, CEO Office, Communications & Corporate Services, Engineering & Projects, Exploration & Development, Finance, HSE & Compliance, Human Resources, IT, Data & Knowledge, Legal & Government Affairs, Operations, Supply Chain Management, Wells.

## 4. Metadata — five places, one master

The **document control table** (`ODS.Meta.*` content controls) is the master. The cover, header/footer, the 23 custom properties and Word's built-in properties must agree with it. Fix copies the table to the other four.

### 4.1 The 23 custom properties

| Property | Control table tag(s) | Format | Required | Since |
|---|---|---|---|---|
| ODS.DocumentId | ODS.Meta.DocumentID | docid | always | 1.0 |
| ODS.Title | ODS.Meta.Title, ODS.Meta.ControlTitle | text | always | 1.0 |
| ODS.DocumentType | ODS.Meta.DocumentType | type_name | always | 1.0 |
| ODS.Level | ODS.Meta.Level | level | always | 1.0 |
| ODS.Revision | ODS.Meta.Revision, ODS.Meta.CoverRevision | revision | always | 1.0 |
| ODS.Status | ODS.Meta.Status, ODS.Meta.CoverStatus | status | always | 1.0 |
| ODS.IssueDate | ODS.Meta.IssueDate | date | approved | 1.0 |
| ODS.EffectiveDate | ODS.Meta.EffectiveDate, ODS.Meta.CoverEffectiveDate | date | approved | 1.0 |
| ODS.Author | ODS.Meta.Author | people | always | 1.0 |
| ODS.Reviewer | ODS.Meta.Reviewer | people | approved | 1.0 |
| ODS.Endorser | ODS.Meta.Endorser | people_or_body | approved | 1.0 |
| ODS.Approver | ODS.Meta.Approver | people | approved | 1.0 |
| ODS.DocumentOwner | ODS.Meta.DocumentOwner | people | always | 1.0 |
| ODS.ProcessOwner | ODS.Meta.ProcessOwner | people_or_na | approved | 2.0 |
| ODS.Custodian | ODS.Meta.Custodian | people | approved | 1.0 |
| ODS.PrimaryFunction | ODS.Meta.PrimaryFunction | function | always | 1.0 |
| ODS.Framework | ODS.Meta.Framework | framework | always | 1.0 |
| ODS.TitleOMSTags | ODS.Meta.TitleOMSTags | tags | always | 1.0 |
| ODS.Classification | ODS.Meta.Classification | classification | always | 1.0 |
| ODS.Applicability | ODS.Meta.Applicability | text | always | 1.0 |
| ODS.ReviewInterval | ODS.Meta.ReviewInterval | text | approved | 1.0 |
| ODS.RoleRegister | ODS.Meta.RoleRegister | text | approved | 2.0 |
| ODS.Parent | ODS.Meta.Parent | parent | approved | 2.0 |

### 4.2 Word built-in properties (File › Info)

| Field | Value |
|---|---|
| dc:title | {Title} |
| dc:subject | {DocumentId} |
| cp:keywords | {TitleOMSTags} |
| cp:category | {DocumentType} (Level {Level}) |
| cp:contentStatus | {Status} |
| dc:description | Rev {Revision} · Effective {EffectiveDate} · Owner: {DocumentOwner.name} |
| dc:creator | {Author.name} |
| Manager | {DocumentOwner.name} |
| Company | Acme Caribbean Energy Limited |
| HyperlinkBase | https://oms.cynmark.app/ |

### 4.3 People
Written `Name — Job title` exactly as in `company/ACE_People.csv`, several separated by `; `. Allowed non-person values: Technical Leadership Council, Executive Leadership Team, Not required, Not applicable, Board of Directors. A role in brackets after an exact title (e.g. '(Technical Authority)') is accepted with a warning.

## 5. Headings, bookmarks and OMS tags

- The Title paragraph carries the bookmark `doc_title`; its tag line holds `ODS.OMSTags@doc_title`.
- Every Heading 1 and Heading 2 carries a bookmark and is followed by an **ODS Tag Line** holding the control `ODS.OMSTags@<that bookmark>`.
- New headings use `<DOCID with _>_H<nnn>  e.g. ACE_RSK_STD_001_H004`. Any valid bookmark is accepted; the tag control must name the bookmark of its own heading. Fix adds <DOCID>_Hnnn where missing.
- Tags: 1 to 3 per section, primary first, scope heading down to next heading of same or higher level; not inherited.
- Standard front headings and their tags: Document control → 1.7; Revision history → 1.7; Approval and issue → 2.2, 1.7; Document map → 7.1.

### 5.1 The 54 OMS expectations (valid tags)

**1 Commitment and accountability** — 1.1 Leading OMS across ACE; 1.2 A culture of safe, reliable and accountable work; 1.3 Everyone committed to OMS and the law; 1.4 Our Code of Conduct; 1.5 OMS duties built into every role; 1.6 Keeping OMS visible; 1.7 Controlled documents and records; 1.8 Learning to reduce risk

**2 Policies, standards and objectives** — 2.1 Setting and sharing policies, standards and objectives; 2.2 Approval at the right level; 2.3 Risk-based standards that meet the law; 2.4 Objectives we can measure; 2.5 Working with partners; 2.6 Deviations and exemptions

**3 Organisation, resources and capability** — 3.1 Clear roles, accountabilities and authorities; 3.2 Planning our workforce; 3.3 Competence assurance; 3.4 The right resources; 3.5 Consulting our workforce; 3.6 Contractors and suppliers

**4 Stakeholders and customers** — 4.1 Knowing and engaging our stakeholders; 4.2 Managing stakeholder and customer risks; 4.3 Listening and responding; 4.4 Two-way relationships

**5 Risk assessment and control** — 5.1 Assessing risk and putting barriers in place; 5.2 Recording and reviewing significant risks; 5.3 Managing change; 5.4 Staying alert to rising risk

**6 Asset design and integrity** — 6.1 Designing with the right information; 6.2 Engineering standards through the asset life; 6.3 Staying inside operating limits; 6.4 Safety-critical elements; 6.5 Maintenance, inspection and testing; 6.6 Buying and selling assets

**7 Plans and procedures** — 7.1 Writing plans and procedures; 7.2 Approving plans and procedures; 7.3 Training people to use procedures; 7.4 The current version wherever work is done; 7.5 Emergency and continuity plans

**8 Execution of activities** — 8.1 Ready before we start; 8.2 Doing the work as planned; 8.3 Supervision that checks the work; 8.4 Stop work; 8.5 Recognising good work and correcting poor work

**9 Monitoring, reporting and learning** — 9.1 Monitoring and verification; 9.2 Reporting and investigating incidents; 9.3 Learning and closing actions; 9.4 Leading and lagging indicators; 9.5 Reliable data

**10 Assurance, review and improvement** — 10.1 A risk-based assurance programme; 10.2 Reviewing performance; 10.3 Finding weak controls; 10.4 Planned improvement; 10.5 Leadership review of the whole system

## 6. Styles — what ONE does with each paragraph

Variants without the dot (e.g. `ODSRequirement`) are treated as the same style. **'Shall' is allowed only in the binding styles** (quoted mentions such as “shall” are ignored).

| Style ID | Accepted variants | Binding | ONE meaning |
|---|---|---|---|
| Title | – |  | document title (carries doc_title bookmark) |
| Heading1 | – |  | section; must have bookmark + tag line |
| Heading2 | – |  | sub-section; must have bookmark + tag line |
| Heading3 | – |  | minor heading; tag line optional |
| ODSTagLine | – |  | holds the OMS Tags content control for the heading above |
| DocumentSubTitle | – |  | cover subtitle; shown as summary |
| DocumentKicker | – |  | cover label |
| ODS.Requirement | ODSRequirement | yes | requirement |
| ODS.Responsibility | ODSResponsibility | yes | responsibility (role register) |
| ODS.ApprovalRequirement | ODSApprovalRequirement | yes | approval requirement |
| ODS.RecordRequirement | ODSRecordRequirement | yes | record requirement (records view) |
| ODS.RiskControl | ODSRiskControl | yes | control; must carry Control ID content control(s) |
| ODS.Warning | ODSWarning |  | warning |
| ODS.Note | ODSNote |  | note |
| ODS.PerformanceIndicator | ODSPerformanceIndicator |  | KPI |
| ODS.DocumentReference | ODSDocumentReference |  | reference to an ACE document |
| ODS.ExternalStandard | ODSExternalStandard |  | reference to an external standard |
| ODS.ProcedureStep | ODSProcedureStep |  | procedure step |
| ODS.Definition | ODSDefinition |  | glossary term |
| ODS.Example | ODSExample |  | example |
| OMS.ElementKicker | OMSElementKicker |  | Manual element label |
| ListBullet | – |  | list item |
| ONEBrand | – |  | cover branding (ignored) |
| ONESectionLabel | – |  | cover label (ignored) |
| ONECoverCaption | – |  | cover caption (ignored) |
| ONEMetadata | – |  | cover metadata (ignored) |
| ONEPullQuote | – |  | Manual quote (ignored) |
| ONEQuoteBy | – |  | Manual quote author (ignored) |
| Caption | – |  | figure or table caption |

## 7. Content controls

| Tag | Alias | Use |
|---|---|---|
| ODS.Meta.<Field> | free text (label) | control table and cover values; Field from properties[].meta |
| ODS.OMSTags@<bookmark> | OMS Tags (variants accepted) | OMS expectation tags for the heading carrying <bookmark>; doc_title for the Title |
| ODS.Control@<ControlID> | Control ID | inside ODS.RiskControl paragraphs |

**Control IDs:** `C-<SYS>-<NNN>`, unique across the repository, allocated in blocks by the OMS Manager and recorded in ACE-RSK-REG-002. In a RiskControl paragraph each ID sits inside `ODS.Control@<ID>`.

**References:** ACE documents are recognised in text by the pattern `ACE-SSS-TTT-NNN[-LLL] [§x.y]`.

## 8. Gateway rules

Errors block publication; warnings are listed. 'auto' means ONE Fix can correct it without a person.

| Rule | Check | Severity | Fix | What is checked |
|---|---|---|---|---|
| G1 | Document number, codes and file name | error | manual | DocumentId matches the number pattern; system, type and site codes are valid; file name starts with the number (auto-fix: rename) |
| G2 | Revision and status agree | error | manual | letters ↔ Draft/In Review; digits ↔ Approved/Superseded/Withdrawn; approved issues have issue and effective dates; finals/ holds Approved only (warning) |
| G3 | Custom properties | error | auto | all 23 present with standard names (ODS.Parent missing → warning for legacy); required values filled; values in valid format; no unknown ODS.* properties (warning) |
| G4 | Metadata agrees in the five places | error | auto | control table (ODS.Meta.*) = custom properties (control table is master); built-in Title/Subject/Tags (warning for legacy); header/footer shows number and revision (warning) |
| G5 | Title bookmark and title tags | error | auto | doc_title bookmark on the Title paragraph; title tag control ODS.OMSTags@doc_title = ODS.TitleOMSTags |
| G6 | Headings, bookmarks and OMS tags | error | auto | every Heading 1/2 has a bookmark and is followed by a tag line; tag line holds ODS.OMSTags@<that bookmark> (plain-text tag line = LITE, auto-fix); every tag is one of the 54 expectations; no orphan or duplicate tag controls; 1 to 3 tags per section (warning) |
| G7 | 'Shall' only in binding styles | error | manual | no 'shall' in non-binding paragraphs or table cells; Guidelines contain no binding styles |
| G8 | People match the organisation register | error | auto | each person is 'Name — Job title' exactly as in ACE_People.csv; known name with wrong title → auto-fix; unknown name → manual |
| G9 | Control IDs | error | auto | C-SSS-NNN with a valid system code; unique across the repository; every ODS.RiskControl paragraph carries a Control ID content control (legacy → warning); plain-text IDs in RiskControl paragraphs → auto-fix; controls appendix matches body (warning) |
| G10 | Parent document | error | manual | ODS.Parent set below Level 1 (legacy → warning); parent exists in the document register |
| G11 | References to ACE documents | warning | manual | referenced numbers exist (issued or planned); unknown number → warning |
| G12 | Process (PRS) pair | error | manual | JSON file present with same number and revision; validates against ONE-PRS/1; every step has a bookmarked narrative heading; doc_refs and controls resolve |
| G13 | Implementing processes table (STD, PRA) | warning | manual | table listing implementing processes and procedures present |
| G14 | Media and size | warning | auto | no linked (external) images; no unused media; file under 2 MB |
| G15 | Valid Word XML | error | manual | all parts well-formed; bookmarkStart not before pPr (warning, auto-fix) |
| G16 | No lock or temporary files | error | auto | no ~$ or .tmp files in the submission |

## 9. Process files (PRS)

A Process is a Word description plus a model file `ACE-SSS-PRS-NNN.json` (schema ONE-PRS/1, `protocol/schemas/one-prs-1.schema.json`). Defined in ACE-BPM-PRA-002. Worked example: `schemas/example/ACE-MOC-PRS-001.json`.

## 10. Data spine registers

**Process Register** (`registers/BPM-REG-001.csv`, key `process_id`, owner Manager, Strategy & Planning, defined in ACE-BPM-PRA-001)  
`process_id`, `title`, `l1`, `l2`, `owner` → people, `function`, `policy` → document, `parent` → document, `status`, `revision`, `oms_tags`, `last_review`, `maturity`, `requirements`

**Risk Register** (`registers/RSK-REG-001.csv`, key `risk_id`, owner Head of Internal Audit & Risk Assurance, defined in ACE-RSK-STD-001)  
`risk_id`, `title`, `site`, `hazard`, `top_event`, `threats`, `consequences`, `owner` → people, `asset_id` → asset, `inherent_l`, `inherent_c`, `residual_l`, `residual_c`, `appetite`, `objective_id` → objective, `controls` → control, `review_date`

**Controls Register** (`registers/RSK-REG-002.csv`, key `control_id`, owner Process Safety Lead, defined in ACE-RSK-PRA-001)  
`control_id`, `statement`, `position`, `nature`, `critical`, `risk_id` → risk, `threat`, `barrier`, `doc_ref` → document, `process_step` → process, `owner` → people, `asset_id` → asset, `sce_id` → sce, `evidence`, `test_interval`, `health`, `health_date`, `status`

**SCE Register** (`registers/AIM-REG-001.csv`, key `sce_id`, owner Manager, Technical Excellence, defined in ACE-MNT-PRA-001)  
`sce_id`, `title`, `group`, `site`, `asset_ids` → asset, `performance_standard`, `test_interval`, `last_test`, `next_due`, `status`, `controls` → control

**Asset Register** (`registers/AIM-REG-002.csv`, key `asset_id`, owner Maintenance & Integrity Manager, defined in ACE-MNT-PRA-001)  
`asset_id`, `tag`, `title`, `site`, `parent_id` → asset, `iso14224_class`, `criticality`, `sce`, `in_service`

**Events and Actions — events** (`registers/INC-REG-001_events.csv`, key `event_id`, owner HSE Manager, defined in ACE-INC-STD-001)  
`event_id`, `date`, `site`, `type`, `title`, `risk_ids` → risk, `controls_tested` → control, `controls_failed` → control, `processes` → process, `severity`

**Events and Actions — actions** (`registers/INC-REG-001_actions.csv`, key `action_id`, owner HSE Manager, defined in ACE-INC-STD-001)  
`action_id`, `event_id` → event, `title`, `owner` → people, `due`, `closed`, `result` → document

**Objectives and Opportunities — objectives** (`registers/OMS-REG-001_objectives.csv`, key `objective_id`, owner Manager, Strategy & Planning, defined in ACE-BPM-PRA-001)  
`objective_id`, `title`, `owner` → people, `kpi`, `target`, `year`, `processes` → process, `risks` → risk

**Objectives and Opportunities — opportunities** (`registers/OMS-REG-001_opportunities.csv`, key `opportunity_id`, owner Manager, Strategy & Planning, defined in ACE-RSK-PRA-001)  
`opportunity_id`, `title`, `objective_id` → objective, `owner` → people, `value`, `likelihood`, `benefit`, `status`

## 11. Pack contents

| File | Purpose |
|---|---|
| one-protocol.json | the rule set every tool reads |
| engine/one-audit.js | the single checker (Node, Electron, browser) |
| engine/cli.js | runs the checker over the repository; writes reports/audit.md and audit.json |
| schemas/one-prs-1.schema.json | process file schema |
| registers/*.csv | empty register templates |
| samples/ACE-DOC-PRA-999_…Golden_Sample…docx | test document that passes every rule |
| ../templates/ONE_ACE_Master_Template_v5.dotx | template v5 |
| build/ | scripts that regenerate the JSON and this page |
