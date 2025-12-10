from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from src.db import db
from src.config import Config
from src.models.user import User
from src.controllers.expenses import (
    create_expense, get_expenses, update_expense, delete_expense
)

expense_routes = Blueprint('expenses', __name__, url_prefix='/expenses')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token não fornecido'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token inválido'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'message': 'Acesso negado'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@expense_routes.route('', methods=['POST'])
@token_required
def create_route(current_user):
    data = request.get_json()
    response, status = create_expense(current_user, data)
    return jsonify(response), status

@expense_routes.route('', methods=['GET'])
@token_required
def get_route(current_user):
    response, status = get_expenses(current_user)
    return jsonify(response), status

@expense_routes.route('/<int:id>', methods=['PUT'])
@token_required
def update_route(current_user, id):
    data = request.get_json()
    response, status = update_expense(current_user, id, data)
    return jsonify(response), status

@expense_routes.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_route(current_user, id):
    response, status = delete_expense(current_user, id)
    return jsonify(response), status
