import requests
import os
import uuid

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY") or ""

def get_gigachat_response(prompt):
    if not GIGACHAT_API_KEY:
        raise EnvironmentError("GIGACHAT_API_KEY environment variable is not set")

    token_response = requests.post(
        url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        headers={
            "Authorization": f"Basic {GIGACHAT_API_KEY}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4())
        },
        data={"scope": "GIGACHAT_API_PERS"},
        verify=False,  # WARNING: should be True in production
        timeout=10
    )
    token_response.raise_for_status()
    access_token = token_response.json()["access_token"]

    chat_response = requests.post(
        url="https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4())
        },
        json={
            "model": "GigaChat:latest",
            "messages": [
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "top_p": 0.9
        },
        verify=False,
        timeout=20
    )
    chat_response.raise_for_status()
    return chat_response.json()["choices"][0]["message"]["content"]
