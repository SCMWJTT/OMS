# ONE Icon Standard

**Version 1.0 · 26 November 2026 · Owner: Cynmark Systems Limited (ONE)**

How ONE uses icons on its diagrams, maps and charts. The aim is that a viewer can read a busy diagram from its shapes and colours alone, and get names and numbers only when they ask for them (hover or click).

## 1 Where things live

| File | What it is |
|---|---|
| `standards/icons/ONE_Icon_Standard.md` | This standard |
| `standards/icons/one-icons.json` | **The icon registry.** The only place a concept is mapped to a glyph, colour, shape and badge |
| `standards/icons/build_icons.py` | Rebuilds the registry and the catalogue in section 10 of this standard |
| `standards/icons/custom/` | Custom drawn icons (SVG) as they arrive; see section 8 |

Pages never name a glyph. They ask the registry for a key (for example `doc.PRC` or `reason.transport`) and draw what it returns. Changing an icon, a colour or a badge is an edit to the registry, never to page code or content.

## 2 The grammar: four channels, one meaning each

| Channel | Carries | Example |
|---|---|---|
| **Shape** of the container | The family | Circle = who and what does the work; hexagon = management object; rounded square = artefact; square tile = OMS element; diamond = decision |
| **Glyph** inside | What it is | Shield = control; hourglass = waiting |
| **Badge** at the lower right | Which variant | `PR` on a document = procedure; a truck glyph on the organisation icon = Supply Chain |
| **Colour** of the fill | One dimension, chosen by the view | OMS element colour by default; function colour in organisation views |

Families and shapes:

| Shape | Families |
|---|---|
| Circle | Organisation, sites, external parties, resources, energy equipment, flow and decisions, wait reasons |
| Square tile | OMS framework (elements and expectations) |
| Hexagon | Management objects: opportunity, objective, process, requirement, hazard, risk, control, change, deviation, incident, action, finding, improvement, efficiency, compliance, rule, licence, idea, recognition, value |
| Rounded square | Artefacts: documents, records, data, systems |
| Diamond | Decisions |
| Small circle | Status marks, laid over another icon or a step |

## 3 Colour rules

1. **One meaning per colour on any one view.** A view chooses which dimension colour carries; the legend says which.
2. **OMS element colours** (fixed, `colours.elements`) are the default for management objects and OMS tiles. A management object takes the colour of its home element (risk and control → element 5).
3. **Function colours** (`colours.functions`) are used for organisation icons, lane bands and backgrounds in organisation views.
4. **Documents use a family of blues**, one per type, so a policy, a standard and a procedure can be told apart without reading: Policy navy, Manual petrol, Standard royal, Practice steel, Procedure sky, Work instruction periwinkle, Form blue-teal, Plan indigo, Specification slate blue. Records are one green; data is teal; systems are slate.
5. **Red, amber and green are reserved for status** (`colours.status`): queues, capacity, health, overdue, trend. They are never used to identify a thing.
6. Fills are dark enough to carry a white glyph. Check any new colour for contrast before adding it.
7. Backgrounds work too: tint lanes by function, tint a hot stage, shade the selected area. Thin lines alone do not separate zones well.

## 4 Size and levels of detail

| Level | Shown as | When |
|---|---|---|
| L0 | Coloured dot | Zoomed far out, dense charts |
| L1 | Icon, no label | Normal diagram view. **Minimum 24 px**, normally 28 to 32 px |
| L2 | Icon with badge | When the variant matters (document type, function). Badge about 45% of the icon |
| L3 | Hover card | Name, the one key number, status |
| L4 | Click | The full record or page |

Icons on diagrams carry **no text labels**. The name appears on hover; the legend lists only the icons present on screen.

## 5 Style

- **Solid**, single colour glyph in white on a solid coloured container. No outline styles.
- One base set for generic concepts: Font Awesome Free 6.5.1, solid (see `base_set` in the registry). Icons are CC BY 4.0; the attribution comments in the Font Awesome files must stay.
- Status marks sit at the upper right of the icon or step they qualify; badges sit at the lower right.

## 6 How pages use the registry

1. Ask for a key; draw its `shape`, `colour`, `glyph` and `badge` or `badge_glyph`.
2. If the key has an `svg` (custom drawn), use it instead of the glyph.
3. If a key is missing, fall back to the family's generic key (`doc.generic`, `site.generic`, …) and log it.
4. Process models and registers store **keys**, never glyph names (for example a stage stores `"icon": "mo.risk"`).

## 7 Naming keys

