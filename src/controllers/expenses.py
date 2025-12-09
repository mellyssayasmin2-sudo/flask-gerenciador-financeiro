from src.models.expense import Expense
from src.db import db
from datetime import datetime

def create_expense(user_id, data):
    expense = Expense(
        user_id=user_id,
        category=data['category'],
        amount=data['amount'],
        description=data.get('description')
    )
    db.session.add(expense)
    db.session.commit()
    return expense

def get_expenses(user, filters):
    query = Expense.query

    if user.role != 'admin':
        query = query.filter_by(user_id=user.id)

    if 'category' in filters:
        query = query.filter_by(category=filters['category'])

    if 'min_amount' in filters:
        query = query.filter(Expense.amount >= float(filters['min_amount']))

    if 'max_amount' in filters:
        query = query.filter(Expense.amount <= float(filters['max_amount']))

    if 'start_date' in filters and 'end_date' in filters:
        start = datetime.strptime(filters['start_date'], '%Y-%m-%d')
        end = datetime.strptime(filters['end_date'], '%Y-%m-%d')
        query = query.filter(Expense.date.between(start, end))

    return query.all()

def update_expense(user, expense_id, data):
    expense = Expense.query.get(expense_id)

    if not expense:
        return None

    if user.role != 'admin' and expense.user_id != user.id:
        return 'unauthorized'

    if 'category' in data:
        expense.category = data['category']
    if 'amount' in data:
        expense.amount = data['amount']
    if 'description' in data:
        expense.description = data['description']

    db.session.commit()
    return expense

def delete_expense(user, expense_id):
    expense = Expense.query.get(expense_id)

    if not expense:
        return False

    if user.role != 'admin' and expense.user_id != user.id:
        return 'unauthorized'

    db.session.delete(expense)
    db.session.commit()
    return True
    