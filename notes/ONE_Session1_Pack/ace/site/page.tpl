<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ACE Organisation Chart</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* VOICE: calm, exact reference tool for an operating company's people and lines of authority
   IDEA: the wall-mounted org chart in a plant control building, with the dotted lines drawn in
   PICTURE: function hub map with Engineering & Projects at the centre and the dotted lines into it
   COLOUR and TYPE: ice ground, ink text, hot pink for dotted/technical lines; Space Grotesk + Inter
   LAYOUT: header + view tabs, picture full width, detail drawer on the right (bottom on phones) */
:root{color-scheme:light dark;--bg:light-dark(#dff1f7,#06222e);--ink:light-dark(#06222e,#e3f2f7);--card:light-dark(#ffffff,#0c3040);--line:light-dark(#b7d4de,#24505f);--mute:light-dark(#3c5b66,#9fbfca);--pink:#ff2e7e}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Inter,system-ui,sans-serif;overflow-x:clip}
h1,h2,h3{font-family:"Space Grotesk",Inter,sans-serif;font-weight:600;line-height:1.05;margin:0}
h1{font-size:clamp(28px,4vw,44px);text-wrap:balance}
h2{font-size:22px;margin-bottom:10px}
.band{padding:clamp(20px,3vw,40px) max(4vw,16px)}
header.band{padding-bottom:12px}
.sub{color:var(--mute);margin:8px 0 0;max-width:70ch}
.stats{display:flex;flex-wrap:wrap;gap:8px 28px;margin-top:16px}
.stats b{font-family:"Space Grotesk",Inter,sans-serif;font-size:26px;display:block;line-height:1}
.stats span{font-size:13px;color:var(--mute)}
nav{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:6px;padding:0 max(4vw,16px);border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}
nav a{flex:none;padding:12px 14px;text-decoration:none;color:var(--mute);font-weight:500;border-bottom:3px solid transparent;min-height:44px}
nav a.on{color:var(--ink);border-color:var(--pink)}
nav a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:2px solid var(--pink);outline-offset:2px}
.view{display:none}.view.on{display:block}
.fig{position:relative;height:clamp(420px,70vh,640px);align-self:start}.fig>svg{position:absolute;inset:0;width:100%;height:100%}
.toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}
button,select,input{font:inherit;font-size:16px;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px;min-height:44px}
button{cursor:pointer}button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.chip{display:inline-block;font-size:12px;font-weight:600;color:#fff;border-radius:999px;padding:2px 9px;white-space:nowrap}
.grid2{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:24px}
@media(max-width:900px){.grid2{grid-template-columns:minmax(0,1fr)}}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.note{font-size:13px;color:var(--mute)}
/* structure */
.ceo{display:flex;justify-content:center;margin-bottom:14px}
.fnrow{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
.fncard{text-align:left;background:var(--card);border:1px solid var(--line);border-top:6px solid var(--c);border-radius:10px;padding:10px 12px;display:block;width:100%}
.fncard.act{outline:3px solid var(--c)}
.fncard .n{font-family:"Space Grotesk",Inter,sans-serif;font-weight:600;font-size:15px;line-height:1.15}
.fncard .h{font-size:13px;color:var(--mute)}
.tree{margin-top:18px}
.tree ul{list-style:none;margin:0;padding-left:22px;border-left:1px dashed var(--line)}
.tree>ul{padding-left:0;border:0}
.node{display:flex;flex-wrap:wrap;gap:2px 10px;align-items:baseline;padding:4px 0}
.node .pn{background:none;border:0;padding:0;min-height:0;font-weight:600;color:var(--ink);text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:3px}
.node .t{color:var(--mute);font-size:14px}
.node .ta{font-size:12px;color:var(--pink);font-weight:600}
summary{cursor:pointer;list-style:none}summary::-webkit-details-marker{display:none}
summary .node::before{content:"▸";width:14px;color:var(--mute)}details[open]>summary .node::before{content:"▾"}
.leaf .node::before{content:"";width:14px}
.cnt{font-size:12px;color:var(--mute)}
/* elements */
.els{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;margin-top:10px}
.el{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-size:14px}
.el b{font-family:"Space Grotesk",Inter,sans-serif}
/* tables */
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;font-weight:600;color:var(--mute);border-bottom:2px solid var(--line);padding:8px 6px}
td{border-bottom:1px solid var(--line);padding:8px 6px;vertical-align:top}
tr.click{cursor:pointer}tr.click:hover td{background:color-mix(in srgb,var(--pink) 8%,transparent)}
td.num{text-align:right}
.scroll{overflow-x:auto}
/* drawer */
#drawer{position:fixed;top:0;right:0;width:min(420px,100%);height:100%;background:var(--card);border-left:1px solid var(--line);box-shadow:-8px 0 30px rgba(0,0,0,.15);padding:20px;overflow:auto;transform:translateX(105%);transition:transform .25s;z-index:20}
#drawer.on{transform:none}
#drawer dl{display:grid;grid-template-columns:8.5em 1fr;gap:6px 10px;font-size:14px;margin:14px 0}
#drawer dt{color:var(--mute)}#drawer dd{margin:0}
#drawer .x{float:right}
.lnk{background:none;border:0;padding:0;min-height:0;color:var(--ink);text-decoration:underline;font-size:14px;text-align:left}
@media(max-width:600px){#drawer{top:auto;bottom:0;height:78%;width:100%;border-left:0;border-top:1px solid var(--line);transform:translateY(105%);border-radius:16px 16px 0 0}
.fig{height:440px}table{font-size:13px}.stack thead{display:none}.stack tr{display:grid;padding-block:10px}.stack td{display:flow-root;border:0;padding:3px 0;padding-inline-start:8em;text-align:start}.stack td::before{content:attr(data-l);float:inline-start;width:7.5em;margin-inline-start:-8em;white-space:normal;color:var(--mute)}.stack td:empty{display:none}}
@media(prefers-reduced-motion:reduce){#drawer{transition:none}}
footer{font-size:13px;color:var(--mute)}
.loader{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:16px}
.btn{display:inline-flex;align-items:center;font-size:16px;background:var(--ink);color:var(--bg);border-radius:8px;padding:8px 14px;min-height:44px;cursor:pointer}
#checks{margin-top:8px;max-width:90ch}#checks:empty{display:none}
body.drag{outline:4px dashed var(--pink);outline-offset:-8px}
</style><script>new MutationObserver(()=>{for(const c of document.querySelectorAll('.stack td:not([data-l])')){let i=0,p=c;while(p=p.previousElementSibling)i+=p.colSpan;c.dataset.l=c.closest('table').rows[0].cells[i]?.textContent||''}}).observe(document,{childList:true,subtree:true})</script></head><body>

<header class="band">
  <h1>Acme Caribbean Energy: who reports to whom, and who holds the technical lines</h1>
  <p class="sub">A Central Trinidad crude and gas producer with small Gulf of Paria platforms, land leases and a Central Processing Facility. Solid lines run through 13 functions. Dotted lines tie the discipline leads to Engineering &amp; Projects through the Technical Leadership Council.</p>
  <div class="stats" id="stats"></div>
  <div class="loader">
    <label class="btn" for="csv">Load CSV</label><input id="csv" type="file" accept=".csv,text/csv" hidden>
    <button id="reset" hidden>Back to built-in data</button>
    <span class="note" id="src"></span>
  </div>
  <div id="checks" class="note"></div>
</header>
<nav id="tabs">
  <a href="#network" data-v="network">Cross-functional map</a>
  <a href="#structure" data-v="structure">Reporting structure</a>
  <a href="#disciplines" data-v="disciplines">Discipline leads</a>
  <a href="#people" data-v="people">People</a>
</nav>

<section class="view band" id="v-network">
  <div class="toolbar" role="group" aria-label="Map lines">
    <button id="mLinks" class="on">Function relationships</button>
    <button id="mDot">Discipline-lead dotted lines</button>
    <span class="note" id="mNote">Line weight shows how strong the working relationship is. Select a function to see its links.</span>
  </div>
  <div class="grid2">
    <div class="card fig" id="netfig"><svg id="net" role="img" aria-label="Map of ACE functions and their relationships"></svg></div>
    <div class="card" id="netside"></div>
  </div>
</section>

<section class="view band" id="v-structure">
  <div class="ceo" id="ceo"></div>
  <div class="fnrow" id="fnrow"></div>
  <div class="tree card" id="tree"></div>
  <h2 style="margin-top:28px">OMS element owners</h2>
  <p class="note">IOGP 510 Operating Management System Framework (2014), © IOGP / IPIECA. Element titles reproduced with acknowledgement.</p>
  <div class="els" id="els"></div>
</section>

<section class="view band" id="v-disciplines">
  <h2>32 discipline leads, one Technical Leadership Council</h2>
  <p class="sub" style="margin-bottom:16px">Each lead keeps a solid reporting line in a home function and holds a dotted line to the VP Engineering &amp; Projects. Each is the Technical Authority for the discipline.</p>
  <div class="grid2">
    <div class="card scroll"><table class="stack" id="dtab"></table></div>
    <div class="card"><h3 style="margin-bottom:10px">Leads by home function</h3><div id="dbars"></div></div>
  </div>
</section>

<section class="view band" id="v-people">
  <div class="toolbar">
    <input id="q" type="search" placeholder="Search name, title, discipline or OMS role" aria-label="Search people" style="flex:1 1 260px">
    <select id="fFn" aria-label="Function"></select>
    <select id="fLoc" aria-label="Location"></select>
    <select id="fLvl" aria-label="Grade"></select>
    <span class="note" id="pcount"></span>
  </div>
  <div class="card scroll"><table class="stack" id="ptab"></table></div>
</section>

<footer class="band">All people and the company are fictional. Built-in data as at 21 November 2026. To update, save the People tab of ACE_Organisation.xlsx as CSV and load it here, or drop the file on the page. Cynmark Systems Limited.</footer>
<script type="application/json" id="seed">__SEED__</script>

<aside id="drawer" aria-live="polite"></aside>

<script>
{
const COL={EXEC:"#06222e",EXD:"#a06a00",WEL:"#b3261e",ENP:"#ff2e7e",OPS:"#0b7a75",HSE:"#d96c00",FIN:"#3d5a80",HR:"#7b4fa0",SCM:"#2a7f9e",IDK:"#4a4e69",BDM:"#9c4f2c",CCS:"#6d7a1f",LGA:"#5c5470"};
const SHORT={EXEC:"CEO Office",EXD:"Exploration & Dev.",WEL:"Wells",ENP:"Engineering & Projects",OPS:"Operations",HSE:"HSE & Compliance",FIN:"Finance",HR:"Human Resources",SCM:"Supply Chain",IDK:"IT, Data & Knowledge",BDM:"BD & Markets",CCS:"Comms & Corp. Services",LGA:"Legal & Gov. Affairs"};
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
let D,byId={},kids={},fnBy={},sel=null,mode="links",curFn="ENP";
const chip=f=>`<span class="chip" style="background:${COL[f]}">${esc(fnBy[f].name)}</span>`;
const pbtn=p=>`<button class="lnk" data-p="${p.id}">${esc(p.name)}</button>`;
const isTA=p=>p.oms.startsWith("Technical Authority");

function head(f){const h=byId[f.head];if(h&&h.fn===f.code)return h;return D.people.filter(p=>p.fn===f.code).sort((a,b)=>a.lvl-b.lvl)[0]}
const NOBODY={id:"",name:"Not assigned",title:"Vacant",fn:"EXEC"};
function show(id){
  const p=byId[id];if(!p)return;const m=byId[p.reports_to],d=byId[p.dotted_to];
  const team=(kids[id]||[]);
  $("#drawer").innerHTML=`<button class="x" id="cl" aria-label="Close">Close</button>
  <h2>${esc(p.name)}</h2><div>${esc(p.title)}</div><div style="margin-top:8px">${chip(p.fn)}</div>
  <p style="font-size:15px">${esc(p.jd)}</p>
  <dl><dt>Employee ID</dt><dd>${p.id}</dd><dt>Department</dt><dd>${esc(p.dept)}</dd><dt>Grade</dt><dd>${esc(p.level)}</dd>
  <dt>Reports to</dt><dd>${m?pbtn(m)+" · "+esc(m.title):"Board of Directors"}</dd>
  ${d?`<dt>Dotted line</dt><dd>${pbtn(d)} · ${esc(p.dotted_purpose)}</dd>`:""}
  ${p.oms?`<dt>OMS role</dt><dd>${esc(p.oms)}</dd>`:""}${p.disc?`<dt>Discipline</dt><dd>${esc(p.disc)}</dd>`:""}
  <dt>Location</dt><dd>${esc(p.location)}</dd><dt>Gender, age</dt><dd>${p.gender}, ${p.age}</dd><dt>Hired</dt><dd>${p.hire}</dd>
  <dt>Degree</dt><dd>${esc(p.degree)}, ${esc(p.institution)}</dd>${p.postgrad?`<dt>Further</dt><dd>${esc(p.postgrad)}</dd>`:""}
  ${team.length?`<dt>Direct reports</dt><dd>${team.map(pbtn).join("<br>")}</dd>`:""}</dl>`;
  $("#drawer").classList.add("on");$("#cl").focus();
}
document.addEventListener("click",e=>{
  const b=e.target.closest("[data-p]");if(b){e.preventDefault();show(b.dataset.p);return}
  if(e.target.id==="cl")$("#drawer").classList.remove("on");
});
document.addEventListener("keydown",e=>{if(e.key==="Escape")$("#drawer").classList.remove("on")});

/* ---------- network ---------- */
const svg=$("#net");
function drawNet(){
  if(!D)return;const W=svg.clientWidth,H=svg.clientHeight;if(!W)return;
  const cx=W/2,cy=H/2,R=Math.min(W*(W<520?0.36:0.27),H*0.38),small=W<520;
  const others=D.functions.filter(f=>f.code!=="ENP");const pos={ENP:[cx,cy]};
  others.forEach((f,i)=>{const a=-Math.PI/2+i*2*Math.PI/others.length;pos[f.code]=[cx+R*Math.cos(a),cy+R*Math.sin(a)]});
  const hc=c=>D.people.filter(p=>p.fn===c).length,rad=c=>Math.max(14,Math.sqrt(hc(c))*(small?2.6:3.4));
  let edges="";
  if(mode==="links"){
    for(const l of D.links){const [x1,y1]=pos[l.a],[x2,y2]=pos[l.b];const hit=!sel||l.a===sel||l.b===sel;
      const w={Strong:4,Medium:2.2,Light:1.2}[l.strength];
      edges+=`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${hit&&sel?"#ff2e7e":"currentColor"}" stroke-opacity="${hit?(sel?.9:.35):.07}" stroke-width="${w}"/>`}
  }else{
    const cnt={};D.people.filter(isTA).forEach(p=>cnt[p.fn]=(cnt[p.fn]||0)+1);
    for(const f in cnt){if(f==="ENP")continue;const [x1,y1]=pos[f];const hit=!sel||sel===f||sel==="ENP";
      edges+=`<line x1="${x1}" y1="${y1}" x2="${cx}" y2="${cy}" stroke="#ff2e7e" stroke-width="${1+cnt[f]}" stroke-dasharray="6 5" stroke-opacity="${hit?.85:.12}"/>`;
      const mx=(x1+cx)/2,my=(y1+cy)/2;
      edges+=`<circle cx="${mx}" cy="${my}" r="11" fill="var(--card)" stroke="#ff2e7e"/><text x="${mx}" y="${my+4}" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">${cnt[f]}</text>`}
  }
  let nodes="";
  for(const f of D.functions){const [x,y]=pos[f.code],r=rad(f.code),dim=sel&&sel!==f.code&&mode==="links"&&!D.links.some(l=>(l.a===sel&&l.b===f.code)||(l.b===sel&&l.a===f.code));
    const lx=x+(f.code==="ENP"?0:(x-cx)/R*(r+8)),ly=f.code==="ENP"?y+r+16:y+(y-cy)/R*(r+8)+4;
    const anc=f.code==="ENP"?"middle":Math.abs(x-cx)<8?"middle":x>cx?"start":"end";
    const nm=small?f.code:SHORT[f.code];
    nodes+=`<g data-f="${f.code}" style="cursor:pointer" opacity="${dim?.3:1}" tabindex="0" role="button" aria-label="${esc(f.name)}">
     <circle cx="${x}" cy="${y}" r="${r}" fill="${COL[f.code]}" stroke="${sel===f.code?"#ff2e7e":"var(--card)"}" stroke-width="${sel===f.code?4:2}"/>
     <text x="${x}" y="${y+5}" text-anchor="middle" fill="#fff" font-size="13" font-weight="600">${hc(f.code)}</text>
     <text x="${lx}" y="${ly}" text-anchor="${anc}" font-size="${small?11:13}" font-weight="600" fill="currentColor" stroke="var(--bg)" stroke-width="4" paint-order="stroke">${esc(nm)}</text></g>`}
  svg.innerHTML=`<g style="color:var(--ink)">${edges}${nodes}</g>`;
}
svg.addEventListener("click",e=>{const g=e.target.closest("[data-f]");sel=g?(sel===g.dataset.f?null:g.dataset.f):null;drawNet();side()});
svg.addEventListener("keydown",e=>{if(e.key==="Enter"){const g=e.target.closest("[data-f]");if(g){sel=g.dataset.f;drawNet();side()}}});
function side(){
  const el=$("#netside");
  if(!sel){el.innerHTML=mode==="links"?`<h3 style="margin-bottom:8px">How the functions depend on each other</h3><p class="note">Numbers in the circles are headcount. Engineering &amp; Projects sits at the centre because the technical lines from every function run through it.</p>
   <table><tr><th>Strongest links</th><th></th></tr>${D.links.filter(l=>l.strength==="Strong").map(l=>`<tr><td>${chip(l.a)} ${chip(l.b)}</td><td class="note">${esc(l.nature)}</td></tr>`).join("")}</table>`
   :`<h3 style="margin-bottom:8px">Dotted lines into Engineering &amp; Projects</h3><p class="note">Each dashed line carries the number of discipline leads whose home is in that function. The leads sit on the Technical Leadership Council, chaired by the VP Engineering &amp; Projects.</p>
   ${D.people.filter(isTA).sort((a,b)=>a.fn.localeCompare(b.fn)).map(p=>`<div style="padding:3px 0">${chip(p.fn)} ${pbtn(p)} <span class="note">${esc(p.disc)}</span></div>`).join("")}`;return}
  const f=fnBy[sel],h=head(f)||NOBODY,ls=D.links.filter(l=>l.a===sel||l.b===sel),tas=D.people.filter(p=>isTA(p)&&p.fn===sel);
  el.innerHTML=`<h3>${esc(f.name)}</h3><p style="margin:6px 0">${esc(f.purpose)}</p><p class="note">Head: ${pbtn(h)} · ${esc(h.title)}<br>Main OMS elements: ${esc(f.elements)}</p>
  <h3 style="margin:14px 0 6px;font-size:16px">Relationships (${ls.length})</h3>
  ${ls.map(l=>{const o=l.a===sel?l.b:l.a;return`<div style="padding:4px 0">${chip(o)} <b style="font-size:12px">${l.strength}</b><div class="note">${esc(l.nature)}</div></div>`}).join("")}
  ${tas.length?`<h3 style="margin:14px 0 6px;font-size:16px">Discipline leads based here (${tas.length})</h3>${tas.map(p=>`<div>${pbtn(p)} <span class="note">${esc(p.disc)}</span></div>`).join("")}`:""}
  <p><button id="toTree">Open in reporting structure</button></p>`;
  $("#toTree").onclick=()=>{curFn=sel;location.hash="structure"};
}
$("#mLinks").onclick=()=>{mode="links";$("#mLinks").classList.add("on");$("#mDot").classList.remove("on");$("#mNote").textContent="Line weight shows how strong the working relationship is. Select a function to see its links.";drawNet();side()};
$("#mDot").onclick=()=>{mode="dot";$("#mDot").classList.add("on");$("#mLinks").classList.remove("on");$("#mNote").textContent="Dashed lines show discipline leads reporting on a dotted line to Engineering & Projects.";drawNet();side()};
const netObs=new ResizeObserver(drawNet);netObs.observe(svg);

/* ---------- structure ---------- */
function subtree(id){return(kids[id]||[]).reduce((n,k)=>n+1+subtree(k.id),0)}
function li(p,depth){
  const ch=kids[p.id]||[];
  const row=`<div class="node"><button class="pn" data-p="${p.id}">${esc(p.name)}</button><span class="t">${esc(p.title)}</span>${isTA(p)?`<span class="ta">Technical Authority</span>`:""}${ch.length?`<span class="cnt">${subtree(p.id)} in team</span>`:""}</div>`;
  if(!ch.length)return`<li class="leaf">${row}</li>`;
  return`<li><details ${depth<2?"open":""}><summary>${row}</summary><ul>${ch.map(c=>li(c,depth+1)).join("")}</ul></details></li>`;
}
function drawStructure(){
  const ceo=D.people.find(p=>p.lvl===1)||D.people.find(p=>!byId[p.reports_to])||D.people[0];
  $("#ceo").innerHTML=`<button class="fncard" style="--c:${COL.EXEC};max-width:280px" data-p="${ceo.id}"><div class="n">${esc(ceo.name)}</div><div class="h">Chief Executive Officer</div></button>`;
  $("#fnrow").innerHTML=D.functions.map(f=>{const h=head(f)||NOBODY;return`<button class="fncard ${f.code===curFn?"act":""}" style="--c:${COL[f.code]}" data-fn="${f.code}"><div class="n">${esc(f.name)}</div><div class="h">${esc(h.name)} · ${D.people.filter(p=>p.fn===f.code).length} people</div></button>`}).join("");
  const f=fnBy[curFn],h=head(f);
  const root=curFn==="EXEC"?D.people.filter(p=>p.fn==="EXEC"&&p.reports_to===ceo.id):(h?[h]:[]);
  $("#tree").innerHTML=`<h2>${esc(f.name)}</h2><p class="note" style="margin-top:0">${esc(f.purpose)}</p><ul>${root.map(p=>li(p,0)).join("")}</ul>`;
}
$("#fnrow").addEventListener("click",e=>{const b=e.target.closest("[data-fn]");if(b){curFn=b.dataset.fn;drawStructure()}});

/* ---------- disciplines ---------- */
function drawDisc(){
  const L=D.people.filter(isTA).sort((a,b)=>a.disc.localeCompare(b.disc));
  $("#dtab").innerHTML=`<thead><tr><th>Discipline</th><th>Lead</th><th>Home function</th><th>Solid line to</th></tr></thead><tbody>${
    L.map(p=>`<tr class="click" data-p="${p.id}"><td><b>${esc(p.disc)}</b></td><td>${esc(p.name)}</td><td>${chip(p.fn)}</td><td>${esc(byId[p.reports_to]?.title||"")}</td></tr>`).join("")}</tbody>`;
  const c={};L.forEach(p=>c[p.fn]=(c[p.fn]||0)+1);const mx=Math.max(...Object.values(c));
  $("#dbars").innerHTML=Object.entries(c).sort((a,b)=>b[1]-a[1]).map(([f,n])=>`<div style="margin:8px 0"><div style="display:flex;justify-content:space-between;font-size:14px"><span>${esc(fnBy[f].name)}</span><b>${n}</b></div><div style="height:12px;border-radius:6px;background:${COL[f]};width:${n/mx*100}%"></div></div>`).join("")+
   `<p class="note" style="margin-top:14px">All dotted lines go to ${pbtn(head(fnBy.ENP)||NOBODY)}, VP Engineering &amp; Projects, who chairs the Technical Leadership Council.</p>`;
}

/* ---------- people ---------- */
function opts(el,label,vals){el.innerHTML=`<option value="">${label}</option>`+vals.map(v=>`<option value="${esc(v[0])}">${esc(v[1])}</option>`).join("")}
function drawPeople(){
  const q=$("#q").value.toLowerCase().trim(),f=$("#fFn").value,l=$("#fLoc").value,g=$("#fLvl").value;
  const r=D.people.filter(p=>(!f||p.fn===f)&&(!l||p.location===l)&&(!g||p.level===g)&&(!q||[p.name,p.title,p.disc,p.oms,p.dept].join(" ").toLowerCase().includes(q)));
  $("#pcount").textContent=`${r.length} of ${D.people.length}`;
  $("#ptab").innerHTML=`<thead><tr><th>Name</th><th>Title</th><th>Function</th><th>Location</th><th>Age</th><th>Hired</th></tr></thead><tbody>${
   r.length?r.map(p=>`<tr class="click" data-p="${p.id}"><td><b>${esc(p.name)}</b></td><td>${esc(p.title)}</td><td>${chip(p.fn)}</td><td>${esc(p.location)}</td><td class="num">${p.age}</td><td>${(String(p.hire).match(/\d{4}/)||[""])[0]}</td></tr>`).join(""):`<tr><td colspan="6">No one matches. Clear the search or filters.</td></tr>`}</tbody>`;
}
["#q","#fFn","#fLoc","#fLvl"].forEach(s=>$(s).addEventListener("input",drawPeople));

/* ---------- routing ---------- */
const views=["network","structure","disciplines","people"];
function route(){const v=views.includes(location.hash.slice(1))?location.hash.slice(1):"network";
  views.forEach(x=>{$("#v-"+x).classList.toggle("on",x===v)});document.querySelectorAll("#tabs a").forEach(a=>a.classList.toggle("on",a.dataset.v===v));
  if(v==="structure")drawStructure();if(v==="network")requestAnimationFrame(drawNet);}
addEventListener("hashchange",route);

const SEED=JSON.parse(document.getElementById("seed").textContent);
function init(people,label,checks){
  D={...SEED,people};byId={};kids={};fnBy={};sel=null;
  people.forEach(p=>{byId[p.id]=p});people.forEach(p=>{(kids[p.reports_to]=kids[p.reports_to]||[]).push(p)});
  D.functions.forEach(f=>fnBy[f.code]=f);if(!fnBy[curFn])curFn="ENP";
  const n=c=>people.filter(c).length;
  $("#stats").innerHTML=[[people.length,"people"],[D.functions.length,"functions"],[n(isTA),"discipline leads"],[n(p=>p.gender==="Female"),"women"],[n(p=>/offshore|gulf/i.test(p.location)),"offshore-based"],[n(p=>/land lease/i.test(p.location)),"on land leases"]].map(([a,b])=>`<div><b>${a}</b><span>${b}</span></div>`).join("");
  $("#els").innerHTML=D.elements.map(e=>{const o=byId[e.owner]||NOBODY;return`<div class="el"><b>${e.e}</b> ${esc(e.title)}<div style="margin-top:4px">${o.id?pbtn(o):"Not assigned"}</div><div class="note">${esc(o.title)}</div></div>`}).join("");
  opts($("#fFn"),"All functions",D.functions.map(f=>[f.code,f.name]));
  opts($("#fLoc"),"All locations",[...new Set(people.map(p=>p.location))].sort().map(x=>[x,x]));
  opts($("#fLvl"),"All grades",[...new Set(people.map(p=>p.level))].sort().map(x=>[x,x]));
  $("#src").textContent=label;$("#reset").hidden=!checks;
  $("#checks").innerHTML=checks?(checks.length?`<b>Data check:</b> ${checks.map(esc).join(" · ")}`:"Data check: no problems found."):"";
  drawDisc();drawPeople();side();route();
}
/* ---- CSV ---- */
function parseCSV(t){t=t.replace(/^﻿/,"");const rows=[];let r=[],f="",q=false;
  for(let i=0;i<t.length;i++){const c=t[i];
    if(q){if(c==='"'){if(t[i+1]==='"'){f+='"';i++}else q=false}else f+=c}
    else if(c==='"')q=true;else if(c===","){r.push(f);f=""}else if(c==="\n"||c==="\r"){if(c==="\r"&&t[i+1]==="\n")i++;r.push(f);rows.push(r);r=[];f=""}else f+=c}
  if(f||r.length){r.push(f);rows.push(r)}return rows.filter(x=>x.some(v=>v.trim()))}
const MAP={"Employee ID":"id","Full Name":"name","First Name":"first","Last Name":"last","Gender":"gender","Age":"age","Hire Date":"hire","Job Title":"title","Function Code":"fn","Department":"dept","Grade":"level","Reports To (ID)":"reports_to","Dotted Line To (ID)":"dotted_to","Dotted Line Purpose":"dotted_purpose","Discipline":"disc","OMS Role":"oms","Work Location":"location","Base Degree":"degree","Institution":"institution","Postgraduate / Professional":"postgrad","Job Description":"jd"};
function fromCSV(text,fname){
  const rows=parseCSV(text);if(rows.length<2){$("#checks").textContent="That file has no data rows.";return}
  const hd=rows[0].map(h=>h.trim()),idx={};hd.forEach((h,i)=>{if(MAP[h])idx[MAP[h]]=i});
  const need=["id","fn","reports_to","title"].filter(k=>idx[k]===undefined);
  if(need.length||(idx.name===undefined&&idx.first===undefined)){$("#checks").textContent="This CSV is missing required columns (Employee ID, Full Name, Job Title, Function Code, Reports To (ID)). Save the People tab of the ACE workbook as CSV.";return}
  const g=(r,k)=>idx[k]===undefined?"":(r[idx[k]]||"").trim();
  const people=rows.slice(1).map(r=>{const lv=g(r,"level");return{id:g(r,"id"),name:g(r,"name")||(g(r,"first")+" "+g(r,"last")).trim(),gender:g(r,"gender"),age:g(r,"age"),hire:g(r,"hire"),title:g(r,"title"),fn:g(r,"fn").toUpperCase(),dept:g(r,"dept"),level:lv||"Ungraded",lvl:+((lv.match(/L(\d)/)||[0,9])[1]),reports_to:g(r,"reports_to"),dotted_to:g(r,"dotted_to"),dotted_purpose:g(r,"dotted_purpose"),disc:g(r,"disc"),oms:g(r,"oms"),location:g(r,"location")||"Not stated",degree:g(r,"degree"),institution:g(r,"institution"),postgrad:g(r,"postgrad"),jd:g(r,"jd")}}).filter(p=>p.id);
  const ids=new Set(),dup=[],codes=new Set(SEED.functions.map(f=>f.code));
  people.forEach(p=>{if(ids.has(p.id))dup.push(p.id);ids.add(p.id)});
  const badFn=people.filter(p=>!codes.has(p.fn)),badMgr=people.filter(p=>p.reports_to&&!/board/i.test(p.reports_to)&&!ids.has(p.reports_to)),badDot=people.filter(p=>p.dotted_to&&!ids.has(p.dotted_to));
  const checks=[];
  if(dup.length)checks.push(`${dup.length} duplicate Employee ID(s): ${dup.slice(0,5).join(", ")}`);
  if(badFn.length)checks.push(`${badFn.length} with an unknown Function Code (${badFn.slice(0,3).map(p=>p.name).join(", ")}); they show only in People`);
  if(badMgr.length)checks.push(`${badMgr.length} whose Reports To (ID) is not in the file (${badMgr.slice(0,3).map(p=>p.name).join(", ")})`);
  if(badDot.length)checks.push(`${badDot.length} dotted line(s) to an ID not in the file`);
  init(people,`Showing ${fname}: ${people.length} people`,checks);
}
function readFile(file){if(!file)return;const r=new FileReader();r.onload=()=>fromCSV(String(r.result),file.name);r.readAsText(file)}
$("#csv").addEventListener("change",e=>{readFile(e.target.files[0]);e.target.value=""});
$("#reset").onclick=()=>init(SEED.people,`Built-in data: ${SEED.people.length} people`,null);
addEventListener("dragover",e=>{e.preventDefault();document.body.classList.add("drag")});
addEventListener("dragleave",e=>{if(!e.relatedTarget)document.body.classList.remove("drag")});
addEventListener("drop",e=>{e.preventDefault();document.body.classList.remove("drag");readFile(e.dataTransfer.files[0])});
init(SEED.people,`Built-in data: ${SEED.people.length} people`,null);
}
</script>
</body></html>
