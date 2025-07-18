def build_allocation_prompt(user_profile):
    return f"""
    You are a financial advisor AI.
    The user name is  {user_profile['name']} is {user_profile['age']} years old and wants to invest ₹{user_profile['monthly_investment']} monthly.
    Investment goal: {user_profile['goal']}.
    Investment horizon: {user_profile['horizon']} years.
    Risk level: {user_profile['risk_level']}.

    Based on this, suggest an ideal portfolio allocation. Provide percentages for:
    - Equity mutual funds (large cap, mid cap, small cap)
    - Index funds or ETFs
    - Gold ETFs
    - Bonds / Debt mutual funds
    - Fixed deposits or savings

    Include 1-2 example funds or instruments for each category.
    Keep the tone friendly but professional.
    """

def analyze_portfolio_csv(df):
    tickers = ", ".join(df['Stock'].tolist())
    return f"""
    The user has uploaded a portfolio with the following holdings:
    {df.to_string(index=False)}

    Review this portfolio and:
    - Identify if the portfolio is well-diversified.
    - Highlight any overexposure to a sector or stock.
    - Suggest rebalancing recommendations aligned with moderate risk profile.
    - Recommend reducing underperforming or high-risk holdings.
    """