"""Main chatbot agent using LangGraph"""
import sqlite3
import os
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition

from app.backend.state import ChatState
from app.backend.nodes import chat_node, summarization_node, should_summarize
from app.backend.tools import tools
from config.settings import DATABASE_PATH

# Initialize tool node
tool_node = ToolNode(tools)

# Database setup
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
conn = sqlite3.connect(database=DATABASE_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# Build graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)
graph.add_node("summarization_node", summarization_node)

graph.add_edge(START, "chat_node")

# Single router: after chat_node, go to tools (if tool_calls), summarization_node (if >10 msgs), or END
def route_after_chat(state: ChatState):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    if should_summarize(state):
        return "summarization_node"
    return END

graph.add_conditional_edges(
    "chat_node",
    route_after_chat,
    {"tools": "tools", "summarization_node": "summarization_node", END: END}
)

# After tools run, go back to chat_node for the final answer
graph.add_edge("tools", "chat_node")
graph.add_edge("summarization_node", END)

# Compile chatbot
chatbot = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    """Retrieve all conversation thread IDs from the database"""
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