`family.name` in lower case with underscores (`rec.work_order`), except codes that are already codes in ACE: document types (`doc.PRC`) and function codes (`org.function.SCM`). Keys are never reused for a different meaning. Retired keys stay in the registry with `"retired": true`.

## 8 Custom icons

Energy work needs pictures the free sets do not have. Keys marked *custom wanted* in the catalogue show a generic stand-in until drawn. Brief for the artist:

- Solid, single colour, on a 24 × 24 grid, readable at 24 px; consistent stroke weight and corner style with the base set.
- Deliver SVG named by key (`eq.wellhead.svg`) into `standards/icons/custom/`, then set `"svg": "custom/eq.wellhead.svg"` in `build_icons.py` and rebuild.
- First batch (upstream): wellhead / Christmas tree, platform, FPSO, separator, compressor, pump, pipeline, pig launcher, relief valve, flare, metering skid, crane.
- Second batch (downstream): refinery, distillation column, storage tank, tank farm, jetty / tanker berth, loading rack.

## 9 Extending this standard

- New concept: add it to `build_icons.py` in the right family, run the script, and the catalogue below updates.
- New family: add it to `FAMILIES` with its shape and colour rule; it needs a shape already in section 2, or an update to this standard.
- Room for sister standards sits beside this folder in `standards/` (for example diagrams, charts, colour), each with its own folder.

## 10 Catalogue

Generated from `one-icons.json` by `build_icons.py`. Do not edit by hand.

<!-- CATALOGUE START -->

### Organisation (`org.*`) — circle

The company, its functions, roles, people and sites.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `org.company` | Company | `sitemap` | `#0B5563` |  |
| `org.function.EXEC` | Executive | `sitemap` | `#0B5563` | glyph `user-tie` |
| `org.function.OPS` | Operations | `sitemap` | `#2F6F8F` | glyph `industry` |
| `org.function.ENP` | Engineering & Projects | `sitemap` | `#7A5C9E` | glyph `gears` |
| `org.function.WEL` | Wells | `sitemap` | `#8E5B3A` | glyph `oil-well` |
| `org.function.EXD` | Exploration & Development | `sitemap` | `#2E8A78` | glyph `magnifying-glass-location` |
| `org.function.SCM` | Supply Chain | `sitemap` | `#B07A1F` | glyph `truck` |
| `org.function.HSE` | HSE & Compliance | `sitemap` | `#B5473A` | glyph `helmet-safety` |
| `org.function.HR` | Human Resources | `sitemap` | `#6E9A2E` | glyph `users` |
| `org.function.FIN` | Finance | `sitemap` | `#5B7F3A` | glyph `coins` |
| `org.function.ITD` | IT, Data & Knowledge | `sitemap` | `#3D4FA1` | glyph `laptop-code` |
| `org.function.BDM` | Business Development & Markets | `sitemap` | `#A0527A` | glyph `handshake` |
| `org.function.LGA` | Legal & Government Affairs | `sitemap` | `#57656C` | glyph `scale-balanced` |
| `org.function.CCS` | Communications & Corporate Services | `sitemap` | `#6B7B83` | glyph `bullhorn` |
| `org.function.CTR` | Contractors | `sitemap` | `#7D8D95` | glyph `user-gear` |
| `org.role` | Role | `user` | `#444441` |  |
| `org.person` | Person | `user` | `#444441` |  |
| `org.team` | Team | `users` | `#444441` |  |
| `org.contractor` | Contractor | `user-gear` | `#7D8D95` |  |

### Sites (`site.*`) — circle

Where the work happens.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `site.generic` | Site | `location-dot` | `#0B5563` |  |
| `site.platform` | Offshore platform *(custom wanted)* | `oil-well` | `#0B5563` |  |
| `site.plant` | Process plant | `industry` | `#0B5563` |  |
| `site.shorebase` | Shore base / port | `anchor` | `#0B5563` |  |
| `site.office` | Head office | `building` | `#0B5563` |  |
| `site.terminal` | Terminal | `warehouse` | `#0B5563` |  |
| `site.refinery` | Refinery *(custom wanted)* | `industry` | `#0B5563` |  |
| `site.landlease` | Land lease | `map` | `#0B5563` |  |

### External parties (`ext.*`) — circle

Organisations outside ACE that work passes to or from.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `ext.regulator` | Regulator | `landmark` | `#6B5B4E` |  |
| `ext.customer` | Customer / buyer | `handshake` | `#6B5B4E` |  |
| `ext.partner` | JV partner | `people-arrows` | `#6B5B4E` |  |
| `ext.contractor` | Contractor company | `helmet-safety` | `#6B5B4E` |  |
| `ext.community` | Community | `people-roof` | `#6B5B4E` |  |
| `ext.supplier` | Supplier | `truck-ramp-box` | `#6B5B4E` |  |

