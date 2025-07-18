import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def setup_gemini():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("models/gemini-1.5-flash-latest")

def generate_allocation_response(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"