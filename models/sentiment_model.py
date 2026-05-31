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
    Returns advanced financial sentiment analysis using Groq LLM.
    """

    if self._client is None:
        raise RuntimeError("Model has not been loaded. Call _load() first.")

    prompt = f"""
You are an expert AI financial trading analyst.

Analyze the following financial news.

You MUST return ONLY valid JSON.
Do not return markdown.
Do not return explanations outside JSON.

JSON format:
{{
    "sentiment": "POSITIVE or NEGATIVE or NEUTRAL",
    "confidence": 0.0,
    "analysis": "Brief professional market analysis",
    "signal": "BUY or SELL or HOLD"
}}

Rules:
- Strong positive news = BUY
- Strong negative news = SELL
- Mixed or uncertain news = HOLD
- Confidence must be between 0.0 and 1.0

Financial News:
"{text}"

JSON Response:
"""

    try:
        completion = self._client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=300,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        response_text = completion.choices[0].message.content.strip()

        # Parse JSON
        result = json.loads(response_text)

        sentiment = result.get("sentiment", "NEUTRAL").upper()
        confidence = float(result.get("confidence", 0.5))
        analysis = result.get(
            "analysis",
            "Market sentiment appears neutral."
        )
        signal = result.get("signal", "HOLD").upper()

        # Clamp confidence
        confidence = max(0.0, min(1.0, confidence))

        return {
            "label": sentiment,
            "score": confidence,
            "analysis": analysis,
            "signal": signal,
        }

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Failed to parse Groq response as JSON: {response_text}"
        ) from exc

    except Exception as exc:
        raise RuntimeError(f"Groq API call failed: {str(exc)}") from exc

