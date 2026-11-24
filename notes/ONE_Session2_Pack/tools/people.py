import csv
P={r['Full Name']:r for r in csv.DictReader(open('/home/claude/repo/company/ACE_People.csv',encoding='utf-8-sig'))}
def who(name):
    r=P[name]; return f"{name} — {r['Job Title']}"
def find(s):
    return [who(n) for n,r in P.items() if s.lower() in (n+' '+r['Job Title']).lower()]
