from flask import Blueprint, request
from services.auth_service import register_user, login_user
from utils.response_handler import success_response, error_response

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        result = register_user(data['name'], data['email'], data['password'])
        # After successful registration, log them in to get a token
        login_result = login_user(data['email'], data['password'])
        return success_response(login_result, 201)
    except Exception as e:
        return error_response(str(e), 409)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        result = login_user(data['email'], data['password'])
        return success_response(result, 200)
    except Exception as e:
        return error_response(str(e), 401)