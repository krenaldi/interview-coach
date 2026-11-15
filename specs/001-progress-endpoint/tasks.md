# Tasks: GET /progress

Each task is independently reviewable. Complete them in order — later tasks
build on earlier ones.

---

## T1 — Add `ProgressResponse` to `models.py`

`ProgressResponse` is already defined in `app/models.py`. Verify the four
fields match the spec (`rounds_practised`, `total_attempts`, `average_score`,
`max_possible`) and that `average_score` is typed `float`, not `int`.

**Done when:** `from app.models import ProgressResponse` works and the model
validates a dict with all four fields.

---

## T2 — Add a `compute_progress()` helper to `data.py`

```python
def compute_progress() -> ProgressResponse:
```

Calls `load_results()` internally. Logic:
- `total_attempts` = `len(results)`
- `rounds_practised` = count of distinct `round` values across entries
- `average_score` = `round(mean(r["total"] for r in results), 1)` — `0.0` when
  the list is empty (no division by zero)
- `max_possible` = `20`

No route wiring here — pure data logic, nothing imported from `main.py`.

**Done when:** unit tests pass for the happy path and the empty-list case
without starting the app.

---

## T3 — Write tests for `compute_progress()`

File: `tests/test_progress.py`

| Test | Input | Expected |
|---|---|---|
| empty results | `[]` | `rounds_practised=0, total_attempts=0, average_score=0.0` |
| single entry | one result with `total=12, round="decomposition"` | `rounds_practised=1, total_attempts=1, average_score=12.0` |
| multiple rounds | three entries across two rounds, mixed totals | correct distinct-round count and correct mean |

Patch `data.load_results` with `monkeypatch` — no disk I/O in tests.

**Done when:** `pytest tests/test_progress.py -q` passes with no network calls.

---

## T4 — Wire `GET /progress` in `main.py`

```python
@app.get("/progress", response_model=ProgressResponse)
def get_progress() -> ProgressResponse:
    return data.compute_progress()
```

Handler is one line. Import only what is already in scope.

**Done when:** `GET /progress` appears in `/docs` and returns the correct shape.

---

## T5 — Integration test via `TestClient`

Add to `tests/test_basic.py` (or a new file):

- `GET /progress` on an empty store → HTTP 200, `total_attempts == 0`
- `GET /progress` after monkeypatching `load_results` with two entries →
  correct `average_score`

**Done when:** full test suite (`pytest -q`) stays green.
