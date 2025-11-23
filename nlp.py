# nlp.py
from PIL import Image
import re

try:
    import pytesseract
except Exception:
    pytesseract = None

PDF_PATH = "/mnt/data/NeuroCore AI .pdf"   # your uploaded project brief path

# ---------- OCR ----------
def extract_text_from_image(file_like):
    """
    file_like: file-like (what streamlit returns from file_uploader)
    Returns extracted text or placeholder if pytesseract not installed.
    """
    if pytesseract is None:
        return "(OCR unavailable — install pytesseract/tesseract) Example: Grocery $42.30"
    img = Image.open(file_like)
    text = pytesseract.image_to_string(img)
    return text

# ---------- Simple SMS / amount parsing ----------
AMOUNT_REGEX = r"(?:Rs\.?|PKR)?\s?[\u20B9\$]?\s?(\d{1,3}(?:[,\d]{0,3})*(?:\.\d{1,2})?)"

def extract_amounts(text):
    if not text:
        return []
    matches = re.findall(AMOUNT_REGEX, text)
    # clean commas
    return [m.replace(",", "") for m in matches if m.strip()]

# ---------- Simple rule-based categorization ----------
def categorize(text):
    t = (text or "").lower()
    if any(k in t for k in ["food", "grocery", "restaurant", "supermarket", "cafe"]):
        return "Food"
    if any(k in t for k in ["uber", "careem", "taxi", "ride", "transport", "bus"]):
        return "Transport"
    if any(k in t for k in ["shop", "store", "mall", "amazon", "shopping"]):
        return "Shopping"
    if any(k in t for k in ["bill", "electricity", "water", "gas", "utility"]):
        return "Bills"
    if any(k in t for k in ["salary", "payroll"]):
        return "Income"
    return "Other"
