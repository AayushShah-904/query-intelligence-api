"""
Query Intelligence API Endpoints

Defines the HTTP REST endpoints for submitting research queries and retrieving 
previously extracted intelligence.
"""

import uuid
import json
from fastapi import APIRouter, HTTPException
from app.schemas import QueryRequest, QueryIntelligence, QueryResponse
from app.services import extract_intelligence
from app.database import save_query, fetch_query

router = APIRouter(tags=["Queries"])


@router.post("/queries", response_model=QueryResponse, status_code=201)
def create_query(request: QueryRequest):
    """
    Submit a new natural language research query.
    
    Orchestrates the workflow: validates input, calls Claude to extract structured 
    intelligence, persists the record to SQLite, and returns the complete entity.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        intel = extract_intelligence(request.query)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"LLM returned malformed JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Intelligence extraction failed: {e}")

    query_id = str(uuid.uuid4())
    created_at = save_query(query_id, request.query, intel)

    return QueryResponse(
        id=query_id,
        raw_query=request.query,
        intelligence=intel,
        created_at=created_at
    )


@router.get("/queries/{query_id}", response_model=QueryResponse)
def get_query(query_id: str):
    """Retrieve a previously stored research query and its extracted intelligence by ID."""
    row = fetch_query(query_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Query '{query_id}' not found.")

    intel = QueryIntelligence(
        intent=row["intent"],
        domain=row["domain"],
        entity_type=row["entity_type"],
        geography=row["geography"],
        keywords=json.loads(row["keywords"]),
        refined_query=row["refined_query"],
        confidence=row["confidence"]
    )

    return QueryResponse(
        id=row["id"],
        raw_query=row["raw_query"],
        intelligence=intel,
        created_at=row["created_at"]
    )
