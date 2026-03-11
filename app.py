"""
Talking Rabbitt — AI Construction Intelligence
Gemini AI + Charts + Voice Output
Simple, reliable, fully working.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai
import json, io, re

# ── API KEY ─────────────────────────────────────
GOOGLE_API_KEY = "AIzaSyCkRKt76wHxF773AqAv9T0tvc6yhkZyIzQ"

st.set_page_config(page_title="Rabbitt AI", page_icon="🐇",
                   layout="wide", initial_sidebar_state="expanded")

# ── SESSION STATE ────────────────────────────────
if "chat"     not in st.session_state: st.session_state.chat     = []
if "df"       not in st.session_state: st.session_state.df       = None
if "pending_q" not in st.session_state: st.session_state.pending_q = ""

# ════════════════════════════════════════════════
# CSS — Deep Space Glassmorphism
# ════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@500;700;800;900&family=Instrument+Sans:wght@300;400;500&display=swap');

:root {
    --bg:#03040A; --bg1:#080B12; --bg2:#0E1120;
    --g1:rgba(255,255,255,0.04); --g2:rgba(255,255,255,0.07);
    --bdr:rgba(255,255,255,0.07); --bdra:rgba(139,92,246,0.35);
    --v:#8B5CF6; --c:#06B6D4; --pk:#F472B6; --gr:#34D399; --rd:#F87171;
    --tx:#E2E8F0; --mu:#64748B;
}
html,body,[class*="css"],.stApp {
    background:var(--bg) !important; color:var(--tx) !important;
    font-family:'Instrument Sans',sans-serif !important;
}
.stApp::before {
    content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
    background:
        radial-gradient(ellipse 65% 45% at 10% 15%,rgba(139,92,246,.15) 0%,transparent 60%),
        radial-gradient(ellipse 55% 40% at 90% 80%,rgba(6,182,212,.11) 0%,transparent 58%),
        radial-gradient(ellipse 45% 50% at 55% 5%,rgba(244,114,182,.08) 0%,transparent 52%);
    animation:aurora 18s ease-in-out infinite alternate;
}
@keyframes aurora {
    0%  {transform:scale(1);opacity:1}
    50% {transform:scale(1.05) rotate(1deg);opacity:.87}
    100%{transform:scale(1.02) rotate(-.5deg);opacity:.95}
}
.orbs{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;}
.orb{position:absolute;border-radius:50%;filter:blur(70px);opacity:.18;}
.o1{width:380px;height:380px;background:radial-gradient(circle,#8B5CF6,transparent 70%);top:-100px;left:-100px;animation:o1 22s ease-in-out infinite;}
.o2{width:300px;height:300px;background:radial-gradient(circle,#06B6D4,transparent 70%);bottom:-80px;right:-80px;animation:o2 28s ease-in-out infinite;}
.o3{width:200px;height:200px;background:radial-gradient(circle,#F472B6,transparent 70%);top:40%;right:8%;animation:o3 32s ease-in-out infinite;}
@keyframes o1{0%,100%{transform:translate(0,0)}35%{transform:translate(70px,100px)}70%{transform:translate(30px,150px)}}
@keyframes o2{0%,100%{transform:translate(0,0)}30%{transform:translate(-80px,-70px)}65%{transform:translate(-40px,-130px)}}
@keyframes o3{0%,100%{transform:translate(0,0)}45%{transform:translate(-60px,80px)}75%{transform:translate(40px,40px)}}

section[data-testid="stSidebar"] {
    background:rgba(3,4,10,.94) !important;
    backdrop-filter:blur(24px) !important;
    border-right:1px solid var(--bdr) !important;
}
section[data-testid="stSidebar"] > div{padding-top:0 !important;}
.main .block-container{background:transparent !important;padding:1.5rem 2rem 4rem !important;position:relative;z-index:1;}

/* Glass card */
.gc{background:var(--g1);backdrop-filter:blur(20px);border:1px solid var(--bdr);
    border-radius:18px;padding:1.4rem;position:relative;overflow:hidden;
    transition:border-color .3s,transform .3s,box-shadow .3s;}
.gc::before{content:'';position:absolute;inset:0;
    background:linear-gradient(135deg,rgba(255,255,255,.04) 0%,transparent 55%);
    pointer-events:none;border-radius:inherit;}
.gc:hover{border-color:rgba(139,92,246,.3);transform:translateY(-2px);
          box-shadow:0 8px 36px rgba(139,92,246,.1);}

/* KPI */
.kgrid{display:grid;grid-template-columns:repeat(6,1fr);gap:.6rem;margin-bottom:1.6rem;}
.kt{background:var(--g1);backdrop-filter:blur(14px);border:1px solid var(--bdr);
    border-radius:14px;padding:.95rem .7rem;text-align:center;position:relative;overflow:hidden;
    transition:all .3s cubic-bezier(.34,1.56,.64,1);}
.kt::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,var(--v),var(--c),transparent);opacity:0;transition:opacity .3s;}
.kt:hover{border-color:rgba(139,92,246,.4);background:var(--g2);transform:translateY(-3px) scale(1.02);box-shadow:0 12px 28px rgba(0,0,0,.5);}
.kt:hover::after{opacity:1;}
.kv{font-family:'Cabinet Grotesk',sans-serif;font-size:1.6rem;font-weight:900;
    color:#fff;line-height:1;margin-bottom:.28rem;letter-spacing:-.03em;}
.kl{font-size:.58rem;font-weight:500;color:var(--mu);text-transform:uppercase;letter-spacing:.12em;}

/* Chat bubbles */
.uw{display:flex;justify-content:flex-end;margin:.7rem 0 .25rem;}
.ub{max-width:70%;background:linear-gradient(135deg,rgba(139,92,246,.18),rgba(6,182,212,.1));
    backdrop-filter:blur(12px);border:1px solid rgba(139,92,246,.28);
    border-radius:18px 18px 4px 18px;padding:.8rem 1.1rem;font-size:.9rem;
    color:var(--tx);line-height:1.65;}
.aw{display:flex;justify-content:flex-start;gap:.55rem;margin:.25rem 0 .7rem;align-items:flex-start;}
.ab{max-width:82%;background:var(--g1);backdrop-filter:blur(16px);border:1px solid var(--bdr);
    border-radius:4px 18px 18px 18px;padding:.8rem 1.1rem;font-size:.9rem;color:#CBD5E1;line-height:1.65;}
.bl{font-size:.57rem;font-weight:600;letter-spacing:.13em;text-transform:uppercase;margin-bottom:.28rem;}
.blu{color:#A78BFA;text-align:right;}
.bla{color:#22D3EE;}
.aibadge{width:30px;height:30px;flex-shrink:0;margin-top:2px;
    background:linear-gradient(135deg,#8B5CF6,#06B6D4);border-radius:9px;
    display:flex;align-items:center;justify-content:center;font-size:.9rem;
    box-shadow:0 0 14px rgba(139,92,246,.45);animation:bp 3s ease-in-out infinite;}
@keyframes bp{0%,100%{box-shadow:0 0 14px rgba(139,92,246,.45)}50%{box-shadow:0 0 24px rgba(6,182,212,.6)}}

/* Inputs */
.stTextInput>div>div>input{
    background:rgba(255,255,255,.05) !important;backdrop-filter:blur(12px) !important;
    border:1px solid var(--bdr) !important;border-radius:12px !important;
    color:var(--tx) !important;font-family:'Instrument Sans',sans-serif !important;
    font-size:.92rem !important;padding:.75rem 1rem !important;
    transition:border-color .25s,box-shadow .25s !important;
}
.stTextInput>div>div>input:focus{
    border-color:rgba(139,92,246,.55) !important;
    box-shadow:0 0 0 3px rgba(139,92,246,.09),0 0 20px rgba(139,92,246,.1) !important;
}
.stTextInput>div>div>input::placeholder{color:#1E293B !important;}

/* Buttons */
.stButton>button{
    background:linear-gradient(135deg,#8B5CF6,#06B6D4) !important;
    color:#fff !important;font-family:'Cabinet Grotesk',sans-serif !important;
    font-weight:800 !important;font-size:.82rem !important;letter-spacing:.04em !important;
    border:none !important;border-radius:11px !important;
    transition:all .25s cubic-bezier(.34,1.56,.64,1) !important;
    box-shadow:0 4px 18px rgba(139,92,246,.3) !important;
}
.stButton>button:hover{transform:translateY(-2px) scale(1.03) !important;
    box-shadow:0 8px 28px rgba(139,92,246,.5) !important;}

section[data-testid="stSidebar"] .stButton>button{
    background:var(--g1) !important;color:#94A3B8 !important;
    border:1px solid var(--bdr) !important;box-shadow:none !important;
    font-family:'Instrument Sans',sans-serif !important;font-weight:400 !important;
    font-size:.78rem !important;text-align:left !important;transform:none !important;letter-spacing:0 !important;
}
section[data-testid="stSidebar"] .stButton>button:hover{
    background:var(--g2) !important;border-color:rgba(139,92,246,.3) !important;
    color:#C4B5FD !important;box-shadow:none !important;transform:none !important;
}
.stDownloadButton>button{
    background:var(--g1) !important;color:#22D3EE !important;
    border:1px solid rgba(6,182,212,.25) !important;font-family:'Instrument Sans',sans-serif !important;
    font-weight:500 !important;border-radius:11px !important;box-shadow:none !important;
}
.stDownloadButton>button:hover{background:rgba(6,182,212,.07) !important;
    border-color:rgba(6,182,212,.5) !important;box-shadow:0 0 18px rgba(6,182,212,.15) !important;}

div[data-testid="stFileUploader"]{
    background:var(--g1) !important;backdrop-filter:blur(12px) !important;
    border:1px dashed rgba(139,92,246,.3) !important;border-radius:14px !important;padding:.75rem !important;
}
div[data-testid="stFileUploader"]:hover{border-color:rgba(139,92,246,.6) !important;}
.stDataFrame{border-radius:12px !important;overflow:hidden !important;border:1px solid var(--bdr) !important;}
.stSpinner>div{border-top-color:#8B5CF6 !important;}
.stSuccess{background:rgba(52,211,153,.07) !important;border-color:rgba(52,211,153,.25) !important;border-radius:11px !important;}
.stError{background:rgba(248,113,113,.07) !important;border-color:rgba(248,113,113,.25) !important;border-radius:11px !important;}
::-webkit-scrollbar{width:3px;height:3px;}
::-webkit-scrollbar-thumb{background:rgba(139,92,246,.3);border-radius:3px;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none !important;}
</style>

<div class="orbs">
  <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════
# DATA HELPERS
# ════════════════════════════════════════════════
def fmt_crore(v): return f"₹{v/1e7:.1f} Cr"

def generate_sample_csv():
    data = {
        "Project":  ["Skyline One"]*3+["The Pinnacle"]*2+["Nexus Park"]*3+["Horizon West"]*4+["The Arbour"]*2,
        "Tower":    ["T1","T2","T3","PA","PB","NX1","NX2","NX3","HW1","HW2","HW3","HW4","AR1","AR2"],
        "Slab_Percent":    [96,88,72,99,91,55,63,44,93,78,85,97,34,61],
        "Revenue_Pending": [420000000,385000000,297500000,850000000,762000000,
                            183000000,221000000,146000000,315000000,278000000,
                            332000000,291000000,94000000,167000000],
        "Days_Delayed":    [12,0,45,5,0,90,60,120,8,30,15,0,180,75],
        "Regulatory_Status":["Approved","Approved","Pending NOC","OC Received","Approved",
                              "Pending NOC","Approved","Pending NOC","Approved","OC Received",
                              "Approved","OC Received","Pending NOC","Approved"],
    }
    buf = io.BytesIO()
    pd.DataFrame(data).to_csv(buf, index=False)
    return buf.getvalue()

def df_summary(df):
    return json.dumps({
        "total_towers": len(df),
        "projects": df["Project"].unique().tolist(),
        "avg_slab_percent": round(df["Slab_Percent"].mean(),1),
        "total_revenue_crore": round(df["Revenue_Pending"].sum()/1e7,1),
        "towers_above_90pct": df[df["Slab_Percent"]>90][["Tower","Project","Slab_Percent","Revenue_Pending"]].to_dict("records"),
        "towers_delayed": df[df["Days_Delayed"]>0][["Tower","Project","Days_Delayed"]].to_dict("records"),
        "regulatory_breakdown": df["Regulatory_Status"].value_counts().to_dict(),
        "all_data": df.to_dict("records"),
    }, indent=2)


# ════════════════════════════════════════════════
# CHART BUILDER
# ════════════════════════════════════════════════
CHART_STYLE = dict(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#64748B",family="Instrument Sans"),
    title_font=dict(size=14,color="#A78BFA",family="Cabinet Grotesk"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(color="#64748B"),zeroline=False,showline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(color="#64748B"),zeroline=False,showline=False),
    margin=dict(t=48,l=8,r=8,b=36),
    hoverlabel=dict(bgcolor="#0F172A",bordercolor="#8B5CF6",font_color="#E2E8F0"),
    legend=dict(font=dict(color="#64748B")),
)

def build_chart(cd):
    t  = cd.get("type","bar")
    xs = cd.get("x",[])
    ys = cd.get("y",[])
    title = cd.get("title","")
    labs  = cd.get("labels",{})

    if t == "bar":
        fig = go.Figure(go.Bar(
            x=xs, y=ys,
            marker=dict(color=ys,colorscale=[[0,"#1E1B4B"],[.5,"#8B5CF6"],[1,"#06B6D4"]],showscale=False),
            text=[str(round(v,1)) if isinstance(v,float) else str(v) for v in ys],
            textposition="outside", textfont=dict(color="#94A3B8",size=11),
        ))
        fig.update_layout(title=title,xaxis_title=labs.get("x",""),yaxis_title=labs.get("y",""),**CHART_STYLE)

    elif t == "pie":
        fig = go.Figure(go.Pie(
            labels=xs, values=ys, hole=.52,
            marker=dict(colors=["#8B5CF6","#06B6D4","#F472B6","#34D399","#FBBF24"],
                        line=dict(color="#03040A",width=2)),
            textfont=dict(color="#E2E8F0",size=12),
        ))
        fig.update_layout(title=title,**CHART_STYLE)

    elif t == "scatter":
        fig = go.Figure(go.Scatter(
            x=xs, y=ys, mode="markers+text", text=xs,
            textposition="top center", textfont=dict(color="#94A3B8",size=10),
            marker=dict(size=14,color="#8B5CF6",line=dict(color="#06B6D4",width=1.5),opacity=.85),
        ))
        fig.update_layout(title=title,xaxis_title=labs.get("x",""),yaxis_title=labs.get("y",""),**CHART_STYLE)

    else:  # line
        fig = go.Figure(go.Scatter(
            x=xs, y=ys, mode="lines+markers",
            line=dict(color="#8B5CF6",width=2.5),
            marker=dict(size=8,color="#06B6D4"),
            fill="tozeroy", fillcolor="rgba(139,92,246,0.07)",
        ))
        fig.update_layout(title=title,xaxis_title=labs.get("x",""),yaxis_title=labs.get("y",""),**CHART_STYLE)

    return fig


# ════════════════════════════════════════════════
# GEMINI AI
# ════════════════════════════════════════════════
def ask_ai(df, question, history):
    data_ctx = df_summary(df)

    # Build full prompt — prepend system as first user message (works across all Gemini versions)
    system_msg = f"""You are Rabbitt AI — a sharp construction portfolio analyst.

