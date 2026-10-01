"""Deterministic routing and escalation logic (kept out of the LLM call on purpose,
so routing is auditable, testable, and cheap to change without touching prompts)."""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from .schemas import Category, Queue

CONFIDENCE_THRESHOLD = 0.70
BILLING_DISCREPANCY_THRESHOLD = 500.0

# Keyword examples straight from the assessment ("outage", "down for all users",
# "billing error > $500"), extended with close synonyms that show up in the sample
# data (e.g. "multiple users affected") so the rule generalizes beyond the exact
# wording of the examples.
OUTAGE_KEYWORDS = [
    "outage",
    "down for all users",
    "down for everyone",
    "multiple users affected",
    "all users affected",
]

CATEGORY_QUEUE_MAP = {
    Category.BUG_REPORT: Queue.ENGINEERING,
    Category.INCIDENT_OUTAGE: Queue.ENGINEERING,
    Category.FEATURE_REQUEST: Queue.PRODUCT,
    Category.BILLING_ISSUE: Queue.BILLING,
    Category.TECHNICAL_QUESTION: Queue.IT_SECURITY,
}


def _dollar_amounts(text: str) -> List[float]:
    return [float(m.replace(",", "")) for m in re.findall(r"\$([0-9][0-9,]*(?:\.\d{1,2})?)", text)]


def determine_routing(
    category: Category, confidence: float, raw_message: str
) -> Tuple[Queue, bool, Optional[str]]:
    """Return (routing_queue, escalation_flag, escalation_reason).

    Escalation always wins over the normal category->queue mapping and sends
    the record to the Escalation queue for human review instead.
    """
    reasons: List[str] = []
    lowered = raw_message.lower()

    if confidence < CONFIDENCE_THRESHOLD:
        reasons.append(f"confidence {confidence:.2f} below {CONFIDENCE_THRESHOLD:.2f} threshold")

    if any(keyword in lowered for keyword in OUTAGE_KEYWORDS):
        reasons.append("message contains an outage-severity keyword")

    if category == Category.BILLING_ISSUE:
        amounts = _dollar_amounts(raw_message)
        if len(amounts) >= 2 and abs(amounts[0] - amounts[1]) > BILLING_DISCREPANCY_THRESHOLD:
            reasons.append(
                f"billing discrepancy of ${abs(amounts[0] - amounts[1]):.2f} exceeds "
                f"${BILLING_DISCREPANCY_THRESHOLD:.0f} threshold"
            )

    if reasons:
        return Queue.ESCALATION, True, "; ".join(reasons)

    return CATEGORY_QUEUE_MAP.get(category, Queue.ESCALATION), False, None
