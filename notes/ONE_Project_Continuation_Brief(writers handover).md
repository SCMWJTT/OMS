# ONE Document Publishing System — Continuation Brief

Use this brief to continue the OMS/ONE documentation project in a new ChatGPT conversation. Preserve the established terminology, decisions, document-control rules and workflow. Do not restart the architecture or invent missing source requirements.


## 1. Project purpose

**ONE = One Management System.** The project is an OMS document publishing and navigation system for **ACME Caribbean Energy Limited (ACE)**, based on IOGP OMS concepts and adapted to the company's organizational structure, roles, processes and technical authorities.

The goal is not simply to produce a library of Word files. Approved controlled Word documents remain the authoritative source in the company's repository. ONE will publish and navigate their structured content through:
- OMS elements / expectations and tags;
- ACE organizational functions and responsibilities;
- cross-functional business process maps;
- linked standards, practices, procedures, work instructions, records and controls.

Eventually, ONE should let a user find a requirement, see its accountable owner and process context, follow the process, and open the authoritative document section.


## 2. Architecture and document hierarchy

The current architecture distinguishes documents by purpose:
- **POL — Policy:** commitment, intent and principles.
- **STD — Standard:** mandatory requirements and what must be met.
- **PRA — Practice:** discipline-specific or business-framework methods, technical criteria and how ACE applies recognized practices.
- **PRS — Process:** cross-functional activity sequence, ownership, hand-offs, decisions, controls, inputs/outputs and records.
- **PRC / PLN — Procedure / Plan:** execution detail and arrangements for activities.
- **Work Instructions / Records:** task-level directions and evidence.

Practices and Standards are not substitutes for process maps. Process maps sit between technical/business requirements and procedures, representing how the work actually flows through ACE. Technical Authority and Process Owner may be different roles; do not conflate them.


## 3. Process mapping principles — critical

- Use the **actual ACE organization, role titles, reporting lines and functional boundaries** from the supplied organization chart / people register. Never create generic swimlanes if ACE roles are available.
- Processes should be genuinely cross-functional where the business activity crosses functions.
- For each process, define owner, purpose, trigger, inputs, outputs, steps, decision gateways, hand-offs, accountable/performing roles, controls, Control IDs, records/evidence, systems and linked documents.
- Make the process traceable to technical requirements and risks/barriers.
- Preserve explicit distinction between process accountability and technical endorsement/authority.
- Process maps should later be supported by a consistent machine-readable JSON model, using the actual handover/schema when supplied. Do not invent a canonical JSON schema if the source schema is missing.


## 4. Current document programme and progress

There were 20 priority Policies/Standards previously reported as completed (the exact priority register should be checked/reconciled if available; do not assume the count or order is independently verified). A newer writer brief introduces a set of **10 Practices**.

### New Practice priority set (from the writer brief)
**Business/process framework Practices:**
1. ACE-BPM-PRA-001 — Business Process Management Practice — reported completed.
2. ACE-BPM-PRA-002 — Process Modelling and Process File Practice — reported completed.
3. ACE-BPM-PRA-003 — Process Ownership and Continuous Improvement Practice — produced, but not yet quality-approved.
4. ACE-RSK-PRA-001 — Controls and Barrier Linkage Practice — produced, but not yet quality-approved.

**Discipline Practices listed in the brief:**
5. ACE-OPS-PRA-001 — Operating Envelopes and Integrity Operating Windows Practice.
6. ACE-WEL-PRA-001 — Well Barriers and Well Handover Practice.
7. ACE-AIM-PRA-001 — Risk-Based Inspection and Corrosion Management Practice.
8. ACE-MNT-PRA-001 — Equipment Criticality and SCE Maintenance Practice.
9. ACE-LOG-PRA-001 — Marine and Aviation Logistics Practice.
10. ACE-HMA-PRA-001 — Hydrocarbon Measurement and Allocation Practice.

The next document(s) to continue from this list should be confirmed against the priority brief/register. The four listed above have been produced, but PRA-003 and RSK-PRA-001 are not yet considered quality-test passed.

### Documents just produced (latest batch)
- ACE-BPM-PRA-003 — Process Ownership and Continuous Improvement Practice, Draft Rev A.
- ACE-RSK-PRA-001 — Controls and Barrier Linkage Practice, Draft Rev A.

These are only **7 pages each**, while the writer brief's recommended range is 12–30 pages. The previous response explicitly flagged them as underdeveloped and **not ready for auditor approval**. Expand substantively—not with filler—and quality-test them before considering approved.

### Prior business-process Practices (reported as produced)
- ACE-BPM-PRA-001 — Business Process Management Practice, Draft Rev A (20 pages, reported).
- ACE-BPM-PRA-002 — Process Modelling and Process File Practice, Draft Rev A (25 pages, reported).
These have documented caveats: the actual v5 template was not available at the time, Role Register IDs were pending, and the canonical JSON schema / Handover Section 11 was not available. Confirm whether these files have since been corrected against the true source materials before treating them as compliant.


