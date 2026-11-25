import csv, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
P = {r['Full Name']: r for r in csv.DictReader(open(os.path.join(ROOT, 'company/ACE_People.csv'), encoding='utf-8-sig'))}
def who(name):
    r = P[name]
    if r['Status'] != 'Active':
        raise ValueError(f"{name} is not active staff")
    return f"{name} — {r['Job Title']}"
def find(s):
    return [who(n) for n, r in P.items() if r['Status'] == 'Active' and s.lower() in (n + ' ' + r['Job Title']).lower()]
