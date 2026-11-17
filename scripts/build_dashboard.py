#!/usr/bin/env python3
"""Generate dashboard/index.html — a self-contained, dependency-free dashboard
over the project's datasets. All data embedded inline; vanilla JS + SVG; no CDN;
no innerHTML (DOM built via createElement/textContent only).

Panels:
  1. headline stats
  2. pilot transformation distribution + loss gradient (Phase VI)
  3. Livy I-X event series: type distribution, events by book, trigger×channel heatmap
  4. claim tests T1/T3 summary
  5. causal-claim graph (circular layout from claims.jsonl + ontology)
  6. chapter map coverage
"""
import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard"


def jl(p):
    return [json.loads(l) for l in (ROOT / p).open(encoding="utf-8")]


def build_data():
    ev = jl("extractions/livy_events.jsonl")
    alns = jl("extractions/alignments.jsonl")
    claims = jl("extractions/claims.jsonl")
    cmap = jl("extractions/chapter_map.jsonl")
    onto = json.loads((ROOT / "schema/ontology.json").read_text(encoding="utf-8"))
    sel = json.loads((ROOT / "reports/selection_analysis.json").read_text(encoding="utf-8"))
    tests = json.loads((ROOT / "reports/claim_tests.json").read_text(encoding="utf-8"))

    ev_by_type = collections.Counter(e["event_type"] for e in ev)
    trig_chan = collections.defaultdict(collections.Counter)
    for e in ev:
        trig_chan[e["trigger_domain"]][e["resolution_channel"]] += 1

    used = set()
    edges = []
    for c in claims:
        for cv in c["cause_variables"]:
            for evv in c["effect_variables"]:
                edges.append({"s": cv, "t": evv, "claim": c["claim_id"],
                              "author": c["author"], "type": c["claim_type"],
                              "statement": c["statement"]})
                used.add(cv); used.add(evv)
    nodes = [{"id": v["id"], "label": v["label"].split(" (")[0].split(" — ")[0],
              "domain": v["domain"], "role": v["role"]}
             for v in onto["variables"] if v["id"] in used]

    conf_counts = collections.Counter(c["confidence"] for c in cmap)

    return {
        "stats": {
            "passages": 1349, "chapters": 142, "livy_chapters": 530,
            "events": len(ev), "alignments": len(alns), "claims": len(claims),
            "observations": 26, "datasets": 12,
        },
        "transformations": sel["by_transformation"],
        "loss_gradient": sel["loss_rate_by_dimension"],
        "ev_by_type": dict(ev_by_type.most_common()),
        "trig_chan": {t: dict(c) for t, c in trig_chan.items()},
        "t1": tests["T1_roba_vs_onori"],
        "t3": tests["T3_selection_bias"],
        "graph": {"nodes": nodes, "edges": edges},
        "chapter_conf": dict(conf_counts),
        "events_scatter": [
            {"b": e["book"], "c": int(e["passage_id"].split(":")[3]),
             "t": e["event_type"], "ch": e["resolution_channel"]}
            for e in ev],
    }


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Discourses on Rome — Dashboard</title>
<style>
:root{
  --bg:#f5efe0; --panel:#fffbf0; --ink:#2a2118; --accent:#8b2500;
  --accent2:#1f4e5f; --muted:#8a7a63; --line:#d8cdb4;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);
  font-family:Georgia,'Iowan Old Style','Palatino Linotype',serif;padding:24px;}
h1{font-size:30px;font-variant:small-caps;letter-spacing:1px}
h2{font-size:17px;font-variant:small-caps;letter-spacing:.5px;color:var(--accent);
  border-bottom:1px solid var(--line);padding-bottom:6px;margin-bottom:12px}
.sub{color:var(--muted);font-style:italic;margin:6px 0 18px}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(430px,1fr))}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:6px;
  padding:18px;box-shadow:0 1px 4px rgba(90,70,40,.12)}
.panel.wide{grid-column:1/-1}
.statrow{display:flex;flex-wrap:wrap;gap:14px;margin-bottom:20px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:6px;
  padding:12px 20px;text-align:center;flex:1;min-width:110px}
