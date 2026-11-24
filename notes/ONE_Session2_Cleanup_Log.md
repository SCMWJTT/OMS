# ONE / ACE — Session 2 repository clean-up log (24 November 2026)

## What changed

| Item | Action |
|---|---|
| `finals/~$E-MOC-PRC-001…docx` | Deleted (Word lock file) |
| ENG-STD-901, ENG-SPC-410 Draft A (drafts/) | Deleted. The Rev 01 finals are more compliant (binding styles, "shall" rule, revision history). Draft A used invalid code C-SIS |
| DOC-POL-001, DOC-PRC-001 Rev A | Reissued as Rev 01, effective 1 Apr 2026 (with Manual Rev 04). DOC-PRC approval matrix updated to 5 levels |
| AIM, MNT, OPS, WEL-PRA-001 Rev A | Reissued as Rev 01, effective 1 Jun 2026 |
| COW-PRC-001, COW-PRC-002 Draft A | Reissued as Rev 01, effective 1 Jun 2026, Level 4 |
| BPM-PRA-001, 002, 003; RSK-PRA-001 | Written new. Rev 01, effective 1 Apr 2026 |
| Original writer files | Moved to `samples/lite/` as Fix test input |
| New folders | `processes/`, `registers/`, `superseded/` |

## Defects found in the writer files (fixed in Rev 01)

- OPS-PRA and WEL-PRA: 39 identical placeholder control paragraphs each (C-OPS/WEL-001 to 039). Replaced by 12 real controls each.
- COW-PRC-001/002: tables corrupted (header split one letter per column); Control IDs malformed (`C-C-COW-PTW-001`). Tables repaired; IDs C-COW-001 to 019.
- AIM-PRA and MNT-PRA: no binding statements at all; controls only in the appendix. Binding statements and RiskControl paragraphs added.
- All: properties empty or partly filled; no bookmarks; tags as plain text; no named owners; "shall" in Normal paragraphs; parents marked "(planned)".

## All 12 reissued documents now have

23 properties filled; control table with all values as ODS.Meta controls (including Parent, ProcessOwner, Level, RoleRegister); bookmark and OMS Tags control on every heading; "shall" only in binding styles; Control ID content control in every RiskControl paragraph; controls appendix matching the body; Word built-in properties per DOC-STD-002 Rev 02 §5.3; people exactly as in ACE_People.csv; no stray media or thumbnail. 101 Control IDs, all unique.

## Still to handle by the protocol Fix (not edited by hand)

The 20 Rev 01 finals from Wave 1: no ODS.Parent; Framework "Rev 03"; control-table text such as "Standard (Level 2)" and "01 (approved issue)"; Word Subject field holds "ID | ONE management system"; ENG-SPC-410 Level = "Technical"; ENG-901/410 have only 5 Meta controls; no Control IDs (the earlier "1–4 IDs" count was false matches inside document numbers).

## Tools

`notes/ONE_Session2_Pack/tools/` — `gen.py` (STRICT builder from a spec, shell = OPS-STD-001), `extract.py` (LITE → spec, text kept), `verify.py` (independent check), `run.py`. Specs in `notes/ONE_Session2_Pack/specs/`.

## Protocol Pack (24 November 2026, afternoon)

- `protocol/` added: one-protocol.json, ONE_Protocol_v1.md, the shared checker (engine/one-audit.js), process schema ONE-PRS/1 with the MOC example, nine register templates, golden sample ACE-DOC-PRA-999.
- Template v5 added to `templates/`; v4 and the preview moved to `superseded/`.
- Manual Rev 04: one paragraph restyled from ODS.RiskControl to ODS.Requirement (a requirement about controls, not a control). Text unchanged.
- Test result: all 33 controlled documents PASS (29) or PASS AFTER FIX (4); golden sample PASS; the 6 writer originals in samples/lite FAIL only on genuine defects.
