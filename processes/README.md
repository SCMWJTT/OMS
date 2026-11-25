# processes/

Process model files, one per mapped L3 process (`ACE-SSS-PRS-NNN.json`, schema **ONE-PRS/2** in `protocol/schemas/one-prs-2.schema.json`; ONE-PRS/1 files are still read). See ACE-BPM-PRA-002.

| File | Process | Character |
|---|---|---|
| `ACE-MOC-PRS-001.json` | Management of Change | Information-heavy: records, reviews and decisions between Operations and Engineering |
| `ACE-AIM-PRS-001.json` | Inspection Planning and Execution | Cyclical and physical: crews and equipment move offshore by helicopter and boat |

Each model is measured from its ledger in `registers/`:

- `BPM-LOG-<process>_cases.csv` — one row per case (a change, an inspection)
- `BPM-LOG-<process>_events.csv` — one row per step a case passed through: `arrived` (work reached the step), `started` (someone began), `finished`, branch taken, rework flag, trip

Improvement items are in `registers/CI-REG-001.csv` (stages in `CI-REG-001_history.csv`); value assumptions in `registers/BPM-VAL-001.csv`.

`tools/build_ledgers.py` rebuilds the two ledgers and the CI register (the MOC ledger from the MOC register; the inspection ledger simulated from the asset register, including the PL-101 story). Run it only when those inputs change.
