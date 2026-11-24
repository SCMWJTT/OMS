# ONE Auditor report

Protocol 1.0.0 · engine 1.0.0 · 2026-11-24

**40 files:** PASS 30 · PASS AFTER FIX 4 · FAIL 6

| Folder | File | Format | Legacy | Outcome | Errors (auto/manual) | Warnings |
|---|---|---|---|---|---|---|
| finals | ACE-AIM-PRA-001 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-AIM-STD-001 | STRICT | yes | PASS | 0 / 0 | 7 |
| finals | ACE-AIM-STD-002 | STRICT | yes | PASS | 0 / 0 | 8 |
| finals | ACE-BPM-PRA-001 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-BPM-PRA-002 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-BPM-PRA-003 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-CON-STD-001 | STRICT | yes | PASS | 0 / 0 | 9 |
| finals | ACE-COW-PRC-001 | STRICT |  | PASS | 0 / 0 | 1 |
| finals | ACE-COW-PRC-002 | STRICT |  | PASS | 0 / 0 | 1 |
| finals | ACE-COW-STD-001 | STRICT | yes | PASS | 0 / 0 | 6 |
| finals | ACE-DOC-POL-001 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-DOC-PRC-001 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-DOC-STD-001 | STRICT | yes | PASS | 0 / 0 | 8 |
| finals | ACE-DOC-STD-002 | STRICT | yes | PASS | 0 / 0 | 7 |
| finals | ACE-EMR-STD-001 | STRICT | yes | PASS | 0 / 0 | 9 |
| finals | ACE-ENG-SPC-410 | STRICT | yes | PASS AFTER FIX | 1 / 0 | 10 |
| finals | ACE-ENG-STD-901 | STRICT | yes | PASS | 0 / 0 | 7 |
| finals | ACE-INC-STD-001 | STRICT | yes | PASS | 0 / 0 | 9 |
| finals | ACE-LDR-POL-001 | STRICT | yes | PASS AFTER FIX | 1 / 0 | 5 |
| finals | ACE-MNT-PRA-001 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-MNT-STD-001 | STRICT | yes | PASS | 0 / 0 | 7 |
| finals | ACE-MOC-PRC-001 | STRICT | yes | PASS AFTER FIX | 1 / 0 | 8 |
| finals | ACE-OMS-STD-002 | STRICT | yes | PASS | 0 / 0 | 12 |
| finals | ACE-OPS-PRA-001 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-OPS-STD-001 | STRICT | yes | PASS | 0 / 0 | 9 |
| finals | ACE-PPL-STD-003 | STRICT | yes | PASS | 0 / 0 | 7 |
| finals | ACE-PRF-STD-002 | STRICT | yes | PASS | 0 / 0 | 8 |
| finals | ACE-PSM-STD-001 | STRICT | yes | PASS | 0 / 0 | 8 |
| finals | ACE-RSK-PRA-001 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-RSK-STD-001 | STRICT | yes | PASS | 0 / 0 | 7 |
| finals | ACE-WEL-PRA-001 | STRICT |  | PASS | 0 / 0 | 0 |
| finals | ACE-WEL-STD-001 | STRICT | yes | PASS | 0 / 0 | 9 |
| manuals | ACE-OMS-MAN-001 | STRICT |  | PASS AFTER FIX | 1 / 0 | 15 |
| samples/lite | ACE-AIM-PRA-001 | LITE |  | FAIL | 27 / 4 | 3 |
| samples/lite | ACE-COW-PRC-001 | LITE |  | FAIL | 19 / 3 | 6 |
| samples/lite | ACE-COW-PRC-002 | LITE |  | FAIL | 20 / 2 | 6 |
| samples/lite | ACE-MNT-PRA-001 | LITE |  | FAIL | 29 / 4 | 3 |
| samples/lite | ACE-OPS-PRA-001 | LITE |  | FAIL | 57 / 5 | 3 |
| samples/lite | ACE-WEL-PRA-001 | LITE |  | FAIL | 58 / 3 | 2 |
| protocol/samples | ACE-DOC-PRA-999 | STRICT |  | PASS | 0 / 0 | 0 |

## Findings

