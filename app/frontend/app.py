"""Streamlit frontend for LangGraph Chatbot"""
import sys
from pathlib import Path

# Ensure the project root is on the Python path when Streamlit runs this file
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app.frontend.utils import initialize_session_state
from app.frontend.ui import render_sidebar, render_chat

# ============ Page Config ============
st.set_page_config(
    page_title="Agentic Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============ Initialization ============
initialize_session_state()

# ============ Render UI ============
render_sidebar()
render_chat()
