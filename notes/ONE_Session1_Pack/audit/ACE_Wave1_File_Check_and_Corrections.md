# ACE Wave 1 — Repository File Check and Corrections

*Checked: SCMWJTT/OMS (commit e39538e), 21 November 2026. 11 Word files in `finals/`, 2 templates in `templates/`.*

## Summary

| | Before | After |
|---|---|---|
| Files passing the gateway check | 0 of 11 | 11 of 11 (the 2 drafts pass with the expected “no dates yet” warning) |
| Files whose hidden properties belonged to another document | 5 (AIM, COW, MNT, MOC, PRF all carried ACE-RSK-STD-001) | 0 |
| Files using the standard property names | 0 | 11 |
| Title OMS tags attached to the title | 0 | 11 |
| Word page counts changed by the corrections | — | none |

Corrected copies are in `ACE_Wave1_Corrected.zip`. Your originals in GitHub were not changed. Revision numbers and dates were **not** changed.

## What was found

1. **Wrong hidden properties (serious).** Five documents had the Risk Management Standard's properties: number, title, author, reviewers, approver, owner and tags. In Word they look correct; the web reader showed all five as “Risk Management Standard”.
2. **Two property schemes.** The master template uses the standard names (`ODS.DocumentId`, `ODS.DocumentType`, `ODS.DocumentOwner` …). The finals used different ones (`DocumentID`, `Type`, `Owner` …) and lacked Process Owner and Role Register.
3. **Document details in four places.** The control-table content controls (`ODS.Meta.*`), the custom properties, Word's own core properties and the header/footer text. Headers and footers were all correct. The content controls were correct in every file, so they were used as the single source for everything else.
4. **Title tags orphaned.** The finals had lost the `doc_title` bookmark that the template puts on the Title, so title tags did not attach to anything.
5. **Core properties incomplete.** Word's Title field was empty in all 11; no document identifier; subject, category and description were inconsistent; the two drafts showed a 2013 creation date inherited from the template.
6. **Role-only entries.** COW and MNT listed the owner as just “VP Operations”, and custodians as “Control of Work System Owner” and “Maintenance & Integrity Manager”.
7. **Small consistency items.** Rohan Ali's title written as “Plant Manager, CPF” (org chart: “Plant Manager - Central Processing Facility”); the Framework field worded three different ways; the PSM warning “This example shall not be used…”.

## What was corrected (per file)

### ACE-AIM-STD-001_Asset_Integrity_Management_Standard_Rev01.docx

- **Control field Framework:** IOGP Report 510 (2014); ACE-OMS-MAN-001; ONE publication standards → IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 03. *Same wording in every document.*
- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 20 properties, non-standard names; DocumentID was ACE-RSK-STD-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Hidden properties disagreed with the document.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-AIM-STD-001), subject, category, keywords and description set. *Word's own fields agree with the document.*

### ACE-COW-STD-001_Control_of_Work_Standard_Rev01.docx

- **Control field DocumentOwner:** VP Operations → Sophia Hosany — VP Operations. *Field held a role or system name, not a named person from the org chart.*
- **Control field Custodian:** Control of Work System Owner — VP Operations → Adrian Rodriguez — Permit to Work Coordinator (Offshore). *Field held a role or system name, not a named person from the org chart.*
- **Control field Framework:** IOGP Report 510 (2014); ACE-OMS-MAN-001; ONE publication standards → IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 03. *Same wording in every document.*
- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 20 properties, non-standard names; DocumentID was ACE-RSK-STD-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Hidden properties disagreed with the document.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-COW-STD-001), subject, category, keywords and description set. *Word's own fields agree with the document.*

### ACE-DOC-POL-001_Policy_RevA.docx

- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 17 properties, non-standard names; DocumentID was ACE-DOC-POL-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Standard property names.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description; created 2013 → Title, identifier (ACE-DOC-POL-001), subject, category, keywords and description set; created Nov 2026. *Word's own fields agree with the document.*

### ACE-DOC-PRC-001_Procedure_RevA.docx

- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 17 properties, non-standard names; DocumentID was ACE-DOC-PRC-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Standard property names.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description; created 2013 → Title, identifier (ACE-DOC-PRC-001), subject, category, keywords and description set; created Nov 2026. *Word's own fields agree with the document.*

### ACE-DOC-STD-001_Document_Records_Management_Standard_Rev01.docx

- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 19 properties, non-standard names; DocumentID was ACE-DOC-STD-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Standard property names.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-DOC-STD-001), subject, category, keywords and description set. *Word's own fields agree with the document.*

### ACE-DOC-STD-002_Operational_Document_Publishing_Standard_Rev01.docx

- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 19 properties, non-standard names; DocumentID was ACE-DOC-STD-002 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Standard property names.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-DOC-STD-002), subject, category, keywords and description set. *Word's own fields agree with the document.*

