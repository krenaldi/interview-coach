# Plan: GET /progress endpoint

## Context

The user wants a read-only endpoint that summarises practice history stored in
`data/results.json`. The file is currently an empty array `[]`. `/score` is
still a stub and never calls `save_result()`, so the endpoint will return
zeroes until Module 3 wires that up — that's expected and fine.

---

## Files to change, and what changes in each

### 1. `app/models.py`

Add one new response model:

```python
class ProgressResponse(BaseModel):
    rounds_practised: int          # count of distinct round values seen
    total_attempts: int            # total number of scored results
    average_score: float           # mean of result["total"]; 0.0 when empty
    max_possible: int              # e.g. 20 — from the first result, or hardcoded
```

No existing models are touched.

### 2. `app/data.py`

Add a `load_results()` function (mirrors the existing `load_questions` pattern —
read the file, parse JSON, return a plain list):

```python
def load_results() -> list[dict]:
    path = DATA_DIR / "results.json"
    return json.loads(path.read_text(encoding="utf-8"))
```

`save_result()` is left untouched.

### 3. `app/main.py`

Add the route after `/questions`, import `ProgressResponse`:

```python
@app.get("/progress")
def get_progress() -> ProgressResponse:
    results = data.load_results()
    if not results:                          # guard: never divide by zero
        return ProgressResponse(
            rounds_practised=0, total_attempts=0,
            average_score=0.0, max_possible=20,
        )
    rounds = set(r["round"] for r in results)
    totals = [r["total"] for r in results]
    return ProgressResponse(
        rounds_practised=len(rounds),
        total_attempts=len(results),
        average_score=round(sum(totals) / len(totals), 2),
        max_possible=results[0]["max"],
    )
```

The empty-results early return is the **only** place division is performed, so
no additional guard is needed elsewhere in the function.

### 4. `tests/test_basic.py`

Add one test for this endpoint:

- `test_progress_empty` — calls `GET /progress` with `results.json` as `[]`
  (its current state) and asserts the response is 200, `total_attempts == 0`,
  and `average_score == 0.0`. This directly exercises the division-by-zero
  guard without any monkeypatching or fixtures.

---

## Order of changes

1. `app/models.py` — define the shape first so everything else can import it
2. `app/data.py` — add `load_results()`
3. `app/main.py` — add the route (depends on both above)
4. `tests/test_basic.py` — add the test last, once the endpoint exists to test

---

## What could break or is easy to get wrong

| Risk | Detail |
|------|--------|
| Division by zero | `average_score` must guard on empty results before dividing |
| `results.json` missing or malformed | `load_results()` will raise; consider a try/except that returns `[]` |
| `max_possible` hardcoded vs. read from data | Using `results[0]["max"]` assumes every record stores `max`; if the shape differs this KeyErrors |
| `round` field absent from records | Records saved by the future `/score` implementation must include `"round"` — not guaranteed yet |

---

## The single riskiest assumption

**Records in `results.json` will have `"round"`, `"total"`, and `"max"` keys.**

Right now `save_result()` accepts a raw `dict` and the shape is nowhere
specified — it depends on what Module 3 passes in when wiring `/score`. If that
dict uses different key names (e.g. `"score_total"` instead of `"total"`), the
progress endpoint silently errors or KeyErrors at runtime. The safe fix is to
define the record shape as a Pydantic model in `models.py` now, and type
`save_result` to accept it — but that is a scope call for the user to make.

---

## Verification

```bash
pytest -q                              # existing + new tests pass
uvicorn app.main:app --reload
curl http://127.0.0.1:8000/progress   # returns zeroes (results.json is empty)
# Manually append a record to data/results.json, re-call — check the maths
```
