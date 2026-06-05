"""Configuration settings for the application"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/chatbot.db")

# Streamlit Configuration
STREAMLIT_THEME = os.getenv("STREAMLIT_THEME", "light")
