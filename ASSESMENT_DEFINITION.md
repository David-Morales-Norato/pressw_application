# Technical Assessment: AI-Powered Recipe Chatbot

## Problem Statement

You have been brought on as an **AI Engineer** to develop a **FastAPI** application that answers queries about **how to make food dishes**. Your application should leverage **LangGraph** to build a pipeline of “nodes” that classify and respond to user queries.

### Key Requirements

1. **Query Classification**
    - Determine if a user’s question is about **cooking/recipes** (e.g., “How do I make bbq chicken pizza?”) or **not** cooking-related (e.g., “What’s the best time to invest in stocks?”).
2. **Non-Relevant Query Handling**
    - For questions **not** about cooking, your system should respond politely but clearly that it can only address cooking-related queries.
3. **Research & Response**
    - For cooking-related queries, the application should:
        1. **Research Tools**
            1. Use the **SERP API** (via LangGraph) to search the web for recipes.
            2. A tool that provides the system a list of cookware the user has available
        2. **Response Decision Node**: Decide if the information gathered is sufficient or if additional research is needed. If sufficient, return a final detailed answer.
4. **End-to-End Flow**
    - Provide one or more **FastAPI endpoints** (e.g., `POST /api/cooking`) that accepts a user’s query and returns the system’s answer (JSON response).
    - If the query is **non-cooking**, immediately respond with a polite “I’m sorry, but I only handle cooking-related questions.”
    - If the query is **cooking-related**, perform the above research and respond with a recipe to make the dish the user is interested in.

You will have **2 hours** to complete this assessment. We understand that you may not finish **all** features under time constraints, but we want to see how you design, structure, and prioritize your solution.

---

## Assignment Requirements

### 1. Graph/Chain Construction

- **LangGraph**
    - Implement a pipeline (or chain) of nodes:
        1. **Query Classification Node**
            - Classifies the user’s query as cooking or non-cooking.
            - If non-cooking, it routes the flow to a “non-relevant” response node.
        2. **Non-Relevant Node**
            - Generates a polite refusal message (e.g., “I can only help with cooking queries.”).
        3. **Research Node**
            - Bind the available tools to the LLM within this research node
            - Uses the **SERP API** (provided by LangChain) to conduct online searches about cooking techniques.
            - Create an `available_cookware` tool that provides an array list of available for the user cookware. The current cookware can be hardcoded as:
                
                ```python
                [
                  "Spatula",
                  "Frying Pan", 
                  "Little Pot", 
                  "Stovetop", 
                  "Whisk",
                  "Knife",
                  "Ladle",
                  "Spoon"
                ]
                ```
                
            - Incorporates relevant details (e.g., step-by-step guidance, references).
        4. **Response Decision Node**
            - Determines if further research is needed.
            - Either loops back to the **Research Node** or constructs a final answer.

### 2. FastAPI Setup & Code Quality

1. **FastAPI Application**
    - Implement a minimal, clean FastAPI service with at least one endpoint (e.g., `POST /api/cooking`).
    - Return JSON responses containing your final answer or refusal message.
2. **PEP 8 & Formatting**
    - Your code should follow **PEP 8** guidelines. Using **Black** or another autoformatter is encouraged.
3. **Logging/Debugging**
    - Include basic logging or debug print statements to help trace the flow.

### 3. Docker & Environment Setup

1. **Dockerfile**
    - Provide a `Dockerfile` to containerize your FastAPI application.
    - You can use the [standard PressW FastAPI Dockerfile](https://gist.github.com/elmdecoste/fb1d94daf800d8680b0cce69dd9df2cd) as a bootstrap
2. **Docker Compose**
    - Supply a `docker-compose.yml` if any additional services are required (e.g., environment for SERP keys).
    - The Docker Compose setup should make it straightforward to start your application.
3. **Environment Variables**
    - Document any required variables (e.g., SERP API key) in your README.
    - Show how to configure them (e.g., `.env` file, Docker Compose `env_file`).

### 4. Authentication & Deployment (Documentation Only)

- **Authentication**: You do **not** need to implement a full authentication flow, but in your README, explain how you **would** secure your application (e.g., API keys, OAuth, or JWT).
- **Deployment**: Explain how you would deploy and scale this FastAPI service in a production environment (e.g., Docker orchestration, load balancing, environment config).

---

## Project Structure & Deliverables

1. **Repository Layout**
    - You may keep your code in a single repository (e.g., a `backend/` directory with the following files):
        
        ```
        bash
        Copy
        backend/
          ├── main.py             # Entry point for FastAPI
          ├── graphs/ # Or whichever structure you prefer for your nodes
          ├── pyproject.toml
          ├── Dockerfile
          ├── ...
        docker-compose.yml
        README.md
        
        ```
        
2. **Root README**
    - Provide a top-level README with clear instructions on:
        - How to install dependencies (e.g., `poetry install`).
        - How to run the application (e.g., `uvicorn main:app --reload`).
        - How to run via Docker (`docker build ...`, `docker-compose up ...`).
        - Any environment variable usage (SERP API keys, etc.).
    - Briefly summarize your approach to building the **classification**, **research**, and **response** nodes.
    - Outline any **future improvements** you would make if you had more time.
3. **Timeboxing**
    - You have **2 hours** total. We value seeing how you prioritize essential functionality under time constraints.
    - Include a short note about **trade-offs** or **incomplete features** (if any) and how you would address them with more time.

---

## Evaluation Criteria

1. **Functionality**
    - Does your backend correctly differentiate cooking vs. non-cooking queries?
    - For cooking-related queries, does it integrate with a SERP API to gather relevant techniques?
    - Does it construct a coherent final response (or refusal message)?
2. **Code Quality & Organization**
    - Is your Python code clean, modular, and PEP 8 compliant?
    - Are nodes/pipeline steps reasonably organized within the codebase?
3. **Documentation & Setup**
    - Does the README clearly explain how to run the application?
    - Are environment variables and external dependencies described?
    - Is the Docker setup functional and straightforward?
4. **Time Management & Problem-Solving**
    - We understand 2 hours is not a lot of time. We’ll look at how you approached the core problem and how you documented any next steps or improvements.

---

## Getting Started

1. **Clone/Initialize a Repo**
    - Create a new repository or use the provided starter repo.
    - Begin by setting up FastAPI, installing LangGraph.
2. **Implement the Pipeline**
    - Start by creating your classification, refusal, research, and decision nodes.
    - Test the flow locally to ensure you can differentiate and handle queries correctly.
3. **Containerize**
    - Add your `Dockerfile`.
    - If needed, create a `docker-compose.yml` for easy local orchestration.
4. **Finalize & Deliver**
    - Include instructions in your README.
    - Note any outstanding issues or improvements to address.

---

**Good luck** with creating your **AI-Powered Recipe Chatbot** backend! We look forward to reviewing your approach, code quality, and decision-making under the 2-hour time constraint.