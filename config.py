import os
from dotenv import load_dotenv

load_dotenv()



GEMINI = "gemini"
OPENROUTER = "openrouter"

GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

OPENROUTER_MODEL = "openai/gpt-oss-120b"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

LLM_PROVIDER = OPENROUTER
if LLM_PROVIDER == OPENROUTER:
    LLM_MODEL = OPENROUTER_MODEL
elif LLM_PROVIDER == GEMINI:
    LLM_MODEL = GEMINI_MODEL
else:
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in .env")

if not MONGODB_DATABASE:
    raise ValueError("MONGODB_DATABASE not found in .env")