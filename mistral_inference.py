import requests
import os

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY") or ""

def get_mistral_response(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small",  # Or "mistral-medium" if enabled
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload, timeout=20)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
