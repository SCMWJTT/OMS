# OMS brand: colours and graphics (PNG for Word, same palette for web)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, FancyBboxPatch, Polygon
from matplotlib import font_manager as fm
import numpy as np, os

import glob
for f in glob.glob("/usr/share/fonts/opentype/inter/Inter-*.otf"):
    fm.fontManager.addfont(f)
FONT = "Inter"
plt.rcParams["font.family"] = FONT

INK = "#12232E"; TEAL = "#0E5A6B"; FLARE = "#F26B21"; SAND = "#F6F1E8"; SKY = "#A7D8E3"; MUTE = "#5B6B73"
EL = {1:"#0B4F5E",2:"#0F6B7A",3:"#1E8796",4:"#3AA3AE",5:"#D9480F",6:"#F26B21",7:"#F5923E",8:"#F8B26A",9:"#3D5A80",10:"#5C7BA6"}
ELNAME = {1:"Commitment &\naccountability",2:"Policies, standards\n& objectives",3:"Organisation,\nresources & capability",4:"Stakeholders\n& customers",
          5:"Risk assessment\n& control",6:"Asset design\n& integrity",7:"Plans &\nprocedures",8:"Execution\nof activities",
          9:"Monitoring,\nreporting & learning",10:"Assurance, review\n& improvement"}
GROUPS = [("LEAD",[1,2,3,4],TEAL),("CONTROL",[5,6,7,8],FLARE),("LEARN",[9,10],"#3D5A80")]
OUT = "/home/claude/oms/img"; os.makedirs(OUT, exist_ok=True)

def ang(i):  # segment i (1..10) centre angle, clockwise from top
    return 90 - (i-0.5)*36

def wheel(path, highlight=None, size=7, labels=True, center=True, bg=None):
    fig, ax = plt.subplots(figsize=(size,size), dpi=200)
    ax.set_xlim(-1.32,1.32); ax.set_ylim(-1.32,1.32); ax.axis("off"); ax.set_aspect("equal")
    if bg: fig.patch.set_facecolor(bg)
    else: fig.patch.set_alpha(0)
    # group arcs
    if labels:
        for name, els, col in GROUPS:
            a1 = 90 - (max(els))*36 + 1.2; a2 = 90 - (min(els)-1)*36 - 1.2
            ax.add_patch(Wedge((0,0),1.16,a1,a2,width=0.05,color=col,alpha=0.9 if highlight is None else 0.35))
            mid = np.radians((a1+a2)/2)
            ax.text(1.25*np.cos(mid),1.25*np.sin(mid),name,ha="center",va="center",fontsize=11*size/7,fontweight=700,color=col,
                    rotation=(np.degrees(mid)-90) if np.sin(mid)>0 else (np.degrees(mid)+90))
    for i in range(1,11):
        a2 = 90-(i-1)*36; a1 = a2-36
        on = highlight is None or highlight == i
        ax.add_patch(Wedge((0,0),1.08 if (highlight==i) else 1.0,a1+0.6,a2-0.6,width=0.5 if highlight!=i else 0.58,
                           color=EL[i], alpha=1 if on else 0.18))
        r = 0.75 if highlight!=i else 0.79; t = np.radians(ang(i))
        ax.text(r*np.cos(t), r*np.sin(t)+0.05, str(i), ha="center", va="center", fontsize=22*size/7, fontweight=800,
                color="white" if on else EL[i])
        if labels and size >= 6:
            ax.text(r*np.cos(t), r*np.sin(t)-0.09, ELNAME[i], ha="center", va="center", fontsize=6.2*size/7,
                    fontweight=600, color="white" if on else EL[i], linespacing=1.05)
    if center:
        ax.add_patch(Circle((0,0),0.46,color=INK))
        ax.text(0,0.1,"OMS",ha="center",va="center",fontsize=34*size/7,fontweight=800,color="white")
        ax.text(0,-0.12,"ONE MANAGEMENT\nSYSTEM",ha="center",va="center",fontsize=7.5*size/7,fontweight=600,color=SKY,linespacing=1.2)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.02, transparent=bg is None)
    plt.close(fig)

def element_badges():
    for i in range(1,11):
        wheel(f"{OUT}/el{i}.png", highlight=i, size=3.2, labels=False, center=True)

