import os
import json
from typing import Annotated, Literal, TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import sys
import os

# Add parent directory to sys.path to allow imports from 'backend' package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the existing RAG function
from backend.rag import search_rag

load_dotenv()

# --- 1. Define Tools ---

@tool
def web_search(query: str):
    """
    Search the internet for real-time or public information using DuckDuckGo.
    Use this for:
    - Current events
    - General knowledge not likely to be in internal documents
    - Fact checking
    """
    search = DuckDuckGoSearchRun()
    return search.invoke(query)

@tool
def rag_search(query: str):
    """
    Search internal documents (knowledge base) for specific information.
    Use this for:
    - Internal policies, reports, or specific document content
    - Information that was likely uploaded by the user
    """
    try:
        results = search_rag(query, limit=10) # Comparison with more candidates
        if not results:
            return "No relevant internal documents found."
        
        # Deduplication Logic
        seen_content = set()
        unique_results = []
        
        for item in results:
            text = item.get('text', '').strip()
            # simple deduplication by exact text match (hash)
            # could be improved with fuzzy matching if needed
            if text in seen_content:
                continue
                
            seen_content.add(text)
            unique_results.append(item)
            
            if len(unique_results) >= 5: # Keep top 5 unique
                break
        
        # Format results for the LLM
        formatted = ""
        for item in unique_results:
            text = item.get('text', '')
            source = item.get('source', 'unknown')
            # Normalize source path for cleaner output (basename only)
            source_name = os.path.basename(source)
            page = item.get('page', 'N/A')
            formatted += f"Source: {source_name} (Page {page})\nContent: {text}\n---\n"
        return formatted
    except Exception as e:
        return f"Error querying RAG: {str(e)}"

# List of tools available to the agent
tools = [web_search, rag_search]

# --- 2. Define State ---

from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# --- 3. Structured Output for Analysis ---

class QueryAnalysis(BaseModel):
    """Structure to validate user query clarity."""
    is_clear: bool = Field(description="Set to True if the query is clear enough to attempt a search/answer. Set to False if it is too vague (e.g., 'It', 'How much?', 'Where?').")
    clarification: str = Field(description="If is_clear is False, provide a polite Vietnamese question asking for clarification. If True, leave empty.")

# --- 4. Define Nodes ---

# Main Agent LLM (Heavy)
llm = ChatOpenAI(model="gpt-4.1", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Analyzer LLM (Fast/Cheaper - logic could use gpt-4o-mini or same model)
# We use .with_structured_output to force JSON
analyzer_llm = llm.with_structured_output(QueryAnalysis)

def analyze_node(state: AgentState):
    """
    Gatekeeper node. Checks if the LAST message from user is clear.
    """
    messages = state["messages"]
    
    
    try:
        analysis = analyzer_llm.invoke(messages)
    except Exception:
        # Fallback if structured output fails (rare)
        return {} 
    
    
    if not analysis.is_clear:
        # If vague, we inject the clarification request directly as the AI response
        return {"messages": [AIMessage(content=analysis.clarification)]}
    
    # If clear, we don't modify state, just pass through.
    return {}

def router_logic(state: AgentState):
    """
    Decides where to go after analyze_node.
    """
    messages = state["messages"]
    last_msg = messages[-1]
    
    # If the analysis node added an AI message (clarification), it means we stop.
    if isinstance(last_msg, AIMessage) and not last_msg.tool_calls:
        # The analyzer formulated a clarification response.
        return "end"
        
    return "continue"

def agent_node(state: AgentState):
    """
    The agent node responsible for making decisions (planning).
    It looks at the conversation history and decides whether to call a tool or end.
    """
    # System prompt to enforce behavior
    system_prompt = SystemMessage(content="""You are an advanced Agentic RAG assistant.
    Your goal is to answer user queries comprehensively by leveraging your tools.
    
    CORE RULES:
    1. **Language**: Always answer in Vietnamese unless requested otherwise.
    2. **Query Refinement**: 
       - BEFORE calling `rag_search`: Extract key entities and concepts. Formulate a search query that maximizes semantic retrieval (e.g., convert "nó hoạt động thế nào" to "cơ chế hoạt động của hệ thống X").
       - BEFORE calling `web_search`: Create specific, keyword-heavy search queries (e.g., "giá vàng SJC hôm nay" instead of "giá vàng thế nào").
    3. **Tool Selection Strategy**:
       - `rag_search`: PRIORITY 1 for internal docs.
       - `web_search`: PRIORITY 2 for external info/facts.
       - If comparing, use both.
    4. **Self-Correction**: If a tool returns "No results", try synonyms.

    RESPONSE STRUCTURE:
    - **Thought**: Explain plan.
    - **Action**: Execute tools.
    - **Synthesis**: Answer.
    """)
    
    messages = [system_prompt] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# --- 5. Build Graph ---

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze", analyze_node)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))


# Start -> Analyze (The Gatekeeper)
workflow.add_edge(START, "analyze")

# Conditional Edge from Analyze
workflow.add_conditional_edges(
    "analyze",
    router_logic,
    {
        "end": END,       # If vague, we already replied with clarification, so END.
        "continue": "agent" # If clear, go to main Agent.
    }
)

# Conditional Edge from Agent (Tool use or End)
workflow.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",  # If tool_calls exist, go to 'tools' node
        "__end__": END     # If no tool_calls, end the workflow
    }
)

# Automatic edge from tools back to agent
workflow.add_edge("tools", "agent")

# Compile the graph with memory
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

class LangGraphAgent:
    def __init__(self):
        self.app = graph

    def run(self, query: str, thread_id: str = "default"):
        """
        Run the agent with the given query and thread_id for memory.
        """
        # Config to identify the conversation thread
        config = {"configurable": {"thread_id": thread_id}}
        
        inputs = {"messages": [HumanMessage(content=query)]}
        
        # We invoke the graph with config.
        # The result will contain the full history of messages including tool calls.
        result = self.app.invoke(inputs, config=config)
        
        messages = result["messages"]
        final_answer = messages[-1].content
        
        # Extract execution details for the UI
        # We look for ToolMessages and the preceding AIMessage to show "planning" and "output"
        execution_details = []
        plan_steps = []
        
        for i, msg in enumerate(messages):
            if msg.type == "ai" and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    plan_steps.append({
                        "tool": tool_call["name"],
                        "query": str(tool_call["args"]),
                        "reasoning": "Agent decided to call this tool."
                    })
            
            if msg.type == "tool":
                execution_details.append({
                    "step": {"tool": msg.name},
                    "output": msg.content
                })

        return {
            "plan": plan_steps,
            "execution_details": execution_details,
            "answer": final_answer
        }
