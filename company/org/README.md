# ACE organisation files

The portal's Company pages are read from these files and from `company/ACE_People.csv`. Edit them in Excel or any text editor, save as CSV, and the site updates on the next build.

| File | What it holds | Edit it when |
|---|---|---|
| `../ACE_People.csv` | Every person: name, job title, Role ID, function, site, manager, Status (Active or Left) and Left Date | someone joins, moves or leaves |
| `roles.csv` | The role catalogue: one row per job role, with function, grade, reporting line, dotted line, sites and purpose | a role is created, renamed or moves |
| `oms_roles.csv` | OMS duties (Area Authority, Technical Authority…) and the job roles that carry them | a duty is assigned to a different role |
| `sites.csv` | Sites, their Area Authority and their position on the business map | a site opens or changes hands |
| `functions.csv` | The functions, their head role, purpose and main OMS elements | the organisation changes |
| `function_links.csv` | How strongly functions work together, and what flows between them | working relationships change |
| `staff_changes.csv` | A log of joiners, movers and leavers | someone joins, moves or leaves |

**When someone leaves:** set their Status to `Left` and fill in Left Date; add the new person with the same Job Title and Role ID; log both in `staff_changes.csv`. Documents that still name the person who left are listed under Gaps.

**Why roles, not people:** documents name roles ("the Inspection Lead"). The staff list says who holds each role today, so documents stay correct when people change.

`notes/ONE_Session2_Pack/tools/build_org.py` created these files from the staff list once; from now on they are the master.
