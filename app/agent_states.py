from typing import TypedDict, List, Optional


class AgentState(TypedDict, total=False):
    """
    State type for the chef recipes agent.

    Attributes:
        query (str): The user's input query
        is_cooking_related (bool): Whether the query is related to cooking
        cooking_ware (List[str]): List of available cooking ware
        search_results (str): Results from the search API
        has_enough_info (bool): Whether we have sufficient information to answer
        response (str): The final response to the user
        error_message (Optional[str]): Any error message to be returned
        search_loop_count (int): Number of times we've searched for information
    """

    query: str
    is_cooking_related: bool
    cooking_ware: List[str]
    search_results: str
    has_enough_info: bool
    response: str
    error_message: Optional[str]
    search_loop_count: int
