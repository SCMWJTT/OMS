# extracted from ACE-DOC-PRC-001_Procedure_RevA.docx
BODY = [('h1', 'Purpose, expected outputs and applicability', '1.7, 7.2'),
 ('p',
  'This Procedure describes the end-to-end work performed by document owners, authors, Technical Authorities, reviewers, approvers and Document '
  'Controllers. Its purpose is to ensure that staff use approved instructions, that changes are traceable and that business records remain reliable '
  'and available for the required period.'),
 ('p',
  'It covers controlled documents and records across ACE Head Office, the Point Lisas Shore Base, the Gulf of Paria platforms and pipelines, land '
  'leases, the Central Processing Facility, wells activity, projects and contractor interfaces. It applies to materials originally created in Word '
  'as well as received contractor or external documents accepted into ACE custody.'),
 ('req',
  'This Procedure shall be applied together with Part D of the OMS Manual. Where a more specific approved standard defines a greater requirement, '
  'the greater requirement shall govern.'),
 ('p',
  'The normal route creates one approved Word source, its registered metadata, a gateway evidence report, a publication event and communication '
  'evidence. For records, the route creates a captured record in an approved system of record, linked to its class, owner, retention and disposition '
  'rules.'),
 ('h1', 'Triggers, inputs and decisions', '1.7, 5.3'),
 ('p',
  'Use the document-control workflow whenever a new requirement is introduced, an existing instruction needs revision, an MOC affects an instruction '
  'or drawing, a regulation or contract changes, a review comes due, a user reports an error, or a document is proposed for retirement. Use the '
  'records-control workflow at the point that a decision or completed activity generates evidence that must be retained.'),
 ('t',
  [['Trigger', 'Originator / input', 'Expected control action'],
   ['New requirement or process', 'Function or system owner; approved business need', 'Initiate new controlled document and classify its type.'],
   ['Technical or operating change',
    'MOC owner; engineering or operations change package',
    'Determine affected source documents, drawings, forms, records and user competence.'],
   ['Periodic review',
    'Document register alerts; accountable document owner',
    'Verify continued validity, revise if needed or record no-change review.'],
   ['Incident, audit or reported inconsistency',
    'Area Authority, HSE, auditor or staff member',
    'Assess urgency and operating risk; open correction or restriction.'],
   ['Contractor deliverable',
    'Contract owner; verified vendor or consultant output',
    'Check acceptance criteria, asset applicability, custodian and record class.'],
   ['Records due for retention decision',
    'Record class owner; retention schedule report',
    'Verify hold status, audit or regulatory needs and disposition route.']]),
 ('h1', 'Roles, authorities and segregation of duties', '3.1, 7.2'),
 ('t',
  [['Role', 'Required activities / decision authority'],
   ['Requestor / process owner', 'States the business need, affected users, sites and process; supplies source evidence.'],
   ['Document owner', 'Accepts content responsibility, nominates author and reviewers, checks applicability and communicates revisions.'],
   ['Author / subject specialist', 'Creates accurate, implementable content, identifies requirements and records, and resolves review comments.'],
   ['Technical Writer — Ryan Ramsaran', 'Supports structure, procedural clarity, template use, section mapping and semantic styles.'],
   ['Document Controller — Allison St. Hill / Paul Gomes',
    'Allocates document identifiers through the register; verifies metadata and issue evidence; publishes and archives.'],
   ['Information Management Lead — Sanjay Jagessar',
    'Owns naming rules, register integrity, gateway exception decisions within delegated control, and publication assurance.'],
   ['OMS Manager — Marissa Bobb', 'Reviews expectation mapping and alignment with the 10-element OMS framework.'],
   ['Technical Authority', 'Endorses technical requirements, technical deviations and affected safety-critical content.'],
   ['Approver', 'Accepts the controlled content and the documented effect on their function or assigned authority.'],
   ['Area Authority / supervisor', 'Verifies that crews can retrieve and use current instructions; controls any local copies or restrictions.'],
   ['Records owner / Legal', 'Sets business retention class, determines hold applicability and authorises lawful disposition.'],
   ['Internal Audit & Risk Assurance', 'Samples the effectiveness and independence of the whole process.']]),
 ('req',
  'Document Control shall not substitute its publication check for the technical, operational or managerial approval required by the OMS Manual.'),
 ('req',
  'The author shall not self-approve a document unless an expressly authorised, recorded exception within the approval framework permits that '
  'arrangement.'),
 ('h2', 'Approval authority by document class', '2.2, 7.2'),
 ('t',
  [['Document class', 'Who approves', 'Technical endorsement'],
   ['Manual or policy (Level 1)', 'Chief Executive Officer', 'Executive Leadership Team; Legal and element owners review.'],
   ['Standard (Level 2)', 'System owner — Executive Leadership Team', 'Technical Authority where technical.'],
   ['Procedure, plan or guideline (Level 3)', 'Function manager', 'Technical Authority where technical.'],
   ['Work instruction, form or register (Level 4)', 'Responsible supervisor or manager', 'As required by governing technical content.'],
   ['Engineering standard or specification', 'Designated Technical Authority', 'Technical Leadership Council.']]),
 ('p',
  'A document may involve multiple functions. Its one approving role is assigned by the class and ownership rules above; affected functions review '
  'and Technical Authorities endorse within their recognised jurisdiction. The approval record also states the version actually reviewed.'),
 ('h1', 'Controlled document workflow', '7.2, 1.7, 7.4'),
 ('p',
  'The following stages are performed in sequence. The record of each gate must be sufficient to reconstruct who decided what and against which '
  'revision. An incomplete or rejected gate returns the document to the named owner or author with an actionable reason.'),
 ('t',
  [['Stage', 'Gate / output', 'Owner of the activity'],
   ['1 — Initiate', 'Approved request to draft, or written instruction to revise', 'Document owner / requestor'],
   ['2 — Register', 'Identifier, document class, registered owner and draft status', 'Document Controller'],
   ['3 — Author', 'Structured Word source and required technical attachments', 'Author and Technical Writer'],
   ['4 — Review', 'Comments, responses and consolidated review evidence', 'Affected function reviewers'],
   ['5 — Endorse', 'Technical approval evidence where required', 'Technical Authority'],
   ['6 — Approve', 'Decision made by the authorised approving role', 'Approver'],
   ['7 — Gateway', 'Completed automated and human publication checks', 'Document Control'],
   ['8 — Issue', 'Numbered Approved issue in repository; prior issue superseded', 'Document Controller'],
   ['9 — Deploy', 'Communication and training or briefing evidence', 'Document owner / line managers'],
   ['10 — Sustain', 'Periodic review, change monitoring and controlled withdrawal', 'Document owner / Document Control']]),
 ('h2', 'Stage 1 — Initiate and classify', '1.7, 7.1'),
 ('step',
  '1.  Requestor records the objective, scope, process or asset, affected locations, expected users, initiating change or compliance driver, and the '
  'planned implementation date.'),
 ('step',
  '2.  Document owner confirms whether an existing current document can be revised instead of creating a competing instruction. Search the ONE '
  'document map and register for overlaps or active supersession.'),
 ('step',
  '3.  Select the document class and ownership under the OMS Manual hierarchy. Identify whether the material is corporate, technical or '
  'site-specific, and whether technical endorsement or legal review is required.'),
 ('step',
  '4.  Identify other documents, drawings, forms, work instructions and roles affected. For an operating change, record the corresponding MOC '
  'reference and readiness dependency.'),
 ('rec', 'The initial request and classification decision shall be recorded with the document identifier or change package reference.'),
 ('rc',
  'Avoid parallel procedures for the same task unless the differences in asset, activity and authority are deliberate and clear. Reuse a single '
  'corporate standard with site-specific implementing documents where this is more reliable.'),
 ('h2', 'Stage 2 — Register and assign an identifier', '1.7'),
 ('step',
  '1.  Author or owner sends the document request to Document Control with type, owner, system code, proposed title and, where relevant, site code.'),
 ('step',
  '2.  Document Controller checks for duplicates and records the next available identifier under ACE-AAA-TTT-NNN-SSS. Use the three-letter system '
  'code and the controlled type-code table in the OMS Manual.'),
 ('step',
  '3.  Allocate the first working revision letter A and Draft status. Record the owner, custodian, named author, expected reviewers and next control '
  'checkpoint.'),
 ('req', 'Only Document Control shall issue a new document number. A retired or withdrawn number shall not be assigned to a new document.'),
 ('req',
  'A document changing to a different system or type shall receive a new identifier and explicit supersession mapping, rather than silently reusing '
  'its former identifier.'),
 ('p',
  'For example, a site-specific emergency plan may use ACE-EMR-PLN-001-CPF; a corporate procedure normally has no site suffix. Engineering standards '
  'use the prescribed engineering discipline number blocks.'),
 ('h2', 'Stage 3 — Author in the ONE Word template', '7.1, 1.7'),
 ('step',
  '1.  Create the source document from the controlled ONE template for its class. Do not begin by editing a downloaded PDF or an uncontrolled old '
  'copy.'),
 ('step',
  '2.  Populate the cover, document-control properties, subject and applicability, full approval route, revision history and the required framing '
  'sections: purpose, scope, definitions and references.'),
 ('step',
  '3.  Write an executable process in clear role-based language. Separate mandatory requirements, responsibilities, approval gates, records, risk '
  'controls and actual procedural steps using their corresponding ODS paragraph styles.'),
 ('step',
  '4.  Use Title and Heading 1, Heading 2 and Heading 3 only. Place the section numbers in heading text; use native Word tables, captions, pictures '
  'and editable cross-references as appropriate.'),
 ('step', '5.  Give each heading a stable bookmark so that ONE can link directly to that section even when its position in the document changes.'),
 ('step',
  '6.  Insert an OMS Tags content control beneath the document title and relevant headings. Use valid expectation numbers separated by commas, '
  'without E prefixes or duplicates, and ordered from most relevant first.'),
 ('req',
  'A heading-level OMS tag shall apply to that heading’s section. A child heading shall not inherit the parent’s tag as an explicit claim of its own '
  'coverage.'),
 ('p',
  'For example, an approval step may have OMS 7.2; the technical review section may independently carry OMS 6.4 and 7.2; the records section may '
  'carry OMS 1.7 and 9.5. Title tags indicate coverage for the overall document.'),
 ('rc',
  'Do not apply requirement styling to background description, or hide mandatory instructions in ordinary prose. The semantic style forms part of '
  'the machine-readable operational meaning.'),
 ('h2', 'Stage 4 — Internal quality check and review', '7.2, 3.1'),
 ('step',
  '1.  Author checks that each requirement has a clear owner or implementing role, each approval gate has a named authority, and each record has a '
  'capture and retention route.'),
 ('step',
  '2.  Technical Writer checks procedural order, consistent terminology, level of detail, numbering, referenced files, tables, semantic styles, '
  'bookmark uniqueness and tag syntax.'),
 ('step',
  '3.  Owner selects reviewers representing actual affected functions, Area Authorities and users. Where required, include HSE, Legal, Information '
  'Management and the OMS Manager.'),
 ('step',
  '4.  Issue the review copy as a lettered revision. Compile substantive comments in one review record with the reviewer, section, concern, response '
  'and disposition.'),
 ('step',
  '5.  Resolve contested requirements with the accountable functional owner and Technical Authority rather than silently removing safety or '
  'regulatory constraints.'),
 ('rec',
  'Review responses, disposition decisions and final source revision shall be retained as approval evidence associated with the document number.'),
 ('h2', 'Stage 5 — Technical endorsement and approval', '2.2, 7.2'),
 ('step',
  '1.  Identify the applicable approval route from the class matrix in section 3.1; verify the recorded owner and delegated authority remain '
  'current.'),
 ('step',
  '2.  Obtain technical endorsement for technical and safety-critical content, including design envelopes, asset integrity criteria, isolation '
  'requirements, competence restrictions and barriers where applicable.'),
 ('step',
  '3.  Provide the final reviewed Word source, open actions, resolved-comment record, change impact summary and effective-date proposal to the '
  'authorised approver.'),
 ('step',
  '4.  Record the approving role’s decision and date against the exact source revision and checksum or immutable repository version identifier.'),
 ('appr',
  'The approved issue shall not be released before all mandatory endorsements and approvals have been recorded; verbal agreement is not a substitute '
  'for issue evidence.'),
 ('p',
  'A material change after an approval decision invalidates that decision for the changed section unless the approver explicitly signs off the '
  'resulting revision. Editorial corrections that do not change meaning may use the controlled editorial-change path where authorised.'),
 ('h2', 'Stage 6 — Automated publishing gateway', '7.4, 1.7'),
 ('step',
  '1.  Document Controller sends the final Word source through the automated ONE gateway. Record file name, identifier, proposed revision and check '
  'timestamp.'),
 ('step',
  '2.  Validate the document identifier, uniqueness, class and revision against the document register; verify mandatory document properties and an '
  'approval record.'),
 ('step',
  '3.  Validate title tags and section tags for acceptable syntax, validity against the IOGP expectation register, order, duplicates and mapping to '
  'the registered document.'),
 ('step',
  '4.  Validate allowed heading levels, heading bookmarks, style use, and substantive mandatory obligations that have not been assigned the correct '
  'requirement style.'),
 ('step',
  '5.  Validate links to referenced ACE documents and identify missing or withdrawn targets, unavailable attachments and unrecognised site codes.'),
 ('step', '6.  Classify outcomes as Blocking, Review Required or Advisory; correct all blocking findings before controlled publication.'),
 ('t',
  [['Severity', 'Typical result', 'Required disposition'],
   ['Blocking',
    'Invalid document number; missing approval; duplicate/invalid OMS tag; missing core properties; unresolved mandatory-style failure.',
    'Reject publication and return to owner/author for correction.'],
   ['Review Required',
    'Unresolved link, untagged substantive section, unclear owner assignment, unusual document type usage.',
    'Document Controller documents decision and obtains owner clarification.'],
   ['Advisory',
    'Editorial consistency, presentation or accessibility improvements that do not change meaning.',
    'Record for improvement or correct before release where practicable.']]),
 ('appr',
  'A document that fails the gateway shall not be published until failures are corrected or a Document Controller records an accepted exception in '
  'accordance with the OMS Manual.'),
 ('p',
  'A check report is not a technical approval. The gateway checks structure, traceability and publication readiness; the approving authority remains '
  'accountable for the content.'),
 ('h2', 'Stage 7 — Issue, publish and supersede', '7.4, 1.7'),
 ('step',
  '1.  After approval and gateway clearance, Document Control assigns the next sequential numeric approved revision: first issue 01, then 02, 03 and '
  'so on.'),
 ('step',
  '2.  Update status to Approved and record issue date, effective date, approval evidence, owner, review due date, audience, registered content '
  'checksum and publication path.'),
 ('step',
  '3.  Place the approved Word source in the designated controlled repository and make the associated ONE views available from that source and its '
  'tags.'),
 ('step',
  '4.  Verify access to the full document and to the mapped heading sections through the OMS wheel, relevant function, process and role navigation '
  'where such mappings exist.'),
 ('step',
  '5.  Change the superseded revision status to Superseded, remove it from default active retrieval and retain it in the historical record with its '
  'effective period.'),
 ('step',
  '6.  Notify the document owner that the release is completed, provide the controlled location, and reconcile any previously registered controlled '
  'copies.'),
 ('rec',
  'The register, approved source, approval evidence, gateway report, publication log and superseded revision shall be retained as a traceable issue '
  'package.'),
 ('warn', 'Never use a draft, superseded, withdrawn or unverified local copy as the controlling instruction for a live operation.'),
 ('h2', 'Stage 8 — Communicate, brief and verify use', '7.3, 7.4'),
 ('step',
  '1.  Owner assesses the effect of the issue on operations, engineering, maintenance, wells, contractors, competence, permits, site packs and '
  'related work instructions.'),
 ('step',
  '2.  Identify the affected groups by function, location and role. For Pommerac A, include both offshore rotations and shore-based support; for CPF '
  'changes, include affected shift teams and contractor supervisors.'),
 ('step',
  '3.  Communicate the change, effective date, affected document numbers and superseded instructions. Use targeted briefing and competence '
  'verification when changed control steps affect personnel safety or asset barriers.'),
 ('step',
  '4.  Area Authorities or nominated supervisors verify that the current issue is retrievable at points of work and replace or withdraw registered '
  'local copies.'),
 ('step',
  '5.  Where an approved document is a prerequisite for a changed operation, confirm readiness before the new work proceeds under the applicable MOC '
  'or commissioning process.'),
 ('rec',
  'Briefing attendance, training acknowledgement, controlled-copy reconciliation and readiness decisions shall be retained when required by the '
  'change impact assessment.'),
 ('h2', 'Stage 9 — Periodic review, correction and revision', '1.7, 9.4'),
 ('step',
  '1.  Document Control provides review-due information to owners at an interval that leaves time for substantive review and authorisation before '
  'the expiry date.'),
 ('step',
  '2.  Owner checks applicable law, organisation, asset configuration, process, technical standard, lessons learned, user feedback, references, '
  'roles and records requirements.'),
 ('step',
  '3.  If content remains valid, retain a dated no-change review decision and reset the review due date under the governing cycle without '
  'misrepresenting the existing issue as a new revised text.'),
 ('step',
  '4.  If content changes, initiate the revision using the current approved source, a draft letter and a documented change summary. Repeat affected '
  'technical, operational and approval gates.'),
 ('step',
  '5.  If the document no longer applies, initiate controlled withdrawal and verify the effect on dependent documents and active work packs.'),
 ('req',
  'The review cycle shall be three years for policy, standards and procedures, annual for emergency plans and at least every five years for work '
  'instructions, forms and registers, unless a shorter applicable cycle is required.'),
 ('p',
  'Engineering standards and specifications also use a three-year cycle. An overdue review does not itself authorise a new instruction; the document '
  'owner must assess the risk and record a managed action.'),
 ('h2', 'Stage 10 — Withdraw and archive', '1.7, 7.4'),
 ('step',
  '1.  Owner raises a withdrawal request stating the reason, replacement or successor if any, asset and location impact, dependent references and '
  'planned withdrawal date.'),
 ('step',
  '2.  Document Control checks outstanding hyperlinks, ONE section mappings, active training resources, contractor work packs and controlled hard '
  'copies.'),
 ('step',
  '3.  Obtain the owner’s authorisation and any required function or Technical Authority input, then mark the affected issue Withdrawn at the '
  'approved effective date.'),
 ('step',
  '4.  Remove the withdrawn item from active operational navigation while maintaining a historical entry, reason, owner, revision and supersession '
  'trail.'),
 ('step',
  '5.  Archive the content and associated approval history under the controlled retention rule; do not delete the identifier or recycle its number.'),
 ('rec', 'Withdrawal approval, notification and archive location shall be recorded in the document register.'),
 ('h2', 'Urgent safety corrections and temporary instructions', '5.3, 8.4'),
 ('p',
  'Urgent information may be needed before a revised full document can complete the normal review cycle. The owner and Area Authority jointly assess '
  'whether work should stop, remain restricted, or proceed only under an approved interim control. An urgent correction must not be achieved by '
  'circulating an uncontrolled replacement instruction.'),
 ('step',
  '1.  Report the error or gap immediately to the Area Authority, accountable owner and Information Management Lead, including affected task, '
  'location and potential consequence.'),
 ('step',
  '2.  Determine whether Stop Work, MOC, operating deviation, temporary procedure, site instruction or formal notice is required within the relevant '
  'governing standard.'),
 ('step',
  '3.  Assign temporary document control, approver, scope, affected users, effective interval, expiry and withdrawal conditions before the interim '
  'instruction is used.'),
 ('step',
  '4.  Communicate to affected shifts and contractors and retain evidence of acknowledgement. Track conversion to the permanent controlled '
  'revision.'),
 ('appr',
  'No interim instruction shall bypass an applicable safety-critical approval, Technical Authority endorsement, Area Authority control or legal '
  'duty.'),
 ('rc', 'A short urgent work instruction is not a substitute for a full revision where the underlying process or barrier has materially changed.'),
 ('h1', 'Controlled copies, contractor documents and access', '7.4, 3.6'),
 ('h2', 'Controlled offline and hard-copy arrangements', '7.4'),
 ('p',
  'Some sites cannot assume continuous connectivity. Pommerac A, vessel operations, remote land leases and emergency teams may therefore maintain '
  'specially registered controlled sets for resilience, provided that they have a custodian and reconciliation process.'),
 ('step',
  '1.  Area Authority requests an offline or hard-copy control arrangement and identifies the document set, custodian, location and verification '
  'frequency.'),
 ('step', '2.  Document Control registers each controlled copy or signed offline package with its source revision and issued date.'),
 ('step',
  '3.  Site custodian checks publication updates, replaces changed copies and records withdrawal of obsolete copies before affected work proceeds.'),
 ('step',
  '4.  On restoration of connectivity, reconcile the local package and report any delay, discrepancy or use of outdated material as a '
  'document-control finding.'),
 ('rec', 'The controlled-copy register shall record copy ID, holder, location, source revision, date issued, last verified and date withdrawn.'),
 ('h2', 'Contractor and external-origin materials', '3.6, 1.7'),
 ('p',
  'Vendors supply equipment manuals, inspection certificates, drawings, test reports, commissioning records, as-built information and proprietary '
  'procedures. Their acceptance as ACE records does not automatically make every vendor instruction an ACE-controlled procedure.'),
 ('step',
  '1.  Contract owner identifies contractual deliverables, document format, intended ACE use, information sensitivity and acceptance criteria before '
  'handover.'),
 ('step',
  '2.  Technical Authority or nominated technical reviewer checks the content, completeness, revision and asset applicability of received technical '
  'deliverables.'),
 ('step',
  '3.  The record-class owner determines whether the item is a reference record, technical baseline, approved supplier procedure or source material '
  'for an ACE-controlled instruction.'),
 ('step',
  '4.  Document Control registers the received item and relationship to the ACE asset, contract, equipment tag, project and approved storage '
  'location.'),
 ('req',
  'A contractor procedure shall not displace an ACE-controlled operating requirement unless its use is formally accepted through the applicable '
  'contract bridging and approval process.'),
 ('h2', 'Access management and confidentiality', '9.5, 7.4'),
 ('req',
  'The system owner shall maintain access rights appropriate to the document or record classification, while ensuring that legitimate users can '
  'retrieve current operational requirements.'),
 ('p',
  'Read access to ordinary operational requirements is broad where possible; edit, approval, publication and disposal permissions are separated. '
  'Legal, personnel, medical, commercial and other restricted content is limited to authorised roles.'),
 ('rec', 'Changes to privileged access, ownership, major repository permissions and records-system configuration shall produce auditable evidence.'),
 ('h1', 'Records management workflow', '9.5, 1.7'),
 ('h2', 'Decide what becomes a record', '9.5'),
 ('p',
  'Records are generated by completing work, making decisions and verifying conditions. They differ from documents that instruct people on what to '
  'do. Some systems contain both: a permit template is a controlled document, whereas the completed permit is a record; an inspection plan is an '
  'instruction, whereas the signed inspection findings are records.'),
 ('step',
  '1.  At process design or document revision, identify the expected records, their operational purpose, governing requirement, originator and '
  'required approval or review.'),
 ('step',
  '2.  Assign each record class to a nominated owner and approved system of record; verify that it can be retrieved by asset, process, event, date '
  'or personnel identifier as required.'),
 ('step', '3.  Specify minimum metadata and record quality conditions before personnel begin using the related form or system.'),
 ('step',
  '4.  Verify that the record class appears in the retention register and is subject to the longest applicable requirement, including legal holds.'),
 ('h2', 'Capture and authenticate records', '9.5, 8.3'),
 ('rec',
  'A business record shall be captured promptly after the underlying action, with sufficient context to establish what was done, who did it, the '
  'applicable asset or scope, the date and the applicable review or approval.'),
 ('p',
  'Examples include a signed permit and isolation certificate, CMMS work-order completion and test result, safety-critical element inspection '
  'outcome, shift handover, training assessment, well intervention report, contract approval and investigation action verification.'),
 ('step',
  '1.  Originator creates the record using the approved system or controlled form and includes required identities, dates, references, asset or '
  'equipment tags, results and attachments.'),
 ('step', '2.  Supervisor, verifier or approver checks completeness and plausibility where the process requires a second-person review.'),
 ('step',
  '3.  Transfer or save the completed record in its system of record. Do not leave the only copy in a personal mailbox, chat exchange, removable '
  'drive or individual user folder.'),
 ('step',
  '4.  Identify any correction transparently. Preserve the original state or available audit history and associate the correcting person, time and '
  'justification with the revised record.'),
 ('rc',
  'A scanned signature page without its associated technical result, date, asset identity or full parent record may be inadequate evidence. Preserve '
  'the full evidential package and its context.'),
 ('h2', 'Index, link and protect', '9.5'),
 ('p',
  'Different records use different databases and controlled repositories. ONE does not require extracting or duplicating every record into one '
  'store; it needs an approved catalogue of record classes and reliable links to the controlling application.'),
 ('step',
  '1.  Record-class owner identifies mandatory indexing fields: record ID, associated document or activity, site or asset, record date, owner, '
  'classification and retention trigger.'),
 ('step',
  '2.  Information Management verifies that stored items are retrievable through authorised pathways and that superseded technical baselines remain '
  'traceable.'),
 ('step',
  '3.  System administrator confirms the required backup, restoration, integrity monitoring and access audit controls for the record’s risk and '
  'sensitivity.'),
 ('step',
  '4.  For physical originals, record the custody location, responsible holder and check-in/check-out controls; include a scanned reference where '
  'this is authorised and useful.'),
 ('h2', 'Apply the approved retention schedule', '1.7, 9.5'),
 ('p',
  'The OMS Manual establishes the following minimum corporate periods. The Document and Records Management Standard will maintain the full approved '
  'schedule, including more specific legal, licence and business retention obligations. Retention may not begin until the correct trigger (for '
  'example project closure, asset retirement or employment termination) is known.'),
 ('t',
  [['Record class', 'Minimum retention from OMS Manual', 'Typical system / owner'],
   ['Approved OMS documents and revision history', 'Life of the company', 'Controlled repository / Document Control'],
   ['Design, as-built and asset integrity records',
    'Life of the asset plus 10 years',
    'Engineering and integrity record systems / Engineering owner'],
   ['Permits to work and isolation certificates', '5 years', 'Control of Work records / Operations'],
   ['Incident investigations and HAZOP reports', 'Life of the asset plus 10 years', 'HSE / process safety records'],
   ['Competence and training records', 'Employment plus 10 years', 'People systems / Human Resources'],
   ['Health surveillance records', '40 years', 'Restricted occupational-health record service'],
   ['Audit reports and management reviews', '10 years', 'Assurance / Board governance records']]),
 ('req',
  'Where applicable law, contract, licence, investigation, safety case or other governing requirement demands longer preservation, the longer period '
  'shall prevail.'),
 ('h2', 'Hold, preservation and regulatory response', '9.5, 2.3'),
 ('step',
  '1.  Legal & Government Affairs, Internal Audit, HSE or the accountable record owner identifies the records likely to be relevant to a threatened '
  'or active proceeding, investigation, audit or regulatory request.'),
 ('step',
  '2.  Legal & Government Affairs defines the hold scope, start time, custodians and affected record systems and sends an instruction to the '
  'relevant record-class owners and system administrators.'),
 ('step',
  '3.  Information Management and affected system owners apply retention locks or equivalent preservation controls, suspend routine disposition, and '
  'log acknowledgement from custodians.'),
 ('step',
  '4.  Legal & Government Affairs reviews the hold periodically and authorises the documented release when appropriate; record-class owners then '
  'resume the ordinary retention assessment.'),
 ('rec',
  'Preservation notices, acknowledgements, affected record scope, release decisions and system control evidence shall be retained in the approved '
  'restricted repository.'),
 ('h2', 'Archive and dispose of eligible records', '1.7, 9.5'),
 ('step',
  '1.  Records owner produces an eligible-for-disposition list from approved retention rules and verified retention triggers. Remove records still '
  'needed for ongoing operations, contractual claims or active assets.'),
 ('step',
  '2.  Check active holds, pending inquiries, legal and regulatory needs, contract conditions and historical preservation requirements. Obtain Legal '
  'confirmation where applicable.'),
 ('step',
  '3.  Obtain an authorised disposal decision from the accountable record-class owner and Information Management, in line with the approved '
  'retention schedule and delegated authority.'),
 ('step',
  '4.  For permanent or extended-preservation records, transfer to the approved archival location with index, context, integrity protection and a '
  'retrieval owner.'),
 ('step',
  '5.  For approved destruction, perform secure deletion or witnessed physical destruction as appropriate to classification, and record the method '
  'and completion date.'),
 ('appr', 'No destruction shall proceed without documented authorisation and confirmation that retention and preservation conditions are satisfied.'),
 ('rec',
  'The disposal certificate shall include record classes, date range, source location, authorisation, hold check, destruction or archival method, '
  'operator and completion date.'),
 ('h2', 'Data migration and system replacement', '9.5, 7.4'),
 ('p',
  'Replacement of an engineering archive, enterprise content store, maintenance application or HR system must preserve evidence as well as the '
  'files. A technically successful migration is insufficient if revision history, signatures, assets, links or retention triggers are lost.'),
 ('step', '1.  System owner inventories affected record classes, document identifiers, dependencies, preserved revisions and records under hold.'),
 ('step',
  '2.  Define source-to-destination mappings for content, properties, authorship, history, access permissions and links; retain the source system as '
  'needed to establish fidelity.'),
 ('step', '3.  Run sampled completeness, readability, checksum, access and retrieval tests with record owners before cutover approval.'),
 ('step',
  '4.  Create a signed migration reconciliation report and controlled decommissioning decision. Archive source logs needed to explain subsequent '
  'record history.'),
 ('rec', 'Migration plans, test evidence, exception dispositions and acceptance decisions shall be retained as system-control records.'),
 ('h1', 'Incident handling, escalation and deviations', '5.4, 10.4'),
 ('h2', 'Error, obsolete information or publication failure', '5.4, 7.4'),
 ('p',
  'Any person may report a misleading procedure, wrong revision, broken ONE link, contradictory standard, missing safety-critical record or '
  'uncontrolled instruction. The response is proportional to the risk created by reliance on that information.'),
 ('step', '1.  Capture the affected document or record identifier, location, user, current activity, observed failure and potential consequence.'),
 ('step',
  '2.  Inform the document owner, Document Control and Area Authority where live operations could be affected. Apply Stop Work or task restriction '
  'where relevant.'),
 ('step', '3.  Owner classifies severity and determines if MOC, incident reporting, technical deviation or urgent document correction is required.'),
 ('step',
  '4.  Create an action record for correction, communication, evidence of removal of bad copies and verification that normal retrieval is restored.'),
 ('h2', 'Deviation and gateway exception', '2.6, 1.7'),
 ('p',
  'A formal deviation from a substantive OMS requirement belongs in the governed deviation process; a limited technical publishing exception (for '
  'example a known converter limitation that does not change the approved instruction) can be decided within delegated Document Control authority if '
  'the gateway rules permit it.'),
 ('req',
  'A gateway exception shall identify the specific check, reason, affected section, risk, compensating control, decision owner and expiry or '
  'corrective-action requirement.'),
 ('appr',
  'An administrative publication exception shall not permit missing approval, invalid operational authority, obsolete safety-critical instructions '
  'or breach of a legal retention obligation.'),
 ('h1', 'Registers, evidence and performance', '9.4, 9.5'),
 ('h2', 'Minimum document register fields', '1.7, 7.4'),
 ('t',
  [['Field group', 'Mandatory data / control purpose'],
   ['Identity', 'Document identifier, title, system, document type, site suffix, current issue, status.'],
   ['Authority', 'Owner, custodian, author, reviewer set, endorsement, approving role and approved evidence reference.'],
   ['Scope and navigation', 'Primary function, relevant business process, audience/roles, applicability and IOGP title tags.'],
   ['Lifecycle', 'Created, draft, review, issue and effective dates; review due; supersedes/replaced-by; withdrawal reason.'],
   ['Publication', 'Source location, file version or checksum, gateway result, ONE publication link and any controlled copies.'],
   ['Assurance', 'Exception register, open actions, history, correspondence, related MOC or incident and change impact.']]),
 ('h2', 'Minimum record class catalogue fields', '9.5'),
 ('t',
  [['Field group', 'Mandatory data / control purpose'],
   ['Record class', 'Class name, description, governing process and accountable owner.'],
   ['Storage', 'System of record, custodian, authorised access and backup/resilience classification.'],
   ['Context', 'Asset/site, business identifier, creator, creation date and associated approved document where relevant.'],
   ['Retention', 'Minimum period, legal basis where applicable, retention trigger, hold status and scheduled disposition.'],
   ['Disposition', 'Approving role, archive or destruction record, decision date and responsible operator.']]),
 ('h2', 'Monthly control checks and quarterly reporting', '9.4, 10.1'),
 ('step',
  '1.  Document Control checks overdue reviews, gateway failures, approved documents missing properties, inaccessible source files and unclosed '
  'replacement or withdrawal actions.'),
 ('step',
  '2.  Record-class owners sample expected evidence for completeness, accessibility and age-appropriate retention; prioritise major accident hazard, '
  'well integrity, maintenance and permit records.'),
 ('step',
  '3.  Information Management Lead consolidates exceptions by function, cause, operational consequence and trend, and proposes corrective action '
  'with owners and dates.'),
 ('step',
  '4.  VP IT, Data & Knowledge reviews quarterly performance with the OMS Manager and reports recurring or high-consequence weaknesses through ACE '
  'assurance and management review.'),
 ('p',
  'The OMS Manual sets the controlled-document overdue-review performance objective below 5%. Other indicators should be baselined and assigned '
  'targets by the DOC system owner rather than presenting unapproved targets as existing corporate requirements.'),
 ('h1', 'References and precedence', '1.7, 7.1'),
 ('ref', 'ACE-OMS-MAN-001, Rev 03 — One Management System Manual, especially sections A.4, A.6, D.1–D.7 and Appendix 3.'),
 ('ref', 'ACE-DOC-POL-001 — Document and Records Management Policy (associated draft policy; formal issue subject to approval).'),
 ('ref', 'ACE-DOC-STD-001 — Document and Records Management Standard (programme priority; verify approved revision before operational use).'),
 ('ref', 'ACE-DOC-STD-002 — Operational Document Publishing Standard (programme priority; verify approved revision before operational use).'),
 ('ref', 'ACE-MOC-PRC-001 — Management of Change Procedure (programme priority; verify approved revision before operational use).'),
 ('ref', 'ACE-OMS-STD-002 — Deviation and Exemption Standard (programme priority; verify approved revision before operational use).'),
 ('p',
  'If a referenced supporting document has not yet been issued as Approved, its planned identifier and title are provided for programme traceability '
  'only. This Procedure is subject to the already approved OMS Manual and cannot itself establish a substitute operational approval for a document '
  'still in draft.'),
 ('app', 'Release readiness checklist', '7.2, 7.4'),
 ('t',
  [['Check', 'Evidence or decision required'],
   ['Identity and register', 'Unique number, class, owner, status, revision and site code agree with the corporate register.'],
   ['Source structure', 'Current ONE Word template, Title/Heading 1–3, stable heading bookmarks, native tables.'],
   ['OMS linkage', 'Title and section tags valid, unique within each scope and aligned with registered expectations.'],
   ['Meaning and use', 'Mandatory requirements, duties, gates, warnings, risk controls, records and steps use correct styles.'],
   ['Technical correctness', 'Affected functions reviewed; Technical Authority endorsement recorded where required.'],
   ['Formal approval', 'Approver and authorised level verified; correct revision/version, date and decision captured.'],
   ['Publishing quality', 'Gateway passed or formal documented acceptable exception; final links and retrieval tested.'],
   ['Operational deployment', 'Audience, briefing, changes to other documents and site copies identified.'],
   ['Source and history', 'Final Word source, immutable evidence, superseded issues and next review are preserved.']]),
 ('app', 'Worked application examples', '7.4, 5.3'),
 ('h2', 'Pommerac A maintenance instruction change', '6.4, 7.4'),
 ('p',
  'A recurring ESD valve function test is changed because the equipment performance standard and maintenance task have been revised. The Maintenance '
  '& Integrity team identifies the work instruction, safety-critical element register, CMMS task, permit requirements and contractor briefing as '
  'affected items. The relevant Technical Authority endorses the technical change, the responsible manager approves the work instruction, and '
  'Document Control verifies metadata, tags and publication. The OIM ensures both offshore rotations receive the revised instruction before the next '
  'test. The old controlled copy is reconciled, and the approved test completion remains a maintenance record.'),
 ('h2', 'CPF procedure correction discovered on shift', '8.4, 7.4'),
 ('p',
  'A CPF operator finds that an approved procedure cites the wrong isolation point after a plant modification. The operator reports the discrepancy '
  'and the Plant Manager assesses the immediate task under Stop Work and MOC arrangements. The owner initiates a corrected controlled issue, '
  'documents the affected technical basis and obtains the required reviews. A temporary instruction is only used if approved within the applicable '
  'authority. When the revision is issued, the shift teams are briefed and the outdated local copy is withdrawn.'),
 ('h2', 'Contractor inspection deliverable', '9.5, 6.5'),
 ('p',
  'A contractor delivers an ultrasonic thickness survey for a CPF vessel. The Inspection Lead verifies the report, asset identification, instrument '
  'traceability and findings. Document Control or the nominated record custodian registers the accepted report in the integrity records system under '
  'the asset. The retention class follows the asset-life-plus-ten-years minimum, subject to any longer relevant requirement or preservation hold. '
  'ONE may link the controlling inspection standard without duplicating the signed report itself.'),
 ('app', 'Terms used in this Procedure', '1.7'),
 ('t',
  [['Term', 'Operational meaning'],
   ['Draft revision', 'Letter-coded source under preparation, review or approval; not valid as an approved instruction.'],
   ['Approved issue', 'Numeric revision authorised under the approval matrix and recorded in the controlled register.'],
   ['Gateway', 'Automated plus human acceptance controls required before publication.'],
   ['Superseded', 'Previously approved issue replaced by a newer authorised issue; kept for history.'],
   ['Withdrawn', 'Formerly governed document removed from current application by a recorded decision.'],
   ['Controlled copy', 'A specifically registered offline/hard-copy instance subject to reconciliation.'],
   ['Record class', 'Defined category of evidence with owner, system of record and retention rule.'],
   ['Retention trigger', 'Event that starts a records retention period, for example asset retirement or employee separation.'],
   ['Technical Authority', 'Designated discipline lead authorised to assess technical adequacy independent of line management.'],
   ['Area Authority', 'Accountable person controlling activities at the relevant facility or work area.']])]
