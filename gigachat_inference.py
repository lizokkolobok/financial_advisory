import requests
import uuid

AUTH_HEADER = ""
TOKEN_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

def get_access_token():
    headers = {
        "Authorization": f"Basic {AUTH_HEADER}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4())  
    }
    data = {
        "scope": "GIGACHAT_API_PERS"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get token: {response.status_code}, {response.text}")

def get_gigachat_response(prompt: str) -> str:
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4())
    }

    payload = {
        "model": "GigaChat:latest",
        "messages": [
            {"role": "system", "content": "You are a helpful financial advisor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post(CHAT_URL, headers=headers, json=payload, verify=False)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"GigaChat API error: {response.status_code}, {response.text}")





