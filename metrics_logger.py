import json, os
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer, util

# Load sentiment analyzer and embedding model
analyzer = SentimentIntensityAnalyzer()
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

###############################################################################
#  HELPERS
###############################################################################
def detect_framing(text: str) -> str:
    pos_kw = [
        "maximize returns", "growth", "aggressive", "higher yield",
        "upside potential", "outperform", "capital appreciation"
    ]
    neg_kw = [
        "minimize risk", "preserve capital", "low volatility", "defensive",
        "conservative", "downside protection", "safe investment"
    ]
    text_low = text.lower()
    pos = sum(kw in text_low for kw in pos_kw)
    neg = sum(kw in text_low for kw in neg_kw)
    if pos > neg:
        return "risk-positive"
    if neg > pos:
        return "risk-averse"
    if pos == neg == 0:
        return "neutral"
    return "mixed"

def compute_consistency(responses: list[str]) -> float | None:
    """Compute average cosine similarity among response embeddings."""
    if not responses or len(responses) < 2:
        return None
    embeddings = embed_model.encode(responses, convert_to_tensor=True)
    scores = [
        util.cos_sim(embeddings[i], embeddings[j]).item()
        for i in range(len(responses))
        for j in range(i + 1, len(responses))
    ]
    return round(sum(scores) / len(scores), 4) if scores else None

###############################################################################
#  MAIN LOGGER
###############################################################################
LOGFILE = "data/model_metrics.json"
os.makedirs("data", exist_ok=True)

def log_session_metrics(prompt: str,
                        response: str,
                        model_version: str,
                        username: str | None = None,
                        alt_responses: list[str] | None = None) -> None:
    """Append one row of metrics to model_metrics.json."""

    # Basic metrics
    verbosity = len(response.split())
    factuality = sum(
        "according to" in ln.lower() or "based on" in ln.lower()
        for ln in response.splitlines()
    )
    framing = detect_framing(response)
    risk_bias = framing in ("risk-positive", "risk-averse")
    sentiment_score = round(analyzer.polarity_scores(response)["compound"], 4)

    # Consistency score using multiple responses
    consistency_score = compute_consistency(alt_responses) if alt_responses else None

    # Final record
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": username,
        "model": model_version,
        "prompt_excerpt": prompt[:120],
        "verbosity": verbosity,
        "factuality": factuality,
        "framing": framing,
        "risk_bias_detected": risk_bias,
        "sentiment": sentiment_score,
        "consistency": consistency_score
    }

    # Load existing
    data: list[dict]
    if os.path.exists(LOGFILE):
        with open(LOGFILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append and save
    data.append(row)
    with open(LOGFILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)