from langgraph.graph import StateGraph, END, START
from typing import Literal
import os

# Import the mocked tools
from agent_tools.cooking_ware import coocking_ware_tool
from agent_tools.google_search import GoogleSearchTool
from agent_tools.llm import LLM
from agent_states import AgentState
from prompts import (
    cooking_related_prompt,
    sufficient_info_prompt,
    generate_response_prompt,
)


class ChefRecipesAgent:
    """Agent that handles cooking-related queries using a graph of tools and LLMs."""

    def __init__(self, serpapi_key: str | None = None):
        """
        Initialize the agent with its tools and LLMs.

        Args:
            serpapi_key: Optional API key for SERP API. If not provided, uses environment variable.
        """
        self.setup_tools(serpapi_key)
        self.setup_llms()
        self.graph = self.create_agent_graph()

    def setup_tools(self, serpapi_key: str | None = None):
        """Initialize the tools used by the agent."""
        api_key = serpapi_key or os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise ValueError(
                "SERPAPI_API_KEY must be provided either through environment or constructor"
            )

        self.google_search_tool = GoogleSearchTool(api_key=api_key)
        self.cooking_ware_tool = coocking_ware_tool

    def setup_llms(self):
        """Initialize the LLM models used by the agent."""
        self.llm_cooking_related = LLM(
            model=os.getenv("COOKING_RELATED_MODEL"),
            temperature=0.3,
            prompt=cooking_related_prompt,
        )

        self.llm_sufficient_info = LLM(
            model=os.getenv("SUFFICIENT_INFO_MODEL"),
            temperature=0.3,
            prompt=sufficient_info_prompt,
        )

        self.llm_generate_response = LLM(
            model=os.getenv("GENERATE_RESPONSE_MODEL"),
            temperature=0.3,
            prompt=generate_response_prompt,
        )

    def decide_if_cooking_related(self, state: AgentState) -> AgentState:
        """
        Determine if the query is cooking-related using LLM.

        The LLM will analyze the query in context and determine if it's related to:
        - Cooking techniques
        - Recipe requests
        - Kitchen equipment
        - Food preparation
        """

        # Prepare the context with the query
        context = f"User Query: {state['query']}\n"
        # Use LLM to analyze if the query is cooking-related
        llm_response = self.llm_cooking_related.invoke(context)

        # Expect the LLM to return "yes" or "no" with reasoning
        is_cooking_related = "yes" in llm_response.lower().strip()

        return {
            **state,
            "is_cooking_related": is_cooking_related,
        }

    def get_cooking_ware(self, state: AgentState) -> AgentState:
        """Retrieve the cooking ware available to the user."""
        cooking_ware = self.cooking_ware_tool(state["query"])
        return {**state, "cooking_ware": cooking_ware}

    def search_for_information(self, state: AgentState) -> AgentState:
        """Search for information related to the query."""
        state.search_loop_count += 1
        search_results = self.google_search_tool(state["query"])
        return {**state, "search_results": search_results}

    def determine_if_enough_info(self, state: AgentState) -> AgentState:
        """Determine if we have enough information to generate a response using LLM."""
        context = []

        # Add the original query for context
        context.append(f"User Query: {state['query']}")

        # Add cooking ware information if available
        if state.get("cooking_ware"):
            ware_list = ", ".join(state["cooking_ware"])
            context.append(f"Available cooking ware: {ware_list}")
        else:
            context.append("No cooking ware information available.")

        # Add search results if available
        if state.get("search_results"):
            context.append(f"Search information: {state['search_results']}")
        else:
            context.append("No search results available.")

        # Add search loop count for context
        context.append(
            f"Number of search attempts: {state.get('search_loop_count', 0)}"
        )

        # Use LLM to determine if we have enough information
        llm_response = self.llm_sufficient_info.invoke("\n".join(context))

        # Expect the LLM to return "yes" or "no"
        has_enough_info = "yes" in llm_response.lower().strip()

        return {
            **state,
            "has_enough_info": has_enough_info,
            "sufficiency_reasoning": llm_response,
        }

    def generate_response(self, state: AgentState) -> AgentState:
        """Generate a response using the LLM."""
        context = []
        if state.get("cooking_ware"):
            ware_list = ", ".join(state["cooking_ware"])
            context.append(f"Available cooking ware: {ware_list}")
        if state.get("search_results"):
            context.append(f"Search information: {state['search_results']}")
        response = self.llm_generate_response.invoke(context)
        return {**state, "response": response}

    def generate_error_not_cooking(self, state: AgentState) -> AgentState:
        """Generate error response for non-cooking queries."""
        error_message = "I'm sorry, but I only handle cooking-related questions."
        return {**state, "error_message": error_message, "response": error_message}

    def generate_error_insufficient_info(self, state: AgentState) -> AgentState:
        """Generate error response for insufficient information."""
        error_message = "I don't have enough information to provide a good answer to your cooking question."
        return {**state, "error_message": error_message, "response": error_message}

    def route_based_on_cooking_relevance(
        self, state: AgentState
    ) -> Literal["get_cooking_ware_node", "not_cooking"]:
        """Route based on whether the query is cooking-related."""
        return "get_cooking_ware_node" if state["is_cooking_related"] else "not_cooking"

    def route_based_on_info_sufficiency(
        self, state: AgentState
    ) -> Literal["generate_response", "insufficient_info"]:
        """Route based on whether we have enough information."""
        return "generate_response" if state["has_enough_info"] else "insufficient_info"

    def create_agent_graph(self) -> StateGraph:
        """Create the agent graph based on the diagram."""
        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("decide_cooking_relevance", self.decide_if_cooking_related)
        graph.add_node("get_cooking_ware_node", self.get_cooking_ware)
        graph.add_node("search_api", self.search_for_information)
        graph.add_node("check_info_sufficiency", self.determine_if_enough_info)
        graph.add_node("generate_response", self.generate_response)
        graph.add_node("not_cooking", self.generate_error_not_cooking)
        graph.add_node("insufficient_info", self.generate_error_insufficient_info)

        # Add edges
        graph.add_edge(START, "decide_cooking_relevance")
        graph.add_conditional_edges(
            "decide_cooking_relevance",
            self.route_based_on_cooking_relevance,
            {
                "get_cooking_ware_node": "get_cooking_ware_node",
                "not_cooking": "not_cooking",
            },
        )
        graph.add_edge("get_cooking_ware_node", "search_api")
        graph.add_edge("search_api", "check_info_sufficiency")
        graph.add_conditional_edges(
            "check_info_sufficiency",
            self.route_based_on_info_sufficiency,
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

    def invoke(self, state: AgentState) -> AgentState:
        """
        Process a query through the agent graph.

        Args:
            state: Initial state containing at least the query

        Returns:
            Final state after processing through the graph
        """
        return self.graph.invoke(state)
