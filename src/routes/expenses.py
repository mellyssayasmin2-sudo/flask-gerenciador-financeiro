from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from src.db import db
from src.config import Config
from src.models.user import User
from src.controllers.expenses import (
    create_expense, get_expenses, update_expense, delete_expense
)

expense_routes = Blueprint('expense_routes', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        header = request.headers.get('Authorization')

        if not header:
            return jsonify({'message': 'Token ausente!'}), 401

        parts = header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'message': 'Formato inválido!'}), 401

        token = parts[1]

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = db.session.get(User, data['user_id'])
        except:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(user, *args, **kwargs):
        if user.role != 'admin':
            return jsonify({'message': 'Acesso negado!'}), 403
        return f(user, *args, **kwargs)
    return decorated


@expense_routes.route('/expenses', methods=['POST'])
@token_required
def create_route(current_user):
    data = request.get_json()
    expense = create_expense(current_user.id, data)
    return jsonify({
        'id': expense.id,
        'category': expense.category,
        'amount': expense.amount
    }), 201


@expense_routes.route('/expenses', methods=['GET'])
@token_required
def get_route(current_user):
    filters = request.args.to_dict()
    expenses = get_expenses(current_user, filters)
    output = [{
        'id': e.id,
        'category': e.category,
        'amount': e.amount,
        'description': e.description,
        'date': e.date.isoformat()
    } for e in expenses]
    return jsonify({'expenses': output}), 200


@expense_routes.route('/expenses/<int:id>', methods=['PUT'])
@token_required
def update_route(current_user, id):
    data = request.get_json()
    result = update_expense(current_user, id, data)

    if result == 'unauthorized':
        return jsonify({'message': 'Acesso negado!'}), 403

    if not result:
        return jsonify({'message': 'Despesa não encontrada!'}), 404

    e = result
    return jsonify({
        'id': e.id,
        'category': e.category,
        'amount': e.amount
    }), 200


@expense_routes.route('/expenses/<int:id>', methods=['DELETE'])
@token_required
def delete_route(current_user, id):
    result = delete_expense(current_user, id)

    if result == 'unauthorized':
        return jsonify({'message': 'Acesso negado!'}), 403

    if not result:
        return jsonify({'message': 'Despesa não encontrada!'}), 404

    return jsonify({'message': 'Despesa removida!'}), 200
