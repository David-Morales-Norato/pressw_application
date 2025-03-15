from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chef_recepies_agent import ChefRecipesAgent
from agent_states import AgentState
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Cooking Assistant API",
    description="API for handling cooking-related queries",
    version="0.1.0",
)

# Create the agent instance
chef_agent = ChefRecipesAgent()


# Define request model
class QueryRequest(BaseModel):
    query: str


# Define response model
class QueryResponse(BaseModel):
    response: str


@app.post("/api/cooking", response_model=QueryResponse)
async def cooking_query(request: QueryRequest):
    """
    Endpoint to handle cooking-related queries using the agent graph.

    Args:
        request: QueryRequest containing the user's cooking query

    Returns:
        QueryResponse containing the agent's response

    Raises:
        HTTPException: If there's an error processing the query
    """
    try:
        # Initialize the agent state with the query and search loop count
        initial_state: AgentState = {"query": request.query, "search_loop_count": 0}

        # Run the agent with the initial state
        final_state = chef_agent.invoke(initial_state)

        # Extract the response from the final state
        response = final_state.get("response", None)
        if not response:
            # If no response was generated, check for error message
            response = final_state.get(
                "error_message", "Sorry, I couldn't process your query."
            )

        return QueryResponse(response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint that provides basic API information."""
    return {
        "message": "Welcome to the Cooking Assistant API. Use /api/cooking to query about cooking."
    }


# Run the application if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