### finals/ACE-AIM-STD-001_Asset_Integrity_Management_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** warning: Primary function 'Engineering & Projects / Asset Integrity and Inspection' is not one of the 13 ACE functions
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-AIM-STD-001'
- **G9** warning: RiskControl paragraph without a Control ID — _A green maintenance schedule is not proof of barrier health _
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-AIM-STD-002_Inspection_Management_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** warning: Primary function 'Asset Integrity and Inspection (AIM)' is not one of the 13 ACE functions
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ACE-AIM-STD-002 | ONE management system', should be 'ACE-AIM-STD-002'
- **G9** warning: RiskControl paragraph without a Control ID — _Equipment with unknown remaining integrity, missing critical_
- **G9** warning: RiskControl paragraph without a Control ID — _Access and exposure risks for radiography, confined space, w_
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-CON-STD-001_Contractor_and_Supplier_Management_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ACE-CON-STD-001 — Contractor and Supplier Management Standard', should be 'ACE-CON-STD-001'
- **G9** warning: RiskControl paragraph without a Control ID — _Where the scope could affect a major accident barrier, safet_
- **G9** warning: RiskControl paragraph without a Control ID — _High-risk contractors shall demonstrate that worksite superv_
- **G9** warning: RiskControl paragraph without a Control ID — _Work involving an ineffective or unavailable critical barrie_
- **G9** warning: RiskControl paragraph without a Control ID — _Nonconforming safety-critical items shall remain segregated _
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-COW-PRC-001_Permit_to_Work_Procedure_Rev01.docx — PASS
- **G6** warning: 1 section(s) carry more than 3 tags

### finals/ACE-COW-PRC-002_Isolation_and_Reinstatement_Procedure_Rev01.docx — PASS
- **G6** warning: 1 section(s) carry more than 3 tags

### finals/ACE-COW-STD-001_Control_of_Work_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** warning: Primary function 'Operations — Control of Work' is not one of the 13 ACE functions
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-COW-STD-001'
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-DOC-STD-001_Document_Records_Management_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-DOC-STD-001'
- **G9** warning: RiskControl paragraph without a Control ID — _A site team shall not rely on an unapproved draft to justify_
- **G9** warning: RiskControl paragraph without a Control ID — _Where a cyber incident, broken link or repository outage mak_
- **G9** warning: RiskControl paragraph without a Control ID — _If a current instruction cannot be shown to be approved and _
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-DOC-STD-002_Operational_Document_Publishing_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-DOC-STD-002'
- **G9** warning: RiskControl paragraph without a Control ID — _Work involving a safety-critical element shall identify the _
- **G9** warning: RiskControl paragraph without a Control ID — _Where the publication view is unavailable or out of synchron_
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-EMR-STD-001_Emergency_Crisis_and_Business_Continuity_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ACE-EMR-STD-001 — Emergency, Crisis and Business Continuity Standard', should be 'ACE-EMR-STD-001'
- **G9** warning: RiskControl paragraph without a Control ID — _Protection of life, safe isolation and prevention of escalat_
- **G9** warning: RiskControl paragraph without a Control ID — _Where a critical response resource is impaired, the Area Aut_
- **G9** warning: RiskControl paragraph without a Control ID — _Personnel shall not disclose personal casualty details, spec_
- **G9** warning: RiskControl paragraph without a Control ID — _Recovery actions that change plant, controls, competence or _
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-ENG-SPC-410_Safety_Instrumented_Systems_Specification_Rev01.docx — PASS AFTER FIX
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** error (auto-fix): ODS.Level 'Technical' is not a number 1–5
- **G4** warning (auto-fix): Control table values not in Meta controls: DocumentType, IssueDate, Author, Reviewer, Endorser, Approver, DocumentOwner, Custodian, PrimaryFunction, Framework, TitleOMSTags, Classification, Applicability, ReviewInterval
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ACE-ENG-SPC-410 • Specification • 6.2, 6.4, 5.1', should be 'ACE-ENG-SPC-410'
- **G9** warning: RiskControl paragraph without a Control ID — _A generic example of a shutdown loop must never substitute f_
- **G9** warning: RiskControl paragraph without a Control ID — _A control loop, alarm or operator response shall not be cred_
- **G9** warning: RiskControl paragraph without a Control ID — _A single shared component or service that can defeat both th_
- **G9** warning: RiskControl paragraph without a Control ID — _No test is complete until temporary bypasses, forced values,_
- **G9** warning: RiskControl paragraph without a Control ID — _Do not bypass or suppress a credited safety function solely _
- **G10** warning: ODS.Parent not set