## 5. Template, document standards and authoring rules

- **ONE Master Template v5 (.dotx)** was recently generated and linked in the previous conversation: `ONE_ACE_Master_Template_v5.dotx`. It was created from available v4 plus requirements, because the actual v5 template was not present at that time. Therefore do not claim it is an exact official v5 implementation until it is compared against the source specification/template.
- Use the master template for every new document; never copy an existing document as a base.
- The Word **Title** built-in property must always be populated (this error occurred repeatedly in earlier files). Title property must match the document title.
- New Practice documents: **Draft Revision A**, no approval/effective dates (leave blank as required by writer brief).
- Earlier approved documents used dates **1 January 2026** when instructed.
- Follow current document standard and corrections file exactly; check the latest versions before generating.
- Earlier template issues: pointed/table elements extended beyond printable margins; keep tables and shapes within page boundaries.
- Cover branding: ONE mark and ACE logo; ACE logo embedded, not externally linked, and only on front page. Do not add placeholder text such as “ACE company logo.”
- Maintain the required metadata fields/properties. The latest brief mentioned **23 custom properties including `ODS.Parent`**; verify exact property names/count against the current spec rather than guessing.
- Check title, document number, revision/status, dates, owner, approvals, built-in properties, custom properties, headers/footers, bookmarks and OMS tags for consistent identity.
- Use semantic Word styles and heading hierarchy; OMS tags must be attached according to the governing tagging convention. Earlier convention: Title = whole document, Heading 1 = chapter, Heading 2 = section; tags are numeric OMS tag values, comma-separated if multiple.
- Use “shall” only in permitted mandatory requirement styles/locations as defined by the current standard. Avoid decorative use of “shall.”
- Avoid empty pages, blank trailing pages, broken bookmarks/heading links, linked images, metadata mismatch, oversize tables, diagram labels crowding boxes and unnecessary blank sections.
- Include substantive content, appropriate tables, practical examples and diagrams when the document type supports them. Do not pad content to hit a page count. Verify visual rendering page-by-page.
- Ensure process-related documents define process interfaces, owner, role accountability, decisions, controls, inputs/outputs, records and linked docs, using ACE's real structure.


## 6. Quality gates before delivery

For every document, perform and report a real check of:
1. Correct clean master template source.
2. Correct filename, document number, title, revision, status and dates.
3. Word built-in Title property populated (critical recurring issue).
4. Required custom metadata properties present and consistent (exact names/count from spec).
5. Heading hierarchy, semantic styles and OMS tags.
6. Bookmark uniqueness and links validity.
7. Mandatory “shall” usage complies with standard.
8. Tables, diagrams, shapes and images within margins; no broken references.
9. ACE logo embedded and on cover only; ONE branding placement as specified.
10. Render all pages and inspect layout, pagination, diagrams and tables.
11. Content is substantial and specific to ACE's actual roles/structure; identify unresolved source data instead of inventing.
12. Any JSON model, if required, validates against the canonical schema (only when schema is available).

Do not state “passed,” “approved,” or “compliant” without actually completing the relevant checks. The external ONE publishing gateway has not been run in prior batches; distinguish local checks from gateway validation.


## 7. Source files that must be available in the new chat

Re-upload or attach the current source versions if not available in the new conversation:
- ONE Writer Brief for Standards and Practices (`ONE_Writer_Brief_Standard_Practices.md`)
- current document publishing standard and corrections/errors file (latest revision)
- actual ONE Master Template v5 DOTX, if the auditor/team has provided the official version
- OMS Manual Rev 04
- ACE organization chart and people / role register
- document priority list/register
- Handover Section 11 and canonical JSON process schema, if process-model files are being created
- logo assets, if template packaging/editing is required

Do not rely on a previous summary when these sources can be inspected. If files are missing, state that clearly and request them rather than guessing requirements.


## 8. Working style

The user prefers concise, direct responses and does not want code unless requirements are clear. Discuss choices first when requested. For document production, work in batches of two, report filenames/links, document identifiers and a concise quality-check summary. The user is testing documents with an auditor/quality gate; treat their corrections as authoritative and incorporate them into future work.


## 9. Continuation prompt to paste into the new chat

> Continue the ONE Document Publishing System project using the attached **ONE Project Continuation Brief** and the source documents I upload. First read the brief and current source files, confirm your understanding concisely, and reconcile the document progress/next two documents against the priority list. Do not generate any documents until you confirm the next pair and any missing inputs. Follow the latest document standard and corrections strictly. Critical recurring check: populate Word's built-in **Title** property. Use the official v5 template if supplied, not a reconstructed one. Create documents in batches of two, substantial and ACE-specific, with diagrams/tables where useful, and perform actual rendered/metadata checks before claiming quality pass.
