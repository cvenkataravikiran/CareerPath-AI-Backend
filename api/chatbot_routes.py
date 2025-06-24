# api/chatbot_routes.py

from flask import Blueprint, request
from utils.response_handler import success_response, error_response
from services.chatbot_service import get_chatbot_response  # <-- IMPORT THE NEW SERVICE

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'input' not in data:
        return error_response("Missing 'input' in request body", 400)
    
    user_input = data.get('input')
    if not user_input.strip():
        return error_response("Input cannot be empty", 400)

    try:
        # ---- THIS IS THE CRITICAL CHANGE ----
        # REMOVE the old mocked response:
        # bot_response = f"This is a real backend response for: '{user_input}'. The real AI logic is coming soon!"
        
        # NEW: Call the real AI service to get a response
        bot_response_text = get_chatbot_response(user_input)
        
        # The success_response function wraps our text in the correct JSON format
        return success_response({"response": bot_response_text})
    
    except Exception as e:
        # This will catch any unexpected errors during the process
        print(f"Error in chatbot route: {e}")
        return error_response("An error occurred while processing your request.",500)
    