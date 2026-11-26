# ONE Process Data Requirement

**Version 1.0 · 26 November 2026 · Owner: Cynmark Systems Limited (ONE)**

What ONE needs to know about a process in order to draw it, measure it and show the effect of improvement. This is not a corporate data standard: a company keeps its own systems. It is the **OMS requirement for process data**: the records the company must make available, from the stores it already has, for a process to be managed through ONE. One schema serves every process, so efficiency and improvement can be compared across processes.

## 1 Who does what

| Role | Responsibility |
|---|---|
| Process owner | Accountable that the process has a current model and data that meets this requirement |
| **OMS data champion** | Keeps the feeds running, fixes gaps, maintains the mapping files and the reason codes, reports data confidence |
| System owners (CMMS, permit, MOC, ERP, document system) | Provide the extracts or connections the mapping file names |
| Auditor (OMS element 10) | Tests the data as well as the documents (section 6) |

## 2 The records

| Record | File | Fields | Typical source in an energy company |
|---|---|---|---|
| **Case** — one instance of the process (a change, an inspection, a permit) | `registers/BPM-LOG-<process>_cases.csv` | `case_id, process_id, revision, site, class or type, title, ref, opened, closed, outcome, due` (+ process-specific columns) | MOC tool, CMMS work order header, permit system |
| **Step event** — one pass of a case through one step | `registers/BPM-LOG-<process>_events.csv` | `case_id, step_id, lane, arrived, started, finished, branch, rework, wait_reason, rework_reason, trip` | Status history or audit trail of the same systems |
| **Capacity** — how much of each role is available to the process | `registers/BPM-CAP-001.csv` | `process_id, lane, role_id, people, hours_per_week, from, to, note` | Rosters, HR, or a monthly entry by the process owner |
| **Scenario / change log** — dated changes that affect the process | `registers/BPM-SCN-001.csv` | `date, process_id, kind, description, step_id, ref` | Process revisions, MOCs, organisation changes, CI items |
| **Cost items** — non-labour cost per case | trips in the events file; others as columns on the case | e.g. helicopter seats, boat days, contractor hours, parts | ERP, logistics booking, manifests |
| **Value assumptions** | `registers/BPM-VAL-001.csv` | `key, name, value, unit, basis, source` | Finance and planning figures |

Inside the process model (`processes/<process>.json`, schema ONE-PRS/2) the owner also keeps:

- **Stages** — 3 to 6 stages that group the steps (the map opens at this level).
- **Artefact catalogue** — the documents, records, data and systems the process touches, each with an icon key, and per step whether it is Created, Read or Updated.
- **Step targets** — the target time for each step (`target_days`).

## 3 Times: why three

`arrived` (work reached the step), `started` (someone began work on it) and `finished`. Waiting = started − arrived; working = finished − started. Without `started`, waiting and working cannot be separated and the bottleneck cannot be explained.

## 4 Reason codes

Waiting longer than one working day, and every rework, carries a reason from a short fixed list (icons `reason.*` in the ONE Icon Standard):

| Code | Meaning |
|---|---|
| `resource` | The person or team is busy with other work |
| `information` | Waiting for information or input from someone else |
| `approval` | Waiting for an approval or signature |
| `transport` | Waiting for a seat, a boat or a vehicle |
| `weather` | Weather or sea state outside limits |
| `batch` | Held to be done with others (weekly meeting, platform campaign) |
| `parts` | Waiting for parts or materials |
| `window` | Waiting for a maintenance or operating window |
| `permit` | Waiting for a permit or isolation |
| `incomplete` | Input incomplete or wrong (used for rework) |

Most companies do not record reasons today. Adding one drop-down to the existing form is usually the single most valuable change.

## 5 Mapping each process to its sources

Each process has a small mapping file, `processes/maps/<process>.map.json`, saying which system and which field feed each column above, how often, and who owns the extract. The demo company (ACE) has no live systems: its data is curated by `processes/tools/build_ledgers.py` from the ACE registers and the scenario file, in exactly this shape.

## 6 Data confidence and audit

ONE shows a **data confidence** mark on every process page:

| Mark | Rule |
|---|---|
| High | ≥ 95% of events have all three times; ≥ 90% of long waits have a reason; newest event no older than 7 days |
| Medium | ≥ 80% complete; ≥ 50% of long waits have a reason; newest event no older than 31 days |
| Low | Anything less |

Audit rule (proposed for ACE-BPM-PRA-003): a process cannot be rated above maturity level 2 without twelve months of data at Medium or better, nor above level 3 without High.

## 7 Extending

New fields are added at the end of a file and are optional for older data, so existing processes keep working. New reason codes need an icon key in the registry first.
