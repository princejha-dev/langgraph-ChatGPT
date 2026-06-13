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
    - ONLY use tools if the user asks for real-time information (e.g. current stock prices, recent news) or specifically requests a search.
    - DO NOT use tools recurrently or multiple times for the same query unless explicitly needed.
    - Once you receive the tool's output, provide the final answer immediately without calling more tools.
    - Never expose internal reasoning or tool outputs directly.
    - If uncertain, be honest instead of inventing information.
    """
    )

    try:
        response = llm_with_tools.invoke([system_prompt] + messages)
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