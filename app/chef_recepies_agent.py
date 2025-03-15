from langgraph.graph import StateGraph, END, START
from typing import Literal

# Import the mocked tools
from app.agent_tools.cooking_ware import coocking_ware_tool
from app.agent_tools.google_search import GoogleSearchTool
from app.agent_tools.llm import LLM
from app.agent_states import AgentState
from app.prompts import (
    cooking_related_prompt,
    sufficient_info_prompt,
    generate_response_prompt,
)
import os

google_search_tool = GoogleSearchTool(api_key=os.getenv("SERPAPI_API_KEY"))

llm_cooking_related = LLM(
    model=os.getenv("COOKING_RELATED_MODEL"),
    temperature=0.3,
    prompt=cooking_related_prompt,
)
llm_sufficient_info = LLM(
    model=os.getenv("SUFFICIENT_INFO_MODEL"),
    temperature=0.3,
    prompt=sufficient_info_prompt,
)

llm_generate_response = LLM(
    model=os.getenv("GENERATE_RESPONSE_MODEL"),
    temperature=0.3,
    prompt=generate_response_prompt,
)


# Node functions for the graph
def decide_if_cooking_related(state: AgentState) -> AgentState:
    """Determine if the query is cooking-related."""
    query = state["query"].lower()

    # Mock decision logic - check if query contains cooking-related keywords
    cooking_keywords = [
        "cook",
        "recipe",
        "food",
        "meal",
        "dish",
        "ingredient",
        "bake",
        "fry",
        "boil",
        "grill",
        "kitchen",
        "pot",
        "pan",
        "oven",
        "stove",
        "eat",
        "dinner",
        "lunch",
        "breakfast",
    ]

    is_cooking_related = any(keyword in query for keyword in cooking_keywords)
    return {**state, "is_cooking_related": is_cooking_related}


def get_cooking_ware(state: AgentState) -> AgentState:
    """Retrieve the cooking ware available to the user."""
    cooking_ware = coocking_ware_tool(state["query"])
    return {**state, "cooking_ware": cooking_ware}


def search_for_information(state: AgentState) -> AgentState:
    """Search for information related to the query."""
    state.search_loop_count += 1
    search_results = google_search_tool(state["query"])
    return {**state, "search_results": search_results}


def determine_if_enough_info(state: AgentState) -> AgentState:
    """Determine if we have enough information to generate a response."""
    # Mock logic - in a real implementation, this would be more sophisticated
    # For now, we'll say we have enough info if we have both cooking ware and search results
    has_enough_info = bool(state.get("cooking_ware")) and bool(
        state.get("search_results")
    )
    return {**state, "has_enough_info": has_enough_info}


def generate_response(state: AgentState) -> AgentState:
    """Generate a response using the LLM."""
    context = []

    # Add cooking ware information
    if state.get("cooking_ware"):
        ware_list = ", ".join(state["cooking_ware"])
        context.append(f"Available cooking ware: {ware_list}")

    # Add search results
    if state.get("search_results"):
        context.append(f"Search information: {state['search_results']}")

    # Generate response using the LLM
    response = llm_generate_response.invoke(context)
    return {**state, "response": response}


def generate_error_not_cooking(state: AgentState) -> AgentState:
    """Generate error response for non-cooking queries."""
    error_message = "I'm sorry, but I only handle cooking-related questions."
    return {**state, "error_message": error_message, "response": error_message}


def generate_error_insufficient_info(state: AgentState) -> AgentState:
    """Generate error response for insufficient information."""
    error_message = "I don't have enough information to provide a good answer to your cooking question."
    return {**state, "error_message": error_message, "response": error_message}


# Define routing logic
def route_based_on_cooking_relevance(
    state: AgentState,
) -> Literal["get_cooking_ware_node", "not_cooking"]:
    """Route based on whether the query is cooking-related."""
    return "get_cooking_ware_node" if state["is_cooking_related"] else "not_cooking"


def route_based_on_info_sufficiency(
    state: AgentState,
) -> Literal["generate_response", "insufficient_info"]:
    """Route based on whether we have enough information."""
    return "generate_response" if state["has_enough_info"] else "insufficient_info"


# Create the graph
def create_agent_graph() -> StateGraph:
    """Create the agent graph based on the diagram."""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("decide_cooking_relevance", decide_if_cooking_related)
    graph.add_node("get_cooking_ware_node", get_cooking_ware)
    graph.add_node("search_api", search_for_information)
    graph.add_node("check_info_sufficiency", determine_if_enough_info)
    graph.add_node("generate_response", generate_response)
    graph.add_node("not_cooking", generate_error_not_cooking)
    graph.add_node("insufficient_info", generate_error_insufficient_info)

    # Add edges
    graph.add_edge(START, "decide_cooking_relevance")
    graph.add_conditional_edges(
        "decide_cooking_relevance",
        route_based_on_cooking_relevance,
        {
            "get_cooking_ware_node": "get_cooking_ware_node",
            "not_cooking": "not_cooking",
        },
    )
    graph.add_edge("get_cooking_ware_node", "search_api")
    graph.add_edge("search_api", "check_info_sufficiency")
    graph.add_conditional_edges(
        "check_info_sufficiency",
        route_based_on_info_sufficiency,
        {
            "generate_response": "generate_response",
            "insufficient_info": "insufficient_info",
        },
    )
    graph.add_edge("insufficient_info", "search_api")
    # Add edges to end states
    graph.add_edge("generate_response", END)
    graph.add_edge("not_cooking", END)

    return graph.compile()
