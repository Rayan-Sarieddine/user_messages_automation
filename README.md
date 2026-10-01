# ArcVault Intake & Triage

Three pieces:

- **`ai/`** — `arcvault_ai`, a standalone Python package. One OpenAI structured-output
  call does classification + enrichment together; a separate deterministic module
  decides routing queue + escalation. Everything is Pydantic-validated.
- **`backend/`** — FastAPI service. `POST /api/triage` calls `arcvault_ai.run_triage`,
  persists the validated record to `backend/data/records.json`, and returns it.
  `GET /api/records` lists everything stored so far.
- **`frontend/`** — Next.js form (React Hook Form + TanStack Query) that posts to the
  backend and renders the classification, routing, escalation flag, and summary.

## Run it

```bash
# 1. ai + backend (one venv, installed from backend/ so the relative -e ../ai resolves)
python3 -m venv .venv && source .venv/bin/activate
cd backend && pip install -r requirements.txt && cd ..

# 2. OpenAI key lives only in ai/.env (OPENAI_API_KEY=...)

# 3. start the API
cd backend && uvicorn app.main:app --reload --port 8000

# 4. frontend, in another terminal
cd frontend && pnpm install && pnpm dev
# open http://localhost:3000
```

To run the 5 assessment sample messages directly through the pipeline and dump a
JSON file of the resulting records:

```bash
source .venv/bin/activate
cd ai && python run_samples.py   # writes ai/output.json
```

## Design notes

- **One LLM call**: `arcvault_ai/classifier.py` sends a single `chat.completions.create`
  call with `response_format={"type": "json_schema", "strict": True}` so category,
  priority, confidence, core issue, identifiers, urgency signal, and summary all come
  back in one structured payload — no second call for enrichment.
- **Routing/escalation are plain Python, not the LLM**: `arcvault_ai/routing.py` maps
  category → queue (Engineering / Billing / Product / IT-Security) and separately
  checks confidence < 0.70, outage keywords, and billing discrepancies > $500 to
  force a record into the `Escalation` queue. Keeping this deterministic makes it
  auditable and cheap to tune without touching prompts.
- **Validation boundary**: the LLM's JSON is parsed into `TriageExtraction` (Pydantic);
  only after that succeeds does the pipeline build the final `TriageRecord`, which the
  backend persists. A malformed LLM response surfaces as a 502, not a bad record on disk.
