# Spec: GET /progress

## Why
The app has no way to surface practice history to a candidate. `/progress`
closes that gap: one call returns everything needed to show improvement over
time without the caller having to parse `results.json` themselves.

## What it returns

```json
{
  "rounds_practised": 3,
  "total_attempts": 3,
  "average_score": 11.3,
  "max_possible": 20
}
```

Pydantic model: `models.ProgressResponse` (already defined).

| Field | Type | Description |
|---|---|---|
| `rounds_practised` | `int` | Count of distinct `round` values seen across all results |
| `total_attempts` | `int` | Total number of scored entries in `results.json` |
| `average_score` | `float` | Mean of all `total` fields, rounded to one decimal place |
| `max_possible` | `int` | Always `20` (four categories × 5) |

## What it reads

Calls `data.load_results()` — the only source of truth. The route handler must
not open files directly.

## Acceptance criteria

1. **Happy path** — with N ≥ 1 entries in `results.json`, all four fields are
   present and arithmetically correct.
2. **Empty case** — when `results.json` is `[]`, the endpoint returns HTTP 200
   with `rounds_practised: 0`, `total_attempts: 0`, `average_score: 0.0`,
   `max_possible: 20`. It does **not** return 404 or raise an exception.
3. **Route** — registered as `GET /progress`; visible in Swagger at `/docs`.
4. **No side effects** — read-only; it never writes to `results.json`.

## Out of scope

- Per-round breakdown (e.g. average score by round type)
- Trend data or time-series history
- Pagination or filtering
- Writing or clearing results
