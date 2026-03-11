"""
Talking Rabbitt — AI-Powered Construction Intelligence
Design: Deep Space Glassmorphism + Animated Aurora + Claude AI
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
import json
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Rabbitt AI",
    page_icon="🐇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DEEP SPACE GLASSMORPHISM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@400;500;700;800;900&family=Instrument+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:       #03040A;
    --glass1:   rgba(255,255,255,0.04);
    --glass2:   rgba(255,255,255,0.07);
    --glass3:   rgba(255,255,255,0.10);
    --border:   rgba(255,255,255,0.08);
    --borderac: rgba(139,92,246,0.4);
    --c1:       #8B5CF6;
    --c2:       #06B6D4;
    --c3:       #F472B6;
    --c4:       #34D399;
    --text:     #E2E8F0;
    --muted:    #64748B;
    --dim:      #1E293B;
}

/* BASE */
html, body, [class*="css"], .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Instrument Sans', sans-serif !important;
}

/* ════════════════════════════════
   ANIMATED AURORA BACKGROUND
════════════════════════════════ */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    background:
        radial-gradient(ellipse 60% 40% at 15% 20%, rgba(139,92,246,0.18) 0%, transparent 65%),
        radial-gradient(ellipse 50% 35% at 85% 75%, rgba(6,182,212,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 40% 50% at 60% 10%, rgba(244,114,182,0.10) 0%, transparent 55%),
        radial-gradient(ellipse 55% 30% at 30% 85%, rgba(52,211,153,0.08) 0%, transparent 50%);
    animation: auroraShift 18s ease-in-out infinite alternate;
    pointer-events: none;
}
@keyframes auroraShift {
    0%   { opacity: 1; transform: scale(1) rotate(0deg); }
    33%  { opacity: 0.85; transform: scale(1.05) rotate(1deg); }
    66%  { opacity: 0.95; transform: scale(0.98) rotate(-1deg); }
    100% { opacity: 1; transform: scale(1.03) rotate(0.5deg); }
}

/* ════════════════════════════════
   FLOATING ORBS
════════════════════════════════ */
.orb-container {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.25;
}
.orb1 {
    width: 350px; height: 350px;
    background: radial-gradient(circle, #8B5CF6, transparent 70%);
    top: -80px; left: -80px;
    animation: floatOrb1 20s ease-in-out infinite;
}
.orb2 {
    width: 280px; height: 280px;
    background: radial-gradient(circle, #06B6D4, transparent 70%);
    bottom: -60px; right: -60px;
    animation: floatOrb2 25s ease-in-out infinite;
}
.orb3 {
    width: 200px; height: 200px;
    background: radial-gradient(circle, #F472B6, transparent 70%);
    top: 40%; right: 10%;
    animation: floatOrb3 30s ease-in-out infinite;
}
.orb4 {
    width: 160px; height: 160px;
    background: radial-gradient(circle, #34D399, transparent 70%);
    bottom: 20%; left: 5%;
    animation: floatOrb4 22s ease-in-out infinite;
}
@keyframes floatOrb1 {
    0%,100% { transform: translate(0,0) scale(1); }
    25%     { transform: translate(60px,80px) scale(1.1); }
    50%     { transform: translate(30px,140px) scale(0.95); }
    75%     { transform: translate(80px,50px) scale(1.05); }
}
@keyframes floatOrb2 {
    0%,100% { transform: translate(0,0) scale(1); }
    30%     { transform: translate(-80px,-60px) scale(1.15); }
    60%     { transform: translate(-40px,-120px) scale(0.9); }
    80%     { transform: translate(-100px,-30px) scale(1.08); }
}
@keyframes floatOrb3 {
    0%,100% { transform: translate(0,0) scale(1); }
    40%     { transform: translate(-60px,80px) scale(1.2); }
    70%     { transform: translate(40px,40px) scale(0.85); }
}
@keyframes floatOrb4 {
    0%,100% { transform: translate(0,0) scale(1); }
    35%     { transform: translate(80px,-50px) scale(1.1); }
    65%     { transform: translate(40px,-100px) scale(0.92); }
}

/* ════════════════════════════════
   PARTICLES (CSS only)
════════════════════════════════ */
.particles {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
}
.particle {
    position: absolute;
    width: 2px; height: 2px;
    background: white;
    border-radius: 50%;
    opacity: 0;
    animation: particleFade var(--dur, 8s) linear var(--delay, 0s) infinite;
}
@keyframes particleFade {
    0%   { opacity: 0; transform: translateY(0) scale(0); }
    10%  { opacity: 0.6; transform: translateY(-20px) scale(1); }
    90%  { opacity: 0.2; transform: translateY(-200px) scale(0.5); }
    100% { opacity: 0; transform: translateY(-220px) scale(0); }
}

/* ════════════════════════════════
   SIDEBAR
════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: rgba(3,4,10,0.85) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ════════════════════════════════
   MAIN CONTENT
════════════════════════════════ */
.main .block-container {
    background: transparent !important;
    padding: 1.5rem 2rem 4rem !important;
    position: relative;
    z-index: 1;
}

/* ════════════════════════════════
   GLASS CARDS
════════════════════════════════ */
.g-card {
    background: var(--glass1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s;
}
.g-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 60%);
    pointer-events: none;
    border-radius: inherit;
}
.g-card:hover {
    border-color: rgba(139,92,246,0.3);
    box-shadow: 0 8px 40px rgba(139,92,246,0.12), inset 0 1px 0 rgba(255,255,255,0.1);
    transform: translateY(-2px);
}

/* ════════════════════════════════
   KPI TILES
════════════════════════════════ */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(6,1fr);
    gap: 0.65rem;
    margin-bottom: 1.75rem;
}
.kpi-tile {
    background: var(--glass1);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1rem 0.75rem 0.9rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
    cursor: default;
}
.kpi-tile::after {
    content:'';
    position:absolute;
    top:0;left:0;right:0;
    height:1px;
    background: linear-gradient(90deg, transparent, var(--c1), var(--c2), transparent);
    opacity:0;
    transition: opacity 0.3s;
}
.kpi-tile:hover {
    border-color: rgba(139,92,246,0.35);
    background: var(--glass2);
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 30px rgba(0,0,0,0.4), 0 0 20px rgba(139,92,246,0.08);
}
.kpi-tile:hover::after { opacity:1; }
.kpi-val {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 1.7rem;
    font-weight: 900;
    color: #fff;
    line-height: 1;
    margin-bottom: 0.3rem;
    letter-spacing: -0.03em;
}
.kpi-lbl {
    font-size: 0.58rem;
    font-weight: 500;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* ════════════════════════════════
   CHAT BUBBLES
════════════════════════════════ */
.chat-user-wrap { display:flex; justify-content:flex-end; margin:0.8rem 0 0.3rem; }
.chat-ai-wrap   { display:flex; justify-content:flex-start; gap:0.6rem; margin:0.3rem 0 0.8rem; align-items:flex-start; }

.chat-bubble-user {
    max-width: 70%;
    background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(6,182,212,0.12));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 20px 20px 4px 20px;
    padding: 0.85rem 1.1rem;
    font-size: 0.9rem;
    color: var(--text);
    line-height: 1.65;
    box-shadow: 0 4px 20px rgba(139,92,246,0.1);
}
.chat-bubble-ai {
    max-width: 80%;
    background: var(--glass1);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: 4px 20px 20px 20px;
    padding: 0.85rem 1.1rem;
    font-size: 0.9rem;
    color: #CBD5E1;
    line-height: 1.65;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.bubble-lbl {
    font-size: 0.57rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.bubble-lbl-user { color: #A78BFA; text-align:right; }
.bubble-lbl-ai   { color: #22D3EE; }

.ai-badge {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #8B5CF6, #06B6D4);
    border-radius: 9px;
    display: flex; align-items:center; justify-content:center;
    font-size: 0.9rem; flex-shrink:0; margin-top:2px;
    box-shadow: 0 0 15px rgba(139,92,246,0.5);
    animation: badgePulse 3s ease-in-out infinite;
}
@keyframes badgePulse {
    0%,100% { box-shadow: 0 0 15px rgba(139,92,246,0.5); }
    50%     { box-shadow: 0 0 25px rgba(6,182,212,0.6); }
}

/* ════════════════════════════════
   HERO / LANDING
════════════════════════════════ */
.hero-wrap {
    background: var(--glass1);
    backdrop-filter: blur(24px);
    border: 1px solid var(--border);
    border-radius: 28px;
    padding: 4rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.hero-wrap::before {
    content:'';
    position:absolute;
    top:-100px; left:50%; transform:translateX(-50%);
    width:400px; height:300px;
    background: radial-gradient(ellipse, rgba(139,92,246,0.15) 0%, transparent 70%);
    animation: heroGlow 6s ease-in-out infinite alternate;
}
@keyframes heroGlow {
    from { opacity:0.5; transform:translateX(-50%) scale(1); }
    to   { opacity:1;   transform:translateX(-50%) scale(1.2); }
}
.hero-eyebrow {
    display: inline-flex; align-items:center; gap:0.5rem;
    background: var(--glass2);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 100px;
    padding: 0.3rem 0.9rem;
    font-size: 0.62rem;
    font-weight: 600;
    color: #A78BFA;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-dot {
    width:6px; height:6px;
    background:#8B5CF6;
    border-radius:50%;
    box-shadow: 0 0 8px #8B5CF6;
    animation: dotPulse 2s ease-in-out infinite;
}
@keyframes dotPulse { 0%,100%{transform:scale(1)}50%{transform:scale(1.5)} }

.hero-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 2.8rem; font-weight: 900;
    line-height: 1.08; letter-spacing: -0.04em;
    color: #fff; margin-bottom: 0.85rem;
}
.hero-title .grad {
    background: linear-gradient(90deg, #8B5CF6, #06B6D4, #F472B6);
    background-size: 200% 100%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradShift 5s linear infinite;
}
@keyframes gradShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero-sub {
    font-size: 0.95rem; color: #64748B; line-height: 1.7;
    max-width: 460px; margin: 0 auto 1.8rem; font-weight: 300;
}

/* ════════════════════════════════
   STREAMLIT OVERRIDES
════════════════════════════════ */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.8rem 1.1rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 4px rgba(139,92,246,0.08), 0 0 20px rgba(139,92,246,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: #334155 !important; }

.stButton > button {
    background: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%) !important;
    color: white !important;
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 12px !important;
    transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
    box-shadow: 0 4px 20px rgba(139,92,246,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.03) !important;
    box-shadow: 0 8px 30px rgba(139,92,246,0.45) !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: var(--glass1) !important;
    color: #94A3B8 !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.78rem !important;
    text-align: left !important;
    transform: none !important;
    letter-spacing: 0 !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--glass2) !important;
    border-color: rgba(139,92,246,0.3) !important;
    color: #C4B5FD !important;
    box-shadow: none !important;
    transform: none !important;
}

.stDownloadButton > button {
    background: var(--glass1) !important;
    color: #22D3EE !important;
    border: 1px solid rgba(6,182,212,0.25) !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: rgba(6,182,212,0.07) !important;
    border-color: rgba(6,182,212,0.5) !important;
    box-shadow: 0 0 20px rgba(6,182,212,0.15) !important;
}

div[data-testid="stFileUploader"] {
    background: var(--glass1) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px dashed rgba(139,92,246,0.3) !important;
    border-radius: 16px !important;
    padding: 0.75rem !important;
    transition: all 0.25s !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: rgba(139,92,246,0.6) !important;
    background: rgba(139,92,246,0.04) !important;
}

.stDataFrame {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}
.stSpinner > div { border-top-color: #8B5CF6 !important; }
.stSuccess {
    background: rgba(52,211,153,0.07) !important;
    border-color: rgba(52,211,153,0.25) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
}
.stError {
    background: rgba(248,113,113,0.07) !important;
    border-color: rgba(248,113,113,0.25) !important;
    border-radius: 12px !important;
}

::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 3px; }
::-webkit-scrollbar-track { background: transparent; }

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
</style>

<!-- ANIMATED BACKGROUND LAYERS -->
<div class="orb-container">
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>
    <div class="orb orb4"></div>
</div>
<div class="particles">
    <div class="particle" style="left:8%;  top:70%; --dur:9s;  --delay:0s;   width:2px; height:2px;"></div>
    <div class="particle" style="left:18%; top:60%; --dur:12s; --delay:1s;   width:1px; height:1px;"></div>
    <div class="particle" style="left:28%; top:80%; --dur:8s;  --delay:2.5s; width:2px; height:2px;"></div>
    <div class="particle" style="left:42%; top:65%; --dur:11s; --delay:0.5s; width:1px; height:1px;"></div>
    <div class="particle" style="left:55%; top:75%; --dur:10s; --delay:3s;   width:2px; height:2px;"></div>
    <div class="particle" style="left:65%; top:55%; --dur:13s; --delay:1.5s; width:1px; height:1px;"></div>
    <div class="particle" style="left:75%; top:85%; --dur:9s;  --delay:4s;   width:2px; height:2px;"></div>
    <div class="particle" style="left:85%; top:60%; --dur:11s; --delay:2s;   width:1px; height:1px;"></div>
    <div class="particle" style="left:92%; top:70%; --dur:8s;  --delay:0.8s; width:2px; height:2px;"></div>
    <div class="particle" style="left:35%; top:90%; --dur:14s; --delay:3.5s; width:1px; height:1px;"></div>
    <div class="particle" style="left:48%; top:45%; --dur:10s; --delay:1.2s; width:2px; height:2px;"></div>
    <div class="particle" style="left:72%; top:40%; --dur:12s; --delay:5s;   width:1px; height:1px;"></div>
</div>
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
# HELPERS
# ─────────────────────────────────────────────
def fmt_crore(val: float) -> str:
    return f"₹{val/1e7:.1f} Cr"

def df_to_context(df: pd.DataFrame) -> str:
    """Convert dataframe to a concise JSON summary for the AI."""
    summary = {
        "total_towers": len(df),
        "projects": df["Project"].unique().tolist(),
        "avg_slab_percent": round(df["Slab_Percent"].mean(), 1),
        "total_revenue_pending_crore": round(df["Revenue_Pending"].sum() / 1e7, 1),
        "towers_above_90pct_slab": df[df["Slab_Percent"] > 90]["Tower"].tolist(),
        "towers_delayed": df[df["Days_Delayed"] > 0][["Tower","Days_Delayed"]].to_dict("records"),
        "regulatory_status_breakdown": df["Regulatory_Status"].value_counts().to_dict(),
        "full_data": df.to_dict("records"),
    }
    return json.dumps(summary, indent=2)


# ─────────────────────────────────────────────
# GEMINI AI QUERY ENGINE
# ─────────────────────────────────────────────
def ask_claude(df: pd.DataFrame, question: str, chat_history: list) -> tuple:
    """
    Send question + full data context to Gemini.
    Returns (answer_text, chart_fig_or_None)
    """
    data_context = df_to_context(df)

    system_prompt = f"""You are Rabbitt AI, an expert construction project analyst assistant with deep knowledge of real estate development, construction timelines, revenue collection, and regulatory compliance.

