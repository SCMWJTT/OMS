<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ACE OMS Manual</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* VOICE: confident company handbook; branded, calm, easy to scan
   IDEA: the OMS wheel poster on the control-room wall, made navigable
   PICTURE: the ten-segment wheel, each segment counting the sections that address it
   COLOUR and TYPE: OMS brand — Paria teal, deep ink, flare orange on sand; Montserrat + Inter
   LAYOUT: brand band, wheel + contents on the left, the manual itself on the right, checks in a drawer */
:root{color-scheme:light dark;
 --bg:light-dark(#f6f1e8,#0f1d26);--paper:light-dark(#ffffff,#152733);--ink:light-dark(#12232e,#e6eef2);--mute:light-dark(#5b6b73,#9fb3bd);
 --line:light-dark(#e3dccf,#29404d);--teal:light-dark(#0e5a6b,#5fc1d1);--flare:#f26b21;--sky:#a7d8e3;
 --req:light-dark(#fdeee4,#3a2618);--resp:light-dark(#e6f1f3,#173843);--kpi:light-dark(#eef2f8,#1e2a3d);--note:light-dark(#f6f1e8,#24323a);
 --appr:light-dark(#eceff3,#202c38);--rec:light-dark(#f1f1f1,#25303a);--warn:light-dark(#fde7e4,#40201c)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif;overflow-x:clip}
h1,h2,h3,.brand{font-family:Montserrat,Inter,sans-serif}
button,input,select{font:inherit;font-size:15px;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:8px 12px;min-height:44px}
button{cursor:pointer}button:focus-visible,a:focus-visible,input:focus-visible,summary:focus-visible{outline:2px solid var(--flare);outline-offset:2px}
.top{background:#12232e;color:#fff;padding:18px max(4vw,16px) 16px}
.top .row{display:flex;flex-wrap:wrap;align-items:center;gap:14px 22px;justify-content:space-between}
.mark{display:flex;align-items:center;gap:12px}
.mark b{font-family:Montserrat;font-weight:800;font-size:26px;letter-spacing:.5px}
.mark span{font-size:13px;color:var(--sky);line-height:1.2}
.doct{font-family:Montserrat;font-weight:700;font-size:clamp(22px,3vw,32px);margin:14px 0 4px;line-height:1.1}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:#c9d8de}
.meta b{color:#fff;font-weight:600}
.actions{display:flex;flex-wrap:wrap;gap:8px}
.actions button,.actions label{background:transparent;color:#fff;border:1px solid #3f5a68;border-radius:8px;padding:8px 14px;min-height:44px;display:inline-flex;align-items:center;cursor:pointer;font-size:15px}
.actions .pri{background:var(--flare);border-color:var(--flare);color:#fff;font-weight:600}
.src{font-size:13px;color:#c9d8de;margin-top:8px}
.wrap{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:28px;padding:24px max(4vw,16px);max-width:1320px;margin:0 auto}
@media(max-width:900px){.wrap{grid-template-columns:minmax(0,1fr)}.side{position:static!important;max-height:none!important}}
.side{position:sticky;top:12px;align-self:start;max-height:calc(100vh - 24px);overflow:auto;padding-right:4px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:14px}
#wheel{width:100%;max-width:300px;display:block;margin:0 auto}
#wheel path{cursor:pointer;transition:opacity .15s}
#elpanel{margin-top:10px;font-size:14px}
#elpanel h3{font-size:16px;margin:0 0 6px}
.ex{border-top:1px solid var(--line);padding:6px 0}
.ex b{color:var(--teal)}
.ex a{display:block;color:var(--ink);text-decoration:none;padding:2px 0 2px 10px;font-size:13.5px}
.ex a.pri{border-left:3px solid var(--flare)}
.ex a:hover{color:var(--flare)}
.empty{color:var(--flare);font-size:13px}
details.toc{margin-top:12px}details.toc summary{font-weight:600;cursor:pointer;padding:6px 0}
.toc a{display:block;text-decoration:none;color:var(--ink);font-size:14px;padding:3px 0 3px 8px;border-left:2px solid transparent}
.toc a.l2{padding-left:20px;font-size:13px;color:var(--mute)}
.toc a.on{border-left-color:var(--flare);color:var(--teal)}
.toc input{width:100%;margin:4px 0 8px}
.filters{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;align-items:center}
.filters button{min-height:38px;padding:6px 12px;font-size:14px;border-radius:999px}
.filters button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.filters span{font-size:13px;color:var(--mute)}
main.card{padding:clamp(18px,3vw,44px)}
#doc{max-width:760px}
#doc h1{font-size:clamp(24px,3vw,30px);color:var(--teal);margin:44px 0 6px;line-height:1.15;scroll-margin-top:16px}
#doc h1:first-child{margin-top:0}
#doc h2{font-size:20px;margin:30px 0 4px;line-height:1.2;scroll-margin-top:16px}
#doc h3{font-size:16.5px;margin:22px 0 4px;color:var(--teal);scroll-margin-top:16px}
#doc .title{font-family:Montserrat;font-size:clamp(30px,4vw,42px);font-weight:800;margin:0 0 6px}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:2px 0 12px}
.tag{font-size:12px;font-weight:600;border-radius:999px;padding:2px 10px;color:#fff;background:var(--c);white-space:nowrap;cursor:pointer;border:0;min-height:0}
.tag.sec{background:transparent;color:var(--c);box-shadow:inset 0 0 0 1.5px var(--c)}
#doc p{margin:0 0 10px}
.s{border-left:4px solid var(--b);background:var(--f);padding:8px 12px;border-radius:0 8px 8px 0;margin:0 0 8px!important}
.s small{display:block;font-size:11.5px;font-weight:700;color:var(--b);margin-bottom:1px}
.s-Requirement{--f:var(--req);--b:var(--flare)}.s-Responsibility{--f:var(--resp);--b:var(--teal)}
.s-PerformanceIndicator{--f:var(--kpi);--b:#5c7ba6}.s-Note{--f:var(--note);--b:var(--sky)}
.s-ApprovalRequirement{--f:var(--appr);--b:#3d5a80}.s-RecordRequirement{--f:var(--rec);--b:var(--mute)}
.s-RiskControl{--f:var(--resp);--b:#1e8796}.s-Warning{--f:var(--warn);--b:#c0392b;font-weight:600}
.s-DocumentReference{background:none;border:0;padding:0 0 0 18px;font-size:14.5px;color:var(--teal);margin:0 0 4px!important}
.s-DocumentReference::before{content:"→ ";margin-left:-16px}
.s-ExternalStandard{background:none;border:0;padding:0;font-size:13.5px;font-style:italic;color:var(--mute)}
.s-ProcedureStep,.s-Definition{background:none;border:0;padding:0 0 0 18px;border-radius:0}
.s-ElementKicker{background:none;border:0;padding:0;color:var(--flare);font-weight:700;font-size:14px}
.kicker{color:var(--flare);font-weight:700;font-size:13px}
.subtitle{color:var(--mute);font-size:17px}
ul.bl{margin:0 0 10px;padding-left:22px}
figure{margin:14px 0 18px;text-align:center}figure img{max-width:min(100%,560px);height:auto}
.cap{font-size:13px;color:var(--mute);font-style:italic;text-align:center;margin-top:-8px!important}
.tw{overflow-x:auto;margin:6px 0 16px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{background:#0e5a6b;color:#fff;text-align:left;padding:7px 9px;font-weight:600}
td{border-bottom:1px solid var(--line);padding:7px 9px;vertical-align:top}
td p{margin:0 0 4px!important}
table.lay td{border:0;padding:0 12px 0 0}table.lay{margin:0}
.hide{display:none!important}
#drawer{position:fixed;top:0;right:0;width:min(460px,100%);height:100%;background:var(--paper);border-left:1px solid var(--line);box-shadow:-10px 0 30px rgba(0,0,0,.18);padding:20px;overflow:auto;transform:translateX(105%);transition:transform .25s;z-index:20}
#drawer.on{transform:none}
#drawer h2{font-size:20px;margin:0 0 8px}
.res{display:flex;gap:10px;padding:8px 0;border-top:1px solid var(--line);font-size:14px}
.res i{font-style:normal;font-weight:700;width:64px;flex:none}
.res .err{color:#c0392b}.res .wrn{color:#d98a00}.res .ok{color:#2f8f5b}.res .inf{color:var(--mute)}
.res a{color:var(--teal)}
.score{font-family:Montserrat;font-size:22px;font-weight:800;margin:6px 0 10px}
.dl{display:grid;grid-template-columns:10em 1fr;gap:4px 10px;font-size:13.5px}
.dl dt{color:var(--mute)}.dl dd{margin:0}
body.drag main{outline:4px dashed var(--flare);outline-offset:6px}
@media(max-width:600px){table{font-size:12.5px}.res i{width:54px}.dl{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){#drawer,#wheel path{transition:none}}
</style></head><body>
<header class="top">
  <div class="row">
    <div class="mark"><svg width="40" height="40" viewBox="-1 -1 2 2" aria-hidden="true" id="mini"></svg><div><b>OMS</b><br><span>One Management System</span></div></div>
    <div class="actions">
      <label class="pri" for="file">Load Word file</label><input id="file" type="file" accept=".docx" hidden>
      <button id="checkBtn">Check document</button>
      <button id="infoBtn">Document details</button>
    </div>
  </div>
  <div class="doct" id="dtitle">Loading…</div>
  <div class="meta" id="dmeta"></div>
  <div class="src" id="src"></div>
</header>

<div class="wrap">
  <aside class="side">
    <div class="card">
      <svg id="wheel" viewBox="-110 -110 220 220" role="img" aria-label="OMS wheel: select an element to see the sections that address it"></svg>
      <div id="elpanel"><p class="note" style="font-size:13.5px;color:var(--mute);margin:6px 0 0">Select an element to see which sections of this document address each expectation. Numbers show how many sections are tagged.</p></div>
    </div>
    <details class="toc card" open><summary>Contents</summary><input id="tq" type="search" placeholder="Find a section" aria-label="Find a section"><nav id="toc"></nav></details>
  </aside>
  <main class="card">
    <div class="filters" role="group" aria-label="Show">
      <button data-f="all" class="on">Everything</button>
      <button data-f="req">Requirements</button>
      <button data-f="resp">Responsibilities</button>
      <button data-f="kpi">Measures</button>
      <button data-f="ref">Documents referenced</button>
      <span id="fcount"></span>
    </div>
    <article id="doc"></article>
  </main>
</div>
<aside id="drawer" aria-live="polite"></aside>

<script>__JSZIP__</script>
<script>
{
const REG=__REGISTRY__;            // expectation number -> ACE topic; element names
const SEED="__DOCX_B64__";
const EC={1:"#0B4F5E",2:"#0F6B7A",3:"#1E8796",4:"#3AA3AE",5:"#D9480F",6:"#F26B21",7:"#F5923E",8:"#E0962F",9:"#3D5A80",10:"#5C7BA6"};
const REQUIRED=["DocumentId","Title","DocumentType","Revision","IssueDate","EffectiveDate","Status","Author","Reviewer","Approver","DocumentOwner","ProcessOwner","PrimaryFunction","Framework","TitleOMSTags","Classification","Applicability","RoleRegister"];
const $=s=>document.querySelector(s),esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
let M=null,selEl=null,filter="all",blobs=[];
const HINT=`<p style="font-size:13.5px;color:var(--mute);margin:6px 0 0">Select an element to see which sections of this document address each expectation. Numbers show how many sections are tagged.</p>`;
const elOf=n=>+String(n).split(".")[0];

/* ---------- read the .docx ---------- */
async function readDocx(buf,name){
  const z=await JSZip.loadAsync(buf);
  const txt=async p=>z.file(p)?await z.file(p).async("string"):null;
  const X=s=>new DOMParser().parseFromString(s,"application/xml");
  const sx=X(await txt("word/styles.xml")||"<x/>"),styles={};
  for(const s of sx.getElementsByTagName("w:style")){const id=s.getAttribute("w:styleId"),n=s.getElementsByTagName("w:name")[0];styles[id]=n?n.getAttribute("w:val"):id}
  const rx=X(await txt("word/_rels/document.xml.rels")||"<x/>"),rels={};
  for(const r of rx.getElementsByTagName("Relationship"))rels[r.getAttribute("Id")]=r.getAttribute("Target");
  blobs.forEach(u=>URL.revokeObjectURL(u));blobs=[];const img={};
  for(const [id,t] of Object.entries(rels)){const p="word/"+t.replace(/^\//,"");if(/media\//.test(p)&&z.file(p)){const b=await z.file(p).async("blob");const u=URL.createObjectURL(b);blobs.push(u);img[id]=u}}
  const meta={};const cx=await txt("docProps/custom.xml");
  if(cx)for(const p of X(cx).getElementsByTagName("property")){meta[p.getAttribute("name").replace(/^ODS\./,"")]=p.textContent.trim()}
  const core=await txt("docProps/core.xml");if(core&&!meta.Title){const t=X(core).getElementsByTagName("dc:title")[0];if(t)meta.Title=t.textContent}
  const body=X(await txt("word/document.xml")).getElementsByTagName("w:body")[0];
  const blocks=[];for(const n of body.childNodes){if(n.nodeName==="w:p")blocks.push(para(n,styles,img));else if(n.nodeName==="w:tbl")blocks.push(tbl(n,styles,img))}
  return{name,meta,blocks};
}
function para(p,styles,img){
  const ps=[...p.childNodes].find(n=>n.nodeName==="w:pPr");let sid=null;
  if(ps){const s=[...ps.childNodes].find(n=>n.nodeName==="w:pStyle");if(s)sid=s.getAttribute("w:val")}
  const o={t:"p",style:sid?(styles[sid]||sid):"Normal",runs:[],bms:[],imgs:[],tag:null,field:false};
  (function walk(n,inSdt){for(const c of n.childNodes){const nm=c.nodeName;
    if(nm==="w:pPr"||nm==="w:rPr")continue;
    if(nm==="w:bookmarkStart"){const b=c.getAttribute("w:name");if(b&&!b.startsWith("_"))o.bms.push(b);continue}
    if(nm==="w:sdt"){const pr=c.getElementsByTagName("w:sdtPr")[0],tg=pr&&pr.getElementsByTagName("w:tag")[0],v=tg?tg.getAttribute("w:val"):"";
      const cont=c.getElementsByTagName("w:sdtContent")[0];const text=cont?[...cont.getElementsByTagName("w:t")].map(t=>t.textContent).join(""):"";
      if(/^ODS\.OMSTags@/.test(v)){o.tag={bm:v.split("@")[1],value:text};continue}
      if(cont)walk(cont,true);continue}
    if(nm==="w:instrText"){o.field=true;continue}
    if(nm==="w:r"){const rp=[...c.childNodes].find(x=>x.nodeName==="w:rPr");const b=rp&&rp.getElementsByTagName("w:b").length&&rp.getElementsByTagName("w:b")[0].getAttribute("w:val")!=="0",i=rp&&rp.getElementsByTagName("w:i").length>0;
      for(const x of c.childNodes){if(x.nodeName==="w:t")o.runs.push({x:x.textContent,b,i});else if(x.nodeName==="w:tab")o.runs.push({x:" "});else if(x.nodeName==="w:br")o.runs.push({x:"\n"});
        else if(x.nodeName==="w:drawing"){const bl=x.getElementsByTagName("a:blip")[0];if(bl){const id=bl.getAttribute("r:embed");if(img[id])o.imgs.push(img[id])}}}
      continue}
    walk(c,inSdt)}})(p,false);
  o.text=o.runs.map(r=>r.x).join("");return o;
}
function tbl(t,styles,img){
  const rows=[];for(const tr of t.childNodes){if(tr.nodeName!=="w:tr")continue;const cells=[];
    for(const tc of tr.childNodes){if(tc.nodeName!=="w:tc")continue;const ps=[];for(const c of tc.childNodes){if(c.nodeName==="w:p")ps.push(para(c,styles,img));else if(c.nodeName==="w:tbl")ps.push(tbl(c,styles,img))}
      const shd=tc.getElementsByTagName("w:shd")[0];cells.push({ps,fill:shd?shd.getAttribute("w:fill"):null})}
    rows.push(cells)}
  return{t:"tbl",rows};
}

/* ---------- model ---------- */
const isHead=s=>/^(title|heading [1-3])$/i.test(s);
const lvl=s=>/^title$/i.test(s)?0:+s.slice(-1);
const odsName=s=>(s.match(/^ODS\.(.+)$/)||[])[1]||(s==="OMS.ElementKicker"?"ElementKicker":null);
const idOf=bm=>bm.replace(/[^A-Za-z0-9-]/g,"-");
function build(raw){
  const tags={},heads=[];
  raw.blocks.forEach(b=>{if(b.t==="p"&&b.tag)tags[b.tag.bm]=b.tag.value});
  let n=0;raw.blocks.forEach(b=>{if(b.t==="p"&&isHead(b.style)){b.id=b.bms[0]?idOf(b.bms[0]):"h"+(++n);b.bm=b.bms[0]||null;b.tags=b.bm&&tags[b.bm]!==undefined?tags[b.bm]:null;heads.push(b)}});
  const byExp={};heads.forEach(h=>{if(!h.tags)return;h.tags.split(",").map(s=>s.trim()).filter(Boolean).forEach((t,i)=>{(byExp[t]=byExp[t]||[]).push({id:h.id,text:h.text,pri:i===0})})});
  return{...raw,tags,heads,byExp};
}

/* ---------- render document ---------- */
const LABEL={Requirement:"Requirement",Responsibility:"Responsibility",ApprovalRequirement:"Approval",RecordRequirement:"Record",RiskControl:"Risk control",Warning:"Warning",PerformanceIndicator:null,Note:null};
const FIL={req:["Requirement","ApprovalRequirement","RecordRequirement"],resp:["Responsibility"],kpi:["PerformanceIndicator"],ref:["DocumentReference"]};
function runsHTML(rs){return rs.map(r=>{let s=esc(r.x).replace(/\n/g,"<br>");if(r.b)s=`<b>${s}</b>`;if(r.i)s=`<i>${s}</i>`;return s}).join("")}
function tagChips(v){if(!v)return"";return`<div class="tags">${v.split(",").map(s=>s.trim()).filter(Boolean).map((t,i)=>`<button class="tag ${i?"sec":""}" style="--c:${EC[elOf(t)]||"#5b6b73"}" data-exp="${esc(t)}" title="${esc(REG.exp[t]?REG.exp[t]+" (E"+t+")":"Not in the OMS register")}">E${esc(t)}</button>`).join("")}</div>`}
function pHTML(b,inCell){
  if(b.t==="tbl")return tblHTML(b);
  if(b.tag||b.field)return"";
  let h="";
  if(b.imgs.length)h+=b.imgs.map(u=>`<figure><img src="${u}" alt=""></figure>`).join("");
  if(!b.text.trim())return h;
  const st=b.style;
  if(isHead(st)&&!inCell){const L=lvl(st);if(L===0)return h+`<h1 class="title" id="${b.id}">${esc(b.text)}</h1>${tagChips(b.tags)}`;
    return h+`<h${L} id="${b.id}">${esc(b.text)}</h${L}>${tagChips(b.tags)}`}
  const od=odsName(st);
  if(od){const lab=LABEL[od];return h+`<p class="s s-${od}" data-k="${od}">${lab?`<small>${lab}</small>`:""}${runsHTML(b.runs)}</p>`}
  if(/^list/i.test(st))return h+`<ul class="bl"><li>${runsHTML(b.runs)}</li></ul>`;
  if(/caption/i.test(st))return h+`<p class="cap">${runsHTML(b.runs)}</p>`;
  if(/kicker/i.test(st))return h+`<p class="kicker">${runsHTML(b.runs)}</p>`;
  if(/subtitle/i.test(st))return h+`<p class="subtitle">${runsHTML(b.runs)}</p>`;
  return h+`<p>${runsHTML(b.runs)}</p>`;
}
function tblHTML(t){
  const layout=t.rows.length===1&&t.rows[0].some(c=>c.ps.some(p=>p.imgs&&p.imgs.length));
  if(layout)return`<table class="lay"><tr>${t.rows[0].map(c=>`<td>${c.ps.map(p=>pHTML(p,true)).join("")}</td>`).join("")}</tr></table>`;
  const head=t.rows[0],rest=t.rows.slice(1);
  const cell=c=>c.ps.map(p=>p.t==="tbl"?tblHTML(p):runsHTML(p.runs||[])).join("<br>");
  const lightFill=f=>f&&f!=="auto"&&!/^(0E5A6B|12232E|FFFFFF|F4F7F8)$/i.test(f);
  return`<div class="tw"><table><thead><tr>${head.map(c=>`<th>${cell(c)}</th>`).join("")}</tr></thead><tbody>${rest.map(r=>`<tr>${r.map(c=>`<td${lightFill(c.fill)?` style="background:#${c.fill};color:#12232e"`:""}>${cell(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}
function render(){
  const md=M.meta;
  $("#dtitle").textContent=md.Title||M.heads[0]?.text||M.name;
  $("#dmeta").innerHTML=[["",md.DocumentId],["Revision",md.Revision],["Status",md.Status],["Effective",md.EffectiveDate],["Owner",md.DocumentOwner]].filter(x=>x[1]).map(([k,v])=>`<span>${k?k+" ":""}<b>${esc(v)}</b></span>`).join("");
  $("#doc").innerHTML=M.blocks.map(b=>pHTML(b,false)).join("");
  $("#toc").innerHTML=M.heads.filter(h=>lvl(h.style)>=1&&lvl(h.style)<=2).map(h=>`<a href="#${h.id}" class="l${lvl(h.style)}">${esc(h.text)}</a>`).join("");
  drawWheel();$("#elpanel").innerHTML=HINT;applyFilter();
}

/* ---------- wheel ---------- */
function arc(r0,r1,a0,a1){const p=(r,a)=>[r*Math.sin(a*Math.PI/180),-r*Math.cos(a*Math.PI/180)].map(v=>v.toFixed(2)).join(" ");
  return`M${p(r1,a0)}A${r1} ${r1} 0 0 1 ${p(r1,a1)}L${p(r0,a1)}A${r0} ${r0} 0 0 0 ${p(r0,a0)}Z`}
function drawWheel(){
  const cnt={};M.heads.forEach(h=>{if(h.tags)new Set(h.tags.split(",").map(s=>elOf(s.trim()))).forEach(e=>cnt[e]=(cnt[e]||0)+1)});
  let s="";
  for(let i=1;i<=10;i++){const a0=(i-1)*36+1,a1=i*36-1,mid=(i-0.5)*36*Math.PI/180,on=!selEl||selEl===i;
    s+=`<path d="${arc(46,selEl===i?104:98,a0,a1)}" fill="${EC[i]}" opacity="${on?1:.25}" data-el="${i}" tabindex="0" role="button" aria-label="Element ${i}: ${esc(REG.el[i])}, ${cnt[i]||0} sections"><title>${i} ${esc(REG.el[i])}</title></path>`;
    s+=`<text x="${(72*Math.sin(mid)).toFixed(1)}" y="${(-72*Math.cos(mid)+2).toFixed(1)}" text-anchor="middle" font-family="Montserrat,Inter" font-weight="800" font-size="17" fill="#fff" pointer-events="none" opacity="${on?1:.6}">${i}</text>`;
    s+=`<text x="${(72*Math.sin(mid)).toFixed(1)}" y="${(-72*Math.cos(mid)+15).toFixed(1)}" text-anchor="middle" font-family="Inter" font-weight="600" font-size="8.5" fill="#fff" pointer-events="none" opacity="${on?.95:.5}">${cnt[i]||0}</text>`}
  s+=`<circle r="42" fill="#12232e"/><text y="2" text-anchor="middle" font-family="Montserrat,Inter" font-weight="800" font-size="20" fill="#fff">OMS</text><text y="13" text-anchor="middle" font-family="Inter" font-size="5.4" fill="#a7d8e3">ONE MANAGEMENT</text><text y="20" text-anchor="middle" font-family="Inter" font-size="5.4" fill="#a7d8e3">SYSTEM</text>`;
  $("#wheel").innerHTML=s;
  let m="";for(let i=1;i<=10;i++){const a0=(i-1)*36+2,a1=i*36-2;m+=`<path d="${arc(.45,.98,a0,a1).replace(/(\d+\.\d+)/g,v=>(+v/1).toFixed(3))}" fill="${EC[i]}"/>`}
  $("#mini").innerHTML=m;
}
function elPanel(){
  const el=$("#elpanel");if(!selEl){return}
  const exps=Object.keys(REG.exp).filter(k=>elOf(k)===selEl).sort((a,b)=>+a.split(".")[1]-+b.split(".")[1]);
  el.innerHTML=`<h3 style="color:${EC[selEl]}">Element ${selEl} — ${esc(REG.el[selEl])}</h3>`+exps.map(k=>{const hs=M.byExp[k]||[];
    return`<div class="ex"><b>E${k}</b> ${esc(REG.exp[k])}${hs.length?hs.map(h=>`<a href="#${h.id}" class="${h.pri?"pri":""}">${esc(h.text)}</a>`).join(""):`<div class="empty">Not addressed in this document</div>`}</div>`}).join("")+
    `<p style="font-size:12.5px;color:var(--mute);margin:8px 0 0">Orange bar: the section's primary tag. <button id="clr" style="min-height:32px;padding:2px 10px;font-size:13px">Show all elements</button></p>`;
  $("#clr").onclick=()=>{selEl=null;drawWheel();$("#elpanel").innerHTML=HINT};
}
$("#wheel").addEventListener("click",e=>{const p=e.target.closest("[data-el]");if(!p)return;selEl=+p.dataset.el;drawWheel();elPanel()});
$("#wheel").addEventListener("keydown",e=>{if(e.key==="Enter"){const p=e.target.closest("[data-el]");if(p){selEl=+p.dataset.el;drawWheel();elPanel()}}});
document.addEventListener("click",e=>{const t=e.target.closest("[data-exp]");if(t){selEl=elOf(t.dataset.exp);drawWheel();elPanel();$("#elpanel").scrollIntoView({block:"nearest"})}});

/* ---------- filters and contents ---------- */
function applyFilter(){
  const keep=FIL[filter];let shown=0;
  document.querySelectorAll("#doc > *").forEach(n=>{
    if(!keep){n.classList.remove("hide");return}
    const isH=/^H[1-3]$/.test(n.tagName)||n.classList.contains("tags");
    const ok=n.dataset&&keep.includes(n.dataset.k);if(ok)shown++;
    n.classList.toggle("hide",!(isH||ok))});
  $("#fcount").textContent=keep?`${shown} shown`:"";
}
document.querySelectorAll("[data-f]").forEach(b=>b.onclick=()=>{filter=b.dataset.f;document.querySelectorAll("[data-f]").forEach(x=>x.classList.toggle("on",x===b));applyFilter()});
$("#tq").addEventListener("input",()=>{const q=$("#tq").value.toLowerCase();document.querySelectorAll("#toc a").forEach(a=>a.classList.toggle("hide",q&&!a.textContent.toLowerCase().includes(q)))});
const io=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){document.querySelectorAll("#toc a").forEach(a=>a.classList.toggle("on",a.getAttribute("href")==="#"+en.target.id))}})},{rootMargin:"0px 0px -75% 0px"});
const watch=()=>{io.disconnect();document.querySelectorAll("#doc h1,#doc h2").forEach(h=>io.observe(h))};

/* ---------- checks (the gateway) ---------- */
function check(){
  const R=[],md=M.meta,bms=new Set(M.heads.map(h=>h.bm).filter(Boolean));
  const fmt=/^\s*\d{1,2}\.\d{1,2}\s*(,\s*\d{1,2}\.\d{1,2}\s*)*$/;
  let nTags=0;
  for(const [bm,v] of Object.entries(M.tags)){nTags++;
    const h=M.heads.find(x=>x.bm===bm),where=h?`<a href="#${h.id}">${esc(h.text)}</a>`:`bookmark “${esc(bm)}”`;
    if(!bms.has(bm))R.push(["err",`OMS tag control points to bookmark “${esc(bm)}”, which is not on a heading.`]);
    if(!v.trim())continue;
    if(!fmt.test(v)){R.push(["err",`Tags “${esc(v)}” at ${where} are not numbers separated by commas.`]);continue}
    const list=v.split(",").map(s=>s.trim());
    const bad=list.filter(t=>!REG.exp[t]);if(bad.length)R.push(["err",`${bad.map(t=>"E"+t).join(", ")} at ${where} ${bad.length>1?"are":"is"} not in the OMS register.`]);
    if(new Set(list).size!==list.length)R.push(["err",`Duplicate tags at ${where}.`]);
  }
  const miss=REQUIRED.filter(k=>!md[k]);
  if(miss.length)R.push(["wrn",`Document properties missing: ${miss.join(", ")}.`]);
  if(md.DocumentId&&!/^ACE-[A-Z]{3}-[A-Z]{3}-\d{3}(-[A-Z]{3})?$/.test(md.DocumentId))R.push(["wrn",`Document number “${esc(md.DocumentId)}” does not follow ACE-AAA-TTT-NNN (Manual Part D.2).`]);
  if(md.Revision){const approved=/approved/i.test(md.Status||"");
    if(/^[A-Z]$/i.test(md.Revision)&&approved)R.push(["err",`Revision ${esc(md.Revision)} is a draft letter but the status is Approved.`]);
    else if(!/^(\d{2}|[A-Z])$/i.test(md.Revision))R.push(["wrn",`Revision “${esc(md.Revision)}” does not follow the ACE format (A, B … for drafts; 01, 02 … for approved issues).`]);}
  const title=M.heads.find(h=>lvl(h.style)===0);
  if(title&&md.TitleOMSTags&&(title.tags||"").replace(/\s/g,"")!==md.TitleOMSTags.replace(/\s/g,""))R.push(["wrn",`Title tags (${esc(title.tags||"none")}) do not match the Title OMS Tags property (${esc(md.TitleOMSTags)}).`]);
  const OKSHALL=["Requirement","Responsibility","ApprovalRequirement","RecordRequirement","RiskControl"];
  const shall=[];M.blocks.forEach(b=>{if(b.t==="p"&&!OKSHALL.includes(odsName(b.style))&&!isHead(b.style)&&/\bshall\b/i.test(b.text))shall.push(`${b.style}: ${b.text}`)});
  if(shall.length)R.push(["wrn",`${shall.length} “shall” statement${shall.length>1?"s are":" is"} in a style that must not contain “shall” (allowed: Requirement, Responsibility, Approval, Record, Risk Control), for example: “${esc(shall[0].slice(0,110))}…”`]);
  const untagged=M.heads.filter(h=>lvl(h.style)>=1&&!h.tags).length;
  R.push(["inf",`${untagged} heading${untagged===1?"":"s"} without OMS tags (allowed).`]);
  const covered=Object.keys(REG.exp).filter(k=>M.byExp[k]).length;
  R.push(["inf",`${nTags} tag controls; ${covered} of ${Object.keys(REG.exp).length} expectations addressed.`]);
  const e=R.filter(r=>r[0]==="err").length,w=R.filter(r=>r[0]==="wrn").length;
  const verdict=e?`Fails the gateway: ${e} error${e>1?"s":""}, ${w} warning${w!==1?"s":""}`:w?`Passes with ${w} warning${w>1?"s":""}`:"Passes the gateway";
  if(!e&&!w)R.unshift(["ok","All tag controls, numbers and properties are valid."]);
  $("#drawer").innerHTML=`<button id="cl" style="float:right">Close</button><h2>Document check</h2><p style="font-size:13.5px;color:var(--mute)">The automated gateway check from the OMS Manual, Part D.6, run on ${esc(M.name)}.</p>
   <div class="score" style="color:${e?"#c0392b":w?"#d98a00":"#2f8f5b"}">${verdict}</div>${R.map(([k,t])=>`<div class="res"><i class="${k}">${{err:"Error",wrn:"Warning",inf:"Info",ok:"OK"}[k]}</i><span>${t}</span></div>`).join("")}`;
  openDrawer();
}
function details(){
  const md=M.meta;$("#drawer").innerHTML=`<button id="cl" style="float:right">Close</button><h2>Document details</h2><p style="font-size:13.5px;color:var(--mute)">Read from the Word file's document properties.</p>
   <dl class="dl">${Object.keys(md).length?Object.entries(md).map(([k,v])=>`<dt>${esc(k.replace(/([a-z])([A-Z])/g,"$1 $2"))}</dt><dd>${esc(v)}</dd>`).join(""):"<dd>No document properties found.</dd>"}</dl>`;openDrawer()}
function openDrawer(){$("#drawer").classList.add("on");$("#cl").onclick=()=>$("#drawer").classList.remove("on");$("#cl").focus()}
$("#checkBtn").onclick=check;$("#infoBtn").onclick=details;
document.addEventListener("keydown",e=>{if(e.key==="Escape")$("#drawer").classList.remove("on")});
document.addEventListener("click",e=>{const a=e.target.closest("#drawer a[href^='#']");if(a&&innerWidth<700)$("#drawer").classList.remove("on")});

/* ---------- load ---------- */
async function load(buf,name,label){
  try{const raw=await readDocx(buf,name);M=build(raw);selEl=null;render();watch();$("#src").textContent=label;
    if(location.hash){const t=document.getElementById(location.hash.slice(1));if(t)t.scrollIntoView()}}
  catch(err){$("#src").textContent=`Could not read ${name}: it may not be a Word .docx file.`}
}
$("#file").addEventListener("change",e=>{const f=e.target.files[0];if(f)f.arrayBuffer().then(b=>load(b,f.name,`Showing ${f.name}, loaded in this browser. Nothing is uploaded or saved.`));e.target.value=""});
addEventListener("dragover",e=>{e.preventDefault();document.body.classList.add("drag")});
addEventListener("dragleave",e=>{if(!e.relatedTarget)document.body.classList.remove("drag")});
addEventListener("drop",e=>{e.preventDefault();document.body.classList.remove("drag");const f=e.dataTransfer.files[0];if(f)f.arrayBuffer().then(b=>load(b,f.name,`Showing ${f.name}, loaded in this browser. Nothing is uploaded or saved.`))});
const bin=Uint8Array.from(atob(SEED),c=>c.charCodeAt(0));
load(bin.buffer,"ACE-OMS-MAN-001_OMS_Manual_Rev03.docx","Showing the built-in copy of the approved manual. Edit the Word file and load it here to see your changes.");
}
</script>
</body></html>