### OMS framework (`oms.*`) — tile

The ten OMS elements and their expectations.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `oms.element.1` | Commitment and accountability | `flag` | `#0B5563` | 1 |
| `oms.element.2` | Policies, standards and objectives | `landmark` | `#3D4FA1` | 2 |
| `oms.element.3` | Organisation, resources and capability | `people-group` | `#7A4FA0` | 3 |
| `oms.element.4` | Stakeholders and customers | `handshake` | `#B5427A` | 4 |
| `oms.element.5` | Risk assessment and control | `triangle-exclamation` | `#C8402F` | 5 |
| `oms.element.6` | Asset design and integrity | `oil-well` | `#E07A1F` | 6 |
| `oms.element.7` | Plans and procedures | `book` | `#D6A21E` | 7 |
| `oms.element.8` | Execution of activities | `play` | `#6E9A2E` | 8 |
| `oms.element.9` | Monitoring, reporting and learning | `graduation-cap` | `#2E9A78` | 9 |
| `oms.element.10` | Assurance, review and improvement | `magnifying-glass` | `#2F7FB8` | 10 |
| `oms.expectation` | OMS expectation | `list-check` | `#0B5563` |  |
| `oms.manual` | OMS manual | `book-bookmark` | `#0B5563` |  |

### Management objects (`mo.*`) — hex

Opportunities, objectives, processes, requirements, risks, controls, incidents, improvement, compliance and value.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `mo.opportunity` | Business opportunity | `seedling` | `#3D4FA1` |  |
| `mo.objective` | Objective / target | `bullseye` | `#3D4FA1` |  |
| `mo.process` | Process | `diagram-project` | `#D6A21E` |  |
| `mo.requirement` | Requirement | `list-check` | `#3D4FA1` |  |
| `mo.hazard` | Hazard | `fire-flame-curved` | `#C8402F` |  |
| `mo.risk` | Risk | `triangle-exclamation` | `#C8402F` |  |
| `mo.control` | Control / barrier | `shield-halved` | `#C8402F` |  |
| `mo.change` | Change (MOC) | `arrows-rotate` | `#C8402F` |  |
| `mo.deviation` | Deviation | `route` | `#C8402F` |  |
| `mo.incident` | Incident / event | `burst` | `#2E9A78` |  |
| `mo.action` | Action | `square-check` | `#2E9A78` |  |
| `mo.finding` | Audit finding | `circle-exclamation` | `#2F7FB8` |  |
| `mo.improvement` | Improvement | `arrow-trend-up` | `#2E9A78` |  |
| `mo.efficiency` | Efficiency | `gauge-high` | `#2F7FB8` |  |
| `mo.compliance` | Compliance | `scale-balanced` | `#3D4FA1` |  |
| `mo.regulation` | Rule / regulation | `gavel` | `#B5427A` |  |
| `mo.licence` | Licence / permit to operate | `certificate` | `#B5427A` |  |
| `mo.idea` | Idea | `lightbulb` | `#2E9A78` |  |
| `mo.recognition` | Recognition | `trophy` | `#7A4FA0` |  |
| `mo.value` | Value | `sack-dollar` | `#A87A12` |  |
| `mo.cost` | Cost | `money-bill-wave` | `#A87A12` |  |
| `mo.benefit` | Benefit | `hand-holding-dollar` | `#A87A12` |  |
| `mo.revenue` | Revenue | `file-invoice-dollar` | `#A87A12` |  |
| `mo.profit` | Profit | `chart-line` | `#A87A12` |  |
| `mo.budget` | Budget | `coins` | `#A87A12` |  |

### Documents (`doc.*`) — doc

Controlled documents. One base glyph; type shown by its blue and its letter badge.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `doc.POL` | Policy | `file-lines` | `#14275E` | P |
| `doc.MAN` | Manual | `file-lines` | `#0E4D6E` | M |
| `doc.STD` | Standard | `file-lines` | `#2648A6` | S |
| `doc.PRA` | Practice | `file-lines` | `#1D6FA3` | PA |
| `doc.PRC` | Procedure | `file-lines` | `#2E8BC9` | PR |
| `doc.WIN` | Work instruction | `file-lines` | `#5468C4` | WI |
| `doc.FRM` | Form | `file-lines` | `#3A9AB8` | F |
| `doc.PLN` | Plan | `file-lines` | `#3F3A9C` | PL |
| `doc.SPC` | Specification | `file-lines` | `#5B7FA6` | SP |
| `doc.generic` | Document | `file-lines` | `#2648A6` |  |

