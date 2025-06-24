from flask import jsonify

def success_response(data=None, message="", status_code=200):
    """
    Generates a standardized successful API response.
    """
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message, status_code=400):
    """
    Generates a standardized error API response.
    """
    response = {
        "success": False,
        "error": message,
        "data": None
    }
    return jsonify(response), status_code