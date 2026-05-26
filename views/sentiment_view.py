"""
View Layer
Responsible for: All Streamlit rendering — inputs, outputs, layout.
Zero business logic or model calls belong here.
"""

import streamlit as st
from controllers.sentiment_controller import SentimentController


def configure_page() -> None:
    st.set_page_config(
        page_title="AI Trading Sentiment",
        layout="centered",
    )


def render_header() -> None:
    st.title("📈 AI Trading Sentiment Analyzer")
    st.write("Analyze financial market news using AI")


def render_input() -> str:
    return st.text_area("Enter Financial News")


def render_analyze_button() -> bool:
    return st.button("Analyze Sentiment")


def render_result(result: dict) -> None:
    """Render the full analysis result returned by the controller."""

    # --- Prediction ---
    st.subheader("Prediction Result")
    st.write(f"Sentiment: {result['label']}")
    st.write(f"Confidence: {result['confidence']}%")

    # --- Market Analysis ---
    st.subheader("Market Analysis")
    st.write(result["analysis"])

    # --- Trading Signal ---
    st.subheader("Trading Signal")
    signal = result["signal"]

    if "BUY" in signal:
        st.success(signal)
    elif "SELL" in signal:
        st.error(signal)
    else:
        st.info(signal)

    # --- Low-confidence warning ---
    if result["low_confidence"]:
        st.warning(
            "Low confidence prediction. "
            "Use additional market confirmation."
        )


def render_empty_warning() -> None:
    st.warning("Please enter financial news")


# ------------------------------------------------------------------
# Main entrypoint called by app.py
# ------------------------------------------------------------------

def run(controller: SentimentController) -> None:
    """Render the full Streamlit page."""

    configure_page()
    render_header()

    news = render_input()

    if render_analyze_button():
        if not news.strip():
            render_empty_warning()
        else:
            try:
                result = controller.analyze(news)
            except Exception as exc:
                st.error(f"Error loading model or analyzing sentiment: {exc}")
            else:
                render_result(result)
