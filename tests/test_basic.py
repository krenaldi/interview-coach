"""Basic tests.  Run:  pytest -q

These cover the endpoints that already work in the seed. In Module 3 (test)
you'll ADD adversarial tests for /score that reveal the compute_total() bug.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.models import CategoryScore
from app.scoring import compute_total

client = TestClient(app)


def test_rounds_not_empty() -> None:
    resp = client.get("/rounds")
    assert resp.status_code == 200
    assert "decomposition" in resp.json()


def test_questions_for_round() -> None:
    resp = client.get("/questions", params={"round": "decomposition"})
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_questions_unknown_round_returns_404() -> None:
    resp = client.get("/questions", params={"round": "does-not-exist"})
    assert resp.status_code == 404


def test_compute_total_sums_all_categories() -> None:
    categories = [
        CategoryScore(name=name, score=3, feedback="ok")
        for name in [
            "Clarifying questions", "Decomposition", "Risk identification", "Communication"
        ]
    ]
    assert compute_total(categories) == 12


def test_progress_empty() -> None:
    resp = client.get("/progress")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_attempts"] == 0
    assert body["average_score"] == 0.0


def test_progress_with_results(monkeypatch) -> None:
    from app import data

    fake = [
        {"round": "decomposition", "total": 10, "max": 20, "summary": ""},
        {"round": "behavioral", "total": 14, "max": 20, "summary": ""},
    ]
    monkeypatch.setattr(data, "load_results", lambda: fake)
    resp = client.get("/progress")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_attempts"] == 2
    assert body["rounds_practised"] == 2
    assert body["average_score"] == round((10 + 14) / 2, 1)
