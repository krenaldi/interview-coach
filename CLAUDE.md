# CLAUDE.md — FDE Interview Prep Assistant

## What we're building
A FastAPI app that runs mock Forward Deployed Engineer interviews and scores
answers against a rubric. The Swagger UI at `/docs` is the UI — no frontend.
Favour clarity over cleverness: every line should be explainable in an interview.

## Stack
- Python 3.11+, **FastAPI** (served by uvicorn), **Pydantic v2**
- Data: plain **JSON files** in `data/` — no database
- Scoring: an offline **mock** scorer by default; the **OpenAI API** when
  `OPENAI_API_KEY` is set (model is `app/config.MODEL_ID`, currently `gpt-4o-mini`)
- Tests: **pytest** — never call the network in a test; `USE_MOCK` is always
  `True` in the test environment because no key is set

## Project layout

```text
app/
  main.py      # Route handlers — thin, delegates to helpers
  models.py    # Pydantic schemas (Question, ScoreRequest, ScoreResponse, …)
  scoring.py   # Scoring logic — main workshop file
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

## Conventions

- All disk access goes through `app/data.py` — route handlers never open files
- All settings (paths, model id, API key presence) come from `app/config.py`
- Pydantic models live in `app/models.py`; no ad-hoc dicts in route return values
- One constant (`config.MODEL_ID`) controls the OpenAI model — never hardcode it
- Tests use `fastapi.testclient.TestClient`; no `pytest-asyncio` needed

## Guardrails for you, the agent

- Do not add a database — keep storage as plain JSON files in `data/`
- Do not add a frontend — the Swagger `/docs` page is the intended UI
- Do not change the four rubric categories defined in `scoring.RUBRIC_CATEGORIES`
  without also updating `data/rubric.md` — they must stay in sync
- Do not call the OpenAI API (or any network) from inside a test
- Keep the seeded bug in `compute_total()` until the user reaches Module 3 (debug)
- When wiring `/score`, also call `data.save_result()` to persist the response

## How to run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload    # → http://127.0.0.1:8000/docs
pytest -q
```

Copy `.env.example` to `.env` and add `OPENAI_API_KEY=sk-...` to enable the
real scorer. Without it the app runs fine on the offline mock.
