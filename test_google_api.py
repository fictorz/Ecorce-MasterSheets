import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load from .env

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set!")

genai.configure(api_key=api_key)

# genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content("Hello")
print(response)