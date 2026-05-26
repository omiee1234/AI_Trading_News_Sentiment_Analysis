"""
App-wide configuration.
Override any value with environment variables for different deployments.
"""

import os

# Path to the saved HuggingFace model directory
MODEL_PATH: str = os.getenv("MODEL_PATH", "./saved_model")

# Predictions below this threshold trigger a low-confidence warning in the UI
CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "70"))
