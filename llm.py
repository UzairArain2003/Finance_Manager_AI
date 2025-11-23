# llm.py
import requests

def groq_answer(api_key: str, prompt: str):
    """
    Send a prompt to Groq LLaMA-3 API if key provided.
    Fallback to free local model (dummy) if API fails or key missing.
    """
    # If no API key, use dummy free response
    if not api_key:
        return f"[Free model] I understood: {prompt[:100]}..."  # simple dummy response

    try:
        # Correct Groq endpoint
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful finance assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        # Fallback free response if API fails
        return f"[Free model fallback] Could not reach Groq API: {str(e)}\nI understood: {prompt[:100]}..."
