from core.db import mongo
from bson.objectid import ObjectId
import cloudinary.uploader

def get_user_profile(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
    if not user:
        raise Exception("User not found")
    user['_id'] = str(user['_id'])
    return user

def update_user_profile(user_id, data, photo_file):
    update_fields = {k: v for k, v in data.items() if k in ['name', 'headline', 'phone', 'linkedin', 'github']}

    if photo_file:
        upload_result = cloudinary.uploader.upload(photo_file)
        update_fields['photo'] = upload_result['secure_url']
    
    if not update_fields:
        return get_user_profile(user_id)

    mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': update_fields})
    return get_user_profile(user_id)

def update_user_planner(user_id, planner_data):
    """Updates the entire planner array for a specific user."""
    if not isinstance(planner_data, list):
        raise ValueError("Planner data must be a list of tasks.")
        
    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'planner': planner_data}}
    )
    # Return the updated user profile which now includes the new planner
    return get_user_profile(user_id)