from flask import Blueprint, request, jsonify
from src.controllers.auth import signup, login, promote_user
from src.routes.expenses import token_required, admin_required

auth_routes = Blueprint('auth', __name__, url_prefix='/auth')

@auth_routes.route('/signup', methods=['POST'])
def signup_route():
    data = request.get_json()
    response, status = signup(data)
    return jsonify(response), status

@auth_routes.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    response, status = login(data)
    return jsonify(response), status

@auth_routes.route('/promote/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def promote_route(current_user, user_id):
    response, status = promote_user(user_id)
    return jsonify(response), status
