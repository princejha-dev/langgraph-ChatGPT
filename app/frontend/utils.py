import streamlit as st
import uuid
from app.backend.agent import chatbot, retrieve_all_threads

def generate_thread_id():
    """Generate a new unique thread ID"""
    return str(uuid.uuid4())

def add_thread(thread_id):
    """Add a thread to the chat threads list"""
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def reset_chat():
    """Reset chat and create a new thread"""
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []

def load_conversation(thread_id):
    """Load conversation history from a specific thread"""
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = generate_thread_id()

    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = retrieve_all_threads()

    add_thread(st.session_state["thread_id"])
