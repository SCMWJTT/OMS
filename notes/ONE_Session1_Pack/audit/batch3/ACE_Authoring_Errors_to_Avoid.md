# ACE / ONE — Document Errors to Avoid

*Lessons from the Wave 1 file check, 21 November 2026. Use this before uploading any new document to the OMS repository.*

---

## The one rule behind most of the errors

**Every document holds its details in up to five places:**

1. the cover block (number, revision, status, effective date);
2. the **document control table** (the grey table after the cover);
3. Word's hidden **custom properties** (File › Info › Properties › Advanced › Custom);
4. Word's **built-in properties** (Title, Subject, Keywords and so on);
5. the **header and footer** text.

**The document control table is the master.** Fill it in once and correctly. Everything else must say exactly the same thing. The gateway check compares them, and the check script can rebuild 3 and 4 from the table. Places 1 and 5 you must update by hand.

---

## Errors found in Wave 1 and how to avoid them

### 1. Starting a new document from a copy of another document — serious

**What happened:** five documents (AIM, COW, MNT, MOC, PRF) were started from a copy of the Risk Management Standard. The visible pages were rewritten, but the hidden properties still said *ACE-RSK-STD-001, Risk Management Standard*, with Christina Bain as author and George Habib as approver. In Word everything looked right; the web reader showed all five as "Risk Management Standard".

**Avoid it:** always start from the master template: **File › New › Personal › ONE_ACE_Master_Template**, or double-click the `.dotx`. Never use "Save As" on an existing document to make a new one. Template v3 has its hidden properties **blank**, so a mistake shows up as missing rather than wrong.

**Check:** File › Info › Properties › Advanced › Custom. Every value must belong to *this* document.

### 2. Different property names

**What happened:** the template used the standard names (`ODS.DocumentId`, `ODS.DocumentType`, `ODS.DocumentOwner` …), but the finals used other names (`DocumentID`, `Type`, `Owner` …).

**Avoid it:** don't add, rename or delete custom properties. Use the 22 names in the template exactly:

`ODS.DocumentId` · `ODS.Title` · `ODS.DocumentType` · `ODS.Level` · `ODS.Revision` · `ODS.Status` · `ODS.IssueDate` · `ODS.EffectiveDate` · `ODS.Author` · `ODS.Reviewer` · `ODS.Endorser` · `ODS.Approver` · `ODS.DocumentOwner` · `ODS.ProcessOwner` · `ODS.Custodian` · `ODS.PrimaryFunction` · `ODS.Framework` · `ODS.TitleOMSTags` · `ODS.Classification` · `ODS.Applicability` · `ODS.ReviewInterval` · `ODS.RoleRegister`

**Value formats:**

| Property | Format |
|---|---|
| `ODS.DocumentType` | `Standard`, `Procedure`, `Policy` … (the word only) |
| `ODS.Level` | `2` (the number only) |
| `ODS.Revision` | `A`, `B` for drafts; `01`, `02` for approved issues |
| `ODS.Status` | `Draft`, `In Review`, `Approved`, `Superseded` or `Withdrawn` |
| Dates | `1 January 2026` style; leave blank in a draft |

### 3. Title tags not attached to the title

**What happened:** the template puts a hidden bookmark called `doc_title` on the Title paragraph. In the finals it had been lost, probably when the title was retyped or pasted over, so the title's OMS tags pointed at nothing.

**Avoid it:** don't delete the Title paragraph or paste a new one over it. Click inside the existing title and type. Use **Paste › Keep Text Only** when pasting into any heading.

**Check:** Insert › Bookmark, then tick *Hidden bookmarks*. `doc_title` must be listed, and **Go To** must land on the title.

### 4. Built-in properties left empty or stale

**What happened:** Word's Title field was empty in all 11 files. There was no document number in the built-in fields, and subject, category and description varied. The two drafts showed a 2013 creation date inherited from an old template.

**Avoid it:** in File › Info, fill in **Title** (the document title), **Tags** (the title OMS tags) and **Categories** (for example `Standard (Level 2)`). The check script fills in the rest.

### 5. A role instead of a person

**What happened:** COW and MNT listed the owner as just "VP Operations", and the custodians as "Control of Work System Owner" and "Maintenance & Integrity Manager".

**Avoid it:** always write **Name — Job title**, exactly as in the ACE organisation workbook, for example *Sophia Hosany — VP Operations*. Committees are allowed only as endorsers (for example *Technical Leadership Council*).

### 6. Job titles that differ from the org chart

**What happened:** "Plant Manager, CPF" was used where the org chart says "Plant Manager - Central Processing Facility".

**Avoid it:** copy titles from `ACE_People.csv`. Don't shorten them.

### 7. Free-text fields worded differently in each document

**What happened:** the Framework field said three different things across the 11 files.

**Avoid it:** use the fixed wording **IOGP Report 510 (2014); ACE-OMS-MAN-001 Rev 03**.

### 8. "Shall" in the wrong style

**What happened:** the Process Safety standard had a warning reading "This example shall not be used…". A warning is not a requirement style, so the binding word was in the wrong place.

**The rule:**

| "Shall" is allowed in | "Shall" is not allowed in |
|---|---|
| ODS.Requirement · ODS.Responsibility · ODS.ApprovalRequirement · ODS.RecordRequirement · ODS.RiskControl | ODS.Warning · ODS.Note · ODS.Example · Normal text · List Bullet · table cells |

