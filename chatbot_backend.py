from langchain_groq import ChatGroq
from langchain.messages import HumanMessage
from langgraph.graph import StateGraph, START , END 
from pydantic import BaseModel , Field
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv
import  operator
import os

load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="qwen/qwen3-32b")

#pydantic schema
class ai_response(BaseModel):
    response : str=Field(description="ai response on user input")

#structure model 
model = llm.with_structured_output(ai_response)

#state
class chatbot(TypedDict):
    user_input: str
    ai_response: str


#agent function
def chat_with_ai(state:chatbot)->chatbot:

    prompt = state['user_input']
    
    output = model.invoke(prompt)

    return {"ai_response": [output.response]}
    

#graph building
graph = StateGraph(chatbot)

graph.add_node("chat_node",chat_with_ai)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile()

# response = chatbot.invoke(
#     {"user_input":"what is 2+2"}
# )

# print(response)



