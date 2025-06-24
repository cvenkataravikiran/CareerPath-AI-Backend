import os
import json
import datetime
from openai import OpenAI # <-- Yes, you still use the OpenAI library!
from core.db import mongo
from bson.objectid import ObjectId

# NEW: Configure the client to point to Groq's API
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1", # <-- This is the magic line
)

def generate_roadmap_from_text(user_id, career_goal):
    # The prompt is the same as the one for Ollama/Mistral. Simple and direct.
    prompt = f"""
    You are a career planning AI that generates learning roadmaps in a specific JSON format.
    Your response MUST be a valid JSON object and nothing else. Do not add any text before or after the JSON.
    Create a detailed learning roadmap for a "{career_goal}".
    The root object must have "role_name", "estimated_time", and "levels".
    - "role_name" must be the career goal.
    - "estimated_time" must be a total time string (e.g., "6-9 Months").
    - "levels" must be an OBJECT with three keys: "beginner", "intermediate", "advanced".
    Each level must be an object with "title" and a "skills" array.
    Each object in the "skills" array must have "name" and a "resource" object with "title" and a valid "url".
    """
    try:
        # The API call is IDENTICAL to the OpenAI v1.0+ code
        response = client.chat.completions.create(
            # We use a recommended open-source model available on Groq, like Llama 3 or Mistral
            model="llama3-8b-8192", 
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that only responds with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            # Groq doesn't support the response_format parameter, so a strong prompt is key.
        )
        
        # The response content is a raw string that needs parsing
        roadmap_data = json.loads(response.choices[0].message.content)

        # Save to DB (this part remains the same)
        mongo.db.roadmaps.insert_one({
            "user_id": ObjectId(user_id),
            "career_goal": roadmap_data.get("role_name"),
            "created_at": datetime.datetime.utcnow(),
            "roadmap_data": roadmap_data
        })
        return roadmap_data
    except Exception as e:
        raise Exception(f"AI service failed: {e}")

# You would apply the same client configuration in resume_parser_service.py