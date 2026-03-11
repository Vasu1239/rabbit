import streamlit as st
import pandas as pd
import numpy as np
import os

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Talking Rabbitt · DLF Analytics",
    page_icon="🐇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS: Navy / Dark theme ────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Font ---- */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0B1526;
    color: #E8EDF5;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1F3C 0%, #091629 100%);
    border-right: 1px solid #1E3A5F;
}
section[data-testid="stSidebar"] * { color: #C8D8F0 !important; }

/* Main area background */
.main .block-container {
    background-color: #0B1526;
    padding-top: 2rem;
}

/* Headings */
h1, h2, h3 { font-family: 'DM Serif Display', serif; color: #FFFFFF; }

/* Cards */
.metric-card {
    background: linear-gradient(135deg, #112244 0%, #0D1F3C 100%);
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}
.metric-card .label { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em;
                       text-transform: uppercase; color: #6B8FBF; }
.metric-card .value { font-size: 1.8rem; font-weight: 700; color: #FFFFFF; margin-top: 2px; }

/* Answer box */
.answer-box {
    background: linear-gradient(135deg, #0F2847 0%, #112040 100%);
    border-left: 4px solid #3B82F6;
    border-radius: 0 12px 12px 0;
    padding: 1.4rem 1.8rem;
    margin: 1rem 0;
    font-size: 1.05rem;
    line-height: 1.7;
    color: #D6E4FF;
}

/* Input box */
.stTextInput > div > div > input {
    background-color: #112244 !important;
    border: 1px solid #1E3A5F !important;
    color: #E8EDF5 !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1.4rem;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(59,130,246,0.4);
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #1E3A5F;
    border-radius: 12px;
    background-color: #0D1F3C;
}

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; }

/* Divider */
hr { border-color: #1E3A5F; }

/* Spinner */
.stSpinner > div { border-top-color: #3B82F6 !important; }

/* Tab style */
.stTabs [data-baseweb="tab-list"] { background-color: #0D1F3C; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: #6B8FBF; border-radius: 6px; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #1D4ED8; color: white; }

/* Rabbit logo pulse */
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.6} }
.logo-pulse { animation: pulse 3s ease-in-out infinite; }

/* Badge */
.badge {
    display: inline-block;
    background: rgba(59,130,246,0.2);
    color: #93C5FD;
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar Branding ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.5rem 0 1rem 0;'>
        <div style='font-size:3rem; margin-bottom:0.3rem;' class='logo-pulse'>🐇</div>
        <div style='font-family:"DM Serif Display",serif; font-size:1.6rem;
                    color:#FFFFFF; letter-spacing:-0.02em;'>Talking Rabbitt</div>
        <div style='color:#6B8FBF; font-size:0.8rem; margin-top:2px;'>
            Powered by LangChain · OpenAI
        </div>
        <div style='margin-top:0.6rem;'><span class='badge'>DLF Analytics MVP</span></div>
    </div>
    <hr style='border-color:#1E3A5F; margin: 1rem 0;'>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Your key is never stored — only used for this session.",
    )

    st.markdown("<hr style='border-color:#1E3A5F;'>", unsafe_allow_html=True)
    st.markdown("### 💡 Sample Questions")
    sample_qs = [
        "Which project has the highest pending revenue?",
        "Show total Sales_Q1 by Region",
        "How many units are under construction?",
        "Compare Q1 vs Q2 sales per Tower",
        "Which region underperformed in Q2?",
    ]
    for q in sample_qs:
        st.markdown(f"<div style='color:#93C5FD; font-size:0.83rem; padding:4px 0;'>→ {q}</div>",
                    unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#3B5278; font-size:0.72rem; text-align:center;'>"
        "Talking Rabbitt v1.0 · Sprint MVP<br>Built for DLF Executive Suite</div>",
        unsafe_allow_html=True,
    )


# ── Sample data generator ────────────────────────────────────────────────────
def generate_sample_data() -> pd.DataFrame:
    np.random.seed(42)
    projects   = ["Camellias", "Privana", "Magnolias", "Ultima", "The Crest",
                  "Aralias", "Ireo Victory", "Kings Court", "Skycourt", "The Grove"]
    towers     = [f"T{i}" for i in range(1, 11)]
    regions    = ["NCR", "Mumbai", "Chennai", "Bangalore", "Hyderabad"]
    statuses   = ["Ready to Move", "Under Construction", "Pre-Launch", "Sold Out"]

    records = []
    for i, proj in enumerate(projects):
        q1 = np.random.randint(12, 95) * 10
        q2 = int(q1 * np.random.uniform(0.7, 1.4))
        records.append({
            "Project":  proj,
            "Tower":    towers[i],
            "Region":   np.random.choice(regions),
            "Status":   np.random.choice(statuses, p=[0.3, 0.4, 0.2, 0.1]),
            "Sales_Q1": q1,
            "Sales_Q2": q2,
            "Pending_Revenue_Cr": round(np.random.uniform(25, 420), 1),
            "Units_Sold": np.random.randint(40, 300),
        })
    return pd.DataFrame(records)


# ── Chart auto-selector ───────────────────────────────────────────────────────
def auto_chart(df: pd.DataFrame, question: str):
    """Heuristically pick chart type and relevant columns from the df + question."""
    q_lower = question.lower()
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    if not num_cols:
        return

    # Prefer grouping column hinted by question
    x_col = None
    for c in cat_cols:
        if c.lower() in q_lower:
            x_col = c
            break
    if x_col is None and cat_cols:
        x_col = cat_cols[0]

    # Which numeric cols to plot — prefer ones mentioned
    y_cols = [c for c in num_cols if c.lower() in q_lower] or num_cols[:3]

    if x_col and len(df) <= 50:
        plot_df = df[[x_col] + y_cols].set_index(x_col)
    else:
        plot_df = df[y_cols].head(20)

    st.markdown("#### 📊 Auto-Generated Visualisation")

    use_line = any(w in q_lower for w in ["trend", "compare", "vs", "over", "quarter", "q1", "q2"])

    if use_line:
        st.line_chart(plot_df, use_container_width=True)
    else:
        st.bar_chart(plot_df, use_container_width=True)


# ── LangChain agent (lazy import so app works even without keys) ──────────────
def run_agent(df: pd.DataFrame, question: str, key: str) -> str:
    try:
        from langchain_experimental.agents import create_pandas_dataframe_agent
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=key,
        )
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=False,
            allow_dangerous_code=True,
            agent_executor_kwargs={"handle_parsing_errors": True},
        )
        system_prefix = (
            "You are a senior real-estate data analyst for DLF, India's leading developer. "
            "Answer the user's question in clear, concise business English. "
            "Be specific — quote exact numbers from the data. "
            "Keep your reply under 5 sentences unless a table is needed. "
            "Never say you cannot answer — always derive an insight."
        )
        result = agent.invoke(system_prefix + "\n\nQuestion: " + question)
        return result.get("output", str(result))

    except ImportError as e:
        return (
            f"⚠️ Missing dependency: `{e.name}`. "
            "Please install requirements: `pip install -r requirements.txt`"
        )
    except Exception as e:
        return f"❌ Agent error: {str(e)}"


# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:0.5rem;'>
    <h1 style='margin-bottom:0;'>Talking Rabbitt <span style='font-size:1.8rem;'>🐇</span></h1>
    <p style='color:#6B8FBF; font-size:1rem; margin-top:0.2rem;'>
        Ask your DLF sales data anything — get instant answers + charts.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Step 1 · Data Source ──────────────────────────────────────────────────────
col_up, col_gen = st.columns([3, 2], gap="large")

with col_up:
    st.markdown("#### 📂 Upload Sales CSV")
    uploaded = st.file_uploader(
        "Drop your CSV here", type=["csv"],
        label_visibility="collapsed",
    )

with col_gen:
    st.markdown("#### 🎲 Or Use Demo Data")
    st.caption("Pre-loaded with 10 DLF projects across 5 regions.")
    gen_btn = st.button("⚡ Generate Sample DLF Data", use_container_width=True)

# ── Resolve dataframe ─────────────────────────────────────────────────────────
df: pd.DataFrame | None = None

if "sample_df" not in st.session_state:
    st.session_state.sample_df = None

if gen_btn:
    st.session_state.sample_df = generate_sample_data()

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.session_state.sample_df = None  # clear sample if real file loaded
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
elif st.session_state.sample_df is not None:
    df = st.session_state.sample_df

# ── Data loaded UI ─────────────────────────────────────────────────────────────
if df is not None:
    st.markdown("---")

    # KPI row
    num_cols = df.select_dtypes(include="number").columns.tolist()
    kpi_cols = st.columns(min(4, len(num_cols) + 1))

    with kpi_cols[0]:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='label'>Total Records</div>
            <div class='value'>{len(df):,}</div>
        </div>""", unsafe_allow_html=True)

    for i, nc in enumerate(num_cols[:3], start=1):
        if i < len(kpi_cols):
            with kpi_cols[i]:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='label'>{nc.replace('_', ' ')}</div>
                    <div class='value'>{df[nc].sum():,.0f}</div>
                </div>""", unsafe_allow_html=True)

    # Data preview tabs
    tab_data, tab_stats = st.tabs(["📋 Data Preview", "📈 Summary Statistics"])
    with tab_data:
        st.dataframe(df, use_container_width=True, height=220)
    with tab_stats:
        st.dataframe(df.describe().round(2), use_container_width=True)

    st.markdown("---")

    # ── Step 2 · Ask a Question ───────────────────────────────────────────────
    st.markdown("#### 💬 Ask Your Question")

    # Quick-pick buttons
    qcols = st.columns(3)
    quick = [
        "Which project has the highest pending revenue?",
        "Show total Sales_Q1 by Region",
        "Compare Q1 vs Q2 sales per Tower",
    ]
    if "prefill" not in st.session_state:
        st.session_state.prefill = ""

    for i, qc in enumerate(qcols):
        with qc:
            if st.button(quick[i], use_container_width=True, key=f"quick_{i}"):
                st.session_state.prefill = quick[i]

    question = st.text_input(
        "Your question",
        value=st.session_state.prefill,
        placeholder="e.g. Which region underperformed in Q2?",
        label_visibility="collapsed",
    )

    ask_btn = st.button("🔍 Ask Talking Rabbitt", use_container_width=False)

    # ── Step 3 · Answer + Chart ───────────────────────────────────────────────
    if ask_btn and question.strip():
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API key in the sidebar to enable AI answers.")
        else:
            with st.spinner("🐇 Rabbitt is thinking…"):
                answer = run_agent(df, question, api_key)

            st.markdown("#### 🤖 Answer")
            st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)

            st.markdown("---")
            auto_chart(df, question)

    elif ask_btn and not question.strip():
        st.info("Please type a question above before clicking Ask.")

else:
    # Empty state
    st.markdown("""
    <div style='text-align:center; padding: 4rem 2rem; color:#3B5278;'>
        <div style='font-size:4rem; margin-bottom:1rem;'>🐇</div>
        <div style='font-size:1.2rem; font-family:"DM Serif Display",serif; color:#6B8FBF;'>
            Upload a CSV or generate sample data to begin
        </div>
        <div style='font-size:0.9rem; margin-top:0.5rem;'>
            Talking Rabbitt will answer your sales questions in seconds.
        </div>
    </div>
    """, unsafe_allow_html=True)
