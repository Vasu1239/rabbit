"""
Talking Rabbitt — Conversational Intelligence MVP
Target Customer: DLF Limited (India's Largest Real Estate Developer)
Built for: Rabbitt AI Assessment
Design: Luxury Glassmorphism — Black Obsidian + Gold
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
    page_title="Talking Rabbitt | DLF Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# LUXURY CSS — Obsidian + Gold Glassmorphism
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --obsidian:   #080B10;
    --void:       #0D1117;
    --glass:      rgba(255,255,255,0.04);
    --glass-md:   rgba(255,255,255,0.07);
    --glass-hi:   rgba(255,255,255,0.11);
    --gold:       #C9A84C;
    --gold-light: #E8C96A;
    --gold-glow:  rgba(201,168,76,0.25);
    --platinum:   #D4D9E0;
    --silver:     #8B95A3;
    --emerald:    #10B981;
    --ruby:       #F43F5E;
    --border:     rgba(201,168,76,0.18);
    --border-dim: rgba(255,255,255,0.07);
    --shadow:     0 8px 32px rgba(0,0,0,0.6);
    --shadow-gold:0 0 40px rgba(201,168,76,0.12);
}

html, body, [class*="css"], .stApp {
    background: var(--obsidian) !important;
    color: var(--platinum) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(201,168,76,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(59,130,246,0.03) 0%, transparent 55%),
        radial-gradient(ellipse 50% 60% at 50% 50%, rgba(16,185,129,0.02) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1117 0%, #080B10 100%) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 30px rgba(0,0,0,0.5) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

.main .block-container {
    background: transparent !important;
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1400px;
}

.glass-card {
    background: var(--glass);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-dim);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.glass-card:hover {
    border-color: var(--border);
    box-shadow: var(--shadow-gold);
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.metric-tile {
    background: var(--glass);
    border: 1px solid var(--border-dim);
    border-radius: 14px;
    padding: 1.1rem 0.75rem;
    text-align: center;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}
.metric-tile::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.metric-tile:hover::before { opacity: 1; }
.metric-tile:hover {
    border-color: var(--border);
    background: var(--glass-md);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.metric-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--gold-light);
    line-height: 1;
    margin-bottom: 0.35rem;
}
.metric-lbl {
    font-size: 0.62rem;
    font-weight: 500;
    color: var(--silver);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.bubble-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.75rem 0;
}
.bubble-user-inner {
    max-width: 75%;
    background: linear-gradient(135deg, rgba(201,168,76,0.13), rgba(201,168,76,0.06));
    border: 1px solid rgba(201,168,76,0.28);
    border-radius: 20px 20px 4px 20px;
    padding: 0.85rem 1.2rem;
    color: var(--platinum);
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.bubble-user-name {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.3rem;
    text-align: right;
}

.bubble-ai {
    display: flex;
    justify-content: flex-start;
    margin: 0.75rem 0;
}
.bubble-ai-inner {
    max-width: 80%;
    background: var(--glass-md);
    border: 1px solid var(--border-dim);
    border-radius: 4px 20px 20px 20px;
    padding: 0.85rem 1.2rem;
    color: var(--platinum);
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.bubble-ai-name {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--emerald);
    margin-bottom: 0.3rem;
}

.welcome-hero {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3.5rem 2rem;
    text-align: center;
    box-shadow: var(--shadow-gold);
    position: relative;
    overflow: hidden;
}
.welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gold-light);
    margin-bottom: 0.5rem;
}
.welcome-sub {
    font-size: 0.9rem;
    color: var(--silver);
    max-width: 420px;
    margin: 0 auto 1rem;
    line-height: 1.6;
}

div[data-testid="stFileUploader"] {
    background: var(--glass) !important;
    border: 1px dashed rgba(201,168,76,0.3) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: var(--gold) !important;
    background: var(--glass-md) !important;
}

.stTextInput > div > div > input {
    background: var(--glass) !important;
    border: 1px solid rgba(201,168,76,0.22) !important;
    border-radius: 12px !important;
    color: var(--platinum) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--silver) !important; opacity: 0.55; }

.stButton > button {
    background: linear-gradient(135deg, #C9A84C, #A8882E) !important;
    color: #080B10 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    border: none !important;
    border-radius: 10px !important;
    letter-spacing: 0.03em;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(201,168,76,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(201,168,76,0.45) !important;
}

.stDownloadButton > button {
    background: var(--glass-md) !important;
    color: var(--gold-light) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: rgba(201,168,76,0.12) !important;
}

.stDataFrame { border-radius: 12px !important; overflow: hidden !important; border: 1px solid var(--border-dim) !important; }
.stSpinner > div { border-top-color: var(--gold) !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-thumb { background: rgba(201,168,76,0.25); border-radius: 4px; }

section[data-testid="stSidebar"] .stButton > button {
    background: var(--glass) !important;
    color: var(--silver) !important;
    border: 1px solid var(--border-dim) !important;
    box-shadow: none !important;
    font-weight: 400 !important;
    font-size: 0.8rem !important;
    text-align: left !important;
    transform: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--glass-md) !important;
    border-color: var(--border) !important;
    color: var(--gold-light) !important;
    box-shadow: none !important;
    transform: none !important;
}

.stSuccess { background: rgba(16,185,129,0.08) !important; border-color: rgba(16,185,129,0.3) !important; }
.stError   { background: rgba(244,63,94,0.08) !important;  border-color: rgba(244,63,94,0.3) !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SAMPLE DATA GENERATOR
# ─────────────────────────────────────────────
def generate_sample_csv() -> bytes:
    data = {
        "Project": [
            "DLF One Midtown","DLF One Midtown","DLF One Midtown",
            "The Camellias","The Camellias",
            "DLF 5","DLF 5","DLF 5",
            "Privana West","Privana West","Privana West","Privana West",
            "The Arbour","The Arbour",
        ],
        "Tower": ["T1","T2","T3","CA","CB","D5A","D5B","D5C","PW1","PW2","PW3","PW4","AR1","AR2"],
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
            "RERA Approved","RERA Approved","Pending NOC",
            "OC Received","RERA Approved",
            "Pending NOC","RERA Approved","Pending NOC",
            "RERA Approved","OC Received","RERA Approved","OC Received",
            "Pending NOC","RERA Approved",
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
    if any(k in q for k in ["project","compare","comparison","best","worst"]):
        return "project_comparison"
    return "general"


def fmt_crore(val: float) -> str:
    return f"₹{val/1e7:.1f} Cr"


CHART_THEME = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#8B95A3", family="DM Sans"),
    title_font=dict(size=14, color="#C9A84C", family="Playfair Display"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#8B95A3"), zeroline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#8B95A3"), zeroline=False),
    margin=dict(t=48, l=10, r=10, b=36),
    hoverlabel=dict(bgcolor="#0D1117", bordercolor="#C9A84C", font_color="#D4D9E0"),
)


def _fig(fig):
    fig.update_layout(**CHART_THEME)
    fig.update_traces(textfont_color="#080B10", textfont_size=11)
    return fig


def answer_query(df: pd.DataFrame, query: str):
    intent = classify_query(query)

    if intent == "ready_for_collection":
        result = df[df["Slab_Percent"] > 90].sort_values("Revenue_Pending", ascending=False)
        if result.empty:
            return "No towers currently exceed the 90% slab completion threshold.", None, None
        total = result["Revenue_Pending"].sum()
        answer = (
            f"**{len(result)} tower(s)** are above 90% slab completion and ready for collection.  \n"
            f"**Total Revenue Unlockable:** {fmt_crore(total)}"
        )
        fig = px.bar(
            result, x="Tower", y="Revenue_Pending",
            color="Slab_Percent", color_continuous_scale=["#1e3a5f","#C9A84C","#10B981"],
            title="Towers Ready for Collection — Revenue Pending",
            text=result["Revenue_Pending"].apply(fmt_crore),
            hover_data=["Project","Regulatory_Status"],
            labels={"Revenue_Pending":"Revenue (₹)","Slab_Percent":"Slab %"},
        )
        return answer, result[["Project","Tower","Slab_Percent","Revenue_Pending","Regulatory_Status"]], _fig(fig)

    elif intent == "delayed_towers":
        result = df[df["Days_Delayed"] > 0].sort_values("Days_Delayed", ascending=False)
        if result.empty:
            return "No towers are currently delayed. Portfolio is on schedule.", None, None
        answer = (
            f"**{len(result)} tower(s)** are delayed.  \n"
            f"**Worst:** Tower {result.iloc[0]['Tower']} — {result.iloc[0]['Days_Delayed']} days behind schedule."
        )
        fig = px.bar(
            result, x="Tower", y="Days_Delayed",
            color="Days_Delayed", color_continuous_scale=["#C9A84C","#F43F5E"],
            title="Delayed Towers — Days Behind Schedule",
            text="Days_Delayed", hover_data=["Project"],
            labels={"Days_Delayed":"Days Delayed"},
        )
        return answer, result[["Project","Tower","Slab_Percent","Days_Delayed","Regulatory_Status"]], _fig(fig)

    elif intent == "revenue_analysis":
        grp = df.groupby("Project")["Revenue_Pending"].sum().reset_index().sort_values("Revenue_Pending", ascending=False)
        total = df["Revenue_Pending"].sum()
        answer = (
            f"**Total Portfolio Revenue Pending:** {fmt_crore(total)}  \n"
            f"**Top Project:** {grp.iloc[0]['Project']} — {fmt_crore(grp.iloc[0]['Revenue_Pending'])}"
        )
        fig = px.bar(
            grp, x="Project", y="Revenue_Pending",
            color="Revenue_Pending", color_continuous_scale=["#1a2744","#C9A84C"],
            title="Revenue Pending by Project",
            text=grp["Revenue_Pending"].apply(fmt_crore),
            labels={"Revenue_Pending":"Revenue (₹)"},
        )
        return answer, grp, _fig(fig)

    elif intent == "regulatory_status":
        sc = df["Regulatory_Status"].value_counts().reset_index()
        sc.columns = ["Status","Count"]
        answer = (
            f"**Regulatory Status across {len(df)} towers:**  \n"
            + "  \n".join(f"— **{r['Status']}:** {r['Count']} towers" for _, r in sc.iterrows())
        )
        fig = px.pie(
            sc, names="Status", values="Count",
            color_discrete_sequence=["#10B981","#C9A84C","#F43F5E"],
            title="Regulatory Status Distribution", hole=0.5,
        )
        fig.update_traces(textfont_color="#D4D9E0", textfont_size=12)
        return answer, df[["Project","Tower","Regulatory_Status"]], _fig(fig)

    elif intent == "progress_overview":
        result = df.sort_values("Slab_Percent", ascending=False)
        avg = df["Slab_Percent"].mean()
        answer = (
            f"**Portfolio Average Slab Completion:** {avg:.1f}%  \n"
            f"**Leading:** {result.iloc[0]['Tower']} ({result.iloc[0]['Slab_Percent']}%)  |  "
            f"**Lagging:** {result.iloc[-1]['Tower']} ({result.iloc[-1]['Slab_Percent']}%)"
        )
        fig = px.bar(
            result, x="Tower", y="Slab_Percent",
            color="Slab_Percent", color_continuous_scale=["#F43F5E","#C9A84C","#10B981"],
            title="Construction Slab Completion — All Towers",
            text="Slab_Percent", hover_data=["Project"],
            labels={"Slab_Percent":"Slab %"},
        )
        fig.add_hline(y=90, line_dash="dot", line_color="#C9A84C",
                      annotation_text="Collection Threshold 90%",
                      annotation_font_color="#C9A84C")
        return answer, result, _fig(fig)

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
            grp, x="Avg_Slab", y="Total_Revenue", size="Avg_Delay", color="Project",
            title="Project Comparison: Slab % vs Revenue vs Delay (bubble = delay)",
            labels={"Avg_Slab":"Avg Slab %","Total_Revenue":"Total Revenue Pending"},
            size_max=55, color_discrete_sequence=["#C9A84C","#10B981","#3B82F6","#F43F5E","#A78BFA"],
        )
        return answer, grp, _fig(fig)

    else:
        answer = (
            "I can analyse your DLF portfolio. Try asking:  \n\n"
            "— *Which towers are ready for billing?*  \n"
            "— *Show me delayed towers*  \n"
            "— *What's the pending revenue?*  \n"
            "— *Show construction progress*  \n"
            "— *What's the RERA status?*  \n"
            "— *Compare projects*"
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
    st.markdown("""
    <div style="padding:1.8rem 1rem 1rem;border-bottom:1px solid rgba(201,168,76,0.15);margin-bottom:1.2rem;">
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem;">
            <div style="width:40px;height:40px;background:linear-gradient(135deg,#C9A84C,#7a5e1a);
                        border-radius:10px;display:flex;align-items:center;justify-content:center;
                        font-size:1.25rem;flex-shrink:0;box-shadow:0 4px 12px rgba(201,168,76,0.3);">🐇</div>
            <div>
                <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
                            color:#E8C96A;line-height:1.1;">Talking Rabbitt</div>
                <div style="font-size:0.6rem;color:#3a4d5e;letter-spacing:0.12em;text-transform:uppercase;">
                    Rabbitt AI · MVP</div>
            </div>
        </div>
        <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);
                    border-radius:20px;padding:0.22rem 0.65rem;display:inline-flex;align-items:center;gap:0.4rem;">
            <span style="width:6px;height:6px;background:#10B981;border-radius:50%;display:inline-block;
                         box-shadow:0 0 6px #10B981;animation:pulse 2s infinite;"></span>
            <span style="font-size:0.62rem;color:#10B981;font-weight:600;letter-spacing:0.08em;">SYSTEM ONLINE</span>
        </div>
    </div>
    <style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}</style>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.6rem;color:#3a4d5e;letter-spacing:0.12em;text-transform:uppercase;margin:0 0 0.5rem;">Sample Data</p>', unsafe_allow_html=True)
    st.download_button(
        label="⬇  Download dlf_progress.csv",
        data=generate_sample_csv(),
        file_name="dlf_progress.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.6rem;color:#3a4d5e;letter-spacing:0.12em;text-transform:uppercase;margin:0 0 0.5rem;">Quick Queries</p>', unsafe_allow_html=True)

    example_queries = [
        "Which towers are ready for billing?",
        "Show me delayed towers",
        "What's the pending revenue?",
        "Show construction progress",
        "What's the RERA status?",
        "Compare all projects",
    ]
    for eq in example_queries:
        if st.button(eq, use_container_width=True, key=f"eq_{eq}"):
            st.session_state["prefill_query"] = eq

    if st.session_state.df is not None:
        df_s = st.session_state.df
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(201,168,76,0.25),transparent);margin-bottom:1rem;"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.6rem;color:#3a4d5e;letter-spacing:0.12em;text-transform:uppercase;margin:0 0 0.6rem;">Portfolio Snapshot</p>', unsafe_allow_html=True)

        for icon, label, val in [
            ("🏙", "Projects", df_s['Project'].nunique()),
            ("🏢", "Towers", len(df_s)),
            ("✅", "Ready (>90%)", len(df_s[df_s["Slab_Percent"]>90])),
            ("⚠️", "Delayed", len(df_s[df_s["Days_Delayed"]>0])),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span style="font-size:0.78rem;color:#5a6678;">{icon} {label}</span>
                <span style="font-family:'Playfair Display',serif;font-size:0.95rem;
                             color:#C9A84C;font-weight:700;">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:0.75rem;background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.18);
                    border-radius:10px;padding:0.75rem;text-align:center;">
            <div style="font-size:0.58rem;color:#3a4d5e;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.2rem;">
                Total Revenue Pending</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.25rem;color:#E8C96A;font-weight:700;">
                {fmt_crore(df_s["Revenue_Pending"].sum())}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:2rem;text-align:center;">
        <div style="font-size:0.58rem;color:#1e2a38;letter-spacing:0.06em;">
            Built for DLF Limited · © 2025 Rabbitt AI
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:0.25rem;">
    <div>
        <div style="font-size:0.6rem;color:#3a4d5e;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:0.3rem;">
            DLF Limited · Construction Analytics
        </div>
        <h1 style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:800;
                   color:#D4D9E0;margin:0;line-height:1.1;">
            Portfolio Intelligence<span style="color:#C9A84C;">.</span>
        </h1>
    </div>
    <div style="text-align:right;padding-bottom:0.2rem;">
        <div style="font-size:0.6rem;color:#3a4d5e;margin-bottom:0.15rem;">Powered by</div>
        <div style="font-family:'Playfair Display',serif;font-size:0.95rem;color:#C9A84C;font-weight:700;">
            Rabbitt AI</div>
    </div>
</div>
<div style="height:1px;background:linear-gradient(90deg,rgba(201,168,76,0.6),rgba(201,168,76,0.1),transparent);
            margin-bottom:1.5rem;"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UPLOAD STATE
# ─────────────────────────────────────────────
if st.session_state.df is None:
    st.markdown("""
    <div class="welcome-hero">
        <div style="font-size:2.8rem;margin-bottom:0.75rem;">🏗️</div>
        <div class="welcome-title">Welcome to Talking Rabbitt</div>
        <div class="welcome-sub">
            Upload your DLF construction site data to unlock conversational intelligence.
            Ask questions in plain English — get instant charts and insights.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    col_up, col_hint = st.columns([3, 2])

    with col_up:
        st.markdown('<p style="font-size:0.6rem;color:#3a4d5e;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">Upload CSV</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Drop CSV", type=["csv"], label_visibility="collapsed",
            help="Download the sample file from the sidebar",
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
                    st.success(f"✅ Loaded {len(df)} towers across {df['Project'].nunique()} projects.")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    with col_hint:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:0.6rem;color:#3a4d5e;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.75rem;">
                Required Columns
            </div>
            <div style="font-size:0.82rem;color:#8B95A3;line-height:2.2;">
                <span style="color:#C9A84C;margin-right:0.5rem;">▸</span>Project<br>
                <span style="color:#C9A84C;margin-right:0.5rem;">▸</span>Tower<br>
                <span style="color:#C9A84C;margin-right:0.5rem;">▸</span>Slab_Percent<br>
                <span style="color:#C9A84C;margin-right:0.5rem;">▸</span>Revenue_Pending<br>
                <span style="color:#C9A84C;margin-right:0.5rem;">▸</span>Days_Delayed<br>
                <span style="color:#C9A84C;margin-right:0.5rem;">▸</span>Regulatory_Status
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHAT INTERFACE
# ─────────────────────────────────────────────
else:
    df = st.session_state.df

    ready_count   = len(df[df["Slab_Percent"] > 90])
    delayed_count = len(df[df["Days_Delayed"] > 0])
    total_rev     = df["Revenue_Pending"].sum()
    avg_slab      = df["Slab_Percent"].mean()

    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-tile">
            <div class="metric-val">{df['Project'].nunique()}</div>
            <div class="metric-lbl">Projects</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val">{len(df)}</div>
            <div class="metric-lbl">Towers</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val" style="color:#10B981;">{ready_count}</div>
            <div class="metric-lbl">Ready to Bill</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val" style="color:#F43F5E;">{delayed_count}</div>
            <div class="metric-lbl">Delayed</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val" style="font-size:1.2rem;">{fmt_crore(total_rev)}</div>
            <div class="metric-lbl">Revenue Pending</div>
        </div>
        <div class="metric-tile">
            <div class="metric-val">{avg_slab:.0f}%</div>
            <div class="metric-lbl">Avg Slab</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.6rem;color:#3a4d5e;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.75rem;">Conversation</p>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:2.5rem 1.5rem;">
            <div style="font-size:1.8rem;margin-bottom:0.6rem;color:#C9A84C;">✦</div>
            <div style="font-family:'Playfair Display',serif;font-size:1rem;color:#C9A84C;margin-bottom:0.4rem;">
                Ask me anything about your portfolio</div>
            <div style="font-size:0.82rem;color:#3a4d5e;max-width:380px;margin:0 auto;">
                Use the quick queries in the sidebar or type your own question below</div>
        </div>
        """, unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="bubble-user">
                <div class="bubble-user-inner">
                    <div class="bubble-user-name">You</div>
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bubble-ai">
                <div class="bubble-ai-inner">
                    <div class="bubble-ai-name">🐇 Rabbitt AI</div>
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

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    prefill = st.session_state.pop("prefill_query", "")

    col_q, col_send = st.columns([6, 1])
    with col_q:
        query = st.text_input(
            "query", value=prefill,
            placeholder="Ask about billing readiness, delays, revenue, RERA status…",
            label_visibility="collapsed", key="chat_input",
        )
    with col_send:
        submit = st.button("Ask  →", use_container_width=True)

    if submit and query.strip():
        with st.spinner("Analysing…"):
            answer, df_result, fig = answer_query(df, query)
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({
            "role": "assistant", "content": answer,
            "df_result": df_result, "fig": fig,
        })
        st.rerun()

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    col_a, col_b, _ = st.columns([1.3, 1.5, 5])
    with col_a:
        if st.button("🗑  Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with col_b:
        if st.button("📤  New Dataset", use_container_width=True):
            st.session_state.df = None
            st.session_state.chat_history = []
            st.rerun()