### Records (`rec.*`) — doc

Evidence that work was done. One green; type shown by the badge glyph.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `rec.generic` | Record | `file-circle-check` | `#3B6D11` |  |
| `rec.work_order` | Work order | `file-circle-check` | `#3B6D11` | glyph `wrench` |
| `rec.permit` | Permit to work | `file-circle-check` | `#3B6D11` | glyph `fire` |
| `rec.moc` | MOC record | `file-circle-check` | `#3B6D11` | glyph `arrows-rotate` |
| `rec.inspection` | Inspection report | `file-circle-check` | `#3B6D11` | glyph `magnifying-glass` |
| `rec.risk_assessment` | Risk assessment | `file-circle-check` | `#3B6D11` | glyph `triangle-exclamation` |
| `rec.deferral` | Deferral record | `file-circle-check` | `#3B6D11` | glyph `clock` |
| `rec.manifest` | Manifest / booking | `file-circle-check` | `#3B6D11` | glyph `helicopter` |
| `rec.training` | Training record | `file-circle-check` | `#3B6D11` | glyph `graduation-cap` |
| `rec.certificate` | Certificate | `file-circle-check` | `#3B6D11` | glyph `certificate` |
| `rec.review` | Review record | `file-circle-check` | `#3B6D11` | glyph `clipboard-check` |
| `rec.anomaly` | Anomaly record | `file-circle-check` | `#3B6D11` | glyph `circle-exclamation` |

### Data and measurement (`data.*`) — doc

Measures, KPIs, registers and dashboards.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `data.measure` | Measure / trend | `chart-line` | `#0F7C8C` |  |
| `data.kpi` | KPI | `gauge-high` | `#0F7C8C` |  |
| `data.register` | Register | `database` | `#0F7C8C` |  |
| `data.dataset` | Dataset / table | `table` | `#0F7C8C` |  |
| `data.dashboard` | Dashboard | `chart-pie` | `#0F7C8C` |  |
| `data.reading` | Field reading | `temperature-half` | `#0F7C8C` |  |
| `data.meter` | Meter | `gauge` | `#0F7C8C` |  |

### Systems (`sys.*`) — doc

Where records and data live.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `sys.generic` | System | `desktop` | `#3D4A55` |  |
| `sys.cmms` | Maintenance system (CMMS) | `desktop` | `#3D4A55` | glyph `screwdriver-wrench` |
| `sys.erp` | ERP / finance system | `desktop` | `#3D4A55` | glyph `coins` |
| `sys.docs` | Document system | `desktop` | `#3D4A55` | glyph `folder-open` |
| `sys.permit` | Permit system | `desktop` | `#3D4A55` | glyph `fire` |
| `sys.moc` | MOC system | `desktop` | `#3D4A55` | glyph `arrows-rotate` |
| `sys.rbi` | RBI / inspection software | `desktop` | `#3D4A55` | glyph `magnifying-glass` |
| `sys.logistics` | Logistics booking | `desktop` | `#3D4A55` | glyph `helicopter` |
| `sys.training` | Training system | `desktop` | `#3D4A55` | glyph `graduation-cap` |

### Resources (`res.*`) — circle

People, materials, money, transport and time.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `res.people` | People | `user-group` | `#7A4FA0` |  |
| `res.competence` | Competence | `id-badge` | `#7A4FA0` |  |
| `res.materials` | Materials | `boxes-stacked` | `#8E6A2E` |  |
| `res.spares` | Spares / parts | `box` | `#8E6A2E` |  |
| `res.tools` | Tools and NDT equipment | `toolbox` | `#8E6A2E` |  |
| `res.vehicle` | Vehicle | `truck` | `#8E6A2E` |  |
| `res.helicopter` | Helicopter | `helicopter` | `#8E6A2E` |  |
| `res.vessel` | Vessel | `ship` | `#8E6A2E` |  |
| `res.money` | Money | `coins` | `#A87A12` |  |
| `res.time` | Time | `clock` | `#444441` |  |

### Energy equipment (`eq.*`) — circle

