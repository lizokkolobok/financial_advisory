import numpy as np
import pandas as pd

def monte_carlo_simulation(start_amount=10000, years=30, annual_return=0.07, volatility=0.15, n_simulations=500):
    np.random.seed(42)
    results = []
    for _ in range(n_simulations):
        prices = [start_amount]
        for _ in range(years):
            shock = np.random.normal(loc=annual_return, scale=volatility)
            new_value = prices[-1] * (1 + shock)
            prices.append(new_value)
        results.append(prices)
    return np.array(results)

def analyze_debt(df_loans):
    suggestions = []
    if df_loans.empty:
        return "No debt information provided."

    df_loans['Monthly Interest'] = df_loans['Balance'] * df_loans['InterestRate'] / 12
    df_loans['PriorityScore'] = df_loans['InterestRate'] / df_loans['MonthlyPayment']
    df_loans = df_loans.sort_values(by='PriorityScore', ascending=False)

    for row in df_loans.itertuples():
        suggestions.append(
            f"Pay down **{row.Type}** first (Balance: ${row.Balance}, Interest: {row.InterestRate*100:.2f}%)"
        )

    return "\n".join(suggestions)
