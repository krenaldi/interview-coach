"""Unit tests for data.compute_progress() — no disk I/O, no network."""
import pytest

from app import data


def _make_result(round_name: str, total: int) -> dict:
    return {"round": round_name, "total": total, "max": 20, "categories": [], "summary": ""}


def test_empty_results(monkeypatch):
    monkeypatch.setattr(data, "load_results", lambda: [])
    p = data.compute_progress()
    assert p.rounds_practised == 0
    assert p.total_attempts == 0
    assert p.average_score == 0.0
    assert p.max_possible == 20


def test_single_entry(monkeypatch):
    monkeypatch.setattr(data, "load_results", lambda: [_make_result("decomposition", 12)])
    p = data.compute_progress()
    assert p.rounds_practised == 1
    assert p.total_attempts == 1
    assert p.average_score == 12.0


def test_multiple_rounds(monkeypatch):
    results = [
        _make_result("decomposition", 10),
        _make_result("behavioral", 14),
        _make_result("decomposition", 8),
    ]
    monkeypatch.setattr(data, "load_results", lambda: results)
    p = data.compute_progress()
    assert p.rounds_practised == 2
    assert p.total_attempts == 3
    assert p.average_score == round((10 + 14 + 8) / 3, 1)
