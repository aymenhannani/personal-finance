# data_processing/financial_summary.py

def calculate_financial_summary(data, income_category_name='Income'):
    # Identify Income and Expense Transactions
    data['Category_Lower'] = data['Category'].str.lower()
    income_data = data[data['Category_Lower'] == income_category_name.lower()]
    expense_data = data[data['Category_Lower'] != income_category_name.lower()]

    # Calculate Totals
    total_income = income_data['Amount'].sum()
    total_expenses = expense_data['Amount'].sum()
    net_amount = total_income - total_expenses

    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_amount': net_amount,
        'income_data': income_data,
        'expense_data': expense_data
    }
