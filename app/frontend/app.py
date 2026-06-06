"""Streamlit frontend for LangGraph Chatbot"""
import sys
from pathlib import Path

import streamlit as st
import uuid
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Ensure the project root is on the Python path when Streamlit runs this file
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.backend.agent import chatbot, retrieve_all_threads


# ============ Utility Functions ============
def generate_thread_id():
    """Generate a new unique thread ID"""
    return str(uuid.uuid4())


def reset_chat():
    """Reset chat and create a new thread"""
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []


def add_thread(thread_id):
    """Add a thread to the chat threads list"""
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):
    """Load conversation history from a specific thread"""
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])


# ============ Session State Setup ============
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])


# ============ Page Config ============
st.set_page_config(
    page_title="Agentic Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============ Sidebar ============
with st.sidebar:
    st.title("🤖 Agentic Chatbot")
    
    if st.button("➕ New Chat", use_container_width=True):
        reset_chat()
        st.rerun()
    
    st.divider()
    st.subheader("💬 Conversations")
    
    for thread_id in st.session_state["chat_threads"][::-1]:
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(f"📌 {str(thread_id)[:8]}...", key=f"thread_{thread_id}"):
                st.session_state["thread_id"] = thread_id
                messages = load_conversation(thread_id)
                temp_messages = []
                for msg in messages:
                    role = "user" if isinstance(msg, HumanMessage) else "assistant"
                    temp_messages.append({"role": role, "content": msg.content})
                st.session_state["message_history"] = temp_messages
                st.rerun()


# ============ Main Chat Area ============
st.header("🤖 Agentic Chatbot")
st.markdown("Ask me anything! I am an Agentic chatbot.")

# Display conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare config for streaming
    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

    # Stream assistant response
    with st.chat_message("assistant"):
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                # Handle tool messages
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` ...", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` ...",
                            state="running",
                            expanded=True,
                        )

                # Stream assistant tokens
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize tool status
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
