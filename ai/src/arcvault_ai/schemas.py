"""Pydantic schemas for the ArcVault intake/triage pipeline."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, confloat


class Category(str, Enum):
    BUG_REPORT = "Bug Report"
    FEATURE_REQUEST = "Feature Request"
    BILLING_ISSUE = "Billing Issue"
    TECHNICAL_QUESTION = "Technical Question"
    INCIDENT_OUTAGE = "Incident/Outage"


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Queue(str, Enum):
    ENGINEERING = "Engineering"
    BILLING = "Billing"
    PRODUCT = "Product"
    IT_SECURITY = "IT/Security"
    ESCALATION = "Escalation"


class Source(str, Enum):
    EMAIL = "Email"
    WEB_FORM = "Web Form"
    SUPPORT_PORTAL = "Support Portal"


class TriageExtraction(BaseModel):
    """The single structured-output payload returned by the LLM call.

    Classification (category/priority/confidence) and enrichment (core issue,
    identifiers, urgency signal, summary) are produced together in one call
    for efficiency rather than as two separate round trips.
    """

    category: Category
    priority: Priority
    confidence: confloat(ge=0, le=1) = Field(
        ..., description="Model's self-reported certainty in the category, 0-1."
    )
    core_issue: str = Field(..., description="The core issue in one sentence.")
    identifiers: List[str] = Field(
        default_factory=list,
        description="Account IDs, invoice numbers, error codes, URLs, etc. mentioned in the message.",
    )
    urgency_signal: str = Field(
        ..., description="Short phrase describing the urgency signal found in the message."
    )
    summary: str = Field(
        ..., description="2-3 sentence human-readable summary for the receiving team."
    )


class TriageRecord(BaseModel):
    """The final persisted record: LLM output + deterministic routing/escalation logic."""

    id: str
    source: Source
    raw_message: str
    category: Category
    priority: Priority
    confidence: float
    core_issue: str
    identifiers: List[str]
    urgency_signal: str
    summary: str
    routing_queue: Queue
    escalation_flag: bool
    escalation_reason: Optional[str] = None
    created_at: str
