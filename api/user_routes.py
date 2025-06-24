from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import get_user_profile, update_user_profile, update_user_planner
from utils.response_handler import success_response, error_response

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    try:
        profile = get_user_profile(user_id)
        return success_response(profile)
    except Exception as e:
        return error_response(str(e), 404)

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    profile_data = request.form.to_dict()
    profile_photo = request.files.get('photo')
    try:
        updated_profile = update_user_profile(user_id, profile_data, profile_photo)
        return success_response(updated_profile, message="Profile updated successfully")
    except Exception as e:
        return error_response(str(e), 500)

@user_bp.route('/planner', methods=['PUT'])
@jwt_required()
def update_planner():
    user_id = get_jwt_identity()
    planner_data = request.get_json()
    try:
        updated_user = update_user_planner(user_id, planner_data)
        # We only need to return the updated planner itself
        return success_response(updated_user.get('planner'), message="Planner updated successfully")
    except Exception as e:
        return error_response(str(e), 500)