**Fix it when you see it:**
- **If the sentence is binding,** cut it into its own paragraph and apply **ODS.Requirement**.
- **If it is a caution,** rewrite it as a plain instruction: "Do not…", "Stop and…", "Check…".
- Example: *"This example shall not be used as a SIL determination"* becomes *"Do not use this example as a SIL determination."*

**Find them quickly in Word:** Ctrl+H › More › tick *Find whole words only* › Find what: `shall` › **Format › Style** › choose ODS.Warning, then click *Find Next*. Repeat for ODS.Note and Normal.

### 9. Files that should not be uploaded

**What happened:** `~$E-MOC-PRC-001…docx` was uploaded. It is a temporary lock file Word creates while a document is open, and it is still in the repository.

**Avoid it:** close Word before uploading. Never upload files whose names start with `~$`. Delete this one from the `finals` folder.

### 10. Missing files

**What happened:** the Incident standard (ACE-INC-STD-001) is listed as complete but is not in the repository, and is not in the latest upload either.

**Avoid it:** after uploading, compare the repository folder with the priority list.

### 11. Old template left a placeholder number in Word's hidden fields (batch 3)

**What happened:** the OMS Policy and the Deviation standard carried `ACE-AAA-STD-001` in Word's built-in document number field, and the Word Title field was empty. This is template v2's placeholder; template v3 has it blank.

**Avoid it:** always start from the latest template (now **v4**). Delete older templates from your computer and the repository so they can't be picked by mistake. In File › Info, fill in **Title**.

### 12. Unused pictures inside the template (batch 3)

**What happened:** the template carried 13 images that appear nowhere in it, and every new document inherited them. Each file was about 1 MB instead of about 130 KB.

**Avoid it:** use template **v4**, which has the unused images removed. If you ever copy pictures into a template to try them out, delete them before saving. The template should contain only the ONE mark and the ACE logo.

### 13. XML written in the wrong order by the document generator (batch 3)

**What happened:** in the two new files, the tool that produced them wrote parts of the Word file in an order Word's rules don't allow:
- the heading bookmark before the paragraph settings, on every heading;
- tag-control labels in the wrong order;
- shading entries with a missing value;
- table and cell settings out of sequence.

Word usually copes, but it can trigger a "Word found unreadable content" repair, and a repair can silently drop bookmarks, and with them the OMS tags.

**Avoid it:** fix the tool that writes the tags and bookmarks. Bookmarks go *after* the paragraph settings (`w:pPr`), never before. Until then, put every new file through the check before uploading; the corrections are automatic and change nothing you can see.

---

## The "shall" fix in the template

Template v4 (`ONE_ACE_Master_Template_v4.dotx`, same as v3 without the unused images) contains:
- a **template guidance note** (ODS.Note style) directly after the example requirement, stating the "shall" rule above and telling the author to remove it before issue;
- an **example warning** written as a plain instruction ("Do not start work on a safety-critical element until the isolation has been verified."), so authors copy the right pattern.

If you edit the template yourself, open the `.dotx` with **right-click › Open** (double-clicking makes a new document instead):

1. **Modify each style's description.** Home › Styles pane › right-click **ODS.Warning** › Modify. Leave the formatting alone; these styles are described as follows:
   - ODS.Warning: "Personnel-safety warning. Plain instruction. No 'shall'."
   - ODS.Note: "Non-binding note. No 'shall'."
   - ODS.Requirement: "Binding requirement. Use 'shall'."
2. **Put the rule in the publishing standard.** At the next revision of ACE-DOC-STD-002, add one requirement listing the allowed and disallowed styles from the table above. That makes the gateway rule and the written rule the same.

---

## The logo

- The ACE logo (`images/logo.png`, flame mark) appears **once, on the cover only**, top right, beside the ONE mark. It is not repeated in headers or footers. `images/logo_lg.png` is the large master copy for print and web use.
- **Template v2** *linked* the logo with an INCLUDEPICTURE field. It only appeared if the `images` folder sat next to the file; otherwise the cover showed the text "[images/logo.png]".
- **Template v3** *embeds* the logo, so it travels inside every document.
- The finals already have the logo embedded. The old `LogoAssetPath` property was removed; it isn't needed.
- **Rule:** never re-insert the logo as a link. If you replace it, use Insert › Pictures › This Device, and don't choose "Link to File".

---

## Before you upload: checklist

1. Started from **template v4**, not a copy of another document.
2. Document control table complete. Every person is **Name — Job title** from the org chart.
3. Cover block, header and footer match the table (number, revision, status, date).
4. File › Info: Title, Tags and Categories filled in.
5. Custom properties belong to this document (File › Info › Properties › Advanced › Custom).
6. `doc_title` bookmark is on the title (Insert › Bookmark › Hidden bookmarks).
7. Every heading has its OMS tag line: numbers only, comma-separated, most relevant first, no duplicates.
8. No "shall" in Warning, Note or Normal text (Find with style filter).
9. Template guidance paragraphs deleted.
10. File name follows `ACE-AAA-TTT-NNN_Title_With_Underscores_Rev01.docx` (drafts: `_RevA`).
11. Word closed before upload. No `~$` files.
12. Run the web reader's **Check document** on the file. It must say *Passes the gateway* (drafts may show the "no dates" warning).
