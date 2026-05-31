"""
View Layer
Responsible for: All Streamlit rendering — inputs, outputs, layout.
Zero business logic or model calls belong here.
"""

import streamlit as st
from controllers.sentiment_controller import SentimentController


def configure_page() -> None:
    st.set_page_config(
        page_title="AI Trading Sentiment Analyzer",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    
    # Premium Modern Dark Theme with Trading Dashboard Style
    st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #e0e0e0;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding: 2rem 1rem;
    }
    
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2.5rem;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.95;
        margin-top: 0.8rem;
        letter-spacing: 0.5px;
    }
    
    .input-section {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .input-section > div > div {
        color: #e0e0e0;
    }
    
    textarea {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 10px !important;
        color: #e0e0e0 !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    textarea:focus {
        background-color: rgba(255, 255, 255, 0.12) !important;
        border-color: #667eea !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.2) !important;
    }
    
    .result-container {
        margin-top: 2rem;
        padding: 2rem;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .metric-box {
        background: rgba(102, 126, 234, 0.1);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-box:hover {
        background: rgba(102, 126, 234, 0.15);
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .metric-box h3 {
        color: #667eea;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-box p {
        color: #e0e0e0;
        margin: 0.5rem 0;
    }
    
    .positive-signal {
        background: linear-gradient(135deg, #00d084 0%, #00a86b 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(0, 208, 132, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .positive-signal:hover {
        box-shadow: 0 12px 35px rgba(0, 208, 132, 0.4);
    }
    
    .negative-signal {
        background: linear-gradient(135deg, #ff3838 0%, #d63031 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(255, 56, 56, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .negative-signal:hover {
        box-shadow: 0 12px 35px rgba(255, 56, 56, 0.4);
    }
    
    .neutral-signal {
        background: linear-gradient(135deg, #ffa502 0%, #ff8500 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(255, 165, 2, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .neutral-signal:hover {
        box-shadow: 0 12px 35px rgba(255, 165, 2, 0.4);
    }
    
    .signal-box {
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        letter-spacing: 0.5px;
    }
    
    .progress-bar {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 1.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    [role="progressbar"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        height: 8px !important;
        border-radius: 10px !important;
    }
    
    .analysis-box {
        background: rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        line-height: 1.8;
        margin: 1.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Buttons */
    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    [data-testid="stButton"] > button:active {
        transform: translateY(0) !important;
    }
    
    /* Alerts */
    .stWarning, .stSuccess, .stError {
        border-radius: 12px !important;
        border-left: 4px solid !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning {
        background: rgba(255, 165, 2, 0.1) !important;
        border-left-color: #ffa502 !important;
    }
    
    .stSuccess {
        background: rgba(0, 208, 132, 0.1) !important;
        border-left-color: #00d084 !important;
    }
    
    .stError {
        background: rgba(255, 56, 56, 0.1) !important;
        border-left-color: #ff3838 !important;
    }
    
    /* Subheaders */
    [data-testid="stMarkdownContainer"] h2 {
        color: #e0e0e0 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        letter-spacing: 0.3px !important;
    }
    
    [data-testid="stMarkdownContainer"] h3 {
        color: #b0b0b0 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """, unsafe_allow_html=True)


def render_header() -> None:
    st.markdown("""
    <div class="main-header">
        <h1>📈 AI Trading Sentiment Analyzer</h1>
        <p>Powered by Groq's Llama 3.3 70B • Real-time Financial Sentiment Analysis</p>
    </div>
    """, unsafe_allow_html=True)


def render_input() -> str:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.subheader("📰 Enter Financial News")
    news = st.text_area(
        "Analyze any financial news or market update:",
        placeholder="e.g., 'Apple reports record quarterly earnings exceeding analyst expectations...'",
        height=130,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return news


def render_analyze_button() -> bool:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        return st.button("🚀 Analyze Sentiment", use_container_width=True, key="analyze_btn")


def render_result(result: dict) -> None:
    """Render premium trading dashboard results."""
    
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    
    # --- Key Metrics Row ---
    col1, col2, col3 = st.columns(3, gap="large")
    
    sentiment_emoji = "📈" if "POSITIVE" in result["label"] else "📉" if "NEGATIVE" in result["label"] else "➡️"
    sentiment_color = "#00d084" if "POSITIVE" in result["label"] else "#ff3838" if "NEGATIVE" in result["label"] else "#ffa502"
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3>💡 Sentiment</h3>
            <p style="font-size: 2.2rem; margin: 0.8rem 0; color: {sentiment_color};">{sentiment_emoji}</p>
            <p style="font-size: 1.3rem; margin: 0.5rem 0;">{result['label']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        confidence = result['confidence']
        conf_color = "#00d084" if confidence >= 75 else "#ffa502" if confidence >= 50 else "#ff3838"
        st.markdown(f"""
        <div class="metric-box">
            <h3>🎯 Confidence</h3>
            <p style="font-size: 2.2rem; margin: 0.8rem 0; color: {conf_color};">{confidence}%</p>
            <p style="font-size: 0.9rem; color: #b0b0b0;">Prediction accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        strength = "🔥 STRONG" if confidence >= 75 else "⚡ FAIR" if confidence >= 50 else "❄️ WEAK"
        strength_color = "#00d084" if confidence >= 75 else "#ffa502" if confidence >= 50 else "#ff3838"
        st.markdown(f"""
        <div class="metric-box">
            <h3>💪 Signal Strength</h3>
            <p style="font-size: 1.2rem; margin: 0.8rem 0; color: {strength_color};">{strength}</p>
            <p style="font-size: 0.9rem; color: #b0b0b0;">Decision confidence</p>
        </div>
        """, unsafe_allow_html=True)
    
    # --- Confidence Progress Bar ---
    st.markdown(f"""
    <div style="margin: 2rem 0; color: #b0b0b0;">
        <small>📊 Confidence Level</small>
    </div>
    """, unsafe_allow_html=True)
    st.progress(result['confidence'] / 100)
    
    # --- Market Analysis ---
    st.markdown("### 📊 Market Analysis")
    st.markdown(f"""
    <div class="analysis-box">
        {result['analysis']}
    </div>
    """, unsafe_allow_html=True)
    
    # --- Trading Signal ---
    st.markdown("### 💼 Trading Signal")
    
    signal = result["signal"]
    signal_type = "positive" if "BUY" in signal else "negative" if "SELL" in signal else "neutral"
    signal_class = f"{signal_type}-signal"
    
    st.markdown(f"""
    <div class="signal-box {signal_class}">
        {signal}
    </div>
    """, unsafe_allow_html=True)
    
    # --- Warnings & Recommendations ---
    if result["low_confidence"]:
        st.warning(
            "⚠️ **Caution: Low Confidence** — This prediction has moderate uncertainty. "
            "Recommend using additional sources and technical analysis before trading.",
            icon="⚠️"
        )
    else:
        st.success(
            "✅ **High Confidence** — Signal strength is adequate for decision-making support. "
            "Always validate with additional research.",
            icon="✅"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_empty_warning() -> None:
    st.warning(
        "📝 Please enter financial news or market data to analyze",
        icon="📝"
    )


def render_error(error: str) -> None:
    st.error(f"❌ Error: {error}", icon="❌")


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
            with st.spinner("🔍 Analyzing sentiment with Groq AI..."):
                try:
                    result = controller.analyze(news)
                except Exception as exc:
                    render_error(str(exc))
                else:
                    render_result(result)
