# processes/

Process model files, one per mapped L3 process (`ACE-SSS-PRS-NNN.json`, schema **ONE-PRS/2** in `protocol/schemas/one-prs-2.schema.json`; ONE-PRS/1 files are still read). See ACE-BPM-PRA-002.

| File | Process | Character |
|---|---|---|
| `ACE-MOC-PRS-001.json` | Management of Change | Information-heavy: records, reviews and decisions between Operations and Engineering |
| `ACE-AIM-PRS-001.json` | Inspection Planning and Execution | Cyclical and physical: crews and equipment move offshore by helicopter and boat |

Since v2 each model also holds **stages** (the map opens at this level), an **artefact catalogue** with create / read / update per step, **step targets**, and **icon keys** from the ONE icon registry (`standards/icons/one-icons.json`). The data each process needs is set out in `standards/process-data/ONE_Process_Data_Requirement.md`.

Each model is measured from its ledger in `registers/`:

- `BPM-LOG-<process>_cases.csv` — one row per case (a change, an inspection)
- `BPM-LOG-<process>_events.csv` — one row per step a case passed through: `arrived` (work reached the step), `started` (someone began), `finished`, branch taken, rework flag, `wait_reason`, `rework_reason`, trip
- `BPM-CAP-001.csv` — hours each lane (role) has for the process, by period; `BPM-SCN-001.csv` — dated changes behind the history
- `maps/<process>.map.json` — which source system would feed each field in a real company

Improvement items are in `registers/CI-REG-001.csv` (stages in `CI-REG-001_history.csv`); value assumptions in `registers/BPM-VAL-001.csv`.

`tools/build_ledgers.py` rebuilds the two ledgers and the CI register, then runs `tools/enrich_ledgers.py` (reasons, capacity, scenarios, mapping files) (the MOC ledger from the MOC register; the inspection ledger simulated from the asset register, including the PL-101 story). Run it only when those inputs change.
