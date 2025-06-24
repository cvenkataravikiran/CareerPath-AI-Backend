import pdfplumber
import os
import io
from openai import OpenAI # Keep using the OpenAI library
from .roadmap_service import generate_roadmap_from_text

# UPDATED: Configure the client to point to Groq's API
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), # <-- Use the correct key name
    base_url="https://api.groq.com/openai/v1",
)

def extract_text_from_pdf(pdf_bytes):
    """Extracts raw text content from a PDF provided as bytes."""
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Could not read PDF file. It might be corrupted or image-based. Error: {e}")


def get_goal_from_resume_text(text):
    """Uses Groq to infer the most likely career goal from resume text."""
    if not text.strip():
        raise ValueError("Resume appears to be empty or could not be read.")

    prompt = f"""
    Analyze the following resume text and identify the most likely career goal or target job title for this person.
    Focus on job titles in the experience section, the summary/objective section, and key technical skills to infer the role.
    Return only the job title as a simple string, for example: "Full Stack Developer" or "Data Scientist". Do not add any other text.

    Resume Text (first 4000 characters):
    ---
    {text[:4000]}
    ---
    Inferred Career Goal:
    """
    try:
        # UPDATED: The API call is now to Groq
        response = client.chat.completions.create(
            model="llama3-8b-8192", # Using a fast model on Groq
            messages=[
                {"role": "system", "content": "You are an expert HR analyst who is skilled at identifying career roles from resumes. Respond only with the job title."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=50
        )
        goal = response.choices[0].message.content.strip().replace('"', '')
        if not goal:
            raise Exception("AI could not determine a career goal from the resume.")
        return goal
    except Exception as e:
        print(f"Error calling AI for resume parsing: {e}")
        raise


def generate_roadmap_from_resume(user_id, pdf_bytes):
    """Orchestrates the resume-to-roadmap generation process."""
    resume_text = extract_text_from_pdf(pdf_bytes)
    career_goal = get_goal_from_resume_text(resume_text)
    
    # This will now use the Groq-configured client in roadmap_service.py
    return generate_roadmap_from_text(user_id, career_goal)