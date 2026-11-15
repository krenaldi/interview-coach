"""Load the question bank and rubric, and read/write results.

All disk access lives here, so the rest of the app never touches JSON files
directly. If storage ever moved to a database, this is the only file to change.
"""
from __future__ import annotations

import json

from .config import DATA_DIR
from .models import ProgressResponse, Question


def load_rounds() -> list[str]:
    """Return the available round types, derived from the question bank."""
    questions = load_questions()
    # dict.fromkeys keeps first-seen order and drops duplicates.
    return list(dict.fromkeys(q.round for q in questions))


def load_questions(round: str | None = None) -> list[Question]:
    """Load all questions, optionally filtered to a single round."""
    raw = json.loads((DATA_DIR / "questions.json").read_text(encoding="utf-8"))
    questions = [Question(**item) for item in raw]
    if round is not None:
        questions = [q for q in questions if q.round == round]
    return questions


def load_rubric() -> str:
    """Return the scoring rubric as markdown text."""
    return (DATA_DIR / "rubric.md").read_text(encoding="utf-8")


def load_results() -> list[dict]:
    """Return all scored results from data/results.json."""
    path = DATA_DIR / "results.json"
    return json.loads(path.read_text(encoding="utf-8"))


def compute_progress() -> ProgressResponse:
    """Aggregate all scored results into a progress summary."""
    results = load_results()
    total_attempts = len(results)
    rounds_practised = len({r["round"] for r in results})
    average_score = round(sum(r["total"] for r in results) / total_attempts, 1) if results else 0.0
    return ProgressResponse(
        rounds_practised=rounds_practised,
        total_attempts=total_attempts,
        average_score=average_score,
        max_possible=20,
    )


def save_result(record: dict) -> None:
    """Append one scored result to data/results.json."""
    path = DATA_DIR / "results.json"
    results = json.loads(path.read_text(encoding="utf-8"))
    results.append(record)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
