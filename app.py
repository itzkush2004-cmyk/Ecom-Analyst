import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from query_runner import run_query
from insight import generate_insight
from confidence import get_confidence

st.set_page_config(page_title="Ecom Analyst", layout="centered", page_icon="🛒")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background-color: #f8fafc !important; }
.block-container { max-width: 720px !important; padding: 2rem 1.5rem 8rem !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

h1 {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    color: #0f172a !important;
    font-family: 'Inter', sans-serif !important;
    background: none !important;
    -webkit-text-fill-color: #0f172a !important;
}
h2, h3 {
    font-family: 'Inter', sans-serif !important;
    background: none !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #2563eb !important;
    -webkit-text-fill-color: #2563eb !important;
}

.stCaption { color: #94a3b8 !important; font-size: 11px !important; }

[data-testid="stPillsContainer"] { gap: 6px !important; }
[data-testid="stPillsContainer"] button {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 20px !important;
    color: #374151 !important;
    font-size: 12px !important;
    font-family: 'Inter', sans-serif !important;
    padding: 6px 14px !important;
    font-weight: 400 !important;
    transition: all 150ms ease !important;
    box-shadow: none !important;
}
[data-testid="stPillsContainer"] button:hover {
    border-color: #2563eb !important;
    color: #2563eb !important;
    background: #eff6ff !important;
}
[data-testid="stPillsContainer"] button[aria-pressed="true"] {
    background: #eff6ff !important;
    border-color: #2563eb !important;
    color: #2563eb !important;
}

[data-testid="stBottom"] { background-color: #f8fafc !important; }
[data-testid="stBottom"] > div { background-color: #f8fafc !important; }
[data-testid="stChatInputContainer"] {
    background: #1e293b !important;
    border: none !important;
    border-radius: 50px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15) !important;
    padding: 4px 4px 4px 20px !important;
}
[data-testid="stChatInputContainer"]:focus-within {
    box-shadow: 0 0 0 3px rgba(37,99,235,0.3) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    color: #ffffff !important;
    background: transparent !important;
    caret-color: #ffffff !important;
    pointer-events: auto !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #94a3b8 !important; }
[data-testid="stChatInputSubmitButton"] { background: #2563eb !important; border-radius: 50% !important; }
[data-testid="stChatInputSubmitButton"] svg { fill: #ffffff !important; }

[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 16px !important;
    margin-bottom: 8px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

.stDataFrame { border: 1px solid #e2e8f0 !important; border-radius: 12px !important; overflow: hidden !important; }
.stDataFrame th {
    background-color: #eff6ff !important;
    color: #1d4ed8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-family: 'Inter', sans-serif !important;
}
.stDataFrame td {
    color: #1a1a1a !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    border-color: #f1f5f9 !important;
}

/* ── Expander header — explicit color reset ── */
[data-testid="stExpander"] summary {
    background: #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    cursor: pointer !important;
}
[data-testid="stExpander"] summary:hover {
    background: #e2e8f0 !important;
    color: #2563eb !important;
    -webkit-text-fill-color: #2563eb !important;
}
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary p {
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
    font-size: 13px !important;
}
[data-testid="stExpander"] summary:hover span,
[data-testid="stExpander"] summary:hover p {
    color: #2563eb !important;
    -webkit-text-fill-color: #2563eb !important;
}

/* ── Code block inside expander ── */
[data-testid="stExpander"] .stCode,
[data-testid="stExpander"] pre,
[data-testid="stExpander"] code {
    background-color: #0f172a !important;
    border-radius: 8px !important;
    color: #93c5fd !important;
    -webkit-text-fill-color: #93c5fd !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    line-height: 1.7 !important;
}

/* ── Code block outside expander ── */
.stCode, pre, code {
    background-color: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #93c5fd !important;
    -webkit-text-fill-color: #93c5fd !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    line-height: 1.7 !important;
}

.stAlert {
    background-color: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-left: 3px solid #2563eb !important;
    border-radius: 12px !important;
    color: #1e3a5f !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
}

.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #bfdbfe !important;
    color: #2563eb !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    height: auto !important;
    padding: 5px 14px !important;
    font-family: 'Inter', sans-serif !important;
}
.stDownloadButton > button:hover { background: #eff6ff !important; }

.stSpinner > div { border-top-color: #2563eb !important; }

button[kind="tertiary"] {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    color: #374151 !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 150ms ease !important;
    padding: 6px 16px !important;
    height: auto !important;
    margin-top: 8px !important;
}
button[kind="tertiary"]:hover {
    border-color: #2563eb !important;
    color: #2563eb !important;
    background: #eff6ff !important;
}

hr { border-color: #e2e8f0 !important; opacity: 1 !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-thumb { background: #bfdbfe; border-radius: 4px; }
.stMarkdown p { color: #374151 !important; font-size: 13.5px !important; line-height: 1.7 !important; }
.stMarkdown strong { color: #0f172a !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation" not in st.session_state:
    st.session_state.conversation = []

SUGGESTIONS = {
    "🏆 Top 5 revenue categories": "Which are the top 5 product categories by total revenue?",
    "🚚 Avg delivery time by state": "What is the average delivery time in days by customer state?",
    "💳 Most common payment method": "What is the most common payment method used by customers?",
    "⭐ Lowest review score categories": "Which product categories have the lowest average review scores?",
    "📦 Monthly order trends 2018": "Show me monthly order volume trends for 2018",
}

has_history = len(st.session_state.messages) > 0

# ── Title row ─────────────────────────────────────────────────────────────────
title_row = st.container(horizontal=True, vertical_alignment="center")
with title_row:
    st.title("🛒 Ecom Analyst", anchor=False, width="stretch")
    if has_history:
        def clear_conversation():
            st.session_state.messages = []
            st.session_state.conversation = []
        st.button(
            "Restart",
            icon=":material/refresh:",
            on_click=clear_conversation,
            type="tertiary"
        )

# ── Landing page ──────────────────────────────────────────────────────────────
if not has_history:
    st.caption("Ask anything about the Olist Brazilian E-Commerce dataset · 1.5M+ records · 9 tables · powered by LLaMA 3")
    st.write("")
    initial_question = st.chat_input("Ask a question about your e-commerce data...")
    selected = st.pills(
        label="Suggestions",
        label_visibility="collapsed",
        options=list(SUGGESTIONS.keys()),
        key="selected_suggestion",
    )
    st.write("")
    st.caption("Olist Brazilian E-Commerce · 1.5M+ records · 9 tables")
    if initial_question:
        user_message = initial_question
    elif selected:
        user_message = SUGGESTIONS[selected]
    else:
        st.stop()
else:
    user_message = st.chat_input("Ask a follow-up...")

# ── Render message history ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            if msg.get("confidence"):
                color_map = {"High": "#16a34a", "Medium": "#d97706", "Low": "#dc2626"}
                bg_map = {"High": "#f0fdf4", "Medium": "#fffbeb", "Low": "#fef2f2"}
                border_map = {"High": "#bbf7d0", "Medium": "#fde68a", "Low": "#fecaca"}
                c = color_map.get(msg["confidence"], "#d97706")
                b = bg_map.get(msg["confidence"], "#fffbeb")
                br = border_map.get(msg["confidence"], "#fde68a")
                st.markdown(
                    f"""<div style='margin-bottom:10px;'>
                    <span style='background:{b};color:{c};border:1px solid {br};
                    padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;
                    text-transform:uppercase;letter-spacing:0.05em;font-family:Inter,sans-serif;'>
                    {msg["confidence"]} Confidence</span>
                    <span style='color:#94a3b8;font-size:12px;margin-left:8px;font-family:Inter,sans-serif;'>
                    {msg.get("confidence_reason","")}</span></div>""",
                    unsafe_allow_html=True
                )
            if msg.get("insight"):
                st.info(msg["insight"])
            if msg.get("df") is not None:
                st.subheader("Results")
                st.caption(f"{msg['rows']} rows · {msg['time']}s")
                st.dataframe(msg["df"], use_container_width=True)
                st.download_button(
                    label="⬇ Download CSV",
                    data=msg["csv"],
                    file_name="results.csv",
                    mime="text/csv",
                    key=f"dl_{msg['timestamp']}"
                )
            if msg.get("sql"):
                with st.expander("View Generated SQL"):
                    st.code(msg["sql"], language="sql")

# ── Process new message ───────────────────────────────────────────────────────
if user_message:
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                start = datetime.now()
                sql, df = run_query(user_message, st.session_state.conversation)
                elapsed = round((datetime.now() - start).total_seconds(), 2)
            except ValueError as e:
                st.error(str(e))
                st.stop()
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        with st.spinner("Reviewing query..."):
            confidence_result = get_confidence(user_message, sql)
            confidence = confidence_result.get("confidence", "Medium")
            reason = confidence_result.get("reason", "")

        with st.spinner("Analysing results..."):
            try:
                insight = generate_insight(user_message, df.to_string(index=False))
            except Exception:
                insight = None

        color_map = {"High": "#16a34a", "Medium": "#d97706", "Low": "#dc2626"}
        bg_map = {"High": "#f0fdf4", "Medium": "#fffbeb", "Low": "#fef2f2"}
        border_map = {"High": "#bbf7d0", "Medium": "#fde68a", "Low": "#fecaca"}
        c = color_map.get(confidence, "#d97706")
        b = bg_map.get(confidence, "#fffbeb")
        br = border_map.get(confidence, "#fde68a")
        st.markdown(
            f"""<div style='margin-bottom:10px;'>
            <span style='background:{b};color:{c};border:1px solid {br};
            padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;
            text-transform:uppercase;letter-spacing:0.05em;font-family:Inter,sans-serif;'>
            {confidence} Confidence</span>
            <span style='color:#94a3b8;font-size:12px;margin-left:8px;font-family:Inter,sans-serif;'>
            {reason}</span></div>""",
            unsafe_allow_html=True
        )

        if insight:
            st.info(insight)

        st.subheader("Results")
        st.caption(f"{len(df)} rows · {elapsed}s")
        st.dataframe(df, use_container_width=True)

        st.download_button(
            label="⬇ Download CSV",
            data=df.to_csv(index=False),
            file_name="results.csv",
            mime="text/csv",
            key=f"dl_new_{datetime.now().timestamp()}"
        )

        with st.expander("View Generated SQL"):
            st.code(sql, language="sql")

    st.session_state.conversation.append({
        "question": user_message,
        "sql": sql,
        "result": df.to_string(index=False)
    })
    st.session_state.messages.append({
        "role": "assistant",
        "content": "",
        "sql": sql,
        "df": df,
        "csv": df.to_csv(index=False),
        "rows": len(df),
        "time": elapsed,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "insight": insight,
        "confidence": confidence,
        "confidence_reason": reason
    })

    st.rerun()