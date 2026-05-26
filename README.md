<<<<<<< HEAD
# 📈 AI Trading Sentiment Analyzer

Analyzes financial market news with a fine-tuned HuggingFace classifier and returns a **BUY / SELL / HOLD** signal with confidence score.

---

## Project Structure (MVC)

```
trading_sentiment/
│
├── app.py                          # Entrypoint — wires Controller → View
│
├── models/
│   ├── __init__.py
│   └── sentiment_model.py          # ML model loading & raw inference
│
├── controllers/
│   ├── __init__.py
│   └── sentiment_controller.py     # Business logic — signals & analysis
│
├── views/
│   ├── __init__.py
│   └── sentiment_view.py           # All Streamlit UI code
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # App-wide config & env vars
│
├── saved_model/                    # HuggingFace model weights (not in git)
├── requirements.txt
├── .gitignore
└── README.md
```

### Layer responsibilities

| Layer | File | Does |
|---|---|---|
| **Model** | `models/sentiment_model.py` | Loads pipeline, returns raw `{label, score}` |
| **Controller** | `controllers/sentiment_controller.py` | Maps label → signal/analysis, checks confidence |
| **View** | `views/sentiment_view.py` | All `st.*` calls — zero logic |
| **Config** | `config/settings.py` | `MODEL_PATH`, `CONFIDENCE_THRESHOLD` via env vars |
| **App** | `app.py` | One-liner bootstrap only |

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/<you>/trading-sentiment.git
cd trading-sentiment

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place your model weights
#    Copy your fine-tuned model into ./saved_model/

# 5. Run
streamlit run app.py
```

---

## Configuration

| Env Variable | Default | Description |
|---|---|---|
| `MODEL_PATH` | `./saved_model` | Path to HuggingFace model directory |
| `CONFIDENCE_THRESHOLD` | `70` | Below this % a warning is shown |

Set them in a `.env` file or export before running:

```bash
export MODEL_PATH=/path/to/model
export CONFIDENCE_THRESHOLD=75
streamlit run app.py
```

---

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub (without `saved_model/` — use Git LFS or host externally).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Set **Main file path** to `app.py`.
4. Add secrets/env vars in the Streamlit Cloud dashboard under **Advanced settings**.

> **Note:** For large model files, upload to Hugging Face Hub and load via `pipeline("text-classification", model="your-hf-repo")`.

---

## Model Notes

The app expects a HuggingFace `text-classification` model whose labels contain the strings **bullish**, **bearish**, or neither (mapped to HOLD).
=======
# AI_Trading_News_Sentiment_Analysis
🚀 AI Resume Analyzer is an AI-powered web application that analyzes resumes for ATS compatibility, identifies missing skills and keywords, provides improvement suggestions, and generates optimized resumes for specific companies. Built using Python, Streamlit, OpenRouter API, NLP concepts, and PDF/DOCX processing.
>>>>>>> 9870341976d04bd9df9d3e488a3574a74670bf05
