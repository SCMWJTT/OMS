# extracted from ACE-MNT-PRA-001_Equipment_Criticality_and_SCE_Maintenance_Practice_RevA.docx
BODY = [('h1', 'Purpose and scope', '6.4, 6.5, 8.2'),
 ('p',
  'This Practice defines ACE’s equipment criticality ranking and maintenance strategy method, including identification and maintenance assurance for '
  'Safety-Critical Elements (SCEs). It supports the Maintenance Management Standard and links to Asset Integrity, Risk, Control of Work and ONE '
  'deviation controls.'),
 ('p',
  'Applies to equipment and maintainable assets at the CPF, Pommerac A, Chenet B, Sapodilla C, land leases, shore base and supporting '
  'infrastructure.'),
 ('h1', 'Roles and authority', '6.4, 3.6'),
 ('p',
  'Reliability & Maintenance Lead owns criticality methodology and strategy consistency. Maintenance & Integrity Manager assures cross-functional '
  'alignment. Maintenance Superintendent coordinates execution and backlog. Equipment discipline leads advise failure modes and strategy. Operations '
  'confirms operating context and access, and accepts operational handover.'),
 ('p',
  'SCE designation and performance requirements are endorsed through integrity and technical authority arrangements. Operations and Maintenance must '
  'jointly resolve maintenance deferral or impairment decisions.'),
 ('h1', 'Equipment hierarchy and criticality', '6.4, 6.5'),
 ('p',
  'Maintain a consistent equipment hierarchy from site/system to functional location, equipment and maintainable component. Unique equipment IDs '
  'connect CMMS, integrity registers, ONE, drawings and maintenance history.'),
 ('p',
  'Rank equipment A/B/C using ACE risk criteria: safety/environment consequence, production impact, escalation potential, repairability, redundancy, '
  'detectability and failure history. Document rationale and uncertainty; avoid assigning criticality solely by equipment type.'),
 ('h1', 'Criticality method and reassessment', '6.4, 5.4'),
 ('p',
  'A-critical equipment has high consequence or essential barrier/function significance and requires enhanced strategy, planning and assurance. '
  'B-critical equipment has material consequence requiring managed preventive or condition-based maintenance. C equipment has lower consequence '
  'where a justified run-to-failure strategy may be acceptable.'),
 ('p',
  'Review ranking after failure, significant change, barrier role change, operating context change, redundancy loss, new risk assessment or '
  'reliability trend.'),
 ('h1', 'Safety-Critical Elements and performance standards', '6.5, 5.4'),
 ('p',
  'Identify SCEs through risk and barrier analysis and maintain the SCE register linked to AIM-REG-001 and performance standards. Each SCE has a '
  'defined safety function, required performance, verification method, maintenance tasks, test interval, failure criteria and impairment response.'),
 ('p',
  'SCE maintenance is not merely a work-order frequency: the task and test must verify the required function and preserve evidence of acceptance.'),
 ('h1', 'Maintenance strategy selection', '6.4, 6.5'),
 ('p',
  'Choose preventive/time-based, predictive/condition-based, functional testing, corrective or run-to-failure strategies according to failure modes, '
  'consequence, detection, degradation, data availability and lifecycle cost.'),
 ('p',
  'For A-critical assets, use an RCM-light review: function, functional failure, credible failure modes, consequence, effective task, task interval '
  'and residual risk. Run-to-failure requires documented justification and confirmation that failure consequence is tolerable.'),
 ('h1', 'Work order priority, backlog and planning', '6.4, 7.1'),
 ('p',
  'Prioritise work by risk, SCE status, operating impact, defect severity, overdue exposure, resource and access constraints. Priority is not a '
  'substitute for approved risk classification.'),
 ('p',
  'Maintenance planning confirms scope, materials, isolation needs, competency, vendor support, test requirements, permits, work packs and schedule '
  'dependencies. Backlog ageing and risk-weighted overdue work are reviewed.'),
 ('h1', 'SCE overdue, impairment, bypass and deviation', '6.5, 8.2, 7.1'),
 ('p',
  'An overdue SCE maintenance or test task is treated as a deviation and raised under ACE-OMS-STD-002. The record includes risk, expiry, approval, '
  'interim measures and visible ONE tracking. No overdue task is silently rescheduled to conceal the exposure.'),
 ('p',
  'Defeat, bypass, inhibit or impairment of an SCE requires Control of Work authorization, affected barrier identification, risk assessment, '
  'duration, compensating measures, communication, restoration checks and override-log entry. Escalate if conditions or time limit change.'),
 ('h1', 'Failure data, records and systems', '7.5, 6.4'),
 ('p',
  'Capture equipment ID, criticality, SCE flag, failure mode, symptom, cause, downtime, repair, parts, task history, test results and recurrence. '
  'Preserve links between work order, defect, risk, SCE register and performance standard.'),
 ('p',
  'Failure data is reviewed for repeat failures, task effectiveness, bad actors, spare strategy and criticality assumptions. CMMS data must be '
  'complete, consistent and auditable.'),
 ('h1', 'Performance, verification and process interfaces', '6.4, 9.5, 10.4'),
 ('p',
  'Reliability & Maintenance Lead reviews criticality coverage, preventive compliance, risk-weighted backlog, overdue SCE work, repeat failures, '
  'maintenance effectiveness and bad actors. Assurance samples SCE work orders for task quality, test acceptance, restoration and record '
  'completeness.'),
 ('h1', 'Implementing processes and procedures', '7.1, 7.4'),
 ('p',
  'These planned processes execute this Practice. Process maps must show Operations, Maintenance Planning, discipline Technical Authorities, Supply '
  'Chain and Integrity handovers.'),
 ('app', 'Criticality selection matrix', '6.4, 6.5'),
 ('t',
  [['Class', 'Indicative basis', 'Maintenance strategy expectation', 'Approval/evidence'],
   ['A',
    'High consequence, essential function, SCE or limited redundancy',
    'Preventive/predictive, functional tests, enhanced planning, failure review',
    'Documented risk/criticality assessment and TA input'],
   ['B',
    'Material production/asset consequence, manageable redundancy or repair',
    'Preventive/condition monitoring, planned corrective work',
    'Criticality basis and strategy record'],
   ['C',
    'Low consequence, tolerable and bounded failure impact',
    'Run-to-failure may be considered if justified; basic inspection as needed',
    'Documented justification and review trigger']]),
 ('app', 'Processes and procedures implementing this Practice', '7.1, 7.4'),
 ('t',
  [['Number', 'Title', 'Status', 'Steps relied on'],
   ['ACE-MNT-PRS-001',
    'Maintenance Planning and Scheduling Process',
    'Planned',
    'Criticality, strategy, work identification, planning, scheduling, execution and close-out'],
   ['ACE-MNT-PRS-002', 'SCE Deviation Process', 'Planned', 'Overdue/impairment review, approval, safeguards, restoration and closure'],
   ['ACE-MNT-WIN-001-PAP',
    'Pommerac A SCE maintenance work instruction',
    'Planned / priority list item',
    'Task execution, verification and evidence capture']]),
 ('app', 'Controls established by this Practice', '5.4, 7.1, 7.4'),
 ('t',
  [['Control ID', 'Control statement', 'Risk addressed', 'Section', 'Process step', 'Evidence'],
   ['C-MNT-001',
    'Equipment hierarchy and unique identifiers are maintained',
    'Untraceable maintenance history',
    '3',
    'Asset data review',
    'Equipment register'],
   ['C-MNT-002', 'Criticality is risk-based and documented', 'Strategy mismatches consequence', '3,4', 'Criticality review', 'Assessment'],
   ['C-MNT-003', 'SCE register and performance standard linkage is maintained', 'Barrier function unassured', '5', 'SCE review', 'SCE register'],
   ['C-MNT-004',
    'Maintenance strategy matches failure mode and risk',
    'Ineffective tasks or unmanaged failures',
    '6',
    'Strategy selection',
    'Strategy record'],
   ['C-MNT-005', 'A-critical tasks are planned and monitored', 'High consequence maintenance missed', '6,7', 'Work planning', 'CMMS plan'],
   ['C-MNT-006', 'Risk-weighted backlog is reviewed', 'High-risk overdue work hidden', '7', 'Backlog review', 'Backlog report'],
   ['C-MNT-007', 'Overdue SCE work has deviation controls', 'SCE exposure unmanaged', '8', 'SCE deviation', 'Deviation record'],
   ['C-MNT-008', 'SCE bypass/impairment is authorised and logged', 'Barrier defeated without control', '8', 'Control of Work', 'Override log'],
   ['C-MNT-009', 'Work completion includes test/restore evidence', 'Function not restored or proven', '8,9', 'Work close-out', 'Test and handback'],
   ['C-MNT-010', 'Failure feedback updates strategy', 'Recurring failure not addressed', '9,10', 'Reliability review', 'Failure analysis/actions']])]
