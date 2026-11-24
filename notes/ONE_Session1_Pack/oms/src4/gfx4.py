# New Rev 04 graphics (same palette as brand.py)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, FancyArrowPatch
from matplotlib import font_manager as fm
import glob, numpy as np
for f in glob.glob("/usr/share/fonts/opentype/inter/Inter-*.otf"): fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Inter"
INK="#12232E"; TEAL="#0E5A6B"; FLARE="#F26B21"; SAND="#F6F1E8"; SKY="#A7D8E3"; MUTE="#5B6B73"; NAVY="#3D5A80"
OUT="/home/claude/oms/img"
def save(fig,name): fig.savefig(f"{OUT}/{name}",dpi=200,bbox_inches="tight",pad_inches=0.05,transparent=True); plt.close(fig)

# 1. five-level pyramid with golden thread
def pyramid():
    fig,ax=plt.subplots(figsize=(8,5.2)); ax.set_xlim(-0.3,9.8); ax.set_ylim(0.7,6.4); ax.axis("off")
    L=[("Policy","OMS Manual · Policies","Why — our commitments · CEO","#0B4F5E"),
       ("Standard · Practice","Standards · Practices · Specifications","What must be true · how each discipline does it","#0F6B7A"),
       ("Process","Processes (swimlanes)","Who does what, in what order, across functions","#1E8796"),
       ("Procedure · Plan","Procedures · Plans","How one activity is done, step by step","#3AA3AE"),
       ("Task · Record","Work instructions · Forms · Registers","One task at one site · the evidence","#7FC3CC")]
    top=6.2; h=1.08; x0=4.4
    for i,(lv,t,s,c) in enumerate(L):
        y1=top-i*h; y0=y1-h+0.08; w1=1.9+i*0.44; w0=1.9+(i+1)*0.44
        ax.add_patch(Polygon([[x0-w0,y0],[x0+w0,y0],[x0+w1,y1],[x0-w1,y1]],color=c))
        tc="white" if i<4 else INK
        ax.text(x0,(y0+y1)/2+0.15,t,ha="center",va="center",fontsize=10.5,fontweight=700,color=tc)
        ax.text(x0,(y0+y1)/2-0.2,s,ha="center",va="center",fontsize=7.6,color=tc)
        ax.text(x0-w0-0.12,(y0+y1)/2,f"Level {i+1}",ha="right",va="center",fontsize=9,fontweight=700,color=c if i<4 else TEAL)
    # golden thread
    ax.add_patch(FancyBboxPatch((9.05,0.85),0.55,5.3,boxstyle="round,pad=0.02,rounding_size=0.25",color=FLARE))
    ax.text(9.325,3.5,"THE GOLDEN THREAD  ·  mission to record",rotation=90,ha="center",va="center",fontsize=8.2,fontweight=700,color="white")
    save(fig,"pyramid5.png")

# 2. golden thread chevrons
def thread():
    items=["Mission\nVision · Values","Strategy &\nobjectives","Policy","Standard &\nPractice","Process","Procedure","Record &\nevidence"]
    cols=["#0B4F5E","#0F6B7A","#1E8796","#3AA3AE",FLARE,"#F5923E",NAVY]
    fig,ax=plt.subplots(figsize=(10,1.5)); ax.set_xlim(0,len(items)*1.42+0.2); ax.set_ylim(0,1.2); ax.axis("off")
    for i,(t,c) in enumerate(zip(items,cols)):
        x=i*1.42; p=[[x,0.1],[x+1.3,0.1],[x+1.55,0.6],[x+1.3,1.1],[x,1.1],[x+0.25,0.6]]
        ax.add_patch(Polygon(p,color=c)); ax.text(x+0.78,0.6,t,ha="center",va="center",fontsize=8.6,fontweight=700,color="white",linespacing=1.1)
    save(fig,"thread.png")

# 3. control hinge
def hinge():
    fig,ax=plt.subplots(figsize=(7.5,5.2)); ax.set_xlim(-4.2,4.2); ax.set_ylim(-2.9,2.9); ax.axis("off"); ax.set_aspect("equal")
    nodes=[("Risk &\nthreat",FLARE),("Bow-tie\nbarrier","#D9480F"),("Document\nsection",TEAL),("Process\nstep","#1E8796"),
           ("Role &\nperson","#0F6B7A"),("Asset ·\nSCE",NAVY),("Evidence\nrecord","#5C7BA6"),("OMS\nexpectation","#3AA3AE")]
    for i,(t,c) in enumerate(nodes):
        a=np.radians(90-i*45); x,y=3.0*np.cos(a),2.15*np.sin(a)
        ax.plot([0,x],[0,y],color="#C9D3D7",lw=2.2,zorder=1)
        ax.add_patch(FancyBboxPatch((x-0.78,y-0.38),1.56,0.76,boxstyle="round,pad=0.02,rounding_size=0.18",color=c,zorder=2))
        ax.text(x,y,t,ha="center",va="center",fontsize=8.6,fontweight=700,color="white",zorder=3,linespacing=1.05)
    ax.add_patch(Circle((0,0),0.95,color=INK,zorder=4))
    ax.text(0,0.18,"CONTROL",ha="center",va="center",fontsize=12,fontweight=800,color="white",zorder=5)
    ax.text(0,-0.2,"C-AIM-014",ha="center",va="center",fontsize=8.5,color=SKY,zorder=5)
    ax.text(0,-0.45,"health: effective",ha="center",va="center",fontsize=7,color=SKY,zorder=5)
    save(fig,"hinge.png")

