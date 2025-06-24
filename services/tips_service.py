# services/tips_service.py

import os
from openai import OpenAI
import random

# Configure the client to use Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# A list of diverse topics for the AI to generate tips about
TIP_TOPICS = [
    "a common mistake to avoid in React.js",
    "a useful git command for beginners",
    "a networking tip for landing a tech job",
    "a productivity hack for developers",
    "an explanation of REST APIs in simple terms",
    "a common data structure and its use case",
    "a tip for writing a better resume headline",
    "how to prepare for a technical interview",
    "the importance of a portfolio project",
    "a useful VS Code extension",
    "a quick explanation of Python list comprehensions",
    "a tip on how to deal with imposter syndrome"
]

def generate_daily_tip():
    """
    Asks the AI to generate a short, actionable tip based on a random topic.
    """
    # Choose a random topic to keep the tips fresh
    topic = random.choice(TIP_TOPICS)
    
    system_prompt = (
        "You are an AI that provides short, insightful, and actionable tips for people learning a career in technology. "
        "The tip should be a single, concise paragraph. Do not use any markdown or special formatting. "
        "Directly state the tip without any introductory phrases like 'Here's a tip:'."
    )
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Give me a tip about: {topic}"}
            ],
            temperature=0.9, # Higher temperature for more variety
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Daily tip AI service failed: {e}")
        # Provide a good default fallback tip if the API fails
        return "Consistency is key. Spending even 15-30 minutes learning every day is more effective than one long session per week."