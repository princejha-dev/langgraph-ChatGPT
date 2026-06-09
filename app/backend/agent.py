"""Main chatbot agent using LangGraph"""
import sqlite3
import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages.utils import trim_messages, count_tokens_approximately
from .tools import tools

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"))
llm_with_tools = llm.bind_tools(tools)
MAX_TOKENS = 5000


# Define chat state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# Chat node
def chat_node(state: ChatState):

    #trim the lastes msg (according to MAX_TOKENS)
    messages = trim_messages(
        messages= state['messages'],
        token_counter= count_tokens_approximately,
        strategy= "last",
        max_tokens= MAX_TOKENS
    )

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# Initialize tool node
tool_node = ToolNode(tools)

# Database setup
db_path = os.getenv("DATABASE_PATH", "data/chatbot.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)
conn = sqlite3.connect(database=db_path, check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# Build graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

# Compile chatbot
chatbot = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    """Retrieve all conversation thread IDs from the database"""
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
