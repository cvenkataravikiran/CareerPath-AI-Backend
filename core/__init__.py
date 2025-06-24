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

    # ======================= START: THE FIX =======================
    # This is a more robust and explicit CORS configuration that is less likely
    # to fail during preflight checks on production servers.

    # Define the exact origin of your frontend.
    origins = "https://career-path-ai-ochre.vercel.app"
    
    # We will now initialize CORS with very specific parameters.
    CORS(
        app,
        # This allows requests from your specific Vercel URL.
        origins=origins,
        # This allows cookies and authorization headers to be sent.
        supports_credentials=True,
        # This explicitly lists the HTTP methods your frontend is allowed to use.
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        # This explicitly lists the custom headers your frontend is allowed to send.
        allow_headers=["Content-Type", "Authorization"]
    )
    # ======================== END: THE FIX ========================

    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # --- Blueprint Registrations (No changes here) ---
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