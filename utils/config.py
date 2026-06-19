import os
from pathlib import Path
from dotenv import load_dotenv

# Absolute path to factcheck-agent/.env
env_path = Path(__file__).resolve().parent.parent / ".env"

# Force reload from this file
load_dotenv(dotenv_path=env_path, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))

# TEMP DEBUG
print("ENV FILE:", env_path)
print(
    "Gemini Key Loaded:",
    GEMINI_API_KEY[:15] if GEMINI_API_KEY else "None"
)
print(
    "Tavily Key Loaded:",
    TAVILY_API_KEY[:10] if TAVILY_API_KEY else "None"
)
print("Gemini Key Loaded:", GEMINI_API_KEY[:20])