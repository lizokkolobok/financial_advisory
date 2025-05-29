import os
import json
from datetime import datetime

def save_session(username, profile, advice, model):
    sessions_dir = "sessions"
    os.makedirs(sessions_dir, exist_ok=True)

    if not username:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username = f"session_{timestamp}"

    session_data = {
        "timestamp": str(datetime.now()),
        "profile": profile,
        "advice": advice,
        "model": model  # ✅ Add model to be used in analytics
    }

    filepath = os.path.join(sessions_dir, f"{username}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

def load_session(username):
    filepath = f"sessions/{username}.json"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None



