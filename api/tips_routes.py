# api/tips_routes.py

from flask import Blueprint
from services.tips_service import generate_daily_tip
from utils.response_handler import success_response

tips_bp = Blueprint('tips_bp', __name__)

@tips_bp.route('/daily', methods=['GET'])
def get_daily_tip_route():
    """
    API endpoint to fetch a single, AI-generated daily tip.
    """
    tip = generate_daily_tip()
    return success_response({"daily_tip": tip})