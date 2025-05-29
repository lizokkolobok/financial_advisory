import pandas as pd

def generate_portfolio(risk_profile, sectors=None, risk_allocation=None):
    if sectors is None:
        sectors = ['Tech', 'Healthcare', 'Energy', 'Finance']
    
    # Extract risk string if risk_profile is a dict
    if isinstance(risk_profile, dict):
        risk_profile_str = risk_profile.get("risk", "").lower()
    else:
        risk_profile_str = str(risk_profile).lower()

    if risk_allocation is None:
        if "cautious" in risk_profile_str:
            risk_allocation = {'Low Risk': 60, 'Medium Risk': 30, 'High Risk': 10}
        elif "aggressive" in risk_profile_str:
            risk_allocation = {'Low Risk': 20, 'Medium Risk': 30, 'High Risk': 50}
        else:
            risk_allocation = {'Low Risk': 40, 'Medium Risk': 40, 'High Risk': 20}

    data = []
    for sector in sectors:
        for risk_level, percent in risk_allocation.items():
            data.append({
                "Sector": sector,
                "Risk Level": risk_level,
                "Allocation (%)": round(percent / len(sectors), 2)
            })

    return pd.DataFrame(data)


