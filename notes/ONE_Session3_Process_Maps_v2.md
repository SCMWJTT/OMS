# ONE Session 3: process maps v2, icon standard and process data requirement

## Decided with Wilmark
- New `standards/` folder for ONE's own standards; `templates/` moved into it (`standards/templates/`). Room for `diagrams/`, `charts/`, `colour/`.
- **ONE Icon Standard v1.0** (`standards/icons/`): shape = family, glyph = what, badge = variant, colour = one dimension per view; documents get a family of blues; red/amber/green only for status. Registry `one-icons.json` (168 keys, 14 families, 19 flagged for custom drawing) built by `build_icons.py`. Base set Font Awesome Free 6.5.1 solid, loaded from cdnjs in the portal.
- **ONE Process Data Requirement v1.0** (`standards/process-data/`): not a corporate data standard but the OMS requirement for process data, from existing stores; process owner accountable, OMS data champion responsible; one schema for all processes; data confidence mark; proposed maturity rule.

## Process page v2
- Opens on a **stage strip** (lead time, target, queue, waiting/working bar, bottleneck flag), then the **selected stage only** as a swimlane, with **seven views**: who does what, functions, information (C/R/U artefacts), time and cost (vs step targets), bottlenecks (queue, reasons, capacity use), improvement, risk and controls.
- Headline tiles: lead time, share of time worked, right first time / on time, cost per case, **data confidence**.
- Step card changes with the view; the full step record is one click away. KPI, value, functions, improvement, trace-a-case and SIPOC panels kept below.
- Data added: stages, artefacts, targets and icon keys in both models; wait and rework reasons in the ledgers; `BPM-CAP-001` capacity (TA post vacant from March 2025; logistics campaign change June 2025); `BPM-SCN-001` dated changes; `processes/maps/*.map.json`.

## Next
- Improvement board redesign (visual cards, A3 page) — not started.
- Custom energy icons from the brief in the icon standard §8.
- Use the scenario file to drive the simulation parameters (today it records the changes; capacity is read from BPM-CAP-001).
