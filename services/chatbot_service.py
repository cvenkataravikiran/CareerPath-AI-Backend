# services/chatbot_service.py

import os
from openai import OpenAI

# The client configuration remains the same
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def get_chatbot_response(user_input):
    """
    Gets a response from the AI model for a given user input, with instructions to use Markdown.
    """
    # ---- THIS IS THE CRITICAL CHANGE ----
    # We are giving the AI a personality and strict formatting rules.
    system_prompt = (
        "You are CareerPath AI, a friendly and expert AI career assistant. "
        "Your goal is to provide clear, well-structured, and helpful advice. "
        "**Always format your response using Markdown.** "
        "Use headings (`##`), bold text (`**text**`), and bulleted lists (`-` or `*`) to make the information easy to read. "
        "For example, when asked for a career path, structure your response with clear sections like '## Key Skills', '## Salary Expectations', etc."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Chatbot AI service failed: {e}")
        return "I'm sorry, but I'm having trouble connecting to my knowledge base right now. Please try again in a moment."