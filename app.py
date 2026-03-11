"""
Talking Rabbitt - Conversational Intelligence MVP
Target Customer: DLF Limited (India's Largest Real Estate Developer)
Built for: Rabbitt AI Assessment
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import os

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
# CUSTOM CSS — Navy Blue Professional Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Root Variables ── */
    :root {
        --navy:      #0A1628;
        --navy-mid:  #122040;
        --navy-card: #1A2E50;
        --accent:    #00C2FF;
        --accent2:   #FFB800;
        --text:      #E8EEF8;
        --muted:     #8A9BB5;
        --success:   #00E5A0;
        --danger:    #FF4F6B;
    }

    /* ── Global ── */
    html, body, [class*="css"] {
        background-color: var(--navy) !important;
        color: var(--text) !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--navy-mid) !important;
        border-right: 1px solid rgba(0,194,255,0.15);
    }

    /* ── Main area ── */
    .main .block-container {
        padding-top: 1.5rem;
        background: var(--navy);
    }

    /* ── Cards ── */
    .card {
        background: var(--navy-card);
        border: 1px solid rgba(0,194,255,0.15);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── Metric boxes ── */
    .metric-row { display: flex; gap: 1rem; margin-bottom: 1rem; }
    .metric-box {
        flex: 1;
        background: var(--navy-card);
        border: 1px solid rgba(0,194,255,0.2);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        text-align: center;
    }
    .metric-box .val {
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent);
    }
    .metric-box .lbl {
        font-size: 0.75rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ── Section headers ── */
    .section-title {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        color: var(--accent);
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    /* ── Chat messages ── */
    .chat-user {
        background: rgba(0,194,255,0.1);
        border: 1px solid rgba(0,194,255,0.25);
        border-radius: 12px 12px 2px 12px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: var(--text);
    }
    .chat-ai {
        background: rgba(26,46,80,0.9);
        border: 1px solid rgba(255,184,0,0.2);
        border-radius: 2px 12px 12px 12px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: var(--text);
    }
    .chat-label {
        font-size: 0.65rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .chat-label.user { color: var(--accent); }
    .chat-label.ai   { color: var(--accent2); }

    /* ── Badge ── */
    .badge {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .badge-green  { background: rgba(0,229,160,0.15); color: var(--success); border: 1px solid rgba(0,229,160,0.3); }
    .badge-yellow { background: rgba(255,184,0,0.15);  color: var(--accent2); border: 1px solid rgba(255,184,0,0.3); }
    .badge-red    { background: rgba(255,79,107,0.15);  color: var(--danger);  border: 1px solid rgba(255,79,107,0.3); }

    /* ── Streamlit overrides ── */
    .stTextInput > div > div > input {
        background: var(--navy-card) !important;
        border: 1px solid rgba(0,194,255,0.3) !important;
        color: var(--text) !important;
        border-radius: 8px;
    }
    .stButton > button {
        background: var(--accent) !important;
        color: var(--navy) !important;
        font-weight: 700;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover { opacity: 0.85; }
    .stDataFrame { border-radius: 8px; overflow: hidden; }
    div[data-testid="stFileUploader"] {
        background: var(--navy-card);
        border: 1px dashed rgba(0,194,255,0.35);
        border-radius: 10px;
        padding: 0.5rem;
    }
    .stSelectbox > div > div {
        background: var(--navy-card) !important;
        border-color: rgba(0,194,255,0.3) !important;
        color: var(--text) !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SAMPLE DATA GENERATOR
# ─────────────────────────────────────────────
def generate_sample_csv() -> bytes:
    """Generate a realistic DLF construction site CSV for demo purposes."""
    data = {
        "Project": [
            "DLF One Midtown", "DLF One Midtown", "DLF One Midtown",
            "The Camellias", "The Camellias",
            "DLF 5", "DLF 5", "DLF 5",
            "Privana West", "Privana West", "Privana West", "Privana West",
            "The Arbour", "The Arbour",
        ],
        "Tower": [
            "T1", "T2", "T3",
            "CA", "CB",
            "D5A", "D5B", "D5C",
            "PW1", "PW2", "PW3", "PW4",
            "AR1", "AR2",
        ],
        "Slab_Percent": [96, 88, 72, 99, 91, 55, 63, 44, 93, 78, 85, 97, 34, 61],
        "Revenue_Pending": [
            42_00_00_000, 38_50_00_000, 29_75_00_000,
            85_00_00_000, 76_20_00_000,
            18_30_00_000, 22_10_00_000, 14_60_00_000,
            31_50_00_000, 27_80_00_000, 33_20_00_000, 29_10_00_000,
            9_40_00_000,  16_70_00_000,
        ],
        "Days_Delayed": [12, 0, 45, 5, 0, 90, 60, 120, 8, 30, 15, 0, 180, 75],
        "Regulatory_Status": [
            "RERA Approved", "RERA Approved", "Pending NOC",
            "OC Received", "RERA Approved",
            "Pending NOC", "RERA Approved", "Pending NOC",
            "RERA Approved", "OC Received", "RERA Approved", "OC Received",
            "Pending NOC", "RERA Approved",
        ],
    }
    df = pd.DataFrame(data)
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()


# ─────────────────────────────────────────────
# NLP QUERY ENGINE
# ─────────────────────────────────────────────
def classify_query(query: str) -> str:
    """Simple keyword-based intent classifier."""
    q = query.lower()
    if any(k in q for k in ["ready", "billing", "collection", "complete", "handover", "done"]):
        return "ready_for_collection"
    if any(k in q for k in ["delay", "late", "behind", "overdue", "slow"]):
        return "delayed_towers"
    if any(k in q for k in ["revenue", "pending", "money", "amount", "value", "crore"]):
        return "revenue_analysis"
    if any(k in q for k in ["regulatory", "rera", "noc", "oc", "approval", "status"]):
        return "regulatory_status"
    if any(k in q for k in ["progress", "slab", "percent", "construction", "overview", "summary"]):
        return "progress_overview"
    if any(k in q for k in ["project", "compare", "comparison", "best", "worst"]):
        return "project_comparison"
    return "general"


def fmt_crore(val: float) -> str:
    """Format a number in Indian Crore notation."""
    cr = val / 1_00_00_000
    return f"₹{cr:.1f} Cr"


def answer_query(df: pd.DataFrame, query: str):
    """
    Core intelligence engine.
    Returns (answer_text, result_df_or_None, fig_or_None).
    """
    intent = classify_query(query)

    # ── Ready for Collection ──────────────────
    if intent == "ready_for_collection":
        threshold = 90
        result = df[df["Slab_Percent"] > threshold].copy()
        result = result.sort_values("Revenue_Pending", ascending=False)
        total_rev = result["Revenue_Pending"].sum()
        answer = (
            f"**{len(result)} tower(s)** have slab completion above {threshold}% "
            f"and are ready for billing/collection.\n\n"
            f"**Total Revenue Pending:** {fmt_crore(total_rev)}"
        )
        if result.empty:
            return "No towers currently exceed the 90% slab completion threshold.", None, None

        fig = px.bar(
            result, x="Tower", y="Revenue_Pending",
            color="Slab_Percent",
            color_continuous_scale=["#0A4A7C", "#00C2FF", "#00E5A0"],
            labels={"Revenue_Pending": "Revenue Pending (₹)", "Slab_Percent": "Slab %"},
            title="🏗️ Towers Ready for Collection — Revenue Pending",
            text=result["Revenue_Pending"].apply(fmt_crore),
            hover_data=["Project", "Regulatory_Status"],
        )
        fig = _style_fig(fig)
        return answer, result[["Project","Tower","Slab_Percent","Revenue_Pending","Regulatory_Status"]], fig

    # ── Delayed Towers ────────────────────────
    elif intent == "delayed_towers":
        result = df[df["Days_Delayed"] > 0].sort_values("Days_Delayed", ascending=False)
        avg_delay = result["Days_Delayed"].mean()
        answer = (
            f"**{len(result)} tower(s)** are experiencing delays.\n\n"
            f"**Average Delay:** {avg_delay:.0f} days | "
            f"**Worst offender:** Tower {result.iloc[0]['Tower']} ({result.iloc[0]['Days_Delayed']} days)"
        )
        if result.empty:
            return "Great news — no towers are currently delayed!", None, None

        fig = px.bar(
            result, x="Tower", y="Days_Delayed",
            color="Days_Delayed",
            color_continuous_scale=["#FFB800","#FF4F6B"],
            title="⚠️ Delayed Towers — Days Behind Schedule",
            text="Days_Delayed",
            hover_data=["Project"],
        )
        fig = _style_fig(fig)
        return answer, result[["Project","Tower","Slab_Percent","Days_Delayed","Regulatory_Status"]], fig

    # ── Revenue Analysis ──────────────────────
    elif intent == "revenue_analysis":
        by_project = df.groupby("Project")["Revenue_Pending"].sum().reset_index()
        by_project = by_project.sort_values("Revenue_Pending", ascending=False)
        total = df["Revenue_Pending"].sum()
        top = by_project.iloc[0]
        answer = (
            f"**Total Portfolio Revenue Pending:** {fmt_crore(total)}\n\n"
            f"**Highest:** {top['Project']} at {fmt_crore(top['Revenue_Pending'])}"
        )
        fig = px.bar(
            by_project, x="Project", y="Revenue_Pending",
            color="Revenue_Pending",
            color_continuous_scale=["#1A2E50","#00C2FF"],
            title="💰 Revenue Pending by Project",
            text=by_project["Revenue_Pending"].apply(fmt_crore),
        )
        fig = _style_fig(fig)
        return answer, by_project, fig

    # ── Regulatory Status ─────────────────────
    elif intent == "regulatory_status":
        status_counts = df["Regulatory_Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        answer = (
            f"**Regulatory breakdown across {len(df)} towers:**\n\n"
            + "\n".join(f"- **{row['Status']}:** {row['Count']} towers"
                        for _, row in status_counts.iterrows())
        )
        fig = px.pie(
            status_counts, names="Status", values="Count",
            color_discrete_sequence=["#00E5A0","#00C2FF","#FF4F6B"],
            title="📋 Regulatory Status Distribution",
            hole=0.45,
        )
        fig = _style_fig(fig)
        return answer, df[["Project","Tower","Regulatory_Status"]], fig

    # ── Progress Overview ─────────────────────
    elif intent == "progress_overview":
        result = df.sort_values("Slab_Percent", ascending=False)
        avg = df["Slab_Percent"].mean()
        answer = (
            f"**Portfolio Average Slab Completion:** {avg:.1f}%\n\n"
            f"**Leading tower:** {result.iloc[0]['Tower']} ({result.iloc[0]['Slab_Percent']}%) | "
            f"**Lagging tower:** {result.iloc[-1]['Tower']} ({result.iloc[-1]['Slab_Percent']}%)"
        )
        fig = px.bar(
            result, x="Tower", y="Slab_Percent",
            color="Slab_Percent",
            color_continuous_scale=["#FF4F6B","#FFB800","#00E5A0"],
            title="📊 Slab Completion Progress — All Towers",
            text="Slab_Percent",
            hover_data=["Project","Revenue_Pending"],
        )
        fig.add_hline(y=90, line_dash="dash", line_color="#00C2FF",
                      annotation_text="Collection Threshold (90%)")
        fig = _style_fig(fig)
        return answer, result, fig

    # ── Project Comparison ────────────────────
    elif intent == "project_comparison":
        grp = df.groupby("Project").agg(
            Avg_Slab=("Slab_Percent","mean"),
            Total_Revenue=("Revenue_Pending","sum"),
            Avg_Delay=("Days_Delayed","mean"),
        ).reset_index().sort_values("Avg_Slab", ascending=False)
        answer = (
            f"**Project Performance Comparison ({len(grp)} projects):**\n\n"
            f"Top performer: **{grp.iloc[0]['Project']}** — "
            f"{grp.iloc[0]['Avg_Slab']:.1f}% avg slab completion"
        )
        fig = px.scatter(
            grp, x="Avg_Slab", y="Total_Revenue",
            size="Avg_Delay", color="Project",
            title="🔍 Project Comparison: Slab % vs Revenue vs Delay",
            labels={"Avg_Slab": "Avg Slab %", "Total_Revenue": "Total Revenue Pending"},
            size_max=50,
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig = _style_fig(fig)
        return answer, grp, fig

    # ── General / Fallback ────────────────────
    else:
        answer = (
            "I can help you with:\n\n"
            "- **Collection readiness** — *'Which towers are ready for billing?'*\n"
            "- **Delays** — *'Show me delayed towers'*\n"
            "- **Revenue** — *'What's the pending revenue?'*\n"
            "- **Regulatory** — *'What's the RERA status?'*\n"
            "- **Progress** — *'Show construction progress'*\n"
            "- **Comparison** — *'Compare projects'*\n\n"
            "Please try one of the above queries or rephrase your question."
        )
        return answer, None, None


def _style_fig(fig):
    """Apply consistent dark Navy theme to all Plotly figures."""
    fig.update_layout(
        plot_bgcolor="#0A1628",
        paper_bgcolor="#122040",
        font=dict(color="#E8EEF8", family="Segoe UI"),
        title_font=dict(size=15, color="#00C2FF"),
        coloraxis_colorbar=dict(tickfont=dict(color="#8A9BB5")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#8A9BB5")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#8A9BB5")),
        margin=dict(t=50, l=20, r=20, b=40),
    )
    fig.update_traces(textfont_color="#0A1628")
    return fig


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
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
        <div style="font-size:2.5rem;">🐇</div>
        <div style="font-size:1.3rem; font-weight:800; color:#00C2FF; letter-spacing:0.05em;">
            TALKING RABBITT
        </div>
        <div style="font-size:0.7rem; color:#8A9BB5; letter-spacing:0.15em; text-transform:uppercase;">
            Conversational Intelligence
        </div>
        <div style="margin-top:0.5rem; padding:0.3rem 0.8rem; background:rgba(0,194,255,0.1);
                    border:1px solid rgba(0,194,255,0.25); border-radius:20px;
                    font-size:0.65rem; color:#00C2FF; display:inline-block;">
            Rabbitt AI — Assessment MVP
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📥 Sample Data</div>', unsafe_allow_html=True)
    st.download_button(
        label="⬇️ Download dlf_progress.csv",
        data=generate_sample_csv(),
        file_name="dlf_progress.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown('<div class="section-title">💡 Example Queries</div>', unsafe_allow_html=True)
    example_queries = [
        "Which towers are ready for billing?",
        "Show me delayed towers",
        "What's the pending revenue?",
        "Show construction progress",
        "What's the RERA status?",
        "Compare projects",
    ]
    for eq in example_queries:
        if st.button(eq, use_container_width=True, key=f"eq_{eq}"):
            st.session_state["prefill_query"] = eq

    st.markdown("---")
    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown('<div class="section-title">📊 Dataset Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:0.8rem; color:#8A9BB5; line-height:2;">
            🏗️ <b style="color:#E8EEF8">{df['Project'].nunique()}</b> Projects<br>
            🏢 <b style="color:#E8EEF8">{len(df)}</b> Towers<br>
            💰 <b style="color:#00C2FF">{fmt_crore(df['Revenue_Pending'].sum())}</b> Revenue<br>
            📈 <b style="color:#00E5A0">{df['Slab_Percent'].mean():.1f}%</b> Avg. Slab
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.65rem; color:#3A4D6A; text-align:center; line-height:1.8;">
        Powered by <b style="color:#8A9BB5">Rabbitt AI</b><br>
        Built for DLF Limited<br>
        © 2025 — Assessment MVP
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN AREA — HEADER
# ─────────────────────────────────────────────
col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown("""
    <h1 style="font-size:1.8rem; font-weight:800; color:#E8EEF8; margin:0 0 0.25rem;">
        DLF Construction Intelligence
    </h1>
    <p style="color:#8A9BB5; font-size:0.9rem; margin:0;">
        Ask natural language questions about your construction portfolio
    </p>
    """, unsafe_allow_html=True)
with col_badge:
    st.markdown("""
    <div style="text-align:right; padding-top:0.5rem;">
        <span class="badge badge-green">● Live</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FILE UPLOADER
