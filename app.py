"""
Talking Rabbitt — Conversational Intelligence Platform
Built for Rabbitt AI Assessment
Design: Neo-Minimal — Pure Black + Electric Cyan/Violet
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Rabbitt AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS — Neo-Minimal Next-Gen
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --bg:         #060608;
    --bg1:        #0C0C10;
    --bg2:        #111116;
    --bg3:        #18181F;
    --cyan:       #00F5D4;
    --violet:     #7C3AED;
    --violet-lt:  #A78BFA;
    --pink:       #F472B6;
    --green:      #34D399;
    --red:        #F87171;
    --amber:      #FBBF24;
    --white:      #F1F1F3;
    --grey:       #6B6B7B;
    --grey-lt:    #9999A8;
    --border:     rgba(255,255,255,0.06);
    --border-hi:  rgba(0,245,212,0.2);
    --glow-cyan:  0 0 30px rgba(0,245,212,0.12);
    --glow-v:     0 0 30px rgba(124,58,237,0.15);
}

/* ── BASE ── */
html, body, [class*="css"], .stApp {
    background: var(--bg) !important;
    color: var(--white) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── NOISE TEXTURE OVERLAY ── */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    opacity: 0.4;
}

/* ── GRADIENT MESH BG ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 0% 0%,   rgba(124,58,237,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 100% 100%, rgba(0,245,212,0.06) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 50% 30%,  rgba(244,114,182,0.04) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--bg1) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}

/* ── MAIN ── */
.main .block-container {
    background: transparent !important;
    padding: 1.75rem 2.5rem 4rem !important;
    max-width: 1440px;
}

/* ── METRIC GRID ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.6rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 0.75rem 0.85rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, transform 0.25s;
    cursor: default;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.kpi-card:hover { border-color: var(--border-hi); transform: translateY(-2px); }
.kpi-card:hover::after { opacity: 1; }
.kpi-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.65rem;
    font-weight: 800;
    color: var(--white);
    line-height: 1;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}
.kpi-label {
    font-size: 0.58rem;
    font-weight: 500;
    color: var(--grey);
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* ── CHAT BUBBLES ── */
.msg-wrap-user {
    display: flex;
    justify-content: flex-end;
    margin: 1rem 0 0.4rem;
}
.msg-wrap-ai {
    display: flex;
    justify-content: flex-start;
    margin: 0.4rem 0 1rem;
    gap: 0.6rem;
    align-items: flex-start;
}
.ai-avatar {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, var(--violet), var(--cyan));
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
    margin-top: 2px;
    box-shadow: 0 0 12px rgba(124,58,237,0.4);
}
.bubble-user {
    max-width: 68%;
    background: var(--bg3);
    border: 1px solid rgba(0,245,212,0.15);
    border-radius: 18px 18px 4px 18px;
    padding: 0.8rem 1.1rem;
    font-size: 0.9rem;
    color: var(--white);
    line-height: 1.6;
}
.bubble-ai {
    max-width: 78%;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 4px 18px 18px 18px;
    padding: 0.8rem 1.1rem;
    font-size: 0.9rem;
    color: #C8C8D4;
    line-height: 1.6;
}
.bubble-name {
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.bubble-name.user { color: var(--cyan); text-align: right; }
.bubble-name.ai   { color: var(--violet-lt); }

/* ── WELCOME SCREEN ── */
.hero {
    background: var(--bg1);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 4rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 200px;
    background: radial-gradient(ellipse, rgba(124,58,237,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-logo {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}
.hero-logo::before, .hero-logo::after {
    content: '';
    width: 30px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan));
}
.hero-logo::after { transform: scaleX(-1); }
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--white);
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 0.75rem;
}
.hero-title span {
    background: linear-gradient(90deg, var(--cyan), var(--violet-lt));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.9rem;
    color: var(--grey-lt);
    max-width: 400px;
    margin: 0 auto 2rem;
    line-height: 1.7;
    font-weight: 300;
}
.hero-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
}
.hero-chip {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.3rem 0.9rem;
    font-size: 0.72rem;
    color: var(--grey-lt);
    font-weight: 400;
}

/* ── EMPTY CHAT STATE ── */
.chat-empty {
    background: var(--bg1);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
}

/* ── INPUT OVERRIDES ── */
.stTextInput > div > div > input {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--white) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0,245,212,0.4) !important;
    box-shadow: 0 0 0 3px rgba(0,245,212,0.07) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--grey) !important;
    font-weight: 300 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #00F5D4 0%, #7C3AED 100%) !important;
    color: #060608 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    transition: opacity 0.2s, transform 0.2s !important;
    box-shadow: 0 4px 20px rgba(0,245,212,0.2) !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* GHOST secondary buttons */
section[data-testid="stSidebar"] .stButton > button,
.ghost-btn .stButton > button {
    background: var(--bg3) !important;
    color: var(--grey-lt) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0 !important;
    text-align: left !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg3) !important;
    border-color: rgba(0,245,212,0.25) !important;
    color: var(--cyan) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: var(--bg3) !important;
    color: var(--cyan) !important;
    border: 1px solid rgba(0,245,212,0.2) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    font-size: 0.82rem !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,245,212,0.06) !important;
    border-color: rgba(0,245,212,0.4) !important;
    box-shadow: var(--glow-cyan) !important;
    transform: translateY(-1px) !important;
}

/* ── UPLOAD ZONE ── */
div[data-testid="stFileUploader"] {
    background: var(--bg2) !important;
    border: 1px dashed rgba(0,245,212,0.2) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: all 0.2s !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,245,212,0.5) !important;
    background: rgba(0,245,212,0.03) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--cyan) !important; }

/* ── SUCCESS / ERROR ── */
.stSuccess { background: rgba(52,211,153,0.07) !important; border-color: rgba(52,211,153,0.25) !important; border-radius: 10px !important; }
.stError   { background: rgba(248,113,113,0.07) !important; border-color: rgba(248,113,113,0.25) !important; border-radius: 10px !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

/* ── HIDE CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SAMPLE DATA GENERATOR
# ─────────────────────────────────────────────
def generate_sample_csv() -> bytes:
    data = {
        "Project": [
            "Skyline One","Skyline One","Skyline One",
            "The Pinnacle","The Pinnacle",
            "Nexus Park","Nexus Park","Nexus Park",
            "Horizon West","Horizon West","Horizon West","Horizon West",
            "The Arbour","The Arbour",
        ],
        "Tower": ["T1","T2","T3","PA","PB","NX1","NX2","NX3","HW1","HW2","HW3","HW4","AR1","AR2"],
        "Slab_Percent": [96,88,72,99,91,55,63,44,93,78,85,97,34,61],
        "Revenue_Pending": [
            420000000,385000000,297500000,
            850000000,762000000,
            183000000,221000000,146000000,
            315000000,278000000,332000000,291000000,
            94000000,167000000,
        ],
        "Days_Delayed": [12,0,45,5,0,90,60,120,8,30,15,0,180,75],
        "Regulatory_Status": [
            "Approved","Approved","Pending NOC",
            "OC Received","Approved",
            "Pending NOC","Approved","Pending NOC",
            "Approved","OC Received","Approved","OC Received",
            "Pending NOC","Approved",
        ],
    }
    buf = io.BytesIO()
    pd.DataFrame(data).to_csv(buf, index=False)
    return buf.getvalue()


# ─────────────────────────────────────────────
# QUERY ENGINE
# ─────────────────────────────────────────────
def classify_query(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["ready","billing","collection","complete","handover","done"]):
        return "ready_for_collection"
    if any(k in q for k in ["delay","late","behind","overdue","slow"]):
        return "delayed_towers"
    if any(k in q for k in ["revenue","pending","money","amount","value","crore"]):
        return "revenue_analysis"
    if any(k in q for k in ["regulatory","rera","noc","oc","approval","status"]):
        return "regulatory_status"
    if any(k in q for k in ["progress","slab","percent","construction","overview","summary"]):
        return "progress_overview"
    if any(k in q for k in ["project","compare","comparison","best","worst","all"]):
        return "project_comparison"
    return "general"


def fmt_crore(val: float) -> str:
    return f"₹{val/1e7:.1f} Cr"


def _style(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6B6B7B", family="Outfit"),
        title_font=dict(size=13, color="#00F5D4", family="Syne"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#6B6B7B"), zeroline=False, showline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#6B6B7B"), zeroline=False, showline=False),
        margin=dict(t=44, l=8, r=8, b=32),
        hoverlabel=dict(bgcolor="#111116", bordercolor="#00F5D4", font_color="#F1F1F3", font_family="Outfit"),
        coloraxis_colorbar=dict(tickfont=dict(color="#6B6B7B")),
    )
    fig.update_traces(textfont_size=11)
    return fig


def answer_query(df: pd.DataFrame, query: str):
    intent = classify_query(query)

    if intent == "ready_for_collection":
        result = df[df["Slab_Percent"] > 90].sort_values("Revenue_Pending", ascending=False)
        if result.empty:
            return "No towers currently exceed the 90% slab completion threshold.", None, None
        total = result["Revenue_Pending"].sum()
        answer = (
            f"**{len(result)} tower(s)** are above 90% slab — ready for billing.  \n"
            f"**Unlockable Revenue:** {fmt_crore(total)}"
        )
        fig = px.bar(
            result, x="Tower", y="Revenue_Pending",
            color="Slab_Percent",
            color_continuous_scale=["#1a1a2e","#7C3AED","#00F5D4"],
            title="Ready for Collection — Revenue Pending",
            text=result["Revenue_Pending"].apply(fmt_crore),
            hover_data=["Project","Regulatory_Status"],
            labels={"Revenue_Pending":"Revenue","Slab_Percent":"Slab %"},
        )
        return answer, result[["Project","Tower","Slab_Percent","Revenue_Pending","Regulatory_Status"]], _style(fig)

    elif intent == "delayed_towers":
        result = df[df["Days_Delayed"] > 0].sort_values("Days_Delayed", ascending=False)
        if result.empty:
            return "All towers are on schedule. No delays detected.", None, None
        answer = (
            f"**{len(result)} tower(s)** behind schedule.  \n"
            f"**Worst delay:** Tower {result.iloc[0]['Tower']} — {result.iloc[0]['Days_Delayed']} days"
        )
        fig = px.bar(
            result, x="Tower", y="Days_Delayed",
            color="Days_Delayed",
            color_continuous_scale=["#FBBF24","#F87171"],
            title="Delayed Towers — Days Behind Schedule",
            text="Days_Delayed", hover_data=["Project"],
            labels={"Days_Delayed":"Days Delayed"},
        )
        return answer, result[["Project","Tower","Slab_Percent","Days_Delayed","Regulatory_Status"]], _style(fig)

    elif intent == "revenue_analysis":
        grp = df.groupby("Project")["Revenue_Pending"].sum().reset_index().sort_values("Revenue_Pending", ascending=False)
        total = df["Revenue_Pending"].sum()
        answer = (
            f"**Total Revenue Pending:** {fmt_crore(total)}  \n"
            f"**Top Project:** {grp.iloc[0]['Project']} — {fmt_crore(grp.iloc[0]['Revenue_Pending'])}"
        )
        fig = px.bar(
            grp, x="Project", y="Revenue_Pending",
            color="Revenue_Pending",
            color_continuous_scale=["#1a1a2e","#00F5D4"],
            title="Revenue Pending by Project",
            text=grp["Revenue_Pending"].apply(fmt_crore),
            labels={"Revenue_Pending":"Revenue"},
        )
        return answer, grp, _style(fig)

    elif intent == "regulatory_status":
        sc = df["Regulatory_Status"].value_counts().reset_index()
        sc.columns = ["Status","Count"]
        answer = (
            f"**Regulatory breakdown across {len(df)} towers:**  \n"
            + "  \n".join(f"— **{r['Status']}:** {r['Count']} towers" for _, r in sc.iterrows())
        )
        fig = px.pie(
            sc, names="Status", values="Count",
            color_discrete_sequence=["#34D399","#00F5D4","#F87171","#FBBF24"],
            title="Regulatory Status Distribution", hole=0.55,
        )
        fig.update_traces(textfont_color="#F1F1F3", textfont_size=12)
        return answer, df[["Project","Tower","Regulatory_Status"]], _style(fig)

    elif intent == "progress_overview":
        result = df.sort_values("Slab_Percent", ascending=False)
        avg = df["Slab_Percent"].mean()
        answer = (
            f"**Average Slab Completion:** {avg:.1f}%  \n"
            f"**Leading:** {result.iloc[0]['Tower']} ({result.iloc[0]['Slab_Percent']}%)  ·  "
            f"**Lagging:** {result.iloc[-1]['Tower']} ({result.iloc[-1]['Slab_Percent']}%)"
        )
        fig = px.bar(
            result, x="Tower", y="Slab_Percent",
            color="Slab_Percent",
            color_continuous_scale=["#F87171","#FBBF24","#34D399"],
            title="Slab Completion Progress — All Towers",
            text="Slab_Percent", hover_data=["Project"],
            labels={"Slab_Percent":"Slab %"},
        )
        fig.add_hline(y=90, line_dash="dot", line_color="#00F5D4",
                      annotation_text="Billing Threshold 90%",
                      annotation_font_color="#00F5D4", annotation_font_size=11)
        return answer, result, _style(fig)

    elif intent == "project_comparison":
        grp = df.groupby("Project").agg(
            Avg_Slab=("Slab_Percent","mean"),
            Total_Revenue=("Revenue_Pending","sum"),
            Avg_Delay=("Days_Delayed","mean"),
        ).reset_index().sort_values("Avg_Slab", ascending=False)
        answer = (
            f"**{len(grp)} projects** compared.  \n"
            f"**Top performer:** {grp.iloc[0]['Project']} — {grp.iloc[0]['Avg_Slab']:.1f}% avg slab"
        )
        fig = px.scatter(
            grp, x="Avg_Slab", y="Total_Revenue",
            size="Avg_Delay", color="Project",
            title="Project Comparison: Slab % vs Revenue  (bubble size = delay)",
            labels={"Avg_Slab":"Avg Slab %","Total_Revenue":"Revenue Pending"},
            size_max=55,
            color_discrete_sequence=["#00F5D4","#7C3AED","#34D399","#F87171","#FBBF24"],
        )
        return answer, grp, _style(fig)

    else:
        answer = (
            "Here's what I can analyse for you:  \n\n"
            "— *Which towers are ready for billing?*  \n"
            "— *Show me delayed towers*  \n"
            "— *What's the pending revenue?*  \n"
            "— *Show construction progress*  \n"
            "— *What's the regulatory status?*  \n"
            "— *Compare all projects*"
        )
        return answer, None, None


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df" not in st.session_state:
    st.session_state.df = None


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # ── Brand ─────────────────────────────────
    st.markdown("""
    <div style="padding:1.6rem 1rem 1.2rem;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1rem;">
        <div style="display:flex;align-items:center;gap:0.65rem;margin-bottom:0.8rem;">
            <div style="width:36px;height:36px;
                        background:linear-gradient(135deg,#00F5D4,#7C3AED);
                        border-radius:9px;display:flex;align-items:center;
                        justify-content:center;font-size:1.1rem;flex-shrink:0;
                        box-shadow:0 0 16px rgba(0,245,212,0.25);">⚡</div>
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;
                            color:#F1F1F3;letter-spacing:-0.01em;">Rabbitt AI</div>
                <div style="font-size:0.58rem;color:#3a3a4a;letter-spacing:0.14em;
                            text-transform:uppercase;font-family:'Outfit',sans-serif;">
                    Construction Intel</div>
            </div>
        </div>
        <div style="display:inline-flex;align-items:center;gap:0.4rem;
                    background:rgba(52,211,153,0.07);
                    border:1px solid rgba(52,211,153,0.18);
                    border-radius:100px;padding:0.2rem 0.65rem;">
            <span style="width:5px;height:5px;background:#34D399;border-radius:50%;
                         display:inline-block;box-shadow:0 0 5px #34D399;
                         animation:blink 2s ease-in-out infinite;"></span>
            <span style="font-size:0.58rem;color:#34D399;font-weight:600;
                         letter-spacing:0.1em;text-transform:uppercase;">Live</span>
        </div>
    </div>
    <style>
    @keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
    </style>
    """, unsafe_allow_html=True)

    # ── Sample data ───────────────────────────
    st.markdown('<p style="font-size:0.58rem;color:#3a3a4a;letter-spacing:0.14em;text-transform:uppercase;margin:0 0 0.45rem;font-family:Outfit,sans-serif;">Sample Data</p>', unsafe_allow_html=True)
    st.download_button(
        label="↓  Download sample.csv",
        data=generate_sample_csv(),
        file_name="construction_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Quick queries ─────────────────────────
    st.markdown('<p style="font-size:0.58rem;color:#3a3a4a;letter-spacing:0.14em;text-transform:uppercase;margin:0 0 0.45rem;font-family:Outfit,sans-serif;">Quick Queries</p>', unsafe_allow_html=True)

    for eq in [
        "Which towers are ready for billing?",
        "Show delayed towers",
        "Pending revenue breakdown",
        "Construction progress",
        "Regulatory status",
        "Compare all projects",
    ]:
        if st.button(eq, use_container_width=True, key=f"q_{eq}"):
            st.session_state["prefill_query"] = eq

    # ── Live stats when data loaded ───────────
    if st.session_state.df is not None:
        d = st.session_state.df
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,245,212,0.15),transparent);margin-bottom:1rem;"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.58rem;color:#3a3a4a;letter-spacing:0.14em;text-transform:uppercase;margin:0 0 0.6rem;font-family:Outfit,sans-serif;">Portfolio</p>', unsafe_allow_html=True)

        for icon, lbl, val, color in [
            ("◈", "Projects",   d['Project'].nunique(), "#00F5D4"),
            ("◫", "Towers",     len(d),                 "#F1F1F3"),
            ("◉", "Ready",      len(d[d["Slab_Percent"]>90]), "#34D399"),
            ("◈", "Delayed",    len(d[d["Days_Delayed"]>0]),  "#F87171"),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.38rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span style="font-size:0.75rem;color:#4a4a5a;font-family:Outfit,sans-serif;">
                    {icon}&nbsp; {lbl}</span>
                <span style="font-family:'Syne',sans-serif;font-size:0.95rem;
                             font-weight:700;color:{color};">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        rev = fmt_crore(d["Revenue_Pending"].sum())
        st.markdown(f"""
        <div style="margin-top:0.8rem;padding:0.8rem;
                    background:linear-gradient(135deg,rgba(0,245,212,0.05),rgba(124,58,237,0.05));
                    border:1px solid rgba(0,245,212,0.12);border-radius:10px;text-align:center;">
            <div style="font-size:0.55rem;color:#3a3a4a;letter-spacing:0.12em;
                        text-transform:uppercase;margin-bottom:0.2rem;font-family:Outfit,sans-serif;">
                Revenue Pending</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.2rem;
                        font-weight:800;color:#00F5D4;letter-spacing:-0.02em;">{rev}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ────────────────────────────────
    st.markdown("""
    <div style="position:absolute;bottom:1.2rem;left:0;right:0;text-align:center;">
        <div style="font-size:0.55rem;color:#1e1e28;letter-spacing:0.06em;font-family:Outfit,sans-serif;">
            © 2025 Rabbitt AI
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN — HEADER
# ─────────────────────────────────────────────
col_h, col_tag = st.columns([5, 1])
with col_h:
    st.markdown("""
    <div style="margin-bottom:0.2rem;">
        <div style="font-family:'Syne',sans-serif;font-size:0.58rem;font-weight:600;
                    color:#3a3a4a;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.4rem;">
            Conversational Intelligence Platform
        </div>
        <h1 style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
                   color:#F1F1F3;margin:0;line-height:1.05;letter-spacing:-0.03em;">
            Ask your data<span style="background:linear-gradient(90deg,#00F5D4,#A78BFA);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;"> anything.</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)
with col_tag:
    st.markdown("""
    <div style="text-align:right;padding-top:1.2rem;">
        <div style="display:inline-block;background:rgba(0,245,212,0.06);
                    border:1px solid rgba(0,245,212,0.15);border-radius:100px;
                    padding:0.25rem 0.75rem;">
            <span style="font-size:0.6rem;color:#00F5D4;font-weight:600;
                         letter-spacing:0.1em;text-transform:uppercase;">Beta</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:linear-gradient(90deg,rgba(0,245,212,0.4),rgba(124,58,237,0.2),transparent);margin:0.6rem 0 1.5rem;"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UPLOAD / LANDING STATE
# ─────────────────────────────────────────────
if st.session_state.df is None:

    st.markdown("""
    <div class="hero">
        <div class="hero-logo">⚡ Rabbitt AI</div>
        <div class="hero-title">Construction intelligence,<br><span>conversationally.</span></div>
        <div class="hero-sub">
            Upload your site data and ask questions in plain English.
            Get instant charts, insights, and analysis — no dashboards needed.
        </div>
        <div class="hero-chips">
            <span class="hero-chip">Ready for billing?</span>
            <span class="hero-chip">Delayed towers</span>
            <span class="hero-chip">Revenue analysis</span>
            <span class="hero-chip">RERA status</span>
            <span class="hero-chip">Progress overview</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    col_u, col_spec = st.columns([3, 2])
    with col_u:
        st.markdown('<p style="font-size:0.58rem;color:#3a3a4a;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.4rem;">Upload CSV</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "csv", type=["csv"],
            label_visibility="collapsed",
            help="Use the sample CSV from the sidebar to get started instantly",
        )
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                required = {"Project","Tower","Slab_Percent","Revenue_Pending","Days_Delayed","Regulatory_Status"}
                missing = required - set(df.columns)
                if missing:
                    st.error(f"Missing columns: {', '.join(missing)}")
                else:
                    st.session_state.df = df
                    st.success(f"✓ Loaded {len(df)} towers across {df['Project'].nunique()} projects")
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading file: {e}")

    with col_spec:
        st.markdown("""
        <div style="background:var(--bg2,#111116);border:1px solid rgba(255,255,255,0.06);
                    border-radius:14px;padding:1.25rem 1.5rem;">
            <div style="font-size:0.58rem;color:#3a3a4a;letter-spacing:0.14em;
                        text-transform:uppercase;margin-bottom:0.8rem;">Required Columns</div>
            <div style="font-size:0.8rem;color:#6B6B7B;line-height:2.2;font-family:Outfit,sans-serif;">
                <span style="color:#00F5D4;margin-right:0.5rem;font-size:0.65rem;">▹</span>Project<br>
                <span style="color:#00F5D4;margin-right:0.5rem;font-size:0.65rem;">▹</span>Tower<br>
                <span style="color:#00F5D4;margin-right:0.5rem;font-size:0.65rem;">▹</span>Slab_Percent<br>
                <span style="color:#00F5D4;margin-right:0.5rem;font-size:0.65rem;">▹</span>Revenue_Pending<br>
                <span style="color:#00F5D4;margin-right:0.5rem;font-size:0.65rem;">▹</span>Days_Delayed<br>
                <span style="color:#00F5D4;margin-right:0.5rem;font-size:0.65rem;">▹</span>Regulatory_Status
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHAT INTERFACE
# ─────────────────────────────────────────────
else:
    df = st.session_state.df

    # ── KPIs ─────────────────────────────────
    ready   = len(df[df["Slab_Percent"] > 90])
    delayed = len(df[df["Days_Delayed"] > 0])
    rev     = df["Revenue_Pending"].sum()
    avg_s   = df["Slab_Percent"].mean()

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-num">{df['Project'].nunique()}</div>
            <div class="kpi-label">Projects</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num">{len(df)}</div>
            <div class="kpi-label">Towers</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num" style="color:#34D399;">{ready}</div>
            <div class="kpi-label">Ready to Bill</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num" style="color:#F87171;">{delayed}</div>
            <div class="kpi-label">Delayed</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num" style="font-size:1.15rem;color:#00F5D4;">{fmt_crore(rev)}</div>
            <div class="kpi-label">Revenue Pending</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num">{avg_s:.0f}<span style="font-size:1rem;">%</span></div>
            <div class="kpi-label">Avg Slab</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Conversation ─────────────────────────
    st.markdown('<p style="font-size:0.58rem;color:#3a3a4a;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.75rem;">Conversation</p>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="chat-empty">
            <div style="font-size:1.4rem;margin-bottom:0.5rem;">✦</div>
            <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;
                        color:#F1F1F3;margin-bottom:0.3rem;">Ready to analyse</div>
            <div style="font-size:0.82rem;color:#3a3a4a;max-width:340px;margin:0 auto;font-weight:300;">
                Use the quick queries in the sidebar or type below</div>
        </div>
        """, unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-wrap-user">
                <div class="bubble-user">
                    <div class="bubble-name user">You</div>
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-wrap-ai">
                <div class="ai-avatar">⚡</div>
                <div class="bubble-ai">
                    <div class="bubble-name ai">Rabbitt AI</div>
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if msg.get("df_result") is not None:
                res = msg["df_result"].copy()
                if "Revenue_Pending" in res.columns:
                    res["Revenue_Pending"] = res["Revenue_Pending"].apply(fmt_crore)
                st.dataframe(res, use_container_width=True, hide_index=True, key=f"df_{i}")
            if msg.get("fig") is not None:
                st.plotly_chart(msg["fig"], use_container_width=True, key=f"fig_{i}")

    # ── Input ─────────────────────────────────
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    prefill = st.session_state.pop("prefill_query", "")

    c1, c2 = st.columns([6, 1])
    with c1:
        query = st.text_input(
            "q", value=prefill,
            placeholder="Ask anything — billing readiness, delays, revenue, regulatory status…",
            label_visibility="collapsed", key="chat_input",
        )
    with c2:
        submit = st.button("Send →", use_container_width=True)

    if submit and query.strip():
        with st.spinner("Thinking…"):
            answer, df_result, fig = answer_query(df, query)
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({
            "role": "assistant", "content": answer,
            "df_result": df_result, "fig": fig,
        })
        st.rerun()

    # ── Actions ───────────────────────────────
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    ca, cb, _ = st.columns([1.2, 1.4, 5])
    with ca:
        if st.button("Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with cb:
        if st.button("New Dataset", use_container_width=True):
            st.session_state.df = None
            st.session_state.chat_history = []
            st.rerun()
