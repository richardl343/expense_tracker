# expense_tracker

## Files included:

1.app.py (main application)
2.templates/ (all HTML templates)
3.requirements.txt
4.expenses.db (SQLite database)

## How to run:

1.Install requirements: pip install -r requirements.txt
2.Run the app: python app.py
3.Access at http://localhost:5000

## Test Cases

### Budget Management
1. Set budget for "Food" (₹1000)
2. Set budget for "Transport" (₹500)
3. Verify budgets appear in /budgets

### Expense Tracking
1. Add expense: "Groceries" (₹200, Food)
2. Add expense: "Bus fare" (₹50, Transport)
3. Verify expenses appear on homepage

### Budget Alerts
1. Add ₹900 Food expense
2. Verify Food progress bar turns red (110% spent)
3. Check console for warning message

### Edge Cases
1. Try adding non-numeric amount
2. Try submitting empty form
3. Verify proper error messages
