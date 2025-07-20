# api/auth_routes.py

from flask import Blueprint, request, current_app # <-- Import current_app for logging
from services.auth_service import register_user, login_user
from utils.response_handler import success_response, error_response

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'password')):
        return error_response("Missing name, email, or password", 400)

    try:
        # First, attempt to register the new user
        register_user(data['name'], data['email'], data['password'])
        
        # After successful registration, immediately log them in to get a token
        login_result, _ = login_user(data['email'], data['password']) # Assuming login_user returns a tuple
        
        # Return the login result with a '201 Created' status
        return success_response(login_result, 201)

    except Exception as e:
        # **UPDATED SECTION**
        # Log the actual, detailed error to your Flask terminal for debugging
        current_app.logger.error(f"Registration failed for email {data.get('email')}: {e}") 
        
        # Return a generic but helpful error message to the frontend
        # You can make this more specific if you check the type of exception `e`
        return error_response("Registration failed. The email may already be in use.", 400)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return error_response("Missing email or password", 400)

    try:
        # Attempt to log the user in
        result, status = login_user(data['email'], data['password']) # Assuming login_user returns a tuple
        
        if status != 200:
            return error_response(result.get("message", "Invalid credentials"), status)

        # Return the result (containing a token) with a '200 OK' status
        return success_response(result, 200)

    except Exception as e:
        # **UPDATED SECTION**
        current_app.logger.error(f"Login attempt failed for email {data.get('email')}: {e}")
        return error_response("Invalid email or password.", 401)