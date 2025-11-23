# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Optional dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Local modules
from nlp import extract_text_from_image, PDF_PATH
from backend import process_ocr_text
from analytics import summarize_by_category, simple_forecast
from advisor import generate_budget, goal_progress, investment_suggestions
from fraud import train_demo_model, check_transaction_vector
from llm import groq_answer

# --------------------------------------------
# Load Groq API Key
# --------------------------------------------
GROQ_API_KEY = ""
try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
except:
    pass
GROQ_API_KEY = os.getenv("GROQ_API_KEY", GROQ_API_KEY)

# --------------------------------------------
# Streamlit layout
# --------------------------------------------
st.set_page_config(page_title="Finance Manager AI", layout="wide")
st.sidebar.title("Finance Manager AI")
st.sidebar.markdown(f"Source: {PDF_PATH}")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Upload Receipt", "Goals", "Fraud", "Chat", "Settings"]
)

# --------------------------------------------
# Dashboard
# --------------------------------------------
if page == "Dashboard":
    st.title("📊 Dashboard")
    tx = pd.DataFrame([
        {"date": "2025-06-01", "category": "Food", "amount": 42.3},
        {"date": "2025-06-03", "category": "Bills", "amount": 120.0},
        {"date": "2025-06-05", "category": "Transport", "amount": 15.0},
        {"date": "2025-06-10", "category": "Food", "amount": 30.0},
    ])
    summary = summarize_by_category(tx)
    st.subheader("Spending by category")
    fig = px.pie(summary, names="category", values="amount")
    st.plotly_chart(fig, use_container_width=True)

    monthly = [1200, 1500, 1100, 1800, 1700, 1600]
    forecast = simple_forecast(monthly, periods=3)
    st.subheader("Expense forecast")
    st.write(forecast)

# --------------------------------------------
# Upload Receipt
# --------------------------------------------
elif page == "Upload Receipt":
    st.title("📤 Upload Receipt")
    uploaded = st.file_uploader("Upload receipt (jpg/png)", type=["png", "jpg", "jpeg"])
    if uploaded:
        st.image(uploaded, width=350)
        if st.button("Process Receipt"):
            text = extract_text_from_image(uploaded)
            st.write("Extracted text:")
            st.write(text[:400])
            res = process_ocr_text(text)
            st.success(f"Category: {res['category']} | Amount: ${res['amount']}")

# --------------------------------------------
# Goals
# --------------------------------------------
elif page == "Goals":
    st.title("🎯 Goals & Budget")
    income = st.number_input("Monthly income ($)", value=3000.0)
    budget = generate_budget(income)
    st.json(budget)
    current = st.number_input("Savings now", value=1400.0)
    target = st.number_input("Target", value=2500.0)
    prog = goal_progress(current, target)
    st.progress(prog / 100)
    st.write(f"{prog}% reached")
    st.subheader("Investment Suggestions")
    st.write(investment_suggestions("medium"))

# --------------------------------------------
# Fraud
# --------------------------------------------
elif page == "Fraud":
    st.title("🚨 Fraud Detection (Prototype)")
    if st.button("Train Demo Model"):
        import numpy as np
        rng = np.random.RandomState(42)
        normal = rng.normal(100, 50, size=(200, 2))
        anomalies = rng.normal(6000, 300, size=(8, 2))
        X = np.vstack([normal, anomalies])
        train_demo_model(X)
        st.success("Model trained")
    amount = st.number_input("Transaction Amount", value=50.0)
    hour = st.number_input("Hour (0–23)", min_value=0, max_value=23, value=12)
    if st.button("Check Fraud"):
        result = check_transaction_vector([amount, hour])
        if result == "Fraud":
            st.error("⚠️ Potential Fraud Detected")
        else:
            st.success("✔️ Transaction looks safe")

# --------------------------------------------
# Chat
# --------------------------------------------
# --------------------------------------------
# Chat
# --------------------------------------------
elif page == "Chat":
    st.title("💬 Finance Chatbot")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "text": "Hello! I am your Finance AI assistant. How can I help?"}
        ]

    # Display chat messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='text-align:right;background:#2563EB;color:white;padding:10px;border-radius:10px;margin:5px'>{msg['text']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background:#E5E7EB;padding:10px;border-radius:10px;margin:5px'>{msg['text']}</div>",
                unsafe_allow_html=True
            )

    # Chat input using a form to handle submission
    with st.form("chat_form", clear_on_submit=True):
        user_text = st.text_input("Type your message", key="chat_input_box")
        send = st.form_submit_button("Send")

    if send and user_text.strip():
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "text": user_text})

        # Get bot reply
        from llm import groq_answer  # make sure llm.py is present
        if GROQ_API_KEY:
            reply = groq_answer(GROQ_API_KEY, user_text)
        else:
            # Free fallback if Groq API not configured
            reply = f"[Free model] I understood: {user_text[:100]}..."

        # Add bot reply to history
        st.session_state.chat_history.append({"role": "bot", "text": reply})

# --------------------------------------------
# Settings
# --------------------------------------------
elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Prototype settings screen")
    st.checkbox("Enable demo notifications", value=True)
