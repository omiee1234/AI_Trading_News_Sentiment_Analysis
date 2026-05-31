"""
Controller Layer
Responsible for: Business logic — turning raw model output into
market analysis, trading signals, and confidence checks.
No UI code lives here.
"""

import json
from groq import Groq
from config.settings import API, GROQ_MODEL, CONFIDENCE_THRESHOLD


class SentimentController:
    """Orchestrates the prediction pipeline with direct API calls."""

    def __init__(self):
        if not API:
            raise ValueError(
                "API environment variable is not set. "
                "Please set your Groq API key in the .env file."
            )
        self.client = Groq(api_key=API)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze(self, news: str) -> dict:
        """
        Run the full analysis pipeline for a news string.

        Parameters
        ----------
        news : str   Raw financial news text from the user.

        Returns
        -------
        dict with keys:
            label, confidence, analysis, signal, low_confidence (bool)
        """
        # Call Groq API directly
        prompt = f"""Analyze the sentiment of the following financial news text. 
You must respond with ONLY a valid JSON object (no markdown, no extra text) in this exact format:
{{"sentiment": "POSITIVE" or "NEGATIVE" or "NEUTRAL", "confidence": 0.0 to 1.0}}

News text: "{news}"

JSON response:"""

        try:
            completion = self.client.chat.completions.create(
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
            result = json.loads(response_text)

            label = result.get("sentiment", "NEUTRAL").upper()
            confidence_score = float(result.get("confidence", 0.5))
            confidence_score = max(0.0, min(1.0, confidence_score))
            confidence = round(confidence_score * 100, 2)

            analysis, signal = self._interpret(label)

            return {
                "label":          label,
                "confidence":     confidence,
                "analysis":       analysis,
                "signal":         signal,
                "low_confidence": confidence < CONFIDENCE_THRESHOLD,
            }

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Failed to parse Groq response as JSON: {response_text}"
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {str(exc)}") from exc

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _interpret(label: str) -> tuple[str, str]:
        """Map a model label to (analysis_text, trading_signal)."""

        label_lower = label.lower()

        if "bullish" in label_lower:
            analysis = (
                "The news reflects positive market sentiment "
                "and may indicate strong investor confidence. "
                "This could create upward momentum in the stock price."
            )
            signal = "BUY 📈"

        elif "bearish" in label_lower:
            analysis = (
                "The news reflects negative market sentiment "
                "and may indicate selling pressure or investor concerns. "
                "This could lead to downward market movement."
            )
            signal = "SELL 📉"

        else:
            analysis = (
                "The news appears balanced or uncertain. "
                "Market direction may remain stable until stronger signals emerge."
            )
            signal = "HOLD 😐"

        return analysis, signal
