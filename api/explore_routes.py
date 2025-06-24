from flask import Blueprint, jsonify

explore_bp = Blueprint('explore_bp', __name__)

@explore_bp.route('/trending', methods=['GET'])
def get_trending_careers():
    # This serves the hardcoded data from your frontend via an API
    trending_careers = [
      { "title": "AI/ML Engineer", "description": "Build intelligent models that power the future of technology." },
      { "title": "Cybersecurity Analyst", "description": "Protect digital assets from threats and vulnerabilities." },
      { "title": "Cloud Solutions Architect", "description": "Design and manage robust, scalable cloud infrastructure." },
      { "title": "DevOps Engineer", "description": "Bridge the gap between development and operations for faster releases." },
      { "title": "Product Manager", "description": "Define the vision and strategy for successful tech products." },
      { "title": "UX/UI Designer", "description": "Create intuitive and beautiful user experiences for web and mobile." },
    ]
    return jsonify(trending_careers)