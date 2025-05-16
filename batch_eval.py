import json
import os
from advisor import get_advice
from metrics_logger import log_session_metrics

# Sample profiles
user_profiles = [
    {
        "profile": "- Age: 55\n- Income: $30000\n- Experience: Beginner\n- Goal: Preserve capital with minimal risk\n- Time Horizon: 10 years\nPersonality Traits: {'Openness': 3, 'Conscientiousness': 4, 'Extraversion': 2, 'Agreeableness': 4, 'Neuroticism': 3}",
        "advisor_style": "Balanced",
        "risk_allocation": {"Low Risk": 70, "Medium Risk": 20, "High Risk": 10},
        "sectors": ["Finance"],
        "language": "English"
    },
    {
        "profile": "- Age: 22\n- Income: $20000\n- Experience: Beginner\n- Goal: Aggressive growth, especially in tech and crypto\n- Time Horizon: 15 years\nPersonality Traits: {'Openness': 5, 'Conscientiousness': 2, 'Extraversion': 4, 'Agreeableness': 3, 'Neuroticism': 2}",
        "advisor_style": "Aggressive growth coach",
        "risk_allocation": {"Low Risk": 10, "Medium Risk": 30, "High Risk": 60},
        "sectors": ["Tech", "ESG"],
        "language": "English"
    },
    {
        "profile": "- Age: 40\n- Income: $60000\n- Experience: Intermediate\n- Goal: Long-term growth with socially responsible investing\n- Time Horizon: 20 years\nPersonality Traits: {'Openness': 4, 'Conscientiousness': 5, 'Extraversion': 3, 'Agreeableness': 5, 'Neuroticism': 2}",
        "advisor_style": "Ethical investor advisor",
        "risk_allocation": {"Low Risk": 30, "Medium Risk": 50, "High Risk": 20},
        "sectors": ["ESG", "Consumer Goods"],
        "language": "English"
    },
    {
        "profile": "- Age: 30\n- Income: $150000\n- Experience: Intermediate\n- Goal: Plan a luxurious lifestyle\n- Time Horizon: 10 years\nPersonality Traits: {'Openness': 5, 'Conscientiousness': 2, 'Extraversion': 5, 'Agreeableness': 3, 'Neuroticism': 1}",
        "advisor_style": "Luxury lifestyle planner",
        "risk_allocation": {"Low Risk": 10, "Medium Risk": 30, "High Risk": 60},
        "sectors": ["Tech", "Consumer Goods"],
        "language": "English"
    },
    {
        "profile": "- Age: 65\n- Income: $50000\n- Experience: Intermediate\n- Goal: Conservative investment with tax optimization\n- Time Horizon: 5 years\nPersonality Traits: {'Openness': 3, 'Conscientiousness': 4, 'Extraversion': 2, 'Agreeableness': 4, 'Neuroticism': 3}",
        "advisor_style": "Balanced",
        "risk_allocation": {"Low Risk": 80, "Medium Risk": 15, "High Risk": 5},
        "sectors": ["Finance", "Healthcare"],
        "language": "English"
    },
    {
        "profile": "- Age: 35\n- Income: $150000\n- Experience: Expert\n- Goal: Invest in high-growth tech and AI startups\n- Time Horizon: 10 years\nPersonality Traits: {'Openness': 5, 'Conscientiousness': 4, 'Extraversion': 3, 'Agreeableness': 2, 'Neuroticism': 2}",
        "advisor_style": "Aggressive growth coach",
        "risk_allocation": {"Low Risk": 10, "Medium Risk": 30, "High Risk": 60},
        "sectors": ["Tech", "ESG"],
        "language": "English"
    },
    {
        "profile": "- Age: 45\n- Income: $70000\n- Experience: Intermediate\n- Goal: Save for children’s college and early retirement\n- Time Horizon: 15 years\nPersonality Traits: {'Openness': 3, 'Conscientiousness': 5, 'Extraversion': 3, 'Agreeableness': 4, 'Neuroticism': 3}",
        "advisor_style": "Balanced",
        "risk_allocation": {"Low Risk": 40, "Medium Risk": 40, "High Risk": 20},
        "sectors": ["Finance", "Consumer Goods"],
        "language": "English"
    },
    {
        "profile": "- Age: 28\n- Income: $60000\n- Experience: Intermediate\n- Goal: Gain exposure to blockchain and DeFi projects\n- Time Horizon: 8 years\nPersonality Traits: {'Openness': 5, 'Conscientiousness': 2, 'Extraversion': 4, 'Agreeableness': 3, 'Neuroticism': 2}",
        "advisor_style": "Minimalist advisor",
        "risk_allocation": {"Low Risk": 10, "Medium Risk": 20, "High Risk": 70},
        "sectors": ["Tech", "Finance"],
        "language": "English"
    },
    {
        "profile": "- Age: 38\n- Income: $80000\n- Experience: Beginner\n- Goal: Make socially responsible and low-risk investments\n- Time Horizon: 12 years\nPersonality Traits: {'Openness': 4, 'Conscientiousness': 5, 'Extraversion': 2, 'Agreeableness': 5, 'Neuroticism': 2}",
        "advisor_style": "Ethical investor advisor",
        "risk_allocation": {"Low Risk": 60, "Medium Risk": 30, "High Risk": 10},
        "sectors": ["ESG", "Healthcare"],
        "language": "English"
    },
    {
        "profile": "- Age: 32\n- Income: $120000\n- Experience: Intermediate\n- Goal: Support luxury lifestyle and frequent travel\n- Time Horizon: 5 years\nPersonality Traits: {'Openness': 5, 'Conscientiousness': 2, 'Extraversion': 5, 'Agreeableness': 3, 'Neuroticism': 2}",
        "advisor_style": "Luxury lifestyle planner",
        "risk_allocation": {"Low Risk": 20, "Medium Risk": 30, "High Risk": 50},
        "sectors": ["Consumer Goods", "Tech"],
        "language": "English"
    },
        {
        "profile": "- Age: 68\n- Income: $45000\n- Experience: Beginner\n- Goal: Preserve capital and cover retirement expenses\n- Time Horizon: 7 years\nPersonality Traits: {'Openness': 2, 'Conscientiousness': 4, 'Extraversion': 2, 'Agreeableness': 4, 'Neuroticism': 3}",
        "advisor_style": "Balanced",
        "risk_allocation": {"Low Risk": 85, "Medium Risk": 10, "High Risk": 5},
        "sectors": ["Healthcare", "Finance"],
        "language": "English"
    },
    {
        "profile": "- Age: 34\n- Income: $55000\n- Experience: Intermediate\n- Goal: Invest ethically and sustainably in European markets\n- Time Horizon: 12 years\nPersonality Traits: {'Openness': 4, 'Conscientiousness': 4, 'Extraversion': 3, 'Agreeableness': 5, 'Neuroticism': 2}",
        "advisor_style": "Ethical investor advisor",
        "risk_allocation": {"Low Risk": 40, "Medium Risk": 40, "High Risk": 20},
        "sectors": ["ESG", "Healthcare"],
        "language": "French"
    },
    {
        "profile": "- Age: 29\n- Income: $1000000\n- Experience: Beginner\n- Goal: Start investing in stable but growing companies in Russia\n- Time Horizon: 10 years\nPersonality Traits: {'Openness': 3, 'Conscientiousness': 5, 'Extraversion': 3, 'Agreeableness': 4, 'Neuroticism': 3}",
        "advisor_style": "Minimalist advisor",
        "risk_allocation": {"Low Risk": 50, "Medium Risk": 40, "High Risk": 10},
        "sectors": ["Consumer Goods", "Finance"],
        "language": "Russian"
    }
]

models = ["gpt-4o", "mistral", "gigachat"]

# Run each prompt 3 times for consistency calculation
for user in user_profiles:
    for model in models:
        responses = []

        prompt = f"""
You are a professional financial advisor.
Here's the user's profile:
{user['profile']}

Risk Allocation:
- Low Risk: {user['risk_allocation']['Low Risk']}%
- Medium Risk: {user['risk_allocation']['Medium Risk']}%
- High Risk: {user['risk_allocation']['High Risk']}%

Preferred sectors: {', '.join(user['sectors'])}
Advisor persona: {user['advisor_style']}
Language: {user['language']}

Provide 5 bullet points of personalized investment advice.
"""

        for i in range(3):
            try:
                advice = get_advice(prompt, model=model)
                responses.append(advice)
                print(f"Generated with model {model} for user {user.get('name', 'unnamed')}, run {i+1}")
            except Exception as e:
                print(f"Error for {user.get('name', 'unknown')} with {model}: {e}")

        if responses:
            log_session_metrics(
                prompt=prompt,
                response=responses[0],  # main response
                model_version=model,
                username=user.get("name", f"{user['advisor_style']}_{model}"),
                alt_responses=responses
            )