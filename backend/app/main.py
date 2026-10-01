"""ArcVault intake & triage API.

POST /api/triage: receives a raw inbound message from the frontend form,
runs it through the arcvault_ai pipeline (one LLM call for classification +
enrichment, then deterministic routing/escalation logic), persists the
validated record, and returns it to the caller.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from arcvault_ai import run_triage
from arcvault_ai.schemas import Source, TriageRecord

from .storage import list_records, save_record

logger = logging.getLogger("arcvault.backend")

app = FastAPI(title="ArcVault Intake & Triage API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TriageRequest(BaseModel):
    source: Source = Field(..., description="Where the message came from.")
    message: str = Field(..., min_length=1, max_length=5000)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/triage", response_model=TriageRecord)
def triage(request: TriageRequest) -> TriageRecord:
    try:
        record = run_triage(request.message, request.source)
    except Exception as exc:  # noqa: BLE001 - surfaced to the client as a 502
        logger.exception("Triage pipeline failed")
        raise HTTPException(status_code=502, detail=f"AI processing failed: {exc}") from exc

    save_record(record)
    return record


@app.get("/api/records", response_model=list[TriageRecord])
def records() -> list[dict]:
    return list_records()
