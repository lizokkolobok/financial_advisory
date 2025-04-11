import os
import json
from datetime import datetime

def save_session(username, profile, advice):
    # Ensure sessions directory exists
    sessions_dir = "sessions"
    if not os.path.exists(sessions_dir):
        os.makedirs(sessions_dir)

    # Fallback session name if none is provided
    if not username:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username = f"session_{timestamp}"

    session_data = {
        "timestamp": str(datetime.now()),
        "profile": profile,
        "advice": advice
    }

    # Save session to a JSON file
    filepath = os.path.join(sessions_dir, f"{username}.json")
    with open(filepath, "w") as f:
        json.dump(session_data, f, indent=2)

def load_session(username):
    filepath = f"sessions/{username}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None


