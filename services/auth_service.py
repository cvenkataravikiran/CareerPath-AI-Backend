# services/auth_service.py
from models.user_model import User
from datetime import datetime
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from core.db import mongo


def register_user(name, email, password):
    """
    Registers a new user, hashes their password, and saves them to the database.
    """
    existing = mongo.db.users.find_one({"email": email})
    if existing:
        raise ValueError("This email is already registered.")

    user = User(name=name, email=email, password=password, created_at=datetime.utcnow())
    user_dict = user.to_dict()
    mongo.db.users.insert_one(user_dict)
    return True

def login_user(email, password):
    """
    Authenticates a user and returns their data with access and refresh tokens if successful.
    """
    print(f"[DEBUG] Attempting login for email: {email}")
    data = mongo.db.users.find_one({"email": email})
    if not data:
        print("[DEBUG] No user found with that email.")
        return { 'message': "Invalid email or password" }, 401
    user = User.from_dict(data)
    print(f"[DEBUG] User found. Stored hash: {user.password}")
    if user and user.check_password(password):
        print("[DEBUG] Password check passed.")
        
        # Create both access and refresh tokens using Flask-JWT-Extended
        access_token = create_access_token(identity=user.public_id)
        refresh_token = create_refresh_token(identity=user.public_id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.public_id,
                'name': user.name,
                'email': user.email,
                'profile_photo': user.profile_photo,
                'planner': user.planner
            }
        }, 200
    print("[DEBUG] Password check failed.")
    return { 'message': "Invalid email or password" }, 401