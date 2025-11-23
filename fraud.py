# fraud.py
import numpy as np

try:
    from sklearn.ensemble import IsolationForest
    _HAS_SK = True
except Exception:
    _HAS_SK = False

_model = None

def train_demo_model(X):
    """
    X: 2D array-like numeric (e.g., [[amount, hour, is_foreign], ...])
    Trains IsolationForest and stores it locally.
    """
    global _model
    if not _HAS_SK:
        return None
    Xarr = np.array(X)
    clf = IsolationForest(contamination=0.02, random_state=42)
    clf.fit(Xarr)
    _model = clf
    return _model

def check_transaction_vector(vec):
    """
    vec: [amount, hour] or similar.
    Returns "Fraud" or "Safe".
    If model not trained, fallback: amount threshold.
    """
    global _model
    arr = np.array(vec).reshape(1, -1)
    if _model is not None:
        pred = _model.predict(arr)
        return "Fraud" if pred[0] == -1 else "Safe"
    # fallback rule
    amount = float(arr[0,0])
    # threshold can be tuned
    return "Fraud" if amount > 5000 else "Safe"