You have access to the following construction portfolio data:
{data_context}

Your job is to answer ANY question the user asks about this data — from simple lookups to complex analysis, comparisons, predictions, or strategic recommendations.

RULES:
1. Always answer in clear, concise markdown. Use **bold** for key numbers.
2. If you identify towers/projects for a chart, end your response with a special JSON block wrapped in <CHART> tags like this:
   <CHART>{{"type": "bar"|"pie"|"scatter"|"line", "title": "...", "x": [...], "y": [...], "color": [...optional...], "labels": {{"x":"...", "y":"..."}}}}</CHART>
3. For revenue values in your response, express them in Crore (₹X Cr format, where 1 Cr = 10,000,000).
4. Be conversational, insightful, and proactive — point out patterns, risks, or opportunities the user may not have asked about.
5. If asked for predictions or recommendations, give concrete, actionable advice.
6. Never say you "cannot" do something related to this dataset.
"""

    # Build conversation history for Gemini multi-turn
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt,
    )
    history = []
    for h in chat_history[-8:]:
        if h["role"] == "user":
            history.append({"role": "user", "parts": [h["content"]]})
        elif h["role"] == "assistant":
            history.append({"role": "model", "parts": [h["content"]]})
    chat = model.start_chat(history=history)
    response = chat.send_message(question)
    raw = response.text

    # Parse optional chart
    chart_fig = None
    if "<CHART>" in raw and "</CHART>" in raw:
        try:
            chart_json = raw.split("<CHART>")[1].split("</CHART>")[0].strip()
            cd = json.loads(chart_json)
            answer_text = raw.split("<CHART>")[0].strip()

            ctype = cd.get("type", "bar")
            title = cd.get("title", "")
            labels = cd.get("labels", {})

            CHART_STYLE = dict(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#64748B", family="Instrument Sans"),
                title_font=dict(size=13, color="#A78BFA", family="Cabinet Grotesk"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#64748B"), zeroline=False, showline=False),
                yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#64748B"), zeroline=False, showline=False),
                margin=dict(t=44, l=10, r=10, b=32),
                hoverlabel=dict(bgcolor="#0F172A", bordercolor="#8B5CF6", font_color="#E2E8F0", font_family="Instrument Sans"),
            )

            if ctype == "bar":
                fig = go.Figure(go.Bar(
                    x=cd.get("x", []), y=cd.get("y", []),
                    marker=dict(
                        color=cd.get("y", []),
                        colorscale=[[0,"#1E1B4B"],[0.5,"#8B5CF6"],[1,"#06B6D4"]],
                        showscale=False,
                    ),
                    text=[str(v) for v in cd.get("y", [])],
                    textposition="outside",
                    textfont=dict(color="#94A3B8", size=11),
                ))
                fig.update_layout(title=title, xaxis_title=labels.get("x",""), yaxis_title=labels.get("y",""), **CHART_STYLE)

            elif ctype == "pie":
                fig = go.Figure(go.Pie(
                    labels=cd.get("x", []), values=cd.get("y", []),
                    hole=0.52,
                    marker=dict(colors=["#8B5CF6","#06B6D4","#F472B6","#34D399","#FBBF24"],
                                line=dict(color="#03040A", width=2)),
                    textfont=dict(color="#E2E8F0"),
                ))
                fig.update_layout(title=title, **CHART_STYLE)

            elif ctype == "scatter":
                fig = go.Figure(go.Scatter(
                    x=cd.get("x", []), y=cd.get("y", []),
                    mode="markers+text",
                    text=cd.get("x", []),
                    textposition="top center",
                    textfont=dict(color="#94A3B8", size=10),
                    marker=dict(size=14, color="#8B5CF6",
                                line=dict(color="#06B6D4", width=1.5),
                                opacity=0.85),
                ))
                fig.update_layout(title=title, xaxis_title=labels.get("x",""), yaxis_title=labels.get("y",""), **CHART_STYLE)

            else:  # line
                fig = go.Figure(go.Scatter(
                    x=cd.get("x", []), y=cd.get("y", []),
                    mode="lines+markers",
                    line=dict(color="#8B5CF6", width=2.5),
                    marker=dict(size=7, color="#06B6D4"),
                    fill="tozeroy",
                    fillcolor="rgba(139,92,246,0.06)",
                ))
                fig.update_layout(title=title, xaxis_title=labels.get("x",""), yaxis_title=labels.get("y",""), **CHART_STYLE)

            chart_fig = fig
        except Exception:
            answer_text = raw
    else:
        answer_text = raw

    return answer_text, chart_fig



# ─────────────────────────────────────────────
# TEXT-TO-SPEECH ENGINE (Browser Web Speech API)
# ─────────────────────────────────────────────
def speak_text(text: str, msg_index: int):
    """Inject JS to speak text using browser Web Speech API."""
    # Strip markdown symbols for cleaner speech
    clean = text.replace("**","").replace("*","").replace("#","").replace("`","")
    clean = clean.replace("—","").replace("  \n","... ").replace("\n"," ")
    # Escape for JS string
    clean = clean.replace("\\","").replace('"', '\"').replace("'", "\'")
    clean = clean[:800]  # limit length for speech
    js = f"""
    <script>
    (function() {{
        var sid = 'tts_{msg_index}';
        if (window[sid]) {{ window.speechSynthesis.cancel(); window[sid]=false; return; }}
        window[sid] = true;
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance("{clean}");
        u.rate = 1.05; u.pitch = 1.0; u.volume = 1.0;
        // Pick a good voice
        var voices = window.speechSynthesis.getVoices();
        var preferred = voices.find(v => v.name.includes('Google') && v.lang.startsWith('en'))
                     || voices.find(v => v.lang.startsWith('en-') && !v.name.includes('espeak'))
                     || voices[0];
        if (preferred) u.voice = preferred;
        u.onend = function() {{ window[sid]=false; }};
        window.speechSynthesis.speak(u);
    }})();
    </script>
    """
    return js

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
# ── HARDCODED API KEY ──
GOOGLE_API_KEY = "AIzaSyCkRKt76wHxF773AqAv9T0tvc6yhkZyIzQ"

for k, v in [("chat_history", []), ("df", None), ("api_key", GOOGLE_API_KEY)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.6rem 1rem 1.2rem;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1rem;">
        <div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.85rem;">
            <div style="width:38px;height:38px;
                        background:linear-gradient(135deg,#8B5CF6,#06B6D4);
                        border-radius:10px;display:flex;align-items:center;
                        justify-content:center;font-size:1.1rem;flex-shrink:0;
                        box-shadow:0 0 18px rgba(139,92,246,0.4);
                        animation:badgePulse 3s ease-in-out infinite;">🐇</div>
            <div>
                <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:1rem;
                            font-weight:900;color:#fff;letter-spacing:-0.01em;">Rabbitt AI</div>
                <div style="font-size:0.57rem;color:#1E293B;letter-spacing:0.14em;
                            text-transform:uppercase;font-family:'Instrument Sans',sans-serif;">
                    Construction Intel</div>
            </div>
        </div>
        <div style="display:inline-flex;align-items:center;gap:0.4rem;
                    background:rgba(52,211,153,0.07);
                    border:1px solid rgba(52,211,153,0.2);
                    border-radius:100px;padding:0.22rem 0.7rem;">
            <span style="width:5px;height:5px;background:#34D399;border-radius:50%;
                         display:inline-block;box-shadow:0 0 6px #34D399;
                         animation:dotPulse 2s ease-in-out infinite;"></span>
            <span style="font-size:0.57rem;color:#34D399;font-weight:600;
                         letter-spacing:0.1em;text-transform:uppercase;">AI Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sample data
    st.markdown('<p style="font-size:0.57rem;color:#1E293B;letter-spacing:0.14em;text-transform:uppercase;margin:0 0 0.45rem;font-family:Instrument Sans,sans-serif;">Sample Data</p>', unsafe_allow_html=True)
    st.download_button("↓  Download sample.csv", data=generate_sample_csv(),
                       file_name="construction_data.csv", mime="text/csv", use_container_width=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Quick queries
    st.markdown('<p style="font-size:0.57rem;color:#1E293B;letter-spacing:0.14em;text-transform:uppercase;margin:0 0 0.45rem;font-family:Instrument Sans,sans-serif;">Try These</p>', unsafe_allow_html=True)
    for q in [
        "Which towers are ready for billing?",
        "What's causing the most delays?",
        "Forecast revenue collection for next quarter",
        "Which project is highest risk?",
        "Compare all projects side by side",
        "What regulatory issues need urgent attention?",
        "Give me an executive summary",
    ]:
        if st.button(q, use_container_width=True, key=f"q_{q}"):
            st.session_state["prefill"] = q

    # Live stats
    if st.session_state.df is not None:
        d = st.session_state.df
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(139,92,246,0.3),transparent);margin-bottom:0.9rem;"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.57rem;color:#1E293B;letter-spacing:0.14em;text-transform:uppercase;margin:0 0 0.55rem;">Portfolio</p>', unsafe_allow_html=True)
        for icon, lbl, val, col in [
            ("◈","Projects", d['Project'].nunique(), "#A78BFA"),
            ("◫","Towers",   len(d),                 "#E2E8F0"),
            ("◉","Ready",    len(d[d["Slab_Percent"]>90]), "#34D399"),
            ("▲","Delayed",  len(d[d["Days_Delayed"]>0]),  "#F87171"),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.38rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span style="font-size:0.75rem;color:#334155;font-family:Instrument Sans,sans-serif;">
                    {icon}&ensp;{lbl}</span>
                <span style="font-family:'Cabinet Grotesk',sans-serif;font-size:0.95rem;
                             font-weight:800;color:{col};">{val}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-top:0.8rem;padding:0.85rem;
                    background:linear-gradient(135deg,rgba(139,92,246,0.07),rgba(6,182,212,0.05));
                    border:1px solid rgba(139,92,246,0.15);border-radius:12px;text-align:center;">
            <div style="font-size:0.54rem;color:#1E293B;letter-spacing:0.12em;
                        text-transform:uppercase;margin-bottom:0.2rem;">Revenue Pending</div>
            <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:1.25rem;
                        font-weight:900;color:#22D3EE;letter-spacing:-0.02em;">
                {fmt_crore(d["Revenue_Pending"].sum())}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:2rem;text-align:center;font-size:0.53rem;color:#0F172A;">© 2025 Rabbitt AI</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────
c1, c2 = st.columns([5,1])
with c1:
    st.markdown("""
    <div style="margin-bottom:0.25rem;">
        <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:0.57rem;font-weight:700;
                    color:#1E293B;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.4rem;">
            AI-Powered Construction Intelligence
        </div>
        <h1 style="font-family:'Cabinet Grotesk',sans-serif;font-size:2.3rem;font-weight:900;
                   color:#fff;margin:0;line-height:1.05;letter-spacing:-0.035em;">
            Ask your data
            <span style="background:linear-gradient(90deg,#8B5CF6,#06B6D4,#F472B6);
                         background-size:200% 100%;
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                         background-clip:text;
                         animation:gradShift 5s linear infinite;"> anything.</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div style="text-align:right;padding-top:1.2rem;">
        <div style="display:inline-block;
                    background:rgba(139,92,246,0.1);
                    border:1px solid rgba(139,92,246,0.25);
                    border-radius:100px;padding:0.28rem 0.8rem;">
            <span style="font-size:0.59rem;color:#A78BFA;font-weight:600;
                         letter-spacing:0.1em;text-transform:uppercase;">Claude Powered</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:linear-gradient(90deg,rgba(139,92,246,0.5),rgba(6,182,212,0.3),transparent);margin:0.5rem 0 1.5rem;"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UPLOAD STATE
