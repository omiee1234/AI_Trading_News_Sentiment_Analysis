"""
Model Layer
Responsible for: Loading the ML model and raw inference only.
No business logic, no UI, no signal generation here.
"""

import json
from groq import Groq
from config.settings import API, GROQ_MODEL


class SentimentModel:
    """Wraps the Groq LLM for sentiment analysis."""

    _instance = None  # singleton so client initializes once

    def __init__(self):
        self._client = None

    # ------------------------------------------------------------------
    # Singleton factory
    # ------------------------------------------------------------------

    @classmethod
    def get_instance(cls) -> "SentimentModel":
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._load()
        return cls._instance

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Initialize Groq client."""
        if not API:
            raise ValueError(
                "API environment variable is not set. "
                "Please set your Groq API key to use this model."
            )

        self._client = Groq(api_key=API)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def predict(self, text: str) -> dict:
        """
        Returns sentiment analysis using Groq LLM.

        Parameters
        ----------
        text : str
            The text to analyze for sentiment.

        Returns
        -------
        dict  {"label": str, "score": float}
            label: "POSITIVE", "NEGATIVE", or "NEUTRAL"
            score: confidence score between 0.0 and 1.0
        """
        if self._client is None:
            raise RuntimeError("Model has not been loaded. Call _load() first.")

        prompt = f"""Analyze the sentiment of the following financial news text. 
You must respond with ONLY a valid JSON object (no markdown, no extra text) in this exact format:
{{"sentiment": "POSITIVE" or "NEGATIVE" or "NEUTRAL", "confidence": 0.0 to 1.0}}

News text: "{text}"

JSON response:"""

        try:
            completion = self._client.chat.completions.create(
                model=GROQ_MODEL,
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            response_text = completion.choices[0].message.content.strip()

            # Parse the JSON response
            result = json.loads(response_text)

            # Map sentiment labels to uppercase for consistency
            sentiment = result.get("sentiment", "NEUTRAL").upper()
            confidence = float(result.get("confidence", 0.5))

            # Ensure confidence is within [0, 1]
            confidence = max(0.0, min(1.0, confidence))

            return {
                "label": sentiment,
                "score": confidence,
            }

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Failed to parse Groq response as JSON: {response_text}"
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {str(exc)}") from exc
