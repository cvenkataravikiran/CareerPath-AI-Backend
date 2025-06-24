# CareerPath-AI-Backend
This is the backend for CareerPath AI, a full-stack web application designed to be a personal career co-pilot. This server is built with Flask and Python, and it handles all logics, database interactions, user authentication, and communication with the AI services.
---
# Frontend Repo 
  Link : https://github.com/cvenkataravikiran/CareerPath-AI-Frontend.git

## ✨ Core Features

- **RESTful API:** A well-structured API built with Flask and Blueprints for modularity.
- **AI Integration:** Connects to the Groq API (using the OpenAI SDK) to power roadmap generation, resume analysis, and the conversational chatbot.
- **Secure Authentication:** Implements user registration and login with password hashing (Bcrypt) and protected routes using JSON Web Tokens (JWT).
- **Database Management:** Uses MongoDB to store user profiles, generated roadmaps, and planner data.
- **Cloud Media Uploads:** Integrates with Cloudinary for seamless and secure user profile photo uploads.
- **PDF Resume Parsing:** Extracts text from uploaded PDF resumes to be analyzed by the AI.

---

## 🛠️ Technology Stack

- **Framework:** Flask
- **Language:** Python
- **Database:** MongoDB (with Flask-PyMongo)
- **Authentication:** Flask-JWT-Extended, Flask-Bcrypt
- **AI & Services:** Groq API (via OpenAI SDK), Cloudinary
- **PDF Parsing:** pdfplumber
- **CORS Handling:** Flask-CORS
- **Environment Management:** python-dotenv

----
## 🚀 Getting Started

1.  **Clone the repository:**
    ```
    git clone https://github.com/cvenkataravikiran/CareerPath-AI-Backend.git
    cd careerpath-ai/backend
    ```

2.  **Create and activate a virtual environment:**
    ```
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a file named `.env` in the `backend` directory and add the following, replacing the placeholder values with your actual credentials:

    ```.env
    # Flask & JWT Configuration
    SECRET_KEY='a_very_strong_random_secret_key'
    JWT_SECRET_KEY='another_very_strong_random_jwt_secret'

    # Database Configuration
    MONGO_URI='your_mongodb_connection_string'

    # AI Service API Key
    GROQ_API_KEY='your_groq_api_key'

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME='your_cloudinary_cloud_name'
    CLOUDINARY_API_KEY='your_cloudinary_api_key'
    CLOUDINARY_API_SECRET='your_cloudinary_api_secret'
    ```

5.  **Run the Flask server:**
    ```
    python run.py
    ```
    The server will start, typically on `http://127.0.0.1:5000`
