# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Optional dotenv support for local .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass  # ignore if dotenv not installed

# Local modules
from nlp import extract_text_from_image, PDF_PATH
from backend import process_ocr_text
from analytics import summarize_by_category, simple_forecast
from advisor import generate_budget, goal_progress, investment_suggestions
from fraud import train_demo_model, check_transaction_vector
from llm import configure_gemini, gemini_answer, llama3_answer

# -------------------------------
# Load Gemini API Key safely
# -------------------------------
GEMINI_API_KEY = ""
# 1. Try Streamlit secrets
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

# 2. Fallback to environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)

# 3. Configure Gemini if available
model = None
if GEMINI_API_KEY:
    try:
        model = configure_gemini(GEMINI_API_KEY)
    except Exception as e:
        st.warning(f"Gemini not configured: {str(e)}")

# -------------------------------
# Streamlit layout
# -------------------------------
st.set_page_config(page_title="Finance Manager AI", layout="wide")

st.sidebar.title("Finance Manager AI")
st.sidebar.markdown(f"({PDF_PATH})")
page = st.sidebar.radio("Navigation", ["Dashboard", "Upload Receipt", "Goals", "Fraud", "Chat", "Settings"])

# -------------------------------
# Dashboard
# -------------------------------
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.write("Prototype overview")

    tx = pd.DataFrame([
        {"date":"2025-06-01","category":"Food","amount":42.3},
        {"date":"2025-06-03","category":"Bills","amount":120.0},
        {"date":"2025-06-05","category":"Transport","amount":15.0},
        {"date":"2025-06-10","category":"Food","amount":30.0},
    ])
    summary = summarize_by_category(tx)
    st.subheader("Spending by category")
    fig = px.pie(summary, names="category", values="amount")
    st.plotly_chart(fig, use_container_width=True)

    monthly = [1200, 1500, 1100, 1800, 1700, 1600]
    forecast = simple_forecast(monthly, periods=3)
    st.subheader("Expense forecast (next 3 periods)")
    st.write(forecast)

# -------------------------------
# Upload Receipt
# -------------------------------
elif page == "Upload Receipt":
    st.title("📤 Upload Receipt")
    uploaded = st.file_uploader("Upload receipt image", type=["png","jpg","jpeg"])
    if uploaded:
        st.image(uploaded, width=350)
        if st.button("Process receipt"):
            text = extract_text_from_image(uploaded)
            st.write("Extracted text (first 400 chars):")
            st.write(text[:400])
            res = process_ocr_text(text)
            st.success(f"Category: {res['category']}  Amount: ${res['amount']}")

# -------------------------------
# Goals
# -------------------------------
elif page == "Goals":
    st.title("🎯 Goals & Budget")
    income = st.number_input("Monthly income (USD)", value=3000.0)
    budget = generate_budget(income)
    st.json(budget)
    current = st.number_input("Current saved", value=1400.0)
    target = st.number_input("Goal target", value=2500.0)
    prog = goal_progress(current, target)
    st.progress(prog / 100.0)
    st.write(f"{prog}% reached")
    st.subheader("Investment ideas (medium risk)")
    st.write(investment_suggestions("medium"))

# -------------------------------
# Fraud
# -------------------------------
elif page == "Fraud":
    st.title("🚨 Fraud Detection (Prototype)")
    if st.button("Train demo model (synthetic)"):
        import numpy as np
        rng = np.random.RandomState(42)
        normal = rng.normal(loc=100, scale=50, size=(200, 2))
        anomalies = rng.normal(loc=6000, scale=300, size=(8, 2))
        X = np.vstack([normal, anomalies])
        train_demo_model(X)
        st.success("Demo model trained")

    amount = st.number_input("Transaction amount", value=50.0)
    hour = st.number_input("Hour of day (0-23)", min_value=0, max_value=23, value=12)
    if st.button("Check"):
        res = check_transaction_vector([amount, hour])
        if res == "Fraud":
            st.error("Possible fraud detected")
        else:
            st.success("Transaction looks safe")

# -------------------------------
# Chat
# -------------------------------
elif page == "Chat":
    st.title("💬 Finance Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "text": "Hello! I'm your Finance AI. How can I help?"}
        ]

    # Display chat messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='text-align:right;background:#2563EB;color:white;padding:10px;border-radius:8px;margin:5px'>{msg['text']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background:#E2E8F0;color:black;padding:10px;border-radius:8px;margin:5px'>{msg['text']}</div>",
                unsafe_allow_html=True,
            )

    # Input
    user_text = st.text_input("Type your message...", key="chat_input")

    if st.button("Send"):
        if user_text.strip():
            st.session_state.chat_history.append({"role": "user", "text": user_text})

            # Use Gemini if available
            if model:
                reply = gemini_answer(model, f"You are a helpful finance advisor AI. User said:\n{user_text}")
            else:
                # fallback: local LLaMA 3
                reply = llama3_answer(user_text)

            st.session_state.chat_history.append({"role": "bot", "text": reply})
            st.experimental_rerun()

# -------------------------------
# Settings
# -------------------------------
elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Prototype settings")
    st.checkbox("Enable demo notifications", value=True)
