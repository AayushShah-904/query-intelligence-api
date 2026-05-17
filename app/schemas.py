"""
Data Contracts & Validation Schemas

Defines the structured input and output models for the Query Intelligence API.
These Pydantic models guarantee data integrity and generate interactive API documentation.
"""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Payload expected from the client when submitting a new research query."""
    query: str = Field(..., description="Natural language R&D or market research query")


class QueryIntelligence(BaseModel):
    """
    Structured intelligence extracted from a raw natural language query.
    
    Acts as the standardised data contract for downstream RAG pipelines, routing, 
    and database filtering.
    """
    intent: str = Field(description="Primary intent: 'discover', 'compare', 'monitor', or 'validate'")
    domain: str = Field(description="Core technology or scientific domain e.g. 'battery technology'")
    entity_type: str = Field(description="Target entity type: 'startups', 'research papers', 'experts', or 'patents'")
    geography: str | None = Field(description="Geographic focus if any, e.g. 'Southeast Asia'. Null if global.")
    keywords: list[str] = Field(description="5-7 specific technical keywords for downstream search")
    refined_query: str = Field(description="A clean, optimized version of the query for API searching")
    confidence: float = Field(description="Confidence score 0.0-1.0 on how clearly the query was understood")


class QueryResponse(BaseModel):
    """Complete API response wrapping the persisted query details and extracted intelligence."""
    id: str
    raw_query: str
    intelligence: QueryIntelligence
    created_at: str