### finals/ACE-ENG-STD-901_Engineering_Standards_Framework_and_Technical_Authority_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table values not in Meta controls: DocumentType, IssueDate, Author, Reviewer, Endorser, Approver, DocumentOwner, Custodian, PrimaryFunction, Framework, TitleOMSTags, Classification, Applicability, ReviewInterval
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ACE-ENG-STD-901 • Standard • 6.2, 3.1, 2.6', should be 'ACE-ENG-STD-901'
- **G9** warning: RiskControl paragraph without a Control ID — _A deviation affecting a major accident barrier shall not be _
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-INC-STD-001_Incident_Reporting_and_Investigation_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** warning: Primary function 'HSE & Compliance / Incidents and Learning' is not one of the 13 ACE functions
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-INC-STD-001'
- **G9** warning: RiskControl paragraph without a Control ID — _Incident investigations shall not compromise emergency respo_
- **G9** warning: RiskControl paragraph without a Control ID — _Barrier-related investigation recommendations shall identify_
- **G9** warning: RiskControl paragraph without a Control ID — _The worked example demonstrates classification and evidence _
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-LDR-POL-001_OMS_Policy_Rev01.docx — PASS AFTER FIX
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table values not in Meta controls: TitleOMSTags
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE | Policy (Level 1) | ACE-LDR-POL-001', should be 'ACE-LDR-POL-001'
- **G8** error (auto-fix): Reviewer: 'Sharda Bissoon — VP Legal & Government Affairs' — register title is 'VP Legal & Government Affairs (General Counsel)'
- **G9** warning: RiskControl paragraph without a Control ID — _Everyone has authority and a duty to stop or suspend work wh_

### finals/ACE-MNT-STD-001_Maintenance_Management_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** warning: Primary function 'Operations — Maintenance & Integrity' is not one of the 13 ACE functions
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-MNT-STD-001'
- **G8** warning (auto-fix): Endorser: role qualifier after the title in 'Sharon Alexander — Rotating Equipment Lead (Technical Authority)'
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-MOC-PRC-001_Management_of_Change_Procedure_Rev01.docx — PASS AFTER FIX
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** warning: Primary function 'Engineering & Projects / Technical Excellence' is not one of the 13 ACE functions
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Procedure (Level 3)', should be 'ACE-MOC-PRC-001'
- **G8** error (auto-fix): Reviewer: 'Arjun Gittens — Offshore Operations Manager' — register title is 'Offshore Operations Manager (Gulf of Paria)'
- **G8** warning (auto-fix): Endorser: role qualifier after the title in 'Michelle de Verteuil — Process Engineering Lead (Technical Authority)'
- **G9** warning: RiskControl paragraph without a Control ID — _An intended protective function is not a credited barrier un_
- **G9** warning: RiskControl paragraph without a Control ID — _Where work affects an active barrier, the job is held until _
- **G10** warning: ODS.Parent not set

