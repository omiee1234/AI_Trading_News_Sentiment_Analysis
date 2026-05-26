"""
app.py — Entrypoint
-------------------
Bootstraps the app: wires the Controller to the View and starts Streamlit.
No business logic or UI code belongs here.

Run with:
    streamlit run app.py
"""

from controllers.sentiment_controller import SentimentController
from views.sentiment_view import run

if __name__ == "__main__":
    controller = SentimentController()
    run(controller)