# ─────────────────────────────────────────────
if st.session_state.df is None:
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-eyebrow"><div class="hero-dot"></div>Rabbitt AI · Construction Intelligence</div>
        <div class="hero-title">
            Conversational analytics<br>
            <span class="grad">for construction teams.</span>
        </div>
        <div class="hero-sub">
            Upload your site data and ask anything in plain English.
            Powered by Claude AI — no dashboards, no SQL, no limits.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_u, col_spec = st.columns([3,2])
    with col_u:
        st.markdown('<p style="font-size:0.57rem;color:#1E293B;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.45rem;">Upload your CSV</p>', unsafe_allow_html=True)
        uploaded = st.file_uploader("csv", type=["csv"], label_visibility="collapsed")
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                req = {"Project","Tower","Slab_Percent","Revenue_Pending","Days_Delayed","Regulatory_Status"}
                miss = req - set(df.columns)
                if miss:
                    st.error(f"Missing: {', '.join(miss)}")
                else:
                    st.session_state.df = df
                    st.success(f"✓ Loaded {len(df)} towers across {df['Project'].nunique()} projects")
                    st.rerun()
            except Exception as e:
                st.error(str(e))

    with col_spec:
        st.markdown("""
        <div class="g-card" style="padding:1.2rem 1.4rem;">
            <div style="font-size:0.57rem;color:#1E293B;letter-spacing:0.14em;
                        text-transform:uppercase;margin-bottom:0.75rem;">Required Columns</div>
            <div style="font-size:0.8rem;color:#475569;line-height:2.1;font-family:'Instrument Sans',sans-serif;">
                <span style="color:#8B5CF6;margin-right:0.5rem;">▹</span>Project<br>
                <span style="color:#8B5CF6;margin-right:0.5rem;">▹</span>Tower<br>
                <span style="color:#8B5CF6;margin-right:0.5rem;">▹</span>Slab_Percent<br>
                <span style="color:#8B5CF6;margin-right:0.5rem;">▹</span>Revenue_Pending<br>
                <span style="color:#8B5CF6;margin-right:0.5rem;">▹</span>Days_Delayed<br>
                <span style="color:#8B5CF6;margin-right:0.5rem;">▹</span>Regulatory_Status
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHAT INTERFACE
# ─────────────────────────────────────────────
else:
    df = st.session_state.df

    # KPIs
    ready   = len(df[df["Slab_Percent"]>90])
    delayed = len(df[df["Days_Delayed"]>0])
    rev     = df["Revenue_Pending"].sum()
    avgs    = df["Slab_Percent"].mean()

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-tile">
            <div class="kpi-val">{df['Project'].nunique()}</div>
            <div class="kpi-lbl">Projects</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-val">{len(df)}</div>
            <div class="kpi-lbl">Towers</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-val" style="color:#34D399;">{ready}</div>
            <div class="kpi-lbl">Ready to Bill</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-val" style="color:#F87171;">{delayed}</div>
            <div class="kpi-lbl">Delayed</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-val" style="font-size:1.15rem;color:#22D3EE;">{fmt_crore(rev)}</div>
            <div class="kpi-lbl">Revenue Pending</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-val">{avgs:.0f}<span style="font-size:1rem;font-weight:700;">%</span></div>
            <div class="kpi-lbl">Avg Slab</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.57rem;color:#1E293B;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.75rem;">Conversation</p>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="g-card" style="text-align:center;padding:2.5rem 1.5rem;">
            <div style="font-size:1.6rem;margin-bottom:0.6rem;">✦</div>
            <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:1rem;font-weight:800;
                        color:#fff;margin-bottom:0.35rem;">Ask me anything</div>
            <div style="font-size:0.82rem;color:#1E293B;max-width:360px;
                        margin:0 auto;font-weight:300;line-height:1.6;">
                Powered by Claude AI — ask complex questions, get charts, forecasts &amp; insights
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render chat
    for i, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-user-wrap">
                <div class="chat-bubble-user">
                    <div class="bubble-lbl bubble-lbl-user">You</div>
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Speak button + auto-speak latest message
            is_latest = (i == len(st.session_state.chat_history) - 1)
            speak_js = speak_text(msg['content'], i)
            
            st.markdown(f"""
            <div class="chat-ai-wrap">
                <div class="ai-badge">🐇</div>
                <div style="flex:1;">
                    <div class="chat-bubble-ai">
                        <div class="bubble-lbl bubble-lbl-ai" style="display:flex;justify-content:space-between;align-items:center;">
                            <span>Rabbitt AI</span>
                            <button onclick="(function(){{
                                window.speechSynthesis.cancel();
                                var u=new SpeechSynthesisUtterance(this.dataset.text);
                                u.rate=1.05;u.pitch=1.0;u.volume=1.0;
                                var v=window.speechSynthesis.getVoices();
                                var pv=v.find(x=>x.name.includes('Google')&&x.lang.startsWith('en'))||v.find(x=>x.lang.startsWith('en-'))||v[0];
                                if(pv)u.voice=pv;
                                window.speechSynthesis.speak(u);
                            }}).call(this)"
                            data-text="{msg['content'].replace(chr(34), '').replace('**','').replace('*','').replace('#','').replace(chr(96),'')[:600]}"
                            style="background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.3);
                                   border-radius:6px;padding:0.15rem 0.5rem;cursor:pointer;
                                   color:#A78BFA;font-size:0.65rem;letter-spacing:0.05em;
                                   font-family:Instrument Sans,sans-serif;transition:all 0.2s;"
                            onmouseover="this.style.background='rgba(139,92,246,0.3)'"
                            onmouseout="this.style.background='rgba(139,92,246,0.15)'">
                            🔊 Speak
                            </button>
                        </div>
                        {msg['content']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-speak the latest AI message
            if is_latest and msg.get("auto_speak", True):
                st.markdown(speak_text(msg['content'], i), unsafe_allow_html=True)
            
            if msg.get("df_result") is not None:
                res = msg["df_result"].copy()
                if "Revenue_Pending" in res.columns:
                    res["Revenue_Pending"] = res["Revenue_Pending"].apply(fmt_crore)
                st.dataframe(res, use_container_width=True, hide_index=True, key=f"df_{i}")
            if msg.get("fig") is not None:
                st.plotly_chart(msg["fig"], use_container_width=True, key=f"fig_{i}")

    # ── VOICE INPUT + TEXT INPUT BAR ──────────────
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    prefill = st.session_state.pop("prefill", "")

    # Voice input JS — mic button injects transcript into hidden input + triggers submit
    st.markdown("""
    <style>
    .voice-bar {
        display: flex; align-items: center; gap: 0.6rem;
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(139,92,246,0.25);
        border-radius: 16px;
        padding: 0.4rem 0.6rem 0.4rem 1rem;
        margin-bottom: 0.5rem;
        transition: border-color 0.3s;
    }
    .voice-bar:focus-within { border-color: rgba(139,92,246,0.6); }
    #voice-text-display {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: #E2E8F0;
        font-family: 'Instrument Sans', sans-serif;
        font-size: 0.92rem;
        min-height: 24px;
    }
    #voice-text-display::placeholder { color: #334155; }
    .mic-btn {
        width: 42px; height: 42px;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #8B5CF6, #06B6D4);
        color: white;
        font-size: 1.1rem;
        cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1);
        box-shadow: 0 4px 16px rgba(139,92,246,0.35);
        flex-shrink: 0;
    }
    .mic-btn:hover { transform: scale(1.08); box-shadow: 0 6px 24px rgba(139,92,246,0.55); }
    .mic-btn.listening {
        background: linear-gradient(135deg, #F472B6, #F87171) !important;
        animation: micPulse 0.8s ease-in-out infinite;
        box-shadow: 0 0 0 0 rgba(244,114,182,0.4);
    }
    @keyframes micPulse {
        0%  { box-shadow: 0 0 0 0 rgba(244,114,182,0.5); }
        70% { box-shadow: 0 0 0 12px rgba(244,114,182,0); }
        100%{ box-shadow: 0 0 0 0 rgba(244,114,182,0); }
    }
    .send-btn {
        padding: 0.5rem 1.2rem;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #8B5CF6, #06B6D4);
        color: white;
        font-family: 'Cabinet Grotesk', sans-serif;
        font-weight: 800;
        font-size: 0.82rem;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 4px 16px rgba(139,92,246,0.3);
        flex-shrink: 0;
        letter-spacing: 0.04em;
    }
    .send-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(139,92,246,0.5); }
    .voice-status {
        font-size: 0.65rem;
        color: #F472B6;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 600;
        min-width: 80px;
        text-align: center;
    }
    </style>

    <div class="voice-bar">
        <span style="font-size:0.7rem;color:#334155;flex-shrink:0;">🎙</span>
        <input id="voice-text-display" type="text"
               placeholder="Speak or type — ask anything about your portfolio…"
               oninput="document.getElementById('st-voice-hidden').value=this.value"
               onkeydown="if(event.key==='Enter'){sendVoiceQuery()}"
        />
        <span id="voice-status" class="voice-status"></span>
        <button class="mic-btn" id="mic-btn" onclick="toggleMic()" title="Click to speak">🎤</button>
        <button class="send-btn" onclick="sendVoiceQuery()">Send →</button>
    </div>

    <!-- Hidden bridge to Streamlit -->
    <input type="text" id="st-voice-hidden" style="display:none;" />

    <script>
    var recognition = null;
    var isListening = false;

    function toggleMic() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Voice input is not supported in this browser. Please use Chrome.');
            return;
        }
        if (isListening) {
            recognition.stop();
            return;
        }
        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = 'en-IN';
        recognition.continuous = false;
        recognition.interimResults = true;

        var micBtn = document.getElementById('mic-btn');
        var statusEl = document.getElementById('voice-status');
        var displayInput = document.getElementById('voice-text-display');

        recognition.onstart = function() {
            isListening = true;
            micBtn.classList.add('listening');
            micBtn.textContent = '⏹';
            statusEl.textContent = '● Listening…';
        };
        recognition.onresult = function(e) {
            var transcript = '';
            for (var i = e.resultIndex; i < e.results.length; i++) {
                transcript += e.results[i][0].transcript;
            }
            displayInput.value = transcript;
            document.getElementById('st-voice-hidden').value = transcript;
            if (e.results[e.results.length-1].isFinal) {
                statusEl.textContent = '✓ Got it!';
                setTimeout(function(){ sendVoiceQuery(); }, 400);
            }
        };
        recognition.onerror = function(e) {
            statusEl.textContent = 'Error: ' + e.error;
            isListening = false;
            micBtn.classList.remove('listening');
            micBtn.textContent = '🎤';
        };
        recognition.onend = function() {
            isListening = false;
            micBtn.classList.remove('listening');
            micBtn.textContent = '🎤';
            setTimeout(function(){ statusEl.textContent = ''; }, 2000);
        };
        recognition.start();
    }

    function sendVoiceQuery() {
        var text = document.getElementById('voice-text-display').value.trim();
        if (!text) return;
        // Write into Streamlit's hidden text input and trigger form submit
        var stInputs = window.parent.document.querySelectorAll('input[type="text"]');
        var targetInput = null;
        stInputs.forEach(function(inp) {
            if (inp.getAttribute('aria-label') === 'voice_query_bridge' || inp.placeholder === '') {
                // fallback
            }
        });
        // Use the dedicated hidden streamlit input
        var hiddenBridge = window.parent.document.querySelector('[data-testid="stTextInput"] input');
        if (hiddenBridge) {
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(hiddenBridge, text);
            hiddenBridge.dispatchEvent(new Event('input', { bubbles: true }));
        }
        // Also store in sessionStorage for Streamlit to pick up
        window.parent.sessionStorage.setItem('rabbitt_voice_query', text);
        // Trigger the hidden submit button
        setTimeout(function() {
            var btns = window.parent.document.querySelectorAll('button[kind="secondaryFormSubmit"], button');
            btns.forEach(function(btn) {
                if (btn.textContent.trim() === 'VOICE_SUBMIT') {
                    btn.click();
                }
            });
        }, 100);
    }
    </script>
    """, unsafe_allow_html=True)

    # Hidden Streamlit input bridge for voice
    voice_query = st.text_input("voice_query_bridge", value=prefill,
        label_visibility="collapsed", key="chat_input",
        placeholder="")

    # JS polling to grab voice query from sessionStorage
    st.markdown("""
    <script>
    (function poll() {
        var q = window.sessionStorage.getItem('rabbitt_voice_query');
        if (q) {
            window.sessionStorage.removeItem('rabbitt_voice_query');
            // Inject into streamlit text input
            var inputs = window.parent.document.querySelectorAll('input[type="text"]');
            inputs.forEach(function(inp) {
                if (inp.getAttribute('data-testid') !== undefined || inp.type === 'text') {
                    try {
                        var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        setter.call(inp, q);
                        inp.dispatchEvent(new Event('input', { bubbles: true }));
                    } catch(e) {}
                }
            });
        }
        setTimeout(poll, 800);
    })();
    </script>
    """, unsafe_allow_html=True)

    query = voice_query
    submit = False  # voice auto-submits via JS; text users press Enter

    # Handle Enter-key submission through Streamlit text input
    if query and query != prefill and query.strip():
        submit = True

    if submit and query.strip():
        with st.spinner("🐇 Thinking…"):
            try:
                answer, fig = ask_claude(df, query, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "user", "content": query})
                st.session_state.chat_history.append({
                    "role": "assistant", "content": answer,
                    "df_result": None, "fig": fig,
                })
            except Exception as e:
                st.error(f"AI error: {str(e)}")
        st.rerun()

    # Action buttons
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    ca, cb, cc, _ = st.columns([1.1, 1.4, 1.2, 3.8])
    with ca:
        if st.button("Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with cb:
        if st.button("New Dataset", use_container_width=True):
            st.session_state.df = None
            st.session_state.chat_history = []
            st.rerun()
    with cc:
        st.markdown("""
        <button onclick="window.speechSynthesis.cancel()"
            style="width:100%;background:rgba(248,113,113,0.1);border:1px solid rgba(248,113,113,0.25);
                   border-radius:12px;padding:0.42rem 0.5rem;cursor:pointer;color:#F87171;
                   font-size:0.78rem;font-family:'Cabinet Grotesk',sans-serif;font-weight:700;
                   letter-spacing:0.03em;transition:all 0.2s;"
            onmouseover="this.style.background='rgba(248,113,113,0.22)'"
            onmouseout="this.style.background='rgba(248,113,113,0.1)'">
            🔇 Stop
        </button>
        """, unsafe_allow_html=True)