.stat b{display:block;font-size:26px;color:var(--accent)}
.stat span{font-size:12px;color:var(--muted)}
svg text{font-family:Georgia,serif}
.note{font-size:12px;color:var(--muted);margin-top:8px;line-height:1.5}
.legend{font-size:12px;color:var(--muted);margin-top:6px}
.legend span{display:inline-block;margin-right:12px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px}
#tip{position:fixed;pointer-events:none;background:#2a2118;color:#f5efe0;
  padding:6px 10px;border-radius:4px;font-size:12px;max-width:340px;display:none;
  z-index:10;white-space:pre-line}
a{color:var(--accent2)}
footer{margin-top:28px;color:var(--muted);font-size:12px;font-style:italic}
</style>
</head>
<body>
<h1>Discourses on Rome</h1>
<p class="sub">Reverse-engineering Machiavelli's <i>Discorsi</i> as a historical dataset
 — one-day YOLO build, provided AS IS ·
 <a href="https://github.com/awatson1978/discourses-on-rome">github.com/awatson1978/discourses-on-rome</a></p>
<div id="tip"></div>
<div class="statrow" id="stats"></div>
<div class="grid">
  <div class="panel"><h2>The Loss Gradient</h2>
    <div id="loss"></div>
    <p class="note">Share of information units omitted or abstracted when Machiavelli
    compresses Livy (pilot: 44 aligned units, 3 case studies). He deletes measurement,
    keeps mechanism.</p></div>
  <div class="panel"><h2>Transformation Distribution (pilot)</h2>
    <div id="transforms"></div>
    <p class="note">Fate of each Livy information unit in the Discorsi.
    One unit in five is an <b>addition</b> — Florentine experience, inference, counterfactual.</p></div>
  <div class="panel wide"><h2>Livy I–X Domestic-Political Event Series — 383 events, every chapter coded</h2>
    <div id="scatter"></div>
    <div class="legend" id="scatterleg"></div>
    <p class="note">Every domestic-political event in Livy's first decade, coded independently of
    Machiavelli's citations. x = chapter position within book, row = book. Color = resolution channel.</p></div>
  <div class="panel"><h2>Event Types</h2><div id="types"></div></div>
  <div class="panel"><h2>Trigger Domain × Resolution Channel</h2>
    <div id="heat"></div>
    <p class="note">Row = what the conflict was about; segments = how it resolved.
    The violent row is <b>legal-rights</b>, not property — a domain Machiavelli's
    roba/onori dichotomy does not name.</p></div>
  <div class="panel"><h2>Claim Test: roba vs onori (T1)</h2>
    <div id="t1"></div>
    <p class="note">Machiavelli (Disc I.37): property conflicts turn violent, honors conflicts don't.
    Within Livy I–X both run ~8%. His asymmetry lives entirely in the post-Livian (Gracchan) material.</p></div>
  <div class="panel"><h2>Selection Bias (T3) &amp; Chapter Anchors</h2>
    <div id="t3"></div>
    <p class="note">Left: extraordinary-resolution share of events in Livy chapters Machiavelli
    plausibly cites vs ignores. Right: anchor quality across the 142 Discorsi chapters
    (quote = verbatim Latin quotation detected).</p></div>
  <div class="panel wide"><h2>The Recovered Causal Model — every edge a claim, not a fact</h2>
    <div id="causal"></div>
    <p class="note">Machiavelli's propositions as a graph over the recovered ontology
    (hover edges for the claim). Circular layout; arrow = claimed causal direction;
    red = Machiavelli, blue = Livy's own counterfactual.</p></div>
</div>
<footer>Built 2026-11-16. All quotations in the underlying dataset are machine-verified
verbatim substrings of their cited sources. Caveats: single-coder event series, coded from
an 1857 translation, of a narrative that is itself a late reconstruction. Tests are against
<i>Livy's representation</i>, not Roman reality.</footer>
<script>
const D = __DATA__;
const tip = document.getElementById('tip');
function showTip(e, text){tip.textContent=text;tip.style.display='block';
  tip.style.left=(e.clientX+12)+'px';tip.style.top=(e.clientY+12)+'px';}
