from langchain_core.messages import AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.messages.utils import trim_messages, count_tokens_approximately

from app.backend.state import ChatState
from app.backend.tools import tools
from config.settings import GROQ_MODEL, GROQ_API_KEY

# Initialize LLM
llm = ChatGroq(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY
)
llm_with_tools = llm.bind_tools(tools)
MAX_TOKENS = 5000

def chat_node(state: ChatState):
    # trim the lastes msg (according to MAX_TOKENS)
    messages = trim_messages(
        messages= state['messages'],
        token_counter= count_tokens_approximately,
        strategy= "last",
        max_tokens= MAX_TOKENS
    )

    system_prompt = SystemMessage(
    content="""
    You are a helpful, accurate, and concise AI assistant.

    - Answer directly when possible.
    - Use available tools only when needed.
    - Never expose internal reasoning or tool outputs.
    - After using a tool, provide a natural final answer.
    - If uncertain, be honest instead of inventing information.
    """
    )

    try:
        response = llm_with_tools.invoke([system_prompt] + messages)
        return {"messages": [response]}
    except Exception as e:
        print("Groq Error:", repr(e))
        return {"messages": [AIMessage(content="Sorry, something went wrong. Please try again.")]}


