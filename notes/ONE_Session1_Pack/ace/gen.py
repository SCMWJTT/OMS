import random, json, datetime as dt, sys
sys.path.insert(0, "/home/claude/ace")
from roles import *

random.seed(20261121)
ASOF = dt.date(2026, 11, 21)
FOUNDED = dt.date(2004, 3, 1)

# ---------- names ----------
FIRST = {
 "afro": {"M": ["Kwame","Marlon","Dwayne","Kerwin","Ricardo","Andre","Jason","Wendell","Kurt","Dexter","Brent","Nigel","Damian","Ronald","Darren","Kester","Shane","Jerome","Curtis","Anthony","Kevon","Terrence","Lyndon","Garvin","Hayden","Rawle","Selwyn","Keston","Dillon","Akil","Jabari","Kareem","Winston","Clyde","Rodney","Ainsley","Kendell","Marvin","Roger","Brian"],
          "F": ["Keisha","Natalie","Candice","Shelly-Ann","Marcia","Simone","Kerry-Ann","Allison","Jenelle","Tricia","Sherma","Nicola","Rochelle","Charmaine","Akilah","Nadine","Danielle","Kimberly","Marissa","Shernelle","Abigail","Teresa","Zahra","Jody-Ann","Celeste","Gillian","Melissa","Anya","Renee","Jacqueline","Monique","Tamika","Ayanna","Kathy-Ann","Lisa","Sharon","Sasha","Deborah","Arlene","Kizzy"]},
 "indo": {"M": ["Ravi","Vishnu","Anil","Rajesh","Sanjay","Deoraj","Kiran","Avinash","Rohan","Suresh","Imran","Shiva","Navin","Ramesh","Vijay","Dev","Ashwin","Rakesh","Nikhil","Arjun","Shaheed","Faizal","Ryan","Kevin","Vikash","Amit","Ricky","Ajay","Neil","Satesh","Krishna","Haresh","Nazim","Rishi","Mukesh","Darryl","Varun","Shastri","Ian","Aaron"],
          "F": ["Anjali","Priya","Sharda","Vidya","Rhea","Kavita","Sunita","Nadira","Shivani","Reshma","Asha","Indira","Savitri","Nalini","Shalini","Radhika","Amrita","Leela","Sita","Geeta","Aaliyah","Farah","Sabrina","Ria","Natasha","Vanessa","Shabana","Karishma","Sarita","Devika","Meera","Ashley","Rachel","Anushka","Tara","Seema","Kamini","Rajni","Nisha","Alicia"]},
 "creole": {"M": ["Marc","Philippe","Christian","Gerard","Luis","Carlos","Matthew","Stephen","Paul","Jean-Marc","Adrian","Robert","Gregory","Michael","Patrick"],
            "F": ["Claudine","Nicole","Celine","Isabel","Catherine","Juliana","Stephanie","Monica","Gabrielle","Chantal","Danielle","Sophia","Elena","Michelle","Andrea"]},
 "chinese": {"M": ["Jonathan","Edward","Kenneth","Wayne","Richard","Gary","Raymond","Trevor"],
             "F": ["Karen","Wendy","Lynette","Pamela","Joanne","Christine","Denise","Jennifer"]},
 "syrian": {"M": ["Elias","Joseph","Nadim","Fadi","George","Peter"],
            "F": ["Leila","Nadia","Rania","Maria","Christina","Samira"]},
}
SUR = {
 "afro": ["Joseph","Charles","Thomas","Williams","Phillip","Alexander","Lewis","Baptiste","Francis","Henry","Mitchell","George","St. Hill","Noel","Clarke","Daniel","Jack","Roberts","Bain","Pierre","Cummings","Edwards","Augustine","Mc Kenzie","Pascall","Sealy","Scott","Bobb","Greenidge","John","Paul","Garcia","Felix","Cooper","Wilson","Christopher","Hackett","Modeste","Granger","Bailey","Isaac","Andrews","Prescott","Lovelace","Sandy","Mark","Simmons","Gittens"],
 "indo": ["Maharaj","Ramlal","Persad","Singh","Mohammed","Ali","Khan","Rampersad","Boodoo","Seepersad","Ramnarine","Dookie","Gopaul","Sookdeo","Bissoon","Ramsaran","Jaggernauth","Mahabir","Hosein","Lutchman","Ramkissoon","Ramoutar","Sinanan","Rambharat","Dass","Baksh","Rajkumar","Deonarine","Beharry","Mungal","Sookram","Ramdass","Sankar","Seecharan","Ramcharan","Bhagwandeen","Rahaman","Hosany","Jagessar","Ramsingh"],
 "creole": ["de Verteuil","Gomes","Fernandes","de Souza","Rodriguez","Gonzales","Pereira","Lange","Farfan","Laquis","Boissiere","de Gannes","Mendes","Cipriani","Rostant"],
 "chinese": ["Chin","Achong","Lee Kim","Ho Sing","Ng Wai","Chan","Lum Kin","Kong","Ahyew","Low Chew"],
 "syrian": ["Elias","Habib","Khoury","Haddad","Mansour","Nassief"],
}
GROUP_W = [("afro",36),("indo",38),("creole",12),("chinese",8),("syrian",6)]
BLOCK = {"Carl Ramlakhan","Rajiv Budhooram","Nicole Sinclair","Anand Ramlogan","Kamla Persad","Keith Rowley"}