function hideTip(){tip.style.display='none';}
function svgEl(w,h){const s=document.createElementNS('http://www.w3.org/2000/svg','svg');
  s.setAttribute('viewBox',`0 0 ${w} ${h}`);s.style.width='100%';return s;}
function el(n,attrs){const e=document.createElementNS('http://www.w3.org/2000/svg',n);
  for(const k in attrs)e.setAttribute(k,attrs[k]);return e;}
function txt(x,y,t,size,fill,anchor){const e=el('text',{x,y,'font-size':size||12,
  fill:fill||'#2a2118','text-anchor':anchor||'start'});e.textContent=t;return e;}

// stats (DOM-built, no innerHTML)
const S=D.stats, statDefs=[['passages','corpus passages'],['events','Livy events'],
 ['alignments','aligned units'],['claims','causal claims'],['observations','observations'],
 ['datasets','dataset hypotheses'],['chapters','Discorsi chapters'],['livy_chapters','Livy chapters']];
const statRow=document.getElementById('stats');
statDefs.forEach(([k,l])=>{
  const d=document.createElement('div');d.className='stat';
  const b=document.createElement('b');b.textContent=S[k];
  const sp=document.createElement('span');sp.textContent=l;
  d.appendChild(b);d.appendChild(sp);statRow.appendChild(d);
});

// loss gradient — horizontal bars
(function(){
  const entries=Object.entries(D.loss_gradient);
  const s=svgEl(430,entries.length*34+10);
  entries.forEach(([dim,v],i)=>{
    const y=i*34+8, w=v*280;
    s.appendChild(txt(4,y+14,dim.replace(/_/g,' '),12,'#5a4a33'));
    s.appendChild(el('rect',{x:150,y:y,width:280,height:20,fill:'#eee5cf',rx:3}));
    s.appendChild(el('rect',{x:150,y:y,width:w,height:20,rx:3,
      fill:v>0.7?'#a03020':v>0.4?'#c7903c':'#5b8c5a'}));
    s.appendChild(txt(150+w+6,y+14,Math.round(v*100)+'%',12,'#8a7a63'));
  });
  document.getElementById('loss').appendChild(s);
})();

// transformations — bars
(function(){
  const order=['omission','addition','preservation','abstraction','reinterpretation'];
  const colors={omission:'#a03020',addition:'#1f4e5f',preservation:'#5b8c5a',
    abstraction:'#c7903c',reinterpretation:'#7a4f9e'};
  const total=Object.values(D.transformations).reduce((a,b)=>a+b,0);
  const s=svgEl(430,180);
  order.forEach((t,i)=>{
    const v=D.transformations[t]||0, h=v/16*130, x=i*84+20;
    s.appendChild(el('rect',{x,y:150-h,width:56,height:h,fill:colors[t],rx:3}));
    s.appendChild(txt(x+28,168,t.slice(0,9),11,'#5a4a33','middle'));
    s.appendChild(txt(x+28,144-h,v+' ('+Math.round(100*v/total)+'%)',11,'#2a2118','middle'));
  });
  document.getElementById('transforms').appendChild(s);
})();

// scatter strip of all events
(function(){
  const chColors={ordinary:'#5b8c5a',extraordinary:'#a03020',mixed:'#c7903c',
    unresolved:'#8a7a63',na:'#cabfa8'};
  const maxC=75, W=920, H=330, rowH=30;
  const s=svgEl(W,H);
  for(let b=1;b<=10;b++){
    const y=(b-1)*rowH+22;
    s.appendChild(txt(4,y+5,'Book '+b,12,'#5a4a33'));
    s.appendChild(el('line',{x1:60,y1:y,x2:W-10,y2:y,stroke:'#eee5cf','stroke-width':14}));
  }
  D.events_scatter.forEach(e=>{
    const y=(e.b-1)*rowH+22, x=60+(e.c/maxC)*(W-80);
    const c=el('circle',{cx:x,cy:y,r:5,fill:chColors[e.ch]||'#999',opacity:.85});
    c.addEventListener('mousemove',ev=>showTip(ev,
      e.t+'\nLivy '+e.b+'.'+e.c+' — '+e.ch));
    c.addEventListener('mouseleave',hideTip);
    s.appendChild(c);
  });
  document.getElementById('scatter').appendChild(s);
  const leg=document.getElementById('scatterleg');
  Object.entries(chColors).forEach(([k,v])=>{
    const sp=document.createElement('span');
    const i=document.createElement('i');i.style.background=v;
    sp.appendChild(i);sp.appendChild(document.createTextNode(k));
    leg.appendChild(sp);
  });
})();

