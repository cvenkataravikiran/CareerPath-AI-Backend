# backend/core/__init__.py

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import cloudinary
from .db import mongo
from config import config

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )

    # ======================= START: THE FIX =======================
    # Define the list of origins that are allowed to make requests to your API.
    # This includes your deployed frontend on Vercel and your local development environment.
    origins = [
        "https://career-path-ai-ochre.vercel.app/",  # Production Frontend
        "http://localhost:3000",                   # Local React Dev Server
        "http://127.0.0.1:3000"                    # Alternative Local
    ]

    # Apply a more specific CORS configuration. This explicitly tells the browser
    # that requests from your frontend are safe. It applies these rules to all
    # routes under the /api/ prefix.
    CORS(app, resources={r"/api/*": {"origins": origins}})
    # ======================== END: THE FIX ========================

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from api.auth_routes import auth_bp
    from api.roadmap_routes import roadmap_bp
    from api.user_routes import user_bp
    from api.explore_routes import explore_bp
    from api.chatbot_routes import chatbot_bp
    from api.tips_routes import tips_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(roadmap_bp, url_prefix='/api/roadmaps')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(explore_bp, url_prefix='/api/explore')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(tips_bp, url_prefix='/api/tips')

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the CareerPath AI Backend API!"})
    
    return app
