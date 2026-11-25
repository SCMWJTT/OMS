# ONE Session 3: Process and Improvement dimensions — what was built

Read with `ONE_Session3_Process_Handover.md` (the design) and `ONE_Session3_Policy_Brief.md` (the policy set).

## Decisions taken with Wilmark

- The 12 Session 4 policies are shown as **approved** (demo): new policies Rev 01, LDR-POL-001 and DOC-POL-001 Rev 02, issued 16 Nov 2026, effective 23 Nov 2026. Rebuilt with `notes/ONE_Session4_Pack/tools/issue.py`; the old Rev 01 files of LDR and DOC moved to `superseded/`.
- Value figures use public sources where they exist (`registers/BPM-VAL-001.csv`, each row sourced or marked "Assumption").
- Two contrasting worked processes: **Management of Change** (information-heavy) and **Inspection Planning and Execution** (cyclical, people and material movement offshore).

## The three layers of a process

| Layer | File | Notes |
|---|---|---|
| Design | `processes/ACE-MOC-PRS-001.json`, `processes/ACE-AIM-PRS-001.json` | Schema ONE-PRS/2 (`protocol/schemas/one-prs-2.schema.json`): lanes carry `role_id` and `function`; `flows` typed information / material / people; `cycle`; `commitments` (policy#bookmark); step `value` VA/BVA/NVA, `commitment`, `threshold`; `history` with the CI item behind each revision |
| Run | `registers/BPM-LOG-<process>_cases.csv` and `_events.csv` | Events have arrived / started / finished, so waiting and working are separate. MOC ledger converted from MOC-REG-001 (366 changes, rework returns added at approval); inspection ledger simulated 2024 to Nov 2026 from AIM-REG-002 (424 inspections) |
| Improve | `registers/CI-REG-001.csv` and `_history.csv` | 12 items; sources and routes use the exact lists in ACE-OMS-POL-001 §2.5 and §2.6; baselines and results are measured from the ledgers by `processes/tools/build_ledgers.py` |

## The stories in the data

- **Inspection:** campaign bundling (Rev 02, June 2025, CI-2024-001) cut offshore trips from 93 (2024) to 32 (2026) and logistics from about $1.4M to $0.5M a year, and lifted offshore on-time inspections from 61% to 88%. But deferrals rose (17% → 22%), C-AIM-004 degraded, and the PL-101 deferral extension preceded the near miss EV-2026-161 → MOC-2026-061 and DMAIC item CI-2026-007. The PL-101 inspection case carries those references.
- **MOC:** implementation moved to the Maintenance Planner and the weekly schedule (Rev 02, April 2025, CI-2024-004): median implementation 27 → 20 days; approvals without return 84% → 96% (CI-2025-005). Cycle time is still above 30 days because Technical Authority review waits 18 days (CI-2026-006, open).

## Portal (portal/src/process.js and process.css, joined to app.js by the build)

- `#/process` — figures, the two mapped process cards, the L1/L2 architecture read from ACE-BPM-PRA-001 §4 (filled tiles mapped, outlined planned), policies with the processes they govern, the register.
- `#/process/<id>[/<step>]` — golden thread (values → policy commitments → process → objectives → risks); the map with **Design** (stage animation, no clock; typed flows animated), **Actual** (heat by median wait, path thickness by volume, open cases, real-case replay with waiting vs working), **Before / after** (Rev 01 vs Rev 02 by step); lanes by role or by function; overlays; year and site filters. Step detail panel (who, documents, commitment and values, threshold, controls and risks, ledger figures, CI items). Panels: performance (KPI families with yearly bars, breach flag that points to the CI policy), business value (people cost, logistics, cost of waiting, value delivered or loss avoided), where the time goes, function hand-off matrix and effort by function, improvement and revisions, trace a case (Gantt), SIPOC.
- `#/ci`, `#/ci/<id>` — improvement board by stage, sources and routes, benefit tracker, raised and closed by year, heat of steps that attract improvement; item page with history.
- `#/value` — the assumptions with sources.
- Link-backs: control pages name the process step; risk pages name the process; function pages list the mapped steps they perform with hours and hand-offs; role pages link to their lanes and steps; document pages list the steps that rely on them and mark the sections they use.

## Next

- Map a third process (Offshore Trip Planning or Document Publication) — copy the JSON pattern, add a ledger.
- BPMN 2.0 XML export from ONE-PRS/2.
- Re-parent the Wave 1 Standards to the new policies (Policy Brief Part F).
- The 2026 PRS Word descriptions for the two processes (PRS pair rule, C-BPM-020).
