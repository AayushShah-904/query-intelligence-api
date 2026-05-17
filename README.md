# Query Intelligence Endpoint

## What I built

- **`POST /queries`** — accepts a natural language research query, uses **Claude (claude-sonnet-4)** to extract 7 structured intelligence fields (intent, domain, entity type, geography, keywords, refined query, confidence score), persists to SQLite, and returns the enriched result with a generated UUID.
- **`GET /queries/{id}`** — retrieves any stored query and its extracted intelligence by ID.

## Schema design decisions

Rather than extracting only keywords, I designed a `QueryIntelligence` schema with 7 fields that reflect how a real enterprise research platform would need to consume the data:

| Field | Purpose |
|---|---|
| `intent` | Routes the query to the right downstream pipeline (discover vs compare vs monitor) |
| `domain` | Core technology area for category filtering |
| `entity_type` | Determines which data source to hit — papers, startups, experts, or patents |
| `geography` | Enables regional filtering on startup/market databases |
| `keywords` | 5–7 specific terms for vector search and API queries |
| `refined_query` | Cleaned version optimised for arXiv / web search APIs |
| `confidence` | Flags ambiguous queries for human review before downstream processing |

This pattern is directly inspired by the query parser I built in **Innovation Scout** ([github.com/AayushShah-904/innovation-scout](https://github.com/AayushShah-904/innovation-scout)) — a full agentic RAG pipeline that uses this structured extraction as its first node before parallel search across arXiv, pgvector, and live web.

## Project Structure

The project follows a clean, modular, production-grade FastAPI architecture:

```text
take-home-assessment/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app initialisation & router aggregation
│   ├── config.py        # Environment variables & configuration settings
│   ├── schemas.py       # Pydantic validation & serialisation models
│   ├── database.py      # SQLite connection & persistence helpers
│   ├── services.py      # Anthropic Claude LLM extraction business logic
│   └── routers/
│       ├── __init__.py
│       └── queries.py   # API endpoints (POST /queries, GET /queries/{id})
├── main.py              # Top-level dev runner entry point (`python main.py`)
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Setup & running

```bash
# 1. Install dependencies
pip install fastapi uvicorn anthropic python-dotenv pydantic

# 2. Set your API key
echo "ANTHROPIC_API_KEY=sk-..." > .env

# 3. Run the server
python main.py

# Server starts at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

## Example usage

```bash
# POST a query
curl -X POST http://localhost:8000/queries \
  -H "Content-Type: application/json" \
  -d '{"query": "find battery technology startups in Southeast Asia"}'

# Response
{
  "id": "3f7a1c2d-...",
  "raw_query": "find battery technology startups in Southeast Asia",
  "intelligence": {
    "intent": "discover",
    "domain": "battery technology",
    "entity_type": "startups",
    "geography": "Southeast Asia",
    "keywords": ["solid-state battery", "lithium-ion", "energy storage", "EV", "Series A"],
    "refined_query": "battery technology energy storage startups Southeast Asia",
    "confidence": 0.95
  },
  "created_at": "2026-05-18T14:30:00"
}

# GET by ID
curl http://localhost:8000/queries/3f7a1c2d-...
```

## With more time

- **Replace SQLite with pgvector** — store embeddings of each `refined_query` to enable semantic deduplication and similarity search across past queries (already implemented in Innovation Scout's `vector_store.py`)
- **Add a `POST /queries/{id}/search` endpoint** — trigger the full agentic pipeline (arXiv + web + vector search + LLM ranking) directly from a stored query
- **Streaming responses** — stream LLM extraction progress back to the client using FastAPI's `StreamingResponse`
