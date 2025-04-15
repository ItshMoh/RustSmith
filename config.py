"""
Configuration settings for Rustsmith
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB = os.getenv("MONGODB_DB", "rustsmith")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "user_contexts")


# Project output directory
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.join(os.path.dirname(__file__), "output"))

