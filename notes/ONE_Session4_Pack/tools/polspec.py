"""Shared settings for the Session 4 policy drafts (new policies, Revision A, In Review)."""
from people import who

APPROVER = "Satesh Sankar"


def new_policy(doc, title, subtitle, owner, author, reviewers, custodian, function, tags, roles, body,
               applicability="All ACE activities, sites, employees and contractors", process_owner="Not applicable"):
    meta = dict(DocumentId=doc, Title=title, DocumentType="Policy", Level="1", Revision="A", Status="In Review",
                IssueDate="", EffectiveDate="", Author=who(author), Reviewer="; ".join(who(n) for n in reviewers),
                Endorser="Executive Leadership Team", Approver=who(APPROVER), DocumentOwner=who(owner),
                ProcessOwner=process_owner, Custodian=who(custodian), PrimaryFunction=function, TitleOMSTags=tags,
                Classification="Internal", Applicability=applicability, ReviewInterval="Three years; earlier if triggered",
                RoleRegister="; ".join(roles), Parent="ACE-LDR-POL-001")
    words = "_".join(w for w in title.replace(",", "").split())
    return dict(meta=meta, label="ACE  /  LEVEL 1 POLICY  /  DRAFT FOR REVIEW", subtitle=subtitle,
                cover_note="Proposed effective date 1 January 2027",
                history=[("A", "", "Initial draft for review. Proposed effective date 1 January 2027.")],
                file=f"{doc}_{words}_RevA.docx", processes=None, body=body, controls=None)


def values_note(policy_word="policy"):
    return ("p", f"Each commitment names the ACE values it serves, as set in ACE-LDR-POL-001 section 1. The steps that deliver the "
                 f"commitments are in the governed processes and implementing documents in section 6.")
