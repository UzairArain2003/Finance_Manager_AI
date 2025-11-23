# backend.py
import time
from nlp import extract_amounts, categorize

def process_ocr_text(text):
    """
    Simulated backend: parse amounts and categorize.
    Returns dict.
    """
    time.sleep(0.4)  # simulate light processing
    amounts = extract_amounts(text)
    amt = float(amounts[-1]) if amounts else 0.0
    cat = categorize(text)
    return {"parsed_text": text[:500], "category": cat, "amount": round(amt,2)}

def chat_response(user_msg):
    """
    Prototype rule-based chat reply.
    """
    m = (user_msg or "").lower()
    if "afford" in m or "buy" in m:
        return "Quick check: compare price to your remaining monthly budget. If under 10% of monthly budget, usually OK."
    if "save" in m:
        return "Automate 5-10% transfers to a saving account each payday. Small consistent amounts win."
    return "Tip: track recurring subscriptions and cancel unused ones."