### finals/ACE-OMS-STD-002_Deviation_and_Exemption_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table values not in Meta controls: TitleOMSTags
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE | Standard (Level 2) | ACE-OMS-STD-002', should be 'ACE-OMS-STD-002'
- **G9** warning: RiskControl paragraph without a Control ID — _Consider common-cause failures, dependent barriers, the leng_
- **G9** warning: RiskControl paragraph without a Control ID — _Do not count a manual watch, additional inspection or proced_
- **G9** warning: RiskControl paragraph without a Control ID — _For emergency shutdown, fire and gas, pressure protection or_
- **G9** warning: RiskControl paragraph without a Control ID — _Where an impaired barrier changes the risk during the approv_
- **G9** warning: RiskControl paragraph without a Control ID — _Failure to demonstrate an acceptable independent barrier res_
- **G9** warning: RiskControl paragraph without a Control ID — _Vendor assurance and a purchase order do not authorize an en_
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-OPS-STD-001_Operating_Envelopes_and_Operating_Limits_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** warning: Primary function 'Operations (OPS)' is not one of the 13 ACE functions
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ACE-OPS-STD-001 | ONE management system', should be 'ACE-OPS-STD-001'
- **G9** warning: RiskControl paragraph without a Control ID — _When a limit is uncertain, inaccessible or contradicted by a_
- **G9** warning: RiskControl paragraph without a Control ID — _For operating modes outside the verified design case, the Ar_
- **G9** warning: RiskControl paragraph without a Control ID — _The Shift Supervisor shall secure the plant when the approve_
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-PPL-STD-003_Competence_Assurance_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ACE-PPL-STD-003 — Standard (Level 2)', should be 'ACE-PPL-STD-003'
- **G9** warning: RiskControl paragraph without a Control ID — _Task criticality shall be established using the ACE Risk Mat_
- **G9** warning: RiskControl paragraph without a Control ID — _A contractor competence deficiency affecting a major-acciden_
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-PRF-STD-002_Assurance_and_Audit_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G3** warning: Primary function 'HSE & Compliance / Internal Audit & Risk Assurance' is not one of the 13 ACE functions
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-PRF-STD-002'
- **G8** warning (auto-fix): Approver: role qualifier after the title in 'George Habib — VP HSE & Compliance (system owner)'
- **G8** warning (auto-fix): Approver: role qualifier after the title in 'Nicole Lange — Head of Internal Audit & Risk Assurance (audit authority)'
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-PSM-STD-001_Process_Safety_and_Hazard_Study_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-PSM-STD-001'
- **G8** warning (auto-fix): Endorser: role qualifier after the title in 'Damian Daniel — Process Safety Lead (Technical Authority)'
- **G9** warning: RiskControl paragraph without a Control ID — _A credited barrier that is unavailable, inhibited, overdue f_
- **G9** warning: RiskControl paragraph without a Control ID — _Never count the same physical function twice under different_
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-RSK-STD-001_Risk_Management_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ONE / ACE controlled document — Standard (Level 2)', should be 'ACE-RSK-STD-001'
- **G9** warning: RiskControl paragraph without a Control ID — _When a safety-critical element is bypassed, failed or overdu_
- **G9** warning: RiskControl paragraph without a Control ID — _An administrative restriction cannot be assumed to fully rep_
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### finals/ACE-WEL-STD-001_Well_Integrity_Management_Standard_Rev01.docx — PASS
- **G3** warning (auto-fix): Property ODS.Parent missing (added in template v5)
- **G4** warning (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister, Parent
- **G4** warning (auto-fix): Word built-in subject is 'ACE-WEL-STD-001 — Standard (Level 2)', should be 'ACE-WEL-STD-001'
- **G9** warning: RiskControl paragraph without a Control ID — _A degraded barrier shall not be treated as available solely _
- **G9** warning: RiskControl paragraph without a Control ID — _Personnel shall not bleed or pressure-cycle an anomalous ann_
- **G9** warning: RiskControl paragraph without a Control ID — _A well classified W3 shall be prevented from normal producti_
- **G9** warning: RiskControl paragraph without a Control ID — _A suspended well shall retain a documented barrier and monit_
- **G10** warning: ODS.Parent not set
- **G13** warning: No implementing processes and procedures table

### manuals/ACE-OMS-MAN-001_OMS_Manual_Rev04.docx — PASS AFTER FIX
- **G4** error (auto-fix): Control table lacks v5 rows: Level, ProcessOwner, RoleRegister
- **G6** warning: Heading has no tag line — _How to use this Manual_
- **G6** warning: Heading has no tag line — _Reading the Manual_
- **G6** warning: Heading has no tag line — _Contents_
- **G6** warning: Heading has no tag line — _Element 1 — Commitment and accountability_
- **G6** warning: Heading has no tag line — _Element 2 — Policies, standards and objectives_
- **G6** warning: Heading has no tag line — _Element 3 — Organisation, resources and capability_
- **G6** warning: Heading has no tag line — _Element 4 — Stakeholders and customers_
- **G6** warning: Heading has no tag line — _Element 5 — Risk assessment and control_
- **G6** warning: Heading has no tag line — _Element 6 — Asset design and integrity_
- **G6** warning: Heading has no tag line — _Element 7 — Plans and procedures_
- **G6** warning: Heading has no tag line — _Element 8 — Execution of activities_
- **G6** warning: Heading has no tag line — _Element 9 — Monitoring, reporting and learning_
- **G6** warning: Heading has no tag line — _Element 10 — Assurance, review and improvement_
- **G6** warning: Heading has no tag line — _Appendices_
- **G6** warning: Heading has no tag line — _Appendix 4 — Glossary_

### samples/lite/ACE-AIM-PRA-001_Risk-Based_Inspection_and_Corrosion_Management_Practice_RevA.docx — FAIL
- **G3** error (auto-fix): Property ODS.DocumentId empty; value available in the document
- **G3** error (auto-fix): Property ODS.Title empty; Fix will set 'Risk-Based Inspection and Corrosion Management Practice'
- **G3** error (auto-fix): Property ODS.DocumentType empty; Fix will set 'Practice'
- **G3** error (auto-fix): Property ODS.Level empty; Fix will set '2'
- **G3** error (auto-fix): Property ODS.Revision empty; value available in the document
- **G3** error (auto-fix): Property ODS.Status empty; value available in the document
- **G3** error: ODS.Author has no value anywhere in the document
- **G3** error: ODS.DocumentOwner has no value anywhere in the document
- **G3** error (auto-fix): Property ODS.ProcessOwner empty; Fix will set 'Not applicable'
- **G3** error: ODS.PrimaryFunction has no value anywhere in the document
- **G3** error (auto-fix): Property ODS.Framework empty; value available in the document
- **G3** error (auto-fix): Property ODS.TitleOMSTags empty; Fix will set '6.5, 6.4, 5.4'
- **G3** error (auto-fix): Property ODS.Classification empty; Fix will set 'Internal'
- **G3** error: ODS.Applicability has no value anywhere in the document
- **G3** error (auto-fix): Property ODS.ReviewInterval empty; Fix will set 'Three years; earlier if triggered'
- **G3** error (auto-fix): Property ODS.Parent empty; value available in the document
- **G4** error (auto-fix): Word built-in keywords is 'Standard Practice; Draft Revision A; ONE; OMS', should be '6.5, 6.4, 5.4'
- **G4** warning (auto-fix): Header/footer does not show the document number
- **G4** warning (auto-fix): Header/footer does not show revision A
- **G5** error (auto-fix): Title paragraph has no doc_title bookmark
- **G5** error (auto-fix): No title tag control ODS.OMSTags@doc_title
- **G6** error (auto-fix): Tag line is plain text (LITE) — _1 Purpose and scope_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _2 Roles and technical authority_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _3 Damage mechanisms and corrosion loops_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _4 Risk-based inspection method_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _5 Inspection intervals and strategy_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _6 Corrosion monitoring and mitigation_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _7 Pipeline integrity and surveillance_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _8 Deferral, anomalies and fitness for service_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _9 Data, records and systems_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _10 Performance, assurance and implementing processes_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _11 Implementing processes and procedures_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix A — Controls established by this Practice_
- **G9** warning: Controls appendix and body differ (appendix only: C-AIM-001, C-AIM-002, C-AIM-003, C-AIM-004, C-AIM-005, C-AIM-006, C-AIM-007, C-AIM-008, C-AIM-009, C-AIM-010; body only: -)

### samples/lite/ACE-COW-PRC-001_Permit_to_Work_Procedure_DraftA.docx — FAIL
- **G1** warning (auto-fix): File name does not follow ACE-COW-PRC-001_Title_RevNN.docx — _ACE-COW-PRC-001_Permit_to_Work_Procedure_DraftA.docx_
- **G3** error (auto-fix): Property ODS.ProcessOwner empty; Fix will set 'Not applicable'
- **G3** error (auto-fix): ODS.Level 'Level 3' is not a number 1–5
- **G3** error (auto-fix): Classification 'Controlled document — draft' not one of Public, Internal, Confidential
- **G3** warning: Primary function 'Control of Work permit authorization' is not one of the 13 ACE functions
- **G4** error (auto-fix): Word built-in keywords is 'ONE; ACE; ACE-COW-PRC-001; OMS 8.2, 8.1, 5.1, 3.6', should be '8.2, 8.1, 5.1, 3.6'
- **G4** warning (auto-fix): Header/footer does not show the document number
- **G4** warning (auto-fix): Header/footer does not show revision A
- **G5** error (auto-fix): Title paragraph has no doc_title bookmark
- **G5** error (auto-fix): No title tag control ODS.OMSTags@doc_title
- **G6** error (auto-fix): Tag line is plain text (LITE) — _1 Purpose, scope and permit principles_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _2 Permit applicability and work classification_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _3 Roles and authorization_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _4 Request and work preparation_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _5 Field verification and issue_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _6 Execution and monitoring_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _7 SIMOPS and coordination_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _8 Suspension, shift handover and extension_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _9 Completion, hand-back and closure_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _10 Records, assurance and process interfaces_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _11 Processes and procedures implementing this Procedure_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix A — Controls established by this Procedure_
- **G6** warning: 1 section(s) carry more than 3 tags
- **G7** error: 'shall' in Normal paragraph — _Permit type and supplemental certificates are selected by hazard and t_
- **G8** error (auto-fix): Approver: 'Arjun Gittens — Offshore Operations Manager' — register title is 'Offshore Operations Manager (Gulf of Paria)'
- **G9** error: Malformed Control IDs in the controls table: C-C-COW-PTW-001, C-C-COW-PTW-002, C-C-COW-PTW-003…
- **G9** warning: Controls appendix and body differ (appendix only: C-C-COW-PTW-001, C-C-COW-PTW-002, C-C-COW-PTW-003, C-C-COW-PTW-004, C-C-COW-PTW-005, C-C-COW-PTW-006, C-C-COW-PTW-007, C-C-COW-PTW-008, C-C-COW-PTW-009; body only: -)
- **G15** error: 5 table(s) with the header split one letter per column (damaged table)

### samples/lite/ACE-COW-PRC-002_Isolation_and_Reinstatement_Procedure_DraftA.docx — FAIL
- **G1** warning (auto-fix): File name does not follow ACE-COW-PRC-002_Title_RevNN.docx — _ACE-COW-PRC-002_Isolation_and_Reinstatement_Procedure_DraftA.docx_
- **G3** error (auto-fix): Property ODS.ProcessOwner empty; Fix will set 'Not applicable'
- **G3** error (auto-fix): ODS.Level 'Level 3' is not a number 1–5
- **G3** error (auto-fix): Classification 'Controlled document — draft' not one of Public, Internal, Confidential
- **G3** warning: Primary function 'Isolation and reinstatement' is not one of the 13 ACE functions
- **G4** error (auto-fix): Word built-in keywords is 'ONE; ACE; ACE-COW-PRC-002; OMS 8.2, 6.5, 8.1, 7.1', should be '8.2, 6.5, 8.1, 7.1'
- **G4** warning (auto-fix): Header/footer does not show the document number
- **G4** warning (auto-fix): Header/footer does not show revision A
- **G5** error (auto-fix): Title paragraph has no doc_title bookmark
- **G5** error (auto-fix): No title tag control ODS.OMSTags@doc_title
- **G6** error (auto-fix): Tag line is plain text (LITE) — _1 Purpose, scope and isolation principles_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _2 Roles and responsibilities_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _3 Planning and source identification_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _4 Method selection and design_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _5 Certificate, locks, tags and register_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _6 Apply, secure and verify_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _7 Personal and group lock protection_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _8 Maintain isolation and respond to change_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _9 Clearance and reinstatement planning_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _10 Removal, restoration and return to service_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _11 Complex, emergency and non-standard isolations_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _12 Records, assurance and performance_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _13 Processes and procedures implementing this Procedure_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix A — Controls established by this Procedure_
- **G6** warning: 1 section(s) carry more than 3 tags
- **G9** error: Malformed Control IDs in the controls table: C-C-COW-ISO-001, C-C-COW-ISO-002, C-C-COW-ISO-003…
- **G9** warning: Controls appendix and body differ (appendix only: C-C-COW-ISO-001, C-C-COW-ISO-002, C-C-COW-ISO-003, C-C-COW-ISO-004, C-C-COW-ISO-005, C-C-COW-ISO-006, C-C-COW-ISO-007, C-C-COW-ISO-008, C-C-COW-ISO-009, C-C-COW-ISO-010; body only: -)
- **G15** error: 3 table(s) with the header split one letter per column (damaged table)

### samples/lite/ACE-MNT-PRA-001_Equipment_Criticality_and_SCE_Maintenance_Practice_RevA.docx — FAIL
- **G3** error (auto-fix): Property ODS.DocumentId empty; value available in the document
- **G3** error (auto-fix): Property ODS.Title empty; Fix will set 'Equipment Criticality and Safety-Critical Element Maintenance Practice'
- **G3** error (auto-fix): Property ODS.DocumentType empty; Fix will set 'Practice'
- **G3** error (auto-fix): Property ODS.Level empty; Fix will set '2'
- **G3** error (auto-fix): Property ODS.Revision empty; value available in the document
- **G3** error (auto-fix): Property ODS.Status empty; value available in the document
- **G3** error: ODS.Author has no value anywhere in the document
- **G3** error: ODS.DocumentOwner has no value anywhere in the document
- **G3** error (auto-fix): Property ODS.ProcessOwner empty; Fix will set 'Not applicable'
- **G3** error: ODS.PrimaryFunction has no value anywhere in the document
- **G3** error (auto-fix): Property ODS.Framework empty; value available in the document
- **G3** error (auto-fix): Property ODS.TitleOMSTags empty; Fix will set '6.4, 6.5, 8.2'
- **G3** error (auto-fix): Property ODS.Classification empty; Fix will set 'Internal'
- **G3** error: ODS.Applicability has no value anywhere in the document
- **G3** error (auto-fix): Property ODS.ReviewInterval empty; Fix will set 'Three years; earlier if triggered'
- **G3** error (auto-fix): Property ODS.Parent empty; value available in the document
- **G4** error (auto-fix): Word built-in keywords is 'Standard Practice; Draft Revision A; ONE; OMS', should be '6.4, 6.5, 8.2'
- **G4** warning (auto-fix): Header/footer does not show the document number
- **G4** warning (auto-fix): Header/footer does not show revision A
- **G5** error (auto-fix): Title paragraph has no doc_title bookmark
- **G5** error (auto-fix): No title tag control ODS.OMSTags@doc_title
- **G6** error (auto-fix): Tag line is plain text (LITE) — _1 Purpose and scope_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _2 Roles and authority_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _3 Equipment hierarchy and criticality_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _4 Criticality method and reassessment_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _5 Safety-Critical Elements and performance standards_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _6 Maintenance strategy selection_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _7 Work order priority, backlog and planning_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _8 SCE overdue, impairment, bypass and deviation_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _9 Failure data, records and systems_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _10 Performance, verification and process interfaces_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _11 Implementing processes and procedures_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix A — Criticality selection matrix_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix B — Processes and procedures implementing this Prac_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix C — Controls established by this Practice_
- **G9** warning: Controls appendix and body differ (appendix only: C-MNT-001, C-MNT-002, C-MNT-003, C-MNT-004, C-MNT-005, C-MNT-006, C-MNT-007, C-MNT-008, C-MNT-009, C-MNT-010; body only: -)

### samples/lite/ACE-OPS-PRA-001_Operating_Envelopes_and_Integrity_Operating_Windows_Practice_RevA.docx — FAIL
- **G3** error (auto-fix): Property ODS.IssueDate missing
- **G3** error (auto-fix): Property ODS.EffectiveDate missing
- **G4** warning (auto-fix): Header/footer does not show the document number
- **G4** warning (auto-fix): Header/footer does not show revision A
- **G5** error (auto-fix): Title paragraph has no doc_title bookmark
- **G5** error (auto-fix): No title tag control ODS.OMSTags@doc_title
- **G6** error (auto-fix): Standard heading has no tag line; Fix adds OMS 1.7 — _Document control_
- **G6** error (auto-fix): Standard heading has no tag line; Fix adds OMS 1.7 — _Revision history_
- **G6** error (auto-fix): Standard heading has no tag line; Fix adds OMS 7.1 — _Document map_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Purpose, scope and parent Standard_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Roles and technical authority_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Limit hierarchy and classification_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Establishing and validating limits_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Registers, control-system integration and monitoring_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Excursion response and escalation_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Change, review and assurance_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Records and data quality_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Implementing processes_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix A — Example limits (illustrative, not operating set_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix B — Limit review flow_
- **G7** error: 'shall' in Normal paragraph — _Limits are nested; lower-level targets never override an upper-level s_
- **G7** error: 'shall' in Normal paragraph — _Each limit shall be recorded in the Operating Limits Register with a u_
- **G7** error: 'shall' in Normal paragraph — _Excursions are assessed by limit class, magnitude, duration, trend and_
- **G7** error: 'shall' in Normal paragraph — _Operating limits may be changed only through ACE-MOC-PRC-001. The MOC _
- **G9** error (auto-fix): Control ID(s) C-OPS-001 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-002 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-003 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-004 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-005 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-006 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-007 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-008 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-009 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-010 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-011 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-012 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-013 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-014 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-015 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-016 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-017 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-018 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-019 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-020 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-021 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-022 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-023 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-024 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-025 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-026 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-027 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-028 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-029 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-030 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-031 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-032 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-033 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-034 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-035 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-036 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-037 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-038 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error (auto-fix): Control ID(s) C-OPS-039 as plain text — _Operating limits are technically based, classified, approved_
- **G9** error: 39 control paragraphs have identical text — placeholders, not real controls
- **G11** warning: References to unknown documents: ACE-INC-PRS-001

### samples/lite/ACE-WEL-PRA-001_Well_Barriers_and_Well_Handover_Practice_RevA.docx — FAIL
- **G3** error (auto-fix): Property ODS.IssueDate missing
- **G3** error (auto-fix): Property ODS.EffectiveDate missing
- **G4** warning (auto-fix): Header/footer does not show the document number
- **G4** warning (auto-fix): Header/footer does not show revision A
- **G5** error (auto-fix): Title paragraph has no doc_title bookmark
- **G5** error (auto-fix): No title tag control ODS.OMSTags@doc_title
- **G6** error (auto-fix): Standard heading has no tag line; Fix adds OMS 1.7 — _Document control_
- **G6** error (auto-fix): Standard heading has no tag line; Fix adds OMS 1.7 — _Revision history_
- **G6** error (auto-fix): Standard heading has no tag line; Fix adds OMS 7.1 — _Document map_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Purpose, scope and parent Standard_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Roles and technical authority_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Barrier philosophy and well states_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Barrier element acceptance and verification_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Well integrity categories and response_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Annulus pressure management_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Well handover and return to Wells_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Unmanned platform and land-well application_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Records, performance and assurance_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Implementing processes and procedures_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix A — Well barrier decision flow_
- **G6** error (auto-fix): Tag line is plain text (LITE) — _Appendix B — Reference basis_
- **G7** error: 'shall' in Normal paragraph — _Barrier elements are accepted against a defined function, design envel_
- **G7** error: 'shall' in Normal paragraph — _Chenet B and Sapodilla C are normally unmanned and accessed by boat. B_
- **G9** error (auto-fix): Control ID(s) C-WEL-001 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-002 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-003 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-004 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-005 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-006 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-007 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-008 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-009 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-010 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-011 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-012 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-013 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-014 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-015 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-016 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-017 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-018 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-019 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-020 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-021 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-022 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-023 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-024 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-025 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-026 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-027 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-028 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-029 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-030 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-031 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-032 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-033 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-034 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-035 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-036 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-037 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-038 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error (auto-fix): Control ID(s) C-WEL-039 as plain text — _Well barrier envelopes, elements, verification, category, pr_
- **G9** error: 39 control paragraphs have identical text — placeholders, not real controls