def pick_group():
    r = random.uniform(0, 100); acc = 0
    for g, w in GROUP_W:
        acc += w
        if r <= acc: return g
    return "afro"

used = set()
def make_name(g):
    while True:
        grp = pick_group()
        fn = random.choice(FIRST[grp][g])
        # occasional mixed heritage: first name from one group, surname from another
        sgrp = grp if random.random() > 0.15 else pick_group()
        sn = random.choice(SUR[sgrp])
        full = f"{fn} {sn}"
        if full not in used and full not in BLOCK and fn != sn:
            used.add(full); return fn, sn

# ---------- degrees ----------
UWI = "The University of the West Indies, St. Augustine"
UTT = "The University of Trinidad and Tobago"
ABROAD_ENG = ["Heriot-Watt University (UK)","University of Aberdeen (UK)","Robert Gordon University (UK)","Imperial College London (UK)","Texas A&M University (USA)","University of Calgary (Canada)","University of Houston (USA)","Colorado School of Mines (USA)","University of Manchester (UK)","Dalhousie University (Canada)"]
DEG = {
 "chem": (["BSc Chemical & Process Engineering"], [UWI]*6+[UTT]*2+ABROAD_ENG, ["MSc Process Safety & Loss Prevention","MSc Petroleum Engineering","MBA"]),
 "mech": (["BSc Mechanical Engineering","BSc Mechanical & Manufacturing Engineering"], [UWI]*6+[UTT]*2+ABROAD_ENG, ["MSc Asset Integrity Management","MSc Engineering Management","MBA","MSc Reliability Engineering"]),
 "elec": (["BSc Electrical & Computer Engineering"], [UWI]*7+[UTT]*2+ABROAD_ENG, ["MSc Control Systems","MSc Engineering Management","MBA"]),
 "civil": (["BSc Civil Engineering","BSc Civil & Environmental Engineering"], [UWI]*7+[UTT]+ABROAD_ENG, ["MSc Construction Management","MSc Project Management","MBA"]),
 "petro": (["BSc Petroleum Engineering","BSc Chemical & Process Engineering"], [UWI]*6+[UTT]*2+ABROAD_ENG, ["MSc Petroleum Engineering","MSc Reservoir Evaluation & Management","MBA"]),
 "geo": (["BSc Geology","BSc Geoscience"], [UWI]*5+["University of Leeds (UK)","University of Aberdeen (UK)","University of Calgary (Canada)","University of Houston (USA)"], ["MSc Petroleum Geoscience","MSc Petroleum Geology","PhD Geology"]),
 "gph": (["BSc Physics","BSc Geophysics"], [UWI]*5+["Imperial College London (UK)","University of Leeds (UK)","University of Houston (USA)"], ["MSc Exploration Geophysics","MSc Petroleum Geoscience"]),
 "mat": (["BSc Mechanical Engineering","BSc Materials Engineering"], [UWI]*5+[UTT]+["University of Manchester (UK)","University of Leeds (UK)"], ["MSc Corrosion Control Engineering","MSc Asset Integrity Management"]),
 "chemsci": (["BSc Chemistry","BSc Industrial Chemistry"], [UWI]*6+[UTT], ["MSc Analytical Chemistry"]),
 "acct": (["BSc Accounting","BSc Management Studies (Accounting)"], [UWI]*6+["UWI Cave Hill (Barbados)","Arthur Lok Jack Global School of Business"], ["ACCA","CPA","MBA","MSc Finance"]),
 "econ": (["BSc Economics","BSc Economics & Finance"], [UWI]*6+["UWI Mona (Jamaica)","University of Toronto (Canada)","London School of Economics (UK)"], ["MSc Energy Economics","MBA","MSc Finance"]),
 "mgmt": (["BSc Management Studies","BSc Business Management"], [UWI]*5+["Arthur Lok Jack Global School of Business","UWI Mona (Jamaica)"], ["MBA","MSc Project Management"]),
 "hr": (["BSc Human Resource Management","BSc Psychology","BSc Management Studies"], [UWI]*6+["UWI Mona (Jamaica)"], ["MSc Human Resource Management","MBA"]),
 "law": (["LLB (Hons)"], ["UWI Cave Hill (Barbados)"]*4+["University of London (UK)"], ["Legal Education Certificate, Hugh Wooding Law School","LLM Energy Law"]),
 "comms": (["BA Mass Communication","BA Communication Studies","BA English Literature"], [UWI]*5+["COSTAATT"], ["MA Corporate Communication","MBA"]),
 "social": (["BSc Sociology","BSc Social Work"], [UWI]*5, ["MSc Social Policy"]),
 "it": (["BSc Computer Science","BSc Information Technology"], [UWI]*5+[UTT]*2+["University of Toronto (Canada)"], ["MSc Information Security","MSc Data Science","MBA"]),
 "env": (["BSc Environmental & Natural Resource Management","BSc Biology"], [UWI]*6+[UTT], ["MSc Environmental Management"]),
 "ohs": (["BSc Occupational Health & Safety","BSc Environmental Health","BSc Chemical & Process Engineering"], [UWI]*3+[UTT]*3+["University of Aberdeen (UK)"], ["NEBOSH Diploma","MSc Occupational Safety & Health"]),
 "nursing": (["BSc Nursing"], [UWI]*4+["COSTAATT"], ["Offshore Medic Certificate"]),
 "med": (["MBBS"], [UWI]*4+["UWI Mona (Jamaica)"], ["MSc Occupational Medicine","Diploma in Occupational Health"]),
 "logistics": (["BSc Logistics & Supply Chain Management","BSc Management Studies"], [UWI]*3+[UTT]*2+["Arthur Lok Jack Global School of Business"], ["MSc Supply Chain Management","CIPS Diploma","MBA"]),
 "marine": (["BSc Nautical Science","Master Mariner (Class 1)"], ["Caribbean Maritime University (Jamaica)","Warsash Maritime School (UK)",UTT], ["MSc Maritime Operations"]),
 "tech": (["Technician Diploma - Process Operations","Technician Diploma - Mechanical","Technician Diploma - Electrical & Instrumentation","Associate Degree - Process Technology"], ["NESC Technical Institute","MIC Institute of Technology",UTT,"Point Lisas Campus, UTT","COSTAATT"], ["BSc Engineering Technology"]),
 "admin": (["Associate Degree - Business Administration","Certificate - Office Administration","BSc Management Studies"], ["COSTAATT","ROYTEC","School of Business & Computer Science",UWI], ["BSc Management Studies"]),
}
TECH_SPECIFIC = {"mtech":"Technician Diploma - Mechanical","eitech":"Technician Diploma - Electrical & Instrumentation",
                 "ptech_off":"Technician Diploma - Process Operations","fop":"Technician Diploma - Process Operations",
                 "cro_off":"Associate Degree - Process Technology","cro_on":"Associate Degree - Process Technology",
                 "cad":"Technician Diploma - Drafting & Design","corr_tech":"Technician Diploma - Mechanical"}

