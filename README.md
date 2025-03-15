# Cooking Assistant API

A FastAPI-based cooking assistant that uses LLMs and tools to answer cooking-related queries.

## Setup

1. Create a virtual environment and install dependencies:
```bash
make install
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your SERPAPI API key
   - Configure LLM models if needed

## Running the API

1. Make sure your virtual environment is activated
2. Run the API server:
```bash
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8080
```

## Running with Docker

1. Build the Docker image:
```bash
env $(cat .env | xargs) docker compose  --env-file .env up
```

## API Endpoints

### POST /api/cooking
Submit a cooking-related query:
```bash
curl -X POST "http://localhost:8080/api/cooking" \
     -H "Content-Type: application/json" \
     -d '{"query": "How do I make pasta?"}'
```

### GET /
Get API information:
```bash
curl "http://localhost:8080/"
```

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8080/docs

