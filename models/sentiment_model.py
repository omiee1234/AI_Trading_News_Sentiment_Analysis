"""
Model Layer
Responsible for: Loading the ML model and raw inference only.
No business logic, no UI, no signal generation here.
"""

import os
from transformers import pipeline


class SentimentModel:
    """Wraps the HuggingFace text-classification pipeline."""

    _instance = None  # singleton so model loads once

    def __init__(self, model_path: str = "./saved_model"):
        self.model_path = model_path
        self._classifier = None

    # ------------------------------------------------------------------
    # Singleton factory
    # ------------------------------------------------------------------

    @classmethod
    def get_instance(cls, model_path: str = "./saved_model") -> "SentimentModel":
        if cls._instance is None:
            cls._instance = cls(model_path)
            cls._instance._load()
        return cls._instance

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if self.model_path == "./saved_model" and not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Saved model directory not found: {self.model_path}.\n"
                "Place your HuggingFace model in ./saved_model or set MODEL_PATH to a valid model path."
            )

        try:
            self._classifier = pipeline(
                "text-classification",
                model=self.model_path,
                tokenizer=self.model_path,
            )
        except OSError as exc:
            raise RuntimeError(
                f"Unable to load HuggingFace model from '{self.model_path}'. "
                "Verify the path points to a valid local model directory or a HuggingFace repo ID."
            ) from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def predict(self, text: str) -> dict:
        """
        Returns raw model output.

        Returns
        -------
        dict  {"label": str, "score": float}
        """
        if self._classifier is None:
            raise RuntimeError("Model has not been loaded. Call _load() first.")

        result = self._classifier(text)
        return {
            "label": result[0]["label"],
            "score": result[0]["score"],
        }
