import sqlite3
import json
from datetime import datetime
from app.config import settings
from app.schemas import QueryIntelligence


def init_db():
    """Initialise the SQLite database and create the queries table if it does not exist."""
    conn = sqlite3.connect(settings.DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id          TEXT PRIMARY KEY,
            raw_query   TEXT NOT NULL,
            intent      TEXT,
            domain      TEXT,
            entity_type TEXT,
            geography   TEXT,
            keywords    TEXT,        -- JSON array stored as string
            refined_query TEXT,
            confidence  REAL,
            created_at  TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_query(query_id: str, raw_query: str, intel: QueryIntelligence) -> str:
    """Persist a new query and its extracted intelligence into the database."""
    created_at = datetime.utcnow().isoformat()
    conn = sqlite3.connect(settings.DB_PATH)
    conn.execute("""
        INSERT INTO queries
            (id, raw_query, intent, domain, entity_type, geography,
             keywords, refined_query, confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        query_id,
        raw_query,
        intel.intent,
        intel.domain,
        intel.entity_type,
        intel.geography,
        json.dumps(intel.keywords),
        intel.refined_query,
        intel.confidence,
        created_at
    ))
    conn.commit()
    conn.close()
    return created_at


def fetch_query(query_id: str) -> dict | None:
    """Retrieve a stored query by ID, returning a dictionary representation or None."""
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM queries WHERE id = ?", (query_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)
