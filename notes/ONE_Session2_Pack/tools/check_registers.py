"""Integrity check of registers/ (links, people, ratings, dates). Run from repo root."""
import csv, collections
R = lambda f: list(csv.DictReader(open('registers/' + f, encoding='utf-8')))
P = {r['Full Name']: r['Job Title'] for r in csv.DictReader(open('company/ACE_People.csv', encoding='utf-8-sig'))}
risks, ctl, ev, act, ass, sce, kp, obj, bpm = [R(x) for x in ['RSK-REG-001.csv', 'RSK-REG-002.csv', 'INC-REG-001_events.csv', 'INC-REG-001_actions.csv',
    'AIM-REG-002.csv', 'AIM-REG-001.csv', 'PRF-REG-001_kpis.csv', 'OMS-REG-001_objectives.csv', 'BPM-REG-001.csv']]
err = []
def person(v, w):
    n, _, t = v.partition(' — ')
    if P.get(n) != t: err.append(f'person {w}: {v}')
for t, rows, cols in [('risk', risks, ['owner', 'escalation_vp']), ('control', ctl, ['owner']), ('action', act, ['owner']), ('objective', obj, ['owner']), ('process', bpm, ['owner']), ('kpi', kp, ['owner'])]:
    for r in rows:
        for c in cols: person(r[c], t)
RID = {r['risk_id'] for r in risks}; CID = {c['control_id']: c for c in ctl}; AID = {a['asset_id'] for a in ass}; EID = {e['event_id']: e for e in ev}
OID = {o['objective_id'] for o in obj}; SID = {s['sce_id'] for s in sce}
for c in ctl:
    if c['risk_id'] not in RID: err.append('control risk ' + c['control_id'])
    if c['asset_id'] and c['asset_id'] not in AID: err.append('control asset ' + c['control_id'])
    if c['sce_id'] and c['sce_id'] not in SID: err.append('control sce ' + c['control_id'])
M = {"E": "MHHVV", "D": "MMHHV", "C": "LMMHH", "B": "LLMMH", "A": "LLLMM"}; B = {"L": "Low", "M": "Medium", "H": "High", "V": "Very High"}
for r in risks:
    for x in filter(None, r['controls'].split('; ')):
        if x not in CID: err.append('risk control ' + x)
    if r['asset_id'] and r['asset_id'] not in AID: err.append('risk asset ' + r['risk_id'])
    if r['objective_id'] not in OID: err.append('risk objective ' + r['risk_id'])
    if B[M[r['current_l']][int(r['current_c']) - 1]] != r['current_rating']: err.append('rating ' + r['risk_id'])
    if B[M[r['residual_l']][int(r['residual_c']) - 1]] != r['residual_rating']: err.append('residual rating ' + r['risk_id'])
for e in ev:
    for x in filter(None, (e['controls_tested'] + '; ' + e['controls_failed']).split('; ')):
        if x not in CID: err.append('event control ' + x); continue
        if CID[x]['effective'] and e['date'] < CID[x]['effective']: err.append(f"{e['event_id']} uses {x} before {CID[x]['effective']}")
    for x in filter(None, e['risk_ids'].split('; ')):
        if x not in RID: err.append('event risk ' + x)
for a in act:
    if a['event_id'] not in EID: err.append('action event ' + a['action_id'])
    elif a['closed'] and a['closed'] < EID[a['event_id']]['date']: err.append('action closed before event ' + a['action_id'])
print('Register check:', 'OK' if not err else f'{len(err)} problems', err[:10])