# ─────────────────────────────────────────────
if st.session_state.df is None:
    st.markdown('<div class="section-title">📂 Upload Data</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload your DLF construction CSV",
        type=["csv"],
        help="Download the sample file from the sidebar to get started instantly",
    )
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            required = {"Project","Tower","Slab_Percent","Revenue_Pending","Days_Delayed","Regulatory_Status"}
            missing = required - set(df.columns)
            if missing:
                st.error(f"Missing columns: {', '.join(missing)}. Download the sample CSV to see the expected format.")
            else:
                st.session_state.df = df
                st.success(f"✅ Loaded **{len(df)} towers** across **{df['Project'].nunique()} projects**. Start asking questions below!")
                st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {e}")

    st.markdown("""
    <div class="card" style="text-align:center; padding:2rem;">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🏗️</div>
        <div style="color:#8A9BB5; font-size:0.9rem;">
            Upload a CSV or download the sample file from the sidebar to get started
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHAT INTERFACE (only when data is loaded)
# ─────────────────────────────────────────────
else:
    df = st.session_state.df

    # ── KPI Metrics Row ──────────────────────
    ready_count = len(df[df["Slab_Percent"] > 90])
    delayed_count = len(df[df["Days_Delayed"] > 0])
    total_rev = df["Revenue_Pending"].sum()
    avg_slab = df["Slab_Percent"].mean()

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box">
            <div class="val">{df['Project'].nunique()}</div>
            <div class="lbl">Projects</div>
        </div>
        <div class="metric-box">
            <div class="val">{len(df)}</div>
            <div class="lbl">Towers</div>
        </div>
        <div class="metric-box">
            <div class="val" style="color:#00E5A0">{ready_count}</div>
            <div class="lbl">Ready for Collection</div>
        </div>
        <div class="metric-box">
            <div class="val" style="color:#FF4F6B">{delayed_count}</div>
            <div class="lbl">Towers Delayed</div>
        </div>
        <div class="metric-box">
            <div class="val" style="color:#FFB800">{fmt_crore(total_rev)}</div>
            <div class="lbl">Total Revenue Pending</div>
        </div>
        <div class="metric-box">
            <div class="val">{avg_slab:.0f}%</div>
            <div class="lbl">Avg. Slab Completion</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Chat History ──────────────────────────
    st.markdown('<div class="section-title">💬 Conversation</div>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="card" style="text-align:center; padding:1.5rem;">
            <div style="font-size:1.5rem; margin-bottom:0.5rem;">🤖</div>
            <div style="color:#8A9BB5; font-size:0.9rem;">
                Hi! I'm your DLF construction analyst. Ask me anything about your portfolio.
            </div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-user">
                <div class="chat-label user">You</div>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-ai">
                <div class="chat-label ai">🐇 Rabbitt AI</div>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
            if "df_result" in msg and msg["df_result"] is not None:
                res = msg["df_result"].copy()
                # Format Revenue column if present
                if "Revenue_Pending" in res.columns:
                    res["Revenue_Pending"] = res["Revenue_Pending"].apply(fmt_crore)
                st.dataframe(res, use_container_width=True, hide_index=True)
            if "fig" in msg and msg["fig"] is not None:
                st.plotly_chart(msg["fig"], use_container_width=True)

    # ── Query Input ───────────────────────────
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    prefill = st.session_state.pop("prefill_query", "")

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            "Ask a question",
            value=prefill,
            placeholder="e.g. Which towers are ready for billing?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with col_btn:
        submit = st.button("Ask →", use_container_width=True)

    if submit and query.strip():
        with st.spinner("Analysing..."):
            answer, df_result, fig = answer_query(df, query)

        # Store in history
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "df_result": df_result,
            "fig": fig,
        })
        st.rerun()

    # ── Clear Chat ────────────────────────────
    col_a, col_b = st.columns([4, 1])
    with col_b:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with col_a:
        if st.button("📤 Change Dataset", use_container_width=True):
            st.session_state.df = None
            st.session_state.chat_history = []
            st.rerun()
