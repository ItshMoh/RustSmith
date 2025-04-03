"""
Configuration settings for Rustsmith
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://mohcodes:SitARam%40108@mlproject.yu0js.mongodb.net/?retryWrites=true&w=majority&appName=MlProject")
MONGODB_DB = os.getenv("MONGODB_DB", "rustsmith")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "user_contexts")

# API keys for different LLM providers
API_KEYS = {
    "master": os.getenv("MASTER_API_KEY"),
    "struct": os.getenv("STRUCT_API_KEY"),
    "type": os.getenv("TYPE_API_KEY"),
    "utility": os.getenv("UTILITY_API_KEY"),
    "smith": os.getenv("SMITH_API_KEY"),
}

# Project output directory
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.join(os.path.dirname(__file__), "output"))

# Default model settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8000"))