# 4. ACE value chain / process architecture L1
def chain():
    fig,ax=plt.subplots(figsize=(10,3.6)); ax.set_xlim(0,10.2); ax.set_ylim(0,3.6); ax.axis("off")
    core=["Explore &\nDevelop","Deliver\nWells","Operate &\nProduce","Process,\nMeasure & Sell"]
    for i,t in enumerate(core):
        x=0.1+i*2.5; p=[[x,2.0],[x+2.25,2.0],[x+2.5,2.65],[x+2.25,3.3],[x,3.3],[x+0.25,2.65]] if i else [[x,2.0],[x+2.25,2.0],[x+2.5,2.65],[x+2.25,3.3],[x,3.3]]
        ax.add_patch(Polygon(p,color=[TEAL,"#0F6B7A","#1E8796",FLARE][i])); ax.text(x+1.25,2.65,t,ha="center",va="center",fontsize=10,fontweight=700,color="white")
    ax.text(0.1,3.45,"CORE  —  how ACE creates value",fontsize=8.5,fontweight=700,color=TEAL)
    sup=["Maintain\nAssets","Move People\n& Materials","Manage Risk\n& HSE","People &\nCompetence","Supply Chain","Finance","Information"]
    for i,t in enumerate(sup):
        x=0.1+i*1.43; ax.add_patch(FancyBboxPatch((x,0.95),1.33,0.75,boxstyle="round,pad=0.01,rounding_size=0.1",color="#3AA3AE" if i<2 else "#7FC3CC"))
        ax.text(x+0.665,1.325,t,ha="center",va="center",fontsize=7.8,fontweight=700,color="white" if i<2 else INK)
    ax.text(0.1,1.8,"ENABLING",fontsize=8.5,fontweight=700,color="#1E8796")
    ax.add_patch(FancyBboxPatch((0.1,0.05),10.0,0.6,boxstyle="round,pad=0.01,rounding_size=0.1",color=INK))
    ax.text(5.1,0.35,"GOVERNING  —  Strategy & Planning  ·  OMS  ·  Assurance  ·  Business Process Management",ha="center",va="center",fontsize=8.6,fontweight=700,color="white")
    save(fig,"chain.png")

# 5. mini swimlane
def swim():
    lanes=["Change originator","MOC coordinator","Technical Authority","Area Authority"]
    fig,ax=plt.subplots(figsize=(10,3.4)); ax.set_xlim(0,10); ax.set_ylim(0,4); ax.axis("off")
    for i,l in enumerate(lanes):
        y=3-i; ax.add_patch(plt.Rectangle((0,y),10,1,color=["#EEF5F6","#FFFFFF"][i%2])); ax.add_patch(plt.Rectangle((0,y),1.6,1,color=[TEAL,"#0F6B7A","#1E8796","#3AA3AE"][i]))
        ax.text(0.8,y+0.5,l,ha="center",va="center",fontsize=8,fontweight=700,color="white")
    steps=[(2.3,3,"S01 Raise\nchange",TEAL,False),(4.0,2,"S02 Classify\n& screen","#0F6B7A",False),(5.7,1,"S03 Assess\nhazards","#1E8796",True),
           (7.3,0,"S04 Ready\nto use?","#3AA3AE",True),(8.9,2,"S05 Close\n& update docs","#0F6B7A",False)]
    prev=None
    for x,lane,t,c,ctl in steps:
        y=lane+0.5; ax.add_patch(FancyBboxPatch((x-0.62,y-0.3),1.24,0.6,boxstyle="round,pad=0.01,rounding_size=0.1",color=c,zorder=3))
        ax.text(x,y,t,ha="center",va="center",fontsize=7.2,fontweight=700,color="white",zorder=4)
        if ctl: ax.add_patch(Circle((x+0.62,y+0.3),0.13,color=FLARE,zorder=5)); ax.text(x+0.62,y+0.3,"C",ha="center",va="center",fontsize=6.5,fontweight=800,color="white",zorder=6)
        if prev: ax.add_patch(FancyArrowPatch((prev[0]+0.62,prev[1]),(x-0.62,y),arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.2,zorder=2,connectionstyle="arc3,rad=0"))
        prev=(x,y)
    save(fig,"swimlane.png")

for f in (pyramid,thread,hinge,chain,swim): f()
print("graphics done")
