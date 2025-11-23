# llm.py

# Optional Gemini import (only if installed)
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def configure_gemini(api_key: str):
    """
    Configure and return a GenAI client for Gemini.
    """
    if not GEMINI_AVAILABLE:
        raise ImportError("google-genai package is not installed")
    return genai.Client(api_key=api_key)

def gemini_answer(client, message: str):
    """
    Generate a response from Gemini using the GenAI client.
    """
    if not GEMINI_AVAILABLE:
        return "(Gemini not available)"
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message
        )
        return response.text
    except Exception as e:
        return f"(Gemini Error) {str(e)}"

def llama3_answer(message: str):
    """
    Local LLaMA 3 fallback (dummy response)
    """
    return f"(LLaMA 3 Reply) I understood: {message}"
