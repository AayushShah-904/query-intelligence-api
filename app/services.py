import json
import anthropic
from app.config import settings
from app.schemas import QueryIntelligence

# Initialise the Anthropic client using the configured API key
llm = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def extract_intelligence(query: str) -> QueryIntelligence:
   
    prompt = f"""You are an expert R&D Technology Scout working for an enterprise innovation platform.

A corporate user has submitted the following research query:
"{query}"

Extract structured intelligence from this query. Return ONLY valid JSON matching this exact schema:
{{
  "intent": "<one of: discover | compare | monitor | validate>",
  "domain": "<core technology or scientific domain>",
  "entity_type": "<one of: startups | research papers | experts | patents>",
  "geography": "<geographic focus or null if global>",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "refined_query": "<clean, optimized query for academic/market API search>",
  "confidence": <float between 0.0 and 1.0>
}}

Return ONLY the JSON object. No explanation, no markdown, no code fences."""

    response = llm.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if the model includes them despite strict prompt instructions
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    return QueryIntelligence(**data)