### ACE-MNT-STD-001_Maintenance_Management_Standard_Rev01.docx

- **Control field DocumentOwner:** VP Operations → Sophia Hosany — VP Operations. *Field held a role or system name, not a named person from the org chart.*
- **Control field Custodian:** Maintenance & Integrity Manager → Marc Gomes — Maintenance & Integrity Manager. *Field held a role or system name, not a named person from the org chart.*
- **Job title:** Rohan Ali — Plant Manager, CPF → Rohan Ali — Plant Manager - Central Processing Facility. *Matches the ACE org chart (2 places).*
- **Control field Framework:** IOGP Report 510 (2014); ACE-OMS-MAN-001; ONE publication standards → IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 03. *Same wording in every document.*
- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 20 properties, non-standard names; DocumentID was ACE-RSK-STD-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Hidden properties disagreed with the document.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-MNT-STD-001), subject, category, keywords and description set. *Word's own fields agree with the document.*

### ACE-MOC-PRC-001_Management_of_Change_Procedure_Rev01.docx

- **Job title:** Rohan Ali — Plant Manager, CPF → Rohan Ali — Plant Manager - Central Processing Facility. *Matches the ACE org chart (2 places).*
- **Control field Framework:** IOGP Report 510 (2014); ACE-OMS-MAN-001; ONE publication standards → IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 03. *Same wording in every document.*
- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 20 properties, non-standard names; DocumentID was ACE-RSK-STD-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Hidden properties disagreed with the document.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-MOC-PRC-001), subject, category, keywords and description set. *Word's own fields agree with the document.*

### ACE-PRF-STD-002_Assurance_and_Audit_Standard_Rev01.docx

- **Control field Framework:** IOGP Report 510 (2014); ACE-OMS-MAN-001; ONE publication standards → IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 03. *Same wording in every document.*
- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 20 properties, non-standard names; DocumentID was ACE-RSK-STD-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Hidden properties disagreed with the document.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-PRF-STD-002), subject, category, keywords and description set. *Word's own fields agree with the document.*

### ACE-PSM-STD-001_Process_Safety_and_Hazard_Study_Standard_Rev01.docx

- **Job title:** Rohan Ali — Plant Manager, CPF → Rohan Ali — Plant Manager - Central Processing Facility. *Matches the ACE org chart (2 places).*
- **Warning wording (ODS.Warning):** This example shall not be used as… → Do not use this example as…. *Binding 'shall' belongs in a requirement style; warnings use plain instructions.*
- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 20 properties, non-standard names; DocumentID was ACE-PSM-STD-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Standard property names.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-PSM-STD-001), subject, category, keywords and description set. *Word's own fields agree with the document.*

### ACE-RSK-STD-001_Risk_Management_Standard_Rev01.docx

- **Title bookmark:** Title paragraph had no doc_title bookmark → doc_title bookmark added to the Title paragraph. *Title OMS tags now attach to the title (they were orphaned).*
- **Custom properties:** 20 properties, non-standard names; DocumentID was ACE-RSK-STD-001 → 22 properties, ODS.* names from the ONE master template, values copied from the control table. *Standard property names.*
- **Core properties:** Title empty; no identifier; mixed subject/category/description → Title, identifier (ACE-RSK-STD-001), subject, category, keywords and description set. *Word's own fields agree with the document.*

## Left as found — for your decision

- **Dates.** All 11 keep 1 January 2026. The OMS Manual Rev 03 still says effective 1 January 2027; I recommend moving the Manual's dates back (one file instead of eleven).
- **ACE-INC-STD-001 is missing from the repository.** The Wave 1 summary says it was written; only 11 files are in `finals/`.
- **Word lock file.** `finals/~$E-MOC-PRC-001…docx` is a temporary Word file uploaded by mistake. Delete it.
- **New document numbers.** ACE-DOC-POL-001 and ACE-DOC-PRC-001 are not in the OMS Manual register (Appendix 3) or the priority list. Add them, or confirm they are intended.
- **“Shall” in other binding styles.** Six “shall” statements sit in Responsibility or Risk Control styles (COW, DOC-STD-001, DOC-STD-002). I left them: these are binding styles. The publishing standard should say so explicitly: “shall” is allowed in Requirement, Responsibility, Approval, Record and Risk Control styles, and not in Warning, Note or Normal text.
- **Dual approval in PRF-STD-002** (George Habib and Nicole Lange): unchanged, as noted in your summary.
- **Attached template.** All files point to Word's Normal.dotm, not the ONE master template. Harmless for the test; worth fixing when the template is final.

## Recommendation for the template

Fix the cause, not only the files: the five wrong files were created from a copy of the Risk Management Standard rather than from the master template. In the template, the hidden properties should be **blank**, so a copied value can never survive unnoticed, and the gateway should keep comparing the control table with the properties.