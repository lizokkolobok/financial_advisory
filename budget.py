import pandas as pd

def generate_budget_plan(income):
    try:
        income = float(income.replace(",", ""))
    except:
        income = 50000  # fallback default for parsing errors

    essentials = round(income * 0.50, 2)
    discretionary = round(income * 0.30, 2)
    savings = round(income * 0.20, 2)

    data = {
        "Category": ["Essentials", "Discretionary", "Savings/Investments"],
        "Amount (USD)": [essentials, discretionary, savings],
        "Suggested %": [50, 30, 20],
        "Description": [
            "Rent, food, transportation, insurance, healthcare",
            "Entertainment, dining, subscriptions, travel",
            "Emergency fund, retirement, investments"
        ]
    }

    return pd.DataFrame(data)
