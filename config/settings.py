"""
App-wide configuration.
Override any value with environment variables for different deployments.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Groq API configuration
API: str = os.getenv("API", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Predictions below this threshold trigger a low-confidence warning in the UI
CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "70"))
