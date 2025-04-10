from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

# Database Models
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Categories
CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other']

# Routes
@app.route('/')
def index():
    # Get current month expenses
    current_month = datetime.now().month
    expenses = Expense.query.filter(
        db.extract('month', Expense.date) == current_month
    ).all()
    
    # Calculate totals
    total_spent = sum(exp.amount for exp in expenses)
    
    # Get budgets
    budgets = Budget.query.all()
    budget_data = []
    
    for budget in budgets:
        category_spent = sum(
            exp.amount for exp in expenses 
            if exp.category == budget.category
        )
        budget_data.append({
            'category': budget.category,
            'budget': budget.amount,
            'spent': category_spent,
            'remaining': budget.amount - category_spent
        })
    
    return render_template(
        'index.html',
        expenses=expenses[-5:],  # Show last 5 expenses
        total_spent=total_spent,
        budget_data=budget_data,
        categories=CATEGORIES
    )

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        
        expense = Expense(
            amount=amount,
            category=category,
            description=description
        )
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_expense.html', categories=CATEGORIES)

@app.route('/budgets', methods=['GET', 'POST'])
def budgets():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        
        # Check if budget exists for this category
        existing_budget = Budget.query.filter_by(category=category).first()
        
        if existing_budget:
            existing_budget.amount = amount
            flash('Budget updated successfully!', 'success')
        else:
            budget = Budget(category=category, amount=amount)
            db.session.add(budget)
            flash('Budget set successfully!', 'success')
        
        db.session.commit()
        return redirect(url_for('budgets'))
    
    budgets = Budget.query.all()
    return render_template('budgets.html', budgets=budgets, categories=CATEGORIES)

if __name__ == '__main__':
    app.run(debug=True)