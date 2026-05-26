"""
Controller Layer
Responsible for: Business logic — turning raw model output into
market analysis, trading signals, and confidence checks.
No UI code lives here.
"""

from models.sentiment_model import SentimentModel
from config.settings import MODEL_PATH, CONFIDENCE_THRESHOLD


class SentimentController:
    """Orchestrates the prediction pipeline and enriches the result."""

    def __init__(self):
        self.model = SentimentModel.get_instance(MODEL_PATH)

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
        raw = self.model.predict(news)

        label      = raw["label"]
        confidence = round(raw["score"] * 100, 2)

        analysis, signal = self._interpret(label)

        return {
            "label":          label,
            "confidence":     confidence,
            "analysis":       analysis,
            "signal":         signal,
            "low_confidence": confidence < CONFIDENCE_THRESHOLD,
        }

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
