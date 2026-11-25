# ONE policy drafts: notes for Wilmark

Session 4, November 2026. All drafts are in `drafts/`, status In Review, built on the v5 layout with the Session 4 copy of the generator (`notes/ONE_Session4_Pack/`). Issue and effective dates are blank; proposed effective date 1 January 2027.

## Decisions taken at the start of the session

- **OMS Policy restructured** into the B1 skeleton, keeping every approved sentence (confirmed by Wilmark).
- **Mission, vision and five values** accepted as proposed; each value is its own Heading 2 with one or two sentences on what it means in practice.
- **Risk numbers follow the issued standards**, not the brief's examples: acceptance from ACE-RSK-STD-001, deviation periods from ACE-OMS-STD-002, change classes C1/C2/C3 from ACE-MOC-PRC-001.
- **Security policy owner** is the VP HSE & Compliance; the Telecoms & OT Cyber Security Lead (OT cyber) and VP IT, Data & Knowledge (IT systems) are named in its section 3.

## Patterns used in every policy

- Sections are always numbered the same way (1 Purpose…, 2 Our commitments, 3 Accountabilities, 4 Decision rights and thresholds, 5 How we will know, 6 Governed processes and implementing documents), so ONE finds each part in the same place. Where a policy sets no thresholds, section 4 says so and lists the decision rights it relies on, rather than being left out and shifting the numbers.
- Each commitment heading has a readable bookmark (for example `ACE-LDR-POL-001#COM_STOP_WORK`), and each value has one (`ACE-LDR-POL-001#VAL_SAFETY`), so processes can link to them.
- Each commitment opens with a sentence naming its values ("In line with our value …").
- Every new policy: Revision A, In Review, parent ACE-LDR-POL-001, approver the Chief Executive Officer, endorser the Executive Leadership Team, review interval "Three years; earlier if triggered", author and custodian from the owner's function, three to six reviewers. All people are current staff, named "Name — Job title" from the staff list.
- Section 3 names people in the *Named person* column, as the brief's skeleton asks. Where a governed process is a new candidate with no register entry, its owner is marked "proposed".
- New L2 groups from Brief Part F are shown as "7.6 (proposed)", "12.5 (proposed)" and "12.6 (proposed)" until BPM-PRA-001 is changed.
- Where a number in a policy is new (not in the brief and not in an issued standard), it is listed below under **Proposed numbers** for your decision.

## Results

- All 12 policy files (LDR-POL-001 Rev 02, the ten new policies and DOC-POL-001 Rev 02) **PASS** the checker. The only warnings are the blank issue and effective dates, which are expected in a draft. Checked on `drafts` alone and on `finals manuals drafts` together.
- The **FIN** code is added to `protocol/build/build_protocol.py`, `protocol/one-protocol.json` (regenerated) and Appendix B.1 of the Document Standard. I added it in the build script and did not change the Session 1 Manual source, so the system table in the OMS Manual itself does not yet show FIN. It needs adding at the Manual's next revision.

## 0. ACE-LDR-POL-001 OMS Policy — draft of Rev 02 (Revision A)

Every sentence of Rev 01 is kept and moved into the B1 sections. Rebuilt on the v5 layout, which adds the document map and the full control table (Level, Parent, Title OMS tags, Role register). The approved wording changed in only these places:

