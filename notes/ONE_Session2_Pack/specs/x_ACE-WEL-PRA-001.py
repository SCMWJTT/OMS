# extracted from ACE-WEL-PRA-001_Well_Barriers_and_Well_Handover_Practice_RevA.docx
BODY = [('h1', 'Purpose, scope and parent Standard', '6.4, 6.5'),
 ('p',
  'This Practice defines ACE’s technical method for establishing, verifying, monitoring and handing over well barriers in drilling, completion, '
  'production, suspension, intervention and abandonment states. It applies to wells at Pommerac A (PAP), Chenet B (CHB), Sapodilla C (SAP), and land '
  'leases Tamarind, Pawpaw and Soursop. It serves the planned Well Integrity Management Standard. Well-specific barrier schematics, status records '
  'and acceptance evidence are mandatory parts of the well file.'),
 ('h2', 'Roles and technical authority', '3.1, 6.4'),
 ('t',
  [['Role', 'Accountability'],
   ['Joanne Ho Sing — VP Wells', 'Approves barrier governance and high-risk well status decisions.'],
   ['Shalini Jaggernauth — Well Integrity Lead', 'Maintains barrier methodology, integrity categories, barrier status and technical review.'],
   ['Arjun Ramlal — Drilling Engineering Lead', 'Defines and verifies drilling barrier design and well construction barrier arrangements.'],
   ['Kathy-Ann Simmons — Completions Lead', 'Owns completion barrier design, installation and verification evidence.'],
   ['Nazim Bailey — Completions & Well Intervention Manager', 'Plans intervention barrier changes and confirms intervention readiness and closeout.'],
   ['Luis de Verteuil — Land Operations Manager', 'Coordinates land-well barrier status, access, monitoring and operational handover.'],
   ['Operations / Offshore Operations Manager', 'Accepts operational well status, surveillance and response responsibilities.'],
   ['Wellsite / intervention supervisor', 'Maintains barrier status, records tests, manages changes and communicates status.']]),
 ('h1', 'Barrier philosophy and well states', '6.4, 6.5'),
 ('p',
  'ACE applies a two-independent-barrier philosophy for activities and well states where required by the well design, risk assessment and applicable '
  'standards. The primary and secondary barrier envelopes are identified on a well-specific schematic. Independence is assessed for common failure '
  'modes, shared components, pressure sources, control dependencies and exposure to the same threat. Barrier selection is state-specific; a barrier '
  'configuration acceptable for production may not be acceptable for intervention, suspension or abandonment.'),
 ('t',
  [['Well state', 'Barrier schematic / status evidence', 'Key review'],
   ['Drilling',
    'Primary and secondary drilling barrier envelopes; components, fluids and verification',
    'Before drilling operations and after barrier changes'],
   ['Completion', 'Completion barriers, plugs/valves, test evidence and intended operating state', 'Before completion handover and production start'],
   ['Production',
    'Production barrier envelope and secondary barrier; surveillance and test history',
    'Routine integrity review and operating changes'],
   ['Suspended',
    'Suspension barriers, isolation points, status, monitoring and restoration plan',
    'At suspension and each monitoring/re-entry review'],
   ['Intervention',
    'Intervention-specific barriers, pressure control equipment, test records and contingency',
    'Before work; after each barrier change'],
   ['Abandoned', 'Permanent barrier placement, verification and final schematic', 'Abandonment acceptance and records closeout']]),
 ('h1', 'Barrier element acceptance and verification', '6.4, 6.5, 8.1'),
 ('appr',
  'Barrier elements are accepted against a defined function, design envelope and verification method. The well file shall identify element type, '
  'location, required pressure/temperature/chemical exposure, test criteria, test medium, duration, result, instrument calibration status and any '
  'limitations. Acceptance criteria shall be drawn from the approved well design, applicable technical standard and well-specific engineering basis; '
  'generic values shall not replace well-specific criteria.'),
 ('t',
  [['Element / evidence', 'Acceptance approach', 'Failure or uncertainty response'],
   ['Tubulars, casing and cement',
    'Design basis, cement evaluation where required, pressure test, integrity records and exposure limits',
    'Evaluate loss of containment / annular communication; restrict operations and assess remediation'],
   ['Wellhead and tree valves',
    'Function/pressure test to approved criteria; verify configuration and leak-tightness',
    'Isolate affected flow path; apply contingency and integrity categorisation'],
   ['Packers, plugs and subsurface safety valves',
    'Set/installation records, test/function evidence and qualification within service envelope',
    'Do not credit unverified element as barrier; review alternate barrier and activity limits'],
   ['Fluids and hydrostatic barriers',
    'Density, composition, level and compatibility within approved basis; verify losses and contamination',
    'Restore properties; reassess barrier margin and exposure before proceeding'],
   ['Cemented barrier',
    'Placement records, design and evaluation evidence; confirm intended isolation function',
    'Assess remediation or additional barrier; document technical acceptance'],
   ['Test equipment / records',
    'Calibration validity, test procedure, traceable values and independent review where required',
    'Invalid test is not accepted; repeat after correcting test limitations']]),
 ('h1', 'Well integrity categories and response', '6.4, 5.4'),
 ('t',
  [['Category', 'Definition / examples', 'Response'],
   ['Green',
    'Barriers verified and integrity condition within approved acceptance criteria; no unresolved threat affecting barrier function.',
    'Normal surveillance and scheduled testing.'],
   ['Yellow',
    'Degradation, uncertainty, abnormal annulus pressure or barrier element issue; risk remains managed with defined restrictions.',
    'Notify Wells Integrity; assess within defined timeframe; document restrictions and action owner.'],
   ['Orange',
    'Barrier degradation or evidence indicates elevated risk or reduced barrier redundancy; continued operation/intervention requires specific risk '
    'review.',
    'Prompt technical review; operating restrictions; approved mitigation and frequent surveillance.'],
   ['Red',
    'Barrier failure, uncontrolled pressure/flow, or condition with unacceptable loss of well integrity.',
    'Stop affected operation, secure well using approved response, escalate immediately and manage as incident/emergency as appropriate.']]),
 ('p',
  'Category assignment is based on the well-specific risk and barrier evidence, not solely on a colour label. The responsible Wells Technical '
  'Authority records the rationale, affected well state, required actions, due dates and review frequency. A category change is documented and '
  'communicated to Operations and relevant supporting functions.'),
 ('h1', 'Annulus pressure management', '6.4, 6.5, 9.1'),
 ('p',
  'Annulus pressure is monitored against the well-specific maximum allowable annulus surface pressure (MAASP), pressure source assessment, thermal '
  'effects, fluid level and annulus configuration. MAASP is calculated and approved from the well design and weakest exposed element; it is not '
  'copied from another well. Monitoring frequency is risk-based and increased for unexplained pressure, sustained trends or integrity-category '
  'changes.'),
 ('t',
  [['Control', 'Method / requirement', 'Evidence'],
   ['MAASP basis', 'Record calculation, weakest exposed element, fluid column and assumptions for each annulus.', 'Approved MAASP sheet / well file'],
   ['Monitoring frequency', 'Routine frequency set by well state and category; increase for abnormal pressure/trend.', 'Surveillance log / trend'],
   ['Pressure source assessment',
    'Differentiate thermal, trapped pressure, communication, leakage or fluid expansion; document uncertainty.',
    'Diagnostic record / engineering review'],
   ['Bleed-down',
    'Only under approved plan, with safe discharge route, monitoring, recording and competent supervision. Do not bleed merely to reset a pressure '
    'alarm.',
    'Bleed-down authorization and log'],
   ['Escalation',
    'Notify Well Integrity Lead and Operations for unexplained pressure, threshold exceedance or adverse trend.',
    'Notification, category review and action tracking'],
   ['MAASP exceedance',
    'Secure or restrict affected well state as specified in well-specific response; technical review before resumption.',
    'Incident/deviation record and authorization']]),
 ('h1', 'Well handover and return to Wells', '6.4, 8.1'),
 ('p',
  'Handover is a formal transfer of well status, operational responsibility and surveillance expectations. It is not complete merely because the '
  'well is physically connected to the facility or entered into a production system. The receiving role confirms that the information pack is '
  'complete, barrier status is understood, outstanding actions are accepted and the operating surveillance plan is available.'),
 ('t',
  [['Handover stage', 'Minimum information / decision'],
   ['Wells prepare',
    'Well state; schematic; primary/secondary barriers; element IDs; test results; MAASP; integrity category; restrictions; outstanding anomalies; '
    'monitoring plan; contingency.'],
   ['Technical review', 'Well Integrity Lead or delegated TA confirms barrier evidence, acceptance criteria, unresolved risk and any conditions.'],
   ['Operations acceptance',
    'Receiving Operations role reviews the pack, confirms practical surveillance/response and records acceptance or rejection.'],
   ['Live handover', 'Record effective date/time, well status, restrictions, alarm/monitoring expectations, open actions and responsible roles.'],
   ['Return to Wells for intervention',
    'Operations provides current status, production history, annulus trends, deviations, barriers and recent work; Wells acknowledges and plans '
    'intervention-specific barriers.'],
   ['Closeout',
    'After intervention, update schematic, test evidence, well state, status category, surveillance and register before returning to Operations.']]),
 ('h1', 'Unmanned platform and land-well application', '6.4, 8.1'),
 ('req',
  'Chenet B and Sapodilla C are normally unmanned and accessed by boat. Barrier surveillance and testing plans shall account for weather, boat '
  'availability, visit frequency, equipment readiness, remote monitoring limits and contingency response while the site is unattended. A missed '
  'visit or overdue test shall be assessed against well category and barrier risk; it is not automatically deferred until the next convenient boat '
  'trip. Land wells at Tamarind, Pawpaw and Soursop require site access coordination, local hazards, test equipment logistics and records suitable '
  'for dispersed locations.'),
 ('t',
  [['Location / context', 'Planning controls'],
   ['PAP — manned platform', 'OIM/Operations coordination; daily operational status visibility; well work permits and barrier status updates.'],
   ['CHB / SAP — unmanned platforms',
    'Boat visit plan, access/weather constraints, remote monitoring limitations, visit prioritization by integrity category and contingency for '
    'missed access.'],
   ['LND — Tamarind, Pawpaw, Soursop',
    'Land access, well identification, equipment transport, isolation/pressure test arrangements, local records and communications.'],
   ['PLB support base', 'Materials/test equipment availability, supply boat planning and backload/return of records or samples where required.']]),
 ('h1', 'Records, performance and assurance', '9.1, 9.4, 10.3'),
 ('t',
  [['Record', 'Owner', 'Minimum quality'],
   ['Well barrier schematic', 'Wells Technical Authority', 'Well identifier; state; barrier envelopes; elements; revision; acceptance status.'],
   ['Barrier test record',
    'Wellsite / intervention supervisor',
    'Test date; procedure; criteria; equipment calibration; measured result; pass/fail; reviewer.'],
   ['Well integrity register', 'Well Integrity Lead', 'Category; status; MAASP; surveillance; open actions; last/next review.'],
   ['Annulus pressure log', 'Operations / Wells', 'Annulus ID; pressure; time; conditions; trend; diagnostic; action and escalation.'],
   ['Handover pack and acceptance',
    'Wells and Operations',
    'Complete pack; outstanding items; restrictions; signatures/recorded acknowledgement; timestamp.'],
   ['Barrier change record', 'Wells / MOC owner', 'Reason; risk; approval; schematic update; test evidence; return-to-state verification.']]),
 ('h1', 'Implementing processes and procedures', '7.1, 7.4'),
 ('t',
  [['Process / procedure', 'Status', 'Steps relied on'],
   ['ACE-WEL-PRS-001 Well Handover', 'Planned', 'Prepare pack, technical review, Operations acceptance, live transfer, closeout.'],
   ['ACE-WEL-PRS-002 Annulus Pressure Management',
    'Planned',
    'Monitor, assess trend, diagnose, bleed-down if authorized, escalate, verify and close.'],
   ['ACE-MOC-PRC-001 Management of Change', 'Current', 'Barrier design/state changes, review, authorization, implementation and verification.']]),
 ('app', 'Well barrier decision flow', '6.4, 8.1'),
 ('t',
  [['Step', 'Decision / action'],
   ['1', 'Define well state and activity; identify required primary and secondary barrier envelopes.'],
   ['2', 'Select barrier elements; document independence and common failure considerations.'],
   ['3', 'Set well-specific acceptance criteria and verification plan.'],
   ['4', 'Verify/test each credited element; record traceable evidence.'],
   ['5', 'Assess status category; define restrictions, surveillance and escalation.'],
   ['6', 'Prepare handover or activity readiness pack; receiving role accepts.'],
   ['7', 'Monitor, update status after change, event or test; close records and revise schematic.']]),
 ('app', 'Reference basis', '6.4, 6.5'),
 ('t',
  [['Reference', 'Application'],
   ['NORSOK D-010', 'Well integrity, barrier philosophy and well barrier elements; use current applicable edition.'],
   ['ISO 16530-1', 'Well integrity management principles and lifecycle framework.'],
   ['API RP 90 / 90-2', 'Annulus pressure management and diagnostic considerations, as applicable.'],
   ['ACE-WEL-STD-001', 'Parent Well Integrity Management Standard (planned).']]),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-001'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-002'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-003'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-004'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-005'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-006'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-007'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-008'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-009'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-010'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-011'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-012'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-013'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-014'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-015'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-016'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-017'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-018'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-019'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-020'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-021'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-022'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-023'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-024'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-025'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-026'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-027'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-028'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-029'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-030'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-031'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-032'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-033'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-034'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-035'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-036'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-037'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-038'),
 ('rc',
  'Well barrier envelopes, elements, verification, category, pressure monitoring and handover are documented and reviewed against the well-specific '
  'integrity basis.  Control ID: C-WEL-039')]
