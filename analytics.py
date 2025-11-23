# analytics.py
import pandas as pd
import numpy as np

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    _HAS_STATS = True
except Exception:
    _HAS_STATS = False

def summarize_by_category(df):
    """
    df: DataFrame with columns ['category','amount']
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["category","amount"])
    return df.groupby("category", as_index=False)["amount"].sum()

def simple_forecast(series, periods=3):
    """
    series: list or pd.Series of historical totals (e.g., monthly totals)
    returns list of forecasted floats
    """
    if len(series) == 0:
        return [0.0]*periods

    if _HAS_STATS and len(series) >= 3:
        try:
            model = ExponentialSmoothing(np.array(series), trend="add", seasonal=None)
            fit = model.fit(optimized=True)
            preds = fit.forecast(periods)
            return [float(round(x,2)) for x in preds]
        except Exception:
            pass

    # fallback: mean of last 3 or whole series
    if len(series) >= 3:
        base = float(np.mean(series[-3:]))
    else:
        base = float(np.mean(series))
    return [round(base, 2)] * periods