AGE = {1:(54,60),2:(46,58),3:(40,55),4:(36,54),5:(31,50),6:(24,44),7:(21,57)}
HIRE_MIN_AGE = {1:38,2:32,3:28,4:26,5:23,6:22,7:19}
POSTGRAD_P = {1:0.9,2:0.8,3:0.6,4:0.55,5:0.35,6:0.2,7:0.05}
LEVEL_NAME = {1:"L1 Chief Executive",2:"L2 Vice President",3:"L3 Manager",4:"L4 Lead / Superintendent",5:"L5 Senior Professional / Supervisor",6:"L6 Professional / Specialist",7:"L7 Technician / Administrative"}

def rand_date(a, b):
    return a + dt.timedelta(days=random.randint(0, (b - a).days))

# ---------- expand positions ----------
instances = []
for r in ROLES:
    for i in range(r["count"]):
        instances.append((r, i))
assert len(instances) == 300, len(instances)

# gender: exactly 150/150; leadership alternates
genders = ["F","M"]*150
random.shuffle(genders)
lead_g = iter(["M","F","F","M","F","M","F","M","F","M","F","M","F"])

people = []; holders = {}
for n, (r, i) in enumerate(instances):
    lvl = r["level"]
    if lvl <= 2:
        g = next(lead_g)
        genders.remove(g)
    else:
        g = genders.pop()
    fn, sn = make_name(g)
    age = random.randint(*AGE[lvl])
    birth = rand_date(dt.date(ASOF.year-age-1, ASOF.month, ASOF.day)+dt.timedelta(days=1), dt.date(ASOF.year-age, ASOF.month, ASOF.day))
    earliest = max(FOUNDED, dt.date(birth.year+HIRE_MIN_AGE[lvl], birth.month, min(birth.day,28)))
    latest = dt.date(2026, 10, 31)
    if lvl <= 2:   # senior leaders: hired earlier on average
        latest = min(latest, dt.date(2023, 12, 31))
    if earliest > latest: earliest = latest - dt.timedelta(days=365)
    hire = rand_date(earliest, latest)
    degs, unis, pgs = DEG[r["deg"]]
    deg = TECH_SPECIFIC.get(r["key"], random.choice(degs))
    uni = random.choice(unis)
    pg = random.choice(pgs) if random.random() < POSTGRAD_P[lvl] else ""
    if r["deg"] == "law": pg = "Legal Education Certificate, Hugh Wooding Law School"
    if r["deg"] == "med": pg = "MSc Occupational Medicine"
    loc = r["loc"]
    if r["key"] == "hse_adv": loc = ["PA","LAND","OG","HO"][i]
    if r["key"] in ("mtech","eitech"): loc = ["PA","OG","LAND","OG"][i % 4]
    if r["key"] == "planner": loc = ["HO","PA","OG"][i]
    if r["key"] == "comm_rel": loc = ["LAND","OG"][i]
    pid = f"ACE-{n+1:04d}"
    p = dict(id=pid, key=r["key"], first=fn, last=sn, name=f"{fn} {sn}", gender="Female" if g=="F" else "Male",
             age=age, birth=birth.isoformat(), degree=deg, institution=uni, postgrad=pg, hire=hire.isoformat(),
             title=r["title"], fn=r["fn"], dept=r["dept"], level=LEVEL_NAME[lvl], lvl=lvl,
             location=LOC[loc], pattern=PATTERN[loc], oms=r["oms"], disc=r["disc"], jd=r["jd"],
             email=f"{fn.lower().replace('-','')}.{sn.lower().replace(' ','').replace('.','')}@ace-energy.example",
             _parent=r["parent"], _dotted=r["dotted"], idx=i)
    people.append(p); holders.setdefault(r["key"], []).append(p)

