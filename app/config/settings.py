from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    # List of Models
    ALLOWED_MODEL_NAMES = ["llama-3.1-8b-instant",
                           "llama3-70b-8192"]
    



settings = Settings()