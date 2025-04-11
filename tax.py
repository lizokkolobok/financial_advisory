def generate_tax_tips(income, experience, time_horizon):
    try:
        income = float(income.replace(",", ""))
    except:
        income = 50000  # fallback default

    tips = []

    if income < 40000:
        tips.append("Consider a Roth IRA to allow tax-free withdrawals in retirement.")
        tips.append("Utilize standard deductions and potential Earned Income Tax Credit (EITC).")
    elif income < 100000:
        tips.append("Contribute to a Traditional IRA or 401(k) to reduce taxable income.")
        tips.append("Explore Health Savings Accounts (HSAs) if eligible.")
    else:
        tips.append("Max out 401(k) and HSA contributions to reduce your tax burden.")
        tips.append("Use tax-loss harvesting to offset capital gains.")
        tips.append("Consider municipal bonds for tax-free income.")

    if experience == "Beginner":
        tips.append("Start by using IRS tax calculators or consult a free advisor.")
    elif experience == "Expert":
        tips.append("Explore backdoor Roth IRA strategies and long-term capital gains optimization.")

    if time_horizon >= 10:
        tips.append("Consider estate planning tools like trusts or charitable donations for long-term tax efficiency.")

    return "\n\n".join([f"- {tip}" for tip in tips])