// event types — horizontal bars
(function(){
  const entries=Object.entries(D.ev_by_type);
  const max=entries[0][1];
  const s=svgEl(430,entries.length*23+6);
  entries.forEach(([t,v],i)=>{
    const y=i*23+4,w=v/max*250;
    s.appendChild(txt(4,y+12,t,11.5,'#5a4a33'));
    s.appendChild(el('rect',{x:150,y:y,width:w,height:15,fill:'#1f4e5f',rx:2,opacity:.85}));
    s.appendChild(txt(154+w,y+12,v,11,'#8a7a63'));
  });
  document.getElementById('types').appendChild(s);
})();

// trigger × channel stacked share bars
(function(){
  const chans=['ordinary','mixed','extraordinary','unresolved','na'];
  const chColors={ordinary:'#5b8c5a',extraordinary:'#a03020',mixed:'#c7903c',
    unresolved:'#8a7a63',na:'#cabfa8'};
  const rows=Object.entries(D.trig_chan).map(([t,c])=>
    [t,c,Object.values(c).reduce((a,b)=>a+b,0)]).sort((a,b)=>b[2]-a[2]);
  const s=svgEl(430,rows.length*27+10);
  rows.forEach(([t,c,n],i)=>{
    const y=i*27+6;let x=120;
    s.appendChild(txt(4,y+13,t+' ('+n+')',11.5,'#5a4a33'));
    chans.forEach(ch=>{
      const v=c[ch]||0,w=v/n*260;
      if(v>0){const r=el('rect',{x,y:y,width:w,height:18,fill:chColors[ch]});
        r.addEventListener('mousemove',ev=>showTip(ev,
          t+' × '+ch+': '+v+' events ('+Math.round(100*v/n)+'%)'));
        r.addEventListener('mouseleave',hideTip);
        s.appendChild(r);x+=w;}
    });
  });
  document.getElementById('heat').appendChild(s);
})();

// T1 grouped bars
(function(){
  const t=D.t1, groups=[['property',t.property_domain],
    ['honors-office',t.honors_office_domain],['legal-rights',t.legal_rights_domain]];
  const s=svgEl(430,190);
  groups.forEach(([label,g],i)=>{
    const x=i*140+30, v=g.extraordinary_share, h=v/40*130;
    s.appendChild(el('rect',{x,y:155-h,width:70,height:h,fill:i==2?'#a03020':'#c7903c',rx:3}));
    s.appendChild(txt(x+35,150-h,v+'%',13,'#2a2118','middle'));
    s.appendChild(txt(x+35,172,label,11,'#5a4a33','middle'));
    s.appendChild(txt(x+35,184,'n='+g.n,10,'#8a7a63','middle'));
  });
  document.getElementById('t1').appendChild(s);
})();

// T3: cited vs uncited + chapter map confidence
(function(){
  const s=svgEl(430,190);
  const pairs=[['cited',D.t3.extraordinary_share_cited,'#a03020'],
    ['uncited',D.t3.extraordinary_share_uncited,'#8a7a63']];
  pairs.forEach(([l,v,col],i)=>{
    const x=i*90+30,h=v/20*120;
    s.appendChild(el('rect',{x,y:150-h,width:60,height:h,fill:col,rx:3}));
    s.appendChild(txt(x+30,145-h,v+'%',12,'#2a2118','middle'));
    s.appendChild(txt(x+30,168,l,11,'#5a4a33','middle'));
  });
  const conf=D.chapter_conf, order=['quote','named','name-only','none'];
  const colors={quote:'#5b8c5a',named:'#1f4e5f','name-only':'#c7903c',none:'#cabfa8'};
  let x=240;
  order.forEach(k=>{
    const v=conf[k]||0,w=v/142*170;
    const r=el('rect',{x,y:60,width:w,height:30,fill:colors[k]});
    r.addEventListener('mousemove',ev=>showTip(ev,k+': '+v+' of 142 chapters'));
    r.addEventListener('mouseleave',hideTip);
    s.appendChild(r);x+=w;
  });
  s.appendChild(txt(240,50,'chapter→Livy anchor quality',11,'#5a4a33'));
  s.appendChild(txt(240,110,'quote · named · name-only · none',10,'#8a7a63'));
  document.getElementById('t3').appendChild(s);
})();