PORTFOLIO DATA (JSON):
{data_ctx}

REPLY RULES — follow every rule exactly:
1. Answer in plain markdown. Use **bold** for key numbers.
2. Express money as Crore: e.g. ₹42.0 Cr  (1 Cr = 10,000,000)
3. ALWAYS include a chart. At the very END of your reply put exactly this block:
<CHART>{{"type":"bar","title":"Your Title","x":["A","B","C"],"y":[10,20,30],"labels":{{"x":"X Label","y":"Y Label"}}}}</CHART>
   Replace the example values with real data. type can be bar/pie/line/scatter.
   For pie charts: x = category names, y = numeric values.
4. Answer in under 100 words (before the chart block).
5. Be direct, confident, insightful."""

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Build messages — system as first turn
    messages = [{"role":"user","parts":[system_msg]},
                {"role":"model","parts":["Understood. I am Rabbitt AI. Ready to analyse your construction data."]}]

    for h in history[-6:]:
        role = "model" if h["role"] == "assistant" else "user"
        messages.append({"role": role, "parts": [h["content"]]})
    messages.append({"role":"user","parts":[question]})

    response = model.generate_content(messages)
    raw = response.text

    # Parse <CHART> block
    fig = None
    answer = raw
    if "<CHART>" in raw and "</CHART>" in raw:
        try:
            chart_str  = raw.split("<CHART>")[1].split("</CHART>")[0].strip()
            chart_data = json.loads(chart_str)
            fig        = build_chart(chart_data)
            answer     = raw.split("<CHART>")[0].strip()
        except Exception:
            pass  # keep raw answer, no chart

    return answer, fig


# ════════════════════════════════════════════════
# VOICE OUTPUT (TTS) — injected as plain HTML
# ════════════════════════════════════════════════
def speak(text, key):
    """Auto-speak AI response via browser TTS."""
    clean = re.sub(r'[*#`_~]', '', text)
    clean = re.sub(r'\n+', ' ', clean).strip()
    clean = clean[:600].replace("'","\\'").replace('"','\\"').replace('\\','')
    st.markdown(f"""
    <script>
    (function(){{
      var k='spk_{key}';
      if(sessionStorage.getItem(k)) return;
      sessionStorage.setItem(k,'1');
      function go(){{
        window.speechSynthesis.cancel();
        var u=new SpeechSynthesisUtterance('{clean}');
        u.rate=1.05; u.pitch=1; u.volume=1;
        var vs=speechSynthesis.getVoices();
        var pv=vs.find(v=>v.name.includes('Google')&&v.lang.startsWith('en'))
              ||vs.find(v=>v.lang.startsWith('en-US'))||vs[0];
        if(pv) u.voice=pv;
        speechSynthesis.speak(u);
      }}
      speechSynthesis.getVoices().length ? go() : (speechSynthesis.onvoiceschanged=go);
    }})();
    </script>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════
