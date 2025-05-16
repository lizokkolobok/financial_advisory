import os
import json
import pandas as pd
from collections import Counter
import re

def load_all_sessions():
    sessions = []
    session_dir = "sessions"
    if not os.path.exists(session_dir):
        return pd.DataFrame()

    for filename in os.listdir(session_dir):
        if filename.endswith(".json"):
            with open(os.path.join(session_dir, filename), "r", encoding="utf-8") as f:
                try:
                    session = json.load(f)
                    session["filename"] = filename
                    sessions.append(session)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue

    return pd.DataFrame(sessions)

def summarize_sessions(df):
    if df.empty:
        return {}, pd.DataFrame()

    # Basic Stats
    num_sessions = len(df)
    avg_length = int(df["advice"].apply(lambda x: len(x.split())).mean())

    # Top Keywords
    text_blob = " ".join(df["profile"].fillna("").tolist() + df["advice"].fillna("").tolist())
    words = re.findall(r'\b[a-z]{4,}\b', text_blob.lower())
    top_keywords = Counter(words).most_common(5)

    # Trait Aggregation
    trait_data = []
    for profile in df["profile"]:
        if "Personality Traits:" in profile:
            try:
                json_like = profile.split("Personality Traits:")[1].strip()
                traits = eval(json_like) if isinstance(json_like, str) else json_like
                trait_data.append(traits)
            except Exception as e:
                print(f"Failed to parse traits: {e}")
                continue

    traits_df = pd.DataFrame(trait_data)

    summary = {
        "num_sessions": num_sessions,
        "avg_length": avg_length,
        "top_keywords": top_keywords
    }

    return summary, traits_df



