"""Single structured-output LLM call: classification + enrichment together."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .prompts import RESPONSE_SCHEMA, SYSTEM_PROMPT, build_user_prompt
from .schemas import TriageExtraction

# Load the ai/ package's own .env regardless of which process/cwd imports this
# module (e.g. the backend running from backend/), so the OpenAI key only
# lives in one place.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


@lru_cache(maxsize=1)
def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in the environment.")
    return OpenAI(api_key=api_key)


def classify_and_enrich(raw_message: str, source: str) -> TriageExtraction:
    """Classify + enrich a raw message in exactly one LLM call.

    The response is constrained by a strict JSON schema (OpenAI structured
    outputs), then re-validated with Pydantic before being returned so that
    a malformed/implausible payload never silently reaches the caller.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(raw_message, source)},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "triage_extraction",
                "schema": RESPONSE_SCHEMA,
                "strict": True,
            },
        },
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    return TriageExtraction.model_validate(data)