Upstream and downstream plant. Most need custom drawing; a generic glyph stands in until then.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `eq.well` | Well | `oil-well` | `#D2691E` |  |
| `eq.borehole` | Borehole | `bore-hole` | `#D2691E` |  |
| `eq.wellhead` | Wellhead / Christmas tree *(custom wanted)* | `oil-well` | `#D2691E` |  |
| `eq.platform` | Platform *(custom wanted)* | `tower-observation` | `#D2691E` |  |
| `eq.fpso` | FPSO *(custom wanted)* | `ship` | `#D2691E` |  |
| `eq.separator` | Separator / vessel *(custom wanted)* | `database` | `#D2691E` |  |
| `eq.compressor` | Compressor *(custom wanted)* | `fan` | `#D2691E` |  |
| `eq.pump` | Pump *(custom wanted)* | `gears` | `#D2691E` |  |
| `eq.pipeline` | Pipeline *(custom wanted)* | `arrow-right-arrow-left` | `#D2691E` |  |
| `eq.pig_launcher` | Pig launcher / receiver *(custom wanted)* | `arrow-right-arrow-left` | `#D2691E` |  |
| `eq.relief_valve` | Relief valve *(custom wanted)* | `gauge-high` | `#D2691E` |  |
| `eq.flare` | Flare *(custom wanted)* | `fire-flame-curved` | `#D2691E` |  |
| `eq.tank` | Storage tank *(custom wanted)* | `database` | `#D2691E` |  |
| `eq.tank_farm` | Tank farm *(custom wanted)* | `cubes` | `#D2691E` |  |
| `eq.column` | Distillation column *(custom wanted)* | `industry` | `#D2691E` |  |
| `eq.jetty` | Jetty / tanker berth *(custom wanted)* | `anchor` | `#D2691E` |  |
| `eq.loading_rack` | Loading rack *(custom wanted)* | `truck-droplet` | `#D2691E` |  |
| `eq.meter_skid` | Metering skid *(custom wanted)* | `gauge` | `#D2691E` |  |
| `eq.crane` | Crane *(custom wanted)* | `gears` | `#D2691E` |  |
| `eq.process_plant` | Process plant | `industry` | `#D2691E` |  |

### Flow and decisions (`flow.*`) — circle

Start, end, decision, approval, timer, cycle and what moves between steps.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `flow.start` | Start | `play` | `#444441` |  |
| `flow.end` | End | `stop` | `#444441` |  |
| `flow.decision` | Decision | `code-branch` | `#444441` |  |
| `flow.approval` | Approval | `stamp` | `#444441` |  |
| `flow.timer` | Timer | `clock` | `#444441` |  |
| `flow.cycle` | Cycle | `rotate` | `#444441` |  |
| `flow.handoff` | Hand-off | `people-arrows` | `#E07A1F` |  |
| `flow.information` | Information moves | `share-nodes` | `#2F7FB8` |  |
| `flow.material` | Material moves | `box` | `#8E6A2E` |  |
| `flow.people` | People move | `person-walking` | `#7A4FA0` |  |

### Wait and rework reasons (`reason.*`) — circle

Why work is waiting or coming back. Used in bottleneck views.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `reason.resource` | Person or team busy | `user-clock` | `#E0AE2E` |  |
| `reason.information` | Waiting for information | `circle-question` | `#E0AE2E` |  |
| `reason.approval` | Waiting for approval | `stamp` | `#E0AE2E` |  |
| `reason.transport` | Waiting for transport | `helicopter` | `#E0AE2E` |  |
| `reason.weather` | Weather | `cloud-showers-heavy` | `#E0AE2E` |  |
| `reason.batch` | Held for a batch or campaign | `layer-group` | `#E0AE2E` |  |
| `reason.parts` | Waiting for parts | `box-open` | `#E0AE2E` |  |
| `reason.window` | Waiting for a work window | `calendar-days` | `#E0AE2E` |  |
| `reason.permit` | Waiting for a permit | `file-circle-exclamation` | `#E0AE2E` |  |
| `reason.incomplete` | Incomplete or wrong input (rework) | `rotate-left` | `#E0AE2E` |  |

### Status marks (`st.*`) — mark

Waiting, working, rework, blocked, overdue, effective, degraded, failed, trend.

| Key | Meaning | Glyph | Colour | Badge |
|---|---|---|---|---|
| `st.waiting` | Waiting | `hourglass-half` | `#E0AE2E` |  |
| `st.working` | Working | `gear` | `#0F6E56` |  |
| `st.rework` | Rework | `rotate-left` | `#C8402F` |  |
| `st.blocked` | Blocked | `ban` | `#C8402F` |  |
| `st.overdue` | Overdue | `clock` | `#BA7517` |  |
| `st.effective` | Effective | `check` | `#3B6D11` |  |
| `st.degraded` | Degraded | `minus` | `#BA7517` |  |
| `st.failed` | Failed | `xmark` | `#A32D2D` |  |
| `st.up` | Trend up | `arrow-up` | `#3B6D11` |  |
| `st.down` | Trend down | `arrow-down` | `#C8402F` |  |

<!-- CATALOGUE END -->
