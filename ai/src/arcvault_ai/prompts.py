"""Prompt templates and the JSON schema used for the single structured-output LLM call."""

SYSTEM_PROMPT = """You are a triage assistant for ArcVault, a B2B software company.

You classify and enrich a single inbound customer request in one pass. Follow these rules:

- category: choose exactly one of "Bug Report", "Feature Request", "Billing Issue",
  "Technical Question", "Incident/Outage".
- priority: "Low", "Medium", or "High", based on business impact and urgency expressed
  in the message (e.g. outages affecting multiple users or billing discrepancies are
  typically High; general questions are typically Low).
- confidence: your honest self-assessed certainty in the category assignment, from 0.0
  to 1.0. Use lower values when the message is ambiguous or could fit more than one
  category. Do not default to a high value out of habit.
- core_issue: exactly one sentence stating what the customer actually needs.
- identifiers: a list of any account IDs, invoice numbers, URLs, error codes, dollar
  amounts, dates, or product/vendor names mentioned (e.g. "403", "arcvault.io/user/jsmith",
  "Invoice #8821", "$1,240", "Okta"). Return an empty list if none are present.
- urgency_signal: a short phrase naming the specific textual cue that signals urgency
  (or its absence), e.g. "multiple users affected", "no urgency language used".
- summary: 2-3 sentences, written for the team that will receive this ticket, covering
  what happened and what the customer wants.

Base every field strictly on the content of the message. Do not invent identifiers or
details that are not present in the text."""


def build_user_prompt(raw_message: str, source: str) -> str:
    return f"""Source: {source}
Message:
\"\"\"{raw_message}\"\"\"

Classify and enrich this message according to the system instructions."""


# JSON Schema for OpenAI structured outputs (response_format: json_schema, strict mode).
# Built manually (rather than via TriageExtraction.model_json_schema()) to guarantee it
# satisfies the strict-mode constraints OpenAI enforces (additionalProperties: false
# everywhere, every property required).
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": [
                "Bug Report",
                "Feature Request",
                "Billing Issue",
                "Technical Question",
                "Incident/Outage",
            ],
        },
        "priority": {
            "type": "string",
            "enum": ["Low", "Medium", "High"],
        },
        "confidence": {
            "type": "number",
            "description": "Self-assessed classification confidence, between 0 and 1.",
        },
        "core_issue": {"type": "string"},
        "identifiers": {
            "type": "array",
            "items": {"type": "string"},
        },
        "urgency_signal": {"type": "string"},
        "summary": {"type": "string"},
    },
    "required": [
        "category",
        "priority",
        "confidence",
        "core_issue",
        "identifiers",
        "urgency_signal",
        "summary",
    ],
    "additionalProperties": False,
}
