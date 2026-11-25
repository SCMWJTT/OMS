# ONE Session 4: writing the ACE policies

Instructions for a fresh session whose only job is to write the ACE policies as Word drafts. **What** each policy must say is in `notes/ONE_Session3_Policy_Brief.md`. **How** to produce them is in this file. Where the two differ, this file wins.

Repo: SCMWJTT/OMS (live site oms.cynmark.app). Work on a branch and open a pull request; Wilmark merges on the GitHub website.

## 1. The user

Wilmark (Cynmark Systems Limited), former OMS documentation consultant in Trinidad oil and gas, now building ONE. He is not a programmer: short, plain-language answers; no npm or terminal for him; no long lists of alternatives during build work. ACE (Acme Caribbean Energy) is fictitious. Use only fictitious names: "the Gas Buyer", "the environmental regulator", "the energy ministry". Never name real companies, agencies or institutions.

## 2. Read first, in this order

1. `notes/ONE_Session3_Policy_Brief.md`: Parts A to E (what is missing, the skeleton, the set, one card per policy, and which policy governs which process). Part F is **not** for this session.
2. `protocol/ONE_Document_Standard.md`: styles, tags, controls, roles, self-check. Appendix A lists the 54 valid tags.
3. The two issued policies in `finals/`: ACE-LDR-POL-001 and ACE-DOC-POL-001.
4. ACE-BPM-PRA-001 §3 (the golden thread) and §5 (one governing policy per process).
5. `company/ACE_People.csv` and `company/org/roles.csv` for names and exact job titles.

## 3. What to produce

Eleven Word files in **`drafts/`**, all **for consideration**, none in `finals/`:

| # | File | Kind |
|---|---|---|
| 0 | ACE-LDR-POL-001, draft of Rev 02 | revision of the issued policy |
| 1 | ACE-OMS-POL-001 | new |
| 2 | ACE-RSK-POL-001 | new |
| 3 | ACE-CON-POL-001 | new |
| 4 | ACE-PPL-POL-001 | new |
| 5 | ACE-HMA-POL-001 | new |
| 6 | ACE-FIN-POL-001 | new (needs the FIN code, section 6) |
| 7 | ACE-LDR-POL-002 | new |
| 8 | ACE-ENV-POL-001 | new |
| 9 | ACE-SEC-POL-001 | new (owner decision first, section 7) |
| 10 | ACE-STK-POL-001 | new |
| 11 | ACE-DOC-POL-001, corrected | adds the section 6 tables |

Write them in the brief's order: **0, 1, 2, 3 first** (they drive the three worked processes and the CI dimension), then the rest. Show Wilmark the first one (LDR-POL-001 Rev 02 draft) before writing the others, so he can correct the pattern once.

Also hand back a short **`drafts/ONE_Policies_Draft_Notes.md`**: one paragraph per policy on the choices made (values chosen, thresholds proposed, anything that needs his decision).

## 4. Build every file from the template

- The source of styles, cover, content controls and front matter is **`templates/ONE_ACE_Master_Template_v5.dotx`**. Every paragraph uses a style from that template. No manual formatting.
- The Session 2 generator is the fastest route and gives the STRICT format (tags, Control IDs and metadata in content controls):
  - `notes/ONE_Session2_Pack/tools/gen.py` builds a docx from a Python spec; its `shell.docx` is a passed final made on the v5 template.
  - `notes/ONE_Session2_Pack/specs/ACE-DOC-POL-001.py` is the spec of an issued policy: copy its pattern.
  - `specutil.py` and `people.py` give helpers (`who("Name")` returns "Name — Job title" from the staff list).
  - `run.py` and the specs have hard-coded paths (`/home/claude/...`); point them at the repo copy.
- For the two revisions (LDR-POL-001, DOC-POL-001), **start from the issued Word file** and edit it, so everything already approved stays exactly as it is. Leave the issued files in `finals/` untouched; the drafts are new files.
- Check the result against the template: the style names in the output must all exist in the template.

## 5. Document settings for the drafts