# VOICE INPUT — mic button using Web Speech API
# Transcript is written into a real st.text_input
# via a tiny JS trick that works reliably in Streamlit
# ════════════════════════════════════════════════
def mic_button():
    """Renders an animated mic button. Transcript is appended to query box via JS."""
    st.markdown("""
    <style>
    #micWrap { display:inline-flex; align-items:center; gap:8px; }
    #micBtn2 {
        width:44px;height:44px;border-radius:12px;border:none;cursor:pointer;
        background:linear-gradient(135deg,#8B5CF6,#06B6D4);
        font-size:18px;color:white;
        box-shadow:0 4px 16px rgba(139,92,246,.4);
        transition:all .2s;display:flex;align-items:center;justify-content:center;
    }
    #micBtn2:hover{transform:scale(1.1);box-shadow:0 6px 22px rgba(139,92,246,.65);}
    #micBtn2.on{background:linear-gradient(135deg,#F472B6,#F87171)!important;
        animation:micpulse .7s ease-in-out infinite;}
    @keyframes micpulse{0%{box-shadow:0 0 0 0 rgba(244,114,182,.7)}
        70%{box-shadow:0 0 0 12px rgba(244,114,182,0)}100%{box-shadow:0 0 0 0 rgba(244,114,182,0)}}
    #micStatus{font-size:11px;color:#F472B6;font-weight:600;
        letter-spacing:.08em;text-transform:uppercase;min-width:80px;}
    </style>
    <div id="micWrap">
      <button id="micBtn2" title="Click to speak">🎤</button>
      <span id="micStatus"></span>
    </div>
    <script>
    var _recog=null,_on=false;
    document.getElementById('micBtn2').onclick=function(){
      if(_on){_recog&&_recog.stop();return;}
      var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
      if(!SR){document.getElementById('micStatus').textContent='Not supported';return;}
      _recog=new SR(); _recog.lang='en-IN'; _recog.continuous=false; _recog.interimResults=true;
      _recog.onstart=function(){
        _on=true;
        document.getElementById('micBtn2').classList.add('on');
        document.getElementById('micBtn2').textContent='⏹';
        document.getElementById('micStatus').textContent='● Listening…';
      };
      _recog.onresult=function(e){
        var t='';
        for(var i=e.resultIndex;i<e.results.length;i++) t+=e.results[i][0].transcript;
        // Put transcript into the Streamlit text input
        var inp=window.parent.document.querySelector('input[data-testid="stTextInputRootElement"], input[aria-label="Ask anything"]');
        if(!inp){ var all=window.parent.document.querySelectorAll('input[type=text]'); inp=all[all.length-1]; }
        if(inp){
          var nv=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
          nv.call(inp,t); inp.dispatchEvent(new Event('input',{bubbles:true}));
        }
        if(e.results[e.results.length-1].isFinal){
          document.getElementById('micStatus').textContent='✓ Done!';
        }
      };
      _recog.onerror=function(e){document.getElementById('micStatus').textContent='Error:'+e.error;};
      _recog.onend=function(){
        _on=false;
        document.getElementById('micBtn2').classList.remove('on');
        document.getElementById('micBtn2').textContent='🎤';
        setTimeout(function(){document.getElementById('micStatus').textContent='';},2000);
      };
      _recog.start();
    };
    </script>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:1.5rem 1rem 1.1rem;border-bottom:1px solid rgba(255,255,255,.06);margin-bottom:1rem;">
      <div style="display:flex;align-items:center;gap:.65rem;margin-bottom:.75rem;">
        <div style="width:38px;height:38px;background:linear-gradient(135deg,#8B5CF6,#06B6D4);
             border-radius:10px;display:flex;align-items:center;justify-content:center;
             font-size:1.1rem;box-shadow:0 0 16px rgba(139,92,246,.4);">🐇</div>
        <div>
          <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:1rem;font-weight:900;color:#fff;">Rabbitt AI</div>
          <div style="font-size:.57rem;color:#1E293B;letter-spacing:.14em;text-transform:uppercase;">Construction Intel</div>
        </div>
      </div>
      <div style="display:inline-flex;align-items:center;gap:.4rem;
           background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.2);
           border-radius:100px;padding:.2rem .65rem;">
        <span style="width:5px;height:5px;background:#34D399;border-radius:50%;
              box-shadow:0 0 5px #34D399;animation:bl 2s ease-in-out infinite;display:inline-block;"></span>
        <span style="font-size:.57rem;color:#34D399;font-weight:600;letter-spacing:.1em;text-transform:uppercase;">AI Online</span>
      </div>
    </div>
    <style>@keyframes bl{0%,100%{opacity:1}50%{opacity:.3}}</style>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:.57rem;color:#1E293B;letter-spacing:.14em;text-transform:uppercase;margin:0 0 .4rem;">Sample Data</p>', unsafe_allow_html=True)
    st.download_button("↓  Download sample.csv", data=generate_sample_csv(),
                       file_name="construction_data.csv", mime="text/csv", use_container_width=True)

    st.markdown("<div style='height:.9rem'></div>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:.57rem;color:#1E293B;letter-spacing:.14em;text-transform:uppercase;margin:0 0 .4rem;">Try Asking</p>', unsafe_allow_html=True)

    suggestions = [
        "Which towers are ready for billing?",
        "Show me all delayed towers",
        "What is the total pending revenue?",
        "Which project is highest risk?",
        "Compare all projects by slab %",
        "Show regulatory status breakdown",
        "Give me an executive summary",
        "Which tower has the most delay?",
    ]
    for s in suggestions:
        if st.button(s, use_container_width=True, key=f"s_{s}"):
            st.session_state.pending_q = s
            st.rerun()

    if st.session_state.df is not None:
        d = st.session_state.df
        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(139,92,246,.25),transparent);margin-bottom:.85rem;"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:.57rem;color:#1E293B;letter-spacing:.14em;text-transform:uppercase;margin:0 0 .5rem;">Portfolio</p>', unsafe_allow_html=True)
        for icon,lbl,val,col in [
            ("◈","Projects",d['Project'].nunique(),"#A78BFA"),
            ("◫","Towers",len(d),"#E2E8F0"),
            ("◉","Ready",len(d[d["Slab_Percent"]>90]),"#34D399"),
            ("▲","Delayed",len(d[d["Days_Delayed"]>0]),"#F87171"),
        ]:
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;
                padding:.36rem 0;border-bottom:1px solid rgba(255,255,255,.04);">
                <span style="font-size:.75rem;color:#334155;">{icon}&ensp;{lbl}</span>
                <span style="font-family:'Cabinet Grotesk',sans-serif;font-size:.95rem;font-weight:800;color:{col};">{val}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="margin-top:.75rem;padding:.8rem;
            background:linear-gradient(135deg,rgba(139,92,246,.07),rgba(6,182,212,.05));
            border:1px solid rgba(139,92,246,.14);border-radius:11px;text-align:center;">
            <div style="font-size:.54rem;color:#1E293B;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.18rem;">Revenue Pending</div>
            <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:1.2rem;font-weight:900;color:#22D3EE;letter-spacing:-.02em;">
              {fmt_crore(d["Revenue_Pending"].sum())}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="margin-top:2rem;text-align:center;font-size:.53rem;color:#0F172A;">© 2025 Rabbitt AI</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# MAIN HEADER
# ════════════════════════════════════════════════
h1, h2 = st.columns([5,1])
with h1:
    st.markdown("""
    <div style="margin-bottom:.2rem;">
      <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:.57rem;font-weight:700;
           color:#1E293B;letter-spacing:.2em;text-transform:uppercase;margin-bottom:.35rem;">
        Voice-First AI · Construction Intelligence
      </div>
      <h1 style="font-family:'Cabinet Grotesk',sans-serif;font-size:2.2rem;font-weight:900;
          color:#fff;margin:0;line-height:1.05;letter-spacing:-.035em;">
        Speak. Ask.<span style="background:linear-gradient(90deg,#8B5CF6,#06B6D4,#F472B6);
        background-size:200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;animation:gs 5s linear infinite;"> Understand.</span>
      </h1>
    </div>
    <style>@keyframes gs{0%{background-position:0%}50%{background-position:100%}100%{background-position:0%}}</style>
    """, unsafe_allow_html=True)
with h2:
    st.markdown("""<div style="text-align:right;padding-top:1.1rem;">
      <div style="display:inline-block;background:rgba(139,92,246,.1);
           border:1px solid rgba(139,92,246,.25);border-radius:100px;padding:.25rem .75rem;">
        <span style="font-size:.58rem;color:#A78BFA;font-weight:600;letter-spacing:.1em;text-transform:uppercase;">
          Gemini Powered</span>
      </div></div>""", unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:linear-gradient(90deg,rgba(139,92,246,.5),rgba(6,182,212,.3),transparent);margin:.5rem 0 1.5rem;"></div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# UPLOAD PAGE
# ════════════════════════════════════════════════
if st.session_state.df is None:
    st.markdown("""
    <div class="gc" style="text-align:center;padding:3.5rem 2rem;margin-bottom:1.5rem;">
      <div style="font-size:2.5rem;margin-bottom:.75rem;">🐇</div>
      <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:2rem;font-weight:900;
           color:#fff;letter-spacing:-.03em;margin-bottom:.6rem;">Talk to your data.</div>
      <div style="font-size:.92rem;color:#475569;max-width:420px;margin:0 auto 1.5rem;font-weight:300;line-height:1.7;">
        Upload your construction CSV, then ask anything in plain English or by voice.
        Get instant AI answers with charts, spoken aloud.
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:.45rem;justify-content:center;">
        <span style="background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.2);border-radius:100px;padding:.28rem .8rem;font-size:.72rem;color:#A78BFA;">🎤 Voice input</span>
        <span style="background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.2);border-radius:100px;padding:.28rem .8rem;font-size:.72rem;color:#67E8F9;">📊 Auto charts</span>
        <span style="background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.2);border-radius:100px;padding:.28rem .8rem;font-size:.72rem;color:#6EE7B7;">🔊 Voice answers</span>
        <span style="background:rgba(244,114,182,.08);border:1px solid rgba(244,114,182,.2);border-radius:100px;padding:.28rem .8rem;font-size:.72rem;color:#FBCFE8;">🤖 Gemini AI</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([3,2])
    with c1:
        st.markdown('<p style="font-size:.57rem;color:#1E293B;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.4rem;">Upload CSV</p>', unsafe_allow_html=True)
        up = st.file_uploader("csv", type=["csv"], label_visibility="collapsed")
        if up:
            try:
                df = pd.read_csv(up)
                req = {"Project","Tower","Slab_Percent","Revenue_Pending","Days_Delayed","Regulatory_Status"}
                miss = req - set(df.columns)
                if miss:
                    st.error(f"Missing columns: {', '.join(miss)}")
                else:
                    st.session_state.df = df
                    st.success(f"✓ Loaded {len(df)} towers across {df['Project'].nunique()} projects")
                    st.rerun()
            except Exception as e:
                st.error(str(e))
    with c2:
        st.markdown("""<div class="gc" style="padding:1.2rem 1.4rem;">
          <div style="font-size:.57rem;color:#1E293B;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.7rem;">Required Columns</div>
          <div style="font-size:.8rem;color:#475569;line-height:2.15;">
            <span style="color:#8B5CF6;margin-right:.5rem;">▹</span>Project<br>
            <span style="color:#8B5CF6;margin-right:.5rem;">▹</span>Tower<br>
            <span style="color:#8B5CF6;margin-right:.5rem;">▹</span>Slab_Percent<br>
            <span style="color:#8B5CF6;margin-right:.5rem;">▹</span>Revenue_Pending<br>
            <span style="color:#8B5CF6;margin-right:.5rem;">▹</span>Days_Delayed<br>
            <span style="color:#8B5CF6;margin-right:.5rem;">▹</span>Regulatory_Status
          </div></div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════
# MAIN CHAT INTERFACE
# ════════════════════════════════════════════════
else:
    df = st.session_state.df

    # KPIs
    ready   = len(df[df["Slab_Percent"]>90])
    delayed = len(df[df["Days_Delayed"]>0])
    st.markdown(f"""<div class="kgrid">
      <div class="kt"><div class="kv">{df['Project'].nunique()}</div><div class="kl">Projects</div></div>
      <div class="kt"><div class="kv">{len(df)}</div><div class="kl">Towers</div></div>
      <div class="kt"><div class="kv" style="color:#34D399;">{ready}</div><div class="kl">Ready to Bill</div></div>
      <div class="kt"><div class="kv" style="color:#F87171;">{delayed}</div><div class="kl">Delayed</div></div>
      <div class="kt"><div class="kv" style="font-size:1.1rem;color:#22D3EE;">{fmt_crore(df["Revenue_Pending"].sum())}</div><div class="kl">Revenue Pending</div></div>
      <div class="kt"><div class="kv">{df["Slab_Percent"].mean():.0f}<span style="font-size:1rem;">%</span></div><div class="kl">Avg Slab</div></div>
    </div>""", unsafe_allow_html=True)

    # ── INPUT BAR ─────────────────────────────────
    # pending_q comes from sidebar button clicks
    if "pending_q" not in st.session_state: st.session_state.pending_q = ""

    col_mic, col_input, col_send = st.columns([0.5, 5.5, 1])
    with col_mic:
        mic_button()
    with col_input:
        query = st.text_input(
            "Ask anything",
            placeholder="Type or speak: 'Which towers are delayed?' · 'Show revenue by project' · 'Summary'…",
            label_visibility="collapsed",
            key="main_input",
        )
    with col_send:
        send = st.button("Send →", use_container_width=True, key="send_btn")

    # ── DETERMINE WHAT TO RUN ──────────────────────
    # Priority: sidebar suggestion > typed + Send button
    to_run = ""
    if st.session_state.pending_q:
        to_run = st.session_state.pending_q
        st.session_state.pending_q = ""
    elif send and query.strip():
        to_run = query.strip()

    if to_run:
        with st.spinner("🐇 Thinking…"):
            try:
                answer, fig = ask_ai(df, to_run, st.session_state.chat)
                st.session_state.chat.append({"role":"user","content":to_run})
                st.session_state.chat.append({"role":"assistant","content":answer,"fig":fig})
            except Exception as e:
                st.error(f"AI error: {e}")
        st.rerun()

    # ── CHAT HISTORY ──────────────────────────────
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:.57rem;color:#1E293B;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.6rem;">Conversation</p>', unsafe_allow_html=True)

    if not st.session_state.chat:
        st.markdown("""<div class="gc" style="text-align:center;padding:2.2rem 1.5rem;">
          <div style="font-size:1.5rem;margin-bottom:.5rem;">✦</div>
          <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:.95rem;font-weight:800;color:#fff;margin-bottom:.3rem;">
            Ready — type above or click 🎤 to speak</div>
          <div style="font-size:.8rem;color:#1E293B;font-weight:300;">
            Or pick a question from the sidebar →</div>
        </div>""", unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.chat):
        if msg["role"] == "user":
            st.markdown(f"""<div class="uw">
              <div class="ub"><div class="bl blu">You</div>{msg['content']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="aw">
              <div class="aibadge">🐇</div>
              <div class="ab"><div class="bl bla">Rabbitt AI</div>{msg['content']}</div>
            </div>""", unsafe_allow_html=True)

            # Chart
            if msg.get("fig") is not None:
                st.plotly_chart(msg["fig"], use_container_width=True, key=f"fig_{i}")

            # Auto-speak latest response only
            if i == len(st.session_state.chat) - 1:
                speak(msg["content"], i)

    # ── ACTIONS ───────────────────────────────────
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    ca, cb, cc, _ = st.columns([1.1,1.4,1.5,4])
    with ca:
        if st.button("🗑 Clear", use_container_width=True):
            st.session_state.chat = []
            st.session_state.last_q = ""
            st.rerun()
    with cb:
        if st.button("📤 New Dataset", use_container_width=True):
            st.session_state.df   = None
            st.session_state.chat = []
            st.rerun()
    with cc:
        st.markdown("""<button onclick="window.speechSynthesis.cancel()"
            style="width:100%;background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.25);
            border-radius:11px;padding:.44rem .5rem;cursor:pointer;color:#F87171;
            font-size:.78rem;font-family:'Cabinet Grotesk',sans-serif;font-weight:700;transition:all .2s;"
            onmouseover="this.style.background='rgba(248,113,113,.22)'"
            onmouseout="this.style.background='rgba(248,113,113,.1)'">🔇 Stop Voice</button>
        """, unsafe_allow_html=True)
