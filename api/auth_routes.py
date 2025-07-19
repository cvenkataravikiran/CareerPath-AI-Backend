from flask import Blueprint, request
from services.auth_service import register_user, login_user
from utils.response_handler import success_response, error_response

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        result, status = register_user(data['name'], data['email'], data['password'])

        if status != 201:
            return error_response(result.get("message", "Registration failed"), status)

        # If registered successfully, log in the user
        login_result, _ = login_user(data['email'], data['password'])
        return success_response(login_result, 201)

    except Exception as e:
        return error_response(str(e), 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        result, status = login_user(data['email'], data['password'])

        if status != 200:
            return error_response(result.get("message", "Login failed"), status)

        return success_response(result, 200)

    except Exception as e:
        return error_response(str(e), 500)