| Setting | New policies | Revision drafts (LDR-POL-001, DOC-POL-001) |
|---|---|---|
| Revision | `A` | the next letter not used in that document's revision history (DOC-POL-001 already used A, so B) |
| Status | `In Review` | `In Review` |
| Revision history | A, "Initial draft for review. Proposed effective date 1 January 2027." | add a row: letter, "Draft for Rev 02: <what changed>. Proposed effective date 1 January 2027." |
| Issue date, Effective date | leave blank (set at approval) | leave blank |
| Level | 1 | 1 |
| Document owner | as in the brief's Part C table | unchanged unless the brief says otherwise |
| Approver | Satesh Sankar — Chief Executive Officer | same |
| Endorser | Executive Leadership Team | same |
| Author | a sensible author in the owner's function (Name — Job title from the staff list) | same as issued, or as appropriate |
| Reviewers | 3 to 6 relevant VPs, leads or managers | |
| Custodian | the system's document custodian (OMS-POL-001: Gary Ho Sing — Manager, Strategy & Planning) | |
| Parent | ACE-LDR-POL-001 for every new policy; LDR-POL-001 itself has none | |
| Review interval | Three years; earlier if triggered | |
| Title OMS tags | as in each card (1 to 3) | |
| File name | `ACE-XXX-POL-001_Title_Words_RevA.docx` | `ACE-LDR-POL-001_..._RevA.docx` (or the letter used) |

People are named as "Name — Job title" exactly as in `company/ACE_People.csv`, current staff only (Status Active). Note: Marc Gomes has left; the Maintenance & Integrity Manager is now Keisha Ramnarine.

## 6. Add the FIN system code first

ACE-FIN-POL-001 fails the checker until the code exists:
- add `FIN`, "Finance and Financial Control", elements 2 and 3, to the system list in `protocol/build/build_protocol.py`, then regenerate `protocol/one-protocol.json` with that script;
- add the same row to Appendix B.1 of `protocol/ONE_Document_Standard.md`.

## 7. Decision needed before SEC-POL-001

Ask Wilmark: is the owner the VP HSE & Compliance (physical security leads) or the VP IT, Data & Knowledge (OT cyber leads)? One owner only.

## 8. Writing rules (reminders)

- Use the **B1 skeleton** from the brief for every policy: 1 Purpose, scope and applicability; 2 Our commitments (one Heading 2 per commitment, each with its own tag line); 3 Accountabilities (table); 4 Decision rights and thresholds (only where the policy sets them); 5 How we will know (KPIs, objectives, review frequency); 6 Governed processes and implementing documents (two tables, process IDs from Part E, Current or Planned); Appendix A Controls (only if any).
- **Commitments are outcomes, not steps.** Steps belong in processes and procedures.
- **Each commitment names one or more ACE values** from LDR-POL-001 Rev 02. Write LDR-POL-001 first, so the values exist.
- **Thresholds are numbers or matrix bands**, never "significant". They become the branches in the process maps. Keep every number the brief proposes unless there is a clear reason to change it, and list any change in the draft notes.
- **Cycle frequencies are stated** where the card lists them (quarterly, annual and so on). The process maps read them.
- *Shall* only in the five binding styles; never in tables. Policies are mostly commitments in Normal style with a few binding statements; keep binding statements for real obligations.
- Exact job titles from `company/org/roles.csv`; OMS duties (Area Authority, Technical Authority…) as listed in the Document Standard Appendix C.
- Every Heading 1 and Heading 2 has a tag line with 1 to 3 valid tags, primary first.
- References to other documents by number (`ACE-RSK-STD-001`), including planned ones listed in `registers/DOC-REG-001.csv`.
- Mission, vision and values in LDR-POL-001 Rev 02: each value is its **own Heading 2**, so processes and policies can link to it.

## 9. Check before handing back

Run the checker on the drafts folder (it needs the jszip package):

```
node protocol/engine/cli.js . drafts
```

Target: every policy **PASS**. Warnings are acceptable when they only say a date or person is still to be completed. Fix any error. Then run the Document Standard's self-check (section 12) by eye on each file.

Drafts do not appear on the live site (the site reads `finals/` and `manuals/`), so nothing changes for visitors until Wilmark moves a policy to `finals/`.

## 10. Out of scope for this session

- Moving files to `finals/`.
- Brief Part F: re-parenting the Wave 1 documents, updating BPM-REG-001, new L2 groups in BPM-PRA-001, portal changes.
- Any process maps or CI work. That resumes in the Process session once the policies are accepted.

## 11. Done when

- [ ] FIN code added to the protocol and the Document Standard.
- [ ] Eleven policy drafts in `drafts/`, built from the v5 template, each following the B1 skeleton.
- [ ] All eleven pass the checker (draft-only warnings allowed).
- [ ] `drafts/ONE_Policies_Draft_Notes.md` lists the choices and open decisions.
- [ ] One pull request with all of it.
