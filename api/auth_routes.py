# api/auth_routes.py

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import register_user, login_user
from services.user_service import get_user_by_id
from utils.response_handler import success_response, error_response
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'password')):
        return error_response("Missing name, email, or password", 400)

    try:
        # First, attempt to register the new user
        register_user(data['name'], data['email'], data['password'])
        
        # After successful registration, immediately log them in to get tokens
        login_result, _ = login_user(data['email'], data['password'])
        
        # Return the login result with a '201 Created' status
        return success_response(login_result, 201)

    except Exception as e:
        current_app.logger.error(f"Registration failed for email {data.get('email')}: {e}") 
        return error_response("Registration failed. The email may already be in use.", 400)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return error_response("Missing email or password", 400)

    try:
        # Attempt to log the user in
        result, status = login_user(data['email'], data['password'])
        
        if status != 200:
            return error_response(result.get("message", "Invalid credentials"), status)

        # Return the result (containing access and refresh tokens) with a '200 OK' status
        return success_response(result, 200)

    except Exception as e:
        current_app.logger.error(f"Login attempt failed for email {data.get('email')}: {e}")
        return error_response("Invalid email or password.", 401)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint to refresh the access token using a valid refresh token.
    The refresh token must be sent in the Authorization header.
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get updated user data
        user_data = get_user_by_id(current_user_id)
        if not user_data:
            return error_response("User not found", 404)
        
        # Create a new access token
        new_access_token = create_access_token(identity=current_user_id)
        
        return success_response({
            "access_token": new_access_token,
            "user": user_data
        }, 200)
    except Exception as e:
        current_app.logger.error(f"Token refresh failed: {e}")
        return error_response("Failed to refresh token", 401)