from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from services.roadmap_service import generate_roadmap_from_text
from services.resume_parser_service import generate_roadmap_from_resume
from utils.response_handler import success_response, error_response

roadmap_bp = Blueprint('roadmap_bp', __name__)

@roadmap_bp.route('/generate-by-text', methods=['POST'])
def generate_by_text():
    # user_id = get_jwt_identity()  # Not used if not authenticated
    data = request.get_json()
    career_goal = data.get('goal')
    user_id = data.get('user_id', None)  # Optionally allow user_id in body for testing
    try:
        roadmap = generate_roadmap_from_text(user_id, career_goal)
        return success_response(roadmap, 201)
    except Exception as e:
        return error_response(f"Failed to generate roadmap: {str(e)}", 500)

@roadmap_bp.route('/generate-by-resume', methods=['POST'])
def generate_by_resume():
    # user_id = get_jwt_identity()  # Not used if not authenticated
    file = request.files.get('resume')
    user_id = request.form.get('user_id', None)  # Optionally allow user_id in form for testing
    if not file:
        return error_response("No resume file provided", 400)
    try:
        file_bytes = file.read()
        roadmap = generate_roadmap_from_resume(user_id, file_bytes)
        return success_response(roadmap, 201)
    except Exception as e:
        return error_response(f"Failed to process resume: {str(e)}", 500)