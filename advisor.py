# advisor.py

def generate_budget(monthly_income):
    """
    Returns a recommended budget dict.
    """
    inc = float(monthly_income or 0)
    return {
        "Food": round(inc * 0.25, 2),
        "Transport": round(inc * 0.15, 2),
        "Bills": round(inc * 0.30, 2),
        "Savings": round(inc * 0.20, 2),
        "Other": round(inc * 0.10, 2),
    }

def goal_progress(current, target):
    try:
        cur = float(current); tgt = float(target)
    except Exception:
        return 0.0
    if tgt <= 0:
        return 0.0
    return round(min(100.0, (cur / tgt) * 100.0), 2)

def investment_suggestions(risk="medium"):
    r = (risk or "medium").lower()
    if r == "low":
        return ["Government Bonds", "Fixed Deposits", "High-grade Corporate Bonds"]
    if r == "high":
        return ["Growth Stocks", "Selected Small-cap Funds", "Crypto (risky)"]
    return ["Index Funds", "Balanced Mutual Funds", "ETFs"]