def systems_map(path):
    # the "risk thread": how OMS systems connect
    fig, ax = plt.subplots(figsize=(10,5.8), dpi=200); ax.set_xlim(0,100); ax.set_ylim(0,59); ax.axis("off")
    fig.patch.set_facecolor("white")
    steps = [("Know the\nhazards","Risk Management\nRisk Matrix\nHAZID / HAZOP / LOPA",EL[5]),
             ("Define the\nbarriers","Asset Integrity\nSafety-critical elements\nPerformance standards",EL[6]),
             ("Keep barriers\nhealthy","Maintenance\n& inspection\nOperating limits\nWell integrity",EL[7]),
             ("Do the work\nsafely","Control of Work\nPermits & isolations\nProcedures",EL[8]),
             ("Learn and\nimprove","Incidents & lessons\nKPIs, audit\nManagement review",EL[9])]
    w=17.2; gap=2.2; x=1.5
    for k,(h,b,c) in enumerate(steps):
        ax.add_patch(FancyBboxPatch((x,20),w,26,boxstyle="round,pad=0.4,rounding_size=1.6",fc=c,ec="none"))
        tc = INK if k==3 else "white"
        ax.text(x+w/2,40.5,h,ha="center",va="center",color=tc,fontsize=10,fontweight=800,linespacing=1.1)
        ax.text(x+w/2,28.5,b,ha="center",va="center",color=tc,fontsize=7.8,fontweight=500,linespacing=1.35)
        if k<4: ax.annotate("",xy=(x+w+gap-0.2,33),xytext=(x+w+0.3,33),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.6))
        x+=w+gap
    # MOC band
    ax.add_patch(FancyBboxPatch((1.5,7.5),96.8,7.5,boxstyle="round,pad=0.3,rounding_size=1.2",fc=INK,ec="none"))
    ax.text(50,11.2,"MANAGEMENT OF CHANGE protects the whole chain whenever plant, people, procedures or organisation change",
            ha="center",va="center",color="white",fontsize=9.2,fontweight=700)
    ax.annotate("",xy=(10,47),xytext=(90,47),arrowprops=dict(arrowstyle="-|>",color=MUTE,lw=1.2,connectionstyle="arc3,rad=0.12"))
    ax.text(50,56.5,"Lessons feed back into how we assess risk",ha="center",va="center",color=MUTE,fontsize=8.5,fontweight=600)
    ax.text(50,2.5,"Competence, contractors, documents and leadership support every step",ha="center",va="center",color=TEAL,fontsize=8.8,fontweight=700)
    fig.savefig(path,bbox_inches="tight",pad_inches=0.05); plt.close(fig)

def pyramid(path):
    fig, ax = plt.subplots(figsize=(8,5), dpi=200); ax.set_xlim(0,100); ax.set_ylim(0,62); ax.axis("off")
    levels=[("Level 1","OMS Manual · Policies","Why and what — approved by the CEO",INK),
            ("Level 2","Standards","What must be achieved — approved by system owners",TEAL),
            ("Level 3","Procedures · Plans","How it is done — approved by managers",EL[3]),
            ("Level 4","Work instructions · Forms · Registers","Task detail and records",EL[4])]
    H=13; y=58
    ax.set_xlim(-6,104)
    for k,(lv,name,desc,c) in enumerate(levels):
        top=y; bot=y-H; half_t=12+k*8.2; half_b=12+(k+1)*8.2
        ax.add_patch(Polygon([(42-half_t,top),(42+half_t,top),(42+half_b,bot+0.8),(42-half_b,bot+0.8)],closed=True,fc=c,ec="white",lw=2))
        ax.text(42,top-H/2+2.2,name,ha="center",va="center",color="white",fontsize=10.5,fontweight=800)
        ax.text(42,top-H/2-2.4,desc,ha="center",va="center",color="white",fontsize=7.6,fontweight=500)
        ax.text(42-half_b-1,top-H/2,lv,ha="right",va="center",color=c,fontsize=9.5,fontweight=800)
        y-=H
    ax.add_patch(FancyBboxPatch((85,9),17,40,boxstyle="round,pad=0.4,rounding_size=1.5",fc=FLARE,ec="none"))
    ax.text(93.5,29,"Technical\nstandards\n\nowned by the\nTechnical\nAuthorities",ha="center",va="center",color="white",fontsize=8.5,fontweight=700,linespacing=1.3)
    fig.savefig(path,bbox_inches="tight",pad_inches=0.05,transparent=True); plt.close(fig)

if __name__ == "__main__":
    wheel(f"{OUT}/cover_wheel.png")
    element_badges()
    systems_map(f"{OUT}/systems_map.png")
    pyramid(f"{OUT}/pyramid.png")
    print(sorted(os.listdir(OUT)))
