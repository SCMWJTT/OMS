from specutil import who  # noqa
# Template v5 content: placeholders and guidance. Converted to .dotx after building.
X = "[Name — Job title]"
body = [
("h1", "Purpose, scope and parent Standard", "7.1"),
("p", "[Say what this document turns into method or requirement, where it applies (sites PAP, CHB, SAP, CPF, LND, PLB, HOF) and name its parent document. "
      "Replace the tags in every tag line: primary first, one to three per section, from the 54 OMS expectations.]"),
("ext", "[External standards: cite by number and title. Do not quote them.]"),
("h1", "Roles and technical authority", "3.1"),
("t", [["Role", "Named person", "Accountability"], ["[Role]", X, "[What they are accountable for]"]], [2, 3, 4]),
("resp", "[Responsibility statement: The <role> shall <duty>. Only the five binding styles may contain the word ‘shall’.]"),
("h1", "[Method section title]", "7.1"),
("p", "[Guidance text in Normal. No binding words here.]"),
("req", "[Requirement: one requirement per paragraph, using ‘shall’.]"),
("appr", "[Approval requirement: who approves what.]"),
("rec", "[Record requirement: what record is kept, where and for how long.]"),
("rc", "[Control statement: what is done, by whom, how often (C-SSS-001). Replace C-SSS-001 with an ID from your allocated block.]"),
("note", "[Note: explanation only.]"),
("warn", "[Warning: written as a plain instruction, e.g. ‘Do not…’.]"),
("h1", "Records, data and systems", "7.4"),
("p", "[What the method produces, where it is kept (CMMS, ONE, registers) and the data quality rules.]"),
("h1", "Performance and verification", "9.1"),
("kpi", "[Leading and lagging indicators with targets.]"),
("h1", "Implementing processes and procedures", "7.1, 7.4"),
("t", [["Number", "Title", "Status", "Steps relied on"], ["ACE-SSS-PRS-NNN", "[Process title]", "[Current / Planned]", "[Steps]"]], [2, 3, 1.2, 3.4]),
]
controls = [("C-SSS-001", "[Short control statement]", "[Risk or threat]", "3", "[Process step]", "[Evidence or record]")]
SPEC = dict(
    meta=dict(DocumentId="ACE-SSS-TTT-NNN", Title="[Document title]", DocumentType="[Standard / Practice / Procedure…]", Level="[1–5]",
              Revision="A", Status="Draft", IssueDate="[1 January 2026]", EffectiveDate="[1 January 2026]",
              Author=X, Reviewer=X, Endorser="[Name — Job title, committee, or Not required]", Approver=X, DocumentOwner=X,
              ProcessOwner="Not applicable", Custodian=X, PrimaryFunction="[ACE function]", TitleOMSTags="[x.y, x.y]",
              Classification="Internal", Applicability="[Sites or functions]", ReviewInterval="Three years; earlier if triggered",
              RoleRegister="[Roles used in this document]", Parent="[ACE-SSS-TTT-NNN]"),
    label="ACE  /  LEVEL [n] [TYPE]  /  CONTROLLED DOCUMENT",
    subtitle="[One-line summary of the document.]",
    history=[("A", "[date]", "[Reason for this revision]")],
    processes=None, body=body, controls=controls)
