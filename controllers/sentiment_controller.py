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
        # Call Groq API directly with enhanced prompt for full analysis
        prompt = f"""You are an expert financial trading analyst.

Analyze the following financial news and generate a trading signal based on professional market analysis.

You MUST respond with ONLY valid JSON (no markdown, no extra text).

JSON format:
{{
    "sentiment": "POSITIVE or NEGATIVE or NEUTRAL",
    "confidence": 0.0 to 1.0,
    "analysis": "Brief professional market analysis (1-2 sentences)",
    "signal": "BUY or SELL or HOLD"
}}

Trading Rules:
- POSITIVE sentiment + confidence >= 0.75 → BUY
- NEGATIVE sentiment + confidence >= 0.75 → SELL
- Mixed sentiment or confidence < 0.75 → HOLD
- NEUTRAL sentiment → HOLD

Financial News:
"{news}"

JSON response:"""

        try:
            completion = self.client.chat.completions.create(
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
            result = json.loads(response_text)

            label = result.get("sentiment", "NEUTRAL").upper()
            confidence_score = float(result.get("confidence", 0.5))
            confidence_score = max(0.0, min(1.0, confidence_score))
            confidence = round(confidence_score * 100, 2)
            
            # Get analysis and signal directly from Groq instead of hardcoded logic
            analysis = result.get("analysis", "Market analysis unavailable")
            signal = result.get("signal", "HOLD")
            
            # Add emoji to signal for UI
            signal_emoji_map = {
                "BUY": "BUY 📈",
                "SELL": "SELL 📉",
                "HOLD": "HOLD 😐"
            }
            signal_with_emoji = signal_emoji_map.get(signal.upper(), "HOLD 😐")

            return {
                "label":          label,
                "confidence":     confidence,
                "analysis":       analysis,
                "signal":         signal_with_emoji,
                "low_confidence": confidence < CONFIDENCE_THRESHOLD,
            }

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Failed to parse Groq response as JSON: {response_text}"
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {str(exc)}") from exc


