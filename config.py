import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file!")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found. Check your .env file!")

LLM_MODEL = "gemini/gemini-2.5-flash-lite"
