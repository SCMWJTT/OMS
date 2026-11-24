# ONE Protocol Pack (v1.0)

The single rule set for turning ACE Word documents into ONE. Read **ONE_Protocol_v1.md** first.

| Item | File |
|---|---|
| Rule set (machine) | `one-protocol.json` |
| Rule set (people) | `ONE_Protocol_v1.md` (generated from the JSON) |
| Checker used by every ONE tool | `engine/one-audit.js` |
| Repository check | `engine/cli.js` → `reports/audit.md` |
| Process file schema + MOC example | `schemas/` |
| Register templates | `registers/` |
| Golden sample (passes every rule) | `samples/` |
| Template v5 | `../templates/ONE_ACE_Master_Template_v5.dotx` |
| Regenerate JSON and page | `build/build_protocol.py`, `build/build_protocol_md.py` |

Latest check of the repository: `reports/audit.md`.
