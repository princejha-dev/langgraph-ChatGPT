import re
from langchain_core.messages import HumanMessage, RemoveMessage
from langchain_core.messages import AIMessage, SystemMessage
from langchain_groq import ChatGroq

from app.backend.state import ChatState
from app.backend.tools import tools
from config.settings import GROQ_MODEL, GROQ_API_KEY

# Initialize LLM
llm = ChatGroq(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY
)
llm_with_tools = llm.bind_tools(tools)

def _strip_think(text: str) -> str:
    """Strip <think>...</think> blocks emitted by thinking models."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def chat_node(state: ChatState):
    messages = []
    
    summary = state.get("summary", "")
    if summary:
        messages.append({
            "role": "system",
            "content": f"Conversation summary:\n{summary}"
        })

    messages.extend(state["messages"])

    system_prompt = SystemMessage(
    content="""
    You are a helpful, accurate, and concise AI assistant.

    CRITICAL INSTRUCTIONS:
    - Answer directly from your own knowledge when possible.
    - ONLY use tools for real-time or live data (e.g. live stock prices, breaking news, current events).
    - When you decide to call a tool, output ONLY the tool call. Do NOT write any text or partial answer before calling the tool.
    - After receiving tool results, give one clean final answer.
    - DO NOT call the same tool more than once per user query.
    - Never expose raw tool outputs or internal reasoning.
    - If uncertain about something not requiring live data, say so honestly.
    """
    )

    try:
        response = llm_with_tools.invoke([system_prompt] + messages)
        # Strip think-block content before storing in checkpointer
        if response.content:
            response.content = _strip_think(response.content)
        return {"messages": [response]}
    except Exception as e:
        print("Groq Error:", repr(e))
        return {"messages": [AIMessage(content="Sorry, something went wrong. Please try again.")]}


def summarization_node(state: ChatState):

    existing_summary = state.get('summary', '')

    # Build summarization prompt
    if existing_summary:
        prompt = (
            f"Existing summary:\n{existing_summary}\n\n"
            "Extend the summary using the new conversation above."
        )
    else:
        prompt = "Summarize the conversation above."

    messages_for_summary = state['messages'] + [HumanMessage(content=prompt)]

    response = llm.invoke(messages_for_summary)

    # Keep only last 2 messages verbatim, delete the rest
    messages_to_delete = state["messages"][:-2]

    return {
        "summary": response.content,   # store the string, not the AIMessage object
        "messages": [RemoveMessage(id=m.id) for m in messages_to_delete]
    }

def should_summarize(state: ChatState):
    return len(state["messages"]) > 10