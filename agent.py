import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from typing import Annotated, TypedDict

# LangGraph & LangChain Core
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# LangChain SQL & Groq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq

# Your Custom Files
from custom_tools import calculate_max_revenue
from prompt import SYSTEM_MESSAGE

# Load environment variables
load_dotenv()

# ==========================================
# 1. DATABASE & TOOLS SETUP
# ==========================================
db = SQLDatabase.from_uri("sqlite:///grocery_data.db")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = toolkit.get_tools()

all_tools = sql_tools + [calculate_max_revenue]
llm_with_tools = llm.bind_tools(all_tools)

# ==========================================
# 2. DEFINE THE GRAPH STATE
# ==========================================
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ==========================================
# 3. DEFINE THE NODES
# ==========================================

def assistant(state: State):
    """Call the LLM with tools. Limit to one tool call at a time."""
    response = llm_with_tools.invoke([SYSTEM_MESSAGE] + state["messages"])
    
    # Keep only the first tool call to enforce sequential execution
    if len(response.tool_calls) > 1:
        response = AIMessage(content="", tool_calls=[response.tool_calls[0]])
    
    print(f"Model Content: {response.content}")
    print(f"Model Tool Calls: {response.tool_calls}")
    return {"messages": [response]}

# ==========================================
# 4. BUILD THE GRAPH
# ==========================================
builder = StateGraph(State)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(all_tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph_agent = builder.compile()

# ==========================================
# 5. EXECUTION
# ==========================================

def print_state_logs(result):
    """Print all messages from the State."""
    print("\n===== STATE LOGS =====")
    for i, msg in enumerate(result["messages"]):
        print(f"[{i}] {msg.__class__.__name__}: {msg.content}")
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"     Tool Calls: {msg.tool_calls}")
    print("======================\n")


def ask_agent(question: str):
    result = graph_agent.invoke({"messages": [("user", question)]})
    print_state_logs(result)
    return result["messages"][-1].content

# if __name__ == "__main__":
#     user_query = "What is the revenue for SKU-6?"
#     print(f"Question: {user_query}")
#     answer = ask_agent(user_query)
#     print(f"\nFinal Answer: {answer}")
