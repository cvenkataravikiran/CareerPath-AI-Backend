from core.db import mongo
from bson.objectid import ObjectId
import cloudinary.uploader

def get_user_by_id(user_id):
    """Get user by their public_id or ObjectId for token refresh"""
    # Try to find by public_id first (used in JWT tokens)
    user = mongo.db.users.find_one({'public_id': user_id}, {'password': 0})
    if not user:
        # Fallback to ObjectId if public_id not found
        try:
            user = mongo.db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
        except:
            return None
    
    if not user:
        return None
    
    user['_id'] = str(user['_id'])
    return {
        'id': user.get('public_id', str(user['_id'])),
        'name': user.get('name'),
        'email': user.get('email'),
        'profile_photo': user.get('profile_photo'),
        'planner': user.get('planner', [])
    }

def get_user_profile(user_id):
    # Try public_id first (from JWT), then ObjectId
    user = mongo.db.users.find_one({'public_id': user_id}, {'password': 0})
    if not user:
        try:
            user = mongo.db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
        except:
            pass
    
    if not user:
        raise Exception("User not found")
    user['_id'] = str(user['_id'])
    return user

def update_user_profile(user_id, data, photo_file):
    update_fields = {k: v for k, v in data.items() if k in ['name', 'headline', 'phone', 'linkedin', 'github']}

    if photo_file:
        upload_result = cloudinary.uploader.upload(photo_file)
        update_fields['profile_photo'] = upload_result['secure_url']
    
    if not update_fields:
        return get_user_profile(user_id)

    # Update using public_id first, then ObjectId
    result = mongo.db.users.update_one({'public_id': user_id}, {'$set': update_fields})
    if result.matched_count == 0:
        try:
            mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': update_fields})
        except:
            pass
    
    return get_user_profile(user_id)

def update_user_planner(user_id, planner_data):
    """Updates the entire planner array for a specific user."""
    if not isinstance(planner_data, list):
        raise ValueError("Planner data must be a list of tasks.")
    
    # Update using public_id first, then ObjectId
    result = mongo.db.users.update_one({'public_id': user_id}, {'$set': {'planner': planner_data}})
    if result.matched_count == 0:
        try:
            mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'planner': planner_data}})
        except:
            pass
    
    return get_user_profile(user_id)