# reporting lines (round robin across parent holders) and dotted lines
for p in people:
    par = p["_parent"]
    if par:
        hs = holders[par]; boss = hs[p["idx"] % len(hs)]
        p["reports_to"] = boss["id"]; p["reports_to_name"] = f'{boss["name"]} ({boss["title"]})'
    else:
        p["reports_to"] = "Board of Directors"; p["reports_to_name"] = "Board of Directors"
    d = p["_dotted"]
    if d:
        t = holders[d[0]][0]
        p["dotted_to"] = t["id"]; p["dotted_to_name"] = f'{t["name"]} ({t["title"]})'; p["dotted_purpose"] = d[1]
    else:
        p["dotted_to"] = p["dotted_to_name"] = p["dotted_purpose"] = ""
    # hire after manager's? not required, but senior people should not be hired before company
    del p["_parent"], p["_dotted"]

# ---------- checks ----------
from collections import Counter
assert len({p["name"] for p in people}) == 300
print("gender", Counter(p["gender"] for p in people))
print("leaders", [(p["title"], p["gender"]) for p in people if p["lvl"] <= 2])
for p in people:
    b = dt.date.fromisoformat(p["birth"]); h = dt.date.fromisoformat(p["hire"])
    assert h >= FOUNDED and (h - b).days/365.25 >= 18, p
    a = ASOF.year - b.year - ((ASOF.month, ASOF.day) < (b.month, b.day)); assert a == p["age"], p
print("functions", Counter(p["fn"] for p in people))
print("discipline leads", sum(1 for p in people if p["oms"].startswith("Technical Authority")))

out = dict(people=people, functions=FUNCTIONS, links=CROSS_LINKS, assets=ASSETS, elements=OMS_ELEMENTS,
           holders={k: [x["id"] for x in v] for k, v in holders.items()}, locations=LOC)
json.dump(out, open("/home/claude/ace/ace.json", "w"), indent=1)
print("ok", len(people))
