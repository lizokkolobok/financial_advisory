def get_advisor_tone(style):
    tones = {
        "Balanced": "Respond in a balanced, professional tone.",
        "Minimalist advisor": "Give short, clear, and minimal responses.",
        "Aggressive growth coach": "Sound confident and emphasize high returns.",
        "Ethical investor advisor": "Focus on ESG and ethical investment principles.",
        "Luxury lifestyle planner": "Frame investments around luxury, prestige, and lifestyle upgrades."
    }
    return tones.get(style, "Respond in a balanced, professional tone.")