// causal graph — circular layout
(function(){
  const W=940,H=560,cx=W/2,cy=H/2,R=220;
  const s=svgEl(W,H);
  const defs=el('defs',{});
  ['#8b2500','#1f4e5f'].forEach((c,i)=>{
    const m=el('marker',{id:'arr'+i,viewBox:'0 0 10 10',refX:9,refY:5,
      markerWidth:7,markerHeight:7,orient:'auto-start-reverse'});
    m.appendChild(el('path',{d:'M 0 0 L 10 5 L 0 10 z',fill:c}));
    defs.appendChild(m);
  });
  s.appendChild(defs);
  const N=D.graph.nodes,pos={};
  N.forEach((n,i)=>{
    const a=2*Math.PI*i/N.length - Math.PI/2;
    pos[n.id]=[cx+R*Math.cos(a),cy+R*Math.sin(a),a];
  });
  D.graph.edges.forEach(e=>{
    const p1=pos[e.s],p2=pos[e.t];if(!p1||!p2)return;
    const mx=(p1[0]+p2[0])/2+(cx-(p1[0]+p2[0])/2)*.45,
          my=(p1[1]+p2[1])/2+(cy-(p1[1]+p2[1])/2)*.45;
    const col=e.author==='livy'?'#1f4e5f':'#8b2500';
    const path=el('path',{d:`M ${p1[0]} ${p1[1]} Q ${mx} ${my} ${p2[0]} ${p2[1]}`,
      fill:'none',stroke:col,'stroke-width':1.6,opacity:.55,
      'marker-end':`url(#arr${e.author==='livy'?1:0})`});
    path.addEventListener('mousemove',ev=>showTip(ev,
      e.claim+' ('+e.author+', '+e.type+')\n'+e.statement));
    path.addEventListener('mouseleave',hideTip);
    path.addEventListener('mouseenter',()=>{path.setAttribute('opacity',1);path.setAttribute('stroke-width',3);});
    path.addEventListener('mouseout',()=>{path.setAttribute('opacity',.55);path.setAttribute('stroke-width',1.6);});
    s.appendChild(path);
  });
  const roleCol={explanatory:'#8b2500',outcome:'#1f4e5f',intervention:'#5b8c5a',condition:'#c7903c'};
  N.forEach(n=>{
    const [x,y,a]=pos[n.id];
    s.appendChild(el('circle',{cx:x,cy:y,r:7,fill:roleCol[n.role]||'#999',
      stroke:'#fffbf0','stroke-width':2}));
    const right=Math.cos(a)>=0;
    s.appendChild(txt(x+(right?11:-11),y+4,
      n.label.length>34?n.label.slice(0,32)+'…':n.label,
      11.5,'#2a2118',right?'start':'end'));
  });
  s.appendChild(txt(16,24,'explanatory (red) · outcome (blue) · intervention (green) · condition (gold)',11,'#8a7a63'));
  document.getElementById('causal').appendChild(s);
})();
</script>
</body>
</html>
"""


def main():
    OUT.mkdir(exist_ok=True)
    data = build_data()
    html = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    (OUT / "index.html").write_text(html, encoding="utf-8")
    print(f"dashboard/index.html written ({len(html)//1024} KB), "
          f"{len(data['events_scatter'])} events, "
          f"{len(data['graph']['nodes'])} graph nodes, "
          f"{len(data['graph']['edges'])} claim edges")


if __name__ == "__main__":
    main()
