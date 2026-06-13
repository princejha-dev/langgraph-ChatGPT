"""Configuration settings for the application"""
import os
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()

# Tools api key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Database Configuration
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(ROOT_DIR, "data", "chatbot.db"))

# Streamlit Configuration
STREAMLIT_THEME = os.getenv("STREAMLIT_THEME", "light")
