import pandas as pd

def parse_transaction_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return f"Error loading CSV: {e}", None

    required_cols = ['Date', 'Description', 'Amount']
    if not all(col in df.columns for col in required_cols):
        return "CSV must contain 'Date', 'Description', and 'Amount' columns.", None

    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df = df.dropna(subset=['Amount'])

    # Define simple keyword-based categories
    categories = {
        'Essentials': ['rent', 'grocery', 'utilities', 'insurance', 'transport', 'health', 'fuel'],
        'Discretionary': ['restaurant', 'entertainment', 'shopping', 'subscription', 'netflix', 'travel'],
        'Savings/Investments': ['investment', 'retirement', 'transfer', 'brokerage', 'wealthfront']
    }

    def classify(description):
        description = str(description).lower()
        for category, keywords in categories.items():
            if any(word in description for word in keywords):
                return category
        return 'Other'

    df['Category'] = df['Description'].apply(classify)
    summary = df.groupby('Category')['Amount'].sum().reset_index()
    summary.columns = ['Category', 'Total Spent']
    summary['Total Spent'] = summary['Total Spent'].round(2)

    return None, summary
