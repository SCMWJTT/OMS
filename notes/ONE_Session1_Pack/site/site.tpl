<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ONE — ACE OMS Library</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* VOICE: the company's own operating library: confident, calm, built for daily use
   IDEA: the OMS wheel on the control-room wall, wired to every controlled document
   PICTURE: a ten-segment wheel counting the sections in the library that answer each element
   COLOUR and TYPE: ONE brand: Paria teal, deep ink, flare orange on sand; Montserrat + Inter
   LAYOUT: brand band with views, then one working surface per view; reader with contents rail */
:root{color-scheme:light dark;
 --bg:light-dark(#f6f1e8,#0f1d26);--paper:light-dark(#ffffff,#152733);--ink:light-dark(#12232e,#e6eef2);--mute:light-dark(#5b6b73,#9fb3bd);
 --line:light-dark(#e3dccf,#29404d);--teal:light-dark(#0e5a6b,#5fc1d1);--flare:#f26b21;--sky:#a7d8e3;--soft:light-dark(#f3efe7,#1b3140);
 --req:light-dark(#fdeee4,#3a2618);--resp:light-dark(#e6f1f3,#173843);--kpi:light-dark(#eef2f8,#1e2a3d);--note:light-dark(#f6f1e8,#24323a);
 --appr:light-dark(#eceff3,#202c38);--rec:light-dark(#f1f1f1,#25303a);--warn:light-dark(#fde7e4,#40201c);--ok:#2f8f5b;--bad:#c0392b;--amb:#c98400}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif;overflow-x:clip}
h1,h2,h3{font-family:Montserrat,Inter,sans-serif;line-height:1.15;margin:0}
a{color:var(--teal)}
button,input,select{font:inherit;font-size:15px;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:8px 12px;min-height:44px}
button{cursor:pointer}:focus-visible{outline:2px solid var(--flare);outline-offset:2px}
.top{background:#12232e;color:#fff;padding:14px max(4vw,16px) 0;position:sticky;top:0;z-index:10}
.bar{display:flex;flex-wrap:wrap;gap:10px 20px;align-items:center;justify-content:space-between}
.mark{display:flex;align-items:center;gap:12px;text-decoration:none;color:#fff}
.mark b{font-family:Montserrat;font-weight:800;font-size:24px;letter-spacing:.5px;line-height:1}
.mark span{display:block;font-size:12.5px;color:var(--sky);line-height:1.2}
.srch{flex:1 1 260px;max-width:440px;display:flex}
.srch input{width:100%;background:#1c3341;border-color:#35505e;color:#fff}
.srch input::placeholder{color:#9fb3bd}
nav{display:flex;gap:2px;overflow-x:auto;margin-top:10px}
nav a{flex:none;color:#c9d8de;text-decoration:none;padding:10px 14px;border-bottom:3px solid transparent;font-weight:500;min-height:44px}
nav a.on{color:#fff;border-bottom-color:var(--flare)}
main{max-width:1320px;margin:0 auto;padding:24px max(4vw,16px) 48px}
.view{display:none}.view.on{display:block}
.card{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:18px}
.note{color:var(--mute);font-size:14px}
.chip{display:inline-block;font-size:12px;font-weight:600;border-radius:999px;padding:2px 10px;white-space:nowrap}
.tag{text-decoration:none;font-size:12px;font-weight:600;border-radius:999px;padding:2px 10px;color:#fff;background:var(--c);white-space:nowrap;border:0;min-height:0;cursor:pointer}
.tag.sec{background:transparent;color:var(--c);box-shadow:inset 0 0 0 1.5px var(--c)}
.pass{background:#e3f3ea;color:#1f6b43}.warn{background:#fdf1d8;color:#8a5b00}.fail{background:#fbe3e0;color:#9b2c20}
.draft{background:#ece7f6;color:#5b3f8f}.appr{background:#e2eff2;color:#0e5a6b}
/* home */
.home{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px;align-items:center}
@media(max-width:900px){.home{grid-template-columns:minmax(0,1fr)}}
#wheel{width:100%;max-width:520px;display:block;margin:0 auto}
#wheel path{cursor:pointer}
.lede h1{font-size:clamp(28px,3.6vw,44px);margin-bottom:10px;text-wrap:balance}
.stats{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;margin:18px 0}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px}
.stat b{font-family:Montserrat;font-size:28px;display:block;line-height:1}
.stat span{font-size:13px;color:var(--mute)}
.ellist{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px;margin-top:26px}
.ellist a{display:flex;gap:10px;align-items:center;text-decoration:none;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-left:6px solid var(--c);border-radius:10px;padding:10px 12px}
.ellist a b{font-family:Montserrat;font-size:20px;color:var(--c);width:28px}
.ellist small{display:block;color:var(--mute)}
/* tables */
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}
th{text-align:left;font-weight:600;color:var(--mute);border-bottom:2px solid var(--line);padding:8px}
td{border-bottom:1px solid var(--line);padding:8px;vertical-align:top}
tr.go{cursor:pointer}tr.go:hover td{background:var(--soft)}
td.n{white-space:nowrap;font-weight:600;color:var(--teal)}
.filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:14px}
.pills{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:12px}
.pills button{min-height:38px;padding:5px 12px;font-size:14px;border-radius:999px}
.pills button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
/* reader */
.reader{display:grid;grid-template-columns:minmax(0,290px) minmax(0,1fr);gap:24px}
@media(max-width:900px){.reader{grid-template-columns:minmax(0,1fr)}.rail{position:static!important;max-height:none!important}}
.rail{position:sticky;top:130px;align-self:start;max-height:calc(100vh - 150px);overflow:auto}
.rail #toc a{display:block;text-decoration:none;color:var(--ink);font-size:13.5px;padding:3px 0 3px 8px;border-left:2px solid transparent}
.rail #toc a.l2{padding-left:20px;color:var(--mute);font-size:13px}
.rail #toc a:hover{color:var(--flare)}
.dhead h1{font-size:clamp(26px,3vw,36px);margin:6px 0 8px}
.dmeta{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:13.5px;color:var(--mute);margin-bottom:10px}
.dmeta b{color:var(--ink);font-weight:600}
#body{max-width:780px}
#body h2{font-size:24px;color:var(--teal);margin:36px 0 6px;scroll-margin-top:140px}
#body h3{font-size:18px;margin:24px 0 4px;scroll-margin-top:140px}
#body h4{font-size:16px;margin:18px 0 4px;color:var(--teal);scroll-margin-top:140px}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:2px 0 10px}
#body p{margin:0 0 10px}
.s{border-left:4px solid var(--b);background:var(--f);padding:8px 12px;border-radius:0 8px 8px 0;margin:0 0 8px!important}
.s small{display:block;font-size:11.5px;font-weight:700;color:var(--b)}
.Requirement{--f:var(--req);--b:var(--flare)}.Responsibility{--f:var(--resp);--b:var(--teal)}.PerformanceIndicator{--f:var(--kpi);--b:#5c7ba6}
.Note{--f:var(--note);--b:var(--sky)}.ApprovalRequirement{--f:var(--appr);--b:#3d5a80}.RecordRequirement{--f:var(--rec);--b:var(--mute)}
.RiskControl{--f:var(--resp);--b:#1e8796}.Warning{--f:var(--warn);--b:var(--bad);font-weight:600}
.ProcedureStep{border:0;background:none;padding:0 0 0 20px}
.DocumentReference{border:0;background:none;padding:0 0 0 18px;color:var(--teal);font-size:15px}
.xref{font-weight:600;text-decoration:none;border-bottom:1.5px solid currentColor}
.xref.planned{color:var(--mute);border-bottom-style:dashed;cursor:help}
ul.bl{margin:0 0 8px;padding-left:22px}
.related{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:12px 0 22px}
.related a{display:block;font-size:13.5px;text-decoration:none;padding:2px 0}
.related .muted{color:var(--mute);font-size:13.5px}
/* element & roles */
.exp{border-top:1px solid var(--line);padding:12px 0;display:grid;grid-template-columns:70px minmax(0,1fr);gap:10px}
.exp>b{font-family:Montserrat;font-size:18px;color:var(--c)}
.hit{display:block;text-decoration:none;color:var(--ink);font-size:14.5px;padding:3px 0 3px 10px;border-left:3px solid transparent}
.hit.pri{border-left-color:var(--flare)}
.hit small{color:var(--mute)}
.gap{color:var(--bad);font-size:13.5px;font-weight:600}
.split{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:20px}
@media(max-width:800px){.split{grid-template-columns:minmax(0,1fr)}}
.rolelist button{display:flex;justify-content:space-between;width:100%;text-align:left;margin:0 0 6px;min-height:40px}
.rolelist button.on{background:var(--ink);color:var(--bg)}
.quote{font-size:14.5px;margin:0 0 8px}
/* map */
.fig{position:relative;height:clamp(460px,72vh,720px)}.fig>svg{position:absolute;inset:0;width:100%;height:100%}
#map g{cursor:pointer}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:13.5px;color:var(--mute);margin-top:8px}
.legend i{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin-right:5px}
/* gateway */
details.gw{border-top:1px solid var(--line);padding:10px 0}
details.gw summary{cursor:pointer;display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center}
.res{font-size:14px;padding:4px 0 4px 12px}
.res i{font-style:normal;font-weight:700;margin-right:8px}
.err{color:var(--bad)}.wrn{color:var(--amb)}.inf{color:var(--mute)}
mark{background:#ffe3cc;color:#12232e;border-radius:3px}
.hide{display:none!important}
footer{max-width:1320px;margin:0 auto;padding:0 max(4vw,16px) 30px;font-size:13px;color:var(--mute)}
@media(max-width:600px){table{font-size:13px}.stack thead{display:none}.stack tr{display:grid;padding-block:10px}.stack td{display:flow-root;border:0;padding:3px 0;padding-inline-start:7.5em;text-align:start}.stack td::before{content:attr(data-l);float:inline-start;width:7em;margin-inline-start:-7.5em;color:var(--mute)}.stack td:empty{display:none}}
</style><script>new MutationObserver(()=>{for(const c of document.querySelectorAll('.stack td:not([data-l])')){let i=0,p=c;while(p=p.previousElementSibling)i+=p.colSpan;c.dataset.l=c.closest('table').rows[0].cells[i]?.textContent||''}}).observe(document,{childList:true,subtree:true})</script></head><body>
<header class="top">
  <div class="bar">
    <a class="mark" href="#home"><svg width="38" height="38" viewBox="-1 -1 2 2" id="mini" aria-hidden="true"></svg><div><b>ONE</b><span>One Management System · Acme Caribbean Energy</span></div></a>
    <form class="srch" id="sf" role="search"><input id="q" type="search" placeholder="Search every document" aria-label="Search every document"></form>
  </div>
  <nav id="nav">
    <a href="#home" data-v="home">Home</a><a href="#library" data-v="library">Library</a><a href="#elements" data-v="elements">Elements</a>
    <a href="#roles" data-v="roles">Roles</a><a href="#map" data-v="map">Document map</a><a href="#gateway" data-v="gateway">Gateway</a>
  </nav>
</header>
<main>
  <section class="view" id="v-home">
    <div class="home">
      <svg id="wheel" viewBox="-130 -130 260 260" role="img" aria-label="OMS wheel: sections in the library addressing each element"></svg>
      <div class="lede">
        <h1>Every approved ACE document, read straight from its Word source and mapped to the OMS</h1>
        <p class="note" style="font-size:16px">Each segment counts the sections that address that element across the library. Select one to see which documents answer each expectation, and where the gaps are.</p>
        <div class="stats" id="stats"></div>
        <p class="note" id="built"></p>
      </div>
    </div>
    <div class="ellist" id="ellist"></div>
  </section>

  <section class="view" id="v-library">
    <div class="filters">
      <select id="fSys" aria-label="System"></select><select id="fType" aria-label="Type"></select>
      <label class="note"><input type="checkbox" id="fDraft" style="min-height:0;width:auto"> Include drafts</label>
      <span class="note" id="lcount"></span>
    </div>
    <div class="card tw"><table class="stack" id="ltab"></table></div>
  </section>

  <section class="view" id="v-doc">
    <div class="reader">
      <aside class="rail card"><details id="railbox" open><summary class="note" style="font-weight:600;margin-bottom:6px;cursor:pointer">Contents</summary><div id="toc"></div></details></aside>
      <article>
        <div class="dhead" id="dhead"></div>
        <div class="pills" id="dfil" role="group" aria-label="Show">
          <button data-f="all" class="on">Everything</button><button data-f="req">Requirements</button><button data-f="resp">Responsibilities</button>
          <button data-f="steps">Steps</button><button data-f="ref">Documents referenced</button><span class="note" id="dcount"></span>
        </div>
        <div id="body"></div>
      </article>
    </div>
  </section>

  <section class="view" id="v-elements"><div id="elbody"></div></section>

  <section class="view" id="v-roles">
    <h2 style="font-size:26px;margin-bottom:6px">Who does what</h2>
    <p class="note" style="margin-top:0">Requirements, responsibilities, approvals, records, risk controls, steps and warnings that name each role, across all approved documents.</p>
    <div class="split"><div class="rolelist" id="rolelist"></div><div class="card" id="rolebody"></div></div>
  </section>

  <section class="view" id="v-map">
    <h2 style="font-size:26px;margin-bottom:6px">How the documents connect</h2>
    <p class="note" style="margin-top:0">Lines show where one document refers to another. Grey dashed circles are documents that are referenced but not yet written; their names appear when you select a document that refers to them. Select a document to see its links.</p>
    <div class="card fig"><svg id="map" role="img" aria-label="Map of document references"></svg></div>
    <div class="legend"><span><i style="background:#0e5a6b"></i>Approved</span><span><i style="background:#7b5bb5"></i>Draft</span><span><i style="background:transparent;border:1.5px dashed #8a9aa2"></i>Planned, not yet in the library</span><span id="mapsel"></span></div>
  </section>

  <section class="view" id="v-gateway">
    <h2 style="font-size:26px;margin-bottom:6px">Publishing gateway</h2>
    <p class="note" style="margin-top:0">The automated check from the OMS Manual, Part D.6, run on every Word file in the repository at build time.</p>
    <div class="stats" id="gstats"></div>
    <div class="card" id="gbody"></div>
  </section>

  <section class="view" id="v-search">
    <h2 style="font-size:26px;margin-bottom:10px" id="stitle">Search</h2>
    <div class="card" id="sbody"></div>
  </section>
</main>
<footer>Acme Caribbean Energy is fictional. ONE demonstration by Cynmark Systems Limited. Element titles and expectation numbering from IOGP Report 510 (2014), © IOGP and IPIECA, used with acknowledgement.</footer>
<script type="application/json" id="data">__DATA__</script>
<script>
{
const D=JSON.parse(document.getElementById("data").textContent);
const EC={1:"#0B4F5E",2:"#0F6B7A",3:"#1E8796",4:"#3AA3AE",5:"#D9480F",6:"#F26B21",7:"#F5923E",8:"#E0962F",9:"#3D5A80",10:"#5C7BA6"};
const $=s=>document.querySelector(s),esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const elOf=t=>+String(t).split(".")[0];
const isDraft=d=>/draft/i.test(d.status);
const byId={};D.docs.forEach(d=>byId[d.id]=d);
const pub=()=>D.docs.filter(d=>!isDraft(d));
const txt=b=>b.k==="h"?b.t:b.k==="tbl"?b.rows.map(r=>r.join(" ")).join(" "):(b.r||[]).map(r=>r[0]).join("");
const statusChip=d=>`<span class="chip ${isDraft(d)?"draft":"appr"}">${isDraft(d)?"Draft "+esc(d.rev):"Rev "+esc(d.rev)}</span>`;
const gwChip=g=>`<span class="chip ${g.verdict}">${g.verdict==="pass"?"Passes":g.verdict==="warn"?g.warnings+" warning"+(g.warnings>1?"s":""):g.errors+" error"+(g.errors>1?"s":"")}</span>`;
const tagChips=v=>v?`<div class="tags">${v.split(",").map(s=>s.trim()).filter(Boolean).map((t,i)=>`<a class="tag ${i?"sec":""}" style="--c:${EC[elOf(t)]}" href="#el-${elOf(t)}" title="${esc((D.exp[t]||"")+" (E"+t+")")}">E${esc(t)}</a>`).join("")}</div>`:"";

/* ---------- index of tags across the library ---------- */
function tagIndex(docs){
  const ex={};docs.forEach(d=>d.secs.forEach(s=>{if(!s.tags)return;s.tags.split(",").map(x=>x.trim()).forEach((t,k)=>{(ex[t]=ex[t]||[]).push({d,s,pri:k===0})})}));
  return ex;
}

/* ---------- wheel ---------- */
function arc(r0,r1,a0,a1){const p=(r,a)=>[r*Math.sin(a*Math.PI/180),-r*Math.cos(a*Math.PI/180)].map(v=>v.toFixed(2)).join(" ");
  return`M${p(r1,a0)}A${r1} ${r1} 0 0 1 ${p(r1,a1)}L${p(r0,a1)}A${r0} ${r0} 0 0 0 ${p(r0,a0)}Z`}
function drawMini(){let m="";for(let i=1;i<=10;i++)m+=`<path d="${arc(.45,.98,(i-1)*36+2,i*36-2)}" fill="${EC[i]}"/>`;$("#mini").innerHTML=m}
function home(){
  const docs=pub(),ex=tagIndex(docs),cnt={},prim={};
  Object.entries(ex).forEach(([t,hs])=>{const e=elOf(t);cnt[e]=(cnt[e]||0)+hs.length;prim[e]=(prim[e]||0)+hs.filter(h=>h.pri).length});
  const covered=Object.keys(D.exp).filter(k=>(ex[k]||[]).some(h=>h.pri)).length;
  const groups=[["LEAD",1,4,"#0E5A6B"],["CONTROL",5,8,"#F26B21"],["LEARN",9,10,"#3D5A80"]];
  let s="";
  groups.forEach(([n,a,b,c])=>{const a0=(a-1)*36+1.5,a1=b*36-1.5;s+=`<path d="${arc(112,117,a0,a1)}" fill="${c}"/>`;
    const mid=((a0+a1)/2)*Math.PI/180,x=124*Math.sin(mid),y=-124*Math.cos(mid);const rot=(a0+a1)/2>90&&(a0+a1)/2<270?(a0+a1)/2+180:(a0+a1)/2;
    s+=`<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle" font-family="Montserrat,Inter" font-weight="800" font-size="9" fill="${c}" transform="rotate(${rot.toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)})">${n}</text>`});
  for(let i=1;i<=10;i++){const a0=(i-1)*36+1,a1=i*36-1,mid=(i-.5)*36*Math.PI/180;
    s+=`<a href="#el-${i}"><path d="${arc(50,108,a0,a1)}" fill="${EC[i]}"><title>${i} ${esc(D.el[i])}: ${cnt[i]||0} sections</title></path></a>`;
    const x=80*Math.sin(mid),y=-80*Math.cos(mid);
    s+=`<text x="${x.toFixed(1)}" y="${(y-4).toFixed(1)}" text-anchor="middle" font-family="Montserrat,Inter" font-weight="800" font-size="20" fill="#fff" pointer-events="none">${i}</text>`;
    s+=`<text x="${x.toFixed(1)}" y="${(y+12).toFixed(1)}" text-anchor="middle" font-family="Inter" font-weight="600" font-size="9.5" fill="#fff" pointer-events="none">${cnt[i]||0}</text>`}
  s+=`<circle r="46" fill="#12232e"/><text y="4" text-anchor="middle" font-family="Montserrat,Inter" font-weight="800" font-size="24" fill="#fff">ONE</text><text y="18" text-anchor="middle" font-family="Inter" font-size="6.2" fill="#a7d8e3">ONE MANAGEMENT SYSTEM</text>`;
  $("#wheel").innerHTML=s;
  const secs=docs.reduce((n,d)=>n+d.secs.length,0),links=Object.values(ex).reduce((n,h)=>n+h.length,0);
  $("#stats").innerHTML=[[docs.length,"approved documents"],[D.docs.length-docs.length,"drafts in progress"],[secs.toLocaleString(),"sections"],[links.toLocaleString(),"OMS tag links"],[`${covered}/54`,"expectations with a primary section"],[D.docs.filter(d=>d.gateway.verdict!=="fail").length+"/"+D.docs.length,"files passing the gateway"]].map(([a,b])=>`<div class="stat"><b>${a}</b><span>${b}</span></div>`).join("");
  $("#built").textContent=`Built ${D.built} from ${D.source}.`;
  $("#ellist").innerHTML=Object.entries(D.el).map(([n,t])=>`<a href="#el-${n}" style="--c:${EC[n]}"><b>${n}</b><span>${esc(t)}<small>${cnt[n]||0} sections · ${prim[n]||0} primary</small></span></a>`).join("");
}

/* ---------- library ---------- */
function opts(el,label,vals){el.innerHTML=`<option value="">${label}</option>`+vals.map(([v,t])=>`<option value="${esc(v)}">${esc(t)}</option>`).join("")}
function library(){
  const sys=$("#fSys").value,ty=$("#fType").value,dr=$("#fDraft").checked;
  const rows=D.docs.filter(d=>(dr||!isDraft(d))&&(!sys||d.system===sys)&&(!ty||d.type===ty)).sort((a,b)=>a.level.localeCompare(b.level)||a.id.localeCompare(b.id));
  $("#lcount").textContent=`${rows.length} document${rows.length===1?"":"s"}`;
  $("#ltab").innerHTML=`<thead><tr><th>Number</th><th>Title</th><th>Type</th><th>System</th><th>Revision</th><th>Effective</th><th>Owner</th><th>Gateway</th></tr></thead><tbody>${
   rows.map(d=>`<tr class="go" data-go="doc-${d.id}"><td class="n">${esc(d.id)}</td><td><b>${esc(d.title)}</b><div class="note">${d.secs.length} sections · ${d.words.toLocaleString()} words</div></td><td>${esc(d.type)}${d.level?` (L${esc(d.level)})`:""}</td><td>${esc(d.systemName)}</td><td>${statusChip(d)}</td><td>${esc(d.eff||"—")}</td><td>${esc((d.owner||"").split(" — ")[0])}</td><td>${gwChip(d.gateway)}</td></tr>`).join("")}</tbody>`;
}
document.addEventListener("click",e=>{const r=e.target.closest("[data-go]");if(r&&!e.target.closest("a"))location.hash=r.dataset.go});
["#fSys","#fType","#fDraft"].forEach(s=>$(s).addEventListener("change",library));

/* ---------- reader ---------- */
const LABEL={Requirement:"Requirement",Responsibility:"Responsibility",ApprovalRequirement:"Approval",RecordRequirement:"Record",RiskControl:"Risk control",Warning:"Warning",PerformanceIndicator:"Measure"};
const FIL={req:["Requirement","ApprovalRequirement","RecordRequirement"],resp:["Responsibility"],steps:["ProcedureStep"],ref:["DocumentReference"]};
function linkRefs(h,self){return h.replace(/\bACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?\b/g,id=>{if(id===self)return id;
  if(byId[id])return`<a class="xref" href="#doc-${id}" title="${esc(byId[id].title)}">${id}</a>`;
  return`<span class="xref planned" title="${esc(D.known[id]?D.known[id]+" — planned, not yet in the library":"Not in the library")}">${id}</span>`})}
function runsHTML(rs,self){return linkRefs(rs.map(([t,b,i])=>{let s=esc(t).replace(/\n/g,"<br>");if(b)s=`<b>${s}</b>`;if(i)s=`<i>${s}</i>`;return s}).join(""),self)}
let curDoc=null,dfilter="all";
function openDoc(id,secIdx){
  const d=byId[id];if(!d){location.hash="library";return}
  if(curDoc!==id){curDoc=id;dfilter="all";document.querySelectorAll("#dfil [data-f]").forEach(b=>b.classList.toggle("on",b.dataset.f==="all"));
    const refBy=D.docs.filter(x=>x.refs.includes(id));
    $("#dhead").innerHTML=`<div class="note" style="font-weight:600;color:var(--flare)">${esc(d.id)} · ${esc(d.type)}${d.level?" · Level "+esc(d.level):""} · ${esc(d.systemName)}</div><h1>${esc(d.title)}</h1>
     ${tagChips(d.titleTags)}<div class="dmeta"><span>${statusChip(d)}</span><span>Effective <b>${esc(d.eff||"not assigned")}</b></span><span>Owner <b>${esc(d.owner)}</b></span><span>Approver <b>${esc(d.approver)}</b></span><span>Gateway ${gwChip(d.gateway)}</span></div>
     <div class="related card"><div><div class="note" style="font-weight:600">This document refers to</div>${d.refs.length?d.refs.map(r=>byId[r]?`<a href="#doc-${r}">${r} ${esc(byId[r].title)}</a>`:`<div class="muted">${r} ${esc(D.known[r]||"")} · planned</div>`).join(""):'<div class="muted">No other documents</div>'}</div>
     <div><div class="note" style="font-weight:600">Referred to by</div>${refBy.length?refBy.map(x=>`<a href="#doc-${x.id}">${x.id} ${esc(x.title)}</a>`).join(""):'<div class="muted">Not referenced yet</div>'}</div></div>`;
    let h="",listOpen=false;
    d.blocks.forEach((b,i)=>{
      if(b.k!=="li"&&listOpen){h+="</ul>";listOpen=false}
      if(b.k==="h"){const L=Math.min(b.l+1,4);h+=`<h${L} id="s-${i}">${esc(b.t)}</h${L}>${tagChips(b.tags)}`;return}
      if(b.k==="tbl"){h+=`<div class="tw" data-k="tbl"><table><thead><tr>${b.rows[0].map(c=>`<th>${linkRefs(esc(c),d.id)}</th>`).join("")}</tr></thead><tbody>${b.rows.slice(1).map(r=>`<tr>${r.map(c=>`<td>${linkRefs(esc(c),d.id)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;return}
      if(b.k==="li"){if(!listOpen){h+='<ul class="bl" data-k="li">';listOpen=true}h+=`<li>${runsHTML(b.r,d.id)}</li>`;return}
      if(b.k==="p"){h+=`<p data-k="p">${runsHTML(b.r,d.id)}</p>`;return}
      const lab=LABEL[b.k];h+=`<p class="s ${esc(b.k)}" data-k="${esc(b.k)}">${lab?`<small>${lab}</small>`:""}${runsHTML(b.r,d.id)}</p>`});
    if(listOpen)h+="</ul>";
    $("#body").innerHTML=h;
    $("#railbox").open=innerWidth>900;
    $("#toc").innerHTML=d.secs.filter(s=>s.l<=2).map(s=>`<a class="l${s.l}" href="#doc-${d.id}-${s.i}">${esc(s.t)}</a>`).join("");
    applyDF();
  }
  if(secIdx!=null){const t=document.getElementById("s-"+secIdx);if(t)requestAnimationFrame(()=>t.scrollIntoView())}else scrollTo(0,0);
}
function applyDF(){const keep=FIL[dfilter];let n=0;
  document.querySelectorAll("#body > *").forEach(el=>{if(!keep){el.classList.remove("hide");return}
    const isH=/^H[2-4]$/.test(el.tagName)||el.classList.contains("tags");const ok=keep.includes(el.dataset.k);if(ok)n++;el.classList.toggle("hide",!(isH||ok))});
  $("#dcount").textContent=keep?`${n} shown`:""}
document.querySelectorAll("#dfil [data-f]").forEach(b=>b.onclick=()=>{dfilter=b.dataset.f;document.querySelectorAll("#dfil [data-f]").forEach(x=>x.classList.toggle("on",x===b));applyDF()});

/* ---------- elements ---------- */
function element(n){
  const docs=pub(),ex=tagIndex(docs);
  const exps=Object.keys(D.exp).filter(k=>elOf(k)===n).sort((a,b)=>+a.split(".")[1]-+b.split(".")[1]);
  const nav=Object.keys(D.el).map(k=>`<a class="tag ${+k===n?"":"sec"}" style="--c:${EC[k]};font-size:14px;padding:4px 12px" href="#el-${k}">${k}</a>`).join(" ");
  $("#elbody").innerHTML=`<div class="tags" style="margin-bottom:14px">${nav}</div><div class="card" style="border-top:8px solid ${EC[n]}">
   <div class="note" style="font-weight:700;color:${EC[n]}">ELEMENT ${n}</div><h2 style="font-size:clamp(24px,3vw,32px);margin:4px 0 12px">${esc(D.el[n])}</h2>
   ${exps.map(k=>{const hs=(ex[k]||[]).sort((a,b)=>b.pri-a.pri);const pri=hs.filter(h=>h.pri),sec=hs.filter(h=>!h.pri);
     return`<div class="exp" style="--c:${EC[n]}"><b>E${k}</b><div><div style="font-weight:600">${esc(D.exp[k])}</div>
     ${pri.length?groupHits(pri,true):`<div class="gap">No section names this as its primary expectation</div>`}
     ${sec.length?`<details><summary class="note" style="cursor:pointer">Also addressed in ${sec.length} other section${sec.length>1?"s":""}</summary>${groupHits(sec,false)}</details>`:""}</div></div>`}).join("")}</div>`;
  scrollTo(0,0);
}
function groupHits(hs,pri){const g={};hs.forEach(h=>(g[h.d.id]=g[h.d.id]||[]).push(h));
  return Object.values(g).sort((a,b)=>b.length-a.length).map(list=>{const d=list[0].d;
    if(list.length===1)return`<a class="hit ${pri?"pri":""}" href="#doc-${d.id}-${list[0].s.i}">${esc(d.title)} <small>· ${esc(list[0].s.t)}</small></a>`;
    return`<details class="hit ${pri?"pri":""}" style="padding-left:10px"><summary style="cursor:pointer">${esc(d.title)} <small>· ${list.length} sections</small></summary>${list.map(h=>`<a class="hit" href="#doc-${d.id}-${h.s.i}"><small>${esc(h.s.t)}</small></a>`).join("")}</details>`}).join("")}
function elementsIndex(){location.replace("#el-1")}

/* ---------- roles ---------- */
let curRole=null;
function roles(){
  const docs=pub(),R={};docs.forEach(d=>Object.entries(d.roles).forEach(([r,is])=>{(R[r]=R[r]||[]).push({d,is})}));
  const list=Object.entries(R).map(([r,v])=>[r,v.reduce((n,x)=>n+x.is.length,0)]).filter(x=>x[1]>=3).sort((a,b)=>b[1]-a[1]);
  if(!curRole||!R[curRole])curRole=list[0][0];
  $("#rolelist").innerHTML=list.map(([r,n])=>`<button data-role="${esc(r)}" class="${r===curRole?"on":""}"><span>${esc(r)}</span><b>${n}</b></button>`).join("");
  const v=R[curRole];
  $("#rolebody").innerHTML=`<h3 style="font-size:20px;margin-bottom:4px">${esc(curRole)}</h3><p class="note" style="margin-top:0">${v.reduce((n,x)=>n+x.is.length,0)} statements in ${v.length} documents</p>`+
   v.sort((a,b)=>b.is.length-a.is.length).map(({d,is})=>`<details ${v.length<=3?"open":""}><summary style="cursor:pointer;padding:6px 0"><b>${esc(d.title)}</b> <span class="note">${esc(d.id)} · ${is.length}</span></summary>${is.map(i=>{const b=d.blocks[i];
     const sec=[...d.secs].reverse().find(s=>s.i<i);return`<p class="s ${esc(b.k)} quote"><small>${LABEL[b.k]||b.k.replace(/([a-z])([A-Z])/g,"$1 $2")} · <a href="#doc-${d.id}-${sec?sec.i:0}">${esc(sec?sec.t:"")}</a></small>${runsHTML(b.r,d.id)}</p>`}).join("")}</details>`).join("");
}
document.addEventListener("click",e=>{const b=e.target.closest("[data-role]");if(b){curRole=b.dataset.role;roles()}});

/* ---------- map ---------- */
let mapSel=null;
function drawMap(){
  const svg=$("#map"),W=svg.clientWidth,H=svg.clientHeight;if(!W)return;
  const lib=D.docs,ids=new Set(lib.map(d=>d.id)),planned=[...new Set(lib.flatMap(d=>d.refs))].filter(r=>!ids.has(r)).sort();
  const cx=W/2,cy=H/2,R1=Math.min(W,H)*0.30,R2=Math.min(W,H)*0.46,small=W<560,pos={};
  lib.forEach((d,i)=>{const a=-Math.PI/2+i*2*Math.PI/lib.length;pos[d.id]=[cx+R1*Math.cos(a),cy+R1*Math.sin(a)]});
  planned.forEach((p,i)=>{const a=-Math.PI/2+(i+.5)*2*Math.PI/planned.length;pos[p]=[cx+R2*Math.cos(a),cy+R2*Math.sin(a)]});
  const inbound={};lib.forEach(d=>d.refs.forEach(r=>inbound[r]=(inbound[r]||0)+1));
  let s="";
  lib.forEach(d=>d.refs.forEach(r=>{if(!pos[r])return;const on=!mapSel||mapSel===d.id||mapSel===r;
    s+=`<line x1="${pos[d.id][0]}" y1="${pos[d.id][1]}" x2="${pos[r][0]}" y2="${pos[r][1]}" stroke="${on&&mapSel?"#f26b21":"currentColor"}" stroke-opacity="${on?(mapSel?.85:.22):.05}" stroke-width="${on&&mapSel?2:1.2}"/>`}));
  const label=(id,x,y,dim)=>{const out=Math.hypot(x-cx,y-cy)>R1*1.3,ang=Math.atan2(y-cy,x-cx);const lx=x+Math.cos(ang)*(out?16:-0),ly=y+Math.sin(ang)*(out?16:0);
    const short=small?id.replace("ACE-",""):id.replace("ACE-","");const anchor=Math.cos(ang)>0.2?"start":Math.cos(ang)<-0.2?"end":"middle";
    return`<text x="${(out?lx:x).toFixed(1)}" y="${(out?ly:y+ (y<cy?-16:24)).toFixed(1)}" text-anchor="${out?anchor:"middle"}" dominant-baseline="middle" font-size="${small?9:11}" font-weight="600" fill="currentColor" opacity="${dim?.35:1}" stroke="var(--paper)" stroke-width="3" paint-order="stroke">${short}</text>`};
  planned.forEach(p=>{const [x,y]=pos[p],on=!mapSel||mapSel===p||(byId[mapSel]&&byId[mapSel].refs.includes(p));
    s+=`<g data-m="${p}"><title>${esc(p+" "+(D.known[p]||"")+" — planned")}</title><circle cx="${x}" cy="${y}" r="${4+Math.min(inbound[p]||0,6)}" fill="var(--paper)" stroke="#8a9aa2" stroke-dasharray="3 2" stroke-width="1.5" opacity="${on?1:.3}"/>${(mapSel&&on&&mapSel!==p)||mapSel===p||(!mapSel&&(inbound[p]||0)>=4&&!small)?label(p,x,y,false):""}</g>`});
  lib.forEach(d=>{const [x,y]=pos[d.id],on=!mapSel||mapSel===d.id||d.refs.includes(mapSel)||(byId[mapSel]&&byId[mapSel].refs.includes(d.id));
    s+=`<g data-m="${d.id}" tabindex="0" role="button" aria-label="${esc(d.id+" "+d.title)}"><title>${esc(d.id+" "+d.title)}</title><circle cx="${x}" cy="${y}" r="${10+Math.min(inbound[d.id]||0,10)}" fill="${isDraft(d)?"#7b5bb5":"#0e5a6b"}" stroke="${mapSel===d.id?"#f26b21":"var(--paper)"}" stroke-width="3" opacity="${on?1:.3}"/>${label(d.id,x,y,!on)}</g>`});
  svg.innerHTML=`<g style="color:var(--ink)">${s}</g>`;
  $("#mapsel").innerHTML=mapSel?(byId[mapSel]?`Selected: <a href="#doc-${mapSel}">${mapSel} ${esc(byId[mapSel].title)}</a> — refers to ${byId[mapSel].refs.length}, referred to by ${inbound[mapSel]||0}`:`Selected: ${mapSel} ${esc(D.known[mapSel]||"")} — planned, referred to by ${inbound[mapSel]||0}`):"";
}
$("#map").addEventListener("click",e=>{const g=e.target.closest("[data-m]");mapSel=g?(mapSel===g.dataset.m?null:g.dataset.m):null;drawMap()});
$("#map").addEventListener("keydown",e=>{if(e.key==="Enter"){const g=e.target.closest("[data-m]");if(g&&byId[g.dataset.m])location.hash="doc-"+g.dataset.m}});
const mapObs=new ResizeObserver(drawMap);mapObs.observe($("#map"));

/* ---------- gateway ---------- */
function gateway(){scrollTo(0,0);
  const c={pass:0,warn:0,fail:0};D.docs.forEach(d=>c[d.gateway.verdict]++);
  $("#gstats").innerHTML=[[D.docs.length,"files checked"],[c.pass,"pass"],[c.warn,"pass with warnings"],[c.fail,"fail"]].map(([a,b])=>`<div class="stat"><b>${a}</b><span>${b}</span></div>`).join("");
  $("#gbody").innerHTML=D.docs.map(d=>`<details class="gw"><summary>${gwChip(d.gateway)}<b>${esc(d.id)}</b><span>${esc(d.title)}</span>${statusChip(d)}<span class="note">${esc(d.file)}</span></summary>
    ${d.gateway.items.length?d.gateway.items.map(([k,t])=>`<div class="res"><i class="${k}">${{err:"Error",wrn:"Warning",inf:"Info"}[k]}</i>${esc(t)}</div>`).join(""):'<div class="res"><i style="color:var(--ok)">OK</i>All checks passed.</div>'}
    <div class="res"><a href="#doc-${d.id}">Open document</a></div></details>`).join("");
}

/* ---------- search ---------- */
function search(q){
  q=q.trim();$("#stitle").textContent=q?`Results for “${q}”`:"Search";if(!q){$("#sbody").innerHTML='<p class="note">Type in the search box above.</p>';return}
  const re=new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"),"gi"),hits=[];
  D.docs.forEach(d=>{let sec=null;d.blocks.forEach((b,i)=>{if(b.k==="h")sec={i,t:b.t};const t=txt(b);if(re.test(t)){re.lastIndex=0;hits.push({d,i,sec,t,k:b.k})}re.lastIndex=0})});
  const show=hits.slice(0,150),byDoc={};show.forEach(h=>(byDoc[h.d.id]=byDoc[h.d.id]||[]).push(h));
  $("#sbody").innerHTML=`<p class="note" style="margin-top:0">${hits.length} match${hits.length===1?"":"es"} in ${new Set(hits.map(h=>h.d.id)).size} documents${hits.length>150?" (first 150 shown)":""}.</p>`+
   Object.values(byDoc).map(hs=>`<h3 style="font-size:17px;margin:16px 0 6px"><a href="#doc-${hs[0].d.id}">${esc(hs[0].d.title)}</a> <span class="note">${esc(hs[0].d.id)}</span></h3>`+hs.map(h=>{
     const pos=h.t.search(re);const a=Math.max(0,pos-80),snip=(a?"…":"")+h.t.slice(a,a+220)+(h.t.length>a+220?"…":"");
     return`<a class="hit" href="#doc-${h.d.id}-${h.k==="h"?h.i:(h.sec?h.sec.i:0)}"><small>${esc(h.sec?h.sec.t:"")} · ${h.k==="h"?"heading":esc(LABEL[h.k]||h.k)}</small><br>${esc(snip).replace(new RegExp(esc(q).replace(/[.*+?^${}()|[\]\\]/g,"\\$&"),"gi"),m=>`<mark>${m}</mark>`)}</a>`}).join("")).join("");
}
let lastQ="";
$("#sf").addEventListener("submit",e=>{e.preventDefault();lastQ=$("#q").value;if(location.hash==="#search")search(lastQ);else location.hash="search"});

/* ---------- routing ---------- */
function show(v){document.querySelectorAll(".view").forEach(x=>x.classList.toggle("on",x.id==="v-"+v));
  const navv=v==="doc"?"library":v==="search"?"":v;document.querySelectorAll("#nav a").forEach(a=>a.classList.toggle("on",a.dataset.v===navv))}
function route(){
  const h=location.hash.slice(1)||"home";let m;
  if((m=h.match(/^doc-(ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(?:-[A-Z]{3})?)(?:-(\d+))?$/))){show("doc");openDoc(m[1],m[2]!=null?+m[2]:null);return}
  if((m=h.match(/^el-(\d+)$/))){show("elements");element(+m[1]);return}
  if(h==="elements"){elementsIndex();return}
  if(h==="library"){show("library");library();return}
  if(h==="roles"){show("roles");roles();return}
  if(h==="map"){show("map");requestAnimationFrame(drawMap);return}
  if(h==="gateway"){show("gateway");gateway();return}
  if(h==="search"){show("search");search(lastQ||$("#q").value);return}
  show("home");home();
}
addEventListener("hashchange",route);
drawMini();
const systems=[...new Set(D.docs.map(d=>d.system))].sort();opts($("#fSys"),"All systems",systems.map(s=>[s,D.systems[s]||s]));
opts($("#fType"),"All types",[...new Set(D.docs.map(d=>d.type))].sort().map(t=>[t,t]));
route();
}
</script>
</body></html>
