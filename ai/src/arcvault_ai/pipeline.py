"""Orchestrates one end-to-end triage run: classify+enrich (1 LLM call) -> route -> validate."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from .classifier import classify_and_enrich
from .routing import determine_routing
from .schemas import Source, TriageRecord


def run_triage(raw_message: str, source: str | Source) -> TriageRecord:
    source_enum = Source(source) if not isinstance(source, Source) else source

    extraction = classify_and_enrich(raw_message, source_enum.value)

    routing_queue, escalation_flag, escalation_reason = determine_routing(
        extraction.category, extraction.confidence, raw_message
    )

    return TriageRecord(
        id=str(uuid.uuid4()),
        source=source_enum,
        raw_message=raw_message,
        category=extraction.category,
        priority=extraction.priority,
        confidence=extraction.confidence,
        core_issue=extraction.core_issue,
        identifiers=extraction.identifiers,
        urgency_signal=extraction.urgency_signal,
        summary=extraction.summary,
        routing_queue=routing_queue,
        escalation_flag=escalation_flag,
        escalation_reason=escalation_reason,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
