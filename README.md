# FDE Interview Prep Assistant

A FastAPI app that runs mock **Forward Deployed Engineer** interviews and scores answers against a structured rubric. The interactive Swagger UI at `/docs` is the intended interface — no separate frontend needed.

## What it does

- Serves interview questions across four round types: `decomposition`, `behavioral`, `system-design`, and `client-roleplay`
- Accepts a candidate's written answer and returns a scored rubric breakdown (0–20)
- Persists every scored attempt to `data/results.json` for progress tracking
- Scores answers with an offline mock scorer by default; switches to the OpenAI API when `OPENAI_API_KEY` is set

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness check |
| `GET` | `/rounds` | List available round types |
| `GET` | `/questions?round=<round>` | Questions for a specific round |
| `POST` | `/score` | Score a candidate's answer |
| `GET` | `/progress` | Summarize practice history |

## Scoring rubric

Each answer is scored **0–5** across four categories (max total **20**):

| Category | What it measures |
|----------|-----------------|
| Clarifying questions | Did you surface unknowns before solving? |
| Decomposition | Did you break the problem into a scoped, sequenced plan? |
| Risk identification | Did you name the riskiest assumption and how to de-risk it? |
| Communication | Was the answer structured and pitched at the listener? |

**Score guide per category:** `0` = absent · `1–2` = weak · `3` = solid · `4` = strong · `5` = exceptional

## Project layout

```
app/
  main.py      # Route handlers — thin, delegates to helpers
  models.py    # Pydantic schemas (Question, ScoreRequest, ScoreResponse, …)
  scoring.py   # Scoring logic
  data.py      # All disk I/O (questions, rubric, results)
  config.py    # Paths + OPENAI_API_KEY / USE_MOCK / MODEL_ID constants
data/
  questions.json   # 6 questions across 4 rounds
  rubric.md        # 4-category rubric, 0–5 each, max 20
  results.json     # Append-only log of scored answers
resources/         # Candidate-facing study guides (not loaded at runtime)
tests/
  test_basic.py    # Tests for the working endpoints
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload    # → http://127.0.0.1:8000/docs
```

## Enable real AI scoring (optional)

```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-...
```

Without a key the app runs fully offline using the built-in mock scorer.

## Run tests

```bash
pytest -q
```

Tests always use the mock scorer (`USE_MOCK=True`) — no network calls.

## Stack

- **Python 3.11+**, FastAPI, uvicorn
- **Pydantic v2** for request/response validation
- **Plain JSON files** in `data/` — no database
- **OpenAI API** (optional) for AI-powered scoring via `gpt-4o-mini`
