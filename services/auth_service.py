# services/auth_service.py
from models.user_model import User
from datetime import datetime, timedelta
import jwt
from flask import current_app
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
    Authenticates a user and returns their data and a JWT if successful.
    """
    data = mongo.db.users.find_one({"email": email})
    if not data:
        return { 'message': "Invalid email or password" }, 401
    user = User.from_dict(data)
    if user and user.check_password(password):
        token_payload = {
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(
            token_payload,
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return { 'token': token, 'name': user.name, 'email': user.email }, 200
    return { 'message': "Invalid email or password" }, 401