- §2.3: "We shall identify hazards…" became "ACE shall identify hazards…".
- §2.4: the stop-work paragraph was a RiskControl without a Control ID. It is now an ordinary Requirement, split into its two sentences; the control itself lives in ACE-COW-STD-001.
- §6.4: the Manual reference changed from Revision 03 to Revision 04 (the current issue).
- §6.4: the closing note no longer names 1 January 2026 as the effective date; it says the policy takes effect on its effective date and records that Rev 01 took effect on 1 January 2026.
- Reviewer title corrected to "VP Legal & Government Affairs (General Counsel)" for Sharda Bissoon (the checker's only error on Rev 01).

Where the Rev 01 text went: the policy statement is in §1 and §1.7; Rev 01 §1–§2 became the commitments in §2; the employee duties in Rev 01 §3.1 went to the stop work, control of work and report-and-learn commitments; the manager, Area Authority and Technical Authority duties in Rev 01 §3.2 went to §3 Accountabilities; the deviation approval rule went to §4; Rev 01 §4 became §5; the controlled references became §6.4.

New content:
- §1: mission, vision and the five values (Safety above all; Integrity in everything; Care for people and places; One team, one way; Learn and improve). The values sit in section 1 so the commitments stay in section 2, as in every other policy.
- §2: new commitments for stop work, operate within limits and independent technical authority. Asset integrity is expanded with "never deferred silently". Report and learn points to ACE-OMS-POL-001 for how improvement is managed.
- §3: an accountabilities table with the policy owner, the custodian, the relevant VPs and the owners of the governed processes, taken from BPM-REG-001.
- §4: the decision rights the policy fixes (restart after stop work, TA endorsement, operating with an impaired SCE). It sets no numeric thresholds of its own.
- §5: three headline KPIs with targets, linked to objectives OBJ-26-02, OBJ-26-03 and OBJ-26-06. §5.2 keeps the Rev 01 assurance sentences and points to ACE-OMS-POL-001 for the cycles (as the brief asks).
- §6: tables for the 22 governed processes (Part E), the implementing Standards and Practices (including planned ACE-LDR-STD-003 Stop Work Authority Standard and ACE-LEG-STD-001), and the ten new policies under this one.
- Title OMS tags changed from 1.1, 2.1, 2.3 to the brief's 1.1, 2.1, 1.2. Reviewers increased from two to five (added the VP Operations, the VP Engineering & Projects and the Head of Internal Audit & Risk Assurance).

**For your decision:**
- Six of the eight process owners named in §3 are Leads or a Superintendent, below the manager level that BPM-PRA-001 §5 requires (Brief Part G item 1). I have named them exactly as the register shows.
- Because "keep every sentence" applied, §5.2 still holds a short version of the assurance commitments as well as pointing to OMS-POL-001. They are consistent with each other.

## 1. ACE-OMS-POL-001 Governance, Assurance and Continuous Improvement Policy

The CI policy. Owner the CEO, custodian Gary Ho Sing (BPM system owner), author Kwame Henry. It has 11 commitments. The ten from the brief are all there: process approach, objectives, three lines of assurance, CI as a duty, the five sources, the four-step method ladder, benefit shown, standardise through control, recognition and maturity. I added an eleventh, the annual leadership review (tag 10.5).

- The five **sources** and four **methods** are written as lists whose items are the exact values for the CI register's `source` and `method` fields.
- The CI stages **Verified** and **Standardised** are defined in commitments 2.7 and 2.8.
- §4 sets who approves each route:
  - Just do it: the line manager.
  - PDCA: the process owner.
  - DMAIC: the process owner, with the function VP approving the resources.
  - Project: by MOC class and the financial limit.
- §4 also sets the reject-or-park rule: only the process owner may reject or park an item, the reason is recorded, and the originator is told within 30 days.
- §5 lists all six cycles in one table.
- **Proposed numbers:**
  - idea-to-decision within 30 days for 90% of items;
  - maturity Level 3 for all Current processes by the end of 2028 (from the brief).
- **For your decision:**
  - ACE-BPM-PRS-003 Improvement Management Process is a new number. It is not yet in BPM-REG-001 or DOC-REG-001.
  - The only linked objective that exists today is OBJ-26-08. The policy says a CI or maturity objective is added from 2027.

## 2. ACE-RSK-POL-001 Operational Risk Management Policy

Owner George Habib, custodian Christina Bain, author Damian Daniel. It has the seven commitments from the brief; the emergency policy is folded in as 2.7. §4 holds five threshold sets, each taken from an issued standard.

**Differences from the brief (as you instructed):**

| Item | Brief example | Policy (from the issued standard) |
|---|---|---|
| Risk acceptance | Low: Area Authority; Medium: VP; High: CEO; Very High: not acceptable | Low: Supervisor or L4 Lead; Medium: Function Manager or Area Authority; High: VP; Very High: not acceptable for routine activity, CEO only for an exceptional recovery plan (ACE-RSK-STD-001 §5.1) |
| Deviation period | 90 days; 30 days for SCEs | 180, 90 or 30 days by residual band (Low, Medium, High); no routine period for Very High; one extension only (ACE-OMS-STD-002 §5) |
| MOC class rule | "Major if it affects an SCE, an operating limit or a lane role" | C3 if a major accident hazard effect, a new or altered SCE, a major tie-in, or a changed shutdown or relief philosophy; C2 if plant configuration, operating limits, procedures, interfaces, competence or roles; otherwise C1 (ACE-MOC-PRC-001 §2.2). So "affects an SCE" maps to C3, and "operating limit or role" maps to C2. |
| Asset risk review | Six-monthly | Six-monthly for the register as a whole, plus quarterly for High risks, as ACE-RSK-STD-001 already requires |
| Emergency levels | "Trigger for each level" | Level 1 Site, Level 2 IMT supported, Level 3 Crisis, using the triggers in ACE-EMR-STD-001 §3.2 and its Appendix A |

- **Proposed numbers:**
  - the risk appetite table by consequence domain (there was no appetite statement anywhere before);
  - a bow-tie review at least every three years.

  The HAZOP five-year interval, the 90-day plan updates and the annual exercises are taken from the issued standards.
- **For your decision:** ACE-MNT-PRS-002 SCE Deviation Process is still owned in the register by Marc Gomes, who has left. Section 3 names the VP Operations as interim owner, as BPM-PRA-001 §5 provides. The merge of this process into "Deviation and exemption" is noted in the governed-processes table but not decided (Brief Part G item 3).

## 3. ACE-CON-POL-001 Supply Chain, Logistics and Local Content Policy

Owner Sasha George, custodian Rhea Sookram, author Lisa Williams. It has the seven commitments from the brief. The people-flow and material-flow commitments carry the pre-boarding checks and the POB record as binding statements, because they are the checks in the trip-planning process.

- The priority order for an oversubscribed flight or boat is a four-row table in §4.2:
  1. Emergency
  2. Safety-critical work
  3. Production-critical
  4. Routine
- Manifest cut-off: 24 hours, with late additions approved by the OIM. This is from the brief.
- **Difference from the brief:** contract performance review frequencies follow ACE-CON-STD-001 §2: High and Very High at least monthly, Medium at least quarterly, Low at completion. The brief's example was High quarterly and Medium six-monthly, which would have been looser than the issued standard.
- **Proposed numbers:**
  - local content: at least 60% of spend, at least 90% of the workforce, and at least 10% of the tender evaluation score;
  - seat and deck-space utilisation at least 85%;
  - fewer than 5% bumped for reasons other than weather;
  - supplier re-qualification every three years (from the brief).

## 4. ACE-PPL-POL-001 People and Competence Policy

Owner Adrian Achong, custodian Andrea Farfan, author Damian St. Hill. It has the five commitments from the brief, plus one on fair recruitment so the conduct check in recruitment has a home.

- §4.1 sets who appoints each role authority: Area Authority, Technical Authority, Performing and Isolating Authority, and Process Owner.
- **Proposed numbers:**
  - no safety-critical re-verification interval longer than three years (the policy states the principle, and each profile sets its own interval);
  - new starters authorised within six months;
  - training plan completion at least 90%.
- **For your decision:** HR has no manager-level owner for recruitment or performance management apart from the Learning & Competence Manager. The VP Human Resources is named as interim owner of those two processes.

## 5. ACE-HMA-POL-001 Hydrocarbon Measurement, Product Quality and Commercial Policy

Owner Karen Jack, custodian Anjali Boodoo, author Navin Sookdeo. It has the five commitments from the brief; customer and product quality are folded in.

- Mismeasurement threshold, from the brief:
  - an error of more than ±0.5% of daily volume, or any custody meter failure, is notified to the Gas Buyer and partners within 24 hours;
  - a smaller error is corrected in the monthly close.
- **Proposed numbers:**
  - shortfall notice: more than 5% of the nominated daily quantity notified 24 hours ahead; unplanned shortfalls within two hours;
  - meter intervals: GC checked daily, secondary instruments verified monthly, crude meters proved at each lifting and at least monthly, allocation meters quarterly, full calibration annually;
  - monthly close by the tenth working day;
  - annual independent allocation audit.

  The meter intervals should be confirmed by the Metering & Measurement Lead when the HMA Practice is written.

## 6. ACE-FIN-POL-001 Financial Control and Delegation of Authority Policy

Owner Teresa Daniel, custodian Krishna Jagessar, author Sherma Isaac. It needed the FIN code, which has been added.

- The Delegation of Authority schedule is a table in §4.1, using the brief's USD bands: Manager 25k, VP 250k, CEO 2M, Board above. A binding segregation-of-duties statement backs the mechanical lane check in ONE.
- **Proposed numbers:**
  - extra rows in the schedule for contract variations (cumulative), budget transfers (not delegated to managers) and write-offs (VP 25k, CEO 250k, Board above);
  - unbudgeted spend needs one level higher, and the CEO above 250k;
  - monthly close by the seventh working day;
  - budget variance within ±5%;
  - fewer than two billing disputes a year.
- **For your decision:** partner billing is quarterly, as in the brief; many joint operating agreements bill monthly, so the policy adds "or more often where an agreement requires". No Finance standards exist in the register yet. The policy lists the two related planned standards and says Finance standards are still to be registered.

## 7. ACE-LDR-POL-002 Code of Conduct and Business Ethics Policy

Owner Sharda Bissoon, custodian Kerry-Ann Mitchell (Corporate Secretary), author Winston Daniel. It has the four commitments from the brief, plus Respect at work. It is the parent of the planned ACE-LDR-STD-001 Code of Conduct.

- The no-bribery, conflict-of-interest and no-retaliation rules are binding statements. The conflict declaration is the check step in tendering, recruitment and award.
- Speak-up concerns can feed the CI register as staff ideas, with the originator's consent.
- **Proposed numbers:**
  - gifts: up to TT$500 recorded; up to TT$2,500 with VP approval; above that, cash, or anything from an open tenderer, not permitted;
  - concerns: acknowledged in 5 working days, assessed in 30 days, closed in 90 days;
  - annual certification at least 98%.
- The governed process "Speak-up and concern handling" is placed under 12.6 (proposed).

## 8. ACE-ENV-POL-001 Environment Policy

Owner George Habib, custodian Kevin Lutchman, author Nadine Cooper. It has the five commitments from the brief.

- **Proposed numbers:**
  - no routine flaring by the end of 2030, with routine flaring cut by at least 15% a year against 2025 (consistent with OBJ-26-07);
  - spill tiers: Tier 1 up to 10 bbl contained on site; Tier 2 above 10 bbl and up to 100 bbl, or any spill reaching the sea, a watercourse or land outside a site; Tier 3 above 100 bbl, beyond ACE capability, or reaching a sensitive coast or fishing ground;
  - Tier 2 and 3 spills reported to the environmental regulator within 24 hours;
  - total spills under 10 bbl a year.

  ACE-EMR-STD-001 §5 defines the three capability tiers but no volumes, so the policy adds the volumes and maps each tier to them.
- The governed process is placed under 7.6 (proposed).

## 9. ACE-SEC-POL-001 Security Policy

Owner George Habib, as you decided; custodian Jenelle Paul; author Dillon Granger. Section 3 names Kevin Mohammed (Telecoms & OT Cyber Security Lead) as accountable for OT cyber security and Marvin Williams (VP IT, Data & Knowledge) as accountable for IT systems.

- The title is "Security Policy"; scope covers physical, IT and OT security.
- Port security at the Point Lisas Shore Base is described generically, with no named external code.
- **Proposed numbers:**
  - leavers' access removed within one working day;
  - no standing remote access to OT, with each session approved, time-limited and logged;
  - an annual security or cyber exercise.

  Quarterly access reviews and the annual risk assessment are from the brief.

## 10. ACE-STK-POL-001 Stakeholder, Community and Grievance Policy

Owner Rodney Garcia, custodian Ricardo Gittens, author Reshma Seecharan. It has the three commitments from the brief, plus emergency preparedness with communities (4.4) and honest communication.

- Grievance times are from the brief: acknowledge in 5 working days, answer in 30 days.
- **Proposed numbers:**
  - escalation to the VP within a further 30 days;
  - same-day referral to Legal for injury, property damage or legal claims;
  - 30 days' notice to fishing communities for planned marine activity, and 72 hours for short notice;
  - quarterly community meetings.
- The governed process is placed under 12.5 (proposed).

## 11. ACE-DOC-POL-001 Document and Records Management Policy — draft of Rev 02 (Revision B)

A minor correction, as the brief asks. Revision B, because A was used before Rev 01.

- **Added:** §3.9 Periodic review, a commitment stating the review intervals from ACE-DOC-STD-001 §7: three years for Levels 1 to 3, emergency plans every year, and five years for work instructions, forms and registers. Also added: §7.1 and §7.2, the governed-processes and implementing-documents tables.
- **Why section 7, not 6:** this policy's section 6 is "Performance, reporting and assurance", and its section 7 is already "Implementation and supporting controlled documents". Putting the tables in section 7 avoids renumbering an approved document.
- **How it was made:** rebuilt with the generator from the Session 2 source of the issued Rev 01, not by hand-editing the Word file. I compared the result paragraph by paragraph with the issued Rev 01: the body is identical apart from the three additions. The issued file in `finals/` is untouched.
- **For your decision:** the eight Rev 01 commitments (3.1 to 3.8) do not name ACE values, because that wording is approved. They could be given value sentences in Rev 02 if you want DOC-POL-001 to match the others fully.

## Open items for the Process session (not done here, as instructed)

- Brief Part F: re-parenting the Wave 1 documents; the BPM-REG-001 `policy` column; the new L2 groups 7.6, 12.5 and 12.6 in BPM-PRA-001; the portal.
- Register entries for ACE-BPM-PRS-003 and for the new candidate processes.
- Adding the eleven policies (the ten new ones and LDR-POL-001 Rev 02) to DOC-REG-001 when they move to `finals/`.
