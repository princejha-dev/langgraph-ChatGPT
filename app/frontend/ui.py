import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.backend.agent import chatbot
from app.frontend.utils import reset_chat, load_conversation

def render_sidebar():
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
                if st.button(f"📌 {str(thread_id)[:20]}", key=f"thread_{thread_id}"):
                    st.session_state["thread_id"] = thread_id
                    messages = load_conversation(thread_id)
                    temp_messages = []
                    for msg in messages:
                        if isinstance(msg, HumanMessage):
                            role = "user"
                        elif isinstance(msg, AIMessage):
                            if not msg.content:
                                continue
                            role = "assistant"
                        else:
                            continue
                        temp_messages.append({"role": role, "content": msg.content})
                    st.session_state["message_history"] = temp_messages
                    st.rerun()

def render_chat():
    st.header("🤖 Agentic Chatbot")
    st.markdown("I am here to help you, Ask me anything!")

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
                try:
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
                            if message_chunk.content:
                                yield message_chunk.content

                except Exception as e:
                    st.error(f"Error: {str(e)}")

            ai_message = st.write_stream(ai_only_stream())

            # Finalize tool status
            if status_holder["box"] is not None:
                status_holder["box"].update(
                    label="✅ Tool finished", state="complete", expanded=False
                )

        # Save assistant message to local session state
        # (It is already saved in sqlite checkpointer by LangGraph)
        if ai_message:
            st.session_state["message_history"].append(
                {"role": "assistant", "content": ai_message}
            )
