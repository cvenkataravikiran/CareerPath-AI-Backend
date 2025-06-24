
from core.db import mongo
from core import bcrypt
from flask_jwt_extended import create_access_token
import datetime

def register_user(name, email, password):
    users = mongo.db.users
    existing_user = users.find_one({'email': email})
    if existing_user:
        raise Exception("User with this email already exists")

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Add all fields from your ProfilePage.js
    new_user = {
        "name": name,
        "email": email,
        "password_hash": hashed_password,
        "role": "user",
        "created_at": datetime.datetime.utcnow(),
        "headline": "Aspiring Professional",
        "phone": "",
        "linkedin": "",
        "github": "",
        "photo": "" # Starts with no photo
    }
    
    users.insert_one(new_user)
    return {"message": "User registered successfully"}

def login_user(email, password):
    users = mongo.db.users
    user = users.find_one({'email': email})

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        user_id = str(user['_id'])
        # Prepare user data to send to the frontend, excluding sensitive info
        user_data_for_token = {
            "id": user_id,
            "name": user.get('name'),
            "email": user.get('email'),
            "headline": user.get('headline'),
            "phone": user.get('phone'),
            "linkedin": user.get('linkedin'),
            "github": user.get('github'),
            "photo": user.get('photo')
        }
        
        access_token = create_access_token(identity=user_id, expires_delta=datetime.timedelta(days=7))
        # The frontend expects the user data and the token together
        return {**user_data_for_token, "access_token": access_token}
    else:
        raise Exception("Invalid email or password")