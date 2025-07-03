import pandas as pd
from datetime import timedelta

def generate_suggestions(data):
    df = pd.DataFrame(data)
    
    # Convert to datetime with UTC awareness
    df['date'] = pd.to_datetime(df['date'], utc=True)
    
    now = pd.Timestamp.now(tz='UTC')
    last_30_days = now - timedelta(days=30)
    
    current_month = now.month
    previous_month = (now - timedelta(days=30)).month

    suggestions = []

    # Filter for last 30 days
    last_30_days_df = df[df['date'] >= last_30_days]

    # Total spending in last 30 days
    total_spent_30 = last_30_days_df['amount'].sum()

    # Spending by category in last 30 days
    last_30_spending = last_30_days_df.groupby('category')['amount'].sum()

    # Monthly spending by category
    df['month'] = df['date'].dt.month
    monthly_spending = df.groupby(['month', 'category'])['amount'].sum().unstack(fill_value=0)

    for category in last_30_spending.index:
        current = monthly_spending.loc[current_month, category] if current_month in monthly_spending.index else 0
        previous = monthly_spending.loc[previous_month, category] if previous_month in monthly_spending.index else 0

        # 📈 Increased spending compared to last month
        if previous > 0 and current > previous * 1.5:
            diff = current - previous
            suggestions.append(
                f"Your {category} spending increased by ₹{diff:.2f} this month. Consider reviewing it."
            )

        # ⚠️ High percentage of total
        percent = (last_30_spending[category] / total_spent_30) * 100 if total_spent_30 > 0 else 0
        if percent > 25:
            suggestions.append(
                f"You're spending {percent:.1f}% of your budget on {category}. Try to reduce it by 15%."
            )

    # 💰 Budgeting warning
    if total_spent_30 > 5000:
        suggestions.append(f"You spent ₹{total_spent_30:.2f} in the last 30 days. Consider setting a monthly budget.")

    return suggestions


def analyze_expenses(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], utc=True)

    now = pd.Timestamp.now(tz='UTC')
    last_30_days = now - timedelta(days=30)
    current_month = now.strftime('%Y-%m')

    recent_df = df[df['date'] >= last_30_days]
    total_spent_30 = recent_df['amount'].sum()
    category_spending = recent_df.groupby('category')['amount'].sum().sort_values(ascending=False)

    suggestions = []
    overbudget = []

    for category, amount in category_spending.items():
        percent = (amount / total_spent_30) * 100
        if percent > 25:
            suggestions.append(f"You're spending {percent:.1f}% of your budget on {category}. Try to reduce it by 15%.")
            overbudget.append(category)

    # Final smart tip
    if total_spent_30 > 5000:
        suggestions.append(f"You spent ₹{total_spent_30:.2f} in the last 30 days. Consider budgeting.")

    summary = {
        'month': current_month,
        'total_spent': total_spent_30,
        'top_category': category_spending.idxmax() if not category_spending.empty else 'N/A',
        'overbudget_categories': overbudget
    }

    return suggestions, summary
